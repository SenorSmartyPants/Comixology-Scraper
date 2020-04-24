import re
from scraping import *

def parseGoogleResult(URL, debug = False):
    soup = fetchWebPage(URL)
    #should be first result - if found
    aResult = soup.find('a', href=re.compile('url\?q=https:\/\/(www|m).comixology.com'))

    if aResult:
        matchCMXURL = re.search('url\?q=(.+?)[&?%]', findAttributeValue(aResult, 'href'))
        CMXURL = matchCMXURL.group(1)
        if debug:
            print("URL = " + CMXURL) 

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
