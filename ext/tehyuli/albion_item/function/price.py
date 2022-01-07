import json
import os
import requests


def priceCheck(*arg):
    print(arg)
    print(len(arg))
    if len(arg) == 3:
        url = "https://www.albion-online-data.com/api/v2/stats/prices/{item}@{enchan}?qualities={qual}".format(item = arg[0], enchan = arg[1], qual = arg[2])
    elif len(arg) == 2:
        url = "https://www.albion-online-data.com/api/v2/stats/prices/{item}?qualities={qual}".format(item = arg[0], qual = arg[1])
    elif len(arg) == 1:
        url = "https://www.albion-online-data.com/api/v2/stats/prices/{item}".format(item = arg[0])
    else:
        return False
    response = requests.get(url)
    data = response.json()
    data_filter = []
    for i in range(len(data)):
        if data[i]['sell_price_min'] != 0 or data[i]['sell_price_max'] != 0 or data[i]['buy_price_min'] or data[i]['buy_price_max']:
            datainput = {
                'city' : data[i]['city'],
                'sell': {
                    'min' : data[i]['sell_price_min'],
                    'max' : data[i]['sell_price_max']
                },
                'buy' : {
                    'min' : data[i]['buy_price_min'],
                    'max' : data[i]['buy_price_max']
                }
            }
            data_filter.append(datainput)
    return data_filter