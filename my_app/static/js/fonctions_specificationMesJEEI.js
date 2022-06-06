



function fonction_Presentation()
{
    console.log("fonction_Presentation")
    //surligner le menu dans lequel on se trouve
    fonction_activationBouton("navLinkPresentation")

    //selection de ce qu'on doit afficher
    fonction_selectionContenuSousPage('idContenuSousPagePresentation')

    
}

function fonction_Documentation()
{
    console.log("fonction_Documentation")
    fonction_activationBouton("navLinkDocumentation")
    //selection de ce qu'on doit afficher
    fonction_selectionContenuSousPage('idContenuSousPageDocumentation')
}

function fonction_Resultats()
{
    console.log("fonction_Resultats")
    fonction_activationBouton("navLinkResultats")
    //selection de ce qu'on doit afficher
    fonction_selectionContenuSousPage('idContenuSousPageResultats')
}


function fonction_Test()
{
    console.log("fonction_Test")
    fonction_activationBouton("navLinkTest")
    //selection de ce qu'on doit afficher
    fonction_selectionContenuSousPage('idContenuSousPageTest')
}



function fonction_ListeExperimentations()
{
    console.log("fonction_ListeExperiemtnation")
    fonction_activationBouton("navLinkListeExperimentations")
    //selection de ce qu'on doit afficher
    fonction_selectionContenuSousPage('idContenuSousPageListeExperimentations')
}

function fonction_Equipe()
{
    console.log("fonction_Equipe")
    fonction_activationBouton("navLinkEquipe")
    //selection de ce qu'on doit afficher
    fonction_selectionContenuSousPage('idContenuSousPageEquipe')
}




//permet de mettre en evidence le bouton qui est selectionné
function fonction_activationBouton(boutonAColorer)
{
    //codeHtml =  document.getElementById(boutonAColorer).innerHTML
    
    //on désactive tous les autres
    document.getElementById("navLinkListeExperimentations").innerHTML='<a  class="nav-link nvSousPage" onclick="fonction_ListeExperimentations()">Liste Experimentations</a>'
    document.getElementById("navLinkTest").innerHTML='<a  class="nav-link nvSousPage" onclick="fonction_Test()">Test</a>'
    document.getElementById("navLinkResultats").innerHTML='<a  class="nav-link nvSousPage" onclick="fonction_Resultats()">Resultats</a>'
    document.getElementById("navLinkDocumentation").innerHTML='<a  class="nav-link nvSousPage" onclick="fonction_Documentation()">Documentation</a>'
    document.getElementById("navLinkPresentation").innerHTML='<a  class="nav-link nvSousPage" onclick="fonction_Presentation()">Présentation</a>'
    document.getElementById("navLinkEquipe").innerHTML='<a  class="nav-link nvSousPage" onclick="fonction_Equipe()">Equipe</a>'
    


    //Remplace la ligne de spécification du bouton dans HTML pour que ca devienne actif
    //techniquement j'ajoute juste un "active" à class="nav-link "
    if(boutonAColorer=="navLinkListeExperimentations")
    {
        document.getElementById("navLinkListeExperimentations").innerHTML='<a  class="nav-link active" onclick="fonction_ListeExperimentations()">Liste Experimentations</a>'
    }
    else if (boutonAColorer=="navLinkTest")
    {
        document.getElementById("navLinkTest").innerHTML='<a  class="nav-link nvSousPage active" onclick="fonction_Test()">Test</a>'
    }
    else if(boutonAColorer=="navLinkResultats")
    {
        document.getElementById("navLinkResultats").innerHTML='<a  class="nav-link nvSousPage active" onclick="fonction_Resultats()">Resultats</a>'
    }
    else if(boutonAColorer=="navLinkDocumentation")
    {
        document.getElementById("navLinkDocumentation").innerHTML='<a  class="nav-link nvSousPage active" onclick="fonction_Documentation()">Documentation</a>'
    }
    else if(boutonAColorer=="navLinkPresentation")
    {
        document.getElementById("navLinkPresentation").innerHTML='<a  class="nav-link nvSousPage active" onclick="fonction_Presentation()">Présentation</a>'
    }
    else if(boutonAColorer=="navLinkEquipe")
    {
        document.getElementById("navLinkEquipe").innerHTML='<a  class="nav-link nvSousPage active" onclick="fonction_Equipe()">Equipe</a>'
    }
   
}



//variables globales pour pouvoir reset ensuite facilement (sinon pas possible de recuperer aprys un style.display="none")
//en plus comme ça il garde les données du formulaire
displayDocumentation=document.getElementById("idContenuSousPageDocumentation").style.display
displayTest=document.getElementById("idContenuSousPageTest").style.display
displayResultats=document.getElementById("idContenuSousPageResultats").style.display
displayListeExperimentations=document.getElementById("idContenuSousPageListeExperimentations").style.display
displayPresentation= document.getElementById("idContenuSousPagePresentation").style.display
displayPresentation= document.getElementById("idContenuSousPageEquipe").style.display
//comme ca il cache directement tt...sinon il affiche tt et c'est seulement quand je clique le menu qu'il cache ce qu'il faut
document.getElementById("idContenuSousPageDocumentation").style.display="none"
document.getElementById("idContenuSousPageTest").style.display="none"
document.getElementById("idContenuSousPageResultats").style.display="none"
document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
document.getElementById("idContenuSousPageEquipe").style.display="none"



//cette fonction reçoit l'ID d'une macro d'affichage HTML. En fonctoon de ce qu'elle recoit elle cache les autres et n'affiche que celle passée en parametre
function fonction_selectionContenuSousPage(idSousPage)
{
    console.log("fonction_selectionContenuSousPage")
    switch(idSousPage)
    {
        case 'idContenuSousPagePresentation':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById("idContenuSousPageEquipe").style.display="none"
            document.getElementById(idSousPage).style.display=displayPresentation
            break;

        case 'idContenuSousPageDocumentation':
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById("idContenuSousPageEquipe").style.display="none"
            document.getElementById(idSousPage).style.display=displayDocumentation
            break;

        case 'idContenuSousPageTest':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById("idContenuSousPageEquipe").style.display="none"
            document.getElementById(idSousPage).style.display=displayTest
            break;

        case 'idContenuSousPageResultats':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById("idContenuSousPageEquipe").style.display="none"
            document.getElementById(idSousPage).style.display=displayResultats
            break;

        case 'idContenuSousPageListeExperimentations':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageEquipe").style.display="none"
            document.getElementById(idSousPage).style.display=displayListeExperimentations
            break;
        case 'idContenuSousPageEquipe':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById(idSousPage).style.display=displayListeExperimentations
            break;
    }

}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//chargé de renvoyer vers le BackEnd les données sauvées relatives à la table Jeei
function fonction_sauvegardeTableJeei(idChamps,idJEEI)
{
    console.log("fonction_sauvegarde")
    console.log("champs :"+idChamps) //obligé de travailler avec l'idDuCamps pour pouvoir aller chercher la valeur à la ligne suivante

    let valeur=document.getElementById(idChamps).value
    console.log("valeur :"+valeur)
    console.log("ID "+idJEEI)
    
    if(idChamps=="idNomMonJEEI")
    {
        champs="nom"
    }
    else if(idChamps=="idDescriptifMonJEEI")
    {
        champs="descriptif"
    }
    /* pas besoin car géré directement
    else if(idChamps=='idImageMonJEEI')
    {
        champs="img"
        valeur="img"+str(idJEEI)
    }
    */
   
   else if(idChamps=="idNbrJoueursMinMonJEEI")
   {
       champs="nbrJoueursMin"
       //valeur=String(valeur)
   }
   else if(idChamps=="idNbrJoueursMaxMonJEEI")
   {
       champs="nbrJoueursMax"
       //valeur=String(valeur)
   }
   else if(idChamps=="idBudgetMonJEEI")
   {
       champs="budget"
       //valeur=String(valeur)
   }
   else if(idChamps=="idDureeMinutesMonJEEI")
   {
       champs="dureeMinutes"
       //valeur=String(valeur)
   }
   else if(idChamps=="idScenarioMonJEEI")
   {
       champs="scenario"
       //valeur=String(valeur)
   }
   else if(idChamps=="idChapitreMonJEEI")
   {
       champs="chapitre"
       //valeur=String(valeur)
   }
   else if(idChamps=="idThemeMonJEEI")
   {
       champs="theme"
       //valeur=String(valeur)
   }
   else if(idChamps=="idPublicCibleMonJEEI")
   {
       champs="publicCible"
       //valeur=String(valeur)
   }
 



       
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/sauvegardeTableJeei?champs='+ champs+'&valeur='+valeur+'&idJEEI='+idJEEI  );  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            reponseBackEnd(this.responseText, champs)   
        }
    };
}

function reponseBackEnd(responseText, champs)
{
    //if(champs!='img')//pour l'instant pas besoin de validateur pour ce champs là car on le voit à l'ecran
    
    {
        console.log("reponseBackEnd")
        console.log(responseText)
        //console.log(champs)
        //console.log(responseText)
       
        var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
        //console.log(fichJsonParse.reponse, champs)//
        
    
        affichageValidationSauvegarde='<h3>  <span style="color:white"class="badge bg-success ">V</span></h3>' 
        document.getElementById("affichageValidationSauvegarde"+champs).innerHTML=affichageValidationSauvegarde;
        window.setTimeout("document.getElementById('affichageValidationSauvegarde'+champs).style.visibility='hidden';", 2000)
        
    }

   
    
  
    
}




function fonction_sauvegardeSpecificationTest(champs,idChamps,idTest)
{
    console.log("fonction_sauvegardeSpecificationTest")
    console.log("champs :"+idChamps) //obligé de travailler avec l'idDuCamps pour pouvoir aller chercher la valeur à la ligne suivante

    let valeur=document.getElementById(idChamps+idTest).value
    console.log("valeur :"+valeur)
    console.log("ID "+idTest)
    


    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/sauvegardeSpecificationTest?champs='+ champs+'&valeur='+valeur+'&idTest='+idTest  );  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            reponseBackEndTest(this.responseText, champs,idTest)   
        }
    };

}

function reponseBackEndTest(responseText, champs,idTest)
{
    //if(champs!='img')//pour l'instant pas besoin de validateur pour ce champs là car on le voit à l'ecran
    
    {
        console.log("reponseBackEndTest")
        console.log(responseText)
        //console.log(champs)
        //console.log(responseText)
       
        var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
        //console.log(fichJsonParse.reponse, champs)//
        
    
        affichageValidationSauvegarde='<h3>  <span style="color:white"class="badge bg-success">V</span></h3>' 
        document.getElementById('validationTest'+champs+idTest).innerHTML=affichageValidationSauvegarde
        
    }

   
    
  
    
}

function fonction_ajouterMembreEquipe(id)
{
    console.log("id JEEI :"+id)

    let membre=
       { nom:"",
        prenom:"",
        email:"",
        universite:""}
    
    //membre=[]

    membre.nom=document.getElementById("nomMembreEquipeModal").value
    membre.prenom=document.getElementById("prenomMembreEquipeModal").value
    membre.email=document.getElementById("emailMembreEquipeModal").value
    membre.universite=document.getElementById("universiteMembreEquipeModal").value

    //membre=JSON.stringify(membre);
    console.log("donnees du modal")
    console.log(membre.nom)

    
    
    
    
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/sauvegardeNouveauMembre?idJeei='+ id+'&membreNom='+membre.nom +'&membrePrenom='+membre.prenom +'&membreEmail='+membre.email +'&membreUniversite='+membre.universite);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            afficherLeNouveauMembre(this.responseText)   
        }
    };

}


function afficherLeNouveauMembre(responseText)
{
        console.log("afficherLeNouveauMembre")
        console.log(responseText)
        //console.log(champs)
        //console.log(responseText)
        if (responseText=="nok")
        {
            console.log("chercheur deja ajouté")
            document.getElementById("flashModalMembreexistant").innerHTML="<div class='alert alert-warning' style = 'margin-left:25px;'role='alert'> Cet utilisateur est déjà assigné à ce projet </div>"
        }
        else
        {
            var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
            //console.log(fichJsonParse.reponse, champs)//
            console.log(fichJsonParse)
      
        
            //je recup dans une variable la liste actuelle et j'y ajoute mon new membre
            listeMembre = document.getElementById("listeEquipe").innerHTML

            newmembre =recreationMembreHTML(fichJsonParse)

            document.getElementById("listeEquipe").innerHTML= listeMembre + newmembre

      
  
            let d = document.getElementById('exampleModalCenter')
            d.style.display = "none"
        }


          


     

}


function recreationMembreHTML(membre)
{
    return '<div class="col-sm-5 carteMembreEquipe"  > <ul class="list-group list-group-flush"> <li class="list-group-item"> <B> Nom</B> :'+membre.reponse.nom+' </li> <li class="list-group-item"> <B> Prénom</B> :'+membre.reponse.prenom+' </li> <li class="list-group-item"> <B>Université  </B>: '+membre.reponse.universite+' </li> <li class="list-group-item"> <B> email </B>: '+membre.reponse.email+' </li> </ul> </div>' 
}


function fonction_validerJEEI(idJeei,question)
{
    console.log("fonction_validerJEEI")
    document.getElementById('idNomMonJEEI').disabled = true;
    document.getElementById('idDescriptifMonJEEI').disabled = true;
    document.getElementById('idNbrJoueursMinMonJEEI').disabled = true;
    document.getElementById('idNbrJoueursMaxMonJEEI').disabled = true;
    document.getElementById('idBudgetMonJEEI').disabled = true;
    document.getElementById('idDureeMinutesMonJEEI').disabled = true;
    document.getElementById('idScenarioMonJEEI').disabled = true;
    document.getElementById('idPublicCibleMonJEEI').disabled = true;
    document.getElementById('idThemeMonJEEI').disabled = true;
    document.getElementById('idChapitreMonJEEI').disabled = true;
    var questions = document.getElementsByClassName('form-control testQuestion')
    for(var i=0;i<questions.length;i++)
    {
        questions[i].disabled=true
    }
    document.getElementById('idBtnModalEquipe').disabled = true;
    document.getElementById('idBtnChargezSpec').disabled = true;
    document.getElementById('btnExpDansSpec').disabled = false;

    document.getElementById('btnValiderJeeibtn').disabled = true;
    document.getElementById('btnValiderJeeibtn').innerHTML= "<button  id='btnValiderJeeibtn' class='btn btn-danger'> Validé   </button>"

  
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/validerJEEI?idJeei='+ idJeei);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            //afficherLeNouveauMembre(this.responseText)   
            console.log("ok c'est validé")
        }
    };



    //href="http://127.0.0.1:5000/ValiderMonJEEI?idJEEI={{monJEEIRecupere.id}}

}