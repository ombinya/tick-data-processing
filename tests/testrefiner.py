import unittest
from ..refiner import Refiner


class TestRefiner(unittest.TestCase):
    def setUp(self):
        self.dbfilename = "somedb.db"
        refiner = Refiner(self.dbfilename)

    def test_db_file_exists():
        return False


if __name__ == "__main__":
    unittest.main()
