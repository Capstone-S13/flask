from flask import Blueprint

STORE_BLUEPRINT = Blueprint('store', __name__, template_folder='templates')

from . import views