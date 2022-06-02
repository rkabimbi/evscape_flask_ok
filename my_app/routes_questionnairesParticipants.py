##########################################################
#mes imports
##########################################################

from ntpath import join
from turtle import pos
from my_app import app
from flask import Flask, redirect
from flask import request
from flask import render_template
from jinja2 import Template
from jinja2 import Environment, PackageLoader
from jinja2 import environment
from random import randint, shuffle
import math

from my_app import db
from my_app.models.experimentation import Experimentation
from my_app.models.jeei_package.questionApprentissage import QuestionApprentissage
from my_app.models.participant import Participant, Sexe, ExperienceJeei, Localisation, Experience  #import de la db

from my_app.models.user import User

from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from flask import json, jsonify
import random
from my_app.models.jeei_package.specification import PublicCible



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()

from my_app.models.jeei_package.jeei import Jeei
from my_app.models.jeei_package.specification import Specification, Statut, Theme, PublicCible
from my_app.models.jeei_package.jointureJeeiUser import JointureJeeiUser
from my_app.models.evaluation import Evaluation
from my_app.models.questionnaireMotivation import QuestionnaireMotivation
from my_app.models.questionnaireUX import QuestionnaireUX, Benchmark
from my_app.models.questionnairePreTest import QuestionnairePreTest
from my_app.models.questionnairePostTest import QuestionnairePostTest





""" 
@app.route("/questionnaireParticipantsUX", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsUX():
    nomJEEI="Deskape"
    return render_template("frontend_etudiant/questionnaireParticipantsUX.html",currentUser=current_user,nomJEEI=nomJEEI)
"""


@app.route("/questionnaireParticipantsMotivation/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsMotivation(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        nomJEEI=jeei.nom
        return render_template("frontend_etudiant/questionnaireParticipantsMotivation.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation)
    else:
       return render_template("frontend_etudiant/noaccess.html")


@app.route("/sauvegardeQuestionnaireMotivation/<int:IdExperimentation>/<int:IdParticipant>", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnaireMotivation(IdExperimentation,IdParticipant):
    print("sauvegardeQuestionnaireMotivation")
    #on va parametrer l'evaluation (à ce stade pas encore fait car on ne sait pas si l'utilisateur va vrmt evaluer le JEEI)
    #pour les autres formulaire il faudra juste recuperer l'eval (ici on la crée)
    participant=Participant.query.filter_by(id=IdParticipant).first()
    experimentation=Experimentation.query.filter_by(id=IdExperimentation).first()
    idJeei=experimentation.fk_JeeiId

    #je lui cree une evaluation
    evaluation=Evaluation.query.filter_by(fk_ParticipantId=participant.id).first()
    evaluation.questionnaireMotivation=True
    
    db.session.add(evaluation)
    db.session.commit()

    #je cree une instance de la clase questionnaire motivation
    questionnaireMotivation=QuestionnaireMotivation()
    print(request.args.get("likertm01"))
    questionnaireMotivation.m01=request.args.get("likertm01")
    print(request.args.get("likertm02"))
    questionnaireMotivation.m02=request.args.get("likertm02")
    print(request.args.get("likertm03"))
    questionnaireMotivation.m03=request.args.get("likertm03")
    
    db.session.add(questionnaireMotivation)
    db.session.commit()


    #je recupere le questionnaire que je viens de cree
    idQuestionnaire = QuestionnaireMotivation.query.order_by(QuestionnaireMotivation.id.desc()).first().id
    #j'assigne son id à l'évaluation pr creer du lien entre l'évaluation et le questionnaire concerné
    evaluation.fk_QuestionnaireMotivationId=idQuestionnaire
    db.session.add(evaluation)
    db.session.commit()

    return render_template("frontend_etudiant/remerciements.html")




  



@app.route("/questionnaireParticipantsDemographique/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsDemographique(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        nomJEEI=jeei.nom
        return render_template("frontend_etudiant/questionnaireParticipantsDemographique.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation,sexes=Sexe,localisations=Localisation, experiences=Experience, experiencesJeei=ExperienceJeei,etudes=PublicCible)
    else:
       return render_template("frontend_etudiant/noaccess.html")


@app.route("/sauvegardeQuestionnaireDemographique", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnaireDemographique():
    print("sauvegardeQuestionnaireDemographique")
    idParticipant= request.args.get("idParticipant")
    participant = Participant.query.filter_by(id=idParticipant).first()

    #je recupere l'évaluation liée
    evaluation=Evaluation.query.filter_by(fk_ParticipantId=participant.id).first()
    evaluation.questionnaireDemographique=True
    db.session.add(evaluation)
    db.session.commit()


    participant.age=request.args.get("age")
    participant.sexe=request.args.get("sexe")
    participant.localisation= request.args.get("localisation")
    participant.experience=request.args.get("experience")
    participant.expJEEI=request.args.get("experienceJeei")
    participant.etudes=request.args.get("etude")
    db.session.add(participant)
    db.session.commit()
    return "ok"

@app.route("/remerciements", methods=['GET', 'POST'])
def fonction_remerciements():
    return render_template("frontend_etudiant/remerciements.html")

@app.route("/noaccess", methods=['GET', 'POST'])
def fonction_noaccess():
    return render_template("frontend_etudiant/noaccess.html")





@app.route("/questionnaireParticipantsUX/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsUX(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        
        return render_template("frontend_etudiant/questionnaireParticipantsUX.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation,benchmarks=Benchmark)
    else:
       return render_template("frontend_etudiant/noaccess.html")


@app.route("/sauvegardeQuestionnaireUX/<int:IdExperimentation>/<int:IdParticipant>", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnaireUX(IdExperimentation,IdParticipant):
    print("sauvegardeQuestionnaireUX")

    participant=Participant.query.filter_by(id=IdParticipant).first()
    experimentation=Experimentation.query.filter_by(id=IdExperimentation).first()
    idJeei=experimentation.fk_JeeiId

    #on va chercher l'evaluation
    evaluation=Evaluation.query.filter_by(fk_ParticipantId=participant.id).first()
    print("//////////////////////////////////////////////////")
    print(evaluation)
    print("//////////////////////////////////////////////////")
    evaluation.questionnaireUX=True
    db.session.add(evaluation)
    db.session.commit()


    #je cree une instance de la clase questionnaire UX
    questionnaireUX=QuestionnaireUX()
    db.session.add(questionnaireUX)
    db.session.commit()

    #link evaluation et questionnaire UX
    questionnaireUx = QuestionnaireUX.query.order_by(QuestionnaireUX.id.desc()).first()
    evaluation=Evaluation.query.filter_by(fk_ParticipantId=participant.id).first()
    evaluation.fk_QuestionnaireUXId=questionnaireUx.id
    db.session.add(evaluation)
    db.session.commit()

   
    
    questionnaireUX.u01=request.args.get("likertu01")
    
    questionnaireUX.u02=request.args.get("likertu02")
   
    questionnaireUX.u03=request.args.get("likertu03")

    questionnaireUX.u04=request.args.get("likertu04")

    questionnaireUX.u05=request.args.get("likertu05")

    questionnaireUX.u06=request.args.get("likertu06")

    questionnaireUX.u07=request.args.get("likertu07")

    questionnaireUX.u08=request.args.get("likertu08")

    questionnaireUX.u09=request.args.get("likertu09")

    questionnaireUX.u10=request.args.get("likertu10")

    questionnaireUX.u11=request.args.get("likertu11")

    questionnaireUX.u12=request.args.get("likertu12")

    questionnaireUX.u13=request.args.get("likertu13")

    questionnaireUX.u14=request.args.get("likertu14")

    questionnaireUX.u15=request.args.get("likertu15")

    questionnaireUX.u16=request.args.get("likertu16")

    questionnaireUX.u17=request.args.get("likertu17")

    questionnaireUX.u18=request.args.get("likertu18")

    questionnaireUX.u19=request.args.get("likertu19")

    questionnaireUX.u20=request.args.get("likertu20")

    questionnaireUX.u21=request.args.get("likertu21")

    questionnaireUX.u22=request.args.get("likertu22")

    questionnaireUX.u23=request.args.get("likertu23")

    questionnaireUX.u24=request.args.get("likertu24")

    questionnaireUX.u25=request.args.get("likertu25")


    
    db.session.add(questionnaireUX)
    db.session.commit()


    #je recupere le questionnaire que je viens de cree
    questionnaire = QuestionnaireUX.query.order_by(QuestionnaireUX.id.desc()).first()
    #j'assigne son id à l'évaluation pr creer du lien entre l'évaluation et le questionnaire concerné
    evaluation.fk_QuestionnaireUXId=questionnaire.id  
    db.session.add(evaluation)
    db.session.commit()





    return render_template("frontend_etudiant/remerciements.html")



@app.route("/questionnaireParticipantsPreTest/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsPreTest(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        nomJEEI=jeei.nom
        #je vais chercher la liste de questions à envoyer
        specificationId =jeei.fk_SpecificationId
        questionsApprentissage = QuestionApprentissage.query.filter_by(fk_SpecificationId=specificationId).all()
        #on va recup les propositions de chaque questions d'apprentissage et les mettre dans un ordre aleatoire
        dictQuestionsApprentissage={
            "id":[],
            "question":[],
            "reponses":[]
        }
        for questionApprentissage in questionsApprentissage:
            tabQuestionApprentissage=[]
            tabQuestionApprentissage.append(questionApprentissage.solutionCorrecte)
            tabQuestionApprentissage.append(questionApprentissage.solutionIncorrecte1)
            tabQuestionApprentissage.append(questionApprentissage.solutionIncorrecte2)
            tabQuestionApprentissage.append(questionApprentissage.solutionIncorrecte3)
            print("Tab avant melnage")
            print(tabQuestionApprentissage)
            print("Tab apres melnage")
            shuffle(tabQuestionApprentissage)
            print(tabQuestionApprentissage)
            dictQuestionsApprentissage["id"].append(questionApprentissage.id)
            dictQuestionsApprentissage["question"].append(questionApprentissage.question)
            dictQuestionsApprentissage["reponses"].append(tabQuestionApprentissage)

        print(dictQuestionsApprentissage)
        return render_template("frontend_etudiant/questionnaireParticipantsPreTest.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation,questionsApprentissage=dictQuestionsApprentissage)
    else:
       return render_template("frontend_etudiant/noaccess.html")


@app.route("/sauvegardeQuestionnairePreTest", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnairePreTest():
    print("sauvegardeQuestionnairePreTest")
    idParticipant= request.args.get("idParticipant")
    participant = Participant.query.filter_by(id=idParticipant).first()

    #je recupere l'évaluation liée
    evaluation=Evaluation.query.filter_by(fk_ParticipantId=participant.id).first()
    evaluation.preTest=True
    db.session.add(evaluation)
    db.session.commit()

    #je cree une instance de la clase questionnaire PreTest
    questionnairePreTest=QuestionnairePreTest()
    db.session.add(questionnairePreTest)
    db.session.commit()

    #link evaluation et questionnaire UX
    questionnaire = QuestionnairePreTest.query.order_by(QuestionnairePreTest.id.desc()).first()
    evaluation.fk_QuestionnairePreTestId=questionnaire.id
    db.session.add(evaluation)
    db.session.commit()

    questionnairePreTest.pt01=request.args.get("responseQ1")
    questionnairePreTest.pt02=request.args.get("responseQ2")
    questionnairePreTest.pt03=request.args.get("responseQ3")
    questionnairePreTest.pt04=request.args.get("responseQ4")
    questionnairePreTest.pt05=request.args.get("responseQ5")
    questionnairePreTest.pt06=request.args.get("responseQ6")
    questionnairePreTest.pt07=request.args.get("responseQ7")
    questionnairePreTest.pt08=request.args.get("responseQ8")
    questionnairePreTest.pt09=request.args.get("responseQ9")
    questionnairePreTest.pt10=request.args.get("responseQ10")
    
    
    db.session.add(questionnairePreTest)
    db.session.commit()
    return "ok"




@app.route("/questionnaireParticipantsPostTest/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsPostTest(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        nomJEEI=jeei.nom
        #je vais chercher la liste de questions à envoyer
        specificationId =jeei.fk_SpecificationId
        questionsApprentissage = QuestionApprentissage.query.filter_by(fk_SpecificationId=specificationId).all()
        #on va recup les propositions de chaque questions d'apprentissage et les mettre dans un ordre aleatoire
        dictQuestionsApprentissage={
            "id":[],
            "question":[],
            "reponses":[]
        }
        for questionApprentissage in questionsApprentissage:
            tabQuestionApprentissage=[]
            tabQuestionApprentissage.append(questionApprentissage.solutionCorrecte)
            tabQuestionApprentissage.append(questionApprentissage.solutionIncorrecte1)
            tabQuestionApprentissage.append(questionApprentissage.solutionIncorrecte2)
            tabQuestionApprentissage.append(questionApprentissage.solutionIncorrecte3)
            print("Tab avant melnage")
            print(tabQuestionApprentissage)
            print("Tab apres melnage")
            shuffle(tabQuestionApprentissage)
            print(tabQuestionApprentissage)
            dictQuestionsApprentissage["id"].append(questionApprentissage.id)
            dictQuestionsApprentissage["question"].append(questionApprentissage.question)
            dictQuestionsApprentissage["reponses"].append(tabQuestionApprentissage)

        print(dictQuestionsApprentissage)
        return render_template("frontend_etudiant/questionnaireParticipantsPostTest.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation,questionsApprentissage=dictQuestionsApprentissage)
    else:
       return render_template("frontend_etudiant/noaccess.html")


@app.route("/sauvegardeQuestionnairePostTest", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnairePostTest():
    print("sauvegardeQuestionnairePostTest")
    idParticipant= request.args.get("idParticipant")
    participant = Participant.query.filter_by(id=idParticipant).first()

    #je recupere l'évaluation liée
    evaluation=Evaluation.query.filter_by(fk_ParticipantId=participant.id).first()
    evaluation.postTest1=True
    db.session.add(evaluation)
    db.session.commit()

    #je cree une instance de la clase questionnaire PreTest
    questionnairePostTest=QuestionnairePostTest()
    db.session.add(questionnairePostTest)
    db.session.commit()

    #link evaluation et questionnaire UX
    questionnaire = QuestionnairePostTest.query.order_by(QuestionnairePostTest.id.desc()).first()
    evaluation.fk_QuestionnairePostTestId=questionnaire.id
    db.session.add(evaluation)
    db.session.commit()

    questionnairePostTest.pt01=request.args.get("responseQ1")
    questionnairePostTest.pt02=request.args.get("responseQ2")
    questionnairePostTest.pt03=request.args.get("responseQ3")
    questionnairePostTest.pt04=request.args.get("responseQ4")
    questionnairePostTest.pt05=request.args.get("responseQ5")
    questionnairePostTest.pt06=request.args.get("responseQ6")
    questionnairePostTest.pt07=request.args.get("responseQ7")
    questionnairePostTest.pt08=request.args.get("responseQ8")
    questionnairePostTest.pt09=request.args.get("responseQ9")
    questionnairePostTest.pt10=request.args.get("responseQ10")
    
    
    db.session.add(questionnairePostTest)
    db.session.commit()
    return "ok"
