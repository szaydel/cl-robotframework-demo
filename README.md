# cl-robotframework-demo
A simple demo setup for my colleagues. This repo is not likely to be useful to anyone else.
```
$ robot -b debug.log atest/bundler.robot
==============================================================================
Bundler :: A demo suite focused on the provision bundle functionality. It e...
==============================================================================
Exporter SSH Key is encrypted :: We expect that the private key fo... | PASS |
------------------------------------------------------------------------------
Host SSH Keys are encrypted :: We expect that the host (sensor) pr... | PASS |
------------------------------------------------------------------------------
ECDSA Host SSH Key uses secp256r curve :: We expect that the host ... | PASS |
------------------------------------------------------------------------------
RSA Host SSH Key is not less than 3072 bytes :: We expect that the... | PASS |
------------------------------------------------------------------------------
Validate Cert Hygiene expiring certificate configuration :: Valida... | PASS |
------------------------------------------------------------------------------
Validate SFTP file export configuration :: Validate that previousl... | PASS |
------------------------------------------------------------------------------
Validate SFTP file export configuration invalid path :: Validate t... | FAIL |
UnexpectedConfiguration: Expected bro.export.sftp.file.path to be /c/b/a; actual value is /a/b/c
------------------------------------------------------------------------------
Validate SFTP file export configuration invalid server port :: Val... | FAIL |
UnexpectedConfiguration: Expected bro.export.sftp.file.server to be server=127.0.0.1:1234; actual value is 127.0.0.1:9876
------------------------------------------------------------------------------
Validate SFTP file export configuration invalid user :: Validate t... | FAIL |
UnexpectedConfiguration: Expected bro.export.sftp.file.user to be cba; actual value is abc
------------------------------------------------------------------------------
Removing backup bundle bundle1.json
Bundler :: A demo suite focused on the provision bundle functional... | FAIL |
9 critical tests, 6 passed, 3 failed
9 tests total, 6 passed, 3 failed
==============================================================================
Debug:   /home/broala/robotf/debug.log
Output:  /home/broala/robotf/output.xml
Log:     /home/broala/robotf/log.html
Report:  /home/broala/robotf/report.html
```
