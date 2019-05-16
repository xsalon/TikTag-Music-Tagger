# File: OnlineServices.py
# Project: TikTag
# Author: Marek Salon (xsalon00)
# Contact: xsalon00@stud.fit.vutbr.cz
# Date: 10.5.2019
# Description: Online services interface for utilitazing all services potencial

from TikTagServices.DiscogsDB import DiscogsDB as Discogs
from TikTagServices.MusicBrainzDB import MusicBrainzDB as MusicBrainz
from TikTagServices.SpotifyDB import SpotifyDB as Spotify
from TikTagServices.AcoustID import AcoustID
from TikTagServices.ServiceError import *
from datetime import datetime as dt


class OnlineServices(object):
    """Class for getting parsed informations from implemented services"""
    SERVICES = ["Discogs", "Spotify", "Musicbrainz"]

    def __init__(self, services):
        self.services = services
        self.clientDiscogs = None
        self.clientSpotify = None
        self.clientMusicbrainz = None

        
    def initServices(self, services, discogs_code=None):
        if "Discogs" in services:
            if not self.clientDiscogs and not discogs_code:
                self.clientDiscogs = Discogs()
                authUrl = self.clientDiscogs.getAuthUrl()
                raise ServiceRequirement("Discogs", "Authorization required", authUrl)
            elif self.clientDiscogs and discogs_code:
                try:
                    self.clientDiscogs.authorization(discogs_code)
                    self.clientDiscogs.identity()
                except ServiceError as e:
                    self.clientDiscogs = None
                    raise ServiceError(e.code, e.msg)

        if "Spotify" in services:
            if not self.clientSpotify:
                self.clientSpotify = Spotify()

        if "Musicbrainz" in services:
            if not self.clientMusicbrainz:
                self.clientMusicbrainz = MusicBrainz()


    def servicesStatus(self):
        if "Discogs" in self.services and not self.clientDiscogs:
            return False;
        if "Spotify" in self.services and not self.clientSpotify:
            return False;
        if "Musicbrainz" in self.services and not self.clientMusicbrainz:
            return False;
        return True


    def checkOriginalDateValid(self, metadata):
        if "Original Date" in metadata and metadata["Original Date"] and "Date" in metadata and metadata["Date"]:
            if len(str(metadata["Original Date"])) ==  10 and len(str(metadata["Date"])) == 10:
                date1 = dt.strptime(metadata["Original Date"], "%Y-%m-%d")
                date2 = dt.strptime(metadata["Date"], "%Y-%m-%d")
                return min(date1, date2)
            elif len(str(metadata["Original Date"])) ==  4 and len(str(metadata["Date"])) == 4:
                return min(int(metadata["Original Date"]), int(metadata["Date"]))
            elif len(str(metadata["Original Date"])) ==  4 and len(str(metadata["Date"])) == 10:
                date1 = dt.strptime(metadata["Original Date"] + "-12-30", "%Y-%m-%d")
                date2 = dt.strptime(metadata["Date"], "%Y-%m-%d")
                return min(date1, date2)
            elif len(str(metadata["Original Date"])) ==  10 and len(str(metadata["Date"])) == 4:
                date1 = dt.strptime(metadata["Original Date"], "%Y-%m-%d")
                date2 = dt.strptime(metadata["Date"] + "-12-30", "%Y-%m-%d")
                return min(date1, date2)
        return False

   
    def getTags(self, metadata, enableFP=False , path=None, length=False):
        finalDict = {}
        if "artist" in metadata and "title" in metadata:
            for service in self.services:
                try:
                    if service == "Discogs":
                        resultDiscogs = self.clientDiscogs.getByRecord(metadata, length)
                        if resultDiscogs:
                            for key, value in resultDiscogs.items():
                                if not key in finalDict or not finalDict[key]:
                                    finalDict[key] = value
                    elif service == "Spotify":
                        resultSpotify = self.clientSpotify.getByRecord(metadata, length)
                        if resultSpotify:
                            for key, value in resultSpotify.items():
                                if not key in finalDict or not finalDict[key]:
                                    finalDict[key] = value
                    elif service == "Musicbrainz":
                        resultMusicbrainz = self.clientMusicbrainz.getByRecord(metadata, length)
                        if resultMusicbrainz:
                            for key, value in resultMusicbrainz.items():
                                if not key in finalDict or not finalDict[key]:
                                    finalDict[key] = value
                except ServiceError as e:
                    raise ServiceError(e.code, e.msg)
            
            if not finalDict and not enableFP:
                return metadata
       
        elif enableFP and path:
            fingerprint = AcoustID()
            finalDict = fingerprint.getFingerprintedData(path)
            if finalDict:
                finalDict = self.getTags(finalDict, 0, path)
            else:
                return {}

        originalDate = self.checkOriginalDateValid(finalDict)
        if originalDate:
            if len(str(originalDate)) > 3:
                originalDate = str(originalDate)[:4]
            finalDict["Original Date"] = originalDate

        if not "Title" in finalDict or finalDict["Title"]:
            if "title" in metadata and metadata["title"]:
                finalDict["Title"] = metadata["title"]

        if not "Artist" in finalDict or finalDict["Artist"]:
            if "artist" in metadata and metadata["artist"]:
                finalDict["Artist"] = metadata["artist"]

        #print(finalDict)      
        return finalDict