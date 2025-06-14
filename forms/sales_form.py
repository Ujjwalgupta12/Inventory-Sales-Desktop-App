from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QMessageBox
)
import sqlite3

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Form")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Product Name")

        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("Customer Name")

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        self.quantity_input.textChanged.connect(self.update_totals)

        self.unit_input = QComboBox()
        self.unit_input.addItems(["Units", "Kg", "Liters"])

        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("Rate per Unit")
        self.rate_input.textChanged.connect(self.update_totals)

        self.total_rate_label = QLabel("Total Rate: ₹0.00")
        self.tax_input = QLineEdit()
        self.tax_input.setPlaceholderText("Tax %")
        self.tax_input.textChanged.connect(self.update_totals)

        self.final_amount_label = QLabel("Final Amount: ₹0.00")

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_form)

        layout.addWidget(QLabel("Sales Form"))
        layout.addWidget(self.product_input)
        layout.addWidget(self.customer_input)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.unit_input)
        layout.addWidget(self.rate_input)
        layout.addWidget(self.total_rate_label)
        layout.addWidget(self.tax_input)
        layout.addWidget(self.final_amount_label)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def update_totals(self):
        try:
            qty = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            tax = float(self.tax_input.text() or 0)
        except ValueError:
            self.total_rate_label.setText("Total Rate: ₹0.00")
            self.final_amount_label.setText("Final Amount: ₹0.00")
            return

        total = qty * rate
        final = total + (total * tax / 100)

        self.total_rate_label.setText(f"Total Rate: ₹{total:.2f}")
        self.final_amount_label.setText(f"Final Amount: ₹{final:.2f}")

    def submit_form(self):
        product = self.product_input.text()
        customer = self.customer_input.text()
        quantity = self.quantity_input.text()
        unit = self.unit_input.currentText()
        rate = self.rate_input.text()
        tax = self.tax_input.text()

        try:
            qty = float(quantity)
            rate = float(rate)
            tax_val = float(tax)
            total = qty * rate
            final = total + (total * tax_val / 100)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for Quantity, Rate, and Tax.")
            return

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                customer TEXT,
                quantity REAL,
                unit TEXT,
                rate REAL,
                total REAL,
                tax REAL,
                final_amount REAL
            )
        """)
        cursor.execute("""
            INSERT INTO sales (product, customer, quantity, unit, rate, total, tax, final_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (product, customer, qty, unit, rate, total, tax_val, final))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Sales entry saved successfully!")
        self.clear_fields()

    def clear_fields(self):
        self.product_input.clear()
        self.customer_input.clear()
        self.quantity_input.clear()
        self.rate_input.clear()
        self.tax_input.clear()
        self.unit_input.setCurrentIndex(0)
        self.total_rate_label.setText("Total Rate: ₹0.00")
        self.final_amount_label.setText("Final Amount: ₹0.00")
