from TikTagServices.DiscogsDB import DiscogsDB as Discogs
from TikTagServices.MusicBrainzDB import MusicBrainzDB as MusicBrainz
from TikTagServices.SpotifyDB import SpotifyDB as Spotify
from TikTagServices.AcoustID import AcoustID
from TikTagServices.ServiceError import *


class OnlineServices(object):
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

   
    def getTags(self, metadata, enableFP=False ,path=None):
        finalDict = {}
        print("VNORENIE")
        print(metadata)
        print(" ")
        if "artist" in metadata and "title" in metadata:
            for service in self.services:
                try:
                    if service == "Discogs":
                        resultDiscogs = self.clientDiscogs.getByRecord(metadata)
                        if resultDiscogs:
                            for key, value in resultDiscogs.items():
                                if not key in finalDict or not finalDict[key]:
                                    finalDict[key] = value
                    elif service == "Spotify":
                        resultSpotify = self.clientSpotify.getByRecord(metadata)
                        if resultSpotify:
                            for key, value in resultSpotify.items():
                                if not key in finalDict or not finalDict[key]:
                                    finalDict[key] = value
                    elif service == "Musicbrainz":
                        resultMusicbrainz = self.clientMusicbrainz.getByRecord(metadata)
                        if resultMusicbrainz:
                            for key, value in resultMusicbrainz.items():
                                if not key in finalDict or not finalDict[key]:
                                    finalDict[key] = value
                except ServiceError as e:
                    if e.code == "404":
                        print(e.code, e.msg)
                    else:
                        raise ServiceError(e.code, e.msg)
            
            if not finalDict and not enableFP:
                return metadata
       
        elif enableFP and path:
            fingerprint = AcoustID()
            finalDict = fingerprint.getFingerprintedData(path)
            if finalDict:
                print("FINGERPRINT")
                print(finalDict)
                finalDict = self.getTags(finalDict, 0, path)
            else:
                return {}
        
        print("OUTPUT")
        print(finalDict)
        return finalDict