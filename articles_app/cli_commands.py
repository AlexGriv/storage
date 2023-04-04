import csv

import click

from . import app, db
from .models import Article


@app.cli.command('load_articles')
def load_articles_command():
    """Функция загрузки мнений в базу данных."""
    with open('articles.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            article = Article(**row)
            db.session.add(article)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений: {counter}')
