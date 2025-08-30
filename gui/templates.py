from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtGui

"""Functions introduce all templates for the windows (label,line,button...) and functions (display errors)"""

def window_settings(self,name,geometry,fixed_size):
    self.setWindowTitle(name)
    self.setGeometry(*geometry)
    self.setFixedSize(*fixed_size)
    self.setWindowIcon(QtGui.QIcon('icon.png'))
    self.setStyleSheet("QWidget {background-color: #FFFFFF;" \
                            "border: 5px groove #A799FA;" \
                            "padding: 10px;}")

def button_template(name,width,height,connect_func):
        new_button = QPushButton(name)
        new_button.setFixedSize(width,height)
        new_button.setFlat(True)
        new_button.clicked.connect(connect_func)
        new_button.setStyleSheet("background-color: #E2EAF4;" \
                            "border: 2px groove #A799FA;" \
                            "padding: 5px;" \
                            "font-size: 12px;" \
                            "font-weight: bold;" \
                        "color: #33324D")
        
        return new_button

def back_button_template(name,widget,geometry,connect_func):
        new_back_button = QPushButton(name,widget)
        new_back_button.setGeometry(*geometry)
        new_back_button.setFlat(True)
        new_back_button.clicked.connect(connect_func)
        new_back_button.setStyleSheet("background-color: #E2EAF4;" \
                            "border: 1px groove #A799FA;" \
                            "padding: 1px;")
        return new_back_button


def line_template(width,height):
        new_line = QLineEdit()
        new_line.setFixedSize(width,height)
        new_line.setStyleSheet("background-color: #E2EAF4;" \
                            "border: 1px groove #A799FA;" \
                            "padding: 0px;")
        return new_line

def label_template(text,width,height):
        new_label = QLabel()
        new_label.setText(text)
        new_label.setFixedSize(width,height)
        new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        new_label.setStyleSheet("background-color: #FFFFFF;" \
                                "font-size: 12px ;" \
                                "font-weight: bold;" \
                                "color: #33324D;"
                                "padding: 0px;"
                                "border: 1px groove #FFFFFF;")
        return new_label
       
def alert_label_template(width,height):
        new_alert_label = QLabel()
        new_alert_label.setFixedSize(width,height)
        new_alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        new_alert_label.setStyleSheet("background-color: #FFFFFF;" \
                                "font-size: 12px ;" \
                                "font-weight: bold;" \
                                "color: #33324D;"
                                "padding: 0px;"
                                "border: 1px groove #FFFFFF;")
        new_alert_label.hide()
        return new_alert_label

def display_alert(self,alert_label,text,time,connect_func):
        #function to display error if they are and execute an action (ex: object.hide()) when the time is out
        alert_label.setText(text)
        alert_label.show()
        if time != "inf":
            self.timer = QTimer()
            self.timer.timeout.connect(connect_func)
            self.timer.start(time)

def title_template(text,width,height,font_size=45):
        new_title = QLabel()
        new_title.setText(text)
        new_title.setFixedSize(width,height)
        new_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        new_title.setStyleSheet("background-color: #FFFFFF;" \
                                f"font-size: {font_size}px ;" \
                                "font-weight: bold;" \
                                "color: #33324D;"
                                "padding: 2px;"
                                "border: 5px dashed #A799FA;")
        return new_title

def display_requests_template(geometry):
        new_display_requests = QLabel()
        new_display_requests.setGeometry(*geometry)
        new_display_requests.setAlignment(Qt.AlignmentFlag.AlignCenter)
        new_display_requests.setStyleSheet("background-color: #FFFFFF;" \
                                "font-size: 12px ;" \
                                "font-weight: bold;" \
                                "color: #33324D;"
                                "padding: 2px;"
                                "border: 0px solid #FFFFFF;")
        return new_display_requests

