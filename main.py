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


class color:
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
    print(f" {color.CYAN}1{color.RESET}. Add Expense")
    print(f" {color.CYAN}2{color.RESET}. Edit Expense")
    print(f" {color.CYAN}3{color.RESET}. Delete Expense")
    print(f" {color.CYAN}4{color.RESET}. View Expenses")
    print(f" {color.CYAN}5{color.RESET}. Search by Category")
    print(f" {color.CYAN}6{color.RESET}. Set Budget")
    print(f" {color.CYAN}7{color.RESET}. Check Budget Status")
    print(f" {color.CYAN}8{color.RESET}. Monthly Summary")
    print(f" {color.CYAN}9{color.RESET}. Category Breakdown")
    print(f"{color.CYAN}10{color.RESET}. Top Expenses")
    print(f"{color.CYAN}11{color.RESET}. Export to CSV")
    print(f"{color.CYAN}12{color.RESET}. Exit")
    print("-" * menu_width)


def add_expense_flow(service):
    print_header("Add New Expense")
    amount = input("Amount ($): ").strip()
    category = input("Category: ").strip().title()
    description = input("Description (optional): ").strip()
    date_input = input("Date (DD-MM-YYYY) [blank = today]: ").strip()
    try:
        new_id = service.add_expense(amount, category, description, date_input)
        print(f"\n{color.GREEN}Saved expense #{new_id}.{color.RESET}")
        logging.info(f"Added expense #{new_id}: {category}, ${amount}.")
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def view_expenses_flow(service):
    print_header("View Expenses")
    month_input = input("Filter by month (YYYY-MM) [blank = all]: ").strip()
    month = month_input if month_input else None
    rows = service.list_expenses(month)
    if not rows:
        print(f"\n{color.RED}No expenses found.{color.RESET}")
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
        print(f"\n{color.RED}Error: expense ID must be a whole number.{color.RESET}")
        logging.error(f"Invalid expense ID entered (not a number).")
    except NotFoundError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Not found: {e}")
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def delete_expense_flow(service):
    print_header("Delete Expense")
    id_input = input("Expense ID to delete: ").strip()
    try:
        expense_id = int(id_input)
        service.delete_expense(expense_id)
        print(f"\n{color.GREEN}Expense #{expense_id} deleted.{color.RESET}")
        logging.info(f"Deleted expense #{expense_id}")
    except ValueError:
        print(f"\n{color.RED}Error: expense ID must be a whole number.{color.RESET}")
        logging.error(f"Invalid expense ID entered (not a number).")
    except NotFoundError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Not found: {e}")


def search_by_category_flow(service):
    print_header("Search By Category")
    category_input = input("Category to be seached: ").strip().title()
    try:
        result = service.search_by_category(category_input)
        if not result:
            print(f"\n{color.RED}No expenses found in that category.{color.RESET}")
        else:
            for expense in result:
                print(
                    f"[{expense['id']:>3}] {expense['date']}  {expense['category']:<15} ${expense['amount']:>10.2f}  {expense['description']}"
                )
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def set_budget_flow(service):
    print_header("Set Budget")
    category = input("Category: ").strip().title()
    amount = input("Monthly limit ($): ").strip()
    try:
        service.set_budget(category, amount)
        print(
            f"\n{color.GREEN}Budget set: {category} — {amount} per month.{color.RESET}"
        )
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def check_budget_flow(service):
    print_header("Check Budget Status")
    category = input("Category: ").strip().title()
    month_input = input("Month (YYYY-MM) [blank = current month]: ").strip()
    month = month_input if month_input else datetime.now().strftime("%Y-%m")
    try:
        alert = service.check_alert(category, month)
        if alert is None:
            print(f"\n{color.RED}No budget set for that category.{color.RESET}")
        else:
            print(f"\n{alert}")
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
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
        print(f"\n{color.RED}No expenses found for that month.{color.RESET}")
    else:
        for category, total in cat_breakdown.items():
            print(f"  {category:<15} ${total:>10.2f}")


def top_expenses_flow(service):
    print_header("Top Expenses")
    month_input = input("Month (YYYY-MM) [blank = current month]: ").strip()
    month = month_input if month_input else datetime.now().strftime("%Y-%m")
    top = service.top_expenses(month, limit=5)
    if not top:
        print(f"\n{color.RED}No expenses found for that month.{color.RESET}")
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
    print(f"\n{color.GREEN}Exported to '{path}'.{color.RESET}")


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
