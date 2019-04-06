from PyQt5.QtWidgets import QFileSystemModel
from PyQt5 import QtCore
from PyQt5.QtCore import QDir

class MyFileSystemModel(QFileSystemModel):
    def __init__(self, path, data, parent=None):
        super(MyFileSystemModel, self).__init__(parent)
        self.setRootPath(path)
        self.setFilter(QDir.NoDotAndDotDot | QDir.Files | QDir.AllDirs)
        filterFormatsList = ["*.mp3", "*.flac", "*.m4a"]
        self.setNameFilters(filterFormatsList)
        self.setNameFilterDisables(0)
        self.count = 0
        
        #self._data = DataStructure()
    
    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(MyFileSystemModel, self).columnCount() + 1

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole): 
        headerList = ["Name", "Size", "Type", "Modified", "Status"]
        for i in range(5):
            if (section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
                return headerList[i]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        self.count = self.count+1
        #print(str(index) + " | " + str(role) + " | " + str(self.count))
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                return str(MyFileSystemModel.filePath(self, index))
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignLeft
        return super(MyFileSystemModel, self).data(index, role)

    