#!/usr/bin/env python3
from pprint import pprint

import getCMXData
import google
from utils import getCMXIDFromString

from mylar_utils import *

def mapCMXtoMetadata(CMXData):
    #TODO: configure which metadata to update, or maybe which to scrape, then update all in the metadata
    md = GenericMetadata()
    md.isEmpty = False

    md.series = CMXData.get('series', None)
    md.volume = CMXData.get('volume', None) 
    md.issue = CMXData.get('issue', None)

    md.comments = CMXData.get('description', None)
    md.webLink = CMXData.get('webLink', None)
    #md.coverURL = CMXData.get('coverURL', None)

    md.publisher = CMXData.get('publisher', None)

    #credits
    for role in ['Writer','Penciller','Inker','Colorist','Cover']: #,'Artist'
        for person in CMXData.get(role, []):
            md.addCredit(person, role)

    md.genre = ', '.join(CMXData.get('genres', None))

    #?
    #md.pageCount = CMXData.get('pageCount', None)

    md.year = CMXData.get('Year', None)
    md.month = CMXData.get('Month', None)
    md.day = CMXData.get('Day', None)

    md.notes = CMXData.get('Notes', None)

    print("mapped data")
    print(md)

    return md

def processArchive(ca, style):
    md = ca.readMetadata( style )
    print("{0} {1} #{2} ({3})".format(md.series, md.format, md.issue, md.volume))

    print("Title={0}".format(md.title))
    print("Notes={0}".format(md.notes))

    #check for CMXDB in notes
    CMXID = getCMXIDFromString(md.notes)
    print("CMXID in notes = {0}".format(CMXID))

    if CMXID is None:
        CMXID = google.findCMXID(md.series, md.volume, md.issue, md.format)
        print("CMXID google result = {0}".format(CMXID))
    
    if CMXID is not None:
        CMXData = getCMXData.byCMXID(CMXID)
        mdCMX = mapCMXtoMetadata(CMXData)
        
        updateMetadata(md, mdCMX, style)


def main():
    filename = getFilename()
    ca = getComicArchive(filename)
    style = MetaDataStyle.CIX #ComicRack Style metadata

    if ca.hasMetadata( style ):
        processArchive(ca, style)
    else:
        print("Comic archive does not have metadata", file=sys.stderr)

if __name__ == '__main__':
    main()