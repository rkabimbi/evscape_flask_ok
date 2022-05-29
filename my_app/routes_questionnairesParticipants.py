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
from my_app.models.participant import Participant, Sexe #import de la db

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





@app.route("/questionnaireParticipantsUX", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsUX():
    nomJEEI="Deskape"
    return render_template("frontend_etudiant/questionnaireParticipantsUX.html",currentUser=current_user,nomJEEI=nomJEEI)



@app.route("/questionnaireParticipantsMotivation", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsMotivation():
    nomJEEI="Deskape"
    return render_template("frontend_etudiant/questionnaireParticipantsMotivation.html",currentUser=current_user,nomJEEI=nomJEEI)


@app.route("/questionnaireParticipantsDemographique/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_questionnaireParticipantsDemographique(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        nomJEEI=jeei.nom
        return render_template("frontend_etudiant/questionnaireParticipantsDemographique.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation,sexes=Sexe)
    else:
       return render_template("user_login.html")


@app.route("/sauvegardeQuestionnaireDemographique", methods=['GET', 'POST'])
def fonction_sauvegardeQuestionnaireDemographique():
    print("sauvegardeQuestionnaireDemographique")
    idParticipant= request.args.get("idParticipant")
    participant = Participant.query.filter_by(id=idParticipant).first()
    participant.age=request.args.get("age")
    participant.sexe=request.args.get("sexe")
    db.session.add(participant)
    db.session.commit()
    return render_template("frontend_etudiant/remerciements.html")

