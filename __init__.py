import os
import json

from mysql.connector import connect

with open(os.getcwd() + '/config.json') as config:
    data = json.load(config)

DB = connect(
    host=data['db_host'],
    port=3306,
    user=data['db_user'],
    password=data['db_pass'],
    database=data['db_name'],
)
selection = DB.cursor()