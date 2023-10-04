import os
from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_msearch import Search


app = Flask(__name__, static_folder="static")
app.config.from_object(Config)
# app.secret_key = os.urandom(36)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
mail = Mail()
search = Search()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

mail.init_app(app)
search.init_app(app)



from . import views, error_handlers
from .user.auth import auth

app.register_blueprint(auth)
