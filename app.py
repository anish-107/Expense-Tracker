from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit,
    QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses, add_expenses, delete_expenses


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()

    def settings(self):
        """
        Sets up the window's geometry and title.
        """
        self.setGeometry(750, 300, 550, 500)
        self.setWindowTitle("Expense Tracker App")

    def initUI(self):
        """
        Initializes the UI components like date picker, dropdowns, buttons, and table.
        """
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.date_box.setDisplayFormat("yyyy-MM-dd")
        self.date_box.setFixedWidth(150)
        self.date_box.setFixedHeight(40)

        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton("Add Expense")
        self.btn_del = QPushButton("Delete Expense")

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_dropdown()
        self.btn_add.clicked.connect(self.add_expense)
        self.btn_del.clicked.connect(self.delete_expense)

        self.apply_styles()

        self.setup_layout()

    def setup_layout(self):
        """
        Configures the layout of the widgets on the window.
        """
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_del)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f9fc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
                color: #333;
            }

            QLabel {
                font-size: 15px;
                color: #34495e;
                font-weight: bold;
                margin: 5px;
            }

            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 2px solid #dcdde1;
                border-radius: 6px;
                font-size: 14px;
                background-color: #ffffff;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #3498db;
            }

            QPushButton {
                padding: 10px 20px;
                background-color: #27ae60;
                color: #fff;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2ecc71;
            }

            QPushButton:pressed {
                background-color: #229954;
            }

            QTableWidget {
                background-color: #ffffff;
                gridline-color: #ecf0f1;
                border: 1px solid #dcdde1;
                border-radius: 6px;
                font-size: 14px;
            }

            QTableWidget::item {
                padding: 5px;
            }

            QTableWidget::item:selected {
                background-color: #3498db;
                color: #ffffff;
            }

            QHeaderView::section {
                background-color: #34495e;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border: none;
                padding: 8px;
                text-align: left;
            }
        """)

    def populate_dropdown(self):
        """
        Populates the category dropdown with predefined options.
        """
        categories = ["Food", "Rent", "Bills", "Entertainment", "Shopping", "Other"]
        self.dropdown.addItems(categories)

    def load_table_data(self):
        """
        Loads the data from the database into the table.
        """
        expenses = fetch_expenses()
        self.table.setRowCount(0)  # Reset the table to empty

        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        """
        Clears the input fields after an operation.
        """
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        """
        Adds a new expense to the database.
        """
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()  # Fixed issue with incorrect operator

        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description cannot be empty.")
            return

        if add_expenses(date, category, amount, description):
            self.load_table_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense.")

    def delete_expense(self):
        """
        Deletes the selected expense from the database.
        """
        selected_row = self.table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Uh oh", "You need to choose a row to delete.")
            return

        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm",
            "Are you sure you want to delete?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()