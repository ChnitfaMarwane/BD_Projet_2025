import streamlit as st
import sqlite3
import pandas as pd
from datetime import date # Pour la validation des dates

DB_FILE = "hotel_streamlit.db"

# --- Fonction pour se connecter à la DB ---
def get_connection():
    return sqlite3.connect(DB_FILE)

# --- Fonctions pour récupérer les données ---
def get_reservations():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT R.Id_Reservation, Cl.Nom_complet, H.Ville AS Hotel_Ville,
               Ch.Numero_Chambre, R.Date_arrivee, R.Date_depart
        FROM Reservation R
        JOIN Client Cl ON R.Id_Client = Cl.Id_Client
        JOIN Chambre Ch ON R.Id_Chambre = Ch.Id_Chambre
        JOIN Hotel H ON Ch.Id_Hotel = H.Id_Hotel
        ORDER BY R.Date_arrivee DESC
    """, conn)
    conn.close()
    return df

def get_clients():
    conn = get_connection()
    df = pd.read_sql_query("SELECT Id_Client, Nom_complet, Email, Ville FROM Client ORDER BY Nom_complet", conn)
    conn.close()
    return df

def get_available_rooms(start_date, end_date):
    conn = get_connection()
    query = """
        SELECT C.Id_Chambre, C.Numero_Chambre, H.Ville, T.Type_Nom, T.Tarif
        FROM Chambre C
        JOIN Hotel H ON C.Id_Hotel = H.Id_Hotel
        JOIN Type_Chambre T ON C.Id_Type = T.Id_Type
        WHERE C.Id_Chambre NOT IN (
            SELECT R.Id_Chambre
            FROM Reservation R
            WHERE (R.Date_arrivee < ?)
              AND (R.Date_depart > ?)
        )
        ORDER BY H.Ville, C.Numero_Chambre
    """
    # Convertir les dates en chaînes YYYY-MM-DD pour la requête
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    df = pd.read_sql_query(query, conn, params=(end_date_str, start_date_str))
    conn.close()
    return df

# --- Fonctions pour ajouter des données ---
def add_client(nom, email, adresse, ville, cp, tel):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Client (Nom_complet, Email, Adresse, Ville, Code_postal, Numero_telephone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, email, adresse, ville, cp, tel))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        st.error(f"Erreur SQLite lors de l'ajout client: {e}")
        return False

def add_reservation(id_client, id_chambre, date_arrivee, date_depart):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Reservation (Id_Client, Id_Chambre, Date_arrivee, Date_depart)
            VALUES (?, ?, ?, ?)
        """, (id_client, id_chambre, date_arrivee.strftime('%Y-%m-%d'), date_depart.strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        st.error(f"Erreur SQLite lors de l'ajout réservation: {e}")
        return False

# --- Interface Streamlit ---
st.set_page_config(page_title="Gestion Hôtelière", layout="wide")
st.title("🏨 Interface de Gestion Hôtelière")

menu = ["Consulter Réservations", "Consulter Clients", "Chambres Disponibles", "Ajouter Client", "Ajouter Réservation"]
choice = st.sidebar.selectbox("Menu", menu)

st.sidebar.info("Projet Bases de Données S4 - 2025")

if choice == "Consulter Réservations":
    st.subheader("Liste des Réservations")
    df_reservations = get_reservations()
    st.dataframe(df_reservations, use_container_width=True)

elif choice == "Consulter Clients":
    st.subheader("Liste des Clients")
    df_clients = get_clients()
    st.dataframe(df_clients, use_container_width=True)

elif choice == "Chambres Disponibles":
    st.subheader("Rechercher des Chambres Disponibles")
    today = date.today()
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("Date d'arrivée", value=today)
    with col2:
        date_fin = st.date_input("Date de départ", value=pd.Timedelta(days=1) + today)

    if st.button("Rechercher"):
        if date_debut >= date_fin:
            st.warning("La date de départ doit être après la date d'arrivée.")
        else:
            df_rooms = get_available_rooms(date_debut, date_fin)
            if not df_rooms.empty:
                st.write(f"Chambres disponibles entre le {date_debut} et le {date_fin} :")
                st.dataframe(df_rooms, use_container_width=True)
            else:
                st.info("Aucune chambre disponible pour cette période.")


elif choice == "Ajouter Client":
    st.subheader("Ajouter un Nouveau Client")
    with st.form("client_form", clear_on_submit=True):
        nom = st.text_input("Nom Complet*")
        email = st.text_input("Email*")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        cp = st.text_input("Code Postal")
        tel = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter Client")
        if submitted:
            if nom and email: # Validation simple
                if add_client(nom, email, adresse, ville, cp, tel):
                    st.success("Client ajouté avec succès !")
                else:
                    st.error("Échec de l'ajout du client (l'email existe peut-être déjà).")
            else:
                st.warning("Le nom et l'email sont obligatoires.")

elif choice == "Ajouter Réservation":
    st.subheader("Ajouter une Nouvelle Réservation")

    clients = get_clients()
    # Assurez-vous que la base de données existe et peut être lue
    try:
        chambres = pd.read_sql_query("SELECT Id_Chambre, Numero_Chambre, Id_Hotel FROM Chambre", get_connection())
        # Créer des listes pour les selectbox
        client_list = {row['Nom_complet']: row['Id_Client'] for index, row in clients.iterrows()}
        chambre_list = {f"Chambre {row['Numero_Chambre']} (Hôtel {row['Id_Hotel']})": row['Id_Chambre'] for index, row in chambres.iterrows()}

        with st.form("reservation_form", clear_on_submit=True):
            selected_client_nom = st.selectbox("Client", options=list(client_list.keys()))
            selected_chambre_desc = st.selectbox("Chambre", options=list(chambre_list.keys()))
            date_arr = st.date_input("Date d'arrivée", value=date.today())
            date_dep = st.date_input("Date de départ", value=pd.Timedelta(days=1) + date.today())

            submitted = st.form_submit_button("Ajouter Réservation")
            if submitted:
                id_cli = client_list[selected_client_nom]
                id_ch = chambre_list[selected_chambre_desc]
                if date_arr < date_dep:
                    # Idéalement, il faudrait vérifier ici si la chambre est dispo !
                    # Pour ce projet, on ajoute directement.
                    if add_reservation(id_cli, id_ch, date_arr, date_dep):
                        st.success("Réservation ajoutée avec succès !")
                    else:
                        st.error("Échec de l'ajout de la réservation.")
                else:
                    st.warning("La date de départ doit être après la date d'arrivée.")
    except Exception as e:
        st.error(f"Impossible de charger les clients ou les chambres. Avez-vous exécuté 'create_db.py' ? Erreur: {e}")