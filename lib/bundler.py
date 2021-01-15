import json
import requests
from json import JSONDecodeError

from pathlib import Path
from typing import Dict


from cryptography.hazmat.primitives.serialization import load_ssh_public_key
from robot.api import logger


class KeyNotEncryptedError(Exception):
    pass


class InvalidNamespaceError(Exception):
    pass


class SSHKeyInvalid(Exception):
    pass


class BundleDownloadError(Exception):
    pass


class UnexpectedConfiguration(Exception):
    pass


class BundlerLibrary:
    backup_bundle: Dict = {}
    OUTPUT = "bundle1.json"
    BASE_URL = "http://localhost/api/provision/bundle"
    BUNDLE_PWD = "1234"
    NO_SENSITIVE = "0"

    def prepare_system_backup_bundle(self):
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json",
        }
        params = {
            "bundle-password": self.BUNDLE_PWD,
            "no-sensitive": self.NO_SENSITIVE,
            "type": "backup",
        }
        resp = requests.get(self.BASE_URL, params=params, headers=headers)
        resp.raise_for_status()

        if not resp.content:
            errmsg = "Received no content from the sensor"
            logger.console(errmsg, newline=True, stream="stderr")
            raise BundleDownloadError(errmsg)
        try:
            self.backup_bundle: Dict = resp.json()
        except JSONDecodeError as e:
            raise BundleDownloadError(e.msg)

        with open(self.OUTPUT, "wb") as f:
            f.write(resp.content)
        logger.info(f"Retrieved backup bundle {self.OUTPUT} in {resp.elapsed} seconds")
        return resp.status_code

    def _load_bundle_from_file(self):
        if self.backup_bundle:
            return
        # Robotframework can deal with exceptions gracefully
        with open(self.OUTPUT, "rb") as f:
            self.backup_bundle = json.load(f)

    def _nested_get(self, namespace):
        subset = self.backup_bundle
        levels = namespace.split(".")
        for k in levels:
            try:
                subset = subset[k]
            except KeyError:
                raise InvalidNamespaceError(f"{namespace} does not exist in bundle")
        return subset

    def exporter_keys_are_encrypted(self):
        self._load_bundle_from_file()
        namespace = "keys.exporter.private"
        private_key = self._nested_get(namespace)
        if not private_key.startswith("**encrypted**"):
            raise KeyNotEncryptedError(f"Exporter key in {namespace} must be encrypted")
        return True

    def host_keys_are_encrypted(self):
        self._load_bundle_from_file()
        namespaces = (
            "keys.host.dsa.private",
            "keys.host.ecdsa.private",
            "keys.host.ed25519.private",
            "keys.host.rsa.private",
        )
        for namespace in namespaces:
            private_key = self._nested_get(namespace)
            if not private_key.startswith("**encrypted**"):
                raise KeyNotEncryptedError(f"Host key in {namespace} must be encrypted")
        return True

    def ecdsa_host_key_uses_secp256r1_curve(self):
        self._load_bundle_from_file()
        pk_namespace = self._nested_get("keys.host.ecdsa.public")
        pubkey = load_ssh_public_key(bytes(pk_namespace, "utf-8"))
        curve = pubkey.curve.name
        if curve != "secp256r1":
            raise SSHKeyInvalid(f"Expected secp256r1 curve; got {curve} instead")
        return True

    def rsa_host_key_length_is_at_least_3072_bytes(self):
        self._load_bundle_from_file()
        pk_namespace = self._nested_get("keys.host.rsa.public")
        pubkey = load_ssh_public_key(bytes(pk_namespace, "utf-8"))
        if pubkey.key_size < 3072:
            raise SSHKeyInvalid(
                f"Expected rsa key to be at least 3072 bytes; got {pubkey.key_size} instead"
            )
        return True

    def validate_cert_hygiene_expiring_certs_settings(
        self, age: int = 90, enable: bool = False
    ):
        self._load_bundle_from_file()
        age_key = "bro.pkgs.corelight.cert_hygiene.config.expiring_cert_age"
        enable_key = "bro.pkgs.corelight.cert_hygiene.config.expiring_certs.enable"
        actual_age: int = self.backup_bundle["options"][age_key]
        actual_enable: bool = self.backup_bundle["options"][enable_key]
        if age != actual_age:
            raise UnexpectedConfiguration(
                f"Expected {age_key} to be {age}; actual value is {actual_age}"
            )
        if enable != actual_enable:
            raise UnexpectedConfiguration(
                f"Expected {enable_key} to be {enable}; actual value is {actual_enable}"
            )
        return True

    def validate_sftp_file_export_settings(
        self, path: str = "/", server: str = "", user: str = ""
    ):
        self._load_bundle_from_file()
        path_key = "bro.export.sftp.file.path"
        server_key = "bro.export.sftp.file.server"
        user_key = "bro.export.sftp.file.user"
        actual_path: str = self.backup_bundle["options"][path_key]
        actual_server: str = self.backup_bundle["options"][server_key]
        actual_user: str = self.backup_bundle["options"][user_key]
        if path != actual_path:
            raise UnexpectedConfiguration(
                f"Expected {path_key} to be {path}; actual value is {actual_path}"
            )
        if server != actual_server:
            raise UnexpectedConfiguration(
                f"Expected {server_key} to be {server}; actual value is {actual_server}"
            )
        if user != actual_user:
            raise UnexpectedConfiguration(
                f"Expected {user_key} to be {user}; actual value is {actual_user}"
            )
        return True

    def remove_backup_bundle_file(self):
        if Path(self.OUTPUT).exists():
            logger.console(f"Removing backup bundle {self.OUTPUT}")
            Path(self.OUTPUT).unlink()


if __name__ == "__main__":
    bl = BundlerLibrary()
    bl.prepare_system_backup_bundle()
    bl.exporter_keys_are_encrypted()
    bl.host_keys_are_encrypted()
    bl.ecdsa_host_key_uses_secp256r1_curve()
    bl.rsa_host_key_length_is_at_least_3072_bytes()
    bl.validate_cert_hygiene_expiring_certs_settings()
