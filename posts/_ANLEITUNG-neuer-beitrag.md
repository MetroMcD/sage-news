---
# Anleitung: Neuen Beitrag anlegen
---

## Schritt 1 – Datei benennen

Der Dateiname bestimmt die Sortierung auf der Hauptseite (neueste oben).

Format: `JJJJ-MM-TT-kurztitel.md`

Beispiele:
- `2026-05-01-sage-100-update-904.md`
- `2026-05-15-gobd-checkliste.md`

Der Kurztitel darf nur Kleinbuchstaben, Zahlen und Bindestriche enthalten (keine Leerzeichen, keine Umlaute).

---

## Schritt 2 – Kopfinformationen (Front Matter)

Jede Datei beginnt mit einem Block zwischen `---` Trennlinien:

```
---
title:    Vollständiger Titel des Beitrags
date:     1. Mai 2026
category: Sage 100
tag:      Release
summary:  Kurze Vorschau (1–2 Sätze, erscheint auf der Hauptseite)
readTime: 4 min
featured: false
---
```

### Erlaubte Werte

| Feld       | Beispielwerte                                              |
|------------|------------------------------------------------------------|
| category   | `Sage 100` · `Sage X3` · `Sage Operations` · `Sage Intact` |
| tag        | `Release` · `Neu` · `KI` · `Cloud` · `Compliance` · `News` · `Perspektive` |
| featured   | `true` (großes Kachel-Layout) oder `false` (normales Layout) |
| readTime   | `3 min` · `5 min` · `8 min` usw.                          |
| date       | Deutsches Format: `28. Apr 2026`                          |

---

## Schritt 3 – Inhalt schreiben

Nach dem zweiten `---` kommt der Beitragstext in Markdown.

```markdown
**Kurzfazit:** Ein Satz Zusammenfassung.

## Überschrift

Absatztext...

- Listenpunkt 1
- Listenpunkt 2
```

---

## Schritt 4 – Auf GitHub hochladen

1. Öffne das Repository auf GitHub:  
   `https://github.com/MetrMcD/sage-news`

2. Navigiere in den Ordner `posts/`

3. Klicke auf **Add file → Upload files** (oder **Create new file**)

4. Lade die fertige `.md`-Datei hoch (oder füge den Text direkt ein)

5. Unten bei **Commit changes**:
   - Kurze Beschreibung eingeben, z. B. `Neuer Beitrag: Sage 100 v9.0.4`
   - **Commit directly to the `main` branch** auswählen

6. Auf **Commit changes** klicken – der Beitrag erscheint sofort auf der Webseite.

---

## Tipp: Bilder einbinden

Bilder in den Ordner `uploads/` hochladen, dann im Text referenzieren:

```markdown
![Bildbeschreibung](../uploads/dateiname.png)
```
