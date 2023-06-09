import datetime, os
from flask import abort, flash, redirect, request, render_template, url_for, session
from flask_login import login_required, current_user, login_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import app, db
from .forms import ArticleForm, ArticleFormUpdate, LoginForm
from .models import Article, User



@app.route('/', methods=['GET', 'POST'])
def index_view():
    page = request.args.get('page', 1, type=int)
    article = Article.query.order_by(Article.timestamp.desc()).paginate(page=page, per_page=5)
    # article = Article.query.order_by(Article.timestamp.desc()).all()
    # return render_template('articles.html', article=article, user=user, form=form)
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
    if current_user.is_authenticated:
        user_id = str(current_user.id)
        return render_template('articles.html', user_id=user_id, article=article, user=current_user, form=form)
    return render_template('articles.html', article=article, user=current_user, form=form)



@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_article_view():
    form = ArticleForm()
    if form.validate_on_submit():
        text = form.text.data
        if Article.query.filter_by(text=text).first():
            flash('Такая статья уже была оставлена ранее!')
            return render_template('add_article.html', form=form)
        article = Article(
            title=form.title.data,
            intro=form.intro.data,
            text=form.text.data,
            prog_lang=form.prog_lang.data,
            author=current_user
        )
        db.session.add(article)
        db.session.commit()
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index_view'))
    user_id = str(current_user.id)
    return render_template('add_article.html', user_id=user_id, form=form, user=current_user)


@app.route('/articles/<int:id>/update', methods=['GET', 'POST'])
@login_required
def article_update(id, user=current_user):
    article = Article.query.get_or_404(id)
    user_id = str(current_user.id)
    if article.author != current_user:
        return redirect(url_for('article_view', id=id))
    form = ArticleFormUpdate()
    if request.method == 'GET':
        form.title.data = article.title
        form.intro.data = article.intro
        form.prog_lang.data = article.prog_lang
        form.text.data = article.text
    if form.validate_on_submit():
        article.title=form.title.data
        article.intro=form.intro.data
        article.prog_lang=form.prog_lang.data
        article.text=form.text.data
        try:
            db.session.commit()
            return redirect(url_for('article_view', id=id))
        except:
            return "При редактировании произошла ошибка"

    else:
        return render_template('article_update.html', user_id=user_id, user=current_user, article=article, form=form)


@app.route('/articles/<int:id>')
def article_view(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', user=current_user, article=article)


@app.route('/articles/<int:id>/delete')
@login_required
def article_delete(id):
    article = Article.query.get_or_404(id)
    if article.author != current_user:
        flash('Нельзя удалять чужие статьи', 'danger')
        return render_template('article.html', article=article)
    else:
        try:
            db.session.delete(article)
            db.session.commit()
            return redirect('/')
        except:
            return "При удалении произошла ошибка"
