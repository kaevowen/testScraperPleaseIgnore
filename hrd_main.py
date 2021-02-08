import sys

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCalendarWidget, QWidget, QToolButton
from PyQt5.QtCore import Qt, QThread, QDate, pyqtSignal, pyqtSlot, QSize, QObject
from PyQt5 import uic, QtGui
from datetime import datetime, timedelta

import hrd_login

login_class = uic.loadUiType("login_gui.ui")[0]
main_class = uic.loadUiType("main_gui.ui")[0]


class LoginWindow(QMainWindow, login_class):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.loginBtn.clicked.connect(self.login)
        self.PWbox.returnPressed.connect(self.login)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.MainWindow = object()

    def login(self):
        hrd_id = self.IDbox.text()
        hrd_pw = self.PWbox.text()
        chklogin = hrd_login.chkLogin(hrd_id, hrd_pw)
        if chklogin == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("아이디 또는 패스워드가 맞지 않습니다!")
            msg.exec_()

        elif chklogin == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("api키를 불러올 수 없습니다. 마이 페이지에서 발급받아주세요.")
            msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("로그인 성공!")
            msg.exec_()


class MainWindow(QMainWindow, main_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.startDateToolBtn.clicked.connect(self.ToggleCalendarWidget)
        self.endDateToolBtn.clicked.connect(self.ToggleCalendarWidget)
        self.cal = [QCalendarWidget(), QCalendarWidget()]
        self.cal[0].setObjectName('startCal')
        self.cal[1].setObjectName('endCal')
        [i.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) for i in self.cal]
        [i.setVerticalHeaderFormat(False) for i in self.cal]
        [i.clicked.connect(self.setDateFromCalendar) for i in self.cal]
        self.isCalOpened = [False, False]

    def ToggleCalendarWidget(self):
        idx = 0 if self.sender().objectName() == 'startDateToolBtn' else 1
        if not self.isCalOpened[idx]:
            p = QtGui.QCursor.pos()
            self.cal[idx].setGeometry(p.x(), p.y() + 10, 281, 183)
            self.isCalOpened[idx] = not self.isCalOpened[idx]
            self.cal[idx].show()
        else:
            self.isCalOpened[idx] = not self.isCalOpened[idx]
            self.cal[idx].hide()

    def setDateFromCalendar(self):
        if self.sender().objectName() == 'startCal':
            self.startDate.setDate(self.cal[0].selectedDate())
            self.cal[0].hide()
            self.isCalOpened[0] = not self.isCalOpened[0]

        else:
            self.endDate.setDate(self.cal[1].selectedDate())
            self.cal[1].hide()
            self.isCalOpened[1] = not self.isCalOpened[1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # LW = LoginWindow()
    LW = MainWindow()
    LW.show()
    app.exec_()