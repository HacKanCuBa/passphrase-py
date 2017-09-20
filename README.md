# Passphrase

**Passphrase** is a tool to generate **cryptographically secure** passphrases and passwords. It's currently based on the security of Python's [Lib/secrets](https://docs.python.org/3/library/secrets.html#module-secrets), both passphrases and passwords are securelly generated using `secrets.choice()`:

> The `secrets` module is used for generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets.

It also makes use of the [EFF Large Wordlist](https://www.eff.org/es/document/passphrase-wordlists) as words reference for passphrases.

A secure passphrase must be of at least 5 words. 7 is better, and maybe you can add a random number to the list. If you need a password, make it bigger than 12 characters, and preffer more than 16. Passwords are comprised of digits, upper and lower case letters and punctuation symbols - more specifically: `ascii_letters`, `digits` and `punctuation` from [Lib/string](https://docs.python.org/3.6/library/string.html#string-constants) -.

## Requirements

* Python 3.6
* flake8 [optional] for linting

[passphrase.py](/src/passphrase.py) is a stand-alone, self contained (the word list is embedded in it) script, and has no requirements besides Python 3.6 (because the `secrets` module is present since that Python version). I'm planning to implement PyNaCl so it can be used with Python 3.x.

## How to use it

Just download the script, preferrably fom the [latest release](/releases/latest) - releases are always signed - and give it execution permission. It can be run as `:~$ python3.6 src/passphrase.py`, or if you copy it to /usr/local/bin (system-wide availability) or ~/.local/bin (user-wide availability), as `:~$ passphrase`.

Check the [man page](man/passphrase.md) for more information.

### Examples of use

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
:~$ passphrase -p -w 16
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

