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

import subprocess
from unittest import TestCase

import passphrase.__main__


class TestValidInputs(TestCase):

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
            all([(c.islower() or c == ' ') for c in result])
        )
        # has 6 words
        self.assertEqual(len(result.split()), 6)

    def test_main_option_version(self):
        cmd = ['python3', '-m', 'passphrase', '--version']
        result = subprocess.run(
                                cmd,
                                stdout=subprocess.PIPE
                               ).stdout.decode('utf-8')
        self.assertEqual(result, passphrase.__main__.__version_string__ + '\n')

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
                passphrase.__main__.__version_string__,
                result
            )

    def test_main_option_insecure(self):
        # How can simulate low system entropy?? (without actually consuming
        # all of it...)
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
            '[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-'
            '[‌​0-9a-f]{12}'
        )

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
                '[a-zA-Z\d\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]'
                '\^\_\`\{\|\}\~]+'
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
            '[A-Z\-]+'
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
            '[a-z\-]+'
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
            '[\d]+'
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
            '[a-zA-Z\d\-]+'
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
            '[\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_'
            '\`\{\|\}\~]+'
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
                '^([a-z\-]+[ ])+[a-z\-]+$'
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
                '^([0-9]{6}[ ]){19}[0-9]{6}$'
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
                '^([a-z\-]+[\|])+[a-z\-]+$'
            )

    def test_main_option_output(self):
        from random import randint
        from tempfile import gettempdir
        from os.path import join as os_path_join, isfile as os_path_isfile

        tmpfile = os_path_join(
            gettempdir(),
            'passphrase_tests',
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
            with open(tmpfile, mode='rt', encoding='utf-8') as f:
                self.assertEqual(result, f.read())

    def test_main_option_input(self):
        from random import randint
        from tempfile import gettempdir
        from os.path import join as os_path_join

        words = [
            'vivacious',
            'frigidly',
            'condiment',
            'passive',
            'reverse',
            'brunt'
        ]
        tmpfile = os_path_join(
            gettempdir(),
            'passphrase_tests',
            'test_main_option_input.' + str(randint(100000, 999999))
        )
        with open(tmpfile, mode='wt+', encoding='utf-8') as wordfile:
            wordfile.write('\n'.join(words))

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
                self.assertIn(word, words)

    def test_main_option_input_diceware(self):
        from random import randint
        from tempfile import gettempdir
        from os.path import join as os_path_join

        wordsd = [
            '123456\tvivacious',
            '163456\tfrigidly',
            '153456\tcondiment',
            '143456\tpassive',
            '133456\tpenpal',
            '113456\talarm'
        ]
        words = [word.split()[1] for word in wordsd]
        tmpfile = os_path_join(
            gettempdir(),
            'passphrase_tests',
            'test_main_option_input.' + str(randint(100000, 999999))
        )
        with open(tmpfile, mode='wt+', encoding='utf-8') as wordfile:
            wordfile.write('\n'.join(wordsd))

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
            for word in result.split():
                self.assertIn(word, words)


class TestInvalidInputs(TestCase):

    def test_main(self):
        pass
