from flask import Flask
from flask_bootstrap import Bootstrap
import os
from config import Config
from flask_admin import Admin
from flask_mail import Mail
from flask_login import LoginManager
from flask_email_verifier import EmailVerifier



app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)


#Pour l'envoi de mail

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER'),
    "MAIL_PASSWORD": os.environ.get('EMAIL_PASSWORD')
}

app.config.update(mail_settings)

mail = Mail(app)

app.config.from_object(Config)
app.config.from_pyfile('config.py')

admin = Admin(app)
verifier = EmailVerifier(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'



from . import views
