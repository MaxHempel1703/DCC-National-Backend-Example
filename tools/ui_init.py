import ui.tl_ui, ui.cert_ui, ui.rule_ui, ui.rl_ui, ui.detailCert_ui, ui.uploadCert_ui, ui.deleteCert_ui, ui.deleteRule_ui
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidgetItem, QStackedWidget
from PySide6.QtGui import QColor, QAction, Qt
from PySide6.QtCore import QDate
from tools.dcc_utility import compare_dateTime, decode_rawData, decode_cms, download_countrylist
from tools.dcc_utility import create_certificate, delete_certificate, open_validationRules, update_validationRules 
from tools.tl_utility import select_table_tl, get_rawData, update_table
from tools.rl_utility import select_table_rl
from tools.config import config
from cryptography.exceptions import UnsupportedAlgorithm

class Tl_Ui(QMainWindow, ui.tl_ui.Ui_MainWindow):
    def change_mainWindow(self, q):
        widget.setCurrentIndex((1) if q == self.actionCert else (2) if q == self.actionRule else (3) if q == self.actionRl else (0))

    def fill_table(self):
        type = str(self.combo1.currentText())
        country = str(self.combo2.currentText())
        table = self.table1
        table.setRowCount(0)
        if type == "-":
            type = None
        elif type == "AUTH":
            type = "AUTHENTICATION"
        if country == "-":
            country = None
        rows = select_table_tl(type, country)
        table.setRowCount(len(rows))
        row = 0
        for cert in rows:
            button = QPushButton(table)
            button.setText("Details")
            button.clicked.connect(self.detail_window)
            table.setCellWidget(row, 0, button)
            table.setItem(row, 1, QTableWidgetItem(cert[0]))
            table.setItem(row, 2, QTableWidgetItem(cert[1]))
            certificateType = cert[2]
            if certificateType == "AUTHENTICATION":
                certificateType = "AUTH"
            table.setItem(row, 3, QTableWidgetItem(certificateType))
            table.setItem(row, 4, QTableWidgetItem(cert[3]))
            expiryDate = str(decode_rawData(cert[6]).not_valid_after)
            table.setItem(row, 5, QTableWidgetItem(expiryDate))
            for x in range(5):
                cell = table.item(row, x+1)
                cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
            row += 1
        table.sortItems(5, order=Qt.AscendingOrder)
        row = 0
        for cert in rows:
            try: 
                model = table.model()
                expiryDate = model.data(model.index(row, 5))
                diff = compare_dateTime(expiryDate.split(" ")[0])
                table.item(row, 5).setBackground(
                    QColor(255,0,0) if diff < 0 
                    else QColor(255,255,0) if diff < 30 
                    else QColor(0,255,0))
                row += 1
            except AttributeError:
                self.fill_table()

    def detail_window(self):
        table = self.table1
        win = self.detail_win
        win.setWindowModality(Qt.ApplicationModal)
        btn = QApplication.focusWidget()
        pos = table.indexAt(btn.pos())
        model = table.model()
        kid = model.data(model.index(pos.row(), 1))
        win.label_kid.setText(str(kid))
        win.label_issuer.setText(str(decode_rawData(get_rawData(kid)).issuer))
        win.label_version.setText(str(decode_rawData(get_rawData(kid)).version))
        try:
            win.label_sha.setText(str(decode_rawData(get_rawData(kid)).signature_hash_algorithm))
        except UnsupportedAlgorithm as e:
            win.label_sha.setText(str(e))
        win.show()
        return win

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(950, 650)
        table = self.table1
        self.menuCerts.triggered[QAction].connect(self.change_mainWindow)
        self.detail_win = DetailCert_Ui()
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 100)
        table.setSortingEnabled(True)
        cl = download_countrylist()
        for c in cl:
            self.combo2.addItem(c)
        self.fill_table()
        self.combo1.currentTextChanged.connect(self.fill_table)
        self.combo2.currentTextChanged.connect(self.fill_table)

class Cert_Ui(QMainWindow, ui.cert_ui.Ui_MainWindow):
    def change_mainWindow(self, q):
        widget.setCurrentIndex((1) if q == self.actionCert else (2) if q == self.actionRule else (3) if q == self.actionRl else (0))
        if q == self.actionTl:
            Tl.combo1.setCurrentIndex(0)
            Tl.combo2.setCurrentIndex(0)
            Tl.fill_table()

    def fill_table(self):
        if self.delete_win.isVisible():
            self.delete_win.close()
        if self.upload_win.isVisible():
            self.upload_win.close()
        table = self.table1
        table.setRowCount(0)
        rows = select_table_tl(None, config()['Country_Name'])
        table.setRowCount(len(rows)+1)
        row = 0
        for cert in rows:
            button = QPushButton(table)
            button.setText("Details")
            button.clicked.connect(self.detail_window)
            table.setCellWidget(row, 0, button)
            table.setItem(row, 1, QTableWidgetItem(cert[0]))
            certificateType = cert[2]
            if certificateType == "AUTHENTICATION":
                certificateType = "AUTH"
            table.setItem(row, 2, QTableWidgetItem(certificateType))
            table.setItem(row, 3, QTableWidgetItem(cert[3]))
            expiryDate = str(decode_rawData(cert[6]).not_valid_after)
            table.setItem(row, 4, QTableWidgetItem(expiryDate))
            if certificateType == "DSC":
                button = QPushButton(table)
                button.setText("Delete")
                button.clicked.connect(self.delete_window)
                button.setStyleSheet("background-color: red")
                table.setCellWidget(row, 5, button)
            for x in range(4):
                cell = table.item(row, x+1)
                cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
            row += 1
        table.sortItems(2, order=Qt.AscendingOrder)
        button = QPushButton(table)
        button.setText("New Certificate")
        button.clicked.connect(self.upload_window)
        table.setCellWidget(row, 1, button)
        table.setSpan(row, 1, 1, 4)

    def detail_window(self):
        win = self.detail_win
        win.setWindowModality(Qt.ApplicationModal)
        btn = QApplication.focusWidget()
        pos = self.table1.indexAt(btn.pos())
        model = self.table1.model()
        kid = model.data(model.index(pos.row(), 1))
        win.label_kid.setText(str(kid))
        win.label_issuer.setText(str(decode_rawData(get_rawData(kid)).issuer))
        win.label_version.setText(str(decode_rawData(get_rawData(kid)).version))
        win.label_sha.setText(str(decode_rawData(get_rawData(kid)).signature_hash_algorithm))
        win.show()
        return win

    def upload_window(self):
        win = self.upload_win
        win.setWindowModality(Qt.ApplicationModal)
        win.update_values()
        date = QDate.currentDate()
        win.calendar_TS.setDateRange(date, QDate(date.year()+1, date.month(), date.day()))
        win.calendar_ED.setDateRange(date, QDate(date.year()+3, date.month(), date.day()))
        win.calendar_TS.selectionChanged.connect(win.update_values)
        win.calendar_ED.selectionChanged.connect(win.update_values)
        ts = win.calendar_TS.selectedDate().toPython()
        ed = win.calendar_ED.selectedDate().toPython()
        win.pushButton.clicked.connect(lambda: create_certificate(ts, ed))
        win.pushButton.clicked.connect(update_table)
        win.pushButton.clicked.connect(self.fill_table)
        win.show()
        return win

    def delete_window(self):
        win = self.delete_win
        win.setWindowModality(Qt.ApplicationModal)
        btn = QApplication.focusWidget()
        pos = self.table1.indexAt(btn.pos())
        model = self.table1.model()
        kid = model.data(model.index(pos.row(), 1))
        win.label_kid.setText(str(kid))
        type = model.data(model.index(pos.row(), 2))
        win.label_type.setText(str(type))
        rawData = decode_rawData(get_rawData(kid))
        win.label_issuer.setText(str(rawData.issuer))
        expiryDate = str(rawData.not_valid_after)
        diff = compare_dateTime(expiryDate.split(" ")[0])
        win.label_msg.setText(
        "This certificate " + (f"is valid for another {diff}" if diff >= 0 
        else "has been invalid for " + str(-diff)) + f" days. Proceed?"
        )
        win.button1.clicked.connect(lambda: delete_certificate(kid))
        win.button1.clicked.connect(update_table)
        win.button1.clicked.connect(self.fill_table)
        win.show()
        return win

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(950, 650)
        self.setWindowTitle("DCC-Admin-Tool: Cert")
        self.detail_win = DetailCert_Ui()
        self.upload_win = UploadCert_Ui()
        self.delete_win = DeleteCert_Ui()
        self.menuCerts.triggered[QAction].connect(self.change_mainWindow)
        self.fill_table()

class Rule_Ui(QMainWindow, ui.rule_ui.Ui_MainWindow):
    def change_mainWindow(self, q):
        widget.setCurrentIndex((1) if q == self.actionCert else (2) if q == self.actionRule else (3) if q == self.actionRl else (0))

    def update_window(self):
        btn = QApplication.focusWidget()
        pos = self.table1.indexAt(btn.pos())
        model = self.table1.model()
        id = model.data(model.index(pos.row(), 1))
        print("update " + id)

    def delete_window(self):
        win = self.delete_win
        win.setWindowModality(Qt.ApplicationModal)
        btn = QApplication.focusWidget()
        pos = self.table1.indexAt(btn.pos())
        model = self.table1.model()
        id = model.data(model.index(pos.row(), 1))
        win.label_id.setText(str(id))
        win.show()
        return win

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(950, 650)
        self.setWindowTitle("DCC-Admin-Tool: Rule")
        table = self.table1
        self.menuCerts.triggered[QAction].connect(self.change_mainWindow)
        self.delete_win = DeleteRule_Ui()
        rules = open_validationRules()
        table.setRowCount(len(rules)*4)
        row = 1
        for ruleId in rules.keys():
            ruleVersions = rules[ruleId]
            for ruleVersion in ruleVersions:
                table.setSpan(row-1, 0, 1, 7)
                ruleJson = decode_cms(ruleVersion)
                button = QPushButton(table)
                button.setText("Update")
                button.clicked.connect(self.update_window)
                table.setCellWidget(row, 0, button)
                table.setItem(row, 1, QTableWidgetItem(ruleJson['Identifier']))
                table.setItem(row, 2, QTableWidgetItem(ruleJson['Type']))
                table.setItem(row, 3, QTableWidgetItem(ruleJson['CertificateType']))
                table.setItem(row, 4, QTableWidgetItem(ruleVersion['validFrom']))
                table.setItem(row, 5, QTableWidgetItem(ruleVersion['validTo']))
                button = QPushButton(table)
                button.setText("Delete")
                button.clicked.connect(self.delete_window)
                button.setStyleSheet("background-color: red")
                table.setCellWidget(row, 6, button)
                table.setSpan(row, 0, 2, 1)
                table.setSpan(row, 6, 2, 1)
                row += 1
                table.setItem(row+1, 0, QTableWidgetItem("Ver. " + ruleVersion['version']))
                table.setItem(row+1, 6, QTableWidgetItem(
                    str(compare_dateTime(ruleVersion['validTo'].split("T")[0])) + " days left"))
                table.setSpan(row, 1, 2, 5)
                for language in ruleJson['Description']:
                    if language['lang'] == str(config()['Country_Name']).lower():
                        table.setItem(row, 1, QTableWidgetItem(language['desc']))
                if table.itemAt(row, 1) == None:
                    for language in ruleJson['Description']:
                        if language['lang'] == "en":
                            table.setItem(row, 1, QTableWidgetItem(language['desc']))
                row += 3
        for row in range(table.rowCount()):
            for column in range(table.columnCount()):
                cell = table.item(row, column)
                if cell != None:
                    cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

class Rl_Ui(QMainWindow, ui.rl_ui.Ui_MainWindow):
    def change_mainWindow(self, q):
        widget.setCurrentIndex((1) if q == self.actionCert else (2) if q == self.actionRule else (3) if q == self.actionRl else (0))

    def fill_table(self):
        deleted = str(self.comboBox.currentText())
        country = config()['Country_Name'] if self.checkBox.isChecked() else None
        table = self.table1
        table.setRowCount(0)
        if deleted == "-":
            deleted = None
        elif deleted == "True":
            deleted = 1
        elif deleted == "False":
            deleted = 0
        rows = select_table_rl(deleted, country)
        table.setRowCount(len(rows))
        row = 0
        for batch in rows:
            table.setItem(row, 0, QTableWidgetItem(batch[0]))
            table.setItem(row, 1, QTableWidgetItem(batch[1]))
            table.setItem(row, 2, QTableWidgetItem(batch[2]))
            table.setItem(row, 3, QTableWidgetItem("True" if batch[3] == "1" else "False"))
            row += 1
        table.sortItems(3, order=Qt.DescendingOrder)
        for x in range(table.rowCount()):
                for y in range(table.columnCount()):
                    cell = table.item(x, y)
                    cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(950, 650)
        self.setWindowTitle("DCC-Admin-Tool: Revocation")
        table = self.table1
        self.menuCerts.triggered[QAction].connect(self.change_mainWindow)
        table.setSortingEnabled(True)
        self.fill_table()
        self.comboBox.currentTextChanged.connect(self.fill_table)
        self.checkBox.stateChanged.connect(self.fill_table)
                
class DetailCert_Ui(QMainWindow, ui.detailCert_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(750, 350)

class UploadCert_Ui(QMainWindow, ui.uploadCert_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(350, 650)

    def update_values(self):
        self.label_TS.setText(str(self.calendar_TS.selectedDate().toPython()))
        self.label_ED.setText(str(self.calendar_ED.selectedDate().toPython()))

class DeleteCert_Ui(QMainWindow, ui.deleteCert_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(550, 300)

class DeleteRule_Ui(QMainWindow, ui.deleteRule_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(550, 300)
    
def ui_init():
    app = QApplication()
    app.setApplicationDisplayName('DCC-Admin-Tool')
    update_validationRules()
    print("Finished.")
    global widget, Tl
    widget = QStackedWidget()
    Tl = Tl_Ui()
    Cert = Cert_Ui()
    Rule = Rule_Ui()
    Rl = Rl_Ui()
    widget.addWidget(Tl)
    widget.addWidget(Cert)
    widget.addWidget(Rule)
    widget.addWidget(Rl)
    widget.setCurrentWidget(Tl)
    widget.show()
    app.exec()

