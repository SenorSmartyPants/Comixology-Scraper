from url_utils import UrlPathEncode
from parseGoogle import parseGoogleResult

GOOGLEURL = "https://www.google.com/search?q="
GOOGLEBASESEARCH = "site:comixology.com inurl:digital-comic intitle:\"{0} ({1}\" intitle:\"#{2}\""
COMICFORMATSEARCH = ' intitle:{0}'

def buildGoogleQueryURL(series, volume, issue, format, debug = False):
    QS = GOOGLEBASESEARCH.format(series, volume, issue)
    if format and format == 'Annual':
        QS += COMICFORMATSEARCH.format(format)

    QS = UrlPathEncode(QS)
    URL = GOOGLEURL + QS
    if debug:
        print(URL)
    return URL

def googleSeries(series, volume, issue, format, debug = False):
    URL = buildGoogleQueryURL(series, volume, issue, format)
    if debug:
        print(URL) 
    return parseGoogleResult(URL, debug)

def findCMXID(series, volume, issue, format, debug = False):
    CMXID = googleSeries(series, volume, issue, format, debug)
    if CMXID is None:
        #try without volume, if one was passed in
        if debug:
            print("Trying without volume")
        CMXID = googleSeries(series, "", issue, format, debug)
    return CMXID
