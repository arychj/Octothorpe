# Must be run on machine running spotify client
# based on https://github.com/nih0/spotify-local-http-api

import ssl
from string import ascii_lowercase
from random import choice
import urllib
import json
import time

from ..Service import Service

class Spotify(Service):
    _oauth_token = None
    _csrf_token = None
    _request_context = None

    _port = 4370
    DEFAULT_RETURN_ON = ["login", "logout", "play", "pause", "error", "ap"]

    def Play(self, artist="", track=""):
        if(len(artist) == 0):
            return self.Pause(False)
        else:
            if(len(track) > 0):
                tracks = self._search("track", {"artist": artist, "track": track})
                if(len(tracks) > 0):
                    self._call("/remote/play.json", {
                        "uri": tracks[0]["uri"],
                        "context": tracks[0]["uri"],
                    })

                    self.Log(f"Playing track {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}")

                    return {"now_playing": f"{tracks[0]['name']} by {tracks[0]['artists'][0]['name']}"}
                else:
                    return {"error": "unknown song"}
            else:
                artists = self._search("artist", {"artist": artist})
                if(len(artists) > 0):
                    self._call("/remote/play.json", {
                        "uri": artists[0]["uri"],
                        "context": artists[0]["uri"],
                    })

                    self.Log(f"Playing artist {artists[0]['name']}")
                    return {"now_playing": artists[0]["name"]}
                else:
                    return {"error": "unknown artist"}

    #this should be an injector
    def Status(self):
        return self._call("/remote/status.json", {
            "returnafter": 59,
            "returnon": ",".join(Spotify.DEFAULT_RETURN_ON)
        })

    def Pause(self, pause=True):
        self._call("/remote/pause.json", {
            "pause": "true" if pause else "false"
        })

        return {"state": "paused" if pause else "playing"}

    def Unpause(self):
        return self.Pause(False)

    def Stop(self):
        return self.Pause()

    def _search(self, type, query, broader=False):
        self.Debug(f"Searching for '{query}'")

        q = ""
        for term, value in query.items():
            if(broader):
                q += f"{term}:{value.replace(' ', '*')} "
            else:
                q += f"{term}:{value} "

        q = q.strip()

        results = self._call(
            url= "api://search", 
            params = {
                "type": type,
                "q": q
            },
            authenticated=False
        )

        items = results[f"{type}s"]["items"]
        if(len(items) == 0 and broader == False):
            self.Debug("No results found, broadening search")
            return self._search(type, query, True)
        else:
            return items

    def _call(self, url, params={}, authenticated=True):
        if(authenticated):
            params["oauth"] = self._get_oauth_token()
            params["csrf"] = self._get_csrf_token()

        url = self._build_url(url) + "?" + urllib.parse.urlencode(params)
        request = urllib.request.Request(url, headers = {"Origin": self.Settings.GetString("origin_header")})

        return json.loads(urllib.request.urlopen(request, context=Spotify._get_request_context()).read())

    def _build_url(self, url):
        if(url.startswith("http")):
            return url
        elif(url.startswith("api://")):
            return self.Settings.GetString("api_base_endpoint") + "/" + url[6:]
        else:
            return "https://%s:%d%s" % ("localhost.spotilocal.com", self.Settings.GetInt("port"), url)

    def _get_oauth_token(self):
        if(Spotify._oauth_token == None):
            Spotify._oauth_token = self._call(self.Settings.GetString("oauth_provider"), authenticated=False)["t"]

        return Spotify._oauth_token

    def _get_csrf_token(self):
        if(Spotify._csrf_token == None):
            Spotify._csrf_token = self._call("/simplecsrf/token.json", authenticated=False)["token"]
         
        return Spotify._csrf_token

    @classmethod
    def _get_request_context(cls):
        if(cls._request_context == None):
            cls._request_context = ssl.create_default_context()
            cls._request_context.check_hostname = False
            cls._request_context.verify_mode = ssl.CERT_NONE

        return cls._request_context

    @classmethod
    def _get_version(cls):
        return cls._call("/service/version.json", params={"service": "remote"})

#    def open_spotify_client():
#        return get(_build_url("/remote/open.json"), headers=ORIGIN_HEADER).text

