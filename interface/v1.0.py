# Form implementation generated from reading ui file 'v1.0.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 576)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_tools = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_tools.setGeometry(QtCore.QRect(-1, -1, 1021, 31))
        self.widget_tools.setObjectName("widget_tools")
        self.openFile_tools = QtWidgets.QPushButton(parent=self.widget_tools)
        self.openFile_tools.setEnabled(True)
        self.openFile_tools.setGeometry(QtCore.QRect(10, 0, 31, 31))
        self.openFile_tools.setAutoFillBackground(True)
        self.openFile_tools.setText("")
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::DocumentOpen")
        self.openFile_tools.setIcon(icon)
        self.openFile_tools.setIconSize(QtCore.QSize(24, 24))
        self.openFile_tools.setAutoDefault(False)
        self.openFile_tools.setDefault(False)
        self.openFile_tools.setFlat(True)
        self.openFile_tools.setObjectName("openFile_tools")
        self.save_tools = QtWidgets.QPushButton(parent=self.widget_tools)
        self.save_tools.setEnabled(True)
        self.save_tools.setGeometry(QtCore.QRect(40, 0, 31, 31))
        self.save_tools.setAutoFillBackground(True)
        self.save_tools.setText("")
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::DocumentSave")
        self.save_tools.setIcon(icon)
        self.save_tools.setIconSize(QtCore.QSize(24, 24))
        self.save_tools.setAutoDefault(False)
        self.save_tools.setDefault(False)
        self.save_tools.setFlat(True)
        self.save_tools.setObjectName("save_tools")
        self.dotPut_tools = QtWidgets.QPushButton(parent=self.widget_tools)
        self.dotPut_tools.setEnabled(True)
        self.dotPut_tools.setGeometry(QtCore.QRect(70, 0, 31, 31))
        self.dotPut_tools.setAutoFillBackground(True)
        self.dotPut_tools.setText("")
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::MailMessageNew")
        self.dotPut_tools.setIcon(icon)
        self.dotPut_tools.setIconSize(QtCore.QSize(24, 24))
        self.dotPut_tools.setAutoDefault(False)
        self.dotPut_tools.setDefault(False)
        self.dotPut_tools.setFlat(True)
        self.dotPut_tools.setObjectName("dotPut_tools")
        self.movePlot_tools = QtWidgets.QPushButton(parent=self.widget_tools)
        self.movePlot_tools.setEnabled(True)
        self.movePlot_tools.setGeometry(QtCore.QRect(100, 0, 31, 31))
        self.movePlot_tools.setAutoFillBackground(True)
        self.movePlot_tools.setText("")
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::DocumentOpenRecent")
        self.movePlot_tools.setIcon(icon)
        self.movePlot_tools.setIconSize(QtCore.QSize(24, 24))
        self.movePlot_tools.setAutoDefault(False)
        self.movePlot_tools.setDefault(False)
        self.movePlot_tools.setFlat(True)
        self.movePlot_tools.setObjectName("movePlot_tools")
        self.areaPlot = QtWidgets.QWidget(parent=self.centralwidget)
        self.areaPlot.setGeometry(QtCore.QRect(-1, 29, 1021, 501))
        self.areaPlot.setObjectName("areaPlot")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setGeometry(QtCore.QRect(301, 125, 134, 72))
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuStyle = QtWidgets.QMenu(parent=self.menuSettings)
        self.menuStyle.setObjectName("menuStyle")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_File = QtGui.QAction(parent=MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionExport = QtGui.QAction(parent=MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionInfo = QtGui.QAction(parent=MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.actionsettings = QtGui.QAction(parent=MainWindow)
        self.actionsettings.setObjectName("actionsettings")
        self.actionProperties = QtGui.QAction(parent=MainWindow)
        self.actionProperties.setObjectName("actionProperties")
        self.actionDefault = QtGui.QAction(parent=MainWindow)
        self.actionDefault.setObjectName("actionDefault")
        self.actionDark = QtGui.QAction(parent=MainWindow)
        self.actionDark.setObjectName("actionDark")
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuHelp.addAction(self.actionInfo)
        self.menuStyle.addAction(self.actionDefault)
        self.menuStyle.addAction(self.actionDark)
        self.menuSettings.addAction(self.menuStyle.menuAction())
        self.menuSettings.addAction(self.actionProperties)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuStyle.setTitle(_translate("MainWindow", "Style"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))
        self.actionExport.setText(_translate("MainWindow", "Save"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
        self.actionsettings.setText(_translate("MainWindow", "settings"))
        self.actionProperties.setText(_translate("MainWindow", "Properties"))
        self.actionDefault.setText(_translate("MainWindow", "Default"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
