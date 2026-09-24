import sqlite3


class Storage:
    def __init__(self, db_path="expenses.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount>0),
        description TEXT
         )
     """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL UNIQUE,
                monthly_limit REAL NOT NULL CHECK(monthly_limit>0)
            )
        """)

        self.conn.commit()

    def add_expense(self, amount, category, description, date):
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO expenses (amount, category, description, date) "
                "VALUES (?,?,?,?)",
                (amount, category, description, date),
            )
        return cur.lastrowid

    def get_expense(self, expense_id):
        cur = self.conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        return cur.fetchone()

    def list_expenses(self, month=None):
        if month is None:
            cur = self.conn.execute(
                "SELECT * FROM expenses ORDER BY date DESC, id DESC"
            )
        else:
            cur = self.conn.execute(
                "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC, id DESC",
                (month + "-%",),
            )
        return cur.fetchall()

    def set_budget(self, category, monthly_limit):
        with self.conn:
            self.conn.execute(
                "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?) "
                "ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit",
                (category, monthly_limit),
            )

    def get_budget(self, category):
        cur = self.conn.execute("SELECT * FROM budgets WHERE category= ?", (category,))
        return cur.fetchone()

    def list_budgets(self):
        cur = self.conn.execute("SELECT * FROM budgets ORDER BY category ")
        return cur.fetchall()

    def get_month_total(self, category, month):
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = ? AND date LIKE ?",
            (category, month + "-%"),
        )
        return cur.fetchone()[0]

    def close(self):
        self.conn.close()
