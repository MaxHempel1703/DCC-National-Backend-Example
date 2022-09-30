# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rl.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(950, 650)
        self.actionTl = QAction(MainWindow)
        self.actionTl.setObjectName(u"actionTl")
        self.actionCert = QAction(MainWindow)
        self.actionCert.setObjectName(u"actionCert")
        self.actionRule = QAction(MainWindow)
        self.actionRule.setObjectName(u"actionRule")
        self.actionRl = QAction(MainWindow)
        self.actionRl.setObjectName(u"actionRl")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.table1 = QTableWidget(self.centralwidget)
        if (self.table1.columnCount() < 4):
            self.table1.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table1.setObjectName(u"table1")
        self.table1.setGeometry(QRect(0, 0, 925, 600))
        self.table1.setMinimumSize(QSize(640, 0))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(580, 60, 100, 20))
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(720, 60, 100, 25))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(610, 40, 49, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 950, 22))
        self.menuCerts = QMenu(self.menubar)
        self.menuCerts.setObjectName(u"menuCerts")
        self.menuCerts.setGeometry(QRect(267, 126, 160, 126))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuCerts.menuAction())
        self.menuCerts.addAction(self.actionTl)
        self.menuCerts.addAction(self.actionCert)
        self.menuCerts.addAction(self.actionRule)
        self.menuCerts.addAction(self.actionRl)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionTl.setText(QCoreApplication.translate("MainWindow", u"Trustlist", None))
        self.actionCert.setText(QCoreApplication.translate("MainWindow", u"Certificates", None))
        self.actionRule.setText(QCoreApplication.translate("MainWindow", u"Rules", None))
        self.actionRl.setText(QCoreApplication.translate("MainWindow", u"Revocation", None))
        ___qtablewidgetitem = self.table1.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Bid", None));
        ___qtablewidgetitem1 = self.table1.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Country", None));
        ___qtablewidgetitem2 = self.table1.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Timestamp", None));
        ___qtablewidgetitem3 = self.table1.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Deleted?", None));
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"-", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"False", None))

        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Only Country ?", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Deleted", None))
        self.menuCerts.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi

