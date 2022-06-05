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

#on crée une table 
class Experimentation(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Experimentation' #pour renomr la table 
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    idInterne = db.Column(db.Integer,nullable=True)
    dateEvenement= db.Column(db.Date, nullable=True)
    etape1 =db.Column(db.Boolean,default=False, nullable=False)
    etape2 =db.Column(db.Boolean,default=False, nullable=False)
    etape3 =db.Column(db.Boolean,default=False, nullable=False)
    etape4 =db.Column(db.Boolean,default=False, nullable=False)
    etape5 =db.Column(db.Boolean,default=False, nullable=False)
    etape6 =db.Column(db.Boolean,default=False, nullable=False)
    etape7 =db.Column(db.Boolean,default=False, nullable=False)
    etape8 =db.Column(db.Boolean,default=False, nullable=False)
    etape9 =db.Column(db.Boolean,default=False, nullable=False)
    etape10 =db.Column(db.Boolean,default=False, nullable=False)
    etape11 =db.Column(db.Boolean,default=False, nullable=False)
    etape12 =db.Column(db.Boolean,default=False, nullable=False)
    etape13 =db.Column(db.Boolean,default=False, nullable=False)
    fk_JeeiId = db.Column(db.Integer, db.ForeignKey('Jeei.id'),nullable=False)#db.foreignkey : c'est l'id de l'autre table et le nom de la table correspond à la back ref
    fk_UserId = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    rel_Participant = relationship("Participant", backref='Experimentation', uselist=False)
    rel_Evaluation = relationship("Evaluation", backref='Experimentation', uselist=False)


  
    
    
    def __init__(self,fk_JeeiId,fk_UserId,idInterne,):
        self.fk_JeeiId=fk_JeeiId
        self.fk_UserId=fk_UserId
        self.idInterne=idInterne
        self.dateEvenement=datetime.today()

       

        #creation table jointure directement (il va assigner la personne qui le crée comme membre d'equipe)
        #creation de jointure entre JEEI et User
        #jointureJeeiUser=JointureJeeiUser(fk_JeeiId=self.id,fk_UserId=createurId)
        #db.session.add(jointureJeeiUser)#sauve dans la DB
        #db.session.commit()
      
    
    
    def __repr__(self):#toString
        return "( id = %s, idInterne=%s, etape1 = %s , etape2=%s, etape3=%s,etape4=%s,etape5=%s, etape6=%s,etape7=%s,etape8=%s,etape9=%s,etape10=%s,etape11=%s,etape12=%s,jeeiId=%s)\n" % ( self.id, self.idInterne,self.etape1,self.etape2,self.etape3,self.etape4,self.etape5,self.etape6, self.etape7,self.etape8,self.etape9,self.etape10,self.etape11,self.etape12,self.fk_JeeiId)




db.create_all()#impératif!!!!

