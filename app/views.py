from flask import render_template,request,redirect,url_for,render_template_string,flash,make_response
from . import app,login_manager,verifier
from .models import DevisForm,User,LoginForm,SignupForm
from werkzeug import secure_filename
import os
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


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

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
def process():
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

    return render_template('static_oldsite_process.html',form=form, allowed=app.config['ALLOWED_EXTENSIONS'])

@app.route('/test')
def test():
    return render_template('index.html')



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
