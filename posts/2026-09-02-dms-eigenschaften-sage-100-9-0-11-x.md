---
title: "DMS-Eigenschaften nach Sage-100-LiveUpdate auf 9.0.11.x – Fehlende Dokumentenarten und Metadaten"
date: "2. September 2026"
category: "Sage 100"
tag: "Release"
summary: "Nach dem Update auf Sage 100 9.0.11.x können eigene DMS-Dokumentenarten ihre Eigenschaften verlieren. Grund ist die Umstellung der DMS-Masken auf neue Technik. Ab Version 9.0.12 wird das Verfahren erneut umgestellt."
readTime: "2 min"
featured: false
slug: "dms-eigenschaften-sage-100-9-0-11-x"
---

Wenn Sie die Sage 100 von Version 9.0.10.7 auf 9.0.11.x aktualisiert haben und sich nun fragen, warum Ihre selbst angelegten DMS-Dokumentenarten ein mysteriöses Eigenleben entwickeln – keine Sorge, Sie haben nichts falsch gemacht. Die DMS-Masken wurden auf eine neue Technik umgestellt, und Ihre alten Anpassungen haben schlichtweg nicht mitbekommen, dass sie jetzt „metadatenkompatibel" sein müssen.

Die Symptome sind wie folgt:

- Ihre Dokumentenarten erscheinen zwar in der Suche und Ablage, aber die **Eigenschaftsfelder** bleiben beharrlich leer. Als hätte jemand vergessen, den Innenraum einzubauen.
- Die Dokumentenarten oder ihre Eigenschaften bleiben **komplett unsichtbar**. Sie existieren, aber sie zeigen sich nicht. Eine philosophische Frage, mit der man sich beschäftigen kann, wenn gerade kein Kunde wartet.
- Der Zugriff auf Ihre eigenen Wertelisten hinter den Eigenschaftsfeldern? Fehlanzeige. Die Hintertür ist zu, und der Schlüssel steckt auf der anderen Seite.

## Ursache

Mit dem Update auf 9.0.11.x wurden die DMS-Masken technisch grundlegend erneuert. Das ist an sich eine gute Sache, vergleichbar mit dem Einbau eines modernen Sicherheitssystems – nur dass die alte Schließanlage plötzlich nicht mehr passt. Ihre eigenhändig erstellten Dokumentenarten müssen nun „metadatenkompatibel" sein, sonst verweigern sie schlicht den Dienst. Ich möchte an dieser Stelle betonen, dass dies kein Grund zur Panik ist. Aber ein Grund, die Bedienungsanleitung zu lesen, bevor man einfach losschraubt.

## Ausblick auf Version 9.0.12

Zur Version 9.0.12 wird das Verfahren noch einmal umgestellt. Diesmal aber richtig. Partneranpassungen werden dann als **vollwertige Metadaten in einer eigenen, änderbaren Partner-Lösung** bereitgestellt, die über den bekannten `AppendTo`-Mechanismus die Sage-DMS-Elemente erweitert. Klingt kompliziert? Ist es auch, aber diesmal funktioniert es.

Ein wichtiger Hinweis, den ich mit Nachdruck anbringen möchte: Die in 9.0.11 automatisch erzeugten Metadaten müssen gelöscht werden, bevor die Umstellung auf 9.0.12 erfolgt. Nicht vergessen, nicht aufschieben, nicht hoffen, dass es sich von selbst erledigt. Tut es nicht.

## Einordnung für die Praxis

Wer nach dem Update auf 9.0.11.x mit DMS-Problemen kämpft, steht vor einer strategischen Frage: die Metadaten jetzt mühsam anpassen und hoffen, dass es bis 9.0.12 hält – oder direkt auf die 9.0.12 warten, die das Verfahren grundlegend vereinfacht. Beides sind valide Optionen. Die eine erfordert Arbeit jetzt, die andere erfordert Geduld. Ich empfehle, die Situation zu analysieren, eine Entscheidung zu treffen und dann nicht ständig die Einstellungen zu ändern. Das verwirrt das System. Und mich.

---
Quelle: Sage GmbH (zusammengefasst mit KI für Sage-News.de)