import sqlite3
import os

DB_FILE = "hotel_streamlit.db"

# Supprimer l'ancienne DB si elle existe, pour repartir de zéro (optionnel)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Ancienne base de données '{DB_FILE}' supprimée.")

try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("Base de données SQLite créée/connectée.")

    # --- Création des Tables ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Hotel (
        Id_Hotel INTEGER PRIMARY KEY AUTOINCREMENT, Ville TEXT NOT NULL,
        Pays TEXT NOT NULL, Code_postal TEXT NOT NULL )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Client (
        Id_Client INTEGER PRIMARY KEY AUTOINCREMENT, Adresse TEXT, Ville TEXT,
        Code_postal TEXT, Email TEXT UNIQUE, Numero_telephone TEXT,
        Nom_complet TEXT NOT NULL )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Type_Chambre (
        Id_Type INTEGER PRIMARY KEY AUTOINCREMENT, Type_Nom TEXT NOT NULL,
        Tarif REAL NOT NULL )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Chambre (
        Id_Chambre INTEGER PRIMARY KEY AUTOINCREMENT, Numero_Chambre INTEGER NOT NULL,
        Etage INTEGER NOT NULL, Fumeurs INTEGER NOT NULL,
        Id_Type INTEGER NOT NULL, Id_Hotel INTEGER NOT NULL,
        FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type),
        FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel) )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservation (
        Id_Reservation INTEGER PRIMARY KEY AUTOINCREMENT, Date_arrivee TEXT NOT NULL,
        Date_depart TEXT NOT NULL, Id_Client INTEGER NOT NULL,
        Id_Chambre INTEGER NOT NULL,
        FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client),
        FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre) )''')

    print("Tables créées.")

    # --- Insertion des Données ---
    cursor.execute("INSERT INTO Hotel (Id_Hotel, Ville, Pays, Code_postal) VALUES (1, 'Paris', 'France', '75001'), (2, 'Lyon', 'France', '69002')")
    cursor.execute("""INSERT INTO Client (Id_Client, Adresse, Ville, Code_postal, Email, Numero_telephone, Nom_complet) VALUES
        (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
        (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
        (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
        (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
        (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')""")
    cursor.execute("INSERT INTO Type_Chambre (Id_Type, Type_Nom, Tarif) VALUES (1, 'Simple', 80), (2, 'Double', 120)")
    cursor.execute("""INSERT INTO Chambre (Id_Chambre, Numero_Chambre, Etage, Fumeurs, Id_Type, Id_Hotel) VALUES
        (1, 201, 2, 0, 1, 1), (2, 502, 5, 1, 1, 2), (3, 305, 3, 0, 2, 1),
        (4, 410, 4, 0, 2, 2), (5, 104, 1, 1, 2, 2), (6, 202, 2, 0, 1, 1),
        (7, 307, 3, 1, 1, 2), (8, 101, 1, 0, 1, 1)""")
    cursor.execute("""INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client, Id_Chambre) VALUES
        (1, '2025-06-15', '2025-06-18', 1, 1), (2, '2025-07-01', '2025-07-05', 2, 2),
        (3, '2025-08-10', '2025-08-14', 3, 3), (4, '2025-09-05', '2025-09-07', 4, 6),
        (5, '2025-09-20', '2025-09-25', 5, 8), (7, '2025-11-12', '2025-11-14', 2, 4),
        (9, '2026-01-15', '2026-01-18', 4, 7), (10, '2026-02-01', '2026-02-05', 2, 5)""")

    print("Données insérées.")

    conn.commit() # Important: Sauvegarder les changements

except sqlite3.Error as error:
    print("Erreur SQLite :", error)
finally:
    if conn:
        conn.close()
        print("Connexion SQLite fermée.")