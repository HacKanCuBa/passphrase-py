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
from tempfile import gettempdir
from unittest import TestCase
from shutil import rmtree, copy
from random import randint
import subprocess

import passphrase.tests.constants as constants
import passphrase.__main__
from passphrase.aux import Aux


def _test_setup():
    tmpdir = os_path_join(
        gettempdir(),
        'passphrase_tests'
    )
    try:
        mkdir(tmpdir, 0o755)
    except FileExistsError:
        pass
    # Build bin
    cmd = ['make', 'install-common']
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        ).stdout.decode('utf-8')
    except subprocess.CalledProcessError as err:
        raise AssertionError(
            'Make recipe which attempted to create Passphrase binary '
            'exited with nonzero value, error: {}'.format(err)
        )
    mkdir_pos = result.find('mkdir ') + 6
    make_tmpdir = result[mkdir_pos:mkdir_pos + 26]
    bin_tmpdir = os_path_join(make_tmpdir, 'passphrase')
    bin_ = os_path_join(tmpdir, 'passphrase')
    copy(bin_tmpdir, bin_)
    rmtree(make_tmpdir, ignore_errors=True)
    return tmpdir, bin_


class TestValidInputs(TestCase):

    def setUp(self):
        self.tmpdir, self.bin = _test_setup()
        self.assertTrue(Aux.isfile_notempty(self.bin))

    def tearDown(self):
        rmtree(self.tmpdir, ignore_errors=True)

    def test_main_defaults(self):
        cmd = [self.bin, ]
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
        cmd = [self.bin, '--version']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        self.assertEqual(result, passphrase.__main__.__version_string__ + '\n')

    def test_main_option_help(self):
        cmds = (
            [self.bin, '--help'],
            [self.bin, '-h']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            self.assertIn(
                passphrase.__main__.__version_string__,
                result
            )

    def test_main_option_insecure(self):
        # How can simulate low system entropy?? (without actually consuming
        # all of it...)
        pass

    def test_main_option_no_newline(self):
        cmd = [self.bin, '--no-newline']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        self.assertNotEqual(result[-1:], '\n')

    def test_main_option_mute(self):
        cmds = (
           [self.bin, '--mute'],
           [self.bin, '-m']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8')
            self.assertEqual(result, '')

    def test_main_option_verbose(self):
        cmds = (
           [self.bin, '--verbose'],
           [self.bin, '-v']
        )
        for cmd in cmds:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.assertIn(
                passphrase.__main__.__version_string__,
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
           [self.bin, '--entropybits', '1024'],
           [self.bin, '-e', '1024']
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
        cmd = [self.bin, '--uuid4']
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
        cmd = [self.bin, '--coin']
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
           [self.bin, '--password', '20'],
           [self.bin, '-p', '20']
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
        cmd = [self.bin, '--password', '--use-uppercase']
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
        cmd = [self.bin, '--password', '--use-lowercase']
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
        cmd = [self.bin, '--password', '--use-digits']
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
        cmd = [self.bin, '--password',
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
        cmd = [self.bin, '--password',
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
            [self.bin, '--words', '20'],
            [self.bin, '-w', '20']
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
            [self.bin, '--numbers', '20'],
            [self.bin, '-n', '20']
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
            [self.bin, '--separator', '|'],
            [self.bin, '-s', '|']
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
            [self.bin, '--output', tmpfile],
            [self.bin, '-o', tmpfile]
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
            [self.bin, '--input', wordfile.name],
            [self.bin, '-i', wordfile.name]
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
            [self.bin, '--input', wordfile.name,
             '--diceware'],
            [self.bin, '--input', wordfile.name, '-d']
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


class TestInvalidInputs(TestCase):

    def setUp(self):
        self.tmpdir, self.bin = _test_setup()
        self.assertTrue(Aux.isfile_notempty(self.bin))

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
        cmds = ([self.bin, '--inexistent'], )
        expected = ('error: unrecognized arguments', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_words(self):
        cmds = (
            [self.bin, '--words'],
            [self.bin, '-w'],
            [self.bin, '--words', 'a'],
            [self.bin, '-w', 'a'],
            [self.bin, '--words', '-1'],
            [self.bin, '-w', '-1'],
            [self.bin, '--words', '1.0'],
            [self.bin, '-w', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_numbers(self):
        cmds = (
            [self.bin, '--numbers'],
            [self.bin, '-n'],
            [self.bin, '--numbers', 'a'],
            [self.bin, '-n', 'a'],
            [self.bin, '--numbers', '-1'],
            [self.bin, '-n', '-1'],
            [self.bin, '--numbers', '1.0'],
            [self.bin, '-n', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_entropybits(self):
        cmds = (
            [self.bin, '--entropybits'],
            [self.bin, '-e'],
            [self.bin, '--entropybits', 'a'],
            [self.bin, '-e', 'a'],
            [self.bin, '--entropybits', '-1'],
            [self.bin, '-e', '-1'],
            [self.bin, '--entropybits', '1.0'],
            [self.bin, '-e', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_use_uppercase(self):
        cmds = (
            [self.bin, '--use-uppercase', 'a'],
            [self.bin, '--use-uppercase', '-1'],
            [self.bin, '--use-uppercase', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_use_lowercase(self):
        cmds = (
            [self.bin, '--use-lowercase', 'a'],
            [self.bin, '--use-lowercase', '-1'],
            [self.bin, '--use-lowercase', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_password(self):
        cmds = (
            [self.bin, '--password', 'a'],
            [self.bin, '-p', 'a'],
            [self.bin, '--password', '-1'],
            [self.bin, '-p', '-1'],
            [self.bin, '--password', '1.0'],
            [self.bin, '-p', '1.0'],
        )
        expected = ('error: argument', )
        self._test_base(cmds, expected)

    def test_main_invalid_param_output(self):
        cmds = (
            [self.bin, '--output', '/'],
            [self.bin, '-o', '/'],
            [self.bin, '--output', '/inexistent'],
            [self.bin, '-o', '/inexistent'],
            [self.bin, '--output', '/inexistent/denied'],
            [self.bin, '-o', '/inexistent/denied'],
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
            [self.bin, '--input', '/'],
            [self.bin, '-i', '/'],
            [self.bin, '--input', '/inexistent'],
            [self.bin, '-i', '/inexistent'],
            [self.bin, '--input', '/inexistent/denied'],
            [self.bin, '-i', '/inexistent/denied'],
            [self.bin, '--input', '/dev/zero'],
            [self.bin, '-i', '/dev/zero'],
            [self.bin, '--diceware', '--input', '/'],
            [self.bin, '-d', '-i', '/'],
            [self.bin, '--diceware', '--input', '/inexistent'],
            [self.bin, '-d', '-i', '/inexistent'],
            [self.bin, '--diceware', '--input', '/inexistent/denied'],
            [self.bin, '-d', '-i', '/inexistent/denied'],
            [self.bin, '--diceware', '--input', '/dev/zero'],
            [self.bin, '-d', '-i', '/dev/zero'],
        )
        expected = ('Error: file', )
        self._test_base(cmds, expected)
