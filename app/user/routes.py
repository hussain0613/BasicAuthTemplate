from . import api_routes
## now from views
from . import user_rt
from .views import dashboard

user_rt.get('/')(dashboard)
