from . import user_api_rt
from .api import (dahsboard, login_params, login_form, login_json, sign_up, request_reset_password, reset_password, all_users, profile,
logout)

from fastapi.responses import JSONResponse

user_api_rt.get("/", name='user.api.dashboard', response_class=JSONResponse)(dahsboard)
user_api_rt.get("/profile", name='user.api.profile')(profile)
user_api_rt.get("/get_all_users/", name='user.api.get_all_users')(all_users)
user_api_rt.post("/signup/", name='user.api.signup')(sign_up)
user_api_rt.get("/token/", name='user.api.login', response_class=JSONResponse)(login_params)
user_api_rt.post("/token/", name='user.api.login', response_class=JSONResponse)(login_form)
user_api_rt.put("/token/",  name='user.api.login', response_class=JSONResponse)(login_json)
user_api_rt.get("/logout", name='user.api.logout', response_class=JSONResponse)(logout)
user_api_rt.post("/request_reset_password/", name='user.api.request_reset_password')(request_reset_password)
user_api_rt.put("/reset_password/", name='user.api.reset_password')(reset_password)
