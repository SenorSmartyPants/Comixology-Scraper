import sys
import config as cfg

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
    settings = ComicTaggerSettings()

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

# mdOriginal = existing metadata in Comic archive
# mdNew = newly scraped metadata
def updateMetadata(mdOriginal, mdNew, style):
    print(mdOriginal)

    if cfg.overwrite:
        mdOriginal.overlay(mdNew)
        mdUpdated = mdOriginal
    else:
        mdNew.overlay(mdOriginal)
        mdUpdated = mdNew

    print('merged data')
    print(mdUpdated)

    #artist role will result in duplicates in inker and penciller if metadata exists
    print(ComicInfoXml().stringFromMetadata(mdUpdated))

    #save metadata
    #if not ca.writeMetadata(mdUpdated, style):
    #    print("The tag save seemed to fail!", file=sys.stderr)
    #    return False
    #else:
    #    print("Save complete.", file=sys.stderr)    