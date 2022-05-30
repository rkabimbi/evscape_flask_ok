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
from random import randint
import math

from my_app import db
from my_app.models.experimentation import Experimentation
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



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()

from my_app.models.jeei_package.jeei import Jeei
from my_app.models.jeei_package.specification import Specification, Statut, Theme, PublicCible
from my_app.models.jeei_package.jointureJeeiUser import JointureJeeiUser
from my_app.models.evaluation import Evaluation
from my_app.models.questionnaireMotivation import QuestionnaireMotivation





@app.route("/questionnaireParticipantsUX", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsUX():
    nomJEEI="Deskape"
    return render_template("frontend_etudiant/questionnaireParticipantsUX.html",currentUser=current_user,nomJEEI=nomJEEI)



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
       return render_template("user_login.html")


@app.route("/sauvegardeQuestionnaireMotivation/<int:IdExperimentation>/<int:IdParticipant>", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnaireMotivation(IdExperimentation,IdParticipant):
    print("sauvegardeQuestionnaireMotivation")
    #on va parametrer l'evaluation (à ce stade pas encore fait car on ne sait pas si l'utilisateur va vrmt evaluer le JEEI)
    #pour les autres formulaire il faudra juste recuperer l'eval (ici on la crée)
    participant=Participant.query.filter_by(id=IdParticipant).first()
    experimentation=Experimentation.query.filter_by(id=IdExperimentation).first()
    idJeei=experimentation.fk_JeeiId

    #je lui cree une evaluation
    evaluation=Evaluation(idJeei,experimentation.id,participant.id)
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
    return render_template("frontend_etudiant/remerciements.html")




  



@app.route("/questionnaireParticipantsDemographique/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsDemographique(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        nomJEEI=jeei.nom
        return render_template("frontend_etudiant/questionnaireParticipantsDemographique.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation,sexes=Sexe,localisations=Localisation, experiences=Experience, experiencesJeei=ExperienceJeei)
    else:
       return render_template("user_login.html")


@app.route("/sauvegardeQuestionnaireDemographique", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnaireDemographique():
    print("sauvegardeQuestionnaireDemographique")
    idParticipant= request.args.get("idParticipant")
    participant = Participant.query.filter_by(id=idParticipant).first()
    participant.age=request.args.get("age")
    participant.sexe=request.args.get("sexe")
    participant.localisation= request.args.get("localisation")
    participant.experience=request.args.get("experience")
    participant.expJeei=request.args.get("experienceJeei")
    db.session.add(participant)
    db.session.commit()
    return "ok"

@app.route("/remerciements", methods=['GET', 'POST'])
def fonction_remerciements():
    return render_template("frontend_etudiant/remerciements.html")
