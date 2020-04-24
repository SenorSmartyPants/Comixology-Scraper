import re
from scraping import *
import time

def parseGoogleResult(URL, debug = False):
    sleepseconds = 5
    if debug:
        print('sleeping {0} seconds...'.format(sleepseconds))
    #wait X seconds so we don't hammer google and get blocked
    time.sleep(sleepseconds)

    soup = fetchWebPage(URL)

    #no page returned
    if not soup:
        if debug:
            #usually from 429, bot detected
            print("http status != 200")
        return -1 # don't keep searching

    #should be first result - if found
    aResult = findElement(soup, 'a', 'href', '.comixology.com', substring=True)

    if aResult:
        CMXURL = findAttributeValue(aResult, 'href')
        if debug:
            print("URL = " + CMXURL) 

        matchCMXID = re.search('\/([0-9]+)\??.*$', CMXURL)
        if matchCMXID:
            CMXID = matchCMXID.group(1)
            if debug:
                print("CMXID google result = {0}".format(CMXID))   
            return CMXID
    else:
      #not all series include the volume year
        if debug:
            print("no match found on google.com")
        return None
