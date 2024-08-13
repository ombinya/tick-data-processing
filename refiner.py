from sqlite3 import connect
import os


class Refiner:
    def __init__(self, dbfilepath):
        self.dbfilepath = dbfilepath
        # Each segment is 10 minutes (600 seconds) long; I need at least half number (300) of ticks
        self.minimumsegmentsize = (10 * 60) / 2

    def db_file_exists(self):
        return os.path.exists(self.dbfilepath)


if __name__ == "__main__":
    dbfilepath = "data/eurusd.db"
    refiner = Refiner(dbfilepath)

