#command line tool utilizing the genius site to get lyrics

import lxml
from bs4 import BeautifulSoup
import argparse
import urllib3
import certifi

#urllib3.disable_warnings()
#https://genius.com/search?q=word1+word2  <-search
#https://genius.com/word1-word2-lyrics <- lyric at end for lyric urls

def yesOrNo(text=""):
    """Asks for user to input y or n. Returns true if y"""
    response = input(text + " (y/n)? ")
    return(response.lower() == "y")


parser = argparse.ArgumentParser()
parser.add_argument("searchTerms", help="terms for which you are searching")
args = parser.parse_args()
searchList = args.searchTerms.split(" ")
searchUrl = "https://genius.com/search?q="
for term in searchList:
    if term != "":
        searchUrl += (term + "+")
searchUrl = searchUrl[0:len(searchUrl)-1]
http = urllib3.PoolManager(
    cert_reqs= 'CERT_REQUIRED',
    ca_certs= certifi.where()
)
searchPage = http.request('GET', searchUrl)
searchPage = BeautifulSoup(searchPage.data, 'lxml')
resultList = searchPage.find_all('a', attrs={'class': ' song_link'})
optionList =  [] # list of possible song lyrics
urlList = [] # list of urls
for result in resultList:
    url = result.get('href')
    if url[len(url)-7:len(url)] == "-lyrics":
        lyricsUrl = url
        title = result.text
        optionList.append(title)
        urlList.append(url)

for i in range(len(optionList)):
    # removes newline characters from beginning and end
    optionList[i] = optionList[i][1:len(optionList[i])-1] 
    print(str(i) + ") " + optionList[i])
choice = int(input("Choose an option ( 0-" + str(len(optionList)-1) + " ): "))
if(choice < len(optionList) and choice >= 0):
    lyricsUrl = urlList[choice]
    lyricsPage = http.request('GET', lyricsUrl)
    lyricsPage = BeautifulSoup(lyricsPage.data, 'lxml')
    lyricsPage = http.request('GET', lyricsUrl)
    lyricsPage = BeautifulSoup(lyricsPage.data, 'lxml')
    lyrics = lyricsPage.find('lyrics',attrs={'class': 'lyrics'}).text
    print("\n" + optionList[choice])
    print(lyrics)
else:
    print("Not a valid option")
