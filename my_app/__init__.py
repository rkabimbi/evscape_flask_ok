#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy #import pour gestion DB
#from flask_migrate import Migrate, MigrateCommand #pour maj la DB sans tt perdre (ajouter colonne et autres)
from flask_login import LoginManager

from flask_cors import CORS, cross_origin #important sans ca...il n'accepte pas les trucsAJAX!!! : https://flask-cors.readthedocs.io/en/latest/ 

from flask_mail import Mail



app = Flask (__name__)
CORS(app)
db=SQLAlchemy(app) #creation d'un objet de type SQLAlchemy
app.config.from_object(BaseConfig)
#migrate=Migrate(app,db)
print ("in init  : %s" %__name__)#afficher la valeur de main / pour savoir où on est
app.config['TEMPLATES_AUTO_RELOAD']=True



#gestion des login

#init du login manager

login_manager = LoginManager( app )
login_manager.login_view = "fonction_login" #ca c'est l'adresse de base si les gens essaye d'acceder à des pages securisée c'est à cette fonction là qui vont (qui affiche une page html)
login_manager.login_message_category = "info"
login_manager.login_message = "Vous ne pouvez pas acceder à cette page sans vous logguer. Veuillez taper un mdp/user correct" #si jamais on essaye d'acceder à une page direct ce message 'flash" apparaitra
login_manager.session_protection = 'strong'

#pour avoir plusieurs fichier routes!!!!
from my_app import routes
from my_app import routes_flux
from my_app import routes_mesJEEI
from my_app import routes_specificationMesJEEI
from my_app import routes_remplissageDB
from my_app import routes_mesExperimentations
from my_app import routes_uneExperimentation
from my_app import routes_listeParticipants
from my_app import routes_questionnairesParticipants
from my_app import routes_avis