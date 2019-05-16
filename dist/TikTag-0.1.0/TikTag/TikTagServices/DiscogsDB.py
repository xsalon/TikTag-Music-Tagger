# File: DiscogsDB.py
# Project: TikTag
# Author: Marek Salon (xsalon00)
# Contact: xsalon00@stud.fit.vutbr.cz
# Date: 10.5.2019
# Description: Discogs service using official python API

import discogs_client
import time
from TikTagServices.ServiceError import ServiceError
from TikTagServices.FuzzyComparer import FuzzyComparer

class DiscogsDB(object):
    """Discogs class service implementation and parsing"""
    def __init__(self):
        self.customerKey = "IHkJHfvrguwTouLOuOTl"
        self.secretKey = "doLEDwLjrQuEwJCRrdTVEsjgegqqNEQC"
        self.client = discogs_client.Client("TikTag/1.0")
        self.client.set_consumer_key(self.customerKey, self.secretKey)
        self.counter = 0


    def getAuthUrl(self):
        rckey, rcsecret, authurl = self.client.get_authorize_url()
        return authurl


    def authorization(self, code):
        try:
            self.client.get_access_token(code)
        except discogs_client.exceptions.HTTPError as e:
            raise ServiceError(e.status_code, e.msg)


    def identity(self):
        try:
            me = self.client.identity()
        except discogs_client.exceptions.HTTPError as e:
            raise ServiceError(e.status_code, e.msg)


    def inTracklist(self, tracklist, title, artist=None, length=False):
        for track in tracklist:
            if FuzzyComparer.fuzzComparer(track.title, title):
                okStatus = True
                if artist:
                    for trackArtist in track.artists:
                        if FuzzyComparer.fuzzComparer(artist, trackArtist.name):
                            self.artistNeeded = True;
                            okStatus = True
                if track.duration and length:
                    if self.durationCompare(track.duration, length):
                        okStatus = True
                    else:
                        okStatus = False
                return okStatus
        return False


    def getFromTracklist(self, tracklist, title, artist=None, length=False):
        for track in tracklist:
            if FuzzyComparer.fuzzComparer(track.title, title):
                if artist:
                    for trackArtist in track.artists:
                        if FuzzyComparer.fuzzComparer(artist, trackArtist.name):
                            return track
                else:
                    return track
        return False


    def chooseFromResults(self, results, title, artist, isRelease, length=None):
        result = None
        if results.count > 4:
            count = 5;
        else:
            count = results.count

        for i in range(count):
            if isRelease:
                for trackArtist in results[i].artists:
                     if FuzzyComparer.fuzzComparer(trackArtist.name, artist):
                        if self.inTracklist(results[i].tracklist, title, length=length):
                            self.result = results[i]
                            return results[i]
                     else:
                        if self.inTracklist(results[i].tracklist, title, artist, length):
                            self.result = results[i]
                            return results[i]
            else:
                if self.inTracklist(results[i].tracklist, title, length=length):
                    self.result = results[i]
                    return results[i]
        return False


    def durationCompare(self, resultLength, givenLength):
        if len(resultLength) < 6:
            procLength = str(resultLength).split(":")
            msLength = (int(procLength[0])*60 + int(procLength[1]))*1000
            #print(int(msLength), " vs ", int(givenLength))
            #print(abs(int(msLength) - int(givenLength)))
            if abs(int(msLength) - int(givenLength)) < 10000:
                return True
            else:
                return False
        return True
   

    def makeTagDict(self, result, title, artist, finalDict, isRelease):
        if self.artistNeeded:
            track = self.getFromTracklist(result.tracklist, title, artist)
        else:
            track = self.getFromTracklist(result.tracklist, title)
        
        if not finalDict["Album"] and result.title:
            finalDict["Album"] = result.title
        
        if not finalDict["Album Artist"]:
            if "artists" in dir(result) and result.artists:
                finalDict["Album Artist"] = []
                for artist in result.artists:
                    finalDict["Album Artist"].append(artist.name)

        if not finalDict["Date"] and "year" in result.data:
            finalDict["Date"] = result.data["year"]
        
        if not finalDict["Original Date"] and isRelease and result.master:
            if self.inTracklist(result.master.tracklist, title):
                if "year" in result.master.data:
                    finalDict["Original Date"] = result.master.data["year"]

        if not finalDict["Genre"] and result.genres:
            finalDict["Genre"] = result.genres

        if not finalDict["Track Number"] and track.position:
            if "-" in track.position:
                finalDict["Track Number"] = track.position.split("-")[1]
            elif len(track.position) == 2:
                finalDict["Track Number"] = track.position[1]
            else:
                finalDict["Track Number"] = track.position

        if not finalDict["Disc Number"] and track.position:
            if "-" in track.position:
                finalDict["Disc Number"] = track.position.split("-")[0]

        if not finalDict["Length"] and track.duration:
            finalDict["Length"] = track.duration
        
        if not finalDict["Catalog Number"] and "catno" in result.data:
            finalDict["Catalog Number"] = result.data["catno"]

        if not finalDict["Organization"] and "label" in result.data:
            if len(result.data['label']) == 1:
                finalDict["Organization"] = result.data["label"]

        if not finalDict["Barcode"] and "barcode" in result.data:
            finalDict["Barcode"] = result.data["barcode"]

        if "extraartists" in track.data:
            extraArtistsList = track.data["extraartists"]
            for extraArtist in extraArtistsList:
                if not finalDict["Lyricist"] and extraArtist["role"] == "Written-By":
                    finalDict["Lyricist"].append(extraArtist["name"])
                if not finalDict["Modified by"] and extraArtist["role"] == "Remix":
                    finalDict["Modified by"].append(extraArtist["name"])
                if not finalDict["Composer"] and extraArtist["role"] == "Composed By":
                    finalDict["Composer"].append(extraArtist["name"])
                if not not finalDict["Arranger"] and extraArtist["role"] == "Arranged By":
                    finalDict["Arranger"].append(extraArtist["name"])

        return finalDict


    def getByRecord(self, metadata, length=False):
        self.artistNeeded = False
        isRelease = False
        isAlbum = False
        finalDict = {
             'Album' : None,
             'Album Artist' : None,
             'Date' : None,
             'Original Date' : None,
             'Genre' : None,
             'Track Number' : None,
             'Disc Number' : None,
             'Catalog Number' : None,
             'Organization' : None,
             'Modified by' : [],
             'Composer' : [],
             'Lyricist' : [],
             'Length' : None,
             'Arranger' : [],
             'Barcode' : None
        };

        try:
            if "artist" in metadata and "title" in metadata:
                artist = FuzzyComparer.queryProcessor(' '.join(metadata["artist"]).strip())
                title = FuzzyComparer.queryProcessor(' '.join(metadata["title"]).strip())
                release = ''
                results = None
                if "album" in metadata and metadata["album"]:
                    release = ' '.join(metadata["album"]).strip()
                    isAlbum = True
                queryAlbum = artist + " " + release + " " + title
                queryNoAlbum = artist + " " + title
              
                if isAlbum:
                    results = self.client.search(query=queryAlbum, type="master")
                
                if not results or results.count == 0:
                    results = self.client.search(query=queryNoAlbum, type="master")

                if results.count == 0:
                    if isAlbum:
                        results = self.client.search(query=queryAlbum, type="release")
                    if results.count == 0:
                        results = self.client.search(query=queryNoAlbum, type="release")
                    if results.count > 0:
                        isRelease = True;
                    else:
                        return False
                        #raise ServiceError("404", "Song " + artist + " - " + title + " not found!")
            else:
                return False
        except discogs_client.exceptions.HTTPError as e:
            raise ServiceError(e.status_code, e.msg)

        if length:
            length = length*1000

        result = self.chooseFromResults(results, title, artist, isRelease, length)
        if not result:
            return False

        print("--------", self.counter)
        self.counter += 1
        finalDict = self.makeTagDict(result, title, artist, finalDict, isRelease)

        if not isRelease and result.main_release:
            finalDict = self.makeTagDict(result.main_release, title, artist, finalDict, isRelease)
        #print(str(finalDict))
        time.sleep(0.8)
        return finalDict