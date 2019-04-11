import mutagen
import taglib
import os.path
from TikTagCtrl.MP3tag import MP3tag

class Tagger(object):
    fileFormats = ["mp3", "flac", "m4a"]

    @classmethod
    def openFile(cls, path):
        fileExtension = os.path.splitext(path)[1][1:].strip().lower()
        if fileExtension not in cls.fileFormats:
            return None

        if fileExtension == "mp3":
            file = MP3tag(path)

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
    def retrieveImages(cls, path):
        file = cls.openFile(path)
        if file:
            return file.retrieveImages()
        else:
            #try catch osetrenia
            return ""

        
    @staticmethod
    def checkStatus(path):
        pass


