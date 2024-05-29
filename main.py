from Packages.GUIController import GUI
from PyQt6.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = GUI()
    sys.exit(app.exec())