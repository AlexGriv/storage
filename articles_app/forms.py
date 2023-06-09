from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from .models import User



class ArticleForm(FlaskForm):
    title = StringField(
        'Введите название',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    intro = StringField(
        'Краткое описание',
        validators=[Length(1, 300), Optional()]
    )
    text = CKEditorField('Напишите подробно', validators=[DataRequired(message='Обязательное поле')])
    #text = TextAreaField('Напишите подробно',validators=[DataRequired(message='Обязательное поле')])
    prog_lang = StringField(
        'Добавьте язык програмирования',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 64)]
    )
    submit = SubmitField('Добавить')


class ArticleFormUpdate(ArticleForm):
    submit = SubmitField('Редактировать')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('This username is already taken, please use another one.', 'danger')
            raise ValidationError('This username is already taken, please use another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('This email is already taken, please use another one.', 'danger')
            raise ValidationError('This email is already taken, please use another one.')


class AccountUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = FileField(validators=[FileAllowed(['png', 'pdf', 'jpg'], "wrong format!")])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash('This username is already taken, please use another one.', 'danger')
                raise ValidationError('This username is already taken, please use another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                flash('This email is already taken, please use another one.', 'danger')
                raise ValidationError('This email is already taken, please use another one.')
