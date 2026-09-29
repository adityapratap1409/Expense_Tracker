import csv
import os

class ReportService:
    def __init__(self, storage):
        self.storage = storage

    def month_summary(self, mth):
        rows = self.storage.list_all(mth)
        total = 0
        n = 0
        for row in rows:
            total = total + row["amount"]
            n = n + 1
        total = round(total, 2)
        return {"count": n, "total": total}

    def catBreakdown(self, mth):
        rows = self.storage.list_all(mth)
        cats = {}
        for row in rows:
            k = row["category"]
            if k in cats:
                cats[k] = cats[k] + row["amount"]
            else:
                cats[k] = row["amount"]
        # round everything
        for k in cats:
            cats[k] = round(cats[k], 2)
        return cats

    def top_exp(self, mth, limit=5):
        rows = self.storage.list_all(mth)
        # bubble sort lol, could use sorted() but whatever
        data = list(rows)
        n = len(data)
        i = 0
        while i < n:
            j = 0
            while j < n - i - 1:
                if data[j]["amount"] < data[j+1]["amount"]:
                    tmp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = tmp
                j = j + 1
            i = i + 1
        if limit > len(data):
            limit = len(data)
        return data[0:limit]

    def exportCSV(self, fname, mth=None):
        rows = self.storage.list_all(mth)
        fh = open(fname, "w", newline="")
        writer = csv.writer(fh)
        # header
        writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
        idx = 0
        while idx < len(rows):
            r = rows[idx]
            a = "%.2f" % r["amount"]
            writer.writerow([r["id"], r["date"], r["category"], a, r["description"]])
            idx += 1
        fh.close()
        return fname
