from .. import Base, Session, env

from fastapi import APIRouter

user_api_rt = APIRouter()
user_rt = APIRouter()


from . import routes
user_rt.include_router(user_api_rt, prefix="/api")
