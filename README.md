# storage
Мини-проект склад решений:
* Создание, редактирование постов/статей, комментирование статей/постов.

## Технологии
* Python 3.11
* Flask==2.2.3
* Flask-Admin==1.6.1
* Flask-CKEditor==0.4.6
* Flask-SQLAlchemy==3.0.3
* PyJWT==2.8.0
* Flask-msearch==0.2.9.2
* Flask-Login==0.6.2

## Как запустить проект локально
Клонировать репозиторий:
```
https://github.com/AlexGriv/storage.git
```

Выполните по очереди команды:
```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

Создайте суперпользователя через DBeaver или аналог, роль admin


### Пример
```
![Иллюстрация к проекту](https://github.com/AlexGriv/storage/raw/master/demo.png)

## Автор
AlexGriv https://github.com/AlexGriv