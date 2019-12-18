from flask import render_template,request,redirect,url_for,render_template_string,flash
from . import app
from .models import DevisForm

@app.route('/')
def base():
    form = DevisForm()
    return render_template('static_oldsite.html',form=form)
