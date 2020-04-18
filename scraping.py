# HTMLAgility and Xpath syntax
import sys
import clr
clr.AddReference('HtmlAgilityPack') 

from HtmlAgilityPack import HtmlWeb
from HtmlAgilityPack import HtmlDocument

clr.AddReference('System.Web')
from System.Web import HttpUtility
# for HTMLdecode

import System
import System.Text
# this handles unicode encoding:
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

# region Parsing helper functions
def constructFilter(name, value, substring):
    if substring:
        filter = "contains({0}, '{1}')".format(name, value)
    else:
        filter = "{0}='{1}'".format(name, value)
    return filter

def constructSelector(elementName, filterAttr = None, filterAttrValue = None, text = None, substring = False):
    xpath = "//" + elementName
    if filterAttr is not None or text is not None:
        xpath += "["
    if filterAttr is not None:
        xpath += constructFilter('@' + filterAttr, filterAttrValue, substring)
    if filterAttr is not None and text is not None:
        xpath += " and "        
    if text is not None:
        xpath += constructFilter('text()', text, substring)
    if filterAttr is not None or text is not None:
        xpath += "]"
    return xpath

def findElement(soup, elementName, filterAttr = None, filterAttrValue = None, text = None, substring = False):
    xpath = constructSelector(elementName, filterAttr, filterAttrValue, text, substring)
    return soup.DocumentNode.SelectSingleNode(xpath)

def findElements(soup, elementName, filterAttr = None, filterAttrValue = None, text = None, substring = False):
    xpath = constructSelector(elementName, filterAttr, filterAttrValue, text, substring)
    return soup.DocumentNode.SelectNodes(xpath)

def getText(element):
    return unicode(HttpUtility.HtmlDecode((element.InnerText.strip())))

def findAttributeValue(element, targetAttr):
    return unicode(HttpUtility.HtmlDecode(element.Attributes[targetAttr].Value))

def getNextSibling(element):
    return element.SelectSingleNode("following-sibling::*")

# endregion

#return beautifulsoup or htmlDoc
def fetchWebPage(URL):
    return HtmlWeb().Load(URL)