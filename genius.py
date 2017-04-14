#command line tool utilizing the genius site to get lyrics

import lxml, argparse, urllib3, certifi, sys
from bs4 import BeautifulSoup
from termcolor import colored, cprint

#https://genius.com/search?q=word1+word2  <-search
#https://genius.com/word1-word2-lyrics <- lyric at end for lyric urls

# not implemented yet
help = """
usage: genius.py [-h] [-m] [-b] S [S ...]

positional arguments:
S             the search terms

optional arguments:
-h, --help    show this help message and exit
-m            use menu for song selection
-b            bolds titles
"""

def yesOrNo(text=""):
    """Asks for user to input y or n. Returns true if y"""
    response = input(text + " (y/n)? ")
    return(response.lower() == "y")

def cleanNonAlNum(aString):
    newString = ""
    for i in aString:
        if(i.isalnum()):
            newString += i
    return newString
#cprint('[Chorus]', 'white', attrs=['bold'], end=' ')
def formatText(inputText):
    textList = inputText.split('\n')
    for line in textList:
        print(line)

# get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("searchTerms", help="terms for which you are searching")
args = parser.parse_args()
searchList = args.searchTerms.split(" ")

# set up urllib3 with cirtifi certificates
http = urllib3.PoolManager(
    cert_reqs= 'CERT_REQUIRED',
    ca_certs= certifi.where()
)

# create the initial url for the search on genius
searchUrl = "https://genius.com/search?q="
for term in searchList:
    if term != "":
        searchUrl += (term + "+")

searchUrl = searchUrl[0:len(searchUrl)-1] # remove the last '+' from the url

# get page with search results
searchPage = http.request('GET', searchUrl)
searchPage = BeautifulSoup(searchPage.data, 'lxml')
resultList = searchPage.find_all('a', attrs={'class': ' song_link'})
optionList =  [] # list of possible song lyrics
urlList = [] # list of urls
for result in resultList: # checks if the results are lyrics-results or articles
    url = result.get('href')
    if url[len(url)-7:len(url)] == "-lyrics":
        lyricsUrl = url
        title = result.text
        optionList.append(title)
        urlList.append(url)

for i in range(len(optionList)): # create option list
    # removes newline characters from beginning and end
    optionList[i] = optionList[i][1:len(optionList[i])-1] 
    print(str(i) + ") " + optionList[i])

choice = int(input("Choose an option ( 0-" + str(len(optionList)-1) + " ): "))

if(choice < len(optionList) and choice >= 0): # get and display chosen lyrics
    lyricsUrl = urlList[choice]
    lyricsPage = http.request('GET', lyricsUrl)
    lyricsPage = BeautifulSoup(lyricsPage.data, 'lxml')
    lyricsPage = http.request('GET', lyricsUrl)
    lyricsPage = BeautifulSoup(lyricsPage.data, 'lxml')
    lyrics = lyricsPage.find('lyrics',attrs={'class': 'lyrics'}).text
    print("\n" + optionList[choice])
    formatText(lyrics)
    #print(lyrics)
else:
    print("Not a valid option")

print(cleanNonAlNum("Joey Bada$$"))

