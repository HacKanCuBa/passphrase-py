# tests_aux
SOMESTRING = 'The quick brown fox jumps over the Lazy dog 123456'
SOMESTRING_LOWERS = 'hequickbrownfoxjumpsovertheazydog'
SOMESTRING_UPPERS = 'TL'
SOMESTRING_CHARS = 'ThequickbrownfoxjumpsovertheLazydog'

SOMEMIXEDLIST = (
    [
        [[], ['b']],
        ('a', ),
        {12, 'bTh', 0},
        ('f', 1, 2, 3, ((3, 4, ['v', 'bjk']), (['a', 4, 'HC']))),
        'OoO',
    ],
    0xff,
)
SOMEMIXEDLIST_LOWERS = 'babhfvbjkao'
SOMEMIXEDLIST_UPPERS = 'THCOO'
SOMEMIXEDLIST_CHARS = 'babThfvbjkaHCOoO'
SOMEMIXEDLIST_UPPERCASE = (
    [
        [[], ['B']],
        ('A', ),
        {12, 'BTH', 0},
        ('F', 1, 2, 3, ((3, 4, ['V', 'BJK']), (['A', 4, 'HC']))),
        'OOO',
    ],
    0xff,
)

SOMENONLETTERSLIST = (1, 2, '.', {1: '--'})
# <>

# tests_calc tests_main tests_passphrase
WORDS = [
    'vivacious',
    'frigidly',
    'condiment',
    'passive',
    'reverse',
    'brunt'
]
WORDS_ENTROPY = 2.58
# <>

# tests_main tests_passphrase
WORDSD = [
    '123456\tvivacious',
    '163456\tfrigidly',
    '153456\tcondiment',
    '143456\tpassive',
    '133456\tpenpal',
    '113456\talarm'
]
# <>

# Wrong types for the types not indicated
WRONGTYPES_INT = (
    {1, 2},
    {'a': 1, 'b': 2},
    'aaaa',
    (1, 2),
    [1, 2],
    1.2,
    1j,
)
WRONGTYPES_STR = (
    {1, 2},
    {'a': 1, 'b': 2},
    (1, 2),
    [],
    1,
    1.234,
    1j,
)
WRONGTYPES_STR_INT = (
    {1, 2},
    {'a': 1, 'b': 2},
    (1, 2),
    [],
    1.234,
    1j,
)
WRONGTYPES_INT_FLOAT = (
    {1, 2},
    {'a': 1, 'b': 2},
    'aaaa',
    (1, 2),
    [],
    1j,
)
WRONGTYPES_LIST_TUPLE = (
    {1, 2},
    {'a': 1, 'b': 2},
    'aaaa',
    1234,
    1.234,
    1j,
)
WRONGTYPES_LIST_SET_TUPLE_STR = (
    {'a': 1, 'b': 2},
    1.2,
    1,
    1j,
)
WRONGTYPES_LIST_SET_TUPLE_STR_DICT = (
    1.2,
    1,
    1j,
)
WRONGTYPES_LISTOF_INT_FLOAT_COMPLEX_STR = (
    [1, (2, 3)],
    ['a', 1.2, 1j, {'a', 'b'}],
    [{1, 2}, ],
)
