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

WORDS = (
    'vivacious',
    'frigidly',
    'condiment',
    'passive',
    'reverse',
    'brunt'
)

WORDS_ENTROPY = 2.58


class TestValidInputs(TestCase):

    def test_entropy_bits(self):
        values = (
            (WORDS, WORDS_ENTROPY),
            ((1, 2), 1.0),
            ((), 0.0),
            ([], 0.0),
        )
        for i in values:
            bits = passphrase.calc.entropy_bits(i[0])
            self.assertAlmostEqual(bits, i[1], places=2)

    def test_entropy_bits_nrange(self):
        values = (
            (0, 9, 3.17),
            (9, 0, 3.17),
            (1, 1, 0),
            (1, 99, 6.61),
            (1, 9999999999, 33.22),
            (100000.0, 999999.0, 19.78)
        )
        for i in values:
            bits = passphrase.calc.entropy_bits_nrange(i[0], i[1])
            self.assertAlmostEqual(bits, i[2], places=2)

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
        for v in values:
            a = passphrase.calc.words_amount_needed(v[0], v[1], v[2], v[3])
            self.assertEqual(a, v[4])


class TestInvalidInputs(TestCase):

    def test_entropy_bits(self):
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            1234,
            1.234,
            (1, 2, (3, 4)),
            set({1, 2, 3, 4})
        )
        for t in wrongtypes:
            self.assertRaises(TypeError, passphrase.calc.entropy_bits, t)

    def test_entropy_bits_nrange(self):
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            []
        )
        for t in wrongtypes:
            self.assertRaises(
                TypeError,
                passphrase.calc.entropy_bits_nrange,
                t,
                t
            )
        self.assertRaises(
            ValueError,
            passphrase.calc.entropy_bits_nrange,
            -1,
            0
        )

    def test_password_length_needed(self):
        wrongtypes_e = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            []
        )
        for t in wrongtypes_e:
            self.assertRaises(
                TypeError,
                passphrase.calc.password_length_needed,
                t,
                'a'
            )
        wrongtypes_c = (
            {1, 2},
            {'a': 1, 'b': 2},
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            [],
            1,
            1.234
        )
        for t in wrongtypes_c:
            self.assertRaises(
                TypeError,
                passphrase.calc.password_length_needed,
                10,
                t
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
        wrongtypes = (
            {1, 2},
            {'a': 1, 'b': 2},
            'aaaa',
            (1, 2, (3, 4)),
            set({1, 2, 3, 4}),
            []
        )
        for t in wrongtypes:
            self.assertRaises(
                TypeError,
                passphrase.calc.words_amount_needed,
                t,
                t,
                t,
                t
            )
        self.assertRaises(
            ValueError,
            passphrase.calc.words_amount_needed,
            -1,
            -1,
            -1,
            -1
        )
