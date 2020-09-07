import re
from scraping import *

def parseGoogleResult(URL, debug = False):
    soup = fetchWebPage(URL)

    #no page returned
    if not soup:
        if debug:
            #usually from 429, bot detected
            print("http status != 200")
        return -1

    #should be first result - if found
    aResult = soup.find('a', href=re.compile('https:\/\/(www|m).comixology.com'))

    if aResult:
        CMXURL = findAttributeValue(aResult, 'href')
        if debug:
            print("URL = " + CMXURL) 

        matchCMXID = re.search('\/([0-9]+)\??.*$', CMXURL)
        CMXID = matchCMXID.group(1)
        if debug:
            print("CMXID google result = {0}".format(CMXID))  

        return CMXID
    else:
      #not all series include the volume year
        if debug:
            print("no match found on google.com")
        return None
