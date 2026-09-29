import sqlite3

# TODO maybe switch to sqlalchemy someday
DB_SCHEMA_VER = 1

class Storage:
    def __init__(self, db_path="expenses.db"):
        self._path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._setup_tables()

    def _setup_tables(self):
        # expenses table
        q1 = """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount>0),
            description TEXT
        )"""
        self.conn.execute(q1)

        # budgets came later in v2
        q2 = """CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL UNIQUE,
            monthly_limit REAL NOT NULL CHECK(monthly_limit>0)
        )"""
        self.conn.execute(q2)
        self.conn.commit()

    def add_exp(self, amt, cat, desc, dt):
        sql = "INSERT INTO expenses (amount, category, description, date) VALUES (?,?,?,?)"
        with self.conn:
            c = self.conn.execute(sql, (amt, cat, desc, dt))
        return c.lastrowid

    def getExp(self, eid):
        c = self.conn.execute("SELECT * FROM expenses WHERE id=?", (eid,))
        r = c.fetchone()
        if r is not None:
            return r
        return None

    def list_all(self, mth=None):
        # FIXME: probably should validate month format here
        if mth == None:
            sql = "SELECT * FROM expenses ORDER BY date DESC, id DESC"
            c = self.conn.execute(sql)
        else:
            p = mth + "%"
            sql = "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC, id DESC"
            c = self.conn.execute(sql, (p,))
        rows = []
        for r in c.fetchall():
            rows.append(r)
        return rows

    def setBudget(self, cat, limit):
        sql = ("INSERT INTO budgets (category, monthly_limit) VALUES (?,?) "
               "ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit")
        with self.conn:
            self.conn.execute(sql, (cat, limit))

    def get_bgt(self, cat):
        c = self.conn.execute("SELECT * FROM budgets WHERE category=?", (cat,))
        return c.fetchone()

    def all_budgets(self):
        c = self.conn.execute("SELECT * FROM budgets ORDER BY category")
        return c.fetchall()

    def month_sum(self, cat, mth):
        # get total for category in a month
        p = mth + "-%"
        sql = "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE category=? AND date LIKE ?"
        c = self.conn.execute(sql, (cat, p))
        val = c.fetchone()[0]
        return val

    def updExpense(self, eid, amt, cat, desc, dt):
        sql = "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=?"
        with self.conn:
            c = self.conn.execute(sql, (amt, cat, desc, dt, eid))
        return c.rowcount

    def del_exp(self, eid):
        with self.conn:
            c = self.conn.execute("DELETE FROM expenses WHERE id=?", (eid,))
        cnt = c.rowcount
        return cnt

    def close(self):
        self.conn.close()
