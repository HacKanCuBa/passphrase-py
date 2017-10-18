from unittest import TestCase
from random import randint

import passphrase.secrets


class TestValidInputs(TestCase):

    def test_getrandbits(self):
        errmsg = "randbits(%d) returned %d"
        for _ in range(5):
            nbits = randint(1, 30)
            rand = passphrase.secrets.getrandbits(nbits)
            self.assertIsInstance(rand, int)
            self.assertTrue(0 <= rand < 2**nbits, errmsg % (nbits, rand))

    def test_randbelow(self):
        prev = 0
        repeat = 0
        for i in (10, 100, 10000):
            rand = passphrase.secrets.randbelow(i)
            self.assertIn(rand, range(i))
            if prev == rand:
                repeat += 1
            self.assertTrue(
                repeat < 2,
                "randbelow(%d) returned the same number twice in a row!" % (i)
            )
            prev = rand


class TestInvalidInputs(TestCase):

    def test_getrandbits(self):
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            1.234,
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            ()
        )
        for t in wrongtypes:
            self.assertRaises(TypeError, passphrase.secrets.getrandbits, t)
        self.assertRaises(ValueError, passphrase.secrets.getrandbits, 0)
        self.assertRaises(ValueError, passphrase.secrets.getrandbits, -1)

    def test_randbelow(self):
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            1.234,
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            ()
        )
        for t in wrongtypes:
            self.assertRaises(TypeError, passphrase.secrets.randbelow, t)
        self.assertRaises(ValueError, passphrase.secrets.randbelow, 0)
        self.assertRaises(ValueError, passphrase.secrets.randbelow, -1)
