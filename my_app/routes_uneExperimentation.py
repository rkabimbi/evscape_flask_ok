
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

@app.route("/uneExperimentation", methods=['GET', 'POST'])
@login_required
def fonction_uneExperimentation():
    print("fonction_uneExperimentation")
    idJEEIaEnvoyer = request.args.get("idJEEI")
    JEEIAEnvoyer = Jeei.query.filter_by(id=idJEEIaEnvoyer).first()
    specificationAEnvoyer = specification=Specification.query.filter_by(id=JEEIAEnvoyer.fk_SpecificationId).first()
    #creation experimentatio,
    experimentation = Experimentation(fk_JeeiId=JEEIAEnvoyer.id,fk_UserId=current_user.id)
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
    
