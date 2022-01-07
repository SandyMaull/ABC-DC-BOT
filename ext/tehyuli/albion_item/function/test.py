# from rapidfuzz import process, fuzz
from re import search
from ext.db_module import fetch
import json


# def getrawfromAPI():
#     response = requests.get("https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json")
#     data = response.json()
#     datasortrawAPI = []
#     for i in range(len(data)):
#         try:
#             datainput = {
#                 'id' : data[i]['Index'],
#                 'name': data[i]['LocalizedNames']['EN-US'],
#                 'uniq_name' : data[i]['UniqueName']
#             }
#             datasortrawAPI.append(datainput) if datainput not in datasortrawAPI else datasortrawAPI
#         except:
#             continue

#     return datasortrawAPI

# def ByNames(item):
#     data = getrawfromAPI()
#     datasortrawName = []
#     for i in range(len(data)):
#         datainput = data[i]['name']
#         datasortrawName.append(datainput) if datainput not in datasortrawName else datasortrawName
#     data_ret = process.extract(item, datasortrawName, scorer=fuzz.WRatio, limit=5)
#     return data_ret

# datasortraw = []
# with open("albion_items.txt", 'r') as data_file:
#    for line in data_file:
#       sline = line.split(": ")
#       sline[1] = sline[1].replace(" ", "")
#       sline[1] = sline[1].replace("\n", "")
#       if len(sline) > 2:
#          sline[2] = sline[2].replace("\n", "")
#       datasortraw.append(sline)

# def SearchEngineFilter(item):
#    datasort = []
#    for i in range(len(datasortraw)):
#       try:
#          datainput = datasortraw[i][2]
#          filterdata = [
#                "Beginner's ",
#                "Novice's ",
#                "Journeyman's ",
#                "Adept's ",
#                "Expert's ",
#                "Master's ",
#                "Grandmaster's ",
#                "Elder's ",
#                "Beginner ",
#                "Novice ",
#                "Journeyman ",
#                "Adept ",
#                "Expert ",
#                "Master ",
#                "Grandmaster ",
#                "Elder "
#          ]
#          for i in range(len(filterdata)):
#             if search(filterdata[i], datainput):
#                datainput = datainput.replace(filterdata[i], "")
#             else:
#                continue
         
#          datasort.append(datainput) if datainput not in datasort else datasort
#       except:
#          continue
#    data_ret = process.extract(item, datasort, scorer=fuzz.WRatio, limit=10)
#    return data_ret

# def SearchEngineNonFilter(item):
#    datasort = []
#    for i in range(len(datasortraw)):
#       try:
#          datainput = datasortraw[i][2] + " - [" + datasortraw[i][1] + "]"
#          filterdata = [
#                "@1",
#                "@2",
#                "@3",
#                "Beginner's ",
#                "Novice's ",
#                "Journeyman's ",
#                "Adept's ",
#                "Expert's ",
#                "Master's ",
#                "Grandmaster's ",
#                "Elder's ",
#                "Beginner ",
#                "Novice ",
#                "Journeyman ",
#                "Adept ",
#                "Expert ",
#                "Master ",
#                "Grandmaster ",
#                "Elder ",
#                "T1_",
#                "T2_",
#                "T3_",
#                "T4_",
#                "T5_",
#                "T6_",
#                "T7_",
#                "T8_"
#          ]
#          for i in range(len(filterdata)):
#             if search(filterdata[i], datainput):
#                datainput = datainput.replace(filterdata[i], "")
#             else:
#                continue

#          datasort.append(datainput) if datainput not in datasort else datasort
#       except:
#          continue
#    data_ret = process.extract(item, datasort, scorer=fuzz.partial_token_sort_ratio, limit=10)
#    return data_ret



# def SearchEngineFilter(item):
#     datasort = []
#     for i in range(len(datasortraw)):
#         try:
#             datainput = datasortraw[i][2]
#             filterdata = [
#                 "Beginner's ",
#                 "Novice's ",
#                 "Journeyman's ",
#                 "Adept's ",
#                 "Expert's ",
#                 "Master's ",
#                 "Grandmaster's ",
#                 "Elder's ",
#                 "Beginner ",
#                 "Novice ",
#                 "Journeyman ",
#                 "Adept ",
#                 "Expert ",
#                 "Master ",
#                 "Grandmaster ",
#                 "Elder "
#             ]
#             for i in range(len(filterdata)):
#                 if search(filterdata[i], datainput):
#                     datainput = datainput.replace(filterdata[i], "")
#                 else:
#                     continue
            
#             datasort.append(datainput) if datainput not in datasort else datasort
#         except:
#             continue
#     data_ret = process.extract(item, datasort, scorer=fuzz.WRatio, limit=10)
#     return data_ret

# def SearchEngineNonFilter(item):
#     datasort = []
#     for i in range(len(datasortraw)):
#         try:
#             datainput = datasortraw[i][2] + " - [" + datasortraw[i][1] + "]"
#             filterdata = [
#                 "@1",
#                 "@2",
#                 "@3"
#             ]
#             for i in range(len(filterdata)):
#                 if search(filterdata[i], datainput):
#                     datainput = datainput.replace(filterdata[i], "")
#                 else:
#                     continue

#             datasort.append(datainput) if datainput not in datasort else datasort
#         except:
#             continue
#     data_ret = process.extract(item, datasort, scorer=fuzz.partial_token_sort_ratio, limit=10)
#     return data_ret

# data = SearchEngineNonFilter("xcrossbow")
# listdata = ""
# for i in range(len(data)):
#       listdata += "**{item}** \n Kecocokan Penelusuran: *{matching}%* \n\n".format( item = data[i][0], matching = round(data[i][1], 2) )
# dataprint = '**Hasil Pencarian (10 Hasil Relevan) **\n {listdata}'.format(listdata = listdata)

# print(dataprint)

# print(developer_check())