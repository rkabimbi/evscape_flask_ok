##########################################################
#mes imports
##########################################################

from ntpath import join
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

from my_app.models.jeei_package.jeei import Jeei
from my_app.models.jeei_package.specification import Specification, Statut, Theme, PublicCible
from my_app.models.jeei_package.jointureJeeiUser import JointureJeeiUser





@app.route("/mesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_mesJEEI():

    #Extraction des données (on gagne en manipulation et rapidité en chargeant tt d'abord)
    mesJEEI=Jeei.query.all()
    specifications= Specification.query.all()
    #users= User.query.all()


    #Step1 - Rechercher dans DB que tous les JEEI propres à l'utilisateurs connectés. Quand on dit PROPRES càd ceux qu'il a crée ou ceux
    # pour lesquels il a fait une experimentation!!! ATTENTION DONC

    #...

    #Step2 - Convertir ce que la DB renvoi en dictionnaire

    #...
    #ATTENTION lors de la conversion important de garder les noms utilisés ci-dessous en en-tête sinon ca va bugger

    
    mesJEEI=fonction_conversionSQLDICT(mesJEEI,specifications)
  
   
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
    



def fonction_conversionSQLDICT(mesJEEI,specifications):
    res ={"noms":[],"auteurs":[],"nbrExperimentations":[],"img":[],"themes":[],"id":[],"statuts":[],"descriptifs":[]}

    for JEEI in mesJEEI:
        res["noms"].append(JEEI.nom)
        jointureJeeiUser=JointureJeeiUser.query.filter_by(fk_JeeiId=JEEI.id).first()#car le premier dans la jointure est d'office le createur car crée au moment
        createur=User.query.filter_by(id=jointureJeeiUser.fk_UserId).first()
        createur=createur.lastname+", "+createur.firstname
        res["auteurs"].append(createur)
        res["nbrExperimentations"].append(10) # en attendant d'avoir les tables qu'il faut
        if specifications[JEEI.fk_SpecificationId-1].theme!=None:#si y a pas de value selectionnée par l'utilisateur et qu'on a donc un JEEI sans thème alors ici quand il va faire la fonction .value ca va bugguer
            res["themes"].append(specifications[JEEI.fk_SpecificationId-1].theme.value)#-1 car la liste commence à zero et .value c'est pour recuperer le string de l'enum
             
        else:#obligé de faire ce else sinon quand il charge les cartes il lui manque des données pour les boucles dans le HTML
            res["themes"].append(None)
        res["id"].append(JEEI.id)
        res["img"].append(JEEI.img)
        res["descriptifs"].append(JEEI.descriptif)
        if specifications[JEEI.fk_SpecificationId-1].statut!=None:#voir remarque au niveau de "theme"
            res["statuts"].append(specifications[JEEI.fk_SpecificationId-1].statut.value)#-1 car la liste commence à zero
        else:#obligé de faire ce else sinon quand il charge les cartes il lui manque des données pour les boucles dans le HTML
            res["statuts"].append(None)
  
    return res
        