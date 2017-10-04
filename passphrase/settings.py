"""Settings file for Passphrase modules"""

# Set to False to avoid even trying to use NumPy
TRY_NUMPY = True

# Random numbers in passphrases are generated in the range [MIN_NUM, MAX_NUM]
MIN_NUM = 100000
MAX_NUM = 999999

# Default minimal ammount of entropy bits
ENTROPY_BITS_MIN = 77  # From EFF's post: http://bit.ly/2hlExE6
