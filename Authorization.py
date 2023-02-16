from PyQt5.Qt import *
from PyQt5 import QtCore
import sqlite3
from Registration import MainWindow
from Сipher import *
from Checkers import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 350)
        self.u_name_label = QLabel(MainWindow)
        self.u_name_label.setGeometry(QRect(150, 100, 80, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.u_name_label.setFont(font)
        self.u_name_label.setAlignment(Qt.AlignCenter)
        self.u_name_label.setObjectName("u_name_label")
        self.password_linel = QLabel(MainWindow)
        self.password_linel.setGeometry(QRect(150, 140, 80, 20))
        font = QFont()
        font.setPointSize(10)
        self.password_linel.setFont(font)
        self.password_linel.setAlignment(Qt.AlignCenter)
        self.password_linel.setObjectName("password_linel")
        self.username_linet = QLineEdit(MainWindow)
        self.username_linet.setGeometry(QRect(220, 100, 120, 25))
        self.username_linet.setObjectName("username_linet")
        self.pass_lineEdit = QLineEdit(MainWindow)
        self.pass_lineEdit.setGeometry(QRect(220, 140, 120, 25))
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.login_btn = QPushButton(MainWindow)
        self.login_btn.setGeometry(QRect(180, 180, 50, 25))
        self.login_btn.setObjectName("login_btn")
        self.signup_btn = QPushButton(MainWindow)
        self.signup_btn.setGeometry(QRect(240, 180, 120, 25))
        self.signup_btn.setObjectName("signup_btn")
        self.label = QLabel(MainWindow)
        self.label.setGeometry(QRect(100, 20, 400, 80))
        font = QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Авторизация"))
        self.label.setText(_translate("MainWindow", "Итальянские Шашки"))
        self.u_name_label.setText(_translate("MainWindow", "Логин"))
        self.password_linel.setText(_translate("MainWindow", "Пароль"))
        self.login_btn.setText(_translate("MainWindow", "Войти"))
        self.signup_btn.setText(_translate("MainWindow", "Зарегистрироваться"))


class LoginDatabase():
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def is_table(self, table_name):
        query = "SELECT name from sqlite_master WHERE type='table' AND name='{}';".format(table_name)
        cursor = self.conn.execute(query)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True


class MainMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.login_btn.clicked.connect(self.loginCheck)
        self.signup_btn.clicked.connect(self.signUpCheck)


    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def signUpShow(self):
        self.signUpWindow = MainWindow(self)
        self.signUpWindow.show()

    @QtCore.pyqtSlot()
    def loginCheck(self):
        

        username = trippledesencrypt(self.username_linet.text())
        password = trippledesencrypt(self.pass_lineEdit.text())
        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Ошибка', 'Вы не заполнили все поля.')
            return


        file = open('user_data.txt', 'r', encoding='utf-8')
        text = file.readlines()
        file.close()

        for i in range(len(text)):
            if i < (len(text) - 1):
                text[i] = text[i][:-1]
            row = text[i].split(" ")
            flag = True
            if username == row[0] and password == row[2]:
                self.close()
                flag = False
                run()
                break

        if flag:
            self.showMessageBox('Внимание!', 'Неправильное имя пользователя или пароль.')


    def signUpCheck(self):
        self.signUpShow()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainMainWindow()
    w.show()
    sys.exit(app.exec_())