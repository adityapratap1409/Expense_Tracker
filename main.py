"""
main.py

Interactive CLI Expense Tracker.

Run it with:
    python main.py

Presents a simple menu-driven terminal interface for adding expenses,
viewing a summary, and exporting everything to CSV. All persistence
logic lives in tracker.py.
"""
from tracker import ExpenseTracker

Data_File = "data.json"
menu_width = 42
def print_header(title):
    print("\n" + "=" * menu_width)
    print(title.center(menu_width))
    print("=" * menu_width)
def print_menu():
    print("\n" + "-" * menu_width)
    print(" 1. Add Expense")
    print(" 2. View Summary")
    print(" 3. Export to CSV")
    print(" 4. Exit")
    print("-" * menu_width)
def prompt_float(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  That doesn't look like a number. Try again.")
            continue
        if value <= 0:
            print("  Please enter a positive amount.")
            continue
        return value
def add_expense_flow(tracker):
    print_header("Add New Expense")
    amount = prompt_float("Amount ($): ")
    category = input("Category (e.g. Food, Rent, Transport): ").strip() or "Uncategorized"
    description = input("Description: ").strip() or "-"
    date_input = input("Date (YYYY-MM-DD) [blank = today]: ").strip()
    expense = tracker.add_expense(amount, category, description, date_input or None)
    print(f"\nSaved:\n  {expense}")
def view_summary_flow(tracker):
    print_header("Expense Summary")
    summary = tracker.get_summary()
    if summary is None:
        print("No expenses recorded yet. Add one from the main menu.")
        return

    print(f"Total expenses logged: {summary['count']}")
    print(f"Total amount spent:    ${summary['total']:.2f}")

    print("\nBy category:")
    for category, amount in sorted(summary["by_category"].items(), key=lambda kv: -kv[1]):
        print(f"  {category:<15} ${amount:>10.2f}")

    print("\nAll expenses:")
    for expense in tracker.expenses:
        print(f"  {expense}")
def export_csv_flow(tracker):
    print_header("Export to CSV")
    if not tracker.expenses:
        print("No expenses to export yet.")
        return
    filename = input("Export filename [expenses_export.csv]: ").strip() or "expenses_export.csv"
    path = tracker.export_to_csv(filename)
    print(f"Exported {len(tracker.expenses)} expense(s) to '{path}'.")
def main():
    tracker = ExpenseTracker(Data_File)
    print_header("Expense Tracker")
    while True:
        print_menu()
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            add_expense_flow(tracker)
        elif choice == "2":
            view_summary_flow(tracker)
        elif choice == "3":
            export_csv_flow(tracker)
        elif choice == "4":
            print("\nGoodbye! Your data has been saved to " + Data_File)
            break
        else:
            print("\nInvalid choice -- please enter 1, 2, 3, or 4.")
if __name__ == "__main__":
    main()
