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

"""Generate cryptographically strong pseudo-random numbers.

Numbers generated with this module are suitable for managing secrets such as
account authentication, tokens, and similar.

"""

from typing import Union
from math import ceil

from .random import randint as random_randint, randbytes as random_randbytes

__version__ = '0.5.5'


def randchoice(seq: Union[str, list, tuple, dict, set]) -> any:
    """Return a randomly chosen element from the given sequence.

    Raises TypeError if *seq* is not str, list, tuple, dict, set and an
    IndexError if it is empty.

    >>> randchoice((1, 2, 'a', 'b'))  #doctest:+SKIP
    'a'

    """
    if not isinstance(seq, (str, list, tuple, dict, set)):
        raise TypeError('seq must be str, list, tuple, dict or set')
    if len(seq) <= 0:
        raise IndexError('seq must have at least one element')

    if isinstance(seq, set):
        values = list(seq)
        return randchoice(values)
    elif isinstance(seq, dict):
        indexes = list(seq)
        index = randchoice(indexes)
    else:
        index = randbelow(len(seq))

    return seq[index]


def randbelow(num: int) -> int:
    """Return a random int in the range [0,num).

    Raises ValueError if num <= 0, and TypeError if it's not an integer.

    >>> randbelow(16)  #doctest:+SKIP
    13

    """
    if not isinstance(num, int):
        raise TypeError('number must be an integer')
    if num <= 0:
        raise ValueError('number must be greater than zero')
    if num == 1:
        return 0

    # https://github.com/python/cpython/blob/3.6/Lib/random.py#L223
    nbits = num.bit_length()    # don't use (n-1) here because n can be 1
    randnum = random_randint(nbits)    # 0 <= randnum < 2**nbits
    while randnum >= num:
        randnum = random_randint(nbits)
    return randnum


def randbetween(lower: int, upper: int) -> int:
    """Return a random int in the range [lower, upper].

    Raises ValueError if any is lower than 0, and TypeError if any is not an
    integer.

    """
    if not isinstance(lower, int) or not isinstance(upper, int):
        raise TypeError('lower and upper must be integers')
    if lower < 0 or upper <= 0:
        raise ValueError('lower and upper must be greater than zero')

    return randbelow(upper - lower + 1) + lower


def randhex(ndigits: int) -> str:
    """Return a random text string of hexadecimal characters.

    The string has *ndigits* random digits.
    Raises ValueError if ndigits <= 0, and TypeError if it's not an integer.

    >>> randhex(16)  #doctest:+SKIP
    '56054d728fc56f63'

    """
    if not isinstance(ndigits, int):
        raise TypeError('number of digits must be an integer')
    if ndigits <= 0:
        raise ValueError('number of digits must be greater than zero')

    nbytes = ceil(ndigits / 2)
    rbytes = random_randbytes(nbytes)
    hexstr = rbytes.hex()[:ndigits]

    return hexstr


def randbool() -> bool:
    """Return boolean random value.

    >>> randbool()  #doctest:+SKIP
    True

    """
    num = random_randint(8)
    return num > 127
