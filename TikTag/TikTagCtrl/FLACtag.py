from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType
from io import BytesIO
from TikTagCtrl.TaggerError import *
from PIL import Image
import datetime


class AlbumArt(object):
    def __init__(self, tag):
        self.tag = tag
        self.type = str(PictureType(self.tag.type)).split('.')[1]
        self.desc = str(self.tag.desc)
        self.mime = str(self.tag.mime)
        try:
            img = Image.open(BytesIO(tag.data))
            self.width, self.height = img.size
            self.depth = str(FLACtag.modeToBpp[img.mode]) + "bit"
        except Exception:
            raise ModuleTaggerError("Unsupported or currupted embedded image found!", "")
        self.resolution = str(self.width) + "x" + str(self.height)
        self.size = "Size: " + str(len(tag.data)) + " B"
        self.infoString = self.type + "\n" + self.mime + "\n" + self.depth + "\n" + self.desc + "\n" + self.resolution + "\n" + self.size


class FLACtag(object):
    modeToBpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
    
    def __init__(self, path):
        self.file = FLAC(path)
        self.hashValue = 0

        #normalize name of key value
        for key in self.file.tags.keys():
            if " " in key:
                newKey = key.replace(" ", "")
                self.file[newKey] = self.file.pop(key)


        for i in range(len(self.file.pictures)):
            self.file.pictures[i] = self.file.pictures[i]
            self.file.pictures[i].HashKey = i

        self.hashValue = len(self.file.pictures)

        self.tagKeys = {
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
               'Initial Key' : 'key',
               'Encoded by' : 'encodedby',
               'Encoder' : 'encoder',
               'Encoder Options' : 'encoder_options',
               'Encoded with' : 'encoded_using',
               'Compilation' : 'compilation', 
               'Organization' : 'organization',
               'Location' : 'location',
               'Contact' : 'contact',
               'Description' : 'description',
               'ISRC' : 'isrc',
               'Comment' : 'comment',
               'Modified by' : 'modified',
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
               'Language' : 'language', 
               'Track ID (MB)' : 'musicbrainz_trackid', 
               'Website' : 'website', 
               'Replay Gain' : 'replaygain_track_gain', 
               'Replay Gain Peak' : 'replaygain_track_peak', 
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
        
        generalInfo["Codec"] = "FLAC "
       
        return generalInfo


    def metadata(self):
        #print(str(dict(self.file.tags)))
        return dict(self.file.tags)


    def retrieveImages(self):
        imgList = []
        for image in self.file.pictures:
            imgList.append(AlbumArt(image))
        return imgList


    def addImage(self, desc, type, data, format):
        pic = Picture()
        pic.data = data
        pic.type = PictureType(type)
        pic.mime = 'image/' + str(format)
        pic.desc = desc

        try:
            img = Image.open(BytesIO(data))
            pic.width, pic.height = img.size
            pic.depth = FLACtag.modeToBpp[img.mode]
        except Exception:
            raise ModuleTaggerError("Cannot open selected picture!", "") 

        self.file.add_picture(pic)
        self.file.save()


    def changeImageType(self, type, hash):
        for image in self.file.pictures:
            if image.HashKey == hash:
                image.type = type
        self.file.save()


    def changeImageDesc(self, desc, hash):
        for image in self.file.pictures:
            if image.HashKey == hash:
                image.desc = desc
        self.file.save()


    def deleteImage(self, hash):        
        newList = []
        for image in self.file.pictures:
            if not image.HashKey == hash:
                newList.append(image)

        self.file.clear_pictures()

        for img in newList:
            self.file.add_picture(img)
        self.file.save()


    def deleteAllImages(self):
        self.file.clear_pictures()
        self.file.save()


    def editTag(self, name, value):
        valueList = [x.strip() for x in value.split(',')]
        self.file[self.tagKeys[name]] = valueList
        self.file.save()


    def putTag(self, name, value):
        if type(value) is list:
            value = [str(i) for i in value]
        else:
            value = str(value)
        if name[0].isupper():
            self.file[self.tagKeys[name]] = value
        elif name in self.tagKeys.values():
            self.file[name] = value
        self.file.save()


    def deleteTag(self):
        self.file.delete()
        self.file.save()


    def checkImageUnique(self, desc):
        return True