from unittest import TestCase

import passphrase.secrets


class TestValidInputs(TestCase):

    def test_randchoice(self):
        values = (
            (1, 2, 3, 4),
            [1, 2, 3, 4],
            {1, 2, 3, 4},
            {1: 1, 2: 2, 3: 3, 4: 4},
            '1234'
        )
        for value in values:
            rand = passphrase.secrets.randchoice(value)
            self.assertIn(rand, value)

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

    def test_randbetween(self):
        lower = 2
        for upper in (10, 100, 10000):
            rand = passphrase.secrets.randbetween(lower, upper)
            self.assertIsInstance(rand, int)
            self.assertTrue(lower <= rand <= upper)
            lower = upper

    def test_randhex(self):
        for i in (1, 10, 100):
            rand = passphrase.secrets.randhex(i)
            self.assertIsInstance(rand, str)
            self.assertEqual(len(rand), i)


class TestInvalidInputs(TestCase):

    def test_randchoice(self):
        wrongtypes = (
            1.234,
            1
        )
        for t in wrongtypes:
            self.assertRaises(TypeError, passphrase.secrets.randchoice, t)
        self.assertRaises(IndexError, passphrase.secrets.randchoice, {})

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

    def test_randbetween(self):
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
            self.assertRaises(TypeError, passphrase.secrets.randbetween, t, t)
        self.assertRaises(ValueError, passphrase.secrets.randbetween, 0, 0)
        self.assertRaises(ValueError, passphrase.secrets.randbetween, -1, -1)

    def test_randhex(self):
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
            self.assertRaises(TypeError, passphrase.secrets.randhex, t)
        self.assertRaises(ValueError, passphrase.secrets.randhex, 0)
        self.assertRaises(ValueError, passphrase.secrets.randhex, -1)
