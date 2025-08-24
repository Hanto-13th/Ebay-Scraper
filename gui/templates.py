from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from PyQt6 import QtGui

def window_settings(self,name,geometry,fixed_size):
    self.setWindowTitle(name)
    self.setGeometry(*geometry)
    self.setFixedSize(*fixed_size)
    self.setWindowIcon(QtGui.QIcon('icon.png'))

def button_template(name,weight,height,connect_func):
        new_button = QPushButton(name)
        new_button.setFixedSize(weight,height)
        new_button.setFlat(True)
        new_button.clicked.connect(connect_func)
        return new_button

def back_button_template(name,widget,geometry,connect_func):
        new_back_button = QPushButton(name,widget)
        new_back_button.setGeometry(*geometry)
        new_back_button.setFlat(True)
        new_back_button.clicked.connect(connect_func)
        return new_back_button


def line_template(weight,height):
        new_line = QLineEdit()
        new_line.setFixedSize(weight,height)
        return new_line


def alert_label_template(widget,geometry):
        new_alert_label = QLabel(widget)
        new_alert_label.setGeometry(*geometry)
        new_alert_label.hide()
        return new_alert_label

def display_alert(self,alert_label,text,time,connect_func):
        alert_label.setText(text)
        alert_label.show()
        if time != "inf":
            self.timer = QTimer()
            self.timer.timeout.connect(connect_func)
            self.timer.start(time)

