import sys

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

# mdKeep = this metadata will not be altered if it has a value
# mdAdd = Non-null values will be added into mdKeep
def updateMetadata(mdKeep, mdAdd, style):
    print(mdKeep)
    mdAdd.overlay(mdKeep)

    print('merged data')
    print(mdAdd)

    #artist role will result in duplicates in inker and penciller if metadata exists
    print(ComicInfoXml().stringFromMetadata(mdAdd))

    #save metadata
    #if not ca.writeMetadata(md, style):
    #    print("The tag save seemed to fail!", file=sys.stderr)
    #    return False
    #else:
    #    print("Save complete.", file=sys.stderr)    