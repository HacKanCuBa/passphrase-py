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

from os.path import join as os_path_join, isfile as os_path_isfile
from os import mkdir
from argparse import ArgumentTypeError
from tempfile import gettempdir
from unittest import TestCase
from shutil import rmtree
from random import randint
import subprocess

from passphrase import __main__
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

    def tearDown(self):
        rmtree(self.tmpdir, ignore_errors=True)

    def test_main_defaults(self):
        cmd = ['python3', '-m', 'passphrase']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        # ends with newline
        self.assertEqual(result[-1:], '\n')
        # remove newline
        result = result[:-1]
        # has only letters, and are lowercase
        self.assertTrue(
            all([c.islower() for c in result.split()])
        )
        # has 6 words
        self.assertEqual(len(result.split()), 6)

    def test_main_option_version(self):
        cmd = ['python3', '-m', 'passphrase', '--version']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        self.assertEqual(result, __main__.__version_string__ + '\n')

    def test_main_option_help(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--help'],
            ['python3', '-m', 'passphrase', '-h']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            self.assertIn(
                __main__.__version_string__,
                result
            )

    def test_main_option_insecure(self):
        # I can not mock this test when run as module, but it's being
        # tested at tests_main
        pass

    def test_main_option_no_newline(self):
        cmd = ['python3', '-m', 'passphrase', '--no-newline']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        self.assertNotEqual(result[-1:], '\n')

    def test_main_option_mute(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--mute'],
            ['python3', '-m', 'passphrase', '-m']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            self.assertEqual(result, '')

    def test_main_option_verbose(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--verbose'],
            ['python3', '-m', 'passphrase', '-v']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.assertIn(
                __main__.__version_string__,
                result.stderr.decode('utf-8')
            )
            self.assertIn(
                'bits of entropy for calculations',
                result.stderr.decode('utf-8')
            )
            self.assertIn(
                'Generating a passphrase of',
                result.stderr.decode('utf-8')
            )
            self.assertIn(
                'The entropy of this passphrase is',
                result.stderr.decode('utf-8')
            )

    def test_main_option_entropybits(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--entropybits', '1024'],
            ['python3', '-m', 'passphrase', '-e', '1024']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            # remove newline
            result = result[:-1]
            self.assertEqual(len(result.split()), 80)

    def test_main_option_uuid4(self):
        cmd = ['python3', '-m', 'passphrase', '--uuid4']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        # remove newline
        result = result[:-1]
        self.assertRegex(
            result,
            r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-'
            r'[0-9a-f]{12}'
        )

    def test_main_option_coin(self):
        cmd = ['python3', '-m', 'passphrase', '--coin']
        for _ in range(10):
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            # remove newline
            result = result[:-1]
            self.assertIn(result, ('Heads', 'Tails'))

    def test_main_option_password(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--password', '20'],
            ['python3', '-m', 'passphrase', '-p', '20']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            # remove newline
            result = result[:-1]
            self.assertEqual(len(result), 20)
            self.assertRegex(
                result,
                r'[a-zA-Z\d\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]'
                r'\^\_\`\{\|\}\~]+'
            )

    def test_main_option_password_use_uppercase(self):
        cmd = ['python3', '-m', 'passphrase', '--password', '--use-uppercase']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        # remove newline
        result = result[:-1]
        self.assertRegex(
            result,
            r'[A-Z\-]+'
        )

    def test_main_option_password_use_lowercase(self):
        cmd = ['python3', '-m', 'passphrase', '--password', '--use-lowercase']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        # remove newline
        result = result[:-1]
        self.assertRegex(
            result,
            r'[a-z\-]+'
        )

    def test_main_option_password_use_digits(self):
        cmd = ['python3', '-m', 'passphrase', '--password', '--use-digits']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        # remove newline
        result = result[:-1]
        self.assertRegex(
            result,
            r'[\d]+'
        )

    def test_main_option_password_use_alphanumeric(self):
        cmd = ['python3', '-m', 'passphrase', '--password',
               '--use-alphanumeric']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        # remove newline
        result = result[:-1]
        self.assertRegex(
            result,
            r'[a-zA-Z\d\-]+'
        )

    def test_main_option_password_use_punctuation(self):
        cmd = ['python3', '-m', 'passphrase', '--password',
               '--use-punctuation']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        # remove newline
        result = result[:-1]
        self.assertRegex(
            result,
            r'[\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_'
            r'\`\{\|\}\~]+'
        )

    def test_main_option_passphrase_words(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--words', '20'],
            ['python3', '-m', 'passphrase', '-w', '20']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            # remove newline
            result = result[:-1]
            self.assertEqual(len(result.split()), 20)
            self.assertRegex(
                result,
                r'^([a-z\-]+[ ])+[a-z\-]+$'
            )

    def test_main_option_passphrase_numbers(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--numbers', '20'],
            ['python3', '-m', 'passphrase', '-n', '20']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            # remove newline
            result = result[:-1]
            self.assertEqual(len(result.split()), 20)
            self.assertRegex(
                result,
                r'^([0-9]{6}[ ]){19}[0-9]{6}$'
            )

    def test_main_option_passphrase_separator(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--separator', '|'],
            ['python3', '-m', 'passphrase', '-s', '|']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            # remove newline
            result = result[:-1]
            # some words have dashes in it
            self.assertRegex(
                result,
                r'^([a-z\-]+[\|])+[a-z\-]+$'
            )

    def test_main_option_output(self):
        tmpfile = os_path_join(
            self.tmpdir,
            'test_main_option_output.' + str(randint(100000, 999999))
        )
        cmds = (
            ['python3', '-m', 'passphrase', '--output', tmpfile],
            ['python3', '-m', 'passphrase', '-o', tmpfile]
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            self.assertTrue(os_path_isfile(tmpfile))
            with open(tmpfile, mode='rt', encoding='utf-8') as tfile:
                self.assertEqual(result, tfile.read())

    def test_main_option_input(self):
        tmpfile = os_path_join(
            self.tmpdir,
            'test_main_option_input.' + str(randint(100000, 999999))
        )
        with open(tmpfile, mode='wt+', encoding='utf-8') as wordfile:
            wordfile.write('\n'.join(constants.WORDS))

        cmds = (
            ['python3', '-m', 'passphrase', '--input', wordfile.name],
            ['python3', '-m', 'passphrase', '-i', wordfile.name]
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
            ).stdout.decode('utf-8')
            self.assertTrue(result)
            for word in result.split():
                self.assertIn(word, constants.WORDS)

    def test_main_option_input_diceware(self):
        tmpfile = os_path_join(
            self.tmpdir,
            'test_main_option_input.' + str(randint(100000, 999999))
        )
        with open(tmpfile, mode='wt+', encoding='utf-8') as wordfile:
            wordfile.write('\n'.join(constants.WORDSD))

        cmds = (
            ['python3', '-m', 'passphrase', '--input', wordfile.name,
             '--diceware'],
            ['python3', '-m', 'passphrase', '--input', wordfile.name, '-d']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
            ).stdout.decode('utf-8')
            self.assertTrue(result)
            words = [word.split()[1] for word in constants.WORDSD]
            for word in result.split():
                self.assertIn(word, words)

    def test_bigger_than_zero(self):
        self.assertEqual(__main__._bigger_than_zero('1'), 1)


class TestInvalidInputs(TestCase):

    def setUp(self):
        self.tmpdir = os_path_join(
            gettempdir(),
            'passphrase_tests'
        )
        try:
            mkdir(self.tmpdir, 0o755)
        except FileExistsError:
            pass

    def tearDown(self):
        rmtree(self.tmpdir, ignore_errors=True)

    def _test_base(self, cmds, expected):
        for index, cmd in enumerate(cmds):
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            ).stderr.decode('utf-8')
            self.assertIn(
                expected[index] if len(expected) > 1 else expected[0],
                result
            )

    def test_main_inexistent_option(self):
        cmds = (['python3', '-m', 'passphrase', '--inexistent'], )
        expected = ('error: unrecognized arguments', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_words(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--words'],
            ['python3', '-m', 'passphrase', '-w'],
            ['python3', '-m', 'passphrase', '--words', 'a'],
            ['python3', '-m', 'passphrase', '-w', 'a'],
            ['python3', '-m', 'passphrase', '--words', '-1'],
            ['python3', '-m', 'passphrase', '-w', '-1'],
            ['python3', '-m', 'passphrase', '--words', '1.0'],
            ['python3', '-m', 'passphrase', '-w', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_numbers(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--numbers'],
            ['python3', '-m', 'passphrase', '-n'],
            ['python3', '-m', 'passphrase', '--numbers', 'a'],
            ['python3', '-m', 'passphrase', '-n', 'a'],
            ['python3', '-m', 'passphrase', '--numbers', '-1'],
            ['python3', '-m', 'passphrase', '-n', '-1'],
            ['python3', '-m', 'passphrase', '--numbers', '1.0'],
            ['python3', '-m', 'passphrase', '-n', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_entropybits(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--entropybits'],
            ['python3', '-m', 'passphrase', '-e'],
            ['python3', '-m', 'passphrase', '--entropybits', 'a'],
            ['python3', '-m', 'passphrase', '-e', 'a'],
            ['python3', '-m', 'passphrase', '--entropybits', '-1'],
            ['python3', '-m', 'passphrase', '-e', '-1'],
            ['python3', '-m', 'passphrase', '--entropybits', '1.0'],
            ['python3', '-m', 'passphrase', '-e', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_use_uppercase(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--use-uppercase', 'a'],
            ['python3', '-m', 'passphrase', '--use-uppercase', '-1'],
            ['python3', '-m', 'passphrase', '--use-uppercase', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_use_lowercase(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--use-lowercase', 'a'],
            ['python3', '-m', 'passphrase', '--use-lowercase', '-1'],
            ['python3', '-m', 'passphrase', '--use-lowercase', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_password(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--password', 'a'],
            ['python3', '-m', 'passphrase', '-p', 'a'],
            ['python3', '-m', 'passphrase', '--password', '-1'],
            ['python3', '-m', 'passphrase', '-p', '-1'],
            ['python3', '-m', 'passphrase', '--password', '1.0'],
            ['python3', '-m', 'passphrase', '-p', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_output(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--output', '/'],
            ['python3', '-m', 'passphrase', '-o', '/'],
            ['python3', '-m', 'passphrase', '--output', '/inexistent'],
            ['python3', '-m', 'passphrase', '-o', '/inexistent'],
            ['python3', '-m', 'passphrase', '--output', '/inexistent/denied'],
            ['python3', '-m', 'passphrase', '-o', '/inexistent/denied'],
        )
        expected = (
            'Error: file',
            'Error: file',
            'Error: file',
            'Error: file',
            'Error: permission denied',
            'Error: permission denied',
        )
        self._test_base(cmds, expected)

    def test_main_invalid_param_input(self):
        cmds = (
            ['python3', '-m', 'passphrase', '--input', '/'],
            ['python3', '-m', 'passphrase', '-i', '/'],
            ['python3', '-m', 'passphrase', '--input', '/inexistent'],
            ['python3', '-m', 'passphrase', '-i', '/inexistent'],
            ['python3', '-m', 'passphrase', '--input', '/inexistent/denied'],
            ['python3', '-m', 'passphrase', '-i', '/inexistent/denied'],
            ['python3', '-m', 'passphrase', '--input', '/dev/zero'],
            ['python3', '-m', 'passphrase', '-i', '/dev/zero'],
            ['python3', '-m', 'passphrase', '--diceware', '--input', '/'],
            ['python3', '-m', 'passphrase', '-d', '-i', '/'],
            ['python3', '-m', 'passphrase', '--diceware', '--input',
             '/inexistent'],
            ['python3', '-m', 'passphrase', '-d', '-i', '/inexistent'],
            ['python3', '-m', 'passphrase', '--diceware', '--input',
             '/inexistent/denied'],
            ['python3', '-m', 'passphrase', '-d', '-i', '/inexistent/denied'],
            ['python3', '-m', 'passphrase', '--diceware', '--input',
             '/dev/zero'],
            ['python3', '-m', 'passphrase', '-d', '-i', '/dev/zero'],
        )
        expected = ('Error: input file', )
        self._test_base(cmds, expected)

    def test_bigger_than_zero(self):
        self.assertRaises(ArgumentTypeError, __main__._bigger_than_zero, '-1')
