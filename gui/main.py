import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox
)


API_URL = "http://127.0.0.1:5000/users"


class UserManagementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management System")
        self.setGeometry(100, 100, 700, 450)

        self.selected_user_id = None

        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone")

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city")

        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Phone"))
        layout.addWidget(self.phone_input)

        layout.addWidget(QLabel("City"))
        layout.addWidget(self.city_input)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user)

        self.update_button = QPushButton("Update User")
        self.update_button.clicked.connect(self.update_user)

        self.delete_button = QPushButton("Delete User")
        self.delete_button.clicked.connect(self.delete_user)

        self.refresh_button = QPushButton("Refresh Users")
        self.refresh_button.clicked.connect(self.load_users)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)

        layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "City"])
        self.table.cellClicked.connect(self.select_user)

        layout.addWidget(self.table)

        self.setLayout(layout)

    def add_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        city = self.city_input.text()

        if not name or not email or not phone or not city:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "city": city
        }

        try:
            response = requests.post(API_URL, json=data)
            result = response.json()

            if response.status_code == 201:
                QMessageBox.information(self, "Success", result["message"])
                self.clear_inputs()
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", result.get("error", "Something went wrong"))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not connect to API:\n{str(e)}")

    def load_users(self):
        try:
            response = requests.get(API_URL)
            users = response.json()

            self.table.setRowCount(len(users))

            for row, user in enumerate(users):
                self.table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
                self.table.setItem(row, 1, QTableWidgetItem(user["name"]))
                self.table.setItem(row, 2, QTableWidgetItem(user["email"]))
                self.table.setItem(row, 3, QTableWidgetItem(user["phone"]))
                self.table.setItem(row, 4, QTableWidgetItem(user["city"]))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load users:\n{str(e)}")

    def select_user(self, row, column):
        self.selected_user_id = int(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.email_input.setText(self.table.item(row, 2).text())
        self.phone_input.setText(self.table.item(row, 3).text())
        self.city_input.setText(self.table.item(row, 4).text())

    def update_user(self):
        if self.selected_user_id is None:
            QMessageBox.warning(self, "Error", "Please select a user to update")
            return

        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        city = self.city_input.text()

        if not name or not email or not phone or not city:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "city": city
        }

        try:
            response = requests.put(f"{API_URL}/{self.selected_user_id}", json=data)
            result = response.json()

            if response.status_code == 200:
                QMessageBox.information(self, "Success", result["message"])
                self.clear_inputs()
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", result.get("error", "Something went wrong"))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not connect to API:\n{str(e)}")

    def delete_user(self):
        if self.selected_user_id is None:
            QMessageBox.warning(self, "Error", "Please select a user to delete")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                response = requests.delete(f"{API_URL}/{self.selected_user_id}")
                result = response.json()

                if response.status_code == 200:
                    QMessageBox.information(self, "Success", result["message"])
                    self.clear_inputs()
                    self.load_users()
                else:
                    QMessageBox.warning(self, "Error", result.get("error", "Something went wrong"))

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not connect to API:\n{str(e)}")

    def clear_inputs(self):
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.city_input.clear()
        self.selected_user_id = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserManagementApp()
    window.show()
    sys.exit(app.exec_())