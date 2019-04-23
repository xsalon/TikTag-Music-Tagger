from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import BitrateMode
from mutagen.id3 import ID3, APIC, PictureType
from TikTagCtrl.TaggerError import *
from io import BytesIO
from PIL import Image
import datetime
import os

class AlbumArt():
    def __init__(self, tag):
        self.tag = tag
        #popis pri hover
        self.type = str(tag.type).split('.')[1]
        self.encoding = str(tag.encoding).split('.')[1]
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
    def __init__(self, path):
        self.file = MP3(path, ID3=EasyID3)
        self.id3file = ID3(path)

        self.bitrateModeTable = {
            BitrateMode.UNKNOWN : "CBR",
            BitrateMode.CBR : "CBR",
            BitrateMode.VBR : "VBR",
            BitrateMode.ABR : "ABR"
        }

 
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


    def metadata(self):
        #print(EasyID3.valid_keys.keys())
        #print(dict(self.file.tags))
        return dict(self.file.tags)


    def editTag(self, name, value):
        valueList = [x.strip() for x in value.split(',')]
        self.file[name] = valueList
        self.file.save()


    def retrieveImages(self):
        imgList = []
        for image in self.id3file.getall("APIC"):
            imgList.append(AlbumArt(image))
        return imgList


    def addLocalImage(self, desc, type, data, format):
        self.id3file.add(APIC(3, 'image/' + str(format), type, desc, data))
        self.id3file.save()


    def addOnlineImage(self, desc, type, data, format):
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


    def deleteImages(self, hash):
        self.id3file.delall(hash)
        self.id3file.save()


    def editTag(self, name, value):
        valueList = [x.strip() for x in value.split(',')]
        self.file[name] = valueList
        self.file.save()


    def putTag(self, name, value):
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
               





