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

from unittest import TestCase
from random import randint

from passphrase.aux import Aux


STRING = 'The quick brown fox jumps over the Lazy dog 123456'
LST = (
    [
        [[], ['b']],
        ['a'],
        {12, 'bTh', 0},
        ('f', 1, 2, 3, ((3, 4, ['v', 'bjk']), (['a', 4, 'HC'])))
    ]
)


class TestValidInputs(TestCase):

    def test_make_all_uppercase(self):
        strupper = Aux.make_all_uppercase(STRING)
        self.assertIsInstance(strupper, type(STRING))
        self.assertTrue(strupper.isupper())

        lstupper = Aux.make_all_uppercase(LST)
        self.assertIsInstance(lstupper, type(LST))
        self.assertTrue(str(lstupper).isupper())

        arr = list(STRING)
        lstupper = Aux.make_all_uppercase(arr)
        self.assertIsInstance(lstupper, type(arr))
        self.assertTrue(str(lstupper).isupper())

    def test_lowercase_chars(self):
        self.assertEqual(
            Aux.lowercase_chars(STRING),
            'hequickbrownfoxjumpsovertheazydog'
        )
        self.assertEqual(
            Aux.lowercase_chars(list(STRING)),
            'hequickbrownfoxjumpsovertheazydog'
        )
        self.assertEqual(
            Aux.lowercase_chars(LST),
            'babhfvbjka'
        )

    def test_uppercase_chars(self):
        self.assertEqual(
            Aux.uppercase_chars(STRING),
            'TL'
        )
        self.assertEqual(
            Aux.uppercase_chars(list(STRING)),
            'TL'
        )
        self.assertEqual(
            Aux.uppercase_chars(LST),
            'THC'
        )

    def test_chars(self):
        self.assertEqual(
            Aux.chars(STRING),
            'ThequickbrownfoxjumpsovertheLazydog'
        )
        self.assertEqual(
            Aux.chars(list(STRING)),
            'ThequickbrownfoxjumpsovertheLazydog'
        )
        self.assertEqual(
            Aux.chars(LST),
            'babThfvbjkaHC'
        )

    def test_lowercase_count(self):
        self.assertEqual(
            Aux.lowercase_count(STRING),
            33
        )
        self.assertEqual(
            Aux.lowercase_count(list(STRING)),
            33
        )
        self.assertEqual(
            Aux.lowercase_count(LST),
            10
        )

    def test_uppercase_count(self):
        self.assertEqual(
            Aux.uppercase_count(STRING),
            2
        )
        self.assertEqual(
            Aux.uppercase_count(list(STRING)),
            2
        )
        self.assertEqual(
            Aux.uppercase_count(LST),
            3
        )

    def test_chars_count(self):
        self.assertEqual(
            Aux.chars_count(STRING),
            35
        )
        self.assertEqual(
            Aux.chars_count(list(STRING)),
            35
        )
        self.assertEqual(
            Aux.chars_count(LST),
            13
        )

    def test_make_chars_uppercase(self):
        string = 'The quick brown fox jumps over the lazy dog 123456'
        upperstart = Aux.uppercase_count(string)
        uppercase = randint(0, 10)
        for _ in range(0, 1000):
            strupper = Aux.make_chars_uppercase(string, uppercase)
            self.assertIsInstance(strupper, str)
            self.assertEqual(
                Aux.uppercase_count(strupper),
                uppercase + upperstart
            )

        lst = list(string)
        lstupper = Aux.make_chars_uppercase(lst, uppercase)
        self.assertIsInstance(lstupper, list)
        self.assertEqual(
            Aux.uppercase_count(lstupper),
            uppercase + upperstart
        )

        uppercase = len(string) * 2
        strupper = Aux.make_chars_uppercase(string, uppercase)
        self.assertIsInstance(strupper, str)
        self.assertTrue(strupper.isupper())

        uppercase = randint(0, 2)
        lst = (
            [
                [[], ['b']],
                ['a'],
                {12, 'bsh', 0},
                ('f', 1, 2, 3, ((3, 4, ['v', 'bjk']), (['a', 4, 'p'])))
            ]
        )
        lstupper = Aux.make_chars_uppercase(lst, uppercase)
        self.assertIsInstance(lstupper, type(lst))
        self.assertEqual(
            Aux.uppercase_count(lstupper),
            uppercase
        )


class TestInvalidInputs(TestCase):

    def test_make_all_uppercase(self):
        wrongtypes = (
            {'a': 1, 'b': 2},
            1.2,
            1
        )
        for wrongtype in wrongtypes:
            self.assertRaises(TypeError, Aux.make_all_uppercase, wrongtype)

    def test_make_chars_uppercase(self):
        wrongtypes = (
            {'a': 1, 'b': 2},
            1.2,
            1
        )
        for wrongtype in wrongtypes:
            self.assertRaises(
                TypeError,
                Aux.make_chars_uppercase,
                wrongtype,
                0
            )

        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            {1, 2, 3, 4},
            (1, 2),
            [1, 2],
            1.2
        )
        for wrongtype in wrongtypes:
            self.assertRaises(
                TypeError, Aux.make_chars_uppercase,
                [],
                wrongtype
            )
        self.assertRaises(ValueError, Aux.make_chars_uppercase, [], -1)

    def test_lowercase_chars(self):
        pass

    def test_uppercase_chars(self):
        pass

    def test_chars(self):
        pass

    def test_lowercase_count(self):
        pass

    def test_uppercase_count(self):
        pass

    def test_chars_count(self):
        pass
