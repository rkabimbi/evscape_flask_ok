
function fonction_Presentation()
{
    console.log("fonction_Presentation")
    fonction_activationBouton("navLinkPresentation")
    
}

function fonction_Documentation()
{
    console.log("fonction_Documentation")
    fonction_activationBouton("navLinkDocumentation")
}

function fonction_Resultats()
{
    console.log("fonction_Resultats")
    fonction_activationBouton("navLinkResultats")
}


function fonction_Test()
{
    console.log("fonction_Test")
    fonction_activationBouton("navLinkTest")
}



function fonction_ListeExperimentations()
{
    console.log("fonction_ListeExperiemtnation")
    fonction_activationBouton("navLinkListeExperimentations")
}




//permet de mettre en evidence le bouton qui est selectionné
function fonction_activationBouton(boutonAColorer)
{
    codeHtml =  document.getElementById(boutonAColorer).innerHTML
    
    //on désactive tous les autres
    document.getElementById("navLinkListeExperimentations").innerHTML='<a  class="nav-link" onclick="fonction_ListeExperimentations()">Liste Experimentations</a>'
    document.getElementById("navLinkTest").innerHTML='<a  class="nav-link" onclick="fonction_Test()">Test</a>'
    document.getElementById("navLinkResultats").innerHTML='<a  class="nav-link" onclick="fonction_Resultats()">Resultats</a>'
    document.getElementById("navLinkDocumentation").innerHTML='<a  class="nav-link" onclick="fonction_Documentation()">Documentation</a>'
    document.getElementById("navLinkPresentation").innerHTML='<a  class="nav-link" onclick="fonction_Presentation()">Présentation</a>'
    


    //Remplace la ligne de spécification du bouton dans HTML pour que ca devienne actif
    //techniquement j'ajoute juste un "active" à class="nav-link "
    if(boutonAColorer=="navLinkListeExperimentations")
    {
        document.getElementById("navLinkListeExperimentations").innerHTML='<a  class="nav-link active" onclick="fonction_ListeExperimentations()">Liste Experimentations</a>'
    }
    else if (boutonAColorer=="navLinkTest")
    {
        document.getElementById("navLinkTest").innerHTML='<a  class="nav-link active" onclick="fonction_Test()">Test</a>'
    }
    else if(boutonAColorer=="navLinkResultats")
    {
        document.getElementById("navLinkResultats").innerHTML='<a  class="nav-link active" onclick="fonction_Resultats()">Resultats</a>'
    }
    else if(boutonAColorer=="navLinkDocumentation")
    {
        document.getElementById("navLinkDocumentation").innerHTML='<a  class="nav-link active" onclick="fonction_Documentation()">Documentation</a>'
    }
    else if(boutonAColorer=="navLinkPresentation")
    {
        document.getElementById("navLinkPresentation").innerHTML='<a  class="nav-link active" onclick="fonction_Presentation()">Présentation</a>'
    }
   
}
