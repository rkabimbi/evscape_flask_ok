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
from my_app.models.experimentation import Experimentation
from my_app.models.participant import Participant
from my_app.models.jeei_package.jeei import Jeei

#on crée une table 
class Evaluation(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Evaluation' #pour renomr la table 
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dateCreation= db.Column(db.Date, nullable=True)
    fk_JeeiId = db.Column(db.Integer, db.ForeignKey('Jeei.id'),nullable=False)
    fk_ExperimentationId = db.Column(db.Integer, db.ForeignKey('Experimentation.id'),nullable=False)
    fk_ParticipantId = db.Column(db.Integer, db.ForeignKey('Participant.id'),nullable=False)
    


  
    
    
    def __init__(self,fk_JeeiId,fk_ExperimentationId,fk_ParticipantId):
        self.fk_JeeiId=fk_JeeiId
        self.dateCreation=datetime.today()
        self.fk_ExperimentationId=fk_ExperimentationId
        self.fk_ParticipantId=fk_ParticipantId
    

       

      
    
    
    def __repr__(self):#toString
        return "( id = %s, dateCreation=%s, JeeiID = %s , ExperimentationId=%s, ParticipantId=%s)\n" % ( self.id, self.dateCreation,self.fk_JeeiId,self.fk_ExperimentationId,self.fk_ParticipantId)




db.create_all()#impératif!!!!

