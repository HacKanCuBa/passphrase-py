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

from passphrase.aux import Aux


string = 'The quick brown fox jumps over the Lazy dog 123456'
lst = (
    [
        [[], ['b']],
        ['a'],
        {12, 'bTh', 0},
        ('f', 1, 2, 3, ((3, 4, ['v', 'bjk']), (['a', 4, 'HC'])))
    ]
)


class TestValidInputs(TestCase):

    def test_make_all_uppercase(self):
        strupper = Aux.make_all_uppercase(string)
        self.assertIsInstance(strupper, type(string))
        self.assertTrue(strupper.isupper())

        lstupper = Aux.make_all_uppercase(lst)
        self.assertIsInstance(lstupper, type(lst))
        self.assertTrue(str(lstupper).isupper())

        arr = list(string)
        lstupper = Aux.make_all_uppercase(arr)
        self.assertIsInstance(lstupper, type(arr))
        self.assertTrue(str(lstupper).isupper())

    def test_lowercase_chars(self):
        self.assertEqual(
            Aux.lowercase_chars(string),
            'hequickbrownfoxjumpsovertheazydog'
        )
        self.assertEqual(
            Aux.lowercase_chars(list(string)),
            'hequickbrownfoxjumpsovertheazydog'
        )
        self.assertEqual(
            Aux.lowercase_chars(lst),
            'babhfvbjka'
        )

    def test_uppercase_chars(self):
        self.assertEqual(
            Aux.uppercase_chars(string),
            'TL'
        )
        self.assertEqual(
            Aux.uppercase_chars(list(string)),
            'TL'
        )
        self.assertEqual(
            Aux.uppercase_chars(lst),
            'THC'
        )

    def test_chars(self):
        self.assertEqual(
            Aux.chars(string),
            'ThequickbrownfoxjumpsovertheLazydog'
        )
        self.assertEqual(
            Aux.chars(list(string)),
            'ThequickbrownfoxjumpsovertheLazydog'
        )
        self.assertEqual(
            Aux.chars(lst),
            'babThfvbjkaHC'
        )

    def test_lowercase_count(self):
        self.assertEqual(
            Aux.lowercase_count(string),
            33
        )
        self.assertEqual(
            Aux.lowercase_count(list(string)),
            33
        )
        self.assertEqual(
            Aux.lowercase_count(lst),
            10
        )

    def test_uppercase_count(self):
        self.assertEqual(
            Aux.uppercase_count(string),
            2
        )
        self.assertEqual(
            Aux.uppercase_count(list(string)),
            2
        )
        self.assertEqual(
            Aux.uppercase_count(lst),
            3
        )

    def test_chars_count(self):
        self.assertEqual(
            Aux.chars_count(string),
            35
        )
        self.assertEqual(
            Aux.chars_count(list(string)),
            35
        )
        self.assertEqual(
            Aux.chars_count(lst),
            13
        )


class TestInvalidInputs(TestCase):

    def test_make_all_uppercase(self):
        wrongtypes = (
            {'a': 1, 'b': 2},
            1.2,
            1
        )
        for t in wrongtypes:
            self.assertRaises(TypeError, Aux.make_all_uppercase, t)
