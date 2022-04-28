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

from my_app import db #import de la db

from my_app.models.user import User

from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from flask import json, jsonify

from my_app.models.jeei_package.jeei import Jeei



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()




@app.route("/specificationMesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_specificationMesJEEI():
    print("specificationMesJEEI")
    """" 
    #recuperation ID qui est communiqué depuis le HTML
    idJEEIAmodifier = request.args.get("idJEEI")
    monJEEIAEnvoyer=None
    if idJEEIAmodifier: #si un id est renseigné (ca veut dire qu'on a cliqué uncarte)
        #chercher dans DB
        user = User.query.filter_by(username=formLogin.username.data).first()

        #màj monJEEIAENVOYER   

    else: #si pas d'id communiqué ca veut dire qu'on a cliqué le bouton jaune (creer un nouveau)
        #creer un nouveau JEEI dans la DB

        #màj monJEEIAENVOYER
    
    """
    jeei = Jeei.query.filter_by().first()
    print(jeei)
    return render_template("specificationMesJEEI.html",currentUser=current_user)



