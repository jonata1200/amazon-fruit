# main.py

import sys
from PyQt6.QtWidgets import QApplication
from modules.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Passa a instância 'app' para a MainWindow
    window = MainWindow(app) 
    
    window.show()
    sys.exit(app.exec())