from unittest import TestCase

import passphrase.passphrase


class TestPassphrase(TestCase):

    def test_generate(self):
        passp = passphrase.passphrase.Passphrase()
        p = passp.generate()
        self.assertTrue(type(p) == list)
