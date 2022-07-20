from flask import Flask
from flask_login import LoginManager

from application.models import db, dbBind

login_manager = LoginManager()
login_manager.login_view = "/"

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    
    db.init_app(app)
    login_manager.init_app(app)

    from application.models import UserDb
    import application.system as system

    @login_manager.user_loader
    def load_user(userId):
        return system.get_user(userId)

    from application.auth import AUTH_BLUEPRINT
    from application.customer import CUSTOMER_BLUEPRINT
    from application.store import STORE_BLUEPRINT

    app.register_blueprint(AUTH_BLUEPRINT)
    app.register_blueprint(CUSTOMER_BLUEPRINT, url_prefix='/customer')
    app.register_blueprint(STORE_BLUEPRINT, url_prefix='/store')
    
    return app
<<<<<<< HEAD

# if __name__== "__main__":
#     app = create_app('flask.cfg')
#     app.run(debug=True)
=======
>>>>>>> ea89de58c2b2c68d3c0a3a91a2583620af041966
