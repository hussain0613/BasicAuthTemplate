from .. import Base, Session, env

from flask import Blueprint

user_bp = Blueprint("user", __name__)
user_api_bp = Blueprint("api", __name__)

from . import api

