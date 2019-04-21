# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tagFileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 175)
        Dialog.setMinimumSize(QtCore.QSize(0, 175))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 175))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formatGroupBox = QtWidgets.QGroupBox(Dialog)
        self.formatGroupBox.setObjectName("formatGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.formatGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.formatGroupBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.formatStringLineEdit = QtWidgets.QLineEdit(self.formatGroupBox)
        self.formatStringLineEdit.setObjectName("formatStringLineEdit")
        self.gridLayout_2.addWidget(self.formatStringLineEdit, 0, 0, 1, 2)
        self.formatStringPreview = QtWidgets.QLabel(self.formatGroupBox)
        self.formatStringPreview.setText("")
        self.formatStringPreview.setObjectName("formatStringPreview")
        self.gridLayout_2.addWidget(self.formatStringPreview, 4, 0, 1, 1)
        self.tagListComboBox = QtWidgets.QComboBox(self.formatGroupBox)
        self.tagListComboBox.setObjectName("tagListComboBox")
        self.gridLayout_2.addWidget(self.tagListComboBox, 3, 0, 1, 1)
        self.addTagButton = QtWidgets.QPushButton(self.formatGroupBox)
        self.addTagButton.setMinimumSize(QtCore.QSize(0, 0))
        self.addTagButton.setMaximumSize(QtCore.QSize(75, 16777215))
        self.addTagButton.setObjectName("addTagButton")
        self.gridLayout_2.addWidget(self.addTagButton, 3, 1, 1, 1)
        self.previewButton = QtWidgets.QPushButton(self.formatGroupBox)
        self.previewButton.setObjectName("previewButton")
        self.gridLayout_2.addWidget(self.previewButton, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.formatGroupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tag - File"))
        self.formatGroupBox.setTitle(_translate("Dialog", "Format options"))
        self.addTagButton.setText(_translate("Dialog", "Add"))
        self.previewButton.setText(_translate("Dialog", "Preview"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
