import sqlite3


# TODO: maybe look into using an ORM later if this gets too big,
# but raw sqlite is fine for a simple tracker script right now.
class Storage:
    def __init__(self, db_path="expenses.db"):
        # saving path just in case we need it later lol
        self.db_file = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        # creating tables if they don't already exist
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount>0),
        description TEXT
         )
     """)

        # separate table for budgets, added this later after v1
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL UNIQUE,
                monthly_limit REAL NOT NULL CHECK(monthly_limit>0)
            )
        """)

        self.conn.commit()

    def add_expense(self, amount, category, description, date):
        # wait, sometimes people pass date first, sometimes amount first...
        # just make sure the SQL matches what's expected.
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO expenses (amount, category, description, date) "
                "VALUES (?,?,?,?)",
                (amount, category, description, date),
            )
        return cur.lastrowid

    def get_expense(self, expense_id):
        # simple fetch by id
        cur = self.conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = cur.fetchone()
        return row

    def list_expenses(self, month=None):
        # month should probably be like '2023-11' format
        if month is None:
            cur = self.conn.execute(
                "SELECT * FROM expenses ORDER BY date DESC, id DESC"
            )
        else:
            # using LIKE for filtering by month string prefix
            query_filter = month + "%"
            cur = self.conn.execute(
                "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC, id DESC",
                (query_filter,),
            )

        results = cur.fetchall()
        return results

    def set_budget(self, category, monthly_limit):
        # upsert logic for budgets
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
        # let's just grab everything ordered by category name alphabetically
        cur = self.conn.execute("SELECT * FROM budgets ORDER BY category ")
        return cur.fetchall()

    def get_month_total(self, category, month):
        # Calculates sum for a specific category in a given month
        patt = month + "-%"
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = ? AND date LIKE ?",
            (category, patt),
        )
        val = cur.fetchone()[0]
        return val

    def update_expense(self, expense_id, amount, category, description, date):
        with self.conn:
            cur = self.conn.execute(
                "UPDATE expenses SET amount = ?, category = ?, description = ?, date = ? WHERE id = ?",
                (amount, category, description, date, expense_id),
            )
        return cur.rowcount

    def delete_expense(self, expense_id):
        with self.conn:
            cur = self.conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cur.rowcount

    def close(self):
        self.conn.close()
