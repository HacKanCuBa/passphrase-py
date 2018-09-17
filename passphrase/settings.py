"""Settings file for Passphrase modules."""

# Random numbers in passphrases are generated in the range [MIN_NUM, MAX_NUM].
# Scope: all
# Type: integer
# Default: 100000 and 999999
MIN_NUM = 100000
MAX_NUM = 999999

# Minimal amount of entropy bits desired and recommended to use.
# Scope: all
# Type: integer
# Default: 77 (from EFF's post: http://bit.ly/2hlExE6)
ENTROPY_BITS_MIN = 77

# Minimal amount of entropy bits that must be available on the system.
# Scope: script
# Type: integer
# Default: 128 (os.urandom might hang if lower than 128)
SYSTEM_ENTROPY_BITS_MIN = 128
