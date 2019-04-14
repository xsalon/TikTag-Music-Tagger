from mutagen.mp3 import EasyMP3 as MP3
from mutagen.mp3 import BitrateMode
from mutagen.id3 import ID3, APIC, PictureType
from io import BytesIO
import base64
from PIL import Image
import random
import requests
import datetime

class AlbumArt():
    def __init__(self, tag):
        self.tag = tag
        self.type = str(tag.type).split('.')[1]
        self.encoding = str(tag.encoding).split('.')[1]
        img = Image.open(BytesIO(tag.data))
        self.width, self.height = img.size
        self.resolution = str(self.width) + "x" + str(self.height)
        self.size = str(len(tag.data)) + " B"
        self.infoString = self.type + "\n" + str(self.tag.mime) + "\n" + self.encoding + "\n" + self.resolution + "\n" + self.size

class MP3tag(object):
    def __init__(self, path):
        self.file = MP3(path)
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

    def retrieveImages(self):
        imgList = []
        for image in self.id3file.getall("APIC"):
            imgList.append(AlbumArt(image))
        return imgList

    def addLocalImage(self, image, desc, type):
        data = open(image, 'rb').read()
        self.id3file.add(APIC(3, 'image/jpeg', type, desc, data))
        self.id3file.save()

    def addOnlineImage(self, url, desc, type):
        response = requests.get(url)
        data = response.content
        self.id3file.add(APIC(3, 'image/jpeg', type, desc, data))
        self.id3file.save()

    def changeImageType(self, type, hash):
        for image in self.id3file.getall("APIC"):
            if image.HashKey == hash:
                image.type = type
        self.id3file.save()

    def deleteImages(self, hash):
        self.id3file.delall(hash)
        self.id3file.save()

    def metadata(self):
        return dict(self.file.tags)




