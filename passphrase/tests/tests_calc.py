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

import passphrase.calc
import passphrase.tests.constants as constants


class TestValidInputs(TestCase):

    def test_entropy_bits(self):
        values = (
            (constants.WORDS, constants.WORDS_ENTROPY),
            ((1, 2), 1.0),
            ((), 0.0),
            ([], 0.0),
            ((1, ), 0.0),
        )
        for val in values:
            bits = passphrase.calc.entropy_bits(val[0])
            self.assertAlmostEqual(bits, val[1], places=2)

    def test_entropy_bits_nrange(self):
        values = (
            (0, 9, 3.17),
            (9, 0, 3.17),
            (1, 1, 0),
            (1, 99, 6.61),
            (1, 9999999999, 33.22),
            (100000.0, 999999.0, 19.78)
        )
        for val in values:
            bits = passphrase.calc.entropy_bits_nrange(val[0], val[1])
            self.assertAlmostEqual(bits, val[2], places=2)

    def test_password_length_needed(self):
        from string import digits, ascii_letters, punctuation

        chars = digits + ascii_letters + punctuation
        values = (
            (52, 8),
            (53, 9),
            (128, 20),
            (100, 16),
            (512, 79),
        )
        for val in values:
            lst = passphrase.calc.password_length_needed(val[0], chars)
            self.assertEqual(lst, val[1])

    def test_words_amount_needed(self):
        values = (
            (77, 12.92, 19.93, 0, 6),
            (77, 12.92, 19.93, 1, 5),
            (77, 12.92, 19.93, 5, 0),
            (77, 12.92, 3.32, 5, 5),
            (128, 12.92, 19.93, 0, 10)
        )
        for val in values:
            result = passphrase.calc.words_amount_needed(
                val[0],
                val[1],
                val[2],
                val[3]
            )
            self.assertEqual(result, val[4])

    def test_password_entropy(self):
        from string import (
            digits,
            ascii_lowercase,
            ascii_uppercase,
            punctuation
        )

        values = (
            (0, digits, 0.0),
            (10, ascii_lowercase + ascii_uppercase, 57.00),
            (1, digits, 3.32),
            (1, punctuation, 5.0),
            (3, 'asdfghjklOP', 10.38)
        )
        for val in values:
            self.assertAlmostEqual(
                passphrase.calc.password_entropy(val[0], val[1]),
                val[2],
                places=2
            )

    def test_passphrase_entropy(self):
        values = (
            (0, 1.0, 1.0, 0, 0.0),
            (1, 1.0, 1.0, 0, 1.0),
            (10, 10.0, 10.0, 10, 200.0),
            (6, 12.92481, 1.0, 0, 77.55),
            (0, 1.0, 3.32192, 10, 33.22),
        )
        for val in values:
            self.assertAlmostEqual(
                passphrase.calc.passphrase_entropy(
                    val[0],
                    val[1],
                    val[2],
                    val[3]
                ),
                val[4],
                places=2
            )


class TestInvalidInputs(TestCase):

    def test_entropy_bits(self):
        for wrongtype in constants.WRONGTYPES_LIST_TUPLE:
            self.assertRaises(
                TypeError,
                passphrase.calc.entropy_bits,
                wrongtype
            )
        for wrongtype in constants.WRONGTYPES_LISTOF_INT_FLOAT_COMPLEX_STR:
            self.assertRaises(
                TypeError,
                passphrase.calc.entropy_bits,
                wrongtype
            )

    def test_entropy_bits_nrange(self):
        for wrongtype in constants.WRONGTYPES_INT_FLOAT:
            self.assertRaises(
                TypeError,
                passphrase.calc.entropy_bits_nrange,
                wrongtype,
                1
            )
            self.assertRaises(
                TypeError,
                passphrase.calc.entropy_bits_nrange,
                1,
                wrongtype
            )
        self.assertRaises(
            ValueError,
            passphrase.calc.entropy_bits_nrange,
            -1,
            1
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.entropy_bits_nrange,
            1,
            -1
        )

    def test_password_length_needed(self):
        for wrongtype in constants.WRONGTYPES_INT_FLOAT:
            self.assertRaises(
                TypeError,
                passphrase.calc.password_length_needed,
                wrongtype,
                'a'
            )
        for wrongtype in constants.WRONGTYPES_STR:
            self.assertRaises(
                TypeError,
                passphrase.calc.password_length_needed,
                10,
                wrongtype
            )
        self.assertRaises(
            ValueError,
            passphrase.calc.password_length_needed,
            -1,
            'a'
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.password_length_needed,
            10,
            ''
        )

    def test_words_amount_needed(self):
        for wrongtype in constants.WRONGTYPES_INT_FLOAT:
            self.assertRaises(
                TypeError,
                passphrase.calc.words_amount_needed,
                wrongtype,
                1,
                1,
                1
            )
            self.assertRaises(
                TypeError,
                passphrase.calc.words_amount_needed,
                1,
                wrongtype,
                1,
                1
            )
            self.assertRaises(
                TypeError,
                passphrase.calc.words_amount_needed,
                1,
                1,
                wrongtype,
                1
            )
            self.assertRaises(
                TypeError,
                passphrase.calc.words_amount_needed,
                1,
                1,
                1,
                wrongtype
            )
        self.assertRaises(
            ValueError,
            passphrase.calc.words_amount_needed,
            -1,
            1,
            1,
            1
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.words_amount_needed,
            1,
            -1,
            1,
            1
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.words_amount_needed,
            1,
            1,
            -1,
            1
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.words_amount_needed,
            1,
            1,
            1,
            -1
        )

    def test_password_entropy(self):
        for wrongtype in constants.WRONGTYPES_INT:
            self.assertRaises(
                TypeError,
                passphrase.calc.password_entropy,
                wrongtype,
                'a'
            )
        for wrongtype in constants.WRONGTYPES_STR:
            self.assertRaises(
                TypeError,
                passphrase.calc.password_entropy,
                1,
                wrongtype
            )
        self.assertRaises(
            ValueError,
            passphrase.calc.password_entropy,
            -1,
            'a'
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.password_entropy,
            1,
            ''
        )

    def test_passphrase_entropy(self):
        for wrongtype in constants.WRONGTYPES_INT_FLOAT:
            self.assertRaises(
                TypeError,
                passphrase.calc.passphrase_entropy,
                wrongtype,
                1,
                1,
                1
            )
            self.assertRaises(
                TypeError,
                passphrase.calc.passphrase_entropy,
                1,
                wrongtype,
                1,
                1
            )
            self.assertRaises(
                TypeError,
                passphrase.calc.passphrase_entropy,
                1,
                1,
                wrongtype,
                1
            )
            self.assertRaises(
                TypeError,
                passphrase.calc.passphrase_entropy,
                1,
                1,
                1,
                wrongtype
            )
        self.assertRaises(
            ValueError,
            passphrase.calc.passphrase_entropy,
            -1,
            1,
            1,
            1
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.passphrase_entropy,
            1,
            -1,
            1,
            1
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.passphrase_entropy,
            1,
            1,
            -1,
            1
        )
        self.assertRaises(
            ValueError,
            passphrase.calc.passphrase_entropy,
            1,
            1,
            1,
            -1
        )
