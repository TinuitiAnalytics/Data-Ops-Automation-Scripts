from openpyxl.reader import excel
import xlsxwriter
import openpyxl
import db_connection
import json
import pandas as pd
import tempfile
import numpy as np
from datetime import datetime

with open('query_config.json','r') as file:
    config_data = json.load(file)

def get_cmx_data(dataset_name,dimensions):
    #date range condition from/ To and in condition
    #cam,report,dim
    #min report date , dic dim
    dw_query = f''' select  distinct({dimensions}) from  {dataset_name} ; '''
    db_conn.execute(dw_query)
    # headers_dt = [field[0] for field in db_conn.description]
    data_dt = db_conn.fetchall()
    return  data_dt    



def compare_dimensions():
    check_list = []
    for dataset_name,value in config_data.items():
        for dimensions in value['dimensions']:
            if dimensions == 'device':
                data_dt = get_cmx_data(dataset_name,dimensions)
                dw_val = []
                for i in data_dt:
                    for j in i:
                        dw_val.append(j)
                unmatched_list_device = dataset_name , dimensions ,list(set(value['expected_device_values']) - set(dw_val)) + list(set(dw_val) - set(value['expected_device_values'])) 
                if unmatched_list_device is not None:
                    check_list.append(unmatched_list_device) 
            elif dimensions == 'brand':
                data_dt_br = get_cmx_data(dataset_name,dimensions)
                dw_val_br = []
                for i in data_dt_br:
                    for j in i:
                        dw_val_br.append(j)
                unmatched_list_brand = dataset_name , dimensions , list(set(value['expected_brand_values']) - set(dw_val_br)) + list(set(dw_val_br) - set(value['expected_brand_values'])) 
                if unmatched_list_brand is not None:
                    check_list.append(unmatched_list_brand)
    res_list = []
    for item in sorted(check_list, key=lambda check_list: check_list[2]):
        res_list.append(item)
    with open('unmatched_dimensions.txt', 'w') as f:
        for item in res_list:
            f.write(str(item)+'\n')
        f.close()   


if __name__ == "__main__":
    start = datetime.now()
    print(f"Start Process Time {start}")
    db_conn, con = db_connection.db_connect()
    compare_dimensions()
    print("table imported !")
    db_conn.close()
    con.close()
    end = datetime.now()
    print(f"End Process Time {end}")
   