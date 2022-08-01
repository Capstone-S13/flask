from flask import Blueprint

ORDER_BLUEPRINT = Blueprint('order', __name__, template_folder='templates')

from . import views