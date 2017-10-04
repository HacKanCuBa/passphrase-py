"""Calc: Auxiliar calculations
"""

from math import ceil, fabs, log10
from .settings import TRY_NUMPY

__version__ = "0.4.0"

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


def entropy_bits_nrange(minimum: int, maximum: int) -> float:
    # Shannon:
    # d = fabs(maximum - minimum)
    # ent = -(1/d) * log(1/d, 2) * d
    # Aprox form: digits * log2(10)
    ent = ceil(log10(fabs(maximum - minimum))) * 3.321928
    return ent


def password_len_needed(entropybits: int) -> int:
    # entropy_bits(list(characters)) = 6.554588
    return ceil(entropybits / 6.554588)


def words_amount_needed(entropybits: int,
                        entropy_w: float,
                        entropy_n: float,
                        amount_n: int) -> int:
    # Thanks to @julianor for this tip to calculate default amount of
    # entropy: minbitlen/log2(len(wordlist)).
    # I set the minimum entropy bits and calculate the amount of words
    # needed, cosidering the entropy of the wordlist.
    # Then: entropy_w * amount_w + entropy_n * amount_n >= ENTROPY_BITS_MIN

    amount_w = (entropybits - entropy_n * amount_n) / entropy_w

    if amount_w > -1.0:
        return ceil(fabs(amount_w))

    return 0
