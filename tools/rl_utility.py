import sqlite3, json
from sqlite3 import Error
from tools.config import config
from tools.dcc_utility import download_revocationlist
from os import path

def db_connect():
    try:
        if not path.isfile(f"{config()['Main_Location']}/data/revocationlist.sql"):
            config_data = config()
            config_data['Last_Updated_Rl'] = "2020-01-01T00:00:00+02:00"
            with open (f"{config()['Main_Location']}/config.json", "w") as c:
                json.dump(config_data, c, indent = 4)
                c.close()
        return sqlite3.connect(f"{config()['Main_Location']}/data/revocationlist.sql")
    except Error as e:
        print(e)
        return None

def check_for_entry(batchId):
    cur = db.cursor()
    sql_statement = """ SELECT name FROM sqlite_master WHERE type = ? AND name = ? """
    values = ['table', 'batches']
    cur.execute(sql_statement, values)
    result = cur.fetchall()
    if result == 0:
        sql_statement = """ SELECT EXISTS (SELECT 1 FROM batches WHERE batchId = ? """
        value = [batchId, ]
        cur.execute(sql_statement, value)
        result = cur.fetchall()
    cur.close()
    return True if result == 1 else False 

def select_table_rl(deleted, country):
    sql_statement = """ SELECT * FROM batches """
    values = []
    if deleted != None:
        sql_statement += """ WHERE deleted = ? """
        values = (deleted, )
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
    sql_statement = """ CREATE TABLE IF NOT EXISTS batches (
        batchId text PRIMARY KEY,
        country text,
        date text,
        deleted text
    ); """
    cur = db.cursor()
    cur.execute(sql_statement)
    cur.close()
    db.commit()

def update_table():
    cur = db.cursor() 
    batchlist = download_revocationlist().text
    if batchlist:
        for batch in json.loads(batchlist)['batches']:
            if not check_for_entry(batch['batchId']):
                print(f"Inserting batch with batchId {batch['batchId']}")
                sql_statement = """ INSERT OR IGNORE INTO batches
                (
                    batchId, country, date, deleted
                )
                VALUES(?,?,?,?) """
                values = (
                    batch['batchId'], 
                    batch['country'],  
                    batch['date'], 
                    batch['deleted']
                )
                cur.execute(sql_statement, values)
    cur.close()
    db.commit()
    
def rl_init():
    global db
    db = db_connect()
    create_table()
    update_table()
    
    

