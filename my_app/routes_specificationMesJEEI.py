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
import os
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
from my_app.models.upload_file import allowed_file
from werkzeug.utils import secure_filename
from flask import send_from_directory

@app.route("/specificationMesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_specificationMesJEEI():
    print("specificationMesJEEI")
    
    #recuperation ID qui est communiqué depuis le HTML
    print("id recuperé de HTML :", request.args.get("idJEEI") )
    idJEEIAmodifier = request.args.get("idJEEI")
    monJEEIAEnvoyer=None
    specification=None
    if idJEEIAmodifier: #si un id est renseigné (ca veut dire qu'on a cliqué uncarte et donc on doit aller chercher le JEEI en question)
        #chercher dans DB
        monJEEIAEnvoyer = Jeei.query.filter_by(id=idJEEIAmodifier).first()
        #je vais chercher la spécification liée au JEEI
        specification=Jeei.query.filter_by(id=monJEEIAEnvoyer.fk_SpecificationId).first()
 

    else: #si pas d'id communiqué ca veut dire qu'on a cliqué le bouton jaune (creer un nouveau)
        #creer un nouveau Specification  qui soit vierge
        specification= Specification(None,None,None,None,None,None,None,None,None)
        db.session.add(specification)#sauve dans la DB
        db.session.commit()
        #je recupere le numero d'id de la spécification que je viens de créer
        newSpecificationId=Specification.query.order_by(Specification.id.desc()).first().id
        print("dernier eleent =",newSpecificationId)
        #je creer un JEEI et renseigne à quel specification il est lié (celle que je viens de creer)
        monJEEIAEnvoyer=Jeei(None,None,None,fk_SpecificationId=newSpecificationId)
        db.session.add(monJEEIAEnvoyer)#sauve dans la DB
        db.session.commit()
        newJeeiId=Jeei.query.order_by(Jeei.id.desc()).first().id
        flash("Votre Jeu d'Evasion a été crée [id :"+str(newJeeiId)+ "]. Bonne évaluation!!!", 'success')


        
    print(monJEEIAEnvoyer)
    print(specification)
    return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEIAEnvoyer,specificationJEEIRecupere=specification)



@app.route("/sauvegardeTableJeei", methods=['GET', 'POST'])
@login_required
def fonction_sauvegardeTableJeei():
    champs = request.args.get("champs")
    valeur= request.args.get("valeur")
    idJEEI= request.args.get("idJEEI")

    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    if champs=="nom":
        monJEEI.nom=valeur
        db.session.commit()
    elif champs=="descriptif":
        monJEEI.descriptif=valeur
        db.session.commit()
    
    
    
    #pour confirme que tout s'est bien passe côté front
    reponse= jsonify(reponse="ok")
  
    return reponse




@app.route('/uploadPhoto', methods=['GET', 'POST'])#Get et post est important pour tester avec quelle méthode on est arrivé 
#(pour eviter que des gens tapent l'url à la main. S'ils le font on est en mode GET et alors on prévoit dans la méthode qu'on tient pas compte du truc (on recharge la page))
def upload_file( ):

    idJEEI= request.args.get("idJEEI")
    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    if 'file' not in request.files:#si pas de fichier
            flash('Pas de fichier', 'danger')#flash c'est qqch que flask sait intepreter et donc on peut faire des messages d'erreur
            return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI)
    file = request.files['file'] #si on est ici c'est qu'il y a un fichier
    if file.filename == '':#si non du fichier est vide
            flash('Pas de fichier selectionné', 'danger')
            return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI)

    
    if file and allowed_file(file.filename):#si on a un fichier et que le format est permis
        filename = secure_filename(file.filename)#methode qui evite des attaques où charges des fichiers systeme (elle rajoute des donées au nom)
        print(filename)
        print(monJEEI)
        monJEEI.img="static/img/img"+str(monJEEI.id)+".jpeg" #on sauve l'adresse dans l'attribut image
        db.session.commit()
        nomPhoto="img"+str(monJEEI.id)+".jpeg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomPhoto))#on sauve le fichier

        print(redirect(request.base_url))

        return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI)
    