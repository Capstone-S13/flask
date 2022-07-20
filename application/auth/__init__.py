from flask import Blueprint

AUTH_BLUEPRINT = Blueprint('auth', __name__, template_folder='templates')

from . import views