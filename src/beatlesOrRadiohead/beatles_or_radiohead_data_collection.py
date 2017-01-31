import urllib.request
import json

from dateutil.parser import parse
import time
import urllib.error

tracksProcessed = []
def get_json(urlToHit):
    time.sleep(2)
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

            name = trackInfo["artist"]["name"]
            url = trackInfo["preview"]

            f.write(format.format(trackId, name, url))

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



format = '{},{},{}\n'
f = open('sample_band_data.csv', 'w')
f.write(format.format("id", "decade", "explicit lyrics", "sample url"))

for band in ["beatles", "radiohead"]:
    trackSearchUrl = "http://api.deezer.com/search?q=artist:"+band

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
        if ("next" not in jsonResponse):
            break
        trackSearchUrl = jsonResponse["next"];

f.close()
