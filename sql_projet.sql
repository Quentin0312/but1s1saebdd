# Règles de nommage
# https://sql.sh/1396-nom-table-colonne
# TODO : Les appliquer (Dans loopping puis copier coller !)!

DROP TABLE IF EXISTS Concerne;
DROP TABLE IF EXISTS Tri;
DROP TABLE IF EXISTS Recolte;
DROP TABLE IF EXISTS Distance_entre_benne;
DROP TABLE IF EXISTS Achat;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Ramassage;
DROP TABLE IF EXISTS Reduction;
DROP TABLE IF EXISTS Categorie_client;
DROP TABLE IF EXISTS Type_vetement;
DROP TABLE IF EXISTS Benne_collecte;

CREATE TABLE Benne_collecte
(
    id_benne          INT NOT NULL AUTO_INCREMENT,
    emplacement_benne VARCHAR(50),
    distance_magasin  INT,
    PRIMARY KEY (id_benne)
);

CREATE TABLE Type_vetement
(
    id_type      INT NOT NULL AUTO_INCREMENT,
    libelle_type VARCHAR(50),
#     Range valeurs possibles pour les prix ?
#     À appliquer partout ailleurs
    prix_kg_type DECIMAL(15, 2),
    PRIMARY KEY (id_type)
);

CREATE TABLE Categorie_client
(
    id_categorie      INT NOT NULL AUTO_INCREMENT,
    libelle_categorie VARCHAR(50),
    PRIMARY KEY (id_categorie)
);

CREATE TABLE Reduction
(
    id_reduction     INT NOT NULL AUTO_INCREMENT,
#     Correspond à un pourcentage ? Renommer pourcentage_reduction et appliquer les modifs (dans les inserts !?)
    valeur_reduction INT,
    id_type          INT NOT NULL,
    id_categorie     INT NOT NULL,
    PRIMARY KEY (id_reduction),
    FOREIGN KEY (id_type) REFERENCES Type_vetement (id_type),
    FOREIGN KEY (id_categorie) REFERENCES Categorie_client (id_categorie)
);

CREATE TABLE Ramassage
(
    id_ramassage   INT NOT NULL AUTO_INCREMENT,
    date_ramassage DATE,
    PRIMARY KEY (id_ramassage)
);

CREATE TABLE Client
(
    id_client            INT NOT NULL AUTO_INCREMENT,
    nom_client           VARCHAR(50),
#     Taille max numéro de tél ?
    tel_client           VARCHAR(50),
    adresse_client       VARCHAR(50),
    email_client         VARCHAR(50),
    date_naissace_client DATE,
    id_categorie         INT NOT NULL,
    PRIMARY KEY (id_client),
    FOREIGN KEY (id_categorie) REFERENCES Categorie_client (id_categorie)
);

CREATE TABLE Achat
(
    id_achat   INT NOT NULL AUTO_INCREMENT,
    date_achat DATE,
    prix_total DECIMAL(15, 2),
    id_client  INT NOT NULL,
    PRIMARY KEY (id_achat),
    FOREIGN KEY (id_client) REFERENCES Client (id_client)
);

CREATE TABLE Distance_entre_benne
(
    id_benne_1     INT NOT NULL,
    id_benne_2     INT NOT NULL,
    distance_benne INT,
    PRIMARY KEY (id_benne_1, id_benne_2),
    FOREIGN KEY (id_benne_1) REFERENCES Benne_collecte (id_benne),
    FOREIGN KEY (id_benne_2) REFERENCES Benne_collecte (id_benne)
);

CREATE TABLE Recolte
(
    id_benne     INT,
    id_ramassage INT,
    PRIMARY KEY (id_benne, id_ramassage),
    FOREIGN KEY (id_benne) REFERENCES Benne_collecte (id_benne),
    FOREIGN KEY (id_ramassage) REFERENCES Ramassage (id_ramassage)
);

CREATE TABLE Tri
(
    id_type         INT,
    id_ramassage    INT,
#     Range de valeurs pour le poids ?
#     À appliquer partout
    poids_type_trie DECIMAL(15, 2),
    PRIMARY KEY (id_type, id_ramassage),
    FOREIGN KEY (id_type) REFERENCES Type_vetement (id_type),
    FOREIGN KEY (id_ramassage) REFERENCES Ramassage (id_ramassage)
);

CREATE TABLE Concerne
(
    id_achat           INT,
    id_reduction       INT,
    poid_type_vetement DECIMAL(15, 2),
    PRIMARY KEY (id_achat, id_reduction),
    FOREIGN KEY (id_achat) REFERENCES Achat (id_achat),
    FOREIGN KEY (id_reduction) REFERENCES Reduction (id_reduction)
);

INSERT INTO Benne_collecte (id_benne, emplacement_benne, distance_magasin)
VALUES (1, '1 rue gaston defferre', 2000),
       (2, '2 rue ernest duvillard', 500),
       (3, '3 rue marcel paul', 2100);

INSERT INTO Type_vetement (id_type, libelle_type, prix_kg_type)
VALUES (1, 't-shirt', 20),
       (2, 'pantalon', 25),
       (3, 'robe', 40);

INSERT INTO Categorie_client (id_categorie, libelle_categorie)
VALUES (1, 'poids plume'),
       (2, 'léger'),
       (3, 'lourd'),
       (4, 'méga lourd');

INSERT INTO Reduction (id_reduction, valeur_reduction, id_type, id_categorie)
VALUES (NULL, 0, 1, 1),(NULL, 0, 2, 1),(NULL, 0, 3, 1),
       (NULL, 2, 1, 2),(NULL, 4, 2, 2),(NULL, 5, 3, 2),
       (NULL, 5, 1, 3),(NULL, 7, 2, 3),(NULL, 10, 3, 3),
       (NULL, 10, 1, 4),(NULL, 14, 2, 4),(NULL, 20, 3, 4);

SELECT * FROM Benne_collecte;
SELECT * FROM Type_vetement;
SELECT * FROM Categorie_client;
SELECT * FROM Reduction;

SHOW TABLES;

