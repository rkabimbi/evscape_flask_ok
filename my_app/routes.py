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


#lancement de la fonction
function_lancementDBFictive()



######################################################

#gere le login
@app.route("/", methods=['GET', 'POST'])
def fonction_login():
    if current_user.is_authenticated:#si authentifie
        return redirect(url_for('fonction_flux'))#alors tu peux aller à la page d'acceuil 
    formLogin = FormLogin()#creation d'un objet de type FormLogin (formulaire WTF)
    if formLogin.validate_on_submit():#si le formulaire a été submit**
        user = User.query.filter_by(username=formLogin.username.data).first()#j'instancie user avec l'objet dont je recupere l'usrname dans le formulaire 
        print(user)
        if not user or not check_password_hash(user.password, formLogin.password.data):#si la requete n'a rien renvoyé dans user (None)...càd il dit que pas d'utilisateur dans la db ou si code pas correct(code que je dois hasher vu qu'il est hashé dans la db)
            flash('Cet utilisateur n\'existe pas ou MDP incorrect','danger')
            return redirect(url_for('fonction_login')) 
        #dans les autres cas on peut logguer le perso
        login_user(user, remember=True) #remember ca sera utile pour ouvrir et fermer explorateur internet
        flash('Connexion réussie','success')
        return redirect(url_for('fonction_flux'))#alors tu peux aller à la page d'acceuil (c'est ce qui est demandé dans la spec (aller à la liste))
    formInscr = FormRegister()# c'est un hack sinon ca marche pas le truc facon SPA(DONC NE PAS RETIRER!!!JAMAIS)
    return render_template("user_login.html", formulaireLogin = formLogin,currentUser=current_user, formulaireInscription=formInscr)

#gere le logout
@app.route('/Logout')
@login_required
def logout():
    logout_user()
    flash('Deconnexion réussie','success')
    return redirect(url_for('fonction_login'))



@app.route("/inscription", methods=['GET', 'POST'])
def fonction_inscription():
    formInscr = FormRegister()#je creer mon formulaire qui est de type FormRegister
    if formInscr.validate_on_submit():
        email = formInscr.email.data
        username = formInscr.username.data
        password = formInscr.password.data
        
        firstname = formInscr.firstname.data 
        lastname = formInscr.lastname.data
        
        if User.query.filter_by(email=email).first():#verifier que l'email existe pas deja. Si je ne fais pas ça il va créer l'objet MAIS vu que dans la classe User j'ai bien mis que c'était unique ca va tt faire planter :D
            flash('Cette adresse email a déjà été utilisée', 'danger')
            print('Erreur inscription email')
            return redirect(url_for('fonction_inscription'))#pour rediriger ves une fonction 
        if User.query.filter_by(username=username).first():#verifie que le username existe pas deja. Si je ne fais pas ça il va créer l'objet MAIS vu que dans la classe User j'ai bien mis que c'était unique ca va tt faire planter :
            flash('Ce nom d\'utilisateur a déjà été utilisé', 'danger')
            print('Erreur inscription utilisateur existant')
            return redirect(url_for('fonction_inscription'))   #il retourne à register (et donc ne crée pas dans la db)
        password = generate_password_hash(password, "sha256")#si pas de probleme avec email ou username alors il crypte le code"""
        
        new_user = User(username=username,firstname=firstname, lastname=lastname,password=password,email=email)#crée l'utilisateur (je n'utilise pas de constructeur . je trouce cela plus clair comme ceci
        print('utilisateur sauvé!!!!!!!')
        db.session.add(new_user)#sauve dans la DB
        db.session.commit()
        flash('Enregistrement de profil bien opéré','success')
    return redirect(url_for('fonction_login'))   











