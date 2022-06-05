
from turtle import pos

from sqlalchemy import Identity
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
import my_app
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
import time

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
from flask_mail import Mail, Message
from my_app.models.evaluation import Evaluation
#config email
import random

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '2a505d7be718ed'
app.config['MAIL_PASSWORD'] = '37960d02bef471'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail=Mail(app)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!route pour creer une nouvelle experimentation !!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route("/uneExperimentation", methods=['GET', 'POST'])
@login_required
def fonction_uneExperimentation():
    print("fonction_uneExperimentation")
    idJEEIaEnvoyer = request.args.get("idJEEI")
    JEEIAEnvoyer = Jeei.query.filter_by(id=idJEEIaEnvoyer).first()
    
    specificationAEnvoyer = specification=Specification.query.filter_by(id=JEEIAEnvoyer.fk_SpecificationId).first()



    #pour recup que les experimentations liées aux JEEI afin de connaitre le numéro "idInterne" du JEEI par rapport à l'experimentation en question
    experimentations=Experimentation.query.filter_by(fk_JeeiId=JEEIAEnvoyer.id).all()

    #je lui donne le numero "interne"
    dernierIdInterne=len(experimentations)
    print("nbInterne :",dernierIdInterne)

    #creation experimentatio,
    experimentation = Experimentation(fk_JeeiId=JEEIAEnvoyer.id,fk_UserId=current_user.id,idInterne=dernierIdInterne+1)
    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()

    print(experimentation)
    


    return render_template("uneExperimentation.html",currentUser=current_user,JEEI=JEEIAEnvoyer,specification=specificationAEnvoyer,experimentation=experimentation)


@app.route("/consulterGroupesParticipants", methods=['GET', 'POST'])
@login_required
def fonction_consulterGroupesParticipants():
    print("consulterGroupesParticipants")
    print("Afficher la liste des groupes construits par la machine ")
    
    idJEEIaEnvoyer = request.args.get("idJEEI")
    JEEIAEnvoyer = Jeei.query.filter_by(id=idJEEIaEnvoyer).first()
    idExperimentation = request.args.get("idExperimentation")
    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
   
    return render_template("groupesParticipants.html",currentUser=current_user,JEEI=JEEIAEnvoyer,idExperimentation=idExperimentation,participants=participants)



@app.route("/afficherUneExperimentationExistante", methods=['GET', 'POST'])
@login_required
def fonction_afficherUneExperimentationExistante():
    print("afficherUneExperimentationExistante")
    idExperimentation= request.args.get("idExperimentation")
    experimentation = Experimentation.query.filter_by(id=idExperimentation).first()
    JEEIAEnvoyer= Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
    specificationAEnvoyer = Specification.query.filter_by(id=JEEIAEnvoyer.fk_SpecificationId).first()


    return render_template("uneExperimentation.html",currentUser=current_user,JEEI=JEEIAEnvoyer,specification=specificationAEnvoyer,experimentation=experimentation)



@app.route("/validerEtapeExperimentation", methods=['GET', 'POST'])
@login_required
def fonction_validerEtapeExperimentation():
    print("validerEtapeExperimentation")
    idExperimentation= request.args.get("idExperimentation")
    etape= int(request.args.get("etape"))
    print(idExperimentation, etape)
    experimentation = Experimentation.query.filter_by(id=idExperimentation).first()
    if etape==2:
        experimentation.etape2=True
    if etape==3:
        experimentation.etape3=True
    if etape==4:
        experimentation.etape4=True
        experimentation.etape5=True#car cette etape ne necessite pas de validation
        creerGroupe(idExperimentation)
    if etape==6:
        experimentation.etape6=True
    if etape==7:
        experimentation.etape7=True
    if etape==8:
        experimentation.etape8=True
    if etape==9:
        experimentation.etape9=True
    if etape==10:
        experimentation.etape10=True
    if etape==11:
        experimentation.etape11=True
    if etape==12:
        experimentation.etape12=True
    if etape==13:
        experimentation.etape13=True

    db.session.add(experimentation)#sauve dans la DB
    db.session.commit()
    print(experimentation)

    return "ok"


def creerGroupe(idExperimentation):
    #recup de tous les participants propre à l'experimentation concernée
    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
    nbrParticipantsValides=0
    for participant in participants:
        if participant.consentement:
            nbrParticipantsValides=nbrParticipantsValides+1

    nbrParticipantGroupeExp=nbrParticipantsValides/2
    #tant qu'il y a des membres a assigné au groupe exp
    while nbrParticipantGroupeExp>0:
        #parcours la liste de tous les participants
        for participant in participants:
            #si consentement , tjrs des membres à assigner (obligé car boucle dans boucle)!!! et qu'il est pas deja assigné au groupe exp (pour eviter repetition d'une meme personne)
            if participant.consentement and nbrParticipantGroupeExp>0 and  not participant.groupeExperimental:
                #on lui donne une valeur aleatoire
                participant.groupeExperimental= random.choice([True,False])
                db.session.add(participant) 
                db.session.commit()
                if participant.groupeExperimental:
                    nbrParticipantGroupeExp=nbrParticipantGroupeExp-1
                    print("j'ai sauve un membre experimental")


@app.route("/debloquerFormulaireDemographique", methods=['GET', 'POST'])
@login_required
def fonction_debloquerFormulaireDemographique():
    print("fonction_debloquerFormulaireDemographique - Envoie email")
    #on recupere tous les etudiants liés à l'experience lambda
    idExperimentation= request.args.get("idExperimentation")
    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
    print("liste Participants liée à l'experimentation ",idExperimentation)
    print(participants)
    experimentation=Experimentation.query.filter_by(id=idExperimentation).first()

    jeei = Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()

    
    for participant in participants:
        
        if participant.consentement:#si il a marqué son consentment

            #on crée alors un évaluation complète pour lui
    

            evaluation=Evaluation(jeei.id,experimentation.id,participant.id)
            db.session.add(evaluation)
            db.session.commit()
            time.sleep(0.4)#je met un time de 5 secondes sinon python envoi plus de 3 emails par seconde et alors mailtrap ne suis pas et ca renvoi une erreur 500

            #on lui envoi un email
            msg = Message((jeei.nom,' : Formulaire démographique'), sender = ( 'Equipe EvscApp' ,'rudy.kabimbingoy@teams.student.unamur.be'), recipients = [participant.email ])
            url="http://127.0.0.1:5000/questionnaireParticipantsDemographique/"+participant.urlPerso
            #url="location.href='http://127.0.0.1:5000/questionnaireParticipantsDemographique/'"
            msg.html = "<b>"+participant.nom+"</b>, <p>Vous avez marqué votre consentement à participer à l'activité "+jeei.nom+". Merci dès lors de bien vouloir compléter une enquête démographique via le lien ci-dessous </p> <a href="+url+">Questionnaire Démographique </a>"
            #<button onclick='"+ url+ "'> Enquête Démographique </button>"
            mail.send(msg)
    


    return "Messages envoyés!"



@app.route("/debloquerFormulaireMotivation", methods=['GET', 'POST'])
@login_required
def fonction_debloquerFormulaireMotivation():
    print("fonction_debloquerFormulaireMotivation - Envoie email")
    #on recupere tous les etudiants liés à l'experience lambda
    idExperimentation= request.args.get("idExperimentation")
    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
    print("liste Participants liée à l'experimentation ",idExperimentation)
    print(participants)
    experimentation=Experimentation.query.filter_by(id=idExperimentation).first()

    jeei = Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()

    
    for participant in participants:
        
        if participant.consentement:#si il a marqué son consentment
            time.sleep(0.4)#je met un time de 5 secondes sinon python envoi plus de 3 emails par seconde et alors mailtrap ne suis pas et ca renvoi une erreur 500
            msg = Message((jeei.nom,' : Formulaire de Motivation'), sender = ( 'Equipe EvscApp' ,'rudy.kabimbingoy@teams.student.unamur.be'), recipients = [participant.email ])
            url="http://127.0.0.1:5000/questionnaireParticipantsMotivation/"+participant.urlPerso
            #url="location.href='http://127.0.0.1:5000/questionnaireParticipantsDemographique/'"
            msg.html = "<b>"+participant.nom+"</b>, <p>Vous avez marqué votre consentement à participer à l'activité "+jeei.nom+". Merci dès lors de bien vouloir compléter une enquête de motivation via le lien ci-dessous </p> <a href="+url+">Questionnaire Motivation </a>"
            #<button onclick='"+ url+ "'> Enquête Démographique </button>"
            mail.send(msg)
    


    return "Messages envoyés!"

   

@app.route("/debloquerFormulaireUX", methods=['GET', 'POST'])
@login_required
def fonction_debloquerFormulaireUX():
    print("fonction_debloquerFormulaireUX - Envoie email")
    #on recupere tous les etudiants liés à l'experience lambda
    idExperimentation= request.args.get("idExperimentation")
    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
    print("liste Participants liée à l'experimentation ",idExperimentation)
    print(participants)
    experimentation=Experimentation.query.filter_by(id=idExperimentation).first()

    jeei = Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()

    
    for participant in participants:
        
        if participant.consentement:#si il a marqué son consentment
            time.sleep(0.4)#je met un time de 5 secondes sinon python envoi plus de 3 emails par seconde et alors mailtrap ne suis pas et ca renvoi une erreur 500
            msg = Message((jeei.nom,' : Formulaire UX'), sender = ( 'Equipe EvscApp' ,'rudy.kabimbingoy@teams.student.unamur.be'), recipients = [participant.email ])
            url="http://127.0.0.1:5000/questionnaireParticipantsUX/"+participant.urlPerso
            #url="location.href='http://127.0.0.1:5000/questionnaireParticipantsDemographique/'"
            msg.html = "<b>"+participant.nom+"</b>, <p>Vous avez marqué votre consentement à participer à l'activité "+jeei.nom+". Merci dès lors de bien vouloir compléter une enquête UX via le lien ci-dessous </p> <a href="+url+">Questionnaire UX </a>"
            #<button onclick='"+ url+ "'> Enquête Démographique </button>"
            mail.send(msg)
    


    return "Messages envoyés!"



@app.route("/debloquerFormulairePreTest", methods=['GET', 'POST'])
@login_required
def fonction_debloquerFormulairePreTest():
    print("fonction_debloquerFormulairePreTest - Envoie email")

    #on recupere tous les etudiants liés à l'experience lambda
    idExperimentation= request.args.get("idExperimentation")
    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
    print("liste Participants liée à l'experimentation ",idExperimentation)
    print(participants)
    experimentation=Experimentation.query.filter_by(id=idExperimentation).first()

    jeei = Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
  

    
    for participant in participants:
        
        if participant.consentement:#si il a marqué son consentment
            time.sleep(0.4)#je met un time de 5 secondes sinon python envoi plus de 3 emails par seconde et alors mailtrap ne suis pas et ca renvoi une erreur 500
            msg = Message((jeei.nom,' : Questionnaire Pre-Test'), sender = ( 'Equipe EvscApp' ,'rudy.kabimbingoy@teams.student.unamur.be'), recipients = [participant.email ])
            url="http://127.0.0.1:5000/questionnaireParticipantsPreTest/"+participant.urlPerso
            #url="location.href='http://127.0.0.1:5000/questionnaireParticipantsDemographique/'"
            msg.html = "<b>"+participant.nom+"</b>, <p>Vous avez marqué votre consentement à participer à l'activité "+jeei.nom+". Merci dès lors de bien vouloir compléter un questionnaire de pre-test via le lien ci-dessous </p> <a href="+url+">Questionnaire Pre-test </a>"
            #<button onclick='"+ url+ "'> Enquête Démographique </button>"
            mail.send(msg)
    


    return "Messages envoyés!"



@app.route("/debloquerFormulairePostTest", methods=['GET', 'POST'])
@login_required
def fonction_debloquerFormulairePostTest():
    print("fonction_debloquerFormulairePostTest - Envoie email")

    #on recupere tous les etudiants liés à l'experience lambda
    idExperimentation= request.args.get("idExperimentation")
    participants=Participant.query.filter_by(fk_ExperimentationId=idExperimentation).all()
    print("liste Participants liée à l'experimentation ",idExperimentation)
    print(participants)
    experimentation=Experimentation.query.filter_by(id=idExperimentation).first()

    jeei = Jeei.query.filter_by(id=experimentation.fk_JeeiId).first()
  

    
    for participant in participants:
        
        if participant.consentement:#si il a marqué son consentment
            time.sleep(0.4)#je met un time de 5 secondes sinon python envoi plus de 3 emails par seconde et alors mailtrap ne suis pas et ca renvoi une erreur 500
            msg = Message((jeei.nom,' : Questionnaire Post-Test'), sender = ( 'Equipe EvscApp' ,'rudy.kabimbingoy@teams.student.unamur.be'), recipients = [participant.email ])
            url="http://127.0.0.1:5000/questionnaireParticipantsPostTest/"+participant.urlPerso
            #url="location.href='http://127.0.0.1:5000/questionnaireParticipantsDemographique/'"
            msg.html = "<b>"+participant.nom+"</b>, <p>Vous avez marqué votre consentement à participer à l'activité "+jeei.nom+". Merci dès lors de bien vouloir compléter un questionnaire de post-test via le lien ci-dessous </p> <a href="+url+">Questionnaire Post-test </a>"
            #<button onclick='"+ url+ "'> Enquête Démographique </button>"
            mail.send(msg)
    


    return "Messages envoyés!"