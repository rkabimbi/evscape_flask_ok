##########################################################
#mes imports
##########################################################

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



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()






@app.route("/mesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_mesJEEI():

    #en attendant la DB. A noter que je suis obligé de renvoyer tous les JEEI d'un coup pour que ca marche de l'autre côté
    mesJEEI={  
        "noms":["Descape1","Descape2","Descape3","Descape4","Descape5","Descape6","Descape7","Descape8","Descape9","Descape10"],
        "auteurs":["Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy"],
        "nbrExperimentations":[0,0,0,0,0,0,0,0,0,0],
        "img":["static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest2.jpeg","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest2.jpeg"],
        "themes":["Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite","Cryptographie"],
        "id":[502,785,893,1058,17,526,854,8962,2562,455]
    }

 
    return render_template("mesJEEI.html",currentUser=current_user,mesJEEI=mesJEEI)

