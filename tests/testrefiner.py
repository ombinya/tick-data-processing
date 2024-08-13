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

    def test_all_segments_valid(self):
        segments = [[1 for i in range(self.refiner.minimumsegmentsize - 1)] for j in range(6)]
        self.assertFalse(self.refiner.all_segments_valid(segments))

        segments = [[1 for i in range(self.refiner.minimumsegmentsize)] for j in range(6)]
        self.assertTrue(self.refiner.all_segments_valid(segments))

        segments = [[1 for i in range(self.refiner.minimumsegmentsize + 1)] for j in range(6)]
        self.assertTrue(self.refiner.all_segments_valid(segments))


if __name__ == "__main__":
    unittest.main()
