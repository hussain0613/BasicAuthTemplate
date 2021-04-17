import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

def get_env_vars():
    config = {
        "SECRET_KEY" : os.getenv("SECRET_KEY"),
        "DATABASE_URI" : os.getenv("DATABASE_URI")
    }
    return config
