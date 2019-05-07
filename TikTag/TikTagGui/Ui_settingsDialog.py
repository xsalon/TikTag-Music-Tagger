# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views\settingsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 380)
        Dialog.setMinimumSize(QtCore.QSize(320, 380))
        Dialog.setMaximumSize(QtCore.QSize(320, 380))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.onlineSettings = QtWidgets.QWidget()
        self.onlineSettings.setObjectName("onlineSettings")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.onlineSettings)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.onlineSettings)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget.setIconSize(QtCore.QSize(30, 30))
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.label = QtWidgets.QLabel(self.onlineSettings)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.groupBoxOverwrite = QtWidgets.QGroupBox(self.onlineSettings)
        self.groupBoxOverwrite.setObjectName("groupBoxOverwrite")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBoxOverwrite)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButtonComplete = QtWidgets.QRadioButton(self.groupBoxOverwrite)
        self.radioButtonComplete.setChecked(True)
        self.radioButtonComplete.setObjectName("radioButtonComplete")
        self.verticalLayout_3.addWidget(self.radioButtonComplete)
        self.radioButtonOverwrite = QtWidgets.QRadioButton(self.groupBoxOverwrite)
        self.radioButtonOverwrite.setObjectName("radioButtonOverwrite")
        self.verticalLayout_3.addWidget(self.radioButtonOverwrite)
        self.verticalLayout_2.addWidget(self.groupBoxOverwrite)
        self.tabWidget.addTab(self.onlineSettings, "")
        self.generalSettings = QtWidgets.QWidget()
        self.generalSettings.setObjectName("generalSettings")
        self.tabWidget.addTab(self.generalSettings, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.label.setText(_translate("Dialog", "* Priority is specified by order"))
        self.groupBoxOverwrite.setTitle(_translate("Dialog", "Download mode"))
        self.radioButtonComplete.setText(_translate("Dialog", "Complete default metadata"))
        self.radioButtonOverwrite.setText(_translate("Dialog", "Overwrite default metadata"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.onlineSettings), _translate("Dialog", "Online"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalSettings), _translate("Dialog", "General"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
