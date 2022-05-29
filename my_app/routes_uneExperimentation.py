
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
import my_app #import de la db

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
from flask_mail import Mail, Message
#config email

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


    #en attendant je fais ceci
    idExperimentation=1
    return render_template("groupesParticipants.html",currentUser=current_user,JEEI=JEEIAEnvoyer,idExperimentation=1)



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
    


@app.route("/debloquerFormulaireDemographique", methods=['GET', 'POST'])
@login_required
def fonction_debloquerFormulaireDemographique():
    print("fonction_debloquerFormulaireDemographique - Envoie email")
   
    msg = Message('Hello from the other side!', sender = ( 'Equipe EvscApp' ,'rudy.kabimbingoy@teams.student.unamur.be'), recipients = ['paul@mailtrap.io'])
    msg.html = "<b>Hey Paul</b>, sending you this email from my <a href='https://google.com'>Flask app</a>, lmk if it works"
    mail.send(msg)
    return "Message sent!"