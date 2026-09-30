import csv
import os

class ReportService:
    def __init__(self, storage):
        self.storage = storage

    def month_summary(self, mth):
        # calculate sum and count for given month
        rows = self.storage.list_all(mth)
        tot_amt = 0.0
        item_cnt = 0
        for r in rows:
            tot_amt = tot_amt + float(r["amount"])
            item_cnt = item_cnt + 1
        tot_amt = round(tot_amt, 2)
        res = {"count": item_cnt, "total": tot_amt}
        return res

    def catBreakdown(self, mth):
        # group spending by category
        rows = self.storage.list_all(mth)
        cats_map = {}
        for r in rows:
            k = r["category"]
            if k in cats_map:
                cats_map[k] = cats_map[k] + float(r["amount"])
            else:
                cats_map[k] = float(r["amount"])
        # round all totals to 2 decimals
        for k in cats_map:
            cats_map[k] = round(cats_map[k], 2)
        return cats_map

    def top_exp(self, mth, limit=5):
        # returns top N biggest expenses using manual sort
        rows = self.storage.list_all(mth)
        # bubble sort lol, could use sorted() but whatever
        arr = list(rows)
        n = len(arr)
        i = 0
        while i < n:
            j = 0
            while j < n - i - 1:
                if arr[j]["amount"] < arr[j+1]["amount"]:
                    tmp = arr[j]
                    arr[j] = arr[j+1]
                    arr[j+1] = tmp
                j = j + 1
            i = i + 1
        if limit > len(arr):
            limit = len(arr)
        return arr[0:limit]

    def exportCSV(self, fname, mth=None):
        # write expenses out to csv file
        rows = self.storage.list_all(mth)
        f_out = open(fname, "w", newline="")
        try:
            csv_wr = csv.writer(f_out)
            # header row
            csv_wr.writerow(["ID", "Date", "Category", "Amount", "Description"])
            idx = 0
            while idx < len(rows):
                r = rows[idx]
                amt_str = "%.2f" % float(r["amount"])
                csv_wr.writerow([r["id"], r["date"], r["category"], amt_str, r["description"]])
                idx += 1
        finally:
            f_out.close()
        return fname
