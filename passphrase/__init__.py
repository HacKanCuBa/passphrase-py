"""Passphrase - Generates cryptographically secure passphrases and passwords.

Passphrases are built by picking from a word list using cryptographically
secure random number generator. Passwords are built from printable characters.
by HacKan (https://hackan.net) under GNU GPL v3.0+.

"""

from .passphrase import Passphrase
from .aux import Aux

__all__ = ('Passphrase', 'Aux', )
