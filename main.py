# This script downloads spotify songs through youtube

from __future__ import unicode_literals
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep
import spotifyScraper
import youtube_dl
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib.request

# Spotify API client credentials are put in
client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

spotifyScraper.URLtoID()

fullSongName=[]

max_tracks_per_call = 50
file = open('listfile.txt')

tids = file.read().split()
# Separating artist names and song names form every song link
for start in range(0, len(tids), max_tracks_per_call):
    results = sp.tracks(tids[start: start + max_tracks_per_call])
    for track in results['tracks']:
        fullSongName.append(track['name'] + '-' + track['artists'][0]['name'])

ytsearch=[]
ytsonglinks=[]
# Creating youtube search links for every song and putting them in a list
for i in fullSongName:
    yturl='https://www.youtube.com/results?search_query='+i.replace(" ", "%20").replace("-", "%20")
    ytsearch.append(yturl)
   
print('Getting Links...')

# Sraping youtube, taking the link of the first song of the search results and storing it in a list
for i in ytsearch:
    page = urllib.request.urlopen(i)

    soup = BeautifulSoup(page, 'html5lib')

    ytsong=soup.find("div", { "class" : "yt-lockup-content"})

    href= ytsong.find('a', href=True)

    ytsonglinks.append('https://www.youtube.com'+ href['href'])

    print('Links Acquired:',len(ytsonglinks))

# Setting up youtube_dl parameters
ydl_opts = {
    'outtmpl':'Songs/%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],}
    


# Using youtube_dl to download mp3 files from the links that we got
for x in ytsonglinks:
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([x])  
    except:
        pass

    

print ('\nF I N I S H E D ! ! !\n')


sleep(20)







            