from sensor.models import TimeStamp

def make_timestamp( row ):
    timedate_format = "%Y-%m-%dT%H:%M:%SZ"
    row["timestamp_data"] = TimeStamp.create( row["timestamp_data"], timedate_format )
    return row

def with_cutoff(elt, cutoff):
    elt['value'] = min(cutoff, elt['value'])
    return elt

def downsample(lst, minutes = 15, cutoff = 100):
    if not lst:
        return []
    ret = []
    prev = None
    ret.append(with_cutoff(lst[0], cutoff))
    prev = lst[0]['timestamp_data']
    for e in lst:
        delta = e['timestamp_data'] - prev
        if delta.total_seconds() > minutes*60:
            ret.append(with_cutoff(e, cutoff))
            prev = e['timestamp_data']
    if ret[-1]['timestamp_data'] != lst[-1]['timestamp_data']:
        ret.append(with_cutoff(lst[-1], cutoff)) # retain the last element
    return ret


def make_datalist( lst, block_size = 15, value_cutoff = 100):
    query = downsample( lst, minutes = block_size , cutoff = value_cutoff)
    return map( make_timestamp , query )
