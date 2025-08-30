import sys
import threading
from PyQt6.QtWidgets import QApplication
from . import windows
from backend.main import app

"""The users entrypoint for use the app"""

def run_flask():
    """Start Flask in a separate thread."""
    #'use_reloader=False' prevents Flask from starting twice
    app.run(debug=False, use_reloader=False)

def main():

    #start Flask in the background (daemon thread will stop when GUI closes)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    #start the GUI (must run in the main thread)
    gui = QApplication(sys.argv)

    main_window = windows.MainWindow()
    main_window.show()
   
    gui.exec()
        
if __name__ == "__main__":
    main()