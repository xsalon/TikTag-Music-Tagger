from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from TikTagGui.MyFileSystemModel import MyFileSystemModel
from TikTagGui.Ui_MainWindow import Ui_MainWindow
from TikTagCtrl.Tagger import Tagger
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.supportedFormats = Tagger.fileFormats

        self.actionSelectFolder.triggered.connect(self.selectFolderDialog)
        self.treeView.clicked.connect(self.fetchTags)
        self.albumArtLabel.mousePressEvent = self.pageUpImage
        self.bigAlbumArtLabel.mousePressEvent = self.pageDownImage

    def selectFolderDialog(self):
        rootPath = QDir.rootPath()
        folder = str(QFileDialog.getExistingDirectory(None, "Select Directory", rootPath))
        
        if rootPath != folder:
            self.createMusicList(folder)

    def createMusicList(self, folder):
        path = ''                 
        self.fileModel = MyFileSystemModel(path)

        self.treeView.setModel(self.fileModel)
        self.treeView.setRootIndex(self.fileModel.index(folder))
        self.treeView.setSortingEnabled(1)
        self.treeView.header().setSectionResizeMode(0, QHeaderView.Stretch);
        self.treeView.header().setSectionResizeMode(1, QHeaderView.ResizeToContents);
        
        for i in range(self.fileModel.columnCount()):
            self.treeView.hideColumn(i)
        self.treeView.showColumn(0)
        self.treeView.showColumn(4)

    def fetchTags(self, index):
        path = index.model().filePath(index)
        generalInfo = Tagger.fetchGeneralInfo(path)

        self.labelDuration.setText("Duration: " + generalInfo["Duration"])
        self.labelSampleRate.setText("Sample Rate: " + generalInfo["Sample Rate"])
        self.labelChannels.setText("Channels: " + generalInfo["Channels"])
        self.labelBitrate.setText("Bitrate: " + generalInfo["Bitrate"]) 
        self.labelCodec.setText("Codec: " + generalInfo["Codec"])

        headerTabLabels = ["Name", "Value"]
        metadata = Tagger.fetchTags(path)

        self.tagTableModel = QStandardItemModel(len(metadata), 2)
        self.tagTableModel.setHorizontalHeaderLabels(headerTabLabels)
        self.tableView.setModel(self.tagTableModel)
        #self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        rows = 0;
        
        for tagname, tagvalue in metadata.items():
            firstitem = QStandardItem(tagname)
            seconditem = QStandardItem(str(tagvalue))
            self.tagTableModel.setItem(rows, 0, firstitem)
            self.tagTableModel.setItem(rows, 1, seconditem)
            rows += 1

        cover = QPixmap()
        cover.loadFromData(Tagger.retrieveImages(path))
        self.albumArtLabel.setPixmap(cover)
        self.bigAlbumArtLabel.setPixmap(cover)

    def pageUpImage(self, event):
        self.verticalStackedWidget.setCurrentIndex(1)

    def pageDownImage(self, event):
        self.verticalStackedWidget.setCurrentIndex(0)
      
