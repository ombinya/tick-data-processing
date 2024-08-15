import unittest
from ..refiner import Refiner
import os


class TestRefiner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up class")
        asset = "eurusd"
        cls.refiner = Refiner(asset)

        cls.selection = [
            (1707922800, .1),  # 2024-02-14 18:00
            (1707922800 + (60 * 9), .1),  # 2024-02-14 18:09
            (1707922800 + (60 * 10), .2),  # 2024-02-14 18:10
            (1707922800 + (60 * 19), .3),  # 2024-02-14 18:19
            (1707922800 + (60 * 20), .4),  # 2024-02-14 18:20
            (1707922800 + (60 * 29), .5),  # 2024-02-14 18:29
            (1707922800 + (60 * 30), .6),  # 2024-02-14 18:30
            (1707922800 + (60 * 39), .7),  # 2024-02-14 18:39
            (1707922800 + (60 * 40), .8),  # 2024-02-14 18:40
            (1707922800 + (60 * 49), .9),  # 2024-02-14 18:49
            (1707922800 + (60 * 50), .8),  # 2024-02-14 18:50
            (1707922800 + (60 * 59), .7),  # 2024-02-14 18:59
        ]

        cls.segments = [
            [(1707922800, .1), (1707922800 + (60 * 9), .1)],
            [(1707922800 + (60 * 10), .2), (1707922800 + (60 * 19), .3)],
            [(1707922800 + (60 * 20), .4), (1707922800 + (60 * 29), .5)],
            [(1707922800 + (60 * 30), .6), (1707922800 + (60 * 39), .7)],
            [(1707922800 + (60 * 40), .8), (1707922800 + (60 * 49), .9)],
            [(1707922800 + (60 * 50), .8), (1707922800 + (60 * 59), .7)]
        ]

        cls.selection_averages = [.1, .25, .45, .65, .85, .75]
        cls.selection_comparisons = "UUUUD"

    def test_refine_data(self):
        print("Testing refine_data")
        # self.assertFalse(self.refiner.db_file_exists(self.refiner.destinationdbfilepath))
        # self.refiner.refine_data()
        # self.assertTrue(self.refiner.db_file_exists(self.refiner.destinationdbfilepath))

    def test_create_destination_db_file(self):
        print("Testing create_destination_db_file")
        self.assertFalse(self.refiner.db_file_exists(self.refiner.destinationdbfilepath))
        self.refiner.create_destination_db_file()
        self.assertTrue(self.refiner.db_file_exists(self.refiner.destinationdbfilepath))

    def test_db_file_exists(self):
        print("Testing db_file_exists")
        self.assertTrue(self.refiner.db_file_exists(self.refiner.sourcedbfilepath))
        falserefiner = Refiner("asset")
        self.assertFalse(falserefiner.db_file_exists(falserefiner.sourcedbfilepath))

    def test_all_segments_valid(self):
        print("Testing all_segments_valid")
        segments = [[1 for i in range(self.refiner.minimumsegmentsize - 1)] for j in range(6)]
        self.assertFalse(self.refiner.all_segments_valid(segments))

        segments = [[1 for i in range(self.refiner.minimumsegmentsize)] for j in range(6)]
        self.assertTrue(self.refiner.all_segments_valid(segments))

        segments = [[1 for i in range(self.refiner.minimumsegmentsize + 1)] for j in range(6)]
        self.assertTrue(self.refiner.all_segments_valid(segments))

    def test_get_segments(self):
        print("Testing get_segments")

        actual = self.refiner.get_segments(self.selection)
        expected = self.segments
        self.assertEqual(actual, expected)

    def test_get_selection_averages(self):
        actual = self.refiner.get_selection_averages(self.segments)
        expected = self.selection_averages

        for pair in zip(actual, expected):
            self.assertAlmostEqual(*pair)

    def test_get_selection_comparisons(self):
        actual = self.refiner.get_selection_comparisons(self.selection_averages)
        expected = self.selection_comparisons

        self.assertEqual(actual, expected)

    @classmethod
    def tearDownClass(cls):
        print("Running teardown")
        try:
            os.remove(cls.refiner.destinationdbfilepath)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
