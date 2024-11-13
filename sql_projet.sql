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
#     nom complet et non com et prenom ?
    nom_client           VARCHAR(50),
#     Taille max numéro de tél ?
    tel_client           VARCHAR(50),
#     Ajouter code postal dans les adresse ? et aussi bennes !!
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
VALUES (1, 0, 1, 1),
       (2, 0, 2, 1),
       (3, 0, 3, 1),
       (4, 2, 1, 2),
       (5, 4, 2, 2),
       (6, 5, 3, 2),
       (7, 5, 1, 3),
       (8, 7, 2, 3),
       (9, 10, 3, 3),
       (10, 10, 1, 4),
       (11, 14, 2, 4),
       (12, 20, 3, 4);

INSERT INTO Ramassage (id_ramassage, date_ramassage)
VALUES (1, '2024-11-04'),
       (2, '2024-10-28');

INSERT INTO Client (id_client, nom_client, tel_client, adresse_client, email_client, date_naissace_client, id_categorie)
VALUES (1, 'DOE Jane', '0693333401', '31 chemin des chevaliers', 'janedoe@outlook.com', '2001-01-01', 1),
       (2, 'DUPOND Nicolas', '0692028077', '1 boulevard richelieu', 'dupondnicolas@gmail.com', '1997-05-15', 2);


INSERT INTO Achat (id_achat, date_achat, prix_total, id_client)
VALUES (1, '2024-10-28', 15.5, 2),
       (2, '2024-11-04', 25, 1);

INSERT INTO Distance_entre_benne (id_benne_1, id_benne_2, distance_benne)
VALUES (1, 2, 2100),
       (1, 3, 1050),
       (2, 3, 3000);

INSERT INTO Recolte (id_benne, id_ramassage)
VALUES (1, 1),
       (2, 1),
       (3, 2);

INSERT INTO Tri (id_type, id_ramassage, poids_type_trie)
VALUES (1, 1, 50),
       (2, 1, 74),
       (3, 2, 34);

INSERT INTO Concerne (id_achat, id_reduction, poid_type_vetement)
VALUES (1, 4, 0.97),
       (2, 2, 2);

SELECT *
FROM Benne_collecte;
SELECT *
FROM Type_vetement;
SELECT *
FROM Categorie_client;
SELECT *
FROM Reduction;
SELECT *
FROM Ramassage;
SELECT *
FROM Client;
SELECT *
FROM Achat;
SELECT *
FROM Distance_entre_benne;
SELECT *
FROM Recolte;
SELECT *
FROM Tri;
SELECT *
FROM Concerne;
SHOW TABLES;

