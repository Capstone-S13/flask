from flask import Blueprint

RMF_BLUEPRINT = Blueprint('rmf', __name__)

from . import views