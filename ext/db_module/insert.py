import mysql.connector
from ext.db_module import connection
import json


def checktable():
    db = connection.connect()
    cursor = db.cursor()
    sql = "SHOW TABLES"
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


for val in checktable():
    exec(f"""def {val[0]}(value):
        db = connection.connect()
        cursor = db.cursor()
        cursor.execute('select * from {val[0]}')
        fetchdatacolumn = cursor.fetchall()
        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description]
        testfield = "("
        for i in range(len(field_names)):
            if field_names[i] == 'id':
                continue
            else:
                testfield += field_names[i]
            if i == len(field_names) - 1:
                break
            else:
                testfield += ", "
        testfield += ")"
        sql = 'INSERT INTO {val[0]} {{field}} VALUES {{value}}'.format(field = testfield, value = value)
        try:
            cursor.execute(sql)
            db.commit()
            return True
        except:
            print(sql)
            return False""")

# Example use:
# insert.history("('value1', 'value2', ...etc)")