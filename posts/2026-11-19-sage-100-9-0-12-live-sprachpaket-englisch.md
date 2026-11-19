---
title: "Sage 100 9.0.12 ist live: Access-Dialoge im Ruhestand, E-Rechnung mit Nebenjob und ein englisches Sprachpaket zum Nachladen"
date: 19. Nov 2026
category: Sage 100
tag: Release
summary: Sage 100 9.0.12 ist live: neue Oberfläche, viele E-Rechnungs-Stellschrauben, Intrastat-CORE und DATEV-Altlasten raus. Das englische Sprachpaket gibt es separat.
readTime: 6 min
featured: false
slug: sage-100-9-0-12-live-sprachpaket-englisch
---

**Kurzfazit:** Seit gestern ist die **Sage 100 9.0.12** verfügbar. Aus der Pilotversion ist ein Release geworden, aus Access-Dialogen sind Assistenten geworden, und die E-Rechnung hat jetzt mehr Einstellmöglichkeiten als manches Auto. Das **englische Sprachpaket** gibt es wie gewohnt als **separaten Download**. Bitte nicht erwarten, dass es sich beim Update von selbst dazuschleicht.

Die Eckdaten des Änderungsdokuments hatten wir schon in der [Pilotversion-Vorschau](/sage-100-9-0-12-pilotversion-neuerungen/) angerissen, inklusive der Bugfix-Listen. Heute geht es um das, was Sage im Neuerungsdokument auf 27 Seiten beschreibt. Ja, ich habe sie gelesen. Ja, es gibt viele Screenshots von Dialogen, in denen „Weiter >“ steht. Sie bekommen die Kurzfassung.

## Warenwirtschaft: Access wird weiter entsorgt

Das Muster dieses Releases ist klar: Alte Dialoge raus, neue Assistenten rein, und alles läuft auch im **accessfreien Smart Client**. Neu in der Warenwirtschaft:

- **Bestellvorschläge erstellen** ist ein Assistent. Die Artikelauswahl steuern Sie über die Selektionsart: Standardauswahl, individuelle Auswahl oder Filterauswahl. Nach dem Start gibt es eine Hinweismeldung (wie viele Artikel geprüft, wie viele Positionen hinzugefügt) und ein Protokoll mit Lieferantenvergleich.
- **Disposition bearbeiten** hat einen neuen Dialog mit zusätzlichen Spalten und Hamburger-Menü. Achtung: Den aktivieren Sie selbst in den Mandanteneinstellungen unter „Sage 100 Dialogeinstellungen“. Wer ihn dort nicht findet, bekommt weiter den alten und wundert sich, wo die Neuerung bleibt.
- **Preisanfragen und Bestellungen erstellen**, Bedarfsverursacher und Rechnungen erstellen sind ebenfalls auf der neuen Oberfläche. Die Rechnungserstellung bleibt belegbezogen.
- **Preisnachweis und EK-Projektnachweis** in der Belegerfassung: ein neuer Dialog zeigt kundenspezifische Preise, Rabatte, Preis- und Rabattlisten sowie den kalkulatorischen EK.
- **Inventur:** Ein Assistent ändert Bewertungssätze (multiplizieren, allgemein, je Artikelgruppe oder je Artikel). Inventurbewertung und Erfassungsprotokoll gibt es als neue Berichte.
- **Projektschlussrechnung** erstellen und stornieren als Assistenten, Wiedervorlagen laufen in der Warenwirtschaft durchgängig neu.
- **Rewe-Übergabe** mit Filter nach Belegbearbeiter und Übergabeperiode, optional nur für gedruckte Belege.
- **Lieferavis erfassen** in der Auskunft „Offene Warenlieferungen“, Belegnummernprotokoll als neue Auskunft mit vorgeschaltetem Selektionsdialog.
- **Gesamtfertigmeldung** in der Produktion ist jetzt ein Assistent.

Und im **Control Center** wurden die **vordefinierten Auskunftsaufrufe entfernt**. Die Auskünfte selbst gibt es weiter, nur eben auf der Registerkarte „Aufrufe (Funktionen)“. Wer seine Mitarbeiter auf die alte Registerkarte trainiert hat: Sie dürfen erklären, wohin sie umgezogen ist.

## E-Rechnung: Der Nebenjob wird zum Hauptberuf

Zehn Seiten des Dokuments gehören der E-Rechnung. Das Thema ist bekanntlich nicht kleiner geworden. Die wichtigsten Neuerungen:

**Benutzerdefinierte E-Rechnungsfelder.** Im Sage 100 Administrator gibt es unter „Benutzerdefinierte Felder und Register“ den neuen Kontextmenüeintrag **„E-Rechnungsfeld hinzufügen“**. Dort ordnen Sie ein Feld einem **BT-Knoten** zu. Das klingt nach Chirurgie, meint aber nur die Stelle im XML, an der das Feld landet. Verfügbar für Adresse, Artikel, Einkaufs- und Verkaufsbeleg samt Positionen sowie Kunden/Lieferanten. Typische Beispiele aus dem Dokument:

- **Eigentumsvorbehalt:** BT-21 (Code AAJ) plus BT-22 (Text) in der Mandantenadresse.
- **Pfandartikel:** BT-160/BT-161 (Attributname/-wert), z. B. DEPOSIT und RETURNABLE.
- **Kostenstelle des Kunden:** BT-19 im Beleg, BT-133 je Position.
- **Ausschreibungs-, Objekt- und Vertragsreferenzen:** BT-17, BT-18, BT-122 und BT-12, jeweils mit passendem Typ-Code.
- **Leistungszeitraum, Bestellnummer, Freitext je Position:** BT-134/135, BT-132, BT-127.

Wichtig: In den allermeisten Fällen müssen Sie **gar nichts** tun. Die Felder sind optional. Sie sind für den Fall da, dass Ihr Kunde, typischerweise eine große Handelskette, plötzlich Dinge verlangt, die in keinem Standard stehen. Dann sind Sie vorbereitet.

**Steuercodes mit Begründung.** In den Steuersätzen gibt es jetzt **E-Rechnungscode, Reasoncode und Reason-Text**. Gedacht für steuerbefreite Sachverhalte, die sich nicht von allein erklären. Beispiel Export in die Schweiz: E-Rechnungscode G, Reasoncode „Ausfuhr in Drittländer“ (VATEX-EU-G), dazu der Grund als Text. Im Standardfall: nichts ändern.

**Weitere Neuerungen rund um die E-Rechnung:**

- **Anhänge** lassen sich in die E-Rechnung einbetten (BG-24), per Hamburger-Menü im VK-Beleg und Drag & Drop. Der Beleg muss vorher gespeichert sein.
- **GLN** am Adressstamm für abweichende Lieferadressen (BT-71).
- **Abweichender Rechnungsempfänger** im Format ZUGFeRD Extended. Nur dann, wenn der Kunde auf diesen E-Rechnungstyp eingestellt ist.
- **Rabatte** werden separat ausgewiesen, mit Grund und Code 95.
- **Zu- und Abschläge** auf Dokumentenebene können einen Reason Code erhalten. Ohne Auswahl nimmt Sage 100 automatisch ZZZ (Zuschlag) bzw. 95 (Abschlag).
- **Gutschriftverfahren:** Leistungszeitraum bei EK-Belegen möglich.
- **Import:** Der E-Rechnungsimport versteht jetzt auch UBL.

## Rechnungswesen: Die Anlagenbuchhaltung ist nun komplett umgezogen

Was in der Pilotphase noch Ankündigung war, ist jetzt Release. In neuer Technik stehen bereit:

- **Anlagenbuchhaltung:** Grundlagen (fünf Dialoge), Stammdaten, Termine und Wiedervorlagen, Buchungsassistent, periodische und jährliche Abschreibungen sowie der Anlagenspiegel. Für Deutschland gibt es die Varianten „Anlagenspiegel“ und „nach BilRuG“, für die Schweiz einen neuen Anlagenspiegel. Österreich behält die Access-Berichte nach RÄG. Kleiner Trost: Immerhin bleibt etwas übrig.
- **Bilanzauswertung und Kontennachweis** lassen sich nach Excel ausgeben, auch gemeinsam in einer Datei, mit Vergleichszeitraum und Abweichung in Prozent.
- **Umsatzsteuer für Organschaften** (Deutschland): Voranmeldungen der Tochtermandanten als XML einlesen, zusammenfassen und per ELSTER übermitteln. Wichtig: nur gleiche Meldezeiträume und mindestens zwei Dateien.
- **Mahnwesen:** Sammeldruck und Einzeldruck in neuer Technik, mit Sprache, E-Mail-Versand, DMS-Ablage und Hintergrundbild.
- **DMS:** Externe Dokumente lassen sich im Smart Client auch im Regiezentrum ablegen, und die Mehrfachablage (mehrere Dokumente mit gleicher Verschlagwortung) gibt es in Rechnungswesen und Warenwirtschaft.

## Schweiz: Die Adressen werden strukturiert

- **Swiss Payment Standards 2026:** Die Erstellung von Überweisungsdateien (pain.001) ist angepasst, gültig für die Verarbeitung ab dem 13. November 2026. Die Adressen kommen aus Adressstamm bzw. Mandantenadresse. Ort und Land prüfen. Straße und Hausnummer werden gemeinsam aus dem Feld „Straße“ übertragen, ohne automatische Aufteilung. Die Annahme hängt zudem von den Prüfungen Ihrer Bank ab. pain.008 (Lastschrift) ist nicht betroffen.
- **SCOR-Referenz** in den OP-Details wird in der pain.001 strukturiert ausgegeben. Die QR-Referenz (QRR) bleibt. Die automatische Übernahme über Buchungserfassung oder QR-Code-Assistenten gehört nicht zu 9.0.12.

## Bitte vor dem Update lesen

Jetzt der Teil ohne Pointe:

- **Intrastat:** Ab 2027 geht die XML-Datei nur noch über eSTATISTIK.CORE. IDEV wird vom Statistischen Bundesamt nicht mehr unterstützt. Nötig sind Anmeldung und Registrierung. Testdaten sind nicht mehr erforderlich, die Materialnummer entfällt, die Validierung ist strenger (leere Felder werden nicht mehr übergeben). Wer im Januar anfängt zu registrieren, ist im Januar zu spät.
- **DATEV-Altlasten:** Die Formate KNE/OBE und ihre Komponenten sind aus dem Standardumfang entfernt. Direkte Aufrufe von `self32.dll`, `Datev.dll` oder `OLReweDatev.dll` gehen nicht mehr. Der EXTF-Export bleibt fachlich unverändert. Wer individuelle Anpassungen von einem Partner hat: vorher fragen.
- **Control Center:** vordefinierte Aufrufe sind weg (siehe oben).
- **Neue Dialoge** (z. B. Disposition) müssen teils aktiv eingeschaltet werden.

## Das englische Sprachpaket

Wie bei 9.0.11 wird die englische Oberfläche **getrennt heruntergeladen und installiert**. Wer mit englischsprachigen Anwendern oder Tochtergesellschaften arbeitet, sollte das Paket zusammen mit dem Update einplanen, statt es hinterher zu suchen. Das Änderungsdokument selbst enthält keine Angaben zu Umfang und Stand des Pakets. Details dazu bekommen Sie bei Ihrem Sage-Fachhändler.

## Und jetzt?

Update planen, Partneranpassungen prüfen, Intrastat-Registrierung anstoßen. **Für das Update melden Sie sich bitte bei Ihrem Sage-Fachhändler.** Bei verteilten Installationen gilt die bekannte Reihenfolge: erst **Application Server**, dann **Sage-100-Server**, zuletzt die **Clients**. Und wer Access-Dialoge liebt: Jetzt ist ein guter Zeitpunkt, Abschied zu nehmen. Sage nimmt ihn Ihnen ohnehin ab.

---
Quelle: Sage GmbH, Änderungsdokument Sage 100 9.0.12 (zusammengefasst mit KI für Sage-News.de)
