# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uploadCert.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(350, 650)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.calendar_TS = QCalendarWidget(self.centralwidget)
        self.calendar_TS.setObjectName(u"calendar_TS")
        self.calendar_TS.setGeometry(QRect(10, 90, 256, 190))
        self.calendar_ED = QCalendarWidget(self.centralwidget)
        self.calendar_ED.setObjectName(u"calendar_ED")
        self.calendar_ED.setGeometry(QRect(10, 320, 256, 190))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 30, 171, 16))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(90, 550, 91, 24))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 90, 61, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(280, 320, 61, 16))
        self.label_TS = QLabel(self.centralwidget)
        self.label_TS.setObjectName(u"label_TS")
        self.label_TS.setGeometry(QRect(100, 290, 80, 16))
        self.label_ED = QLabel(self.centralwidget)
        self.label_ED.setObjectName(u"label_ED")
        self.label_ED.setGeometry(QRect(100, 520, 80, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 350, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"New Digital Signer Certificate", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Create/Upload", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Timestamp", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ExpiryDate", None))
        self.label_TS.setText(QCoreApplication.translate("MainWindow", u"TS", None))
        self.label_ED.setText(QCoreApplication.translate("MainWindow", u"ED", None))
    # retranslateUi

