from bs4 import BeautifulSoup
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Use Spotipy module to authenticate spotify account and grant access. docs : https://spotipy.readthedocs.io/en/2.13.0/
# #spotipy.oauth2.SpotifyOAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/",
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

# Gets user to input the date they are looking for in specified format
date = input("Which year do you want to travel to? Type the date in this format YYYYMMDD:")
# URL of the historical singles charts
URL = "https://www.officialcharts.com/charts/singles-chart/"

# Scrapes the URL of the year specified by the user (adding the date into the URL)
response = requests.get(f"{URL}{date}")
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")

# Creates empty list of song titles
song_titles = []

# Scrapes all song titles using name and class.
titles = soup.find_all(name="div", class_="title")

# Cycles through all the song titles and removes spaces at beginning and end of string with strip. Add them to the song
# titles list
for title in titles:
    song_titles.append(title.getText().strip())

# Empy list of URI (used to identify specific songs)
song_uris = []
year = date[0:4]

# Loops through the song titles and tries to located them on spotify by searching track name and year. Tries to append
# the URI to the song_uri's list, if not possible, skips to the next song.
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creates a
playlist = sp.user_playlist_create(user=user_id, name=f"top 100 from {date}", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

