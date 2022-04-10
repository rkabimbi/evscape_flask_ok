from my_app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms   import StringField, SubmitField #classe utilisée pour construire les champs des formulaires
from wtforms.validators import InputRequired, Length, ValidationError,NumberRange #validateur d'input
from wtforms   import PasswordField, BooleanField, FileField, IntegerField,RadioField
from wtforms.validators import  EqualTo

from wtforms   import PasswordField
from wtforms.validators import DataRequired, Email

from datetime import date
from flask import flash

from wtforms.fields import DateField, EmailField, TelField


#formulaire pour inscription utilisateur
class FormRegister( FlaskForm ):
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=20,message='Username doit avoir une longueur de  %(min)d à %(max)d caractères')])
    email = StringField('Email:', validators=[Email(message="Le format d'email n'est pas correct"), InputRequired(), Length(min=3, max=60,message="Veuillez renseigner un email d'une taille entre %(min)d à %(max)d caractères")])
    birthday = DateField("Birthday", default=date.today(), validators=[DataRequired(message="Entrez une date de naissance")])
    firstname = StringField('First name:', validators=[InputRequired(), Length(min=2, max=30,message='Votre prénom doit avoir une longueur de  %(min)d à %(max)d caractères')])
    lastname = StringField('Last name:', validators=[InputRequired(), Length(min=2, max=30,message='Votre nom doit avoir une longueur de  %(min)d à %(max)d caractères')])
    password = PasswordField('Password:', validators=[Length(min=3, max=60,message='Votre mdp doit avoir une longueur de  %(min)d à %(max)d caractères')])
    passwordConfirmation = PasswordField('Confirmation Password:', validators=[Length(min=3, max=60), EqualTo('password',message='Veuillez verifier votre password car visiblement différent de celui tapé précédemment') ])
    admin=BooleanField('Admin',default=1)

    submit   = SubmitField('Enregistrer')


