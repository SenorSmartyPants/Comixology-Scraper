import clr
clr.AddReference('System.Web')
from System.Web import HttpUtility

def UrlPathEncode(string):
    return HttpUtility.UrlEncode(string)