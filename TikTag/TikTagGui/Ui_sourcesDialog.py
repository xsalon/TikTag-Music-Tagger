# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sourcesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(186, 110)
        Dialog.setMinimumSize(QtCore.QSize(186, 110))
        Dialog.setMaximumSize(QtCore.QSize(186, 110))
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(15, 9, 15, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxDiscogs = QtWidgets.QCheckBox(Dialog)
        self.checkBoxDiscogs.setChecked(True)
        self.checkBoxDiscogs.setObjectName("checkBoxDiscogs")
        self.verticalLayout.addWidget(self.checkBoxDiscogs)
        self.checkBoxMusicBrainz = QtWidgets.QCheckBox(Dialog)
        self.checkBoxMusicBrainz.setChecked(True)
        self.checkBoxMusicBrainz.setObjectName("checkBoxMusicBrainz")
        self.verticalLayout.addWidget(self.checkBoxMusicBrainz)
        spacerItem = QtWidgets.QSpacerItem(5, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set Sources"))
        self.checkBoxDiscogs.setText(_translate("Dialog", "Discogs"))
        self.checkBoxMusicBrainz.setText(_translate("Dialog", "MusicBrainz"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
