
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
   
}


//variables globales pour pouvoir reset ensuite facilement (sinon pas possible de recuperer aprys un style.display="none")
//en plus comme ça il garde les données du formulaire

    displayDocumentation=document.getElementById("idContenuSousPageDocumentation").style.display
    displayTest=document.getElementById("idContenuSousPageTest").style.display
    displayResultats=document.getElementById("idContenuSousPageResultats").style.display
    displayListeExperimentations=document.getElementById("idContenuSousPageListeExperimentations").style.display
    displayPresentation= document.getElementById("idContenuSousPagePresentation").style.display



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
            document.getElementById(idSousPage).style.display=displayPresentation
            break;

        case 'idContenuSousPageDocumentation':
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById(idSousPage).style.display=displayDocumentation
            break;

        case 'idContenuSousPageTest':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById(idSousPage).style.display=displayTest
            break;

        case 'idContenuSousPageResultats':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById("idContenuSousPageListeExperimentations").style.display="none"
            document.getElementById(idSousPage).style.display=displayResultats
            break;

        case 'idContenuSousPageListeExperimentations':
            document.getElementById("idContenuSousPageDocumentation").style.display="none"
            document.getElementById("idContenuSousPageTest").style.display="none"
            document.getElementById("idContenuSousPageResultats").style.display="none"
            document.getElementById("idContenuSousPagePresentation").style.display="none"
            document.getElementById(idSousPage).style.display=displayListeExperimentations
            break;
    }

}
