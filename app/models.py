from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextField
from wtforms.validators import DataRequired,Email
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea



class DevisForm(FlaskForm):
    nom = StringField('Nom de famille',validators=[DataRequired()],render_kw={"placeholder": "Nom de famille"})
    prenom = StringField('Prénom', validators=[DataRequired()],render_kw={"placeholder": "Prénom"})
    email = EmailField('Adresse mail',[validators.DataRequired(), validators.Email()],render_kw={"placeholder": "Email"})
    tel = StringField(render_kw={"placeholder": "Téléphone"})
    description = StringField('Parlez nous de votre projet',widget=TextArea(),render_kw={"placeholder": "Parlez nous de votre projet"})
    file = SubmitField('Ajouter un fichier',render_kw={"placeholder": "Email"})
    submit = SubmitField('Envoyer !',render_kw={"placeholder": "Email"})
