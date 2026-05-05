---
name: sage-news-email-bericht
description: >
  Verarbeitet eingehende E-Mails von Sage (sage.de, sage.com) oder mit dem
  Betreff-Präfix ##sage und erzeugt daraus einen druckfertigen Sage-News-Bericht
  im definierten Stil – professionelles DACH-Geschäftsdeutsch mit leichtem
  Situationshumor. Liefert fertigen Markdown-Text inkl. Front Matter zur
  direkten Ablage im posts/-Ordner des Sage-News-Repos.
---

# Sage News – E-Mail-zu-Bericht-Skill

## Zweck

Dieser Skill beschreibt, wie eingehende Sage-E-Mails automatisch in
veröffentlichungsfertige Beiträge für die Sage-News-Website umgewandelt werden.
Jeder Bericht folgt demselben Aufbau und demselben Ton, unabhängig vom Thema.

---

## Schritt 1 – E-Mail-Erkennung

Eine E-Mail wird verarbeitet, wenn **eine** der folgenden Bedingungen zutrifft:

| Bedingung              | Beispiel                                      |
|------------------------|-----------------------------------------------|
| Absender-Domain        | `@sage.de` oder `@sage.com`                   |
| Betreff-Präfix         | Betreff enthält `##sage` (Groß-/Kleinschreibung egal) |

Trifft keine Bedingung zu → E-Mail ignorieren, keinen Bericht erstellen.

`#F` ist **kein** allgemeines Verarbeitungssignal, sondern nur ein zusätzliches Steuersignal für `featured`.

---

## Schritt 2 – Kategorie bestimmen

Prüfe den Inhalt der E-Mail und weise **eine** Hauptkategorie zu:

| Kategorie          | Erkennungshinweise                                                         |
|--------------------|----------------------------------------------------------------------------|
| `Sage 100`         | „Sage 100", „S100", Fibu, DATEV, GoBD, Jahresabschluss, Warenwirtschaft   |
| `Sage X3`          | „Sage X3", „X3", Multi-Site, HR-Modul, People, internationale Prozesse    |
| `Sage Operations`  | „Sage Operations", Produktion, Fertigung, Kapazitätsplanung, MRP, Lager   |
| `Sage Intact`      | „Sage Intact", „Intacct", Mid-Market-Finance, mehrdimensionales Reporting |

Wenn mehrere Kategorien zutreffen: Die **meistgenannte** gewinnt.
Wenn keine passt: `Sage 100` als Fallback.

---

## Schritt 3 – Tag bestimmen

Wähle den passendsten Tag:

| Tag           | Wann                                                           |
|---------------|----------------------------------------------------------------|
| `Release`     | Versionsnummer erwähnt, Patch Notes, „freigegeben", „Update"  |
| `Neu`         | Neues Feature, neue Funktion, neue Komponente                  |
| `KI`          | KI, Machine Learning, Automatisierung, Vorschläge             |
| `Cloud`       | Cloud, SaaS, Hosting, Rechenzentrum, Azure, AWS               |
| `Compliance`  | GoBD, DSGVO, gesetzliche Änderung, Steuer, Pflichtupdate      |
| `Perspektive` | Roadmap, Marktentwicklung, strategische Einordnung            |
| `News`        | Allgemeine Ankündigung, kein passendes Thema oben             |

---

## Schritt 4 – Inhalt zusammenfassen

### Kernfragen vor dem Schreiben

Beantworte diese Fragen aus dem E-Mail-Inhalt – nichts erfinden:

1. **Was ist passiert?** (Release, Feature, Ankündigung, Warnung)
2. **Wen betrifft es?** (Anwender, Admins, Partner, Projektleiter, alle)
3. **Was ändert sich konkret?** (technisch, prozessual, kaufmännisch)
4. **Gibt es eine Handlungsempfehlung?** (Update einplanen, prüfen, abwarten)
5. **Was ist Quelle, was ist Einordnung?** (trennen!)

### Länge

- Standardbeitrag: **300–500 Wörter**
- Komplexe Themen (mehrere Module, technische Tiefe): bis **700 Wörter**
- Kurzmeldung (reine Ankündigung ohne Details): **150–250 Wörter**

---

## Schritt 5 – Bericht schreiben

### Ton und Stil

**Grundton:** Professionelles DACH-Geschäftsdeutsch – sachlich, direkt,
umsetzungsorientiert. Kein Marketing-Sprech, keine Superlativen, keine
Buzzword-Dichte.

**SEO-Anforderung:** Der Beitrag soll nicht nur gut lesbar, sondern auch suchfreundlich aufgebaut sein.

- Wichtige Begriffe aus **Produkt**, **Versionsstand**, **Problem/Korrektur** und **Anwendungsbereich** sollen natürlich vorkommen
- Besonders relevant sind **Titel**, **Summary**, **Zwischenüberschriften** und die ersten Absätze
- Formuliere so, dass reale Suchanfragen gut getroffen werden, z. B. Kombinationen aus `Sage 100`, Versionsnummer, `LiveUpdate`, `Hotfix`, `ZUGFeRD`, `XRechnung`, `SQL Server 2025` oder dem betroffenen Modul
- Keine Keyword-Stapelung, kein Clickbait, keine unnatürlichen Wiederholungen

**Humor:** Leichter Situationshumor – kein Kabarett, kein Slapstick.
Der Witz kommt aus dem Alltag der Zielgruppe, nicht aus einem Gag-Archiv.

#### Humor-Regeln

| Erlaubt                                              | Verboten                              |
|------------------------------------------------------|---------------------------------------|
| Wiedererkennbare Alltagssituation als Einstieg       | Flache Witze oder Wortspiele um des Witzes willen |
| Trockene Beobachtung über bekannte Schmerzpunkte     | Emojis oder Ausrufezeichen-Ketten     |
| Schlusssatz greift Einstiegsbild humorvoll wieder auf | Übertriebenes Selbstlob von Sage      |
| Implizites „das kennen wir alle" ohne es auszusprechen | Sarkasmus auf Kosten des Lesers      |

#### Typische Einstiegssituationen (Inspiration, nicht 1:1 kopieren)

- Montagmorgen / Freitag 16:45 Uhr
- Die Excel-Datei, die „eigentlich ganz gut funktioniert"
- Das Post-it als Notlösung für ein Systemproblem
- Der Kollege, der das alles „schon immer so gemacht hat"
- Die E-Mail-Kette mit 47 Antworten statt einem zentralen System

#### Stilbeispiele

**Schlecht (zu trocken):**
> SQL Server 2025 wurde für Sage 100 freigegeben. Dies ist für bestehende
> Installationen relevant.

**Schlecht (zu albern):**
> OMG SQL Server 2025 ist DA! 🎉 Endlich!! Datenbankparty!!!

**Gut:**
> Niemand muss heute Nacht die Datenbank anfassen. Aber wer beim nächsten
> Kundengespräch mit „SQL Server 2025 ist freigegeben, wir haben das bereits
> geprüft" aufwartet, wirkt angenehm professionell. Und das ist auch was wert.

---

## Schritt 6 – Markdown-Datei erzeugen

### Dateiname

Format: `JJJJ-MM-TT-kurztitel.md`

- Wenn im Betreff ein eindeutiges Datum steht, verwende dieses Datum
- Sonst: Datum der E-Mail
- Nur wenn beides unklar ist: heutiges Datum
- Dasselbe Datum muss konsistent für Dateinamen und Front Matter verwendet werden
- Kurztitel: Kleinbuchstaben, Zahlen, Bindestriche, keine Umlaute, keine Leerzeichen
- Beispiel: `2026-05-01-sql-server-2025-sage-100.md`

### Front Matter

### Datumsregel für historische Beiträge

Steht im Betreff der E-Mail ein klares Datum, gilt dieses als **Erscheinungsdatum** des Beitrags.

Erlaubte Datumsformate im Betreff:
- `DD.MM.YYYY` → Beispiel: `01.05.2026`
- `D. Monat YYYY` → Beispiel: `1. Mai 2026`
- `YYYY-MM-DD` → Beispiel: `2026-05-01`

Beispiele:
- `Update vom 01.05.2026` → `date: 1. Mai 2026`
- `Webinar 1. Mai 2026` → `date: 1. Mai 2026`
- `Release 2026-05-01` → `date: 1. Mai 2026`

Regeln:
- Das Betreff-Datum hat Vorrang vor dem technischen Maildatum.
- Das gewählte Datum muss sowohl im Front Matter als auch im Dateinamen verwendet werden.
- Beiträge mit älterem Datum werden bewusst historisch einsortiert und nicht künstlich auf das aktuelle Datum gesetzt.
- Wenn im Betreff mehrere Daten stehen oder das Datum nicht eindeutig ist, verwende das Maildatum.
- Andere Schreibweisen werden nicht geraten, sondern als nicht eindeutig behandelt.


```markdown
---
title: [Präziser Titel – Nutzen oder Änderung, kein Clickbait]
date: [Tag. Monat Jahreszahl]  ← deutsches Format: "1. Mai 2026"
category: [Sage 100 | Sage X3 | Sage Operations | Sage Intact]
tag: [Release | Neu | KI | Cloud | Compliance | Perspektive | News]
summary: [1–2 Sätze Vorschau – erscheint auf der Hauptseite]
readTime: [X min]
featured: false
---
```

`featured: true` setzen, wenn mindestens **eine** der folgenden Bedingungen erfüllt ist:
- Der Betreff enthält `#F` (Groß-/Kleinschreibung egal)
- Der Betreff enthält `LiveUpdate`, `Live Update` oder `Hotfix`
- Der Mail-Inhalt macht klar, dass es sich um ein `LiveUpdate` oder einen `Hotfix` handelt

Sonst gilt: `featured: false`

Wichtig:
- `#F` ist ein zusätzliches manuelles Steuersignal im Betreff
- `#F` ersetzt **nicht** `##sage`
- Featured-Beiträge bleiben auf der Website nur eine Woche lang featured und fallen danach automatisch auf normale Beiträge zurück

### Inhalt-Struktur

```markdown
[Einstiegssatz oder kurze Szene – 1–3 Sätze, optional mit Humor]

[Kernaussage in 1–2 Sätzen: Was wurde freigegeben / geändert / angekündigt?]

## [Thematische Zwischenüberschrift]

[Fließtext oder Aufzählung mit den wichtigsten Punkten]

- **Punkt 1** erläutert kurz
- **Punkt 2** erläutert kurz
- ...

## Fazit

[1–3 Sätze: Was bedeutet das, was ist zu tun? Ggf. Schlussbild aus dem Einstieg aufgreifen.]
```

**Kein `Kurzfazit`-Block und kein `Quelle:`-Block** für automatisch generierte
E-Mail-Berichte – die Quelle ist implizit der Sage-Newsletter.
Ausnahme: Der Bot wird explizit angewiesen, eine Quelle einzutragen.

## Audio

Aktuell **keine automatische Audio-Nachbearbeitung**.

Regeln:
- Textbeiträge werden ohne Audio veröffentlicht.
- Kein automatisches Enqueueing, kein automatischer NotebookLM-Lauf, kein automatisches Einfügen in Beiträge.
- Audio wird vorerst nur manuell getestet und bei Bedarf später bewusst nachgezogen.
- Fehler oder Limits bei NotebookLM dürfen den Veröffentlichungsworkflow nicht beeinflussen.

---

## Schritt 7 – Qualitätsprüfung vor der Ausgabe

- [ ] Dateiname folgt dem `JJJJ-MM-TT-kurztitel.md`-Schema
- [ ] Datum wurde korrekt priorisiert: Betreff-Datum vor Maildatum vor heutigem Datum
- [ ] Alle Front-Matter-Felder vorhanden und korrekt befüllt
- [ ] `featured` wurde korrekt aus `#F`, `LiveUpdate` oder `Hotfix` abgeleitet
- [ ] Kategorie und Tag passen zum Inhalt
- [ ] Kein Inhalt erfunden – nur was in der E-Mail steht
- [ ] Humor vorhanden aber nicht aufdringlich
- [ ] Länge im Zielbereich (300–500 Wörter Standard)
- [ ] Titel, Summary und Zwischenüberschriften sind suchfreundlich formuliert
- [ ] Wichtige Suchbegriffe kommen organisch im Text vor
- [ ] Schlusssatz gibt eine klare Handlungsempfehlung oder ein Fazit
- [ ] Keine Emojis, keine Ausrufezeichen-Ketten, kein Marketingdeutsch

---

## Vollständiges Beispiel

**Eingehende E-Mail:**
> Von: newsletter@sage.de | Betreff: 01.05.2026 – SQL Server 2025 freigegeben für Sage 100

**Ausgabe:**

```markdown
---
title: SQL Server 2025 für Sage 100 freigegeben
date: 1. Mai 2026
category: Sage 100
tag: Release
summary: Sage hat SQL Server 2025 für relevante Einsatzszenarien freigegeben. Wer noch auf einer älteren Datenbankversion sitzt – kein Stress, aber langsam mal hinschauen.
readTime: 2 min
featured: false
---

Gute Neuigkeit aus der Welt der Datenbanken, die normalerweise niemand aufgeregt
macht: **SQL Server 2025 ist für Sage 100 freigegeben.**

Für alle, die ihre Sage-100-Umgebung gerade so laufen lassen wie seit Jahren
und sich denken „läuft doch" – genau für euch ist das ein guter Moment, mal
kurz hinzuschauen. Wer mittelfristig Modernisierungen, Migrationen oder neue
Installationen plant, sollte die unterstützten Konstellationen kennen.
Sonst plant man an der Realität vorbei.

## Was das bedeutet

- **Neue Projekte** sollten direkt auf SQL Server 2025 aufsetzen
- **Bestehende Systeme** müssen nicht sofort migriert werden, aber
  Kompatibilität und Supportfähigkeit prüfen lohnt sich jetzt
- **Partner und Admins** sollten Kundenumgebungen auf dem Radar haben –
  bevor der Kunde fragt

## Fazit

Niemand muss heute Nacht die Datenbank anfassen. Aber wer beim nächsten
Kundengespräch mit „SQL Server 2025 ist freigegeben, wir haben das bereits
geprüft" aufwartet, wirkt angenehm professionell. Und das ist auch was wert.
```
