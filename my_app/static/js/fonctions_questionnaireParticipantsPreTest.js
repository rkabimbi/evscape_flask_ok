function fonction_sauverPreTest(idParticipant,questionsApprentissage)
{
    console.log("fonction_sauverPreTest")
    console.log(questionsApprentissage)


    //je recupere tte les valeur de mon questionnaire
    responseQ1=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[0]+'"]:checked').value;
    responseQ2=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[1]+'"]:checked').value;
    responseQ3=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[2]+'"]:checked').value;
    responseQ4=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[3]+'"]:checked').value;
    responseQ5=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[4]+'"]:checked').value;
    responseQ6=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[5]+'"]:checked').value;
    responseQ7=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[6]+'"]:checked').value;
    responseQ8=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[7]+'"]:checked').value;
    responseQ9=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[8]+'"]:checked').value;
    responseQ10=document.querySelector('input[name="flexRadioDefault'+questionsApprentissage.id[9]+'"]:checked').value;


    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/sauvegardeQuestionnairePreTest?idParticipant='+ idParticipant+'&responseQ1='+responseQ1+'&responseQ2='+responseQ2  +'&responseQ3='+responseQ3 +'&responseQ4='+responseQ4 +'&responseQ5='+responseQ5 +'&responseQ6='+responseQ6 +'&responseQ7='+responseQ7 +'&responseQ8='+responseQ8 +'&responseQ9='+responseQ9 +'&responseQ10='+responseQ10 );  
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

function reponseBackEndPreTest(responseText) 
{
    console.log("retour du back pour le questionnaire preTest")
  
    window.location.href = "http://127.0.0.1:5000/remerciements";
}