from fileinput import filename
from pathlib import Path
import sys, io, os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QCheckBox, QPushButton
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QFile, QRect, QEvent

from gui.app_corpus.pripol_graph_loader import PriPolGraphHandler
# from gui.app_corpus.postproc_graph_loader import PostProcGraphHandler

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
        self.tcpip_mode = False

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
        self.ui.app_blacklist.clicked.connect(self.setAppBlacklist)
        self.ui.pushButton.clicked.connect(self.downloadAPKs)
        globals.redirect_print_func = self.redirect_print

        # set up frida buttons
        self.ui.frida_bypass.clicked.connect(self.fridaBypass)
        self.ui.frida_collect.clicked.connect(self.fridaCollect)
        self.ui.frida_collect_uninstall.clicked.connect(self.fridaCollectUninstall)
        self.ui.reinstall_frida_app.clicked.connect(self.fridaReinstallAPK)
        self.ui.connect_oculus_wireless.clicked.connect(self.connectOculus)
        self.ui.frida_instructions.append("""
        In this tab you can collect pcaps using frida to bypass ssl pinnings.
        First you will need to select an app from the left bar to experiment with.
        Then you can use the buttons below to collect pcaps.
        """)
        self.apk_mapping = dict()
        self.setupFridaList() # in case apks are already populated
        self.selectedApk = None

        # set up post-processing buttons
        self.ui.frida_process_pcaps.clicked.connect(self.postProcessing)
        # self.ui.post_processing.clicked.connect(self.postProcessing)
        # self.ui.pp_graphs.clicked.connect(self.ppGraphs)

        # set up privacy policy buttons
        self.ui.set_up_analysis.clicked.connect(self.setUpAnalysis)
        self.ui.analyze_data.clicked.connect(self.analyzeData)
        self.ui.create_graphs.clicked.connect(self.createGraphs)

    def resizeEvent(self, event):
        self.ui.horizontalLayoutWidget.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.ui.app_layout_object.setGeometry(QRect(0, 0, self.width() - 30, self.height() - 30))
        self.ui.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, self.width() - 30, self.height() - 30))
        self.ui.horizontalLayoutWidget_5.setGeometry(QRect(0, 0, self.width() - 30, self.height() - 30)) # frida
        self.ui.horizontalLayoutWidget_3.setGeometry(QRect(0, 0, self.width() - 30, self.height() - 30)) # network to policy consistency
        QMainWindow.resizeEvent(self, event)

    def redirect_print(self, *args, **kwargs):
        tab_name = self.ui.tabWidget.currentWidget().objectName()
        if tab_name == "a_trafficcollection":
            out = io.StringIO()
            print(*args, **kwargs, file=out)
            self.ui.textEdit.append(out.getvalue())
        elif tab_name == "c_privacypolicies":
            out = io.StringIO()
            print(*args, **kwargs, file=out)
            self.ui.privacy_policies_log.append(out.getvalue())
        elif tab_name == "d_frida":
            out = io.StringIO()
            print(*args, **kwargs, file=out)
            self.ui.frida_shell_log.append(out.getvalue())
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

    def setAppBlacklist(self):
        self.path_manager.run_command(utils.Command.APK_BLACKLIST)

    def downloadAPKs(self):
        self.path_manager.run_command(utils.Command.APK_DOWNLOAD)
        # now check apk folder to add to frida apps
        self.setupFridaList()

    def setupFridaList(self):
        apks = list(filter(lambda x: x.endswith("apk"), os.listdir((self.path_manager.APK_PROCESSING / "APKs"))))
        self.apk_list = apks
        for apk in apks:
            if apk in self.apk_mapping:
                continue
            def buttonCallback(apk_name):
                self.redirect_print("apk: ", apk_name, " selected.")
                self.selectedApk = apk_name
                result = self.path_manager.run_command(utils.Command.FRIDA_SELECT_APK, [self.selectedApk])
                if result is None:
                    self.selectedApk = None
                    return
                self.ui.frida_instructions.setText(
                    f"""
You have selected: {self.selectedApk}. You can perform the following actions:
1. Reupload the frida signed apk.
2. Launch the app and begin collecting pcaps (Collect PCAPs)
For launching the app, please perform the following steps. First, toggle the antmonitor switch to on.
Next, open the app in oculus and click through any warnings to get the app to launch. Then, click the "Collect PCAPs button".
This should allow you to start playing the app (without clicking this button you will see a black screen).
Finally, close the app, this will resume the gui for further use.
3. Download PCAPs from the oculus
4. Download PCAPs from the oculus and uninstall the frida signed apk.
                    """
                )
            buttonCallbackWithApk = partial(buttonCallback, apk)
            new_button = QPushButton(apk)
            new_button.clicked.connect(buttonCallbackWithApk)
            self.apk_mapping[apk] = new_button
            self.ui.frida_app_layout.addWidget(new_button)
        
    # FRIDA BUTTONS

    def connectOculus(self):
        if self.selectedApk is None:
            self.redirect_print("Before connecting wirelessly, choose an app to test")
            return
        instructions = self.ui.frida_instructions.toPlainText()
        if "wireless instructions" not in instructions:
            self.ui.frida_instructions.append(
            """
Device has been set up in tcpip mode, you may now unplug the device.
If you attempt to do anything but test an app, you must have the usb device plugged in.
            """)
        self.path_manager.run_command(utils.Command.ADB_CONNECT_TCP_IP)

    def fridaReinstallAPK(self):
        if self.selectedApk is None:
            self.redirect_print("select an apk before trying to reinstall it")
        else:
            self.redirect_print("reinstalling the currently selected apk")
            self.path_manager.run_command(utils.Command.FRIDA_REINSTALL_APK, [self.selectedApk])


    def fridaBypass(self):
        self.redirect_print("bypassing ssl pinnings")
        self.path_manager.run_command(utils.Command.FRIDA_BYPASS, [self.selectedApk])

    def fridaCollect(self):
        self.redirect_print("downloading pcaps (without performing post processing")
        self.path_manager.run_command(utils.Command.FRIDA_COLLECT)

    def fridaCollectUninstall(self):
        self.redirect_print("downloading pcaps and uninstalling apk for selected app")
        self.path_manager.run_command(utils.Command.FRIDA_COLLECT_UNINSTALL)
        # do something with selected bypass app

    # POST PROCESSING BUTTONS

    def postProcessing(self):
        self.redirect_print("running post-processing")
        self.path_manager.run_command(utils.Command.POST_PROCESSING)

    # def ppGraphs(self):
    #     self.redirect_print("creating post-processing graphs")
    #     self.path_manager.run_command(utils.Command.PP_GRAPHS)
    #
    #     PostProcGraphHandler
    #     self.postproc_graph_loader = PostProcGraphHandler(utils.PathManager.POSTPROC_GRAPHS)
    #     # created graphs table
    #     self.ui.postproc_graph_table.setRowCount(4)
    #     self.ui.postproc_graph_table.setColumnCount(2)
    #     fieldnames = ["Graph","Open",]
    #     for row, graph in enumerate(self.postproc_graph_loader.graphs):
    #         self.ui.postproc_graph_table.setItem(row, 0, QTableWidgetItem(graph))
    #         self.ui.postproc_graph_table.setItem(row, 1, QTableWidgetItem())# TODO add open button)) # TODO check

    # PRIVACY POLICY BUTTONS

    def setUpAnalysis(self):
        self.redirect_print("setting up privacy policy analysis")

        # setup privacy policy analysis paths + loaders
        pppath = self.path_manager.ovrseen_path / utils.PathManager.POST_PROCESSING / "PCAPs/all-merged-with-esld-engine-privacy-developer-party.csv"
        self.pp_data_loader = PPDataHandler(pppath)
        # apps data table
        self.path_manager.run_command(utils.Command.SETUP_ANALYSIS, [self.pp_data_loader.packages()])

        self.ui.privacy_policies_app_list.setRowCount(self.pp_data_loader.number_of_apps)
        self.ui.privacy_policies_app_list.setColumnCount(1)
        fieldnames = ["App_Title"]
        for row, app in enumerate(self.pp_data_loader.apps()):
            self.ui.privacy_policies_app_list.setItem(row, 0, QTableWidgetItem(app))

    def analyzeData(self):
        self.redirect_print("conducting privacy policy analysis")
        self.path_manager.run_command(utils.Command.ANALYZE_DATA)

    def createGraphs(self):
        self.redirect_print("creating graphs")
        self.path_manager.run_command(utils.Command.CREATE_GRAPHS)

        self.pripol_graph_loader = PriPolGraphHandler(utils.PathManager.PRIPOL_GRAPHS)
        # created graphs table
        # self.ui.pripol_graph_table.setRowCount(4)
        # self.ui.pripol_graph_table.setColumnCount(2)
        # fieldnames = ["Graph","Open",]
        # for row, graph in enumerate(self.pripol_graph_loader.graphs):
        #     self.ui.pripol_graph_table.setItem(row, 0, QTableWidgetItem(graph))
        #     self.ui.pripol_graph_table.setItem(row, 1, QTableWidgetItem())# TODO add open button)) # TODO check
