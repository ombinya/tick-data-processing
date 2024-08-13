import unittest
from ..refiner import Refiner
import os


class TestRefiner(unittest.TestCase):
    def setUp(self):
        # Directory of the current script
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the db file
        self.dbfilepath = os.path.join(self.current_dir, '..', 'data', 'eurusd.db')

        self.refiner = Refiner(self.dbfilepath)

    def test_db_file_exists(self):
        self.assertTrue(self.refiner.db_file_exists())

        falsefilepath = os.path.join(self.current_dir, '..', 'data', 'falsefile.db')
        self.refiner.dbfilepath = falsefilepath

        self.assertFalse(self.refiner.db_file_exists())


if __name__ == "__main__":
    unittest.main()
