function fonction_sauverPreTest(idParticipant,questionsApprentissage)
{
    console.log(fonction_sauverPreTest)
    console.log(questionsApprentissage)


    //je recupere tte les valeur de mon questionnaire
    reponseQ1=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ2=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ3=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ4=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ5=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ6=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ7=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ8=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ9=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    reponseQ10=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;


    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/sauvegardeQuestionnairePreTest?idParticipant='+ idParticipant+'&responseQ1='+reponseQ+'&responseQ2='+reponseQ2  +'&responseQ3='+reponseQ3 +'&responseQ4='+reponseQ4 +'&responseQ5='+reponseQ5 +'&responseQ6='+reponseQ6 +'&responseQ7='+reponseQ7 +'&responseQ8='+reponseQ8 +'&responseQ9='+reponseQ9 +'&responseQ10='+reponseQ10 );  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            reponseBackEndPreTest(this.responseText)   
        }
    };

    
}

function reponseBackEndPreTest(this.responseText) 
{
    console.log("retour du back pour le questionnaire preTest")
}