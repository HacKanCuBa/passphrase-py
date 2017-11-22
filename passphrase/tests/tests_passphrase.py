from unittest import TestCase
from random import randint
from uuid import UUID

import passphrase.passphrase

WORDS = (
    'vivacious',
    'frigidly',
    'condiment',
    'passive',
    'reverse',
    'brunt'
)
WORDS_ENTROPY = 2.58
WORDS_FILE = '/tmp/words.list'
with open(WORDS_FILE, mode='wt', encoding='utf-8') as wordfile:
    wordfile.write('\n'.join(WORDS))

WORDSD = (
    '123456\tvivacious',
    '163456\tfrigidly',
    '153456\tcondiment',
    '143456\tpassive',
    '133456\tpenpal',
    '113456\talarm'
)
WORDSD_FILE = '/tmp/wordsd.list'
with open(WORDSD_FILE, mode='wt', encoding='utf-8') as wordfile:
    wordfile.write('\n'.join(WORDSD))


class TestValidInputs(TestCase):

    def test_init(self):
        passp1 = passphrase.passphrase.Passphrase()
        self.assertIsInstance(passp1, passphrase.passphrase.Passphrase)

        passp2 = passphrase.passphrase.Passphrase(WORDS_FILE, False)
        self.assertIsInstance(passp2, passphrase.passphrase.Passphrase)

        passp3 = passphrase.passphrase.Passphrase(WORDSD_FILE, True)
        self.assertIsInstance(passp3, passphrase.passphrase.Passphrase)

    def test_entropy_bits(self):
        self.assertAlmostEqual(
            passphrase.passphrase.Passphrase.entropy_bits(WORDS),
            WORDS_ENTROPY,
            places=2
        )
        self.assertAlmostEqual(
            passphrase.passphrase.Passphrase.entropy_bits((10.1, 1005)),
            9.96,
            places=2
        )

    def test_generate(self):
        amount_w = randint(0, 10)
        amount_n = randint(0, 10)
        passp = passphrase.passphrase.Passphrase()
        passp.amount_w = amount_w
        passp.amount_n = amount_n
        p = passp.generate()
        self.assertIsInstance(p, list)
        self.assertEqual(len(p), amount_w + amount_n)

    def test_generate_password(self):
        length = randint(0, 10)
        passp = passphrase.passphrase.Passphrase()
        passp.passwordlen = length
        p = passp.generate_password()
        self.assertIsInstance(p, list)
        self.assertEqual(len(p), length)

    def test_generate_uuid4(self):
        passp = passphrase.passphrase.Passphrase()
        p = passp.generate_uuid4()
        self.assertIsInstance(p, list)
        self.assertEqual(len(p), 5)
        passp.separator = ''
        uuid4 = UUID(str(passp), version=4)
        self.assertEqual(str(passp), uuid4.hex)

    def test_import_words_from_file(self):
        passp = passphrase.passphrase.Passphrase()

        ret = passp.import_words_from_file(WORDS_FILE, False)
        self.assertIsNone(ret)
        self.assertEqual(passp._wordlist, list(WORDS))

        ret = passp.import_words_from_file(WORDSD_FILE, True)
        self.assertIsNone(ret)
        wordsd_ = [word.split()[1] for word in WORDSD]
        self.assertEqual(passp._wordlist, list(wordsd_))

    def test_password_len_needed(self):
        passp = passphrase.passphrase.Passphrase()
        passp.entropy_bits_req = 128
        p_len = passp.password_len_needed()
        self.assertEqual(p_len, 20)

    def test_words_amount_needed(self):
        passp = passphrase.passphrase.Passphrase()

        w = passp.words_amount_needed()
        self.assertEqual(w, 6)

        passp.import_words_from_file(WORDS_FILE, False)
        w = passp.words_amount_needed()
        self.assertEqual(w, 30)

    def test_entropy_bits_req(self):
        passp = passphrase.passphrase.Passphrase()
        passp.entropy_bits_req = 1
        self.assertEqual(passp.entropy_bits_req, 1)

    def test_randnum_min(self):
        passp = passphrase.passphrase.Passphrase()
        passp.randnum_min = 1
        self.assertEqual(passp.randnum_min, 1)

    def test_randnum_max(self):
        passp = passphrase.passphrase.Passphrase()
        passp.randnum_max = 1
        self.assertEqual(passp.randnum_max, 1)

    def test_amount_w(self):
        passp = passphrase.passphrase.Passphrase()
        passp.amount_w = 1
        self.assertEqual(passp.amount_w, 1)

    def test_amount_n(self):
        passp = passphrase.passphrase.Passphrase()
        passp.amount_n = 1
        self.assertEqual(passp.amount_n, 1)

    def test_passwordlen(self):
        passp = passphrase.passphrase.Passphrase()
        passp.passwordlen = 1
        self.assertEqual(passp.passwordlen, 1)

    def test_wordlist(self):
        passp = passphrase.passphrase.Passphrase()
        passp.wordlist = WORDS
        self.assertEqual(passp.wordlist, list(WORDS))

    def test_to_string(self):
        passp = passphrase.passphrase.Passphrase()
        p = str(passp)
        self.assertEqual(len(p), 0)
        passp.generate()
        p = str(passp)
        self.assertIsInstance(p, str)
        self.assertTrue(len(p) > 0)


class TestInvalidInputs(TestCase):

    def test_init(self):
        self.assertRaises(
            FileNotFoundError,
            passphrase.passphrase.Passphrase,
            'nonexistent.file'
        )
        self.assertRaises(
            FileNotFoundError,
            passphrase.passphrase.Passphrase,
            'nonexistent.file',
            True
        )

    def test_entropy_bits(self):
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            1,
            1.1
        )
        for t in wrongtypes:
            self.assertRaises(
                TypeError,
                passphrase.passphrase.Passphrase.entropy_bits,
                t
            )
        self.assertRaises(
            ValueError,
            passphrase.passphrase.Passphrase.entropy_bits,
            (-1, 0)
        )

    def test_import_words_from_file(self):
        passp = passphrase.passphrase.Passphrase()
        self.assertRaises(
            FileNotFoundError,
            passp.import_words_from_file,
            'nonexistent.file',
            False
        )
        self.assertRaises(
            FileNotFoundError,
            passp.import_words_from_file,
            'nonexistent.file',
            True
        )

    def test_password_len_needed(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            ()
        )
        for t in wrongtypes:
            passp._entropy_bits_req = t
            with self.assertRaises(TypeError) as ct:
                passp.password_len_needed()
            self.assertIn(
                'entropybits can only be int or float',
                str(ct.exception)
            )

        passp._entropy_bits_req = -1
        with self.assertRaises(ValueError) as ct:
            passp.password_len_needed()
        self.assertIn(
            'entropybits should be greater than 0',
            str(ct.exception)
        )

    def test_entropy_bits_req(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            ()
        )
        for t in wrongtypes:
            with self.assertRaises(TypeError) as ct:
                passp.entropy_bits_req = t
            self.assertIn(
                'entropy_bits_req can only be int or float',
                str(ct.exception)
            )
        with self.assertRaises(ValueError) as ct:
            passp.entropy_bits_req = -1
        self.assertIn(
            'entropy_bits_req should be greater than 0',
            str(ct.exception)
        )

    def test_randnum_min(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            (),
            1.1
        )
        for t in wrongtypes:
            with self.assertRaises(TypeError) as ct:
                passp.randnum_min = t
            self.assertIn(
                'randnum_min can only be int',
                str(ct.exception)
            )
        with self.assertRaises(ValueError) as ct:
            passp.randnum_min = -1
        self.assertIn(
            'randnum_min should be greater than 0',
            str(ct.exception)
        )

    def test_randnum_max(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            (),
            1.1
        )
        for t in wrongtypes:
            with self.assertRaises(TypeError) as ct:
                passp.randnum_max = t
            self.assertIn(
                'randnum_max can only be int',
                str(ct.exception)
            )
        with self.assertRaises(ValueError) as ct:
            passp.randnum_max = -1
        self.assertIn(
            'randnum_max should be greater than 0',
            str(ct.exception)
        )

    def test_amount_w(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            (),
            1.1
        )
        for t in wrongtypes:
            with self.assertRaises(TypeError) as ct:
                passp.amount_w = t
            self.assertIn(
                'amount_w can only be int',
                str(ct.exception)
            )
        with self.assertRaises(ValueError) as ct:
            passp.amount_w = -1
        self.assertIn(
            'amount_w should be greater than 0',
            str(ct.exception)
        )

    def test_amount_n(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            (),
            1.1
        )
        for t in wrongtypes:
            with self.assertRaises(TypeError) as ct:
                passp.amount_n = t
            self.assertIn(
                'amount_n can only be int',
                str(ct.exception)
            )
        with self.assertRaises(ValueError) as ct:
            passp.amount_n = -1
        self.assertIn(
            'amount_n should be greater than 0',
            str(ct.exception)
        )

    def test_passwordlen(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            (),
            1.1
        )
        for t in wrongtypes:
            with self.assertRaises(TypeError) as ct:
                passp.passwordlen = t
            self.assertIn(
                'passwordlen can only be int',
                str(ct.exception)
            )
        with self.assertRaises(ValueError) as ct:
            passp.passwordlen = -1
        self.assertIn(
            'passwordlen should be greater than 0',
            str(ct.exception)
        )

    def test_wordlist(self):
        passp = passphrase.passphrase.Passphrase()
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            set({1, 2, 3, 4}),
            1.1,
            1
        )
        for t in wrongtypes:
            with self.assertRaises(TypeError) as ct:
                passp.wordlist = t
            self.assertIn(
                'wordlist can only be list or tuple',
                str(ct.exception)
            )
