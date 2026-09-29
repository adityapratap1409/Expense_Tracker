import csv

class ReportService:
    def __init__(self, storage):
        self.storage = storage

    def month_summary(self, mth):
        rows = self.storage.list_all(mth)
        cnt = len(rows)
        tot = 0.0
        for r in rows:
            tot = tot + r["amount"]
        return {"count": cnt, "total": round(tot, 2)}

    def catBreakdown(self, mth):
        rows = self.storage.list_all(mth)
        by_cat = {}
        for r in rows:
            c = r["category"]
            if c not in by_cat:
                by_cat[c] = 0.0
            by_cat[c] = round(by_cat[c] + r["amount"], 2)
        return by_cat

    def top_exp(self, mth, limit=5):
        rows = self.storage.list_all(mth)
        top = sorted(rows, key=lambda x: x["amount"], reverse=True)
        return top[:limit]

    def exportCSV(self, fname, mth=None):
        rows = self.storage.list_all(mth)
        f = open(fname, "w", newline="", encoding="utf-8")
        w = csv.writer(f)
        w.writerow(["ID", "Date", "Category", "Amount", "Description"])
        for r in rows:
            amt_str = "%.2f" % r["amount"]
            w.writerow([r["id"], r["date"], r["category"], amt_str, r["description"]])
        f.close()
        return fname
