from flask import Flask,render_template,request,redirect,url_for,flash, session
from . import app
from .models import DevisForm, FormProcess
from werkzeug import secure_filename, MultiDict
import phonenumbers
import os
from flask_mail import Message
from app import mail


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

    if request.method == 'POST':
        resultat = request.form

        Fprenom      =  resultat.get("prenom")
        Fnom         =  resultat.get("nom")
        Femail       =  resultat.get("email")
        Fdescription =  resultat.get("description")
        Fphone       =  resultat.get("phone")
        valide       =  True

        #Validation numéro de téléphone
        if len(Fphone) == 0:
            flash("Votre numéro de téléphone est obligatoire.","errorphone")
            valide = False
        else:
            try:
                p = phonenumbers.parse(Fphone)
                if not phonenumbers.is_valid_number(p):
                    raise ValueError()
            except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                flash("Votre numéro de téléphone n'est pas valide.", "errorphone")
                valide = False
        #Si le formulaire est validé et il n'y a pas d'erreur
        if form.validate_on_submit() and valide == True:
            flash("Merci d'avoir rempli ce formulaire, nous vous répondrons rapidement.","validation")
            msg = Message(Fprenom + ' ' + Fnom + ' a contacté Junior ESIEE', recipients=['bureau@junioresiee.com'])
            msg.body = Fprenom + '' + Fnom + ' a contacté Junior ESIEE pour ' + Fdescription + '\n peut être recontacté au ' + Fphone + Femail
            msg.html = render_template('templatemail.html',
                                        Prenom          =   Fprenom,
                                        Nom             =   Fnom,
                                        Description     =   Fdescription,
                                        Phone           =   Fphone,
                                        Email           =   Femail,
            )
            mail.send(msg)
            return redirect('/process')
        else:
            session['formdata'] = request.form
            return redirect('/process#contact')

    elif request.method == 'GET':
        formdata = session.get('formdata', None)
        if formdata:
            form = FormProcess(MultiDict(formdata))
            form.validate()
            session.pop('formdata')
        return render_template('static_oldsite_process.html',form=form)


@app.route('/test')
def test():
    return render_template('index.html')