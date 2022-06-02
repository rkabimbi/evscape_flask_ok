function fonction_confirmationConsentement(experimentationId,participantId)
{
    console.log("fonction_confirmationConsentement")

    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/confirmationConsentement?experimentationId='+ experimentationId+'&participantId='+participantId);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            reponseBackEndConfirmationConsentement(this.responseText)   
        }
    };

}

function reponseBackEndConfirmationConsentement(reponseText)
{
    console.log("il a consenti")
    window.location.href = "http://127.0.0.1:5000//remerciements";
}