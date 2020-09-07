# beautifulSoup

import re
import requests 
from bs4 import BeautifulSoup 

# region Parsing helper functions
def constructFilter(name, value, substring):
    filter = None
    if name is not None:
        if substring:
            filter={name: re.compile(value)}
        else:
            filter={name: value}
    return filter

def findElement(soup, elementName, filterAttr = None, filterAttrValue = None, text = None, substring = False):
    attrs = constructFilter(filterAttr, filterAttrValue, substring)
    if attrs is None:
        return soup.find(elementName, text=text)
    else:
        return soup.find(elementName, attrs=attrs, text=text)

def findElements(soup, elementName, filterAttr = None, filterAttrValue = None, text = None, substring = False):
    attrs = constructFilter(filterAttr, filterAttrValue, substring)
    if attrs is None:
        return soup.find_all(elementName, text=text)
    else:
        return soup.find_all(elementName, attrs=attrs, text=text)

def getText(element):
    return element.get_text(strip=True)

def findAttributeValue(element, targetAttr):
    return element[targetAttr]    

def getNextSibling(element):
    return element.find_next_sibling()

# endregion

#return beautifulsoup or htmlDoc
def fetchWebPage(URL):
    if URL:
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            print('http status code = {0}'.format(response.status_code))
            return None