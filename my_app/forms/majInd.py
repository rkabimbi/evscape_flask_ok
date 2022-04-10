from my_app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms   import StringField, SubmitField #classe utilisée pour construire les champs des formulaires
from wtforms.validators import InputRequired, Length, ValidationError,NumberRange #validateur d'input
from wtforms   import PasswordField, BooleanField, FileField, IntegerField
from wtforms.validators import  EqualTo
from wtforms   import PasswordField



#formulaire de mise à jour indice
class MajInd( FlaskForm ):
    indice   = StringField('Indice:', validators=[InputRequired(), Length(min=5, max=50, message='Indice doit avoir une taille entre %(min)d et  %(max)d ')]) 
    submit  = SubmitField('Soumettre')


