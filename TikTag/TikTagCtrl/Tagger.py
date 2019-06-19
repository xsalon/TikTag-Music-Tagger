# File: Tagger.py
# Project: TikTag
# Author: Marek Salon (xsalon00)
# Contact: xsalon00@stud.fit.vutbr.cz
# Date: 10.5.2019
# Description: Interface for TikTagCtrl module

import mutagen
import os.path
import requests
import imghdr
from mutagen import MutagenError
from TikTagCtrl.MP3tag import MP3tag
from TikTagCtrl.FLACtag import FLACtag
from TikTagCtrl.TaggerError import *

class Tagger(object):
    """Static methods for metadata manipulations"""
    FILEFORMATS = ["mp3", "flac"]
    IMAGEFORMATS = ["jpg", "png", "jpeg", "jfif"]
   
    IMAGETYPES = ["Other", "File Icon", "Other File Icon", "Front Cover", "Back Cover", "Leaflet Page", "Media", 
                  "Lead Artist", "Artist/Performer", "Conductor", "Band", "Composer", "Lyricist/Text Writer", "Recording Location", "During Recording",
                  "During Performance", "Screen Capture", "Fish", "Illustration", "Band/Artist Logo", "Publisher/Studio Logo"]

    GENERALKEYS = [
               'Title',
               'Artist',
               'Album',
               'Album Artist', 
               'Date',
               'Original Date', 
               'Genre',
               'Track Number', 
               'Disc Number',
               'Catalog Number',
               'BPM',
               'Initial Key',
               'ISRC',
               'Composer', 
               'Lyricist', 
               'Length'
                ]


    @classmethod
    def openFile(cls, path):
        fileExtension = os.path.splitext(path)[1][1:].strip().lower()
        if fileExtension not in Tagger.FILEFORMATS:
           raise TaggerError("File not supported!", path)
        try:
           if fileExtension == "mp3":
                file = MP3tag(path)
           elif fileExtension == "flac":
                file = FLACtag(path)
        except MutagenError as e:
            raise TaggerError("Cannot open file because " + str(e), path)
        return file


    @classmethod
    def getKeys(cls, path):
        file = cls.openFile(path)
        return file.TAGKEYS


    @classmethod
    def getOnlyLength(cls, path):
        file = cls.openFile(path)
        return file.getLength()

        
    @classmethod
    def fetchTags(cls, path):
        file = cls.openFile(path)
        return file.metadata()


    @classmethod
    def fetchGeneralInfo(cls, path):
        file = cls.openFile(path)
        return file.generalInfo()


    @classmethod
    def editTag(cls, name, value, path):
        try:
            file = cls.openFile(path)
            file.editTag(name, value)
        except MutagenError:
            raise TaggerError("Tag in file cannot be edited!", path)


    @classmethod
    def putTag(cls, name, value, path):
        try:
            file = cls.openFile(path)
            file.putTag(name, value)
        except MutagenError:
            raise TaggerError("Tag in file cannot be changed!", path)
 
    
    @classmethod
    def retrieveCoverImage(cls, path):
        file = cls.openFile(path)
        data = None

        try:
            for item in file.retrieveImages():
                if item.type == "COVER_FRONT":
                    return item.tag.data
                else:
                    data = item.tag.data
        except ModuleTaggerError as e:
            raise TaggerError(e.msg, e.src)

        if data:
            return data



    @classmethod
    def retrieveSelectedImage(cls, hash, path):
        file = cls.openFile(path)
        try:
            for item in file.retrieveImages():
                if item.tag.HashKey == hash:
                    return item.tag.data
        except ModuleTaggerError as e:
            raise TaggerError(e.msg, e.src)

        
    @classmethod
    def retrieveAllImagesDetails(cls, path):
        file = cls.openFile(path)
        try:
            return file.retrieveImages()
        except ModuleTaggerError as e:
            raise TaggerError(e.msg, e.src)


    @classmethod
    def addImage(cls, mode, src, desc, type, path):
        file = cls.openFile(path)
        if mode == "path":
            try:
                data = open(src, 'rb').read()
                format = imghdr.what("image", data)
                if not format or format not in cls.IMAGEFORMATS:
                    raise TaggerError("Unsupported image file format!", format)
                else:
                    file.addImage(desc, type, data, format)
            except IOError:
                raise TaggerError("Cannot open image file!", src)
            except ModuleTaggerError as e:
                raise TaggerError(e.msg, path)
        
        elif mode == "url":
            try:
                response = requests.get(src)
                data = response.content
                format = imghdr.what("image", data)
                if not format or format not in cls.IMAGEFORMATS:
                    raise TaggerError("Unsupported image file format!", format)
                else:
                    file.addImage(desc, type, data, format)
            except ModuleTaggerError as e:
                raise TaggerError(e.msg, path)
            except Exception as e:
                raise TaggerError("Cannot load image from url!", src)             

        else:
            raise TaggerError("Wrong mode selected", "")


    @classmethod
    def changeImageType(cls, type, hash, path):
        try:
            file = cls.openFile(path)
            file.changeImageType(type, hash)
        except MutagenError:
            raise TaggerError("Image type cannot be changed!", path)


    @classmethod
    def changeImageDesc(cls, desc, hash, path):
        try:
            file = cls.openFile(path)
            file.changeImageDesc(desc, hash)
        except MutagenError:
            raise TaggerError("Image description cannot be changed!", path)


    @classmethod
    def deleteImage(cls, hash, path):
        try:
            file = cls.openFile(path)
            file.deleteImage(hash)
        except MutagenError:
            raise TaggerError("Image deletion cannot be done!", path)


    @classmethod
    def deleteAllImages(cls, path):
        try:
            file = cls.openFile(path)
            file.deleteAllImages()
        except MutagenError:
            raise TaggerError("Images deletion cannot be done!", path)


    @classmethod
    def deleteTag(cls, path):
        try:
            file = cls.openFile(path)
            file.deleteTag()
        except MutagenError:
            raise TaggerError("Whole tag cannot be deleted!", path)


    @classmethod
    def checkImageUnique(cls, desc, path):
        file = cls.openFile(path)
        return file.checkImageUnique(desc)

    
    @staticmethod
    def checkStatus(path):
        #if needed in future
        pass
