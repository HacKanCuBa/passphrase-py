#!/usr/bin/env python3

"""Download EFF Wordlist and create a usable word dictionary (removes
numerical column)"""


import os
import urllib.request
from passphrase import read_words_from_diceware


def diceware_to_words(filepath, output=None):
    words = read_words_from_diceware(filepath)
    if output is None:
        print('\n'.join(words))
    else:
        with open(output, mode='wt', encoding='utf-8') as wordsfile:
            wordsfile.write('\n'.join(words))


def get_eff_wordlist():
    wordlistfile = 'eff_large_wordlist.txt'
    with urllib.request.urlopen(
        'https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt'
    ) as response, open(wordlistfile, mode='wb') as out_file:
        data = response.read()
        out_file.write(data)

    return wordlistfile


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Download the EFF Large Wordlist and create a usable '
        'word dictionary from it. It outputs to standard ouput unless an '
        'output file is specified with -o | --output (existing file is '
        'overwritten).\n'
        'Optionally, use -i | --input to specify an input file (it must '
        'have the same format as any diceware word list).'
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
        help="specify an input file (it must have the same format as any "
             "diceware word list)"
    )

    args = parser.parse_args()

    if args.input is None:
        inputfile = get_eff_wordlist()
    elif os.path.isfile(args.input) is True:
        inputfile = args.input
    else:
        raise ValueError("Input file doesn't exist")

    diceware_to_words(filepath=inputfile, output=args.output)
