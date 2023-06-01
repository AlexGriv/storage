# from random import randrange
from flask import abort, flash, redirect, request, render_template, url_for, session
from flask_login import login_required, current_user, login_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import app, db
from .forms import ArticleForm, ArticleFormUpdate, LoginForm
from .models import Article, User


@app.route('/', methods=['GET', 'POST'])
def index_view():
    # form = LoginForm()
    user = current_user
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
            flash('Не удалось войти, проверьте почту или пароль', 'danger')

    return render_template('articles.html', article=article, user=user, form=form)


@app.route('/add', methods=['GET', 'POST'])
def add_article_view():
    user = current_user
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
    return render_template('add_article.html', form=form, user=user)


@app.route('/articles/<int:id>/update', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get_or_404(id)
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
        return render_template('article_update.html', article=article, form=form)


@app.route('/articles/<int:id>')
def article_view(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article)


@app.route('/articles/<int:id>/delete')
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


# @app.route('/random')
#def random():
#    quantity = Article.query.count()
#    if not quantity:
#        abort(404)
#    offset_value = randrange(quantity)
#    article = Article.query.offset(offset_value).first()
#    if not article:
#        abort(404)
#    return render_template('article.html', article=article)