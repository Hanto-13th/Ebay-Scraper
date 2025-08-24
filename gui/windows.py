from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from . import templates
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        templates.window_settings(self,"Ebay Scrapper",(420,80,650,650),(650,650))

        widget = QWidget()
        self.setCentralWidget(widget)

        self.button_creation = templates.button_template("Requests Creation",220,40,self.to_creation_window)
        self.button_read = templates.button_template("Read The Requests",220,40,self.to_read_window)
        self.button_deletion = templates.button_template("Requests Deletion",220,40,self.to_deletion_window)
        self.button_all_deletion = templates.button_template("Delete All Requests",220,40,self.to_all_deletion_window)
        self.button_send_data = templates.button_template("Send The EBAY Data to Discord",220,40,self.to_send_data_window)

        layout = QVBoxLayout()
        layout.setSpacing(75)

        layout.addStretch()
        layout.addWidget(self.button_creation, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_read, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_deletion, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_all_deletion, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_send_data, alignment=Qt.AlignmentFlag.AlignCenter)
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
        

        templates.window_settings(self,"Ebay Scrapper",(420,80,650,650),(650,650))

        widget = QWidget()
        self.setCentralWidget(widget)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignHCenter)  
        form.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)  
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(50)  
        form.setContentsMargins(20, 20, 20, 20)

        self.product_line = templates.line_template(220,20)
        form.addRow("Enter the product name :", self.product_line)
        self.price_line = templates.line_template(220,20)
        form.addRow("Enter the price to reach :", self.price_line)
        self.option_line = templates.line_template(20,20)
        form.addRow("Choose your options for this request (SELL: 0 or BUY: 1) :", self.option_line)

        self.button_back_window = templates.back_button_template("Back",widget,(10,20,80, 25),self.back_window)
        self.button_request_creation = templates.button_template("Create a Request",220,40,self.create_a_request)
        self.alert_label = templates.alert_label_template(widget,(0,0,200,40))


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
        data = {}

        if len(product_name) == 0:
            templates.display_alert(self,self.alert_label,"Error: set a valid product name !",1500,self.alert_label.hide)
        else:
            data["product_name"] = product_name
        try:
            price_to_reach = float(price_to_reach)
        except ValueError:
            templates.display_alert(self,self.alert_label,"Error: the value is not allowed, Only use integers or floating point numbers !",1500,self.alert_label.hide)
        else:
            data["price"] = float(price_to_reach)
        if option_buy_or_sell not in ("0", "1"):
            templates.display_alert(self,self.alert_label,"Error: the value is not allowed, Only use '0' for SELL option or '1' for BUY option !",1500,self.alert_label.hide)
        else:
            data["option"] = int(option_buy_or_sell)
        if len(data) == 3:
            self.alert_label.hide()
            try:
                response = requests.post("http://127.0.0.1:5000/create_requests_into_db",json=data,timeout=5)
            except requests.exceptions.ConnectionError:
                templates.display_alert(self,self.alert_label,"Impossible to contact the server, verify the Flask connection",1500,self.alert_label.hide)
            except requests.exceptions.ConnectTimeout:
                templates.display_alert(self,self.alert_label,"The Flask server is taking too long to respond",1500,self.alert_label.hide)
            else:
                message = response.json()
                if response.status_code != 200:
                    templates.display_alert(self,self.alert_label,f"The Requests Creation Has Failed ! : {response.status_code} error",1500,self.alert_label.hide)
                elif message["success"] == False:
                    templates.display_alert(self,self.alert_label,f"The Requests Creation Has Failed ! : {message["message"]}",1500,self.alert_label.hide)
                else:
                    templates.display_alert(self,self.alert_label,"Request Created !",500,self.alert_label.hide)

                
    def back_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class Read_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        

        templates.window_settings(self,"Ebay Scrapper",(420,80,650,650),(650,650))

        widget = QWidget()
        self.setCentralWidget(widget)

        self.button_back_window = templates.back_button_template("Back",widget,(10,20,80, 25),self.back_window)
        self.display_requests = QLabel(widget)
        self.display_requests.setGeometry(100,50,500,500)

        try:
            response = requests.get("http://127.0.0.1:5000/read_requests_into_db_table",timeout=5)
        except requests.exceptions.ConnectionError:
            templates.display_alert(self,self.display_requests,"Impossible to contact the server, verify the Flask connection","inf",None)
        except requests.exceptions.ConnectTimeout:
            templates.display_alert(self,self.display_requests,"The Flask server is taking too long to respond","inf",None)
        else:
            message = response.json()
            if response.status_code != 200:
                templates.display_alert(self,self.display_requests,f"Impossible To Read The Data ! : {response.status_code} error","inf",None)
            elif message["success"] == False:
                templates.display_alert(self,self.display_requests,f"The Requests Creation Has Failed ! : {message["message"]}","inf",None)
            else:
                templates.display_alert(self,self.display_requests,message["results"],"inf",None)



    def back_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class Deletion_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        templates.window_settings(self,"Ebay Scrapper",(420,80,650,650),(650,650))

        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout()
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignHCenter)  
        form.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)  
        form.setHorizontalSpacing(0)
        form.setVerticalSpacing(0)  
        form.setContentsMargins(20, 0, 20, 5)
     
        self.button_back_window = templates.back_button_template("Back",widget,(10,20,80, 25),self.back_window)
        self.button_deletion = templates.button_template("Delete the request",120,25,self.delete_the_request)
        self.display_requests = QLabel(widget)
        self.display_requests.setGeometry(100,50,500,500)
        self.delete_line = templates.line_template(50,20)
        form.addRow("Choose the Request ID to delete:", self.delete_line)
        self.alert_label = templates.alert_label_template(widget,(0,0,200,40))

        main_layout.addStretch()
        main_layout.addWidget(self.display_requests, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(form)
        main_layout.addWidget(self.button_deletion, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.alert_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(15)
        main_layout.addStretch()

        widget.setLayout(main_layout)


        try:
            response = requests.get("http://127.0.0.1:5000/read_requests_into_db_table",timeout=5)
        except requests.exceptions.ConnectionError:
            templates.display_alert(self,self.display_requests,"Impossible to contact the server, verify the Flask connection","inf",None)
        except requests.exceptions.ConnectTimeout:
            templates.display_alert(self,self.display_requests,"The Flask server is taking too long to respond","inf",None)
        else:
            message = response.json()
            if response.status_code != 200:
                templates.display_alert(self,self.display_requests,f"Impossible To Read The Data ! : {response.status_code} error","inf",None)
            elif message["success"] == False:
                templates.display_alert(self,self.display_requests,f"The Requests Creation Has Failed ! : {message["message"]}","inf",None)
            else:
                templates.display_alert(self,self.display_requests,message["results"],"inf",None)

    
    def delete_the_request(self):
        id_to_delete = self.delete_line.text()
        data = {}

        if len(id_to_delete) == 0:
            templates.display_alert(self,self.alert_label,"Error: the value is not allowed, Only use valid ID number !",1500,self.alert_label.hide)
        else:
            try:
                id_to_delete = int(id_to_delete)
            except ValueError:
                templates.display_alert(self,self.alert_label,"Error: the value is not allowed, Only use valid ID number !",1500,self.alert_label.hide)
            else:
                data["id"] = int(id_to_delete)
                self.alert_label.hide()
                try:
                    response = requests.post("http://127.0.0.1:5000/delete_requests_into_db_table",json=data,timeout=5)
                except requests.exceptions.ConnectionError:
                    templates.display_alert(self,self.alert_label,"Impossible to contact the server, verify the Flask connection",1500,self.alert_label.hide)
                except requests.exceptions.ConnectTimeout:
                    templates.display_alert(self,self.alert_label,"The Flask server is taking too long to respond",1500,self.alert_label.hide)
                else:
                    message = response.json()
                    if response.status_code != 200:
                        templates.display_alert(self,self.alert_label,f"The Requests Deletion Has Failed ! : {response.status_code} error",1500,self.alert_label.hide)
                    elif message["success"] == False:
                        templates.display_alert(self,self.alert_label,f"The Requests Deletion Has Failed ! : {message["message"]}",1500,self.alert_label.hide)
                    else:
                        templates.display_alert(self,self.alert_label,"Request Deleted !",500,self.alert_label.hide)
                        try:
                            response = requests.get("http://127.0.0.1:5000/read_requests_into_db_table",timeout=5)
                        except requests.exceptions.ConnectionError:
                            templates.display_alert(self,self.display_requests,"Impossible to contact the server, verify the Flask connection","inf",None)
                        except requests.exceptions.ConnectTimeout:
                            templates.display_alert(self,self.display_requests,"The Flask server is taking too long to respond","inf",None)
                        else:
                            message = response.json()
                            if response.status_code != 200:
                                templates.display_alert(self,self.display_requests,f"Impossible To Read The Data ! : {response.status_code} error","inf",None)
                            elif message["success"] == False:
                                templates.display_alert(self,self.display_requests,f"The Requests Creation Has Failed ! : {message["message"]}","inf",None)
                            else:
                                templates.display_alert(self,self.display_requests,message["results"],"inf",None)

                            
    def back_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class All_Deletion_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        templates.window_settings(self,"Ebay Scrapper",(535,275,400,150),(400,150))

        widget = QWidget()
        self.setCentralWidget(widget)

        self.alert_label = QLabel(widget)
        self.alert_label.setGeometry(70,0,380,85)
        self.alert_label.setText("Are you sure you want to delete all the requests?")

        self.button_yes = templates.back_button_template("Yes",widget,(110,85,50, 30),self.all_deletion)
        self.button_no = templates.back_button_template("No",widget,(240,85,50, 30),self.back_window)




    def back_window(self):
        self.close()
    
    def all_deletion(self):
        try:
            response = requests.post("http://127.0.0.1:5000/delete_all_requests_into_db_table",timeout=5)
        except requests.exceptions.ConnectionError:
            templates.display_alert(self,self.alert_label,"Impossible to contact the server, verify the Flask connection","inf",None)

        except requests.exceptions.ConnectTimeout:
            templates.display_alert(self,self.alert_label,"The Flask server is taking too long to respond","inf",None)
        else:
            message = response.json()
            if response.status_code != 200:
                templates.display_alert(self,self.alert_label,f"The Requests Deletion Has Failed ! : {response.status_code} error","inf",None)

            elif message["success"] == False:
                templates.display_alert(self,self.alert_label,f"The Requests Deletion Has Failed ! : {message["message"]}","inf",None)
            else:
                templates.display_alert(self,self.alert_label,"All Requests Has Been Deleted !",1500,self.close)


class Send_Data_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        

        templates.window_settings(self,"Ebay Scrapper",(535,275,400,150),(400,150))


        widget = QWidget()
        self.setCentralWidget(widget)

        self.alert_label = QLabel(widget)
        self.alert_label.setGeometry(70,0,380,85)
        self.alert_label.setText("Do you want to recieve the data on your Discord ?")

        self.button_yes = templates.back_button_template("Yes",widget,(110,85,50, 30),self.send_data)
        self.button_no = templates.back_button_template("No",widget,(240,85,50, 30),self.back_window)

    def back_window(self):
        self.close()
    
    def send_data(self):

        try:
            response = requests.post("http://127.0.0.1:5000/run_full_ebay_process",timeout=5)
        except requests.exceptions.ConnectionError:
            templates.display_alert(self,self.alert_label,"Impossible to contact the server, verify the Flask connection","inf",None)

        except requests.exceptions.ConnectTimeout:
            templates.display_alert(self,self.alert_label,"The Flask server is taking too long to respond","inf",None)
        else:
            message = response.json()
            if response.status_code != 200:
                templates.display_alert(self,self.alert_label,f"Sending Data Failed : {response.status_code} error","inf",None)
            elif "success" in message and message["success"] == False:
                templates.display_alert(self,self.alert_label,f"Sending Data Failed : {message["message"]}","inf",None)
            elif "error" in message:
                templates.display_alert(self,self.alert_label,f"Sending Data Failed : {message["error_description"]}","inf",None)
            elif "errors" in message:
                errors_details = message["errors"][0]
                templates.display_alert(self,self.alert_label,f"Sending Data Failed : {errors_details["longMessage"]}","inf",None)
            else:
                templates.display_alert(self,self.alert_label,f"The Data Has Been Send with {message["untreated_data"]} Untreated Data !",1500,self.close)


