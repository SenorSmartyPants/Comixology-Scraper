import sys
import argparse
import re
import requests 
from pprint import pprint 
from bs4 import BeautifulSoup 
from datetime import datetime

import google

debug = False

CMXBASEURL = "https://www.comixology.com/a/digital-comic/"

def parseMultiple(soup):
  items = []
  for item in soup:
    items.append(item.get_text(strip=True))
  return items

def findCMXURL(args):
    CMXID = google.findCMXID(args)
    parseCMX(getResponseByID(CMXID), CMXID)

def getResponseByID(CMXID):
  URL = CMXBASEURL + CMXID
  
  r = requests.get(URL) 
  return r

def parseCMX(r, CMXID):
  soup = BeautifulSoup(r.content, 'html.parser')
  
  metadata = {}

  #content from head
  titleVolumeAndIssue = soup.find("meta", attrs={'name':'twitter:title'})['content']
  match = re.search('(.*?)( \((\d{4})-\d{0,4}\))? #(.*?)( \(of \d\))?$', titleVolumeAndIssue)
  metadata['series'] = match.group(1)
  if match.group(2) is not None:
    metadata['volume'] = match.group(3)
  metadata['issue'] = match.group(4)

  metadata['description'] = soup.find("meta", attrs={'name':'description'})['content']
  metadata['webLink'] = soup.find("meta", attrs={'name':'url'})['content']
  metadata['coverURL'] = soup.find("meta", attrs={'name':'image'})['content']


  #content from body
  metadata['publisher'] = soup.find("h3", attrs={'title':'Publisher'}).get_text(strip=True)
  #credits
  metadata['writer'] = parseMultiple(soup.find_all("h2", attrs={'title':'Written by'}))
  metadata['penciller'] = parseMultiple(soup.find_all("h2", attrs={'title':'Pencils'}))
  metadata['inker'] = parseMultiple(soup.find_all("h2", attrs={'title':'Inks'}))
  metadata['colorist'] = parseMultiple(soup.find_all("h2", attrs={'title':'Colored by'}))
  metadata['coverArtist'] = parseMultiple(soup.find_all("h2", attrs={'title':'Cover by'}))
  #is art by the same as penciller?
  metadata['artist'] = parseMultiple(soup.find_all("h2", attrs={'title':'Art by'}))
  metadata['genres'] = parseMultiple(soup.find_all('a', href=re.compile('comics-genre')))

  pageCount = soup.find("h4", text="Page Count").find_next_sibling().get_text(strip=True)
  pages = re.search('(.*) Pages', pageCount).group(1)
  metadata['pageCount'] = pages

  printDateStr = soup.find("h4", text="Print Release Date").find_next_sibling().get_text(strip=True)
  printDate = datetime.strptime(printDateStr, '%B %d %Y')
  metadata['Year'] = printDate.year
  metadata['Month'] = printDate.month
  metadata['Day'] = printDate.day

  metadata['Notes'] = "Tagged with Comixology-Scraper on {0}. [CMXDB{1}]".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            CMXID)


  pprint(metadata)

  return metadata

def byCMXID(args):
  r = getResponseByID(args.CMXID)
  parseCMX(r, args.CMXID) 


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