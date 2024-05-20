import os
from pathlib import Path
import cx_Oracle
from datetime import datetime
from config import ora_db_user, ora_db_pass, ora_db_sn
from Error_Log import write_erro_log

def execute_sql(str_sql):
    try:
        conn = cx_Oracle.connect(ora_db_user, ora_db_pass, ora_db_sn)
        crsr = conn.cursor()
        crsr.execute(str_sql)
        conn.commit()
        
    except Exception as e:
        write_erro_log(erro_log=str(e))
            
def execute_sql_multi(list_query):
    try:
        conn = cx_Oracle.connect(ora_db_user, ora_db_pass, ora_db_sn)
        crsr = conn.cursor()

        for index, query in enumerate(list_query):
            crsr.execute(query)
            conn.commit()
            print("********************************************")
            print(f"Comando {index} executado")
            print("********************************************")
        
        conn.close()
    
    except Exception as e:
        write_erro_log(erro_log=str(e))
        
