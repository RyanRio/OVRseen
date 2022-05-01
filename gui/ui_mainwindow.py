# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: rgb(172, 180, 179)")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 791, 551))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.horizontalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabPosition(QTabWidget.East)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.a_apps = QWidget()
        self.a_apps.setObjectName(u"a_apps")
        self.a_apps.setStyleSheet(u"")
        self.app_layout_object = QFrame(self.a_apps)
        self.app_layout_object.setObjectName(u"app_layout_object")
        self.app_layout_object.setGeometry(QRect(110, 100, 601, 391))
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.app_layout_object.sizePolicy().hasHeightForWidth())
        self.app_layout_object.setSizePolicy(sizePolicy1)
        self.app_layout = QHBoxLayout(self.app_layout_object)
        self.app_layout.setObjectName(u"app_layout")
        self.app_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.app_list_table = QTableWidget(self.app_layout_object)
        if (self.app_list_table.columnCount() < 2):
            self.app_list_table.setColumnCount(2)
        self.app_list_table.setObjectName(u"app_list_table")
        sizePolicy.setHeightForWidth(self.app_list_table.sizePolicy().hasHeightForWidth())
        self.app_list_table.setSizePolicy(sizePolicy)
        self.app_list_table.setRowCount(0)
        self.app_list_table.setColumnCount(2)

        self.app_layout.addWidget(self.app_list_table)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.label = QLabel(self.app_layout_object)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(13)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label)

        self.set_ovrseen_base_path = QPushButton(self.app_layout_object)
        self.set_ovrseen_base_path.setObjectName(u"set_ovrseen_base_path")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.set_ovrseen_base_path.sizePolicy().hasHeightForWidth())
        self.set_ovrseen_base_path.setSizePolicy(sizePolicy3)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.set_ovrseen_base_path)

        self.load_dataset_file = QPushButton(self.app_layout_object)
        self.load_dataset_file.setObjectName(u"load_dataset_file")
        sizePolicy3.setHeightForWidth(self.load_dataset_file.sizePolicy().hasHeightForWidth())
        self.load_dataset_file.setSizePolicy(sizePolicy3)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.load_dataset_file)

        self.label_2 = QLabel(self.app_layout_object)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.label_2)

        self.dataset_files = QListWidget(self.app_layout_object)
        self.dataset_files.setObjectName(u"dataset_files")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.dataset_files.sizePolicy().hasHeightForWidth())
        self.dataset_files.setSizePolicy(sizePolicy4)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.dataset_files)

        self.ovrseen_directory = QLabel(self.app_layout_object)
        self.ovrseen_directory.setObjectName(u"ovrseen_directory")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.ovrseen_directory.sizePolicy().hasHeightForWidth())
        self.ovrseen_directory.setSizePolicy(sizePolicy5)
        self.ovrseen_directory.setMaximumSize(QSize(16777215, 20))
        self.ovrseen_directory.setFont(font)
        self.ovrseen_directory.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.ovrseen_directory)


        self.app_layout.addLayout(self.formLayout)

        self.tabWidget.addTab(self.a_apps, "")
        self.a_trafficcollection = QWidget()
        self.a_trafficcollection.setObjectName(u"a_trafficcollection")
        self.horizontalLayoutWidget_2 = QWidget(self.a_trafficcollection)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(30, 40, 681, 461))
        self.traffic_collection_layout_internal = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.traffic_collection_layout_internal.setObjectName(u"traffic_collection_layout_internal")
        self.traffic_collection_layout_internal.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setVerticalSpacing(6)
        self.clear_antmonitor_data = QPushButton(self.horizontalLayoutWidget_2)
        self.clear_antmonitor_data.setObjectName(u"clear_antmonitor_data")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.clear_antmonitor_data.sizePolicy().hasHeightForWidth())
        self.clear_antmonitor_data.setSizePolicy(sizePolicy6)
        self.clear_antmonitor_data.setMaximumSize(QSize(16777215, 20))

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.clear_antmonitor_data)

        self.frida_libs = QPushButton(self.horizontalLayoutWidget_2)
        self.frida_libs.setObjectName(u"frida_libs")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.frida_libs.sizePolicy().hasHeightForWidth())
        self.frida_libs.setSizePolicy(sizePolicy7)
        self.frida_libs.setMaximumSize(QSize(16777215, 20))

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.frida_libs)

        self.unity_so_files = QPushButton(self.horizontalLayoutWidget_2)
        self.unity_so_files.setObjectName(u"unity_so_files")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.unity_so_files)

        self.connect_oculus = QPushButton(self.horizontalLayoutWidget_2)
        self.connect_oculus.setObjectName(u"connect_oculus")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.connect_oculus)

        self.textEdit_2 = QTextEdit(self.horizontalLayoutWidget_2)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setReadOnly(True)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.textEdit_2)

        self.app_blacklist = QPushButton(self.horizontalLayoutWidget_2)
        self.app_blacklist.setObjectName(u"app_blacklist")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.app_blacklist)

        self.pushButton = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName(u"pushButton")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.pushButton)


        self.traffic_collection_layout_internal.addLayout(self.formLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.textEdit = QTextEdit(self.horizontalLayoutWidget_2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.textEdit)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_3.addWidget(self.pushButton_2)


        self.traffic_collection_layout_internal.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.a_trafficcollection, "")
        self.d_frida = QWidget()
        self.d_frida.setObjectName(u"d_frida")
        self.horizontalLayoutWidget_5 = QWidget(self.d_frida)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(30, 30, 641, 451))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frida_app_layout = QVBoxLayout()
        self.frida_app_layout.setObjectName(u"frida_app_layout")
        self.label_7 = QLabel(self.horizontalLayoutWidget_5)
        self.label_7.setObjectName(u"label_7")

        self.frida_app_layout.addWidget(self.label_7)


        self.horizontalLayout_4.addLayout(self.frida_app_layout)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_9 = QLabel(self.horizontalLayoutWidget_5)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_7.addWidget(self.label_9)

        self.frida_instructions = QTextEdit(self.horizontalLayoutWidget_5)
        self.frida_instructions.setObjectName(u"frida_instructions")

        self.verticalLayout_7.addWidget(self.frida_instructions)

        self.reinstall_frida_app = QPushButton(self.horizontalLayoutWidget_5)
        self.reinstall_frida_app.setObjectName(u"reinstall_frida_app")

        self.verticalLayout_7.addWidget(self.reinstall_frida_app)

        self.frida_bypass = QPushButton(self.horizontalLayoutWidget_5)
        self.frida_bypass.setObjectName(u"frida_bypass")

        self.verticalLayout_7.addWidget(self.frida_bypass)

        self.frida_collect = QPushButton(self.horizontalLayoutWidget_5)
        self.frida_collect.setObjectName(u"frida_collect")

        self.verticalLayout_7.addWidget(self.frida_collect)

        self.frida_collect_uninstall = QPushButton(self.horizontalLayoutWidget_5)
        self.frida_collect_uninstall.setObjectName(u"frida_collect_uninstall")

        self.verticalLayout_7.addWidget(self.frida_collect_uninstall)


        self.horizontalLayout_4.addLayout(self.verticalLayout_7)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_8 = QLabel(self.horizontalLayoutWidget_5)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_2.addWidget(self.label_8)

        self.frida_shell_log = QTextEdit(self.horizontalLayoutWidget_5)
        self.frida_shell_log.setObjectName(u"frida_shell_log")

        self.verticalLayout_2.addWidget(self.frida_shell_log)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.d_frida, "")
        self.b_post_processing = QWidget()
        self.b_post_processing.setObjectName(u"b_post_processing")
        self.horizontalLayoutWidget_4 = QWidget(self.b_post_processing)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(40, 30, 581, 431))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget_4)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.textEdit_3 = QTextEdit(self.horizontalLayoutWidget_4)
        self.textEdit_3.setObjectName(u"textEdit_3")

        self.horizontalLayout_3.addWidget(self.textEdit_3)

        self.tabWidget.addTab(self.b_post_processing, "")
        self.c_privacypolicies = QWidget()
        self.c_privacypolicies.setObjectName(u"c_privacypolicies")
        self.horizontalLayoutWidget_3 = QWidget(self.c_privacypolicies)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(30, 30, 701, 491))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.set_up_analysis = QPushButton(self.horizontalLayoutWidget_3)
        self.set_up_analysis.setObjectName(u"set_up_analysis")

        self.verticalLayout_4.addWidget(self.set_up_analysis)

        self.analyze_data = QPushButton(self.horizontalLayoutWidget_3)
        self.analyze_data.setObjectName(u"analyze_data")

        self.verticalLayout_4.addWidget(self.analyze_data)

        self.create_graphs = QPushButton(self.horizontalLayoutWidget_3)
        self.create_graphs.setObjectName(u"create_graphs")

        self.verticalLayout_4.addWidget(self.create_graphs)

        self.label_4 = QLabel(self.horizontalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_4.addWidget(self.label_4)

        self.privacy_policies_log = QTextEdit(self.horizontalLayoutWidget_3)
        self.privacy_policies_log.setObjectName(u"privacy_policies_log")

        self.verticalLayout_4.addWidget(self.privacy_policies_log)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_5 = QLabel(self.horizontalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_5.addWidget(self.label_5)

        self.privacy_policies_app_list = QTableWidget(self.horizontalLayoutWidget_3)
        self.privacy_policies_app_list.setObjectName(u"privacy_policies_app_list")

        self.verticalLayout_5.addWidget(self.privacy_policies_app_list)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_6 = QLabel(self.horizontalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_6.addWidget(self.label_6)

        self.privacy_policies_graph_list = QListWidget(self.horizontalLayoutWidget_3)
        self.privacy_policies_graph_list.setObjectName(u"privacy_policies_graph_list")

        self.verticalLayout_6.addWidget(self.privacy_policies_graph_list)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.tabWidget.addTab(self.c_privacypolicies, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.load_dataset_file.clicked.connect(MainWindow.loadAppCorpusFile)
        self.set_ovrseen_base_path.clicked.connect(MainWindow.setOVRSeenDirectory)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"App Corpus Configuration", None))
        self.set_ovrseen_base_path.setText(QCoreApplication.translate("MainWindow", u"Choose OVRSeen Directory", None))
        self.load_dataset_file.setText(QCoreApplication.translate("MainWindow", u"Load Dataset File", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Dataset Files:", None))
        self.ovrseen_directory.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.a_apps), QCoreApplication.translate("MainWindow", u"Apps", None))
        self.clear_antmonitor_data.setText(QCoreApplication.translate("MainWindow", u"Clear Antmonitor Data", None))
        self.frida_libs.setText(QCoreApplication.translate("MainWindow", u"Download Frida Libs", None))
#if QT_CONFIG(tooltip)
        self.unity_so_files.setToolTip(QCoreApplication.translate("MainWindow", u"Click this to let the app find your downloaded unity so files, please select the directory of the unity so files zip", None))
#endif // QT_CONFIG(tooltip)
        self.unity_so_files.setText(QCoreApplication.translate("MainWindow", u"Move Unity Folder", None))
        self.connect_oculus.setText(QCoreApplication.translate("MainWindow", u"Connect to Oculus", None))
        self.textEdit_2.setMarkdown(QCoreApplication.translate("MainWindow", u"For additional information follow along with the traffic collection tab on the\n"
"wiki, however this automates many of the tasks required.\n"
"\n"
"", None))
#if QT_CONFIG(tooltip)
        self.app_blacklist.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the list of apps that won't be used for traffic collection", None))
#endif // QT_CONFIG(tooltip)
        self.app_blacklist.setText(QCoreApplication.translate("MainWindow", u"Set App Blacklist", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Download APKs", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Shell Log", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Clear Log", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.a_trafficcollection), QCoreApplication.translate("MainWindow", u"APK Setup", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Apps To Test (Click to begin testing)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Follow The Instructions Below", None))
        self.reinstall_frida_app.setText(QCoreApplication.translate("MainWindow", u"Reupload new Signed APK", None))
        self.frida_bypass.setText(QCoreApplication.translate("MainWindow", u"Collect PCAPs", None))
        self.frida_collect.setText(QCoreApplication.translate("MainWindow", u"Download PCAPs from Device", None))
        self.frida_collect_uninstall.setText(QCoreApplication.translate("MainWindow", u"Download PCAPs and Uninstall", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Shell Log", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.d_frida), QCoreApplication.translate("MainWindow", u"Frida", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.textEdit_3.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Click here to download the required filter lists: <a href=\"https://drive.google.com/uc?id=1rySec21Xx_t_x9T04KCX7W4oGUCtf3tt\"><span style=\" text-decoration: underline; color:#007af4;\">google drive link</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Then click &quot;select filter lists&quot; to set up your filters</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.b_post_processing), QCoreApplication.translate("MainWindow", u"Post Processing", None))
        self.set_up_analysis.setText(QCoreApplication.translate("MainWindow", u"Set Up Analysis", None))
        self.analyze_data.setText(QCoreApplication.translate("MainWindow", u"Analyze App Data", None))
        self.create_graphs.setText(QCoreApplication.translate("MainWindow", u"Generate Graphs", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Shell Log", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Apps", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Graphs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.c_privacypolicies), QCoreApplication.translate("MainWindow", u"Privacy Policies", None))
    # retranslateUi

