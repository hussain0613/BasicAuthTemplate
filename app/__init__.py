from .config import get_env_vars
from .utils import db_init
env = get_env_vars()

engine, Base, Session = db_init(env)


from .user.models import User

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()
    app.mount(path = "/user/statics", app = StaticFiles(directory="app/user/statics"), name="user_statics")
    
    from .user import user_rt
    
    app.include_router(user_rt, prefix="/user")
    
    return app

