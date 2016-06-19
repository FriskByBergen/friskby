#!/usr/bin/python3

import requests
import timestring
#  import re
#  import time
from datetime import date
import psycopg2
from friskby.GW.friskby_gw import FriskByGW

sensor_types = ['_PM10', '_PM25']

GW = FriskByGW()

luft_map = {"BG_1": "http://www.luftkvalitet.info/home/"
                          "overview.aspx?type=2&topic=1&id=%7b751808f5-d561-4737-9185-4ecc0e834975%7d", # LODDEFJORD
            "BG_2": "http://luftkvalitet.info/"
                             "home/overview.aspx?type=2&topic=1&id=%7b4ff685c1-ad51-4468-b2fc-08345d11f447%7d", # DANMARKSPLASS
            "BG_3": "http://www.luftkvalitet.info/home/"
                         "overview.aspx?type=2&topic=1&id=%7b5b0ff070-e6e6-4f60-88a3-bd923ac3a7e6%7d", # RAADHUSET
            "BG_4": "http://www.luftkvalitet.info/home/"
                      "overview.aspx?type=2&topic=1&id=%7bceade2ac-e62f-4e50-af7c-347e402fff27%7d" # AASANE

            }
# keys for parsing data
komponent_id = ["PM10", "PM2.5"] #, "NO2", "O3"]

key = "00001111-2222-3333-4444-555566667777"

#current_date = date.today().isoformat()

for device in luft_map:
    response = requests.get(luft_map[device])
    if response.status_code == 200:
        response = response.text
        translation_table = dict.fromkeys(map(ord, '"<>='), ' ')
        response = response.translate(translation_table)
        t_split = response.split()

        k = 27  #  constant

        #time
 #       time_i = t_split.index('ctl00_cph_Map_ctl00_gwStation_ctl02_Label2', 0, -1)
 #       ts = timestring.Date(current_date + " " + t_split[time_i + 1])

        for i in range(len(komponent_id)):
            try:
                index = t_split.index(komponent_id[i], 0, -1)
            except ValueError as e:
                pass
            else:
                sensor_id = device + sensor_types[i]
                sensor = GW.getSensor(sensor_id, key)
                a = index + k
                n = t_split[a].replace(',', '.')
                try:
                    n = float(n)
                except ValueError as e:
                    pass  # better to use Warnings here
                else:
                    # yes, the value from the sensor can be negative (probably because of an error)
                    if n > 0:
                        sensor.postValue(n)

    else:
        print("Can't get data from the site")