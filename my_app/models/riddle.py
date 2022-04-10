from flask_login import UserMixin
from my_app import login_manager
from my_app import db #importe l'objet DB cree dans le init.py
from werkzeug.security import generate_password_hash, check_password_hash #pour generer le password
from datetime import datetime#pour le timestamp du message (j'ai pas utilisé)


from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from my_app.models.user import User#si je ne fais pas ça alors il ne sait pas acceder à la foreginkey!!!!!!!


#on crée une table d'Enigmes
class Enigmes( db.Model):# pour heriter de tt ce qui est model
    
    __tablename__ = 'enigme' #pour renomr la table "enigme""
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)#type Integer, clé primaire et increment automatiue
    niveau = db.Column(db.Integer, unique=False, nullable=False)
    question = db.Column(db.String(200))
    reponse = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#on crée une colonne dans la table qui contient la clée etrangere user.id (voir table User)
    r_indice=db.relationship('Clue', backref=db.backref('ind', lazy=True),cascade="all, delete-orphan")#pour effacer en cascade ce qui est lié à l'enigme
    categorie=db.Column(db.String(200),nullable=True)
    
    def __repr__(self):#toString
        return "(id=%i, question = %s, reponse = %s , niveau=%s, user=%s)\n" % (self.id, self.question, self.reponse,self.niveau,self.user_id)

    def getQuestion(self):
        return str(self.question)

    def __init__(self,niveau,question,reponse,user_id,categorie):#constructeur mais dans la pratique je prefere utiliser avec des "="
            self.niveau=niveau
            self.question=question
            self.reponse=reponse
            self.user_id = user_id
            self.categorie=categorie
    

db.create_all()#impératif!!!!!!



class EnigmesJsn():# pour heriter de tt ce qui est model
    
    
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)#type Integer, clé primaire et increment automatiue
    #niveau = db.Column(db.Integer, unique=False, nullable=False)
    #question = db.Column(db.String(200))
    #reponse = db.Column(db.String(200))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#on crée une colonne dans la table qui contient la clée etrangere user.id (voir table User)
    #r_indice=db.relationship('Clue', backref=db.backref('ind', lazy=True),cascade="all, delete-orphan")#pour effacer en cascade ce qui est lié à l'enigme
    
    #def __repr__(self):#toString
    #    return "(id=%i, question = %s, reponse = %s , niveau=%s, user=%s)\n" % (self.id, self.question, self.reponse,self.niveau,self.user_id)

    #def getQuestion(self):
    #    return str(self.question)
    niveau=0
    question="xxxxx"
    reponse="xxxxxx"
    user_id=0
    r_indice=0
    id=0


    def __init__(self,niveau,question,reponse,user_id,r_indice,id):#constructeur mais dans la pratique je prefere utiliser avec des "="
            self.niveau=niveau
            self.question=question
            self.reponse=reponse
            self.user_id = user_id
            self.r_indice=r_indice
            self.id=id
    
    def __repr__(self):#toString
        return "(id=%i, question = %s, reponse = %s , niveau=%s, user=%s)\n" % (self.id, self.question, self.reponse,self.niveau,self.user_id)


