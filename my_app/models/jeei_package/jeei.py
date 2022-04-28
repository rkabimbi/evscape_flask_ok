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
class Jeei(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Jeei' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(80), unique=False, nullable=False)
    img = db.Column(db.String(120), unique=False)

    dateCreation= db.Column(db.Date, nullable=True)

    #r_enigme=db.relationship('Enigmes', backref=db.backref('auteur', lazy=True))#on dit que la relation c'est avec la classe Enigmes 
    
    
    def __init__(self, nom,img):

        self.nom = nom
        self.img = img
        self.dateCreation= datetime.today() 
    
    
    def __repr__(self):#toString
        return "( id = %s, nom = %s , img=%s,dateCreation=%s)\n" % ( self.id, self.nom,self.img,self.dateCreation)




db.create_all()#impératif!!!!


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))