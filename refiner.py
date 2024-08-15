from sqlite3 import connect
import os
from datetime import datetime
from statistics import mean


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

            cur.execute("SELECT * FROM {} ORDER BY epoch DESC LIMIT 1".format(self.sourcetablename))
            lastrow = cur.fetchone()
            lastepoch = lastrow[0]
            endepoch = int(lastepoch)

            data = []
            counter = 0
            previousday = None

            for i in range(startepoch, endepoch, 3600):
                j = i + 3600

                selection = cur.execute("""
                    SELECT * FROM {}
                    WHERE (epoch >= {} AND epoch < {})
                """.format(self.sourcetablename, i, j)).fetchall()

                segments = self.get_segments(selection)
                
                if self.all_segments_valid(segments):
                    selectionaverages = self.get_selection_averages(segments)
                    selectioncomparisons = self.get_selection_comparisons(selectionaverages)
                    openingprice = selection[0][1]
                    closingprice = selection[-1][1]

                    hourcomparison = self.comparison(openingprice, closingprice)
                else:
                    selectioncomparisons = "-"
                    hourcomparison = "-"

                openingdatetime = datetime.fromtimestamp(i)

                data.append([
                    openingdatetime.year,
                    openingdatetime.month,
                    openingdatetime.day,
                    openingdatetime.hour,
                    selectioncomparisons,
                    hourcomparison
                ])

                if previousday != openingdatetime.day:
                    print("Day:", openingdatetime)
                    previousday = openingdatetime.day

                # counter += 1
                # if counter == 24:
                #     break

            for i in range(len(data) - 1):
                nexthourcomparison = data[i + 1][-1]
                data[i].append(nexthourcomparison)

            print("Inserting data")
            self.insert_data(data[:-1])
            print("Done!")

    def create_destination_db_file(self):
        try:
            os.remove(self.destinationdbfilepath)
        except FileNotFoundError:
            pass

        with connect(self.destinationdbfilepath) as con:
            cur = con.cursor()

            cur.execute("""
                CREATE TABLE data (year, month, day, hour, segment_comparisons, hour_comparison, next_hour_comparison)
            """)

        con.close()

    def db_file_exists(self, filepath):
        return os.path.exists(filepath)

    def get_segments(self, selection):
        segments = [[] for i in range(6)]

        for row in selection:
            dateobj = datetime.fromtimestamp(row[0])
            segmentindex = dateobj.minute // 10
            segments[segmentindex].append(row)

        return segments
    
    def all_segments_valid(self, segments):
        for segment in segments:
            if len(segment) < self.minimumsegmentsize:
                return False

        return True

    def get_selection_averages(self, segments):
        averages = []

        for segment in segments:
            prices = [row[1] for row in segment]
            segmentaverage = mean(prices)
            averages.append(segmentaverage)

        return averages

    def get_selection_comparisons(self, averages):
        comparisons = []
        for i in range(len(averages) - 1):
            a = averages[i]
            b = averages[i + 1]

            comparison = self.comparison(a, b)
            comparisons.append(comparison)

        return "".join(comparisons)

    def comparison(self, a, b):
        if a > b:
            return "D"
        elif a < b:
            return "U"
        else:
            return "X"

    def insert_data(self, data):
        with connect(self.destinationdbfilepath) as con:
            cur = con.cursor()

            cur.executemany("""
                INSERT INTO data
                VALUES (?,?,?,?,?,?,?)
            """, data)

        con.close()


if __name__ == "__main__":
    asset = "eurusd"
    refiner = Refiner(asset)
    refiner.refine_data()

