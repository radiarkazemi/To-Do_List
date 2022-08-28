from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QListWidget, QPushButton, \
    QListWidgetItem, QMessageBox, QLineEdit
from PyQt5 import uic
import sys
import sqlite3
from PyQt5 import QtCore
from QShamsiCalendarWidget import QShamsiCalendarWidget


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("todo_list.ui", self)

        self.list = self.findChild(QListWidget, "listWidget")
        self.save_changes_btn = self.findChild(QPushButton, "save_pushButton")
        # self.delete = self.findChild(QPushButton, "delete_pushButton")
        self.add = self.findChild(QPushButton, "add_pushButton")
        self.add_line = self.findChild(QLineEdit, "addTask_lineEdit")
        self.calendar = QShamsiCalendarWidget(1350, 1450)
        self.calendar.setGeometry(10, 170, 431, 361)
        self.window().layout().addWidget(self.calendar)
        self.save_changes_btn.clicked.connect(self.save_changes)
        self.add.clicked.connect(self.add_new_task)
        # self.delete.clicked.connect(self.delete_task)
        self.calendar_date_changed()

        self.show()

    def calendar_date_changed(self):
        date_selection = self.calendar.sel_date_changed.connect(self.date_changed)
        # self.tasklist(date_selection)

    def date_changed(self):
        date = str(self.calendar.selected_date)
        self.tasklist(date)

    def tasklist(self, date):
        self.list.clear()
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE if not exists todo_list(
            Task text,
        Completed text,
        Date_t timestamp)
        """)
        query = "SELECT Task,Completed FROM todo_list WHERE Date_t = ? "
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.list.addItem(item)

        db.commit()
        db.close()

    def save_changes(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = str(self.calendar.selected_date)
        for i in range(self.list.count()):
            item = self.list.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE todo_list SET Completed='YES' WHERE Task=? AND Date_t=?"
            else:
                query = "UPDATE todo_list SET Completed='NO' WHERE Task=? AND Date_t=?"
            row = (task, date)
            cursor.execute(query, row)
        db.commit()
        msg = QMessageBox()
        msg.setText("Changes Saved!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def add_new_task(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = str(self.calendar.selected_date)
        new_task = str(self.add_line.text())
        query = "INSERT INTO todo_list(Task,Completed,Date_t) VALUES (?,?,?)"
        row = (new_task, 'NO', date,)
        cursor.execute(query, row)
        db.commit()

        self.tasklist(date)
        self.add_line.clear()

    # def delete_task(self):
    #     db = sqlite3.connect("data.db")
    #     cursor = db.cursor()
    #     date = str(self.calendar.selected_date)
    #     delete_task = str(self.list.currentItem())
    #     query = "DELETE FROM todo_list WHERE Task=? AND Date_t=?"
    #     row = (delete_task, date,)
    #     cursor.execute(query, row)
    #     db.commit()
    #
    #     self.tasklist(date)


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
