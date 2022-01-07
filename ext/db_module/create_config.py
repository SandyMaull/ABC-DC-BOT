import mysql.connector
from ext.db_module import connection
from ext.db_module import create_table

def create():
    if create_table.create() == False:
        print('Table already exists!, continue to next job')

    db = connection.connect()
    cursor = db.cursor()
    sql = "INSERT INTO config (name, value) VALUES (%s, %s)"
    values = [
        ('DEBUG', 'FALSE'),
        ('MUSIC', 'FALSE'),
        ('ALBION', 'FALSE'),
    ]

    try:
        for val in values:
            cursor.execute(sql, val)
            db.commit()
        print("Success insert data to table!")
        return True
    except:
        print("Fail to insert data to table, check permission or content of data!")
        return False
