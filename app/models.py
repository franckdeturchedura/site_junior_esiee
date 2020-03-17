from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField,TextField, PasswordField, BooleanField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired,Email, ValidationError, Length
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from flask_login import UserMixin




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
    file        =   FileField(render_kw={"placeholder": "Ajouter un fichier"},label="Ajouter un fichier")
    submit      =   SubmitField('Envoyer !',
                                render_kw={"placeholder": "Envoyer !"})


class User(UserMixin):
    def __init__(self, id, username=''):
        self.username = username
        self.id = id

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Go')

class SignupForm(FlaskForm):
    email = EmailField('Adresse mail',[validators.DataRequired(), validators.Email()],render_kw={"placeholder": "Email"})
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Go')
