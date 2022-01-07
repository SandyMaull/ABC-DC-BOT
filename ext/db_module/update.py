import mysql.connector
from ext.db_module import connection
import json

def one(table, fieldKey, valueKey, fieldUpdate, valueUpdate):
    db = connection.connect()
    cursor = db.cursor()
    sql = "UPDATE {table} SET {fieldUpdate} = '{valueUpdate}' WHERE {fieldKey} = '{valueKey}'".format(table = table, fieldUpdate = fieldUpdate, valueUpdate = valueUpdate, fieldKey = fieldKey, valueKey = valueKey)
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except:
        print('Error when updating data!')
        return False