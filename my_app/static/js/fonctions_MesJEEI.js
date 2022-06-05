
var numPagerGlobal //[hack]
function fonction_affichageMesJEEI(numPager, listeMesJEEI,nbrPagesTotal,nbrJEEI)
{
    
    numPagerGlobal=numPager //informer JS du pager Actuel [hack]
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
        document.getElementById("concepteurMesJEEI"+i).innerHTML="<B> Concepteur</B> : "+listeMesJEEI.auteurs[(indexDBSol+i)]
        document.getElementById("nomMesJEEI"+i).innerHTML=listeMesJEEI.noms[(indexDBSol+i)]
        document.getElementById("imgMesJEEI"+i).innerHTML='<img   src='+listeMesJEEI.img[(indexDBSol+i)]+' class="card-img-top imgCardMesJEEI"  alt="...">'
        document.getElementById("themeMesJEEI"+i).innerHTML="<B> Thème</B> : "+listeMesJEEI.themes[(indexDBSol+i)]
        document.getElementById("statutMesJEEI"+i).innerHTML="<B> Evolution apprentissage (moyenne)</B> :"+listeMesJEEI.scores[(indexDBSol+i)]
        document.getElementById("descriptifMesJEEI"+i).innerHTML=listeMesJEEI.descriptifs[(indexDBSol+i)]
        document.getElementById("nbrExperimentationsMesJEEI"+i).innerHTML="<B> Nbr expérimentations</B> :"+listeMesJEEI.nbrExperimentations[(indexDBSol+i)]

        //pour gerer le disabled si jms il est pas validé
        if(listeMesJEEI.estValide[(indexDBSol+i)]==1)
        {
            document.getElementById("btnExperimentationMesJeei"+i).innerHTML="<a  href='http://127.0.0.1:5000/uneExperimentation?idJEEI="+listeMesJEEI.id[(indexDBSol+i)]+"' role='button' class='btn btn-outline-warning'>Expérimenter</a>"
        }
        else
        {
            document.getElementById("btnExperimentationMesJeei"+i).innerHTML="<a  href='http://127.0.0.1:5000/uneExperimentation?idJEEI="+listeMesJEEI.id[(indexDBSol+i)]+"' role='button' class='btn btn-outline-warning disabled' >Expérimenter</a>"
        }




        document.getElementById("btnDataMesJeei"+i).innerHTML="<a class='btn btn-outline-secondary  ' href='http://127.0.0.1:5000/specificationMesJEEI?idJEEI="+listeMesJEEI.id[(indexDBSol+i)]+"' role='button' >Data</a>"
        document.getElementById("btnEffacerMesJeei"+i).innerHTML="<a class='btn btn-outline-danger ' href='http://127.0.0.1:5000/SupprimerMonJEEI?idJEEI="+listeMesJEEI.id[(indexDBSol+i)]+"' role='button' disabeld >Supprimer</a>"
    }
    
    //regler le probleme de la dernière page qui peut contenir moins de 4 elements (suite)
    if(numPager==nbrPagesTotal)//si on est à la dernière page
    {
        for(let i=3;i>=nbrCarteAAfficher;i--)
        {

            document.getElementById("carteMesJEEI"+i).style.visibility = "hidden";
        }
    }
    window.top.window.scrollTo(0,0)//permet de revenir en haut de la page (sinon ca reste bloqué sur le pager-->pas top)


}

//redirection vers la route de notre choix (j'ai du faire ca pour gerer onclick et rendre ma carte cliquable)
function redirectionVers(numCarte)
{
    if(numPagerGlobal==null)//dans le cas où on arrive sur la page et qu'on a pas encore cliqué sur le pager [hck]
    {
        console.log("DANS NAN")
        numPagerGlobal=1
    }

        
        console.log("redirectionvers")
        numPagerGlobal=parseInt(numPagerGlobal)
        numCarte=parseInt(numCarte)
        let idJEEI=(numPagerGlobal-1)*4+numCarte+1
        //idJEEI=idJEEI.toString()
        console.log(idJEEI)
        adresseRedicrection = '/specificationMesJEEI?idJEEI='+idJEEI 
        console.log(adresseRedicrection)
        
        location.href = adresseRedicrection;


}




