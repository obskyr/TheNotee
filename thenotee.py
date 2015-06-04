#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pushbullet import Pushbullet
from yetee import Yetee

def doIt():
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(os.path.join(scriptDir, "pushbullet.auth"), 'r') as f:
            auth = f.read().strip()
    except IOError:
        print "Please provide your Pushbullet API "\
            "key in a file called pushbullet.auth."
        print "You can find it at https://www.pushbullet.com/account."
        return
    
    try:
        channelTag = sys.argv[1]
    except IndexError:
        channelTag = None

    pb = Pushbullet(auth)

    if channelTag is not None:
        for channel in pb.channels:
            if channel.channel_tag == channelTag:
                pusher = channel
                break
        else:
            print "You don't own a channel with the tag @{}.".format(
                channelTag)
            return
    else:
        pusher = pb

    yetee = Yetee()

    title = "New shirt{} on The Yetee!".format(
        "s" if len(yetee.shirts) != 1 else ""
    )
    body = " and ".join(shirt.name for shirt in yetee.shirts)
    body += "." if yetee.shirts and yetee.shirts[-1].name[-1] not in ".!?" \
        else ""

    pusher.push_link(
        title,
        "http://theyetee.com/",
        body
    )

    # Alternatively, if you want to push the images:

    # for shirt in yetee.shirts:
    #     pb.push_file(
    #         file_url=shirt.images[0],
    #         file_name=shirt.name,
    #         file_type='image/jpeg',
    #         body="One of today's shirts on The Yetee! http://theyetee.com/"
    #     )


if __name__ == '__main__':
    doIt()
