from . import Session, user_rt, env
from .models import User
from .pydantic_models import (LoginModel, SignUpModel, RequestResetPasswordModel, ResetPasswordModel)

from fastapi import Response, Request
import json

#@user_rt.get("/")
async def dahsboard(request:Request):
    #token = request.query_params.get('login_token')
    token = request.headers.get("Authorization")
    print(token)
    if(token):
        resp = User.verify_login_token(token.split()[1], Session(), env['SECRET_KEY'])
        if(resp.get('user')): 
            #resp['user'] = resp['user'].to_dict()
            #resp['user'].pop("password")
            resp['message'] = f"Hello! you are logged in as {resp['user']['username']}"
        return resp
    
    return {"Message": "Hello. You are in not logged in dashboard now"}


#@user_rt.post("/signup/")
async def sign_up(info:SignUpModel, request:Request):
    data = await request.json()
    resp = User.create_user(Session(), **data)
    if resp.get('user'):
        if(resp['user'].get('password')): 
            resp['user'].pop('password')
    #else:
    #    resp = {"message": "user not created, username/mail already", "user": None}
    
    return resp

#@user_rt.post("/login/")
async def login(info:LoginModel, request:Request):
    data = await request.json()
    resp = {}
    if(data.get("password")):
        password = data.pop("password")
        res = User.get_login_token(Session(), env["SECRET_KEY"], password, **data)
        resp = Response()
        resp.headers["Authorization"] = f"Bearer {res['token']}"
        resp.headers["Content-Type"] = "application/json"
        resp.body = json.dumps(res).encode()
    else:
        resp["message"] = "No passowrd provided"
    return resp

#@user_rt.post("/request_reset_password/")
async def request_reset_password(info:RequestResetPasswordModel, request:Request):
    data = await request.json()
    resp = User.get_reset_password_token(data.get('email'), env['SECRET_KEY'], Session())
    return resp

#@user_rt.put("/reset_password/")
async def reset_password(info:ResetPasswordModel, token:str,request:Request):
    #token = await request.query_params.get('token')
    data = await request.json()
    email = data.get('email')
    pw = data.get('password')
    if(not token or not pw): return {"Message": "missing token/new password"}
    resp = User.reset_password(email, pw, token, env['SECRET_KEY'], Session())
    #print(f"[******************] {type(resp)}")
    return resp


#@user_rt.get("/get_all_users/")
async def all_users(request:Request):
    users = User.get_all(Session())
    resp = []
    for user in users:
        d = user.to_dict()
        #d.pop("password")
        resp.append(d)
    return {'users': resp}


