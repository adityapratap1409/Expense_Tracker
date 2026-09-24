import sqlite3
class Storage:
    def __init__(self, db_path="expenses.db" ):
        self.conn=sqlite3.connect(db_path)
        self.conn.row_factory=sqlite3.Row
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
            cur=self.conn.execute(
                "INSERT INTO expenses (amount, category, description, date) "
                "VALUES (?,?,?,?)",
                (amount, category, description, date)
            )
        return cur.lastrowid


    def get_expense(self, expense_id):
        cur=self.conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id, ))
        return cur.fetchone()


    # def list_expenses(self):


    # def set_budget(self, category, monthly_limit):


    # def get_budget(self, category):


    # def list_budgets(self):

    # def get_month_total(self, category, month):


 
