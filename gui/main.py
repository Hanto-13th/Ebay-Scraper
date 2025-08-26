import sys
from PyQt6.QtWidgets import QApplication
from . import windows

"""The entrypoint for the GUI part and users"""

def main():

    app = QApplication(sys.argv)

    main_window = windows.MainWindow()
    main_window.show()
   
    app.exec()
        
if __name__ == "__main__":
    main()