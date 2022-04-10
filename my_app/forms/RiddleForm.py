from my_app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms   import StringField, SubmitField #classe utilisée pour construire les champs des formulaires
from wtforms.validators import InputRequired, Length, ValidationError,NumberRange #validateur d'input
from wtforms   import PasswordField, BooleanField, FileField, IntegerField,SelectField
from wtforms.validators import  EqualTo,Optional

#on crée une classe NameForm laquelle herite de FlaskForm 
#creation formulaire enigme
class EnigmeForm( FlaskForm ):
    #champ de type String, avec le label "Question" et un validateur. Les messages d'erreurs sont gérés via HTML
    question    = StringField('Question:', validators=[InputRequired(), Length(min=5, max=70, message='Question doit avoir une longueur de  %(min)d à %(max)d caractères')]) 
    reponse = StringField('Réponse:', validators=[InputRequired(), Length(min=5, max=15, message='Reponse doit avoir une longueur de  %(min)d à %(max)d caractères')])
    niveau = IntegerField('Niveau:', validators=[InputRequired(), NumberRange(min=0, max=5, message='Niveau doit être compris entre  %(min)d et %(max)d ')])
    categorie = SelectField('Categorie :', validators=[Optional()],choices=[('math','math'),('humour','humour'),('sciences','sciences')])
    submit  = SubmitField('Soumettre')#attribut submit -->IMPERATIF!!!!

#creation formulaire de reponse aux enigmes
class ReponseForm(FlaskForm):
    reponse = StringField('Réponse:', validators=[InputRequired(), Length(min=5, max=15, message='Reponse doit avoir une longueur de  %(min)d à %(max)d caractères')])
    submit  = SubmitField('Soumettre')



