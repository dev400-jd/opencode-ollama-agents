# Projekt

Lokaler Coding-Agent mit OpenCode, Ollama und `gpt-oss:20b`; Kontextbudget: 16K.
`scripts/`: Python-Standardbibliothek; `tests/`: unittest; `docs/`: Einrichtung.
Antworte knapp auf Deutsch. Lies Dokumentation nur bei Bedarf.

## Aufgabenbearbeitung

- Prüfe `git status --short`; erhalte vorhandene Änderungen.
- Kläre Ziel und Abnahmekriterien aus dem Auftrag. Frage nur bei blockierender Unklarheit.
- Untersuche relevante Stellen, ändere gezielt, prüfe das Ergebnis.
- Im Profil `coordinator`: delegiere Tests an `test-worker`, Code/Dokumentation an `worker`, nacheinander. Arbeiter halten Paketgrenzen ein und delegieren nicht weiter.

## Kontext sparen

- Suche zuerst Dateinamen oder Symbole mit `rg`; alternativ `find`/`grep`.
- Lies kleine Dateien vollständig, größere zunächst als relevante Ausschnitte.
- Lies unveränderte Inhalte nur erneut, wenn konkrete Informationen fehlen.
- Begrenze Such- und Logausgaben; erweitere Ausschnitte bei fehlender Evidenz.
- Bewahre umfangreiche Prüfausgaben lokal auf; werte Exitcode und Fehlerstellen aus. Ausgabe-Kürzung darf Fehler nicht verdecken.
- Prüfe betroffene Diffs statt Dateien erneut vollständig auszugeben.
- Wiederhole erfolglose Versuche nur mit neuer Hypothese oder geänderten Bedingungen. Bei Stillstand benenne Befund und benötigte Information.
- Berichte Fortschritt nur mit neuen Erkenntnissen; wiederhole keine Gesprächshistorie.

## Verifikation

- Bei Fehlerbehebungen: Regressionstest zuerst fehlschlagen sehen, dann korrigieren und erneut prüfen.
- Isoliere Fehlerfälle: Alle übrigen Voraussetzungen müssen erfolgreich simuliert sein.
- Ergänze bestehende Tests; entferne sie nur auf Auftrag. Passe Produktivverhalten nicht allein an unvollständige Mocks an.
- Python-Tests: `python3 -m unittest discover -s tests -v`.
- Bei Diagnoseänderungen zusätzlich: `python3 scripts/doctor.py`; reale Ausgabe und Exitcode prüfen. Keine Dienste dafür installieren oder starten.
- Bei reinen Dokumentationsänderungen genügen Diff- und Inhaltsprüfung.
- Untersuche Widersprüche zwischen Tool-Ausgabe und Schlussfolgerung vor dem Abschluss.
- Prüfe jedes Abnahmekriterium und den Diff auf unbeabsichtigte Löschungen, bevor du „fertig“ meldest.

## Arbeitsstand

- Erstelle bei Übergaben `.agent-state.md` mit höchstens ungefähr 200 Wörtern. Ersetze den bisherigen Stand; keine Logs oder Geheimnisse.
- Felder: Ziel, Abnahmekriterien, geänderte Dateien, verifizierte Befehle/Ergebnisse samt Stand, offene Punkte, nächster Schritt.
- Übernimm alle offenen Anforderungen; die Übergabe muss ohne den alten Chat verständlich sein.
- Lies sie beim Fortsetzen, falls vorhanden. Gleiche sie mit Git und aktuellem Auftrag ab; übernimm veraltete Angaben nicht ungeprüft.
- Erfinde keine Kontext-Prozentwerte. Bereite bei angeforderter Übergabe den Stand vor; lösche oder komprimiere keine Sitzung eigenmächtig.

## Abschluss und Git

- Berichte kurz: **Geändert · Geprüft · Offen**. Nenne tatsächliche Prüfungen und Ergebnisse; kennzeichne Ungeprüftes. Behaupte keine vollständige Erfüllung bei offenen Anforderungen.
- Commit und Push nur bei entsprechendem Auftrag; verwende ausschließlich aufgabenbezogene Dateien.
