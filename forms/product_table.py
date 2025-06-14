from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
import sqlite3

class ProductTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master List")
        self.setFixedSize(900, 500)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(QLabel("All Products"))
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT barcode, sku, category, subcategory, name, price, tax, unit, image_path FROM product_master")
        rows = cursor.fetchall()
        conn.close()

        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Barcode", "SKU", "Category", "Subcategory", "Name", "Price", "Tax", "Unit", "Image Path"])
        self.table.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell)))
