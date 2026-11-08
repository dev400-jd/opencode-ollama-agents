# Agenten-Workflow mit OpenCode

Das Profil wurde mit OpenCode 2.2.4 und lokalem `ollama/gpt-oss:20b`
erprobt. Alle Rollen verwenden dasselbe Modell und arbeiten nacheinander.

## Start und Auftrag

Ollama muss laufen und das Modell vorhanden sein. Im Repository starten:

```bash
opencode --standalone
```

`opencode.json` wählt `coordinator` und das lokale Modell. Prüfe beides
im Chat, besonders bei bestehenden Sitzungen. `--standalone` startet einen
privaten OpenCode-Server; Ollama wird damit nicht gestartet.

Beschreibe Ziel, erlaubte Dateien und erwartetes Ergebnis, zum Beispiel:

```text
Prüfe tests/test_doctor.py auf fehlende Isolation und ergänze nötige Mocks.
Delegiere die Änderung an test-worker. Erhalte alle vorhandenen Tests und
ändere nur diese Testdatei. Prüfe anschließend selbst die Tests und den Diff.
Prüfbefehl: python3 -m unittest discover -s tests -v
Kein Commit oder Push.
```

Dieser Auftrag bearbeitet Tests und führt sie aus.

## Rollen und Ablauf

| Profil | Aufgabe | Schreibrechte über Edit-Werkzeuge |
|---|---|---|
| `coordinator` | Kleine Pakete delegieren und Ergebnisse prüfen | `.agent-state.md` |
| `test-worker` | Tests ergänzen | `tests/*` |
| `worker` | Code oder Dokumentation ändern | `scripts/*`, `docs/*`, `README.md` |

Die Profile liegen in `.opencode/agents/`. Ein Paket nennt Ziel, erlaubte
Dateien, unveränderte Anforderungen, Abnahmekriterien und Prüfbefehle
in höchstens etwa 200 Wörtern. Arbeiter delegieren nicht weiter.

Bei Fehlerbehebungen gilt:

1. `test-worker` ergänzt den Regressionstest und erhält vorhandene Tests.
2. Der Koordinator führt die Tests selbst aus und prüft den erwarteten Fehler.
3. `worker` korrigiert den Code; Tests bleiben unverändert.
4. Der Koordinator prüft selbst Tests, `git status --short` und den Diff.

Shell-Freigaben umfassen Git-Status/Diff und die unittest-Suite;
Koordinator und Code-Arbeiter dürfen zusätzlich `python3 scripts/doctor.py`
ausführen. Commit, Push und Dienststarts sind in den Profilen nicht freigegeben.

## Einstellungen und Prüfung

`opencode.json` setzt 16.384 Tokens Kontext, 2.048 Tokens Ausgabe und
automatische Komprimierung mit 2.000 Tokens erhaltener Historie sowie
4.096 Tokens Reserve. Die Provider-Anbindung benötigt
`package: "@ai-sdk/openai-compatible"` und die lokale Ollama-URL.
Der Koordinator hat 16 Modellschritte, jeder Arbeiter 12.

Im Repository prüfen:

```bash
opencode debug agents --standalone
python3 -m unittest discover -s tests -v
git diff --check
ollama ps
```

Erwartet: `coordinator` als `primary`, beide Arbeiter als `subagent` mit
lokalem Modell; `ollama ps` zeigt den tatsächlich geladenen Kontext.
Bei Schreibaufgaben müssen echte Arbeiteraufrufe im Chat sichtbar sein.
Ein CLI-Exitcode 0 allein belegt keinen erfolgreichen Auftrag.

Der manuelle Chatversuch zeigte Regressionstest zuerst rot, danach beide
Tests grün und eine nachgeholte Diff-Prüfung. Der Koordinator versuchte
anfangs selbst zu editieren; seine Berechtigung blockierte das. Der vorherige
CLI-Versuch lieferte trotz Arbeiteraufrufen keine Änderungen. Die Calc-Vorlage
wurde nach dem Versuch entfernt.

Automatische Delegation bleibt Modellverhalten. Beide Arbeiter teilen den
Arbeitsbaum; die Rechte sind keine Betriebssystem-Sandbox. Lange Sitzungen,
Komprimierungsqualität und Kontextvorteile sind bisher nicht nachgewiesen.
