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
from my_app.models.questionnaireUEQ import QuestionnaireUEQ







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


@app.route("/sauvegardeUEQ", methods=['GET', 'POST'])
@login_required
def fonction_sauvegardeUEQ():
    questionnaireUEQ=QuestionnaireUEQ.query.filter_by(fk_UserId=current_user.id).first()
    #verifier qu'il n'existe pas déjà une eval. Si c'est le cas ca ecrase l'ancienne. Si pas d'existante on en cree un new
    if not questionnaireUEQ:
        questionnaireUEQ=QuestionnaireUEQ(current_user.id)
    
    questionnaireUEQ.u01=request.args.get("likertu01")
    questionnaireUEQ.u02=request.args.get("likertu02")
    questionnaireUEQ.u03=request.args.get("likertu03")
    questionnaireUEQ.u04=request.args.get("likertu04")
    questionnaireUEQ.u05=request.args.get("likertu05")
    questionnaireUEQ.u06=request.args.get("likertu06")
    questionnaireUEQ.u07=request.args.get("likertu07")
    questionnaireUEQ.u08=request.args.get("likertu08")
    questionnaireUEQ.u09=request.args.get("likertu09")
    questionnaireUEQ.u10=request.args.get("likertu10")
    questionnaireUEQ.u11=request.args.get("likertu11")
    questionnaireUEQ.u12=request.args.get("likertu12")
    questionnaireUEQ.u13=request.args.get("likertu13")
    questionnaireUEQ.u14=request.args.get("likertu14")
    questionnaireUEQ.u15=request.args.get("likertu15")
    questionnaireUEQ.u16=request.args.get("likertu16")
    questionnaireUEQ.u17=request.args.get("likertu17")
    questionnaireUEQ.u18=request.args.get("likertu18")
    questionnaireUEQ.u19=request.args.get("likertu19")
    questionnaireUEQ.u20=request.args.get("likertu20")
    questionnaireUEQ.u21=request.args.get("likertu21")
    questionnaireUEQ.u22=request.args.get("likertu22")
    questionnaireUEQ.u23=request.args.get("likertu23")
    questionnaireUEQ.u24=request.args.get("likertu24")
    questionnaireUEQ.u25=request.args.get("likertu25")
    questionnaireUEQ.u26=request.args.get("likertu26")
    questionnaireUEQ.commentaire=request.args.get("commentaireUEQ")



    db.session.add(questionnaireUEQ)#sauve dans la DB
    db.session.commit()
        
    return render_template("merciUEQ.html",currentUser=current_user)
