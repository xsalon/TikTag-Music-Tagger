from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from TikTagGui.MyFileSystemModel import MyFileSystemModel
from TikTagGui.Ui_MainWindow import Ui_MainWindow
from TikTagGui.Ui_urlDialog import Ui_Dialog as UrlDialog
from TikTagGui.Ui_pathDialog import Ui_Dialog as PathDialog
from TikTagGui.Ui_tagFileDialog import Ui_Dialog as TagFileDialog
from TikTagCtrl.Tagger import Tagger
from TikTagCtrl.TaggerError import *
import shutil
import enum
import sys
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.filePath = None
        self.supportedFormats = Tagger.fileFormats

        self.headerList = ["Name", "Size", "Type", "Modified", "Status"]
        self.fileModel = MyFileSystemModel(self.headerList)
        
        self.ctxListWidget = QMenu()   
        self.ctxListWidgetMapper = QSignalMapper(self)
        self.ctxListWidgetActions = []
        self.actionAddImgByPath = QAction()
        self.actionAddImgByUrl = QAction()
        self.actionSetImgDesc = QAction()
        self.actionDelImg = QAction()
        self.actionDelAllImg = QAction()

        self.ctxTreeView = QMenu()   
        self.actionMakeDir = QAction()
        self.actionOpenFile = QAction()
        self.actionDetails = QAction()
        self.actionRemoveFile = QAction()
        
        self.ctxTreeViewHeader = QMenu()   
        self.ctxTreeViewHeaderMapper = QSignalMapper(self)
        self.ctxTreeViewHeaderActions = []

        self.actionSelectFolder.triggered.connect(self.selectFolderDialog)
        self.actionLevelUp.triggered.connect(self.levelUp)
        self.actionDelete.triggered.connect(self.deleteFiles)
        self.actionSetRootDir.triggered.connect(self.setRootDirectory)
        self.actionCreateFolder.triggered.connect(self.newFolder)
        self.actionRefresh.triggered.connect(self.refreshFileModel)
        self.actionTagToFile.triggered.connect(self.tagToFileName)
        self.actionFileToTag.triggered.connect(self.fileToTagName)
        self.actionFileToTag.triggered.connect(self.deleteTag)
        
        self.actionLevelUp.setEnabled(False)
        self.actionDelete.setEnabled(False)
        self.actionSetRootDir.setEnabled(False)
        self.actionCreateFolder.setEnabled(False)
        self.actionRefresh.setEnabled(False)
        self.actionTagToFile.setEnabled(False)
        self.actionFileToTag.setEnabled(False)
        self.actionDeleteTag.setEnabled(False)

        self.albumArtLabel.mousePressEvent = self.pageUpImage
        self.bigAlbumArtLabel.mousePressEvent = self.pageDownImage

        self.treeView.clicked.connect(self.fetchTags)

        self.listWidget.customContextMenuRequested.connect(self.showCtxListWidget)
        self.listWidget.itemClicked.connect(self.bigImageChange)

        self.tableWidget.itemChanged.connect(self.editTag)

  
    def selectFolderDialog(self):
        rootPath = QDir.rootPath()
        folder = str(QFileDialog.getExistingDirectory(None, "Select Directory", rootPath))
        
        if not self.treeView.model():
            if rootPath != folder:
                self.initWorkDirectory(folder)
        else:
            if rootPath != folder:
                self.changeWorkDirectory(folder)

    
    def initWorkDirectory(self, folder):
        self.fileModel.setReadOnly(False)
        self.treeView.setModel(self.fileModel)
        self.changeWorkDirectory(folder)
        self.treeView.setSortingEnabled(1)
        self.treeView.header().setContextMenuPolicy(Qt.CustomContextMenu)
        self.initCtxTreeViewHeader()
        self.initCtxListWidget()
        self.initCtxTreeView()
        self.treeView.customContextMenuRequested.connect(self.showCtxTreeView)
        self.treeView.header().customContextMenuRequested.connect(self.showCtxTreeViewHeader)
        self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents);
        #self.treeView.header().setSectionResizeMode(0, QHeaderView.Stretch);
        #self.treeView.header().setSectionResizeMode(1, QHeaderView.ResizeToContents);

        self.treeView.selectionModel().selectionChanged.connect(self.enableActions)
        self.actionCreateFolder.setEnabled(True)
        self.actionLevelUp.setEnabled(True)
        self.actionRefresh.setEnabled(True)
        
        for i in range(self.fileModel.columnCount()):
            self.treeView.hideColumn(i)
        self.treeView.showColumn(0)


    def changeWorkDirectory(self, folder):
        self.fileModel.setRootPath(folder)
        self.treeView.setRootIndex(self.fileModel.index(folder))

    
    def fetchTags(self):
        path = self.fileModel.filePath(self.treeView.currentIndex())
        
        if os.path.isdir(path):
            return
        
        self.filePath = path
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

        try:
            generalInfo = Tagger.fetchGeneralInfo(path)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)

        self.labelDuration.setText("Duration: " + generalInfo["Duration"])
        self.labelSampleRate.setText("Sample Rate: " + generalInfo["Sample Rate"])
        self.labelChannels.setText("Channels: " + generalInfo["Channels"])
        self.labelBitrate.setText("Bitrate: " + generalInfo["Bitrate"]) 
        self.labelCodec.setText("Codec: " + generalInfo["Codec"])

        headerTabLabels = ["Name", "Value"]
        
        try:
            metadata = Tagger.fetchTags(path)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)

        oldState = self.tableWidget.blockSignals(True)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(headerTabLabels)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        rows = 0;

        for tagview, tagname in Tagger.id3Keys.items():
            self.tableWidget.insertRow(rows)
            firstitem =  QTableWidgetItem(tagview)
            valueTag = metadata.get(tagname, "")
            firstitem.setFlags(firstitem.flags() ^ Qt.ItemIsEditable)
            stringItem = ""
            for valueItem in valueTag:
                stringItem += valueItem + ", "
            seconditem =  QTableWidgetItem(stringItem[:-2])
            self.tableWidget.setItem(rows, 0, firstitem)
            self.tableWidget.setItem(rows, 1, seconditem)
            rows += 1

        self.tableWidget.blockSignals(oldState)
        self.fetchImages()

    
    def fetchImages(self):
        self.listWidget.clear()
        self.bigAlbumArtLabel.clear()
        self.albumArtLabel.clear()
        cover = QPixmap()
        
        try:
            cover.loadFromData(Tagger.retrieveCoverImage(self.filePath))
            self.albumArtLabel.setPixmap(cover)
            self.bigAlbumArtLabel.setPixmap(cover)
            images = Tagger.retrieveAllImagesDetails(self.filePath)

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
        except TaggerError as e:
            self.bigAlbumArtLabel.setWordWrap(True);
            self.albumArtLabel.setWordWrap(True);
            self.bigAlbumArtLabel.setText("File contains unsupported or corrupted image data labeled as image tag! You can delete it with Delete All option below.")
            self.albumArtLabel.setText("Unsupported or corrupted image data!")
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)

    
    def initCtxListWidget(self):
        self.submenuAdd = self.ctxListWidget.addMenu("Add")
        self.actionAddImgByPath = self.submenuAdd.addAction("Path...")
        self.actionAddImgByUrl = self.submenuAdd.addAction("URL...")
        self.initAddImageByPath()
        self.initAddImageByUrl()
        self.actionAddImgByPath.triggered.connect(self.showAddImageByPath)
        self.actionAddImgByUrl.triggered.connect(self.showAddImageByUrl)

        self.submenuType = self.ctxListWidget.addMenu("Type")      
        for i in range(len(Tagger.imageTypes)):
            self.ctxListWidgetActions.insert(i, self.submenuType.addAction(Tagger.imageTypes[i]))
            self.ctxListWidgetActions[i].triggered.connect(self.ctxListWidgetMapper.map)
            self.ctxListWidgetMapper.setMapping(self.ctxListWidgetActions[i], i)

        self.ctxListWidgetMapper.mapped[int].connect(self.changeImageType)

        self.actionSetImgDesc = self.ctxListWidget.addAction("Description...")
        self.actionSetImgDesc.triggered.connect(self.editDesc)

        self.actionDelImg = self.ctxListWidget.addAction("Delete")
        self.actionDelImg.triggered.connect(self.deleteImage)
        
        self.actionDelAllImg = self.ctxListWidget.addAction("Delete All")
        self.actionDelAllImg.triggered.connect(self.deleteAllImages)


    def showCtxListWidget(self):
        self.submenuType.menuAction().setVisible(False)
        self.actionSetImgDesc.setVisible(False)
        self.actionDelImg.setVisible(False)

        if self.listWidget.selectedItems():
            self.submenuType.menuAction().setVisible(True)  
            
            if len(self.listWidget.selectedItems()) == 1:
                self.actionSetImgDesc.setVisible(True)

            self.actionDelImg.setVisible(True)

        if not self.filePath:
            self.submenuAdd.setEnabled(False)
            self.actionDelAllImg.setEnabled(False)
        else:
            self.submenuAdd.setEnabled(True)
            self.actionDelAllImg.setEnabled(True)
        
        cursor = QCursor()     
        self.ctxListWidget.exec_(cursor.pos())


    def initCtxTreeView(self):
        self.actionMakeDir = self.ctxTreeView.addAction("New Folder")
        self.actionMakeDir.triggered.connect(self.newFolder)
        self.actionOpenFile = self.ctxTreeView.addAction("Open")
        self.actionDetails = self.ctxTreeView.addAction("Details")
        self.actionRemoveFile = self.ctxTreeView.addAction("Delete")
        self.actionOpenFile.triggered.connect(self.openFiles)
        self.actionDetails.triggered.connect(self.getDetails)
        self.actionRemoveFile.triggered.connect(self.deleteFiles)


    def showCtxTreeView(self):
        self.actionOpenFile.setVisible(False)
        self.actionDetails.setVisible(False)
        self.actionRemoveFile.setVisible(False)
        self.actionMakeDir.setVisible(True)

        indexes = self.treeView.selectionModel().selectedIndexes()
        if indexes:
            self.actionMakeDir.setVisible(False)
            self.actionOpenFile.setVisible(True)
            self.actionDetails.setVisible(True)
            self.actionRemoveFile.setVisible(True)

        cursor = QCursor()     
        self.ctxTreeView.exec_(cursor.pos())

    
    def initCtxTreeViewHeader(self):
        for i in range(len(self.headerList)):
            self.ctxTreeViewHeaderActions.insert(i, self.ctxTreeViewHeader.addAction(self.headerList[i]))
            self.ctxTreeViewHeaderActions[i].setCheckable(True)
            self.ctxTreeViewHeaderActions[i].toggled.connect(self.ctxTreeViewHeaderMapper.map)
            self.ctxTreeViewHeaderMapper.setMapping(self.ctxTreeViewHeaderActions[i], i)

        self.ctxTreeViewHeaderMapper.mapped[int].connect(self.showColumns)
        self.ctxTreeViewHeaderActions[0].setVisible(False)


    def showCtxTreeViewHeader(self):
        cursor = QCursor()     
        self.ctxTreeViewHeader.exec_(cursor.pos())


    def bigImageChange(self):
        try:
            cover = QPixmap()
            hash = self.listWidget.selectedItems()[0].data(Qt.UserRole)
            cover.loadFromData(Tagger.retrieveSelectedImage(hash, self.filePath))
            self.bigAlbumArtLabel.setPixmap(cover)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)


    def editDesc(self):
        text, res = QInputDialog.getText(self, "Edit", "Description:")
        if res:
            item = self.listWidget.selectedItems()
            try:
                if not Tagger.checkImageUnique(text, self.filePath):
                    if not self.questionDialogYesNo("Overwrite Image", "Image with same description already exist. Do you want replace it?"):
                        return
                Tagger.changeImageDesc(text, item[0].data(Qt.UserRole), self.filePath)
            except TaggerError as e:
                QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                print(e.msg, e.src)
            self.fetchImages()


    def initAddImageByPath(self):
        self.imgPathDialog = QDialog()
        self.uiImgPathDialog = PathDialog()
        self.uiImgPathDialog.setupUi(self.imgPathDialog)
        for item in Tagger.imageTypes:
            self.uiImgPathDialog.imgTypeComboBox.addItem(item)

        self.uiImgPathDialog.openButton.clicked.connect(self.getImgPathDialog)
    
        
    def showAddImageByPath(self):
        self.uiImgPathDialog.pathLineEdit.clear()
        self.uiImgPathDialog.descLineEdit.clear()
        self.uiImgPathDialog.imgTypeComboBox.setCurrentText("Other")

        if self.imgPathDialog.exec() == QDialog.Accepted:
            path = self.uiImgPathDialog.pathLineEdit.text()
            if path == "":
                return
            desc = self.uiImgPathDialog.descLineEdit.text()
            type = Tagger.imageTypes.index(self.uiImgPathDialog.imgTypeComboBox.currentText())
            try:
                if not Tagger.checkImageUnique(desc, self.filePath):
                    if not self.questionDialogYesNo("Overwrite Image", "Image with same description already exist. Do you want replace it?"):
                        return
                Tagger.addImage("path", path, desc, type, self.filePath)
            except TaggerError as e:
                QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                print(e.msg, e.src)
            self.fetchImages()


    def getImgPathDialog(self):
        rootPath = QDir.rootPath()
        image = QFileDialog.getOpenFileName(self, "Select Images", rootPath, "Image Files (*.jpg *.png *.jpeg)")
        self.uiImgPathDialog.pathLineEdit.setText(image[0])


    def initAddImageByUrl(self):
        self.imgUrlDialog = QDialog()
        self.uiImgUrlDialog = UrlDialog()
        self.uiImgUrlDialog.setupUi(self.imgUrlDialog)
        for item in Tagger.imageTypes:
            self.uiImgUrlDialog.imgTypeComboBox.addItem(item)


    def showAddImageByUrl(self):
        self.uiImgUrlDialog.urlLineEdit.clear()
        self.uiImgUrlDialog.descLineEdit.clear()
        self.uiImgUrlDialog.imgTypeComboBox.setCurrentText("Other")

        if self.imgUrlDialog.exec() == QDialog.Accepted:
            url = self.uiImgUrlDialog.urlLineEdit.text()
            if url == "":
                return
            desc = self.uiImgUrlDialog.descLineEdit.text()
            type = Tagger.imageTypes.index(self.uiImgUrlDialog.imgTypeComboBox.currentText())
            try:
                if not Tagger.checkImageUnique(desc, self.filePath):
                    if not self.questionDialogYesNo("Overwrite Image", "Image with same description already exist. Do you want replace it?"):
                        return
                Tagger.addImage("url", url, desc, type, self.filePath)
            except TaggerError as e:
                QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                print(e.msg, e.src)
            self.fetchImages()


    def changeImageType(self, type):
        try:
            for item in self.listWidget.selectedItems():
                Tagger.changeImageType(type, item.data(Qt.UserRole), self.filePath)
        except TaggerError as e:
            print(e.msg, e.src)
        self.fetchImages()


    def deleteImage(self):
        try:
            for item in self.listWidget.selectedItems():
                Tagger.deleteImages(item.data(Qt.UserRole), self.filePath)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)
        self.fetchImages()


    def deleteAllImages(self):
        try:
            Tagger.deleteImages("APIC", self.filePath)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)
        self.fetchImages()


    def questionDialogYesNo(self, name, question):
        msgBox = QMessageBox(QMessageBox.Question, name, question)
        msgBox.addButton(QMessageBox.Yes)
        msgBox.addButton(QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        reply = msgBox.exec()
        if reply == QMessageBox.Yes:
            return True
        else:
            return False


    def pageUpImage(self, event):
        self.verticalStackedWidget.setCurrentIndex(1)


    def pageDownImage(self, event):
        self.verticalStackedWidget.setCurrentIndex(0)


    def editTag(self, item):
        tagview = self.tableWidget.item(item.row(), 0).text()
        try:
            Tagger.editTag(Tagger.id3Keys[tagview], item.text(), self.filePath)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)


    def openFiles(self):
        for item in self.treeView.selectedIndexes():
            if item.column() == 0:  
                path = self.fileModel.filePath(item)
                os.startfile(path)


    def getDetails(self): 
        pass


    def deleteFiles(self):
        for item in self.treeView.selectedIndexes():
            if item.column() == 0:
                if self.fileModel.isDir(item):
                    if not self.fileModel.rmdir(item):
                        if self.questionDialogYesNo("Delete Folder", "This folder contains files, are you sure to delete it?"):
                            dirToRemove = QDir(self.fileModel.filePath(item))
                            dirToRemove.removeRecursively()
                else:
                    self.fileModel.remove(item)


    def newFolder(self):
        text, res = QInputDialog.getText(self, "Create Folder", "Name:")
        if res and text:
            path = self.fileModel.filePath(self.treeView.rootIndex())
            subDirs = [o for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]
            if text in subDirs:
                QMessageBox.warning(self, "Warning", "Folder already exists!", QMessageBox.Ok)
            else:
                self.fileModel.mkdir(self.treeView.rootIndex(), text)

    
    def setRootDirectory(self):
        self.changeWorkDirectory(self.fileModel.filePath(self.treeView.selectedIndexes()[0]))


    def levelUp(self):
        self.changeWorkDirectory(self.fileModel.filePath(self.treeView.rootIndex().parent()))


    def refreshFileModel(self):
        self.changeWorkDirectory(self.fileModel.filePath(self.treeView.rootIndex()))


    def enableActions(self):
        self.actionDelete.setEnabled(False)
        self.actionSetRootDir.setEnabled(False)
        self.actionTagToFile.setEnabled(False)
        self.actionFileToTag.setEnabled(False)
        self.actionDeleteTag.setEnabled(False)
        
        indexes = self.treeView.selectionModel().selectedIndexes()
        indexesCount = len(indexes)
        if indexesCount > 0:
            self.actionDelete.setEnabled(True)

            if all(not self.fileModel.isDir(item) for item in indexes):
                self.actionTagToFile.setEnabled(True)
                self.actionFileToTag.setEnabled(True)
                self.actionDeleteTag.setEnabled(True)
        
        if len(indexes) == self.fileModel.columnCount() and self.fileModel.isDir(indexes[0]):
            self.actionSetRootDir.setEnabled(True)           


    def showColumns(self, pos):
        if self.ctxTreeViewHeaderActions[pos].isChecked():
            self.treeView.showColumn(pos)
        else:
            self.treeView.hideColumn(pos)


    def tagToFileName(self):
        print("TtF")
        self.tagFileDialog = QDialog()
        self.uiTagFileDialog = TagFileDialog()
        self.uiTagFileDialog.setupUi(self.tagFileDialog)

        tagKeys = list(Tagger.id3Keys.keys())
        for i in range(11):
            self.uiTagFileDialog.tagListComboBox.addItem(tagKeys[i])

        self.uiTagFileDialog.previewButton.clicked.connect(self.chooseTagProp)
        self.tagFileDialog.exec()

        
    def chooseTagProp(self):
        print(Tagger.id3Keys[self.uiTagFileDialog.tagListComboBox.currentText()])
   
        
    def fileToTagName(self):
        print("FtT")


    def deleteTag(self):
        print("del tag")