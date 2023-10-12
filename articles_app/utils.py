import secrets, os
from PIL import Image
from flask import current_app, render_template, url_for
from flask_login import current_user
from flask_mail import Message
from .forms import ResetForm, ResetPasswordForm
from articles_app import mail
from .models import User




def picture_path(picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(picture.filename)
    picture_filename = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', 'profile_pics', str(current_user.id))
    if not full_path:
        os.mkdir(full_path)
    picture_pa = os.path.join(full_path, picture_filename)
    size = (200, 200)
    dir = full_path
    for file in os.scandir(dir):
        if file != picture_filename:
            os.remove(file.path)
    i = Image.open(picture)
    i.thumbnail(size)
    i.save(picture_pa)
    return picture_filename


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_reset_email(user):
    form = ResetForm()
    token = user.get_reset_token()
    send_email('Password change request',
               sender='noreply@demo.com',
               recipients=[user.email],
               text_body=render_template('reset_password.txt',
                                         user=current_user, token=token, form=form),
               html_body=render_template('reset_password.html',
                                         user=current_user, token=token, form=form))

