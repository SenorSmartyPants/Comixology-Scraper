#!/bin/sh
# $1 nzbname = original nzb name
# $2 nzbpath = path to the nzb before Mylar moves it
# $3 newfilename = the name given to the file by Mylar
# $4 newpath = path to the file after Mylar has processed it
# $5 metadata = seriesmetadata { name, comicyear, comicid , issueid, issueyear, issue, publisher } (didn't use it but appears to be the same as you state from a casual glance).

/usr/bin/python3 /app/comictagger.py -S /storage/Comics/Comixology-Scraper/mylar.py "$4"