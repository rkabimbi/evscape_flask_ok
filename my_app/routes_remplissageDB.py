##########################################################
#mes imports
##########################################################

from cgi import test

from sqlalchemy import true
from my_app import app
from flask import Flask, redirect
from flask import request
from flask import render_template
from jinja2 import Template
from jinja2 import Environment, PackageLoader
from jinja2 import environment
from random import randint
import math

from my_app import db #import de la db




from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from flask import json, jsonify
from my_app.models.experimentation import Experimentation
from my_app.models.participant import Participant
from my_app.models.questionnaireMotivation import QuestionnaireMotivation
from my_app.models.questionnairePreTest import QuestionnairePreTest
from my_app.models.questionnaireUX import QuestionnaireUX
from my_app.models.questionnairePostTest import QuestionnairePostTest

from my_app.models.user import User
import random

from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()


from my_app.models.jeei_package.jeei import Jeei

from my_app.models.jeei_package.specification import Specification, Statut, Theme, PublicCible
from my_app.models.jeei_package.questionApprentissage import QuestionApprentissage
from my_app.models.jeei_package.jointureJeeiUser import JointureJeeiUser
from my_app.models.participant import Participant, Sexe, ExperienceJeei, Localisation, Experience
from my_app.models.evaluation import Evaluation
from my_app.models.questionnaireUEQ import QuestionnaireUEQ

"""
Pour rappel le fonction de flask c'est qu'à chaque changement il reparcours tt le fichier je pense. Notament pour le login.
Je pens donc que je dois laisser la racine à la page "home" et juste faire sur le chemin racine que si pas connecté il renvoi la page login!!!!
comme ca quand mon formulaire de wtf est validé ca va repasser par la racine
"""




#####################################################
#REMPLIASSAGE DB (à effacer à la fin)
#####################################################

def function_lancementDBFictive():
    db.drop_all()
    db.create_all()

    utilisateur=User(username="rootroot",firstname="Rudy",lastname="KABIMBI",password=generate_password_hash("rootrootroot", "sha256"),email="rudykabimbi@evscApp.edu",titre="chercheur",universite="Unamur")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()
    utilisateur=User(username="gyernaux",firstname="Gonzague",lastname="Yernaux",password=generate_password_hash("rootrootroot", "sha256"),email="gonzagueyernaux@evscApp.edu",titre="assistant",universite="Unamur")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()
    utilisateur=User(username="bvandezande",firstname="Bart",lastname="Vandezande",password=generate_password_hash("rootrootroot", "sha256"),email="bvandz@kul.com",titre="assistant",universite="KUL")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()








    #CREA De JEEI
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=500,dureeMinutes=150, publicCible=PublicCible.MASTER,theme=Theme.AL,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Logique propositionelle",statut=Statut.ENCOURS,documentation="")
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=3,nbrJoueursMin=2,budget=5500,dureeMinutes=120, publicCible=PublicCible.PRIMAIRE,theme=Theme.DS,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="chiffrement de cesar",statut=Statut.ENCOURS,documentation="")
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=8,nbrJoueursMin=1,budget=1500,dureeMinutes=60,statut=Statut.PRET, publicCible=PublicCible.SECONDAIRE,theme=Theme.HCI,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Diagramme de classe",documentation="")

    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=850,dureeMinutes=100, publicCible=PublicCible.MASTER,theme=Theme.AL,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Recursivité",statut=Statut.ENCOURS,documentation="")
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=500,dureeMinutes=150,statut=Statut.PRET, publicCible=PublicCible.BACCALAUREAT,theme=Theme.PL,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Orienté objet",documentation="")

    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=18,nbrJoueursMin=2,budget=2800,dureeMinutes=150, publicCible=PublicCible.BACCALAUREAT,theme=Theme.AL,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Complexité",statut=Statut.ENCOURS,documentation="")

    db.session.add(specification)#sauve dans la DB
    db.session.commit()


    jeei=Jeei(nom="DesKape",img="static/img/img1.png",descriptif="Retrouvez les copies d\'examen",fk_SpecificationId=1,auteurID=2)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Unbox",img="static/img/img2.png",descriptif="Les poupees russes vous feront perdre la tête",fk_SpecificationId=2,auteurID=1)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="The green house",img="static/img/img3.png",descriptif="Un jeu qui vous en fera voir de toutes les couleursimg",fk_SpecificationId=3,auteurID=3)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Algorithmo Express",img="static/img/img4.png",descriptif="Entrez dans les méandres de la récursivité",fk_SpecificationId=4,auteurID=1)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="The Stranger Things",img="static/img/img5.png",descriptif="Inspirez de la série TV",fk_SpecificationId=5,auteurID=1)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Descape Basics",img="static/img/img6.png",descriptif="Un jeu simple mais éfficace",fk_SpecificationId=6,auteurID=2)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()



    #crea questionApprentissage

    
    for i in range(1,7):
    
        for q in range(1,11):
            question = QuestionApprentissage(question="Question"+str(q)+"Spec"+str(i),solutionCorrecte="Reponse"+str(q)+"Spec"+str(i), solutionIncorrecte1="responseA", solutionIncorrecte2="reponseB",solutionIncorrecte3="reponseC",explicatif="tu aurais dû mieux faire",fk_SpecificationID=i)
            db.session.add(question)
            db.session.commit()

 
    #creation de jointure entre JEEI et User
    jointureJeeiUser=JointureJeeiUser(fk_JeeiId=1,fk_UserId=2)
    db.session.add(jointureJeeiUser)#sauve dans la DB
    db.session.commit()

    #creation de jointure entre JEEI et User
    jointureJeeiUser=JointureJeeiUser(fk_JeeiId=3,fk_UserId=3)
    db.session.add(jointureJeeiUser)#sauve dans la DB
    db.session.commit()

       #creation de jointure entre JEEI et User
    jointureJeeiUser=JointureJeeiUser(fk_JeeiId=6,fk_UserId=1)
    db.session.add(jointureJeeiUser)#sauve dans la DB
    db.session.commit()

           #creation de jointure entre JEEI et User
    jointureJeeiUser=JointureJeeiUser(fk_JeeiId=6,fk_UserId=2)
    db.session.add(jointureJeeiUser)#sauve dans la DB
    db.session.commit()

          #creation de jointure entre JEEI et User
    jointureJeeiUser=JointureJeeiUser(fk_JeeiId=2,fk_UserId=2)
    db.session.add(jointureJeeiUser)#sauve dans la DB
    db.session.commit()

          #creation de jointure entre JEEI et User
    jointureJeeiUser=JointureJeeiUser(fk_JeeiId=4,fk_UserId=3)
    db.session.add(jointureJeeiUser)#sauve dans la DB
    db.session.commit()

          #creation de jointure entre JEEI et User
    jointureJeeiUser=JointureJeeiUser(fk_JeeiId=5,fk_UserId=1)
    db.session.add(jointureJeeiUser)#sauve dans la DB
    db.session.commit()
    
    experimentation = Experimentation(fk_JeeiId=1,fk_UserId=2,idInterne=1)
    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()

    experimentation = Experimentation(fk_JeeiId=1,fk_UserId=1,idInterne=2)
    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()

    experimentation = Experimentation(fk_JeeiId=1,fk_UserId=1,idInterne=3)
    experimentation.etape1=True #je fait ca pour eviter de devoir tjrs valider la liste des personne
    experimentation.etape2=True
    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()

    #experimentation = Experimentation(fk_JeeiId=3,fk_UserId=2,idInterne=1)
    #db.session.add(experimentation)#sauve dans la DB
    #db.session.commit()

    experimentation = Experimentation(fk_JeeiId=3,fk_UserId=1,idInterne=2)
    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()

    participant = Participant()
    participant.age=21
    participant.sexe=Sexe.MASCULIN
    participant.email='rkabimbi@yahoo.fr'
    participant.expJEEI=ExperienceJeei.RAREMENT
    participant.etudes=PublicCible.BACCALAUREAT
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.EXPERT
    participant.groupeExperimental=True
    participant.consentement=True
    participant.fk_ExperimentationId=1
    participant.nom='jean'
    participant.prenom='pierre'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

 
    participant = Participant()
    participant.age=24
    participant.sexe=Sexe.FEMININ
    participant.email='rudy.kabimbingoy@student.unamur.be'
    participant.expJEEI=ExperienceJeei.RAREMENT
    participant.etudes=PublicCible.BACCALAUREAT
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.EXPERT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Boudlal'
    participant.prenom='Khalid'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()


   

    participant = Participant()
    participant.age=20
    participant.sexe=Sexe.MASCULIN
    participant.email='zouzou@yahoo.fr'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Tozer'
    participant.prenom='Elie'
  
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    
    participant = Participant()
    participant.age=21
    participant.sexe=Sexe.MASCULIN
    participant.email='rudy.kabimbingoy@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Lita'
    participant.prenom='Zoe'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()
    
    participant = Participant()
    participant.age=18
    participant.sexe=Sexe.MASCULIN
    participant.email='rudy.kabimbiLito@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='toto'
    participant.prenom='litoe'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    participant = Participant()
    participant.age=19
    participant.sexe=Sexe.MASCULIN
    participant.email='rudy.RusaiLito@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Gisele'
    participant.prenom='Giligi'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    participant = Participant()
    participant.age=27
    participant.sexe=Sexe.MASCULIN
    participant.email='Patrick.RusaiLito@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Patricke'
    participant.prenom='Kluivert'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    participant = Participant()
    participant.age=12
    participant.sexe=Sexe.MASCULIN
    participant.email='bernard.albert@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Bernard'
    participant.prenom='Albert'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()
    
    participant = Participant()
    participant.age=23
    participant.sexe=Sexe.MASCULIN
    participant.email='riLito@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='to'
    participant.prenom='lie'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    participant = Participant()
    participant.age=19
    participant.sexe=Sexe.MASCULIN
    participant.email='rudy.RusaiLito@s.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Gele'
    participant.prenom='Gigi'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    participant = Participant()
    participant.age=27
    participant.sexe=Sexe.MASCULIN
    participant.email='Paick.RuiLito@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Patrke'
    participant.prenom='Klert'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    participant = Participant()
    participant.age=12
    participant.sexe=Sexe.MASCULIN
    participant.email='berd.albert@student.unamur.be'
    participant.expJEEI=ExperienceJeei.REGULIEREMENT
    participant.etudes=PublicCible.MASTER
    participant.localisation= Localisation.AFRIQUE
    participant.experience= Experience.NEANT
    participant.groupeExperimental=False
    participant.consentement=True
    participant.fk_ExperimentationId=3
    participant.nom='Berrd'
    participant.prenom='Aert'
    db.session.add(participant)#sauve dans la DB
    db.session.commit()




    ###########################################################################
    #        REMPLISSAGE DB spécifique pour tester les calculs!!!! #######
    #####################################################################
    # 
    # #remplir une exp pour GreenHouse avec une eval
    # 
     
    expGreenHouse=Experimentation.query.filter_by(fk_JeeiId=3).first()
    
    participant=Participant()
    participant.age=5
    participant.sexe=Sexe.MASCULIN
    participant.email="Cloclo@kabi.be"
    participant.expJEEI=ExperienceJeei.RAREMENT
    participant.etudes=PublicCible.PRIMAIRE
    participant.localisation=Localisation.EUROPE
    participant.experience=Experience.NEANT
    participant.consentement=True
    participant.groupeExperimental=True
    participant.nom="Francois"
    participant.prenom="Claude"
    participant.urlPerso="djkbsjdhskdkjsdiuklsdjf"
    participant.fk_ExperimentationId=expGreenHouse.id
    db.session.add(participant)#sauve dans la DB
    db.session.commit()
    print("ok")
    expGreenHouse.etape1=True
    expGreenHouse.etape2=True
    expGreenHouse.etape3=True
    expGreenHouse.etape4=True
    expGreenHouse.etape5=True
    expGreenHouse.etape6=True
    expGreenHouse.etape7=False
    expGreenHouse.etape8=False
    expGreenHouse.etape9=False
    expGreenHouse.etape10=False
    expGreenHouse.etape11=True
    expGreenHouse.etape12=True
    expGreenHouse.fk_JeeId=3
    expGreenHouse.fk_UserId=1
    db.session.add(expGreenHouse)#sauve dans la DB
    db.session.commit()
    print("ok2")

    expGreenHouse=Experimentation.query.order_by(Experimentation.id.desc()).first()
    participant=Participant.query.order_by(Participant.id.desc()).first()

    evaluationA=Evaluation(3,expGreenHouse.id,participant.id)
    evaluationA.questionnaireDemographique=True


    qMot=QuestionnaireMotivation()
    qMot.m01=2
    qMot.m02=2
    qMot.m03=4
    db.session.add(qMot)#sauve dans la DB
    db.session.commit()
    evaluationA.questionnaireMotivation=True
    evaluationA.fk_QuestionnaireMotivationId=QuestionnaireMotivation.query.order_by(QuestionnaireMotivation.id.desc()).first().id

    print("ok3")
    
    qUX=QuestionnaireUX()
    qUX.u01=2
    qUX.u02=2
    qUX.u03=4
    qUX.u04=2
    qUX.u05=2
    qUX.u06=4
    qUX.u07=2
    qUX.u08=2
    qUX.u09=4
    qUX.u10=2
    qUX.u11=2
    qUX.u12=4
    qUX.u13=2
    qUX.u14=2
    qUX.u15=4
    qUX.u16=2
    qUX.u17=2
    qUX.u18=4
    qUX.u19=2
    qUX.u20=2
    qUX.u21=4
    qUX.u22=2
    qUX.u23=2
    qUX.u24=4
    qUX.u25=4
    db.session.add(qUX)#sauve dans la DB
    db.session.commit()
    evaluationA.questionnaireUX=True
    evaluationA.fk_QuestionnaireUXId=QuestionnaireUX.query.order_by(QuestionnaireUX.id.desc()).first().id
    print("ok4")

    qPre=QuestionnairePreTest()
    qPost=QuestionnairePostTest()
    db.session.add(qPre)#sauve dans la DB
    db.session.commit()
    db.session.add(qPost)#sauve dans la DB
    db.session.commit()
    qPre=QuestionnairePreTest.query.order_by(QuestionnairePreTest.id.desc()).first()
    qPost=QuestionnairePostTest.query.order_by(QuestionnairePostTest.id.desc()).first()
    print(qPre)
    print(qPost)
    evaluationA.fk_QuestionnairePreTestId=qPre.id
    evaluationA.fk_QuestionnairePostTestId=qPost.id
    print(evaluationA)
    
    
    

    db.session.add(evaluationA)#sauve dans la DB
    db.session.commit()
    print("ok5")
   


    




    ########REMPLISSAGE FULL POUR DESKAPE

    experimentation=Experimentation.query.filter_by(id=3).first()
    experimentation.etape1=True
    experimentation.etape2=True
    experimentation.etape3=True
    experimentation.etape4=True
    experimentation.etape5=True
    experimentation.etape6=True
    experimentation.etape7=True
    experimentation.etape8=True
    experimentation.etape9=True
    experimentation.etape10=True
    experimentation.etape11=True
    experimentation.etape12=True
    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()

    idJeei=1
    specification=Specification.query.filter_by(id=idJeei).first()
    questionsApprentissage=QuestionApprentissage.query.filter_by(fk_SpecificationId=specification.id).all()
    print("questions")
    print(questionsApprentissage)


    
    participants = Participant.query.filter_by(fk_ExperimentationId=3).all()
    print(participants)
    for participant in participants:
          participant.groupeExperimental=random.choice([True,False])
          db.session.add(participant)#sauve dans la DB
          db.session.commit()
          print(participant)
          evaluation=Evaluation(1,3,participant.id)
          db.session.add(evaluation)#sauve dans la DB
          db.session.commit()
          evaluation = Evaluation.query.filter_by(fk_ParticipantId=participant.id).first()
          print(evaluation)
          evaluation.questionnaireDemographique=True
          evaluation.questionnaireMotivation=True
          evaluation.postTest1=True
          evaluation.preTest=True
          evaluation.questionnaireUX=True
          db.session.add(evaluation)#sauve dans la DB
          db.session.commit()

          #creation et linkage du questionnaire motivation avec eval
          questionnaireMotivation=QuestionnaireMotivation()
          db.session.add(questionnaireMotivation)#sauve dans la DB
          db.session.commit()
          questionnaireMotivation=QuestionnaireMotivation.query.order_by(QuestionnaireMotivation.id.desc()).first()
          evaluation.fk_QuestionnaireMotivationId=questionnaireMotivation.id
          db.session.add(evaluation)#sauve dans la DB
          db.session.commit()


          questionnaireMotivation=QuestionnaireMotivation.query.filter_by(id=evaluation.fk_QuestionnaireMotivationId).first()
          questionnaireMotivation.m01=randint(0,4)
          questionnaireMotivation.m02=randint(0,4)
          questionnaireMotivation.m03=random.choice([0,2,4])
          db.session.add(questionnaireMotivation)#sauve dans la DB
          db.session.commit()

          questionnaireUX=QuestionnaireUX()
          db.session.add(questionnaireUX)#sauve dans la DB
          db.session.commit()
          questionnaireUX=QuestionnaireUX.query.order_by(QuestionnaireUX.id.desc()).first()
          evaluation.fk_QuestionnaireUXId=questionnaireUX.id
          db.session.add(evaluation)#sauve dans la DB
          db.session.commit()


          questionnaireUX=QuestionnaireUX.query.filter_by(id=evaluation.fk_QuestionnaireUXId).first()
          questionnaireUX.u01=randint(0,4)
          questionnaireUX.u02=randint(0,4)
          questionnaireUX.u03=randint(0,4)
          questionnaireUX.u04=randint(0,4)
          questionnaireUX.u05=randint(0,4)
          questionnaireUX.u06=randint(0,4)
          questionnaireUX.u07=randint(0,4)
          questionnaireUX.u08=randint(0,4)
          questionnaireUX.u09=randint(0,4)
          questionnaireUX.u10=randint(0,4)
          questionnaireUX.u11=randint(0,4)
          questionnaireUX.u12=randint(0,4)
          questionnaireUX.u13=randint(0,4)
          questionnaireUX.u14=randint(0,4)
          questionnaireUX.u15=randint(0,4)
          questionnaireUX.u16=randint(0,4)
          questionnaireUX.u17=randint(0,4)
          questionnaireUX.u18=randint(0,4)
          questionnaireUX.u19=randint(0,4)
          questionnaireUX.u20=randint(0,4)
          questionnaireUX.u21=randint(0,4)
          questionnaireUX.u22=randint(0,4)
          questionnaireUX.u23=randint(0,4)
          questionnaireUX.u24=randint(0,4)
          questionnaireUX.u25=randint(0,4)
       
          db.session.add(questionnaireUX)#sauve dans la DB
          db.session.commit()

          questionnairePreTest=QuestionnairePreTest()
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()
          questionnairePreTest=QuestionnairePreTest.query.order_by(QuestionnairePreTest.id.desc()).first()
          evaluation.fk_QuestionnairePreTestId=questionnairePreTest.id
          db.session.add(evaluation)#sauve dans la DB
          db.session.commit()
          #for question in questionsApprentissage:
          questionnairePreTest.pt01=random.choice(["abstention","abstention","abstention",questionsApprentissage[0].solutionCorrecte, questionsApprentissage[0].solutionIncorrecte1, questionsApprentissage[0].solutionIncorrecte2,questionsApprentissage[0].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt02=random.choice(["abstention","abstention","abstention",questionsApprentissage[1].solutionCorrecte, questionsApprentissage[1].solutionIncorrecte1, questionsApprentissage[1].solutionIncorrecte2,questionsApprentissage[1].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt03=random.choice(["abstention","abstention","abstention",questionsApprentissage[2].solutionCorrecte, questionsApprentissage[2].solutionIncorrecte1, questionsApprentissage[2].solutionIncorrecte2,questionsApprentissage[2].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt04=random.choice(["abstention","abstention","abstention",questionsApprentissage[3].solutionCorrecte, questionsApprentissage[3].solutionIncorrecte1, questionsApprentissage[3].solutionIncorrecte2,questionsApprentissage[3].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt05=random.choice(["abstention","abstention","abstention",questionsApprentissage[4].solutionCorrecte, questionsApprentissage[4].solutionIncorrecte1, questionsApprentissage[4].solutionIncorrecte2,questionsApprentissage[4].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt06=random.choice(["abstention","abstention","abstention",questionsApprentissage[5].solutionCorrecte, questionsApprentissage[5].solutionIncorrecte1, questionsApprentissage[5].solutionIncorrecte2,questionsApprentissage[5].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt07=random.choice(["abstention","abstention","abstention",questionsApprentissage[6].solutionCorrecte, questionsApprentissage[6].solutionIncorrecte1, questionsApprentissage[6].solutionIncorrecte2,questionsApprentissage[6].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt08=random.choice(["abstention","abstention","abstention",questionsApprentissage[7].solutionCorrecte, questionsApprentissage[7].solutionIncorrecte1, questionsApprentissage[7].solutionIncorrecte2,questionsApprentissage[7].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt09=random.choice(["abstention","abstention","abstention",questionsApprentissage[8].solutionCorrecte, questionsApprentissage[8].solutionIncorrecte1, questionsApprentissage[8].solutionIncorrecte2,questionsApprentissage[8].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()

          questionnairePreTest.pt10=random.choice(["abstention","abstention","abstention",questionsApprentissage[9].solutionCorrecte, questionsApprentissage[9].solutionIncorrecte1, questionsApprentissage[9].solutionIncorrecte2,questionsApprentissage[9].solutionIncorrecte3])
          db.session.add(questionnairePreTest)#sauve dans la DB
          db.session.commit()


          ###idem pour post test

          questionnairePostTest=QuestionnairePostTest()
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()
          questionnairePostTest=QuestionnairePostTest.query.order_by(QuestionnairePostTest.id.desc()).first()
          evaluation.fk_QuestionnairePostTestId=questionnairePostTest.id
          db.session.add(evaluation)#sauve dans la DB
          db.session.commit()
          #for question in questionsApprentissage:
          questionnairePostTest.pt01=random.choice(["abstention","abstention",questionsApprentissage[0].solutionCorrecte, questionsApprentissage[0].solutionCorrecte,questionsApprentissage[0].solutionCorrecte,questionsApprentissage[0].solutionCorrecte,questionsApprentissage[0].solutionIncorrecte1, questionsApprentissage[0].solutionIncorrecte2,questionsApprentissage[0].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt02=random.choice(["abstention","abstention",questionsApprentissage[1].solutionCorrecte, questionsApprentissage[1].solutionCorrecte, questionsApprentissage[1].solutionCorrecte, questionsApprentissage[1].solutionCorrecte, questionsApprentissage[1].solutionCorrecte, questionsApprentissage[1].solutionIncorrecte1, questionsApprentissage[1].solutionIncorrecte2,questionsApprentissage[1].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt03=random.choice(["abstention","abstention",questionsApprentissage[2].solutionCorrecte, questionsApprentissage[2].solutionCorrecte, questionsApprentissage[2].solutionCorrecte, questionsApprentissage[2].solutionCorrecte, questionsApprentissage[2].solutionCorrecte, questionsApprentissage[2].solutionIncorrecte1, questionsApprentissage[2].solutionIncorrecte2,questionsApprentissage[2].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt04=random.choice(["abstention","abstention",questionsApprentissage[3].solutionCorrecte, questionsApprentissage[3].solutionIncorrecte1, questionsApprentissage[3].solutionIncorrecte2,questionsApprentissage[3].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt05=random.choice(["abstention","abstention",questionsApprentissage[4].solutionCorrecte, questionsApprentissage[4].solutionIncorrecte1, questionsApprentissage[4].solutionIncorrecte2,questionsApprentissage[4].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt06=random.choice(["abstention","abstention",questionsApprentissage[5].solutionCorrecte, questionsApprentissage[5].solutionIncorrecte1, questionsApprentissage[5].solutionIncorrecte2,questionsApprentissage[5].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt07=random.choice(["abstention","abstention",questionsApprentissage[6].solutionCorrecte, questionsApprentissage[6].solutionCorrecte, questionsApprentissage[6].solutionCorrecte, questionsApprentissage[6].solutionCorrecte, questionsApprentissage[6].solutionCorrecte, questionsApprentissage[6].solutionIncorrecte1, questionsApprentissage[6].solutionIncorrecte2,questionsApprentissage[6].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt08=random.choice(["abstention","abstention",questionsApprentissage[7].solutionCorrecte, questionsApprentissage[7].solutionCorrecte, questionsApprentissage[7].solutionCorrecte, questionsApprentissage[7].solutionCorrecte, questionsApprentissage[7].solutionCorrecte, questionsApprentissage[7].solutionCorrecte, questionsApprentissage[7].solutionIncorrecte1, questionsApprentissage[7].solutionIncorrecte2,questionsApprentissage[7].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt09=random.choice(["abstention","abstention",questionsApprentissage[8].solutionCorrecte, questionsApprentissage[8].solutionCorrecte,questionsApprentissage[8].solutionCorrecte,questionsApprentissage[8].solutionCorrecte,questionsApprentissage[8].solutionCorrecte,questionsApprentissage[8].solutionCorrecte,questionsApprentissage[8].solutionCorrecte,questionsApprentissage[8].solutionIncorrecte1, questionsApprentissage[8].solutionIncorrecte2,questionsApprentissage[8].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()

          questionnairePostTest.pt10=random.choice(["abstention","abstention",questionsApprentissage[9].solutionCorrecte,questionsApprentissage[9].solutionCorrecte, questionsApprentissage[9].solutionCorrecte, questionsApprentissage[9].solutionCorrecte,  questionsApprentissage[9].solutionIncorrecte1, questionsApprentissage[9].solutionIncorrecte2,questionsApprentissage[9].solutionIncorrecte3])
          db.session.add(questionnairePostTest)#sauve dans la DB
          db.session.commit()



          

          




#lancement de la fonction
#function_lancementDBFictive()