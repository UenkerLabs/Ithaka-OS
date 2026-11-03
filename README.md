<p align="center"><img src="docs/banner.svg" alt="Leman OS für das Nothing Phone (3a) Pro. Offen entwickelt." /></p>

# Leman OS

[![Projektprüfung](https://github.com/YZUe1980/leman-os/actions/workflows/validate.yml/badge.svg)](https://github.com/YZUe1980/leman-os/actions/workflows/validate.yml)

**Dein Handy. Deine Apps. Deine Entscheidung.**

[English](README.en.md) · [Bauanleitung](docs/BUILD.md) · [Gerätestatus](docs/STATUS.md) · [Fahrplan](docs/ROADMAP.md) · [Mitmachen](CONTRIBUTING.md)

**Leman OS** ist ein inoffizielles Android-16-System für das **Nothing Phone (3a) Pro**. Es basiert auf **LineageOS 23.2** und bringt **microG, F-Droid und Aurora Store** mit, ohne vorinstallierte Google-Dienste. Als nächster Schritt wird es auf **Infomaniak** als zentralen Dienst für Mail, Kontakte, Kalender, Dateien und Backup ausgerichtet. Build-Konfiguration, Quellenstände und Testergebnisse sind öffentlich, damit andere die Arbeit nachvollziehen und verbessern können.

**Entwicklungsstand:** Das System läuft auf unserem A059P mit Android 16 und Kernel 6.6. Verschlüsselung, Magisk-Root, Telefonie mit VoLTE, Verbindungen, Kameras, microG und die App-Stores sind geprüft; offen ist nur Glyph. Eine öffentliche Veröffentlichung gibt es bisher nicht.

## Was Leman OS ausmacht

- **Ohne Google-Dienste:** microG ersetzt die proprietären Google Play-Dienste.
- **Apps nach eigener Wahl:** F-Droid und Aurora Store sind eingebaut; alle mitgelieferten Apps sind quelloffen.
- **Infomaniak-Integration (in Arbeit):** Kontakte und Kalender über kSync direkt in den System-Apps, Infomaniak Mail, kDrive und Backups aufs kDrive. Details in [APPS.md](docs/APPS.md).
- **Updates über den eingebauten Updater:** künftige Versionen kommen direkt aufs Handy ([OTA.md](docs/OTA.md)).
- **Nachvollziehbare Entwicklung:** feste Quellenstände, offene Skripte und dokumentierte Tests.
- **Optionales Root:** Magisk lässt sich nach dem ersten Start installieren.

## Was „ohne Google“ hier bedeutet

Leman OS enthält keine vorinstallierten proprietären Google Play-Dienste und Google-Apps. Aurora Store greift weiterhin auf Google Play zu; optionale Funktionen von microG können ebenfalls Google-Verbindungen herstellen. Verbleibende Netzwerk-Standardwerte und Abhängigkeiten dokumentieren wir ausdrücklich.

Außerdem benötigt das Gerät proprietäre Treiber- und Firmwarebestandteile. **Das Repository ist Open Source; der gesamte Firmware-Stack ist es nicht.** Hier veröffentlichen wir die Konfiguration und Verweise auf die Quellen. Firmwarearchive, APKs, private Signierschlüssel und persönliche Gerätedaten gehören nicht hinein.

## So geht es weiter

Bau, Installation und Start auf dem **A059P** sind erfolgreich, einschließlich des Wechsels von Kernel 6.1 auf 6.6. Der [Installationsbericht](docs/INSTALLATION.md) hält den bestätigten Ablauf fest, der [Statusbericht](docs/STATUS.md) die Gerätetests vom 3. November 2026. Als Nächstes folgen ein Build mit aktuellen Quellen und Updates über den eingebauten Updater, danach die Infomaniak-Integration. Der [Fahrplan](docs/ROADMAP.md) zeigt die Reihenfolge.

Mit der [Bauanleitung](docs/BUILD.md) lässt sich der Entwicklungsstand selbst bauen; der neue Wrapper ist noch nicht durch einen vollständigen frischen Bau bestätigt.

## Mitmachen

Du kennst dich mit Android-Gerätequellen aus, kannst Fehler sauber nachstellen oder möchtest die Dokumentation verbessern? Beiträge sind willkommen. Bitte lies [CONTRIBUTING.md](CONTRIBUTING.md) und nenne bei Fehlerberichten den genauen Build-Stand.

## Grundlagen und Lizenzen

Leman OS basiert auf LineageOS, NullDebris' Geräte- und Kernelquellen, LineageOS for microG, microG, F-Droid und Aurora Store. Unsere neuen Skripte und Texte stehen unter [Apache-2.0](LICENSE); fremde Komponenten behalten ihre jeweiligen Lizenzen ([Übersicht](docs/THIRD_PARTY.md)). Leman OS ist ein unabhängiges Community-Projekt und kein offizielles Angebot von Nothing, LineageOS oder Infomaniak.

GitHub Actions prüft Skripte und Manifeste bei Änderungen automatisch. Der vollständige Android-Bau läuft derzeit auf dem Entwicklungsrechner. [Details zur CI](docs/CI.md).
