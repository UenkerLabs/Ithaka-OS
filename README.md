<p align="center"><img src="docs/banner.svg" alt="Nothing Phone (3a) Pro — LineageOS, microG und Aurora Store. Offen entwickelt." /></p>

# Nothing Phone (3a) Pro — LineageOS, microG & Aurora

[![Projektprüfung](https://github.com/YZUe1980/nothing-phone-3a-pro-lineageos-google-free-aurora/actions/workflows/validate.yml/badge.svg)](https://github.com/YZUe1980/nothing-phone-3a-pro-lineageos-google-free-aurora/actions/workflows/validate.yml)

**Dein Handy. Deine Apps. Deine Entscheidung.**

[English](README.en.md) · [Bauanleitung](docs/BUILD.md) · [Gerätestatus](docs/STATUS.md) · [Mitmachen](CONTRIBUTING.md)

Wir entwickeln eine inoffizielle **LineageOS-23.2-Version für das Nothing Phone (3a) Pro** mit **microG, F-Droid und Aurora Store**. Unsere Build-Konfiguration, Quellenstände und Testergebnisse werden öffentlich, damit andere die Arbeit nachvollziehen und verbessern können.

**Entwicklungsstand: Die ROM läuft auf unserem A059P: Android 16, Kernel 6.6, Verschlüsselung und Magisk-Root sind geprüft. Telefonie mit VoLTE, Verbindungen, Kameras, microG und die App-Stores sind ebenfalls getestet; offen ist nur Glyph. Eine öffentliche ROM-Veröffentlichung gibt es bisher nicht.**

## Was das Projekt ausmacht

- **Weniger vorinstallierte Google-Software:** microG ersetzt die proprietären Google Play-Dienste.
- **Apps nach eigener Wahl:** F-Droid und Aurora Store sind in der Build-Konfiguration enthalten.
- **Nachvollziehbare Entwicklung:** feste Quellenstände, offene Skripte und dokumentierte Tests.
- **Optionales Root:** Magisk 30.7 wurde nach dem ersten Start installiert und mit einem Root-Aufruf geprüft.
- **Gemeinsam verbessern:** Fehlerberichte und Beiträge sammeln wir zunächst direkt auf GitHub.

## Was „Google free“ hier bedeutet

Unser Ziel ist ein System ohne vorinstallierte proprietäre Google Play-Dienste und Google-Apps. Aurora Store greift weiterhin auf Google Play zu; optionale Funktionen von microG können ebenfalls Google-Verbindungen herstellen. Verbleibende Netzwerk-Standardwerte und Abhängigkeiten dokumentieren wir ausdrücklich.

Außerdem benötigt das Gerät proprietäre Treiber- und Firmwarebestandteile. **Das Repository ist Open Source; der gesamte Firmware-Stack ist es nicht.** Hier veröffentlichen wir die Konfiguration und Verweise auf die Quellen. Firmwarearchive, APKs, private Signierschlüssel und persönliche Gerätedaten gehören nicht hinein.

## So geht es weiter

Bau, Installation und Start auf dem **A059P** sind erfolgreich, einschließlich des Wechsels von Kernel 6.1 auf 6.6. Der [Installationsbericht](docs/INSTALLATION.md) hält den bestätigten Ablauf und seine Besonderheiten fest. Die Gerätetests vom 3. November 2026 waren bis auf Glyph erfolgreich. Als Nächstes folgen ein Build mit aktuellen Quellen und [Updates über den LineageOS-Updater](docs/OTA.md).

Der [Statusbericht](docs/STATUS.md) zeigt, was erledigt ist und welche Prüfungen noch ausstehen. Mit der [Bauanleitung](docs/BUILD.md) lässt sich der Entwicklungsstand untersuchen; der neue Wrapper ist noch nicht durch einen vollständigen frischen Bau bestätigt.

## Mitmachen

Du kennst dich mit Android-Gerätequellen aus, kannst Fehler sauber nachstellen oder möchtest die Dokumentation verbessern? Beiträge sind willkommen. Bitte lies [CONTRIBUTING.md](CONTRIBUTING.md) und nenne bei Fehlerberichten den genauen Build-Stand.

Die Arbeit basiert auf LineageOS, NullDebris' Geräte- und Kernelquellen, LineageOS for microG, microG, F-Droid, Aurora Store und Magisk. Unsere neuen Skripte und Texte stehen unter [Apache-2.0](LICENSE); fremde Komponenten behalten ihre jeweiligen Lizenzen. Dieses unabhängige Community-Projekt ist kein offizielles Angebot von Nothing oder LineageOS.

GitHub Actions prüft Skripte und Manifeste bei Änderungen automatisch. Der vollständige Android-Bau läuft derzeit auf dem Entwicklungsrechner. [Details zur CI](docs/CI.md).
