"""Passphrase - Generates cryptographically secure passphrases and passwords

Passphrases are built by picking from a word list using cryptographically
secure random number generator. Passwords are built from printable characters.
by HacKan (https://hackan.net) under GNU GPL v3.0+
"""

from sys import stderr, version_info, exit as sys_exit
import argparse
from .passphrase import Passphrase

__author__ = "HacKan"
__license__ = "GNU GPL 3.0+"
__version__ = "0.4.2"

assert (version_info >= (3, 2)), "This script requires Python 3.2+"


def print_stderr(string: str) -> None:
    print("{}".format(string), file=stderr)


def print_version() -> None:
    print("Passphrase v{}\nby HacKan (https://hackan.net) FOSS under GNU "
          "GPL v3.0 or newer".format(__version__))


def bigger_than_zero(value: int) -> int:
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(
            "{} should be bigger than 0".format(ivalue)
        )
    return ivalue


def main():
    passphrase = Passphrase()

    PASSWD_LEN_MIN_GOOD = passphrase.password_len_needed()
    WORDS_AMOUNT_MIN_DEFAULT = 6  # Just for EFF's Large Wordlist
    NUMS_AMOUNT_MIN_DEFAULT = 0

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Passphrase v{version} - Copyright HacKan '
        '(https://hackan.net) GNU GPL v3.0+.\n\n'
        'Generates a cryptographically secure passphrase, based on '
        'a wordlist, or a\npassword, and prints it to standard output.\n'
        'By default, it uses an embedded EFF Large Wordlist for passphrases.\n'
        'Passphrases with less than {wordsamountmin} words are considered '
        'insecure. A safe bet is \nbetween {wordsamountmin} and 7 words, '
        'plus at least a number.\n'
        'For passwords, use at least {passwdmin} characters, but prefer '
        '{passwdpref} or more.\n\n'
        'Instead of words and numbers, a password (random string of '
        'printable\ncharacters from Python String standard) can be generated '
        'by\n-p | --password, specifying the length.\n'
        'A custom wordlist can be specified by -i | --input, the format must '
        'be: \nsingle column, one word per line. If -d | --diceware is used, '
        'the input\nfile is treated as a diceware wordlist (two columns).'
        '\nOptionally, -o | --output can be used to specify an output file '
        '(existing \nfile is overwritten).\n'
        'The number of words is {wordsamountmin} by default, but it '
        'can be changed by -w | --words.\n'
        'The number of numbers is {numsamountmin} by default, but it can be '
        'changed by\n-n | --numbers. The generated numbers are between '
        '{minnum} and {maxnum}.\n'
        'The default separator is a blank space, but any character or '
        'character\nsequence can be specified by -s | --separator.\n'
        '\nExample output:\n'
        '\tDefault parameters:\tchalice sheath postcard modular cider size\n'
        '\tWords=3, Numbers=2:\tdepraved widow office 184022 320264\n'
        '\tPassword, 20 chars:\tsF#s@B+iR#ZIL-yUWKPR'.format(
            minnum=passphrase.randnum_min,
            maxnum=passphrase.randnum_max,
            wordsamountmin=WORDS_AMOUNT_MIN_DEFAULT,
            numsamountmin=NUMS_AMOUNT_MIN_DEFAULT,
            passwdmin=PASSWD_LEN_MIN_GOOD,
            passwdpref=PASSWD_LEN_MIN_GOOD + 4,
            version=__version__
        )
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="print program version and licensing information and exit"
    )
    parser.add_argument(
        "--newline",
        action="store_true",
        default=False,
        help="print newline at the end of the passphrase/password"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="quiet mode, it won't print anything but error messages "
             "(usefull with -o | --output)"
    )
    parser.add_argument(
        "-p",
        "--password",
        type=bigger_than_zero,
        const=PASSWD_LEN_MIN_GOOD,
        nargs='?',
        help="generate a password of specified length from all printable "
             "characters"
    )
    parser.add_argument(
        "-w",
        "--words",
        type=bigger_than_zero,
        help="specify the amount of words (0 or more)"
    )
    parser.add_argument(
        "-n",
        "--numbers",
        type=bigger_than_zero,
        default=NUMS_AMOUNT_MIN_DEFAULT,
        help="specify the amount of numbers (0 or more)"
    )
    parser.add_argument(
        "-s",
        "--separator",
        type=str,
        default=' ',
        help="specify a separator character (space by default)"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="specify an output file (existing file is overwritten)"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="specify an input file (it must have the following format: "
             "single column, one word per line)"
    )
    parser.add_argument(
        "-d",
        "--diceware",
        action="store_true",
        default=False,
        help="specify input file as a diceware list (format: two colums)"
    )

    args = parser.parse_args()

    inputfile = args.input
    outputfile = args.output
    separator = args.separator
    is_diceware = args.diceware
    passwordlen = args.password
    amount_w = args.words
    amount_n = args.numbers
    show_version = args.version
    quiet = args.quiet
    newline = args.newline

    if show_version is True:
        print_version()
        sys_exit()

    if inputfile is not None:
        try:
            passphrase.import_words_from_file(inputfile, is_diceware)
        except FileNotFoundError as err:
            print_stderr("Error: {}".format(err))
            sys_exit(1)

    if passwordlen is not None:
        if passwordlen < PASSWD_LEN_MIN_GOOD:
            print_stderr(
                "Warning: Insecure password length chosen! Should be bigger "
                "than or equal to {}".format(PASSWD_LEN_MIN_GOOD)
            )

        passphrase.passwordlen = passwordlen
        passphrase.generate_password()
        separator = ''
    else:
        passphrase.amount_n = amount_n
        amount_w_good = passphrase.words_amount_needed()
        if amount_w is None:
            amount_w = amount_w_good
        elif amount_w < amount_w_good:
            print_stderr(
                "Warning: Insecure amount of words chosen! Should be "
                "bigger than or equal to {}".format(amount_w_good)
            )

        passphrase.amount_w = amount_w
        passphrase.generate()

    passphrase.separator = separator

    if quiet is False:
        if newline is True:
            print(passphrase)
        else:
            print(passphrase, end='')

    if outputfile is not None:
        with open(outputfile, mode='wt', encoding='utf-8') as outfile:
            lf = '\n' if newline is True else ''
            outfile.write(str(passphrase) + lf)


if __name__ == "__main__":
    main()
