import re
import requests 
from pprint import pprint 
from bs4 import BeautifulSoup 
from datetime import datetime

import config as cfg


CMXBASEURL = "https://www.comixology.com/a/digital-comic/"

def buildComixologyURL(CMXID):
    return CMXBASEURL + CMXID

def parseReleaseDate(releaseDateElement, metadata):
    if releaseDateElement is not None:
        releaseDateStr = releaseDateElement.find_next_sibling().get_text(strip=True)
        releaseDate = datetime.strptime(releaseDateStr, '%B %d %Y')
        metadata['Year'] = releaseDate.year
        metadata['Month'] = releaseDate.month
        metadata['Day'] = releaseDate.day

def parseMultiple(soup):
    items = []
    for item in soup:
        items.append(item.get_text(strip=True))
    return items

def parseCMX(r, CMXID, debug = False):
    soup = BeautifulSoup(r.content, 'html.parser')

    metadata = {}

    # region content from head
    titleVolumeAndIssue = soup.find("meta", attrs={'name':'twitter:title'})['content']
    match = re.search('(.*?)( \((\d{4})-\d{0,4}\))? #(.*?)( \(of \d\))?$', titleVolumeAndIssue)
    metadata['series'] = match.group(1)
    metadata['volume'] = match.group(3)
    metadata['issue'] = match.group(4)

    if cfg.scrape['description']:
        metadata['description'] = soup.find("meta", attrs={'name':'description'})['content']
    if cfg.scrape['webLink']:
        metadata['webLink'] = soup.find("meta", attrs={'name':'url'})['content']
    if cfg.scrape['coverURL']:
        metadata['coverURL'] = soup.find("meta", attrs={'name':'image'})['content']
    # endregion


    #content from body
    if cfg.scrape['publisher']:
        metadata['publisher'] = soup.find("h3", attrs={'title':'Publisher'}).get_text(strip=True)

    # region credits
    if cfg.scrape['credits']:
        metadata['Writer'] = parseMultiple(soup.find_all("h2", attrs={'title':'Written by'}))
        metadata['Penciller'] = parseMultiple(soup.find_all("h2", attrs={'title':'Pencils'}))
        metadata['Inker'] = parseMultiple(soup.find_all("h2", attrs={'title':'Inks'}))
        metadata['Colorist'] = parseMultiple(soup.find_all("h2", attrs={'title':'Colored by'}))
        metadata['Cover'] = parseMultiple(soup.find_all("h2", attrs={'title':'Cover by'}))
        #artist is the same as both Penciller and Inker according to ComicTagger
        metadata['Penciller'] = parseMultiple(soup.find_all("h2", attrs={'title':'Art by'}))
        metadata['Inker'] = parseMultiple(soup.find_all("h2", attrs={'title':'Art by'}))
    # endregion

    if cfg.scrape['genres']:
        metadata['genres'] = parseMultiple(soup.find_all('a', href=re.compile('comics-genre')))

    if cfg.scrape['pageCount']:
        pageCount = soup.find("h4", text="Page Count").find_next_sibling().get_text(strip=True)
        pages = re.search('(.*) Pages', pageCount).group(1)
        metadata['pageCount'] = pages

    # region Release Date
    if cfg.scrape['releaseDate']:
        releaseDateElement = soup.find("h4", text="Print Release Date")
        if releaseDateElement is not None:
            parseReleaseDate(releaseDateElement, metadata)
        else:
            releaseDateElement = soup.find("h4", text="Digital Release Date")
            parseReleaseDate(releaseDateElement, metadata)
    # endregion

    if cfg.scrape['Notes']:
        metadata['Notes'] = "Tagged with Comixology-Scraper on {0}. [CMXDB{1}]".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            CMXID)

    if debug:
        pprint(metadata)

    return metadata

def byCMXID(CMXID, debug = False):
    return parseCMX(requests.get(buildComixologyURL(CMXID)), CMXID, debug)