from flask import render_template,request,redirect,url_for,render_template_string,flash
from . import app

@app.route('/')
def base():
    return render_template('static_oldsite.html')
