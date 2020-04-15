#!/usr/bin/env python3
import sys
import argparse
import getCMXData
import google

# main entry point for command line searches

def main():
    parser = argparse.ArgumentParser(description='Get genre string for a comic from Comixology.com')
    parser.add_argument("--debug", action='store_true')
    subparser = parser.add_subparsers(help='sub-command help')

    byID = subparser.add_parser('cmxid', help='cmxid -h', description='Get comic by CMXID')
    byID.add_argument("CMXID", help="CMXID from comixology URL")
    byID.set_defaults(func=byCMXID)

    byname = subparser.add_parser('search', help='search -h', description='Get comic by name')
    byname.add_argument("series", help="Comic Series name. e.g. Doctor Strange")
    byname.add_argument("volume", help="Starting year for a volume. e.g. 2015")
    byname.add_argument("issue", help="Issue Number. Don't include # sign")
    byname.add_argument("--format", help="Don't include for regular series. \"Annual\" would be most common")
    byname.set_defaults(func=findCMXURL)

    #print help message if no args, then exit
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)

def byCMXID(args):
    return getCMXData.byCMXID(args.CMXID, args.debug)


def findCMXURL(args):
    CMXID = google.findCMXID(args.series, args.volume, args.issue, args.format, args.debug)
    return getCMXData.byCMXID(CMXID, args.debug)   


if __name__ == "__main__":
    main()