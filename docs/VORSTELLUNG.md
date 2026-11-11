# Ithaka OS – Android-System für Nothing Phone (3a) Pro

**Ithaka OS** ist ein offenes Entwicklungsprojekt für das **Nothing Phone (3a) Pro**: ein eigenes Android-System auf Basis von **LineageOS 23.2**, mit **microG und F-Droid** und ohne vorinstallierte Google-Dienste.

Das Repository enthält Quellenstände, Build-Konfigurationen, Skripte, Installationshinweise und dokumentierte Prüfergebnisse. Technische Kompatibilität und Einschränkungen sind in den jeweiligen Build-Berichten ausgewiesen.

Ithaka OS läuft auf dem Nothing Phone (3a) Pro mit Android 16 und Kernel 6.6. Installation, Verschlüsselung, VoLTE, Verbindungen und Kameras wurden auf einem Nothing Phone (3a) Pro A059P geprüft. **Glyph funktioniert seit dem dokumentierten Build vom 03.11.2026.** microG ist vorhanden; bei Play-Integrity-abhängigen Anwendungen (beispielsweise der früheren Claude-Anmeldung) bestanden am 04.11.2026 Einschränkungen. Ein Entwicklungskanal im integrierten Updater ist dokumentiert, aber ein reguläres OTA-Update und ein öffentlicher Endnutzer-Release sind nicht vollständig abgenommen. Infomaniak-Apps sind im Build vorhanden; kDrive-Backup benötigt weitere Tests.

Auch „ohne Google“ verwenden wir präzise: keine vorinstallierten proprietären Google Play-Dienste und Google-Apps. Optionale microG-Funktionen können Google-Dienste nutzen. Aurora Store für Google-Play-Apps ist nicht vorinstalliert, lässt sich aber aus F-Droid nachinstallieren. Die benötigte proprietäre Gerätefirmware wird durch ein offenes Build-Rezept ebenfalls nicht automatisch Open Source.

Ithaka OS baut auf der Arbeit von LineageOS, NullDebris, LineageOS for microG und vielen weiteren freien Projekten auf. Das Repository enthält die gerätespezifische Konfiguration und dokumentierte Build- und Gerätetests.

Wer Android-Gerätequellen kennt, sauber testen kann oder die Dokumentation verbessern möchte, ist eingeladen mitzumachen. Wir sammeln alles direkt auf GitHub.

**[Ithaka OS ansehen und mitmachen](https://github.com/UenkerLabs/Ithaka-OS)**
