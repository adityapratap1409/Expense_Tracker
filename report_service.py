import csv


class ReportService:
    def __init__(self, storage):
        self.storage = storage

    def month_summary(self, mth):
        # total spent & transaction count for the month
        rows = self.storage.list_all(mth)
        cnt = len(rows)
        total = sum(r["amount"] for r in rows)
        return {"count": cnt, "total": round(total, 2)}

    def catBreakdown(self, mth):
        # group spending by category
        rows = self.storage.list_all(mth)
        by_cat = {}
        for r in rows:
            c = r["category"]
            by_cat[c] = round(by_cat.get(c, 0.0) + r["amount"], 2)
        return by_cat

    def top_exp(self, mth, limit=5):
        # highest spends first
        rows = self.storage.list_all(mth)
        top = sorted(rows, key=lambda x: x["amount"], reverse=True)
        return top[:limit]

    def exportCSV(self, fname, mth=None):
        # export to csv file
        rows = self.storage.list_all(mth)

        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Date", "Category", "Amount", "Description"])
            for r in rows:
                w.writerow(
                    [
                        r["id"],
                        r["date"],
                        r["category"],
                        f'{r["amount"]:.2f}',
                        r["description"],
                    ]
                )

        return fname
