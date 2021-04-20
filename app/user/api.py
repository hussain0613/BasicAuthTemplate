## when building csrf token scope takeo may be hash kore deoa jay... or may be csrf token gular jonno amar custom token gen use kora jay
## for every form submission the client will first ask for a csrf token with a scope, server will generate one and send to the client
## thn client will use it when submitting form
## most probably don't need the csrf token as all important resources will be guarded by user's password

from . import Session, user_api_rt, env
from .models import User
from .pydantic_models import (LoginModel, SignUpModel, RequestResetPasswordModel, ResetPasswordModel)
from .utils import check_n_set_auth_head

from fastapi import Response, Request, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/api/token')
async def get_current_user(token:str = Depends(oauth2_scheme)):
    r = User.verify_login_token(token, Session(), env['SECRET_KEY'])
    return r.get('user')


async def dahsboard(request:Request):
    resp = Response()
    resp.headers['content-type'] = 'application/json'
    user = check_n_set_auth_head(request, resp)
    if user:
        r_dict = {}
        r_dict['message'] = f"Hello! you are logged in as {user['username']}"
        r_dict['user'] = user
        resp.body = json.dumps(r_dict, default=str).encode()
        return resp
    
    return {
        "Message": "Hello. You are in not logged in dashboard now",
        "user":None,
        "links":{
            "login":{
                'api': request.url_for('user.api.login')#'https://127.0.0.1:800/user/api/login'
            },
            'signup': {
                'api': request.url_for('user.api.signup')
            },
            'testing': request.url_for('user_statics', path="/index.html")
        }
    }

async def all_users(request:Request):
    users = User.get_all(Session())
    resp = []
    for user in users:
        d = user.to_dict()
        resp.append(d)
    return {'users': resp}

async def profile(user:dict = Depends(get_current_user)):
    return user

async def sign_up(info:SignUpModel, request:Request):
    data = await request.json()
    resp = User.create_user(Session(), **data)
    if resp.get('user'):
        if(resp['user'].get('password')): 
            resp['user'].pop('password')
    
    return resp

async def login(**data):
    resp = Response()
    user_data = {}
    if data.get('username'):
        user_data['username'] = data['username']
    if data.get('email'):
        user_data['email'] = data['email']
    
    if(data.get("password")):
        password = data.pop("password")
        res = User.get_login_token(Session(), env["SECRET_KEY"], password, **user_data)
        if res.get('token'):
            resp = Response()
            if(data.get('remember_me')) and data.get('remember_me') in [True, 'true', 'True', 1]: resp.set_cookie("tk", res['token'])
            resp.headers['content-type'] = 'application/json'
            resp.body = json.dumps({'access_token': res['token'], 'token_type': 'bearer'}).encode()
            return resp
        
    resp.headers['content-type'] = 'application/json'
    resp.body = json.dumps({'detail': "invalid username/password_2"}).encode()
    return resp

async def login_form(request:Request, form_data: OAuth2PasswordRequestForm = Depends()):
    ## this one is accessed with post method
    form_data = await request.form()
    data = {}
    for key in form_data:
        data[key] = form_data.get(key)
    return await login(**data)
    
async def login_params(request:Request, username, password, remember_me):
    ## this one is accessed with get method
    params = request.query_params
    data ={}

    for key in params:
        data[key] = params.get(key)
    return await login(**data)

async def login_json(request:Request, cred:LoginModel):
    ## this one is accessed with put method
    data = await request.json()
    return await login(**data)

async def logout():
    resp = Response()
    resp.headers['content-type'] = 'application/json'
    #resp.set_cookie('tk', '')
    resp.delete_cookie('tk')
    resp.body = json.dumps({"message": "logged out"}).encode()
    return resp

async def request_reset_password(info:RequestResetPasswordModel, request:Request):
    data = await request.json()
    resp = User.get_reset_password_token(data.get('email'), env['SECRET_KEY'], Session())
    return resp

async def reset_password(info:ResetPasswordModel, token:str,request:Request):
    data = await request.json()
    email = data.get('email')
    pw = data.get('password')
    if(not token or not pw): return {"Message": "missing token/new password"}
    resp = User.reset_password(email, pw, token, env['SECRET_KEY'], Session())
    return resp



