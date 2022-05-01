from fileinput import filename
from pathlib import Path
import sys, io
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QCheckBox
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QFile, QRect, QEvent

from gui.app_corpus.graph_loader import GraphHandler

from .ui_mainwindow import Ui_MainWindow
from . import globals, utils
from gui.app_corpus.app_loader import AppLoader
from gui.app_corpus.postprocessed_data_loader import PPDataHandler
from functools import partial

class MainWindow(QMainWindow):

    def __init__(self):
        global redirect_print_func
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.path_manager = utils.PathManager()
        self.app_loader = AppLoader()
        self.redirect_print_func = None

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

        # set up traffic collection slots
        self.ui.clear_antmonitor_data.clicked.connect(self.clearAntmonitorData)
        self.ui.frida_libs.clicked.connect(self.downloadFridaLibs)
        self.ui.unity_so_files.clicked.connect(self.moveUnityFolder)
        self.ui.connect_oculus.clicked.connect(self.connectOculus)
        self.ui.app_blacklist.clicked.connect(self.setAppBlacklist)
        self.ui.pushButton.clicked.connect(self.downloadAPKs)
        globals.redirect_print_func = self.redirect_print

        # set up privacy policy buttons
        self.ui.set_up_analysis.clicked.connect(self.setUpAnalysis)
        self.ui.load_collected.clicked.connect(self.loadCollected)
        self.ui.analyze_data.clicked.connect(self.analyzeData)
        self.ui.create_graphs.clicked.connect(self.createGraphs)

        # setup privacy policy analysis paths + loaders
        pppath = self.path_manager.ovrseen_path / utils.PathManager.POST_PROCESSING / "all-merged-with-esld-engine-privacy-developer-party.csv"
        self.pp_data_loader = PPDataHandler(pppath)
        # apps data table
        self.ui.app_data_table.setRowCount(self.pp_data_loader.number_of_apps)
        self.ui.app_data_table.setColumnCount(2)
        fieldnames = ["Selected","App_Title"]
        for row, app in enumerate(self.pp_data_loader.apps):
            self.ui.app_data_table.setItem(row, 0, QTableWidgetItem(QCheckBox())) # TODO check
            self.ui.app_data_table.setItem(row, 1, QTableWidgetItem(app))

    def resizeEvent(self, event):
        self.ui.horizontalLayoutWidget.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.ui.app_layout_object.setGeometry(QRect(0, 0, self.width() - 20, self.height() - 20))
        self.ui.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, self.width() - 30, self.height() - 30))
        QMainWindow.resizeEvent(self, event)

    def redirect_print(self, *args, **kwargs):
        tab_name = self.ui.tabWidget.currentWidget().objectName()
        if tab_name == "a_trafficcollection":
            out = io.StringIO()
            print(*args, **kwargs, file=out)
            self.ui.textEdit.append(out.getvalue())
        else:
            print(*args, **kwargs)

    # app corpus signals

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
        print(self.path_manager.ovrseen_path)
        self.ui.ovrseen_directory.setText("OVRSeen Directory: " + str(self.path_manager.ovrseen_path))

    def closeEvent(self, event: QCloseEvent) -> None:
        print("closed")
        self.app_loader.close()
        return super().closeEvent(event)

    # TRAFFIC COLLECTION SLOTS

    def clearAntmonitorData(self):
        self.redirect_print("clearing antmonitor data")
        stdout, stderr = self.path_manager.run_command(utils.Command.CLEAR_ANTMONITOR_DATA)

    def downloadFridaLibs(self):
        self.redirect_print("installing frida libs")
        self.path_manager.run_command(utils.Command.GET_FRIDA_LIBS)

    def moveUnityFolder(self):
        unity_folder = QFileDialog.getExistingDirectory(self)
        if len(unity_folder) > 0:
            self.path_manager.run_command(utils.Command.MOVE_UNITY_SOS, [unity_folder])




    def connectOculus(self):
        self.path_manager.run_command(utils.Command.ADB_CONNECT_TCP_IP)

    def setAppBlacklist(self):
        self.path_manager.run_command(utils.Command.APK_BLACKLIST)

    def downloadAPKs(self):
        self.path_manager.run_command(utils.Command.APK_DOWNLOAD)

    # PRIVACY POLICY BUTTONS

    def setUpAnalysis(self):
        self.redirect_print("setting up privacy policy analysis")
        self.path_manager.run_command(utils.Command.SETUP_ANALYSIS)

    def loadCollected(self):
        self.redirect_print("loading collected application traffic data")
        self.path_manager.run_command(utils.Command.LOAD_COLLECTED)

    def analyzeData(self):
        self.redirect_print("conducting privacy policy analysis")
        self.path_manager.run_command(utils.Command.ANALYZE_DATA)

    def createGraphs(self):
        self.redirect_print("creating graphs")
        self.path_manager.run_command(utils.Command.CREATE_GRAPHS)

        self.graph_loader = GraphHandler(utils.PathManager.GRAPHS)
        # created graphs table
        self.ui.graph_table.setRowCount(4)
        self.ui.graph_table.setColumnCount(2)
        fieldnames = ["Graph","Open",]
        for row, graph in enumerate(self.graph_loader.graphs):
            self.ui.graph_table.setItem(row, 0, QTableWidgetItem(graph))
            self.ui.graph_table.setItem(row, 1, QTableWidgetItem())# TODO add open button)) # TODO check