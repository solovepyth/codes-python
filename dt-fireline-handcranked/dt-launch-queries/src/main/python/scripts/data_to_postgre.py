import sys
import os
from pathlib import Path

module_path = str(Path(__file__).parent.parent.absolute())   
if module_path not in sys.path:       
    sys.path.append(module_path)

import csv
import pandas as pd
import urllib
from io import StringIO
from jinja2 import Template
from sqlalchemy import create_engine
from importlib import reload
from config.config import Variables
from time import time
from datetime import datetime,date,timedelta
from multiprocessing.pool import ThreadPool
from scripts.read_write_functions import *
import psycopg2
import logging
import glob
reload(logging)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)


cheminsql=module_path+'/sql/'





def drop_table_if_exists_pg(tablename,variables=Variables()):
    conn=psycopg2.connect(\
        database=variables.DB_NAMEPG,\
        user=variables.DB_USERPG,\
        password=variables.DB_PASSWORDPG,\
        host=variables.DB_HOSTPG,\
        port=variables.DB_PORTPG\
    )
    cursor = conn.cursor()
    logging.info("curseur créé")
    sql = f'''DROP table IF EXISTS {variables.DB_SCHEMAPG}.{tablename} '''
    cursor.execute(sql)
    logging.info("table supprimée !")
    with open(cheminsql+f"{tablename}_create.sql") as f:
        req=Template(f.read()).render()
    cursor.execute(req)
    logging.info("table crée !")    
    conn.commit();conn.close()

def drop_table__pg(tablename,variables=Variables()):
    conn=psycopg2.connect(\
        database=variables.DB_NAMEPG,\
        user=variables.DB_USERPG,\
        password=variables.DB_PASSWORDPG,\
        host=variables.DB_HOSTPG,\
        port=variables.DB_PORTPG\
    )
    cursor = conn.cursor()
    logging.info("curseur créé")
    sql = f'''DROP table IF EXISTS {variables.DB_SCHEMAPG}.{tablename} '''
    cursor.execute(sql)
    logging.info("table supprimée !")
    

def create_lower_dict(df):
    dico={k:v for k,v in dict(zip(df.columns.tolist(),[x.lower() for x in df.columns.tolist()])).items()}
    return dico


def extract_and_load(liste,variables=Variables()):
    src_liste=[21,78]
    if liste[1] not in src_liste:
        logging.error("pas un host sql server existant")
    elif liste[1]==src_liste[0]:
        HOST=variables.DB_HOST2
    else:
        HOST=variables.DB_HOST1
    uri1=f"mssql+pyodbc://{HOST}:{variables.DB_PORT}/{variables.DB_NAME}?driver=SQL+server"
    engine=create_engine(uri1);conn=engine.connect()
    df=pd.read_sql_query(liste[0],conn)
    conn.close();engine.dispose()
    logging.info("Dataframe extrait")
    uri2=f"postgresql+psycopg2://{variables.DB_USERPG}:{variables.DB_PASSWORDPG}@{variables.DB_HOSTPG}:{variables.DB_PORTPG}/{variables.DB_NAMEPG}"
    engine=create_engine(uri2);conn=engine.connect()
    df.rename(columns=create_lower_dict(df)).to_sql(liste[2], con=create_engine(uri2),schema=variables.DB_SCHEMAPG,chunksize=300000, index=False,if_exists='append')
    conn.close();engine.dispose()
    logging.info("table chargée")

def df_to_postgres(liste,variables=Variables()):
    variables=Variables()
    lstfile=glob.glob(os.path.join(liste[0],liste[1]))
    uri2=f"postgresql+psycopg2://{variables.DB_USERPG}:{variables.DB_PASSWORDPG}@{variables.DB_HOSTPG}:{variables.DB_PORTPG}/{variables.DB_NAMEPG}"
    engine=create_engine(uri2);conn=engine.connect()
    for f in lstfile[:3]:
        df=pd.read_parquet(f)
        df['dateofactivity']=datetime.strptime(Path(f).stem[-10:],"%Y_%m_%d").date()
        start_time=time()
        df.rename(columns=create_lower_dict(df)).to_sql(liste[2], con=create_engine(uri2),schema=variables.DB_SCHEMAPG,chunksize=500000, index=False,if_exists='replace')
        print(f"fichier {Path(f).stem} loaded in {str(timedelta(time()-start_time))}")
        conn.close();engine.dispose()
    logging.info("table fully loaded")

def genererate_create_ddl(liste,variables=Variables()):
    uri1=f"mssql+pyodbc://TDBP78WV:{variables.DB_PORT}/{variables.DB_NAME}?driver=SQL+server"
    logging.info(f"uri:{uri1}")
    with open(f"{cheminsql}select_all_fromtable.sql") as f:
        req=Template(f.read()).render(liste=liste)
        engine=create_engine(uri1);conn=engine.connect()
        df=pd.read_sql_query(req,conn)
        conn.close();engine.dispose()
        logging.info("Dataframe extrait")
    uri2=f"postgresql+psycopg2://{variables.DB_USERPG}:{variables.DB_PASSWORDPG}@{variables.DB_HOSTPG}:{variables.DB_PORTPG}/{variables.DB_NAMEPG}"
    engine=create_engine(uri2);conn=engine.connect()
    df.head(0).to_sql(liste[1], con=create_engine(uri2),schema=variables.DB_SCHEMAPG, index=False,if_exists='replace')
    conn.close();engine.dispose()
    logging.info("table chargée")


def extract_and_load_with_chunks(table,src,variables=Variables()):
    src_liste=[21,78]
    if src not in src_liste:
        logging.error("pas un host sql server existant")
    elif src==src_liste[0]:
        HOST=variables.DB_HOST2
    else:
        HOST=variables.DB_HOST1

    uri1=f"mssql+pyodbc://{HOST}:{variables.DB_PORT}/{variables.DB_NAME}?driver=SQL+server"
    engine=create_engine(uri1);conn=engine.connect()
    with open(Cheminsql+f'{table}.sql') as f:
        req=Template(f.read()).render()        
        iteration=0
        conn2=psycopg2.connect(\
        database=variables.DB_NAMEPG,\
        user=variables.DB_USERPG,\
        password=variables.DB_PASSWORDPG,\
        host=variables.DB_HOSTPG,\
        port=variables.DB_PORTPG\
        )
        for df in pd.read_sql_query(req,conn,chunksize=50000):
            sio = StringIO()
            writer = csv.writer(sio)
            writer.writerows(df.values)
            sio.seek(0)
            with conn2.cursor() as c:
                c.copy_from(
                    file=sio,
                    table=f"{table}",
                    columns=df.rename(columns=create_lower_dict(df)).columns.tolist(),
                    sep=","
                )
                conn2.commit()            
            iteration+=df.shape[0]
            logging.info(f"{iteration} lignes chargée")        
        logging.info("table totalement extraite")
        conn2.close()
    conn.close();engine.dispose()

if __name__=='__main__':
    lstdates=[x.strftime("%F") for x in pd.date_range(start="2022-09-01",end="2022-10-10")]
    lstreq=[render_req([f"{cheminsql}select_all_fromtable.sql",'dwh_all_billing','dwh_fact_sgsn_msisdn','day',x,78,1000]) for x in lstdates]
    lstparam=[[x,78,'dwh_fact_sgsn_msisdn'] for x in lstreq]
    with ThreadPool(4) as pool:
        pool.map(extract_and_load,lstparam)