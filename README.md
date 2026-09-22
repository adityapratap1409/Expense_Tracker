# Python Expense Tracker
A simple interactive command-line expense tracker. No dependencies
beyond the Python standard library.
## Features
- Add Expense — log an amount, category, description, and date (defaults to today if left blank).
- View Summary — see total spend, a breakdown by category, and a
  full list of every recorded expense.
- Export to CSV — write all expenses to a `.csv` file you can open in Excel, Google Sheets, Numbers, etc.
- Persistent storage — expenses are saved to `data.json` after every add, so your data survives between runs.
## File Layout
python-expense-tracker/
├── main.py       # Entry point: the interactive menu loop
├── tracker.py    # Expense and ExpenseTracker classes (data + logic)
├── README.md     # This file
└── data.json     # Where your expenses are stored (JSON array)
## Requirements
- Python 3.7 or later
- No third-party packages required
## Running It
From inside the `python-expense-tracker/` folder:
```bash
python main.py
```
(On some systems you may need `python3 main.py` instead.)
## Usage
You'll see a menu like this:
```
------------------------------------------
 1. Add Expense
 2. View Summary
 3. Export to CSV
 4. Exit
------------------------------------------
Choose an option (1-4):
```
- 1 — Add Expense: enter the amount, category, description, and
  optionally a date (`YYYY-MM-DD`). Leaving the date blank uses
  today's date.
- 2 — View Summary: prints the total amount spent, a per-category
  breakdown, and every individual expense.
- 3 — Export to CSV: choose a filename (or accept the default
  `expenses_export.csv`) and every expense is written out as CSV.
- 4 — Exit: quits the program. Your data is already saved, since
  every add operation writes to `data.json` immediately.
## Data Storage
Expenses live in `data.json` as a plain JSON array, for example:
```json
[
  {
    "id": 1,
    "amount": 12.5,
    "category": "Food",
    "description": "Lunch",
    "date": "2026-09-11"
  }
]
```
If `data.json` is missing or unreadable, the app doesn't crash — it
simply starts with an empty ledger and creates a fresh file the next
time you add an expense.
## Design Notes
- `Expense` (in `tracker.py`) represents a single expense record, and
  knows how to convert itself to/from a dictionary for JSON storage.
- `ExpenseTracker` (also in `tracker.py`) owns the list of expenses,
  handles loading/saving `data.json`, computes summaries, and exports
  CSV files.
- `main.py` contains only the interactive menu loop and terminal
  I/O — all the actual data logic stays in `tracker.py`, keeping
  concerns separated.
