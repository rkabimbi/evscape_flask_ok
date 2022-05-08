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

#on crée une table 
class QuestionApprentissage(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'QuestionApprentissage' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    question = db.Column(db.String(120),nullable=True,default='')
    solutionCorrecte = db.Column(db.String(120),nullable=True,default='')
    solutionIncorrecte1 = db.Column(db.String(120),nullable=True,default='')
    solutionIncorrecte2 = db.Column(db.String(120),nullable=True,default='')
    solutionIncorrecte3 = db.Column(db.String(120),nullable=True,default='')
    explicatif = db.Column(db.Text(),nullable=True,default='')
    fk_SpecificationId = db.Column(db.Integer, db.ForeignKey('Specification.id'))
    


    #score=db.Column(db.Integer,default=0)
    #r_enigme=db.relationship('Enigmes', backref=db.backref('auteur', lazy=True))#on dit que la relation c'est avec la classe Enigmes 
    
    
    def __init__(self,question,solutionCorrecte, solutionIncorrecte1, solutionIncorrecte2, solutionIncorrecte3, explicatif,fk_SpecificationID ):
        self.question=question
        self.solutionCorrecte=solutionCorrecte
        self.solutionIncorrecte1=solutionIncorrecte1
        self.solutionIncorrecte2=solutionIncorrecte2
        self.solutionIncorrecte3=solutionIncorrecte3
        self.explicatif=explicatif
        self.fk_SpecificationId=fk_SpecificationID

       
        #self.key_Jeei=key_Jeei
    



    
    
    
    def __repr__(self):#toString
        return "( id = %s, question=%s \n, solutionCorrecte=%s\n,explicatif=%s\n,solutionIncorrecte1=%s,\n solutionIncorrecte2=%s,\nsolutionIconrrecte3=%s)\n" % ( self.id,self.question,self.solutionCorrecte,self.explicatif, self.solutionIncorrecte1,self.solutionIncorrecte2,self.solutionIncorrecte3)




db.create_all()#impératif!!!!

