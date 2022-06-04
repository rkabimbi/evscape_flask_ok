from email.policy import default
import imp
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
from my_app.models.questionnaireUX import QuestionnaireUX
from my_app.models.questionnaireMotivation import QuestionnaireMotivation
from my_app.models.questionnairePreTest import QuestionnairePreTest
from my_app.models.questionnairePostTest import QuestionnairePostTest

#on crée une table 
class Evaluation(UserMixin, db.Model):#userMixiin c'est pr traiter lesmethodes relatives aux login et l'autre pour les DB
    __tablename__ = 'Evaluation' #pour renomr la table 
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dateCreation= db.Column(db.Date, nullable=True)

    #pour faire le suivi de l'etat d'avancement de chaque participant dans l'evaluation
    questionnaireDemographique = db.Column(db.Boolean, default=False,nullable=False)
    questionnaireMotivation= db.Column(db.Boolean, default=False,nullable=False)
    preTest  = db.Column(db.Boolean, default=False,nullable=False)
    postTest1  = db.Column(db.Boolean, default=False,nullable=False)
    questionnaireUX = db.Column(db.Boolean, default=False,nullable=False)
    postTest2 = db.Column(db.Boolean, default=False,nullable=False)

    fk_JeeiId = db.Column(db.Integer, db.ForeignKey('Jeei.id'),nullable=False)
    fk_ExperimentationId = db.Column(db.Integer, db.ForeignKey('Experimentation.id'),nullable=False)
    fk_ParticipantId = db.Column(db.Integer, db.ForeignKey('Participant.id'),nullable=False)
    fk_QuestionnaireMotivationId = db.Column(db.Integer, db.ForeignKey('QuestionnaireMotivation.id'),nullable=True)
    fk_QuestionnaireUXId = db.Column(db.Integer, db.ForeignKey('QuestionnaireUX.id'),nullable=True)
    fk_QuestionnairePreTestId = db.Column(db.Integer, db.ForeignKey('QuestionnairePreTest.id'),nullable=True)
    fk_QuestionnairePostTestId = db.Column(db.Integer, db.ForeignKey('QuestionnairePostTest.id'),nullable=True)

   
    
    def __init__(self,fk_JeeiId,fk_ExperimentationId,fk_ParticipantId):
        self.fk_JeeiId=fk_JeeiId
        self.dateCreation=datetime.today()
        self.fk_ExperimentationId=fk_ExperimentationId
        self.fk_ParticipantId=fk_ParticipantId
    
 
    
    
    def __repr__(self):#toString
        return "( id = %s, dateCreation=%s, questionnaireDemo=%s, questionnaireMot=%s,preTest=%s,posttes1=%s, questionnaireUx=%s,posttest2=%s, JeeiID = %s , ExperimentationId=%s, ParticipantId=%s,motivation=%s, ux=%s,pre=%s;post=%s)\n" % ( self.id, self.dateCreation,self.questionnaireDemographique,self.questionnaireMotivation,self.preTest, self.postTest1,self.questionnaireUX,self.postTest2,self.fk_JeeiId,self.fk_ExperimentationId,self.fk_ParticipantId,self.fk_QuestionnaireMotivationId,self.fk_QuestionnaireUXId,self.fk_QuestionnairePreTestId,self.fk_QuestionnairePostTestId)




db.create_all()#impératif!!!!

