/*
function fonction_Pagination(numPagination,mesJEEI)
{
    console.log("fonction_Pagination - page :"+numPagination)
    console.log(mesJEEI)
    //destructuring du JSON
        const{noms,auteurs,nbrExperimentations,themes,id,img}=mesJEEI
        console.log("Données reçues mesJEEI")
        console.log(noms)
        console.log(auteurs)
        console.log(nbrExperimentations)
        console.log(themes)
        console.log(id)
        console.log(img)

    
    
    //calcul des bornes
        let borneInfIntervalleListeJEEI=(numPagination-1)*4
        let borneSupIntervalleListeJEEI=numPagination*4-1

        

    //remplacer dans la page HTML avec les valeurs qu'il faut
        
        let codeHTML=""

        for(let positionDsJson=borneInfIntervalleListeJEEI;positionDsJson<=borneSupIntervalleListeJEEI;positionDsJson++)
        {
            //codeHTML=codeHTML+" {{ macro_MesJEEI.afficherCarteMesJEEI("+mesJEEI+" ,"+positionDsJson+"  ) }}"


            codeHTML=codeHTML+"<div class='card cardMesJEEI' >"
            codeHTML=codeHTML+"<img src=' "+img[positionDsJson]+"' class='card-img-top imgCardMesJEEI'  >"
            codeHTML=codeHTML+'<div class="card-body">'
            codeHTML=codeHTML+'<h5 class="card-title"><B> '+noms[positionDsJson]+'</B></h5>'
            codeHTML=codeHTML+'<p class="card-text">Some quick example text to build on the card title and make up the bulk of the cards content.</p>'
            codeHTML=codeHTML+'</div> <ul class="list-group list-group-flush">'
            codeHTML=codeHTML+'<li class="list-group-item"><B> Thème</B> :  '+themes[positionDsJson]+' </li>'
            codeHTML=codeHTML+'<li class="list-group-item"><B> Statut</B> : Verouillé</li>'
            codeHTML=codeHTML+'<li class="list-group-item"><B> Nbr Experimentations</B> :'+nbrExperimentations[positionDsJson]+'</li> </ul>'
            codeHTML=codeHTML+' <div class="card-body"><a class="btn btn-outline-secondary" href="http://127.0.0.1:5000/SpecificationsJEEI?idJEEI='+id[positionDsJson]+'" role="button">Modifier</a>'
            codeHTML=codeHTML+'<a class="btn btn-outline-warning" href="http://127.0.0.1:5000/ExperimentationJEEI?idJEEI='+id[positionDsJson]+'" role="button">Expérimentation</a>'
            codeHTML=codeHTML+'<a class="btn btn-outline-success" href="http://127.0.0.1:5000/DataJEEI?idJEEI='+id[positionDsJson]+'" role="button">Data</a>'
            codeHTML=codeHTML+'    <a class="btn btn-outline-danger" href="http://127.0.0.1:5000/SupprimerMonJEEI?idJEEI='+id[positionDsJson]+'" role="button">Supprimer</a>    </div> </div> '



        }
        
        document.getElementById("composantMesJEEI").innerHTML=codeHTML



}
*/

function fonction_pagination(pagination)
{
    console.log(pagination)

    //il va envoyer une requête au serveur sur la routes : selectEnigme et va passer via un GET le numHasard et 
     var xhttp = new XMLHttpRequest();//crée un objet de type XMLHttpRequest
     let url = new URL('http://127.0.0.1:5000/mesJEEICartes?pagination='+ pagination);//configuration de l'url de la route à emprunter pour communiquer avec la DB. On assignera cette adresse à Xttp à la prochaine ligne de code  
     xhttp.open("GET", url.toString(), true);
     xhttp.send()
     xhttp.onreadystatechange = function()
     { 
         if (this.readyState == 4 && this.status == 200) 
         { 
             
             console.log("ok ")
             fonction_affichageCartes(this.responseText)   
         }
     };
}

function fonction_affichageCartes(responseText)
{
    console.log("fonction_affichageCartes");
    responseText=JSON.stringify(responseText)
    
    var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
   // console.log(fichJsonParse)//affichage Liste Enigmes 
}


function fonction_affichageMesJEEI(numPager, listeMesJEEI)
{
    
    console.log("fonction_affichageMesJEEI")
    let indexDBSol=(numPager-1)*4 //le premier index de DB qu'il va afficher (pour qu'on ajoute ensuite 1,2,3,4 et qu'on puisse donc afficher ceux qui se suivent dans la db)
    console.log(indexDBSol)
    
    for(let i=0;i<4;i++)
    {
        console.log("element de base :")
        console.log(document.getElementById("nomMesJEEI"+i).innerHTML)
        console.log("element de remplacement")
        console.log(listeMesJEEI.noms[(indexDBSol+i)])
        document.getElementById("nomMesJEEI"+i).innerHTML=listeMesJEEI.noms[(indexDBSol+i)]
    }
}

