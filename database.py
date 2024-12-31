import os
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

# Define a user-friendly directory for the database
def get_db_path(db_name):
    app_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "ExpenseTracker")
    os.makedirs(app_data_dir, exist_ok=True)  # Create the directory if it doesn't exist
    return os.path.join(app_data_dir, db_name)

def init_db(db_name):
    """
    Initializes the SQLite database connection and creates the expenses table if it doesn't exist.
    """
    db_path = get_db_path(db_name)

    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_path)

    if not database.open():
        return False

    query = QSqlQuery()
    query.exec("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)

    return True

def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        expenses.append([query.value(i) for i in range(5)])
    return expenses

def add_expenses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)
    return query.exec()

def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)
    return query.exec()
