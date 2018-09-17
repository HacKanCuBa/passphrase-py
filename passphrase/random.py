#  ***************************************************************************
#  This file is part of Passphrase:
#  A cryptographically secure passphrase and password generator
#  Copyright (C) <2017>  <Ivan Ariel Barrera Oro>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  ***************************************************************************

"""Low level library to access system's randomness source.

Values generated with this module are suitable for generating cryptographically
secure tokens.

Check Secrets library for higher level functions.

"""

from os import urandom as _urandom

__version__ = '0.1.1'


def randbytes(nbytes: int) -> bytes:
    r"""Return a random byte string containing *nbytes* bytes.

    Raises ValueError if nbytes <= 0, and TypeError if it's not an integer.

    >>> randbytes(16)  #doctest:+SKIP
    b'\\xebr\\x17D*t\\xae\\xd4\\xe3S\\xb6\\xe2\\xebP1\\x8b'

    """
    if not isinstance(nbytes, int):
        raise TypeError('number of bytes shoud be an integer')
    if nbytes <= 0:
        raise ValueError('number of bytes must be greater than zero')

    return _urandom(nbytes)


def randint(nbits: int) -> int:
    """Generate an int with nbits random bits.

    Raises ValueError if nbits <= 0, and TypeError if it's not an integer.

    >>> randint(16)  #doctest:+SKIP
    1871

    """
    if not isinstance(nbits, int):
        raise TypeError('number of bits should be an integer')
    if nbits <= 0:
        raise ValueError('number of bits must be greater than zero')

    # https://github.com/python/cpython/blob/3.6/Lib/random.py#L676
    nbytes = (nbits + 7) // 8                       # bits / 8 and rounded up
    num = int.from_bytes(randbytes(nbytes), 'big')
    return num >> (nbytes * 8 - nbits)              # trim excess bits
