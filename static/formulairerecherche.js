//LES PAGES DES FORMULAIRES//

//déclaration des variables
const suivant = '<input type="button" value="Suivant">';
const precedent = '<input type="button" value="Précédent">';
const valide = '<input id="valider" type="submit" value="Valider" style="cursor: pointer">';
let repassage; //vérifie si on est repasse juste au formulaire 1 pour éviter d'en créer un nouveau
let repassage2;
let formulaire1;
let formulaire2;
let formulaire3;

//animation lors de l'avancement de la barre
function animation_progress_bar(valeur){
    let i = document.querySelector("#barreprogress").value //valeur de la progression actuelle (récupérer pour pemmettre l'animation
    if (valeur>i){
        d = setInterval(event=>{i++; document.querySelector("#barreprogress").value = i; if(i>=valeur){clearInterval(d)}}, 10)
    }
    else {
        d = setInterval(event=>{i--; document.querySelector("#barreprogress").value = i; if(i<=valeur){clearInterval(d)}}, 10)
    }
}


//récupère la section formulaire (pour afficher les différentes pages)
function pour_tous_page_config(){ //pour déclarer l'élément
    container = document.getElementsByClassName("formulaire")[0]; //recupere l element section formulaire
}

//premiere page du formulaire
function afficher(id, elementclique){
    pour_tous_page_config();
    repassage = false;
    //affiche la barre de progression
    document.querySelector("#barreprogress").display = "block";
    if (islogin=='True' || isloginagence=='True'){
        animation_progress_bar(50);
    }
    else {
        animation_progress_bar(34);
    }


    elementclique.querySelectorAll('a').forEach(link => {link.style.color = '#4065c6';}); //l element du menu qui est selectionne

    //supprime tous les formulaires créer s'il y en a (pour éviter les conflits)
    if (container.querySelector("form")!=null) {container.querySelectorAll("form").forEach(form=>form.remove());} //supprimer le(s) formulaire(s) actuelle dans section "formulaire"

    //creation du nouveau formulaire (page 1)
    formulaire1 = document.createElement('form'); //creer l'element form
    formulaire1.setAttribute('id', 'form1');


    //afficher l'élément si appartement est selectionné
    if (id=="appartement"){
        document.getElementsByClassName("titre")[0].innerHTML = "<h1>Recherche d'appartement </h1>";

        //j'écris mon html
        formulaire1.innerHTML = `
        <!--si tu veux vendre ou louer-->
            <div id="vente_loc">
                <label for="vente_loc">Je veux : </label>
                <select style="width: 400px;" name="vente_loc" required aria-required="true">
                    <option value="" disabled selected>--Selectionner--</option>
                    <option value="Vente_neuf">Etre propriétaire (d'un appartement neuf)</option>
                    <option value="Vente_ancien">Etre propriétaire (d'un appartement ancien)</option>
                    <option value="Location">Etre locataire </option>
                </select>
            </div><br>
            <!--fin de si tu veux vendre ou louer-->

            <!--choisir le type correspondant au bien-->
            <div id="typedebien">
                <center><label for="typedebien">Choisissez le type de bien que vous cherchez : </label></center>
                <div tabindex="0" data-value="Appartement">Appartement (T2-T7)</div>
                <div tabindex="0" data-value="Duplex">Duplex</div>
                <div tabindex="0" data-value="Triplex">Triplex</div>
                <div tabindex="0" data-value="Studio">Studio</div>
                <div tabindex="0" data-value="Loft">Loft</div>
                <div tabindex="0" data-value="Rez_de_jardin">Rez de jardin</div>
                <div tabindex="0" data-value="Viager appartement">Viager appartement</div>
            </div>
            <div class="suiv_prec">
                ${suivant}
            </div>
        `
    }

    //afficher l'élément si villa est selectionné
    if (id=="villa"){
        document.getElementsByClassName("titre")[0].innerHTML = "<h1>Recherche de villa </h1>";
        //j'écris mon html
        formulaire1.innerHTML = `
        <!--si tu veux vendre ou louer-->
            <div id="vente_loc">
                <label for="vente_loc">Je veux : </label>
                <select style="width: 400px;" name="vente_loc" required aria-required="true">
                    <option value="" disabled selected>--Selectionner--</option>
                    <option value="Vente_neuf">Etre propriétaire (d'une villa neuf)</option>
                    <option value="Vente_ancien">Etre propriétaire (d'une villa ancien)</option>
                    <option value="Location">Etre locataire </option>
                </select>
            </div><br>
            <!--fin de si tu veux vendre ou louer-->

        <!--choisir le type correspondant au bien-->
            <div id="typedebien">
                <center><label for="typedebien">Choisissez le type de bien que vous cherchez : </label></center>
                <div tabindex="0" data-value="Château">Château</div>
                <div tabindex="0" data-value="Bastide">Bastide</div>
                <div tabindex="0" data-value="Ferme">Ferme</div>
                <div tabindex="0" data-value="Maison">Maison</div>
                <div tabindex="0" data-value="Maison de village">Maison de village</div>
                <div tabindex="0" data-value="Mas">Mas</div>
                <div tabindex="0" data-value="Viager maison">Viager maison</div>
                <div tabindex="0" data-value="Villa">Villa</div>
                <div tabindex="0" data-value="Propriété">Propriété</div>
                <div tabindex="0" data-value="Rez de villa">Rez de villa</div>
            </div>
            <div class="suiv_prec">
                ${suivant}
            </div>
        `
    }

    //afficher l'élément si Bureau est selectionné
    if(id=="bureau_et_commerce"){
        document.getElementsByClassName("titre")[0].innerHTML = "<h1>Recherche de bureau </h1>";
        //j'écris mon html
        formulaire1.innerHTML = `
                <!--si tu veux vendre ou louer-->
            <div id="vente_loc">
                <label for="vente_loc">Je veux : </label>
                <select style="width: 400px;" name="vente_loc" required aria-required="true">
                    <option value="" disabled selected>--Selectionner--</option>
                    <option value="Vente_neuf">Etre propriétaire (d'un bureau neuf)</option>
                    <option value="Vente_ancien">Etre propriétaire (d'un bureau ancien)</option>
                    <option value="Location">Etre locataire </option>
                </select>
            </div><br>
            <!--fin de si tu veux vendre ou louer-->

        <!--choisir le type correspondant au bien-->
            <div id="typedebien" style="align-items: center">
                <center><label for="typedebien">Choisissez le type de bien que vous cherchez : </label></center>
                <div tabindex="0" data-value="Bureau">Bureau <span style="font-size: 12pt; font-style: italic"> (Ajouter la superficie en m² des bureaux dans la section détail)</span></div>
                <div tabindex="0" data-value="Local d'activité">Local d'activité</div>
                <div tabindex="0" data-value="Cession de droit au bail">Cession de droit au bail</div>
                <div tabindex="0" data-value="Fond de commerce">Fond de commerce</div>
                <div tabindex="0" data-value="Local commercial">Local commercial</div>
                <div tabindex="0" data-value="Local professionnel">Local professionnel</div>
                <div tabindex="0" data-value="Murs commerciaux">Murs commerciaux</div>
                <div tabindex="0" data-value="Terrain">Terrain</div>
            </div>
            <div class="suiv_prec">
                ${suivant}
            </div>
        `
    }


    if (id=="autre"){
        document.getElementsByClassName("titre")[0].innerHTML = "<h1>Autre recherche possible </h1>";
        //j'écris mon html
        formulaire1.innerHTML = `
                <!--si tu veux vendre ou louer-->
            <div id="vente_loc">
                <label for="vente_loc">Je veux : </label>
                <select style="width: 400px;" name="vente_loc" required aria-required="true">
                    <option value="" disabled selected>--Selectionner--</option>
                    <option value="Vente_neuf">Etre propriétaire (d'un bien neuf)</option>
                    <option value="Vente_ancien">Etre propriétaire (d'un bien ancien)</option>
                    <option value="Location">Etre locataire </option>
                </select>
            </div><br>
            <!--fin de si tu veux vendre ou louer-->

        <!--choisir le type correspondant au bien-->
            <div id="typedebien" style="align-items: center">
                <center><label for="typedebien">Choisissez le type de bien que vous cherchez : </label></center>
                <div tabindex="0" data-value="Garage">Garage</div>
                <div tabindex="0" data-value="Cabanon">Cabanon</div>
                <div tabindex="0" data-value="Cave">Cave</div>
                <div tabindex="0" data-value="Chalet">Chalet</div>
                <div tabindex="0" data-value="Immeuble">Immeuble</div>
                <div tabindex="0" data-value="Parking">Parking</div>
                <div tabindex="0" data-value="Viager">Viager</div>
                <div tabindex="0" data-value="Autre">Autre (spécifier dans les détails)</div>
            </div>
            <div class="suiv_prec">
                ${suivant}
            </div>
        `
    }


    container.appendChild(formulaire1); //ajouter l'élement à la section formulaire
    gerer_click_form1(); //actionner les click necessaire (boutton suivant, précédent...)
}

//Deuxieme page du formulaire
function afficher2(){
    pour_tous_page_config();
    if (islogin=='True' || isloginagence=='True'){
        animation_progress_bar(100);
    }
    else {
        animation_progress_bar(65);
    }
    repassage = true;
    container.querySelector("#form1").style.display = "none";
    formulaire2 = document.createElement('form'); //creer l'element form
    formulaire2.setAttribute('id', 'form2'); //verifier s'il on en a besoin
    formulaire2.innerHTML = `
            <div class="bloc_form">
            <h4>Quel est votre budget ?</h4>
                <div id="prixactu">
                    <label for="prix" id="prix_actu_min" style="justify-content: right; align-items: end; text-align: right">0 €</label>
                    <input type="range" name="prix_min" min="0" max="5000000" step="10000" value="5000000">
                    <input type="range" name="prix_max" min="0" max="5000000" step="10000" value="5000000">
                    <label for="prix" id="prix_actu_max">5 000 000 €</label>
                </div>
            </div>
            <div id="nombrechambre" class="bloc_form" style=" display:flex; justify-content: center; align-items: center; flex-direction: row; padding: 15px 0">
                <label for="nombrechambre">Nombre de pièce : </label>
                <div class="nc">
                    <div><input type="checkbox" checked><label>1</label></div>
                    <div><input type="checkbox"><label>2</label></div>
                    <div><input type="checkbox"><label>3</label></div>
                    <div><input type="checkbox"><label>4</label></div>
                    <div><input type="checkbox"><label>5</label></div>
                    <div><input type="checkbox"><label>6</label></div>
                    <div><input type="checkbox"><label>7</label></div>
                    <div><input type="checkbox"><label>8</label></div>
                    <div><input type="checkbox"><label>9</label></div>
                    <div><input type="checkbox"><label>10</label></div>
                </div>
            </div>
            <div class="bloc_form" style="display: flex; justify-content: center; flex-direction: column; align-items: center; padding: 15px 0">
            <label for="detailbien">Dites nous en plus sur ce que vous cherchez (facultatif)</label>
            <textarea id="detailbien" autocapitalize="sentences" autocomplete="off" cols="88" form="form2" maxlength="5000" placeholder="Détail sur le bien que vous cherchez" rows="6" style="width: 94%;"></textarea>
            </div>
            <div id="adresse">
                <div id="pays">
                    <label class="pays">Pays : </label>
                    <input name="pays" class="pays" type="text" required>
                    <button type="button" onclick="paysapi()" id="but1">Valider le pays</button>
                </div>
                <div id="ville">
                    <label class="ville">Ville : </label>
                    <input name="ville" class="ville" type="text" required>
                    <button type="button" onclick="villeapi()" id="but2" disabled>Valider la ville</button>
                </div>
                <div id="arrondissement">
                    <label class="arrondissement">Arrondissement : </label>
                    <input name="arrondissement" class="arrondissement" type="number" min="0" minlength="5" maxlength="6" value="00000" required>
                    <button type="button" id="but3" disabled>Valider</button>
                </div>
            </div>
            
            
            `
        if (islogin=="True"){
            console.log(islogin);
            formulaire2.innerHTML +=`
            <div class="suiv_prec" style="margin-top: 10px">
                ${precedent}
                ${valide}
        </div>`;
        }
        else if (isloginagence=="True"){
            formulaire2.innerHTML +=`
            <div class="suiv_prec" style="margin-top: 10px">
                ${precedent}
                <button style="cursor: not-allowed; padding: 10px 50px 10px" disabled>un agent ne peut pas soumettre de formulaire</button>
        </div>`;

        }
        else {
        formulaire2.innerHTML +=`
            <div class="suiv_prec" style="margin-top: 10px">
                ${precedent}
                ${suivant}
        </div>`;
        }


    container.appendChild(formulaire2); //ajouter l'élement à la section formulaire
    document.querySelector("#prixactu").addEventListener('input', event =>{ //gérer les labels pour choisir
        let min = Math.abs(document.querySelector("input[name='prix_min']").value-document.querySelector("input[name='prix_min']").getAttribute("max"))
        document.querySelector("#prix_actu_min").innerText = min.toLocaleString('fr-FR') + " €";
        //document.querySelector("input[name='prix_max']").setAttribute("min", ee)
        let max = parseInt(document.querySelector("input[name='prix_max']").value)
        document.querySelector("#prix_actu_max").innerText = max.toLocaleString('fr-FR') + " €";
    })

    gerer_click_form2();

}

function afficher_login(){
    pour_tous_page_config();
    animation_progress_bar(100);
    repassage2 = true; //vrai si on a executer cette fonction une fois
    container.querySelector("#form2").style.display = "none";
    formulaire3 = document.createElement('form'); //creer l'element form
    formulaire3.setAttribute('id', 'login'); //verifier s'il on en a besoin
    formulaire3.innerHTML = `
    <iframe src="/login=iframe" style="width: 100%;height: 400px; border: transparent"></iframe>
    <div class="suiv_prec">
        ${precedent}
        ${valide}
    </div>
    `;

    container.appendChild(formulaire3);
    document.querySelector("#valider").disabled = true;
    document.querySelector("#valider").style.cursor = "not-allowed";
    gerer_click_form3();
}