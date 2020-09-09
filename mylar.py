#!/usr/bin/env python3
from pprint import pprint

import getCMXData
import google
from utils import getCMXIDFromString

from mylar_utils import *

def mapCMXtoMetadata(CMXData):
    md = GenericMetadata()
    md.isEmpty = False

    md.series = CMXData.get('series', None)
    md.volume = CMXData.get('volume', None) 
    md.issue = CMXData.get('issue', None)
    md.issueCount = CMXData.get('issueCount', None)
    md.format = CMXData.get('format', None)

    md.comments = CMXData.get('description', None)
    md.webLink = CMXData.get('webLink', None)

    md.publisher = CMXData.get('publisher', None)

    #credits
    for role in ['Writer','Penciller','Inker','Colorist','Cover']: #,'Artist'
        for person in CMXData.get(role, []):
            md.addCredit(person, role)

    md.genre = ', '.join(CMXData.get('genres', None))

    md.year = CMXData.get('Year', None)
    md.month = CMXData.get('Month', None)
    md.day = CMXData.get('Day', None)

    md.notes = CMXData.get('Notes', None)

    md.ageRating = CMXData.get('ageRating', None)
    #critialRating/CommunityRating is not saved in ComicInfo.xml
    md.criticalRating = CMXData.get('starRating', None)
    #price does not get saved to ComicInfo.xml.
    #but does for COMET. Have not used this script with COMET output
    md.price = CMXData.get('price', None)

    print("mapped Comixology data")
    print(md)

    return md

def processArchive(ca, style):
    md = ca.readMetadata( style )
    print("{0} {1} #{2} ({3})".format(md.series, md.format, md.issue, md.volume))
    print("Notes={0}".format(md.notes))

    #check for CMXDB in notes
    CMXID = getCMXIDFromString(md.notes)
    if CMXID is not None:
        print("CMXID in notes = {0}".format(CMXID))
        IDinCA = True
    else:
        IDinCA = False

    if CMXID is None:
        CMXID = google.findCMXID(md.series, md.volume, md.issue, md.format)
        print("CMXID google result = {0}".format(CMXID))
    
    if CMXID is not None:
        CMXData = getCMXData.byCMXID(CMXID)
        mdCMX = mapCMXtoMetadata(CMXData)
        
        if IDinCA or verifyMatch(md, mdCMX):
            print('matched to Comixology')
            updateMetadata(md, mdCMX, ca, style)
        else:
            print('Not a close enough match')


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