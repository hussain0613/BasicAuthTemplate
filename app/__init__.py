from .config import get_env_vars
from .utils import db_init
env = get_env_vars()

engine, Base, Session = db_init(env)


from .user.models import User

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(env)

    from .user import user_bp
    
    app.register_blueprint(user_bp, url_prefix="/user/")
    
    return app

