from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QComboBox,
    QPushButton, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtGui import QPixmap
import sqlite3
import os
import shutil

class ProductForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master Form")
        self.setFixedSize(500, 650)

        layout = QVBoxLayout()

        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Barcode")

        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("SKU ID")

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")

        self.subcategory_input = QLineEdit()
        self.subcategory_input.setPlaceholderText("Subcategory")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product Name")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")

        self.tax_input = QLineEdit()
        self.tax_input.setPlaceholderText("Tax %")

        self.unit_input = QComboBox()
        self.unit_input.addItems(["Units", "Kg", "Liters"])

        self.image_path = ""
        self.image_label = QLabel("No Image Selected")
        self.image_label.setFixedHeight(100)

        self.select_image_btn = QPushButton("Select Product Image")
        self.select_image_btn.clicked.connect(self.select_image)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_form)

        layout.addWidget(QLabel("Product Master Entry"))
        layout.addWidget(self.barcode_input)
        layout.addWidget(self.sku_input)
        layout.addWidget(self.category_input)
        layout.addWidget(self.subcategory_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.price_input)
        layout.addWidget(self.tax_input)
        layout.addWidget(self.unit_input)

        layout.addWidget(self.image_label)
        layout.addWidget(self.select_image_btn)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Product Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path).scaled(100, 100)
            self.image_label.setPixmap(pixmap)

    def submit_form(self):
        barcode = self.barcode_input.text()
        sku = self.sku_input.text()
        category = self.category_input.text()
        subcategory = self.subcategory_input.text()
        name = self.name_input.text()
        desc = self.description_input.toPlainText()
        price = self.price_input.text()
        tax = self.tax_input.text()
        unit = self.unit_input.currentText()

        # Save image to ./images/ directory
        if self.image_path:
            os.makedirs("images", exist_ok=True)
            img_filename = os.path.basename(self.image_path)
            saved_path = os.path.join("images", img_filename)
            shutil.copy(self.image_path, saved_path)
        else:
            saved_path = ""

        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_master (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode TEXT,
                    sku TEXT,
                    category TEXT,
                    subcategory TEXT,
                    name TEXT,
                    description TEXT,
                    price REAL,
                    tax REAL,
                    unit TEXT,
                    image_path TEXT
                )
            """)
            cursor.execute("""
                INSERT INTO product_master (
                    barcode, sku, category, subcategory, name, description, price, tax, unit, image_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (barcode, sku, category, subcategory, name, desc, float(price), float(tax), unit, saved_path))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Saved", "Product saved successfully.")
            self.clear_fields()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error saving product: {str(e)}")

    def clear_fields(self):
        self.barcode_input.clear()
        self.sku_input.clear()
        self.category_input.clear()
        self.subcategory_input.clear()
        self.name_input.clear()
        self.description_input.clear()
        self.price_input.clear()
        self.tax_input.clear()
        self.unit_input.setCurrentIndex(0)
        self.image_label.setText("No Image Selected")
        self.image_label.setPixmap(QPixmap())
        self.image_path = ""
