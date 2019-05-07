import spotipy
import spotipy.oauth2 as oauth2
import json
import spotipy
import sys

class SpotifyDB(object):
    def __init__(self):
        self.client_id = "18b12f99b644451f88d0460db3e35c74"
        self.client_secret = "94a01ec88f53412e83e62c4cd134486c"
        self.credentials = oauth2.SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        token = self.credentials.get_access_token()
        self.sp = spotipy.Spotify(auth=token)
    
    def getByRecord(self, metadata):   
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
            'Copyright' : []
        };

        if "artist" in metadata and "title" in metadata:
            artist = ' '.join(metadata["artist"]).strip()
            title = ' '.join(metadata["title"]).strip()
            query = artist + " " + title

            results = self.sp.search(q=query, limit=1, type="track")

            try:
                track = results["tracks"]["items"][0]
                album = self.sp.album(track["album"]["id"])
                features = self.sp.audio_features(track["id"])[0]
            except IndexError:
                return False

            #print(track)
            #print("---------------------------------------------------------------")
            #print(album)
            #print("---------------------------------------------------------------")
            #print(features)

        if track["name"]:
            finalDict["Title"] = track["name"]

        if track["artists"]:
            finalDict["Artist"] = [artist["name"] for artist in track["artists"]]

        if album["name"]:
            finalDict["Album"] = album["name"]

        if album["artists"]:
            finalDict["Album Artist"] = [artist["name"] for artist in album["artists"]]

        if album["release_date"]:
            finalDict["Date"] = album["release_date"]

        if album["genres"]:
            finalDict["Genre"] = album["genres"]

        if track["track_number"]:
            finalDict["Track Number"] = track["track_number"]

        if track["disc_number"]:
            finalDict["Disc Number"] = track["disc_number"]

        if features["tempo"]:
            finalDict["BPM"] = round(features["tempo"])

        if features["key"]:
            finalDict["Initial Key"] = features["key"]

        if track["external_ids"]["isrc"]:
            finalDict["ISRC"] = track["external_ids"]["isrc"]

        if album["copyrights"]:
            finalDict["Copyright"] = [right["text"] for right in album["copyrights"]]

        return finalDict