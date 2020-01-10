from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired,Email, ValidationError, Length
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
import phonenumbers


class DevisForm(FlaskForm):
    nom = StringField('Nom de famille',validators=[DataRequired()],render_kw={"placeholder": "Nom de famille"})
    prenom = StringField('Prénom', validators=[DataRequired()],render_kw={"placeholder": "Prénom"})
    email = EmailField('Adresse mail',[validators.DataRequired(), validators.Email()],render_kw={"placeholder": "Email"})
    tel = StringField(render_kw={"placeholder": "Téléphone"})
    description = TextField('Parlez-nous de votre projet',widget=TextArea(),render_kw={"placeholder": "Parlez nous de votre projet"})
    file = FileField(render_kw={"placeholder": "Ajouter un fichier"},label="Ajouter")
    recaptcha = RecaptchaField()
    submit = SubmitField('Envoyer !',render_kw={"placeholder": "Envoyer !"})
#test en cours sans fichier validators=[FileRequired()]

class FormProcess(FlaskForm):
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
    submit      =   SubmitField('Envoyer !',
                                render_kw={"placeholder": "Envoyer !"})