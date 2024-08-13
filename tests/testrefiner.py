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

    def test_get_segments(self):
        selection = [
            (1707922800, .1),  # 2024-02-14 18:00
            (1707922800 + (60 * 9), .1),  # 2024-02-14 18:09
            (1707922800 + (60 * 10), .1),  # 2024-02-14 18:10
            (1707922800 + (60 * 19), .1),  # 2024-02-14 18:19
            (1707922800 + (60 * 20), .1),  # 2024-02-14 18:20
            (1707922800 + (60 * 29), .1),  # 2024-02-14 18:29
            (1707922800 + (60 * 30), .1),  # 2024-02-14 18:30
            (1707922800 + (60 * 39), .1),  # 2024-02-14 18:39
            (1707922800 + (60 * 40), .1),  # 2024-02-14 18:40
            (1707922800 + (60 * 49), .1),  # 2024-02-14 18:49
            (1707922800 + (60 * 50), .1),  # 2024-02-14 18:50
            (1707922800 + (60 * 59), .1),  # 2024-02-14 18:59
        ]

        expected = [
            [(1707922800, .1), (1707922800 + (60 * 9), .1)],
            [(1707922800 + (60 * 10), .1), (1707922800 + (60 * 19), .1)],
            [(1707922800 + (60 * 20), .1), (1707922800 + (60 * 29), .1)],
            [(1707922800 + (60 * 30), .1), (1707922800 + (60 * 39), .1)],
            [(1707922800 + (60 * 40), .1), (1707922800 + (60 * 49), .1)],
            [(1707922800 + (60 * 50), .1), (1707922800 + (60 * 59), .1)]
        ]

        actual = self.refiner.get_segments(selection)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
