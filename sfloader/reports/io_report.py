from sfloader.reports.base import BaseReport


class IOReport(BaseReport):
    def call(self, status, rows):
        print("\n\n")
        print(f"{status.upper()} REPORT")
        print(f"Rows: {len(rows)-1} received")
        [print(f"{row}\n") for row in rows]
        print("\n\n")
