# Passphrase developers guide

[![Ballmer "developers!"](https://passh.hackan.net/img/developers.png)](http://www.youtube.com/watch?v=V-FkalybggA "Developers")

This guide is intended for developers that want to implement **Passphrase** in their projects or that want to contribute to this project.

## Contributing

If you want to develope or contribute to this project, you can quickly start by issuing `make devenvironment`: it creates a virtualenv directory and installs requirements and the *Passphrase* package. This is, of course, not mandatory.

Every contribution must be acompanied by it's tests. As a general guideline, follow PEP8 (flake8 must run without warnings) and prefer Exceptions over assumptions. Try hard on not to add dependencies: I'm going to reject PRs with external dependencies that are not entirely justified (and for this project in particular, having 0 dependencies is very important).

Not sure on what to contribute with? Here you go:

* Solve opened issues.
* Review PRs.
* Add support for unsupported OSes.
* Improve code quality or provide code reviews.
* Improve current tests or add new ones.

## About the package

**Passphrase** modules were written with usability and security in mind. Most, if not all, methods and functions will severily restrict the data type it can process; this is to avoid unexpected issues. The library always prefers to fail (raise exception) instead of doing something wrong, so when in doubt during implementation, i.e. when using parameters from the user, use a `try-except` block.

In regard of using parameters from the user inside an app, there's no `system()` call nor similar, neither a DB access so it's perfectly safe. The library always checks for correct data types and values. However, bare in mind that a **DoS is possible** if a ridiculously huge number is ussed for passphrase or password length! Upper limits in amounts and legths are never forced, so *be careful*: restrict that in your app by testing first which values are sane. A tip from the hat: a passphrase bigger than 20 words & numbers, or a password longer than 50 chars, is rather strange.

On the security side, if you are implementing this in an app that's used by a ton of users, be careful regarding the amount of entropy in your system! Repeated unpaused calls to the OS's random source to extract data can have a negative impact on the system's entropy thus causing generated values to have poor quality and be insecure. A way to avoid this is by implementing `sleep`s in your code, using a random duration:

```python
def pause_sec(min, max) -> int:
    # This method is cryptographically insecure!
    from time import time

    seed = time() - float(str(time()).split('.')[0])
    return int(seed * (max - min) + min)

...

my_async_sleep(pause_sec(1, 5))
```

Of course, you can't just pause the whole server, or let the user hanging there for some seconds... or maybe, you can. I let you decide how to solve it. Another, even better, way to solve this is to provide the system for a secure external random source, such as a randomness generator like Chaoskey.

If you are using a Linux OS, you can use `Aux::system_entropy()` to determine how much entropy does your system have prior making a request for random data (**Passphrase** does this when runs as a script). You should always have more than 128 bits or the call to `os.urandom()` might hang or fail.

### Requirements

* **Python 3.5+**.
* [Flake8](http://flake8.pycqa.org/en/latest/) [optional] for linting.
* [Nose](https://nose.readthedocs.io/en/latest/) [optional] for collecting and running tests.
* [Coverage](https://bitbucket.org/ned/coveragepy) [optional] for coverage check with Nose.

## Linting

Run `make lint` or `flake8 .`.

## Testing

Run `make test` or `nosetests -v`. Remove the `-v` if you don't want a verbose output. Before running tests, it's recommended to check for syntax errors and similar by linting first. Also, `make coverage` is available to check for tests coverage.

## How to use it as a package

Download the files, preferrably fom the [latest release](https://github.com/HacKanCuBa/passphrase-py/releases/latest) - releases are always signed -. Once downloaded and verified, use `setup.py` to install (I let you decide whether to use virtualenv or not): `./setup.py install`. You can also do `make package-install` with the same outcome. Run it with `sudo` or elevated privileges to install it system-wide.  
Using *pip* for installation is not recommended given that it's very insecure. But if you insist, just do `pip install hc-passphrase`.  
To uninstall, run `make package-uninstall` or `pip uninstall hc-passphrase`.  

Please let me know if you use this in your app, I would love that :)

### Examples of use

A good example is how [I implemented it](passphrase/__main__.py).

```python
>>> from passphrase.passphrase import Passphrase
>>> passphrase = Passphrase('/tmp/mi_own_wordlist.txt')
>>> 
>>> # WARNING: entropy and good default values ARE NOT automatically calculated!
>>> # If amounts are not specified, an exception occurs.
>>> passphrase.generate()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/hackan/Workspace/passphrase/passphrase/passphrase/passphrase.py", line 345, in generate
    raise ValueError('Can\'t generate passphrase: '
ValueError: Can't generate passphrase: wordlist is empty or amount_n or amount_w isn't set
>>> passphrase.amount_w = 6
>>> passphrase.amount_n = 0
>>> passphrase.generate()
['shop', 'jolt', 'spoof', 'cupid', 'pouch', 'dose']
>>> 
>>> # You must set the desired entropy prior executing any calculation, or else...
>>> passphrase.words_amount_needed()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/hackan/Workspace/passphrase/passphrase/passphrase/passphrase.py", line 314, in words_amount_needed
    raise ValueError('Cant\' calculate the words amount needed: '
ValueError: Cant' calculate the words amount needed: entropy_bits_req or amount_n isn't set
>>> passphrase.entropy_bits_req = 77
>>> passphrase.words_amount_needed()
8
>>> 
>>> passphrase.amount_w = passphrase.words_amount_needed()
>>> passphrase.generate()
['grub', 'mummy', 'woozy', 'whole', 'ritzy', 'sift', 'train', 'radar']
>>> 
>>> # Change the wordlist (note than no other parameter is changed!)
>>> passphrase.import_words_from_file('/tmp/some_other_wordlist.txt', False)
>>> passphrase.generate()
['vexingly', 'skedaddle', 'gilled', 'desolate', 'cartoon', 'frail', 'brute', 'filled']
```

```python
# In a system backend, propose the user a good random passphrase for him to
# use, or a safe password.

def generate_passphrase() -> str:
    from passphrase.passphrase import Passphrase
    # Use internal wordlist (if it doesn't exists, an exception raises)
    passphrase = Passphrase('internal')
    passphrase.entropy_bits_req = 77    # EFF's minimum recommended
    passphrase.amount_n = 1
    passphrase.amount_w = passphrase.words_amount_needed()
    passphrase.generate()   # This returns a list
    passphrase.separator = '-'  # By default, separator is a blank space!
    # Convert the last result to a string separated by dashes
    proposedPassphrase = str(passphrase)
    return proposedPassphrase

def generate_password() -> str:
    from passphrase.passphrase import Passphrase
    passphrase = Passphrase()
    passphrase.entropy_bits_req = 77    # EFF's minimum recommended
    passphrase.passwordlen = passphrase.password_length_needed()
    passphrase.generate_password()   # This returns a list
    passphrase.separator = ''   # By default, separator is a blank space!
    # Convert the last result to a string
    proposedPassword = str(passphrase)
    return proposedPassword
```

#### Docker

To securely use it in a Dockerfile, do:

```
ENV PASSPHRASE_VERSION 1.0.0

RUN gpg --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys 0x35710D312FDE468B
RUN wget -O /tmp/passphrase-v${PASSPHRASE_VERSION}.tar.gz https://github.com/HacKanCuBa/passphrase-py/archive/v${PASSPHRASE_VERSION}.tar.gz
RUN wget -O /tmp/passphrase-v${PASSPHRASE_VERSION}.tar.gz.sig https://github.com/HacKanCuBa/passphrase-py/releases/download/v1.0.0rc1/passphrase-v${PASSPHRASE_VERSION}.tar.gz.sig
RUN gpg --trust-model always --verify /tmp/passphrase-v${PASSPHRASE_VERSION}.tar.gz.sig /tmp/passphrase-v${PASSPHRASE_VERSION}.tar.gz \
    && cd /tmp \
    && tar -xf passphrase-v${PASSPHRASE_VERSION}.tar.gz \
    && cd passphrase-py-${PASSPHRASE_VERSION} \
    && make package-install
```

It doesn't matter which OS is the base, as long as it has GnuPG package installed (either versions 1.4+ or 2+).

You can also just `pip install hc-passphrase` but, again, it's insecure. Yeah, I know: it's a single line vs. all that... If only *pip* used some crypto...

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
