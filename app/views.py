from flask import render_template,request,redirect,url_for,render_template_string, session, flash,make_response
from . import app,login_manager,verifier
from .models import FormProcess,User,LoginForm,SignupForm
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
import phonenumbers
import os
from flask_mail import Message
from app import mail
from flask_login import logout_user, login_required,login_user, current_user
from ldap3 import Connection, ALL, Server
from json import dumps, loads




def connect(accountName,password):
    server = Server('dc1.lan.esiee.fr', use_ssl=True, get_info=ALL)
    conn = Connection(server, user="cn=LDAP,ou=comptes_services,ou=utilisateurs,DC=lan,DC=esiee,DC=fr",password="UE=cv,VR1^%Mbj43")
    conn.bind()
    conn.search('DC=lan, DC=esiee, DC=fr', "(&(objectclass=person)(sAMAccountName="+accountName+"))",attributes=['distinguishedName', 'sn', 'telephoneNumber', 'displayName', 'roomNumber', 'givenName','Name'])
    if len(conn.entries)>0:
        DN = conn.entries[0].distinguishedName.value
        conn = Connection(server, user=DN, password=password)
        if(conn.bind()) :
            return True
    return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validation_formulaire(form,lien):

    resultat = request.form

    Fprenom      =  resultat.get("prenom")
    Fnom         =  resultat.get("nom")
    Femail       =  resultat.get("email")
    Fdescription =  resultat.get("description")
    Fphone       =  resultat.get("phone")
    file         =  request.files["file"]
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

    #vérification du fichier s'il y en a un        
    if file and allowed_file(file.filename)==False:
            flash("Le type de votre fichier n'est pas supporté.","fileerror")
            valide = False

    #Si le formulaire est validé et il n'y a pas d'erreur
    if form.validate_on_submit() and valide == True:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("Merci d'avoir rempli ce formulaire, nous vous répondrons rapidement.","validation")
        msg = Message(Fprenom + ' ' + Fnom + ' a contacté Junior ESIEE', sender=app.config.get("MAIL_USERNAME"),recipients=['remi.boidet@junioresiee.com'])
        msg.body = Fprenom + '' + Fnom + ' a contacté Junior ESIEE pour ' + Fdescription + '\n peut être recontacté au ' + Fphone + Femail
        msg.html = render_template('templatemail.html',
                                    Prenom          =   Fprenom,
                                    Nom             =   Fnom,
                                    Description     =   Fdescription,
                                    Phone           =   Fphone,
                                    Email           =   Femail,
                                    )
        mail.send(msg)
    else:
        session['formdata'] = request.form
        lien = lien + '#contact'
    return(lien)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/', methods = ['GET', 'POST'])
def base():
    form = FormProcess(request.form)

    if request.method == 'POST':
        lien = validation_formulaire(form,'/')
        return redirect(lien)

    elif request.method == 'GET':
        formdata = session.get('formdata', None)
        if formdata:
            form = FormProcess(MultiDict(formdata))
            form.validate()
            session.pop('formdata')
        return render_template('static_oldsite.html',form=form)

@app.route('/process', methods = ['GET', 'POST'])
def formprocess():
    form = FormProcess(request.form)

    if request.method == 'POST':
        lien = validation_formulaire(form,'/process')
        return redirect(lien)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route('/sign_up', methods=('GET', 'POST'))
def sign_up():

    form = SignupForm()

    if form.validate_on_submit():


        email_address_info = verifier.verify(form.email.data)
        if email_address_info is not None:#tout se passe bien avec l'adresse mail
            flash("email vérifié")
        else:
            resp = make_response('None', 404)
    return render_template('sign_up.html', form=form)



'''
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if connect(form.login.data, form.password.data):
            u = User(42, form.login.data)
            login_user(u, remember=form.remember_me.data)
            flash("Connection réussie")
            return redirect('/success/'+form.login.data)
    flash("Echec de la Connection")
    return render_template('login.html', form=form)
'''


@app.route('/success/<username>')
@login_required

def sucess(username):
    return "Salut " + username + ".\nTu es arrivé jusque là. "


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "you are logged out"
