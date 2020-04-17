from scraping import *
import re
try:
    from pprint import pprint
except ImportError:
    pprint = print
import time

import config as cfg


CMXBASEURL = "https://www.comixology.com/a/digital-comic/"

def buildComixologyURL(CMXID):
    return CMXBASEURL + CMXID

def parseReleaseDate(releaseDateElement, metadata):
    if releaseDateElement is not None:
        releaseDateStr = getText(getNextSibling(releaseDateElement))
        releaseDate = time.strptime(releaseDateStr, '%B %d %Y')
        metadata['Year'] = releaseDate[0]
        metadata['Month'] = releaseDate[1]
        metadata['Day'] = releaseDate[2]

def parseMultiple(soup):
    items = []
    for item in soup:
        items.append(getText(item))
    return items

def parseCMX(r, CMXID, debug = False):
    soup = BeautifulSoup(r.content, 'html.parser')

    metadata = {}

    # region content from head
    titleVolumeAndIssue = findAttributeValue(findElement(soup, "meta", 'name', 'twitter:title'),'content')
    match = re.search('(.*?)( \((\d{4})-\d{0,4}\))? #(.*?)( \(of \d\))?$', titleVolumeAndIssue)
    if cfg.scrape['series']:
        metadata['series'] = match.group(1)
    if cfg.scrape['volume']:
        metadata['volume'] = match.group(3)
    if cfg.scrape['issue']:
        metadata['issue'] = match.group(4)

    if cfg.scrape['description']:
        metadata['description'] = findAttributeValue(findElement(soup, 'meta', 'name', 'description'), 'content')
    if cfg.scrape['webLink']:
        metadata['webLink'] = findAttributeValue(findElement(soup, 'meta', 'name', 'url'), 'content')
    if cfg.scrape['coverURL']:
        metadata['coverURL'] = findAttributeValue(findElement(soup, 'meta', 'name', 'image'), 'content')
    # endregion


    #content from body
    if cfg.scrape['publisher']:
        metadata['publisher'] = getText(findElement(soup, 'h3', 'title', 'Publisher'))

    # region credits
    if cfg.scrape['credits']:
        metadata['Writer'] = parseMultiple(findElements(soup, 'h2', 'title', 'Written by'))
        metadata['Penciller'] = parseMultiple(findElements(soup, 'h2', 'title', 'Pencils'))
        metadata['Inker'] = parseMultiple(findElements(soup, 'h2', 'title', 'Inks'))
        metadata['Colorist'] = parseMultiple(findElements(soup, 'h2', 'title', 'Colored by'))
        metadata['Cover'] = parseMultiple(findElements(soup, 'h2', 'title', 'Cover by'))
        #artist is the same as both Penciller and Inker according to ComicTagger
        artists = findElements(soup, 'h2', 'title', 'Art by')
        metadata['Penciller'] = parseMultiple(artists)
        metadata['Inker'] = parseMultiple(artists)
    # endregion

    if cfg.scrape['genres']:
        metadata['genres'] = parseMultiple(findElements(soup, 'a', 'href', 'comics-genre', substring=True))

    if cfg.scrape['pageCount']:
        pageCount = getText(getNextSibling(findElement(soup, 'h4', text='Page Count')))
        pages = re.search('(.*) Pages', pageCount).group(1)
        metadata['pageCount'] = pages

    # region Release Date
    if cfg.scrape['releaseDate']:
        releaseDateElement = findElement(soup, 'h4', text='Print Release Date')
        if releaseDateElement is not None:
            parseReleaseDate(releaseDateElement, metadata)
        else:
            releaseDateElement = findElement(soup, 'h4', text='Digital Release Date')
            parseReleaseDate(releaseDateElement, metadata)
    # endregion

    metadata['Notes'] = "Scraped metadata from Comixology [CMXDB{0}]".format(
        CMXID)

    if debug:
        pprint(metadata)

    return metadata

def byCMXID(CMXID, debug = False):
    return parseCMX(fetchWebPage(buildComixologyURL(CMXID)), CMXID, debug)