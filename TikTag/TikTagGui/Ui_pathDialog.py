# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views\pathDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 175)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(400, 175))
        Dialog.setMaximumSize(QtCore.QSize(400, 175))
        Dialog.setModal(True)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setContentsMargins(-1, 15, -1, -1)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setObjectName("formLayout")
        self.pathLabel = QtWidgets.QLabel(Dialog)
        self.pathLabel.setObjectName("pathLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pathLabel)
        self.descLabel = QtWidgets.QLabel(Dialog)
        self.descLabel.setObjectName("descLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.descLabel)
        self.descLineEdit = QtWidgets.QLineEdit(Dialog)
        self.descLineEdit.setObjectName("descLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.descLineEdit)
        self.imgTypeLabel = QtWidgets.QLabel(Dialog)
        self.imgTypeLabel.setObjectName("imgTypeLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.imgTypeLabel)
        self.imgTypeComboBox = QtWidgets.QComboBox(Dialog)
        self.imgTypeComboBox.setObjectName("imgTypeComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.imgTypeComboBox)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pathLineEdit = QtWidgets.QLineEdit(self.widget)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.horizontalLayout.addWidget(self.pathLineEdit)
        self.openButton = QtWidgets.QPushButton(self.widget)
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setMinimumSize(QtCore.QSize(0, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pathLineEdit, self.openButton)
        Dialog.setTabOrder(self.openButton, self.descLineEdit)
        Dialog.setTabOrder(self.descLineEdit, self.imgTypeComboBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Open Image"))
        self.pathLabel.setText(_translate("Dialog", "Path:"))
        self.descLabel.setText(_translate("Dialog", "Description:"))
        self.imgTypeLabel.setText(_translate("Dialog", "Type:"))
        self.openButton.setText(_translate("Dialog", "Open..."))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
