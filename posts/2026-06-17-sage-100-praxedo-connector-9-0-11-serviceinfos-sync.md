---
title: "Sage 100 Praxedo-Connector 9.0.11 erweitert Serviceinfos und bereinigt Synchronisationsfehler"
date: "17. Juni 2026"
category: "Sage 100"
tag: "Release"
summary: "Version 9.0.11 des Praxedo-Connectors fuer Sage 100 erweitert Service- und Batchprozesse und behebt Fehler bei Synchronisation, Speicherverbrauch und Installation."
readTime: "2 min"
featured: false
slug: "sage-100-praxedo-connector-9-0-11-serviceinfos-sync"
---
Mit Version 9.0.11 bekommt der Praxedo-Connector fuer Sage 100 mehrere funktionale Ergaenzungen und Korrekturen, die direkt in Service- und Synchronisationsprozesse eingreifen. Besonders relevant sind die Anpassungen fuer Unternehmen, die Servicetouren, Lagerbestaende und Servicevorgaenge mit Praxedo abgleichen.

## Fakten aus dem Update

Bei Servicetouren und Serviceprojekten wurden die Ansprechpartnerinformationen erweitert. Im Batchupload der Lagerbestaende entfernt der Connector die Bestaende in Praxedo fuer alle ausgewaehlten Lager zunaechst vollstaendig und fuellt sie anschliessend anhand der ausgewaehlten Bestaende neu. Fuer den Batchupload von Objekten wurde die Pflichtfeldpruefung um die Objektart in der Listenauswahl ergaenzt.

Auch im Bereich Servicevorgaenge wurden mehrere Punkte nachgezogen. Beim Batchupload kommen weitere Informationen zum Servicevorgang hinzu, darunter Servicenummer und Adressen-Matchcode. Beim Batchdownload wurde ein Problem genannt, bei dem unter Verwendung von xRM-Servicevorgangs-Aktivitaeten Teile des Servicevorgangs unter Umstaenden nicht vollstaendig aktualisiert wurden. Zusaetzlich wird die Bezeichnung von Praxedo-Sammelartikeln beim Download nun immer nach Sage uebernommen.

Darueber hinaus uebermittelt der Connector benutzerdefinierte Felder mit NULL-Werten jetzt auch beim Upload von Sage zu Praxedo. Fuer langlaufende Dienstanwendungen nennt das Update zudem eine Behebung von Out-of-Memory-Fehlern bei Massensynchronisationen. Im Installationsbereich werden Datenbankskripte kuenftig nur noch im Verzeichnis 120 abgelegt.

## Einordnung

Das Release kombiniert kleinere funktionale Erweiterungen mit Korrekturen an kritischen Betriebsstellen. Vor allem die Punkte zu unvollstaendig aktualisierten Servicevorgaengen, Massensynchronisationen und Lagerbestands-Uploads deuten auf praktische Auswirkungen im laufenden Betrieb hin.

## Empfehlung

Sinnvoll ist ein gezielter Blick auf Installationen, die viele Servicevorgaenge synchronisieren oder den Batchabgleich fuer Lagerbestaende intensiv nutzen. Vor einem Rollout sollte geprueft werden, wie sich das neue Verhalten beim Lagerupload und die korrigierten Synchronisationsprozesse in den eigenen Ablaeufen auswirken.

Quelle: Sage GmbH
