from utils import *

#@Name	Comixology Scraper
#@Hook	Books
#@Description Scrape Comixology website for metadata
def ComixologyScraper(books):
    for book in books:
        print book.Series
        print book.Notes
        getCMXIDFromString(book.Notes)