from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QTimer
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Ebay Scrapper")
        self.setGeometry(420,80,650,650)
        self.setFixedSize(650,650)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)
        layout.setSpacing(75)

        layout.addStretch()
        

        button_creation = QPushButton("Requests Creation")
        button_creation.setFixedSize(220, 40)
        button_creation.setFlat(True)
        button_creation.clicked.connect(self.to_creation_window)
        layout.addWidget(button_creation, alignment=Qt.AlignmentFlag.AlignCenter)

        button_read = QPushButton("Read The Requests")
        button_read.setFixedSize(220, 40)
        button_read.setFlat(True)
        button_read.clicked.connect(self.to_read_window)
        layout.addWidget(button_read, alignment=Qt.AlignmentFlag.AlignCenter)

        button_deletion = QPushButton("Requests Deletion")
        button_deletion.setFixedSize(220, 40)
        button_deletion.setFlat(True)
        button_deletion.clicked.connect(self.to_deletion_window)
        layout.addWidget(button_deletion, alignment=Qt.AlignmentFlag.AlignCenter)

        button_all_deletion = QPushButton("Delete All Requests")
        button_all_deletion.setFixedSize(220, 40)
        button_all_deletion.setFlat(True)
        button_all_deletion.clicked.connect(self.to_all_deletion_window)
        layout.addWidget(button_all_deletion, alignment=Qt.AlignmentFlag.AlignCenter)

        button_send_data = QPushButton("Send The EBAY Data to Discord")
        button_send_data.setFixedSize(220, 40)
        button_send_data.setFlat(True)
        button_send_data.clicked.connect(self.to_send_data_window)
        layout.addWidget(button_send_data, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        widget.setLayout(layout)


    def to_creation_window(self):
        self.creation_window = Creation_Window()
        self.creation_window.show()
        self.close()
    
    def to_read_window(self):
        self.read_window = Read_Window()
        self.read_window.show()
        self.close()
    
    def to_deletion_window(self):
        self.deletion_window = Deletion_Window()
        self.deletion_window.show()
        self.close()
    
    def to_all_deletion_window(self):
        self.all_deletion_window = All_Deletion_Window()
        self.all_deletion_window.show()

    def to_send_data_window(self):
        self.send_data_window = Send_Data_Window()
        self.send_data_window.show()

class Creation_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Ebay Scrapper")
        self.setGeometry(420,80,650,650)
        self.setFixedSize(650,650)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        widget = QWidget()
        self.setCentralWidget(widget)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignHCenter)  
        form.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)  
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(50)  
        form.setContentsMargins(20, 20, 20, 20)


        self.product_line = QLineEdit()
        self.product_line.setFixedSize(220,20)
        form.addRow("Enter the product name :", self.product_line)


        self.price_line = QLineEdit()
        self.price_line.setFixedSize(220,20)
        form.addRow("Enter the price to reach :", self.price_line)

        self.option_line = QLineEdit()
        self.option_line.setFixedSize(20,20)
        form.addRow("Choose your options for this request (SELL: 0 or BUY: 1) :", self.option_line)


        self.button_back_window = QPushButton("Back",widget)
        self.button_back_window.setGeometry(10,20,80, 25)
        self.button_back_window.setFlat(True)
        self.button_back_window.clicked.connect(self.back_window)

        self.button_request_creation = QPushButton("Create a Request")
        self.button_request_creation.setFixedSize(220, 40)
        self.button_request_creation.setFlat(True)
        self.button_request_creation.clicked.connect(self.create_a_request)

        self.alert_label = QLabel(widget)
        self.alert_label.setGeometry(0,0,200,40)
        self.alert_label.hide()


        main_layout = QVBoxLayout()

        main_layout.addStretch()

        main_layout.addLayout(form)
        main_layout.addWidget(self.button_request_creation, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.alert_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.setSpacing(20)

        main_layout.addStretch()

        widget.setLayout(main_layout)


    def create_a_request(self):
        product_name = (self.product_line.text()).lower()
        price_to_reach = self.price_line.text()
        option_buy_or_sell = self.option_line.text()
        json = []

        if len(product_name) == 0:
            self.alert_label.setText("Error: set a valid product name !")
            self.alert_label.show()
        else:
            json.append(product_name)
        try:
            price_to_reach = float(price_to_reach)
        except ValueError:
            self.alert_label.setText("Error: the value is not allowed, Only use integers or floating point numbers !")
            self.alert_label.show()
        else:
            json.append(float(price_to_reach))
        if option_buy_or_sell not in ("0", "1"):
            self.alert_label.setText("Error: the value is not allowed, Only use '0' for SELL option or '1' for BUY option !")
            self.alert_label.show()
        else:
            json.append(int(option_buy_or_sell))
        if len(json) == 3:
            self.alert_label.hide()
            response = requests.post("http://127.0.0.1:5000/create_requests_into_db",json=json)
            if response.status_code != 200:
                self.alert_label.setText(f"The Requests Creation Has Failed ! : {response.status_code} error")
                self.alert_label.show()
            else:
                self.alert_label.setText("Request Created !")
                self.alert_label.show()
                self.timer = QTimer()
                self.timer.timeout.connect(self.alert_label.hide)
                self.timer.start(500)
                


    
    def back_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class Read_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Ebay Scrapper")
        self.setGeometry(420,80,650,650)
        self.setFixedSize(650,650)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        widget = QWidget()
        self.setCentralWidget(widget)

        self.button_back_window = QPushButton("Back",widget)
        self.button_back_window.setGeometry(10,20,80, 25)
        self.button_back_window.setFlat(True)
        self.button_back_window.clicked.connect(self.back_window)

        self.display_requests = QLabel(widget)
        self.display_requests.setGeometry(100,50,500,500)


        response = requests.get("http://127.0.0.1:5000/read_requests_into_db_table")
        if response.status_code != 200:
            self.display_requests.setText(f"Impossible To Read The Data ! : {response.status_code} error")
        else:
            self.display_requests.setStyleSheet("border :3px solid blue")
            self.display_requests.setText(response.text)

    def back_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class Deletion_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Ebay Scrapper")
        self.setGeometry(420,80,650,650)
        self.setFixedSize(650,650)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)
        layout.setSpacing(0)

        layout.addStretch()
        


        button = QPushButton("Create a Request")

        
        button.setFixedSize(220, 40)
        button.setFlat(True)
        button.clicked.connect(self.the_button_was_clicked)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        widget.setLayout(layout)


    def the_button_was_clicked(self):
        print("Clicked!")

class All_Deletion_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Ebay Scrapper")
        self.setGeometry(535,275,400,150)
        self.setFixedSize(400,150)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        widget = QWidget()
        self.setCentralWidget(widget)

        self.alert_label = QLabel(widget)
        self.alert_label.setGeometry(70,0,300,85)
        self.alert_label.setText("Are you sure you want to delete all the requests?")
        #self.alert_label.setStyleSheet("border :3px solid blue")

        self.button_back_window = QPushButton("Yes",widget)
        self.button_back_window.setGeometry(110,85,50, 30)
        self.button_back_window.setFlat(True)
        self.button_back_window.clicked.connect(self.all_deletion)


        self.button_back_window = QPushButton("No",widget)
        self.button_back_window.setGeometry(240,85,50, 30)
        self.button_back_window.setFlat(True)
        self.button_back_window.clicked.connect(self.back_window)



    def back_window(self):
        self.close()
    
    def all_deletion(self):

        response = requests.post("http://127.0.0.1:5000/delete_all_requests_into_db_table")
        if response.status_code != 200:
            self.alert_label.setText(f"The Requests Deletion Has Failed ! : {response.status_code} error")
        else:
            self.alert_label.setText("All Requests Has Been Deleted !")
            self.timer = QTimer()
            self.timer.timeout.connect(self.close)
            self.timer.start(1500)


class Send_Data_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Ebay Scrapper")
        self.setGeometry(535,275,400,150)
        self.setFixedSize(400,150)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        widget = QWidget()
        self.setCentralWidget(widget)

        self.alert_label = QLabel(widget)
        self.alert_label.setGeometry(70,0,300,85)
        self.alert_label.setText("Do you want to recieve the data on your Discord ?")
        #self.alert_label.setStyleSheet("border :3px solid blue")

        self.button_back_window = QPushButton("Yes",widget)
        self.button_back_window.setGeometry(110,85,50, 30)
        self.button_back_window.setFlat(True)
        self.button_back_window.clicked.connect(self.send_data)


        self.button_back_window = QPushButton("No",widget)
        self.button_back_window.setGeometry(240,85,50, 30)
        self.button_back_window.setFlat(True)
        self.button_back_window.clicked.connect(self.back_window)



    def back_window(self):
        self.close()
    
    def send_data(self):

        response = requests.post("http://127.0.0.1:5000/run_full_ebay_process")
        if response.status_code != 200:
            self.alert_label.setText(f"Sending Data Failed : {response.status_code} error")
        else:
            self.alert_label.setText("The Data Has Been Send !")
            self.timer = QTimer()
            self.timer.timeout.connect(self.close)
            self.timer.start(1500)

