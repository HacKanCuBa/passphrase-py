# Passphrase

**Passphrase** is a tool to generate **cryptographically secure** passphrases and passwords.

Its security is based on Python's [os.urandom](https://docs.python.org/3/library/os.html#os.urandom) to get cryptographically secure random bits to make an integer number.

It also makes use of the [EFF's Large Wordlist](https://www.eff.org/es/document/passphrase-wordlists) as words reference for passphrases.

A secure passphrase must be of at least 6 words, but 7 is better, and maybe you can add a random number to the list. If you need a password, make it bigger than 8 characters (NIST's latest recommendation), and preffer more than 12 (I recommend 16 or more). Passwords are comprised of digits, upper and lower case letters and punctuation symbols - more specifically: `ascii_letters`, `digits` and `punctuation` from [Lib/string](https://docs.python.org/3.6/library/string.html#string-constants) -.

Those settings mentioned are speciffically for the EFF's Large Wordlist. If you specify a different wordlist, the minimum amount of words for a passphrase to be secure changes: for shorter lists, the amount increases. The minimum secure amount of words (for a passphrase) or characters (for a password) are calculated by **Passphrase** and a warning is shown if the chosen number is too low.

## Requirements

* **Python 3.2+**
* NumPy 1.13+ [optional] for faster entropy computation
* Flake8 [optional] for linting

[passphrase.py](/src/passphrase.py) is a stand-alone, self contained script (the word list is embedded in it). It gets plenty of benefits from NumPy if you use external wordlists, because it computes the entropy of it, but it works fine without it. For the embedded one, it makes no difference.

## How to use it

Just download the script, preferrably fom the [latest release](https://github.com/HacKanCuBa/passphrase-py/releases/latest) - releases are always signed - and give it execution permission. It can be run as `:~$ python3.6 src/passphrase.py`, or if you copy it to /usr/local/bin (system-wide availability) or ~/.local/bin (user-wide availability), as `:~$ passphrase`.

You can use `make install` to install it system-wide (requires root or `sudo`) or `make altinstall` for user-wide. Installing it simply copies the script to destination directory, along with the man page.

To install requirements, use pip: `pip3 install -r requirements.txt`.

### Examples of use

Check the [man page](man/passphrase.md) for more information.

#### Generate a passphrase of 6 words (default settings)

```
:~$ passphrase
trophy affiliate clobber vivacious aspect thickness
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
:~$ passphrase -i eff_short_wordlist_1_1column.txt
wimp broke dash pasta zebra viral outer clasp
:~$ passphrase -d -i eff_short_wordlist_1.txt 
mouse trend coach stain shut rhyme baggy scale
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

## Is this really secure?

First of all, we will say that a password or passphrase generator algorithm is secure if its output is *trully* random. To achieve that, **Passphrase** relies entirely on `os.urandom`. The whole program is quite big, but most of it is just the menues and the word list. The generator algorithms are very short and simple:

```python
def getrandbits(k: int) -> int:
    """getrandbits(k) -> x.  Generates an int with k random bits."""
    # https://github.com/python/cpython/blob/3.6/Lib/random.py#L676
    if k <= 0:
        raise ValueError('number of bits must be greater than zero')
    if k != int(k):
        raise TypeError('number of bits should be an integer')
    numbytes = (k + 7) // 8                       # bits / 8 and rounded up
    x = int.from_bytes(_urandom(numbytes), 'big')
    return x >> (numbytes * 8 - k)                # trim excess bits


def randbelow(n: int) -> int:
    """Return a random int in the range [0,n).  Raises ValueError if n==0."""
    # https://github.com/python/cpython/blob/3.6/Lib/random.py#L223
    k = n.bit_length()  # don't use (n-1) here because n can be 1
    r = getrandbits(k)  # 0 <= r < 2**k
    while r >= n:
        r = getrandbits(k)
    return r


def generate(wordlist: list, amount_w: int, amount_n: int) -> list:
    passphrase = []
    for i in range(0, amount_w):
        index = randbelow(len(wordlist))
        passphrase.append(wordlist[index])

    for i in range(0, amount_n):
        num = randbelow(MAX_NUM - MIN_NUM + 1) + MIN_NUM
        passphrase.append(num)

    return passphrase


def generate_password(length: int) -> list:
    characters = list(digits + ascii_letters + punctuation)
    passwd = generate(characters, length + 1, 0)
    return passwd
```

The whole magic is done by `randbelow()`, that returns a random natural number lower than the given value, that is then used as index for the word or character list. `randbelow()` uses `getrandbits()` which in turn uses `os.urandom` at the back. `os.urandom` always provides an interface to the OS's cryptographically secure random generator. And both `randbelow()` and `getrandbits()` where copyied from Python's Lib/random, but trimmed down so that they don't allow anything fishy. This also makes **Passphrase** independent from unnecessary libraries and potential vulnerabilities.

The algorithms are very straight forward, easy to understand and verify. *Boring crypto is the best crypto*.

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
