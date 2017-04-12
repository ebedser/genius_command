#command line tool utilizing the genius site to get lyrics

import lxml
from bs4 import BeautifulSoup
import argparse
import urllib3

urllib3.disable_warnings()
#https://genius.com/search?q=word1+word2  <-search
#https://genius.com/word1-word2-lyrics <- lyric at end for lyric urls


parser = argparse.ArgumentParser()
parser.add_argument("song", help="the song for which you want lyrics")
args = parser.parse_args()
searchList = args.song.split(" ")
searchUrl = "https://genius.com/search?q="
for term in searchList:
    if term != "":
        searchUrl += (term + "+")
searchUrl = searchUrl[0:len(searchUrl)-1]
http = urllib3.PoolManager()
page = http.request('GET', searchUrl)
page = BeautifulSoup(page.data, 'lxml')
resultList = page.find_all('a', attrs={'class': ' song_link'})
lyricsUrl = ""
for result in resultList:
    url = result.get('href')
    if url[len(url)-7:len(url)] == "-lyrics":
        lyricsUrl = url
        break

lyricsPage = http.request('GET', lyricsUrl)
lyricsPage = BeautifulSoup(lyricsPage.data, 'lxml')

lyrics = lyricsPage.find('lyrics',attrs={'class': 'lyrics'}).text
print(lyrics)
