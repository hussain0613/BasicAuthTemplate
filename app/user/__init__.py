from .. import Base, Session, env

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

user_api_rt = APIRouter()
user_rt = APIRouter()
user_rt.mount(path = "/statics", app = StaticFiles(directory="app/user/statics"), name="statics")
#user_rt.mount("/",)


from . import routes
user_rt.include_router(user_api_rt, prefix="/api")
