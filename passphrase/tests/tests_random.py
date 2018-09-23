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
from random import randrange
from test.support.script_helper import assert_python_ok
from os.path import dirname, realpath, join as os_path_join

import passphrase.random
import passphrase.tests.constants as constants


class TestValidInputs(TestCase):

    def test_randint(self):
        errmsg = 'randint(%d) returned %d'
        for _ in range(5):
            nbits = randrange(1, 30)
            rand = passphrase.random.randint(nbits)
            self.assertIsInstance(rand, int)
            self.assertTrue(0 <= rand < 2**nbits, errmsg % (nbits, rand))

    def get_randbytes_subprocess(self, count):
        random_module_path = os_path_join(
            dirname(dirname(realpath(__file__))),
            'random.py'
        )
        # Python 3.5+
        code = '\n'.join((
            'import sys',
            'import importlib.util',
            'spec = importlib.util.spec_from_file_location'
            '("passphrase.random", "%s")' % random_module_path,
            'random = importlib.util.module_from_spec(spec)',
            'spec.loader.exec_module(random)',
            'data = random.randbytes(%s)' % count,
            'sys.stdout.buffer.write(data)',
            'sys.stdout.buffer.flush()'))
        out = assert_python_ok('-c', code)
        stdout = out[1]
        self.assertEqual(len(stdout), count)
        return stdout

    def test_randbytes(self):
        # http://bit.ly/2zX0ChB
        self.assertEqual(len(passphrase.random.randbytes(1)), 1)
        self.assertEqual(len(passphrase.random.randbytes(10)), 10)
        self.assertEqual(len(passphrase.random.randbytes(100)), 100)
        self.assertEqual(len(passphrase.random.randbytes(1000)), 1000)

        data1 = passphrase.random.randbytes(16)
        self.assertIsInstance(data1, bytes)
        data2 = passphrase.random.randbytes(16)
        self.assertNotEqual(data1, data2)

        data1 = self.get_randbytes_subprocess(16)
        data2 = self.get_randbytes_subprocess(16)
        self.assertNotEqual(data1, data2)


class TestInvalidInputs(TestCase):

    def test_randint(self):
        for wrongtype in constants.WRONGTYPES_INT:
            self.assertRaises(TypeError, passphrase.random.randint, wrongtype)
        self.assertRaises(ValueError, passphrase.random.randint, 0)
        self.assertRaises(ValueError, passphrase.random.randint, -1)

    def test_randbytes(self):
        for wrongtype in constants.WRONGTYPES_INT:
            self.assertRaises(
                TypeError,
                passphrase.random.randbytes,
                wrongtype)
        self.assertRaises(ValueError, passphrase.random.randbytes, 0)
        self.assertRaises(ValueError, passphrase.random.randbytes, -1)
