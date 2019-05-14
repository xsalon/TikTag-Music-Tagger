import acoustid
from collections import Counter
import json

class AcoustID(object):
    def __init__(self):
        self.clientId = "MXg04WOm0X"

    def mostCommon(self, list):
            data = Counter(list)
            return data.most_common(1)[0][0]

    def getFingerprintedData(self, path):
        finalDict = {
            "artist" : [],
            "title" : [],
            "musicbrainz_releasetrackid" : [],
            "Artist" : None,
            "Title" : None,
            "Release Track ID (MB)" : None,
            }
        artistCompare = []
        artistList = []
        resultList = acoustid.match(self.clientId, path, parse=False)

        if resultList and "status" in resultList:
            if resultList["status"] == "ok":
                for item in resultList["results"]:
                    if "recordings" in item:
                        for i, result in enumerate(item["recordings"]):
                            if "artists" in result:
                                for artist in result["artists"]:
                                    artistList.append(artist["name"])
                                artistCompare.append(', '.join(artistList))
                                artistList.clear()
                                if i == 10:
                                    break

        potentialArtist = self.mostCommon(artistCompare)

        joinWord = ", "
        for item in resultList["results"]:
            if "recordings" in item:
                for result in item["recordings"]:
                    if "artists" in result:
                        for artist in result["artists"]:
                            artistList.append(artist["name"])
                            if "joinphrase" in artist:
                                joinWord = artist["joinphrase"]
                        if ', '.join(artistList) == potentialArtist:
                            finalDict["Artist"] = joinWord.join(artistList)
                            finalDict["Title"] = result["title"]
                            finalDict["Release Track ID (MB)"] = result["id"]
                            finalDict["artist"].append(' '.join(artistList))
                            finalDict["title"].append(result["title"])
                            finalDict["musicbrainz_releasetrackid"].append(result["id"])
                            return finalDict
                        artistList.clear()
        return False