import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from forms.receiving_form import GoodsForm
from forms.sales_form import SalesForm
from forms.Product_form import ProductForm
from forms.product_table import ProductTable

class MainDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infotech Dashboard")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Choose a Form"))

        btn_goods = QPushButton("Goods Receiving")
        btn_sales = QPushButton("Sales Form")
        btn_product = QPushButton("Product Master")
        btn_table = QPushButton("View Saved Products")

        btn_goods.clicked.connect(self.open_goods_form)
        btn_sales.clicked.connect(self.open_sales_form)
        btn_product.clicked.connect(self.open_product_form)
        btn_table.clicked.connect(self.open_product_table)

        layout.addWidget(btn_goods)
        layout.addWidget(btn_sales)
        layout.addWidget(btn_product)
        layout.addWidget(btn_table)

        self.setLayout(layout)

    def open_goods_form(self):
        self.goods_form = GoodsForm()
        self.goods_form.show()

    def open_sales_form(self):
        self.sales_form = SalesForm()
        self.sales_form.show()

    def open_product_form(self):
        self.product_form = ProductForm()
        self.product_form.show()
    
    def open_product_table(self):
        self.product_table = ProductTable()
        self.product_table.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDashboard()
    window.show()
    sys.exit(app.exec())
