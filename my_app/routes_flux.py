##########################################################
#mes imports
##########################################################

from cmath import sqrt
from sqlalchemy import false
from my_app import app
from flask import Flask, redirect
from flask import request
from flask import render_template
from jinja2 import Template
from jinja2 import Environment, PackageLoader
from jinja2 import environment
from random import randint
import math

from my_app import db
from my_app.models.evaluation import Evaluation
from my_app.models.jeei_package.jeei import Jeei
from my_app.models.jeei_package.questionApprentissage import QuestionApprentissage
from my_app.models.jeei_package.specification import Specification
from my_app.models.participant import Participant
from my_app.models.questionnaireMotivation import QuestionnaireMotivation
from my_app.models.questionnairePreTest import QuestionnairePreTest #import de la db
from my_app.models.questionnairePostTest import QuestionnairePostTest #import de la db

from my_app.models.user import User

from my_app.forms.loginForm import FormLogin
from my_app.forms.registerForm import FormRegister
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from flask import json, jsonify
from my_app.routes_specificationMesJEEI import verificationComplet
from my_app.models.questionnaireUX import QuestionnaireUX
import sys
import xlsxwriter
import statistics



from datetime import date
#from dateutil.relativedelta import *#pour calculer age

#from my_app.models.riddleJSN import EnigmesJsn
#db.drop_all()

ligneExel=0 





@app.route("/flux", methods=['GET', 'POST'])
@login_required
def fonction_flux():
    resultats=fonction_calculResultats()
    print(resultats)
    #sys.exit()
    return render_template("flux.html",currentUser=current_user,resultats=resultats)

def fonction_calculResultats():
    resultats={
        "INDQ11A":0,
        "INDQ11B":0,
        "nbrParticipantsExp":0,
        "nbrParticipantsTem":0,
        "INDQ14":0,
        "INDQ23DA":0,
        "INDQ13A":0,
        "INDQ13B":0,
        "INDQ12A":0,
        "INDQ12B":0


    }
    
    #je recupere tte les evaluations et les classes selon que ce soit experimental ou pas
    evaluations=Evaluation.query.all()
    evalExp=[]#ensemble des eval relative au groupe Experimental
    evalTem=[]
    for evaluation in evaluations:
        print("evaluation num : ",evaluation.id, " cocnerne participant ",evaluation.fk_ParticipantId)
        #verifiier que l'evaluation est complete
        questionnaireMotivation=QuestionnaireMotivation.query.filter_by(id=evaluation.fk_QuestionnaireMotivationId).first()
        questionnaireUX=QuestionnaireUX.query.filter_by(id=evaluation.fk_QuestionnaireUXId).first()
        participant=Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
        evalComplete=verificationComplet(questionnaireMotivation, questionnaireUX,participant)#fct definie dans routes_specificationMesJEEI
        evalCompleteComplement=fonction_verificationCompletComplement(evaluation)
        #je ne verifie pas les resultats d'apprentissage car si abstention ou rien rempli pour qq elements alors ca vaut juste un 0 (qq peut s'bastenir sur tt car rien compris)


        #si complete alors
        if (evalComplete and evalCompleteComplement):
            participant=Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
            print("participant", participant.id, " ", participant.prenom," ", participant.nom )
            if participant.groupeExperimental:
                evalExp.append(evaluation)
            else:
                evalTem.append(evaluation)
    

    #pour chacun des groupes cree je calcul l'evolution moyenne des resultats
    print(evalExp)
    print(evalTem)
    nbrTotalEvalExp=len(evalExp)
    nbrTotalEvalTem=len(evalTem)
    resultats["nbrParticipantsExp"]=nbrTotalEvalExp
    resultats["nbrParticipantsTem"]=nbrTotalEvalTem
  

    #pour chaque évaluation du groupeExp
    evolutionApprentissageGlobalRelativeExp=0
    evolutionApprentissageGlobalRelativeTem=0

    workbook = xlsxwriter.Workbook('resultatsEvscape.xlsx')
    worksheetTem = workbook.add_worksheet() 
    worksheetExp = workbook.add_worksheet()
    global ligneExel


    for evaluation in evalExp:
        print("traitement new eval Exp")
        #je vais chercher les resultats du pre-test
        totalPreTest=fonction_CalculScorePreTest(evaluation)
        
        #je vais chercher les resultats du post-test
      
        totalPostTest=fonction_CalculScorePostTest(evaluation)

        participant=Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
        print("Evolution relative de l'evaluation du participant id:(",participant.id,") - nom :",participant.nom)
        print((totalPostTest-totalPreTest)/totalPreTest)
        evolutionApprentissageGlobalRelativeExp=evolutionApprentissageGlobalRelativeExp+(totalPostTest-totalPreTest)/totalPreTest
        ligneExel=ligneExel+1
        fonction_exportExcel(worksheetExp,evaluation,ligneExel)
 
    
    for evaluation in evalTem:
        print("traitement new eval Tem")
        #je vais chercher les resultats du pre-test
        totalPreTest=fonction_CalculScorePreTest(evaluation)
        
        #je vais chercher les resultats du post-test
       
        totalPostTest=fonction_CalculScorePostTest(evaluation)

        participant=Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
        print("Evolution relative de l'evaluation du participant id: (",participant.id,") - nom :",participant.nom)
        print((totalPostTest-totalPreTest)/totalPreTest)
        evolutionApprentissageGlobalRelativeTem=evolutionApprentissageGlobalRelativeTem+(totalPostTest-totalPreTest)/totalPreTest
        ligneExel=ligneExel+1
        fonction_exportExcel(worksheetTem,evaluation,ligneExel)
    
    workbook.close()
    try:
        resultats["INDQ11A"]=evolutionApprentissageGlobalRelativeTem/nbrTotalEvalTem
    except ZeroDivisionError:
        resultats["INDQ11A"]=0
    try:
        resultats["INDQ11B"]=evolutionApprentissageGlobalRelativeExp/nbrTotalEvalExp
    except ZeroDivisionError:
        resultats["INDQ11B"]=0

    ################################
    #calcul du rapport de correlation INDQ14
    ################################

    #calul de la moyenne generale tous groupe confondeur (Ebar) car c'est la base pour la suite
    eBar=0
    eBarExp=0
    eBarTem=0
    pTem=resultats["nbrParticipantsTem"]
    pExp=resultats["nbrParticipantsExp"]
    denominateur=0
  
    for evaluation in evalExp:
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        eBarExp=eBarExp+((resPostTest-resPreTest)/resPreTest) /(pExp) #increment de la moyenne propre au groupe Exp
        eBar= eBar+((resPostTest-resPreTest)/resPreTest) /(pTem+pExp)  #increment de la moyenne general

        
    for evaluation in evalTem:
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        eBarTem=eBarTem+((resPostTest-resPreTest)/resPreTest) /(pTem) #increment de la moyenne propre au groupe Tem
        eBar= eBar+((resPostTest-resPreTest)/resPreTest) /(pTem+pExp)    #increment de la moyenne general 

    print("eBar :",eBar)
    print("eBarExp :",eBarExp)
    print("eBarTem :",eBarTem)
    #calul du denom (je peux pas le faire avant car je dois connaitre la moyenne general or je la connais qu'à l'issure de ces deux premieres boucles)
    denominateur=0
    for evaluation in evalExp:
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        denominateur=denominateur +((((resPostTest-resPreTest)/resPreTest)- eBar)*(((resPostTest-resPreTest)/resPreTest)- eBar))
    for evaluation in evalTem:
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        denominateur=denominateur +((((resPostTest-resPreTest)/resPreTest)- eBar)*(((resPostTest-resPreTest)/resPreTest)- eBar))
    numerateur=0

    numerateur=numerateur+pExp*(eBarExp-eBar)*(eBarExp-eBar)
    numerateur=numerateur+pTem*(eBarTem-eBar)*(eBarTem-eBar)

    try:
        resultats["INDQ14"]=numerateur/denominateur
    except ZeroDivisionError:
        resultats["INDQ14"]=0


    ################################
    #calcul du coefficient de  correlation INDQ23DA (ne se base que sur les data du groupe exp)
    ################################

    resultats["INDQ23DA"]=fonction_coefficientCorrelation(evalExp, pExp)

    resultats["INDQ13B"]=fonction_ecartType(evalExp,pExp)
    resultats["INDQ13A"]=fonction_ecartType(evalTem,pTem)

    resultats["INDQ12B"]=fonction_mediane(evalExp,pExp)
    resultats["INDQ12A"]=fonction_mediane(evalTem,pTem)


    return resultats

def fonction_mediane(evalEch,pEch):
    #creation d'un tableau des valeurs d'evolution
    tabEvol=[]
    for evaluation in evalEch:
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        ev =(resPostTest-resPreTest)/resPreTest
        tabEvol.append(ev)
    
    res=statistics.median(tabEvol)
    return res







#pour formule INDQ13A, INDQ13B
def fonction_ecartType(evalEch,pEch):
    evBar= 0#evolution moyenne du groupe concerné
    
    #calcul de la moyenne des evolution pour le groupe concerné 
    for evaluation in evalEch:
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        evTemp=(resPostTest-resPreTest)/resPreTest/pEch
        evBar=evBar+evTemp

    #calcul de la paranthese
    parenthese=0
    for evaluation in evalEch:
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)

        evTemp=(resPostTest-resPreTest)/resPreTest

        parenthese=parenthese+(evTemp-evBar)*(evTemp-evBar)
      

    res=parenthese/pEch

    res=sqrt(res)
    res=round(res.real,2)+round(res.imag,2)#vu que je calcul racine carré...risque de nbr complexe c'est pr ca que je suis obligé de faire ca


 

    return res

    
        






def fonction_coefficientCorrelation(evalExp,pExp):
    print("fonction_coefficientCorrelation")
    eBar=0 #moyenne evolution apprentissage
    dBar=0 #age moyen
    dAP=0 #age participant

    denominateur=0
    numerateur=0
    partieGauche=0
    partieDroite=0
  
    for evaluation in evalExp:
        #calcul moyenne resultats
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        eBar= eBar+((resPostTest-resPreTest)/resPreTest) /(pExp)  #increment de la moyenne general

        #calcul age moyen
        participant=Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
        dBar=dBar+participant.age/pExp

    for evaluation in evalExp:
        #calcul du numerateur
        resPreTest=fonction_CalculScorePreTest(evaluation)
        resPostTest=fonction_CalculScorePostTest(evaluation)
        eP=(resPostTest-resPreTest)/resPreTest#evolution d'apprentissage pour participant P
        participant=Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()
        age=participant.age
        numerateur=numerateur+(eP-eBar)*(age-dBar)

        #calcul du denom
        partieGauche=partieGauche+(eP-eBar)*(eP-eBar)
        partieDroite=partieDroite+(age-dBar)*(age-dBar)

    
    denominateur=sqrt(partieGauche)*sqrt(partieDroite)

    #si le denominateur est à zero c'est que tous sont à 0 en terme d'evolution ou qu'ils ont tous le meme age
    #il n'y a donc pas de correlation qu'on peut etablir
    if denominateur==0:
        resultat=0
    else:
        resultat=abs(numerateur/denominateur)

    return resultat





#fonction qui offre une verification complémentaire à la précédente (dès cas qui ne devraient pas arriver mais bon)
def fonction_verificationCompletComplement(evaluation):
    if not evaluation.questionnaireDemographique:
        return False
    if not evaluation.questionnaireMotivation:
        return False
    print(evaluation)
    print("eval pretest")
    print(evaluation.preTest)
    if not evaluation.preTest:
        return False
    if not evaluation.postTest1:
        return False
    if not evaluation.questionnaireUX:
        return False
    else :
        return True




def fonction_CalculScorePreTest(evaluation):
    preTest=QuestionnairePreTest.query.filter_by(id=evaluation.fk_QuestionnairePreTestId).first()
    resultatPreTest=0
    #je vais creer un tableau avec les reponses correctes pour calculer le resultats ensuite
    jeei=Jeei.query.filter_by(id=evaluation.fk_JeeiId).first()
    questionsReponses=QuestionApprentissage.query.filter_by(fk_SpecificationId=jeei.fk_SpecificationId).all()

    reponses=[]
    for qr in questionsReponses:
        reponses.append(qr.solutionCorrecte)

    if preTest.pt01==reponses[0]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt01==None or preTest.pt01=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10
    
    if preTest.pt02==reponses[1]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt02==None or preTest.pt02=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10

    if preTest.pt03==reponses[2]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt03==None or preTest.pt03=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10            

    if preTest.pt04==reponses[3]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt04==None or preTest.pt04=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10

    if preTest.pt05==reponses[4]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt05==None or preTest.pt05=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10


    if preTest.pt06==reponses[5]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt06==None or preTest.pt06=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10


    if preTest.pt07==reponses[6]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt07==None or preTest.pt07=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10


    if preTest.pt08==reponses[7]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt08==None or preTest.pt08=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10

    if preTest.pt09==reponses[8]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt09==None or preTest.pt09=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10

    if preTest.pt10==reponses[9]:
        resultatPreTest=resultatPreTest+10
    elif preTest.pt10==None or preTest.pt10=="abstention":
        resultatPreTest=resultatPreTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPreTest=resultatPreTest-10
    
    if resultatPreTest<=0:
        resultatPreTest=10

    print("Resultat pre test = ", resultatPreTest)
    return resultatPreTest



def fonction_CalculScorePostTest(evaluation):

    postTest=QuestionnairePostTest.query.filter_by(id=evaluation.fk_QuestionnairePostTestId).first()
    resultatPostTest=0
    #je vais creer un tableau avec les reponses correctes pour calculer le resultats ensuite
    jeei=Jeei.query.filter_by(id=evaluation.fk_JeeiId).first()
    questionsReponses=QuestionApprentissage.query.filter_by(fk_SpecificationId=jeei.fk_SpecificationId).all()

    reponses=[]
    for qr in questionsReponses:
        reponses.append(qr.solutionCorrecte)

    if postTest.pt01==reponses[0]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt01==None or postTest.pt01=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10
    
    if postTest.pt02==reponses[1]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt02==None or postTest.pt02=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10

    if postTest.pt03==reponses[2]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt03==None or postTest.pt03=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10            

    if postTest.pt04==reponses[3]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt04==None or postTest.pt04=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10

    if postTest.pt05==reponses[4]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt05==None or postTest.pt05=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10


    if postTest.pt06==reponses[5]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt06==None or postTest.pt06=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10


    if postTest.pt07==reponses[6]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt07==None or postTest.pt07=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10


    if postTest.pt08==reponses[7]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt08==None or postTest.pt08=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10

    if postTest.pt09==reponses[8]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt09==None or postTest.pt09=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10

    if postTest.pt10==reponses[9]:
        resultatPostTest=resultatPostTest+10
    elif postTest.pt10==None or postTest.pt10=="abstention":
        resultatPostTest=resultatPostTest+0 #pas utile mais c'est pour bien représenter le protocol
    else:
        resultatPostTest=resultatPostTest-10
    
    if resultatPostTest<=0:
        resultatPostTest=10

    print("Resultat post test = ", resultatPostTest)
    return resultatPostTest


def fonction_exportExcel(worksheet,evaluation,ligne):
    print('fonction_exportExcel')
   
    pretest=QuestionnairePreTest.query.filter_by(id=evaluation.fk_QuestionnairePreTestId).first()
    posttest=QuestionnairePostTest.query.filter_by(id=evaluation.fk_QuestionnairePostTestId).first()
    participant=Participant.query.filter_by(id=evaluation.fk_ParticipantId).first()

    worksheet.write(ligne,0,participant.id)
    worksheet.write(ligne,1,participant.nom)
    worksheet.write(ligne,2,participant.prenom)
    worksheet.write(ligne,3,participant.groupeExperimental)   
    worksheet.write(ligne,4,pretest.pt01)
    worksheet.write(ligne,5,pretest.pt02)
    worksheet.write(ligne,6,pretest.pt03)
    worksheet.write(ligne,7,pretest.pt04)
    worksheet.write(ligne,8,pretest.pt05)
    worksheet.write(ligne,9,pretest.pt06)
    worksheet.write(ligne,10,pretest.pt07)
    worksheet.write(ligne,11,pretest.pt08)
    worksheet.write(ligne,12,pretest.pt09)
    worksheet.write(ligne,13,pretest.pt10)
    worksheet.write(ligne,14,posttest.pt01)
    worksheet.write(ligne,15,posttest.pt02)
    worksheet.write(ligne,16,posttest.pt03)
    worksheet.write(ligne,17,posttest.pt04)
    worksheet.write(ligne,18,posttest.pt05)
    worksheet.write(ligne,19,posttest.pt06)
    worksheet.write(ligne,20,posttest.pt07)
    worksheet.write(ligne,21,posttest.pt08)
    worksheet.write(ligne,22,posttest.pt09)
    worksheet.write(ligne,23,posttest.pt10)

 
