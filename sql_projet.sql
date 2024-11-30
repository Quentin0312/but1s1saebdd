DROP TABLE IF EXISTS Concerne;
DROP TABLE IF EXISTS Tri;
DROP TABLE IF EXISTS Recolte;
DROP TABLE IF EXISTS Reduction;
DROP TABLE IF EXISTS Distance_entre_benne;
DROP TABLE IF EXISTS Achat;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Ramassage;
DROP TABLE IF EXISTS Categorie_client;
DROP TABLE IF EXISTS Type_vetement;
DROP TABLE IF EXISTS Benne_collecte;

CREATE TABLE Benne_collecte
(
    id_benne          INT NOT NULL AUTO_INCREMENT,
    emplacement_benne VARCHAR(100),
    distance_magasin  INT,
    PRIMARY KEY (id_benne)
);

CREATE TABLE Type_vetement
(
    id_type      INT NOT NULL AUTO_INCREMENT,
    libelle_type VARCHAR(50),
    prix_kg_type DECIMAL(6, 2),
    PRIMARY KEY (id_type)
);

CREATE TABLE Categorie_client
(
    id_categorie      INT NOT NULL AUTO_INCREMENT,
    libelle_categorie VARCHAR(50),
    PRIMARY KEY (id_categorie)
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
    prenom_client        VARCHAR(50),
    tel_client           VARCHAR(15),
    adresse_client       VARCHAR(100),
    email_client         VARCHAR(50),
    date_naissace_client DATE,
    id_categorie         INT NOT NULL,
    PRIMARY KEY (id_client),
    CONSTRAINT fk_client_categorieclient FOREIGN KEY (id_categorie) REFERENCES Categorie_client (id_categorie)
);

CREATE TABLE Achat
(
    id_achat   INT NOT NULL AUTO_INCREMENT,
    date_achat DATE,
    prix_total DECIMAL(6, 2),
    id_client  INT NOT NULL,
    PRIMARY KEY (id_achat),
    CONSTRAINT fk_achat_client FOREIGN KEY (id_client) REFERENCES Client (id_client)
);

CREATE TABLE Distance_entre_benne
(
    id_benne_1     INT NOT NULL,
    id_benne_2     INT NOT NULL,
    distance_benne INT,
    PRIMARY KEY (id_benne_1, id_benne_2),
    CONSTRAINT fk_distancebenne1_bennecollecte FOREIGN KEY (id_benne_1) REFERENCES Benne_collecte (id_benne),
    CONSTRAINT fk_distancebenne2_bennecollecte FOREIGN KEY (id_benne_2) REFERENCES Benne_collecte (id_benne)
);

CREATE TABLE Reduction
(
    id_reduction     INT NOT NULL AUTO_INCREMENT, # AJOUT
    id_type          INT,
    id_categorie     INT,
    valeur_reduction INT,
    PRIMARY KEY (id_reduction),
    CONSTRAINT fk_reduction_typevetement FOREIGN KEY (id_type) REFERENCES Type_vetement (id_type),
    CONSTRAINT fk_reduction_categorieclient FOREIGN KEY (id_categorie) REFERENCES Categorie_client (id_categorie),
    CONSTRAINT unique_ramassage UNIQUE (id_type, id_categorie)
);

CREATE TABLE Recolte
(
    id_benne     INT,
    id_ramassage INT,
    PRIMARY KEY (id_benne, id_ramassage),
    CONSTRAINT fk_recolte_bennecollecte FOREIGN KEY (id_benne) REFERENCES Benne_collecte (id_benne),
    CONSTRAINT fk_recolte_ramassage FOREIGN KEY (id_ramassage) REFERENCES Ramassage (id_ramassage)
);

CREATE TABLE Tri
(
    id_tri          INT NOT NULL AUTO_INCREMENT, #AJOUT
    id_type         INT,
    id_ramassage    INT,
    poids_type_trie DECIMAL(6, 2),
    PRIMARY KEY (id_tri),
    CONSTRAINT fk_tri_typevetement FOREIGN KEY (id_type) REFERENCES Type_vetement (id_type),
    CONSTRAINT fk_tri_ramassage FOREIGN KEY (id_ramassage) REFERENCES Ramassage (id_ramassage),
    CONSTRAINT unique_tri UNIQUE (id_type, id_ramassage)
);

CREATE TABLE Concerne
(
    id_type             INT,
    id_achat            INT,
    poids_type_vetement DECIMAL(4, 2),
    PRIMARY KEY (id_type, id_achat),
    CONSTRAINT fk_concerne_typevetement FOREIGN KEY (id_type) REFERENCES Type_vetement (id_type),
    CONSTRAINT fk_concerne_idachat FOREIGN KEY (id_achat) REFERENCES Achat (id_achat)
);

-- INSERTs de base
INSERT INTO Benne_collecte (id_benne, emplacement_benne, distance_magasin)
VALUES (NULL, '1 rue gaston defferre', 2000),
       (NULL, '2 rue ernest duvillard', 500),
       (NULL, '3 rue marcel paul', 2100);

INSERT INTO Type_vetement (id_type, libelle_type, prix_kg_type)
VALUES (NULL, 't-shirt', 20),
       (NULL, 'pantalon', 25),
       (NULL, 'robe', 40),
       (NULL, 'chemise', 30),
       (NULL, 'jupe', 35),
       (NULL, 'veste', 50);

INSERT INTO Categorie_client (id_categorie, libelle_categorie)
VALUES (NULL, 'poids plume'),
       (NULL, 'léger'),
       (NULL, 'lourd'),
       (NULL, 'méga lourd');

INSERT INTO Ramassage (id_ramassage, date_ramassage)
VALUES (NULL, '2024-11-04'),
       (NULL, '2024-10-28'),
       (NULL, '2024-09-12'),
       (NULL, '2024-08-10');


INSERT INTO Distance_entre_benne (id_benne_1, id_benne_2, distance_benne)
VALUES (1, 2, 2100),
       (1, 3, 1050),
       (2, 3, 3000);

INSERT INTO Recolte (id_benne, id_ramassage)
VALUES (1, 1),
       (2, 1),
       (3, 2);

INSERT INTO Tri (id_type, id_ramassage, poids_type_trie)
VALUES (1, 1, 55),
       (1, 2, 74),
       (1, 3, 60),
       (1, 4, 50),

       (2, 1, 45),
       (2, 2, 55),
       (2, 3, 70),
       (2, 4, 30),

       (3, 1, 13),
       (3, 2, 25),
       (3, 3, 10),
       (3, 4, 5),

       (4, 1, 48),
       (4, 2, 55),
       (4, 3, 35),
       (4, 4, 20),

       (5, 1, 18),
       (5, 2, 20),
       (5, 3, 15),
       (5, 4, 2),

       (6, 1, 45),
       (6, 2, 50),
       (6, 3, 60),
       (6, 4, 30);

-- INSERTs pour la série de Tests/SELECTs
INSERT INTO Client (id_client, nom_client, prenom_client, tel_client, adresse_client, email_client,
                    date_naissace_client,
                    id_categorie)
VALUES (NULL, 'MARTIN', 'Elise', '0692123456', '15 avenue des lilas', 'elise.martin@gmail.com', '1985-02-12', 2),
       (NULL, 'ROBERT', 'Paul', '0692987654', '10 rue du temple', 'paul.robert@yahoo.com', '1992-09-23', 3),
       (NULL, 'LOPEZ', 'Marie', '0692334455', '8 rue de la paix', 'marie.lopez@gmail.com', '1990-07-20', 3),
       (NULL, 'SIMON', 'Alex', '0692445566', '45 boulevard du sud', 'alex.simon@hotmail.com', '1988-10-12', 4),
       (NULL, 'DUPONT', 'Jean', '0692556677', '22 rue de la liberté', 'jean.dupont@gmail.com', '1980-05-15', 2),
       (NULL, 'DURAND', 'Sophie', '0692667788', '33 avenue de la république', 'sophie.durand@yahoo.com', '1995-11-25',
        3),
       (NULL, 'LEFEVRE', 'Pierre', '0692778899', '44 boulevard de la paix', 'pierre.lefevre@hotmail.com', '1987-03-10',
        4),
       (NULL, 'MOREAU', 'Claire', '0692889900', '55 rue de la victoire', 'claire.moreau@gmail.com', '1991-08-20', 2),
       (NULL, 'FOURNIER', 'Luc', '0692990011', '66 avenue de la liberté', 'luc.fournier@yahoo.com', '1983-04-15', 3),
       (NULL, 'BERTRAND', 'Anne', '0692001122', '77 boulevard de la république', 'anne.bertrand@hotmail.com',
        '1994-12-05',
        4),
       (NULL, 'ROUX', 'Michel', '0692112233', '88 rue de la paix', 'michel.roux@gmail.com', '1981-06-30', 2);


INSERT INTO Achat (id_achat, date_achat, prix_total, id_client)
VALUES (NULL, '2024-10-01', NULL, 3),
       (NULL, '2024-09-01', NULL, 4),
       (NULL, '2024-10-15', NULL, 5),
       (NULL, '2024-10-10', NULL, 6),
       (NULL, '2024-09-20', NULL, 3),
       (NULL, '2024-10-15', NULL, 9),
       (NULL, '2024-10-15', NULL, 10),
       (NULL, '2024-09-30', NULL, 11),
       (NULL, '2024-08-20', NULL, 5),
       (NULL, '2024-08-10', NULL, 2),
       (NULL, '2024-07-01', NULL, 9);


INSERT INTO Concerne (id_type, id_achat, poids_type_vetement)
VALUES (1, 10, 1.8),
       (2, 9, 2.0),
       (2, 4, 2.0),
       (1, 3, 1.5),
       (2, 1, 1.2),
       (3, 10, 2.5),
       (2, 11, 3.0),
       (1, 9, 1.2),
       (1, 5, 1.0),
       (2, 7, 3.0),
       (3, 8, 2.0),
       (1, 6, 2.5),
       (2, 2, 1.8),
       (4, 1, 1.5), -- Chemise
       (5, 3, 2.0), -- Jupe
       (6, 5, 1.8);

INSERT INTO Reduction (id_type, id_categorie, valeur_reduction)
VALUES (2, 2, 3),
       (1, 1, 3),  -- Réduction pour catégorie "poids plume"
       (2, 1, 5),
       (1, 2, 7),  -- Réduction pour catégorie "léger"
       (3, 2, 12),
       (1, 3, 15), -- Réduction pour catégorie "lourd"
       (2, 3, 20),
       (3, 3, 25),
       (1, 4, 30), -- Réduction pour catégorie "méga lourd"
       (2, 4, 35),
       (3, 4, 40),
       (4, 2, 5),  -- Réduction pour chemise
       (5, 3, 10), -- Réduction pour jupe
       (6, 4, 15); -- Réduction pour veste

UPDATE Achat
SET prix_total = (SELECT SUM(Type_vetement.prix_kg_type * Concerne.poids_type_vetement)
                  FROM Concerne
                           JOIN Type_vetement ON Concerne.id_type = Type_vetement.id_type
                  WHERE Concerne.id_achat = Achat.id_achat)
WHERE Achat.prix_total IS NULL;


# -- Liste des clients ayant acheté des pantalons durant le mois d'octobre 2024
# SELECT sous_requete.id_client, Client.nom_client AS Nom, Client.prenom_client AS Prenom
# FROM (SELECT Achat.id_client AS id_client
#       FROM Concerne
#                JOIN Achat ON Concerne.id_achat = Achat.id_achat
#       WHERE Concerne.id_type = 2
#         AND MONTH(Achat.date_achat) = 10
#         AND YEAR(Achat.date_achat) = 2024
#       GROUP BY Achat.id_client) AS sous_requete
#          JOIN Client ON sous_requete.id_client = Client.id_client;
#
# # -- Afficher le poids trié selon les types de vetements
# # SELECT Type_vetement.libelle_type, sous_requete.poids_total
# # FROM (SELECT Tri.id_type AS id_type, SUM(Tri.poids_type_trie) AS poids_total
# #       FROM Tri
# #       GROUP BY Tri.id_type) AS sous_requete
# #          JOIN Type_vetement ON sous_requete.id_type = Type_vetement.id_type
# # ORDER BY sous_requete.poids_total DESC;
# #
# # -- Total des ventes (en kg) par type de vêtement pour la période du '2024-10-01' au '2024-10-31'
# # SELECT Type_vetement.libelle_type,
# #        SUM(Concerne.poids_type_vetement) AS poids_total_kg_vendu
# # FROM Achat
# #          JOIN Concerne ON Achat.id_achat = Concerne.id_achat
# #          JOIN Type_vetement ON Concerne.id_type = Type_vetement.id_type
# # WHERE Achat.date_achat BETWEEN '2024-10-01' AND '2024-10-31'
# # GROUP BY Type_vetement.id_type, Type_vetement.libelle_type
# # ORDER BY poids_total_kg_vendu DESC;