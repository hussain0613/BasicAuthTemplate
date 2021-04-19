from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi import Request

async def dashboard():
    resp = FileResponse(path = "app/user/statics/index.html")
    return resp


async def login():
    resp = FileResponse(path = "app/user/statics/index.html")
    return resp