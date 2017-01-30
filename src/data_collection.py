import urllib.request
import json

import math
from dateutil.parser import parse
import time
import urllib.error
from string import ascii_lowercase

tracksProcessed = []
def get_json(urlToHit):
    response = urllib.request.urlopen(urlToHit).read()
    return json.loads(response)

def get_tracks(data):
    for track in data:
        try:
            trackUrl = "http://api.deezer.com/track/{}".format(track["id"])
            print(trackUrl)
            trackInfo = get_json(trackUrl)

            trackId = trackInfo["id"]
            if trackId in tracksProcessed:
                continue

            date = parse(trackInfo["release_date"])
            decade = math.floor(date.year/10)*10
            url = trackInfo["preview"]
            explicitLyrics = trackInfo["explicit_lyrics"]

            f.write(format.format(trackId, decade, explicitLyrics, url))

            tracksProcessed.append(trackId)
        except urllib.error.HTTPError:
            print("HTTPError occurred on: " + trackUrl)
            time.sleep(3)
        except KeyError:
            print("KeyError occurred on: " + trackUrl)
            time.sleep(3)
        except ValueError:
            print("ValueError occurred")
            time.sleep(5)
            continue
        except ConnectionResetError:
            print("ConnectionResetError occurred")
            continue



format = '{},{},{},{}\n'
f = open('sample_data.csv', 'w')
f.write(format.format("id", "decade", "explicit lyrics", "sample url"))

for letter in ascii_lowercase:
    trackSearchUrl = "http://api.deezer.com/search?q=track:"+letter

    for index in range(100):
        print("Getting " + trackSearchUrl)
        try:
            jsonResponse = get_json(trackSearchUrl)
            get_tracks(jsonResponse["data"])
        except urllib.error.HTTPError:
            print("HTTPError occurred on")
            time.sleep(3)
        except KeyError:
            print("KeyError occurred on")
            time.sleep(3)
        except ValueError:
            print("ValueError occurred")
            time.sleep(5)
            continue
        except ConnectionResetError:
            print("ConnectionResetError occurred")
            continue
        if ("next" not in jsonResponse):
            break
        trackSearchUrl = jsonResponse["next"];

f.close()
