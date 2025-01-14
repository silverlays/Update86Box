# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)
import app_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(576, 522)
        icon = QIcon()
        icon.addFile(u":/icons/app.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.installedBuildLabel = QLabel(self.groupBox_2)
        self.installedBuildLabel.setObjectName(u"installedBuildLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.installedBuildLabel.sizePolicy().hasHeightForWidth())
        self.installedBuildLabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.installedBuildLabel.setFont(font)
        self.installedBuildLabel.setStyleSheet(u"color: red")
        self.installedBuildLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.installedBuildLabel)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lastestBuildLabel = QLabel(self.groupBox_3)
        self.lastestBuildLabel.setObjectName(u"lastestBuildLabel")
        sizePolicy.setHeightForWidth(self.lastestBuildLabel.sizePolicy().hasHeightForWidth())
        self.lastestBuildLabel.setSizePolicy(sizePolicy)
        self.lastestBuildLabel.setFont(font)
        self.lastestBuildLabel.setStyleSheet(u"color: green")
        self.lastestBuildLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.lastestBuildLabel)


        self.horizontalLayout.addWidget(self.groupBox_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.newDynarecCheckBox = QCheckBox(self.centralwidget)
        self.newDynarecCheckBox.setObjectName(u"newDynarecCheckBox")
        self.newDynarecCheckBox.setChecked(True)

        self.verticalLayout_4.addWidget(self.newDynarecCheckBox)

        self.updateRomsCheckBox = QCheckBox(self.centralwidget)
        self.updateRomsCheckBox.setObjectName(u"updateRomsCheckBox")

        self.verticalLayout_4.addWidget(self.updateRomsCheckBox)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.changelogPlainText = QPlainTextEdit(self.groupBox)
        self.changelogPlainText.setObjectName(u"changelogPlainText")
        self.changelogPlainText.setReadOnly(True)

        self.verticalLayout.addWidget(self.changelogPlainText)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.updateNowPushButton = QPushButton(self.centralwidget)
        self.updateNowPushButton.setObjectName(u"updateNowPushButton")
        font1 = QFont()
        font1.setPointSize(12)
        self.updateNowPushButton.setFont(font1)
        self.updateNowPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.updateNowPushButton)

        self.notNowPushButton = QPushButton(self.centralwidget)
        self.notNowPushButton.setObjectName(u"notNowPushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.notNowPushButton.sizePolicy().hasHeightForWidth())
        self.notNowPushButton.setSizePolicy(sizePolicy1)
        self.notNowPushButton.setFont(font1)
        self.notNowPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.notNowPushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 576, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.updateNowPushButton.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"86Box Updater", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Installed build", None))
        self.installedBuildLabel.setText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Lastest build", None))
        self.lastestBuildLabel.setText("")
        self.newDynarecCheckBox.setText(QCoreApplication.translate("MainWindow", u"New dynarec", None))
        self.updateRomsCheckBox.setText(QCoreApplication.translate("MainWindow", u"Update roms", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Changelog", None))
        self.changelogPlainText.setPlainText("")
        self.updateNowPushButton.setText(QCoreApplication.translate("MainWindow", u"Update now...", None))
        self.notNowPushButton.setText(QCoreApplication.translate("MainWindow", u"Not now", None))
    # retranslateUi

