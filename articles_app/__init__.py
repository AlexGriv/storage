import os
from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config
from flask_ckeditor import CKEditor


app = Flask(__name__, static_folder="static")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)


from . import cli_commands, error_handlers, views
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))