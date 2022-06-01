from flask import Flask
# from flask_login import LoginManager

app = Flask(__name__)

# login_manager = LoginManager()
# login_manager.init_app(app)

# app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
