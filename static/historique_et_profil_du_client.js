//lorsque le client clique sur l'historique, ça l envoie au détail de ce qu'il a écrit

document.addEventListener('DOMContentLoaded', () => {
    if ( !document.location.href.includes("historique/")){
        let div = document.querySelectorAll(".boite_historique");
        div.forEach( element =>
            element.addEventListener('click', event => {
                    let id = element.getAttribute('data-id');
                    window.location.replace(`/historique/${id}`);
                }
            )
        )
    }

if (document.location.href.includes("mon_profil")){
//pour valider la modification dans mon profil
document.querySelector(".grid > input[type='submit']").addEventListener('click', event=>{
    if (!window.confirm("Voulez vous continuer")){
        event.preventDefault();
        alert("Formulaire annulé !");
    }
})}

//modifier le mot de passe
    document.querySelector('#mdp_change').addEventListener('click', event =>{
        const w = 600;
        const h = 300;
        const left = (window.innerWidth - w) / 2;
        const top = (window.innerHeight - h) / 2;
        window.open("/modif_mdp", "_blank", `width=${w},height=${h},left=${left},top=${top}`);
    })

//suppression de compte
    document.querySelector('#suppression').addEventListener('click', event =>{
        if (!window.confirm("voulez vous vraiment supprimer votre compte ?")){
            event.preventDefault()
        }
    })
})


