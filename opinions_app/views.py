from random import randrange
from flask import abort, flash, redirect, request, render_template, url_for
from flask_login import login_required, current_user, login_user

from . import app, db
from .forms import OpinionForm, OpinionFormUpdate
from .models import Opinion, User


@app.route('/', methods=['GET', 'POST'])
def index_view():
    opinion = Opinion.query.order_by(Opinion.timestamp.desc()).all()
    if not opinion:
        abort(404)
    return render_template('opinions.html', opinion=opinion)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/random')
def random():
    quantity = Opinion.query.count()
    if not quantity:
        abort(404)
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first():
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)


@app.route('/opinions/<int:id>/delete')
def opinion_delete(id):
    opinion = Opinion.query.get_or_404(id)
    try:
        db.session.delete(opinion)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении произошла ошибка"


@app.route('/opinions/<int:id>/update', methods=['GET', 'POST'])
def opinion_update(id):
    opinion = Opinion.query.get(id)
    form = OpinionFormUpdate()
    if form.validate_on_submit():
        opinion.title = form.title.data
        opinion.text = form.text.data
        opinion.source =form.source.data
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "При редактировании произошла ошибка"

    else:
        return render_template('opinion_update.html', opinion=opinion, form=form)
