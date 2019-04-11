from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3
from io import BytesIO
import datetime

class MP3tag(object):
    def __init__(self, path):
        self.file = MP3(path)
        self.id3file = ID3(path)
        self.bitrateModeTable = {
            "BitrateMode.UNKNOWN" : "CBR",
            "BitrateMode.CBR" : "CBR",
            "BitrateMode.VBR" : "VBR",
            "BitrateMode.ABR" : "ABR"
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
            generalInfo["Codec"] = "MP3 " + self.bitrateModeTable[str(self.file.info.bitrate_mode)]
       
        return generalInfo

    def retrieveImages(self):
        return self.id3file.get("APIC:").data

    def metadata(self):
        return dict(self.file.tags)




