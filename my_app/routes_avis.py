##########################################################
#mes imports
##########################################################

from cmath import sqrt
from sqlalchemy import false
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
from my_app.models.evaluation import Evaluation
from my_app.models.experimentation import Experimentation
from my_app.models.jeei_package.jeei import Jeei
from my_app.models.jeei_package.questionApprentissage import QuestionApprentissage
from my_app.models.jeei_package.specification import Specification
from my_app.models.participant import Participant
from my_app.models.questionnaireMotivation import QuestionnaireMotivation
from my_app.models.questionnairePreTest import QuestionnairePreTest #import de la db
from my_app.models.questionnairePostTest import QuestionnairePostTest #import de la db

from my_app.models.user import User

from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from flask import json, jsonify
from my_app.routes_specificationMesJEEI import verificationComplet
from my_app.models.questionnaireUX import QuestionnaireUX
import sys
import xlsxwriter



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()







@app.route("/ueq", methods=['GET', 'POST'])
@login_required
def fonction_ueq():
    
    #ATTENTION!!!on ne permet d'afficher UEQ que ssi ils ont au moins une experimentation à leur actif
   experimentations=Experimentation.query.filter_by(fk_UserId=current_user.id).all()
   evaluateur=False
   for experimentation in experimentations:
       if experimentation.etape12:
           evaluateur=True
   return render_template("ueq.html",currentUser=current_user,evaluateur=evaluateur)