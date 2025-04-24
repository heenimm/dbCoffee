DB_PATH = 'release/data/coffee.sqlite'

import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem
)
from release.UI.mainwindow import Ui_MainWindow
from release.UI.addeditform import Ui_AddEditCoffeeForm

DB_PATH = 'release/data/coffee.sqlite'


class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None, row_data=None):
        super().__init__(parent)
        self.setupUi(self)
        self.row_data = row_data

        if row_data:
            self.nameLineEdit.setText(row_data[1])
            self.roastLineEdit.setText(row_data[2])
            self.typeComboBox.setCurrentText(row_data[3])
            self.descriptionLineEdit.setText(row_data[4])
            self.priceLineEdit.setText(str(row_data[5]))
            self.volumeLineEdit.setText(str(row_data[6]))

        self.saveButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.reject)

    def save_data(self):
        try:
            data = (
                self.nameLineEdit.text(),
                self.roastLineEdit.text(),
                self.typeComboBox.currentText(),
                self.descriptionLineEdit.text(),
                float(self.priceLineEdit.text()),
                int(self.volumeLineEdit.text())
            )
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат цены или объема")
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

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


class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
                self.coffeeTable.setItem(i, j, QTableWidgetItem(str(item)))
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
        row_data = [self.coffeeTable.item(row, col).text() for col in range(7)]
        row_data[0] = int(row_data[0])
        row_data[5] = float(row_data[5])
        row_data[6] = int(row_data[6])

        dialog = AddEditCoffeeForm(self, row_data)
        if dialog.exec():
            self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
