from flask import Blueprint

CUSTOMER_BLUEPRINT = Blueprint('customer', __name__, template_folder='templates')

from . import views