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
from my_app.models.jeei_package.specification import Specification, Theme, PublicCible, Statut
from my_app.models.jeei_package.jeei import Jeei
from my_app.models.user import User

#on crée une table 
class JointureJeeiUser(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'JointureJeeiUser' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fk_UserId = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    fk_JeeiId = db.Column(db.Integer, db.ForeignKey('Jeei.id'),nullable=False)

  
    
    
    def __init__(self, fk_UserId, fk_JeeiId):

    
        self.fk_UserId=fk_UserId
        self.fk_JeeiId=fk_JeeiId
    
    
    def __repr__(self):#toString
        return "( id=%s, userId= %s , jeeiId = %s)\n" % ( self.id, self.fk_UserId,self.fk_JeeiId)




db.create_all()#impératif!!!!

