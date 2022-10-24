from json import load
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class ProductionConfig(Config):
    DEBUG = os.getenv('DEBUG')
    print(DEBUG)
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_PORT= os.getenv('MYSQL_PORT')
    MYSQL_DB = os.getenv('MYSQL_DB')


config = {
    'production': ProductionConfig
}