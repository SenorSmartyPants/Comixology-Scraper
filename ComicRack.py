from utils import *
from System import DateTime
from System.IO import Path

import getCMXData
import config as cfg

#@Name	Comixology Scraper
#@Hook	Books
#@Description Scrape Comixology website for metadata
def ComixologyScraper(books):
    booksProcessed = 0
    booksNotMatched = 0

    for book in books:
        IDinCA = False
        CMXData = None
        CMXID = getCMXIDFromString(book.Notes)

        print("======> Scraping {0}".format(Path.GetFileName(book.FilePath)))
        if CMXID is not None:
            IDinCA = True
            CMXData = getCMXData.byCMXID(CMXID, True)

        if CMXID is not None:
            if CMXData is not None and (IDinCA or verifyMatch(book, CMXData)):
                booksProcessed += 1
                mapCMXtoMetadata(CMXData, book, book)
            else:
                booksNotMatched += 1
                print('Not a close enough match')
        else:
            print('Could not find Comixology ID in Notes or via google')
        
        print('')

    print "Comixology Scraper finished (scraped {0}, skipped {1}).".format(booksProcessed, booksNotMatched)
            

#function copied from CVS - ComicVine Scraper
# a quick function to make splitting ComicRack comicbook fields easier
def split(s):
    return s.split(",") if s else [] 

def verifyMatch(book, CMXData):
    return book.Series == CMXData['series'] and book.Number == CMXData['issue'] and book.ReleasedTime.Year == CMXData['Year'] and book.ReleasedTime.Month == CMXData['Month']    

def overwritable(prop):
    if type(prop) is str:
        return cfg.overwrite or len(prop) == 0
    elif type(prop) is int:
         return cfg.overwrite or prop == -1    
    elif type(prop) is DateTime:
        return cfg.overwrite or prop == DateTime.MinValue       
    else:
        return cfg.overwrite or prop is None

def mapCMXtoMetadata(CMXData, md, book):
    if overwritable(md.Series):
        md.Series = CMXData.get('series', md.Series)
    
    if overwritable(md.Volume):
        md.Volume = CMXData.get('volume', md.Volume)
    
    if overwritable(md.Number):
        md.Number = CMXData.get('issue', md.Number)

    if overwritable(md.Summary):
        md.Summary = CMXData.get('description', md.Summary)
    if overwritable(md.Web):
        md.Web = CMXData.get('webLink', md.Web)

    if overwritable(md.Publisher):
        md.Publisher = CMXData.get('publisher', md.Publisher)

    #credits - extra work with the split and join
    if overwritable(md.Writer):
        md.Writer = ', '.join(CMXData.get('Writer', split(md.Writer)))
    if overwritable(md.Penciller):
        md.Penciller = ', '.join(CMXData.get('Penciller', split(md.Penciller)))
    if overwritable(md.Inker):
        md.Inker = ', '.join(CMXData.get('Inker', split(md.Inker)))
    if overwritable(md.Colorist):
        md.Colorist = ', '.join(CMXData.get('Colorist', split(md.Colorist)))
    if overwritable(md.CoverArtist):
        md.CoverArtist = ', '.join(CMXData.get('Cover', split(md.CoverArtist)))

    if overwritable(md.Genre):
        md.Genre = ', '.join(CMXData.get('genres', split(md.Genre)))

    #released date - datetime
    if overwritable(md.ReleasedTime):
        md.ReleasedTime = DateTime(CMXData.get('Year', md.ReleasedTime.Year), 
            CMXData.get('Month', md.ReleasedTime.Month), 
            CMXData.get('Day', md.ReleasedTime.Day))

    #special handling for Notes
    #Add Comixology ID note if not present in the notes. Never overwrite notes
    if md.Notes.find(CMXData['Notes']) == -1:
        #no CMX ID in notes, append to notes
        md.Notes = CMXData['Notes']