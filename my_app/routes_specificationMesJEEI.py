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
from my_app.models.jeei_package.questionApprentissage import QuestionApprentissage
from my_app.models.jeei_package.jointureJeeiUser import JointureJeeiUser

@app.route("/specificationMesJEEI", methods=['GET', 'POST'])
@login_required
def fonction_specificationMesJEEI():
    print("specificationMesJEEI")
    
    #recuperation ID qui est communiqué depuis le HTML
    print("id recuperé de HTML :", request.args.get("idJEEI") )
    idJEEIAmodifier = request.args.get("idJEEI")
    monJEEIAEnvoyer=None
    specification=None
    membres=[]
    
    if idJEEIAmodifier: #si un id est renseigné (ca veut dire qu'on a cliqué uncarte et donc on doit aller chercher le JEEI en question)
        #chercher dans DB
        monJEEIAEnvoyer = Jeei.query.filter_by(id=idJEEIAmodifier).first()
        #je vais chercher la spécification liée au JEEI
        specification=Specification.query.filter_by(id=monJEEIAEnvoyer.fk_SpecificationId).first()
        #je vais chercher les question liées à la spécification
        questions=QuestionApprentissage.query.filter_by(fk_SpecificationId=specification.id).all()

        equipe=JointureJeeiUser.query.filter_by(fk_JeeiId=monJEEIAEnvoyer.id).all()
        
        for membre in equipe:
            membreEquipe =User.query.filter_by(id=membre.fk_UserId).first()
            membres.append(membreEquipe)
        print("Tableaux membres----------------------")
        print(membres)

        
      


    else: #si pas d'id communiqué ca veut dire qu'on a cliqué le bouton jaune (creer un nouveau)
        #creer un nouveau Specification  qui soit vierge
        specification= Specification(None,None,None,None,None,None,None,None,None,None)
        db.session.add(specification)#sauve dans la DB
        db.session.commit()
        #je recupere le numero d'id de la spécification que je viens de créer
        newSpecificationId=Specification.query.order_by(Specification.id.desc()).first().id
        print("dernier eleent =",newSpecificationId)
        #je creer un JEEI et renseigne à quel specification il est lié (celle que je viens de creer)
        monJEEIAEnvoyer=Jeei(None,None,None,fk_SpecificationId=newSpecificationId)
        db.session.add(monJEEIAEnvoyer)#sauve dans la DB
        db.session.commit()
        #je crée 10 test vides
        for q in range(1,11):
            question = QuestionApprentissage(question="Question"+str(q),solutionCorrecte="Reponse"+str(q), solutionIncorrecte1="", solutionIncorrecte2="",solutionIncorrecte3="",explicatif="",fk_SpecificationID=newSpecificationId)
            db.session.add(question)
            db.session.commit()
        newJeeiId=Jeei.query.order_by(Jeei.id.desc()).first().id
        questions = QuestionApprentissage.query.filter_by(fk_SpecificationId=newSpecificationId).all()
        #lier l'utilisateur courant (createur) à ce JEEI via table de jointure
        jointureJeeiUser=JointureJeeiUser( fk_UserId=current_user.id , fk_JeeiId=monJEEIAEnvoyer.id)
        db.session.add(jointureJeeiUser)
        db.session.commit()
        membres.append(current_user)
        print(questions)
        flash("Votre Jeu d'Evasion a été crée [id :"+str(newJeeiId)+ "]. Bonne évaluation!!!", 'success')


        
    print(monJEEIAEnvoyer)
    print(specification)
    return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEIAEnvoyer,specificationJEEIRecupere=specification,theme=Theme,publicCible=PublicCible,questions=questions,membres=membres)



@app.route("/sauvegardeTableJeei", methods=['GET', 'POST'])
@login_required
def fonction_sauvegardeTableJeei():
    champs = request.args.get("champs")
    valeur= request.args.get("valeur")
    idJEEI= request.args.get("idJEEI")

    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    print("monJEEI : ", monJEEI)
    idSpecification=Jeei.query.filter_by(id=idJEEI).first().fk_SpecificationId
    print("idSpecification :",idSpecification)
    specification=Specification.query.filter_by(id=idSpecification).first()
    print("specification",specification)

    if champs=="nom":
        monJEEI.nom=valeur
        db.session.commit()
    elif champs=="descriptif":
        monJEEI.descriptif=valeur
        db.session.commit()
    #elif champs=="img":
        #monJEEI.img="static/img/"+valeur+".jpeg"
        #db.session.commit()
    elif champs=="nbrJoueursMin":
        print("case nbr joueurs min" )
        specification.nbrJoueursMin= valeur
        db.session.commit()
    elif champs=="nbrJoueursMax":
        print("case nbr joueurs max" )
        specification.nbrJoueursMax= valeur
        db.session.commit()
    elif champs=="budget":
        print("case budget" )
        specification.budget= valeur
        db.session.commit()
    elif champs=="dureeMinutes":
        print("case dureeMinutes" )
        specification.dureeMinutes= valeur
        db.session.commit()
    elif champs=="scenario":
        print("case scenario" )
        specification.scenario= valeur
        db.session.commit()
    elif champs=="chapitre":
        print("case chapitre" )
        specification.chapitre= valeur
        db.session.commit()
    elif champs=="publicCible":
        print("case publicCible" )
        specification.publicCible= valeur
        db.session.commit()
    elif champs=="theme":
        print("case theme" )
        specification.theme= valeur
        db.session.commit()
    
    #pour confirme que tout s'est bien passe côté front
    reponse= jsonify(reponse="ok")
  
    return reponse




@app.route('/uploadPhoto', methods=['GET', 'POST'])#Get et post est important pour tester avec quelle méthode on est arrivé 
#(pour eviter que des gens tapent l'url à la main. S'ils le font on est en mode GET et alors on prévoit dans la méthode qu'on tient pas compte du truc (on recharge la page))
def upload_file( ):

    idJEEI= request.args.get("idJEEI")
    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    specification=Specification.query.filter_by(id=monJEEI.fk_SpecificationId).first()
    questions= QuestionApprentissage.query.filter_by(fk_SpecificationId=specification.id).all()
    if 'file' not in request.files:#si pas de fichier
            #flash('Pas de fichier', 'danger')#flash c'est qqch que flask sait intepreter et donc on peut faire des messages d'erreur
            return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,theme=Theme,public=PublicCible,questions=questions,specificationJEEIRecupere=specification)
    file = request.files['file'] #si on est ici c'est qu'il y a un fichier
    if file.filename == '':#si non du fichier est vide
            #flash('Pas de fichier selectionné', 'danger')
            return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,theme=Theme,public=PublicCible,questions=questions,specificationJEEIRecupere=specification)

    
    if file and allowed_file(file.filename):#si on a un fichier et que le format est permis
        filename = secure_filename(file.filename)#methode qui evite des attaques où charges des fichiers systeme (elle rajoute des donées au nom)
        print(filename)
        print(monJEEI)
        monJEEI.img="static/img/img"+str(monJEEI.id)+".jpeg" #on sauve l'adresse dans l'attribut image
        db.session.commit()
        nomPhoto="img"+str(monJEEI.id)+".jpeg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomPhoto))#on sauve le fichier

        print(redirect(request.base_url))

        return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,theme=Theme,public=PublicCible,questions=questions,specificationJEEIRecupere=specification)

@app.route('/uploadFilePdf', methods=['GET', 'POST'])#Get et post est important pour tester avec quelle méthode on est arrivé 
#(pour eviter que des gens tapent l'url à la main. S'ils le font on est en mode GET et alors on prévoit dans la méthode qu'on tient pas compte du truc (on recharge la page))
def upload_filePdf( ):
    print("upload_FilePdf")
    idJEEI= request.args.get("idJEEI")
    monJEEI = Jeei.query.filter_by(id=idJEEI).first()
    idSpecificationMonJEEI = Jeei.query.filter_by(id=idJEEI).first().fk_SpecificationId
    print("spec :",idSpecificationMonJEEI)
    specificationMonJEEI= Specification.query.filter_by(id=idSpecificationMonJEEI).first()
    print(specificationMonJEEI)
    questions= QuestionApprentissage.query.filter_by(fk_SpecificationId=specificationMonJEEI.id).all()

    #j'ai reussi à recup la spec mnt faut que jl'envoi dans le front...à mon avis du coup.. je dois faire ca pour toute les routes qui rendes specificationMesJEEI.html...à voir

    if 'file' not in request.files:#si pas de fichier
            #flash('Pas de fichier', 'danger')#flash c'est qqch que flask sait intepreter et donc on peut faire des messages d'erreur
            print("erreur - pas de fichier")
            return render_template("specificationMesJEEI.html",currentUser=current_user,theme=Theme,public=PublicCible,monJEEIRecupere=monJEEI,questions=questions,specificationJEEIRecupere=specificationMonJEEI)
    file = request.files['file'] #si on est ici c'est qu'il y a un fichier
    if file.filename == '':#si non du fichier est vide
            #flash('Pas de fichier selectionné', 'danger')
            print("erreur - pas de fichier selectionné")
            return render_template("specificationMesJEEI.html",currentUser=current_user,theme=Theme,public=PublicCible,monJEEIRecupere=monJEEI,questions=questions,specificationJEEIRecupere=specificationMonJEEI)


    if file and allowed_file(file.filename):#si on a un fichier et que le format est permis
        filename = secure_filename(file.filename)#methode qui evite des attaques où charges des fichiers systeme (elle rajoute des donées au nom)

        print(filename)
        print(monJEEI)
        specificationMonJEEI.documentation="static/img/doc"+str(monJEEI.id)+".pdf" #on sauve l'adresse dans l'attribut image
        db.session.commit()
        nomFichier="doc"+str(monJEEI.id)+".pdf"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomFichier))#on sauve le fichier

        print(redirect(request.base_url))

    return render_template("specificationMesJEEI.html",currentUser=current_user,monJEEIRecupere=monJEEI,specificationJEEIRecupere=specificationMonJEEI,theme=Theme,public=PublicCible,questions=questions)



@app.route("/sauvegardeSpecificationTest", methods=['GET', 'POST'])
@login_required
def fonction_sauvegardeSpecificationTest():
    champs = request.args.get("champs")
    valeur= request.args.get("valeur")
    idTest= request.args.get("idTest")


    question=QuestionApprentissage.query.filter_by(id=idTest).first()
    print("question",question)
    print(champs)
    print(valeur)
    print(idTest)

    if champs=="question":
        question.question=valeur
        db.session.commit()
    if champs=="solution":
        question.solutionCorrecte=valeur
        db.session.commit()
    if champs=="explicatif":
        question.explicatif=valeur
        db.session.commit()
    if champs=="solutionIncorrecte1":
        question.solutionIncorrecte1=valeur
        db.session.commit()
    if champs=="solutionIncorrecte2":
        question.solutionIncorrecte2=valeur
        db.session.commit()
    if champs=="solutionIncorrecte3":
        question.solutionIncorrecte3=valeur
        db.session.commit()

    print("question",question)
    #pour confirme que tout s'est bien passe côté front
    reponse= jsonify(reponse="ok")
  
    return reponse