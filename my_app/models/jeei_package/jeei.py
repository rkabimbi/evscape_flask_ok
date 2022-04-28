from flask_login import UserMixin
from my_app import login_manager
from my_app import db #importe l'objet DB cree dans le init.py
from werkzeug.security import generate_password_hash, check_password_hash #pour generer le password
from datetime import datetime#pour la date d'annif
from my_app import login_manager # A NE PAS OUBLIER

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from my_app.models.jeei_package.specification import Specification, Statut, Theme, PublicCible


#on crée une table d'Enigmes
class Jeei(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Jeei' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(80),  nullable=True)#nullable pour qu'il puisse creer à vide et completer ensuite
    img = db.Column(db.String(120), nullable=True)
    descriptif = db.Column(db.String(140),  nullable=True)

    dateCreation= db.Column(db.Date, nullable=False)
    fk_SpecificationId = db.Column(db.Integer, db.ForeignKey('Specification.id'),nullable=True)#db.foreignkey : c'est l'id de l'autre table et le nom de la table correspond à la back ref

  
    
    
    def __init__(self, nom,img,descriptif,fk_SpecificationId):

        self.nom = nom
        self.img = img
        self.descriptif = descriptif
        self.dateCreation= datetime.today() 
        self.fk_SpecificationId=fk_SpecificationId
    
    
    def __repr__(self):#toString
        return "( id = %s, nom = %s , img=%s, descriptif=%s,dateCreation=%s,fk_SpecificationId=%s)\n" % ( self.id, self.nom,self.img,self.descriptif,self.dateCreation,self.fk_SpecificationId)




db.create_all()#impératif!!!!

