---
name: sage-news-email-bericht
description: >
  Redaktions- und Publikationsreferenz für Sage-News-Beiträge aus E-Mails oder
  bereitgestellten Inhalten. Enthält die verbindlichen Regeln für Inhalt,
  Front Matter, HTML-Artikelseiten, Listing, Validierung und Deployment.
---

# Sage News – Referenz für Inhalt und Publikation

Diese Datei ergänzt den Master-Skill mit den operativen Detailregeln.
Sie ist die stabile Nachschlagebasis für das Erstellen und Veröffentlichen von
Sage-News-Beiträgen.

## 1. Quelle zuerst verstehen

Der häufigste Fehler ist, den Artikel aus Betrefffragmenten abzuleiten.
Darum gilt:

1. Mail-Body vollständig lesen
2. Anhänge prüfen
3. Betreff nur für Trigger und Datum nutzen
4. enthaltene Links nur als Zusatzkontext nutzen

Beantworte vor dem Schreiben:
- Was genau ist passiert?
- Welches Produkt ist betroffen?
- Wer ist betroffen?
- Was ändert sich praktisch?
- Welche Versionen, Daten, Fristen oder Module sind belegt?
- Was ist Quelle, was Einordnung?

Wenn etwas nicht belegt ist: weglassen.

## 2. Kategorien und Tags

### Kategorie
Genau eine wählen:
- `Sage 100`
- `Sage X3`
- `Sage Operations`
- `Sage Intact`

### Tag
1 oder 2 Tags, immer als String:
- `tag: "Release"`
- `tag: "Release, Compliance"`

Erlaubte Tags:
- `Release`
- `Neu`
- `KI`
- `Cloud`
- `Compliance`
- `Perspektive`
- `News`

## 3. Ton, Stil und Aufbau

Schreibe in professionellem DACH-Business-Deutsch.

Pflicht:
- direkter Einstieg mit echter Information
- klare Relevanz
- gute Lesbarkeit
- natürliche SEO
- klare Einordnung für Praxis und Projekte

Verbote:
- generische Standard-Intros
- Marketing-Geschwurbel
- Clickbait
- Emoji-Kram
- Halluzinationen

Empfohlene Struktur:

```markdown
[Knapper Einstieg mit Relevanz]

[Kernaussage]

## [Zwischenüberschrift]

[Wichtige Punkte]

## Fazit

[Konkrete Empfehlung oder Einordnung]
```

## 4. Länge und readTime

| Wörter | readTime |
|--------|----------|
| 100–200 | 1 min |
| 200–350 | 2 min |
| 350–500 | 3 min |
| 500–650 | 4 min |
| 650+ | 5 min |

Faustregel: 180 Wörter/Minute, aufgerundet.

## 5. Front Matter

```yaml
---
title: "..."
date: "20. Mai 2026"
category: "Sage 100"
tag: "Release"
summary: "..."
readTime: "3 min"
featured: false
slug: "sprechender-slug"
---
```

Regeln:
- alle Felder sind Pflicht
- `featured` standardmäßig immer `false`
- `slug` immer explizit setzen
- deutsches Datumsformat verwenden

## 6. Datum, Dateiname und Slug

Priorität für das Datum:
1. Datum im Betreff
2. Maildatum
3. heutiges Datum

Dateiname:
- `JJJJ-MM-TT-kurztitel.md`

Slug:
- aus dem finalen Titel ableiten
- Kleinbuchstaben
- Leerzeichen zu Bindestrichen
- Umlaute auflösen
- Sonderzeichen entfernen
- maximal 60 Zeichen

## 7. Quellenangabe

Immer am Ende von Markdown und HTML:
- `Quelle: Sage GmbH` bei Sage-Mail
- sonst kurze eindeutige Quelle

## 8. Deduplizierung

Vor dem Schreiben prüfen:
- gleicher oder ähnlicher Slug?
- gleicher oder ähnlicher Titel?
- gleiche Mail / gleiches Thema schon verarbeitet?

Regel:
- gleicher Slug → kein neuer Beitrag
- ähnlicher Titel + gleiches Datum → wahrscheinlich Duplikat
- gleiches Thema + neueres Datum → Update-Beitrag möglich

## 9. HTML-Artikelseite

Pfad:
- `/home/rene/sage-news/<slug>/index.html`

Pflicht:
- vollständiges Seitenlayout
- Canonical auf `https://sage-news.de/<slug>/`
- Header und Footer wie bestehende Seite
- Hero mit Kategorie, Tag(s), Datum, Titel
- Kurzfazit-/Summary-Box
- Artikeltext in HTML
- Quellenangabe

## 10. Design-Regeln

Immer zuerst echte Repo-Dateien prüfen.
Zu bevorzugen ist der zuletzt erstellte bestehende Artikel als Vorlage.

Blog-/Artikel-Variante:
- keine Smartphone-Hand
- keine gelben Logo-Strahlen
- keine Game-UI-Elemente
- ruhiger, blauer, editorialer Business-Look

## 11. Assets und Pfade

Nur verwenden:
- root-relative Pfade
- absolute Web-URLs
- vorhandene Repo-Assets

Nie verwenden:
- `/home/...`
- `file://...`
- neue ungeprüfte lokale Pfade

## 12. Startseite / Listing

Die Startseite muss neue Beiträge automatisch sichtbar machen.

Aktuelle Regel:
- Homepage-Feed mit 9 sichtbaren Beiträgen
- neue Beiträge müssen nach Veröffentlichung im sichtbaren Feed auftauchen
- falls das Frontend dynamisch aus `posts/` lädt, zusätzlich Feed-Limit und Anzeige-Logik prüfen

Bei neuem Beitrag:
1. prüfen, ob das Listing statisch oder dynamisch erzeugt wird
2. neue Karte bzw. neuen Datensatz im sichtbaren Homepage-Feed sicherstellen
3. bei statischem Listing nach bestehendem Muster vorne einfügen
4. bei dynamischem Listing Feed-Limit, Sortierung oder Anzeigezahl anpassen
5. Links immer auf `/<slug>/`

## 13. Validierung

Vor Commit prüfen:
1. HTML existiert
2. Markdown existiert
3. Canonical korrekt
4. Listing-Link korrekt
5. keine lokalen Pfade im HTML
6. genau 8 Karten auf der Startseite

## 14. Deployment

Ablauf:
- `git status`
- Dateien stagen
- committen
- `git push origin main`

Cloudflare Pages deployt automatisch nach Push auf `main`.

## 15. Live-Prüfung

30–60 Sekunden nach Push prüfen:
- Artikelseite erreichbar
- Startseite erreichbar
- Link auf Startseite vorhanden

## 16. Ergebnis an Rene

Kurz antworten:
- `Neue Berichte online (Bereich - Berichtstitel)`
- bei mehreren als kurze Liste
