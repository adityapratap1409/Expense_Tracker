import sqlite3


# TODO: look into an ORM later if this gets too big,
# raw sqlite is totally fine for a simple script right now
class Storage:
    def __init__(self, db_path="expenses.db"):
        self.db_file = db_path  # save path just in case
        self.conn = sqlite3.connect(db_path)
        # row factory lets us access cols like row['amount']
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        # tables setup on first run
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                description TEXT
            )
        """)

        # separate budgets table added after v1
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL UNIQUE,
                monthly_limit REAL NOT NULL CHECK(monthly_limit > 0)
            )
        """)
        self.conn.commit()

    def add_exp(self, amt, cat, desc, dt):
        # insert new expense row
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                (amt, cat, desc, dt),
            )
        return cur.lastrowid

    def getExp(self, exp_id):
        # fetch single row by primary key
        cur = self.conn.execute("SELECT * FROM expenses WHERE id = ?", (exp_id,))
        return cur.fetchone()

    def list_all(self, mth=None):
        # list all or filter by 'YYYY-MM' prefix
        if mth is None:
            cur = self.conn.execute(
                "SELECT * FROM expenses ORDER BY date DESC, id DESC"
            )
        else:
            patt = mth + "%"
            cur = self.conn.execute(
                "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC, id DESC",
                (patt,),
            )
        return cur.fetchall()

    def setBudget(self, cat, lim):
        # upsert: update monthly limit if category already exists
        with self.conn:
            self.conn.execute(
                "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?) "
                "ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit",
                (cat, lim),
            )

    def get_bgt(self, cat):
        cur = self.conn.execute("SELECT * FROM budgets WHERE category = ?", (cat,))
        return cur.fetchone()

    def all_budgets(self):
        # alphabetized list of budgets
        cur = self.conn.execute("SELECT * FROM budgets ORDER BY category")
        return cur.fetchall()

    def month_sum(self, cat, mth):
        # sum of expenses for this category in given month
        patt = mth + "-%"
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = ? AND date LIKE ?",
            (cat, patt),
        )
        return cur.fetchone()[0]

    def updExpense(self, exp_id, amt, cat, desc, dt):
        with self.conn:
            cur = self.conn.execute(
                "UPDATE expenses SET amount = ?, category = ?, description = ?, date = ? WHERE id = ?",
                (amt, cat, desc, dt, exp_id),
            )
        return cur.rowcount

    def del_exp(self, exp_id):
        # returns 0 if nothing matched
        with self.conn:
            cur = self.conn.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
        return cur.rowcount

    def close(self):
        self.conn.close()
