from datetime import datetime
import logging

from storage import Storage
from expense_service import ExpenseService, NotFoundError
from budget_service import BudgetService
from report_service import ReportService
from validators import ValidationError
from logger_config import init_log

DB_FILE = "expenses.db"
MENU_W = 42


# basic terminal colors
class color:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


def hdr(txt):
    print("\n" + "=" * MENU_W)
    print(txt.center(MENU_W))
    print("=" * MENU_W)


def showMenu():
    print("\n" + "-" * MENU_W)
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
    print("-" * MENU_W)


def flow_add(svc):
    hdr("Add New Expense")
    amt = input("Amount ($): ").strip()
    cat = input("Category: ").strip()
    desc = input("Description (optional): ").strip()
    dt = input("Date (DD-MM-YYYY) [blank = today]: ").strip()

    try:
        new_id = svc.add_exp(amt, cat, desc, dt)
        print(f"\n{color.GREEN}Saved expense #{new_id}.{color.RESET}")
        logging.info(f"Added expense #{new_id}: {cat.title()}, ${amt}.")
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def viewFlow(svc):
    hdr("View Expenses")
    mth = input("Filter by month (YYYY-MM) [blank = all]: ").strip() or None
    rows = svc.list_exp(mth)

    if not rows:
        print(f"\n{color.RED}No expenses found.{color.RESET}")
        return

    # formatted table print
    for r in rows:
        print(
            f"[{r['id']:>3}] {r['date']}  {r['category']:<15} ${r['amount']:>10.2f}  {r['description']}"
        )


def edit_flow(svc):
    hdr("Edit Expense")
    raw_id = input("Expense ID to edit: ").strip()

    try:
        exp_id = int(raw_id)
        print("Leave blank to keep existing value:")
        amt = input("New amount [blank = keep current]: ").strip()
        cat = input("New category [blank = keep current]: ").strip()
        desc = input("New description [blank = keep current]: ").strip()
        dt = input("New date (DD-MM-YYYY) [blank = keep current]: ").strip()

        svc.editExp(exp_id, amt, cat, desc, dt)
        print(f"\n{color.GREEN}Expense #{exp_id} updated.{color.RESET}")
        logging.info(f"Updated expense #{exp_id}")
    except ValueError:
        print(f"\n{color.RED}Error: Expense ID must be a whole number.{color.RESET}")
        logging.error("Invalid expense ID (not an int).")
    except NotFoundError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Not found: {e}")
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def delFlow(svc):
    hdr("Delete Expense")
    raw_id = input("Expense ID to delete: ").strip()

    try:
        exp_id = int(raw_id)
        svc.del_exp(exp_id)
        print(f"\n{color.GREEN}Expense #{exp_id} deleted.{color.RESET}")
        logging.info(f"Deleted expense #{exp_id}")
    except ValueError:
        print(f"\n{color.RED}Error: Expense ID must be a whole number.{color.RESET}")
        logging.error("Invalid expense ID entered for deletion.")
    except NotFoundError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Not found: {e}")


def search_cat_flow(svc):
    hdr("Search By Category")
    cat = input("Category to search: ").strip()

    try:
        res = svc.findByCat(cat)
        if not res:
            print(f"\n{color.RED}No expenses found in category '{cat.title()}'.{color.RESET}")
        else:
            for r in res:
                print(
                    f"[{r['id']:>3}] {r['date']}  {r['category']:<15} ${r['amount']:>10.2f}  {r['description']}"
                )
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def setBgtFlow(svc):
    hdr("Set Budget")
    cat = input("Category: ").strip()
    lim = input("Monthly limit ($): ").strip()

    try:
        svc.set_bgt(cat, lim)
        print(
            f"\n{color.GREEN}Budget set: {cat.title()} — ${float(lim):.2f} per month.{color.RESET}"
        )
        logging.info(f"Set budget for {cat.title()} to ${lim}")
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def chk_bgt_flow(svc):
    hdr("Check Budget Status")
    cat = input("Category: ").strip()
    mth = input("Month (YYYY-MM) [blank = current month]: ").strip() or datetime.now().strftime("%Y-%m")

    try:
        alert = svc.chk_alert(cat, mth)
        if alert is None:
            print(f"\n{color.YELLOW}No budget set for category '{cat.title()}'.{color.RESET}")
        else:
            print(f"\n{alert}")
    except ValidationError as e:
        print(f"\n{color.RED}Error: {e}{color.RESET}")
        logging.error(f"Validation error: {e}")


def summary_flow(svc):
    hdr("Monthly Summary")
    mth = input("Month (YYYY-MM) [blank = current month]: ").strip() or datetime.now().strftime("%Y-%m")
    s = svc.month_summary(mth)
    print(f"\n{s['count']} expense(s) totaling ${s['total']:.2f} in {mth}.")


def catFlow(svc):
    hdr("Category Summary")
    mth = input("Month (YYYY-MM) [blank = current month]: ").strip() or datetime.now().strftime("%Y-%m")
    breakdown = svc.catBreakdown(mth)

    if not breakdown:
        print(f"\n{color.RED}No expenses found for {mth}.{color.RESET}")
    else:
        print(f"\nSpending breakdown for {mth}:")
        for c, tot in breakdown.items():
            print(f"  {c:<15} ${tot:>10.2f}")


def top_flow(svc):
    hdr("Top Expenses")
    mth = input("Month (YYYY-MM) [blank = current month]: ").strip() or datetime.now().strftime("%Y-%m")
    top = svc.top_exp(mth, limit=5)

    if not top:
        print(f"\n{color.RED}No expenses found for {mth}.{color.RESET}")
    else:
        print(f"\nTop expenses for {mth}:")
        for r in top:
            print(
                f"[{r['id']:>3}] {r['date']}  {r['category']:<15} ${r['amount']:>10.2f}  {r['description']}"
            )


def csv_flow(svc):
    hdr("Export to CSV")
    fname = input("Filename [expenses_export.csv]: ").strip() or "expenses_export.csv"
    if not fname.endswith(".csv"):
        fname += ".csv"

    mth = input("Month (YYYY-MM) [blank = all]: ").strip() or None
    out = svc.exportCSV(fname, mth)
    print(f"\n{color.GREEN}Successfully exported to '{out}'.{color.RESET}")
    logging.info(f"Exported data to {out}")


def main():
    db = Storage(DB_FILE)
    exp_svc = ExpenseService(db)
    bgt_svc = BudgetService(db)
    rpt_svc = ReportService(db)

    init_log()
    logging.info("Expense Tracker started.")

    hdr("Expense Tracker")

    while True:
        showMenu()
        opt = input("Choose an option (1-12): ").strip()

        if opt == "1":
            flow_add(exp_svc)
        elif opt == "2":
            edit_flow(exp_svc)
        elif opt == "3":
            delFlow(exp_svc)
        elif opt == "4":
            viewFlow(exp_svc)
        elif opt == "5":
            search_cat_flow(exp_svc)
        elif opt == "6":
            setBgtFlow(bgt_svc)
        elif opt == "7":
            chk_bgt_flow(bgt_svc)
        elif opt == "8":
            summary_flow(rpt_svc)
        elif opt == "9":
            catFlow(rpt_svc)
        elif opt == "10":
            top_flow(rpt_svc)
        elif opt == "11":
            csv_flow(rpt_svc)
        elif opt == "12":
            print("\nGoodbye!")
            db.close()
            logging.info("Expense Tracker exited normally.")
            break
        else:
            print(f"\n{color.RED}Invalid option '{opt}'. Please enter 1-12.{color.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSession closed by user. Bye!")
