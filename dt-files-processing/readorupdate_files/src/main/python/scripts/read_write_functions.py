import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

import pandas as pd
from jinja2 import Template

from config.config import Variables
from sqlalchemy import create_engine

import logging
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s:%(message)s', level=logging.INFO, datefmt='%I:%M:%S')





def render_req(liste):
    logger = logging.getLogger(f'__render_req_{Path(liste[0]).stem}__')
    logger.info(f"Process Id : {os.getpid()}")      
    with open(liste[0]) as f:
        req=Template(f.read()).render(liste=[x for x in liste [1:]])
    logger.info(req)
    return req

def render_with_macro(fichier,env):
    render = env.from_string(open(fichier, 'r').read()).render()
    return render

def extract_df(liste,variables=Variables()):
    logger = logging.getLogger('__extract_df__') 
    src_liste=[21,78]
    if liste[1] not in src_liste:
        logger.error("pas un host sql server existant")
    elif liste[1]==21:
        HOST=variables.DB_HOST2
    elif liste[1]==78:
        HOST=variables.DB_HOST1
    logger.info(f"hôte:{HOST}")
    uri=f"mssql+pyodbc://{HOST}:{variables.DB_PORT}/{variables.DB_NAME}?driver=SQL+server"
    engine=create_engine(uri)
    conn=engine.connect()
    logger.info(f"engin créé")
    try:
        df=pd.read_sql_query(liste[0],conn)
        logger.info("données extraites")
        logger.info(df)
    except Exception as e:
        logger.error(e)
        df=pd.DataFrame()
    conn.close();engine.dispose()
    return df

def df_to_fastparquet(liste):
    extract_df(liste[0]).to_parquet(liste[1],compression="gzip",engine="fastparquet")
