from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6 import QtGui

# from Packages.SetupGUI import Ui_Dialog
# from Packages.PlotsAndDF import ExtractData

# from SetupGUI import Ui_Dialog
# from Collector import ExtractData
from Packages.SetupGUI import Ui_Dialog
from Packages.Collector import ExtractData
import sys


class GUI(QWidget):
    tDiagOn = False
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()       
        self.ui.setupUi(self)
        self.tDiagOn = False

        self.ui.transPathButton.clicked.connect(self.selectTransFolder)
        self.ui.tdiagPathButton.clicked.connect(self.selectTDiagFolder)

        self.ui.saveButton.clicked.connect(self.selectSaveFolder)
        self.ui.runButton.clicked.connect(self.runButton)
        self.ui.stopButton.clicked.connect(self.stopButton)

        # self.ui.tdiagButton.clicked.connect(self.tdiagButton)

        self.show()

    
    def selectTransFolder(self):
        self.ui.transPathEdit.setText(QFileDialog.getExistingDirectory()) # opens a folder directory
    def selectSaveFolder(self):
        self.ui.saveEdit.setText(QFileDialog.getExistingDirectory()) # opens a folder directory
    def selectTDiagFolder(self):
        self.ui.tdiagPathEdit.setText(QFileDialog.getExistingDirectory()) # opens a folder directory
    def stopButton(self):
        sys.exit(0)
    def runButton(self):
        ExtractData(self.ui.startingDate.text().strip(), self.ui.startingTime.text().strip(), self.ui.endingDate.text().strip(), self.ui.endingTime.text().strip(), self.ui.transPathEdit.text().strip(), self.ui.tdiagPathEdit.text().strip(), self.ui.saveEdit.text().strip())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = GUI()
    sys.exit(app.exec())

