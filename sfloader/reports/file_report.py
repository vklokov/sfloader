import csv
from sfloader.reports.base import BaseReport


class FileReport(BaseReport):
    def __init__(self, output):
        self.output = output

    def call(self, status, rows):
        with open(f"{self.output}.{status}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimeter=",")
            writer.writerows(rows)
