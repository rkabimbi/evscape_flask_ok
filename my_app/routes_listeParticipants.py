
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
from my_app import db
from my_app.models.participant import Participant #import de la db

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
from my_app.models.participant import Participant
import time
from flask_mail import Mail, Message


app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '2a505d7be718ed'
app.config['MAIL_PASSWORD'] = '37960d02bef471'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail=Mail(app)







@app.route("/listeParticipants", methods=['GET', 'POST'])
@login_required
def fonction_listeParticipants():
    print("fonction_listeParticipants")
    idJEEIaEnvoyer = request.args.get("idJEEI")
    
    #pour chercher la bonne experimentation liée au JEEI
    idExperimentation = request.args.get("idExperimentation")
 
    JEEIAEnvoyer = Jeei.query.filter_by(id=idJEEIaEnvoyer).first()
    specificationAEnvoyer = Specification.query.filter_by(id=JEEIAEnvoyer.fk_SpecificationId).first()
    
    experimentation=Experimentation.query.filter_by(id=idExperimentation).first()
    participants=Participant.query.filter_by(fk_ExperimentationId=experimentation.id).all()
    print(participants)
    
    return render_template("listeParticipants.html",currentUser=current_user,JEEI=JEEIAEnvoyer,specification=specificationAEnvoyer,experimentation=experimentation,participants=participants,nbrParticipants=len(participants))


@app.route("/ajouterParticipant", methods=['GET', 'POST'])
@login_required
def fonction_ajouterParticipant():
    print("Fonction ajouterParticipant")
    idExperimentation = request.args.get("experimentationId")
    participantNom = request.args.get("participantNom")
    participantEmail = request.args.get("participantEmail")
    participantPrenom = request.args.get("participantPrenom")
    
  
    
    participant=Participant()
    participant.email=participantEmail
    participant.fk_ExperimentationId=idExperimentation
    participant.nom=participantNom
    participant.prenom=participantPrenom
    participant.consentement=False
 

    db.session.add(participant)#sauve dans la DB
    db.session.commit()

    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
    nbrParticipants = len(participants)

    participantJzonizable={
        'nom': participant.nom,
        'prenom':participant.prenom,
        'email': participant.email ,
        'consentement':participant.consentement
    }


    reponse= jsonify(reponse=participantJzonizable,nbrParticipants=nbrParticipants)
    print(reponse)

    return reponse


@app.route("/validerListeParticipants", methods=['GET', 'POST'])
@login_required
def fonction_validerListeParticipants():
    print("Fonction validerListeParticipants")
    experimentationId = request.args.get("experimentationId")

    experimentation=Experimentation.query.filter_by(id=experimentationId).first()
    experimentation.etape1=True
    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()

    #on envoi des emails à tous les participants pour demander le consentement

   
    participants=Participant.query.filter_by(fk_ExperimentationId=experimentationId).all()

    print(participants)


    jeei = Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
  

    
    for participant in participants:

            time.sleep(0.4)#je met un time de 5 secondes sinon python envoi plus de 3 emails par seconde et alors mailtrap ne suis pas et ca renvoi une erreur 500
            msg = Message((jeei.nom,' : Consentement'), sender = ( 'Equipe EvscApp' ,'rudy.kabimbingoy@teams.student.unamur.be'), recipients = [participant.email ])
            url="http://127.0.0.1:5000/validationConsentement/"+participant.urlPerso
            #url="location.href='http://127.0.0.1:5000/questionnaireParticipantsDemographique/'"
            msg.html = "<b>"+participant.nom+"</b>, <p>Vous avez été selectionnés pour participer à l'évaluation de "+jeei.nom+" un jeu d'évasion éducatif. Les conditions de participation vous seront expliquées au jour de l'experimentation. Si vous souhaitez y participer merci de marquer votre consentement via le lien ci-desous.  </p> <a href="+url+">Consentement </a>"
            #<button onclick='"+ url+ "'> Enquête Démographique </button>"
            mail.send(msg)

    return "ok"



@app.route("/validationConsentement/<path:UrlUtilisateur>", methods=['GET', 'POST'])
def fonction_validationConsentement(UrlUtilisateur):
    participant=Participant.query.filter_by(urlPerso=UrlUtilisateur).first()
    experimentation=Experimentation.query.filter_by(id=participant.fk_ExperimentationId).first()
    jeei=Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    
    if participant:
        print("c'est bien un participant  et donc on accèpte qu'il se connecte avec cet url qui lui est propre")
        
        return render_template("frontend_etudiant/validationConsentement.html",currentUser=current_user,jeei=jeei,participant=participant, experimentation=experimentation)
    else:
       return render_template("frontend_etudiant/noaccess.html")


@app.route("/confirmationConsentement", methods=['GET', 'POST'])
def fonction_confirmationConsentement():
    participantId= request.args.get("participantId")


    participant=Participant.query.filter_by(id=participantId).first()
    participant.consentement=True
    db.session.add(participant)#sauve dans la DB
    db.session.commit()
    
    return "ok"

       

   