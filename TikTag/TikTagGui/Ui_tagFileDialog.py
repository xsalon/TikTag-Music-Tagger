# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views\tagFileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 210)
        Dialog.setMinimumSize(QtCore.QSize(0, 210))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 210))
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formatGroupBox = QtWidgets.QGroupBox(Dialog)
        self.formatGroupBox.setObjectName("formatGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.formatGroupBox)
        self.gridLayout_2.setContentsMargins(-1, -1, -1, 9)
        self.gridLayout_2.setVerticalSpacing(9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(self.formatGroupBox)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tagListComboBox = QtWidgets.QComboBox(self.widget)
        self.tagListComboBox.setObjectName("tagListComboBox")
        self.horizontalLayout.addWidget(self.tagListComboBox)
        self.addTagButton = QtWidgets.QPushButton(self.widget)
        self.addTagButton.setMinimumSize(QtCore.QSize(0, 0))
        self.addTagButton.setMaximumSize(QtCore.QSize(75, 16777215))
        self.addTagButton.setObjectName("addTagButton")
        self.horizontalLayout.addWidget(self.addTagButton)
        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 2)
        self.formatStringLineEdit = QtWidgets.QLineEdit(self.formatGroupBox)
        self.formatStringLineEdit.setObjectName("formatStringLineEdit")
        self.gridLayout_2.addWidget(self.formatStringLineEdit, 0, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(self.formatGroupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 360, 64))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formatStringPreview = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.formatStringPreview.setText("")
        self.formatStringPreview.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formatStringPreview.setObjectName("formatStringPreview")
        self.verticalLayout.addWidget(self.formatStringPreview)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 3, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.formatGroupBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.formatGroupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tag - File"))
        self.formatGroupBox.setTitle(_translate("Dialog", "Format options"))
        self.addTagButton.setText(_translate("Dialog", "Add"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
