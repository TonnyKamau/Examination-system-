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
            self.dateEdit.clear()
            self.bookEdit.clear()
            self.unitEdit.clear()
            self.telEdit.clear()
            self.courseEdit.clear()
            QMessageBox.information(
                QMessageBox(), 'Successful', 'Record updated Successfully')
        except mc.Error as e:
            QMessageBox.warning(QMessageBox(), 'Error',