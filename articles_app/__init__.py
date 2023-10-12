import os
from flask import Flask, redirect, url_for
from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail
from flask_msearch import Search


app = Flask(__name__, static_folder="static")
app.config.from_object(Config)
# app.secret_key = os.urandom(36)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
mail = Mail(app)
search = Search()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


class DashBoardView(AdminIndexView):
    @login_required
    @expose('/')
    def admin_panel(self):
        from .models import User
        if current_user.is_admin:
            users = User.query.all()
            return self.render('admin/admin.html', users=users)
        else:
            return redirect(url_for('index_view'))

class BackView(BaseView):
    @expose('/')
    def any_page(self):
        return redirect(url_for('index_view'))


admin = Admin(name='Admin panel', template_mode='bootstrap4', index_view=DashBoardView(), endpoint='admin')

admin.init_app(app)
mail.init_app(app)
search.init_app(app)


from .models import User, Article, Comment
admin.add_view(BackView(name='На главную'))
admin.add_view(ModelView(User, db.session, name='Users'))
admin.add_view(ModelView(Article, db.session, name='Articles'))
admin.add_view(ModelView(Comment, db.session, name='Comments'))
from . import views, error_handlers
from .user.auth import auth

app.register_blueprint(auth)
