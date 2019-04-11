import taglib
import os.path

class Taggerz(object):
    def __init__(self, supportedFormats):
        self.formats = supportedFormats
        
    def checkSupport(self, path):
        fileExtension = os.path.splitext(path)[1][1:].strip().lower()
        if fileExtension in self.formats:
            return True
        else:
            return False
        
    def fetchTags(self, path):
        if not self.checkSupport(path):
            return ""

        song = taglib.File(path)
        return song.tags

    def fetchGeneralInfo(self, path):
        if not self.checkSupport(path):
            return ""

        song = taglib.File(path)

        generalInfo = {}
        if hasattr(song, 'lenght'):
            generalInfo["Duration"] = str(song.length)
        else:
            generalInfo["Duration"] = "N/A"
        if hasattr(song, 'sampleRate'):
            generalInfo["Sample Rate"] = str(song.sampleRate)
        if hasattr(song, 'channels'):
            generalInfo["Channels"] = str(song.channels)
        if hasattr(song, 'bitrate'):
            generalInfo["Bitrate"] = str(song.bitrate)
        if hasattr(song, 'codec'):
            generalInfo["Codec"] = str(song.codec)
        else:
            generalInfo["Codec"] = "N/A"
       
        return generalInfo
        
    def checkStatus(self, path):
        if not self.checkSupport(path):
            return ""

        song = taglib.File(path)

        evaluation = 0
        artist = False
        title = False
        if 'ARTIST' in song.tags.keys():
           evaluation += 10
           artist = True
        if 'ALBUM' in song.tags.keys():
           evaluation += 8
        if 'ALBUMARTIST' in song.tags.keys():
           evaluation += 3
        if 'DATE' in song.tags.keys():
           evaluation += 6
        if 'DISCNUMBER' in song.tags.keys():
           evaluation += 2
        if 'GENRE' in song.tags.keys():
           evaluation += 7
        if 'TITLE' in song.tags.keys():
           evaluation += 10
           title = True
        if 'TRACKNUMBER' in song.tags.keys():
           evaluation += 4

        if evaluation > 40:
            return "Good"
        elif evaluation > 20 and artist and title:
            return "Mediocre"
        elif evaluation > 10 and artist and title:
            return "Weak"
        elif bool(song) != True:
            return "None"
        else:
            return "Bad"
