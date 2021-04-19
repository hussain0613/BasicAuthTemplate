from . import Session, user_api_bp, env
from .models import User
from flask import request, Response
import json

@user_api_bp.route("/")
def dahsboard():
    #token = request.args.get('login_token')
    token = request.headers.get_all("Authorization")
    #print(token)
    if(token):
        resp = User.verify_login_token(token[0].split()[1], Session(), env['SECRET_KEY'])
        resp['user'] = resp['user'].to_dict()
        resp['user'].pop("password")
        resp['message'] = f"Hello! you are logged in as {resp['user']['username']}"
        return resp
    
    return {"Message": "Hello. You are in not logged in dashboard now"}

@user_api_bp.route("/signup/", methods=["POST"])
def sign_up():
    data = json.loads(request.data)
    user = User.create_user(Session(), **data)
    resp = {}
    if(user.get('password')): 
        user.pop('password')
        resp = {"message": "user created succesfully", "user": user}
    else:
        resp = {"message": "user not created", "user": user}
    
    return resp

@user_api_bp.route("/token/", methods=["POST"])
def login():
    data = json.loads(request.data)
    resp = {}
    if(data.get("password")):
        password = data.pop("password")
        res = User.get_login_token(Session(), env["SECRET_KEY"], password, **data)
        resp = Response()
        resp.headers["Authorization"] = f"Bearer {res['token']}"
        resp.headers["Content-Type"] = "application/json"
        resp.set_data(json.dumps(res))
    else:
        resp["message"] = "No passowrd provided"
    return resp

@user_api_bp.route("/reset_password/")
def request_reset_password():
    data = json.loads(request.data)
    resp = User.get_reset_password_token(data.get('email'), env['SECRET_KEY'], Session())
    return resp

@user_api_bp.route("/reset_password/", methods= ["POST"])
def reset_passowrd():
    token = request.args.get('token')
    data = json.loads(request.data)
    pw = data.get('password')
    if(not token or not pw): return {"Message": "missing token/new password"}
    resp = User.reset_password(pw, token, env['SECRET_KEY'], Session())
    print(f"[******************] {type(resp)}")
    return resp


@user_api_bp.route("/get_all_users/")
def all_users():
    users = User.get_all(Session())
    resp = []
    for user in users:
        d = user.to_dict()
        d.pop("password")
        resp.append(d)
    return {'users': resp}


