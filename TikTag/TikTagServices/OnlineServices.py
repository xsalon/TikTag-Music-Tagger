from TikTagServices.DiscogsDB import DiscogsDB as Discogs
from TikTagServices.MusicBrainzDB import MusicBrainzDB as MusicBrainz
from TikTagServices.SpotifyDB import SpotifyDB as Spotify
from TikTagServices.GracenoteDB import GracenoteDB as Gracenote
from TikTagServices.ServiceError import *


class OnlineServices(object):
    SERVICES = ["Discogs", "Spotify", "Musicbrainz", "Gracenote"]

    def __init__(self, services):
        self.services = services
        self.clientDiscogs = None
        self.clientSpotify = None
        self.clientMusicbrainz = None
        self.clientGracenote = None

        
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
                self.clientMusicbrainz = "hej"

        if "Gracenote" in services:
            if not self.clientGracenote:
                self.clientGracenote = "hoo"


    def servicesStatus(self):
        if "Discogs" in self.services and not self.clientDiscogs:
            return False;
        if "Spotify" in self.services and not self.clientSpotify:
            return False;
        if "Musicbrainz" in self.services and not self.clientMusicbrainz:
            return False;
        if "Gracenote" in self.services and not self.clientGracenote:
            return False;
        return True

   
    def getTags(self, metadata):
        finalDict = {}
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
                        pass
                    elif service == "Gracenote":
                        pass
                except ServiceError as e:
                    if e.code == "404":
                        print(e.code, e.msg)
                    else:
                        raise ServiceError(e.code, e.msg)
        else:
            pass #fingerprinting
      
        return finalDict