//declaration des variables
let jeveuxoff; //declaration de variable de ce que veut l'utilisateur
let typebienoff; //declaration de variable du type de bien selectionné
let paysoff; //declaration de variable du pays qui sera entrée
let villeoff; //declaration de variable du pays qui sera entrée
let arrondissementoff; //declaration de variable arrondissement de la ville qui sera entrée
let formdata = {}; //un objet qui va contenir les infos de l'utilisateur avant de l'envoyer aux données
let nombrechambreoff = []; //dit si on veut un t1, t2...
let vente;
let prix_minimumoff;
let prix_maximumoff;
let detail_en_plusoff;



//lancer des le lancement de programme
document.addEventListener("DOMContentLoaded", () => {
    const menu = document.querySelectorAll('ul > li');
    switch (id) {
        case "appartement" :
            elementclique = menu[1];
            vente = elementclique.innerText; //elementclique.innerText retourne le nom du titre qui a été cliqué
            afficher("appartement", elementclique);
            break;
        case "villa" :
            elementclique = menu[2];
            vente = elementclique.innerText;
            afficher("villa", elementclique);
            break;
        case "bureau_et_commerce" :
            elementclique = menu[3];
            vente = elementclique.innerText;
            afficher("bureau_et_commerce", elementclique);
            break;

        case "autre" :
            elementclique = menu[4];
            vente = elementclique.innerText;
            afficher("autre", elementclique);
            break;
        default :
            if (!id==""){
                document.location.href="/";
            }
            break;
    }
})