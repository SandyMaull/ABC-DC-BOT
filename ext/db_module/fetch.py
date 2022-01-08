import mysql.connector
from ext.db_module import connection
import json
import asyncio

async def one(table, field, value):
    db = connection.connect()
    cursor = db.cursor()
    sql = "SELECT * FROM {table} WHERE {field} = '{value}'".format(table = table, field = field, value = value)
    try:
        exec_com = lambda: cursor.execute(sql)
        data = lambda: cursor.description
        result = lambda: cursor.fetchone()
        exec_com = await asyncio.to_thread(exec_com)
        data = await asyncio.to_thread(data)
        result = await asyncio.to_thread(result)
        i = 0
        column_name = {}
        while i < len(data):
            column_name[data[i][0]] = str(result[i])
            i += 1
        return json.dumps(column_name)
    except:
        return False

def many(table, field, value):
    db = connection.connect()
    cursor = db.cursor()
    sql = "SELECT * FROM {table} WHERE {field} = '{value}'".format(table = table, field = field, value = value)
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

def all(table):
    db = connection.connect()
    cursor = db.cursor()
    sql = "SELECT * FROM {table}".format(table = table)
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