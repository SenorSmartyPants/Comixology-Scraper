import urllib.parse
import re
import requests 
from bs4 import BeautifulSoup 

debug = False

GOOGLEURL = "https://www.google.com/search?q="
GOOGLEBASESEARCH = "site:comixology.com inurl:digital-comic intitle:\"{0} ({1}\" intitle:\"#{2}\""
COMICFORMATSEARCH = ' intitle:{0}'

def buildGoogleQueryURL(series, volume, issue, format):
    global debug

    QS = GOOGLEBASESEARCH.format(series, volume, issue)
    if format:
        QS += COMICFORMATSEARCH.format(format)

    QS = urllib.parse.quote(QS)
    
    URL = GOOGLEURL + QS
    if debug:
        print(URL)
    return URL

def parseGoogleResult(r, debug = False):

    soup = BeautifulSoup(r.content, 'html.parser')
    #should be first result - if found
    aResult = soup.find('a', href=re.compile('url\?q=https:\/\/(www|m).comixology.com'))

    if aResult:
        matchCMXURL = re.search('url\?q=(.+?)[&?%]', aResult['href'])
        CMXURL = matchCMXURL.group(1)
        if debug:
            print(CMXURL) 

        matchCMXID = re.search('\/([0-9]+)$', CMXURL)
        CMXID = matchCMXID.group(1)
        if debug:
            print(CMXID)

        return CMXID
    else:
      #not all series include the volume year
        if debug:
            print("no match found on google.com")
        return None

def googleSeries(series, volume, issue, format, debug = False):
    URL = buildGoogleQueryURL(series, volume, issue, format)
    if debug:
        print(URL) 
    r = requests.get(URL)
    return parseGoogleResult(r, debug)

def findCMXID(series, volume, issue, format, debug = False):
    CMXID = googleSeries(series, volume, issue, format, debug)
    if CMXID is None:
        #try without volume, if one was passed in
        if debug:
            print("Trying without volume")
        CMXID = googleSeries(series, "", issue, format, debug)
    return CMXID
