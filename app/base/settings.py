import dj_database_url
import logging
import os


# Required environment variables.
token = os.environ['ZORDON_TOKEN']
database = dj_database_url.parse(os.environ['ZORDON_DATABASE'])
superuser = os.environ['ZORDON_SUPERUSER']


# Optional environment variables.
def _get_verbosity():
    verbosity_levels = {
        'SILENT': logging.ERROR,     # Recommended for tests.
        'INFO': logging.INFO,        # Recommended for release.
        'DEBUG': logging.DEBUG + 1,  # Output only Zordon debug messages.
        'FULL': logging.DEBUG,       # All debug messages, including third-party.
    }
    return verbosity_levels[os.getenv('ZORDON_VERBOSITY', 'INFO')]
verbosity = _get_verbosity()
