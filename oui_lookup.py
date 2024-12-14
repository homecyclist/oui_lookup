# OUI Lookup script.
# gian.drosario@gmail.com
# 
# Provides OUI lookup for MAC addresses

import requests
import os
import re

class oui_db:
    '''
    Generate object containing MAC OUI database.
    
    Usage: oui_lookup.lookup("MAC Address")
    '''
    
    def __init__(self):
        # Default settings: 
        self.db_url = "https://standards-oui.ieee.org/"
        self.db_txt = "oui.txt"
        
        # Main Init:
        self.prefixes = self.build_db()

    def __str__(self):
        return "OUI database for %i prefixes." % len(self.prefixes)
    
    def build_db(self):
        if os.path.exists(self.db_txt):
            print("Initializing MAC OUI Database.")
            prefixes = {}
            with open(self.db_txt, 'r', encoding="utf8") as db:
                for line in db.readlines():
                    if "(base 16)" in line:
                        line = line.split()
                        prefix = line[0]
                        company = " ".join(line[3:]).strip()
                        prefixes.update({prefix:company})
            print("OUI database initialized with %i prefixes." % len(prefixes))
            return prefixes
        
        else:
            print("%s not found at script's location. Downloading." % self.db_txt)
            headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"}
            with requests.get(self.db_url, allow_redirects=False, headers=headers) as webdata:
                open(self.db_txt, 'wb').write(webdata.content)
            return self.build_db()

    def lookup(self, mac):
        ''' Returns company for provided MAC address. '''
        
        hex_pattern = r'\b[0-9A-Fa-f]+\b' 
        mac = ''.join(re.findall(hex_pattern, mac))
        prefix =  mac[:6].upper()       
        try:
            return self.prefixes[prefix]
        except:
            return "Unknown vendor."

if __name__ == "__main__":
    # Run standalone for testing:
    test_macs = [
        "74:58:F3:41:4B:1F",
        "C8:9C:DC:78:6B:D6",
        "B4:82:C5:60:97:70",
        "50:EB:71:30:1C:54",
    ]
    
    oui_db = oui_db()
    for mac in test_macs:
        print( oui_db.lookup(mac) )
