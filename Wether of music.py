# Script gives weather conditions occuring in place possible to connect to some of band text.
# Code base on three API: openweathermap.org, geocode.xyz and theaudiodb.com

import requests


def weather_of_music():
    while True:
        author = get_artist()                           # Takes artist name from user
        art_id = get_art_id(author)
        if art_id:                                      # Check is the artist in theaudiodb.com database
            albums = get_discs(art_id)
            songs = get_tracks(albums)
            for song in songs:
                lyrics = get_text(song, author)
                places = get_locs(lyrics)               # Takes locations listed in texts
                for place in places:
                    conditions = get_weather(place)     # Takes weather in founded locations
                    if conditions:
                        weather = conditions["weather"]
                        sentence = f"{author} gives {weather}, because of {place} mentioned in {song}"
                        return sentence
                    else:
                        continue
        else:                                           # Script end while artist is not found
            sentence = "Sorry, this author is no more."
            return sentence


def get_artist():
    author = input("Enter artist or band:\n")
    return author


def get_art_id(artist):
    url = "https://theaudiodb.com/api/v1/json/1/search.php"
    query = artist
    context = {"s": query}
    response = requests.get(url, context)
    output = response.json()
    if output["artists"]:
        return output["artists"][0]["idArtist"]
    else:
        return False


def get_discs(art_id):
    url = "https://theaudiodb.com/api/v1/json/1/album.php"
    query = art_id
    context = {"i": query}
    response = requests.get(url, context)
    output = response.json()
    discography = output["album"]
    discs = []
    for disc in discography:
        disc_id = disc['idAlbum']
        discs.append(disc_id)
    return discs


def get_tracks(albums):
    titles = []
    for album in albums:
        url = "https://theaudiodb.com/api/v1/json/1/track.php"
        query = album
        context = {"m": query}
        response = requests.get(url, context)
        output = response.json()
        tracks = output["track"]
        for track in tracks:
            title = track["strTrack"]
            titles.append(title)
    return titles


def get_text(song, autor):
    while True:
        url = f"https://api.lyrics.ovh/v1/{autor}/{song}"
        response = requests.get(url)
        if response.ok:
            output = response.json()
            text = output["lyrics"]
            return text
        else:
            return None


def get_locs(lyrics):
    while True:
        loc_lst = []
        query = lyrics
        response = requests.post(
            'https://geocode.xyz',
            {
                'sentiment': 'analysis',
                'geoit': 'json',
                'scantext': query,
            }
        )
        if response.status_code == 200:
            output = response.json()
            if type(output['match']) == list:
                for loc in output['match']:
                    loc_lst.append(loc["location"])
                    return loc_lst
            elif type(output['match']) == dict:
                loc_lst.append(output["match"]["location"])
                return loc_lst
        elif response.status_code == 403 and response.json()['error']['code'] == "006":
            # print("Error 403 code 006 handled")
            continue
        elif response.status_code == 403 and response.json()['error']['code'] == "008":
            # print("Error 403 code 008 handled")
            continue
        else:
            print("else")
            break
        return loc_lst


def get_weather(place):
    while True:
        url = "https://api.openweathermap.org/data/2.5/weather"
        api_key = ""    # Enter your API key for openweathermap.org
        context = {"appid": api_key, "q": place}
        response = requests.get(url, context)
        if response.status_code == 200:
            output = {"weather": response.json()['weather'][0]['main'], "place": place}
            return output
        else:
            return False


print(weather_of_music())
