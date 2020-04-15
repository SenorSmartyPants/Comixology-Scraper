import urllib.parse

def UrlPathEncode(string):
    return urllib.parse.quote(string)