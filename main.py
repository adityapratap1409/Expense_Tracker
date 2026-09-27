"""
main.py
An Interactive CLI program made to help users efficiently and accurately manage their monthly expenses.
This program features multiple operations for the user to perform like add, view, edit, delete their expenses, budgets
and also view their top spending categories along with an option to export their expenses in a csv file

"""

from storage import Storage
from expense_service import ExpenseService, NotFoundError
from budget_service import BudgetService
from report_service import ReportService
from validators import ValidationError
from datetime import datetime
import logging
from logger_config import setup_logging

DB_FILE = "expenses.db"
menu_width = 42
class Colors:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"

def print_header(title):
    print("\n" + "=" * menu_width)
    print(title.center(menu_width))
    print("=" * menu_width)


def print_menu():
    print("\n" + "-" * menu_width)
    print(f" {Colors.CYAN}1{Colors.RESET}. Add Expense")
    print(f" {Colors.CYAN}2{Colors.RESET}. Edit Expense")
    print(f" {Colors.CYAN}3{Colors.RESET}. Delete Expense")
    print(f" {Colors.CYAN}4{Colors.RESET}. View Expenses")
    print(f" {Colors.CYAN}5{Colors.RESET}. Search by Category")
    print(f" {Colors.CYAN}6{Colors.RESET}. Set Budget")
    print(f" {Colors.CYAN}7{Colors.RESET}. Check Budget Status")
    print(f" {Colors.CYAN}8{Colors.RESET}. Monthly Summary")
    print(f" {Colors.CYAN}9{Colors.RESET}. Category Breakdown")
    print(f"{Colors.CYAN}10{Colors.RESET}. Top Expenses")
    print(f"{Colors.CYAN}11{Colors.RESET}. Export to CSV")
    print(f"{Colors.CYAN}12{Colors.RESET}. Exit")
    print("-" * menu_width)


def add_expense_flow(service):
    print_header("Add New Expense")
    amount = input("Amount ($): ").strip()
    category = input("Category: ").strip().title()
    description = input("Description (optional): ").strip()
    date_input = input("Date (DD-MM-YYYY) [blank = today]: ").strip()
    try:
        new_id = service.add_expense(amount, category, description, date_input)
        print(f"\n{Colors.GREEN}Saved expense #{new_id}.{Colors.RESET}")
        logging.info(f"Added expense #{new_id}: {category}, ${amount}.")
    except ValidationError as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        logging.error(f"Validation error: {e}")


def view_expenses_flow(service):
    print_header("View Expenses")
    month_input = input("Filter by month (YYYY-MM) [blank = all]: ").strip()
    month = month_input if month_input else None
    rows = service.list_expenses(month)
    if not rows:
        print(f"\n{Colors.RED}No expenses found.{Colors.RESET}")
        return
    for expense in rows:
        print(
            f"[{expense['id']:>3}] {expense['date']}  {expense['category']:<15} ${expense['amount']:>10.2f}  {expense['description']}"
        )


def edit_expense_flow(service):
    print_header("Edit Expense")
    id_input = input("Expense ID to edit: ").strip()
    try:
        expense_id = int(id_input)
        amount = input("New amount [blank = keep current]: ").strip()
        category = input("New category [blank = keep current]: ").strip().title()
        description = input("New description [blank = keep current]: ").strip()
        date_input = input("New date (DD-MM-YYYY) [blank = keep current]: ").strip()
        service.edit_expense(expense_id, amount, category, description, date_input)
        print(f"\nExpense #{expense_id} updated.")
        logging.info(f"Updated expense #{expense_id}")
    except ValueError:
        print(f"\n{Colors.RED}Error: expense ID must be a whole number.{Colors.RESET}")
        logging.error(f"Invalid expense ID entered (not a number).")
    except NotFoundError as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        logging.error(f"Not found: {e}")
    except ValidationError as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        logging.error(f"Validation error: {e}")


def delete_expense_flow(service):
    print_header("Delete Expense")
    id_input = input("Expense ID to delete: ").strip()
    try:
        expense_id = int(id_input)
        service.delete_expense(expense_id)
        print(f"\n{Colors.GREEN}Expense #{expense_id} deleted.{Colors.RESET}")
        logging.info(f"Deleted expense #{expense_id}")
    except ValueError:
        print(f"\n{Colors.RED}Error: expense ID must be a whole number.{Colors.RESET}")
        logging.error(f"Invalid expense ID entered (not a number).")
    except NotFoundError as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        logging.error(f"Not found: {e}")


def search_by_category_flow(service):
    print_header("Search By Category")
    category_input = input("Category to be seached: ").strip().title()
    try:
        result = service.search_by_category(category_input)
        if not result:
            print(f"\n{Colors.RED}No expenses found in that category.{Colors.RESET}")
        else:
            for expense in result:
                print(
                    f"[{expense['id']:>3}] {expense['date']}  {expense['category']:<15} ${expense['amount']:>10.2f}  {expense['description']}"
                )
    except ValidationError as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        logging.error(f"Validation error: {e}")


def set_budget_flow(service):
    print_header("Set Budget")
    category = input("Category: ").strip().title()
    amount = input("Monthly limit ($): ").strip()
    try:
        service.set_budget(category, amount)
        print(f"\n{Colors.GREEN}Budget set: {category} — {amount} per month.{Colors.RESET}")
    except ValidationError as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        logging.error(f"Validation error: {e}")


def check_budget_flow(service):
    print_header("Check Budget Status")
    category = input("Category: ").strip().title()
    month_input = input("Month (YYYY-MM) [blank = current month]: ").strip()
    month = month_input if month_input else datetime.now().strftime("%Y-%m")
    try:
        alert = service.check_alert(category, month)
        if alert is None:
            print(f"\n{Colors.RED}No budget set for that category.{Colors.RESET}")
        else:
            print(f"\n{alert}")
    except ValidationError as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        logging.error(f"Validation error: {e}")


def monthly_summary_flow(service):
    print_header("Monthly Summary")
    month_input = input("Month (YYYY-MM) [blank = current month]: ").strip()
    month = month_input if month_input else datetime.now().strftime("%Y-%m")
    summary = service.monthly_summary(month)
    print(
        f"\n{summary['count']} expense(s) totaling ${summary['total']:.2f} in {month}."
    )


def category_breakdown_flow(service):
    print_header("Category Summary")
    month_input = input("Month (YYYY-MM) [blank = current month]: ").strip()
    month = month_input if month_input else datetime.now().strftime("%Y-%m")
    cat_breakdown = service.category_breakdown(month)
    if not cat_breakdown:
        print(f"\n{Colors.RED}No expenses found for that month.{Colors.RESET}")
    else:
        for category, total in cat_breakdown.items():
            print(f"  {category:<15} ${total:>10.2f}")


def top_expenses_flow(service):
    print_header("Top Expenses")
    month_input = input("Month (YYYY-MM) [blank = current month]: ").strip()
    month = month_input if month_input else datetime.now().strftime("%Y-%m")
    top = service.top_expenses(month, limit=5)
    if not top:
        print(f"\n{Colors.RED}No expenses found for that month.{Colors.RESET}")
    else:
        for expense in top:
            print(
                f"[{expense['id']:>3}] {expense['date']}  {expense['category']:<15} ${expense['amount']:>10.2f}  {expense['description']}"
            )


def export_csv_flow(service):
    print_header("Export to CSV")
    filename = (
        input("Filename [expenses_export.csv]: ").strip() or "expenses_export.csv"
    )
    if not filename.endswith(".csv"):
        filename += ".csv"
    month_input = input("Month (YYYY-MM) [blank = all]: ").strip()
    month = month_input if month_input else None
    path = service.export_csv(filename, month)
    print(f"\n{Colors.GREEN}Exported to '{path}'.{Colors.RESET}")


def main():
    storage = Storage(DB_FILE)
    expense_service = ExpenseService(storage)
    budget_service = BudgetService(storage)
    report_service = ReportService(storage)
    setup_logging()
    logging.info("Expense Tracker started.")

    print_header("Expense Tracker")
    while True:
        print_menu()
        choice = input("Choose an option (1-12): ").strip()
        if choice == "1":
            add_expense_flow(expense_service)
        elif choice == "2":
            edit_expense_flow(expense_service)
        elif choice == "3":
            delete_expense_flow(expense_service)
        elif choice == "4":
            view_expenses_flow(expense_service)
        elif choice == "5":
            search_by_category_flow(expense_service)
        elif choice == "6":
            set_budget_flow(budget_service)
        elif choice == "7":
            check_budget_flow(budget_service)
        elif choice == "8":
            monthly_summary_flow(report_service)
        elif choice == "9":
            category_breakdown_flow(report_service)
        elif choice == "10":
            top_expenses_flow(report_service)
        elif choice == "11":
            export_csv_flow(report_service)
        elif choice == "12":
            print("\nGoodbye!")
            storage.close()
            logging.info("Expense Tracker exited.")
            break
        else:
            print("\nWrong Input.Please try again")


if __name__ == "__main__":
    main()
