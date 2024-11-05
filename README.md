# werkzeug2hashcat
This repository contains a script to convert hashes created by `werkzeug.security.generate_password_hash` function with `method="pbkdf2:sha256"` to a format that is readable by hashcat.

More details can be found on [werkzeug wiki](https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security).

# Usage
This script only uses native python3 libraries, thus no need for additional installation.
```
~/pentest/werkzeug2hashcat ☿ python3 werkzeug2hashcat.py -h
usage: werkzeug2hashcat.py [-h] [-s HASH] [-l HASHLIST]

Process PBKDF2 hash(es) from input and convert to applicable hashcat format.

options:
  -h, --help            show this help message and exit
  -s HASH, --hash HASH  Single PBKDF2 Werkzeug hash to process.
  -l HASHLIST, --hashlist HASHLIST
                        File containing PBKDF2 Werkzeug hashes to process, one per line.
```

## Converting Single Hash
```bash
~/pentest/werkzeug2hashcat ☿ python3 werkzeug2hashcat.py -s 'pbkdf2:sha256:600000$I5bFyb0ZzD69pNX8$e9e4ea5c280e0766612295ab9bff32e5fa1de8f6cbb6586fab7ab7bc762bd978'
sha256:600000:STViRnliMFp6RDY5cE5YOA==:6eTqXCgOB2ZhIpWrm/8y5fod6PbLtlhvq3q3vHYr2Xg=
You can now crack this hash using, hashcat -m 10900 sha256:600000:STViRnliMFp6RDY5cE5YOA==:6eTqXCgOB2ZhIpWrm/8y5fod6PbLtlhvq3q3vHYr2Xg= /usr/share/wordlists/rockyou.txt
```

## Converting Multiple Hashes from File
```bash
~/pentest/werkzeug2hashcat ☿ python3 werkzeug2hashcat.py -l examples/examplehashes.txt
sha256:600000:STViRnliMFp6RDY5cE5YOA==:6eTqXCgOB2ZhIpWrm/8y5fod6PbLtlhvq3q3vHYr2Xg=
sha256:600000:WW5SZ2puaW0=:yVQajGrUC8Bkl5vERgJQQf+smvL3YnJpcdiignLFUO0=
You can now crack this hashes using: hashcat -m 10900 werkzeug_converted_hashcat.hash /usr/share/wordlists/rockyou.txt
```

# Acknowledgments
This code is based by the discussion [here](https://github.com/hashcat/hashcat/issues/3205) and code snippet supplied by [this](https://github.com/tititototutu) user.
