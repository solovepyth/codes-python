from asyncio.log import logger
import sys
import os
from pathlib import Path



module_path = os.path.abspath(Path(__file__).parent.parent)    
if module_path not in sys.path:       
    sys.path.append(module_path)
import pandas as pd
import calendar
import glob
from time import time,sleep
from config.config import Variables

from read_write_functions import *
from scripts.fastmerge import *
from multiprocessing.pool import ThreadPool
from multiprocessing import Process
from datetime import date,timedelta
import gc
import numpy as np


cheminsql=str(Path(module_path))+"/sql/"
#outputfilepath="/data/fichiers/datatree/"
outputfilepath="D:\\Utilisateurs\\solonirina1\\Documents\\03 - Tâches en cours\\Réccurent\\fireline\\dwh-12892\\"

if not os.path.isdir(outputfilepath):
    os.makedirs(outputfilepath,exist_ok=True)

def extract_dates(liste):
    req1=render_req(liste)
    df=extract_df([req1,78])
    return df


def extract_lst_req(liste,src=78):
    with ThreadPool(4) as pool:
        lst_req=list(pool.map(render_req,liste))
    lst_req=[[x,src] for x in lst_req]    
    return lst_req

@logging_decorator
def  ext_output_df(func,liste,nom):
    with ThreadPool(4) as pool:
        lstdf=pool.map(func,liste)
    df=pd.concat(lstdf,axis=0)
    df.to_parquet(f"{outputfilepath}{nom}.parquet",engine="fastparquet")

if __name__=='__main__':
    deb,fin='2022-09-14','2022-10-13'
    df=extract_dates([f'{cheminsql}dwh_dim_date.sql','plage','dwh_billing',deb,deb])
    lstdeb=[[value['sk_date_si'],value['date_d'].strftime("%F")] for key,value in df.iterrows()]
    df=extract_dates([f'{cheminsql}dwh_dim_date.sql','plage','dwh_billing',fin,fin])
    #lstfin=[[value['sk_date_si'],value['date_d'].strftime("%F")] for key,value in df.iterrows()]
    #lstded=[20]
    #dict_param={}
    #lstparam=[f'{cheminsql}DWH-12986.sql',lstdeb[0][1],lstfin[0][1],lstded[n]]
    #ext_output_df(extract_df,extract_lst_req(lstparam),f"DWH_12863_data{deb}")


    
    