import argparse
import urllib.parse
import re
import requests 
from bs4 import BeautifulSoup 

debug = False

CMXBASEURL = "https://www.comixology.com/a/digital-comic/"

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
    aResult = soup.find('a', href=re.compile('url\?q=https:\/\/www.comixology.com'))

    #for a in aResults:
    #    print(a.get_text(strip=True))
    #    print(a['href'])

    if aResult:
        matchCMXURL = re.search('url\?q=(.+?)[&?%]', aResult['href'])
        CMXURL = matchCMXURL.group(1)
        if debug:
            print(CMXURL) 

        matchCMXID = re.search('\/([0-9]+)$', CMXURL)
        CMXID = matchCMXID.group(1)
        if debug:
            print(CMXID)

        parseCMX(getResponseByID(CMXID))
    else:
      #not all series include the volume year
        print("no match found on google.com")

def findCMXURL(args):
    global debug
    debug = args.debug
    URL = buildGoogleQueryURL(args.series, args.volume, args.issue, args.format)
    r = requests.get(URL)
    parseGoogleResult(r)

def getResponseByID(CMXID):
  URL = CMXBASEURL + CMXID
  
  r = requests.get(URL) 
  return r

def parseCMX(r):
  
  soup = BeautifulSoup(r.content, 'html.parser') 

  title = soup.find('h1', class_='title')

  print(title.get_text(strip=True))

  aGenres = soup.find_all('a', href=re.compile('comics-genre'))

  genres = []

  for genre in aGenres:
    genres.append(genre.get_text(strip=True))

  genreList = ", ".join(genres)
  print(genreList)

def byCMXID(args):
  r = getResponseByID(args.CMXID)
  parseCMX(r) 


parser = argparse.ArgumentParser(description='Get genre string for a comic from Comixology.com')
subparser = parser.add_subparsers(help='sub-command help')

byID = subparser.add_parser('cmxid', help='cmxid -h', description='Get comic by CMXID')
byID.add_argument("CMXID", help="CMXID from comixology URL")
byID.set_defaults(func=byCMXID)

byname = subparser.add_parser('search', help='search -h', description='Get comic by name')
byname.add_argument("series", help="Comic Series name. e.g. Doctor Strange")
byname.add_argument("volume", help="Starting year for a volume. e.g. 2015")
byname.add_argument("issue", help="Issue Number. Don't include # sign")
byname.add_argument("--format", help="Don't include for regular series. \"Annual\" would be most common")
byname.add_argument("--debug", help="Output URLs being grabbed", action='store_true')
byname.set_defaults(func=findCMXURL)

#print help message if no args, then exit
if len(sys.argv)==1:
  parser.print_help(sys.stderr)
  sys.exit(1)

args = parser.parse_args()
args.func(args)