from flask_wtf import FlaskForm, RecaptchaField, Form
from wtforms import StringField, SubmitField,TextField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired,Email, ValidationError, Length
from wtforms import validators
from wtforms.widgets import TextArea
import phonenumbers

class FormProcess(Form):
    mini = 2
    maxi = 32
    nom         =   StringField("Nom de famille", 
                                validators=[DataRequired(message="Votre nom est obligatoire."),
                                            Length(min=mini, message="Votre nom est trop court."),
                                            Length(max=maxi,message="Votre nom est trop long.")],
                                render_kw={"placeholder": "Nom de famille"})
    prenom      =   StringField("Prénom",
                                validators=[DataRequired(message="Votre prénom est obligatoire."),
                                            Length(min=mini, message="Votre prénom est trop court."),
                                            Length(max=maxi,message="Votre prénom est trop long.")],
                                render_kw={"placeholder": "Prénom"})
    description =   TextField(  "Parlez-nous de votre projet.",
                                validators=[DataRequired(message="Une description de votre projet est obligatoire."),
                                            Length(min=mini, message="Votre description est trop courte.")],
                                widget=TextArea(),
                                render_kw={"placeholder": "Parlez nous de votre projet."})
    phone       =   StringField('Phone')
    email       =   StringField('Email', 
                                [Email(message="Ce n'est pas une adresse mail valide."),
                                DataRequired(message="Votre adresse email est obligatoire.")],
                                render_kw={"placeholder": "Email"})
    recaptchafield = RecaptchaField()
    file        =   FileField(render_kw={"placeholder": "Ajouter un fichier"},label="Ajouter un fichier")
    submit      =   SubmitField('Envoyer !',
                                render_kw={"placeholder": "Envoyer !"})