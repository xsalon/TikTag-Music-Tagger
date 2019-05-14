import spotipy
from TikTagServices.FuzzyComparer import FuzzyComparer
from datetime import datetime as dt
import spotipy.oauth2 as oauth2
import json
import sys

class SpotifyDB(object):
    SUBSTRINGS = ["feat.", "feat", "featuring", "ft", "ft.", "mix", "original", "extended", "edit", "radio", "ost", ]
    def __init__(self):
        self.client_id = "18b12f99b644451f88d0460db3e35c74"
        self.client_secret = "94a01ec88f53412e83e62c4cd134486c"
        self.credentials = oauth2.SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        token = self.credentials.get_access_token()
        self.sp = spotipy.Spotify(auth=token)
        #self.counter = 0


    def chooseResult(self, item, title, artist, length, album=None):
        if "artists" in item and item["artists"]:
            if FuzzyComparer.fuzzComparer(' '.join([artist["name"] for artist in item["artists"]]), artist):
                if "name" in item and FuzzyComparer.fuzzComparer(item["name"], title):
                    okStatus = True
                    if "duration_ms" in item and length:
                        if FuzzyComparer.durationCompare(item["duration_ms"], length):
                             okStatus = True
                        else:
                             okStatus = False
                    if album:
                        if "album" in item and FuzzyComparer.fuzzComparer(item["album"]["name"], title):
                            okStatus = True
                        else:
                            okStatus = False
                    return okStatus

    
    def getByRecord(self, metadata, length=False): 
        finalDict = {
            'Title' : None,
            'Artist' : [],
            'Album' : None,
            'Album Artist' : [],
            'Date' : None,
            'Genre' : [],
            'Track Number' : None,
            'Disc Number' : None,
            'BPM' : None,
            'Initial Key' : None,
            'ISRC' : None,
            'Copyright' : [],
            'Length' : [],
            'Mood' : None
        };

        if "artist" in metadata and "title" in metadata:
            artist = FuzzyComparer.queryProcessor(' '.join(metadata["artist"]).strip())
            title = FuzzyComparer.queryProcessor(' '.join(metadata["title"]).strip())
            query = artist + " " + title
            album = None
            tracks = []
            if "album" in metadata and metadata["album"]:
                album = ' '.join(metadata["album"]).strip()

            results = self.sp.search(q=query, limit=10, type="track")
            #print(length)
            
            if length:
                length = length*1000
            
            for item in results["tracks"]["items"]:
                if album:
                    if self.chooseResult(item, title, artist, length, album):
                        tracks.append(item)
                else:
                    if self.chooseResult(item, title, artist, length):
                        tracks.append(item)

            if not tracks and album:
                for item in results["tracks"]["items"]:
                    if self.chooseResult(item, title, artist, length):
                        tracks.append(item)

            if not tracks:
                return False

            lowDate = "3000-12-30"
            index = 0
            for i, trackItem in enumerate(tracks):
                if "release_date" in trackItem:
                    if trackItem["release_date_precision"] == "day":
                        date1 = dt.strptime(trackItem["release_date"], "%Y-%m-%d")
                        date2 = dt.strptime(lowDate, "%Y-%m-%d")
                    elif trackItem["release_date_precision"] == "year":
                        date1 = dt.strptime(trackItem["release_date"] + "-12-30", "%Y-%m-%d")
                        date2 = dt.strptime(lowDate, "%Y-%m-%d")
                    else:
                        continue
                    if date2 > date1:
                        if len(releaseItem["date"]) == 4:
                            lowDate = releaseItem["date"] + "-12-30"
                        else:
                            lowDate = releaseItem["date"]
                        index = i

            track = tracks[index]
            if not track:
                return False

            try:
                album = self.sp.album(track["album"]["id"])
                features = self.sp.audio_features(track["id"])[0]
            except IndexError:
                return False

        if "duration_ms" in track and track["duration_ms"]:
            finalDict["Length"] = track["duration_ms"]

        if "name" in track and track["name"]:
            finalDict["Title"] = track["name"]

        if "name" in track and track["artists"]:
            finalDict["Artist"] = [artist["name"] for artist in track["artists"]]

        if "name" in album and album["name"]:
            finalDict["Album"] = album["name"]

        if "artists" in album and album["artists"]:
            finalDict["Album Artist"] = [artist["name"] for artist in album["artists"]]

        if "release_date" in album and album["release_date"]:
            finalDict["Date"] = album["release_date"]

        if "genres" in album and album["genres"]:
            finalDict["Genre"] = album["genres"]

        if "track_number" in track and track["track_number"]:
            finalDict["Track Number"] = track["track_number"]

        if "disc_number" in track and track["disc_number"]:
            finalDict["Disc Number"] = track["disc_number"]

        if "tempo" in features and features["tempo"]:
            finalDict["BPM"] = round(features["tempo"])

        if "key" in features and features["key"]:
            finalDict["Initial Key"] = features["key"]

        if "external_ids" in track and track["external_ids"]["isrc"]:
            if "isrc" in track["external_ids"] and track["external_ids"]["isrc"]:
                finalDict["ISRC"] = track["external_ids"]["isrc"]

        if "copyrights" in album and album["copyrights"]:
            finalDict["Copyright"] = [right["text"] for right in album["copyrights"]]

        if "valence" in features and features["valence"]:
            finalDict["Mood"] = features["valence"]

        #self.counter += 1
        #print(self.counter)
        return finalDict