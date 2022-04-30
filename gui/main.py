from fileinput import filename
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QFile, QRect
from ui_mainwindow import Ui_MainWindow

from utils import PathManager
from app_corpus.app_loader import AppLoader

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.path_manager = PathManager()
        self.app_loader = AppLoader()

        self.ui.app_list_table.setRowCount(self.app_loader.number_of_apps)
        self.ui.app_list_table.setColumnCount(4)
        fieldnames = ["App_Title", "Developer", "Developer_Privacy_Policy"]
        offset = 0
        for store, app_data_list in self.app_loader.apps.items():
            for row, app_data in enumerate(app_data_list):
                for column, name in enumerate(fieldnames):
                    self.ui.app_list_table.setItem(row, column, QTableWidgetItem(app_data[name]))
                self.ui.app_list_table.setItem(row, len(fieldnames), QTableWidgetItem(store.name))
            offset += len(app_data_list)
            self.ui.dataset_files.addItem(store.name)
        self.ui.ovrseen_directory.setText("OVRSeen Directory: " + str(self.path_manager.ovrseen_path))
    
    def resizeEvent(self, event):
        self.ui.horizontalLayoutWidget.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.ui.app_layout_object.setGeometry(QRect(0, 0, self.width() - 20, self.height() - 20))
        self.ui.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, self.width() - 30, self.height() - 30))
        QMainWindow.resizeEvent(self, event)

    def loadAppCorpusFile(self):
        fileName, filter = QFileDialog.getOpenFileName(self, dir=str(self.path_manager.ovrseen_path))
        filePath = Path(fileName)
        assert filePath.is_file() and filePath.name.endswith(".csv")

        previous_count = self.app_loader.number_of_apps
        new_app_data = self.app_loader.load_app_store(filePath)
        self.ui.app_list_table.setRowCount(self.app_loader.number_of_apps)
        self.ui.app_list_table.setColumnCount(4)
        fieldnames = ["App_Title", "Developer", "Developer_Privacy_Policy"]
        for row, app_data in enumerate(new_app_data):
            for column, name in enumerate(fieldnames):
                self.ui.app_list_table.setItem(row, column, QTableWidgetItem(app_data[name]))
            self.ui.app_list_table.setItem(row, len(fieldnames), QTableWidgetItem(filePath.name))
        
        self.ui.dataset_files.addItem(filePath.name)

    def setOVRSeenDirectory(self):
        self.path_manager.ovrseen_path = QFileDialog.getExistingDirectory(self)
        self.ui.ovrseen_directory.setText("OVRSeen Directory: " + str(self.path_manager.ovrseen_path))

    def closeEvent(self, event: QCloseEvent) -> None:
        print("closed")
        self.app_loader.close()
        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())