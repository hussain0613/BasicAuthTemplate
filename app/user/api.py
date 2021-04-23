## when building csrf token scope takeo may be hash kore deoa jay... or may be csrf token gular jonno amar custom token gen use kora jay
## for every form submission the client will first ask for a csrf token with a scope, server will generate one and send to the client
## thn client will use it when submitting form
## most probably don't need the csrf token as all important resources will be guarded by user's password

## ** remeber nam e ulta palta character dile unhandled exception raise kore
## ** also kichu jaygay token return kortasi.. for test now.. pore bondho korte hobe

from . import Session, user_api_rt, env, mail_client
from .models import User, Action
from .pydantic_models import (LoginModel, SignUpModel, RequestResetPasswordModel, ResetPasswordModel)
from .utils import check_n_set_auth_head

from email.message import MIMEPart
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
        "message": "Hello. You are in not logged in dashboard now",
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


async def request_signup(info:RequestResetPasswordModel, request:Request):
    data = await request.json()
    ses = Session()
    resp = User.get_create_user_token(data.get('email'), env['SECRET_KEY'], Session())

    if resp.get('token'):
        mail_msg = MIMEPart()
        mail_msg['From'] = f"{env['APP_NAME']}"
        mail_msg['To'] = f"{data.get('email')}"
        mail_msg['Subject'] = "Confirm Email"

        mail_msg.set_content(
            f"""Follow the link below to complete signup, duration 7 days:
{request.url_for('signup_view')}?token={resp.get('token')}
            """
        )
        mail_client.send_message(mail_msg)
        #resp.pop('token')
        resp['message'] = "email has been sent to user's email address with instructions"
    return resp

async def sign_up(info:SignUpModel, token:str, request:Request):
    data = await request.json()
    resp = User.create_user(Session(), token, env['SECRET_KEY'], **data)
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
    ses = Session()
    resp = User.get_reset_password_token(data.get('email'), env['SECRET_KEY'], ses)

    if resp.get('token'):
        mail_msg = MIMEPart()
        mail_msg['From'] = f"{env['APP_NAME']}"
        mail_msg['To'] = f"{User.get_user_by(ses, email = data.get('email')).email}"
        mail_msg['Subject'] = "Reset Password Request"

        mail_msg.set_content(
            f"""Follow the link below to change reset your password, duration 5 minutes:
{request.url_for('reset_password_veiw')}?token={resp['token']}
            """
        )
        mail_client.send_message(mail_msg)
        #resp.pop('token')
    resp['message'] = "email has been sent to user's email address with instructions"
    return resp

async def reset_password(info:ResetPasswordModel, token:str, request:Request):
    data = await request.json()
    email = data.get('email')
    pw = data.get('password')
    if(not token or not pw): return {"message": "missing token/new password"}
    resp = User.reset_password(email, pw, token, env['SECRET_KEY'], Session())
    return resp


async def get_all_actions():
    actions = Action.get_all(Session())
    actions = [ac.to_dict() for ac in actions]
    return {'actions': actions}


async def get_actions(username):
    ses = Session()
    user = User.get_user_by(ses, username=username)
    actions = Action.get_by_user_id(user.id, ses)
    actions = [ac.to_dict() for ac in actions]
    return {'actions':actions}

