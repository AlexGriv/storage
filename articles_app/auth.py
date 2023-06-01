from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from .models import Article, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db
from .forms import LoginForm


auth = Blueprint('auth', __name__)


@auth.route('/user/<username>', methods=['GET', 'POST'])
def profile(username, page=1):

    user = User.query.filter_by(username=username).first_or_404()
    if user == None:
        flash('Пользователь ' + user.username + ' не найден.')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)

    article = user.article.order_by(Article.timestamp.desc()).paginate(page=page, per_page=5)
    count = article.total
    return render_template('profile.html', user=user, article=article, count=count, page=page)



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
            flash('Не удалось войти, проверьте почту или пароль', 'danger')

    return render_template('login.html', form=form)


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_view'))
