import unittest
from app.zordon import ZordonBot


class TestLaunch(unittest.TestCase):
    def test_basic_launch(self):
        bot_instance = ZordonBot()
        bot_instance.updater.stop()

if __name__ == '__main__':
    unittest.main()
