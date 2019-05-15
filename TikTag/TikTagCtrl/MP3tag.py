# File: MP3tag.py
# Project: TikTag
# Author: Marek Salon (xsalon00)
# Contact: xsalon00@stud.fit.vutbr.cz
# Date: 10.5.2019
# Description: MP3 file manipulations using mutagen lib

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import BitrateMode
from mutagen.id3 import ID3, APIC, PictureType
import mutagen
from TikTagCtrl.TaggerError import *
from io import BytesIO
from PIL import Image
import datetime
import os


class AlbumArt():
    """Metadata picture data object representation"""
    def __init__(self, tag):
        self.tag = tag
        if "." in str(tag.type):
            self.type = str(tag.type).split('.')[1]
        else:
           self.type = str(tag.type)
        if "." in str(tag.encoding):
            self.encoding = str(tag.encoding).split('.')[1]
        else:
           self.type = str(tag.encoding)
        self.mime = str(self.tag.mime)
        self.desc = str(self.tag.desc)
        try:
            img = Image.open(BytesIO(tag.data))
            self.width, self.height = img.size
            self.resolution = str(self.width) + "x" + str(self.height)
        except Exception:
            raise ModuleTaggerError("Unsupported or currupted embedded image found!", "") 
        self.size = "Size: " + str(len(tag.data)) + " B"
        self.infoString = self.type + "\n" + self.mime + "\n" + self.encoding + "\n" + self.desc + "\n" + self.resolution + "\n" + self.size


class MP3tag(object):
     """FLAC methods class"""
     TAGKEYS = {
               'Title' : 'title',
               'Artist' : 'artist',
               'Album' : 'album',
               'Album Artist' : 'albumartist', 
               'Date' : 'date',
               'Original Date' : 'originaldate', 
               'Genre' : 'genre',
               'Track Number' : 'tracknumber', 
               'Disc Number' : 'discnumber',
               'Catalog Number' : 'catalognumber',
               'BPM' : 'bpm',
               'Initial Key' : 'initialkey',
               'Comment' : 'comment',
               'Encoded by' : 'encodedby',
               'Compilation' : 'compilation', 
               'Organization' : 'organization',
               'ISRC' : 'isrc',
               'Modified by' : 'modified', 
               'Composer' : 'composer', 
               'Copyright' : 'copyright',  
               'Lyricist' : 'lyricist', 
               'Length' : 'length', 
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
               'Website' : 'website', 
               'Replay Gain' : 'replaygain_*_gain', 
               'Replay Gain Peak' : 'replaygain_*_peak', 
               'Artist ID (MB)' : 'musicbrainz_artistid', 
               'Album ID (MB)' : 'musicbrainz_albumid',  
               'Album Status (MB)' : 'musicbrainz_albumstatus', 
               'Album Type (MB)' : 'musicbrainz_albumtype', 
               'Release Country' : 'releasecountry', 
               'Release Track ID (MB)' : 'musicbrainz_releasetrackid', 
               'Release Group ID (MB)' : 'musicbrainz_releasegroupid',         
               'AcoustID Fingerprint' : 'acoustid_fingerprint', 
               'AcoustID' : 'acoustid_id'  
        }

     def __init__(self, path):
         self.file = MP3(path, ID3=EasyID3)
         self.id3file = ID3(path)
     
         self.bitrateModeTable = {
             BitrateMode.UNKNOWN : "CBR",
             BitrateMode.CBR : "CBR",
             BitrateMode.VBR : "VBR",
             BitrateMode.ABR : "ABR"
         }
     
         EasyID3.RegisterTextKey("initialkey", "TKEY")
         EasyID3.RegisterTextKey("comment", "COMM")
         EasyID3.RegisterTextKey("modified", "TPE4")
         EasyID3.RegisterTXXXKey('tiktag', 'TikTag')


     def generalInfo(self):
         generalInfo = {}
         #dalsie info v tooltipe
         
         if hasattr(self.file.info, 'length'):
             generalInfo["Duration"] = str(datetime.timedelta(seconds=int(self.file.info.length)))
         
         if hasattr(self.file.info, 'sample_rate'):
             generalInfo["Sample Rate"] = str(self.file.info.sample_rate) + " Hz"
         
         if hasattr(self.file.info, 'channels'):
             generalInfo["Channels"] = str(self.file.info.channels)
         
         if hasattr(self.file.info, 'bitrate'):
             generalInfo["Bitrate"] = str(int(self.file.info.bitrate / 1000)) + " kbps"
         
         if hasattr(self.file.info, 'bitrate_mode'):
             generalInfo["Codec"] = "MP3 " + self.bitrateModeTable[self.file.info.bitrate_mode]
        
         return generalInfo
     
     
     def getLength(self):
         if hasattr(self.file.info, 'length'):
             return self.file.info.length
         else:
             return False
     
     
     def metadata(self):
         #print(EasyID3.valid_keys.keys())
         #print(dict(self.file.tags))
         return dict(self.file.tags)
     
     
     def retrieveImages(self):
         imgList = []
         for image in self.id3file.getall("APIC"):
             imgList.append(AlbumArt(image))
         return imgList
     
     
     def addImage(self, desc, type, data, format):
         self.id3file.add(APIC(3, 'image/' + str(format), type, desc, data))
         self.id3file.save()
     
     
     def changeImageType(self, type, hash):
         image = self.id3file.getall(hash)
         image[0].type = type
         self.id3file.save()
     
     
     def changeImageDesc(self, desc, hash):
         image = self.id3file.getall(hash)
         image[0].desc = desc
         self.id3file.save()
     
     
     def deleteImage(self, hash):
         self.id3file.delall(hash)
         self.id3file.save()
     
     
     def deleteAllImages(self):
         self.id3file.delall("APIC")
         self.id3file.save()
     
     
     def editTag(self, name, value):
         valueList = [x.strip() for x in value.split(',')]
         self.file[MP3tag.TAGKEYS[name]] = valueList
         self.file.save()
     
     
     def putTag(self, name, value):
         if type(value) is list:
             value = [str(i) for i in value]
         else:
             value = str(value)
         if name[0].isupper():
             self.file[MP3tag.TAGKEYS[name]] = value
         elif name in MP3tag.TAGKEYS.values():
             self.file[name] = value
         self.file.save()
     
     
     def deleteTag(self):
         self.file.delete()
         self.file.save()
     
     
     def checkImageUnique(self, desc):
         for image in self.id3file.getall("APIC"):
             if image.desc == desc:
                 return False
         return True
