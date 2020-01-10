from flask import Flask
from flask_bootstrap import Bootstrap
import os
from config import Config
from flask_admin import Admin
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=True)
boot = Bootstrap(app)

#Pour l'envoi de mail
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

app.config.from_object(Config)
app.config.from_pyfile('config.py')

admin = Admin(app)

from . import views

