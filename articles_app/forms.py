from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Email
from flask_ckeditor import CKEditorField


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
    pass