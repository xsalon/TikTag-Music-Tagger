from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MyFileSystemModel import MyFileSystemModel
from Ui_MainWindow import Ui_MainWindow
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.actionSelectFolder.triggered.connect(self.selectFolderDialog)
        self.treeView.clicked.connect(self.fetchTags)

        self.thisdict =	{
            "brand": "Ford",
            "model": "Mustang",
            "year": 1964
        }

    def selectFolderDialog(self):
        rootPath = QDir.rootPath()
        folder = str(QFileDialog.getExistingDirectory(None, "Select Directory", rootPath))
        
        if rootPath != folder:
            self.createMusicList(folder)

    def createMusicList(self, folder):
        path = ''
        data = ""
        self.fileModel = MyFileSystemModel(path, data)

        self.treeView.setModel(self.fileModel)
        self.treeView.setRootIndex(self.fileModel.index(folder))
        self.treeView.setSortingEnabled(1)
        
        for i in range(self.fileModel.columnCount()):
            self.treeView.hideColumn(i)
        self.treeView.showColumn(0)
        self.treeView.showColumn(4)

    def fetchTags(self, index):
        print(index.model().filePath(index))

        self.tagTableModel = QStandardItemModel(len(self.thisdict), 2);
        self.tableView.setModel(self.tagTableModel)
        
        rows = 0;
        
        for tagname, tagvalue in self.thisdict.items():
            firstitem = QStandardItem(tagname)
            seconditem = QStandardItem(tagvalue)
            self.tagTableModel.setItem(rows, 0, firstitem);
            self.tagTableModel.setItem(rows, 1, seconditem);
            rows += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
