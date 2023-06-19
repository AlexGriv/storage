import os

from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from ..models import Article, User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager
from ..forms import LoginForm, SignupForm, AccountUpdateForm, ResetForm, ResetPasswordForm
from ..utils import picture_path, send_reset_email
from ..models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


auth = Blueprint('auth', __name__)



@auth.route('/user/<username>', methods=['GET', 'POST'])
def profile(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    article = user.article.order_by(Article.timestamp.desc()).paginate(page=page, per_page=5)
    count = article.total
    form = AccountUpdateForm()
    if not current_user.is_anonymous:
        if request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.image_file.data = current_user.image_file


        elif form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            if form.image_file.data == None:
                form.image_file = current_user.image_file
            else:
                username = form.username.data
                current_user.image_file = picture_path(form.image_file.data)


            db.session.commit()
            flash('Your account has been updated', 'Success')


            return redirect(url_for('auth.profile', username=current_user.username))

    user_id = str(user.id)

    return render_template('profile.html', form=form, user_id=user_id, user=user, article=article, count=count, page=page)


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect (url_for('index_view'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        full_path = os.path.join(os.getcwd(), 'articles_app/static', 'profile_pics', user.username)
        if not os.path.exists(full_path):
            os.mkdir(full_path)

        #shutil.copy(f'{os.getcwd()}/articles_app/static/profile_pics/default.jpg', full_path)
        flash('Your account has been created', 'success')
        return redirect(url_for('index_view'))

    return render_template('signup.html', form=form)


@auth.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('index_view'))
        else:
            if not user:
                flash('Login failed, please check your email address ', 'danger')
            else:
                flash('Login failed, please check your password', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_view'))


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect (url_for('index_view'))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        send_reset_email(user)
        flash('Password recovery instructions have been sent to the email address provided.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)



@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect (url_for('index_view'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid and expired token', 'warning')
        return redirect(url_for('auth.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been updated', 'Success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', form=form)
