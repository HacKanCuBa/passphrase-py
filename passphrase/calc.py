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

"""Auxiliar calculations."""

from typing import Union, List, Tuple
from math import ceil, fabs, log10, log2

__version__ = '0.4.8'


def entropy_bits(
        lst: Union[
            List[Union[int, str, float, complex]],
            Tuple[Union[int, str, float, complex]]
        ]
) -> float:
    """Calculate the number of entropy bits in a list or tuple of elements."""
    # Based on https://stackoverflow.com/a/45091961
    if not isinstance(lst, (list, tuple)):
        raise TypeError('lst must be a list or a tuple')

    for num in lst:
        if not isinstance(num, (int, str, float, complex)):
            raise TypeError('lst can only be comprised of int, str, float, '
                            'complex')

    n_lst = len(lst)

    if n_lst <= 1:
        return 0.0

    # Some NumPy replacements
    counts = [lst.count(x) for x in lst]
    probs = [c / n_lst for c in counts]

    # Compute entropy
    entropy = 0.0
    for prob in probs:
        entropy -= prob * log2(prob)

    return entropy


def entropy_bits_nrange(
        minimum: Union[int, float], maximum: Union[int, float]
) -> float:
    """Calculate the number of entropy bits in a range of numbers."""
    # Shannon:
    # d = fabs(maximum - minimum)
    # ent = -(1/d) * log(1/d, 2) * d
    # Aprox form: log10(digits) * log2(10)
    if not isinstance(minimum, (int, float)):
        raise TypeError('minimum can only be int or float')
    if not isinstance(maximum, (int, float)):
        raise TypeError('maximum can only be int or float')
    if minimum < 0:
        raise ValueError('minimum should be greater than 0')
    if maximum < 0:
        raise ValueError('maximum should be greater than 0')

    dif = fabs(maximum - minimum)
    if dif == 0:
        return 0.0

    ent = log10(dif) * 3.321928
    return ent


def password_length_needed(entropybits: Union[int, float], chars: str) -> int:
    """Calculate the length of a password for a given entropy and chars."""
    if not isinstance(entropybits, (int, float)):
        raise TypeError('entropybits can only be int or float')
    if entropybits < 0:
        raise ValueError('entropybits should be greater than 0')
    if not isinstance(chars, str):
        raise TypeError('chars can only be string')
    if not chars:
        raise ValueError("chars can't be null")

    # entropy_bits(list(characters)) = 6.554588
    entropy_c = entropy_bits(list(chars))
    return ceil(entropybits / entropy_c)


def words_amount_needed(entropybits: Union[int, float],
                        entropy_w: Union[int, float],
                        entropy_n: Union[int, float],
                        amount_n: int) -> int:
    """Calculate words needed for a passphrase based on entropy."""
    # Thanks to @julianor for this tip to calculate default amount of
    # entropy: minbitlen/log2(len(wordlist)).
    # I set the minimum entropy bits and calculate the amount of words
    # needed, cosidering the entropy of the wordlist.
    # Then: entropy_w * amount_w + entropy_n * amount_n >= ENTROPY_BITS_MIN

    if not isinstance(entropybits, (int, float)):
        raise TypeError('entropybits can only be int or float')
    if not isinstance(entropy_w, (int, float)):
        raise TypeError('entropy_w can only be int or float')
    if not isinstance(entropy_n, (int, float)):
        raise TypeError('entropy_n can only be int or float')
    if not isinstance(amount_n, int):
        raise TypeError('amount_n can only be int')
    if entropybits < 0:
        raise ValueError('entropybits should be greater than 0')
    if entropy_w <= 0:
        raise ValueError('entropy_w should be greater than 0')
    if entropy_n < 0:
        raise ValueError('entropy_n should be greater than 0')
    if amount_n < 0:
        raise ValueError('amount_n should be greater than 0')

    amount_w = (entropybits - entropy_n * amount_n) / entropy_w

    if amount_w > -1.0:
        return ceil(fabs(amount_w))

    return 0


def password_entropy(length: int, chars: str) -> float:
    """Calculate the entropy of a password with given length and chars."""
    if not isinstance(length, int):
        raise TypeError('length can only be int')
    if length < 0:
        raise ValueError('length should be greater than 0')
    if not isinstance(chars, str):
        raise TypeError('chars can only be string')
    if not chars:
        raise ValueError("chars can't be null")

    if length == 0:
        return 0.0

    entropy_c = entropy_bits(list(chars))
    return float(length * entropy_c)


def passphrase_entropy(amount_w: int,
                       entropy_w: Union[int, float],
                       entropy_n: Union[int, float],
                       amount_n: int) -> float:
    """Calculate the entropy of a passphrase with given words and numbers."""
    if not isinstance(amount_w, int):
        raise TypeError('amount_w can only be int')
    if not isinstance(entropy_w, (int, float)):
        raise TypeError('entropy_w can only be int or float')
    if not isinstance(entropy_n, (int, float)):
        raise TypeError('entropy_n can only be int or float')
    if not isinstance(amount_n, int):
        raise TypeError('amount_n can only be int')
    if amount_w < 0:
        raise ValueError('amount_w should be greater than 0')
    if entropy_w < 0:
        raise ValueError('entropy_w should be greater than 0')
    if entropy_n < 0:
        raise ValueError('entropy_n should be greater than 0')
    if amount_n < 0:
        raise ValueError('amount_n should be greater than 0')

    return float(amount_w * entropy_w + amount_n * entropy_n)
