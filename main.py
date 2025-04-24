import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QMessageBox
)
from PyQt6 import uic

DB_PATH = 'coffee.sqlite'

class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, row_data=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.row_data = row_data

        if row_data:
            self.nameLineEdit.setText(row_data[1])
            self.roastLineEdit.setText(row_data[2])
            index = self.typeComboBox.findText(row_data[3])
            self.typeComboBox.setCurrentIndex(index if index >= 0 else 0)
            self.descriptionLineEdit.setText(row_data[4])
            self.priceLineEdit.setText(row_data[5])
            self.volumeLineEdit.setText(row_data[6])
        self.saveButton.clicked.connect(self.save_data)

    def save_data(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        data = (
            self.nameLineEdit.text(),
            self.roastLineEdit.text(),
            self.typeComboBox.currentText(),
            self.descriptionLineEdit.text(),
            self.priceLineEdit.text(),
            self.volumeLineEdit.text(),
        )
        if self.row_data:
            cur.execute("""
                UPDATE coffee SET name=?, roast=?, form=?, description=?, price=?, volume=?
                WHERE id=?
            """, data + (self.row_data[0],))
        else:
            cur.execute("""
                INSERT INTO coffee (name, roast, form, description, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)
        conn.commit()
        conn.close()
        self.accept()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.coffeeTable.setRowCount(0)
        self.coffeeTable.setRowCount(len(result))
        self.coffeeTable.setColumnCount(7)
        for i, row in enumerate(result):
            for j, item in enumerate(row):
                self.coffeeTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))
        conn.close()

    def add_record(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec():
            self.load_data()

    def edit_record(self):
        row = self.coffeeTable.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для редактирования")
            return
        row_data = [
            self.coffeeTable.item(row, col).text() for col in range(7)
        ]
        row_data[0] = int(row_data[0])  # ID как int

        dialog = AddEditCoffeeForm(self, row_data)
        if dialog.exec():
            self.load_data()


if __name__ == "__main__":
    from PyQt6 import QtWidgets
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
