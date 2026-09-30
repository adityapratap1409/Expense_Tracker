# Python Expense Tracker
A simple interactive command-line expenses and budget tracker. No dependencies beyond the Python standard library.

## Features
**Module 1: Expense Management**
- **Add Expenses** — Users can add their expenses and include the category, date, and month they spent that amount on, along with a description for better and effective tracking.
- **Edit Expenses** — Users can edit their already existing expenses' amount, category, description, date, etc.
- **Search Expenses** — Users can search their expenses or filter them by category.

**Module 2: Budgets and Alerts**
- **Monthly Limit Setting** — Users can set a monthly limit for each category.
- **Budget Management and Alert Generation** — Users can set a budget for categories and get alerts for overspending or nearing the limit.

**Module 3: Reports and Analytics**
- **Monthly Summary Generation** — Users can generate a monthly summary showing total spending for a chosen month.
- **Category-wise Report Generation** — Users can generate category-wise reports showing total spending per category for a chosen month.
- **Top Spending Report Generation** — Users can generate a top spending report to see their top 5 expenses, helping them assess and effectively track their spending.

## File Layout

```
main.py
storage.py
expense_service.py
budget_service.py
report_service.py
validators.py
logger_config.py
tests/
test_validators.py
test_storage.py
test_expense_service.py
test_budget_service.py
README.md
statement.md
.gitignore
```

## Requirements
- Python 3.7 or later
- No third-party packages required

## Running It
```bash
python main.py

```

*(On some systems you may need `python3 main.py` instead.)*

## Running Tests

```bash
python -m unittest discover -s tests -v

```

## Usage

You'll see a menu like this:

```
==========================================
Expense Tracker
Add Expense
Edit Expense
Delete Expense
View Expenses
Search by Category
Set Budget
Check Budget Status
Monthly Summary
Category Breakdown
Top Expenses
Export to CSV
Exit

```

Choose an option (1-12):

* **1 — Add Expense**: Asks the user for the amount, category, description, and date. A blank date defaults to today, and a blank description defaults to "-".
* **2 — Edit Expense**: Asks for the expense ID, then new values for amount, category, description, and date. Any field left blank keeps its current value; an invalid ID shows an error.
* **3 — Delete Expense**: Asks for the expense ID and removes that expense permanently. An invalid or missing ID shows an error.
* **4 — View Expenses**: Asks for a month (YYYY-MM), which is optional. Leaving it blank shows all expenses ever recorded, not just the current month.
* **5 — Search by Category**: Asks for a category name and shows all expenses in that category. No match is not an error, just an empty result message.
* **6 — Set Budget**: Asks for a category and a monthly limit amount. Setting a budget again for the same category overwrites the old limit.
* **7 — Check Budget Status**: Asks for a category and an optional month (blank = current month). Shows whether spending is comfortably under, approaching, or over the limit; shows nothing if no budget was ever set for that category.
* **8 — Monthly Summary**: Asks for an optional month (blank = current month) and shows the total number of expenses and total amount spent.
* **9 — Category Breakdown**: Asks for an optional month (blank = current month) and shows total spending per category.
* **10 — Top Expenses**: Asks for an optional month (blank = current month) and shows the 5 largest individual expenses, largest first.
* **11 — Export to CSV**: Asks for an optional filename (defaults to `expenses_export.csv`, `.csv` is added automatically if missing) and an optional month (blank = all). Writes matching expenses to a CSV file.
* **12 — Exit**: Closes the database connection and ends the program. All data is already saved as it happens, so no confirmation is needed.

## Data Storage

Data is stored in a local SQLite database file, `expenses.db`, created automatically the first time the program runs. It is not checked into the repository (see `.gitignore`) since it's generated locally and would otherwise fill up with each user's own test data.

The database has two tables:

### **expenses**

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER | Primary key, auto-incrementing |
| amount | REAL | Must be greater than 0 |
| category | TEXT | Required |
| description | TEXT | Optional, defaults to "-" |
| date | TEXT | Stored as YYYY-MM-DD |

### **budgets**

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER | Primary key, auto-incrementing |
| category | TEXT | Unique — one budget per category |
| monthly_limit | REAL | Must be greater than 0 |

Setting a budget for a category that already has one updates the existing row rather than creating a duplicate.

## Design Notes

The project is split into layers, each with a single responsibility:

* **`validators.py`** — checks and cleans all raw user input (amounts, dates, categories, descriptions) before it reaches anything else. Raises `ValidationError` on bad input.
* **`storage.py`** — the only file that talks to SQLite directly. All other files access the database through this layer, never with raw SQL of their own.
* **`expense_service.py`, `budget_service.py`, `report_service.py**` — one file per module (expense management, budgets and alerts, reports and analytics). Each contains the actual business logic: validating input, calling storage, and returning results. `expense_service.py` also defines `NotFoundError` for operations on expenses that don't exist.
* **`logger_config.py`** — sets up logging to `expense_tracker.log`, recording actions and errors for troubleshooting.
* **`main.py`** — the only file that touches the terminal (`input()`/`print()`). It contains no business logic itself; each menu option calls into one of the three services and displays the result.

This separation makes each layer independently testable: `tests/` contains unit tests for the validators, storage, and both business-logic services, using an in-memory SQLite database (`:memory:`) so tests never touch real data.