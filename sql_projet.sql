# Règles de nommage
# https://sql.sh/1396-nom-table-colonne
# TODO : Les appliquer (Dans loopping puis copier coller !)!

DROP TABLE IF EXISTS Concerne;
DROP TABLE IF EXISTS Tri;
DROP TABLE IF EXISTS Recolte;
DROP TABLE IF EXISTS Récolte;
DROP TABLE IF EXISTS Distance_entre_benne;
DROP TABLE IF EXISTS Achat;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Ramassage;
DROP TABLE IF EXISTS Reduction;
DROP TABLE IF EXISTS Categorie_client;
DROP TABLE IF EXISTS Type_vetement;
DROP TABLE IF EXISTS Benne_collecte;

CREATE TABLE Benne_collecte(
   ID_benne INT AUTO_INCREMENT,
   Emplacement_benne VARCHAR(50),
   Distance_magasin INT,
   PRIMARY KEY(ID_benne)
);

CREATE TABLE Type_vetement(
   ID_type INT AUTO_INCREMENT,
   Libelle_type VARCHAR(50),
   Prix_kg_type DECIMAL(19,4),
   PRIMARY KEY(ID_type)
);

CREATE TABLE Categorie_client(
   ID_catégorie INT AUTO_INCREMENT,
   Libelle_catégorie VARCHAR(50),
   PRIMARY KEY(ID_catégorie)
);

CREATE TABLE Reduction(
   ID_reduction INT AUTO_INCREMENT,
   Valeur_réduction INT,
   ID_type INT NOT NULL,
   ID_catégorie INT NOT NULL,
   PRIMARY KEY(ID_reduction),
   FOREIGN KEY(ID_type) REFERENCES Type_vetement(ID_type),
   FOREIGN KEY(ID_catégorie) REFERENCES Categorie_client(ID_catégorie)
);

CREATE TABLE Ramassage(
   ID_ramassage INT AUTO_INCREMENT,
   Date_ramassage DATE,
   PRIMARY KEY(ID_ramassage)
);

CREATE TABLE Client(
   ID_client INT AUTO_INCREMENT,
   Nom_client VARCHAR(50),
   Tel_client VARCHAR(50),
   Adresse_client VARCHAR(50),
   Email_client VARCHAR(50),
   Date_naissace_client DATE,
   ID_catégorie INT NOT NULL,
   PRIMARY KEY(ID_client),
   FOREIGN KEY(ID_catégorie) REFERENCES Categorie_client(ID_catégorie)
);

CREATE TABLE Achat(
   ID_achat INT AUTO_INCREMENT,
   Date_achat DATE,
   Prix_total INT,
   ID_client INT NOT NULL,
   PRIMARY KEY(ID_achat),
   FOREIGN KEY(ID_client) REFERENCES Client(ID_client)
);

CREATE TABLE Distance_entre_benne(
   ID_benne INT,
   ID_benne_1 INT,
   Distance_benne VARCHAR(50),
   PRIMARY KEY(ID_benne, ID_benne_1),
   FOREIGN KEY(ID_benne) REFERENCES Benne_collecte(ID_benne),
   FOREIGN KEY(ID_benne_1) REFERENCES Benne_collecte(ID_benne)
);

CREATE TABLE Recolte(
   ID_benne INT,
   ID_ramassage INT,
   PRIMARY KEY(ID_benne, ID_ramassage),
   FOREIGN KEY(ID_benne) REFERENCES Benne_collecte(ID_benne),
   FOREIGN KEY(ID_ramassage) REFERENCES Ramassage(ID_ramassage)
);

CREATE TABLE Tri(
   ID_type INT,
   ID_ramassage INT,
    # DECIMAL(?,?)
   Poids_type_trié DECIMAL(15,2),
   PRIMARY KEY(ID_type, ID_ramassage),
   FOREIGN KEY(ID_type) REFERENCES Type_vetement(ID_type),
   FOREIGN KEY(ID_ramassage) REFERENCES Ramassage(ID_ramassage)
);

CREATE TABLE Concerne(
   ID_achat INT,
   ID_reduction INT,
    # DECIMAL(?,?)
   Poid_type_vetement DECIMAL(15,2),
   PRIMARY KEY(ID_achat, ID_reduction),
   FOREIGN KEY(ID_achat) REFERENCES Achat(ID_achat),
   FOREIGN KEY(ID_reduction) REFERENCES Reduction(ID_reduction)
);

SHOW TABLES;