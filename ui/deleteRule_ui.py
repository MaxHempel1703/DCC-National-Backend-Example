# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'deleteRule.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(550, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_id = QLabel(self.centralwidget)
        self.label_id.setObjectName(u"label_id")
        self.label_id.setGeometry(QRect(40, 30, 200, 16))
        self.label_type = QLabel(self.centralwidget)
        self.label_type.setObjectName(u"label_type")
        self.label_type.setGeometry(QRect(310, 30, 200, 16))
        self.label_version = QLabel(self.centralwidget)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setGeometry(QRect(130, 150, 300, 16))
        self.label_desc = QLabel(self.centralwidget)
        self.label_desc.setObjectName(u"label_desc")
        self.label_desc.setGeometry(QRect(105, 85, 350, 16))
        self.button1 = QPushButton(self.centralwidget)
        self.button1.setObjectName(u"button1")
        self.button1.setGeometry(QRect(225, 220, 100, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 550, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_id.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_type.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_desc.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.button1.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
    # retranslateUi

