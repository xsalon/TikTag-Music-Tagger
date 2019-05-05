import musicbrainzngs

class MusicBrainzDB(object):
    def _init_(self, name, password):
        self.name = name
        self.password = password
        musicbrainzngs.set_useragent("TikTag", "1.0")

    def getByRecord(self, path):
        try:
            result = musicbrainzngs.get_recording_by_id("7d4afa1f-cdd4-4b8d-b783-becba69fb903", ["artists"])
        except WebServiceError as exc:
               print("Something went wrong with the request: %s" % exc)
        else:
            print(str(result))