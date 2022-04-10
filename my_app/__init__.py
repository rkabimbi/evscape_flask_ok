#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy #import pour gestion DB
#from flask_migrate import Migrate, MigrateCommand #pour maj la DB sans tt perdre (ajouter colonne et autres)
from flask_login import LoginManager






app = Flask (__name__)
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







from my_app import routes