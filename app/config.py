import os
from dotenv import load_dotenv
#BASEDIR = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(BASEDIR, ".env"))

load_dotenv(".env")
SERVER_TYPE = os.getenv('ENVIRONMENT_TYPE')
if(SERVER_TYPE): load_dotenv(SERVER_TYPE+".env")

def get_env_vars():
    config = {
        "APP_NAME" : os.getenv("APP_NAME"),
        "SECRET_KEY" : os.getenv("SECRET_KEY"),
        "DATABASE_URI" : os.getenv("DATABASE_URI"),
        "MAIL_SERVER" : os.getenv("MAIL_SERVER"),
        "MAIL_PORT" : os.getenv("MAIL_PORT"),
        "MAIL_USERNAME" : os.getenv("MAIL_USERNAME"),
        "MAIL_PASSWORD" : os.getenv("MAIL_PASSWORD"),
        'MAIL_USE_TLS' : os.getenv('MAIL_USE_TLS')
    }
    return config
