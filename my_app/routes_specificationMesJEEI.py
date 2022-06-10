##########################################################
#mes imports
##########################################################

from decimal import DivisionByZero
from turtle import pos
from my_app import app
from flask import Flask, redirect
from flask import request
from flask import render_template
from jinja2 import Template
from jinja2 import Environment, PackageLoader
from jinja2 import environment
from random import randint
import math
import os
from my_app import db #import de la db

from my_app.models.user import User

from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from flask import json, jsonify
from datetime import date

#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()
from my_app.models.jeei_package.jeei import Jeei
from my_app.models.jeei_package.specification import Specification, Statut, Theme, PublicCible
from my_app.models.upload_file import allowed_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
from my_app.models.jeei_package.questionApprentissage import QuestionApprentissage
from my_app.models.jeei_package.jointureJeeiUser import JointureJeeiUser
from random import choice, randint
from my_app.models.experimentation import Experimentation
from my_app.models.participant import Participant, pwd, alphabet_min,alphabet_maj,chiffres,caracteres_speciaux
from my_app.models.evaluation import Evaluation

from my_app.models.questionnaireMotivation import QuestionnaireMotivation
from my_app.models.questionnairePostTest import QuestionnairePostTest
from my_app.models.questionnairePreTest import QuestionnairePreTest
from my_app.models.questionnaireUX import QuestionnaireUX
import sys


@app.route("/specificationMesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_specificationMesJEEI():
    
    
    
    
    print("specificationMesJEEI")


    #recuperation ID qui est communiqué depuis le HTML
    print("id recuperé de HTML :", request.args.get("idJEEI") )
    idJEEIAmodifier = request.args.get("idJEEI")
    monJEEIAEnvoyer=None
    specification=None
    membres=[]
    #pour pouvoir manipuler les données des utilisateurs sur les experimentations qui ne sont donc 
    #pas necessairement celles de l'utilisateur courrant
    users=User.query.all()

    #je fais ca pour obtenir le meme format de reponse quand on passe a une nouvelle ou deja cree ecaluation
    resultatsTem={
            "motivation":0,
            "ux":0,
            "pre":0,
            "post":0,
            "nbrParticipants":0,
            "evolutionApprentissageMoyenne":0
    }
    resultatsExp={
            "motivation":0,
            "ux":0,
            "pre":0,
            "post":0,
            "nbrParticipants":0,
            "evolutionApprentissageMoyenne":0
    }
    resultats=[resultatsTem,resultatsExp]

    infosExperimentations={
        "date":[],
        "id":[],
        "complete":[],
        "prof":[],
        "nbrParticipants":[]
    }
    
    if idJEEIAmodifier: #si un id est renseigné (ca veut dire qu'on a cliqué uncarte et donc on doit aller chercher le JEEI en question)
        #chercher dans DB
        monJEEIAEnvoyer = Jeei.query.filter_by(id=idJEEIAmodifier).first()
        #je vais chercher la spécification liée au JEEI
        specification=Specification.query.filter_by(id=monJEEIAEnvoyer.fk_SpecificationId).first()
        #je vais chercher les question liées à la spécification
        questions=QuestionApprentissage.query.filter_by(fk_SpecificationId=specification.id).all()

        equipe=JointureJeeiUser.query.filter_by(fk_JeeiId=monJEEIAEnvoyer.id).all()
        
        for membre in equipe:
            membreEquipe =User.query.filter_by(id=membre.fk_UserId).first()
            membres.append(membreEquipe)
        print("Tableaux membres----------------------")
        print(membres)

        experimentations = Experimentation.query.filter_by(fk_JeeiId=monJEEIAEnvoyer.id).all()
        calculResultats=False
        for experimentation in experimentations:
            #on va checker si au moins une experimentation est arrivée à l'etape 12
            if experimentation.etape12:
                calculResultats=True
            #on va completer un dict avec tte les informations dont on a besoin pour mettre dans les carte d'experimentation
            infosExperimentations["complete"].append(calculResultats)
            infosExperimentations["date"].append(experimentation.dateEvenement)
        
            infosExperimentations["id"].append(experimentation.id)
            prof=User.query.filter_by(id=experimentation.fk_UserId).first()
            infosExperimentations["prof"].append(prof.lastname+", "+prof.firstname)
            participants=Participant.query.filter_by(fk_ExperimentationId=experimentation.id).all()
            tailleEchantillon=len(participants)
            infosExperimentations["nbrParticipants"].append(tailleEchantillon)

    
        #on ne calcul des resultats que si il y a des experimentations validées (sinon ca fait des divisions par zero)
        if calculResultats:
            resultats=fonction_calculResultats(monJEEIAEnvoyer)
            print(resultats)
        else:
            print("pas d'experimentations évaluées à ce stade!!!!")

        
      


    else: #si pas d'id communiqué ca veut dire qu'on a cliqué le bouton jaune (creer un nouveau)
        #creer un nouveau Specification  qui soit vierge
        specification= Specification(None,None,None,None,None,None,None,None,None,None)
        db.session.add(specification)#sauve dans la DB
        db.session.commit()
        #je recupere le numero d'id de la spécification que je viens de créer
        newSpecificationId=Specification.query.order_by(Specification.id.desc()).first().id
        print("dernier eleent =",newSpecificationId)
        #je creer un JEEI et renseigne à quel specification il est lié (celle que je viens de creer)
        monJEEIAEnvoyer=Jeei(None,None,None,fk_SpecificationId=newSpecificationId,auteurID=current_user.id)
        db.session.add(monJEEIAEnvoyer)#sauve dans la DB
        db.session.commit()
        #je crée 10 test vides
        for q in range(1,11):
            question = QuestionApprentissage(question="Question"+str(q),solutionCorrecte="Reponse"+str(q), solutionIncorrecte1="", solutionIncorrecte2="",solutionIncorrecte3="",explicatif="",fk_SpecificationID=newSpecificationId)
            db.session.add(question)
            db.session.commit()
        newJeeiId=Jeei.query.order_by(Jeei.id.desc()).first().id
        questions = QuestionApprentissage.query.filter_by(fk_SpecificationId=newSpecificationId).all()
        #lier l'utilisateur courant (createur) à ce JEEI via table de jointure
        jointureJeeiUser=JointureJeeiUser( fk_UserId=current_user.id , fk_JeeiId=monJEEIAEnvoyer.id)
        db.session.add(jointureJeeiUser)
        db.session.commit()
        membres.append(current_user)
        print(questions)
        flash("Votre Jeu d'Evasion a été crée [id :"+str(newJeeiId)+ "]. Bonne évaluation!!!", 'success')
        experimentations=None


        
    print(monJEEIAEnvoyer)
    print(specification)
    return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEIAEnvoyer,specificationJEEIRecupere=specification,theme=Theme,publicCible=PublicCible,questions=questions,membres=membres,experimentations=experimentations,users=users,resultats=resultats,infosExperimentations=infosExperimentations)

def fonction_calculResultats(jeei):
    #on va gerer les resultats
        #on recupere  les reponses des questionnaires apprentissage)
        specification=Specification.query.filter_by(id=jeei.fk_SpecificationId).first()
        reponses=QuestionApprentissage.query.filter_by(fk_SpecificationId=specification.id).all()


        #on recupere toutes les experimentations pour lesquelles on est arrivé à l'étape 12 (en lien avec ce jeei)
        experimentations=Experimentation.query.filter_by(fk_JeeiId=jeei.id).all()
        experimentationsRetenues=[]
        for experimentation in experimentations:
            if experimentation.etape12:
                experimentationsRetenues.append(experimentation)
        

        evaluationsRetenues=[]
        #pour chacun de ses experimentations on recupere tte les evaluations où tt est à true
        #on obtient donc l'ensemble des evaluations pour un JEEI (pour toutes les eval)
        for experimentation in experimentationsRetenues:
            #je recupere tt les eval en lien avec les experimentations retenues
            evaluations=Evaluation.query.filter_by(fk_ExperimentationId=experimentation.id).all()
            #je check si les évaluation sont complete ou non et je cree un tableau d'evaluation complete
            for evaluation in evaluations:
                #on recupere chacun des questionnaire liés et pour chacun d'eux on verifie que tout est complété
                #je ne fais pas ca pour les questionnaires pretest et post test car là il peut y avoir abstention
                questionnaireMotivation=QuestionnaireMotivation.query.filter_by(id=evaluation.fk_QuestionnaireMotivationId).first()
                questionnaireUX=QuestionnaireUX.query.filter_by(id=evaluation.fk_QuestionnaireUXId).first()
                participant = Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
                complet=verificationComplet(questionnaireMotivation,questionnaireUX,participant)
                complet2=fonction_verificationCompletComplement2(evaluation)
                if complet and complet2 :
                    #alors on ajoute l'evaluation courrante aux evaluation retenue
                    evaluationsRetenues.append(evaluation)

        #on calcule le resultat
        
        resultatsGroupeExperimental={
            "motivation":0,
            "ux":0,
            "pre":0,
            "post":0,
            "nbrParticipants":0,
            "evolutionApprentissageMoyenne":0
        }

        resultatsGroupeTemoin={
            "motivation":0,
            "ux":0,
            "pre":0,
            "post":0,
            "nbrParticipants":0,
            "evolutionApprentissageMoyenne":0
        }



        nbrMembresGroupeExp=0
        nbrMembresGroupeTem=0
        for evaluation in evaluationsRetenues:
            resultatMotivation=0
            resultatUX=0
            resultatPreTest=0
            resultatPostTest=0
            #motivation
            questionnaireMotivation=QuestionnaireMotivation.query.filter_by(id=evaluation.fk_QuestionnaireMotivationId).first()
            resultatMotivation=resultatMotivation+questionnaireMotivation.m01
            resultatMotivation=resultatMotivation+questionnaireMotivation.m02
            resultatMotivation=resultatMotivation+questionnaireMotivation.m03

            #UX
            questionnaireUX=QuestionnaireUX.query.filter_by(id=evaluation.fk_QuestionnaireUXId).first()
            resultatUX=resultatUX+questionnaireUX.u01
            resultatUX=resultatUX+questionnaireUX.u02
            resultatUX=resultatUX+questionnaireUX.u03
            resultatUX=resultatUX+questionnaireUX.u04
            resultatUX=resultatUX+questionnaireUX.u05
            resultatUX=resultatUX+questionnaireUX.u06
            resultatUX=resultatUX+questionnaireUX.u07
            resultatUX=resultatUX+questionnaireUX.u08
            resultatUX=resultatUX+questionnaireUX.u09
            resultatUX=resultatUX+questionnaireUX.u10
            resultatUX=resultatUX+questionnaireUX.u11
            resultatUX=resultatUX+questionnaireUX.u12
            resultatUX=resultatUX+questionnaireUX.u13
            resultatUX=resultatUX+questionnaireUX.u14
            resultatUX=resultatUX+questionnaireUX.u15
            resultatUX=resultatUX+questionnaireUX.u16
            resultatUX=resultatUX+questionnaireUX.u17
            resultatUX=resultatUX+questionnaireUX.u18
            resultatUX=resultatUX+questionnaireUX.u19
            resultatUX=resultatUX+questionnaireUX.u20
            resultatUX=resultatUX+questionnaireUX.u21
            resultatUX=resultatUX+questionnaireUX.u22
            resultatUX=resultatUX+questionnaireUX.u23
            resultatUX=resultatUX+questionnaireUX.u24
            resultatUX=resultatUX+questionnaireUX.u25

            #PreTest
            preTest=QuestionnairePreTest.query.filter_by(id=evaluation.fk_QuestionnairePreTestId).first()

            if preTest.pt01==reponses[0].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt01==None or preTest.pt01=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10
            
            if preTest.pt02==reponses[1].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt02==None or preTest.pt02=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10

            if preTest.pt03==reponses[2].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt03==None or preTest.pt03=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10            

            if preTest.pt04==reponses[3].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt04==None or preTest.pt04=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10

            if preTest.pt05==reponses[4].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt05==None or preTest.pt05=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10


            if preTest.pt06==reponses[5].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt06==None or preTest.pt06=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10


            if preTest.pt07==reponses[6].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt07==None or preTest.pt07=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10


            if preTest.pt08==reponses[7].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt08==None or preTest.pt08=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10
        
            if preTest.pt09==reponses[8].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt09==None or preTest.pt09=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10

            if preTest.pt10==reponses[9].solutionCorrecte:
                resultatPreTest=resultatPreTest+10
            elif preTest.pt10==None or preTest.pt10=="abstention":
                resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPreTest=resultatPreTest-10
            
            if resultatPreTest<=0:
                resultatPreTest=10

            #PostTest
            postTest=QuestionnairePostTest.query.filter_by(id=evaluation.fk_QuestionnairePostTestId).first()
     
            print(postTest.pt01)
            print(reponses[0])
            if postTest.pt01==reponses[0].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt01==None or postTest.pt01=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10
            
            if postTest.pt02==reponses[1].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt02==None or postTest.pt02=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10



            if postTest.pt03==reponses[2].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt03==None or postTest.pt03=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10            

            if postTest.pt04==reponses[3].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt04==None or postTest.pt04=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10

            if postTest.pt05==reponses[4].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt05==None or postTest.pt05=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10


            if postTest.pt06==reponses[5].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt06==None or postTest.pt06=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10


            if postTest.pt07==reponses[6].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt07==None or postTest.pt07=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10


            if postTest.pt08==reponses[7].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt08==None or postTest.pt08=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10
        
            if postTest.pt09==reponses[8].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt09==None or postTest.pt09=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10

            if postTest.pt10==reponses[9].solutionCorrecte:
                resultatPostTest=resultatPostTest+10
            elif postTest.pt10==None or postTest.pt10=="abstention":
                resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
            else:
                resultatPostTest=resultatPostTest-10
            if resultatPostTest<=0:
                resultatPostTest=10
            
            #on check à quel groupe le participant appartient pour en fonction incrementer ce qu'il faut
            participant = Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
            if participant.groupeExperimental:
                print("--------RESULTATS MEMBRE EXP---------")
                print(resultatMotivation)
                print(resultatUX)
                print(resultatPreTest)
                print(resultatPostTest)
                resultatsGroupeExperimental["motivation"]=resultatsGroupeExperimental["motivation"]+resultatMotivation
                resultatsGroupeExperimental["ux"]=resultatsGroupeExperimental["ux"]+resultatUX
                resultatsGroupeExperimental["pre"]=resultatsGroupeExperimental["pre"]+resultatPreTest
                resultatsGroupeExperimental["post"]=resultatsGroupeExperimental["post"]+resultatPostTest
                nbrMembresGroupeExp=nbrMembresGroupeExp+1
                resultatsGroupeExperimental["evolutionApprentissageMoyenne"]=resultatsGroupeExperimental["evolutionApprentissageMoyenne"]+((resultatPostTest-resultatPreTest)/resultatPreTest)
                
            else:
                print("--------RESULTATS MEMBRE TEM---------")
                print(resultatMotivation)
                print(resultatUX)
                print(resultatPreTest)
                print(resultatPostTest)
                resultatsGroupeTemoin["motivation"]=resultatsGroupeTemoin["motivation"]+resultatMotivation
                resultatsGroupeTemoin["ux"]=resultatsGroupeTemoin["ux"]+resultatUX
                resultatsGroupeTemoin["pre"]=resultatsGroupeTemoin["pre"]+resultatPreTest
                resultatsGroupeTemoin["post"]=resultatsGroupeTemoin["post"]+resultatPostTest
                nbrMembresGroupeTem=nbrMembresGroupeTem+1
                resultatsGroupeTemoin["evolutionApprentissageMoyenne"]=resultatsGroupeTemoin["evolutionApprentissageMoyenne"]+((resultatPostTest-resultatPreTest)/resultatPreTest)


        #Resultats finaux absolus
        print("resultat groupe temoin :",resultatsGroupeTemoin)
        print("resultat groupe exp:",resultatsGroupeExperimental)

        try:
            resultatsGroupeExperimental["evolutionApprentissageMoyenne"]= resultatsGroupeExperimental["evolutionApprentissageMoyenne"]/nbrMembresGroupeExp
        except ZeroDivisionError:
            resultatsGroupeExperimental["evolutionApprentissageMoyenne"]= 0

        try:
            resultatsGroupeTemoin["evolutionApprentissageMoyenne"]=resultatsGroupeTemoin["evolutionApprentissageMoyenne"]/nbrMembresGroupeTem
        except ZeroDivisionError:
            resultatsGroupeTemoin["evolutionApprentissageMoyenne"]=0



        #Resultats finaux relatifs et moyens
        if nbrMembresGroupeExp>0:
            resultatsGroupeExperimental["motivation"]=resultatsGroupeExperimental["motivation"]/(nbrMembresGroupeExp*3*4)
            resultatsGroupeExperimental["ux"]=resultatsGroupeExperimental["ux"]/(nbrMembresGroupeExp*25*4)
            resultatsGroupeExperimental["pre"]=resultatsGroupeExperimental["pre"]/(nbrMembresGroupeExp*10*10)
            resultatsGroupeExperimental["post"]=resultatsGroupeExperimental["post"]/(nbrMembresGroupeExp*10*10)
            resultatsGroupeExperimental["nbrParticipants"]=nbrMembresGroupeExp
        if nbrMembresGroupeTem>0:
            resultatsGroupeTemoin["motivation"]=resultatsGroupeTemoin["motivation"]/(nbrMembresGroupeTem*3*4)
            resultatsGroupeTemoin["ux"]=resultatsGroupeTemoin["ux"]/(nbrMembresGroupeTem*25*4)
            resultatsGroupeTemoin["pre"]=resultatsGroupeTemoin["pre"]/(nbrMembresGroupeTem*10*10)
            resultatsGroupeTemoin["post"]=resultatsGroupeTemoin["post"]/(nbrMembresGroupeTem*10*10)
            resultatsGroupeTemoin["nbrParticipants"]=nbrMembresGroupeTem


        resultats=[resultatsGroupeTemoin,resultatsGroupeExperimental]
        #on doit renvoyer un dictionnaire (voir methode appellante)
        print("resultats absolus")
        print(resultats)

        #A MODIFIER!!!!!! c'est juste pour me permettre de voir ce que ce ca calcule à ce stade avec des print
        return resultats


def verificationComplet(questionnaireMotivation, questionnaireUX,participant):
    if not questionnaireMotivation:#dans le cas où y a un formulaire de motivation
        return False
    else:
        if questionnaireMotivation.m01==None:
            return False
        if questionnaireMotivation.m02==None:
            return False
        if questionnaireMotivation.m03==None:
            return False

    if not questionnaireUX:
        return False
    else:
        if questionnaireUX.u01==None:
            return False
        if questionnaireUX.u02==None:
            return False
        if questionnaireUX.u03==None:
            return False
        if questionnaireUX.u04==None:
            return False
        if questionnaireUX.u05==None:
            return False
        if questionnaireUX.u06==None:
            return False
        if questionnaireUX.u07==None:
            return False
        if questionnaireUX.u08==None:
            return False
        if questionnaireUX.u09==None:
            return False

        if questionnaireUX.u10==None:
            return False
        if questionnaireUX.u11==None:
            return False
        if questionnaireUX.u12==None:
            return False

        if questionnaireUX.u13==None:
            return False
        if questionnaireUX.u14==None:
            return False
        if questionnaireUX.u15==None:
            return False

        if questionnaireUX.u16==None:
            return False
        if questionnaireUX.u17==None:
            return False
        if questionnaireUX.u18==None:
            return False

        if questionnaireUX.u19==None:
            return False
        if questionnaireUX.u20==None:
            return False
        if questionnaireUX.u21==None:
            return False

        if questionnaireUX.u22==None:
            return False
        if questionnaireUX.u23==None:
            return False
        if questionnaireUX.u24==None:
            return False
        if questionnaireUX.u25==None:
            return False

    if not participant:
        return False
    else:
        if participant.sexe==None:
            return False
        if participant.expJEEI==None:
            return False
        if participant.etudes==None:
            return False
        if participant.localisation==None:
            return False
        if participant.experience==None:
            return False
        if not participant.consentement:
            return False

    
    print("evaluation valide entrant en ligne de compte pour le score individuel")
    return True

@app.route("/sauvegardeTableJeei", methods=['GET', 'POST'])
@login_required
def fonction_sauvegardeTableJeei():
    champs = request.args.get("champs")
    valeur= request.args.get("valeur")
    idJEEI= request.args.get("idJEEI")

    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    print("monJEEI : ", monJEEI)
    idSpecification=Jeei.query.filter_by(id=idJEEI).first().fk_SpecificationId
    print("idSpecification :",idSpecification)
    specification=Specification.query.filter_by(id=idSpecification).first()
    print("specification",specification)

    if champs=="nom":
        monJEEI.nom=valeur
        db.session.commit()
    elif champs=="descriptif":
        monJEEI.descriptif=valeur
        db.session.commit()
    #elif champs=="img":
        #monJEEI.img="static/img/"+valeur+".jpeg"
        #db.session.commit()
    elif champs=="nbrJoueursMin":
        print("case nbr joueurs min" )
        specification.nbrJoueursMin= valeur
        db.session.commit()
    elif champs=="nbrJoueursMax":
        print("case nbr joueurs max" )
        specification.nbrJoueursMax= valeur
        db.session.commit()
    elif champs=="budget":
        print("case budget" )
        specification.budget= valeur
        db.session.commit()
    elif champs=="dureeMinutes":
        print("case dureeMinutes" )
        specification.dureeMinutes= valeur
        db.session.commit()
    elif champs=="scenario":
        print("case scenario" )
        specification.scenario= valeur
        db.session.commit()
    elif champs=="chapitre":
        print("case chapitre" )
        specification.chapitre= valeur
        db.session.commit()
    elif champs=="publicCible":
        print("case publicCible" )
        specification.publicCible= valeur
        db.session.commit()
    elif champs=="theme":
        print("case theme" )
        specification.theme= valeur
        db.session.commit()
    
    #pour confirme que tout s'est bien passe côté front
    reponse= jsonify(reponse="ok")
  
    return reponse




@app.route('/uploadPhoto', methods=['GET', 'POST'])#Get et post est important pour tester avec quelle méthode on est arrivé 
#(pour eviter que des gens tapent l'url à la main. S'ils le font on est en mode GET et alors on prévoit dans la méthode qu'on tient pas compte du truc (on recharge la page))
def upload_file( ):

    idJEEI= request.args.get("idJEEI")
    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    specification=Specification.query.filter_by(id=monJEEI.fk_SpecificationId).first()
    questions= QuestionApprentissage.query.filter_by(fk_SpecificationId=specification.id).all()
    if 'file' not in request.files:#si pas de fichier
            #flash('Pas de fichier', 'danger')#flash c'est qqch que flask sait intepreter et donc on peut faire des messages d'erreur
            return redirect('/specificationMesJEEI?idJEEI='+idJEEI)
            #return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,theme=Theme,public=PublicCible,questions=questions,specificationJEEIRecupere=specification)
    file = request.files['file'] #si on est ici c'est qu'il y a un fichier
    if file.filename == '':#si non du fichier est vide
            #flash('Pas de fichier selectionné', 'danger')
            return redirect('/specificationMesJEEI?idJEEI='+idJEEI)
            #return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,theme=Theme,public=PublicCible,questions=questions,specificationJEEIRecupere=specification)

    
    if file and allowed_file(file.filename):#si on a un fichier et que le format est permis
        filename = secure_filename(file.filename)#methode qui evite des attaques où charges des fichiers systeme (elle rajoute des donées au nom)
        print(filename)
        print(monJEEI)
        monJEEI.img="static/img/img"+str(monJEEI.id)+".jpeg" #on sauve l'adresse dans l'attribut image
        db.session.commit()
        nomPhoto="img"+str(monJEEI.id)+".jpeg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomPhoto))#on sauve le fichier

        #print(redirect(request.base_url))
        return redirect('/specificationMesJEEI?idJEEI='+idJEEI)
        #return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,theme=Theme,public=PublicCible,questions=questions,specificationJEEIRecupere=specification)

@app.route('/uploadFilePdf', methods=['GET', 'POST'])#Get et post est important pour tester avec quelle méthode on est arrivé 
#(pour eviter que des gens tapent l'url à la main. S'ils le font on est en mode GET et alors on prévoit dans la méthode qu'on tient pas compte du truc (on recharge la page))
def upload_filePdf( ):
    print("upload_FilePdf")
    idJEEI= request.args.get("idJEEI")
    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    idSpecificationMonJEEI = Jeei.query.filter_by(id=idJEEI).first().fk_SpecificationId
    print("spec :",idSpecificationMonJEEI)
    specificationMonJEEI= Specification.query.filter_by(id=idSpecificationMonJEEI).first()
    print(specificationMonJEEI)
    questions= QuestionApprentissage.query.filter_by(fk_SpecificationId=specificationMonJEEI.id).all()

    #j'ai reussi à recup la spec mnt faut que jl'envoi dans le front...à mon avis du coup.. je dois faire ca pour toute les routes qui rendes specificationMesJEEI.html...à voir

    if 'file' not in request.files:#si pas de fichier
            #flash('Pas de fichier', 'danger')#flash c'est qqch que flask sait intepreter et donc on peut faire des messages d'erreur
            print("erreur - pas de fichier")
            return redirect('/specificationMesJEEI?idJEEI='+idJEEI)
            #return render_template("specificationMesJEEI.html",currentUser=current_user,theme=Theme,public=PublicCible,monJEEIRecupere=monJEEI,questions=questions,specificationJEEIRecupere=specificationMonJEEI)
    file = request.files['file'] #si on est ici c'est qu'il y a un fichier
    if file.filename == '':#si non du fichier est vide
            #flash('Pas de fichier selectionné', 'danger')
            print("erreur - pas de fichier selectionné")
            return redirect('/specificationMesJEEI?idJEEI='+idJEEI)
            #return render_template("specificationMesJEEI.html",currentUser=current_user,theme=Theme,public=PublicCible,monJEEIRecupere=monJEEI,questions=questions,specificationJEEIRecupere=specificationMonJEEI)


    if file and allowed_file(file.filename):#si on a un fichier et que le format est permis
        filename = secure_filename(file.filename)#methode qui evite des attaques où charges des fichiers systeme (elle rajoute des donées au nom)

        print(filename)
        print(monJEEI)
        specificationMonJEEI.documentation="static/img/doc"+str(monJEEI.id)+".pdf" #on sauve l'adresse dans l'attribut image
        db.session.commit()
        nomFichier="doc"+str(monJEEI.id)+".pdf"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomFichier))#on sauve le fichier

        #print(redirect(request.base_url))
        return redirect('/specificationMesJEEI?idJEEI='+idJEEI)

    #return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,specificationJEEIRecupere=specificationMonJEEI,theme=Theme,public=PublicCible,questions=questions)



@app.route("/sauvegardeSpecificationTest", methods=['GET', 'POST'])
@login_required
def fonction_sauvegardeSpecificationTest():
    champs = request.args.get("champs")
    valeur= request.args.get("valeur")
    idTest= request.args.get("idTest")


    question=QuestionApprentissage.query.filter_by(id=idTest).first()
    print("question",question)
    print(champs)
    print(valeur)
    print(idTest)

    if champs=="question":
        question.question=valeur
        db.session.commit()
    if champs=="solution":
        question.solutionCorrecte=valeur
        db.session.commit()
    if champs=="explicatif":
        question.explicatif=valeur
        db.session.commit()
    if champs=="solutionIncorrecte1":
        question.solutionIncorrecte1=valeur
        db.session.commit()
    if champs=="solutionIncorrecte2":
        question.solutionIncorrecte2=valeur
        db.session.commit()
    if champs=="solutionIncorrecte3":
        question.solutionIncorrecte3=valeur
        db.session.commit()

    print("question",question)
    #pour confirme que tout s'est bien passe côté front
    reponse= jsonify(reponse="ok")
  
    return reponse



@app.route("/sauvegardeNouveauMembre", methods=['GET', 'POST'])
@login_required
def fonction_sauvegardeNouveauMembre():
    membreNom=request.args.get("membreNom")
    membreUniversite=request.args.get("membreUniversite")
    membrePrenom=request.args.get("membrePrenom")
    membreEmail=request.args.get("membreEmail")
    idJeei= request.args.get("idJeei")
    reponse="nok"
  
    #on recupere tt les membres de l'équipe à ce stade
    jeei = Jeei.query.filter_by(id=idJeei).first()
    jointuresJeeiUser= JointureJeeiUser.query.filter_by(fk_JeeiId=jeei.id).all()
    print(jointuresJeeiUser)
    existeDeja=False
    #on va verifier si dans les lien entre JEEI et User concernant ce Jeei ci il y a pas qq soit qui a les memes nom soit qui a la meme adresse -->si c'est le cas on ajoute pas (reponse reste "nok")
    for assignation in jointuresJeeiUser:
        membre=assignation.fk_UserId
        
        user = User.query.filter_by(id=membre).first()
        print(user)
        if user.email.lower() == membreEmail.lower() or (user.lastname.lower()==membreNom.lower() and user.firstname.lower()==membrePrenom.lower() and user.universite.lower() == membreUniversite.lower()):
            existeDeja=True
            print("EXISTE DEJA !!!!!!")


    if not existeDeja:
        new_user = User(username=str(membreNom+membrePrenom),firstname=membrePrenom, lastname=membreNom,password=pwd(10,True,True,True,True),email=membreEmail,titre="",universite=membreUniversite)#crée l'utilisateur (je n'utilise pas de constructeur . je trouce cela plus clair comme ceci
        print('utilisateur sauvé!!!!!!!')
        print(new_user)
        db.session.add(new_user)#sauve dans la DB
        db.session.commit()
        newMembreId= User.query.order_by(User.id.desc()).first().id
        jointureJeeiUser = JointureJeeiUser( fk_UserId=newMembreId , fk_JeeiId=idJeei)
        db.session.add(jointureJeeiUser)#sauve dans la DB
        db.session.commit()
        membreARenvoyer=User.query.filter_by(id=newMembreId).first()
        objJson={
            "nom": membreARenvoyer.lastname,
            "prenom":membreARenvoyer.firstname ,
            "email":membreARenvoyer.email ,
            "universite":membreARenvoyer.universite,
            "id":membreARenvoyer.id

        }
 
        reponse= jsonify(reponse=objJson)
  
    return reponse










@app.route("/validerJEEI", methods=['GET', 'POST'])
@login_required
def fonction_validerJEEI():
    idJEEI=request.args.get("idJeei")
    jeei = Jeei.query.filter_by(id=idJEEI).first()
    jeei.estValide=True
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    return "ok"



def fonction_verificationCompletComplement2(evaluation):
    if not evaluation.questionnaireDemographique:
        return False
    if not evaluation.questionnaireMotivation:
        return False
    print(evaluation)
    print("eval pretest")
    print(evaluation.preTest)
    if not evaluation.preTest:
        return False
    if not evaluation.postTest1:
        return False
    if not evaluation.questionnaireUX:
        return False
    else :
        return True
