from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blueprints.customer_blueprint import CUSTOMER_BLUEPRINT
from blueprints.store_blueprint import STORE_BLUEPRINT
from blueprints.login_blueprint import LOGIN_BLUEPRINT

from models import db, dbBind

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/user.db'
app.config['SQLALCHEMY_BINDS'] = dbBind
db.init_app(app)

app.register_blueprint(CUSTOMER_BLUEPRINT, url_prefix='/customer')
app.register_blueprint(STORE_BLUEPRINT, url_prefix='/store')
app.register_blueprint(LOGIN_BLUEPRINT)

if __name__== "__main__":
    app.run(debug=True)