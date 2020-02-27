from flask import Flask
from flask_bootstrap import Bootstrap
import os
from config import Config
from flask_admin import Admin

app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)

app.config.from_object(Config)
app.config.from_pyfile('config.py')

admin = Admin(app)

from . import views
