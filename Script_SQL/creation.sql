CREATE DATABASE IF NOT EXISTS HotelDB;
USE HotelDB;

-- Table Hotel
CREATE TABLE IF NOT EXISTS Hotel (
    Id_Hotel INT AUTO_INCREMENT PRIMARY KEY,
    Ville VARCHAR(255) NOT NULL,
    Pays VARCHAR(255) NOT NULL,
    Code_postal VARCHAR(10) NOT NULL
);

-- Table Client
CREATE TABLE IF NOT EXISTS Client (
    Id_Client INT AUTO_INCREMENT PRIMARY KEY,
    Adresse VARCHAR(255),
    Ville VARCHAR(255),
    Code_postal VARCHAR(10),
    Email VARCHAR(255) UNIQUE,
    Numero_telephone VARCHAR(20),
    Nom_complet VARCHAR(255) NOT NULL
);

-- Table Prestation
CREATE TABLE IF NOT EXISTS Prestation (
    Id_Prestation INT AUTO_INCREMENT PRIMARY KEY,
    Prix DECIMAL(10, 2) NOT NULL,
    Nom_Prestation VARCHAR(255) NOT NULL
);

-- Table Type_Chambre
CREATE TABLE IF NOT EXISTS Type_Chambre (
    Id_Type INT AUTO_INCREMENT PRIMARY KEY,
    Type_Nom VARCHAR(100) NOT NULL,
    Tarif DECIMAL(10, 2) NOT NULL
);

-- Table Chambre
CREATE TABLE IF NOT EXISTS Chambre (
    Id_Chambre INT AUTO_INCREMENT PRIMARY KEY,
    Numero_Chambre INT NOT NULL,
    Etage INT NOT NULL,
    Fumeurs BOOLEAN NOT NULL, -- 0 for false, 1 for true
    Id_Type INT NOT NULL,
    Id_Hotel INT NOT NULL,
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel)
);

-- Table Reservation
CREATE TABLE IF NOT EXISTS Reservation (
    Id_Reservation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivee DATE NOT NULL,
    Date_depart DATE NOT NULL,
    Id_Client INT NOT NULL,
    Id_Chambre INT NOT NULL, -- Ajout crucial
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client),
    FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre)
);

-- Table Evaluation 
CREATE TABLE IF NOT EXISTS Evaluation (
    Id_Evaluation INT AUTO_INCREMENT PRIMARY KEY,
    Date_Evaluation DATE NOT NULL,
    La_note INT CHECK (La_note >= 1 AND La_note <= 5),
    Texte_descriptif TEXT,
    Id_Client INT NOT NULL,
    Id_Hotel INT NOT NULL, -- Ajout
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel)
);

-- Table Offre
CREATE TABLE IF NOT EXISTS Offre (
    Id_Hotel INT NOT NULL,
    Id_Prestation INT NOT NULL,
    PRIMARY KEY (Id_Hotel, Id_Prestation),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation)
);

CREATE TABLE IF NOT EXISTS Concerner (
    Id_Reservation INT NOT NULL,
    Id_Type INT NOT NULL,
    PRIMARY KEY (Id_Reservation, Id_Type),
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
);