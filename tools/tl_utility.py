import sqlite3, json
from sqlite3 import Error
from tools.config import config
from tools.dcc_utility import download_trustlist
from os import path
from datetime import datetime 

def db_connect():
    try:
        if not path.isfile(f"{config()['Main_Location']}/data/trustlist.sql"):
            config_data = config()
            config_data['Last_Updated_Tl'] = "2020-01-01T00:00:00+02:00"
            with open (f"{config()['Main_Location']}/config.json", "w") as c:
                json.dump(config_data, c, indent = 4)
                c.close()
        return sqlite3.connect(f"{config()['Main_Location']}/data/trustlist.sql")
    except Error as e:
        print(e)
        return None

def get_rawData(kid):
    sql_statement = """ SELECT rawData FROM certificates WHERE kid = ? """
    value = [kid, ]
    cur = db.cursor()
    cur.execute(sql_statement, value)
    row = cur.fetchall()
    cur.close()
    return str(row)

def check_for_entry(kid):
    cur = db.cursor()
    sql_statement = """ SELECT name FROM sqlite_master WHERE type = ? AND name = ? """
    values = ['table', 'certificates']
    cur.execute(sql_statement, values)
    result = cur.fetchall()
    if result == 0:
        sql_statement = """ SELECT EXISTS (SELECT 1 FROM certificates WHERE kid = ? """
        value = [kid, ]
        cur.execute(sql_statement, value)
        result = cur.fetchall()
    cur.close()
    return True if result == 1 else False 

def select_table_tl(certificateType, country):
    sql_statement = """ SELECT * FROM certificates """
    values = []
    if certificateType != None:
        sql_statement += """ WHERE certificateType = ? """
        values = (certificateType, )
        if country != None:
            sql_statement += """ AND country = ? """
            values += (country, )
    else:
        if country != None:
            sql_statement += """ WHERE country = ? """
            values = (country, )
    cur = db.cursor()
    cur.execute(sql_statement, values)
    rows = cur.fetchall()
    cur.close()
    return rows
    
def create_table():
    sql_statement = """ CREATE TABLE IF NOT EXISTS certificates (
        kid text PRIMARY KEY,
        country text,
        certificateType text,
        timestamp text,
        thumbprint text,
        signature text,
        rawData text
    ); """
    cur = db.cursor()
    cur.execute(sql_statement)
    cur.close()
    db.commit()

def update_table():
    cur = db.cursor() 
    for cert in json.loads(download_trustlist().text):
        if cert['rawData'] is not None:
            if not check_for_entry(cert['kid']):
                print(f"Inserting certificate with kid {cert['kid']}")
                sql_statement = """ INSERT OR IGNORE INTO certificates 
                (
                    kid, country, certificateType, timestamp, signature, thumbprint, rawData
                )
                VALUES(?,?,?,?,?,?,?) """
                values = (
                    cert['kid'], 
                    cert['country'], 
                    cert['certificateType'], 
                    cert['timestamp'], 
                    cert['signature'], 
                    cert['thumbprint'], 
                    cert['rawData']
                )
                cur.execute(sql_statement, values)
        else:
            print(f"Deleting certificate with kid {cert['kid']}")
            sql_statement = """ DELETE FROM certificates WHERE kid = ? """
            values = (cert['kid'],)
            cur.execute(sql_statement, values)
    cur.close()
    db.commit()
    config_data = config()
    config_data['Last_Updated_Tl'] = datetime.now().replace(microsecond=0).isoformat()+"+02:00"
    with open (f"{config()['Main_Location']}/config.json", "w") as c:
        json.dump(config_data, c, indent = 4)
        c.close()
    
def tl_init():
    global db
    db = db_connect()
    create_table()
    update_table()
    
    

