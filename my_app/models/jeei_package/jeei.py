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
#from my_app.models.jeei_package.jointureJeeiUser import JointureJeeiUser
#from my_app.models.evaluation import Evaluation

#on crée une table 
class Jeei(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Jeei' #pour renomr la table "enigme""
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(80),  nullable=True,default=' ')#nullable pour qu'il puisse creer à vide + Je mets le points pcq sinon dans ele HTML ca pose probleme pr afficher les cartes avec du NONe
    img = db.Column(db.String(120), nullable=True, default=' ')# Je mets le points pcq sinon dans ele HTML ca pose probleme pr afficher les cartes avec du NONe
    descriptif = db.Column(db.String(140),  nullable=True, default=' ')# Je mets le points pcq sinon dans ele HTML ca pose probleme pr afficher les cartes avec du NONe
    estValide =db.Column(db.Boolean,default=False, nullable=False)
    dateCreation= db.Column(db.Date, nullable=False)
    auteurID = db.Column(db.Integer, nullable=False)
    fk_SpecificationId = db.Column(db.Integer, db.ForeignKey('Specification.id'),nullable=False)#db.foreignkey : c'est l'id de l'autre table et le nom de la table correspond à la back ref
    rel_JointureJeeiUser = relationship("JointureJeeiUser", backref='Jeei', uselist=False)
    rel_Experimentation = relationship("Experimentation", backref='Jeei', uselist=False)
    rel_Evaluation = relationship("Evaluation", backref='Jeei', uselist=False)

  
    
    
    def __init__(self, nom,img,descriptif,fk_SpecificationId,auteurID):

        self.nom = nom
        self.img = img
        self.descriptif = descriptif
        self.dateCreation= datetime.today() 
        self.fk_SpecificationId=fk_SpecificationId
        self.auteurID=auteurID

        #creation table jointure directement (il va assigner la personne qui le crée comme membre d'equipe)
        #creation de jointure entre JEEI et User
        #jointureJeeiUser=JointureJeeiUser(fk_JeeiId=self.id,fk_UserId=createurId)
        #db.session.add(jointureJeeiUser)#sauve dans la DB
        #db.session.commit()
      
    
    
    def __repr__(self):#toString
        return "( id = %s, nom = %s , img=%s, descriptif=%s,dateCreation=%s,fk_SpecificationId=%s, estValide=%s,auteurID=%s)\n" % ( self.id, self.nom,self.img,self.descriptif,self.dateCreation,self.fk_SpecificationId,self.estValide, self.auteurID)




db.create_all()#impératif!!!!

