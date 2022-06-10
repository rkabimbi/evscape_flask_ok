
function sauverFormulaireDemographique(idParticipant, idExperimentation)
{
    
    console.log("sauverFormulaireDemographique")
    age= document.getElementById("idQuestionnaireDemographiqueAgeParticipant").value
    sexe = document.getElementById("idQuestionnaireDemographiqueSexeParticipant").value
    localisation = document.getElementById("idQuestionnaireDemographiqueLocalisationParticipant").value
    experience = document.getElementById("idQuestionnaireDemographiqueExperienceParticipant").value
    experienceJeei = document.getElementById("idQuestionnaireDemographiqueExperienceJeeiParticipant").value

    etude = document.getElementById("idQuestionnaireDemographiqueEtudesParticipant").value

    
    console.log("idParticipant "+ idParticipant+ "idExperiemnation:"+ idExperimentation+"age : "+age+"sexe"+sexe+ experienceJeei+" ... "+etude)

    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/sauvegardeQuestionnaireDemographique?idParticipant='+ idParticipant+'&idExperimentation='+idExperimentation+'&age='+age+'&sexe='+sexe+'&localisation='+localisation+'&experience='+experience+'&experienceJeei='+experienceJeei +'&etude='+etude );  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            reponseSauvegardeQuestionnaireDemographique(this.responseText)   
        }
    };
}

function reponseSauvegardeQuestionnaireDemographique(responseText)
{
    console.log("reponseSauvegardeQuestionnaireDemographique")
    console.log(responseText)
    window.location.replace("http://127.0.0.1:5000/remerciements");

  
}