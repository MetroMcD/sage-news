---
title: Sage 100 9.0.12 Pilotversion – Anlagenbuchhaltung im neuen Gewand, DMS-Mehrfachablage und ein Berg E-Rechnungs-Fixes
date: 6. Nov 2026
category: Sage 100
tag: Release
summary: Unverbindliche Vorab-Info zur Pilotversion der Sage 100 9.0.12. Anlagenbuchhaltung in neuer Technik, DMS-Mehrfachablage, DATEV-Altlasten raus und reichlich E-Rechnungs-Korrekturen.
readTime: 5 min
featured: false
slug: sage-100-9-0-12-pilotversion-neuerungen
---

**Kurz und unverbindlich vorab:** Sage hat die Version 9.0.12 angekündigt, die Pilotversion läuft bereits (Build 1402 vom 19.10.2026). Final sind Features und Funktionen aber noch nicht, und Sage behält sich vor, nicht alles zu übernehmen. Die folgenden großen Punkte werden aber voraussichtlich umgesetzt. Die Kurzfassung: kein Feuerwerk, aber ein ordentlicher Frühjahrsputz im Herbst. Die Anlagenbuchhaltung zieht komplett in die neue Technik, das DMS lernt Mehrfachablage, und die E-Rechnung bekommt so viele Korrekturen, dass es fast für eine eigene Staffel reicht. Die finale Version erwarten wir in den kommenden Wochen. Wer tiefer einsteigen will: Sage dokumentiert die Neuerungen bereits in der [Online-Hilfe](https://onlinehilfe.sage.de/onlinehilfe/ol/90/abf/hh_start.htm#whatsnew.htm?TocPath=_____2).

Und bevor jemand fragt: Ja, ich habe die kompletten Wartungstexte gelesen. 41 Seiten. Rund 150 Einträge. Gefühlt jeder zweite endet auf „ControlCenter.Controller.dll“. Sie bekommen hier die Kurzfassung. Ohne DLL-Listen. Gern geschehen.

## Neu: Die Anlagenbuchhaltung zieht um

Der große Brocken dieses Releases. Die Anlagenbuchhaltung verlässt die Access-Welt und steht künftig in **neuer Technik und in der Smart Edition** zur Verfügung:

- **Grundlagen Anlagenbuchhaltung** sind auf fünf übersichtliche Dialoge aufgeteilt: Allgemeines, Erhöhte Absetzungen, Gebäudeabschreibungen, Preisindizes und Sonderabschreibungen.
- **Stammdaten Anlagen**, **Anlagenbuchungsassistent** und **Anlagenspiegel** laufen in neuer Technik.
- **Abschreibungen periodisch und jährlich** sind als neuer Assistent umgesetzt.
- **Anlagentermine** werden als schreibende Liste gepflegt. Bestehende Termine bleiben erhalten, keine Panik.

Außerdem neu im Rechnungswesen:

- **Umsatzsteuer für Organschaften** gibt es jetzt auch in neuer Technik und in der Smart Edition.
- **Bilanz und Kontennachweis** lassen sich **gemeinsam nach Excel** ausgeben. Ein Export statt zwei. Kleine Freude, großer Effekt am Monatsende.

## Neu im DMS

- **Mehrfachablage:** Mehrere Dokumente mit derselben Verschlagwortung in einem Rutsch ablegen, im Rechnungswesen und in der Warenwirtschaft. Wer bisher zwanzig Belege einzeln verschlagwortet hat, darf jetzt kurz durchatmen.
- **Externe Dokumente im Regiezentrum** ablegen geht jetzt auch im **Smart Client**.
- Die **DMS-Inbox** öffnet wieder das zuletzt genutzte Verzeichnis, getrennt nach Rewe und Wawi. Ein zentrales Ablageverzeichnis im UNC-Format wird inklusive Unterordnern angezeigt.

**Für die Schweiz:** Die **SCOR-Referenz (ISO 11649)** kann in den OP-Details gepflegt und strukturiert in der pain.001 ausgegeben werden. Die Anbindung an Buchungserfassung und QR-Code-Assistent folgt später.

## Wichtig: Das sollten Sie vor dem Update wissen

Jetzt kommt der Teil, bei dem ich kurz die Musik leiser drehe. Diese Änderungen verhalten sich anders als bisher oder brauchen Handarbeit:

- **DATEV-Altlasten entfernt:** `self32.dll`, `Datev.dll` und `OLReweDatev.dll` fliegen raus. Sie unterstützen nur die alten Formate KNE/OBE, die DATEV seit 2018 nicht mehr annimmt. Der **DATEV-Export im EXTF-Format bleibt unverändert**. Individuelle Anpassungen, die auf die alten Komponenten zugreifen, müssen angepasst werden.
- **Bestelldispo mit Verursachern neu konzipiert:** Sie liefert jetzt dieselben Mengen und Termine wie die Dispo ohne Verursacher. Das ist logisch und gut, kann aber gewohnte Ergebnisse verändern. Der Support hält eine Beschreibung bereit.
- **Dispofaktor in der Produktionsdisposition:** Er wird jetzt eingerechnet. Dabei werden die **minimale und maximale Losgröße nicht mehr berücksichtigt**, wenn die Berechnung sie über- oder unterschreitet.
- **Chargen und Seriennummern bei eigenen Belegarten:** Gesteuert wird künftig über die **Nachweispflicht** der Belegart, nicht mehr über die Lieferwirkung.
- **Vorgangsübernahme aus „Offene VK-Lieferungen“:** Der alte Access-Eintrag ist weg. Der neue verlangt die Wahl der **Zielbelegart**.
- **Buchungsimport:** Es werden nur noch **offene Perioden** angeboten.
- **Produktion:** Fertigungsaufträge entstehen nur noch aus **konfigurierten** Konfigurationsartikeln. Unterbaugruppen prüfen die Kennzeichen **Eigenfertigung** und **Als Unterbaugruppe** im Artikelstamm.
- **Partnerlösungen:** Gleichnamige Knoten im Regiezentrum werden nicht mehr zusammengeführt. Betroffene Lösungen lassen sich über AppendTo anpassen.

## Bugfixes, die man im Alltag spürt

**E-Rechnung (ZUGFeRD/XRechnung).** Der heimliche Star des Releases. Unter anderem:

- **PDFs werden beim Mailversand wieder mitgeschickt.**
- **Stornos und Gutschriften** nutzen jetzt den Payment Means Code 57 statt 42, damit sie seltener vom Empfänger abgelehnt werden. Stornorechnungen enthalten zusätzlich das **Datum der Ursprungsrechnung** (BT-26).
- **Organschaften** (verbundene Unternehmen) bekommen den erwarteten **Steuerknoten**.
- Kunden-ID trotz GLN, Kundenreferenz statt „Ihr Zeichen“, die richtigen Kontaktdaten des Rechnungsempfängers und kein störender Hash-Code mehr im XML.
- **Import:** Abweichende XML-Präfixe, Dateinamen bis 255 Zeichen, verständliche Fehlermeldungen statt Exceptions, keine falsche Rabattwarnung mehr und eine korrekt ermittelte E-Mail des Rechnungsstellers.
- Der Hinweis zu USt-IdNr. und Steuernummer erscheint nur noch, wenn **beide** Felder leer sind.

**System und Anmeldung**

- Die **Anmeldung ist wieder flott**. Ein unnötiger Aufruf von id.sage.com bei Windows- und SQL-Authentifizierung ist entfernt.
- Proxy-Bypass-Regeln für interne Adressen greifen wieder.
- Das Application Gateway erkennt den MultiuserService auch über einen Alias.
- Zahlen mit **mehr als 4 Nachkommastellen** werden korrekt gespeichert.

**Warenwirtschaft und Druck**

- **Stapeldruck wiederholen** findet die Belege wieder.
- **Serienbelege erstellen** bleibt nicht mehr scheinbar hängen.
- Anhänge per DCM „SendEMail“ gehen wirklich mit.
- Die **Intrastat-Meldung** läuft schneller.
- Die Warnung bei unterschrittenem Meldebestand erscheint wieder.
- Die Variantenerfassung und das Speichern von Langtexten mit Strg+S funktionieren.

**Produktion**

- Kein **korrupter Fertigungsauftrag** mehr nach manuell angelegten Unter-Fertigungsaufträgen.
- Beistellbelege buchen alle Positionen korrekt.
- Die Fremdfertiger-Dispo rechnet richtige Mengen.
- Die Fertigmeldung berechnet den Einstandspreis wieder korrekt.

**Rechnungswesen und Zahlungsverkehr**

- Datumsfelder in der Zahlungsverkehrs-XML haben das richtige Format.
- SEPA-Platzhalter werden korrekt aufgelöst.
- Kein falsches Steuerkennzeichen mehr bei Kursdifferenzen.
- Die **Saldenbestätigung** landet wieder im DMS.
- Die AfA-Korrektur bei Teilabgängen von Anlagen aus der Zeit vor dem Euro stimmt.
- Die OP-Fälligkeitsanalyse im Schweizer Mandanten zeigt CHF.

Und ja, es gibt noch mehr: Cursorpositionen, Seitenzähler, Formatierungen im AppDesigner. Die haben wir bewusst weggelassen, sonst wären Sie jetzt noch nicht fertig mit Lesen. Und wir auch nicht.

## Und jetzt?

Abwarten, Kaffee trinken, Update planen. Bis Sage die finale Version offiziell freigibt, kann sich am Umfang noch etwas ändern.

**Für das Update melden Sie sich bitte bei Ihrem Sage-Fachhändler.** Er plant mit Ihnen den passenden Termin. Bei verteilten Installationen gilt die bekannte Reihenfolge: erst Application Server, dann Sage-100-Server, zuletzt die Clients. Wer DATEV-Anpassungen, eigene Belegarten oder die Dispo mit Verursachern nutzt, spricht das am besten direkt mit an.

---
Quelle: Sage GmbH, Wartungstexte Pilotversion Sage 100 9.0.12 (zusammengefasst mit KI für Sage-News.de)
