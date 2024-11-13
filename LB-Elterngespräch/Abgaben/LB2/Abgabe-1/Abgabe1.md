# 1. Darstellung der CSR und der SSR (Theorie)

## Client-Side Rendering (CSR)

Beim Client-Side Rendering (CSR) handelt es sich um eine Repräsentation der kompletten Benutzeroberfläche im Browser. Die Logik zur Darstellung (HTML, CSS und JavaScript) obliegt dem Client, da nur die Daten vom Server geladen werden. Diese Vorgehensweise führt häufig zu einer Steigerung der Interaktivität und einer störungsfreien Benutzererfahrung, vor allem in Single-Page-Anwendungen (SPAs), in denen Benutzer problemlos zwischen den Seiten navigieren können, ohne dass eine komplette Neuladung der Seite erforderlich ist.

**Beispiele für CSR-Vorteile:**
- Schnelle Interaktionen mit den Benutzern nach dem ersten Download.
- Verringerung des Serveraufwands durch verzögerte Rendering-Aufgaben.
- Flexibilität für Rich-Internet-Anwendungen.

## Server-Side Rendering (SSR)

Beim Server-Side Rendering (SSR) werden die HTML-Seiten auf dem Server gerendert und dem Client als komplette Seiten zur Verfügung gestellt. Dadurch wird die Ladezeit für den Nutzer verkürzt, da die Seiten sofort zugänglich sind. SSR eignet sich häufig besser für SEO und erste Ladezeiten, da Suchmaschinen den Content, den der Server bereitstellt, besser indexieren.

**Beispiele für Vorzüge von SSR:**
- Verbesserte erste Ladegeschwindigkeit (First Paint).
- Verbesserte SEO-Unterstützung.
- Höhere Leistung auf schwächeren Endgeräten.

---

# 2. Theoriedokumentation von MVC

Das Architekturmuster des Model-View-Controllers (MVC) unterteilt die Anwendung in drei wesentliche Bestandteile:

- **Modell:** Umfasst die Unternehmenslogik und die Daten der Anwendung. Das Modell ist für den Zugang zur Datenbank und die Verwaltung der Datenstrukturen verantwortlich.
- **View:** Stellt die Informationen aus dem Modell dar und ist für die Anzeige und die Benutzeroberfläche der Anwendung zuständig.
- **Controller:** Der Controller fungiert als Mittler zwischen dem Modell und der Ansicht. Nutzeraktionen werden vom Controller empfangen, verarbeitet und das Modell sowie/oder die Ansicht entsprechend aktualisiert.

MVC erleichtert die Wartbarkeit und Testbarkeit von Anwendungen, da Änderungen in einer Komponente (z. B. der View) die anderen weniger beeinflussen, was zu einer klaren Trennung der Verantwortlichkeiten führt.

---

# 3. Beschreibung der gewählten Technologie (SSR, CSR) inkl. Begründung

## Wahl der Rendering-Technologie: CSR oder SSR

**Gewählte Technologie:** CSR (Client-Side Rendering)

**Begründung:**  
CSR wurde für dieses Projekt ausgewählt, um die Interaktion der Benutzer und die dynamische Nutzererfahrung zu fördern. CSR ist besonders geeignet für Programme, die eine reibungslose Navigation und reaktionsschnelle Interaktionen innerhalb der Benutzeroberfläche priorisieren. Die Benutzererfahrung wird flüssiger und die Anwendung reagiert schneller auf Benutzeraktionen nach dem initialen Laden, da lediglich die erforderlichen Daten vom Server geladen und das Rendering im Browser stattfinden.