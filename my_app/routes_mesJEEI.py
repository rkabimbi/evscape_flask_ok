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



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()







@app.route("/mesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_mesJEEI():
    #Step1 - Rechercher dans DB que tous les JEEI propres à l'utilisateurs connectés. Quand on dit PROPRES càd ceux qu'il a crée ou ceux
    # pour lesquels il a fait une experimentation!!! ATTENTION DONC

    #...

    #Step2 - Convertir ce que la DB renvoi en dictionnaire

    #...
    #ATTENTION lors de la conversion important de garder les noms utilisés ci-dessous en en-tête sinon ca va bugger

    mesJEEI={  
        "noms":["Descape1","Descape2","Descape3","Descape4","Descape5","Descape6","Descape7","Descape8","Descape9"],
        "auteurs":["Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy"],
        "nbrExperimentations":[0,18,2,85,19,0,64,0,2121],
        "img":["static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest2.jpeg","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/JEEITest1.jpeg"],
        "themes":["Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite"],
        "id":[502,785,893,1058,17,526,854,8962,2562],
        "statuts":["verrouille", "ouvert", "ouvert", "ouvert", "verouille","verrouille", "ouvert", "ouvert", "ouvert"]
    }
    
   
    if mesJEEI: #si mesJEEI n'est pas vide
        print("liste JEEI envoyée vers front")
        print(mesJEEI)
        nbrJEEI=len(mesJEEI['noms'])
        nbrPagesTotal=math.ceil(nbrJEEI/4)#necessaire pour definir la taille de pager
        return render_template("mesJEEI.html",currentUser=current_user,listeMesJEEI=mesJEEI,nbrPagesTotal=nbrPagesTotal,pagination=1,nbrJEEI=nbrJEEI)
    else:
        #on renvoi vers la création de JEEI
        flash("Vous n\'avez pas encore de Jeu d\'évasion à votre actif. Merci d\'en créer un", 'warning')
        return redirect(url_for('fonction_specificationMesJEEI'))
    




@app.route("/specificationMesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_specificationMesJEEI():
    print("specificationMesJEEI")
    return render_template("specificationMesJEEI.html",currentUser=current_user)



