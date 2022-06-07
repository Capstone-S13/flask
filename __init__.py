from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from blueprints.login_blueprint import LOGIN_BLUEPRINT
from blueprints.customer_blueprint import CUSTOMER_BLUEPRINT
from blueprints.store_blueprint import STORE_BLUEPRINT

from models import db, dbBind
import system

app = Flask(__name__)

app.config['SECRET_KEY'] = '8fUqFEeM9WWUnLtBS5BqLhboibcXCVJq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/user.db'
app.config['SQLALCHEMY_BINDS'] = dbBind
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "/"
login_manager.init_app(app)

from models import UserDb

@login_manager.user_loader
def load_user(userId):
    return system.get_user(userId)

app.register_blueprint(LOGIN_BLUEPRINT)
app.register_blueprint(CUSTOMER_BLUEPRINT, url_prefix='/customer')
app.register_blueprint(STORE_BLUEPRINT, url_prefix='/store')

if __name__== "__main__":
    app.run(debug=True)