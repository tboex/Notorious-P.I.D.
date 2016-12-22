from bs4 import BeautifulSoup
import urllib3
import unicodedata
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

baseurl = "genius.com/artists/"
artist = "Andre-3000"

fullList = 'http://genius.com/artists/songs?for_artist_page=14266'
# this is for Andre 3000, gotta find ids? or simply just iterate from 1 - Cap? who knows
songTest = 'http://genius.com/Andre-3000-back-to-black-lyrics'
songTest2 = 'http://genius.com/Outkast-da-art-of-storytellin-part-1-lyrics'

# gotta use this to do full scroll.  VVV
#http://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho

'''
1) Use selenium to scrape urls of all songs,store in massive textfile
DONE 2) use BSoup to scrape those ps and text from <a> tags to ignore those shitty annotations
WIP 3) store those lyrics after sanitizing.
    remove any string that starts with \ like: \xe2\x80\x93

--------------------------------------------------------------------------

copy data and encode with rhyme algorithm
sort rhymes with directory structure
    meter -> end rhyme sound

--------------------------------------------------------------------------

Prompt for Rhyme scheme and first line, 
'''
def fiveSpace(lyricList):
    counter = 0
    for index, val in enumerate(lyricList):
        if val =='':
            counter+=1
            if counter >= 5:
                return lyricList[:index-4]
        else:
            counter=0
def twoSpace(lyricList):
    counter = 0
    for index, val in enumerate(lyricList):
        if val =='':
            counter+=1
            if counter >= 2:
                return lyricList[index+1:]
        else:
            counter=0
def Outro(lyricList):
    for index, val in enumerate(lyricList):
        if val == '[Outro]':
            return lyricList[:index]
    return lyricList
def bracket(lyricList):
    for index, val in enumerate(lyricList):
        if '[' in val:
            lyricList.pop(index)
    return lyricList

def sanitizeLyrics(lyricList): #TODO  IM sure there is a less cancer / regex way to do this, this is kind of a proof of concept rn.
    lyricList = fiveSpace(lyricList)
    lyricList = twoSpace(lyricList)
    lyricList = Outro(lyricList)
    lyricList = bracket(lyricList)
    return lyricList
def fetchLyrics(songUrl):
    lineList = []
    http = urllib3.PoolManager()
    response = http.request('GET', songUrl)
    soup = BeautifulSoup(response.data, "html.parser")
    for lyric in soup.find_all('div', class_="song_body-lyrics"):
        lyrics = lyric.getText()
    lineList = lyrics.splitlines()
    lineList = [x.encode('UTF8') for x in lineList]

    print sanitizeLyrics(lineList)

    return sanitizeLyrics(lineList)
def fetchArtists(artistUrl):
    urlList = []
    http = urllib3.PoolManager()
    response = http.request('GET', artistUrl)
    soup = BeautifulSoup(response.data, "html.parser")
    for a in soup.find_all('a', href=True):
        if 'http://genius.com/' in str(a['href']):
            urlList.append(str(a['href']))
            print "Found the URL:", a['href']
    return urlList
#fetchArtists(fullList)
fetchLyrics(songTest2)
