from flask import Flask,render_template,request,redirect,url_for,render_template_string,flash, session
from . import app
from .models import DevisForm, FormProcess, PhoneForm
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

@app.route('/process', methods = ['GET', 'POST'])
def formprocess():
    form = FormProcess()
    if form.validate_on_submit():
        session['phone']=form.phone.data
        #flash('le nom{}, le prénom {}, le text{}'.format(form.nom.data, form.prenom.data,form.description.data))
        return redirect('/test')
        
    return render_template('static_oldsite_process.html',title='test',form=form)

#@app.route('/test')
#def test():
    #return render_template('index.html')



@app.route('/test', methods=['GET', 'POST'])
def index():
    form = PhoneForm()
    if form.validate_on_submit():
        session['phone'] = form.phone.data
        return redirect(url_for('show_phone'))
    return render_template('index.html', form=form)


@app.route('/showphone')
def show_phone():
    return render_template('show_phone.html', phone=session['phone'])
