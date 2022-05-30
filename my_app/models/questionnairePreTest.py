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



#on crée une table d'Enigmes
class QuestionnaireMotivation(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'QuestionnaireMotivation' 
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
   
    m01 = db.Column(db.Integer, nullable=True)
    m02 = db.Column(db.Integer, nullable=True)
    m03 = db.Column(db.Integer, nullable=True)
    rel_Evaluation = relationship("Evaluation", backref='QuestionnaireMotivation', uselist=False)
 
  

    #score=db.Column(db.Integer,default=0)
    #r_enigme=db.relationship('Enigmes', backref=db.backref('auteur', lazy=True))#on dit que la relation c'est avec la classe Enigmes 

    def __init__(self):
        print("constructeur vide questionnaire motivation")
        
        
 

    
    
    
    def __repr__(self):#toString
        return "( id = %s, m01 = %s , m02=%s, m03=%s)\n" % ( self.id, self.m01,self.m02,self.m03)




db.create_all()#impératif!!!!



