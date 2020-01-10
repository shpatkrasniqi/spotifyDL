# This script gets the links of the firts 30 songs on a spotify playlist and splits the song IDs for all of the songs.

import requests
from bs4 import BeautifulSoup
import html5lib
import html2text


# This function scrapes the provided spotify link 
def URLtoID():
    url = input('Enter Playlist URL: ')

    page = requests.get(url)           

    soup = BeautifulSoup(page.content, 'html5lib')

    uri=soup.findAll("meta", property="music:song")      
    
    uri2=[]

    # URL is seperated, taking only the song ID and putting them in a list
    for element in uri:
        uri2.append(str(element)[46:68])

    # All song IDs are put in a .txt file
    with open('listfile.txt', 'w') as filehandle:
        for listitem in uri2:
            filehandle.write('%s\n' % listitem)




















