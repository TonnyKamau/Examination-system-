from PyQt5.QtCore import QCoreApplication, Qt, QBasicTimer, QPoint, QTimer, QTime, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QFileDialog
import HOME as home
import Login as login
from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator

import pandas as pd
import pdfkit as pdf
import sys
import xlwt
import xlrd
import mysql.connector as mc
mydb = mc.connect(
    host="localhost",
    user="root",
    password="",
    database="examsystem"

)

mycursor = mydb.cursor(buffered=True)



class Mainclass(home.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Mainclass, self).__init__()
        self.setupUi(self)
        self.showMaximized()
        # PAGE 1
        self.btn_page_1.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_1))

        # PAGE 2
        self.btn_page_2.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_2))

        # PAGE 3
        self.btn_page_3.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_3))   
        # PAGE 4
        self.Btn_Panel.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_4))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        head = self.tableWidget_2.horizontalHeader()
        head.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        head.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        head.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        head.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        head.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        head.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        head.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.submitButton.clicked.connect(self.record_details)
        self.submitButton.clicked.connect(self.analysis)
        self.loaddata()
        self.loadtable()
        self.analysis()
        self.exportPDF.clicked.connect(self.printPDF)
        self.importCSV.clicked.connect(self.import_canditates)
        self.confirmregistered.clicked.connect(self.confirm_registered)
        self.exportCSV.clicked.connect(self.printCSV)
        self.searchreg.clicked.connect(self.filterreg)
        self.searchunit.clicked.connect(self.filterexamunit)
        self.refreshButton.clicked.connect(self.loaddata)
        self.refreshButton_2.clicked.connect(self.loadtable)
        self.updateButton.clicked.connect(self.update_details)
        self.deleteButton.clicked.connect(self.deleteRecord) 
    def analysis(self):
        import math
        mycursor.execute("SELECT COUNT(regno) FROM examination_form")
        attendance=mycursor.fetchone()
        mycursor.execute(
            "SELECT COUNT(regno) FROM registered_candidates")
        registered=mycursor.fetchone()
        for row in registered:
            if(row==0.0):
                self.registered.setText("0.0%")
                self.attended.setText("0.0%")
                self.unattended.setText("0.0%")
                break;
            else:
                self.registered.setText("100.0%")
            for low in attendance:
                x=int(row)
                y=int(low)
                attend=(y/x) * 100
                self.attended.setText(str(int(attend))+"%")
                unattend = ((x - y)/x) * 100
                self.unattended.setText(str(int(unattend))+"%")

    def filterexamunit(self):
        unitcode = self.lineexam.text()
        load = "SELECT * from examination_form  where unitcode like  '"+unitcode+"'"
        mycursor.execute(load)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(mycursor):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

    def deleteRecord(self):
        delreg = self.linedelreg.text()
        
        try:
            load = "DELETE from examination_form where regno like  '"+delreg+"'"
            mycursor.execute(load)
            mydb.commit()

            QMessageBox.information(
                QMessageBox(), 'Successful', 'Deleted From Table Successful')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Could not Delete student from the database.')
    def filterreg(self):
        studentreg = self.linereg.text()

        load = "SELECT * from examination_form where regno like  '"+studentreg+"'"
        mycursor.execute(load)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(mycursor):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

    def loaddata(self):
        load = "SELECT * FROM examination_form"   
        mycursor.execute(load)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(mycursor):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

    def loadtable(self):
        load = "SELECT * FROM examination_form"
        mycursor.execute(load)
        self.tableWidget_2.setRowCount(0)
        for row_number, row_data in enumerate(mycursor):
            self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

    def update_details(self):
        try:
            regnumber = self.regEdit.text()
            examcard = self.cardEdit.text()
            date = self.dateEdit.text()
            booklet = self.bookEdit.text()
            examunit = self.unitEdit.text()
            phoneNo = self.telEdit.text()
            course = self.courseEdit.text()
            query = "UPDATE examination_form SET examcardno= %s,bookletno= %s,unitcode= %s,phonenumber= %s, examdate= %s,course = %s WHERE regno = %s"
            value = (examcard, booklet,
                     examunit, phoneNo, date, course,regnumber)
            mycursor.execute(query, value)
            mydb.commit()
            self.regEdit.clear()
            self.cardEdit.clear()
            self.bookEdit.clear()
            self.unitEdit.clear()
            self.telEdit.clear()
            self.courseEdit.clear()
            QMessageBox.information(
                QMessageBox(), 'Successful', 'Record updated Successfully')
        except mc.Error as e:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'error occurence')
    def record_details(self):
        try:
            regnumber = self.regEdit.text()
            examcard = self.cardEdit.text()
            date = self.dateEdit.text()
            booklet = self.bookEdit.text()
            examunit = self.unitEdit.text()
            phoneNo = self.telEdit.text()
            course = self.courseEdit.text()
            query = "INSERT INTO examination_form (regno, examcardno,bookletno,unitcode,phonenumber, examdate,course) VALUES (%s, %s,%s, %s,%s, %s,%s)"
            value = (regnumber,examcard,booklet,examunit,phoneNo,date,course)
            mycursor.execute(query, value)
            mydb.commit()
            self.regEdit.clear()
            self.cardEdit.clear()
            self.bookEdit.clear()
            self.unitEdit.clear()
            self.telEdit.clear()
            self.courseEdit.clear()
            QMessageBox.information(
                QMessageBox(), 'Successful', 'Record inserted Successfully')
        except mc.Error as e:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Duplicate Entries')
    def confirm_registered(self):
        try:
            canditatereg = self.confirmline.text()
            mycursor.execute("SELECT * from registered_candidates where regno like '" +
                             canditatereg + "'")
            result = mycursor.fetchone()

            if result == None:
                QMessageBox.warning(QMessageBox(), 'Error',
                                    'STUDENT NOT REGISTERED FOR EXAMINATION')
            else:
                QMessageBox.information(
                    QMessageBox(), 'Successful', 'STUDENT REGISTERED FOR EXAMINATION')
        except mc.Error as e:
            print("error")
    def printCSV(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, 'Save File', 'Examination form', ".xls(*.xls)")

            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            style.font = font
            model = self.tableWidget_2.model()

            for c in range(model.columnCount()):
                text = model.headerData(c, QtCore.Qt.Horizontal)
                first_col = sheet.col(c+1)
                l = len(text)
                first_col.width = (256 * l) + 1000
                sheet.write(0, c + 1, text, style=style)

            for r in range(model.rowCount()):
                text = model.headerData(r, QtCore.Qt.Vertical)
                sheet.write(r + 1, 0, text, style=style)

            for c in range(model.columnCount()):
                for r in range(model.rowCount()):
                    text = model.data(model.index(r, c))
                    sheet.write(r + 1, c + 1, text)

            wbk.save(filename)
            QMessageBox.information(
                QMessageBox(), 'Successful', 'Exported Successfully')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'ERROR OCCURRED.')
     # PUT BUTTON IMPORT
    def import_canditates(self):
        try:
            import os
            filepath = QFileDialog.getOpenFileName(
                self, 'Open file', '*.xls')[0]
            print(filepath)
            filepath = os.path.normpath(filepath)
            filename = filepath.split(os.sep)
            self.filename.setText(filename[-1])
            sheetname=self.sheetname.text()


            book = xlrd.open_workbook(filename[-1])
            sheet = book.sheet_by_name(sheetname)
            # Get the cursor, which is used to traverse the database, line by line
            # Create the INSERT INTO sql query
            query = """INSERT INTO registered_candidates  (regno,name,examcardno,unitcode,session,course) VALUES (%s, %s, %s, %s, %s, %s)"""

            # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
            for r in range(1, sheet.nrows):
                Registration_Number = sheet.cell(r, 1).value
                Name = sheet.cell(r, 2).value
                Examcard_Number = sheet.cell(r, 3).value
                Exam_unitcode = sheet.cell(r, 4).value
                Session = sheet.cell(r, 5).value
                Course_Name = sheet.cell(r, 6).value
            # Assign values from each row
                values = (Registration_Number,Name ,Examcard_Number,
                        Exam_unitcode, Session, Course_Name)

            # Execute sql Query
                mycursor.execute(query, values)

            # Close the cursor
            mycursor.close()

            # Commit the transaction
            mydb.commit()

            # Close the database connection
            mydb.close()

            # Print results

            columns = str(sheet.ncols)
            rows = str(sheet.nrows)
            print("I just imported columns" + columns + "  " + rows + " rows to MySQL!")
            QMessageBox.information(
                QMessageBox(), 'Successful', 'Imported Successfully')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Enter SHEETNAME first.')




    def printPDF(self):
        try:
            app = QtWidgets.QApplication([])

            w = QtWidgets.QTableWidget(10, 10)
            for i in range(10):
                for j in range(10):
                    it = QtWidgets.QTableWidgetItem("{}-{}".format(i, j))
                    w.setItem(i, j, it)


            filename = "table.pdf"
            model = w.model()

            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            printer.setPaperSize(QtPrintSupport.QPrinter.A4)
            printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
            printer.setOutputFileName(filename)

            doc = QtGui.QTextDocument()

            html = """<html>
            <head>
            <style>
            table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            }
            </style>
            </head>"""
            html += "<table><thead>"
            html += "<tr>"
            for c in range(model.columnCount()):
                html += "<th>{}</th>".format(model.headerData(c, QtCore.Qt.Horizontal))

            html += "</tr></thead>"
            html += "<tbody>"
            for r in range(model.rowCount()):
                html += "<tr>"
                for c in range(model.columnCount()):
                    html += "<td>{}</td>".format(model.index(r, c).data() or "")
                html += "</tr>"
            html += "</tbody></table>"
            doc.setHtml(html)
            doc.setPageSize(QtCore.QSizeF(printer.pageRect().size()))
            doc.print_(printer)
            QMessageBox.information(
                QMessageBox(), 'Successful', 'exported Successfully')
        except Exception:
             QMessageBox.warning(QMessageBox(), 'Error',
                                'error.')
 
class Login(login.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.frame_error.hide()
        self.pushButton_login.clicked.connect(self.checkFields)

    stylePopupError = (
        "background-color: rgb(255, 85, 127); border-radius: 5px;")
    stylePopupOk = ("background-color: rgb(0, 255, 123); border-radius: 5px;")

    def checkFields(self):
        def showMessage(message):
            self.frame_error.show()
            self.label_error.setText(message)
        try:

            textUser = self.lineEdit_user.text()
            textPassword = self.lineEdit_password.text()
            mycursor.execute("SELECT username,password from users where username like '" +
                             textUser + "'and password like '"+textPassword+"'")
            result = mycursor.fetchone()

            if result == None:
                text = "Incorrect Credentials"
                showMessage(text)
                self.frame_error.setStyleSheet(self.stylePopupError)

            else:
                text = " Login Successfully "
                if self.checkBox_save_user.isChecked():
                    text = text + " | Saver user: OK "
                showMessage(text)
                self.frame_error.setStyleSheet(self.stylePopupOk)
                self.w = Mainclass()
                self.w.show()
                self.hide()

        except mc.Error as e:
            text = "error in the database"
            showMessage(text)
            self.frame_error.setStyleSheet(self.stylePopupError)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qt_app = Login()
    qt_app.show()
    app.exec_()
