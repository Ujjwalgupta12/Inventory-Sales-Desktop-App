from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from db import initialize_database, verify_login
import sys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operator Login")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(QLabel("Login Form"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        if verify_login(username, password):
            from main import MainDashboard
            self.main_dashboard = MainDashboard()
            self.main_dashboard.show()
            self.close()

            # 🔜 Here we’ll launch main.py or show the dashboard
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

if __name__ == "__main__":
    initialize_database()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
