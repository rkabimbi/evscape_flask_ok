function fonction_debloquerFormulaireDemographique(idJEEI, idExperimentation)
{
    console.log("fonction_debloquerFormulaireDemographique")
    console.log("On va chercher à débloquer le formulaire en live pour :"+idJEEI + " et l'experimentation :"+idExperimentation)
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
   
}



function fonction_bloquerPostTest(idJEEI, idExperimentation)
{
    console.log("fonction_bloquerPostTest")
   
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
    document.getElementById("etapeExperimentation"+etape).innerHTML='<h5 class="card-title" style="color: grey; font-weight: bold;" id="etapeExperimentation2">Etape '+etape+'<span style="color:green"> [étape validée]</span>'

    document.getElementById("btnValiderEtape"+etape).disabled=true
}
