from flask import *
from functools import wraps
import sqlite3
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets


#configuration mail
message = MIMEMultipart()
message["Subject"] = "Un agent Immobilier voudrais vous contacter"
message["From"] = "the.yomans.club@gmail.com"
smtp_address = 'smtp.gmail.com'
smtp_port = 465


app = Flask(__name__)
app.secret_key = os.urandom(24)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if islogin("client") or islogin("agence"):
            return f(*args, **kwargs)
        else:
            return Response("Accès non autorisé", status=401)
    return wrap

def login_required_for_client(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if islogin("client") :
            return f(*args, **kwargs)
        elif islogin("agence"):
            return Response("Accès réservé au client seulement", status=401)
        else:
            return Response("Accès non autorisé pour les personnes non connecté", status=401)
    return wrap

def login_required_for_agence(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if islogin("agence") :
            return f(*args, **kwargs)
        elif islogin("client"):
            return Response("Accès refusé : réservé aux agences uniquement", status=401)
        else:
            return Response("Accès non autorisé pour les personnes non connecté", status=401)
    return wrap


def islogin(cl_ou_ag):
    if 'user_data' in session:
        prenom = session['user_data']['prenom']
        nom = session['user_data']['nom']
        connection = sqlite3.connect("base_de_donnee.sqlite")
        cursor = connection.cursor()
        verif_client = cursor.execute('SELECT key_user FROM user WHERE prenom=? and nom=?', (prenom, nom,)).fetchall()
        for ligne in verif_client :
            if session['user_data']['key']==ligne[0]:
                if (cl_ou_ag=="client"):
                    connection.close()
                    return True
                else:
                    connection.close()
                    return False
        verif_agence = cursor.execute('SELECT key_user FROM agence WHERE prenom=? and nom=?', (prenom, nom,)).fetchall()
        for ligne in verif_agence:
            if session['user_data']['key']==ligne[0]:
                if (cl_ou_ag=="agence"):
                    connection.close()
                    return True
                else:
                    connection.close()
                    return False
        connection.close()
    session.clear()
    return False


@app.route("/")
def hello_world():
    accueil_test = True
    is_login = str(islogin("client"))
    is_login_agence = str(islogin("agence"))
    return render_template("index.html", accueil_test=accueil_test, is_login=is_login, is_login_agence=is_login_agence)

@app.route("/form")
def formulaire():
    return redirect("/", code=400)

@app.route("/form/<id>", methods=["GET"])
def formulaireee(id):
    is_login = str(islogin("client"))
    is_login_agence = str(islogin("agence"))
    accueil_test = False
    return render_template("rechercheimmo.html", id=id, accueil_test=accueil_test, is_login=is_login, is_login_agence=is_login_agence)

@app.route("/form/<id>", methods=["POST"])
@login_required_for_client
def eregistrement_des_donnes(id):
    formdata = request.get_json() #recuperer le fichier json
    data = formdata['donnee']
    if 'key' not in session['user_data']:
        return Response("Utilisateur non authentifié", 403)

    try:
        connection = sqlite3.connect("base_de_donnee.sqlite")
        cursor = connection.cursor()
        print(session['user_data']['key'])
        cursor.execute("INSERT INTO recherchebien (type_de_bien, soustype_de_bien, prix_minimum, prix_maximum, nombre_chambre, détail_en_plus, ville, pays, numero_arrondissement, id_user) VALUES (?,?,?,?,?,?,?,?,?,?)", (data['type_de_bien']['0'], data['type_de_bien']['1'], data['prix']['minimum'], data['prix']['maximum'], ','.join(data['nombre_piece']), data['detail'], data['ville'], data['pays'], data['arrondissement'], session['user_data']['key']))
        connection.commit()
        connection.close()
        return Response("Validé", 200)
    except:
        return Response("erreur de l'envoie de la requête", 500)


@app.route("/login=<type>", methods=["GET"])
def login(type):
    if islogin("client") or islogin("agence"):
        return Response("<h3>Vous êtes déjà connecté à un compte</h3><a href='/logout'>Se déconnecter</a>", 409, mimetype='text/html')

    return render_template("login.html", type=type)


@app.route("/login=<type>", methods=["POST"])
def login_post(type):
    mail = request.form["mail"]
    password = request.form["password"]
    if not os.path.exists("base_de_donnee.sqlite"):
        return "<script>window.alert('base de donnée introuvable')</script>"

    try :
        connection = sqlite3.connect("base_de_donnee.sqlite")
        cursor = connection.cursor()
        verif_client = cursor.execute("SELECT * FROM user WHERE mail=?", (mail,)).fetchone()
        verif_agence = cursor.execute("SELECT * FROM agence WHERE mail=?", (mail,)).fetchone()
        if verif_client is not None:
            if check_password_hash(verif_client[2], password):
                print("connexion pour le login etabli")
                session['user_data'] = {
                    'mail':mail,
                    'nom':verif_client[3],
                    'prenom':verif_client[4],
                    'key':verif_client[6],
                    'is_agence':'False'
                }
                connection.close()
                if (type=='iframe'):
                    return "<center><h1 style='color:white;'>Connecté</h1></center>"
                else:
                    return redirect("/", code=301)  # Redirige vers une autre page si les identifiants sont valides

            else:
                connection.close()
                return render_template("erreurdanslecompte.html", type=type), 403

        elif verif_agence is not None:
            if check_password_hash(verif_agence[2], password):
                print("connexion pour le login agence etabli")
                session['user_data'] = {
                    'mail':mail,
                    'nom':verif_agence[5],
                    'prenom':verif_agence[6],
                    'nom_agence':verif_agence[3],
                    'key':verif_agence[9],
                    'is_agence':'True'
                }
                connection.close()
                if (type=='iframe'):
                    return "<center><h1 style='color:white;'>Un agent ne peut que lire le formulaire </h1></center>"
                else:
                    return redirect("/", code=301)  # Redirige vers une autre page si les identifiants sont valides
            else :
                connection.close()
                return render_template("erreurdanslecompte.html", type=type), 403
        else:
            connection.close()
            return render_template("erreurdanslecompte.html", type=type), 403

    except sqlite3.Error:
            return "<script>window.alert('erreur lier à la base de donnée')</script>"

    except :
        return "<script>window.alert('erreur inconnu')</script>"


@app.route("/new_user=<key>", methods=["POST"]) #nouvelle utilisateur (key pour identifier si c est un agent ou pas qui créer un compte)
def new_user(key):
    if not (key == "client" or key == "agence"):
        return redirect("/new_user=client", code=307)
    if request.form['password'] != request.form['confirm-password']:
        return "<script>window.alert('les mots de passe ne sont pas identique')</script>"
    new_mail=request.form['mail']
    new_password=generate_password_hash(request.form['password'])
    new_telephone=int(request.form['telephone'])
    new_nom=request.form['nom']
    new_prenom=request.form['prenom']
    key_user=os.urandom(10)
    if (sqlite3.connect("base_de_donnee.sqlite").cursor().execute("SELECT mail FROM agence WHERE mail=?", (new_mail,)).fetchone() != None) or (sqlite3.connect("base_de_donnee.sqlite").cursor().execute("SELECT mail FROM user WHERE mail=?", (new_mail,)).fetchone() != None):
        sqlite3.connect("base_de_donnee.sqlite").close()
        return "<script>window.alert('un compte est déjà créer avec ce mail')</script>"

    if (key=="agence"):
        new_nom_agence = request.form['nom_agence']
        new_CPI = int(request.form['CPI'])
        new_adresse_agence = request.form['adresse_agence']
        try:
            connection = sqlite3.connect("base_de_donnee.sqlite")
            cursor = connection.cursor()
            if all([new_mail, new_password, request.form['password'], request.form['confirm-password'], new_telephone, new_nom, new_prenom,new_nom_agence,new_CPI,new_adresse_agence]) and isinstance(new_telephone, int) and isinstance(new_CPI, int) and '@' in new_mail and cursor.execute("SELECT COUNT(nom_agence) FROM agence where nom_agence=?", (new_nom_agence,)).fetchone()[0]==0: #toute verification necessaire
                cursor.execute("INSERT INTO agence (mail, mdp, nom_agence, adresse_agence, nom, prenom, telephone, numero_cpi, key_user) VALUES (?, ?, ?, ?, ?, ?,?,?,?)", (new_mail, new_password, new_nom_agence, new_adresse_agence, new_nom, new_prenom, new_telephone, new_CPI, key_user))
                connection.commit()
                connection.close()
                return redirect("/login=ok", code=303)
            else:
                return "<script>window.alert('erreur côté client')</script>"

        except sqlite3.Error:
            return "<script>window.alert('erreur lier à la base de donnée')</script>"

        except :
            return "<script>window.alert('erreur inconnu')</script>"




    else:
        try :
            if all([new_mail, new_password, request.form['password'], request.form['confirm-password'], new_telephone, new_nom, new_prenom]) and isinstance(new_telephone, int) and '@' in new_mail: #toute verification necessaire
                connection = sqlite3.connect("base_de_donnee.sqlite")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO user (mail, mdp, nom, prenom, telephone, key_user) VALUES (?, ?, ?, ?, ?, ?)", (new_mail, new_password, new_nom, new_prenom, new_telephone, key_user))
                connection.commit()
                connection.close()
                return redirect("/login=ok", code=303)
            else:
                return "<script>window.alert('erreur côté client')</script>"
        except sqlite3.Error:
            return "<script>window.alert('erreur lier à la base de donnée')</script>"

        except :
            return "<script>window.alert('erreur inconnu')</script>"



@app.route("/new_user=client", methods=["GET"])
def new_client():
    return render_template("new_user_client.html")



@app.route("/new_user=agence", methods=["GET"])
def new_agence():
    return render_template("new_user_agence.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect("/login=ok", code=307)

@app.route('/get_islogin', methods=['GET']) #recuperer juste le login pour verif
def get_islogin():
    is_login = islogin("client")  # Fonction qui vérifie l'état de connexion
    return jsonify({'is_login': str(is_login)})  # Renvoie la valeur de is_login en JSON

@app.route('/historique')
@login_required_for_client
def historique_du_client():
    client = session['user_data']['key']
    connection = sqlite3.connect('base_de_donnee.sqlite')
    cursor = connection.cursor()
    historique = cursor.execute("SELECT * FROM recherchebien where id_user=?", (client,)).fetchall()
    return render_template("historique_du_client.html", historique=historique, is_login="True")

@app.route('/historique/<id>')
@login_required
def historique_detail(id):
    connexion = sqlite3.connect('base_de_donnee.sqlite')
    cursor = connexion.cursor()
    client = cursor.execute("SELECT * FROM recherchebien WHERE id=?", (id,)).fetchone()
    if client==None:
        return Response("Introuvable", 404)

    elif islogin("client"):
        if (client[10]==session['user_data']['key']): #verifie si c'est la même clé
            return render_template("detail_bien.html", is_login="True", bien=client)
        else:
            return Response("Vous n'êtes pas autorisez à consulter ce fichier", 403)

    elif islogin("agence"):
        cle_autorisation_agence = cursor.execute("SELECT cle_d_aurisation FROM autorisation WHERE id_user=? and id_bien=?",(session['user_data']['key'],id)).fetchone()
        info = False
        info_client = None
        if not cle_autorisation_agence==None:
            cle_autorisation_agence = cle_autorisation_agence[0]
            info = True
            info_client = cursor.execute("SELECT nom, prenom, telephone FROM user AS u INNER JOIN autorisation AS a ON u.key_user=a.id_user where a.id_bien=? and a.cle_d_aurisation=?", (id,cle_autorisation_agence)).fetchone()
        #info_client = sqlite3.connect('base_de_donnee.sqlite').cursor().execute("SELECT nom, prenom, telephone FROM user WHERE cle_autaurisation = (select cle_autaurisation from agence where key_user=?)", (session['user_data']['key'],)).fetchone()
        #if not info_client == None:
        #    info = True
        return render_template("detail_bien.html", is_login_agence="True", bien=client, info=info, info_client=info_client)

    else:
        login_required()


@app.route('/mon_profil', methods=['GET'])
@login_required
def profil():
    key = session['user_data']['key']
    connexion = sqlite3.connect('base_de_donnee.sqlite')
    if (islogin("client")):
        info = connexion.cursor().execute("SELECT * FROM user where key_user=?", (key,)).fetchone()
        return render_template("profil.html", info=info, is_login="True", is_login_agence="False")
    elif(islogin("agence")):
        info = connexion.cursor().execute("SELECT * FROM agence where key_user=?", (key,)).fetchone()
        return render_template("profil.html", info=info, is_login="False", is_login_agence="True")
    else:
        return Response("Une erreur s'est produite", 403)

@app.route('/mon_profil', methods=['POST'])
@login_required
def modifierlogin():
    mod_mail = request.form['mail']
    mod_telephone =int(request.form['telephone'])
    mod_nom =request.form['nom']
    mod_prenom =request.form['prenom']
    if all([mod_mail, mod_telephone, mod_nom, mod_prenom]) and '@' in mod_mail and isinstance(mod_telephone, int):
        if (islogin("client")):
            connexion = sqlite3.connect('base_de_donnee.sqlite')
            cursor = connexion.cursor()
            cursor.execute("UPDATE user SET mail=?, telephone=?, nom=?, prenom=? WHERE key_user=?", (mod_mail, mod_telephone, mod_nom, mod_prenom, session['user_data']['key']))
            connexion.commit()
            "<script>window.alert('Donnée modifier !')</script>"
            verif_client = cursor.execute("SELECT * FROM user WHERE key_user=?", (session['user_data']['key'],)).fetchone()
            session.clear()
            session['user_data'] = {
                    'mail':verif_client[1],
                    'nom':verif_client[3],
                    'prenom':verif_client[4],
                    'key':verif_client[6],
                    'is_agence':'False'
                }
            connexion.close()
            return redirect("/mon_profil", code=303)
        else:
            return "<script>window.alert('pas encore codé pour les agences')</script>"
    else:
        return "<script>window.alert('erreur côté client')</script>"

@app.route('/search', methods=['GET'])
@login_required_for_agence
def search():
    return render_template("recherche_pour_lagence.html", is_login_agence="True")

@app.route('/search', methods=['POST'])
@login_required_for_agence
def resultat_recherche():
    cursor = sqlite3.connect('base_de_donnee.sqlite').cursor()
    adresse = str(request.form['adresse']).replace(" ", "").split(',')
    nombre_chambre = str(request.form.get('nombrechambre'))
    detail = str(request.form['detail'])
    mot_detail = detail.split(" ") #tranforme le detail en liste de mot
    if not request.form.get('prix')=="":
        prix_bien = int(request.form.get('prix'))
    else:
        prix_bien = None
    type_bien = request.form.get('type_bien') #on utilise get car s'il input vide, alors erreur
    parametre = [] #sera la liste des paramètres qu'on aura besoin
    condition = [] #sera la liste des conditions

    #filtre de l'adresse
    if len(adresse)==3:
        parametre.append(('%' + adresse[0] + '%'))
        parametre.append(('%' + adresse[1] + '%'))
        parametre.append(('%' + adresse[2] + '%'))
        condition.append("ville LIKE ?")
        condition.append("pays LIKE ?")
        condition.append("numero_arrondissement LIKE ?")

    elif len(adresse)==2:
        parametre.append(('%' + adresse[0] + '%'))
        parametre.append(('%' + adresse[1] + '%'))
        condition.append("ville LIKE ?")
        condition.append("pays LIKE ?")

    elif len(adresse)==1:
        parametre.append(('%' + adresse[0] + '%'))
        condition.append("ville LIKE ?")

    else:
        ne_rien_faire = 1

    #filtrer le nombre de chambre
    if not nombre_chambre=="None":
        parametre.append('%' +nombre_chambre + '%')
        condition.append("nombre_chambre LIKE ?")

    #filtrer le budget
    order_by = []
    parametre_order = []
    order_byy = ""
    if not prix_bien is None:
        parametre.append(prix_bien)
        parametre.append(prix_bien)
        parametre_order.append(prix_bien)
        condition.append("(prix_minimum-10000)<=? AND (prix_maximum+10000)>=?")
        order_byy = " ORDER BY "
        order_by.append("(((prix_minimum+prix_maximum)/2)-?) ASC")

    #filtrer type bien
    if not type_bien =="":
        parametre.append(str(type_bien))
        condition.append("soustype_de_bien = ?")

    #filtrer detail
    condition_or = []
    if not detail =="":
        for a in mot_detail:
            parametre.append('%' + a + '%') #est ajouté au parametre à la suite (car on est toujour dans le where)
            condition_or.append("détail_en_plus LIKE ?")
        condition.append(" OR ".join(condition_or)) #ajoute à la liste des conditions where

    parametre.extend(parametre_order) #ajouter les parametre_order à la fin (car order by se situe après where)
    resultat = cursor.execute("SELECT * FROM recherchebien where " + " AND ".join(condition) + order_byy + ", ".join(order_by), (parametre)) #"s".join(list) transforme list en string avec s entre les valeurs
    resultat_recherche = resultat.fetchall()
    cursor.close()
    return render_template("recherche_pour_lagence.html", result=resultat_recherche, is_login_agence="True")

@app.route("/contacter/<id>", methods=['POST'])
@login_required_for_agence
def contacter_client(id):
    key = session['user_data']['key']
    nom_agence = session['user_data']['nom_agence']
    connexion = sqlite3.connect('base_de_donnee.sqlite')
    cursor = connexion.cursor()
    result = cursor.execute("SELECT mail, telephone FROM user AS u JOIN recherchebien AS r ON r.id_user = u.key_user WHERE r.id = ?", (id,)).fetchone()
    mail_du_client = result[0]
    message['To'] = mail_du_client #destinataire pour envoyer un mail
    cle_personne = ""
    for i in range(20):
        cle_personne+= str(secrets.SystemRandom().randint(0,10))

    cursor.execute("INSERT INTO autorisation (cle_d_aurisation, id_user,id_bien) VALUES (?,?,?)", (cle_personne,key, id))
    #cursor.execute("UPDATE agence SET cle_autaurisation=? where key_user=?", (cle_personne,key))
    connexion.commit()
    #contenu du message
    text_html_message = """
    <html> 
    <head></head>
    <body> 
    <form action='http://127.0.0.1:5000/contacter/""" + id +"""/"""+cle_personne+"""' method="post">
    <p>Bonjour,<br> l'agent immobilier """+ nom_agence +""" aimerais vous contacter à propos de la recherche que vous avez effectuer suivante.<br>
    Pour lui transmettre vos coordonnées (téléphone, nom et prénom) via le site, <input type="submit" value="cliquez ici">. 
    </p>
    <p>
    vous pouvez également l'appeler au """+ str(result[1]) +"""
        </p>
      <p>
    nom de l'agence: """ + nom_agence
    """nom : """ + session['user_data']['nom']
    """prenom : """ + session['user_data']['prenom']
    """<p>
    </form>
    </body> 
    </html> 
    """
    part2  =  MIMEText ( text_html_message ,  'html' )
    message.attach(part2)

    context = ssl.create_default_context()
    connexion.close()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        server.login(message["From"], "adyc lwke yogb dqge")
        server.sendmail(message["From"], message["To"], message.as_string())
    return Response("<h2>Demande envoyé au client</h2>", 200)

@app.route("/contacter/<id>/<key>", methods=['POST'])
def autorisation(id, key):
    #try:
    key = str(key)
    connexion = sqlite3.connect('base_de_donnee.sqlite')
    cursor = connexion.cursor()
    if cursor.execute("SELECT cle_d_aurisation from autorisation where cle_d_aurisation=? and id_bien=?", (key, id)).fetchone()[0]!=key:
        return Response("clé invalide", 403)
    """
    if cursor.execute("SELECT cle_autaurisation from agence where cle_autaurisation=?", (key,)).fetchone()[0]!=key:
        return Response("clé invalide", 403)
        """
    id_client = cursor.execute("SELECT r.id_user from recherchebien AS r INNER JOIN autorisation AS a ON r.id=a.id_bien where a.id_bien=?", (id,)).fetchone()[0]
    cursor.execute("INSERT INTO autorisation (cle_d_aurisation,  id_user, id_bien) VALUES (?,?,?)", (key,id_client,id))

    #cursor.execute("UPDATE user SET cle_autaurisation = ? where key_user = (SELECT id_user FROM recherchebien WHERE id = ?)", (key,id))
    connexion.commit()
    connexion.close()
    return Response("<h2>L'agence a désormé accès à vos coordonnées qui sera : numéro de téléphone, nom, prenom</h2>",200)

    """ except sqlite3.Error:
        return Response("erreur, le serveur n'a pas pu valider la requête", 444)
        except:
        return Response("erreur inconnu", 500)"""


@app.route('/modif_mdp', methods=['GET'])
@login_required
def modification_motdepassee():
    return render_template("modification_du_motdepasse.html")


@app.route('/modif_mdp', methods=['POST'])
@login_required
def modification_motdepasse():
    key = session['user_data']['key']
    ancien_mdp = request.form['ancien_mdp']
    new_mdp = request.form['new_mdp']
    verif_mdp = request.form['verif_mdp']
    print(ancien_mdp)
    try:
        connection = sqlite3.connect('base_de_donnee.sqlite')
        cursor = connection.cursor()
        if islogin("client"):
            ancien = cursor.execute("SELECT mdp FROM user where key_user=?", (key,)).fetchone()[0] #recupere ancien mot de passe
            if check_password_hash(ancien, ancien_mdp):
                if new_mdp==verif_mdp:
                    cursor.execute("UPDATE user SET mdp=? where key_user=?", (generate_password_hash(new_mdp),key))
                    session['user_data']['key'] = ancien
                    connection.commit()
                    connection.close()
                    return Response("<h1>Nouveau mot de passe enregistré, vous pouvez fermer cette page</h1>",200)
                else:
                    return Response("<script>window.alert ('Les mots de passe saisis ne correspondent pas, ou le nouveau mot de passe est identique à l ancien')</script>", content_type='text/html')

        else:
            ancien = cursor.execute("SELECT mdp FROM agence where key_user=?", (key,)).fetchone()[0] #recupere ancien mot de passe
            if check_password_hash(ancien, ancien_mdp):
                if new_mdp==verif_mdp:
                    cursor.execute("UPDATE agence SET mdp=? where key_user=?", (generate_password_hash(new_mdp),key))
                    connection.commit()
                    session['user_data']['key'] = ancien
                    connection.close()
                    return Response("<h1>Nouveau mot de passe enregistré, vous pouvez fermer cette page</h1>",200)
                else:
                    connection.close()
                    return "<script>window.alert ('Les mots de passe saisis ne correspondent pas ou le nouveau mot de passe est identique à l ancien') </script>"
        connection.close()
        return "<script>window.alert('mot de passe incorrect')</script>"


    except sqlite3.Error:
        return "<script>window.alert('erreur lier à la base de donnée')</script>"

    except :
        return "<script>window.alert('erreur inconnu')</script>"


@app.route('/delete', methods=['POST'])
@login_required
def suppression_compte():
    key = session['user_data']['key']
    connexion = sqlite3.connect('base_de_donnee.sqlite')
    cursor = connexion.cursor()
    cle_autorisation = cursor.execute("SELECT DISTINCT cle_d_aurisation FROM autorisation WHERE id_user=?", (key,)).fetchall()
    if cle_autorisation!=None:
        for cle in cle_autorisation:
            cursor.execute("DELETE FROM autorisation where cle_d_aurisation=?", (cle[0],))
    if (islogin("client")):
        cursor.execute("DELETE FROM user where key_user=?", (key,))
        cursor.execute("DELETE FROM recherchebien where id_user=?", (key,))

    elif (islogin("agence")):
        cursor.execute("DELETE FROM agence where key_user=?", (key,))
    else:
        return Response("Une erreur s'est prduite", status=500)
    connexion.commit()
    session.clear()
    connexion.close()
    return Response("<h2>Votre compte a été supprimé</h2><script>setTimeout(function() {window.location.replace = '/';}, 2000);</script>", status=200)



if  __name__ == "__main__" :
    app.run(debug=True)