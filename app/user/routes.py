from . import api_routes

## now from views
from . import user_rt
from .views import dashboard, login, reset_password, sign_up

from fastapi.responses import HTMLResponse

user_rt.get('/', response_class = HTMLResponse)(dashboard)
user_rt.get('/login', response_class = HTMLResponse)(login)
user_rt.get('/reset_password/', response_class = HTMLResponse, name="reset_password_veiw")(reset_password)
user_rt.get('/signup/', response_class = HTMLResponse, name="signup_view")(sign_up)
