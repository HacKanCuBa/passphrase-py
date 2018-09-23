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

from os.path import join as os_path_join
from tempfile import gettempdir
from unittest import TestCase
from random import randint
from shutil import rmtree
from uuid import UUID
from os import mkdir

from passphrase.passphrase import Passphrase
from passphrase.aux import Aux
import passphrase.tests.constants as constants


class TestValidInputs(TestCase):

    def setUp(self):
        self.tmpdir = os_path_join(
            gettempdir(),
            'passphrase_tests'
        )
        try:
            mkdir(self.tmpdir, 0o755)
        except FileExistsError:
            pass

        self.wordsd_file = os_path_join(self.tmpdir, 'wordsd.list')
        with open(self.wordsd_file, mode='wt', encoding='utf-8') as wordfile:
            wordfile.write('\n'.join(constants.WORDSD))
        self.words_file = os_path_join(self.tmpdir, 'words.list')
        with open(self.words_file, mode='wt', encoding='utf-8') as wordfile:
            wordfile.write('\n'.join(constants.WORDS))

    def tearDown(self):
        rmtree(self.tmpdir, ignore_errors=True)

    def test_init(self):
        passp = Passphrase()
        self.assertIsInstance(passp, Passphrase)
        self.assertIsNone(passp.wordlist)

        passp = Passphrase(self.words_file, False)
        self.assertIsInstance(passp, Passphrase)
        self.assertEqual(passp.wordlist, constants.WORDS)

        passp = Passphrase(self.wordsd_file, True)
        self.assertIsInstance(passp, Passphrase)
        self.assertEqual(
            passp.wordlist,
            [word.split()[1] for word in constants.WORDSD]
        )

        passp = Passphrase('internal')
        self.assertIsInstance(passp, Passphrase)
        self.assertEqual(len(passp.wordlist), 7776)

    def test_entropy_bits(self):
        self.assertAlmostEqual(
            Passphrase.entropy_bits(constants.WORDS),
            constants.WORDS_ENTROPY,
            places=2
        )
        self.assertAlmostEqual(
            Passphrase.entropy_bits((10.1, 1005)),
            9.96,
            places=2
        )

    def test_generate(self):
        for _ in range(0, 1000):
            amount_w = randint(0, 10)
            amount_n = randint(0, 10)
            uppercase = randint(1, 5)
            passp = Passphrase()
            passp.load_internal_wordlist()
            passp.amount_w = amount_w
            passp.amount_n = amount_n
            passphrase = passp.generate(uppercase)
            self.assertIsInstance(passphrase, list)
            self.assertEqual(len(passphrase), amount_w + amount_n)
            if amount_w > 0:
                # Perhaps it was requested just 1 word, and many uppercase
                # chars, but the word happens to be just 3 chars long...
                chars = Aux.chars_count(passphrase)
                if chars < uppercase:
                    self.assertTrue(str(passphrase).isupper())
                else:
                    self.assertEqual(
                        Aux.uppercase_count(passphrase),
                        uppercase
                    )
                passp.generate(0)
                self.assertTrue(str(passp).isupper())

                lowercase = randint(-5, -1)
                passphrase = passp.generate(lowercase)
                chars = Aux.chars_count(passphrase)
                if chars < (lowercase * -1):
                    self.assertTrue(str(passphrase).islower())
                else:
                    self.assertEqual(
                        Aux.lowercase_count(passphrase),
                        lowercase * -1
                    )

    def test_generate_password(self):
        length = randint(0, 10)
        passp = Passphrase()
        passp.passwordlen = length
        passphrase = passp.generate_password()
        self.assertIsInstance(passphrase, list)
        self.assertEqual(len(passphrase), length)

    def test_generate_uuid4(self):
        passp = Passphrase()
        passphrase = passp.generate_uuid4()
        self.assertIsInstance(passphrase, list)
        self.assertEqual(len(passphrase), 5)
        passp.separator = ''
        uuid4 = UUID(str(passp), version=4)
        self.assertEqual(str(passp), uuid4.hex)

    def test_import_words_from_file(self):
        passp = Passphrase()
        self.assertIsNone(passp.import_words_from_file(self.words_file, False))
        self.assertEqual(passp.wordlist, constants.WORDS)
        self.assertIsNone(passp.import_words_from_file(self.wordsd_file, True))
        self.assertEqual(
            passp.wordlist,
            [word.split()[1] for word in constants.WORDSD]
        )

    def test_password_length_needed(self):
        passp = Passphrase()
        passp.entropy_bits_req = 128
        p_len = passp.password_length_needed()
        self.assertEqual(p_len, 20)

    def test_words_amount_needed(self):
        passp = Passphrase()
        passp.load_internal_wordlist()
        passp.entropy_bits_req = 77
        passp.amount_n = 0
        amount_w = passp.words_amount_needed()
        self.assertEqual(amount_w, 6)

        passp.import_words_from_file(self.words_file, False)
        amount_w = passp.words_amount_needed()
        self.assertEqual(amount_w, 30)

    def test_entropy_bits_req(self):
        passp = Passphrase()
        passp.entropy_bits_req = 1
        self.assertEqual(passp.entropy_bits_req, 1)

    def test_randnum_min(self):
        passp = Passphrase()
        passp.randnum_min = 1
        self.assertEqual(passp.randnum_min, 1)

    def test_randnum_max(self):
        passp = Passphrase()
        passp.randnum_max = 1
        self.assertEqual(passp.randnum_max, 1)

    def test_amount_w(self):
        passp = Passphrase()
        passp.amount_w = 1
        self.assertEqual(passp.amount_w, 1)

    def test_amount_n(self):
        passp = Passphrase()
        passp.amount_n = 1
        self.assertEqual(passp.amount_n, 1)

    def test_passwordlen(self):
        passp = Passphrase()
        passp.passwordlen = 1
        self.assertEqual(passp.passwordlen, 1)

    def test_wordlist(self):
        passp = Passphrase()
        passp.wordlist = constants.WORDS
        self.assertEqual(passp.wordlist, list(constants.WORDS))

    def test_to_string(self):
        passp = Passphrase()
        passp.load_internal_wordlist()
        passphrase = str(passp)
        self.assertEqual(len(passphrase), 0)
        passp.amount_n = 1
        passp.amount_w = 1
        passp.generate()
        passphrase = str(passp)
        self.assertIsInstance(passphrase, str)
        self.assertTrue(len(passphrase) > 0)

    def test_load_internal_wordlist(self):
        passp = Passphrase()
        self.assertIsNone(passp.wordlist)
        passp.load_internal_wordlist()
        self.assertTrue(passp.wordlist)
        self.assertEqual(len(passp.wordlist), 7776)

    def test_generated_password_entropy(self):
        passp = Passphrase()
        passp.passwordlen = 1
        self.assertAlmostEqual(
            passp.generated_password_entropy(),
            6.55,
            places=2
        )

    def test_generated_passphrase_entropy(self):
        passp = Passphrase('internal')
        passp.amount_n = 1
        passp.amount_w = 1
        self.assertAlmostEqual(
            passp.generated_passphrase_entropy(),
            32.70,
            places=2
        )

    def test_separator(self):
        passp = Passphrase('internal')
        passp.amount_w = 1
        passp.amount_n = 1
        passp.separator = '-.-'
        passp.generate()
        self.assertIn('-.-', str(passp))

    def test_password_use_lowercase(self):
        passp = Passphrase()
        passp.separator = ''
        passp.passwordlen = 5
        passp.password_use_lowercase = True
        passp.password_use_uppercase = False
        passp.password_use_digits = False
        passp.password_use_punctuation = False
        passp.generate_password()
        self.assertRegex(
            str(passp),
            r'[a-z\-]+'
        )

    def test_password_use_uppercase(self):
        passp = Passphrase()
        passp.separator = ''
        passp.passwordlen = 5
        passp.password_use_lowercase = False
        passp.password_use_uppercase = True
        passp.password_use_digits = False
        passp.password_use_punctuation = False
        passp.generate_password()
        self.assertRegex(
            str(passp),
            r'[A-Z\-]+'
        )

    def test_password_use_digits(self):
        passp = Passphrase()
        passp.separator = ''
        passp.passwordlen = 5
        passp.password_use_lowercase = False
        passp.password_use_uppercase = False
        passp.password_use_digits = True
        passp.password_use_punctuation = False
        passp.generate_password()
        self.assertRegex(
            str(passp),
            r'[\d]+'
        )

    def test_password_use_punctuation(self):
        passp = Passphrase()
        passp.separator = ''
        passp.passwordlen = 5
        passp.password_use_lowercase = False
        passp.password_use_uppercase = False
        passp.password_use_digits = False
        passp.password_use_punctuation = True
        passp.generate_password()
        self.assertRegex(
            str(passp),
            r'[\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_'
            r'\`\{\|\}\~]+'
        )


class TestInvalidInputs(TestCase):

    def test_init(self):
        self.assertRaises(
            FileNotFoundError,
            Passphrase,
            'nonexistent.file'
        )
        self.assertRaises(
            FileNotFoundError,
            Passphrase,
            'nonexistent.file',
            True
        )

    def test_entropy_bits(self):
        for wrongtype in constants.WRONGTYPES_LIST_TUPLE:
            self.assertRaises(
                TypeError,
                Passphrase.entropy_bits,
                wrongtype
            )
        self.assertRaises(
            ValueError,
            Passphrase.entropy_bits,
            (-1, 0)
        )

    def test_import_words_from_file(self):
        passp = Passphrase()
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

    def test_password_length_needed(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_INT_FLOAT:
            passp._entropy_bits_req = wrongtype
            with self.assertRaises(TypeError) as context:
                passp.password_length_needed()
            self.assertIn(
                'entropybits can only be int or float',
                str(context.exception)
            )

        passp._entropy_bits_req = -1
        with self.assertRaises(ValueError) as context:
            passp.password_length_needed()
        self.assertIn(
            'entropybits should be greater than 0',
            str(context.exception)
        )
        passp = Passphrase()
        self.assertRaises(ValueError, passp.password_length_needed)
        passp.password_use_lowercase = False
        passp.password_use_uppercase = False
        passp.password_use_digits = False
        passp.password_use_punctuation = False
        self.assertRaises(ValueError, passp.password_length_needed)
        passp.entropy_bits_req = 77
        self.assertRaises(ValueError, passp.password_length_needed)

    def test_entropy_bits_req(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_INT_FLOAT:
            with self.assertRaises(TypeError) as context:
                passp.entropy_bits_req = wrongtype
            self.assertIn(
                'entropy_bits_req can only be int or float',
                str(context.exception)
            )
        with self.assertRaises(ValueError) as context:
            passp.entropy_bits_req = -1
        self.assertIn(
            'entropy_bits_req should be greater than 0',
            str(context.exception)
        )

    def test_randnum_min(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_INT:
            with self.assertRaises(TypeError) as context:
                passp.randnum_min = wrongtype
            self.assertIn(
                'randnum_min can only be int',
                str(context.exception)
            )
        with self.assertRaises(ValueError) as context:
            passp.randnum_min = -1
        self.assertIn(
            'randnum_min should be greater than 0',
            str(context.exception)
        )

    def test_randnum_max(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_INT:
            with self.assertRaises(TypeError) as context:
                passp.randnum_max = wrongtype
            self.assertIn(
                'randnum_max can only be int',
                str(context.exception)
            )
        with self.assertRaises(ValueError) as context:
            passp.randnum_max = -1
        self.assertIn(
            'randnum_max should be greater than 0',
            str(context.exception)
        )

    def test_amount_w(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_INT:
            with self.assertRaises(TypeError) as context:
                passp.amount_w = wrongtype
            self.assertIn(
                'amount_w can only be int',
                str(context.exception)
            )
        with self.assertRaises(ValueError) as context:
            passp.amount_w = -1
        self.assertIn(
            'amount_w should be greater than 0',
            str(context.exception)
        )

    def test_amount_n(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_INT:
            with self.assertRaises(TypeError) as context:
                passp.amount_n = wrongtype
            self.assertIn(
                'amount_n can only be int',
                str(context.exception)
            )
        with self.assertRaises(ValueError) as context:
            passp.amount_n = -1
        self.assertIn(
            'amount_n should be greater than 0',
            str(context.exception)
        )

    def test_passwordlen(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_INT:
            with self.assertRaises(TypeError) as context:
                passp.passwordlen = wrongtype
            self.assertIn(
                'passwordlen can only be int',
                str(context.exception)
            )
        with self.assertRaises(ValueError) as context:
            passp.passwordlen = -1
        self.assertIn(
            'passwordlen should be greater than 0',
            str(context.exception)
        )

    def test_wordlist(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_LIST_TUPLE:
            with self.assertRaises(TypeError) as context:
                passp.wordlist = wrongtype
            self.assertIn(
                'wordlist can only be list or tuple',
                str(context.exception)
            )

    def test_generate(self):
        passp = Passphrase()
        self.assertRaises(ValueError, passp.generate)
        passp.amount_n = 0
        self.assertRaises(ValueError, passp.generate)
        passp.amount_w = 0
        self.assertRaises(ValueError, passp.generate)
        passp.load_internal_wordlist()
        self.assertEqual(passp.generate(), [])

        for wrongtype in constants.WRONGTYPES_INT:
            self.assertRaises(TypeError, passp.generate, wrongtype)

    def test_generate_password(self):
        passp = Passphrase()
        self.assertRaises(ValueError, passp.generate_password)
        passp.password_use_lowercase = False
        passp.password_use_uppercase = False
        passp.password_use_digits = False
        passp.password_use_punctuation = False
        self.assertRaises(ValueError, passp.generate_password)
        passp.passwordlen = 77
        self.assertRaises(ValueError, passp.generate_password)

    def test_separator(self):
        passp = Passphrase()
        for wrongtype in constants.WRONGTYPES_STR:
            with self.assertRaises(TypeError) as context:
                passp.separator = wrongtype
            self.assertIn(
                'separator can only be string',
                str(context.exception)
            )

    def test_words_amount_needed(self):
        passp = Passphrase()
        self.assertRaises(ValueError, passp.words_amount_needed)
        passp.amount_n = 1
        self.assertRaises(ValueError, passp.words_amount_needed)
        passp.entropy_bits_req = 77
        self.assertRaises(ValueError, passp.words_amount_needed)
        passp.load_internal_wordlist()
        self.assertEqual(passp.words_amount_needed(), 5)

    def test_generated_password_entropy(self):
        passp = Passphrase()
        self.assertRaises(ValueError, passp.generated_password_entropy)
        passp.passwordlen = 0
        self.assertEqual(passp.generated_password_entropy(), 0.0)

    def test_generated_passphrase_entropy(self):
        passp = Passphrase()
        self.assertRaises(ValueError, passp.generated_passphrase_entropy)
        passp.load_internal_wordlist()
        self.assertRaises(ValueError, passp.generated_passphrase_entropy)
        passp.amount_n = 0
        self.assertRaises(ValueError, passp.generated_passphrase_entropy)
        passp.amount_w = 0
        self.assertEqual(passp.generated_passphrase_entropy(), 0.0)
