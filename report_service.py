import csv
class ReportService:
    def __init__(self, storage):
        self.storage = storage

    def monthly_summary(self, month):
        rows = self.storage.list_expenses(month)
        count = len(rows)
        total = sum(r["amount"] for r in rows)
        return {"count": count, "total": total}

    def category_breakdown(self, month):
        rows = self.storage.list_expenses(month)
        by_category = {}
        for expense in rows:
            by_category[expense["category"]] = (
                by_category.get(expense["category"], 0) + expense["amount"]
            )
        return by_category

    def top_expenses(self, month, limit=5):
        rows = self.storage.list_expenses(month)
        sorted_rows=sorted(rows, key=lambda expense: expense["amount"], reverse=True)
        return sorted_rows[:limit]

    def export_csv(self, filename, month=None):
       rows = self.storage.list_expenses(month)
       with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
        for expense in rows:
         writer.writerow([expense["id"], expense["date"], expense["category"], f'{expense["amount"]:.2f}', expense["description"]])
        return filename