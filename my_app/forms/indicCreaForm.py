from my_app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms   import StringField, SubmitField #classe utilisée pour construire les champs des formulaires
from wtforms.validators import InputRequired, Length, ValidationError,NumberRange #validateur d'input
from wtforms   import PasswordField, BooleanField, FileField, IntegerField,RadioField
from wtforms.validators import  EqualTo

from wtforms   import PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.fields import DateField, EmailField, TelField
from datetime import date


#formulaire de creation indices
class FormCreaInd( FlaskForm ):
    indice = StringField('Indice:', validators=[InputRequired(), Length(min=5, max=50, message='indice doit avoir une longeur entre %(min)d et %(max)d caracteres')])
    submit   = SubmitField('Enregistrer')


