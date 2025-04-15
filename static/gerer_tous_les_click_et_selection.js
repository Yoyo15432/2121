//gère tous les click de la page formulaire
// declaration des variables
let submit1; //ce sera le boutton suivant du formulaire 1
let submit2; //ce sera le bouton suivant du formulaire 2
let submit3; //ce sera le bouton validé du formulaire 3
let prev2; //ce sera le bouton précédent du formulaire 2
let pays; //pour gérer les villes de l'api

//les actions des différents boutons s'ils sont cliqués
function event1(){ //suivant form1 à 2
    // ajout des données dans le dictionnaire
    if (!repassage){ //vérifie si l'utilisateur et revenue sur la page precedente : s il n'était pas revu, alors on créer le nouveau formulaire 2, sinon on lui raffiche le formulaire
        afficher2();
    }
    else {
        container.querySelector("#form1").style.display = "none";
        container.querySelector("#form2").style.display="block";
        if (islogin=='True' || isloginagence=='True')
            animation_progress_bar(100);
        else {
            animation_progress_bar(68);
        }
    }
}

function event2(){ //precedent form2 à 1
    submit1.addEventListener('click', event1); //reactive l'ecouteur suivant
    //animation progress bar
    if (islogin=='True' || isloginagence=='True'){
        animation_progress_bar(50);
    }
    else {
        animation_progress_bar(34);
    }
    container.querySelector("#form2").style.display="none";
    container.querySelector("#form1").style.display = "block";
}

function event3(){ //suivant form2 à 3
    if (!repassage2){
        afficher_login();
    }
    else {
        animation_progress_bar(100);
        formulaire3.style.display = "block";
        formulaire2.style.display = "none";
    }

    //ecouter pour voir si la personne est connecté
    interval = setInterval(event =>{
        if (islogin=='True'){
            document.querySelector("#valider").disabled = false;
            document.querySelector("#valider").style.cursor = "pointer"; //la survole de la sourir est un pointer car valider est maintenant activé
            clearInterval(interval);
            clearInterval(interval2);
        }
        },1000)
}

function event4(){ // precedent form3 à 2
    animation_progress_bar(68);
    formulaire3.style.display = "none";
    formulaire2.style.display = "block";
    prev2.addEventListener('click', event2);
    submit2.addEventListener('click', event3);
    clearInterval(interval);
}

function valider(event) { //valide le formulaire et va faire le necessaire dans le serveur
    //on defini les valeurs
    event.preventDefault();
    prix_minimumoff = parseInt(document.querySelector("#prix_actu_min").innerText.replace(/\D/g, "")); //replace(/\D/g, "") enleve tous les espaces et symbole qui n est pas un chiffre
    prix_maximumoff = parseInt(document.querySelector("#prix_actu_max").innerText.replace(/\D/g, "")); //replace(/\D/g, "") enleve tous les espaces et symbole qui n est pas un chiffre
    if (prix_minimumoff>=prix_maximumoff){
        return window.alert("Le prix minimum est plus grand que le prix maximum (section budget)")
    }
    detail_en_plusoff = document.querySelector("#detailbien").value;
    nombrechambreoff = [];
    for (let item of document.querySelectorAll(".nc input:checked")) {
        let label = item.nextElementSibling; //recupere le label se trouvant apres input
        nombrechambreoff.push(label.innerText);
    }
    jeveuxoff = document.querySelector("select[name='vente_loc']").value;


    if (jeveuxoff != null && jeveuxoff != '' &&
        nombrechambreoff != null &&
        paysoff != null &&
        villeoff != null &&
        arrondissementoff != null &&
        typebienoff != null &&
        vente != null)
    {
            //on creer le dictionnaire et le json
            formdata.donnee = {
                "loc_vent_loue": jeveuxoff,
                "pays": paysoff,
                "ville": villeoff,
                "arrondissement": parseInt(arrondissementoff),
                "type_de_bien": {0: vente, 1: typebienoff},
                "prix": {"minimum": prix_minimumoff, "maximum": prix_maximumoff},
                "detail": detail_en_plusoff,
                "nombre_piece": nombrechambreoff
            };
            let dico_user = JSON.stringify(formdata); //renvoie une chaine json qui s'appelle dico_user
            if (islogin=='True') {
                //on envoie les données au serveur pour le traitement
                fetch("/form/<id>", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: dico_user
                })
                    .then(response => {
                        if (response.ok) {
                            // Si la réponse est ok, rediriger la page
                            window.location.href = "/historique";} // Redirige à l'historique
                    else {
                        window.alert("erreur inconnu sur le serveur")
                    }})
                        .catch(Error, "erreur de l'envoie de la requête")
        }
            else {
            window.alert("la connexion a été refusé (non connecté)")
        }
    }
    else {
        window.alert("il nous manque des informations !!! Veuillez remplir les champs")
    }
}
//gérer les click
function gerer_click_form1() { //gere les click du formulaire 1
//gérer le tableau de selection du type de bien et défit typedebienoff

    const element = document.querySelectorAll("#typedebien > :nth-child(n+2)");
    //selectionner les elements
    element.forEach(item => {
        item.addEventListener('click', event => {
            element.forEach(i => {
                i.style.background = '';
                i.style.color = ''
            })
            let elementclique = event.target;
            elementclique.style.background = '#103d77';
            elementclique.style.color = 'white';
            let typebienselect = elementclique.getAttribute("data-value");
            typebienoff = typebienselect;
        });
        item.addEventListener('keydown', event=>{ //pour l'accecibilité : si on click sur entrer, alors on simule un clique (donc fonction de addlistener click lancé)
            if (event.key === "Enter"){
                item.click();
            }
        })
    });




    //passer à la deuxieme page du formulaire
        submit1 = document.querySelectorAll(".suiv_prec input[type='button']")[0]; //c'est le boutton suivant du formulaire 1
        submit1.addEventListener('click', event1); //ajoute les données au dictionnaire et affiche la page suivante
    }

function gerer_click_form2(){ //gere les click du formulaire 2
    submit1.removeEventListener('click', event1); //supprimer l'écouter qui ne sert plus désormé
    prev2 = document.querySelectorAll(".suiv_prec input[type='button']")[1]; // c'est le bouton précédent du formulaire 2 (en position 1 car on a fait display none et pas remove)
    prev2.removeEventListener('click', event2); // desactive pour eviter les conflits
    prev2.addEventListener('click', event2); //affiche la page precedente
    if (islogin=="True"){
        submit3 = document.querySelector("#valider"); //c'est le bouton validé du formulaire
        submit3.addEventListener('click', valider);
    }
    else if(isloginagence=="True"){

    }
    else {
        //passer à la troiseme page du formulaire (page de connexion)
        submit2 = document.querySelectorAll(".suiv_prec input[type='button']")[2]; //c'est le bouton suivant du formulaire 2
        submit2.addEventListener('click', event3);
    }
}

function gerer_click_form3(){ //gérer les click du formulaire 3
    jesuistrois = true;
    prev2.removeEventListener('click', event2); //supprimer l'écouter qui ne sert plus désormé
    submit2.removeEventListener('click', event3); //supprimer l'écouter qui ne sert plus désormé
    submit3 = document.querySelector("#valider"); //c'est le bouton validé du formulaire
    submit3.addEventListener('click', valider);
    const prev3 = document.querySelectorAll(".suiv_prec input[type='button']")[3]; //c'est le bouton précédent du formulaire 3 à 2
    prev3.addEventListener('click', event4);
}


// POUR la gestion des API utilisé pour le pays, ville, arrondissement
//api pour les pays
function pays_trouver(){
    elmpays = document.querySelector(".pays");
    elmpays.innerText = `Pays : ${paysoff}`
    test = true;
    document.getElementById("but2").disabled = false;
    document.getElementById("but1").remove();

}

async function paysapi() {
    promesseville = await fetch("https://restcountries.com/v3.1/all");
    promesseville1 = await promesseville.json();
    input = document.getElementsByName("pays");
    input1 = input[0].value.toLowerCase();
    test=false;
    for (let i=0; i<250; i++) {
        if (promesseville1[i].name.common.toLowerCase().includes(input1) && input1.length>=3){
            input[0].remove();
            paysoff= promesseville1[i].name.common;
            pays = promesseville1[i].name.common;
            pays_trouver();
            break;
        }
        for (let translate in promesseville1[i].translations){
            if (promesseville1[i].translations[translate].common.toLowerCase().includes(input1) && input1.length>=3){
                input[0].remove();
                paysoff= promesseville1[i].translations[translate].common;
                pays = promesseville1[i].name.common;
                pays_trouver();
                break;
            }
        }
    }
    if(!test) {if (input1.length<3){console.log("erreur"); window.alert("essayer un mot plus grand")} else {console.log("erreur"); window.alert("Pays non trouvé")}}
}



//api pour les villes suivant le pays enregistré
async function villeapi() {
    promesseville = await fetch("https://countriesnow.space/api/v0.1/countries/population/cities");
    promesseville1 = await promesseville.json();
    console.log(promesseville);


    input = document.getElementsByName("ville");
    input1 = input[0].value.toLowerCase();
    test = false;
    for (let i = 0; i < 4503; i++) {
        if (promesseville1.data[i].country == pays) { //filtres seulement les villes qui ont le pays selectionné
            if (promesseville1.data[i].city.toLowerCase() == input1) { //si la ville est retrouvé dans l api
                test = true;
                input[0].remove();
                villeoff = promesseville1.data[i].city;
                elmville = document.querySelector(".ville");
                elmville.innerText = `Ville : ${villeoff}`;
                document.getElementById("but2").remove();
                document.getElementById("but3").disabled = false;
                break;
            }
        }
    }
    if (!test) {
        console.log("erreur");
        window.alert("Ville non trouvé")
    }
}

//entrer les arrondissements quand ville et pays sont entrées
window.arrondissement = function (){
    input = document.getElementsByName("arrondissement");
    arrondissementoff = input[0].value;
    elmarrondissement = document.querySelector("label.arrondissement");
    elmarrondissement.innerText = `Arrondissement : ${arrondissementoff}`;
    input[0].remove();
    document.getElementById("but3").remove();
}
document.addEventListener("click", event => {
    if (event.target && event.target.id === "but3") {
        arrondissement();
    }
});
