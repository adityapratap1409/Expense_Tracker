from datetime import datetime
import logging
import sys

from storage import Storage
from expense_service import ExpenseService, NotFoundError
from budget_service import BudgetService
from report_service import ReportService
from validators import ValidationError
from logger_config import init_log

DB_FILE = "expenses.db"
MENU_W = 42

class clr:
    RST = "\033[0m"
    CYN = "\033[96m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    RED = "\033[91m"

def _hdr(txt):
    print("\n" + "="*MENU_W)
    print(txt.center(MENU_W))
    print("="*MENU_W)

def _menu():
    print("\n" + "-"*MENU_W)
    items = [
        " %s1%s. Add Expense",
        " %s2%s. Edit Expense",
        " %s3%s. Delete Expense",
        " %s4%s. View Expenses",
        " %s5%s. Search by Category",
        " %s6%s. Set Budget",
        " %s7%s. Check Budget Status",
        " %s8%s. Monthly Summary",
        " %s9%s. Category Breakdown",
        "%s10%s. Top Expenses",
        "%s11%s. Export to CSV",
        "%s12%s. Exit",
    ]
    for t in items:
        print(t % (clr.CYN, clr.RST))
    print("-"*MENU_W)


def _fmt_row(r):
    # helper to format an expense row for display
    s = "[%3s] %s  %-15s $%10.2f  %s" % (
        r['id'], r['date'], r['category'], r['amount'], r['description'])
    return s


def do_add(svc):
    _hdr("Add New Expense")
    amt = input("Amount ($): ").strip()
    cat = input("Category: ").strip()
    desc = input("Description (optional): ").strip()
    dt = input("Date (DD-MM-YYYY) [blank = today]: ").strip()
    try:
        eid = svc.add_exp(amt, cat, desc, dt)
        print("\n" + clr.GRN + "Saved expense #" + str(eid) + "." + clr.RST)
        logging.info("Added expense #%s" % eid)
    except ValidationError as e:
        print("\n" + clr.RED + "Error: " + str(e) + clr.RST)
        logging.error("add failed: %s" % str(e))


def do_view(svc):
    _hdr("View Expenses")
    inp = input("Filter by month (YYYY-MM) [blank = all]: ").strip()
    mth = inp if inp != "" else None
    rows = svc.list_exp(mth)
    if len(rows) == 0:
        print("\n" + clr.RED + "No expenses found." + clr.RST)
    else:
        for r in rows:
            print(_fmt_row(r))


def do_edit(svc):
    _hdr("Edit Expense")
    raw = input("Expense ID to edit: ").strip()
    try:
        eid = int(raw)
    except:
        print("\n" + clr.RED + "Error: ID must be a number." + clr.RST)
        logging.error("bad expense id input")
        return

    print("Leave blank to keep current value:")
    a = input("New amount [blank = keep]: ").strip()
    c = input("New category [blank = keep]: ").strip()
    d = input("New description [blank = keep]: ").strip()
    dt = input("New date DD-MM-YYYY [blank = keep]: ").strip()
    try:
        svc.editExp(eid, a, c, d, dt)
        print("\n" + clr.GRN + "Expense #" + str(eid) + " updated." + clr.RST)
        logging.info("updated #%d" % eid)
    except NotFoundError as e:
        print("\n" + clr.RED + "Error: " + str(e) + clr.RST)
        logging.error(str(e))
    except ValidationError as e:
        print("\n" + clr.RED + "Error: " + str(e) + clr.RST)
        logging.error(str(e))


def do_del(svc):
    _hdr("Delete Expense")
    raw = input("Expense ID to delete: ").strip()
    try:
        eid = int(raw)
        svc.del_exp(eid)
        print("\n" + clr.GRN + "Expense #" + str(eid) + " deleted." + clr.RST)
        logging.info("deleted #%d" % eid)
    except ValueError:
        print("\n" + clr.RED + "Error: ID must be a number." + clr.RST)
    except NotFoundError as e:
        print("\n" + clr.RED + "Error: " + str(e) + clr.RST)


def do_search(svc):
    _hdr("Search By Category")
    cat = input("Category to search: ").strip()
    try:
        res = svc.findByCat(cat)
        if len(res) == 0:
            print("\n" + clr.RED + "Nothing found for '" + cat.title() + "'." + clr.RST)
        else:
            for r in res:
                print(_fmt_row(r))
    except ValidationError as e:
        print("\n" + clr.RED + "Error: " + str(e) + clr.RST)


def do_setbgt(svc):
    _hdr("Set Budget")
    cat = input("Category: ").strip()
    lim = input("Monthly limit ($): ").strip()
    try:
        svc.set_bgt(cat, lim)
        print("\n" + clr.GRN + "Budget set for " + cat.title() + "." + clr.RST)
        logging.info("budget set: %s" % cat.title())
    except ValidationError as e:
        print("\n" + clr.RED + "Error: " + str(e) + clr.RST)


def do_chkbgt(svc):
    _hdr("Check Budget Status")
    cat = input("Category: ").strip()
    inp = input("Month (YYYY-MM) [blank = now]: ").strip()
    mth = inp if inp != "" else datetime.now().strftime("%Y-%m")
    try:
        msg = svc.chk_alert(cat, mth)
        if msg == None:
            print("\n" + clr.YLW + "No budget set for '" + cat.title() + "'." + clr.RST)
        else:
            print("\n" + msg)
    except ValidationError as e:
        print("\n" + clr.RED + "Error: " + str(e) + clr.RST)


def do_summary(svc):
    _hdr("Monthly Summary")
    inp = input("Month (YYYY-MM) [blank = now]: ").strip()
    if inp != "":
        mth = inp
    else:
        mth = datetime.now().strftime("%Y-%m")
    s = svc.month_summary(mth)
    print("\n%d expense(s) totaling $%.2f in %s." % (s['count'], s['total'], mth))


def do_catbrk(svc):
    _hdr("Category Summary")
    inp = input("Month (YYYY-MM) [blank = now]: ").strip()
    mth = inp if inp != "" else datetime.now().strftime("%Y-%m")
    brk = svc.catBreakdown(mth)
    if len(brk) == 0:
        print("\n" + clr.RED + "No expenses for " + mth + "." + clr.RST)
        return
    print("")
    for cat in brk:
        print("  %-15s $%10.2f" % (cat, brk[cat]))


def do_top(svc):
    _hdr("Top Expenses")
    inp = input("Month (YYYY-MM) [blank = now]: ").strip()
    mth = inp if inp != "" else datetime.now().strftime("%Y-%m")
    top = svc.top_exp(mth, 5)
    if len(top) == 0:
        print("\n" + clr.RED + "No expenses for " + mth + "." + clr.RST)
    else:
        print("")
        for r in top:
            print(_fmt_row(r))

def do_csv(svc):
    _hdr("Export to CSV")
    fname = input("Filename [expenses_export.csv]: ").strip()
    if fname == "":
        fname = "expenses_export.csv"
    # add .csv if missing
    if fname.endswith(".csv") == False:
        fname = fname + ".csv"
    inp = input("Month (YYYY-MM) [blank = all]: ").strip()
    mth = inp if inp != "" else None
    out = svc.exportCSV(fname, mth)
    print("\n" + clr.GRN + "Exported to '" + out + "'." + clr.RST)
    logging.info("export: " + out)


def main():
    db = Storage(DB_FILE)
    exp = ExpenseService(db)
    bgt = BudgetService(db)
    rpt = ReportService(db)
    init_log()
    logging.info("app started")

    _hdr("Expense Tracker")

    handlers = {
        "1": lambda: do_add(exp),
        "2": lambda: do_edit(exp),
        "3": lambda: do_del(exp),
        "4": lambda: do_view(exp),
        "5": lambda: do_search(exp),
        "6": lambda: do_setbgt(bgt),
        "7": lambda: do_chkbgt(bgt),
        "8": lambda: do_summary(rpt),
        "9": lambda: do_catbrk(rpt),
        "10": lambda: do_top(rpt),
        "11": lambda: do_csv(rpt),
    }

    running = True
    while running:
        _menu()
        opt = input("Choose an option (1-12): ").strip()
        if opt == "12":
            print("\nGoodbye!")
            db.close()
            logging.info("app closed")
            running = False
        elif opt in handlers:
            handlers[opt]()
        else:
            print("\n" + clr.RED + "Invalid option, try again." + clr.RST)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
