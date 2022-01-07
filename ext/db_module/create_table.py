import mysql.connector
from ext.db_module import connection

def create():
    db = connection.connect()
    cursor = db.cursor()
    sql = """
    CREATE TABLE config (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        value VARCHAR(255)
    )
    """

    try:
        cursor.execute(sql)
        print("Success creating table!")
        return True
    except:
        print("Fail to create table, check permission or may table is already exists!")
        return False