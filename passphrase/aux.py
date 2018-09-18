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

"""Auxiliar functions."""

from subprocess import Popen, PIPE, DEVNULL
from os.path import isfile, getsize
from typing import Union
from sys import stderr

from .secrets import randbelow


__version__ = '0.2.3'


class Aux:
    """Auxiliar functions."""

    @staticmethod
    def lowercase_chars(string: any) -> str:
        """Return all (and only) the lowercase chars in the given string."""
        return ''.join([c if c.islower() else '' for c in str(string)])

    @staticmethod
    def uppercase_chars(string: any) -> str:
        """Return all (and only) the uppercase chars in the given string."""
        return ''.join([c if c.isupper() else '' for c in str(string)])

    @staticmethod
    def chars(string: any) -> str:
        """Return all (and only) the chars in the given string."""
        return ''.join([c if c.isalpha() else '' for c in str(string)])

    @staticmethod
    def lowercase_count(string: any) -> int:
        """Return the number of lowercase chars in the given string."""
        return len(Aux.lowercase_chars(string))

    @staticmethod
    def uppercase_count(string: any) -> int:
        """Return the number of uppercase chars in the given string."""
        return len(Aux.uppercase_chars(string))

    @staticmethod
    def chars_count(string: any) -> int:
        """Return the number of chars in the given string."""
        return len(Aux.chars(string))

    @staticmethod
    def make_all_uppercase(
            lst: Union[list, tuple, str, set]
    ) -> Union[list, tuple, str, set]:
        """Make all characters uppercase.

        It supports characters in a (mix of) list, tuple, set or string.
        The return value is of the same type of the input value.

        """
        if not isinstance(lst, (list, tuple, str, set)):
            raise TypeError('lst must be a list, a tuple, a set or a string')

        if isinstance(lst, str):
            return lst.upper()

        arr = list(lst)

        # enumerate is 70% slower than range
        # for i in range(len(lst)):
        #     if isinstance(arr[i], (list, tuple, str, set)):
        #         arr[i] = Aux.make_all_uppercase(arr[i])
        arr[:] = [
            Aux.make_all_uppercase(element) if (
                isinstance(element, (list, tuple, str, set))
            ) else element for element in arr
        ]

        if isinstance(lst, set):
            return set(arr)
        elif isinstance(lst, tuple):
            return tuple(arr)

        return arr

    @staticmethod
    def _make_one_char_uppercase(string: str) -> str:
        """Make a single char from the string uppercase."""
        if not isinstance(string, str):
            raise TypeError('string must be a string')

        if Aux.lowercase_count(string) > 0:
            while True:
                cindex = randbelow(len(string))
                if string[cindex].islower():
                    aux = list(string)
                    aux[cindex] = aux[cindex].upper()
                    string = ''.join(aux)
                    break

        return string

    @staticmethod
    def make_chars_uppercase(
            lst: Union[list, tuple, str, set],
            uppercase: int
    ) -> Union[list, tuple, str, set]:
        """Make uppercase some randomly selected characters.

        The characters can be in a (mix of) string, list, tuple or set.

        Keyword arguments:
        lst -- the object to make all chars uppercase, which can be a (mix of)
        list, tuple, string or set.
        uppercase -- Number of characters to be set as uppercase.

        """
        if not isinstance(lst, (list, tuple, str, set)):
            raise TypeError('lst must be a list, a tuple, a set or a string')
        if not isinstance(uppercase, int):
            raise TypeError('uppercase must be an integer')
        if uppercase < 0:
            raise ValueError('uppercase must be bigger than zero')

        lowercase = Aux.lowercase_count(lst)
        if uppercase == 0 or lowercase == 0:
            return lst
        elif uppercase >= lowercase:
            # Make it all uppercase
            return Aux.make_all_uppercase(lst)

        arr = list(lst)

        # Check if at least an element is supported
        # This is required to avoid an infinite loop below
        supported = False
        for element in arr:
            if isinstance(element, (list, tuple, str, set)):
                supported = True
                break

        if supported:
            # Pick a word at random, then make a character uppercase
            count = 0
            while count < uppercase:
                windex = randbelow(len(arr))
                element = arr[windex]
                # Skip unsupported types or empty ones
                if element:
                    aux = element
                    if isinstance(element, str):
                        aux = Aux._make_one_char_uppercase(element)
                    elif isinstance(element, (list, tuple, set)):
                        aux = Aux.make_chars_uppercase(element, 1)

                    if aux != element:
                        arr[windex] = aux
                        count += 1

        if isinstance(lst, set):
            return set(arr)
        elif isinstance(lst, str):
            return ''.join(arr)
        elif isinstance(lst, tuple):
            return tuple(arr)

        return arr

    @staticmethod
    def isfile_notempty(inputfile: str) -> bool:
        """Check if the input filename with path is a file and is not empty."""
        try:
            return isfile(inputfile) and getsize(inputfile) > 0
        except TypeError:
            raise TypeError('inputfile is not a valid type')

    @staticmethod
    def print_stderr(string: str) -> None:
        """Print the given string to STDERR."""
        print("{}".format(string), file=stderr)

    @staticmethod
    def system_entropy():
        """Return the system's entropy bit count, or -1 if unknown."""
        arg = ['cat', '/proc/sys/kernel/random/entropy_avail']
        proc = Popen(arg, stdout=PIPE, stderr=DEVNULL)
        response = proc.communicate()[0]
        return int(response) if response else -1
