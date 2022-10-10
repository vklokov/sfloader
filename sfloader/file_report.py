import csv
from sfloader.base_report import BaseReport


class FileReport(BaseReport):
    def __init__(self, output):
        self.output = output

    def call(self, status, rows):
        with open(f"{self.output}.{status}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerows(rows)
