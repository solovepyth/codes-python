import os
from dotenv import load_dotenv

load_dotenv()


class Variables(object):
    ENV = os.environ.get('ENV')
    APP_NAME = os.environ.get('APP_NAME')
    DB_NAME=os.environ.get('DB_NAME')
    DB_NAMEPG=os.environ.get('DB_NAMEPG')
    DB_HOST1 = os.environ.get('DB_HOST1')
    DB_HOST2 = os.environ.get('DB_HOST2')
    DB_HOSTPG = os.environ.get('DB_HOSTPG')
    DB_SCHEMA = os.environ.get('DB_SCHEMA')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_SCHEMAPG = os.environ.get('DB_SCHEMAPG')
    DB_PORTPG = os.environ.get('DB_PORTPG')
    DB_USERPG = os.environ.get('DB_USERPG')
    DB_PASSWORDPG = os.environ.get('DB_PASSWORDPG')
    WORK_DIR=os.environ.get('WORK_DIR')    
    JSON_CONF_TEMPLATE_FILE=os.environ.get('JSON_CONF_TEMPLATE_FILE')
