import json

def config():
    with open ("C:/Users/A200022244/Dev/DCC-Administration/config.json") as c:
        data = json.load(c)
        c.close()
        return data
    