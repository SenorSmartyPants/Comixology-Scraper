import re

def getCMXIDFromString(possibleCMXID):
    CMXID = None
    match = re.search('\[CMXDB(\d+)\]', possibleCMXID)
    if match is not None:
        CMXID = match.group(1)
    
    return CMXID