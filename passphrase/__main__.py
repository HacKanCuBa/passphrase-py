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
"""Passphrase - Generates cryptographically secure passphrases and passwords.

Passphrases are built by picking from a word list using cryptographically
secure random number generator. Passwords are built from printable characters.
by HacKan (https://hackan.net) under GNU GPL v3.0+.

"""

import argparse
import os
import sys
import typing

from .aux import Aux
from .passphrase import Passphrase
from .secrets import randbool
from .settings import ENTROPY_BITS_MIN
from .settings import SYSTEM_ENTROPY_BITS_MIN

__author__ = 'HacKan'
__license__ = 'GNU GPL 3.0+'
__version__ = '1.2.1'
__version_string__ = f'Passphrase v{__version__}\n'
__version_string__ += 'by HacKan (https://hackan.net) FOSS under GNU GPL v3.0 or newer'


class CLIError(Exception):
    """Base exception for CLI errors."""

    def __str__(self) -> str:
        """Human readable representation of the exception."""
        return f'Error: {super().__str__()}'


class CheckFailedError(CLIError):
    """Check has failed error."""


class FileError(CLIError):
    """File related error."""


def print_stderr(obj: object) -> None:
    """Print given objet to stderr."""
    if not isinstance(obj, str) and isinstance(obj, typing.Iterable):
        print(' '.join(obj), file=sys.stderr)
    else:
        print(obj, file=sys.stderr)


def print_warning(string: str) -> None:
    """Print a warning message to stderr."""
    print('Warning:', string, file=sys.stderr)


def _bigger_than_zero(value: str) -> int:
    """Type evaluator for argparse."""
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f'{ivalue} should be bigger than 0')

    return ivalue


def parse_args(args: typing.Optional[typing.Sequence[str]] = None) -> argparse.Namespace:
    """Parse given arguments or optionally use sys.argv instead."""
    parser = argparse.ArgumentParser(
        description='Generate a cryptographically secure passphrase (by'
                    ' default), a password, an UUIDv4 or a coin throw, and '
                    'print it to the standard output or file. Passphrases are '
                    "generated using an embedded EFF's Large wordlist or "
                    'optionally an external one. By '
                    'default, they are 6 words long (for the EFF wordlist), '
                    'and less than that is '
                    'considered insecure. It is recommended to add a number. '
                    'Passwords are random strings of printable characters. By '
                    'default, they use uppercase, lowercase, digits and '
                    'punctuation and 12 characters long, and less than that '
                    'is considered insecure. It is recommended to use 16 or '
                    'more characters. UUIDv4 follows the standard format. '
                    'Coin throwing can output Heads or Tails. All defaults '
                    'are based on entropy, and so are calculations, being 77 '
                    'bits the minimum.',
        epilog=__version_string__,
    )

    passphrase_group = parser.add_argument_group(title='Passphrase arguments')
    password_group = parser.add_argument_group(title='Password arguments')
    others_group = parser.add_argument_group(title='Other generators')

    parser.add_argument(
        '--version',
        action='store_true',
        help='print program version and licensing information and exit',
    )
    parser.add_argument(
        '--insecure',
        action='store_true',
        default=False,
        help="force generation even if the system's entropy is too low",
    )
    parser.add_argument(
        '--no-newline',
        action='store_true',
        default=False,
        help="don't print newline at the end",
    )
    parser.add_argument(
        '-m',
        '--mute',
        action='store_true',
        default=False,
        help="muted mode: it won't print output, only informational, warning "
             'or error messages (usefull with -o | --output)',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='print additional information (can coexist with -m | --mute)',
    )
    parser.add_argument(
        '-e',
        '--entropybits',
        type=_bigger_than_zero,
        default=ENTROPY_BITS_MIN,
        help=f'specify the number of bits to use for entropy calculations '
             f'(defaults to {ENTROPY_BITS_MIN})',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='specify an output file (existing file is overwritten)',
    )

    others_group.add_argument(
        '--uuid4',
        action='store_true',
        default=False,
        help='generate an UUID v4 string',
    )
    others_group.add_argument(
        '--coin',
        action='store_true',
        default=False,
        help='generate a random coin throw: heads or tails',
    )

    password_group.add_argument(
        '-p',
        '--password',
        type=_bigger_than_zero,
        const=0,
        nargs='?',
        help='generate a password of the specified length from all printable '
             'or selected characters',
    )
    password_group.add_argument(
        '--use-uppercase',
        action='store_true',
        default=False,
        help='use uppercase characters for password generation',
    )
    password_group.add_argument(
        '--use-lowercase',
        action='store_true',
        default=False,
        help='use lowercase characters for password generation',
    )
    password_group.add_argument(
        '--use-digits',
        action='store_true',
        default=False,
        help='use digits for password generation',
    )
    password_group.add_argument(
        '--use-alphanumeric',
        action='store_true',
        default=False,
        help='use lowercase and uppercase characters, and digits for password '
             'generation (equivalent to --use-lowercase --use-uppercase '
             '--use-digits)',
    )
    password_group.add_argument(
        '--use-punctuation',
        action='store_true',
        default=False,
        help='use punctuation characters for password generation',
    )
    passphrase_group.add_argument(
        '-w',
        '--words',
        type=_bigger_than_zero,
        help='specify the amount of words (0 or more)',
    )
    passphrase_group.add_argument(
        '-n',
        '--numbers',
        type=_bigger_than_zero,
        default=0,
        help='specify the amount of numbers (they are between 100000 and '
             '999999) (0 or more)',
    )
    passphrase_group.add_argument(
        '-s',
        '--separator',
        type=str,
        default=' ',
        help='specify a separator character (space by default)',
    )
    passphrase_group.add_argument(
        '--uppercase',
        type=_bigger_than_zero,
        const=0,
        nargs='?',
        help='specify the amount of uppercase characters in the passphrase: '
             'zero or no input for all of them or any number of uppercase '
             'characters wanted (the rest are changed to lowercase)',
    )
    passphrase_group.add_argument(
        '--lowercase',
        type=_bigger_than_zero,
        const=0,
        nargs='?',
        help='specify the amount of lowercase characters in the passphrase: '
             'zero or no input for all of them (default) or any number of '
             'lowercase characters wanted (the rest are changed to uppercase)',
    )
    passphrase_group.add_argument(
        '-i',
        '--input',
        type=str,
        help='specify an input file (it must have the following format: '
             'single column, one word per line)',
    )
    passphrase_group.add_argument(
        '-d',
        '--diceware',
        action='store_true',
        default=False,
        help='the input file is a diceware list (two colums format)',
    )

    return parser.parse_args(args)


def generate_passphrase(  # noqa: R701
        *,
        entropy_bits_req: typing.Union[float, int],
        input_: typing.Optional[str],
        diceware: bool,
        numbers: int,
        words: typing.Optional[int],
        lowercase: int,
        uppercase: int,
        separator: str,
) -> Passphrase:
    """Generate passphrase with given settings and return a Passphrase object."""
    try:
        # ToDo: always load internal wordlist unless an input is specified!
        passphrase = Passphrase(input_ or 'internal', diceware)
    except IOError:
        raise FileError(
            f"input file {input_} is empty or it can't be opened or read",
        )

    passphrase.entropy_bits_req = entropy_bits_req

    # ToDo: calculate de amount of numbers needed when words are fixed, the same
    #  way words are calculated when numbers are fixed.
    passphrase.amount_n = numbers
    amount_w_good = passphrase.words_amount_needed()
    amount_w = amount_w_good if words is None else words
    if amount_w < amount_w_good:
        print_warning(
            f'insecure amount of words chosen! Should be bigger than or equal '
            f'to {amount_w_good}',
        )
    passphrase.amount_w = amount_w

    passphrase.separator = separator
    case = (-1 * lowercase) if lowercase else uppercase
    passphrase.generate(case)

    return passphrase


def generate_password(  # noqa: R701
        *,
        entropy_bits_req: typing.Union[float, int],
        length: int,
        use_uppercase: bool,
        use_lowercase: bool,
        use_digits: bool,
        use_punctuation: bool,
        use_alphanumeric: bool,
) -> Passphrase:
    """Generate password with given settings and return a Passphrase object."""
    # ToDo: split this class
    passphrase = Passphrase()
    passphrase.entropy_bits_req = entropy_bits_req

    any_setting = any((
        use_uppercase,
        use_lowercase,
        use_digits,
        use_punctuation,
        use_alphanumeric,
    ))
    if any_setting:
        passphrase.password_use_uppercase = use_uppercase or use_alphanumeric
        passphrase.password_use_lowercase = use_lowercase or use_alphanumeric
        passphrase.password_use_digits = use_digits or use_alphanumeric
        passphrase.password_use_punctuation = use_punctuation

    min_len = passphrase.password_length_needed()
    passphrase.passwordlen = min_len if length < 1 else length
    if passphrase.passwordlen < min_len:
        print_warning(
            f'insecure password length chosen! Should be bigger than or equal '
            f'to {min_len}',
        )

    passphrase.separator = ''
    passphrase.generate_password()

    return passphrase


def generate_uuid4() -> Passphrase:
    """Generate a UUID4 and return a Passphrase object."""
    passphrase = Passphrase()

    passphrase.separator = '-'
    passphrase.generate_uuid4()

    return passphrase


def check_entropy(  # noqa: R701
        *,
        insecure: bool,
        verbose: bool,
        entropybits: int,
        coin: bool,
        uuid4: bool,
        numbers: bool,
        words: bool,
        password: bool,
) -> None:
    """Check system and user selected entropy."""
    # Check system entropy
    system_entropy = Aux.system_entropy()
    if system_entropy < SYSTEM_ENTROPY_BITS_MIN:
        if insecure:
            print_warning(
                f'the system has too few entropy: {system_entropy} bits; '
                f'randomness quality could be poor',
            )
        else:
            raise CheckFailedError(
                f'system entropy too low: {system_entropy} < {SYSTEM_ENTROPY_BITS_MIN}',
            )

    if verbose:
        print_stderr(
            f'Using {entropybits} bits of entropy for calculations (if any). '
            f'The minimum recommended is {ENTROPY_BITS_MIN}',
        )

    # Check selected entropy
    # Only check whenever the generation mode implies an entropy calculation
    check_chosen_entropy = (
            (not coin)
            and (not uuid4)
            and (not numbers or not words or password is not None)
    )
    if check_chosen_entropy and entropybits < ENTROPY_BITS_MIN:
        print_warning(
            f'insecure number of bits for entropy calculations chosen! Should '
            f'be bigger than {ENTROPY_BITS_MIN}',
        )


def _ensure_dir(filename: str) -> None:
    """Ensure directory exists for given filename."""
    # ensure path to file exists or create
    dir_ = os.path.dirname(filename)
    if dir_:
        try:
            os.makedirs(dir_, exist_ok=True)
        except PermissionError:
            raise FileError(f'permission denied to create directory {dir_}')


def write_output_file(
        *,
        output: str,
        passphrase: Passphrase,
        end_of_line: str,
) -> None:
    """Write given passphrase result to a file."""
    _ensure_dir(output)
    try:
        with open(output, mode='wt', encoding='utf-8') as outfile:
            outfile.write(f'{passphrase}{end_of_line}')

    except IOError:
        raise FileError(f"file {output} can't be opened or written")


def main() -> None:  # noqa: C901 R701
    """Passphrase CLI interface."""
    args = parse_args()

    if args.version:
        print(__version_string__)
        return

    if args.verbose:
        print_stderr(__version_string__)

    check_entropy(
        entropybits=args.entropybits,
        words=args.words,
        numbers=args.numbers,
        password=args.password,
        verbose=args.verbose,
        insecure=args.insecure,
        uuid4=args.uuid4,
        coin=args.coin,
    )

    # Generate whatever is requested
    if args.uuid4:
        # Generate uuid4
        if args.verbose:
            print_stderr('Generating UUID v4')
        gen_what = 'UUID v4'
        gen_ent = 120.0

        passphrase = generate_uuid4()

    elif args.coin:
        # Generate a coin throw
        if args.verbose:
            print_stderr('Throwing a coin')
        gen_what = 'coin'
        gen_ent = 1.0

        # ToDo: change this so passphrase is of only one type!
        passphrase = 'Heads' if randbool() else 'Tails'

    elif args.password is not None:
        # Generate a password
        gen_what = 'password'
        passphrase = generate_password(
            entropy_bits_req=args.entropybits,
            length=args.password,
            use_uppercase=args.use_uppercase,
            use_lowercase=args.use_lowercase,
            use_digits=args.use_digits,
            use_punctuation=args.use_punctuation,
            use_alphanumeric=args.use_alphanumeric,
        )
        gen_ent = passphrase.generated_password_entropy()

        if args.verbose:
            password_options = []
            if passphrase.password_use_uppercase:
                password_options.append('uppercase characters')
            if passphrase.password_use_lowercase:
                password_options.append('lowercase characters')
            if passphrase.password_use_digits:
                password_options.append('digits')
            if passphrase.password_use_punctuation:
                password_options.append('punctuation characters')

            print_stderr(
                f'Generating password of {passphrase.passwordlen} characters long '
                f'using {", ".join(password_options)}',
            )

    else:
        # Generate a passphrase
        gen_what = 'passphrase'
        passphrase = generate_passphrase(
            entropy_bits_req=args.entropybits,
            input_=args.input,
            diceware=args.diceware,
            numbers=args.numbers,
            words=args.words,
            lowercase=args.lowercase,
            uppercase=args.uppercase,
            separator=args.separator,
        )

        gen_ent = passphrase.generated_passphrase_entropy()

        if args.verbose:
            generating_text = [
                f'Generating a passphrase of {passphrase.amount_w} words and '
                f'{passphrase.amount_n} numbers using',
            ]
            if args.input is None:
                generating_text.append('the internal wordlist')
            else:
                generating_text.append(f'an external wordlist: {args.input}')
                if args.diceware:
                    generating_text.append('(diceware-like)')
            print_stderr(generating_text)

    if args.verbose:
        print_stderr(f'The entropy of this {gen_what} is {gen_ent:.2f} bits')

    if not args.coin and gen_ent < ENTROPY_BITS_MIN:
        print_warning(
            f'the {gen_what} is too short! its entropy is lower than {ENTROPY_BITS_MIN}',
        )

    end_of_line = '' if args.no_newline else '\n'
    if not args.mute:
        print(passphrase, end=end_of_line)

    if args.output is not None:
        write_output_file(
            output=args.output,
            passphrase=passphrase,
            end_of_line=end_of_line,
        )


if __name__ == '__main__':
    try:
        main()
    except CLIError as exc:
        sys.exit(exc)
