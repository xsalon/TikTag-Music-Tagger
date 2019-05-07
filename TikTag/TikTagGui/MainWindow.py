from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from TikTagGui.MyFileSystemModel import MyFileSystemModel
from TikTagGui.Ui_MainWindow import Ui_MainWindow
from TikTagGui.Ui_urlDialog import Ui_Dialog as UrlDialog
from TikTagGui.Ui_pathDialog import Ui_Dialog as PathDialog
from TikTagGui.Ui_tagFileDialog import Ui_Dialog as TagFileDialog
from TikTagGui.Ui_settingsDialog import Ui_Dialog as SettingsDialog
from TikTagServices.OnlineServices import OnlineServices
from TikTagCtrl.Tagger import Tagger
from TikTagCtrl.TaggerError import *
from TikTagServices.ServiceError import *
import webbrowser
import shutil
import enum
import sys
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.settings = QSettings("FIT VUT", "TikTag");
        self.filePath = None
        self.supportedFormats = Tagger.fileFormats
        self.generalInfo = {}
        self.metadata = {}
        self.metadataCache = []
        self.indexCache = 0
        self.errFound = False
        
        self.initSettings()
        self.onlineTagger = None

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
        self.actionRename = QAction()
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
        self.actionTagToFile.triggered.connect(self.showTagToFileName)
        self.actionFileToTag.triggered.connect(self.showFileToTagName)
        self.actionDeleteTag.triggered.connect(self.deleteTag)
        self.actionFolderByTag.triggered.connect(self.showFolderByTagName)
        self.actionRevertFile.triggered.connect(self.revertFile)
        self.actionSettings.triggered.connect(self.showSettings)
        self.actionGetOnlineTags.triggered.connect(self.getOnlineTags)
        
        self.actionLevelUp.setEnabled(False)
        self.actionCreateFolder.setEnabled(False)
        self.actionRefresh.setEnabled(False)
        self.disableFileActions()

        self.albumArtLabel.mousePressEvent = self.pageUpImage
        self.bigAlbumArtLabel.mousePressEvent = self.pageDownImage

        self.treeView.clicked.connect(self.fetchTags) 
        self.treeView.clicked.connect(self.fetchImages)

        self.listWidget.customContextMenuRequested.connect(self.showCtxListWidget)
        self.listWidget.itemClicked.connect(self.bigImageChange)

        self.tableWidget.itemChanged.connect(self.editTag)

        if self.settings.value("MainWindow/lastDirPath"):
            self.initWorkDirectory(self.settings.value("MainWindow/lastDirPath"))

  
    def selectFolderDialog(self):
        rootPath = QDir.rootPath()
        folder = str(QFileDialog.getExistingDirectory(None, "Select Directory", rootPath))
        
        if folder:
            if not self.treeView.model():
                self.initWorkDirectory(folder)
            else:
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
        self.initTagToFileName()
        self.initFileToTagName()
        self.initFolderByTagName()
        self.treeView.customContextMenuRequested.connect(self.showCtxTreeView)
        self.treeView.header().customContextMenuRequested.connect(self.showCtxTreeViewHeader)
        self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents);
        #self.treeView.header().setSectionResizeMode(0, QHeaderView.Stretch);
        #self.treeView.header().setSectionResizeMode(1, QHeaderView.ResizeToContents);

        self.treeView.selectionModel().selectionChanged.connect(self.enableFileActions)
        self.fileModel.fileRenamed.connect(self.fileRenameCache)
        self.actionCreateFolder.setEnabled(True)
        self.actionLevelUp.setEnabled(True)
        self.actionRefresh.setEnabled(True)
        
        for i in range(self.fileModel.columnCount()):
            self.treeView.hideColumn(i)
        self.treeView.showColumn(0)

        self.settings.setValue("MainWindow/lastDirPath", folder)


    def changeWorkDirectory(self, folder):
        self.fileModel.setRootPath(folder)
        self.treeView.setRootIndex(self.fileModel.index(folder))
        self.settings.setValue("MainWindow/lastDirPath", folder)

    
    def fetchTags(self):
        self.labelDuration.setText("Duration: ")
        self.labelSampleRate.setText("Sample Rate: ")
        self.labelChannels.setText("Channels: ")
        self.labelBitrate.setText("Bitrate: ") 
        self.labelCodec.setText("Codec: ")

        path = self.fileModel.filePath(self.treeView.currentIndex())
        
        if os.path.isdir(path):
            return
        
        self.filePath = path
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        headerTabLabels = ["Name", "Value"]

        try:
            self.generalInfo = Tagger.fetchGeneralInfo(path)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)
            self.errFound = True
            return

        self.labelDuration.setText("Duration: " + self.generalInfo["Duration"])
        self.labelSampleRate.setText("Sample Rate: " + self.generalInfo["Sample Rate"])
        self.labelChannels.setText("Channels: " + self.generalInfo["Channels"])
        self.labelBitrate.setText("Bitrate: " + self.generalInfo["Bitrate"]) 
        self.labelCodec.setText("Codec: " + self.generalInfo["Codec"])
        
        try:
            self.metadata = Tagger.fetchTags(path)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)

        item = next((item for item in self.metadataCache if path in item.keys()), False)
        if not item:
            newDict = {}
            newDict[path] = self.metadata
            self.metadataCache.insert(self.indexCache, newDict)
            if self.indexCache == 100:
                self.indexCache = 0
            else:
                self.indexCache += 1

        oldState = self.tableWidget.blockSignals(True)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(headerTabLabels)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        rows = 0;

        for tagview, tagname in Tagger.getKeys(self.filePath).items():
            self.tableWidget.insertRow(rows)
            firstitem =  QTableWidgetItem(tagview)
            valueTag = self.metadata.get(tagname, "")
            firstitem.setFlags(firstitem.flags() ^ Qt.ItemIsEditable)
            stringItem = ""
            for valueItem in valueTag:
                stringItem += valueItem + ", "
            seconditem =  QTableWidgetItem(stringItem[:-2])
            self.tableWidget.setItem(rows, 0, firstitem)
            self.tableWidget.setItem(rows, 1, seconditem)
            rows += 1

        self.tableWidget.blockSignals(oldState)

    
    def fetchImages(self):
        self.listWidget.clear()
        self.bigAlbumArtLabel.clear()
        self.albumArtLabel.clear()
        cover = QPixmap()
        
        if self.errFound:
            self.errFound = False
            return

        try:
            cover.loadFromData(Tagger.retrieveCoverImage(self.filePath))
            self.albumArtLabel.setPixmap(cover)
            self.bigAlbumArtLabel.setPixmap(cover)
            images = Tagger.retrieveAllImagesDetails(self.filePath)

            for image in images:
                item = QListWidgetItem()
                item.setText(image.infoString)
                if hasattr(image.tag, 'HashKey'):
                    item.setData(Qt.UserRole, image.tag.HashKey)
                else:
                    item.setData(Qt.UserRole, None)
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
            QMessageBox.warning(self, "Error", e.msg, QMessageBox.Ok)
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
        self.actionRename = self.ctxTreeView.addAction("Rename")
        self.actionDetails = self.ctxTreeView.addAction("Details")
        self.actionRemoveFile = self.ctxTreeView.addAction("Delete")
        self.actionOpenFile.triggered.connect(self.openFiles)
        self.actionDetails.triggered.connect(self.getDetails)
        self.actionRename.triggered.connect(self.renameItem)
        self.actionRemoveFile.triggered.connect(self.deleteFiles)


    def showCtxTreeView(self):
        self.actionOpenFile.setVisible(False)
        self.actionDetails.setVisible(False)
        self.actionRemoveFile.setVisible(False)
        self.actionRename.setVisible(False)
        self.actionMakeDir.setVisible(True)

        indexes = self.treeView.selectionModel().selectedIndexes()
        if indexes:
            self.actionMakeDir.setVisible(False)
            self.actionOpenFile.setVisible(True)
            self.actionDetails.setVisible(True)
            self.actionRemoveFile.setVisible(True)

        if len(indexes) == self.fileModel.columnCount():
            self.actionRename.setVisible(True)

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


    def fileRenameCache(self, path, oldName, newName):
        oldKey = path + '/' + oldName
        newKey = path + '/' + newName
        item = next((item for item in self.metadataCache if oldKey in item.keys()), False)
        if item:
            item[newKey] = item.pop(oldKey)


    def renameItem(self):
        self.treeView.edit(self.fileModel.index(self.filePath))


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
                Tagger.deleteImage(item.data(Qt.UserRole), self.filePath)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)
        self.fetchImages()


    def deleteAllImages(self):
        try:
            Tagger.deleteAllImages(self.filePath)
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
            Tagger.editTag(tagview, item.text(), self.filePath)
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


    def disableFileActions(self):
        self.actionDelete.setEnabled(False)
        self.actionSetRootDir.setEnabled(False)
        self.actionTagToFile.setEnabled(False)
        self.actionFileToTag.setEnabled(False)
        self.actionDeleteTag.setEnabled(False)
        self.actionFolderByTag.setEnabled(False)
        self.actionRevertFile.setEnabled(False)
        self.actionGetOnlineTags.setEnabled(False)

    def enableFileActions(self):
        self.disableFileActions()
        indexes = self.treeView.selectionModel().selectedIndexes()
        indexesCount = len(indexes)
        if indexesCount > 0:
            self.actionDelete.setEnabled(True)

            if all(not self.fileModel.isDir(item) for item in indexes):
                self.actionTagToFile.setEnabled(True)
                self.actionFileToTag.setEnabled(True)
                self.actionDeleteTag.setEnabled(True)
                self.actionFolderByTag.setEnabled(True)
                self.actionRevertFile.setEnabled(True)
                self.actionGetOnlineTags.setEnabled(True)
        
        if len(indexes) == self.fileModel.columnCount() and self.fileModel.isDir(indexes[0]):
            self.actionSetRootDir.setEnabled(True)           


    def showColumns(self, pos):
        if self.ctxTreeViewHeaderActions[pos].isChecked():
            self.treeView.showColumn(pos)
        else:
            self.treeView.hideColumn(pos)


    def deleteTag(self):
        for item in self.treeView.selectedIndexes():
                if item.column() == 0:
                       path = self.fileModel.filePath(item)
                       try:
                            Tagger.deleteTag(path)
                       except TaggerError as e:
                            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                            print(e.msg, e.src)
        self.fetchTags()
        self.fetchImages()


    def revertFile(self):
        for item in self.treeView.selectedIndexes():
                if item.column() == 0:
                       path = self.fileModel.filePath(item)
                       metaItem = next((metaItem for metaItem in self.metadataCache if path in metaItem.keys()), False)
                       if metaItem:
                           try:
                                metadata = Tagger.fetchTags(path)
                                print(str(metadata))
                                print(str(metaItem))
                                for key, value in metadata.items():
                                    if not key in metaItem[path]:
                                        Tagger.putTag(key, "", path)
                                for key, value in metaItem[path].items():
                                    if metaItem[path][key]:
                                        Tagger.putTag(key, value, path)

                           except TaggerError as e:
                               QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                               print(e.msg, e.src)
        self.fetchTags()


    #---------------------------------TAG TO FILE--------------------------------------------------
                 
    def initTagToFileName(self):
        self.tagFileDialog = QDialog()
        self.uiTagFileDialog = TagFileDialog()
        self.uiTagFileDialog.setupUi(self.tagFileDialog)

        for key in Tagger.generalKeys:
            self.uiTagFileDialog.tagListComboBox.addItem(key)

        self.uiTagFileDialog.addTagButton.clicked.connect(self.chooseTagFileProp)
        self.uiTagFileDialog.formatStringLineEdit.textChanged.connect(self.previewTagToFile)

   
    def showTagToFileName(self):
        self.uiTagFileDialog.formatStringPreview.clear()   
        self.previewTagToFile()
        if self.tagFileDialog.exec() == QDialog.Accepted:
            for item in self.treeView.selectedIndexes():
                 if item.column() == 0:
                        path = self.fileModel.filePath(item)
                        if not QFile.rename(path, os.path.join(os.path.dirname(path), self.procTagToFileName(path))):
                            QMessageBox.warning(self, "Warning", "File with same name already exists!", QMessageBox.Ok)
            
   
    def procTagToFileName(self, path):
        filename = os.path.basename(path)
        name, extension = os.path.splitext(filename)
        formatString = self.uiTagFileDialog.formatStringLineEdit.text()
        if formatString == "":
            return
        finalString = ""

        try:
            metadata = Tagger.fetchTags(path)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)

        buffer = ""
        buffering = False
        for char in formatString:
            if char == '#' and not buffering:
                buffering = True
            elif char == '#' and buffering:
                buffering = False
                if buffer in metadata:
                    for item in metadata[buffer]:
                        finalString += item
                        finalString += ', '
                    finalString = finalString[:-2]
                buffer = ""
            elif buffering:
                buffer += char
            elif not buffering:
                finalString += char
        return finalString + extension


    def previewTagToFile(self):
        self.uiTagFileDialog.formatStringPreview.setText(self.procTagToFileName(self.filePath))


    def chooseTagFileProp(self):
        temp = self.uiTagFileDialog.formatStringLineEdit.text()
        temp += ('#' + Tagger.getKeys(self.filePath)[self.uiTagFileDialog.tagListComboBox.currentText()] + '#')
        self.uiTagFileDialog.formatStringLineEdit.setText(temp)

    #---------------------------------FILE TO TAG--------------------------------------------------

    def initFileToTagName(self):
        self.fileTagDialog = QDialog()
        self.uiFileTagDialog = TagFileDialog()
        self.uiFileTagDialog.setupUi(self.fileTagDialog)
        self.fileTagDialog.setWindowTitle("File - Tag")
        self.uiFileTagDialog.formatStringPreview.setWordWrap(True)

        for key in Tagger.generalKeys:
            self.uiFileTagDialog.tagListComboBox.addItem(key)

        self.uiFileTagDialog.addTagButton.clicked.connect(self.chooseFileTagProp)
        self.uiFileTagDialog.formatStringLineEdit.textChanged.connect(self.previewFileToTag)


    def procFileToTagName(self, path):   
        filename = os.path.basename(path)
        name, extension = os.path.splitext(filename)
        formatString = self.uiFileTagDialog.formatStringLineEdit.text()
        finalDict = {}
        if formatString == "":
            return finalDict

        bufferKey = ""
        bufferSep = ""
        bufferList = []
        buffering = False
        for char in formatString:
            if char == '#' and not buffering:
                buffering = True
                if bufferSep:
                    bufferList.append(bufferSep)
                bufferSep = ""
            elif char == '#' and buffering:
                buffering = False
                if bufferKey:
                    bufferList.append('#' + bufferKey)
                bufferKey = ""
            elif buffering:
                bufferKey += char
            elif not buffering:
                bufferSep += char

        if bufferSep:
            bufferList.append(bufferSep)

        key = ""
        for i in range(len(bufferList)):
            listWord = bufferList[i]
            if listWord[0] == '#':
                key = listWord[1:]
                if i == len(bufferList)-1:
                    if key in finalDict:
                        finalDict[key].append(name)
                    else:
                        finalDict[key] = [name]
            else:
                splitted = name.split(listWord, 1)
                value = splitted[0]
                
                if len(splitted) > 1:
                    name = splitted[1]

                if key and value:
                    if key in finalDict:
                        finalDict[key].append(value)
                    else:
                        finalDict[key] = [value]

        return finalDict
                
    
    def showFileToTagName(self):
        self.uiFileTagDialog.formatStringPreview.clear()
        self.previewFileToTag()
        if self.fileTagDialog.exec() == QDialog.Accepted:
            for item in self.treeView.selectedIndexes():
                     if item.column() == 0:
                            path = self.fileModel.filePath(item)
                            for key, value in self.procFileToTagName(path).items():
                                try:
                                    Tagger.putTag(key, value, path)
                                except TaggerError as e:
                                    QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                                    print(e.msg, e.src)
            self.fetchTags()
            self.fetchImages()

        
    def previewFileToTag(self):
        previewString = ""
        for key, value in self.procFileToTagName(self.filePath).items():
            previewString += key + " = " + ",".join(value) + "\n"
        self.uiFileTagDialog.formatStringPreview.setText(previewString)

              
    def chooseFileTagProp(self):
        temp = self.uiFileTagDialog.formatStringLineEdit.text()
        temp += ('#' + Tagger.getKeys(self.filePath)[self.uiFileTagDialog.tagListComboBox.currentText()] + '#')
        self.uiFileTagDialog.formatStringLineEdit.setText(temp)

    #---------------------------------FOLDER BY TAG--------------------------------------------------

    def initFolderByTagName(self):
        self.folderByTagDialog = QDialog()
        self.uiFolderByTagDialog = TagFileDialog()
        self.uiFolderByTagDialog.setupUi(self.folderByTagDialog)
        self.folderByTagDialog.setWindowTitle("Tag - Folder")
        self.uiFolderByTagDialog.checkBoxRemove = QCheckBox(self.uiFolderByTagDialog.formatGroupBox)
        self.uiFolderByTagDialog.checkBoxRemove.setObjectName("checkBoxRemove")
        self.uiFolderByTagDialog.gridLayout_2.addWidget(self.uiFolderByTagDialog.checkBoxRemove, 4, 0, 1, 1)
        self.uiFolderByTagDialog.gridLayout.addWidget(self.uiFolderByTagDialog.formatGroupBox, 0, 0, 1, 1)
        _translate = QCoreApplication.translate
        self.uiFolderByTagDialog.checkBoxRemove.setText(_translate("Dialog", "Remove original files"))

        for key in Tagger.generalKeys:
            self.uiFolderByTagDialog.tagListComboBox.addItem(key)

        self.uiFolderByTagDialog.addTagButton.clicked.connect(self.chooseFolderByTagProp)
        self.uiFolderByTagDialog.formatStringLineEdit.textChanged.connect(self.previewFolderByTag)


    def procFolderByTagName(self, path):  
        formatString = self.uiFolderByTagDialog.formatStringLineEdit.text()
        if formatString == "":
            return
        finalString = ""

        try:
            metadata = Tagger.fetchTags(path)
        except TaggerError as e:
            QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
            print(e.msg, e.src)

        buffer = ""
        buffering = False
        for char in formatString:
            if char == '#' and not buffering:
                buffering = True
            elif char == '#' and buffering:
                buffering = False
                if buffer in metadata:
                    for item in metadata[buffer]:
                        finalString += item
                        finalString += ', '
                    finalString = finalString[:-2]
                buffer = ""
            elif buffering:
                buffer += char
            elif not buffering:
                finalString += char
        return finalString
                
    
    def showFolderByTagName(self):
        if self.folderByTagDialog.exec() == QDialog.Accepted:
            for item in self.treeView.selectedIndexes():
                if item.column() == 0:
                       path = self.fileModel.filePath(item)
                       dirPath = self.fileModel.filePath(self.treeView.rootIndex())
                       fileName = os.path.basename(path)
                       subDirs = [o for o in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath,o))]
                       dirName = self.procFolderByTagName(path)
                       if dirName not in subDirs:
                           self.fileModel.mkdir(self.treeView.rootIndex(), dirName)

                       if QFile.copy(path, os.path.join(dirPath, dirName, fileName)):
                           if self.uiFolderByTagDialog.checkBoxRemove.isChecked():
                               if not QFile.remove(path):
                                   QMessageBox.critical(self, "Error", "Cannot delete selected file!", QMessageBox.Ok)
                                   print(e.msg, e.src)
                       else:
                           QMessageBox.critical(self, "Error", "Cannot copy selected file!", QMessageBox.Ok)
                           print(e.msg, e.src)

        
    def previewFolderByTag(self):
        self.uiFolderByTagDialog.formatStringPreview.setText(self.procFolderByTagName(self.filePath))

              
    def chooseFolderByTagProp(self):
        temp = self.uiFolderByTagDialog.formatStringLineEdit.text()
        temp += ('#' + Tagger.getKeys(self.filePath)[self.uiFolderByTagDialog.tagListComboBox.currentText()] + '#')
        self.uiFolderByTagDialog.formatStringLineEdit.setText(temp)


    #--------------------------------- SETTINGS --------------------------------------------------    
    
    def initSettings(self):
        self.settingsDialog = QDialog()
        self.uiSettingsDialog = SettingsDialog()
        self.uiSettingsDialog.setupUi(self.settingsDialog)

        self.uiSettingsDialog.listWidget.itemClicked.connect(lambda item: item.setCheckState(Qt.Checked if item.checkState()==Qt.Unchecked else Qt.Unchecked))

        if not self.settings.value("Settings/Online/ServicesList"):
            self.settings.setValue("Settings/Online/ServicesList", OnlineServices.SERVICES)

        if not self.settings.value("Settings/Online/Mode"):
            self.settings.setValue("Settings/Online/Mode", "Complete")

        for service in self.settings.value("Settings/Online/ServicesList"):
            if not self.settings.value("Settings/Online/" + service):  
                self.settings.setValue("Settings/Online/" + service, 2)



    def showSettings(self):
        if self.settings.value("Settings/Online/Mode") == "Complete":
            self.uiSettingsDialog.radioButtonComplete.setChecked(True)
            self.settings.setValue("Settings/Online/Mode", "Complete")
        else:
            self.uiSettingsDialog.radioButtonOverwrite.setChecked(True)
            self.settings.setValue("Settings/Online/Mode", "Overwrite")
   
        self.uiSettingsDialog.listWidget.clear()
        for service in self.settings.value("Settings/Online/ServicesList"):
                newService = QListWidgetItem()
                newService.setText(service)
                newService.setIcon(QIcon(":/icons/" + service.lower() + ".png"))
                newService.setFlags(newService.flags() ^ Qt.ItemIsUserCheckable)
                if self.settings.value("Settings/Online/" + service) == 2:
                    newService.setCheckState(Qt.Checked);
                else:
                    newService.setCheckState(Qt.Unchecked);
                self.uiSettingsDialog.listWidget.addItem(newService)
    
        if self.settingsDialog.exec() == QDialog.Accepted:
            self.settings.setValue("Settings/Online/ServicesList", [self.uiSettingsDialog.listWidget.item(i).text() for i in range(self.uiSettingsDialog.listWidget.count())])
            for i in range(self.uiSettingsDialog.listWidget.count()):
                if self.uiSettingsDialog.listWidget.item(i).checkState() == Qt.Checked:
                    self.settings.setValue("Settings/Online/" + self.uiSettingsDialog.listWidget.item(i).text(), 2)
                else:
                    self.settings.setValue("Settings/Online/" + self.uiSettingsDialog.listWidget.item(i).text(), 1)
        
            if self.uiSettingsDialog.radioButtonComplete.isChecked():
                self.settings.setValue("Settings/Online/Mode", "Complete")
            else:
                self.settings.setValue("Settings/Online/Mode", "Overwrite")

           
    #---------------------------------GET ONLINE TAGS--------------------------------------------------
    
    def getServicesOrder(self):
         return [self.settings.value("Settings/Online/ServicesList")[i] for i in range(len(self.settings.value("Settings/Online/ServicesList"))) 
                    if self.settings.value("Settings/Online/" + self.settings.value("Settings/Online/ServicesList")[i]) == 2]


    def initOnlineServices(self):
         try:
             self.onlineTagger.initServices(self.getServicesOrder())
         except ServiceRequirement as r:
             webbrowser.open(r.url)
             code, res = QInputDialog.getText(self, "Authorization", "Code:")
             if res:
                 try:
                     self.onlineTagger.initServices(self.getServicesOrder(), code)
                 except ServiceError as e:
                     QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                     print(e.msg)
    
    
    def getOnlineTags(self):
        tasksCount = len([item for item in self.treeView.selectedIndexes() if item.column() == 0])
        progressDialog = QProgressDialog("Downloading...", "Cancel", 0, tasksCount, self)
        progressDialog.setModal(True)
        progressDialog.setWindowTitle("Get Tags")

        if not self.onlineTagger:            
            self.onlineTagger = OnlineServices(self.getServicesOrder())
            self.initOnlineServices()
        elif not set(self.onlineTagger.services) == set(self.getServicesOrder()):
            self.onlineTagger.services = self.getServicesOrder()
            self.initOnlineServices()
        elif not self.onlineTagger.servicesStatus():
            self.onlineTagger.services = self.getServicesOrder()
            self.initOnlineServices()
        
        if self.onlineTagger:
            for i, item in enumerate(self.treeView.selectedIndexes()):
               if item.column() == 0:
                   progressDialog.setValue(i)

                   if progressDialog.wasCanceled():
                       break;

                   path = self.fileModel.filePath(item)
                   try:
                       metadata = Tagger.fetchTags(path)
                       result = self.onlineTagger.getTags(metadata)
                   except TaggerError as e:
                       QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                       print(e.msg, e.src)
                   except ServiceError as e:
                       QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                       print(e.msg)

                   if self.settings.value("Settings/Online/Mode") == "Complete":
                       for key, value in result.items():
                           if not key in metadata or not metadata[key]:
                               if not value == None:
                                    try:
                                        Tagger.putTag(key, value, path)
                                    except TaggerError as e:
                                        QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                                        print(e.msg, e.src)
                   else:
                       for key, value in result.items():
                          if not value == None:
                                try:
                                    Tagger.putTag(key, value, path)
                                except TaggerError as e:
                                    QMessageBox.critical(self, "Error", e.msg, QMessageBox.Ok)
                                    print(e.msg, e.src)
            self.fetchTags()
            progressDialog.setValue(tasksCount)