import sqlite3
import os

if not os.path.exists("base_de_donnee.sqlite"):
    conn = sqlite3.connect("base_de_donnee.sqlite")
    cursor = conn.cursor()
    cursor.executescript("""
CREATE TABLE "user" (
	"id"	INTEGER NOT NULL UNIQUE,
	"mail"	TEXT NOT NULL UNIQUE,
	"mdp"	TEXT NOT NULL,
	"nom"	TEXT NOT NULL,
	"prenom"	TEXT NOT NULL,
	"telephone"	INTEGER NOT NULL,
	"key_user"	BLOB NOT NULL UNIQUE,
	"cle_autaurisation" TEXT DEFAULT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "agence" (
	"id"	INTEGER NOT NULL UNIQUE,
	"mail"	TEXT NOT NULL UNIQUE,
	"mdp"	TEXT NOT NULL,
	"nom_agence" TEXT NOT NULL UNIQUE,
	"adresse_agence" TEXT NOT NULL,
	"nom"	TEXT NOT NULL,
	"prenom"	TEXT NOT NULL,
	"telephone"	INTEGER NOT NULL,
	"numero_cpi" INTEGER NOT NULL UNIQUE,
	"key_user"	BLOB NOT NULL UNIQUE,
	"cle_autaurisation" TEXT DEFAULT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);


CREATE TABLE "recherchebien" (
	"id"	INTEGER NOT NULL UNIQUE,
	"type_de_bien"	INTEGER NOT NULL,
	"soustype_de_bien"	TEXT NOT NULL,
	"prix_minimum"	INTEGER NOT NULL,
	"prix_maximum"	INTEGER NOT NULL,
	"nombre_chambre"	TEXT NOT NULL,
	"détail_en_plus"	TEXT,
	"ville"	TEXT NOT NULL,
	"pays"	TEXT NOT NULL,
	"numero_arrondissement"	INTEGER NOT NULL,
	"id_user" BLOB NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_user") REFERENCES user(key_user)
);

CREATE TABLE "autorisation" (
        "id" INTEGER NOT NULL UNIQUE,
	"cle_d_aurisation" TEXT NOT NULL,
	"id_user" BLOB NOT NULL,
	"id_bien" INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_bien") REFERENCES recherchebien(id)

);
""")
    conn.close()
    print("fichier db créé")

print("succès")
