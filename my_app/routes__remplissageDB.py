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




from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from flask import json, jsonify

from my_app.models.user import User

from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()


from my_app.models.jeei_package.jeei import Jeei

from my_app.models.jeei_package.specification import Specification, Statut, Theme, PublicCible

"""
Pour rappel le fonction de flask c'est qu'à chaque changement il reparcours tt le fichier je pense. Notament pour le login.
Je pens donc que je dois laisser la racine à la page "home" et juste faire sur le chemin racine que si pas connecté il renvoi la page login!!!!
comme ca quand mon formulaire de wtf est validé ca va repasser par la racine
"""




#####################################################
#REMPLIASSAGE DB (à effacer à la fin)
#####################################################

def function_lancementDBFictive():
    db.drop_all()
    db.create_all()

    utilisateur=User(username="rootroot",firstname="Brandon",lastname="Walsh",password=generate_password_hash("rootrootroot", "sha256"),email="BrandoWalsh@BeverlyHills90210.com")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()
    utilisateur=User(username="prudence",firstname="Nick",lastname="Carter",password=generate_password_hash("rootrootroot", "sha256"),email="NickCarter@BackstreeBoys.com")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()
    utilisateur=User(username="BSpears",firstname="Britney",lastname="Spears",password=generate_password_hash("rootrootroot", "sha256"),email="brittney@yahoo.com")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()

    #CREA De JEEI
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=500,dureeMinutes=150, publicCible=PublicCible.MASTER,theme=Theme.MATHEMATIQUE,scenario="scenario de test",chapitre="chapitre test",statut=Statut.ENCOURS,documentation='')
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=3,nbrJoueursMin=2,budget=58500,dureeMinutes=120, publicCible=PublicCible.PRIMAIRE,theme=Theme.SECURITEIT,scenario="scenario de test1",chapitre="chiffrement de cesar",statut=Statut.ENCOURS,documentation='')
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=8,nbrJoueursMin=1,budget=1500,dureeMinutes=60,statut=Statut.PRET, publicCible=PublicCible.SECONDAIRE,theme=Theme.INGENIRIELOGICIEL,scenario="scenario de test2",chapitre="Modelisation",documentation='')

    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=50850,dureeMinutes=100, publicCible=PublicCible.MASTER,theme=Theme.ALGORITHMIE,scenario="scenario de test3",chapitre="preuve",statut=Statut.ENCOURS,documentation='')
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=500,dureeMinutes=150,statut=Statut.PRET, publicCible=PublicCible.BACCALAUREAT,theme=Theme.PROGRAMMATION,scenario="scenario de test",chapitre="chapitre test",documentation='')

    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=18,nbrJoueursMin=2,budget=25800,dureeMinutes=150, publicCible=PublicCible.BACCALAUREAT,theme=Theme.ALGORITHMIE,scenario="scenario de test",chapitre="ce que tu veux",statut=Statut.ENCOURS,documentation='')

    db.session.add(specification)#sauve dans la DB
    db.session.commit()


    jeei=Jeei(nom="Descape The Real Deal",img="static/img/imgLoginPage2.png",descriptif="le meilleur EG de tous les temps",fk_SpecificationId=1)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Unbox",img="static/img/JEEITest1.jpeg",descriptif="le meilleur EG de tous les temps1",fk_SpecificationId=2)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Welcome to the hood",img="static/img/JEEITest2.jpeg",descriptif="le meilleur EG de tous les temps1",fk_SpecificationId=3)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Castramix",img="static/img/JEEITest1.jpeg",descriptif="le meilleur EG de tous les temps3",fk_SpecificationId=4)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="The Stranger Thhings",img="static/img/imgLoginPage2.png",descriptif="le meilleur EG de tous les temps4",fk_SpecificationId=5)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Descape Basics",img="static/img/JEEITest1.jpeg",descriptif="le meilleur EG de tous les temps5",fk_SpecificationId=6)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()


#lancement de la fonction
function_lancementDBFictive()