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
    #en attendant la DB. A noter que je suis obligé de renvoyer tous les JEEI d'un coup pour que ca marche de l'autre côté
    mesJEEI={  
        "noms":["Descape1","Descape2","Descape3","Descape4","Descape5","Descape6","Descape7","Descape8","Descape9","Descape10"],
        "auteurs":["Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy"],
        "nbrExperimentations":[0,0,0,0,0,0,0,0,0,0],
        "img":["static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest2.jpeg","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest2.jpeg"],
        "themes":["Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite","Cryptographie"],
        "id":[502,785,893,1058,17,526,854,8962,2562,455]
    }

    if mesJEEI: #si mesJEEI n'est pas vide
        #trop complexe pour rien...je dois juste renvoyer les 4 premiers points barre
        if request.args.get("pagination"):
            pagination = int(request.args.get("pagination"))
            
        else:
            pagination =1
        print("pagination =",pagination)
        borneInf=(pagination-1)*4
        borneSup=pagination*4-1
      
    
        nbrPagesTotal=math.ceil(len(mesJEEI['noms'])/4)#necessaire pour definir la taille de pager
        listeMesJEEIAEnvoyer=function_extractionSousMatrice4Cartes(mesJEEI,borneInf,borneSup)
        print("Liste qui part1")
        print(listeMesJEEIAEnvoyer)
        return render_template("mesJEEI.html",currentUser=current_user,pagination=pagination,listeMesJEEI=listeMesJEEIAEnvoyer,nbrPagesTotal=nbrPagesTotal)
    else:
        #on renvoi vers la création de JEEI
        flash('Pas de Jeu d Evasion cree', 'warning')
        return redirect(url_for('creationMesJEEI'))
    

def function_extractionSousMatrice4Cartes(mesJEEI,borneInf,borneSup):
    #pas terrible car ici je fais en brut mais je sais que je voudrais tjrs en envoyer que 4 donc pas me compliquer
    print("function_extractionSousMatrice4Cartes")
    print(mesJEEI)
    print(borneInf,borneSup+1)
    liste4Cartes={"noms":[],"auteurs":[],"nbrExperimentations":[],"img":[],"themes":[],"id":[]}

    for positionJEEI in range(borneInf,borneSup+1):#+1 car range c'est un < pas un <=
        liste4Cartes["noms"].append(mesJEEI["noms"][positionJEEI])
        liste4Cartes["auteurs"].append(mesJEEI["auteurs"][positionJEEI])
        liste4Cartes["nbrExperimentations"].append(mesJEEI["nbrExperimentations"][positionJEEI])
        liste4Cartes["img"].append(mesJEEI["img"][positionJEEI])
        liste4Cartes["themes"].append(mesJEEI["themes"][positionJEEI])
        liste4Cartes["id"].append(mesJEEI["id"][positionJEEI])
        print(liste4Cartes)
    return liste4Cartes



@app.route("/creationMesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_creationMesJEEI():
    print("creationMesJEEI")
    return render_template(currentUser=current_user)




@app.route("/mesJEEICartes", methods=['GET', 'POST'])
@login_required
def fonction_mesJEEIcartes():
    print("MesJEEICartes--------------------------------")
    mesJEEI={  
        "noms":["Descape1","Descape2","Descape3","Descape4","Descape5","Descape6","Descape7","Descape8","Descape9","Descape10"],
        "auteurs":["Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy","Rudy"],
        "nbrExperimentations":[0,0,0,0,0,0,0,0,0,0],
        "img":["static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest2.jpeg","static/img/JEEITest1.jpeg","static/img/imgLoginPage2.png", "static/img/imgLoginPage2.png","static/img/JEEITest2.jpeg"],
        "themes":["Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite","Cryptographie","Algorithmie", "Cybersecurite","Cryptographie"],
        "id":[502,785,893,1058,17,526,854,8962,2562,455]
    }
    if mesJEEI: #si mesJEEI n'est pas vide
        if request.args.get("pagination"):
            pagination = int(request.args.get("pagination"))
            borneInf=(pagination-1)*4
        else:
            pagination =1
        borneInf=(pagination-1)*4
        borneSup=pagination*4-1
        listeMesJEEIAEnvoyer=function_extractionSousMatrice4Cartes(mesJEEI,borneInf,borneSup)
        print("Liste qui part2")
        print(listeMesJEEIAEnvoyer)
        listeJsonifiee= jsonify(listeMesJEEIRecue=listeMesJEEIAEnvoyer)
        print(type(listeJsonifiee))
        return listeJsonifiee