from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


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
    text = TextAreaField(
        'Напишите подробно',
        validators=[DataRequired(message='Обязательное поле')]
    )
    prog_lang = StringField(
        'Добавьте язык програмирования',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 64)]
    )
    submit = SubmitField('Добавить')


class ArticleFormUpdate(ArticleForm):
    submit = SubmitField('Редактировать')
