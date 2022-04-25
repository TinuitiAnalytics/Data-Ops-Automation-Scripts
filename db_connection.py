import psycopg2
import json


with open('config.json','r') as file:
    config_data = json.load(file)

def db_connect():
    con = psycopg2.connect(dbname= config_data["dbname"], host=config_data["host"],
    port= config_data["port"], user= config_data["user"], password= config_data["password"])
    cur = con.cursor()
    return cur, con

if __name__ == "__main__":
    pass

