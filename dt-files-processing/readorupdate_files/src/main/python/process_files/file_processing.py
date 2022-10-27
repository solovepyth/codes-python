import sys
import os
from pathlib import Path
#from pptx import Presentation
#from pptx.chart.data import CategoryChartData



module_path = str(Path(__file__).parent.parent.absolute())   
if module_path not in sys.path:       
    sys.path.append(module_path)


import pandas as pd

cheminsql=module_path+'/sql/'
#inputfilepath=
outputfilepath="D:/Utilisateurs/solonirina1/Documents/05 - Docs de gestion/09 - Equipe Data/Automation of telma TV/"

class pptx_to_process:
    def __init__(self,fichier,engine="openpyxl"):
        self.filename=fichier
        self.reader=pd.ExcelFile(self.filename,engine=engine)
    def list_all_sheets(self):
        r=self.reader
        self.sheetlist=r.sheet_names
        return self.sheetlist
    def parsesh(self,feuille):
        r=self.reader
        return r.parse(feuille)                
    def close_reader(self):
        r=self.reader
        r.close()


class excel_to_process:
    def __init__(self,fichier,engine="openpyxl"):
        self.filename=fichier
        self.reader=pd.ExcelFile(self.filename,engine=engine)
    def list_all_sheets(self):
        r=self.reader
        self.sheetlist=r.sheet_names
        return self.sheetlist
    def parsesh(self,feuille):
        r=self.reader
        return r.parse(feuille)                
    def close_reader(self):
        r=self.reader
        r.close()

class excel_to_write:
    def __init__(self,fichier,engine="openpyxl"):
        self.writer=pd.ExcelWriter(fichier,engine=engine)
    def init_sheet(self,df,feuille,index=True):
        pd.DataFrame(df).to_excel(self.writer,sheet_name=feuille,index=index)
        print(f"sheet {feuille} loaded")
    def close_writer(self):
        w=self.writer
        w.close()

if __name__=='__main__':
    fichier=excel_to_process('D:/Utilisateurs/solonirina1/Documents/05 - Docs de gestion/09 - Equipe Data/Automation of telma TV/report.xlsx')
    df_report=fichier.parsesh('allOffer')
    df_report=df_report[(df_report['Date']>='2022-10-11 00:00:01') & (df_report['Date']<='2022-10-20 23:59:59')]
    df_report['dt']=[x.strftime('%F')[:10] for x in df_report['Date']]
    df_report=df_report.rename(columns={'Date':'date injection','Shop':'shop','MSISDN':'msisdn'})
    print(df_report)
    print(df_report.dtypes)
    fichier.close_reader()
    df_export=pd.read_csv('D:/Utilisateurs/solonirina1/Documents/05 - Docs de gestion/09 - Equipe Data/Automation of telma TV/purchase_and_view.csv',sep=",").query("date>='2022-10-11'",engine="python")
    df_export['dateheure']=df_export["date"].str.cat(df_export["time"], sep=" ")
    df_export['dateheure']=pd.to_datetime( df_export['dateheure'])
    df_export['date']=df_export['date'].astype('str')
    df_join=pd.merge(df_export[(df_export['channel']=='BON.FIRST1.AIRTIME.TELMA.TV')].drop_duplicates(),df_report,how="left",left_on=["date","msisdn"],right_on=["dt",'msisdn'])
    df_join['diffsec']=[(x-y).total_seconds() if y<x else (y-x).total_seconds() for x,y in zip(df_join['dateheure'],df_join['date injection'])]
    df_ctrl_dttime=df_join.groupby(['msisdn','date','time']).agg({'diffsec':'min','msisdn':'count'})\
        .rename(columns={'msisdn':'nbnum'})\
        .reset_index()
    df_join=pd.merge(df_join,df_ctrl_dttime.rename(columns={'msisdn':'nd1','date':'date1','time':'time1','diffsec':'diffsec1'})[['nd1','date1','time1','diffsec1']],how="left",left_on=['msisdn','date','time','diffsec'],right_on=['nd1','date1','time1','diffsec1'])
    df_join['ndverif']=df_join['shop'].str[-9:]
    df_join.loc[(df_join['ndverif'].astype('str').str.isnumeric()==True) | (df_join['shop'].str[:10]=='Telma Shop'),'is_animateur']=1
    df_join=df_join[(df_join['nd1'].notna()) & (df_join['shop'].notna())]\
        .drop(columns=['nd1','date1','time1','diffsec1'])\
        .sort_values(by=['shop','msisdn','date','time'],ascending=True)[['date injection', 'shop','date', 'time', 'msisdn', 'channel', 'bundle', 'bundle_price', 'opitons', 'canals', 'date_visio', 'durations', 'top_canal', 'top_duration', 'sum_duration', 'Status', 'diffsec','is_animateur']]
    df_join['injection_animateur']=[1 if x==1 else 0 for x in df_join['is_animateur']]
    df_join['injection_msisdn_url']=[1 if ((x!=1) & (y!='')) else 0 for x,y in zip(df_join['is_animateur'],df_join['shop']) ]
    df_join['visionnage']=[1 if x!='[]' else 0 for x in df_join['channel']]
    #df_join['date_visio']=df_join['date_visio'].apply(lambda x: x.strip("][").split(','))
    #df_join['durations']=df_join['durations'].apply(lambda x: x.strip("][").split(','))
    #df_join['pairs'] = list(list(zip(a,b)) for a,b in zip(df_join['date_visio'], df_join['durations']))
    #df_join=df_join.explode('pairs')
    #df_join[['date_visio','duration_visio']] = pd.DataFrame(df_join.pairs.tolist(), index= df_join.index)
    #df_join['date_visio'] = pd.to_datetime(df_join['date_visio'])
    #df_join['date'] = pd.to_datetime(df_join['date'])
    #df_join['duration_visio'] = [int(float(str(x.strip().replace('','0')))) for x in df_join['duration_visio']]
    #df_join=df_join[df_join['date']==df_join['date_visio']]
    print(df_join.columns)
    print(df_export.columns)
    df = (df_join.groupby(['shop', 'msisdn','date']).agg({'injection_animateur':'sum','injection_msisdn_url':'sum','visionnage':'count'}).reset_index().rename(columns={'shop':'canal_injection','visionnage':'nb_visionnage'}).pivot_table(values=['injection_animateur', 'injection_msisdn_url','nb_visionnage'], 
                    index=['canal_injection', 'msisdn'], 
                    columns='date', 
                    aggfunc='first',
                    fill_value=0)
        .swaplevel(1, 0, axis=1)
        .sort_index(level=0, axis=1, sort_remaining=False))
    print(df) 
    
    
    
    fichier=excel_to_write(f"{outputfilepath}injections_bonus_first_telma_tv.xlsx")
    fichier.init_sheet(df_export[['date', 'time', 'msisdn', 'channel', 'bundle', 'bundle_price','opitons', 'canals', 'date_visio', 'durations', 'top_canal','top_duration', 'sum_duration']],'CAS',False)
    fichier.init_sheet(df_join[['date', 'time', 'msisdn', 'channel', 'bundle','bundle_price', 'opitons', 'canals', 'date_visio', 'durations','top_canal', 'top_duration', 'sum_duration','date injection', 'shop','Status', 'injection_animateur', 'injection_msisdn_url','visionnage']],'inj_bonus',False)
    fichier.init_sheet(df,'recap',True)
    fichier.close_writer()
    
    
    
    

    



    


    

    
    

   
    
  
    
   
    




