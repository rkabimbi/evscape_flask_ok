from collections import UserList
from email.policy import default
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

class Statut(enum.Enum):
    ENCOURS="En-cours"
    PRET="Prêt"

class PublicCible(enum.Enum):
    BACCALAUREAT = "Baccalaureat"
    MASTER = "Master"
    SECONDAIRE = "Seoncdaire"
    PRIMAIRE = "Primaire"
    ADEFINIR = "A Définir" #je fais ca pour mettre des valeurs par defaut sinon à l'afffichage ca bug car il sait pas afficher certain "none"


class Theme(enum.Enum):
    ALGORITHMIE = "Algorithmie"
    PROGRAMMATION = "Programmation"
    SECURITEIT = "Securité Informatique"
    MATHEMATIQUE = "Mathématiques"
    INGENIRIELOGICIEL = "Inegnierie Logicielle"
    ADEFINIR = "A Définir"




#on crée une table d'Enigmes
class Specification(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Specification' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nbrJoueursMin=db.Column(db.Integer,nullable=True,default=0)
    nbrJoueursMax=db.Column(db.Integer,nullable=True,default=0)
    budget=db.Column(db.Float,nullable=True,default=0)
    dureeMinutes=db.Column(db.Integer,nullable=True,default=0)
    scenario = db.Column(db.Text(),nullable=True,default='')
    publicCible =db.Column(db.Enum(PublicCible),nullable=True, default=PublicCible.ADEFINIR)
    theme =db.Column(db.Enum(Theme),nullable=True, default=Theme.ADEFINIR)
    chapitre = db.Column(db.String(120),nullable=True,default='')
    statut =db.Column(db.Enum(Statut),nullable=True, default=Statut.ENCOURS)
    documentation = db.Column(db.String(120), nullable=True, default=' ')#adresse locale vers la doc
    rel_Jeei = relationship("Jeei", backref='Specification', uselist=False)#backref = la manière dont c'est appelé dans l'autre table
    


    #score=db.Column(db.Integer,default=0)
    #r_enigme=db.relationship('Enigmes', backref=db.backref('auteur', lazy=True))#on dit que la relation c'est avec la classe Enigmes 
    
    
    def __init__(self, nbrJoueursMin,nbrJoueursMax,budget,dureeMinutes,scenario,publicCible,theme,chapitre,statut,documentation):

        self.nbrJoueursMax=nbrJoueursMax
        self.nbrJoueursMin=nbrJoueursMin
        self.budget=budget
        self.dureeMinutes=dureeMinutes
        self.scenario=scenario
        self.publicCible=publicCible
        self.theme=theme
        self.chapitre=chapitre
        self.statut=statut
        self.documentation=documentation
        #self.key_Jeei=key_Jeei
    



    
    
    
    def __repr__(self):#toString
        return "( nbrJoueursMax = %s, nbrJouersMin = %s , dureeMinutes=%s, scenario=%s,theme=%s,statut=%s,documentation=%s)\n" % ( self.nbrJoueursMax,self.nbrJoueursMin,self.dureeMinutes,self.scenario,self.theme,self.statut,self.documentation)




db.create_all()#impératif!!!!

