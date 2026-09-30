import sqlite3

# TODO: maybe switch to sqlalchemy someday
DB_SCHEMA_VER = 1

class Storage:
    def __init__(self, db_path="expenses.db"):
        self._path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._setup_tables()

    def _setup_tables(self):
        cur = self.conn.cursor()
        # expenses table
        tbl1 = """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount>0),
            description TEXT
        )"""
        cur.execute(tbl1)

        # budgets table added later in v2
        tbl2 = """CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL UNIQUE,
            monthly_limit REAL NOT NULL CHECK(monthly_limit>0)
        )"""
        cur.execute(tbl2)
        self.conn.commit()

    def add_exp(self, amt, cat, desc, dt):
        # insert new expense row
        sql_q = "INSERT INTO expenses (amount, category, description, date) VALUES (?,?,?,?)"
        with self.conn:
            c = self.conn.execute(sql_q, (amt, cat, desc, dt))
            new_id = c.lastrowid
        return new_id

    def getExp(self, eid):
        # lookup single expense by id
        c = self.conn.execute("SELECT * FROM expenses WHERE id=?", (eid,))
        row = c.fetchone()
        if row != None:
            return row
        return None

    def list_all(self, mth=None):
        # FIXME: probably should validate month format here
        if mth == None or mth == "":
            sql_q = "SELECT * FROM expenses ORDER BY date DESC, id DESC"
            cur = self.conn.execute(sql_q)
        else:
            pat = str(mth) + "%"
            sql_q = "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC, id DESC"
            cur = self.conn.execute(sql_q, (pat,))
        
        rows = []
        all_data = cur.fetchall()
        for r in all_data:
            rows.append(r)
        return rows

    def setBudget(self, cat, limit):
        # upsert monthly budget
        sql_q = ("INSERT INTO budgets (category, monthly_limit) VALUES (?,?) "
                 "ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit")
        with self.conn:
            self.conn.execute(sql_q, (cat, limit))

    def get_bgt(self, cat):
        # fetch budget record for category
        c = self.conn.execute("SELECT * FROM budgets WHERE category=?", (cat,))
        res = c.fetchone()
        return res

    def all_budgets(self):
        c = self.conn.execute("SELECT * FROM budgets ORDER BY category")
        res = c.fetchall()
        return res

    def month_sum(self, cat, mth):
        # get total spend for category in given month
        pat = str(mth) + "-%"
        sql_q = "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE category=? AND date LIKE ?"
        cur = self.conn.execute(sql_q, (cat, pat))
        row = cur.fetchone()
        if row != None:
            tot = row[0]
        else:
            tot = 0
        return tot

    def updExpense(self, eid, amt, cat, desc, dt):
        # update existing expense
        sql_q = "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=?"
        with self.conn:
            c = self.conn.execute(sql_q, (amt, cat, desc, dt, eid))
            cnt = c.rowcount
        return cnt

    def del_exp(self, eid):
        # remove expense record
        with self.conn:
            c = self.conn.execute("DELETE FROM expenses WHERE id=?", (eid,))
            cnt = c.rowcount
        return cnt

    def close(self):
        if self.conn != None:
            self.conn.close()
