# The Notee

The Notee is a program to send you notifications for new Yetee shirts. It's easily scheduled, and lets you throw away remembering to check every day!

You can subscribe to [the Yetee Pushbullet channel](https://www.pushbullet.com/my-channel?tag=yetee) with a single click, and start receiving notifications about new shirts immediately.

![](http://i.imgur.com/RSsHKtM.png?1)

## How to use

It's quite easy once you've installed the [requirements](#requirements).

```
# Push to your Pushbullet:
python thenotee.py

# Push to the channel @yetee that you own:
python thenotee.py yetee
```

First, create a file named `pushbullet.auth` in the `thenotee.py` directory. In this file, put your Pushbullet API key (can be found on [your account page](https://www.pushbullet.com/account) - it'll look like a bunch of random numbers and letters, something like `bQxB6NcyQYNnSqxntrKmIdTey3Y31mGp`), and save the file. Of course, you will only have to do this once.

Then just run `thenotee.py`, and you will get a notification containing the current shirts. You can also push to a specific channel by providing the channel tag as argument to `thenotee.py`. Schedule `thenotee.py` to run every day using your operating system's task scheduler ([cron](http://en.wikipedia.org/wiki/Cron) on Linux and OS X, [Windows Task Scheduler](http://en.wikipedia.org/wiki/Windows_Task_Scheduler) on Windows), and you're all done!

## Requirements

A few things are required to run The Notee. First of all, make sure you have [Python 2](https://python.org/download/) downloaded (and in your PATH, if you're a Windows user). Then make sure you have [pip](https://pip.pypa.io/en/stable/installing.html) (download and run `get-pip.py`).

Once you have pip, run these commands to install the required modules:

```
pip install requests
pip install beautifulsoup4
pip install pushbullet.py
```

Then you should be all set to run The Notee!

## `yetee.py`

Included with The Notee is also `yetee.py`, which works as a The Yetee API! This means you can programmatically get which shirts are currently active, their names, their authors, and when the deal ends. This could be useful for other projects than this one - what do I know. Check out the `Yetee` class in `yetee.py` for some info on how to use it. If you have any questions, just [contact me](#contact).

## Contact

If you've got any questions or just want to talk for a bit, you can find me at [@obskyr](http://twitter.com/obskyr) on Twitter, or [e-mail me](mailto:powpowd@gmail.com). If you want a fast answer, Twitter is the place to go!

If there's a problem with The Notee, or a feature you think should be added, feel free to open an issue or pull request here on GitHub.
