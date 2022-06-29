import os
from flask import Flask
from flask_login import LoginManager

from application.models import db, dbBind
from application.config import config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")
    
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_object(config[config_name])
    
    initialise_extensions(app)
    register_blueprints(app)
    return app

##########################
#### Helper Functions ####
##########################

def initialise_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    
    import application.system as system

    @login_manager.user_loader
    def load_user(userId):
        return system.get_user(userId)

def register_blueprints(app):
    from application.auth import AUTH_BLUEPRINT
    from application.customer import CUSTOMER_BLUEPRINT
    from application.store import STORE_BLUEPRINT
    
    app.register_blueprint(AUTH_BLUEPRINT)
    app.register_blueprint(CUSTOMER_BLUEPRINT, url_prefix='/customer')
    app.register_blueprint(STORE_BLUEPRINT, url_prefix='/store')