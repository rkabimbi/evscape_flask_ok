

function fonction_affichageMesJEEI(numPager, listeMesJEEI,nbrPagesTotal,nbrJEEI)
{
    
    console.log("fonction_affichageMesJEEI")
    let indexDBSol=(numPager-1)*4 //le premier index de DB qu'il va afficher (pour qu'on ajoute ensuite 1,2,3,4 et qu'on puisse donc afficher ceux qui se suivent dans la db)...en gros c'est le plus bas de la liste de 4 JEEI qui seront affichés
    console.log(indexDBSol)
    let nbrCarteAAfficher =4

    //regler le probleme de la dernière page qui peut contenir moins de 4 elements
    if(numPager==nbrPagesTotal)//si on est à la dernière page
    {
        nbrCarteAAfficher=nbrJEEI%4 //nbr de JEEI modulo 4 donne le reste d'elements qu'il faut afficher
    }    
  
    //on remplace les elements dynamique de chaque carte par les nouvelles valeurs en lien avec le pager
    for(let i=0;i<nbrCarteAAfficher;i++)
    {
        console.log("page")
        console.log(listeMesJEEI.img[(indexDBSol+i)])
        document.getElementById("carteMesJEEI"+i).style.visibility = "visible";//si je mets pas ca. Quand on passe de la dernière à une page avant ca n'affiche plus tout car ca reste invisible
        document.getElementById("nomMesJEEI"+i).innerHTML=listeMesJEEI.noms[(indexDBSol+i)]
        document.getElementById("imgMesJEEI"+i).innerHTML=listeMesJEEI.img[(indexDBSol+i)]
        document.getElementById("themeMesJEEI"+i).innerHTML=listeMesJEEI.themes[(indexDBSol+i)]
        document.getElementById("statutMesJEEI"+i).innerHTML=listeMesJEEI.statuts[(indexDBSol+i)]
        document.getElementById("nbrExperimentationsMesJEEI"+i).innerHTML=listeMesJEEI.nbrExperimentations[(indexDBSol+i)]
    }
    
    //regler le probleme de la dernière page qui peut contenir moins de 4 elements (suite)
    if(numPager==nbrPagesTotal)//si on est à la dernière page
    {
        for(let i=3;i>=nbrCarteAAfficher;i--)
        {

            document.getElementById("carteMesJEEI"+i).style.visibility = "hidden";
        }
    }
    


}

//redirection vers la route de notre choix (j'ai du faire ca pour rendre ma carte cliquable)
function redicrectionVers(adresseRedicrection)
{
    location.href = adresseRedicrection;
}

