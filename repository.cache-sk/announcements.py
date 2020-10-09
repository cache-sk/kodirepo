# -*- coding: utf-8 -*-
# Author: cache-sk
# Created on: 2.6.2020
# License: AGPL v.3 https://www.gnu.org/licenses/agpl-3.0.html

import time
import xbmc, xbmcaddon, xbmcgui
import json
import traceback

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

INTERVAL =  24 * 60 * 60 
ANNOUNCEMENTS = 'https://raw.githubusercontent.com/cache-sk/kodirepo/master/announcements.json'
LAST = 'last_ann'

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    
    while not monitor.abortRequested():
        try:
            response = urlopen(ANNOUNCEMENTS)
            data = json.loads(response.read())
            data = sorted(data.items())
            addon = xbmcaddon.Addon()
            last_ann = addon.getSetting(LAST)
            last_ann = 0 if not last_ann else int(last_ann)
            for ann in data:
                ikey = int(ann[0])
                print(str(ikey))
                print(str(last_ann))
                if ikey > last_ann:
                    last_ann = ikey
                    xbmcgui.Dialog().textviewer(addon.getAddonInfo('name'), ann[1])
            addon.setSetting(LAST,str(last_ann))
        except:
            traceback.print_exc()

        if monitor.waitForAbort(INTERVAL):
            break
