from wtforms.validators import DataRequired,Email
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from flask_login import UserMixin




class DevisForm(FlaskForm):
    nom = StringField('Nom de famille',validators=[DataRequired()],render_kw={"placeholder": "Nom de famille"})
    prenom = StringField('Prénom', validators=[DataRequired()],render_kw={"placeholder": "Prénom"})
    email = EmailField('Adresse mail',[validators.DataRequired(), validators.Email()],render_kw={"placeholder": "Email"})
    tel = StringField(render_kw={"placeholder": "Téléphone"})
    description = StringField('Parlez-nous de votre projet',widget=TextArea(),render_kw={"placeholder": "Parlez nous de votre projet"})
    file = FileField(render_kw={"placeholder": "Ajouter un fichier"},label="Ajouter")
    recaptcha = RecaptchaField()
    submit = SubmitField('Envoyer !',render_kw={"placeholder": "Envoyer !"})
#test en cours sans fichier validators=[FileRequired()]


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
