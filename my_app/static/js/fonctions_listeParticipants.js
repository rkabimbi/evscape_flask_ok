
function fonction_ajouterParticipant(idExperimentation){
    console.log("fonction_ajouterParticipant")
    console.log(idExperimentation)
    nom=document.getElementById('idNomListeParticipant').value
    prenom= document.getElementById('idPrenomListeParticipant').value
    email= document.getElementById('idEmailListeParticipant').value
    


    var xhttp = new XMLHttpRequest( );
    let url = new URL('http://127.0.0.1:5000/ajouterParticipant?experimentationId='+ idExperimentation+'&participantNom='+nom +'&participantPrenom='+prenom +'&participantEmail='+email);  
    xhttp.open("GET", url.toString(), true);
    xhttp.send()
    xhttp.onreadystatechange = function()
    { 
        if (this.readyState == 4 && this.status == 200) 
        {
            reponseBackEndAjouterParticipant(this.responseText)   
        }
    };





}

function reponseBackEndAjouterParticipant(responseText)
{
    console.log("retour du backend")
    var fichJsonParse=JSON.parse(responseText)
    console.log(fichJsonParse)

    htmlScroll = document.getElementById('zoneScrollListeParticipants').innerHTML
    //console.log(htmlScroll)
   
    newParticipantHtml ='<div class="col-sm-12 carteListeParticipant"><ul class="list-group list-group-flush"><li class="list-group-item"><B> Nom</B> : '+fichJsonParse.reponse.nom+'<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></li><li class="list-group-item"><B> Prénom</B> : '+fichJsonParse.reponse.prenom+'</li><li class="list-group-item"><B> Email </B>: '+fichJsonParse.reponse.email+'</li><li class="list-group-item"><B> Consentement </B>:  <span class="badge badge-pill badge-danger"> Non</span></li></ul></div>'

    htmlScroll=htmlScroll+newParticipantHtml
    document.getElementById('zoneScrollListeParticipants').innerHTML=htmlScroll
    
} 