#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Powered by the Katamari Forever soundtrack, mostly.

import re
import requests
from urlparse import urljoin
from bs4 import BeautifulSoup

def getSoup(url):
    return BeautifulSoup(requests.get(url).text)

# Note: HTML parsing code incoming. Seeing as HTML pages are always so
# arbitrarily structured, this ain't going to look good.
# But that's how it is, isn't it?

imgUrlRe = re.compile(r"url\([\"\'](.+?)[\"\']\);")

def parseShirt(topDiv, infoDiv, siteUrl, price):
    name = infoDiv.find('h2').get_text().strip()
    # Empty names sometimes become "\xa0".
    if name in [u"No Shirt Available", u"\xa0", u""]:
        return None
    author = infoDiv.get_text().split('\n')[2].strip()[3:]
    imgs = topDiv(class_="imgTeeImage")
    imgUrls = []
    for img in imgs:
        imgUrl = img['style']
        imgUrl = urljoin(siteUrl, imgUrlRe.search(imgUrl).group(1))
        imgUrls.append(imgUrl)

    shirt = Shirt(name, author, price, imgUrls)
    return shirt

def parseShirts(soup, siteUrl, price):
    shirts = []
    for topDiv in \
    soup.find(class_='divShirtLeftTop')('div', recursive=False):
        infoDiv = topDiv.find(class_='divVContainer').find('div')
        shirt = parseShirt(topDiv, infoDiv, siteUrl, price)
        if shirt is not None:
            shirts.append(shirt)
    return shirts

def parseContinueShirts(soup, siteUrl, price):
    shirts = []
    for topDiv in soup.find(
        class_='divShirtLeftBottom'
    )(
        'div', class_='divVContainer', recursive=False
    ):
        infoDiv = topDiv.find('div')
        shirt = parseShirt(topDiv, infoDiv, siteUrl, price)
        if shirt is not None:
            shirts.append(shirt)
    return shirts

def parseTime(soup):
    onload = soup.find('body')['onload']
    # There's no easy way to parse time as CST specifically, sadly.
    # Especially not with DST factoring in...
    timeRe = re.compile(r"^countdown\(([0-9]+),([0-9]+),([0-9]+)\);$")
    t = timeRe.search(onload).groups()
    t = tuple(int(unit) for unit in t) if int(t[0]) else None
    return t

class Yetee(object):
    def __init__(self, isContinue=False):
        if not isContinue:
            siteUrl = "http://theyetee.com/"
            def getPrice(soup):
                rightDiv = soup.find(class_='divShirtRight')
                price = int(
                    rightDiv.find(
                        class_='divShirtPrice'
                    ).get_text(strip=True)[1:]
                )
                return price
            shirtParser = parseShirts
        else:
            siteUrl = "http://theyetee.com/continue.php"
            def getPrice(soup):
                # At the moment, $13 seems to be the only option for Continue.
                return 13
            shirtParser = parseContinueShirts

        soup = getSoup(siteUrl)
        price = getPrice(soup)
        self.ends = parseTime(soup)
        self.shirts = shirtParser(soup, siteUrl, price)

        if not isContinue:
            self.yesterday = Yetee(isContinue=True)


class Shirt(object):
    def __init__(self, name, author, price, images):
        self.name   = name
        self.author = author
        self.price  = price
        self.images = images

    def __repr__(self):
        return "{} by {} ({}, {} images)".format(
            self.name, self.author, '$' + str(self.price), len(self.images)
        )

if __name__ == '__main__':
    yetee = Yetee()
    print "Shirts:"
    if yetee.shirts:
        for shirt in yetee.shirts:
            print "\t{} by {}".format(shirt.name, shirt.author)
    else:
        print "\tNone at the moment!"
    print "Continue shirts:"
    if yetee.yesterday.shirts:
        for shirt in yetee.yesterday.shirts:
            print "\t{} by {}".format(shirt.name, shirt.author)
    else:
        print "\tNone at the moment!"
