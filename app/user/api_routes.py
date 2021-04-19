from . import user_api_rt
from .api import (dahsboard, login, sign_up, request_reset_password, reset_password, all_users)

user_api_rt.get("/")(dahsboard)
user_api_rt.get("/get_all_users/")(all_users)
user_api_rt.post("/signup/")(sign_up)
user_api_rt.post("/login/")(login)
user_api_rt.post("/request_reset_password/")(request_reset_password)
user_api_rt.put("/reset_password/")(reset_password)
