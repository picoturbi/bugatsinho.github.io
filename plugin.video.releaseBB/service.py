# -*- coding: utf-8 -*-

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import cache

import re
import os
import xbmcvfs

_settingsFile = os.path.join(control.addonPath, 'resources', 'settings.xml')
if xbmcvfs.exists(_settingsFile):
    with open(_settingsFile, 'r+') as file:
        data = file.read()
        line = re.findall(r'(<setting id="domain".+?/>)', data)[0]
        line2 = re.findall(r'(<setting id="eztv\.domain".+?/>)', data)[0]

        try:
            eztv_status = client.request('https://eztvstatus.com')
            domains = client.parseDOM(eztv_status, 'a', ret='href', attrs={'class': 'domainLink'})
            domains = [i.split('//')[1].encode('utf-8').upper() for i in domains if domains]
        except IndexError:
            domains = ['eztv.re', 'eztv.ag', 'eztv.it', 'eztv.ch']
            domains = [i.encode('utf-8').upper() for i in domains if domains]
        set_line = '<setting id="eztv.domain" label="EZTV DOMAIN" type="select" values="{0}|{1}|{2}|{3}" default="{0}"/>'
        fline = set_line.format(domains[0], domains[1], domains[2], domains[3], domains[0])

        paste = cache.get(client.request, 12, 'https://pastebin.com/raw/upztzeGt')
        new_data = data.replace(line, paste)
        new_data2 = new_data.replace(line2, fline)
        file.seek(0)
        file.truncate()
        # file.write(new_data)
        file.write(new_data2)
        file.close()
        control.refresh()
else:
    pass
