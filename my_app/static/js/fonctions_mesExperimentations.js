



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
    //selection de c

}


function redirectionVersUneExperimentation(idExperimentation)
{
    adresseRedicrection = '/afficherUneExperimentationExistante?idExperimentation='+idExperimentation 
    console.log(adresseRedicrection)
    
    location.href = adresseRedicrection;
}
