from datetime import datetime
import time
from Import_DataBase import import_to_database

if __name__ == "__main__":
    # Forçar loopping parafuncionar pra sempre
    while True:
        r = import_to_database()
        if r == -1:
            time.sleep(10)
        
        # print("####################################################################")
        # print(datetime.now())
        # print("Nenhum arquivo para baixar...")
        # print("####################################################################")
    
