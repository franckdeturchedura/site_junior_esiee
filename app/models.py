from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired,Email, ValidationError
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
    nom = StringField("Nom de famille", validators=[DataRequired()],render_kw={"placeholder": "Nom de famille"})
    prenom = StringField("Prénom", validators=[DataRequired()],render_kw={"placeholder": "Prénom"})
    description= TextField("Parlez-nous de votre projet", validators=[DataRequired()],widget=TextArea(),render_kw={"placeholder": "Parlez nous de votre projet"})
    phone = StringField('Phone')
    submit = SubmitField('Envoyer')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class PhoneForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')