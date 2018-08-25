from pathlib import Path
import os

TEST_DATA_DIR = Path(os.path.realpath(__file__)).parent.joinpath('data')


class MatcherAny:
    def __eq__(self, _):
        return True
