import json
import sys

from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt, QDate, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCalendarWidget

import hrd_bkend
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
        if chklogin:
            self.MainWindow = MainWindow(chklogin)
            self.MainWindow.show()
            self.hide()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("아이디 또는 패스워드가 맞지 않습니다!")
            msg.exec_()


class MainWindow(QMainWindow, main_class):
    def __init__(self, session):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.session = session
        self.startDate.setDate(QDate.currentDate())
        self.endDate.setDate(QDate.currentDate().addMonths(3))
        self.startDateToolBtn.clicked.connect(self.ToggleCalendarWidget)
        self.endDateToolBtn.clicked.connect(self.ToggleCalendarWidget)
        self.cal = [QCalendarWidget(), QCalendarWidget()]
        self.cal[0].setObjectName('startCal')
        self.cal[1].setObjectName('endCal')
        [i.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) for i in self.cal]
        [i.setVerticalHeaderFormat(False) for i in self.cal]
        [i.clicked.connect(self.setDateFromCalendar) for i in self.cal]
        self.isCalOpened = [False, False]
        self.Worker = QThread()

        self.area = {}
        with open("areaCd.json", 'r', encoding='utf-8') as f:
            self.area = json.load(f)

        self.upperAreaCd.addItems(self.area)
        self.upperAreaCd.currentTextChanged.connect(self.upperAreaCdChanged)

        self.ncs = {}
        with open("ncsCd.json", 'r', encoding='utf-8') as f:
            self.ncs = json.load(f)

        self.upperNcsCd.addItems(self.ncs)
        self.upperNcsCd.currentTextChanged.connect(self.upperNcsCdChanged)
        self.middleNcsCd.currentTextChanged.connect(self.middleNcsCdChanged)
        self.smallNcsCd.currentTextChanged.connect(self.smallNcsCdChanged)

        self.crse = {}
        with open("crseTracseSeCd.json", 'r', encoding='utf-8') as f:
            self.crse = json.load(f)

        self.upperType.addItems(self.crse)
        self.middleType.addItems(self.crse['전체'])
        self.upperType.currentTextChanged.connect(self.upperCrseCdChanged)

        self.execBtn.clicked.connect(self.executeScript)

    def getNcsCode(self):
        ret = ''
        depth = 0
        Text = [
            self.upperNcsCd.currentText(),
            self.middleNcsCd.currentText(),
            self.smallNcsCd.currentText(),
            self.miscNcsCd.currentText()
        ]
        if Text[0] == '전체':
            return None
        else:
            if list(self.ncs).index(Text[0]) < 10:
                ret += '0' + str(list(self.ncs).index(Text[0]) + 1)
            else:
                ret += list(self.ncs).index(Text[0]) + 1

            ret += '0' + str(list(self.ncs[Text[0]]).index(Text[1]) + 1)

            if Text[2] != '전체':
                ret += '0' + str(list(self.ncs[Text[0]][Text[1]]).index(Text[2]))
            if Text[3] != '전체' and Text[3] != '':
                ret += '0' + str(list(self.ncs[Text[0]][Text[1]][Text[2]]).index(Text[3]))

            for i in range(len(Text)):
                if Text[i] == '전체' or Text[i] == '':
                    break
                depth += 1

            if depth == 4:
                return ret + "|" + Text[depth - 1]
            else:
                return ret + "|" + Text[depth - 1] + "  " + Text[depth]

    def getAreaCode(self):
        upperText = self.upperAreaCd.currentText()
        Text = self.areaCd.currentText()
        if upperText == '전체':
            return self.area[upperText]
        else:
            return self.area[upperText][Text] if upperText != '전체' or upperText == '' else ''

    def getCrseCode(self):
        upperText = self.upperType.currentText()
        Text = self.middleType.currentText()
        if list(self.crse).index(upperText) + 1 == 1:
            return '', self.crse[upperText][Text]
        else:
            return str(list(self.crse).index(upperText) + 1), self.crse[upperText][Text]

    def upperCrseCdChanged(self):
        upperText = self.upperType.currentText()
        self.middleType.clear()
        self.middleType.addItems(self.crse[upperText])

    def upperAreaCdChanged(self):
        upperText = self.upperAreaCd.currentText()
        if upperText != '전체':
            self.areaCd.clear()
            self.areaCd.addItems(self.area[upperText])
        else:
            self.areaCd.clear()

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

    def upperNcsCdChanged(self):
        upperText = self.upperNcsCd.currentText()
        if upperText != '전체':
            self.middleNcsCd.clear()
            self.middleNcsCd.addItems(self.ncs[f'{upperText}'])
        else:
            self.middleNcsCd.clear()

    def middleNcsCdChanged(self):
        try:
            upperText = self.upperNcsCd.currentText()
            middleText = self.middleNcsCd.currentText()
            if middleText != '전체':
                self.smallNcsCd.clear()
                self.smallNcsCd.addItems(self.ncs[f'{upperText}'][f'{middleText}'])
            else:
                self.smallNcsCd.clear()
        except KeyError:
            pass

    def smallNcsCdChanged(self):
        try:
            upperText = self.upperNcsCd.currentText()
            middleText = self.middleNcsCd.currentText()
            smallText = self.smallNcsCd.currentText()
            if smallText != '전체':
                self.miscNcsCd.clear()
                self.miscNcsCd.addItems(self.ncs[f'{upperText}'][f'{middleText}'][f'{smallText}'])
            else:
                self.miscNcsCd.clear()
        except KeyError:
            pass

    def executeScript(self):
        print("----- option -----")
        print("keyword = ", self.lineEdit_2.text())
        print(f"areaCode = ", self.getAreaCode())
        print(f"ncsCode = ", self.getNcsCode())
        print(f"{'crseTraceseSe' + self.getCrseCode()[0]}={self.getCrseCode()[1]}")
        print(f"Date = start : {self.startDate.date()} end : {self.endDate.date()}")

        self.Worker = Worker(
            self.session, self.lineEdit_2.text(), self.getCrseCode()[0], self.getCrseCode()[1],
            self.getNcsCode(), self.getAreaCode(),
            self.startDate.date().toString('yyyyMMdd'), self.endDate.date().toString('yyyyMMdd'))
        self.Worker.start()


class Worker(QThread):
    def __init__(self, session, keyword, cCode1, cCode2, nCode, aCode, startDate, endDate, parent=None):
        QThread.__init__(self, parent)
        self.session = session
        self.keyword = keyword
        self.aCode = aCode
        self.nCode = nCode
        self.cCode1 = cCode1
        self.cCode2 = cCode2
        self.startDate = startDate
        self.endDate = endDate

    def run(self):
        hrd_bkend.getDetail(
            self.session, self.keyword,
            self.cCode1, self.cCode2,
            self.nCode, self.aCode,
            self.startDate, self.endDate
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    LW = LoginWindow()
    # LW = MainWindow()
    LW.show()
    app.exec_()
