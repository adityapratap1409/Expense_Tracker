import sqlite3

class Storage:
    def __init__(self, db_path="expenses.db"):
        self.db_file = db_path # save path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row # row factory for dict-like access
        self.init_db()

    def init_db(self):
        # make expenses table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount>0),
                description TEXT
            )
        """)
        # budgets table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL UNIQUE,
                monthly_limit REAL NOT NULL CHECK(monthly_limit>0)
            )
        """)
        self.conn.commit()

    def add_exp(self, amt, cat, desc, dt):
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                (amt, cat, desc, dt)
            )
            return cur.lastrowid

    def getExp(self, exp_id):
        cur = self.conn.execute("SELECT * FROM expenses WHERE id = ?", (exp_id,))
        row = cur.fetchone()
        return row

    def list_all(self, mth=None):
        if mth is not None:
            patt = mth + "%"
            sql = "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC, id DESC"
            cur = self.conn.execute(sql, (patt,))
            rows = cur.fetchall()
            return rows
        else:
            sql = "SELECT * FROM expenses ORDER BY date DESC, id DESC"
            cur = self.conn.execute(sql)
            rows = cur.fetchall()
            return rows

    def setBudget(self, cat, lim):
        # upsert query
        with self.conn:
            self.conn.execute(
                "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?) "
                "ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit",
                (cat, lim)
            )

    def get_bgt(self, cat):
        cur = self.conn.execute("SELECT * FROM budgets WHERE category = ?", (cat,))
        r = cur.fetchone()
        return r

    def all_budgets(self):
        cur = self.conn.execute("SELECT * FROM budgets ORDER BY category")
        res = cur.fetchall()
        return res

    def month_sum(self, cat, mth):
        p = mth + "-%"
        q = "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = ? AND date LIKE ?"
        cur = self.conn.execute(q, (cat, p))
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return 0

    def updExpense(self, exp_id, amt, cat, desc, dt):
        with self.conn:
            cur = self.conn.execute(
                "UPDATE expenses SET amount = ?, category = ?, description = ?, date = ? WHERE id = ?",
                (amt, cat, desc, dt, exp_id)
            )
            return cur.rowcount

    def del_exp(self, exp_id):
        with self.conn:
            cur = self.conn.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
            return cur.rowcount

    def close(self):
        self.conn.close()
