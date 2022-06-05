function fonction_debloquerFormulaireDemographique(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerFormulaireDemographique")
    console.log("On va chercher à débloquer le formulaire en live pour :"+idJEEI + " et l'experimentation :"+idExperimentation)

    //juste renvoyer le num d'IDexperimentation coté back...là il recupere tt les candidats et cree
    //une veluation pr eux  + leur envoi un email 
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/debloquerFormulaireDemographique?idExperimentation='+ idExperimentation);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            retourDebloquerFormulaireDemographique(this.responseText)   
        }
    };
}


function retourDebloquerFormulaireDemographique(responseText)
{
    console.log("retourDebloquerFormulaireDemographique")
    console.log(responseText)
    //var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    
    document.getElementById("etapeExperimentation3").innerHTML='<h5 class="card-title" style="color: grey; font-weight: bold;" id="etapeExperimentation2">Etape 3 <span class="badge badge-success" style="margin-left:15px">emails envoyés</span>'

}




function fonction_bloquerFormulaireDemographique(idJEEI, idExperimentation)
{
    console.log("fonction_bloquerFormulaireDemographique")
    console.log("On va chercher à bloquer le formulaire en live pour :"+idJEEI + " et l'experimentation :"+idExperimentation)
   
}




function fonction_confirmerCoursOk(idJEEI, idExperimentation)
{
    console.log("fonction_confirmerCoursOk")
    console.log(" dire au back end que le cours ets donné (modification classe experimentation) et grisser la case")
}


function fonction_debloquerPreTest(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerPreTest")
    


    //juste renvoyer le num d'IDexperimentation coté back...là il recupere tt les candidats et cree
    //une veluation pr eux  + leur envoi un email 
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/debloquerFormulairePreTest?idExperimentation='+ idExperimentation);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            retourDebloquerFormulairePreTest(this.responseText)   
        }
    };
   
}

function retourDebloquerFormulairePreTest(responseText)
{
    console.log("retourDebloquerFormulairePreTest")
    console.log(responseText)
    //var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    
    document.getElementById("etapeExperimentation7").innerHTML='<h5 class="card-title" style="color: grey; font-weight: bold;" id="etapeExperimentation2">Etape 7 <span class="badge badge-success" style="margin-left:15px">emails envoyés</span>'


}



function fonction_bloquerPreTest(idJEEI, idExperimentation)
{
    console.log("fonction_bloquerPreTest")
    
   
}


function fonction_confirmerCoolingPeriodOk(idJEEI, idExperimentation)
{
    console.log("fonction_confirmerCoolingPeriod Ok")
 
}

function fonction_confirmerActiviteOk(idJEEI, idExperimentation)
{
    console.log("fonction_confirmerActiviteOk")
  
}


function fonction_debloquerPostTest(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerPostTest")
    


    //juste renvoyer le num d'IDexperimentation coté back...là il recupere tt les candidats et cree
    //une veluation pr eux  + leur envoi un email 
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/debloquerFormulairePostTest?idExperimentation='+ idExperimentation);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            retourDebloquerFormulairePostTest(this.responseText)   
        }
    };
   
}

function retourDebloquerFormulairePostTest(responseText)
{
    console.log("retourDebloquerFormulairePostTest")
    console.log(responseText)
    //var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    document.getElementById("etapeExperimentation10").innerHTML='<h5 class="card-title" style="color: grey; font-weight: bold;" id="etapeExperimentation2">Etape 10 <span class="badge badge-success" style="margin-left:15px">emails envoyés</span>'


}


function fonction_debloquerUX(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerUX")
   
}



function fonction_bloquerUX(idJEEI, idExperimentation)
{
    console.log("fonction_bloquerUX")
   
}


function fonction_confirmerFocusGroupOk(idJEEI, idExperimentation)
{
    console.log("fonction_confirmerFocusGroupsOk")
    
}


function fonction_debloquerPostTestRetention(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerPostTest II")
   
}



function fonction_bloquerPostTest(idJEEI, idExperimentation)
{
    console.log("fonction_bloquerPostTest II")
   
}


function fonction_debloquerMotivation(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerMotivation")
 
    console.log("On va chercher à débloquer le formulaire de motivation en live pour :"+idJEEI + " et l'experimentation :"+idExperimentation)

    //juste renvoyer le num d'IDexperimentation coté back...là il recupere tt les candidats et cree
    //une veluation pr eux  + leur envoi un email 
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/debloquerFormulaireMotivation?idExperimentation='+ idExperimentation);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            retourDebloquerFormulaireMotivation(this.responseText)   
        }
    };
    
}

function retourDebloquerFormulaireMotivation(responseText)
{
    console.log("retourDebloquerFormulaireMotivation")
    console.log(responseText)
    //var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    document.getElementById("etapeExperimentation6").innerHTML='<h5 class="card-title" style="color: grey; font-weight: bold;" id="etapeExperimentation2">Etape 6 <span class="badge badge-success" style="margin-left:15px">emails envoyés</span>'


}


function fonction_debloquerUX(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerUX")
 
    console.log("On va chercher à débloquer le formulaire de motivation en live pour :"+idJEEI + " et l'experimentation :"+idExperimentation)

    //juste renvoyer le num d'IDexperimentation coté back...là il recupere tt les candidats et cree
    //une veluation pr eux  + leur envoi un email 
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/debloquerFormulaireUX?idExperimentation='+ idExperimentation);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            retourDebloquerFormulaireUX(this.responseText)   
        }
    };
    
}

function retourDebloquerFormulaireUX(responseText)
{
    console.log("retourDebloquerFormulaireUX")
    console.log(responseText)
    //var fichJsonParse=JSON.parse(responseText);//parsing du fichier JSON envoyé par jsonify
    document.getElementById("etapeExperimentation11").innerHTML='<h5 class="card-title" style="color: grey; font-weight: bold;" id="etapeExperimentation2">Etape 11 <span class="badge badge-success" style="margin-left:15px">emails envoyés</span>'


}



function fonction_bloquerMotivation(idJEEI, idExperimentation)
{
    console.log("fonction_bloquerMotivation")
    
}


function fonction_validerEtape(experimentationId,etape )
{
    console.log("fonctiiion_validerEtape")
    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/validerEtapeExperimentation?idExperimentation='+ experimentationId+'&etape='+etape);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            retourValidationEtape(this.responseText,etape)   
        }
    };
}

function retourValidationEtape(responseText,etape)
{
    console.log("retourValidationEtape")
    document.getElementById("etapeExperimentation"+etape).innerHTML='<h5 class="card-title" style="color: grey; font-weight: bold;" id="etapeExperimentation2">Etape '+etape+'<span class="badge badge-warning" style="margin-left:15px">étape validée</span>'

    document.getElementById("btnValiderEtape"+etape).disabled=true
    nextetape=etape+1//pour debloquer l'etape d'apres
    //si c'est un bouton où il y a un bouton "debloquer avec" alors il doit griser le "debloquer aussi"
    if(etape==3|| etape==6 || etape==7 || etape==10 || etape==11 || etape==13)
    {
        document.getElementById("btnValiderEtapeDebloque"+etape).disabled=true
        console.log("je bloque le debloquer de l'etape "+etape)
        
    }
    if (etape==4)
    {
        next=nextetape+1
        document.getElementById("btnValiderEtapeDebloque"+next).disabled=false
        console.log("je débloque le debloquer de l'etape "+next)

        document.getElementById("btnValiderEtape"+next).disabled=false
        console.log("je débloque le bloquer de l'etape "+next)
    }

    //pour gerer les cas où il y a un ou deux boutons à débloquer après
    if(nextetape==3|| nextetape==6 || nextetape==7 || nextetape==10 || nextetape==11 || nextetape==13)
    {
        document.getElementById("btnValiderEtapeDebloque"+nextetape).disabled=false
        console.log("je débloque le debloquer de l'etape "+nextetape)

        document.getElementById("btnValiderEtape"+nextetape).disabled=false
        console.log("je débloque le bloquer de l'etape "+nextetape)
    }
    else{
            
        document.getElementById("btnValiderEtape"+nextetape).disabled=false
        console.log("je débloque le bloquer de l'etape "+nextetape)
    }



}
