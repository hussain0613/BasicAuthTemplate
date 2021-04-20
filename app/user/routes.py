from . import api_routes

## now from views
from . import user_rt
from .views import dashboard, login

from fastapi.responses import HTMLResponse

user_rt.get('/', response_class = HTMLResponse)(dashboard)
user_rt.get('/login', response_class = HTMLResponse)(login)
