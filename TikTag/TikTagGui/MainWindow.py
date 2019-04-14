from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from TikTagGui.MyFileSystemModel import MyFileSystemModel
from TikTagGui.Ui_MainWindow import Ui_MainWindow
from TikTagGui.Ui_urlDialog import Ui_Dialog as UrlDialog
from TikTagGui.Ui_pathDialog import Ui_Dialog as PathDialog
from TikTagCtrl.Tagger import Tagger
import enum
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.filePath = None
        self.supportedFormats = Tagger.fileFormats

        self.actionSelectFolder.triggered.connect(self.selectFolderDialog)
        self.treeView.clicked.connect(self.fetchTags)
        self.albumArtLabel.mousePressEvent = self.pageUpImage
        self.bigAlbumArtLabel.mousePressEvent = self.pageDownImage

        self.listWidget.customContextMenuRequested.connect(self.ctxListWidget)

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

    def fetchTags(self):
        self.listWidget.clear()
        path = self.fileModel.filePath(self.treeView.currentIndex())
        self.filePath = path
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
        cover.loadFromData(Tagger.retrieveImage(path))
        self.albumArtLabel.setPixmap(cover)
        self.bigAlbumArtLabel.setPixmap(cover)

        images = Tagger.retrieveAllImagesDetails(path)

        for image in images:
            item = QListWidgetItem()
            item.setText(image.infoString)
            item.setData(Qt.UserRole, image.tag.HashKey)
            icon = QIcon()
            picture = QPixmap()
            picture.loadFromData(image.tag.data)
            icon.addPixmap(picture)
            item.setIcon(icon)
            self.listWidget.addItem(item)

    def ctxListWidget(self):
        menu = QMenu()
        submenuAdd = menu.addMenu("Add")
        addByPath = submenuAdd.addAction("Path...")
        addByUrl = submenuAdd.addAction("URL...")
        addByPath.triggered.connect(self.addImageByPath)
        addByUrl.triggered.connect(self.addImageByUrl)

        mapper = QSignalMapper(self)
        if self.listWidget.selectedItems():
            submenuType = menu.addMenu("Type")  
            
            newAction = []
            for i in range(len(Tagger.imageTypes)):
                newAction.insert(i, submenuType.addAction(Tagger.imageTypes[i]))
                newAction[i].triggered.connect(mapper.map)
                mapper.setMapping(newAction[i], i)

            mapper.mapped[int].connect(self.changeImageType)

            delete = menu.addAction("Delete")
            delete.triggered.connect(self.deleteImage)
        cursor = QCursor()

        if not self.filePath:
            submenuAdd.setEnabled(False)
        else:
            submenuAdd.setEnabled(True)
        menu.exec_(cursor.pos())

    def addImageByPath(self):
        self.Dialog = QDialog()
        self.uiDialog = PathDialog()
        self.uiDialog.setupUi(self.Dialog)
        for item in Tagger.imageTypes:
            self.uiDialog.imgTypeComboBox.addItem(item)

        self.uiDialog.openButton.clicked.connect(self.pathDialog)
        
        if self.Dialog.exec() == QDialog.Accepted:
            path = self.uiDialog.pathLineEdit.text()
            desc = self.uiDialog.descLineEdit.text()
            type = Tagger.imageTypes.index(self.uiDialog.imgTypeComboBox.currentText())
            Tagger.addImage("path", path, desc, type, self.filePath)
            self.fetchTags()

    def pathDialog(self):
        rootPath = QDir.rootPath()
        image = QFileDialog.getOpenFileName(self, "Select Images", rootPath, "Image Files (*.jpg *.png)")
        self.uiDialog.pathLineEdit.setText(image[0])

    def addImageByUrl(self):
        self.Dialog = QDialog()
        ui = UrlDialog()
        ui.setupUi(self.Dialog)
        for item in Tagger.imageTypes:
            ui.imgTypeComboBox.addItem(item)
        
        if self.Dialog.exec() == QDialog.Accepted:
            url = ui.urlLineEdit.text()
            desc = ui.descLineEdit.text()
            type = Tagger.imageTypes.index(ui.imgTypeComboBox.currentText())
            Tagger.addImage("url", url, desc, type, self.filePath)
            self.fetchTags()


    def changeImageType(self, type):
        for item in self.listWidget.selectedItems():
            Tagger.changeImageType(type, item.data(Qt.UserRole), self.filePath)
        self.fetchTags()

    def deleteImage(self):
        for item in self.listWidget.selectedItems():
            Tagger.deleteImages(item.data(Qt.UserRole), self.filePath)
        self.fetchTags()

    def pageUpImage(self, event):
        self.verticalStackedWidget.setCurrentIndex(1)

    def pageDownImage(self, event):
        self.verticalStackedWidget.setCurrentIndex(0)
      
