from flask import render_template,request,redirect,url_for,render_template_string,flash
from . import app
from .models import DevisForm
from werkzeug import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods = ['GET', 'POST'])
def base():
    form = DevisForm()
    if request.method == 'POST':


            if form.file.data:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('file uploaded successfully')
                    return redirect(url_for('test'))

                else:
                    if file and not allowed_file(file.filename):
                        flash("Un fichier de type autorisé svp")

    return render_template('static_oldsite.html',form=form, allowed=app.config['ALLOWED_EXTENSIONS'])

@app.route('/test')
def test():
    return render_template('index.html')

@app.route('/process')
def process():
    return render_template('static_oldsite_process.html')
