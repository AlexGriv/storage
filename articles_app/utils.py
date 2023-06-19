import secrets, os
from PIL import Image
from flask import current_app, url_for
from flask_login import current_user
from flask_mail import Message
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

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password change request', sender='noreply@demo.com', recipients=[user.email])
    message.body = f"""
    To reset your password, follow this link:
    {url_for('user.reset_token', token=token, _external=True)}

    If you didn't make this request just ignore this request, no changes will be made.
    You do not need to reply to the email, it is generated automatically.
    """
    mail.send(message)
