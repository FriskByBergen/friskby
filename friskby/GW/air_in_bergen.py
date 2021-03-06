#!/usr/bin/env python

from datetime import datetime as dt
import pytz
import pandas as pd
from friskby_gw import FriskByGW

def data_index(df):
    """Probably this function is not necessary and we can just use 0, 1, 2 in
    post_data(device, df) instead of these variables, but if something will
    change in table, e.g. the first value will be Date, then Time etc. we'll
    have some unexpected values and the script will crash.

    """
    # we need just the first value of 'Verdi', since the second is from
    # yesterday's measurings
    counter = 0
    for i in range(len(df)):
        for j in range(len(df[i])):
            if df[i][j] == 'Komponent':
                component = j
            if df[i][j] == 'Tid':
                tid = j
            if (counter < 1) and (df[i][j] == 'Verdi'):
                value = j
                counter += 1
    return component, tid, value


def post_data(GW, device, df, bergen_time):
    sensor_types = ['_PM10', '_PM25']
    komponent_id = ["PM10", "PM2.5"]
    key = "9fbb2727-067d-4618-af05-e45cafdd673d"

    component, tid, value = data_index(df)
    for dev_id in range(len(komponent_id)):
        for i in range(len(df)):
            if df[i][component] == komponent_id[dev_id]:
                hour, minute = map(int, df[i][tid].split(':'))
                ts = bergen_time.replace(hour=hour,
                                         minute=minute,
                                         second=0,
                                         microsecond=0).isoformat()
                n = float(df[i][value].replace(',', '.'))
                sensor_id = device + sensor_types[dev_id]
                sensor = GW.getSensor(sensor_id, key)
                if(n >= 0):
                    sensor.postValue(n, timestamp = ts)


def main():
    GW = FriskByGW()
    base_url = 'http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%'
    key_bg1 = '7b751808f5-d561-4737-9185-4ecc0e834975%7d' # LODDEFJORD
    key_bg2 = '7b4ff685c1-ad51-4468-b2fc-08345d11f447%7d' # DANMARKSPLASS
    key_bg3 = '7b5b0ff070-e6e6-4f60-88a3-bd923ac3a7e6%7d' # RAADHUSET
    key_bg4 = '7bceade2ac-e62f-4e50-af7c-347e402fff27%7d' # AASANE

    luft_map = {"BG_1": '%s%s' % (base_url, key_bg1),
                "BG_2": '%s%s' % (base_url, key_bg2),
                "BG_3": '%s%s' % (base_url, key_bg3),
                "BG_4": '%s%s' % (base_url, key_bg4)}

    bergen_tz = pytz.timezone('Europe/Oslo')
    bergen_time = dt.now(bergen_tz)

    for device in luft_map:
        try:
            url_read = pd.read_html(luft_map[device], header=0, thousands=".")[1]
            df = url_read.values.tolist()
            post_data(GW, device, df, bergen_time)
        except ValueError as err:
            print('Error occurred on device = %s: %s.' % (device, err))

if __name__ == '__main__':
    main()
