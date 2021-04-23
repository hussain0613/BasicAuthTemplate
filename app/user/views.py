from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/user/templates")

async def dashboard(request:Request):
    resp = templates.TemplateResponse(name="index.html", context={'request': request})
    return resp.body.decode()


async def login(request:Request):
    resp = templates.TemplateResponse(name="login.html", context={'request': request})
    return resp.body.decode()

async def reset_password(request:Request, token:str):
    resp = templates.TemplateResponse(name="reset_password.html", context={'request': request})
    return resp.body.decode()


async def sign_up(request:Request, token:str):
    resp = templates.TemplateResponse(name="signup.html", context={'request': request})
    return resp.body.decode()