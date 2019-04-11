from PyQt5.QtWidgets import QFileSystemModel
from PyQt5 import QtCore
from PyQt5.QtCore import QDir
from TikTagCtrl.Tagger import Tagger

class MyFileSystemModel(QFileSystemModel):
    def __init__(self, path, parent=None):
        super(MyFileSystemModel, self).__init__(parent)
        self.setRootPath(path)
        self.setFilter(QDir.NoDotAndDotDot | QDir.Files | QDir.AllDirs)
        
        filterFormatsList = []
        for format in Tagger.fileFormats:
            filterFormatsList.append("*." + format)
        
        self.setNameFilters(filterFormatsList)
        self.setNameFilterDisables(0)
    
    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(MyFileSystemModel, self).columnCount() + 1

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole): 
        headerList = ["Name", "Size", "Type", "Modified", "Status"]
        for i in range(5):
            if (section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
                return headerList[i]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                filePath = MyFileSystemModel.filePath(self, index)
                return Tagger.checkStatus(filePath)                
        return super(MyFileSystemModel, self).data(index, role)

    