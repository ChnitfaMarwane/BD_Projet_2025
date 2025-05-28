-- Afficher la liste des réservations avec le nom du client et la ville de l’hôtel réservé
SELECT
    R.Id_Reservation,
    R.Date_arrivee,
    R.Date_depart,
    Cl.Nom_complet,
    H.Ville AS Ville_Hotel
FROM Reservation R
JOIN Client Cl ON R.Id_Client = Cl.Id_Client
JOIN Chambre Ch ON R.Id_Chambre = Ch.Id_Chambre
JOIN Hotel H ON Ch.Id_Hotel = H.Id_Hotel;

-- Afficher les clients qui habitent à Paris.
SELECT *
FROM Client
WHERE Ville = 'Paris';

-- Calculer le nombre de réservations faites par chaque client.
SELECT
    Cl.Nom_complet,
    COUNT(R.Id_Reservation) AS Nombre_Reservations
FROM Client Cl
LEFT JOIN Reservation R ON Cl.Id_Client = R.Id_Client
GROUP BY Cl.Id_Client, Cl.Nom_complet
ORDER BY Nombre_Reservations DESC;

-- Donner le nombre de chambres pour chaque type de chambre
SELECT
    T.Type_Nom,
    COUNT(C.Id_Chambre) AS Nombre_Chambres
FROM Type_Chambre T
LEFT JOIN Chambre C ON T.Id_Type = C.Id_Type
GROUP BY T.Id_Type, T.Type_Nom
ORDER BY Nombre_Chambres DESC;

-- Afficher la liste des chambres qui ne sont pas réservées pour une période donnée
SELECT *
FROM Chambre
WHERE Id_Chambre NOT IN (
    SELECT Id_Chambre
    FROM Reservation
    WHERE (Date_arrivee < ?) -- Date de fin souhaitée
      AND (Date_depart > ?)  -- Date de début souhaitée
);