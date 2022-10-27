# DATA SONAR

***

## Summary

This component provides a Docker image that collect technical data kpis on our apps and platforms. 

The code is composed of the following main folders:
- /conf: Contains templated configuration files used to create the tasks.
- /sql: Contains SQL sql to be run on MySQL in order to stream data into KAFKA.
- /scripts: Contains shell scripts responsible for replacing placeholders and contacting the MS SQLServer.

## Build & Run

### Build docker image
```
docker build -t dt-warroom-backend:latest .
```

### Create data-sonar container app
```
docker run \
    -v <path_to_queries_folder>:/app/sql \
    -v <path_to_conf_folder>:/app/conf \
    --env-file <path_to_env> \
    --name=dt-warroom-backend \
    dt-warroom-backend:latest
```
## 1)	Analyse_PDV_monthly. Dans BO : TELMA+DCG+BI+SAVE+Analyse_PDV_monthly. A rafraichir onglet 1 et 2+Enregistrer le fichier+Exporter en type de fichier Excel
## 
## 2)	PM_et_PDV_data. Dans BO : TELMA+DCG+GEOMARKET+CARTOGRAPHIE+cartographie PM et PDV_data. A rafraichir onglet 1 et 2+Enregistrer le fichier+Exporter en type de fichier Excel
## 
## 3)	Rapport_gratte_par_région. Dans BO : TELMA+DCG+BI+SAVE. Conception + dupliquer un rapport+A rafraichir onglet 1 et 2+date A ajouter +Enregistrer le fichier+Exporter en type de fichier Excel
## 
## 4)	Rapport_gratte_par_région recap. Dans BO : TELMA+DCG+BI+SAVE. A rafraichir onglet 1 et 2+date A ajouter +Enregistrer le fichier+Exporter en type de fichier Excel



