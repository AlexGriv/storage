from random import randrange
from flask import abort, flash, redirect, request, render_template, url_for
from flask_login import login_required, current_user, login_user

from . import app, db
from .forms import ArticleForm, ArticleFormUpdate
from .models import Article, User


@app.route('/', methods=['GET', 'POST'])
def index_view():
    #if current_user.name != None:
    #    article = Article.query.order_by(Article.timestamp.desc()).all()
    #    return render_template('articles.html', article=article, name=current_user.name)
    #else:
    #    article = Article.query.order_by(Article.timestamp.desc()).all()
    #    return render_template('articles.html', article=article)
    article = Article.query.order_by(Article.timestamp.desc()).all()
    return render_template('articles.html', article=article)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/random')
def random():
    quantity = Article.query.count()
    if not quantity:
        abort(404)
    offset_value = randrange(quantity)
    article = Article.query.offset(offset_value).first()
    if not article:
        abort(404)
    return render_template('article.html', article=article, name=current_user.name)


@app.route('/add', methods=['GET', 'POST'])
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
            prog_lang=form.prog_lang.data
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article_view', id=article.id))
    return render_template('add_article.html', form=form)


@app.route('/articles/<int:id>')
def article_view(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article, name=current_user.name)


@app.route('/articles/<int:id>/delete')
def article_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении произошла ошибка"


@app.route('/articles/<int:id>/update', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    form = ArticleFormUpdate()
    if form.validate_on_submit():
        article.title = form.title.data
        article.intro =form.intro.data
        article.text = form.text.data
        article.prog_lang =form.prog_lang.data
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "При редактировании произошла ошибка"

    else:
        return render_template('article_update.html', article=article, form=form)
