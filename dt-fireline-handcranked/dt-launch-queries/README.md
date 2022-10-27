# fireline handcranked

***

## Summary

This component provides a Docker image that collect technical data kpis on our apps and platforms. 

The code is composed of the following main folders:
- /conf: Contains templated configuration files used to create the tasks.
- /sql: Contains SQL sql to be run on.
- /scripts: Contains reusable python scripts .

## Build & Run

### Build docker image
```
docker build -t dt-fireline-handcranked:latest .
```

### Create fireline-handcranked container app
```
docker run \
    -v <path_to_queries_folder>:/app/sql \
    -v <path_to_conf_folder>:/app/conf \
    --env-file <path_to_env> \
    --name=dt-warroom-backend \
    dt-warroom-backend:latest
```




