import mysql.connector
from ext.db_module import connection
import json


def one(guild_id, table, field, value):
    db = connection.connect()
    cursor = db.cursor()
    guild_id = str(guild_id)
    if table != 'guild':
        sql = "SELECT {table}.* FROM {table} INNER JOIN guild ON guild.guild_id = '{guild_id}' AND {table}.guild_id = guild.id AND {table}.{field} = '{value}'".format(guild_id = guild_id, table = table, field = field, value = value)
    else:
        sql = "SELECT * FROM {table} WHERE {field} = '{value}'".format(table = table, field = field, value = value)
    # print(sql)
    try:
        cursor.execute(sql)
        data = cursor.description
        result = cursor.fetchone()
        i = 0
        column_name = {}
        while i < len(data):
            column_name[data[i][0]] = str(result[i])
            i += 1
        return json.dumps(column_name)
    except:
        return False

def many(guild_id, table, field, value):
    db = connection.connect()
    cursor = db.cursor()
    guild_id = str(guild_id)
    sql = "SELECT {table}.* FROM {table} INNER JOIN guild ON guild.guild_id = '{guild_id}' AND {table}.guild_id = guild.id AND {table}.{field} = '{value}'".format(guild_id = guild_id, table = table, field = field, value = value)
    # print(sql)
    try:
        cursor.execute(sql)
        data = cursor.description
        result = cursor.fetchall()
        g = 0
        finaldata = {}
        for items in result:
            column_name = {}
            i = 0
            while i < len(data):
                column_name[data[i][0]] = str(items[i])
                i += 1
            finaldata[g] = column_name
            g += 1
        return json.dumps(finaldata)
    except:
        return False

def all(guild_id, table):
    db = connection.connect()
    cursor = db.cursor()
    guild_id = str(guild_id)
    sql = "SELECT {table}.* FROM {table} INNER JOIN guild ON guild.guild_id = '{guild_id}' AND {table}.guild_id = guild.id".format(guild_id = guild_id, table = table)
    # print(sql)
    try:
        cursor.execute(sql)
        data = cursor.description
        result = cursor.fetchall()
        g = 0
        finaldata = {}
        for items in result:
            column_name = {}
            i = 0
            while i < len(data):
                column_name[data[i][0]] = str(items[i])
                i += 1
            finaldata[g] = column_name
            g += 1
        return json.dumps(finaldata)
    except:
        return False

# print(one(665154027318804497, "config", 'name', 'MUSIC'))
# print(one(787698443442323476, "guild", 'guild_id', '787698443442323476'))