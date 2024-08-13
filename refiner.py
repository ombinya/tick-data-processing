from sqlite3 import connect
import os


class Refiner:
    def __init__(self, dbfilepath):
        self.dbfilepath = dbfilepath

    def db_file_exists(self):
        return os.path.exists(self.dbfilepath)


if __name__ == "__main__":
    refiner = Refiner()
