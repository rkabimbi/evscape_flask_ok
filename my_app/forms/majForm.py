from my_app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms   import StringField, SubmitField #classe utilisée pour construire les champs des formulaires
from wtforms.validators import InputRequired, Length, ValidationError,NumberRange #validateur d'input
from wtforms   import PasswordField, BooleanField, FileField, IntegerField, SelectField
from wtforms.validators import  EqualTo
from wtforms   import PasswordField



#formulaire de maj enigme
class MajForm( FlaskForm ):
    question    = StringField('Question:', validators=[InputRequired(), Length(min=5, max=150, message='Question doit avoir une longeur entre %(min)d et %(max)d caracteres')]) 
    reponse = StringField('Réponse:', validators=[InputRequired(), Length(min=5, max=15, message='Reponse doit avoir une longeur entre %(min)d et %(max)d caracteres')])
    niveau = IntegerField('Niveau:', validators=[InputRequired(), NumberRange(min=0, max=5, message='Niveau doit avoir une longeur entre %(min)d et %(max)d caracteres')])
    #ici on construit un attribut submit, qui est un autre type de champs de formulaire (SubmitFiled) et on doit juste spécifier un label ici
    categorie = SelectField('Categorie :', choices=[('math','math'),('humour','humour'),('sciences','sciences')])
    submit  = SubmitField('Soumettre')


