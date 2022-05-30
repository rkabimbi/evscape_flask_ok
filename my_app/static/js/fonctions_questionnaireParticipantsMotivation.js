
/*
function sauverFormulaireMotivation(idParticipant, idExperimentation)
{
    console.log("sauverFormulaireDemographique")
    m01= document.getElementsByName("likert"+"m01"+"idExperimentation").value
    console.log(m01)

    
    console.log("idParticipant "+ idParticipant+ "idExperiemnation:"+ idExperimentation+"age : "+age+"sexe"+sexe+ experienceJeei)

    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/sauvegardeQuestionnaireMotivation?idParticipant='+ idParticipant+'&idExperimentation='+idExperimentation+'&age='+age+'&sexe='+sexe+'&localisation='+localisation+'&experience='+experience+'&experienceJeei='+experienceJeei  );  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            reponseSauvegardeQuestionnaireMotivation(this.responseText)   
        }
    };
}

function reponseSauvegardeQuestionnaireMotivation(responseText)
{
    console.log("reponseSauvegardeQuestionnaireDemographique")
    console.log(responseText)
    window.location.replace("http://127.0.0.1:5000/remerciements");

  
}
*/