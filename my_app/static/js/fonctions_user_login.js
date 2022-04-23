


//fonction me sert à simuler une SPA
function chargementFormulaireInscription()
{
    console.log("chargementFormulaireInscription")
    //je recupere dans le fichier HTML composantInscription l'element dont l'id est composantInscription et le met dans une variable 
    composantInscription=document.getElementById("composantInscription").innerHTML
    console.log(composantInscription)
    //je transfert ce code HTML dans un autre composant :D
    document.getElementById("composantLogin").innerHTML=composantInscription
    
}