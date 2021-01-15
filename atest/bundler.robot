| *** Settings ***
| Documentation     | A demo suite focused on the provision bundle functionality.
| ...               | It exercises the provision bundle some and attempts to
| ...               | validate a few aspects of the data from the retrieved bundle.
|                   |
| Suite Setup       | Prepare System Backup Bundle
| Suite Teardown    | Remove Backup Bundle File

| Library           | OperatingSystem
| Library           | lib.bundler.BundlerLibrary
|
| *** Keywords ***
| ConsLog
| | ${var} =        | Set Variable | This is my Variable
| | Log to Console  | This is the variable I promised you: "${var}"
|
| *** Test Cases ***
| Exporter SSH Key is encrypted
| | [Documentation] | We expect that the private key for SFTP exporter is not going to be
| | ...             | presented in the clear in the bundle. The public keys are never
| | ...             | considered sensitive, since their whole purpose is to be public.
| |                 |
| | ${result}=      | Exporter Keys Are Encrypted
| | Should Be Equal | ${result} | ${TRUE}
|
| Host SSH Keys are encrypted
| | [Documentation] | We expect that the host (sensor) private keys are not going to be
| | ...             | presented in the clear in the bundle. The public keys are never
| | ...             | considered sensitive, since their whole purpose is to be public.
| |                 |
| | ${result}=      | Host Keys Are Encrypted
| | Should Be Equal | ${result} | ${TRUE}
|
| ECDSA Host SSH Key uses secp256r curve
| | [Documentation] | We expect that the host (sensor) ECDSA key will be using NIST
| | ...             |  secp256r elliptic curve.
| |                 |
| | ${result}=      | ECDSA Host Key Uses secp256r1 Curve
| | Should Be Equal | ${result} | ${TRUE}
|
| RSA Host SSH Key is not less than 3072 bytes
| | [Documentation] | We expect that the host (sensor) RSA key will be either 3072 or 4096.
| | ...             | Anything smaller than this is considered to be insecure at this point.
| |                 |
| | ${result}=      | RSA Host Key Length Is At Least 3072 Bytes
| | Should Be Equal | ${result} | ${TRUE}
|
| Validate Cert Hygiene expiring certificate configuration
| | [Documentation] | Validate default settings pertaining to dealing with the expiring certificates.
| | ...             | We are using named arguments here, passing a value. This is an example of 
| | ...             | overriding default parameters with parameters specific to this test.
| | ${result}=      | Validate Cert Hygiene Expiring Certs Settings | age=30 | enable=${TRUE}
| | Should Be Equal | ${result} | ${TRUE}
|
| Validate SFTP file export configuration
| | [Documentation] | Validate that previously set configuration values are persisted and backed-up.
| | ...             | correctly.
| |                 |
| | ${result}=      | Validate SFTP File Export Settings | path=/a/b/c | server=127.0.0.1:9876 | user=abc
| | Should Be Equal | ${result} | ${TRUE}
|
| Validate SFTP file export configuration invalid path
| | [Documentation] | Validate that previously set configuration values are persisted and backed-up.
| | ...             | correctly.
| |                 |
| | ${result}=      | Validate SFTP File Export Settings | path=/c/b/a | server=bar | user=xyz
|
| Validate SFTP file export configuration invalid server port
| | [Documentation] | Validate that previously set configuration values are persisted and backed-up.
| | ...             | correctly.
| |                 |
| | ${result}=      | Validate SFTP File Export Settings | path=/a/b/c | server=server=127.0.0.1:1234 | user=abc
|
| Validate SFTP file export configuration invalid user
| | [Documentation] | Validate that previously set configuration values are persisted and backed-up.
| | ...             | correctly.
| |                 |
| | ${result}=      | Validate SFTP File Export Settings | path=/a/b/c | server=127.0.0.1:9876 | user=cba
|
