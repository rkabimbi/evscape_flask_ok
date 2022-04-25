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
        /*
            ATTENTION j'utilise positionDsJson à la place de l'ID du JEEI pcq on peut avoir un ID 552 qui est le 7 ème EG d'une personne et donc dans le JSON il occupe la position 7 et pas 552
        */
        for(let positionDsJson=borneInfIntervalleListeJEEI;positionDsJson<=borneSupIntervalleListeJEEI;positionDsJson++)
        {
            //codeHTML=codeHTML+" {{ macro_MesJEEI.afficherCarteMesJEEI("+mesJEEI+" ,"+positionDsJson+"  ) }}"
/*   
            codeHTML=codeHTML+" {{ macro_MesJEEI.afficherCarteMesJEEI("+noms[positionDsJson]+" ,"+ auteurs[positionDsJson]+ ","+ nbrExperimentations[positionDsJson]+ ","+ themes[positionDsJson]+ ","+ id[positionDsJson]+ ","+ img[positionDsJson]+ ","+positionDsJson+"  ) }}"
*/

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