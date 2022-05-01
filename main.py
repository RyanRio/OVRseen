from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QFile, QRect, QEvent

import sys

from gui import gui

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = gui.MainWindow()
    window.show()

    sys.exit(app.exec_())