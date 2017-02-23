import os
from flask import render_template, current_app as app

from ..forms.image_form import ImageUploadForm
from .. import main

from flask_login import login_required


@main.route('/image', methods=['GET', 'POST'])
@login_required
def image():
    image = None
    form = ImageUploadForm()
    images_path = os.path.join(app.static_folder, app.config.get('IMAGES_PATH'))
    if form.validate_on_submit():
        image = form.image_file.data.filename
        if not os.path.exists(images_path):
            os.makedirs(images_path)
        form.image_file.data.save(os.path.join(images_path, image))
    return render_template(
        'main/image.html',
        form=form,
        image='uploads/' + image if image else None
        )