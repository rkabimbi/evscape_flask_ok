from collections import UserList
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


class PublicCible(enum.Enum):
    UNIVB = "Baccalaureat"
    UNIVM = "Master"
    SECSUP = "Secondaire superieur"
    SECINF = "Secondaire inférieur"
    PRIM = "Primaire"

class Theme(enum.Enum):
    ALGO = "Algorithmie"
    PROG = "Programmation"
    SEC = 'CyberSecurité'
    MATH = "Mathématique"
    SE = "Ingenirie Logiciel"

class Statut(enum.Enum):
    ENCOURS = "En cours"
    PRET ="Pret"


#on crée une table d'Enigmes
class Specification(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Specification' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nbrJoueursMin=db.Column(db.Integer,default=1)
    nbrJoueursMax=db.Column(db.Integer,default=1)
    budget=db.Column(db.Float,default=0)
    dureeMinutes=db.Column(db.Integer,default=0)
    scenario = db.Column(db.Text(),nullable=True)
    publicCible =db.column(db.Enum(PublicCible))
    theme =db.column(db.Enum(Theme))
    chapitre = db.Column(db.String(120),nullable=True)
    statut =db.column(db.Enum(Theme))
    rel_Jeei = relationship("Jeei", backref='Specification', uselist=False)#backref = la manière dont c'est appelé dans l'autre table
    


    #score=db.Column(db.Integer,default=0)
    #r_enigme=db.relationship('Enigmes', backref=db.backref('auteur', lazy=True))#on dit que la relation c'est avec la classe Enigmes 
    
    
    def __init__(self, nbrJoueursMin,nbrJoueursMax,budget,dureeMinutes,scenario,publicCible,theme,chapitre,statut):

        self.nbrJoueursMax=nbrJoueursMax
        self.nbrJoueursMin=nbrJoueursMin
        self.budget=budget
        self.dureeMinutes=dureeMinutes
        self.scenario=scenario
        self.publicCible=publicCible
        self.theme=theme
        self.chapitre=chapitre
        self.statut=statut
        #self.key_Jeei=key_Jeei
    



    
    
    
    def __repr__(self):#toString
        return "( nbrJoueursMax = %s, nbrJouersMin = %s , dureeMinutes=%s, scenario=%s,theme=%s,statut=%s)\n" % ( self.nbrJoueursMax,self.nbrJoueursMin,self.dureeMinutes,self.scenario,self.theme,self.statut)




db.create_all()#impératif!!!!

