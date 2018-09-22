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

from subprocess import run, PIPE
from unittest import TestCase
from random import randint

from passphrase.aux import Aux
import passphrase.tests.constants as constants


class TestValidInputs(TestCase):

    def test_make_all_uppercase(self):
        strupper = Aux.make_all_uppercase(constants.SOMESTRING)
        self.assertIsInstance(strupper, type(constants.SOMESTRING))
        self.assertTrue(strupper.isupper())

        lstupper = Aux.make_all_uppercase(constants.SOMEMIXEDLIST)
        self.assertIsInstance(lstupper, type(constants.SOMEMIXEDLIST))
        self.assertTrue(str(lstupper).isupper())

        arr = list(constants.SOMESTRING)
        lstupper = Aux.make_all_uppercase(arr)
        self.assertIsInstance(lstupper, type(arr))
        self.assertTrue(str(lstupper).isupper())

    def test_lowercase_chars(self):
        self.assertEqual(
            Aux.lowercase_chars(constants.SOMESTRING),
            constants.SOMESTRING_LOWERS
        )
        self.assertEqual(
            Aux.lowercase_chars(list(constants.SOMESTRING)),
            constants.SOMESTRING_LOWERS
        )
        self.assertEqual(
            Aux.lowercase_chars(constants.SOMEMIXEDLIST),
            constants.SOMEMIXEDLIST_LOWERS
        )

    def test_uppercase_chars(self):
        self.assertEqual(
            Aux.uppercase_chars(constants.SOMESTRING),
            constants.SOMESTRING_UPPERS
        )
        self.assertEqual(
            Aux.uppercase_chars(list(constants.SOMESTRING)),
            constants.SOMESTRING_UPPERS
        )
        self.assertEqual(
            Aux.uppercase_chars(constants.SOMEMIXEDLIST),
            constants.SOMEMIXEDLIST_UPPERS
        )

    def test_chars(self):
        self.assertEqual(
            Aux.chars(constants.SOMESTRING),
            constants.SOMESTRING_CHARS
        )
        self.assertEqual(
            Aux.chars(list(constants.SOMESTRING)),
            constants.SOMESTRING_CHARS
        )
        self.assertEqual(
            Aux.chars(constants.SOMEMIXEDLIST),
            constants.SOMEMIXEDLIST_CHARS
        )

    def test_lowercase_count(self):
        self.assertEqual(
            Aux.lowercase_count(constants.SOMESTRING),
            len(constants.SOMESTRING_LOWERS)
        )
        self.assertEqual(
            Aux.lowercase_count(list(constants.SOMESTRING)),
            len(constants.SOMESTRING_LOWERS)
        )
        self.assertEqual(
            Aux.lowercase_count(constants.SOMEMIXEDLIST),
            len(constants.SOMEMIXEDLIST_LOWERS)
        )

    def test_uppercase_count(self):
        self.assertEqual(
            Aux.uppercase_count(constants.SOMESTRING),
            len(constants.SOMESTRING_UPPERS)
        )
        self.assertEqual(
            Aux.uppercase_count(list(constants.SOMESTRING)),
            len(constants.SOMESTRING_UPPERS)
        )
        self.assertEqual(
            Aux.uppercase_count(constants.SOMEMIXEDLIST),
            len(constants.SOMEMIXEDLIST_UPPERS)
        )

    def test_chars_count(self):
        self.assertEqual(
            Aux.chars_count(constants.SOMESTRING),
            len(constants.SOMESTRING_CHARS)
        )
        self.assertEqual(
            Aux.chars_count(list(constants.SOMESTRING)),
            len(constants.SOMESTRING_CHARS)
        )
        self.assertEqual(
            Aux.chars_count(constants.SOMEMIXEDLIST),
            len(constants.SOMEMIXEDLIST_CHARS)
        )

    def test_make_chars_uppercase(self):
        self.assertEqual(Aux.make_chars_uppercase(constants.SOMESTRING, 0),
                         constants.SOMESTRING)
        upperstart = Aux.uppercase_count(constants.SOMESTRING)
        uppercase = randint(0, 10)
        for _ in range(0, 1000):
            strupper = Aux.make_chars_uppercase(
                constants.SOMESTRING,
                uppercase
            )
            self.assertIsInstance(strupper, str)
            self.assertEqual(
                Aux.uppercase_count(strupper),
                uppercase + upperstart
            )

        lst = list(constants.SOMESTRING)
        lstupper = Aux.make_chars_uppercase(lst, uppercase)
        self.assertIsInstance(lstupper, list)
        self.assertEqual(
            Aux.uppercase_count(lstupper),
            uppercase + upperstart
        )

        uppercase = len(constants.SOMESTRING) * 2
        strupper = Aux.make_chars_uppercase(constants.SOMESTRING, uppercase)
        self.assertIsInstance(strupper, str)
        self.assertTrue(strupper.isupper())

        uppercase = randint(0, 5)
        upperstart = Aux.uppercase_count(constants.SOMEMIXEDLIST)
        lstupper = Aux.make_chars_uppercase(constants.SOMEMIXEDLIST, uppercase)
        self.assertIsInstance(lstupper, type(constants.SOMEMIXEDLIST))
        self.assertEqual(
            Aux.uppercase_count(lstupper),
            uppercase + upperstart
        )

        self.assertEqual(
            Aux.make_chars_uppercase(constants.SOMEMIXEDLIST, 100),
            constants.SOMEMIXEDLIST_UPPERCASE
        )

    def test_system_entropy(self):
        self.assertGreater(Aux.system_entropy(), 0)

    def test_print_stderr(self):
        string = constants.SOMESTRING
        proc = run(
            [
                'python',
                '-c',
                'from passphrase import Aux; Aux.print_stderr("{}")'.format(
                    string
                )
            ],
            stdout=PIPE,
            stderr=PIPE,
        )
        self.assertEqual(proc.stdout.decode('utf-8'), '')
        self.assertEqual(proc.stderr.decode('utf-8'), string + '\n')
        # The following is just for coverage, the actual test is above
        Aux.print_stderr('')


class TestInvalidInputs(TestCase):

    def test_make_all_uppercase(self):
        for wrongtype in constants.WRONGTYPES_LIST_SET_TUPLE_STR:
            self.assertRaises(TypeError, Aux.make_all_uppercase, wrongtype)

    def test_make_chars_uppercase(self):
        for wrongtype in constants.WRONGTYPES_LIST_SET_TUPLE_STR:
            self.assertRaises(
                TypeError,
                Aux.make_chars_uppercase,
                wrongtype,
                0
            )

        for wrongtype in constants.WRONGTYPES_INT:
            self.assertRaises(
                TypeError, Aux.make_chars_uppercase,
                [],
                wrongtype
            )
        self.assertRaises(ValueError, Aux.make_chars_uppercase, [], -1)

    def test_make_one_char_uppercase(self):
        for wrongtype in constants.WRONGTYPES_STR:
            self.assertRaises(
                TypeError,
                Aux._make_one_char_uppercase,
                wrongtype
            )

    def test_isfile_notempty(self):
        for wrongtype in constants.WRONGTYPES_STR_INT:
            self.assertRaises(TypeError, Aux.isfile_notempty, wrongtype)
