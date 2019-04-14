import mutagen
import taglib
import os.path
from TikTagCtrl.MP3tag import MP3tag

class Tagger(object):
    fileFormats = ["mp3", "flac", "m4a"]
    imageTypes = ["Other", "File Icon", "Other File Icon", "Front Cover", "Back Cover", "Leaflet Page", "Media", 
                  "Lead Artist", "Artist/Performer", "Conductor", "Band", "Composer", "Lyricist/Text Writer", "Recording Location", "During Recording",
                  "During Performance", "Screen Capture", "Fish", "Illustration", "Band/Artist Logo", "Publisher/Studio Logo"]

    @classmethod
    def openFile(cls, path):
        fileExtension = os.path.splitext(path)[1][1:].strip().lower()
        if fileExtension not in cls.fileFormats:
            return None

        if fileExtension == "mp3":
            file = MP3tag(path)
        else:
            return None

        return file
        
    @classmethod
    def fetchTags(cls, path):
        file = cls.openFile(path)
        if file:
            return file.metadata()
        else:
            #try catch osetrenia
            return ""

    @classmethod
    def fetchGeneralInfo(cls, path):
        file = cls.openFile(path)
        if file:
            return file.generalInfo()
        else:
            #try catch osetrenia
            return ""
    
    @classmethod
    def retrieveImage(cls, path):
        file = cls.openFile(path)
        data = None #co ak nema album art
        if file:
            for item in file.retrieveImages():
                if item.type == "COVER_FRONT":
                    return item.tag.data
                else:
                    data = item.tag.data
            if data:
                return data
        else:
            #try catch osetrenia
            return "" 
        
    @classmethod
    def retrieveAllImagesDetails(cls, path):
        file = cls.openFile(path)
        if file:
            return file.retrieveImages()
        else:
            #try catch osetrenia
            return ""

    @classmethod
    def addImage(cls, mode, src, desc, type, path):
        file = cls.openFile(path)
        if file:    
            if mode == "path":
                file.addLocalImage(src, desc, type)
            elif mode == "url":
                file.addOnlineImage(src, desc, type)
            else:
                return ""
        else:
            return ""

    @classmethod
    def changeImageType(cls, type, hash, path):
        file = cls.openFile(path)
        if file:
            file.changeImageType(type, hash)
        else:
            return ""

    @classmethod
    def deleteImages(cls, hash, path):
        file = cls.openFile(path)
        if file:
            file.deleteImages(hash)
        else:
            return ""
        
    @staticmethod
    def checkStatus(path):
        pass


