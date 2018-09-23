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

from unittest import TestCase, mock
from io import StringIO
import sys

from passphrase.__main__ import main, __version_string__ as main_version_string
from passphrase.passphrase import Passphrase
from passphrase.aux import Aux


class TestValidInputs(TestCase):

    def setUp(self):
        self._stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self._stdout

    def test_main_defaults(self):
        arg = []
        self.assertEqual(main(arg), 0)
        # ends with newline
        self.assertEqual(sys.stdout.getvalue()[-1:], '\n')
        # remove newline
        result = sys.stdout.getvalue()[:-1]
        # has only letters, and are lowercase
        self.assertTrue(
            all([c.islower() for c in result.split()])
        )
        # has 6 words
        self.assertEqual(len(result.split()), 6)

    def test_main_option_version(self):
        arg = ['--version', ]
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()
        self.assertEqual(result, main_version_string + '\n')

    @mock.patch.object(Aux, 'print_stderr')
    def test_main_option_verbose(self, mock_print_stderr):
        args = (
            ['--verbose', ],
            ['-v', ]
        )
        for arg in args:
            self.assertEqual(main(arg), 0)
            mock_print_stderr.assert_any_call(
                main_version_string
            )
            mock_print_stderr.assert_any_call(
                'Using 77 bits of entropy for calculations (if any). '
                'The minimum recommended is 77'
            )
            mock_print_stderr.assert_any_call(
                'Generating a passphrase of 6 words and 0 numbers using '
                'internal wordlist'
            )
            mock_print_stderr.assert_any_call(
                'The entropy of this passphrase is 77.55 bits'
            )

    @mock.patch.object(Aux, 'print_stderr')
    @mock.patch.object(Aux, 'system_entropy')
    def test_main_option_insecure(self, mock_system_entropy,
                                  mock_print_stderr):
        mock_system_entropy.return_value = 1
        self.assertEqual(main([]), 1)
        mock_print_stderr.assert_any_call(
            'Warning: the system has too few entropy: 1 bits; randomness '
            'quality could be poor'
        )
        mock_print_stderr.assert_any_call(
            'Error: system entropy too low: 1 < 128'
        )
        arg = ['--insecure', ]
        self.assertEqual(main(arg), 0)
        mock_print_stderr.assert_any_call(
            'Warning: the system has too few entropy: 1 bits; randomness '
            'quality could be poor'
        )

    @mock.patch.object(Aux, 'print_stderr')
    def test_main_option_entropy_bits(self, mock_print_stderr):
        args = [
            ['--entropy', '1'],
            ['-e', '1']
        ]
        for arg in args:
            self.assertEqual(main(arg), 0)
            mock_print_stderr.assert_any_call(
                'Warning: insecure number of bits for entropy calculations '
                'chosen! Should be bigger than 77'
            )
            mock_print_stderr.assert_any_call(
                'Warning: the passphrase is too short!'
            )

    @mock.patch.object(Aux, 'print_stderr')
    def test_main_option_uuid4(self, mock_print_stderr):
        arg = ['--uuid4', ]
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()[:-1]  # remove newline
        self.assertRegex(
            result,
            r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-'
            r'[0-9a-f]{12}'
        )
        arg = ['--uuid4', '--verbose']
        self.assertEqual(main(arg), 0)
        mock_print_stderr.assert_any_call('Generating UUID v4')

    @mock.patch.object(Aux, 'print_stderr')
    def test_main_option_coin(self, mock_print_stderr):
        arg = ['--coin', ]
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()[:-1]  # remove newline
        self.assertIn(result, ('Heads', 'Tails'))
        arg = ['--coin', '--verbose']
        self.assertEqual(main(arg), 0)
        mock_print_stderr.assert_any_call('Throwing a coin')

    @mock.patch.object(Aux, 'print_stderr')
    def test_main_option_password(self, mock_print_stderr):
        args = (
            ['--password'],
            ['-p'],
            ['--password', '0'],
            ['-p', '0']
        )
        for arg in args:
            self.assertEqual(main(arg), 0)
            result = sys.stdout.getvalue()[:-1]  # remove newline
            self.assertRegex(
                result,
                r'[a-zA-Z\d\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]'
                r'\^\_\`\{\|\}\~]+'
            )
            sys.stdout = StringIO()  # reset
        arg = ['--password', '8', '--verbose']
        self.assertEqual(main(arg), 0)
        mock_print_stderr.assert_any_call(
            'Warning: insecure password length chosen! Should be bigger than '
            'or equal to 12'
        )
        mock_print_stderr.assert_any_call(
            'Generating password of 8 characters long using uppercase '
            'characters, lowercase characters, digits, punctuation characters'
        )

    def test_main_option_password_use_uppercase(self):
        arg = ['--password', '--use-uppercase']
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()[:-1]  # remove newline
        self.assertRegex(
            result,
            r'[A-Z\-]+'
        )

    def test_main_option_password_use_lowercase(self):
        arg = ['--password', '--use-lowercase']
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()[:-1]  # remove newline
        self.assertRegex(
            result,
            r'[a-z\-]+'
        )

    def test_main_option_password_use_digits(self):
        arg = ['--password', '--use-digits']
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()[:-1]  # remove newline
        self.assertRegex(
            result,
            r'[\d]+'
        )

    def test_main_option_password_use_alphanumeric(self):
        arg = ['--password', '--use-alphanumeric']
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()[:-1]  # remove newline
        self.assertRegex(
            result,
            r'[a-zA-Z\d\-]+'
        )

    def test_main_option_password_use_punctuation(self):
        arg = ['--password', '--use-punctuation']
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()[:-1]  # remove newline
        self.assertRegex(
            result,
            r'[\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_'
            r'\`\{\|\}\~]+'
        )

    @mock.patch.object(Aux, 'print_stderr')
    def test_main_option_words(self, mock_print_stderr):
        args = (
            ['--words', '2'],
            ['-w', '2']
        )
        for arg in args:
            self.assertEqual(main(arg), 0)
            mock_print_stderr.assert_any_call(
                'Warning: insecure amount of words chosen! Should be bigger '
                'than or equal to 6'
            )
            mock_print_stderr.assert_any_call(
                'Warning: the passphrase is too short!'
            )
            result = sys.stdout.getvalue()[:-1]  # remove newline
            self.assertRegex(
                result,
                r'^([a-z\-]+[ ])+[a-z\-]+$'
            )
            sys.stdout = StringIO()  # reset

    def test_main_option_no_newline(self):
        arg = ['--no-newline']
        self.assertEqual(main(arg), 0)
        result = sys.stdout.getvalue()
        self.assertNotEqual(result[-1:], '\n')

    @mock.patch('passphrase.__main__.open')
    @mock.patch('passphrase.__main__.os_path_dirname')
    @mock.patch('passphrase.__main__.os_makedirs')
    def test_main_option_output(self, mock_makedirs, mock_dirname, mock_open):
        args = [
            ['--output', '/somedir/somefile'],
            ['-o', '/somedir/somefile']
        ]
        mock_dirname.return_value = '/somedir'
        mock_makedirs.return_value = True
        for arg in args:
            self.assertEqual(main(arg), 0)
            mock_dirname.assert_called_with('/somedir/somefile')
            mock_makedirs.assert_called_with('/somedir', exist_ok=True)
            mock_open.assert_called_with('/somedir/somefile',
                                         mode='wt', encoding='utf-8')


class TestInvalidInputs(TestCase):

    @mock.patch.object(Aux, 'print_stderr')
    @mock.patch('passphrase.__main__.open')
    @mock.patch('passphrase.__main__.os_path_dirname')
    @mock.patch('passphrase.__main__.os_makedirs')
    def test_main_option_output(self, mock_makedirs, mock_dirname, mock_open,
                                mock_print_stderr):
        args = [
            ['--output', '/somedir/somefile'],
            ['-o', '/somedir/somefile']
        ]
        mock_dirname.return_value = '/somedir'
        mock_makedirs.side_effect = PermissionError()
        for arg in args:
            self.assertEqual(main(arg), 1)
            mock_dirname.assert_called_with('/somedir/somefile')
            mock_makedirs.assert_called_with('/somedir', exist_ok=True)
            mock_print_stderr.assert_called_with(
                'Error: permission denied to create directory /somedir'
            )
        mock_makedirs.side_effect = None
        mock_open.side_effect = IOError()
        for arg in args:
            self.assertEqual(main(arg), 1)
            mock_dirname.assert_called_with('/somedir/somefile')
            mock_makedirs.assert_called_with('/somedir', exist_ok=True)
            mock_print_stderr.assert_called_with(
                "Error: file /somedir/somefile can't be opened or written"
            )

    @mock.patch.object(Passphrase, 'import_words_from_file')
    @mock.patch.object(Aux, 'print_stderr')
    def test_main_option_input(self, mock_print_stderr, mock_import_file):
        args = [
            ['--input', '/somedir/somefile'],
            ['-i', '/somedir/somefile']
        ]
        mock_import_file.side_effect = IOError()
        for arg in args:
            self.assertEqual(main(arg), 1)
            mock_print_stderr.assert_called_with(
                "Error: input file /somedir/somefile is empty or it can't be "
                "opened or read"
            )
