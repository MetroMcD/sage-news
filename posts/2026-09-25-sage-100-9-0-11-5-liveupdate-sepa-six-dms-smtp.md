---
title: "Sage 100 9.0.11.5: LiveUpdate bringt SEPA 3.9, SIX 2026 und Korrekturen für DMS, SMTP und Rewe"
date: "25. September 2026"
category: "Sage 100"
tag: "Release"
summary: "Das LiveUpdate 9.0.11.5 (Build 917) für Sage 100 aktualisiert die SEPA-Spezifikation auf 3.9 nach GBIC-5, integriert SIX 2026 für die Schweiz und behebt Fehler in DMS, SMTP, Buchungserfassung und Warenwirtschaft."
readTime: "3 min"
featured: false
slug: "sage-100-9-0-11-5-liveupdate-sepa-six-dms-smtp"
---

Entweder man hat seine Prozesse im Griff — oder die Prozesse haben einen im Griff. Das Sage 100 LiveUpdate 9.0.11.5 (Build 917) sorgt für klare Verhältnisse: Es aktualisiert den Zahlungsverkehr in Deutschland und der Schweiz und korrigiert daneben Fehler in DMS, SMTP-Versand und Buchungserfassung.

### Zahlungsverkehr: SEPA 3.9 und SIX 2026

Für Deutschland erzeugt die SEPA-Version 3.9 Zahlungsdateien durchgängig nach den aktuellen GBIC-5-Vorgaben — für Standard- und Echtzeitüberweisungen, Lastschriften, Auslandszahlungen und taggleiche Euro-Transaktionen. Die Umstellung läuft über die Auswahl der Version 3.9 im Hausbankenstamm.

Für die Schweiz steht unter den Hausbanken die neue Version „SIX 2026“ bereit: pain.001-Dateien nach den Swiss Payment Standards 2026 inklusive der neuen Vorgaben für Adressangaben. Fällig wird sie zum Stichtag am 14. November 2026; bis dahin bleibt für Überweisungen „SIX 2023“ aktiv. Für Österreich korrigiert das Update zudem fehlende Pflichtfelder (NbOfTxs und CtrlSum) in Lastschrift-Dateien nach Spezifikation 2023.

### DMS und Belegerfassung

Im Dokumentenmanagement bleiben die Eigenschaften nach der Ablage von Dokumenten mit benutzerdefinierten Dokumentarten nicht länger leer. Der Eigenschaften-Dialog der Belegablage aus der Kontoauskunft öffnet wieder zuverlässig, abgelegte Warenwirtschaftsbelege erscheinen wieder in der Buchungserfassung, und externe Dokumentlisten lassen sich wie gewohnt mit F5 aktualisieren.

Im Rechnungswesen bleibt die in der Schnellerfassung gesetzte Kontofixierung über nachfolgende Buchungen hinweg erhalten. Beim Versand der Umsatzsteuervoranmeldung und bei Fehlern in der Gruppenübernahme wiederkehrender Buchungen gibt es jetzt erweiterte Trace-Logs statt kryptischer oder fehlender Meldungen.

### System, SMTP und Warenwirtschaft

- **SMTP-E-Mail-Versand:** Bei der Übergabe an den SMTP-Dialog landen Dateien nicht mehr mehrfach im Anhang. Wer je erleben durfte, wie dieselbe Datei plötzlich doppelt klebte und beim Empfänger für Kopfkratzen sorgte — kann ja mal passieren. Ab jetzt passiert es einfach nicht mehr. Außerdem wurden Probleme beim SMTP-Basic-Versand durch Steuerzeichen im Kennwort behoben (falls Fehler auftreten, Kennwort einmalig neu speichern).
- **Listen und Filter:** Die Markierung ausgewählter Datensätze bleibt nach einer Aktualisierung in Listendialogen erhalten. In Filterzeilen navigiert `STRG + Pfeiltasten` präzise innerhalb des Feldes, die einfachen Pfeiltasten wechseln zwischen den Feldern.
- **Warenwirtschaft & E-Rechnung:** Bei der Belegerstellung wurde die mandantenabhängige Schlüsselermittlung korrigiert. In ZUGFeRD- und XRechnungs-Belegen verschwinden überflüssige Leerzeichen im Namensfeld der BuyerTradeParty nun automatisch.

### Installation

Bei verteilten Umgebungen gilt unverändert die feste Reihenfolge: Zuerst der Application Server, danach der Sage 100 Server, abschließend die Client-Arbeitsplätze.

---
Quelle: Sage GmbH (zusammengefasst mit KI für Sage-News.de)