from openpyxl.reader import excel
import xlsxwriter
import openpyxl
import json
import pandas as pd
import tempfile
import numpy as np
from datetime import datetime
import xlrd
import db_connection

def get_cmx_data(SQL_query):
    dw_query = f''' {SQL_query} '''
    db_conn.execute(dw_query)
    data_dt = db_conn.fetchall()
    # headers_dt = [field[0] for field in db_conn.description]
    return   data_dt , #headers_dt

def get_ex_value():
    df = pd.read_excel('Dynamic dimension.xlsx') 
    res_list = []
    for ind in df.index:
        if df['excecute Y/N'][ind] == 'Yes':
            res_dict = {}
            SQL_query = df['SQL query'][ind]
            test_case_number = df['TC'][ind]
            sql_res = get_cmx_data(SQL_query)
            res_dict['test_case_number'] = test_case_number
            res_dict['Spend Clicks Impresion'] = sql_res
            res_list.append(res_dict)
    df1 = pd.DataFrame(res_list)
    file_name = 'result_data.xlsx'
    df1.to_excel(file_name,index=False)


if __name__ == "__main__":
    start = datetime.now()
    print(f"Start Process Time {start}")
    db_conn, con = db_connection.db_connect()
    get_ex_value()
    print("Data excel export completed")
    db_conn.close()
    con.close()
    end = datetime.now()
    print(f"End Process Time {end}")