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
    print(" " + color.CYAN + "1" + color.RESET + ". Add Expense")
    print(" " + color.CYAN + "2" + color.RESET + ". Edit Expense")
    print(" " + color.CYAN + "3" + color.RESET + ". Delete Expense")
    print(" " + color.CYAN + "4" + color.RESET + ". View Expenses")
    print(" " + color.CYAN + "5" + color.RESET + ". Search by Category")
    print(" " + color.CYAN + "6" + color.RESET + ". Set Budget")
    print(" " + color.CYAN + "7" + color.RESET + ". Check Budget Status")
    print(" " + color.CYAN + "8" + color.RESET + ". Monthly Summary")
    print(" " + color.CYAN + "9" + color.RESET + ". Category Breakdown")
    print(color.CYAN + "10" + color.RESET + ". Top Expenses")
    print(color.CYAN + "11" + color.RESET + ". Export to CSV")
    print(color.CYAN + "12" + color.RESET + ". Exit")
    print("-" * MENU_W)

def flow_add(svc):
    hdr("Add New Expense")
    amt = input("Amount ($): ").strip()
    cat = input("Category: ").strip()
    desc = input("Description (optional): ").strip()
    dt = input("Date (DD-MM-YYYY) [blank = today]: ").strip()

    try:
        new_id = svc.add_exp(amt, cat, desc, dt)
        print("\n" + color.GREEN + ("Saved expense #%s." % new_id) + color.RESET)
        logging.info("Added expense #%s: %s, $%s." % (new_id, cat.title(), amt))
    except ValidationError as e:
        print("\n" + color.RED + ("Error: %s" % e) + color.RESET)
        logging.error("Validation error: %s" % e)

def viewFlow(svc):
    hdr("View Expenses")
    inp = input("Filter by month (YYYY-MM) [blank = all]: ").strip()
    if len(inp) > 0:
        mth = inp
    else:
        mth = None

    rows = svc.list_exp(mth)
    if len(rows) == 0:
        print("\n" + color.RED + "No expenses found." + color.RESET)
        return
    else:
        for r in rows:
            print("[%3s] %s  %-15s $%10.2f  %s" % (r['id'], r['date'], r['category'], r['amount'], r['description']))

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
        print("\n" + color.GREEN + ("Expense #%s updated." % exp_id) + color.RESET)
        logging.info("Updated expense #%s" % exp_id)
    except ValueError:
        print("\n" + color.RED + "Error: Expense ID must be a whole number." + color.RESET)
        logging.error("Invalid expense ID (not an int).")
    except NotFoundError as e:
        print("\n" + color.RED + ("Error: %s" % e) + color.RESET)
        logging.error("Not found: %s" % e)
    except ValidationError as e:
        print("\n" + color.RED + ("Error: %s" % e) + color.RESET)
        logging.error("Validation error: %s" % e)

def delFlow(svc):
    hdr("Delete Expense")
    raw_id = input("Expense ID to delete: ").strip()

    try:
        exp_id = int(raw_id)
        svc.del_exp(exp_id)
        print("\n" + color.GREEN + ("Expense #%s deleted." % exp_id) + color.RESET)
        logging.info("Deleted expense #%s" % exp_id)
    except ValueError:
        print("\n" + color.RED + "Error: Expense ID must be a whole number." + color.RESET)
        logging.error("Invalid expense ID for deletion.")
    except NotFoundError as e:
        print("\n" + color.RED + ("Error: %s" % e) + color.RESET)
        logging.error("Not found: %s" % e)

def search_cat_flow(svc):
    hdr("Search By Category")
    cat = input("Category to search: ").strip()

    try:
        res = svc.findByCat(cat)
        if len(res) == 0:
            print("\n" + color.RED + ("No expenses found in category '%s'." % cat.title()) + color.RESET)
        else:
            for r in res:
                print("[%3s] %s  %-15s $%10.2f  %s" % (r['id'], r['date'], r['category'], r['amount'], r['description']))
    except ValidationError as e:
        print("\n" + color.RED + ("Error: %s" % e) + color.RESET)
        logging.error("Validation error: %s" % e)

def setBgtFlow(svc):
    hdr("Set Budget")
    cat = input("Category: ").strip()
    lim = input("Monthly limit ($): ").strip()

    try:
        svc.set_bgt(cat, lim)
        print("\n" + color.GREEN + ("Budget set: %s — $%.2f per month." % (cat.title(), float(lim))) + color.RESET)
        logging.info("Set budget for %s to $%s" % (cat.title(), lim))
    except ValidationError as e:
        print("\n" + color.RED + ("Error: %s" % e) + color.RESET)
        logging.error("Validation error: %s" % e)

def chk_bgt_flow(svc):
    hdr("Check Budget Status")
    cat = input("Category: ").strip()
    inp = input("Month (YYYY-MM) [blank = current month]: ").strip()
    if len(inp) > 0:
        mth = inp
    else:
        mth = datetime.now().strftime("%Y-%m")

    try:
        alert = svc.chk_alert(cat, mth)
        if alert is None:
            print("\n" + color.YELLOW + ("No budget set for category '%s'." % cat.title()) + color.RESET)
        else:
            print("\n" + alert)
    except ValidationError as e:
        print("\n" + color.RED + ("Error: %s" % e) + color.RESET)
        logging.error("Validation error: %s" % e)

def summary_flow(svc):
    hdr("Monthly Summary")
    inp = input("Month (YYYY-MM) [blank = current month]: ").strip()
    if len(inp) > 0:
        mth = inp
    else:
        mth = datetime.now().strftime("%Y-%m")

    s = svc.month_summary(mth)
    print("\n%s expense(s) totaling $%.2f in %s." % (s['count'], s['total'], mth))

def catFlow(svc):
    hdr("Category Summary")
    inp = input("Month (YYYY-MM) [blank = current month]: ").strip()
    if len(inp) > 0:
        mth = inp
    else:
        mth = datetime.now().strftime("%Y-%m")

    breakdown = svc.catBreakdown(mth)
    if len(breakdown) == 0:
        print("\n" + color.RED + ("No expenses found for %s." % mth) + color.RESET)
    else:
        print("\nSpending breakdown for " + mth + ":")
        for c, tot in breakdown.items():
            print("  %-15s $%10.2f" % (c, tot))

def top_flow(svc):
    hdr("Top Expenses")
    inp = input("Month (YYYY-MM) [blank = current month]: ").strip()
    if len(inp) > 0:
        mth = inp
    else:
        mth = datetime.now().strftime("%Y-%m")

    top = svc.top_exp(mth, limit=5)
    if len(top) == 0:
        print("\n" + color.RED + ("No expenses found for %s." % mth) + color.RESET)
    else:
        print("\nTop expenses for " + mth + ":")
        for r in top:
            print("[%3s] %s  %-15s $%10.2f  %s" % (r['id'], r['date'], r['category'], r['amount'], r['description']))

def csv_flow(svc):
    hdr("Export to CSV")
    fname = input("Filename [expenses_export.csv]: ").strip()
    if len(fname) == 0:
        fname = "expenses_export.csv"
    if not fname.endswith(".csv"):
        fname = fname + ".csv"

    inp = input("Month (YYYY-MM) [blank = all]: ").strip()
    if len(inp) > 0:
        mth = inp
    else:
        mth = None

    out = svc.exportCSV(fname, mth)
    print("\n" + color.GREEN + ("Successfully exported to '%s'." % out) + color.RESET)
    logging.info("Exported data to " + out)

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
            print("\n" + color.RED + ("Invalid option '%s'. Please enter 1-12." % opt) + color.RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSession closed by user. Bye!")
