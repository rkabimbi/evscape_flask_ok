##########################################################
#mes imports
##########################################################

from cgi import test
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
from my_app.models.jeei_package.questionApprentissage import QuestionApprentissage


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

    utilisateur=User(username="rootroot",firstname="Rudy",lastname="KABIMBI",password=generate_password_hash("rootrootroot", "sha256"),email="rudykabimbi@evscApp.edu",titre="chercheur",universite="Unamur")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()
    utilisateur=User(username="gyernaux",firstname="Gonzague",lastname="Yernaux",password=generate_password_hash("rootrootroot", "sha256"),email="gonzagueyernaux@evscApp.edu",titre="assistant",universite="Unamur")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()
    utilisateur=User(username="bvandezande",firstname="Bart",lastname="Vandezande",password=generate_password_hash("rootrootroot", "sha256"),email="bvandz@kul.com",titre="assistant",universite="KUL")
    db.session.add(utilisateur)#sauve dans la DB
    db.session.commit()








    #CREA De JEEI
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=500,dureeMinutes=150, publicCible=PublicCible.MASTER,theme=Theme.MATHEMATIQUE,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Logique propositionelle",statut=Statut.ENCOURS,documentation='')
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=3,nbrJoueursMin=2,budget=5500,dureeMinutes=120, publicCible=PublicCible.PRIMAIRE,theme=Theme.SECURITEIT,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="chiffrement de cesar",statut=Statut.ENCOURS,documentation='')
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=8,nbrJoueursMin=1,budget=1500,dureeMinutes=60,statut=Statut.PRET, publicCible=PublicCible.SECONDAIRE,theme=Theme.INGENIRIELOGICIEL,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Diagramme de classe",documentation='')

    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=850,dureeMinutes=100, publicCible=PublicCible.MASTER,theme=Theme.ALGORITHMIE,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Recursivité",statut=Statut.ENCOURS,documentation='')
    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=4,nbrJoueursMin=2,budget=500,dureeMinutes=150,statut=Statut.PRET, publicCible=PublicCible.BACCALAUREAT,theme=Theme.PROGRAMMATION,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Orienté objet",documentation='')

    db.session.add(specification)#sauve dans la DB
    db.session.commit()
    specification= Specification(nbrJoueursMax=18,nbrJoueursMin=2,budget=2800,dureeMinutes=150, publicCible=PublicCible.BACCALAUREAT,theme=Theme.ALGORITHMIE,scenario="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pellentesque mollis nisi ut maximus. Duis convallis volutpat erat, vel quis.",chapitre="Complexité",statut=Statut.ENCOURS,documentation='')

    db.session.add(specification)#sauve dans la DB
    db.session.commit()


    jeei=Jeei(nom="DesKape",img="static/img/img1.png",descriptif="Retrouvez les copies d'examen",fk_SpecificationId=1,fk_UserId=1)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Unbox",img="static/img/img2.png",descriptif="Les poupées russes vous feront perdre la tête",fk_SpecificationId=2,fk_UserId=2)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="The green house",img="static/img/img3.png",descriptif="Un jeu qui vous en fera voir de toutes les couleursimg",fk_SpecificationId=3,fk_UserId=1)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Algorithmo Express",img="static/img/img4.png",descriptif="Entrez dans les méandres de la récursivité",fk_SpecificationId=4,fk_UserId=1)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="The Stranger Things",img="static/img/img5.png",descriptif="Inspirez de la série TV",fk_SpecificationId=5,fk_UserId=2)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()

    jeei=Jeei(nom="Descape Basics",img="static/img/img6.png",descriptif="Un jeu simple mais éfficace",fk_SpecificationId=6,fk_UserId=2)
    db.session.add(jeei)#sauve dans la DB
    db.session.commit()



    #crea questionApprentissage

    
    for i in range(1,7):
    
        for q in range(1,11):
            question = QuestionApprentissage(question="Question"+str(q)+"Spec"+str(i),solutionCorrecte="Reponse"+str(q)+"Spec"+str(i), solutionIncorrecte1="responseA", solutionIncorrecte2="reponseB",solutionIncorrecte3="reponseC",explicatif="tu aurais dû mieux faire",fk_SpecificationID=i)
            db.session.add(question)
            db.session.commit()

        

#lancement de la fonction
function_lancementDBFictive()