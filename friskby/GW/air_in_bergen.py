#!/usr/bin/python3

import requests
import timestring
#  import re
#  import time
from datetime import date
import psycopg2

# new_db just to test if everything works
connect_db = psycopg2.connect(database="new_db", user="postgres", password="BAZeN49Def2X", host="127.0.0.1", port="5432")
#  connect_db = psycopg2.connect(database="friskby_db", user="postgres", password="BAZeN49Def2X",
# host="127.0.0.1", port="5432")
print ("Opened database successfully")
cur = connect_db.cursor()
all_db_values = ['PLACE', 'DATE_TIME', 'PM10', 'PM25', 'NO2', 'O3']


luft_map = {"DANMARKSPLASS": "http://luftkvalitet.info/"
                             "home/overview.aspx?type=2&topic=1&id=%7b4ff685c1-ad51-4468-b2fc-08345d11f447%7d",
            "LODDEFJORD": "http://www.luftkvalitet.info/home/"
                          "overview.aspx?type=2&topic=1&id=%7b751808f5-d561-4737-9185-4ecc0e834975%7d",
            "AASANE": "http://www.luftkvalitet.info/home/"
                      "overview.aspx?type=2&topic=1&id=%7bceade2ac-e62f-4e50-af7c-347e402fff27%7d",
            "RAADHUSET": "http://www.luftkvalitet.info/home/"
                         "overview.aspx?type=2&topic=1&id=%7b5b0ff070-e6e6-4f60-88a3-bd923ac3a7e6%7d"}
# keys for parsing data
komponent_id = ["ctl00_cph_Map_ctl00_gwStation_ctl02_Label2", "PM10", "PM2.5", "NO2", "O3"]

current_date = date.today().isoformat()

for sted in luft_map:
    text_from_site = requests.get(luft_map[sted])
    if text_from_site.status_code == 200:
        text_from_site = text_from_site.text
        translation_table = dict.fromkeys(map(ord, '"<>='), ' ')
        text_from_site = text_from_site.translate(translation_table)
        t_split = text_from_site.split()

        k = 27  #  constant

        #  a new list to save indexes of components
        komponent_index = []

        #  temporary list to save keys for our values. The number of keys is not a constant
        temp_komp_id = []

        #  temporary list for db fields for values we are going to add since the number of values can change (O3)
        temp_db_fields = ['PLACE']
        for i in range(len(komponent_id)):
            try:
                index = t_split.index(komponent_id[i], 0, -1)
            except ValueError as e:
                pass
            else:
                komponent_index.append(index)
                temp_komp_id.append(komponent_id[i])
                temp_db_fields.append(all_db_values[i+1])

        #  values we are going to add to db
        db_input = []
        if len(temp_komp_id) > 0:
            db_input.append(sted)
            i = 0
            for el in komponent_index:
                a = el + k

                #  format date and time
                if temp_komp_id[i] == "ctl00_cph_Map_ctl00_gwStation_ctl02_Label2":
                    date_time = current_date + " " + t_split[el + 1]
                    date_time = timestring.Date(date_time)
                    db_input.append(date_time)

                #  and add everything to a tuple...
                else:
                    #  ...if "everything" is a number
                    n = t_split[a].replace(',','.')
                    try:
                        float(n)
                    except ValueError as e:
                        pass #  better to use Warnings here
                    else:
                        db_input.append(n)
                i += 1

        # just to check the output. here we have to use smth like
        # current_date.execute("INSERT INTO LUFTKVALITET_STATISTIKK...)
        print("fields we are going to add values: ", temp_db_fields)
        print("values to add to db: ", db_input)

    else:
        print("Can't get data from the site")

connect_db.close()