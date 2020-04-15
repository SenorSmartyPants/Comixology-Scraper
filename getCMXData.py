import re
import requests 
from pprint import pprint 
from bs4 import BeautifulSoup 
from datetime import datetime



CMXBASEURL = "https://www.comixology.com/a/digital-comic/"

def buildComixologyURL(CMXID):
  return CMXBASEURL + CMXID

def parseMultiple(soup):
  items = []
  for item in soup:
    items.append(item.get_text(strip=True))
  return items

def parseCMX(r, CMXID, debug = False):
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

  if debug:
    pprint(metadata)

  return metadata

def byCMXID(CMXID, debug = False):
    return parseCMX(requests.get(buildComixologyURL(CMXID)), CMXID, debug)