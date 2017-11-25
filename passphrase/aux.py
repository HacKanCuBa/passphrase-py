"""Aux: auxiliar functions"""


__version__ = "0.1.0"


class Aux():

    @staticmethod
    def lowercase_chars(s: any) -> str:
        return ''.join([c if c.islower() else '' for c in str(s)])

    @staticmethod
    def uppercase_chars(s: any) -> str:
        return ''.join([c if c.isupper() else '' for c in str(s)])

    @staticmethod
    def chars(s: any) -> str:
        return ''.join([c if c.isalpha() else '' for c in str(s)])

    @staticmethod
    def lowercase_count(s: any) -> int:
        return len(Aux.lowercase_chars(s))

    @staticmethod
    def uppercase_count(s: any) -> int:
        return len(Aux.uppercase_chars(s))

    @staticmethod
    def chars_count(s: any) -> int:
        return len(Aux.chars(s))

    @staticmethod
    def make_all_uppercase(lst: any) -> any:

        if not isinstance(lst, (list, tuple, str, set)):
            raise TypeError('lst must be a list, a tuple, a set or a string')

        if isinstance(lst, str):
            return lst.upper()

        arr = list(lst)

        # enumerate is 70% slower than range
        for i in range(len(lst)):
            if isinstance(arr[i], (list, tuple, str, set)):
                arr[i] = Aux.make_all_uppercase(arr[i])

        if isinstance(lst, set):
            return set(arr)
        elif isinstance(lst, tuple):
            return tuple(arr)

        return arr

    @staticmethod
    def isfile(inputfile: str) -> bool:
        from os.path import isfile

        try:
            return isfile(inputfile)
        except TypeError:
            raise TypeError('inputfile is not a valid type')

    @staticmethod
    def print_stderr(string: str) -> None:
        from sys import stderr

        print("{}".format(string), file=stderr)
