import os
import pathlib


# RELEASE-UPDATE
APP_DIR = pathlib.Path(os.path.realpath(__file__)).parent.parent
PROJECT_NAME = 'Zordon'
PROJECT_VERSION = '3.1.0'
PROJECT_FULL_NAME = '{} v{}'.format(PROJECT_NAME, PROJECT_VERSION)
