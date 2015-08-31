#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Powered by the Katamari Forever soundtrack, mostly.
# Rewrite also powered by the very same! Thought it was only right.

import re
import requests
import time
from calendar import timegm # seriously what why
from urlparse import urljoin
from bs4 import BeautifulSoup

def getSoup(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

# Note: HTML parsing code incoming. Seeing as HTML pages are always so
# arbitrarily structured, this ain't going to look good.
# But that's how it is, isn't it?

imgUrlRe = re.compile(r"url\((.+?)\);")
priceRe = re.compile(r"\$([0-9.]+)")

def parseShirt(featuredTeeDiv, infoDiv, name):
    author = infoDiv.find(class_='artist-info').find(
        class_='artist').get_text().strip()
    
    # If it's like the old site, the following might be '' or '\xa0'
    # sometimes. Don't know if the new site does that, though.
    # If problems spring up where nonexistent shirts show up, this may
    # be the source - just switch out for "if name in [...]".
    if name == 'No Shirt Available':
        return None
    
    imgs = featuredTeeDiv.find(class_='cycle-slideshow')(class_='img')
    imgUrls = []
    for img in imgs:
        imgUrl = img['style']
        imgUrl = imgUrlRe.search(imgUrl).group(1)
        imgUrls.append(imgUrl)

    buyButton = featuredTeeDiv.find('button', class_='btn')
    price = float(priceRe.search(buyButton.get_text()).group(1))

    shirt = Shirt(name, author, price, imgUrls)
    return shirt

def parseShirts(soup, siteUrl):
    containerDiv = soup.find(class_='todays-tees')

    infoDivs = []
    names = []
    for infoDiv in containerDiv(class_='featured-artist'):
        for i, name in enumerate(infoDiv.find(
            class_='title').stripped_strings):
            infoDivs.append(infoDiv)
            names.append(name if i == 0 else name[2:])

    shirts = []
    for featuredTeeDiv, infoDiv, name in zip(
        containerDiv(class_='featured-tee'),
        infoDivs,
        names
    ):
        curShirt = parseShirt(featuredTeeDiv, infoDiv, name)
        if curShirt is not None:
            shirts.append(curShirt)
    return shirts

def parseTime(soup):
    """Return the time the Yetee deal in `soup` ends as Unix seconds."""
    endTime = soup.find(class_='countdown')['data-end']
    if not endTime:
        return None
    
    # Don't want to have to mess with locale-dependent month names.
    months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    endTime = str(months.index(endTime[:3]) + 1).zfill(2) + endTime[3:]
    
    #...And don't want to have to mess with timezone names.
    offsets = {
        'CDT': -5,
        'CST': -6
    }
    offset = offsets[endTime[-3:]] * 60 * 60
    endTime = endTime[:-3] + 'UTC'
    
    endTime = time.strptime(endTime, '%m %d %Y %H:%M:%S %Z')
    endTime = timegm(endTime) - offset
    return endTime

class Yetee(object):
    """A Yetee campaign. Properties include:
    * shirts - A list of the campaign's shirts (as Shirt objects).
    * ends - The time the campaign ends, as Unix seconds.
    * yesterday - Only if there is a Continue at the moment of this
    campaign. If so, a Yetee object for that campaign.
    """
    def __init__(self, isContinue=False):
        self.isContinue = isContinue
        self.update()

    def update(self):
        """Update to the latest campaign."""
        if not self.isContinue:
            siteUrl = "http://theyetee.com/"
        else:
            siteUrl = "http://theyetee.com/continue.php"

        soup = getSoup(siteUrl)
        self.ends = parseTime(soup)
        self.shirts = parseShirts(soup, siteUrl)

        if not self.isContinue:
            self.yesterday = Yetee(isContinue=True)
    
    def timeLeft(self):
        return self.ends - time.time()

class Shirt(object):
    """A Yetee shirt. Properties include:
    * name - The name of the shirt.
    * author - The name of the shirt's author.
    * price - The price of the shirt in USD.
    * images - A list of URLs to the shirt's images.
    """
    def __init__(self, name, author, price, images):
        self.name   = name
        self.author = author
        self.price  = price
        self.images = images
        # Description of the shirt is currently not in.
        # The shirt's detail page has to be loaded for that, and
        # loading more pages doesn't feel worth it.
        
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
