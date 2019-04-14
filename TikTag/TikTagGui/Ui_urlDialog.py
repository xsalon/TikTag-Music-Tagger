# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urlDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 180)
        Dialog.setModal(True)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setContentsMargins(-1, 15, -1, -1)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setObjectName("formLayout")
        self.urlLabel = QtWidgets.QLabel(Dialog)
        self.urlLabel.setObjectName("urlLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.urlLabel)
        self.urlLineEdit = QtWidgets.QLineEdit(Dialog)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.urlLineEdit)
        self.descLabel = QtWidgets.QLabel(Dialog)
        self.descLabel.setObjectName("descLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.descLabel)
        self.descLineEdit = QtWidgets.QLineEdit(Dialog)
        self.descLineEdit.setObjectName("descLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.descLineEdit)
        self.imgTypeLabel = QtWidgets.QLabel(Dialog)
        self.imgTypeLabel.setObjectName("imgTypeLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.imgTypeLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)
        self.imgTypeComboBox = QtWidgets.QComboBox(Dialog)
        self.imgTypeComboBox.setObjectName("imgTypeComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.imgTypeComboBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.urlLabel.setText(_translate("Dialog", "URL:"))
        self.descLabel.setText(_translate("Dialog", "Description:"))
        self.imgTypeLabel.setText(_translate("Dialog", "Type:"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
