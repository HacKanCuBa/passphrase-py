"""Secrets: Generate cryptographically strong pseudo-random numbers

Numbers generated with this module are suitable for managing secrets such as
account authentication, tokens, and similar.
"""

from os import urandom as _urandom

__version__ = "0.4.1"


def getrandbits(nbits: int) -> int:
    """Generates an int with nbits random bits."""
    # https://github.com/python/cpython/blob/3.6/Lib/random.py#L676
    if not isinstance(nbits, int):
        raise TypeError('number of bits should be an integer')
    if nbits <= 0:
        raise ValueError('number of bits must be greater than zero')
    nbytes = (nbits + 7) // 8                       # bits / 8 and rounded up
    num = int.from_bytes(_urandom(nbytes), 'big')
    return num >> (nbytes * 8 - nbits)                # trim excess bits


def randbelow(num: int) -> int:
    """Return a random int in the range [0,num).  Raises ValueError if n<=0."""

    if not isinstance(num, int):
        raise TypeError('number must be an integer')
    if num <= 0:
        raise ValueError('number must be greater than zero')

    # https://github.com/python/cpython/blob/3.6/Lib/random.py#L223
    nbits = num.bit_length()  # don't use (n-1) here because n can be 1
    randnum = getrandbits(nbits)  # 0 <= randnum < 2**nbits
    while randnum >= num:
        randnum = getrandbits(nbits)
    return randnum
