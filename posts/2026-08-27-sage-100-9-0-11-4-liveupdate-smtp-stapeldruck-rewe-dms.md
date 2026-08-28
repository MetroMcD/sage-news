---
title: "Sage 100 9.0.11.4: LiveUpdate behebt Probleme bei SMTP, Stapeldruck, Rewe und DMS"
date: "27. August 2026"
category: "Sage 100"
tag: "Release"
summary: "Das LiveUpdate 9.0.11.4 für Sage 100 bringt Korrekturen für SMTP mit OAuth 2.0, Stapeldruck, Rechnungswesen, DMS und weitere Alltagsprobleme in System und Warenwirtschaft."
readTime: "2 min"
featured: false
slug: "sage-100-9-0-11-4-liveupdate-smtp-stapeldruck-rewe-dms"
---

Sage 100 9.0.11.4 ist da und macht das, was gute Wartungsstände tun sollten: Es räumt den Maschinenraum auf, bevor wieder jemand mit starrem Lächeln behauptet, das System laufe doch eigentlich ganz stabil. Dieses LiveUpdate bringt Korrekturen für System, Warenwirtschaft, Rechnungswesen und DMS. Also genau die Sorte Update, die auf keiner Party gefeiert wird, im Alltag aber verhindert, dass Menschen morgens um 8:17 Uhr bereits mit leerem Blick auf ein Supportticket starren.

Neu im Zahlungsverkehr: Serbien wird jetzt als SEPA-Teilnehmerland berücksichtigt. Außerdem bereitet Sage die strukturierte Adressausgabe für den Schweizer Zahlungsverkehr im Rahmen von SPS 2026 vor. Und jetzt kommt der charmante Teil, den Softwarehersteller so lieben: Die Änderung ist mit diesem Hotfix noch gar nicht aktiv. Richtig, sie wurde angekündigt, geschniegelt, geschniegelt nochmal und dann fürs eigentliche Finale auf ein späteres Hotfix verschoben. Die Scharfschaltung soll vor dem Stichtag am 14. November 2026 erfolgen. Das hier ist also noch nicht der große Auftritt, eher das selbstbewusste Räuspern hinter dem Vorhang.

Der eigentliche Spaßverderber-Vernichter steckt sowieso in den Fehlerkorrekturen. Im Systembereich wird die OAuth-2.0-Anmeldung für den SMTP-Versand wieder gespeichert, statt bei jeder einzelnen E-Mail so zu reagieren, als hätte sie das Konzept „bereits angemeldet“ noch nie kennengelernt. Zusätzlich korrigiert Sage Probleme bei der Suche in der Buchungserfassung, bei Fokusverlusten in Filterleisten und bei dynamischen Menüs im xRM-Umfeld. Kleine technische Macken, große Wirkung. Wie ein Kieselstein im Schuh, nur digital und mit Rechnungsbezug.

Auch in der Warenwirtschaft wurde nicht nur symbolisch mit einem Schraubenschlüssel gewedelt. Behoben wurden unter anderem Fehler beim Stapeldruck mit Hintergrundbild, ein interner Fehler bei sehr langen Stapelkennungen, Auffälligkeiten bei der Intrastatmeldung sowie ein Importfehler bei ZUGFeRD- und XRechnungen mit Zuschlägen in Positionen. Im Rechnungswesen kommen Korrekturen beim Datev-Import, bei XML-Zahlungsdateien und bei der UStID-Mehrfachprüfung dazu. Im DMS wurden außerdem Fehler beim Ablegen externer Dokumente im Zahlungsverkehr und beim Inbox-Verzeichnis beseitigt. Übersetzt ins normale Leben: eine ziemlich breite Keule gegen all das Zeug, das sonst nicht spektakulär explodiert, aber zuverlässig den Tag versaut.

Wichtig bleibt die Reihenfolge bei verteilten Installationen: zuerst der Application Server, dann der Sage-100-Server und zuletzt die Clients. Wer zuletzt Ärger mit SMTP per OAuth 2.0, Stapeldruck, Zahlungsverkehr oder DMS hatte, sollte sich dieses Update genauer ansehen. Nicht, weil Wartungsfenster plötzlich Freizeitparks wären. Das wäre grober Unfug. Sondern weil funktionierende Abläufe immer noch die angenehmere Alternative sind zu Fehlersuche, Rückrufbitten und diesem ganz besonderen Gesichtsausdruck, den Menschen entwickeln, wenn ein Prozess zum dritten Mal an exakt derselben Stelle stirbt.

---
Quelle: Sage GmbH (zusammengefasst mit KI für Sage-News.de)
