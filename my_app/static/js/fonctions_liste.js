

///////////////////////////////////////////////////////////
//PAGE GAME
////////////////////////////////////////////////////////////

//un callback qui se charge automatiquement au lancement de la page pour cacher tt les elements et laisser juste le bouton noir "joeur une nouvelle enigme"
//pour ce faire j'ai mis un "onload" dans l'html qui au chargement html de la page "game" lance ceci automatiquement
function collapseGame()
{ 
    console.log("-------Collapse ONLOAD------")
    //de base ca cache tt les elements hmtl sauf les messages/question et le bouton pr generer enigme
    document.getElementById("btnverif").style.visibility = "hidden";
    document.getElementById("CompteurRouge").style.visibility = "hidden";
    document.getElementById("CompteurVert").style.visibility = "hidden";
    document.getElementById("RecupRepForm").style.visibility = "hidden";
    document.getElementById("CompteurConsecutif").style.visibility = "hidden";
    document.getElementById("TitreComptCons").style.visibility = "hidden"; 

}

var derniereQuestion//pour eviter de selectionner deux fois la meme questions

//lienClique c'est pr savoir si il a clique ou si il arrive ici car il a reussi a repondre à enigme
//si le bouton a été cliqué, ca fera perdre un point , si c'est pcq il a répondu correctement à nune enigme ca sera false et on lui retire pas de points dans ce cas là
function afficherQuestion(nbrEnigmes,lienClique)
{ 
    console.log(nbrEnigmes)
    if(nbrEnigmes<2)
    {
        //si pas d'enigme dans la db et qu'on a clique nouvel enigme alors ca affiche juste le message (un cas que j'ai  bloqué par manque de temps car on peut pas supprimer quand il reste deux enigmes pr que ca continue à fournir des questions sans repetition)
        document.getElementById("TableauEnigmesComplet").innerHTML="Désolé il n'y a pas d'énigmes pour le moment. Revenz plus tard"
    }
    else//si il y a des enigmes dans la DB
    {
        //affiche ces elements HTML 
        document.getElementById("btnverif").style.visibility = "visible";
        document.getElementById("CompteurRouge").style.visibility = "visible";
        document.getElementById("CompteurVert").style.visibility = "visible";
        document.getElementById("RecupRepForm").style.visibility = "visible";
        document.getElementById("CompteurConsecutif").style.visibility = "visible";
        document.getElementById("TitreComptCons").style.visibility = "visible";        
         
        console.log("AfficherQuestion");
        console.log("dernier question :------------- "+derniereQuestion)
        console.log("nbr enigme : "+ nbrEnigmes)
    
        nbrHasard=getRandomInt(1,nbrEnigmes)
        console.log("nbr hasard avant test :"+nbrHasard)
        //gestion des cas où repetition d'enigme
        while(nbrHasard==derniereQuestion)//si le nbr tire au hasard = ancienne enigme 
        {           
            console.log("num hasard repetitf")
            nbrHasard=getRandomInt(1,nbrEnigmes)//alors il tire au hasard
        }
        derniereQuestion=nbrHasard
        console.log("nbr hasard  : "+nbrHasard)
        
        //il va envoyer une requête au serveur sur la routes : selectEnigme et va passer via un GET le numHasard et 
        var xhttp = new XMLHttpRequest( );//crée un objet de type XMLHttpRequest
        let url = new URL('http://127.0.0.1:5000/selectEnigme?fnbrHasard='+ nbrHasard+'&flienClique='+lienClique  );//configuration de l'url de la route à emprunter pour communiquer avec la DB. On assignera cette adresse à Xttp à la prochaine ligne de code  
        xhttp.open("GET", url.toString(), true);
        xhttp.send()
        xhttp.onreadystatechange = function()
        { 
            if (this.readyState == 4 && this.status == 200) 
            { 
                modifPageJeu(this.responseText)   
            }
        };
    }
}

//change la question du jeu + les compteurs.
function modifPageJeu(responseText)
{
    console.log("modifPageJeu")
    var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    console.log(fichJsonParse)//
    if(fichJsonParse.lienClique=="True" )//pour dire : si il y a pas encore eu de score c'est que c'est la première question donc on retire pas de point. LienClique : si c'est true ca veut dire qu'il a cliqué et donc on peut enlver point. Si c'est false c'est qu'il a repondu à la question et donc on doit pas retirer de point
    {
        verifReponse()//pour que quand on change de question il compte des points négatifs (vu que pas de reponse entrée)
    }
    document.getElementById("AffichageEnigmeId").innerHTML = fichJsonParse.question;
}


//fct Hasard
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


function verifReponse()
{
    console.log("verifReponse")
    enigmeActu=document.getElementById("AffichageEnigmeId").innerHTML //je recuperer l'enigme qui est actuellement affichee grace au getIdElement
    reponseUtilisateur=document.getElementById("RecupRepForm").value //car c'est élément de formulaire que je dois recuperer (pour ça que c'est "value")
    
    scoreCons=document.getElementById("CompteurConsecutif").innerHTML //recup la valeur actuelle du score consecutif pr la passer plus bas dans le code du cote serveur
    console.log("enigme recup : "+enigmeActu)
    console.log("rep utilisateur : "+reponseUtilisateur)
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/verifReponse?fenigmeActu='+ enigmeActu+'&freponseUser='+reponseUtilisateur+'&fscoreCons='+scoreCons  );
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
           console.log("dans le if de verifReponse. on va lancer resultat")
            resultat(this.responseText)
        }
    };

}


//gerer les resultats 
function resultat(responseText)
{
    console.log("resultat")
    var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    console.log(fichJsonParse)//
    nbrEnigmes=fichJsonParse.nbrEnigmes
    console.log("nbr enigme : "+nbrEnigmes)
    //si on s'est trompé
    if(fichJsonParse.rep=="False")
    {  
        console.log("Compteur rouge")
        console.log("innerHMTL : "+document.getElementById("CompteurRouge").innerHTML)
        console.log("mon innerhtml est rempli")
        //on augmente le score rouge de 1
        scoreRouge=parseInt(document.getElementById("CompteurRouge").innerHTML) +1
        document.getElementById("CompteurRouge").innerHTML =scoreRouge
        //on met le compteur consecutif à 0
        document.getElementById("CompteurConsecutif").innerHTML =0
        scoreCons=0
    }
    else if(fichJsonParse.rep=="True")
    {
        console.log("Compteur vert")
        console.log("innerHMTL : "+document.getElementById("CompteurVert").innerHTML)
        console.log("mon innerhtml est rempli")
        //je recupere le score vert present sur la page avant d'incrementer et je l'incremente
        scoreVert=parseInt(document.getElementById("CompteurVert").innerHTML) +1
        document.getElementById("CompteurVert").innerHTML =scoreVert
        //j'incremente le compteur consecutif en recuperant sa valeur sur la page et eni incrementant
        scoreCons =parseInt(document.getElementById("CompteurConsecutif").innerHTML)+1
        console.log("score consecutif"+scoreCons)
        document.getElementById("CompteurConsecutif").innerHTML=scoreCons
        //si j'ai 3 rep consecutive
        if(scoreCons==3)
        {
            //je mets l'entiereté de ma page dans un objet "pageGame1complete"
            pageGame1Complete = document.getElementById("contenuGame1") //je recuperer tt ma page dans un objet
            //jefface tt ce contenu
            pageGame1Complete.parentNode.removeChild(pageGame1Complete)//je remove le contenu de la page
            //je remplace le contenu de ma page par un message
            document.getElementById("contenuGame").innerHTML = '<h2 id="messageDeFin">   Bravo, c\'est réussi pour cette première épreuve de l\'escape game. retrouvez nous pour la suite </h2>'//pcq comme j'efface tt juste avant...je dois bien remettre mesbalises html
        }
        //on recommence tt la boucle et je met bien "lienclique" à False pr dire qu'il a bien repondu et que donc on doit pas lui retirer des points
        afficherQuestion(nbrEnigmes,"False")
    }
    
}


///////////////////////////////////////////////////////////
//AFFICHAGE LISTE ENIGME
////////////////////////////////////////////////////////////

//on arrive ici après que la fonction python d'affichage de la liste ns y ait envoyé directement
function gestionListeEnigmes(paginationActuelle)
{ 
    console.log("Gestion liste Enigmes");
    console.log("pagination = "+paginationActuelle)
    //on envoi une requete à la route envoiEnigmes pr qu'elle ns fasse revenir tte les enigmes cotés clients et qu'on puisse afficher la page ici
    var xhttp = new XMLHttpRequest( );//crée un objet de type XMLHttpRequest
    let url = new URL('http://127.0.0.1:5000/EnvoiEnigmes?fpaginationActuelle='+paginationActuelle);//configuration de l'url de la route à emprunter pour communiquer avec la DB. On assignera cette adresse à Xttp à la prochaine ligne de code
    xhttp.open("GET", url.toString(), true);//l'objet xttp prepare sa requete  (on lui "assigne" l'url calculé avant...enfin il va ouvrir le lien et c'est comme ça qu'ensuite sa variable d'instance responseText contiendra le fichier json )
    xhttp.send()//il envoi sa requete vers le serveur
    //une fois que la requete revient et qu'elle es positive
    xhttp.onreadystatechange = function()//assignation d'un call back à mon objet xhttp. Ce callback se lance dès qu'il y a un changement de statut de la requete (requete recue-->requete processe, requete finie)'
    { 
        if (this.readyState == 4 && this.status == 200) //si le send s'est bien passé
        {
           affichageListeEnigmes(this.responseText)//affiche la modification opérée à l'ecran. responseText est une variable d'instance de la classe XMLHttpRequest (c'est cette variable qui contient le JSON que la viewfunction (route) a généré)       
        }
    };
}

function affichageListeEnigmes(responseText)
{
    
    console.log("affichageListeEnigme");
    var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    console.log(fichJsonParse)//affichage Liste Enigmes  
    console.log("Construction tableau en HTML")
    //fct qui construit mon tableau en HTML
    tableauEnigmesHtml=constructionTableauEnigmesEnHtml(fichJsonParse.listeEnigmes,fichJsonParse.admin,fichJsonParse.paginationActuelle,fichJsonParse.listeUsers,fichJsonParse.message)
    //on affiche le tableau crée (code HTML) dans la balise dont l'id est tableauenigmescomplet dans le fichier listeEnigmes.html
    document.getElementById("TableauEnigmesComplet").innerHTML=tableauEnigmesHtml //remplace ce qui est dans mon HTML sous l'id TableauEnigmesComplet
}

//ici l'idée est de générer du code HTML dans un string
function constructionTableauEnigmesEnHtml(listeEnigmes,admin,paginationActuelle,listeUsers,messageFlash)//admin = valeur booleen qui permet de savoir si on est face à un admin ou pas
{ 
    console.log("construction tableau enigmes en html")
    console.log(listeEnigmes)
    //gestion du nbr de page
    tailleListeEnigmes=listeEnigmes.id.length
    nbrPages=Math.ceil(tailleListeEnigmes/5) //arrondir à l'unité supérieure
    console.log("tailleListeEnigmes : "+tailleListeEnigmes)

    //resultat=mon string qui va contenir tt le code html que je vais envoyer via getElementById
    //partie sur les Flash selon le message reçu du serveur
    if(messageFlash=="Suppression Ok")
    {
        var resultat='<div class="alert alert-success" role="alert">'+messageFlash+'  </div>'
    }
    else if(messageFlash=="Suppression interdite")
    {
        messageFlash=messageFlash+" car vous devez toujours avoir au moins deux enigmes pour jouer au jeu. Creez une enigme et ensuite tenter d'en effacer une à nouveau"
        var resultat='<div class="alert alert-danger" role="alert">'+messageFlash+'  </div>'
    }
    else if(messageFlash=="Modification du niveau hors seuil")
    {
        var resultat='<div class="alert alert-danger" role="alert">'+messageFlash+'  </div>'
    }
    else if(messageFlash=="Modification du niveau ok")
    {
        var resultat='<div class="alert alert-success" role="alert">'+messageFlash+'  </div>'
    }
    else
    {
        var resultat=""
    }
    
    //partie pagination
    resultat=resultat+'<nav id="paginationBar" aria-label="Page de navigation">' 
    resultat=resultat+'<ul class="pagination">'
    //on boucle pr afficher les pages (les petits onglets en haut)
    for(i=1;i<=nbrPages;i++)
    {
        resultat=resultat+'<li class="page-item"><a class="page-link" onclick="gestionListeEnigmes('+i+')">'+i+'</a></li>'     
    }
    resultat=resultat+'</ul></nav>'

    //construction de la partie fixe du tableau (partie haute avec le titre)
    resultat=resultat+'<div class="text-center">'+""
    resultat=resultat+'<table class="table table-striped "><!-- classe avec style css rayé-->'
    resultat=resultat+'<thead class="table-dark"><!-- en-tête noire-->'
    resultat=resultat+'    <tr>'
    resultat=resultat+'        <th scope="col">#</th>'
    resultat=resultat+'       <th scope="col">Categorie</th>'
    resultat=resultat+'       <th scope="col">Question</th>'
    resultat=resultat+'       <th scope="col">Niveau</th>'
    //un non admin ne peut pas voir la liste de qui a fait tel ou tel enigme (mais dans l'intervalle j'ai fait en sorte que tt le monde etait utilisateur admin.)
    if(admin)
    {
        resultat=resultat+'            <th scope="col">Auteur</th>'
    }
    resultat=resultat+'        <th scope="col">Incr</th>'
    resultat=resultat+'        <th scope="col">Decr</th>'
    resultat=resultat+'        <th scope="col">Réponse</th>'
    resultat=resultat+'        <th scope="col">Supression</th>'
    resultat=resultat+'        <th scope="col">màj</th>'
    resultat=resultat+'        <th scope="col">ind?</th>'
    resultat=resultat+'        <th scope="col">indice</th>'
    resultat=resultat+'    </tr>'
    resultat=resultat+'</thead>'

    //contenu du tableau
    resultat=resultat+'<tbody id="contenuTableauEnigmes">'
    //bornes pour la pagination (pr savoir quelles enigmes doivent être affichées)
    borneInf=(paginationActuelle-1)*5
    borneSup=paginationActuelle*5
    console.log("paginationActuelle : "+paginationActuelle)
    console.log("BorneInf : "+borneInf+" borneSupr : "+borneSup)
    for(i=borneInf;i<borneSup;i++)
    {
        if(listeEnigmes.id[i]!=null)//si jamais on a pas un tableau est un multiple de 5 il va continuer à iterer pr completer vu les bornes. Ceci permet de dire que si id==null il n'affiche rien :D
        {
            console.log("Dans le for de constructionTableauEnigmesHTML, iteration :"+i)
            console.log("Enigme :"+listeEnigmes.id[i]+ " / Question : "+ listeEnigmes.question[i])
            //caractere de début de ligne <tr>
            resultat=resultat+"<tr id='ligne'"+(i+1)+">"// Ce que je fais avec i+1 c'est construire un id du type : "ligne1, Ligne2,..." ca pourra surement servir . PQ +1? pour que ca corresponde aux id de mes enigmes qui commencent à 1
            //#
            resultat=resultat+"<td>"+ listeEnigmes.id[i] +"</td>"
            //categorie
            resultat=resultat+"<td>"+listeEnigmes.categorie[i] +"</td>"
            //Question
            resultat=resultat+"<td>"+listeEnigmes.question[i] +"</td>"
            //niveau
            resultat=resultat+"<td id='niveau"+(i+1)+"'>"+listeEnigmes.niveau[i]+"</td>"//ici je met un id à ma ligne niveau car j'en ai besoin pr incrementer. i+1 c'est pr que ca corresponde à l'enigme en cours vu que les engimes id commencent à 1 et mon tableau ici à 0
            //auteur
            if(admin)
            {
                idUserActuelle=listeEnigmes.user_id[i]-1//car ca renseigne l'utilisateur num 1 dans la DB MAIS comme j'ai converti la DB en tableau ...ca commence en 0 ...donc je dois faire le chiffre en question -1
                resultat=resultat+"<td>"+listeUsers.username[idUserActuelle]+"</td>"
            }
            //Incr
            resultat=resultat+"<td>"+imgBoutinIncDec('True',listeEnigmes.id[i],paginationActuelle)+"</td>"
            //Decr
            resultat=resultat+"<td>"+imgBoutinIncDec('False',listeEnigmes.id[i],paginationActuelle)+"</td>"
            //Réponse
            resultat=resultat+"<td>"+cacherContenu(listeEnigmes.reponse[i],(i+1))+"</td>"//
            //Suppresion
            resultat=resultat+"<td>"+imgBoutonSupr(listeEnigmes.id[i],paginationActuelle)+ "</td>"
            //màj
            resultat=resultat+"<td>"+ btnMaj(listeEnigmes.id[i], paginationActuelle) +"</td>"
            //ind?
            resultat=resultat+"<td>"+ imgPresenceIndice(listeEnigmes.r_indice[i]) +"</td>"
            //indice
            resultat=resultat+"<td>"+ btnIndices(listeEnigmes.id[i], paginationActuelle) +"</td>"
            //caractere de fin de ligne
            resultat=resultat+"</tr>"
        }
        
    }
    resultat=resultat+"</tbody>"
    resultat=resultat+"</table>"
    resultat=resultat+"</div> " 
    resultat=resultat+'<div> <a class="btn btn-primary" href="/CreationEnigme?pageRetour='+paginationActuelle+'" role="button">Creer Enigme</a></div>'
    console.log(resultat)
   
    console.log("Fin de constructionTablezauEnigmesHTML7")
    return resultat   
}

//ce qui suit ce sont tte mes fction que j'avais déjà avant dans mon HTML mais avec du JINJA

//fonction qui me permet de collapse ma réponse à l'enigme
function cacherContenu(reponseACacher,index)
{
    return '<button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#collapseContenu'+index+'" aria-expanded="false" aria-controls="collapseContenu"> Réponse</button> </p> <div class="collapse" id="collapseContenu'+index+'"><div class="card card-body">'+reponseACacher+'</div></div>' 
}

//fonction permet l'affichage et action sur les boutons d'increm
//incremDecrem est un booleen (que j'ai mis en String :) ) qui permet de savoir si on increm ou decrem
function imgBoutinIncDec(incremDecrem, numEnigmeAModifier,paginationActuelle)
{
    console.log("creation du bouton de fleche update")
    if(incremDecrem=="True")//si on incremente
    {
        console.log("cree image increment")
        img="fas fa-arrow-circle-up"
        temp=1
    }
    else
    {
        console.log("cree image decrement")
        img="fas fa-arrow-circle-down"
        temp=0
    }
    console.log("increm : "+incremDecrem)
    res='<button  class="btn-circle btn-lg"  onclick="envoiNiveau('+temp+','+numEnigmeAModifier+','+paginationActuelle+')">'// permet le declenchement de la fonction "envoiNiveau" dans notre code JS
    res=res+'<span id="bouton'+incremDecrem+numEnigmeAModifier+'" class="'+img+'" ></span>   </button> '//image de la fleche
 
    return res

}


function imgBoutonSupr(numEnigmeASupprimer,paginationActuelle)
{
    console.log("imgBoutonSupr")
    img="fas fa-window-close"
    res='<button  class="btn-circle btn-lg" onclick="suppressionEnigme('+numEnigmeASupprimer+','+paginationActuelle+')">'
    res=res+'<span class="'+img+ '" ></span> </button>'
    return res
}


function imgPresenceIndice(indices)
{
    if(indices=="True")//s'il y a des indices references
    {
        res='</h2><span class="badge badge-pill badge-success">oui</span></h2>'
    }
    else
    {
        res='</h2><span class="badge badge-pill badge-secondary">non</span></h2>'
    }
    return res
}

function btnMaj(numEnigme, paginationActuelle)
{
    return '<a class="btn btn-primary" href="/majEnigme?enigme='+numEnigme+'&paginationActu='+paginationActuelle+'"role="button">màj</a>'
}


function btnIndices(numEnigme,paginationActuelle)
{
    return '<a class="btn btn-primary" href="/voirIndice?enigme='+numEnigme+'&paginationActu='+paginationActuelle+'"role="button">indices</a>'
}


///////////////////////////////////////////////////////////
//SUPPRESSION
////////////////////////////////////////////////////////////

function suppressionEnigme( numEnigm,paginationActuelle)
{  
    console.log("SupprimeEnigme6");
    console.log("num Enigme en cours d'effacement :"+numEnigm)
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/supprimeEnigme?fnumEnigm='+numEnigm+'&fpaginationActuelle='+paginationActuelle);
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {      
           affichageListeEnigmes(this.responseText)
        }
    };
}



///////////////////////////////////////////////////////////
//INCREM DECREM
////////////////////////////////////////////////////////////

function envoiNiveau(incremBool,numEnigm,paginationActuelle)
{ 
    if(incremBool==1)
    {
        incremBool="True"
    }
    else
    {
        incremBool="False"
    }
    console.log("envoiNiveau");
    console.log("increm : "+incremBool)
    console.log(numEnigm)
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/incremDecrem?fincremBool='+ incremBool+"&fnumEnigm="+ numEnigm+"&fpaginationActuelle="+paginationActuelle  );
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {   
            affichageListeEnigmes(this.responseText)
        }
    };
}



