import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

import requests
import json

class Client(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.email = ""
        self.pwd = ""

    def initUI(self):
        email = QLabel('email', self)
        font = email.font()
        font.setPointSize(10)
        email.setFont(font)

        email.move(20, 20)

        pwd = QLabel('password', self)
        font = pwd.font()
        font.setPointSize(10)

        pwd.move(19, 50)

        email_input = QLineEdit(self)
        email_input.move(83, 17)
        email_input.resize(100, 20)
        email_input.textChanged[str].connect(self.emailInput)

        pwd_input = QLineEdit(self)
        pwd_input.move(83, 47)
        pwd_input.resize(100, 20)
        pwd_input.textChanged[str].connect(self.pwInput)

        btn = QPushButton('Submit', self)
        btn.move(70, 80)
        btn.clicked.connect(self.submit)

        self.setWindowTitle('Classto')
        self.setWindowIcon(QIcon('c:/programming/client-background/public/logo.png'))
        self.setFixedSize(220, 110)
        self.show()

    def pwInput(self, pwd):
        self.pwd = pwd
    
    def emailInput(self, email):
        self.email = email

    def submit(self):
        with open("config.json") as config:
            data = json.load(config)
            self.url = data["url"]

        user = requests.post(self.url + "/auth/login/", json = {"email" : self.email, "pw" : self.pwd})

        if user.status_code == 200:
            with open("config.json", "w") as config:
                json.dump({"email" : self.email, "pwd" : self.pwd, "url" : self.url}, config)

            QMessageBox.about(self, "User", "login success")
            QCoreApplication.instance().quit()

        elif not user.status_code == 200:
            QMessageBox.critical(self, "Warning", "User not found")

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Client()
   sys.exit(app.exec_())
