from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(128))
    article = db.relationship('Article', backref='author', lazy='dynamic')
    comment = db.relationship('Comment', backref='comment_author', lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'


class Article(db.Model):
    __searchable__ = ['title', 'text']
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='comment_post', lazy='dynamic', cascade="all, delete-orphan")
    prog_lang = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'User({self.article})'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(64), index=True)
    body = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'Comment({self.body}, {self.timestamp.strftime("%d.%m.%Y-%H:%M")}, {self.article_id})'
