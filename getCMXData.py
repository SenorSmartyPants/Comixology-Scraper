from scraping import *
import re
try:
    from pprint import pprint
except ImportError:
    def pprint(x):
        print(x)
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
    if soup is not None:
        for item in soup:
            items.append(getText(item))
    if len(items) > 0:
        return items

def appendIfNotNone(list, key, value):
    if value is not None:
        list[key] = value

def parseCMX(CMXID, debug = False):
    soup = fetchWebPage(buildComixologyURL(CMXID))

    metadata = {}

    # region content from head
    titleVolumeAndIssue = findAttributeValue(findElement(soup, "meta", 'name', 'twitter:title'),'content')
    match = re.search('(.*?)( \((\d{4})-\d{0,4}\))? #(.*?)( \(of \d\))?$', titleVolumeAndIssue)
    if cfg.scrape['series']:
        metadata['series'] = match.group(1)
    if cfg.scrape['volume']:
        appendIfNotNone(metadata, 'volume', match.group(3))
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
        appendIfNotNone(metadata, 'publisher', getText(findElement(soup, 'h3', 'title', 'Publisher')))

    # region credits
    if cfg.scrape['credits']:
        appendIfNotNone(metadata, 'Writer', parseMultiple(findElements(soup, 'h2', 'title', 'Written by')))
        appendIfNotNone(metadata, 'Penciller', parseMultiple(findElements(soup, 'h2', 'title', 'Pencils')))
        appendIfNotNone(metadata, 'Inker', parseMultiple(findElements(soup, 'h2', 'title', 'Inks')))
        appendIfNotNone(metadata, 'Colorist', parseMultiple(findElements(soup, 'h2', 'title', 'Colored by')))
        appendIfNotNone(metadata, 'Cover', parseMultiple(findElements(soup, 'h2', 'title', 'Cover by')))
        #artist is the same as both Penciller and Inker according to ComicTagger
        artists = parseMultiple(findElements(soup, 'h2', 'title', 'Art by'))
        appendIfNotNone(metadata, 'Penciller', artists)
        appendIfNotNone(metadata, 'Inker', artists)
    # endregion

    if cfg.scrape['genres']:
        appendIfNotNone(metadata, 'genres', parseMultiple(findElements(soup, 'a', 'href', 'comics-genre', substring=True)))

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
    return parseCMX(CMXID, debug)