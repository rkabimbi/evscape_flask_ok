##########################################################
#mes imports
##########################################################

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
from my_app.models.experimentation import Experimentation #import de la db

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
from my_app.models.evaluation import Evaluation
from my_app.models.participant import Participant





@app.route("/mesExperimentations", methods=['GET', 'POST'])
@login_required
def fonction_mesExperimentations():
    user=current_user
    mesExperimentations=Experimentation.query.filter_by(fk_UserId=user.id).all()
    #je vais construire un disctionnaire pq?
    # ici je renvoi un sous tableau de tous les JEEI donc les id ne corrspondront pas
    # aux id des JEEI dans l'objet experimentation
    #je vais donc fournir un dictionnaire qui garanti le bon mapping entre les choses
    experimentationsTabDeDict=[]
    for experimentation in mesExperimentations:
        jeeiExperimente = Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
        specificationJeeiExperimente = Specification.query.filter_by(id=jeeiExperimente.fk_SpecificationId).first()

        compteurParticipantConsentant=0
        participants=Participant.query.filter_by(fk_ExperimentationId=experimentation.id).all()
        for participant in participants:
            if participant.consentement:
                compteurParticipantConsentant=compteurParticipantConsentant+1

        experimentationDict={
            #tous les id ici me permettront de passer aux routes l'id afin qu'ils puissent savoir de quoi
            #il s'agit et rebalancer de l'info
            "idExperimentation": experimentation.id,
            "idJeei":experimentation.fk_JeeiId,
            "idSpecification":jeeiExperimente.fk_SpecificationId,
            "nom":jeeiExperimente.nom,
            "publicCible":specificationJeeiExperimente.publicCible,
            "theme":specificationJeeiExperimente.theme,
            "chapitre":specificationJeeiExperimente.chapitre,
            "participants":compteurParticipantConsentant,
            "dateEvenement":experimentation.dateEvenement,
            "statut": experimentation.etape12
        }

        experimentationsTabDeDict.append(experimentationDict) 

    
    print(experimentationsTabDeDict)
    return render_template("mesExperimentations.html",currentUser=current_user,  mesExperimentations=experimentationsTabDeDict)

   