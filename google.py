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

def parseGoogleResult(r):
    global debug

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

def googleSeries(series, volume, issue, format):
    URL = buildGoogleQueryURL(series, volume, issue, format)
    r = requests.get(URL)
    return parseGoogleResult(r)

def findCMXID(args):
    global debug
    debug = args.debug
    CMXID = googleSeries(args.series, args.volume, args.issue, args.format)
    if CMXID is None:
        #try without volume, if one was passed in
        if debug:
            print("Trying without volume")
        CMXID = googleSeries(args.series, "", args.issue, args.format)
    return CMXID
