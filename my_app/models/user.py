from flask_login import UserMixin
from my_app import login_manager
from my_app import db #importe l'objet DB cree dans le init.py
from werkzeug.security import generate_password_hash, check_password_hash #pour generer le password
from datetime import datetime#pour la date d'annif
from my_app import login_manager # A NE PAS OUBLIER

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


#on crée une table d'Enigmes
class User(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'user' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(250), nullable=False)
    birthday= db.Column(db.Date, nullable=True)
    admin = db.Column(db.Boolean, nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    score=db.Column(db.Integer,default=0)
    r_enigme=db.relationship('Enigmes', backref=db.backref('auteur', lazy=True))#on dit que la relation c'est avec la classe Enigmes 
    
    
    def __init__(self, username, firstname, lastname,password,email,birthday,admin):

        self.username = username
        self.email = email
        self.password = password
        self.birthday = birthday
        self.firstname = firstname
        self.lastname = lastname 

        self.admin = admin 

    
    
    
    def __repr__(self):#toString
        return "( username = %s, firstname = %s , lastname=%s, pwd=%s,email=%s,birth=%s,admin=%s)\n" % ( self.username, self.firstname,self.lastname,self.password,self.email,self.birthday,self.admin)




db.create_all()#impératif!!!!


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))