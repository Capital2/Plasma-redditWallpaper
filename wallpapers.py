#!/usr/bin/env python3

import requests as rq
import random
import math
import dbus
import os


#from https://github.com/pashazz/ksetwallpaper
def setwallpaper(filepath, plugin = 'org.kde.image'):
    jscript = """
    var allDesktops = desktops();
    print (allDesktops);
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "%s";
        d.currentConfigGroup = Array("Wallpaper", "%s", "General");
        d.writeConfig("Image", "file://%s")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript % (plugin, plugin, filepath))


#choose an arbitrary random int
rand = math.floor(random.uniform(0,150))

#the number of the reddit page
page = rand % 25

#the wallpaper needed
x = math.floor(rand/25)

#loop till reaching the page
after=""
for i in range(page+1):
	r=rq.get("https://www.reddit.com/r/wallpapers/top/.json?t=all&after=%s" % after, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'})
	js = r.json()
	after = js["data"]["after"]

link = js["data"]["children"][x]["data"]["url"]

#delete old wallpaper and download a new one
os.system("mkdir ~/wallpaper ; cd ~/wallpaper ; rm -f *.jpg *.jpeg *.png ; wget -c %s" % link)

setwallpaper("~/wallpaper/%s" % link[link.rfind("/")+1:])
