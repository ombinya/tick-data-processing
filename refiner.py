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
        self.sourcetablename = "frxEURUSD"

        self.minimumsegmentsize = int((10 * 60) / 2)

    def refine_data(self):
        if not self.db_file_exists(self.sourcedbfilepath):
            print("The source db file for the asset '{}' does not exist".format(self.asset))
            return

        self.create_destination_db_file()

        with connect(self.sourcedbfilepath) as con:
            cur = con.cursor()

            cur.execute("SELECT * FROM {} LIMIT 1".format(self.sourcetablename))
            firstrow = cur.fetchone()
            firstepoch = firstrow[0]
            firstdatetime = datetime.fromtimestamp(firstepoch)
            firsthour = datetime(
                firstdatetime.year,
                firstdatetime.month,
                firstdatetime.day,
                firstdatetime.hour
            )

            startepoch = int(firsthour.timestamp())

            cur.execute("SELECT * FROM {} ORDER BY epoch DESC LIMIT 1;".format(self.sourcetablename))
            lastrow = cur.fetchone()
            lastepoch = lastrow[0]
            endepoch = int(lastepoch)

            for i in range(startepoch, endepoch, 3600):
                j = i + 3600

                selection = cur.execute("""
                    SELECT * FROM {}
                    WHERE (epoch >= {} AND epoch < {})
                """.format(self.sourcetablename, i, j)).fetchall()

                segments = self.get_segments(selection)

                print(segments[0])
                break

    def create_destination_db_file(self):
        try:
            os.remove(self.destinationdbfilepath)
        except FileNotFoundError:
            pass

        with connect(self.destinationdbfilepath) as con:
            cur = con.cursor()

            cur.execute("""
                CREATE TABLE data (year, month, day, hour, segment_comparisons, hour_comparison)
            """)

        con.close()

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
    refiner.refine_data()

