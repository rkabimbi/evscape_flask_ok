from cmath import exp
from flask_login import UserMixin
from my_app import login_manager
from my_app import db #importe l'objet DB cree dans le init.py
from werkzeug.security import generate_password_hash, check_password_hash #pour generer le password
from datetime import datetime#pour la date d'annif
from my_app import login_manager # A NE PAS OUBLIER

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from random import choice, randint

from my_app.models.jeei_package.specification import PublicCible
from my_app.models.questionnaireMotivation import QuestionnaireMotivation




#pour generer de l'aléatoire
alphabet_min = [ chr(i) for i in range(97,123) ]
alphabet_maj = [ chr(i) for i in range(65,91) ]
chiffres = [ chr(i) for i in range(48,58) ]
caracteres_speciaux = [ '%' , '_' , '-' , '!' , '$' , '^' , '&' , '#' , '(' , ')' , '[' , ']' , '=' , '@']


def pwd(n , min = True, maj = True, chif = True, cs = False):
    alphabets = dict()
    key = 0
    if min:
        alphabets[key] = alphabet_min
        key += 1
    if maj:
        alphabets[key] = alphabet_maj
        key += 1
    if chif:
        alphabets[key] = chiffres
        key += 1
    if cs:
        alphabets[key] = caracteres_speciaux
        key += 1
    
    mdp = ''
    for i in range(n):
            s = randint(0,key-1)
            mdp += choice( alphabets[s] )
            
    return mdp



class Sexe(enum.Enum):
    MASCULIN="Masculin"
    FEMININ="Feminin"

class ExperienceJeei(enum.Enum):
    JAMAIS="Jamais"
    RAREMENT="Rarement"
    REGULIEREMENT="Regulierement"




class Localisation(enum.Enum):
    AFRIQUE="Afrique"
    AMSUD="Amerique du Nord"
    AMNORD="Amerique du Sud"
    ASIE="Asie"
    EUROPE="Europe"
    OCEANIE="Oceanie"

class Experience(enum.Enum):
    NEANT="Néant"
    NOVICE="Novice"
    CONFIRME="Confirme"
    EXPERT="Expert"


#on crée une table d'Enigmes
class Participant(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Participant' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
   
    age = db.Column(db.Integer, nullable=True)
    sexe =db.Column(db.Enum(Sexe),nullable=True)
    email = db.Column(db.String(120))
    expJEEI =db.Column(db.Enum(ExperienceJeei),nullable=True)
    etudes = db.Column(db.Enum(PublicCible),nullable=True)
    localisation =db.Column(db.Enum(Localisation),nullable=True)
    experience = db.Column(db.Enum(Experience),nullable=True)
    groupeExperimental =db.Column(db.Boolean,default=False, nullable=True)
    consentement =db.Column(db.Boolean,default=False, nullable=True)
    nom= db.Column(db.String(120))
    prenom= db.Column(db.String(120))
    urlPerso=db.Column(db.String(120))#pour que chacun ait son propre url et que personne ne puisse le deviner et donc competer à sa place
   

    fk_ExperimentationId = db.Column(db.Integer, db.ForeignKey('Experimentation.id'),nullable=False)
    rel_Evaluation = relationship("Evaluation", backref='Participant', uselist=False)
 
  

    #score=db.Column(db.Integer,default=0)
    #r_enigme=db.relationship('Enigmes', backref=db.backref('auteur', lazy=True))#on dit que la relation c'est avec la classe Enigmes 

    def __init__(self):
        print("constructeur vide participant")
        self.urlPerso=pwd(20,True,True,True,False)
        
 

    
    
    
    def __repr__(self):#toString
        return "( nom = %s, prenom = %s , email=%s, etude=%s,Experimentation=%s,urlPerso=%s)\n" % ( self.nom, self.prenom,self.email,self.etudes,self.fk_ExperimentationId,self.urlPerso)




db.create_all()#impératif!!!!


"""

def __init__(self, age,sexe,email,expJEEI, etudes, localisation,experience,groupeExperimental, consentement,fk_ExperimentationId, nom, prenom):

        self.age=age
        self.sexe=sexe
        self.email=email
        self.expJEEI=expJEEI
        self.etudes=etudes
        self.localisation=localisation
        self.experience=experience
        self.groupeExperimental=groupeExperimental
        self.consentement=consentement
        self.fk_ExperimentationId=fk_ExperimentationId
        self.nom=nom
        self.prenom=prenom
"""


