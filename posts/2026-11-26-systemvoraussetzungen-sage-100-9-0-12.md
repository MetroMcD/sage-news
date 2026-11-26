---
title: Systemvoraussetzungen für Sage 100 Version 9.0.12 veröffentlicht
date: 26. Nov 2026
category: Sage 100
tag: Release
summary: Sage hat die Systemvoraussetzungen für Sage 100 Version 9.0.12 (Stand Oktober 2026) veröffentlicht. Neu ist ein Firewall-Eintrag für die Online-Kursabfrage. Der Systemcheck auf sage-news.de ist bereits angepasst.
readTime: 1 min
featured: false
slug: systemvoraussetzungen-sage-100-9-0-12
---

Zur **Sage 100 9.0.12** gibt es die passenden **Systemvoraussetzungen** mit Stand **Oktober 2026**. Die gute Nachricht vorweg: Wer die Umgebung schon für 9.0.11 vorbereitet hat, muss kaum etwas tun.

## Was ist neu?

Laut Änderungshistorie des Dokuments gibt es gegenüber der Fassung 9.0.11 (Mai) genau eine Änderung:

- **Firewall-Einstellungen für die Online-Kursabfrage** (Kapitel 4.5.2): Die Adresse **https://www.ecb.europa.eu** muss erreichbar sein, damit Sage 100 die Wechselkurse der Europäischen Zentralbank abrufen kann.

Hardware, Betriebssysteme, SQL Server und Office-Versionen bleiben unverändert.

## Wichtig für die Praxis

- Vor dem Update auf **9.0.12** die Freigabe für **www.ecb.europa.eu** in Firewall oder Proxy prüfen, sonst schlägt die Kursabfrage fehl.
- Der **Mainstream-Support** für **Windows Server 2022** und **Access 2021** ist am **13.10.2026** ausgelaufen. Sage gibt beides weiter frei, solange Microsoft Extended Support leistet. Für die Planung neuer Server lohnt der Blick auf Windows Server 2025 und Access 2024.

## Direkter Check

Der **Systemcheck auf der Website** ist auf Version 9.0.12 umgestellt. Er enthält jetzt auch eine **Firewall-Checkliste** mit allen Adressen aus dem Sage-Dokument und bewertet die Support-Enden automatisch nach dem heutigen Datum:

**https://sage-news.de/#systemcheck**

Das aktuelle PDF der Systemvoraussetzungen lässt sich dort direkt herunterladen.

---
Quelle: Sage GmbH (zusammengefasst mit KI für Sage-News.de)
