import mutagen
import taglib
import os.path
import requests
import imghdr
from mutagen import MutagenError
from TikTagCtrl.MP3tag import MP3tag
from TikTagCtrl.TaggerError import *

class Tagger(object):
    fileFormats = ["mp3"]
    imageFormats = ["jpg", "png", "jpeg"]
   
    imageTypes = ["Other", "File Icon", "Other File Icon", "Front Cover", "Back Cover", "Leaflet Page", "Media", 
                  "Lead Artist", "Artist/Performer", "Conductor", "Band", "Composer", "Lyricist/Text Writer", "Recording Location", "During Recording",
                  "During Performance", "Screen Capture", "Fish", "Illustration", "Band/Artist Logo", "Publisher/Studio Logo"]

    id3Keys = {
               'Title' : 'title',
               'Artist' : 'artist',
               'Album' : 'album',
               'Album Artist' : 'albumartist', 
               'Date' : 'date',
               'Original Date' : 'originaldate', 
               'Genre' : 'genre',
               'Composer' : 'composer', 
               'Track Number' : 'tracknumber', 
               'Disc Number' : 'discnumber',
               'Catalog Number' : 'catalognumber',
               'BPM' : 'bpm',
               'Encoded by' : 'encodedby',
               'Compilation' : 'compilation', 
               'Organization' : 'organization',
               'ISRC' : 'isrc',
               'Composer' : 'composer', 
               'Copyright' : 'copyright',  
               'Lyricist' : 'lyricist', 
               'Lenght' : 'length', 
               'Media' : 'media', 
               'Mood' : 'mood', 
               'Version' : 'version', 
               'Conductor' : 'conductor', 
               'Arranger' : 'arranger', 
               'Author' : 'author', 
               'Album Artist Sort' : 'albumartistsort', 
               'Album Sort' : 'albumsort', 
               'Composer Sort' : 'composersort', 
               'Artist Sort' : 'artistsort', 
               'Title Sort' : 'titlesort', 
               'ASIN' : 'asin', 
               'Performer' : 'performer', 
               'Barcode' : 'barcode', 
               'Disc Subtitle' : 'discsubtitle', 
               'Language' : 'language', 
               'Performer*' : 'performer:*', 
               'Track ID (MB)' : 'musicbrainz_trackid', 
               'Website' : 'website', 
               'Replay Gain' : 'replaygain_*_gain', 
               'Replay Gain Peak' : 'replaygain_*_peak', 
               'Artist ID (MB)' : 'musicbrainz_artistid', 
               'Album ID (MB)' : 'musicbrainz_albumid', 
               'Album Artist ID (MB)' : 'musicbrainz_albumartistid', 
               'TRMID (MB)' : 'musicbrainz_trmid', 
               'MusicIP PUID' : 'musicip_puid', 
               'MusicIP Fingerprint' : 'musicip_fingerprint', 
               'Album Status (MB)' : 'musicbrainz_albumstatus', 
               'Album Type (MB)' : 'musicbrainz_albumtype', 
               'Release Country' : 'releasecountry', 
               'Disc ID (MB)' : 'musicbrainz_discid',  
               'Release Track ID (MB)' : 'musicbrainz_releasetrackid', 
               'Release Group ID (MB)' : 'musicbrainz_releasegroupid',         
               'Work ID (MB)' : 'musicbrainz_workid', 
               'AcoustID Fingerprint' : 'acoustid_fingerprint', 
               'AcoustID' : 'acoustid_id'  
        }

    @classmethod
    def openFile(cls, path):
        fileExtension = os.path.splitext(path)[1][1:].strip().lower()
        if fileExtension not in cls.fileFormats:
           raise TaggerError("File not supported!", path)

        try:
            if fileExtension == "mp3":
                file = MP3tag(path)
        except MutagenError:
            raise TaggerError("File cannot be modiefied!")

        return file

        
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
        file = cls.openFile(path)
        file.editTag(name, value)
    
    @classmethod
    def retrieveCoverImage(cls, path):
        file = cls.openFile(path)
        data = None #co ak nema album art

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
            except IOError:
                raise TaggerError("Cannot open image file!", src)
                
            format = imghdr.what("image", data)
            if not format or format not in cls.imageFormats:
                raise TaggerError("Unsupported image file format!", format)
            else:
                file.addLocalImage(desc, type, data, format)
        
        elif mode == "url":
            try:
                response = requests.get(src)
            except Exception:
                raise TaggerError("Cannot load image from url!", src)   
            data = response.content

            format = imghdr.what("image", data)
            if not format or format not in cls.imageFormats:
                raise TaggerError("Unsupported image file format!", format)
            else:
                file.addOnlineImage(desc, type, data, format)
        else:
            raise TaggerError("Wrong mode selected", "")


    @classmethod
    def changeImageType(cls, type, hash, path):
        file = cls.openFile(path)
        file.changeImageType(type, hash)

    @classmethod
    def changeImageDesc(cls, desc, hash, path):
        file = cls.openFile(path)
        file.changeImageDesc(desc, hash)


    @classmethod
    def deleteImages(cls, hash, path):
        file = cls.openFile(path)
        file.deleteImages(hash)

    @classmethod
    def checkImageUnique(cls, desc, path):
        file = cls.openFile(path)
        return file.checkImageUnique(desc)
    
    @staticmethod
    def checkStatus(path):
        pass


