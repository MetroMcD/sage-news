---
title: Sage 100 9.0.11 inkl. Hotfix 9.0.11.1 per LiveUpdate für Kunden ohne Internet
date: 12. Mai 2025
category: Sage 100
tag: Release
summary: Das Service Pack Sage 100 9.0.11 inklusive Hotfix 9.0.11.1 (Build 847) lässt sich auch ohne direkte Internetverbindung per LiveUpdate bereitstellen. Wichtig ist danach vor allem ein Pflichtschritt: Der SA-Systembenutzer muss nach dem Update in jeder Datenbank hinterlegt werden.
readTime: 2 min
featured: false
slug: sage-100-liveupdate-9-0-11-1-ohne-internet
---

Wenn der Produktionsserver keinen Internetzugang hat, ist das beim **Sage 100 LiveUpdate 9.0.11 inklusive Hotfix 9.0.11.1** kein K.o.-Kriterium. Diesmal reicht ein zweiter Rechner mit Internet, ein Datenträger oder ein lokales Netzwerk – also genau die Sorte Umweg, die in vielen Kundenumgebungen ohnehin Alltag ist.

Sage weist darauf hin, dass die für das **LiveUpdate** benötigten Dateien auch auf einem Rechner ohne installierte Sage 100 geladen werden können, solange dort eine Internetverbindung vorhanden ist. Anschließend lassen sich die Dateien per **CD** oder über das **lokale Netzwerk** der eigentlichen Zielumgebung zur Verfügung stellen.

## So funktioniert das LiveUpdate ohne Internetzugang

Für Kunden ohne direkten Internetzugang ist vor allem dieser Punkt relevant:

- **Download auf separatem Rechner:** Die Update-Dateien für **Sage 100 9.0.11 / 9.0.11.1** können auf einem anderen PC mit Internetverbindung geladen werden
- **Bereitstellung offline:** Die Dateien lassen sich anschließend per **CD** oder im **lokalen Netzwerk** an das LiveUpdate übergeben
- **Keine lokale Sage-100-Installation nötig:** Der Download-Rechner muss selbst keine Sage 100 installiert haben

Damit ist das Update auch in abgeschotteten Umgebungen machbar, ohne dass man erst Grundsatzdiskussionen mit der IT-Security führen muss.

## Wichtig nach dem Update: SA-Systembenutzer in jeder Datenbank hinterlegen

Der entscheidende Hinweis steckt nach dem Update auf **Version 9.0.11.1** im administrativen Nachlauf: Der **Systembenutzer muss neu eingetragen** werden. Gemeint ist ein SQL-Benutzer mit Berechtigung **Systemadministrator** – standardmäßig also meist der **SA-User** inklusive Kennwort.

Das erfolgt im **Sage Administrator** für **jede einzelne Datenbank** unter:

- **Datenbanken**
- **Rechtsklick auf die jeweilige Datenbank**
- **Eigenschaften**
- Im Feld **Systembenutzer** einen SQL-Benutzer mit Berechtigung **Systemadministrator** eintragen
- Standardmäßig ist hier meist **SA** gemeint – inklusive passendem Kennwort

Dieser Schritt muss **für jede Datenbank wiederholt** werden. Wer den SA-Systembenutzer nach dem Update nicht sauber hinterlegt, riskiert genau die Art von Folgeproblem, die aus einem Routine-Update unnötig Handarbeit macht.

## Englische Oberfläche: neues Sprachpaket nötig

Wer mit der **englischen Oberfläche der Sage 100** arbeitet, braucht für **Version 9.0.11.1** zusätzlich ein **neues Sprachpaket**. Dieses muss **gemeinsam mit dem LiveUpdate** eingespielt werden.

## Fazit

Das **Service Pack Sage 100 9.0.11 mit Hotfix 9.0.11.1** ist auch für Kunden ohne Internetanschluss sauber per LiveUpdate umsetzbar. Entscheidend ist danach aber der administrative Nachlauf: **SA-Systembenutzer je Datenbank neu setzen** und bei englischer Oberfläche das **neue Sprachpaket** nicht vergessen. Sonst wird aus einem Routineupdate schnell wieder eine kleine Nachmittagsbeschäftigung.

Quelle: Sage GmbH
