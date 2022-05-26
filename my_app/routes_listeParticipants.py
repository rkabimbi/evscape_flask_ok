
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
    
    return render_template("listeParticipants.html",currentUser=current_user,JEEI=JEEIAEnvoyer,specification=specificationAEnvoyer,experimentation=experimentation,participants=participants)
