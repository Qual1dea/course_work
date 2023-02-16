from PyQt5.Qt import *
from Сipher import *

class Ui_signUp(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 450)
        self.label = QLabel(MainWindow)
        self.label.setGeometry(QRect(170, 140, 80, 25))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QLabel(MainWindow)
        self.label_2.setGeometry(QRect(170, 220, 80, 25))
        font = QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(MainWindow)
        self.label_3.setGeometry(QRect(170, 180, 80, 25))
        font = QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.username_linet = QLineEdit(MainWindow)
        self.username_linet.setGeometry(QRect(220, 140, 140, 25))
        self.username_linet.setObjectName("username_linet")
        self.email_lineEdit = QLineEdit(MainWindow)
        self.email_lineEdit.setGeometry(QRect(220, 180, 140, 25))
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.password_lineEdit = QLineEdit(MainWindow)
        self.password_lineEdit.setGeometry(QRect(220, 220, 140, 25))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.signup_btn = QPushButton(MainWindow)
        self.signup_btn.setGeometry(QRect(215, 260, 150, 30))
        self.signup_btn.setObjectName("signup_btn")
        self.label_4 = QLabel(MainWindow)
        self.label_4.setGeometry(QRect(120, 50, 300, 100))
        font = QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация"))
        self.label.setText(_translate("MainWindow", "Логин"))
        self.label_2.setText(_translate("MainWindow", "Пароль"))
        self.label_3.setText(_translate("MainWindow", "Email"))
        self.signup_btn.setText(_translate("MainWindow", "Зарегистрироваться"))
        self.label_4.setText(_translate("MainWindow", "Регистрация аккаунта"))


class MainWindow(QMainWindow, Ui_signUp):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.signup_btn.clicked.connect(self.insertData)

    @pyqtSlot()
    def insertData(self):


        username = trippledesencrypt(self.username_linet.text())
        email = trippledesencrypt(self.email_lineEdit.text())
        password = trippledesencrypt(self.password_lineEdit.text())

        file = open('user_data.txt', 'r', encoding='utf-8')
        text = file.readlines()
        file.close()

        if (not username) or (not email) or (not password):
            msg = QMessageBox.information(self, 'Ошибка', 'Вы не заполнили все поля.')
            return

        flag = True
        for i in range(len(text)):
            text[i] = text[i][:-1]
            row = text[i].split(" ")
            if username == row[0]:
                msg = QMessageBox.information(self, 'Ошибка', 'Пользователь с таким логином уже зарегистрирован.')
                flag = False
                break

        if flag:
            # if log != row[0] and email != row[1]:
            file = open('user_data.txt', 'a', encoding='utf-8')
            file.write('\n' + username + ' ' + email + ' ' + password)
            file.close()
            self.close()


if __name__ == "__main__":
    import sys
    app    = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())