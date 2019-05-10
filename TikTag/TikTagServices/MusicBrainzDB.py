import musicbrainzngs
from datetime import datetime as dt
from TikTagServices.ServiceError import ServiceError

class MusicBrainzDB(object):
    METHOD_COUNT = 3
    
    def _init_(self):
        musicbrainzngs.set_useragent("TikTag", "1.0")


    def checkRecording(self, results, artist, title): 
        try:
            if self.titleComparer(results["title"], title):
                for artistItem in results["artist-credit"]:
                    if self.artistComparer(artistItem["artist"]["name"], artist):
                        return True;
        except KeyError:
            print("nieco zle")
        return False


    def checkRelease(self, results, artist, album=None):
        try:
            if album:
                if self.titleComparer(results["title"], album):
                    if results["status"] == "Official":
                        if "artist-credit" in results:
                            for artistItem in results["artist-credit"]:
                                if self.artistComparer(artistItem["artist"]["name"], artist):
                                    return True;
                        return True;
            else:
                if "artist-credit" in results:
                            for artistItem in results["artist-credit"]:
                                if self.artistComparer(artistItem["artist"]["name"], artist):
                                    return True
        except KeyError:
            print("nieco zle")
        return False


    def titleComparer(self, resultTitle, givenTitle):
        #print(resultTitle, givenTitle)
        return resultTitle.lower() == givenTitle.lower()

    
    def artistComparer(self, resultArtist, givenArtist):
        #print(resultArtist, givenArtist)
        return resultArtist.lower() == givenArtist.lower()


    def getByArtistTitle(self, metadata): 
        musicbrainzngs.set_useragent("TikTag", "1.0")
        if "artist" in metadata and "title" in metadata:
            artist = ' '.join(metadata["artist"]).strip()
            title = ' '.join(metadata["title"]).strip()
            results = None
            releaseResult = None
            results = musicbrainzngs.search_recordings(artist=artist, recording=title)
            if results:
                for record in results["recording-list"]:
                    if self.checkRecording(record, artist, title):
                        recordingResult = record    
                        lowDate = "3000-12-30"
                        index = 0
                        for i, releaseItem in enumerate(recordingResult["release-list"]):
                            if "date" in releaseItem:
                                if len(releaseItem["date"]) == 10:
                                    date1 = dt.strptime(releaseItem["date"], "%Y-%m-%d")
                                    date2 = dt.strptime(lowDate, "%Y-%m-%d")
                                elif len(releaseItem["date"]) == 4:
                                    date1 = dt.strptime(releaseItem["date"] + "-12-30", "%Y-%m-%d")
                                    date2 = dt.strptime(lowDate, "%Y-%m-%d")
                                else:
                                    continue
                                if date2 > date1:
                                    if len(releaseItem["date"]) == 4:
                                        lowDate = releaseItem["date"] + "-12-30"
                                    else:
                                        lowDate = releaseItem["date"]
                                    index = i
                        releaseResult = recordingResult["release-list"][index]
                        return [recordingResult, releaseResult]
        return False


    def getByAlbum(self, metadata):
        musicbrainzngs.set_useragent("TikTag", "1.0")
        if "artist" in metadata and "album" in metadata:
            artist = ' '.join(metadata["artist"]).strip()
            release = ' '.join(metadata["album"]).strip()
            results = None
            releaseResult = None
            results = musicbrainzngs.search_releases(artist=artist, release=release)
            if results:
                lowDate = "3000-12-30"
                index = 0
                for i, releaseItem in enumerate(results["release-list"]):
                    if self.checkRelease(results["release-list"][i], artist, release) :   
                        if "date" in releaseItem:
                            if len(releaseItem["date"]) == 10:
                                date1 = dt.strptime(releaseItem["date"], "%Y-%m-%d")
                                date2 = dt.strptime(lowDate, "%Y-%m-%d")
                            elif len(releaseItem["date"]) == 4:
                                date1 = dt.strptime(releaseItem["date"] + "-12-30", "%Y-%m-%d")
                                date2 = dt.strptime(lowDate, "%Y-%m-%d")
                            else:
                                continue
                            if date2 > date1:
                                if len(releaseItem["date"]) == 4:
                                    lowDate = releaseItem["date"] + "-12-30"
                                else:
                                    lowDate = releaseItem["date"]
                                index = i
                return results["release-list"][index]
        return False


    def getByCatno(self, metadata):
        musicbrainzngs.set_useragent("TikTag", "1.0")
        if "catalognumber" in metadata and "artist" in metadata:
            catno = metadata["catalognumber"]
            artist = ' '.join(metadata["artist"]).strip()
            results = None
            releaseResult = None
            results = musicbrainzngs.search_releases(catno=catno)
            if results:
                lowDate = "3000-12-30"
                index = 0
                for i, releaseItem in enumerate(results["release-list"]):
                    if self.checkRelease(results["release-list"][i], artist):   
                        if "date" in releaseItem:
                            if len(releaseItem["date"]) == 10:
                                date1 = dt.strptime(releaseItem["date"], "%Y-%m-%d")
                                date2 = dt.strptime(lowDate, "%Y-%m-%d")
                            elif len(releaseItem["date"]) == 4:
                                date1 = dt.strptime(releaseItem["date"] + "-12-30", "%Y-%m-%d")
                                date2 = dt.strptime(lowDate, "%Y-%m-%d")
                            else:
                                continue
                            if date2 > date1:
                                if len(releaseItem["date"]) == 4:
                                    lowDate = releaseItem["date"] + "-12-30"
                                else:
                                    lowDate = releaseItem["date"]
                                index = i
                return results["release-list"][index]
        return False

    def mapRecordingResult(self, result, finalDict):
        if "title" in result and result["title"]:
            finalDict["Title"] = result["title"]

        if "artist-credit" in result and result["artist-credit"]:
            finalDict["Artist"] = [artist["artist"]["name"] for artist in result["artist-credit"]]
            finalDict["Artist ID (MB)"] = result["artist-credit"][0]["artist"]["id"]
            if "sort-name" in result["artist-credit"][0]["artist"]:
                finalDict["Artist Sort"] = result["artist-credit"][0]["artist"]["sort-name"]

        if "tag-list" in result["tag-list"]:
            finalDict["Genre"] = [tag["name"] for tag in result["tag-list"]]

        if "isrc-list" in result and result["isrc-list"]:
            finalDict["ISRC"] = result["isrc-list"][0]

        if "medium-list" in result and result["medium-list"]:
            if "position" in result["medium-list"][0]:
                finalDict["Disc Number"] = result["medium-list"][0]["position"]
            if "track-list" in result["medium-list"][0]:
                finalDict["Track Number"] = result["medium-list"][0]["track-list"][0]["number"]

        if "lenght" in result and result["lenght"]:
            finalDict["Lenght"] = result["lenght"]

        if "id" in result:
            finalDict["Release Track ID (MB)"] = result["id"]
        
        return finalDict

    
    def mapReleaseResult(self, result, finalDict):
        if "id" in result:
            finalDict["Album ID (MB)"] = result["id"]

        if "title" in result and result["title"]:
            finalDict["Album"] = result["title"]

        if "status" in result and result["status"]:
            finalDict["Album Status (MB)"] = result["status"]

        if "artist-credit" in result and result["artist-credit"]:
            finalDict["Album Artist"] = [artist["artist"]["name"] for artist in result["artist-credit"]]

        if "release-group" in result and result["release-group"]:
            finalDict["Release Group ID (MB)"] = result["release-group"]["id"]
            if "primary-type" in result["release-group"]:
                finalDict["Album Type (MB)"] = result["release-group"]["primary-type"]

        if result["date"]:
            finalDict["Date"] = result["date"]
            finalDict["Original Date"] = result["date"][:4]

        if "country" in result and result["country"]:
            finalDict["Release Country"] = result["country"]

        if "release-event-list" in result:
            for event in result["release-event-list"]:
                if finalDict["Date"] == event["date"]:
                    if "barcode" in event:
                        finalDict["Barcode"] = event["barcode"]
                    if "asin" in event:
                        finalDict["ASIN"] = event["asin"]
                    if "label-info-list" in event:
                        if "catalog-number" in event["label-info-list"][0]:
                            finalDict["Catalog Number"] = event["label-info-list"][0]["Catalog Number"]
                        if "label" in event["label-info-list"][0]:
                            finalDict["Organization"] = event["label-info-list"][0]["label"]["name"]
                    break

        return finalDict

     
    def getByRecord(self, metadata):
        idAlbum = False
        recordingResult = ''
        releaseResult = ''
        finalDict = {
             'Title' : None,
             'Artist' : [],
             'Album' : None,
             'Album Artist' : [],
             'Date' : None,
             'Original Date' : None,
             'Genre' : None,
             'Track Number' : None,
             'Disc Number' : None,
             'Catalog Number' : None,
             'Organization' : None,
             'Lenght' : None,
             'Barcode' : None,
             'ISRC' : None,
             'ASIN' : None,
             'Artist Sort' : None,
             'Release Track ID (MB)' : None,
             'Artist ID (MB)' : None,
             'Album ID (MB)' : None,
             'Album Status (MB)' : None,
             'Album Type (MB)' : None,
             'Release Country' : None,
             'Release Group ID (MB)' : None
        };

        for i in range(MusicBrainzDB.METHOD_COUNT):
            if i == 0:
                print("title")
                resultList = self.getByArtistTitle(metadata)
                if len(resultList) == 2:
                    finalDict = self.mapRecordingResult(resultList[0], finalDict)
                    finalDict = self.mapReleaseResult(resultList[1], finalDict)
                    break
                resultList = None
            if i == 1:
                print("catno")
                resultList = self.getByCatno(metadata)
                if resultList:
                    finalDict = self.mapReleaseResult(resultList, finalDict)
                    break
                resultList = None
            if i == 2:
                print("album")
                resultList = self.getByAlbum(metadata)
                if resultList:
                    finalDict = self.mapReleaseResult(resultList, finalDict)
                    break
                resultList = None

        return finalDict
            