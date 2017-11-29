Passphrase
==========

**Passphrase** is a tool to generate **cryptographically secure**
passphrases and passwords. A passphrase is a list of words usually
separated by a blank space. This tool acts like a
`diceware <http://world.std.com/~reinhold/diceware.html>`__ generator
(more info in `EFF's website <https://www.eff.org/es/dice>`__).

Its security is based on Python's
`os.urandom <https://docs.python.org/3/library/os.html#os.urandom>`__ to
get cryptographically secure random bits to make an integer number. It
also makes use of the `EFF's Large
Wordlist <https://www.eff.org/es/document/passphrase-wordlists>`__ as
words reference for passphrases.

A secure passphrase must be of at least 6 words, but 7 is better, and
maybe you can add a random number to the list. If you need a password,
make it bigger than 8 characters (`NIST's latest
recommendation <https://nakedsecurity.sophos.com/2016/08/18/nists-new-password-rules-what-you-need-to-know/>`__),
and prefer more than 12 (I recommend 16 or more). Passwords are
comprised of digits, upper and lowercase letters and punctuation symbols
- more specifically: ``ascii_lowercase``, ``ascii_uppercase``,
``digits`` and ``punctuation`` from
`Lib/string <https://docs.python.org/3.6/library/string.html#string-constants>`__
-.

Those settings mentioned are specifically for the EFF's Large Wordlist.
If you specify a different wordlist, the minimum amount of words for a
passphrase to be secure changes: for shorter lists, the amount
increases. The minimum secure amount of words (for a passphrase) or
characters (for a password) are calculated by **Passphrase** and a
warning is shown if the chosen number is too low (when used as a
script), by calculating the list's entropy.

**Important note**: the quality and security of generated passphrases
rely on:

-  the `OS-specific randomness
   source <https://docs.python.org/3/library/os.html#os.urandom>`__, and
-  the quality of the wordlist.

If you are not sure which wordlist to use, just use the one provided by
**Passphrase** (it is used by default when running as a script) or one
of the EFF's wordlists (check at about the middle of `this blog
post <https://www.eff.org/es/dice>`__).

Requirements
------------

-  **Python 3.2+**.

How to use it
-------------

**Passphrase** can be used as a *package* in other apps, or as a
*stand-alone script*.

In any case, just download the files, preferrably fom the `latest
release <https://github.com/HacKanCuBa/passphrase-py/releases/latest>`__
- releases are always signed -.

As a package
~~~~~~~~~~~~

Check the `developers guide <DEVELOPERS.md>`__.

As a script
~~~~~~~~~~~

Once downloaded and verified, you can install it with
``setup.py install`` but I recommend you do ``make install`` for
system-wide installation or ``make altinstall`` for user-wide
installation, as it will create a single executable zip file plus
install the man page.

Examples of use
^^^^^^^^^^^^^^^

Check the `man page <man/passphrase.md>`__ for more information.

Generate a passphrase of 6 words (default settings)
'''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase
    trophy affiliate clobber vivacious aspect thickness

Generate a passphrase of 128 bits of entropy
''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -e 128
    shorty collie prison reopen barge morally flavoring shifter scarcity perfume

Generate a passphrase of 6 words and a number (minimum recommended)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -w 6 -n 1
    jasmine identity chemo suave clerk copartner 853727

Generate a passphrase of 6 words with 5 characters uppercase
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -w 6 --use-uppercase 5
    LiTmus cocoa littEr equation uNwrapped sibliNg

Generate a passphrase of 6 words with 5 characters lowercase
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -w 6 --use-lowercase 5
    MOrTUARY SIesTa MAKEOVER CURABLE JET MARSHy

Generate a password of 16 characters (minimum recommended)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -p 16
    E`31nDL0^$oYu5='

Generate a password of 8 alphanumeric characters only
'''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -p 8 --use-lowercase --use-uppercase --use-digits
    Warning: Insecure password length chosen! Should be bigger than or equal to 13
    7wmivbmR
    :~$ passphrase -p 8 --use-alphanumeric
    Warning: Insecure password length chosen! Should be bigger than or equal to 13
    ipLdqmGU

Use an external wordlist to generate a passphrase
'''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -i eff_short_wordlist_1_1column.txt
    wimp broke dash pasta zebra viral outer clasp
    :~$ passphrase -d -i eff_short_wordlist_1.txt 
    mouse trend coach stain shut rhyme baggy scale

Save the output to a file
'''''''''''''''''''''''''

::

    :~$ passphrase -o pass.txt
    :~$ passphrase > pass.txt

Generate a passphrase and use it with GPG
'''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -o pass.txt | gpg --symmetric --batch --passphrase-fd 0 somefile.txt
    :~$ sha256sum somefile.txt
    589ed823e9a84c56feb95ac58e7cf384626b9cbf4fda2a907bc36e103de1bad2  somefile.txt
    :~$ cat pass.txt | gpg --decrypt --batch --passphrase-fd 0 somefile.txt.gpg | sha256sum -
    gpg: AES256 encrypted data
    gpg: encrypted with 1 passphrase
    589ed823e9a84c56feb95ac58e7cf384626b9cbf4fda2a907bc36e103de1bad2  -

Generate a passphrase avoiding `shoulder surfing <https://en.wikipedia.org/wiki/Shoulder_surfing_(computer_security)>`__
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -q -o pass.txt

Is this really secure?
----------------------

| First of all, we will say that a password or passphrase generator
  algorithm is secure if its output is *trully* random. To achieve that,
  **Passphrase** relies entirely on ``os.urandom``, which always
  provides an interface to the OS's cryptographically secure random
  generator. The whole program is quite big, but most of it is just the
  menues and the word list.
| The generator algorithms are very short and simple, they are in
  `passphrase.passphrase <passphrase/passphrase.py>`__:
  ``Passphrase::generate()`` and ``Passphrase::generate_password()``.
  The lower level functions are in
  `passphrase.random <passphrase/random.py>`__, which directly uses
  ``os.urandom``; higher level functions are in
  `passphrase.secrets <passphrase/secrets.py>`__, that provides a
  convenient interface to those low level functions, so that
  implementation errors are avoided.

| The whole magic is done by
  ```passphrase.secrets.randbelow()`` <passphrase/secrets.py>`__, that
  returns a random natural number lower than the given value, that is
  then used as index for the word or character list by
  ```passphrase.secrets.randchoice`` <passphrase/secrets.py>`__,
  function used by the generators.
| Both ``randbelow()`` and ``randint()`` where copyied from Python's
  Lib/random, but trimmed down so that they don't allow anything fishy.
  This also makes **Passphrase** independent from unnecessary libraries
  and potential external vulnerabilities.

The algorithms are very straight forward, easy to understand and verify.
*Boring crypto is the best crypto*.

Attack surface
~~~~~~~~~~~~~~

Let's analyze some possible attack scenarios and its mitigations. If you
want to add something or you see a mistake, please write an
`issue <https://github.com/HacKanCuBa/passphrase-py/issues>`__.

Attacker is root
^^^^^^^^^^^^^^^^

TL;DR: **game over**.

An attacker that is *root* can do whatever it wants, so it's out of the
scope of this analysis.

Attacker can modify source code or wordlist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If it can modify the source code somehow, or the default
`wordlist <passphrase/wordlist.py>`__, it's also game over since a
software that succesfully checks itself doesn't exist yet. However, it
could be mitigated by placing the files under the ownership of some
privileged user (*root*).

Attacker can modify external libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Passphrase** doesn't require any external library, just Python 3 core.

Timings
-------

I realize at some point that the library was taking waaay longer to work
than before (I solved it in
`2c0eb8b <https://github.com/HacKanCuBa/passphrase-py/commit/2c0eb8bb8057f1c9437dba85a2df198a6f04c5ac>`__),
so I decided to measure each version runtime from now on. So here's the
runtime table for each tag:

+-----------------+----------------+--------------------+-----------------------------------+
| Version (tag)   | Runtime (ms)   | Relative Runtime   | Runtime Change Between Versions   |
+=================+================+====================+===================================+
| v0.2.3          | 43.1           | 1.00               | +0%                               |
+-----------------+----------------+--------------------+-----------------------------------+
| v0.2.3-1        | 41.2           | 0.96               | -4%                               |
+-----------------+----------------+--------------------+-----------------------------------+
| v0.3.0          | 39.1           | 0.91               | -5%                               |
+-----------------+----------------+--------------------+-----------------------------------+
| v0.4.1          | 107            | 2.48               | +174%                             |
+-----------------+----------------+--------------------+-----------------------------------+
| v0.4.2          | 105            | 2.43               | -2%                               |
+-----------------+----------------+--------------------+-----------------------------------+
| v0.4.4          | 105            | 2.43               | +0%                               |
+-----------------+----------------+--------------------+-----------------------------------+
| v0.4.5          | 30.7           | 0.71               | -71%                              |
+-----------------+----------------+--------------------+-----------------------------------+
| v0.4.7          | 30.6           | 0.71               | -0%                               |
+-----------------+----------------+--------------------+-----------------------------------+

| You can try it yourself: download each release, unpack it and time it.
| The command to run, depending on the release version, is:

-  newer than v0.4.5, run: ``make timeit``.
-  older than v0.4.5, run
   ``python3 -m timeit -n 100 -r 10 -s 'import os' 'os.system("python3 -m passphrase -w6 -q")'``.
-  older than v0.4, run:
   ``python3 -m timeit -n 100 -r 10 -s 'import os' 'os.system("python3 src/passphrase.py -w6 -q")'``.

License
-------

**Passphrase** is made by `HacKan <https://hackan.net>`__ under GNU GPL
v3.0+. You are free to use, share, modify and share modifications under
the terms of that `license <LICENSE>`__.

::

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
