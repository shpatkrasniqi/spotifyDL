# This script downloads spotify songs through youtube
from __future__ import unicode_literals
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep
import youtube_dl
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib.request
import urllib.parse
import re


# This function scrapes the provided spotify link 
def URLtoID(url):

    page = requests.get(url)           

    soup = BeautifulSoup(page.content, 'html5lib')

    uri=soup.findAll("meta", property="music:song")      
    
    uri2=[]

    # URL is seperated, taking only the song ID and putting them in a list
    for element in uri:
        uri2.append(str(element)[46:68])

    return uri2

link = input('Enter Playlist URL: ')

# Spotify API client credentials are put in
client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

idlist=URLtoID(link)

fullSongName=[]

max_tracks_per_call = 30

# Separating artist names and song names form every song link
for start in range(0, len(idlist), max_tracks_per_call):
    results = sp.tracks(idlist[start: start + max_tracks_per_call])
    for track in results['tracks']:
        fullSongName.append(track['name'] + '-' + track['artists'][0]['name'])

ytsearch=[]
ytsonglinks=[]

# Creating youtube search links for every song and putting them in a list
for i in fullSongName:
    yturl='https://www.youtube.com/results?search_query='+i.replace(" ", "%20").replace("-", "%20")
    ytsearch.append(yturl)
   
print('Getting Links...')

# Sraping youtube, taking the link of the second song of the search results and storing it in a list
for i in ytsearch:
    
    page = urllib.request.urlopen(i)
    
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', page.read().decode())
    
    ytsonglinks.append("http://www.youtube.com/watch?v=" + search_results[1])
    
    print('Links Acquired:',len(ytsonglinks))

# Setting up youtube_dl parameters
ydl_opts = {
    'outtmpl':'Songs/%(title)s.%(ext)s',
    'extractaudio' : True,
    'format': 'bestaudio/best',
    'noplaylist' : True,
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
