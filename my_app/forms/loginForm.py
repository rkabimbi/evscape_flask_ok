from my_app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms   import StringField, SubmitField #classe utilisée pour construire les champs des formulaires
from wtforms.validators import InputRequired, Length, ValidationError,NumberRange #validateur d'input
from wtforms   import PasswordField, BooleanField, FileField, IntegerField
from wtforms.validators import  EqualTo
from wtforms   import PasswordField



#formulaire login
class FormLogin( FlaskForm ):
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password:', validators=[Length(min=3, max=16)])
    submit   = SubmitField('Soumettre')


