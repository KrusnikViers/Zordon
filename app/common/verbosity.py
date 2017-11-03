import logging
import os

_verbosity_levels = {
    'SILENT': logging.ERROR,  # Recommended for tests.
    'INFO': logging.INFO,  # Recommended for release.
    'DEBUG': logging.DEBUG + 1,  # Output only Zordon debug messages.
    'FULL': logging.DEBUG,  # All debug messages, including third-party.
}
level = _verbosity_levels[os.getenv('ZORDON_VERBOSITY', 'INFO')]

# Not used any more
del _verbosity_levels
