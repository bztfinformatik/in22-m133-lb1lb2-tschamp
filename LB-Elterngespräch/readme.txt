Projekt Voraussetzungen:

Eine einfache Planungs Übersicht für Elterngespräche.
In Dieser können Eltern sich mit einem Temp Passwort anmelden.
Dazu braucht es einen Mail Client welcher die Temp Passwörter versendet.
3 Benutzer Gruppen:
Eltern -> Logen sich mit einem Temp Passwort ein und können so einen freien Termin für das Gespräch auswählen.
Lehrer -> Setzen die Termine für Ihre Klassen in welcher sie Klassenlehrer sind und haben eine Übersicht über alle auch schon vergebenen Termine.
Admin  -> Benutzerverwaltung, Übersicht über alle Termine, Möglichkeit Termine zu verwalten.

Die Anmeldung gibt es mit 2 Optionen:
Die Lehrer und Admin Anmeldung, diese wird wen genügen Zeit übrich ist über SSO passieren ansonsten ist diese auch manuell.
Die Eltern Anmeldung diese funktioniert mit Manuell erstellten Gast Logins mit einem Script welches zudem einen Generierten Temp PW key an die Eltern versendet.

Die Daten welche es dafür braucht müssen vom Lehrer manuell eingetragen werden.
Die Passwörter werden mit bcrypt gespeichert.
Die SQL Tables sehen so aus:
Benutzer (BenutzerID, Vorname, Name, E-Mail).
Eltern (ElternID, Vorname, Name, E-Mail).
Termine (TerminID, Datum, Uhrzeit, Status, Eltern IDs).
Klassen (FachschafftID, KlassenID, Name, zugehörige Lehrer IDs).
Fachschafften (FachschafftID, Fachname, Lehrer IDs).


Workflows pro Benutzer:
Eltern-Flow:
Login → Einsicht in verfügbare Termine → Buchung eines Termins → Bestätigung erhalten.
Lehrer-Flow:
Login → Kalenderübersicht → Einsicht in eigene Terminbuchungen → Verwaltung (Bestätigung/Ablehnung) → Verwaltung Eltern.
Admin-Flow:
Login → Benutzerverwaltung → Rollenverwaltung → Terminübersicht (Gesamtsicht).


Backend Aufgaben:

Benutzer.py
Create-Benutzer -> Lehrer und Admins erstellen mit Vorname, Name, Email (ID wird die nächste genommen).
Edit-Benutzer -> Lehrer und Admins bearbeiten.
Delete-Benutzer -> Lehrer und Admins Löschen.

Fachschafften.py
Create-Fachschafften -> Fachschafften bzw. überkategoriene erstellen mit Fachname und LehrerID (ID wird die nächste genommen).
Edit-Fachschafften -> Fachschafften bearbeiten (lehrer hinzufügen oder entfernen).
Delete-Fachschafften -> Fachschafften löschen(zuerst müssen die Klassen darin gelöscht werden).

Klassen.py
Create-Klassen -> Klassen in Fachschafften erstellen mit Name, FachschafftID, LehrerID(ID wird die nächste genommen)
Edit-Klassen -> Klassen in Fachschafften Bearbeiten.
Delete-Klassen -> Automatisch nach Elterngespräch wird dies gelöscht.

Eltern.py
create-Eltern -> Eltern erstellen mit Vorname, Name.
(Create-Eltern_Login) -> Ein Script welches einen Benutzer erstellt mit einer 5 Stelligen Nummer zusätzlich gibt es ein Generiertes Passwort(ID wird die nächste genommen).


Termine.py
Create-Termine -> Termine erstellen welche die Eltern auswählen können.
Block-Termin -> Termine welche schon ausgewählt wurden werden nicht mehr angezeigt.
Delte-Termine -> Termine löschen welche nicht mehr gebraucht werden.
Edit-Termine -> Termine bearbeiten (falsche daten o. ä.).