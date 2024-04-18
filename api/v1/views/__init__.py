from flask import Blueprint

# Initialize Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import the views after initializing Blueprint to avoid circular imports
from api.v1.views.index import *
