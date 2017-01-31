import csv

import requests
import json

import time

tracksProcessed = []
def get_json(urlToHit):
    response = requests.get(urlToHit).text
    return json.loads(response)

def get_tracks(artist, data):
    for track in data:
        try:
            trackUrl = "http://api.deezer.com/track/{}".format(track["id"])
            print(trackUrl)
            trackInfo = get_json(trackUrl)

            trackId = trackInfo["id"]
            if trackId in tracksProcessed:
                continue

            url = trackInfo["preview"]

            f.write(format.format(trackId, artist, url))

            tracksProcessed.append(trackId)
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
artistsToClassify = csv.reader(open("artists.csv"))

for artist in artistsToClassify:
    trackSearchUrl = "http://api.deezer.com/artist/" + artist[0] + "/top?limit=1000"

    for index in range(100):
        print("Getting " + trackSearchUrl)
        try:
            jsonResponse = get_json(trackSearchUrl)
            get_tracks(artist[1], jsonResponse["data"])
        except KeyError:
            print("KeyError occurred on")
            time.sleep(3)
        except ValueError:
            print("ValueError occurred")
            time.sleep(5)
            continue
        if ("next" not in jsonResponse):
            break
        trackSearchUrl = jsonResponse["next"]

f.close()
