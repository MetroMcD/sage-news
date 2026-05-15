---
title: Sage Operations API-Update: createMultipleWorkOrderTrackings wird asynchron
date: 15. Mai 2026
category: Sage Operations
tag: Release
summary: Sage stellt den API-Vorgang createMultipleWorkOrderTrackings in Sage Operations von synchron auf asynchron um. Wer die API nutzt, muss Aufruf und Ergebnisabruf anpassen.
readTime: 1 min
featured: false
---

Mit dem aktuellen **Mai-Update für Sage Operations** wird der API-Vorgang **`createMultipleWorkOrderTrackings`** nicht mehr synchron, sondern **asynchron** verarbeitet. Wer diese API nutzt, muss deshalb den Ablauf beim Aufruf und beim Abruf der Ergebnisse anpassen.

## Was sich ändert

Bisher wurde der Vorgang synchron verarbeitet. Künftig läuft die Verarbeitung asynchron im Hintergrund.

Das hat zwei direkte Folgen:

- der **API-Aufruf** verhält sich anders als bisher
- auch der **Ergebnisabruf** muss entsprechend angepasst werden

Laut Sage soll die Verarbeitung damit effizienter und robuster werden – vor allem bei **großen** oder **lang laufenden Vorgängen**.

## Was jetzt zu tun ist

Wer **`createMultipleWorkOrderTrackings`** bereits verwendet, sollte die eigene Anbindung zeitnah prüfen. Sage empfiehlt in diesem Fall ausdrücklich, den **Support** zu kontaktieren, damit die Umstellung sauber begleitet werden kann.

## Fazit

Für betroffene Integrationen ist das keine kosmetische Änderung, sondern eine echte Anpassung im Ablauf. Wer die API im Einsatz hat, sollte das Update nicht einfach durchwinken.

Quelle: Sage GmbH
