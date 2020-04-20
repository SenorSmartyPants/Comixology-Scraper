from utils import *
from System import DateTime
from System.IO import Path

import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *

import getCMXData
import config as cfg

#@Name	Comixology Scraper
#@Hook	Books
#@Description Scrape Comixology website for metadata
def ComixologyScraper(books):
    booksProcessed = 0
    booksNotMatched = 0

    for book in books:
        print("======> Scraping {0}".format(Path.GetFileName(book.FilePath)))
        
        CMXData = None
        CMXID = getCMXIDFromString(book.Notes)

        if CMXID is not None:
            print("CMXID in notes = {0}".format(CMXID))
            IDinCA = True
        else:
            IDinCA = False

        if CMXID is not None:
            CMXData = getCMXData.byCMXID(CMXID, True)
            if IDinCA or verifyMatch(book, CMXData):
                booksProcessed += 1
                updateMetadata(book, CMXData)
            else:
                booksNotMatched += 1
                print('Not a close enough match')
        else:
            booksNotMatched += 1
            print('Could not find Comixology ID in Notes or via google')
        
        print('')

    print "Comixology Scraper finished (scraped {0}, skipped {1}).".format(booksProcessed, booksNotMatched)
    MessageBox.Show("Comixology Scraper finished (scraped {0}, skipped {1}).".format(booksProcessed, booksNotMatched), "Comixology Scraper", MessageBoxButtons.OK)
            

#function copied from CVS - ComicVine Scraper
# a quick function to make splitting ComicRack comicbook fields easier
def split(s):
    return s.split(",") if s else [] 

def verifyMatch(book, CMXData):
    print("Verifying match... existing data -> Comixology data")
    seriesEqual = book.Series == CMXData['series']
    numberEqual = book.Number == CMXData['issue']
    yearEqual = book.ReleasedTime.Year == CMXData['Year']
    monthEqual = book.ReleasedTime.Month == CMXData['Month']
    print("Series {0} {2} {1}".format(book.Series, CMXData['series'], '==' if seriesEqual else '!='))
    print("Number {0} {2} {1}".format(book.Number, CMXData['issue'], '==' if numberEqual else '!='))
    print("Year {0} {2} {1}".format(book.ReleasedTime.Year, CMXData['Year'], '==' if yearEqual else '!='))
    print("Month {0} {2} {1}".format(book.ReleasedTime.Month, CMXData['Month'], '==' if monthEqual else '!='))

    return seriesEqual and numberEqual and yearEqual and monthEqual    

def overwritable(prop):
    if type(prop) is str:
        return cfg.overwrite or len(prop) == 0
    elif type(prop) is int:
         return cfg.overwrite or prop == -1    
    elif type(prop) is DateTime:
        return cfg.overwrite or prop == DateTime.MinValue       
    else:
        return cfg.overwrite or prop is None

def updateMetadata(book, CMXData):
    if overwritable(book.Series):
        book.Series = CMXData.get('series', book.Series)
    
    if overwritable(book.Volume):
        book.Volume = CMXData.get('volume', book.Volume)
    
    if overwritable(book.Number):
        book.Number = CMXData.get('issue', book.Number)

    if overwritable(book.Summary):
        book.Summary = CMXData.get('description', book.Summary)
    if overwritable(book.Web):
        book.Web = CMXData.get('webLink', book.Web)

    if overwritable(book.Publisher):
        book.Publisher = CMXData.get('publisher', book.Publisher)

    #credits - extra work with the split and join
    if overwritable(book.Writer):
        book.Writer = ', '.join(CMXData.get('Writer', split(book.Writer)))
    if overwritable(book.Penciller):
        book.Penciller = ', '.join(CMXData.get('Penciller', split(book.Penciller)))
    if overwritable(book.Inker):
        book.Inker = ', '.join(CMXData.get('Inker', split(book.Inker)))
    if overwritable(book.Colorist):
        book.Colorist = ', '.join(CMXData.get('Colorist', split(book.Colorist)))
    if overwritable(book.CoverArtist):
        book.CoverArtist = ', '.join(CMXData.get('Cover', split(book.CoverArtist)))

    if overwritable(book.Genre):
        book.Genre = ', '.join(CMXData.get('genres', split(book.Genre)))

    #released date - datetime
    if overwritable(book.ReleasedTime):
        book.ReleasedTime = DateTime(CMXData.get('Year', book.ReleasedTime.Year), 
            CMXData.get('Month', book.ReleasedTime.Month), 
            CMXData.get('Day', book.ReleasedTime.Day))

    #special handling for Notes
    #Add Comixology ID note if not present in the notes. Never overwrite notes
    if book.Notes.find(CMXData['Notes']) == -1:
        #no CMX ID in notes, append to notes
        if len(book.Notes) > 0:
            book.Notes += "\n"
        book.Notes += CMXData['Notes']