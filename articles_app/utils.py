import secrets, os
from PIL import Image
from flask import current_app
from flask_login import current_user


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

