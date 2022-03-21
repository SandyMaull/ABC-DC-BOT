from rapidfuzz import process, fuzz
from re import search
import json
import os
import requests


datasortraw = []
with open("Include/albion_items.txt", 'r') as data_file:
   for line in data_file:
      sline = line.split(": ")
      sline[1] = sline[1].replace(" ", "")
      sline[1] = sline[1].replace("\n", "")
      if len(sline) > 2:
         sline[2] = sline[2].replace("\n", "")
      datasortraw.append(sline)

def SearchEngine(item):
    datasort = []
    for i in range(len(datasortraw)):
        try:
            datainput = datasortraw[i][2] + " - [" + datasortraw[i][1] + "]"
            filterdata = [
                # "@1",
                # "@2",
                # "@3",
                # "Beginner's ",
                # "Novice's ",
                # "Journeyman's ",
                # "Adept's ",
                # "Expert's ",
                # "Master's ",
                # "Grandmaster's ",
                # "Elder's ",
                # "Beginner ",
                # "Novice ",
                # "Journeyman ",
                # "Adept ",
                # "Expert ",
                # "Master ",
                # "Grandmaster ",
                # "Elder ",
                # "T1_",
                # "T2_",
                # "T3_",
                # "T4_",
                # "T5_",
                # "T6_",
                # "T7_",
                # "T8_"
            ]
            for i in range(len(filterdata)):
                if search(filterdata[i], datainput):
                    datainput = datainput.replace(filterdata[i], "")
                else:
                    continue

            datasort.append(datainput) if datainput not in datasort else datasort
        except:
            continue
    data_ret = process.extract(item, datasort, scorer=fuzz.partial_token_sort_ratio, limit=10)
    return data_ret

def SearchUniqueName(item):
    for i in range(len(datasortraw)):
        if datasortraw[i][1] == item:
            data_ret = item
            break
        else:
            data_ret = False
            continue
    print(data_ret)
    return data_ret

def getrawfromAPI(unique_name):
    with open("Include/albion_items.json", "r", encoding="utf8") as f:
        data = json.load(f)

    for i in range(len(data)):
        if unique_name in data[i]['UniqueName']:
            datainput = {
                'name': data[i]['LocalizedNames']['EN-US'],
                'desc': data[i]['LocalizedDescriptions']['EN-US']
            }
            break
        else:
            datainput = {
                'name': 'NaN',
                'desc': 'NaN'
            }

    return datainput