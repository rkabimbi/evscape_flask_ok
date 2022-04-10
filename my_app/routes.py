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
from my_app.models.clue import Clue
from my_app.models.riddle import Enigmes, EnigmesJsn #import de la table (de la classe contenant la table)
from my_app.forms.RiddleForm import EnigmeForm, ReponseForm
from my_app.models.user import User

from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from my_app.forms.indicCreaForm import FormCreaInd

from my_app.forms.majForm import MajForm
from my_app.forms.majInd import MajInd
from flask import json, jsonify



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn


####################################################################################################################
####################################################################################################################
#CODE AVANT AJAX
####################################################################################################################
####################################################################################################################




#gere la page d'acceuil
@app.route("/", methods=['GET','POST'])
#login_required #pour obliger que l'utilisateur soit# log
def question(reponse=None):
    nbrEnigmes=Enigmes.query.count()
    return render_template("game.html",currentUser=current_user,nbrEnigmes=nbrEnigmes)


#gère la page creation d'enigme
@app.route("/CreationEnigme",methods=['GET','POST'])
@login_required #pour obliger que l'utilisateur soit log
def secret():  
    print("creationenigme")
    pageRetour= request.args.get('pageRetour')#recup dans URL la pagination de retour au niveau de la liste d'enigme
    print("page retour",pageRetour)
    formulaireNewEnigme=EnigmeForm()#instanciation de mon formulaire qui va recevoir les données entrées par l'utilisateur
    enigmesTemp=None
    if formulaireNewEnigme.validate_on_submit():#ca remplace l'ancienne verification sur le post (quand on utilise WTF) 
        print("Je cree l'enigme")
        questionRecup=formulaireNewEnigme.question.data
        reponseRecup=formulaireNewEnigme.reponse.data
        niveauRecup=formulaireNewEnigme.niveau.data
        catRecup=formulaireNewEnigme.categorie.data
        if questionRecup and reponseRecup : #si variable non Null
            print("j'ai recup et je cree")
            enigmesTemp = Enigmes(niveau=niveauRecup, question=questionRecup,reponse=reponseRecup,user_id=current_user.id,categorie=catRecup)# je cree un objet (#constructeur existe mais dans la pratique je prefere utiliser avec des "=")
            db.session.add(enigmesTemp)#on ajoute enigmets Temp à la DB
            db.session.commit()#on commit
            flash('Enigme créee', 'success')#si on arrive ici c'est que tout est ok -->on affiche un flash
            return redirect(url_for('gestionEnigmes',page=pageRetour))#retour à la liste d'enigmes (page = le nom utilisée dans la route AccesAdmin )
    return render_template("creaEnigme.html", enigmes=formulaireNewEnigme,currentUser=current_user,pageRetour=pageRetour)#affichage de la creaEnigme et je passe des argu que je pourrais recup en Jinja  


#gere la page infos
@app.route("/Infos",methods=['GET','POST'])
#@login_required #pour obliger que l'utilisateur soit log
def infos():
    return render_template("infos.html",currentUser=current_user)

#idem rangementDBEnigmenGen mais pour indice 
def rangementDbIndiceGen():
    listeIndicesActuels=Clue.query.all()
    increm=1
    for indiceEnCours in listeIndicesActuels:#iteration sur la liste des indices post effacement (indices pour chaque objet individuel contenu dans ma liste d'objet(Indice) lisyeIndicesActuels)
        indiceEnCours.id = increm #j'itere sur ma db et j'impose un increme qui evolue par step de 1
        db.session.commit()
        increm=increm+1
            
#gère la maj des enigmes
@app.route("/majEnigme", methods=['GET', 'POST'])
@login_required #pour obliger que l'utilisateur soit log
def maj_enigme():
    indexEnigmeRecup = request.args.get("enigme")#récupération de l'index de l'enigme 'dans l'url (get) 
    previousPage=request.args.get("paginationActu")#savoir de quelle page on vient
    print("previous Page :",previousPage)
    enigme=Enigmes.query.filter_by(id=indexEnigmeRecup).first()#on recuperer l'enigme sur base de l'index recup dans l'url 
    auteurEnigme=enigme.user_id#on recuperer l'id de l'auteur de l'enigme
    if current_user.id==auteurEnigme or current_user.admin:#si l'utilisateur courant est le même que l'enigem ou qu'il est admin(securite - empecher que qq d'autres que l'auteur puisse modifier ce qui appartient aux autres)
        formulairMaj=MajForm(question=enigme.question,reponse=enigme.reponse,niveau=enigme.niveau)#crea formulaire de maj pour lequel j'initialise les champs(c'est ca qui fait qu'on sait afficher les anciennes valeurs dans les champs du formulaire)
        if formulairMaj.validate_on_submit():#si validation du formulaire alors tu mets à jour l'enigme et tu la commit
            enigme.question=formulairMaj.question.data
            enigme.reponse=formulairMaj.reponse.data
            enigme.niveau=formulairMaj.niveau.data
            enigme.categorie=formulairMaj.categorie.data
            db.session.commit()   
            adresseretour="/ListeEnigmes?page="+previousPage#on forme l'adresse de retour
            flash('Engime mise-à-jour','success')
            return redirect(adresseretour)
        #si on a pas encore submit
        return render_template("majEnigme.html",currentUser=current_user,formMaj=formulairMaj,enigmeId=indexEnigmeRecup,pageRetour=previousPage,auteur=auteurEnigme)
    else:#si qq essaye de frauder la securité il retourne à la page d'où il vient (il ne voit pas la page de màj enigme)
        adresseretour="/ListeEnigmes?page="+previousPage#on forme l'adresse de retour
        return redirect(adresseretour)

#####################################################
#LOGIN
#####################################################


#gere les inscriptions
@app.route('/Inscription', methods=['POST', 'GET'])
def register():
    formInscr = FormRegister()#je creer mon formulaire qui est de type FormRegister
    if formInscr.validate_on_submit():
        email = formInscr.email.data
        username = formInscr.username.data
        password = formInscr.password.data
        birthday = formInscr.birthday.data 
        firstname = formInscr.firstname.data 
        lastname = formInscr.lastname.data
        admin=formInscr.admin.data  
        if User.query.filter_by(email=email).first():#verifier que l'email existe pas deja. Si je ne fais pas ça il va créer l'objet MAIS vu que dans la classe User j'ai bien mis que c'était unique ca va tt faire planter :D
            flash('Cette adresse email a déjà été utilisée', 'danger')
            return redirect(url_for('register'))#pour rediriger ves une fonction 
        if User.query.filter_by(username=username).first():#verifie que le username existe pas deja. Si je ne fais pas ça il va créer l'objet MAIS vu que dans la classe User j'ai bien mis que c'était unique ca va tt faire planter :
            flash('Ce nom d\'utilisateur a déjà été utilisé', 'danger')
            return redirect(url_for('register'))   #il retourne à register (et donc ne crée pas dans la db)
        password = generate_password_hash(password, "sha256")#si pas de probleme avec email ou username alors il crypte le code
        new_user = User(username=username,firstname=firstname, lastname=lastname,password=password,email=email, birthday=birthday, admin=True)#crée l'utilisateur (je n'utilise pas de constructeur . je trouce cela plus clair comme ceci
        db.session.add(new_user)#sauve dans la DB
        db.session.commit()
        flash('Enregistrement de profil bien opéré','success')
        return redirect(url_for('fonction_login'))   
    return render_template("inscription_form.html", formulaire=formInscr, current_user=None,currentUser=current_user)



#gere le login
@app.route("/login", methods=['GET', 'POST'])
def fonction_login():
    if current_user.is_authenticated:#si authentifie
        return redirect(url_for('question'))#alors tu peux aller à la page d'acceuil 
    formulaireLogin = FormLogin()#creation d'un objet de type FormLogin (formulaire WTF)
    if formulaireLogin.validate_on_submit():#si le formulaire a été submit**
        user = User.query.filter_by(username=formulaireLogin.username.data).first()#j'instancie user avec l'objet dont je recupere l'usrname dans le formulaire 
        if not user or not check_password_hash(user.password, formulaireLogin.password.data):#si la requete n'a rien renvoyé dans user (None)...càd il dit que pas d'utilisateur dans la db ou si code pas correct(code que je dois hasher vu qu'il est hashé dans la db)
            flash('Cet utilisateur n\'existe pas ou MDP incorrect','danger')
            return redirect(url_for('fonction_login')) 
        #dans les autres cas on peut logguer le perso
        login_user(user, remember=True) #remember ca sera utile pour ouvrir et fermer explorateur internet
        flash('Connexion réussie','success')
        return redirect(url_for('gestionEnigmes'))#alors tu peux aller à la page d'acceuil (c'est ce qui est demandé dans la spec (aller à la liste))
    return render_template("user_login.html", formulaire = formulaireLogin, current_user=None,currentUser=current_user)

#gere le logout
@app.route('/Logout')
def logout():
    logout_user()
    flash('Deconnexion réussie','success')
    return redirect(url_for('fonction_login'))


#####################################################
#INDICES
#####################################################


#gere le faite de pouvoir voir la liste des indices
@app.route("/voirIndice", methods=['GET', 'POST'])
@login_required #pour obliger que l'utilisateur soit log
def voir_indices():    
    indexEnigmeRecup = request.args.get("enigme")#recup de l'enigme dont on veut recup tt les indices 
    previousPage=request.args.get("paginationActu") #//TODO : si jamais il y a un probleme avec cette view function alors la remettre mais nrmlt elle ne sert à rien
    previousPageListeEnigme=request.args.get("paginationActuelle")#garder la page où on en était dans la liste des enigmes (pas des indices ((pour le bouton de retour qu'il retourne vers la bonne enigme qu'ilmporte la page d'indice)))
    pageActuelle= request.args.get("page")#recupere dans l'url la valeur de "page"
    enigme=Enigmes.query.filter_by(id=indexEnigmeRecup).first()#on recuperer l'enigme sur base de l'index recup dans l'url
    if current_user.id==enigme.user_id or current_user.admin:
        indices=Clue.query.filter(Clue.enigme_id==indexEnigmeRecup).all()#on fait une requete dans la table Clue. On prends tt les indices existants relatif à l'enigme dont l'index a été recupéré dans l'url (pr ensuite afficher la liste d'indices)
        tailleListeIndices=len(indices)
        nbrPages=math.ceil(tailleListeIndices/5)
        return render_template("voirIndice.html",currentUser=current_user,indices=indices,nbrPage=nbrPages,pageActuelle=pageActuelle,tailleListeInd=tailleListeIndices,enigme=enigme,previous=previousPage,previousPageListeEnigme=previousPageListeEnigme)#
    else:
        flash('Tu essayes de tricher en tapant qqch dans la barre d\'adresse!!! pas bien...tu ne peux pas y acceder', 'danger')
        return redirect(url_for('gestionEnigmes',page=previousPage))


#//TODO : ici j'ai mis un bete truc...à faire quand j'aurai reussi a ajouter des clue
@app.route("/majIndice", methods=['GET', 'POST'])
@login_required #pour obliger que l'utilisateur soit log
def maj_indices(): 
    pageRetourListeok=request.args.get("fpaginationActuelle")
    indexIndiceAModifier = request.args.get("index")#recup l'indice de l'indice
    previousPage=request.args.get("pagination")#recup page dans la liste pr revenir là où on etait
    idenigmeRecup = request.args.get("enigme")#récupération de la dans l'url (get) 
    paginationActuListe=request.args.get('paginationActuListe')
    indiceAModifier=Clue.query.filter_by(id=indexIndiceAModifier).first()#je prends l'index de l'indice à modifier et je m'en sert pour trouver l'indice en question
    enigme=Enigmes.query.filter_by(id=idenigmeRecup).first()#on recuperer l'enigme sur base de l'indice (pour recup ensuite l'auteur (pr securité))
    auteurEnigme=enigme.user_id#on recuperer l'id de l'auteur de l'enigme
    formMajIndic=MajInd(indice=indiceAModifier.indice)#formulaire avec champs prerempli par l'ancien indice (en argument)...je crée un objet de type formulaire avec un champs rempli de l'ancier indice
    if current_user.id==auteurEnigme or current_user.admin:#si l'utilisateur courant est le même que l'enigem ou qu'il est admin(securite)   
        if formMajIndic.validate_on_submit:
            indiceAModifier.indice=formMajIndic.indice.data#je mets à jour l'indice que je souhaitais modifier
            db.session.commit()
        #sinon j'affiche la page de màj de l'indice
        return render_template("majIndice.html",currentUser=current_user,formi=formMajIndic, indice=indiceAModifier , index=indexIndiceAModifier, paginationActu=previousPage, enigme=idenigmeRecup,paginationActuListe=paginationActuListe)
    else:#si tu tentes de mdofieir qch qui ne t'appartient pas --> tu retourne à la page d'où tu viens
        flash('Tu essayes de tricher en tapant qqch dans la barre d\'adresse!!! pas bien...tu ne peux pas y acceder', 'danger')
        adresseretour="/voirIndice?page="+previousPage+"&enigme="+idenigmeRecup+"&paginationActuListe="+paginationActuListe#on forme l'adresse de retour
        return redirect(adresseretour)


#gere la creation indice
@app.route("/CreerIndice", methods=['GET', 'POST'])
@login_required #pour obliger que l'utilisateur soit log
def creer_indices():
    pageRetourListeOk=request.args.get("fpaginationActuelle")
    indexEnigmeRecup = request.args.get("enigme")#recup de l'enigme dont on veut recup tt les indices
    pageRetourListe=request.args.get("paginationActu") #recupere la page d'où il vient (liste enigme)
    page= request.args.get("page")#continue de porter la page de retour à l'enigme!!! (pas l'indice!!!)C'est pr pouvoir revenir au bon endroit sur la liste d'enigme après etre d'abord passé sur la liste d'indice (on transporte l'info de saut en saut)
    enigme=Enigmes.query.filter_by(id=indexEnigmeRecup).first()#on recuperer l'enigme sur base de l'index recup dans l'url
    formCreaIndic=FormCreaInd()
    if formCreaIndic.validate_on_submit():#si validation du formulaire alors tu mets à jour l'enigme et tu la commit
        indice=formCreaIndic.indice.data
        enigmeid= enigme.id#je dis à quelle enigme cet indice est lié
        indiceTemp=Clue(indice,enigmeid)#constructeur de indice
        db.session.add(indiceTemp)
        db.session.commit()
        page= request.args.get("paginationActuListe")#chipotage je sais :D désolé (je fais ca pour transporter la bonne page de retour vers page enigme)...j'ai mélangé l'utilisation des noms de variables (là je vois clair et je sais que c'est bon :D)
        adresseRetour="/voirIndice?page="+pageRetourListe+"&paginationActu="+pageRetourListe+"&enigme="+indexEnigmeRecup+"&paginationActuListe="+page
        flash('Nouvel indice crée','success')
        print(indiceTemp)
        return redirect(adresseRetour)#quand on a posté la new enigme on retourne dans la grille 
    return render_template("creaIndice.html",currentUser=current_user, enigme=enigme, formu=formCreaIndic,pageRetour=pageRetourListe,page=page,pageRetourListeOk=pageRetourListeOk)




#gere la suppression des indices
@app.route("/SupprimeIndice",methods=['GET','POST'])
@login_required #pour obliger que l'utilisateur soit log
def supprimeIndice(): 
    indexIndiceASupprimer = request.args.get("idIndice")#recup l'indexde l'indice
    previousPage=request.args.get("paginationActu")#recup page dans la liste pr revenir là où on etait
    indexEnigmeEnLien=request.args.get("enigme")#index de l'enigme en lien avec indice
    pageRetourListeEnigme=request.args.get("paginationActuListe")#pour continuer à porter de clic en clic l'endroit où je dois retourner dans la liste des enigmes
    indiceAEffacer=Clue.query.filter_by(id=indexIndiceASupprimer).first()
    db.session.delete(indiceAEffacer)#j'efface
    db.session.commit()
    flash('Indice éffaceé','success')
    rangementDbIndiceGen()
    adresseDeRetour="/voirIndice?paginationActu="+str(previousPage)+"&enigme="+indexEnigmeEnLien+"&paginationActuListe="+pageRetourListeEnigme#je cree une adresse avec la pagination où on était avant d'avoir cliqué sur supprimer
    return redirect(adresseDeRetour)  



########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
#CODE AVEC AJAX
########################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################



#####################################################
#INCREM DECREM AJAX
#####################################################

#fonction qui valide ou non le fait qu'on peut décrementer
@app.route("/incremDecrem",methods=['GET','POST'])
@login_required #pour obliger que l'utilisateur soit log
def incremDecrem():
    paginationActuelle = request.args.get("fpaginationActuelle")#recup les données envoyée pdepuis JS
    incremBool = request.args.get("fincremBool") 
    print(incremBool)
    numEnigme = request.args.get("fnumEnigm")
    print(numEnigme)
    enigme=Enigmes.query.filter_by(id=numEnigme).first()
    print("enigme de base : " , enigme)
    if incremBool=="True" and enigme.niveau<5:
        enigme.niveau=enigme.niveau+1
        print("increm")
        message="Modification du niveau ok"#message qu'on passe dans JSON vers JS pour afficher un flash
    elif incremBool=="False" and enigme.niveau>0:
        enigme.niveau=enigme.niveau-1
        print("decrem")
        message="Modification du niveau ok"#message qu'on passe dans JSON vers JS pour afficher un flash
    else:
        print("op interdite")
        message="Modification du niveau hors seuil"#message qu'on passe dans JSON vers JS pour afficher un flash
    db.session.commit()
    print("new enigme :",enigme)
    print("renvoi jsnon")
    #je fais tout ce qui suit car j'aurai besoin de ses données pour envoyer mon JSON et afficher ma liste d'enogme à nouveau
    listeEnigmeResiduelle=Enigmes.query.all()#je mets tte les enigmes de la db dans listeEnigmes (pour renvoyer ça par JSON à JS et qu'il puisse gerer l'affichage)
    nbrEnigmesResiduelles=Enigmes.query.count()
    #s'apprète à renvoyer la nouvelle DB côté client
    listeEnigmeResiduelle=conversionSQLJSON(listeEnigmeResiduelle,nbrEnigmesResiduelles)#transforme ma requete sql en qqch de serialisable par json
    listeUsers=User.query.all()
    nbrUsers=User.query.count()
    listeUsersSerialisable=conversionSQLJSONListeUser(listeUsers,nbrUsers)

    return jsonify(listeEnigmes=listeEnigmeResiduelle,paginationActuelle=paginationActuelle,admin=current_user.admin,listeUsers=listeUsersSerialisable,message=message)#je cree un objet json contenant l'information nécéssaire

#####################################################
#SUPPRESSION AJAX
#####################################################

@app.route("/supprimeEnigme",methods=['GET','POST'])
@login_required #pour obliger que l'utilisateur soit log
def supprimeEnigme():
    
    print("route - supprimeEnigme")
    paginationActuelle = request.args.get("fpaginationActuelle") #recup les données envoyée par mon fichier JS

    numEnigme = request.args.get("fnumEnigm")
    print("num Enigme reçu de JS : ",numEnigme)
    enigmeAEffacer=Enigmes.query.filter_by(id=numEnigme).first()#je recupere l'element à effacer
    if current_user.id==enigmeAEffacer.user_id or current_user.admin:
        print("Dans le if")
        nbrAvantEffacement=Enigmes.query.count()
        if(nbrAvantEffacement>2):
            db.session.delete(enigmeAEffacer)#j'efface
            db.session.commit()
            rangementDbEnigmeGen2()
            rangementDbIndiceGen2()
        else:#si avant effacement il reste <2enigmes alors on n'efface pas (j'ai fait ca sinon ca pete le jeu vu qu'on sait pas repeter deux enigmes à la suite)
            print("Vous n'êtes pas autorisé à supprimer cas pas assez d'enigmes dans la DB")
            #je fais tout ce qui suit car j'aurai besoin de ses données pour envoyer mon JSON et afficher ma liste d'enogme à nouveau
            listeEnigmeResiduelle=Enigmes.query.all()#je mets tte les enigmes de la db dans listeEnigmes (pour renvoyer ça par JSON à JS et qu'il puisse gerer l'affichage)
            nbrEnigmesResiduelles=Enigmes.query.count()#obligé car je ne parviens pas à recup la taille via len()
            #s'apprète à renvoyer la nouvelle DB côté client
            listeEnigmeResiduelle=conversionSQLJSON(listeEnigmeResiduelle,nbrEnigmesResiduelles)#transforme ma requete sql en qqch de serialisable par json
            listeUsers=User.query.all()
            nbrUsers=User.query.count()
            listeUsersSerialisable=conversionSQLJSONListeUser(listeUsers,nbrUsers)
            return jsonify(listeEnigmes=listeEnigmeResiduelle,paginationActuelle=paginationActuelle,admin=current_user.admin,listeUsers=listeUsersSerialisable,message="Suppression interdite")
        listeEnigmeResiduelle=Enigmes.query.all()#je mets tte les enigmes de la db dans listeEnigmes (pour renvoyer ça par JSON à JS et qu'il puisse gerer l'affichage)
        nbrEnigmesResiduelles=Enigmes.query.count()#obligé car je ne parviens pas à recup la taille via len()
        #s'apprète à renvoyer la nouvelle DB côté client
        listeEnigmeResiduelle=conversionSQLJSON(listeEnigmeResiduelle,nbrEnigmesResiduelles)#transforme ma requete sql en qqch de serialisable par json
        listeUsers=User.query.all()
        nbrUsers=User.query.count()
        listeUsersSerialisable=conversionSQLJSONListeUser(listeUsers,nbrUsers)
        #recalcul la page si on avait plusieurs pages et qu'en diminuant on a effacé une page, gra^ce à ceci -->on ne revient pas dessus
        if (nbrEnigmesResiduelles % 5) ==0 and int(paginationActuelle)>1 :#pagination!=1 c'est pr eviter qu'il me sorte une page à 0 qui n'existe pas #si le nbr de page modulo 5==0 ca veut dire que qd en réduisant on est arrivé à l'interval inferieur. Ex: 11 enigmes - 3 pages, je supprime j'ai 10 enigmes et effectivement 10mod5 = 0...ca veut dire que je doit retourner non pas sur la page de base (3) mais sur la page 2 (3-1)
            paginationActuelle=int(paginationActuelle)-1
        x= jsonify(listeEnigmes=listeEnigmeResiduelle,paginationActuelle=paginationActuelle,admin=current_user.admin,listeUsers=listeUsersSerialisable,message="Suppression Ok")#je cree un objet json contenant l'information nécéssaire

        print("Jsnonify a fonctionne")
        return x
    else:#si utilisateur pas autorisé à effacer [OBSOLETE  ]
        print("Vous n'êtes pas autorisé à supprimer car vous n'avez pas les droits")
        #je fais tout ce qui suit car j'aurai besoin de ses données pour envoyer mon JSON et afficher ma liste d'enogme à nouveau
        listeEnigmeResiduelle=Enigmes.query.all()#je mets tte les enigmes de la db dans listeEnigmes (pour renvoyer ça par JSON à JS et qu'il puisse gerer l'affichage)
        nbrEnigmesResiduelles=Enigmes.query.count()
        #s'apprète à renvoyer la nouvelle DB côté client
        listeEnigmeResiduelle=conversionSQLJSON(listeEnigmeResiduelle,nbrEnigmesResiduelles)#transforme ma requete sql en qqch de serialisable par json
        listeUsers=User.query.all()
        nbrUsers=User.query.count()
        listeUsersSerialisable=conversionSQLJSONListeUser(listeUsers,nbrUsers)
        return jsonify(listeEnigmes=listeEnigmeResiduelle,paginationActuelle=paginationActuelle,admin=current_user.admin,listeUsers=listeUsersSerialisable,message="Suppression interdite")

#range la DB (après effacement) de sorte à eviter les trous en décalant tt les indices des éléments à l'ID supérieur de 1 vers le bas
def rangementDbEnigmeGen2():
    listeEnigmeActuels=Enigmes.query.all()#je recupere tt les enigmes
    increm=1#init de increm à 1
    for enigmeEnCours in listeEnigmeActuels:#iteration sur la liste des indices post effacement (indices pour chaque objet individuel contenu dans ma liste d'objet(Indice) lisyeIndicesActuels)  
        #je dois modifier l'indice aussi de tt mes indices liés (sinon ils référenceront un autre enigme :D)
        for indice in enigmeEnCours.r_indice:
            indice.enigme_id= increm#je mets la nouvelle référence (id) d'enigme dans les indices liés à cet enigme
            db.session.commit()
        #je fais le changement d'increment de l'enigme après sinon forcement je ne modifie pas les bons indices :D
        enigmeEnCours.id = increm #j'itere sur ma db et j'impose un increme qui evolue par step de 1
        db.session.commit()
        increm=increm+1

#idem rangementDBEnigmenGen mais pour indice
def rangementDbIndiceGen2():
    listeIndicesActuels=Clue.query.all()
    increm=1
    for indiceEnCours in listeIndicesActuels:#iteration sur la liste des indices post effacement (indices pour chaque objet individuel contenu dans ma liste d'objet(Indice) lisyeIndicesActuels)
        indiceEnCours.id = increm #j'itere sur ma db et j'impose un increme qui evolue par step de 1
        db.session.commit()
        increm=increm+1

#converti l'objet "sql" en dictionnaire qui est un format qui peut etre jnsonifié(question de serialisation)
def conversionSQLJSON(listeEnigmes,nbrEnigmes):
    #init de mon dictionnaire
    listeEnigmesSerialisee={"id":[],"niveau":[],"question":[],"reponse":[],"user_id":[],"r_indice":[],"categorie":[]}
    
    for enigme in range(0,nbrEnigmes):  
        listeEnigmesSerialisee["id"].append(listeEnigmes[enigme].id)
        print("Instanciation enigme N°",listeEnigmesSerialisee["id"])
        listeEnigmesSerialisee["niveau"].append(listeEnigmes[enigme].niveau)
        print("niveau ",listeEnigmesSerialisee["niveau"])
        listeEnigmesSerialisee["categorie"].append(listeEnigmes[enigme].categorie)
        print("categorie ",listeEnigmesSerialisee["categorie"])
        listeEnigmesSerialisee["question"].append(listeEnigmes[enigme].question)
        print("question ",listeEnigmesSerialisee["question"])
        listeEnigmesSerialisee["reponse"].append(listeEnigmes[enigme].reponse)
        print("reponse ",listeEnigmesSerialisee["reponse"])
        listeEnigmesSerialisee["user_id"].append(listeEnigmes[enigme].user_id)
        print("user_id ",listeEnigmesSerialisee["user_id"])
        #si j'ai des indices dans la liste attachée alors je donne True à cette valeur booleene comme ca il l'indique sur la liste
        if(listeEnigmes[enigme].r_indice):
            listeEnigmesSerialisee["r_indice"].append("True")
        else :
            listeEnigmesSerialisee["r_indice"].append("False")      
        print("r_indice ",listeEnigmesSerialisee["r_indice"])
    print("------verification liste renvoyée----------")
    print(listeEnigmesSerialisee)

    return listeEnigmesSerialisee

#####################################################
#GAME1 AJAX
#####################################################


#quand je clique sur le menu Game2
@app.route("/game1",methods=['GET','POST'])
def jouer():

    nbrEnigmes=Enigmes.query.count()
    return render_template("game.html",currentUser=current_user,nbrEnigmes=nbrEnigmes)

#va chercher l'enigme tirée au hasard au niveau du serveur
@app.route("/selectEnigme",methods=['GET','POST'])
def selectEnigme():
    print("dans selectEnigme")
    numEnigme = request.args.get("fnbrHasard") #recup les données envoyée par mon fichier JS
    print(numEnigme)
    lienClique = request.args.get("flienClique") #pour pouvoir passer le fait que l'utilisateur a cliqué le bouton "nouvelle enigme" ou a bien répondu (c'est important dans mon calcul de point js)
    print(lienClique)
    enigme=Enigmes.query.filter_by(id=numEnigme).first()
    print(enigme)
    #renvoi en JSNPN les informations de l'enigmeb+le fait de savoir si il a cliqué le lien ou si il a bien répondu à la question (lien clique)
    return jsonify(id=enigme.id,question=enigme.question, reponse=enigme.reponse,lienClique=lienClique)

validationAcces=False
#verifie la correspondance entre deux réponses (sans tenir compte de la casse)
@app.route("/verifReponse",methods=['GET','POST'])
def verificationReponse() :
    global validationAcces
    print("VerificationReponse")
    questionPosee=request.args.get("fenigmeActu") #recup la question possee
    repUsMaj=request.args.get("freponseUser")#recup reponse de l'utilisateur
    scoreCons=int(request.args.get("fscoreCons"))#recup le score consecutif
    enigme=Enigmes.query.filter_by(question=questionPosee).first()#je recupere la question possee pr ensuite recup la reponse
    repCorMaj=enigme.reponse#je recup la reponse
    print("qPosee :",questionPosee,"repUs :",repUsMaj,"repCor :",repCorMaj)
    #rendre les reponses insensibles à la casse
    repCorMaj=repCorMaj.upper() 
    repUsMaj= repUsMaj.upper()
    nbrEnigmes=Enigmes.query.count()#je recupere la taille de la DB actuelle pcq j'en ai besoin pr qu'il puisse lancer une new question
    if repCorMaj==repUsMaj:
        print("reponse correcte")     
        print("scoreCons :",scoreCons)
        scoreCons=scoreCons+1#increment le scoreconsecuti cote serveur
        print("scoreCons :",scoreCons)
        if(scoreCons==3):#si score est 3 alors je mets à jour la variable globale validationAcces et on sait qu'il peut avoir accès à game-2
            print("validationAces :",validationAcces)
            validationAcces=True
            print("validationAces :",validationAcces)
        return jsonify(rep="True",nbrEnigmes=nbrEnigmes)
    else :
        print("reponse incorecte")
        return jsonify(rep="False",nbrEnigmes=nbrEnigmes)



@app.route("/game-2",methods=['GET','POST'])
def affichageGame2() :
    print("AFFICHAGE GAME 2 validationAces :",validationAcces)
    if not validationAcces:
        print("not")
        message="Petit tricheur...tu dois repondre à 3 enigmes à la suite"
    else:
        print("ok")
        message="MMMMmmm je vous attendais"
        
    return render_template("game2.html",currentUser=current_user,message=message)

#####################################################
#ListeEnigmes
#####################################################
@app.route("/ListeEnigmes",methods=['GET','POST'])
@login_required 
def gestionEnigmes() :
    print("Gestion Enigmes")
    paginationActuelle=request.args.get("page")#ancienne methode (avant AJAX). C'est pr quand on revient d'une page de màj ou suppression
    print("pagination :",paginationActuelle)
    if not paginationActuelle: #a l'init c'est le seul moment où ca arrive (après quand tu voyages dans la page ca ne l'est plus jamais)
        paginationActuelle=1
    return render_template("listeEnigmes.html",paginationActuelle=paginationActuelle, currentUser=current_user) 


#envoi coté client en JSON tte les enigmes pr qu'on puisse les gerer cote clients
@app.route("/EnvoiEnigmes",methods=['GET','POST'])
@login_required 
def envoiEnigmes() :
    print("Envoi Enigmes")
    paginationActuelle=request.args.get("fpaginationActuelle")
    print("pagination =",paginationActuelle)
    listeEnigmes=Enigmes.query.all()#je recupere tt les enigmes
    nbrEnigmes=Enigmes.query.count()
    #fonction crée pr transformer notre objet de la DB en format qui soit serialisable/jsonisable (un dict ici)
    listeEnigmesSerialisable=conversionSQLJSON(listeEnigmes,nbrEnigmes)
    listeUsers=User.query.all()
    nbrUsers=User.query.count()
    #fonction crée pr transformer notre objet de la DB en format qui soit serialisable/jsonisable (un dict)
    listeUsersSerialisable=conversionSQLJSONListeUser(listeUsers,nbrUsers)
    print(current_user.admin)
    print("tout se passe avec succes avant JSNOIFY")
    listeJsonifiee= jsonify(listeEnigmes=listeEnigmesSerialisable,admin=current_user.admin,paginationActuelle=paginationActuelle,listeUsers=listeUsersSerialisable)#admin c'est pour savoir si l'utilisateur est admin et donc ce qu'on peut ou pas afficher
    print("liste enigmes jsonifiee - succes")
    return listeJsonifiee
    



#convertit les utilisateurs en dict
def conversionSQLJSONListeUser(listeUsers,nbrUsers):
    print("conversion liste user vers JSON")
    print("nbr users =", nbrUsers)
    #instanciation du dictionnaire
    listeUsersSerialisee={"id":[],"username":[]}
    #parcours de la liste d'utilisateur passé en param
    for user in range(0,nbrUsers):
        #je mets dans mon dictionnare la valeur d'id pour le user-ième element
        listeUsersSerialisee["id"].append(listeUsers[user].id)
        print("Instanciation user N°",listeUsersSerialisee["id"])
        listeUsersSerialisee["username"].append(listeUsers[user].username)
        print("username ",listeUsersSerialisee["username"])
    print("------verification liste renvoyée----------")
    print(listeUsersSerialisee)
    return listeUsersSerialisee


#le prog tourne avec min 2 enigmes (pas eu le temps d'implémenter le cas où moins de 2 enigmes donc on crée min 2 exemples)
if User.query.count()==0:
    dateNaissance=date(2020,1,1)
    print(dateNaissance)
    userTemp=User(username="example", firstname="exampleFirstName", lastname="exampleLastname",password="example",email="example@viciousgame.be",birthday=dateNaissance,admin=True)
    db.session.add(userTemp)#on ajoute enigmets Temp à la DB
    db.session.commit()#on commit
while Enigmes.query.count()<2:
    enigmesTemp = Enigmes(niveau=0, question="exempleQuestion1",reponse="exxempleReponse1",user_id=1,categorie=None)# je cree un objet (#constructeur existe mais dans la pratique je prefere utiliser avec des "=")
    db.session.add(enigmesTemp)#on ajoute enigmets Temp à la DB
    db.session.commit()#on commit













