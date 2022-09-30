# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'detailCert.ui'
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
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(750, 350)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_issuer = QLabel(self.centralwidget)
        self.label_issuer.setObjectName(u"label_issuer")
        self.label_issuer.setGeometry(QRect(30, 160, 600, 16))
        self.label_version = QLabel(self.centralwidget)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setGeometry(QRect(30, 200, 200, 16))
        self.label_sha = QLabel(self.centralwidget)
        self.label_sha.setObjectName(u"label_sha")
        self.label_sha.setGeometry(QRect(30, 240, 500, 16))
        self.label_kid = QLabel(self.centralwidget)
        self.label_kid.setObjectName(u"label_kid")
        self.label_kid.setGeometry(QRect(250, 50, 250, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 750, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_issuer.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_sha.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_kid.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

