"""
main.py
...docstring, rewritten in your own words for what this version does...
"""
from storage import Storage
from expense_service import ExpenseService, NotFoundError
from budget_service import BudgetService
from report_service import ReportService
from validators import ValidationError

DB_FILE = "expenses.db"
menu_width = 42

def print_header(title):
    print("\n" + "=" * menu_width)
    print(title.center(menu_width))
    print("=" * menu_width)

def print_menu():
    print("\n" + "-" * menu_width)
    print(" 1. Add Expense")
    print(" 2. Edit Expense")
    print(" 3. Delete Expense")
    print(" 4. View Expenses")
    print(" 5. Search by Category")
    print(" 6. Set Budget")
    print(" 7. Check Budget Status")
    print(" 8. Monthly Summary")
    print(" 9. Category Breakdown")
    print("10. Top Expenses")
    print("11. Export to CSV")
    print("12. Exit")
    print("-" * menu_width)

def add_expense_flow(service):
    print_header("Add New Expense")
    amount = input("Amount ($): ").strip()
    category = input("Category: ").strip()
    description = input("Description (optional): ").strip()
    date_input = input("Date (DD-MM-YYYY) [blank = today]: ").strip()
    try:
        new_id = service.add_expense(amount, category, description, date_input)
        print(f"\nSaved expense #{new_id}.")
    except ValidationError as e:
        print(f"\nError: {e}")

def view_expenses_flow(service):
    print_header("View Expenses")
    month_input = input("Filter by month (YYYY-MM) [blank = all]: ").strip()
    month = month_input if month_input else None
    rows = service.list_expenses(month)
    if not rows:
        print("\nNo expenses found.")
        return
    for expense in rows:
        print(f"[{expense['id']:>3}] {expense['date']}  {expense['category']:<15} ${expense['amount']:>10.2f}  {expense['description']}")

def edit_expense_flow(service):
    print_header("Edit Expense")
    id_input = input("Expense ID to edit: ").strip()
    try:
        expense_id = int(id_input)
        amount = input("New amount [blank = keep current]: ").strip()
        category = input("New category [blank = keep current]: ").strip()
        description = input("New description [blank = keep current]: ").strip()
        date_input = input("New date (DD-MM-YYYY) [blank = keep current]: ").strip()
        service.edit_expense(expense_id, amount, category, description, date_input)
        print(f"\nExpense #{expense_id} updated.")
    except ValueError:
        print("\nError: expense ID must be a whole number.")
    except NotFoundError as e:
        print(f"\nError: {e}")
    except ValidationError as e:
        print(f"\nError: {e}")

def main():
    storage = Storage(DB_FILE)
    expense_service = ExpenseService(storage)
    budget_service = BudgetService(storage)
    report_service = ReportService(storage)

    print_header("Expense Tracker")
    while True:
        print_menu()
        choice = input("Choose an option (1-12): ").strip()
        if choice == "1":
            add_expense_flow(expense_service)
        elif choice =="2":
            edit_expense_flow(expense_service)
        elif choice == "4":
            view_expenses_flow(expense_service)
        elif choice == "12":
            print("\nGoodbye!")
            storage.close()
            break
        else:
            print("\nOption not implemented yet.")

if __name__ == "__main__":
    main()