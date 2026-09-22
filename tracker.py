"""
tracker.py

Core data structures and logic for the CLI Expense Tracker.

Classes
-------
Expense         A single expense record.
ExpenseTracker  Holds all expenses, persists them to a JSON file,
                and produces summaries / CSV exports.
"""
import json
import csv
from datetime import datetime
class Expense:
    def __init__(self, expense_id, amount, category, description, date=None):
        self.id = expense_id
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")
    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            expense_id=data["id"],
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data.get("date"),
        )
    def __str__(self):
        return (
            f"[{self.id:>3}] {self.date}  "
            f"{self.category:<15} ${self.amount:>10.2f}  {self.description}"
        )
class ExpenseTracker:
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.expenses = []
        self._next_id = 1
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, "r") as f:
                raw = json.load(f)
            self.expenses = [Expense.from_dict(item) for item in raw]
            if self.expenses:
                self._next_id = max(e.id for e in self.expenses) + 1
        except FileNotFoundError:
            self.expenses = []
        except json.JSONDecodeError:
            print(f"Warning: '{self.data_file}' was empty or corrupted. Starting fresh.")
            self.expenses = []

    def save_data(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump([e.to_dict() for e in self.expenses], f, indent=2)
        except OSError as e:
            print(f"Warning: could not save data ({e}).")

    def add_expense(self, amount, category, description, date=None):
        expense = Expense(self._next_id, amount, category, description, date)
        self.expenses.append(expense)
        self._next_id += 1
        self.save_data()
        return expense

    def get_summary(self):
        if not self.expenses:
            return None
        total = sum(e.amount for e in self.expenses)
        by_category = {}
        for e in self.expenses:
            by_category[e.category] = by_category.get(e.category, 0.0) + e.amount
        return {
            "total": total,
            "count": len(self.expenses),
            "by_category": by_category,
        }
    def export_to_csv(self, filename="expenses_export.csv"):
        """Write all expenses to a CSV file and return the filename used."""
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
            for e in self.expenses:
                writer.writerow(
                    [e.id, e.date, e.category, f"{e.amount:.2f}", e.description]
                )
        return filename
