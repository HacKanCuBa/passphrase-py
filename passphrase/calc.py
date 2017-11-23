"""Calc: Auxiliar calculations
"""

from math import ceil, fabs, log10
from .settings import TRY_NUMPY

__version__ = "0.4.1"

try:
    from math import log2   # Python 3.3+
except ImportError:
    from math import log

    def log2(num: float) -> float:
        return log(num, 2)


if TRY_NUMPY is True:
    try:
        from numpy import count_nonzero as np_count_nonzero
        from numpy import unique as np_unique

        NUMPY = True
    except ImportError:
        NUMPY = False


def entropy_bits(lst: list) -> float:
    # Based on https://stackoverflow.com/a/45091961
    if not isinstance(lst, (list, tuple)):
        raise TypeError('lst must be a list or a tuple')

    for n in lst:
        if not isinstance(n, (int, str, float, complex)):
            raise TypeError('lst can only be comprised of int, str, float, '
                            'long, complex')

    n_lst = len(lst)

    if n_lst <= 1:
        return 0.0

    if TRY_NUMPY is True and NUMPY is True:
        value, counts = np_unique(lst, return_counts=True)
        probs = counts / n_lst
        n_classes = np_count_nonzero(probs)
    else:
        # Some NumPy replacements
        counts = [lst.count(x) for x in set(lst)]
        probs = [c / n_lst for c in counts]
        n_classes = len([x for x in probs if x != 0])

    if n_classes <= 1:
        return 0.0

    # Compute entropy
    ent = 0.0
    for i in probs:
        ent -= i * log2(i)

    return ent


def entropy_bits_nrange(minimum: float, maximum: float) -> float:
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


def password_length_needed(entropybits: float, chars: str) -> int:
    if not isinstance(entropybits, (int, float)):
        raise TypeError('entropybits can only be int or float')
    if entropybits < 0:
        raise ValueError('entropybits should be greater than 0')
    if not isinstance(chars, str):
        raise TypeError('chars can only be string')
    if len(chars) < 1:
        raise ValueError('chars can\t be null')

    # entropy_bits(list(characters)) = 6.554588
    entropy_c = entropy_bits(list(chars))
    return ceil(entropybits / entropy_c)


def words_amount_needed(entropybits: float,
                        entropy_w: float,
                        entropy_n: float,
                        amount_n: int) -> int:
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
