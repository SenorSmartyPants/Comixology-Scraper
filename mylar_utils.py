import sys
import config as cfg

from datetime import date

#using hotio docker paths
#something is weird with the path. Not finding the libs but this path is at the end of the path list
#insert into the start of path and then script works
sys.path.insert(0,'/app/lib')

from comictaggerlib.settings import *
from comictaggerlib.comicarchive import *

def getFilename():
    if len(sys.argv) < 2:
        print("Usage: {0} [comicfile]".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(filename + ": not found!", file=sys.stderr)
        sys.exit(1)

    return filename

def getComicArchive(filename):
    settings = ComicTaggerSettings('/config/app/.ComicTagger')

    #image path needed to start ComicArchive, not sure why.
    #default image path is null in settings
    ca = ComicArchive(
        filename,
        settings.rar_exe_path,
        ComicTaggerSettings.getGraphic('nocover.png'))

    if not ca.seemsToBeAComicArchive():
        print("Sorry, but " + \
            filename + " is not a comic archive!", file=sys.stderr)
        sys.exit(1)

    return ca

def verifyMatch(mdOriginal, mdNew):
    print("Verifying match... existing data -> Comixology data")
    seriesEqual = mdOriginal.series.lower() == mdNew.series.lower()
    seriesEqualNoThe = mdOriginal.series.replace('The ', '', 1).lower() == mdNew.series.replace('The ', '', 1).lower()

    #does series in CBZ equal CMX series + format? 
    #most common for Annuals
    if mdNew.format:
        seriesEqualFormat = mdOriginal.series.lower() == mdNew.series.lower() + ' ' + mdNew.format.lower()
    else:
        seriesEqualFormat = False

    numberEqual = mdOriginal.issue == mdNew.issue
    #or number is 1 and issue is empty
    numberEqual2 = (int(mdOriginal.issue) == 1 and mdNew.issue == '')

    print("Series {0} {2} {1}".format(mdOriginal.series, mdNew.series, '==' if seriesEqual else '!='))
    if not seriesEqual:
    	print("Series 'The' removed {0} {2} {1}".format(mdOriginal.series, mdNew.series, '==' if seriesEqualNoThe else '!='))

    if not seriesEqual and not seriesEqualNoThe:
        print("Series format (Annual) {0} {2} {1}".format(mdOriginal.series, mdNew.series + ' ' + mdNew.format, '==' if seriesEqualFormat else '!='))
    
    print("Number {0} {2} {1}".format(mdOriginal.issue, mdNew.issue, '==' if numberEqual else '!='))
    if not numberEqual:
    	print("Number test 2 (1 == empty) {0} {2} {1}".format(mdOriginal.issue, mdNew.issue, '==' if numberEqual2 else '!='))

    # year and month need an allowable range parameter to fuzzy match 
    # when cover date (which is the date comictagger/comicvine saves) 
    # does not match in store date (which is what comixology provides)
    daysDifferenceTolerance = 67

    originalDate = date(int(mdOriginal.year), int(mdOriginal.month), int(mdOriginal.day))
    newDate = date(mdNew.year, mdNew.month, mdNew.day)
    datediff = abs((newDate - originalDate).days)
    dateEqual = (datediff <= daysDifferenceTolerance)
    print("Dates {0} and {1}({2}) {3} within {4} days".format(originalDate, newDate, datediff, '==' if dateEqual else '!=', daysDifferenceTolerance))

    return (seriesEqual or seriesEqualNoThe or seriesEqualFormat) and (numberEqual or numberEqual2) and dateEqual

# mdOriginal = existing metadata in Comic archive
# mdNew = newly scraped metadata
def updateMetadata(mdOriginal, mdNew, ca, style):
    print('original data')
    print(mdOriginal)

    #special handling for Notes
    #Add Comixology ID note if not present in the notes. Never overwrite notes
    if mdOriginal.notes.find(mdNew.notes) == -1:
        #no CMX ID in notes, append to notes
        newNotes = mdOriginal.notes + '\n' + mdNew.notes
    else:
        newNotes = mdOriginal.notes

    if cfg.overwrite:
        mdOriginal.overlay(mdNew)
        mdUpdated = mdOriginal
    else:
        mdNew.overlay(mdOriginal)
        mdUpdated = mdNew

    mdUpdated.notes = newNotes
    print('merged data')
    print(mdUpdated)

    #save metadata
    if not ca.writeMetadata(mdUpdated, style):
        print("The tag save seemed to fail!", file=sys.stderr)
        return False
    else:
        print("Save complete.", file=sys.stderr)    