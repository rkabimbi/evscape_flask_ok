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
from my_app.models.experimentation import Experimentation
from my_app.routes_specificationMesJEEI import fonction_calculResultats






@app.route("/mesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_mesJEEI():

    #Extraction des données (on gagne en manipulation et rapidité en chargeant tt d'abord)
    mesJEEI=Jeei.query.all()
    specifications= Specification.query.all()
    
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
    res ={"noms":[],"auteurs":[],"auteursID":[],"nbrExperimentations":[],"img":[],"themes":[],"id":[],"statuts":[],"descriptifs":[],"scores":[],"estValide":[]}

    for JEEI in mesJEEI:
        res["noms"].append(JEEI.nom)
        #jointureJeeiUser=JointureJeeiUser.query.filter_by(fk_JeeiId=JEEI.id).first()#car le premier dans la jointure est d'office le createur car crée au moment
        createur=User.query.filter_by(id=JEEI.auteurID).first()
        createur=createur.lastname+", "+createur.firstname
        res["auteurs"].append(createur)
        res["auteursID"].append(JEEI.auteurID)
        
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

        #gestion du nbr d'experimentation par JEEI
        experimentations=Experimentation.query.all()
        total =0
        for experimentation in experimentations:
            if experimentation.fk_JeeiId==JEEI.id:
                total=total+1
        res["nbrExperimentations"].append(total)#validées ou non
        #si il y a des experimentations completes
        """ 
        experimentationOk=False
        for experimentation in experimentations:
            if experimentation.fk_JeeiId==JEEI.id:
                if experimentation.etape12:#si on est arrivé à étape 12 (au moins une fois)
                    experimentationOk=True
        if experimentationOk:
            res["scores"].append(fonction_calculResultats(JEEI))
        else:
            res["scores"].append(0)
        """
        try:
            #je renvoi pas tt le return de la fonction car jinja ne sait pas gerer le tableau de tableau
            resultatsTemp=fonction_calculResultats(JEEI)
            evolutionApprentissageMoyenne=resultatsTemp[1]["evolutionApprentissageMoyenne"]
            res["scores"].append(evolutionApprentissageMoyenne)
        except ZeroDivisionError:
            res["scores"].append(0)
        
        if JEEI.estValide:#je dois procéder de la sorte pcq javascript me pose un probleme avec mes booleens
            res["estValide"].append(1)
        else:
            res["estValide"].append(0)
        
       
       
  
    return res
        