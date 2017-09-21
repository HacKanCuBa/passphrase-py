# Passphrase

**Passphrase** is a tool to generate **cryptographically secure** passphrases and passwords.

For **Python 3.2+**, it's currently based on the security of [LibNaCl's](https://github.com/saltstack/libnacl) [randombytes_uniform](https://download.libsodium.org/doc/generating_random_data/#usage), both passphrases and passwords are securelly generated using `libnacl.randombytes_uniform()`.

For **Python 3.6+**, it's currently based on the security of Python's [Lib/secrets](https://docs.python.org/3/library/secrets.html#module-secrets), both passphrases and passwords are securelly generated using `secrets.choice()` and `secrets.randbelow()`:

> The `secrets` module is used for generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets.

It also makes use of the [EFF Large Wordlist](https://www.eff.org/es/document/passphrase-wordlists) as words reference for passphrases.

A secure passphrase must be of at least 5 words, but 7 is better, and maybe you can add a random number to the list. If you need a password, make it bigger than 8 characters (NIST's latest recommendation), and preffer more than 12 (I recommend 16 or more). Passwords are comprised of digits, upper and lower case letters and punctuation symbols - more specifically: `ascii_letters`, `digits` and `punctuation` from [Lib/string](https://docs.python.org/3.6/library/string.html#string-constants) -.

## Requirements

For **Python 3.6+**:

* flake8 [optional] for linting

For **Python 3.2+**:

* LibNaCl 1.5+
* flake8 [optional] for linting

[passphrase.py](/src/passphrase.py) is a stand-alone, self contained script (the word list is embedded in it). It detects whether you have Python 3.6+ or lower, and acts accordingly. For Python 3.6+, it uses `Lib/secrets` (and is preferred); for Python 3.2+, `libnacl.randombytes_uniform`.

## How to use it

Just download the script, preferrably fom the [latest release](https://github.com/HacKanCuBa/passphrase-py/releases/latest) - releases are always signed - and give it execution permission. It can be run as `:~$ python3.6 src/passphrase.py`, or if you copy it to /usr/local/bin (system-wide availability) or ~/.local/bin (user-wide availability), as `:~$ passphrase`.

You can use `make install` to install it system-wide (requires root or `sudo`) or `make altinstall` for user-wide. Installing it simply copies the script to destination along with the man page.

To install requirements, use pip: `pip3 install -r requirements.txt`.

### Examples of use

Check the [man page](man/passphrase.md) for more information.

#### Generate a passphrase of 5 words (default settings)

```
:~$ passphrase
trophy affiliate clobber vivacious aspect
```

#### Generate a passphrase of 6 words and a number (minimum recommended)

```
:~$ passphrase -w 6 -n 1
jasmine identity chemo suave clerk copartner 853727
```

#### Generate a password of 16 characters (minimum recommended)

```
:~$ passphrase -p 16
E`31nDL0^$oYu5='
```

#### Use an external wordlist to generate a passphrase

```
:~$ passphrase -i my-wordlist.txt
anguished estate placard deceptive entity
:~$ passphrase -d -i my-dicewarelike-wordlist.txt
unnamed unmanned appendix fineness riverside
```

#### Save the output to a file

```
:~$ passphrase -o pass.txt
:~$ passphrase > pass.txt
```

#### Generate a passphrase and use it with GPG

```
:~$ passphrase -o pass.txt | gpg --symmetric --batch --passphrase-fd 0 somefile.txt
:~$ sha256sum somefile.txt
589ed823e9a84c56feb95ac58e7cf384626b9cbf4fda2a907bc36e103de1bad2  somefile.txt
:~$ cat pass.txt | gpg --decrypt --batch --passphrase-fd 0 somefile.txt.gpg | sha256sum -
gpg: AES256 encrypted data
gpg: encrypted with 1 passphrase
589ed823e9a84c56feb95ac58e7cf384626b9cbf4fda2a907bc36e103de1bad2  -
```

#### Generate a passphrase avoiding [shoulder surfing](https://en.wikipedia.org/wiki/Shoulder_surfing_(computer_security))

```
:~$ passphrase -q -o pass.txt
```

## License

**Passphrase** is made by [HacKan](https://hackan.net) under GNU GPL v3.0+. You are free to use, share, modify and share modifications under the terms of that [license](LICENSE).

    Copyright (C) 2017 HacKan (https://hackan.net)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
