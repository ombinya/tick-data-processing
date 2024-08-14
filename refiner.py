from sqlite3 import connect
import os
from datetime import datetime


class Refiner:
    def __init__(self, asset):
        self.asset = asset
        # Directory of the current script
        self.currentdir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the source db file
        self.sourcedbfilepath = self.currentdir + "/data/" + asset + ".db"
        # Construct the path to the source db file
        self.destinationdbfilepath = self.currentdir + "/data/refined" + asset + ".db"
        # Each segment is 10 minutes (600 seconds) long; I need at least half number (300) of ticks
        self.minimumsegmentsize = int((10 * 60) / 2)

    def db_file_exists(self, filepath):
        return os.path.exists(filepath)

    def all_segments_valid(self, segments):
        for segment in segments:
            if len(segment) < self.minimumsegmentsize:
                return False

        return True

    def get_segments(self, selection):
        segments = [[] for i in range(6)]

        for row in selection:
            dateobj = datetime.fromtimestamp(row[0])
            segmentindex = dateobj.minute // 10
            segments[segmentindex].append(row)

        return segments

        # with connect(self.dbfilepath) as con:
        #     cur = con.cursor()
        #
        #     cur.execute(
        #         """SELECT * FROM frxEURUSD WHERE epoch >= 1707922800 AND epoch < 1707926400"""
        #     )
        #
        #     selection = cur.fetchall()
        #
        #     return len(selection)


if __name__ == "__main__":
    asset = "eurusd"
    refiner = Refiner(asset)

