# Leistungsdaten & Benchmarks

Dieses Dokument beschreibt die Hardware‑, Modell‑ und Inferenz‑Konfiguration, die wir auf einem **MacBook Pro M4 Pro (24 GB Unified Memory)** verwendet haben, sowie die gemessenen Performance‑Werte.

## 1. Hardwarekonfiguration

- **Prozessor**: Apple M4 Pro (CPU – 12‑Core, GPU – 18‑Core)
- **RAM**: 24 GB Unified Memory
- **Grafik**: Integrierte Apple GPU (Metal)
- **Speicher**: SSD (≥ 512 GB)

## 2. Modell & Quantisierung

- **Modell**: `gpt-oss:20b`
- **Quantisierung**: MXFP4 (8‑Bit für Gewichtungen, 4‑Bit für Aktivierungen)
- **Backend**: `llama.cpp` mit Metal‑GPU‑Beschleunigung

## 3. Konfiguration der Inferenz

- **Kontextfenster**: 16384 Tokens
- **Flash‑Attention**: aktiv (`OLLAMA_FLASH_ATTENTION=1`)
- **KV‑Cache‑Typ**: `q8_0` (`OLLAMA_KV_CACHE_TYPE=q8_0`)

## 4. Messwerte (in OpenCode)

| Messung | Wert | Einheit | Bemerkung |
|---------|------|---------|-----------|
| Tokens pro Sekunde |  | Tokens/s | Gemessen im Echtzeit‑Chat‑Modus mit dem OpenCode UI |
| GPU‑Speicherverbrauch | ~12 GB | GB | Modellgröße + KV‑Cache |
| CPU‑Verbrauch | < 10 % | % | Hauptlast liegt auf der GPU |
| Kontextfenster | 16384 | Tokens | Basiskonfiguration für schnelle Antwortzeiten |

> **Hinweis**: Diese Werte wurden in einer stabilen Umgebung ohne Hintergrundprozesse gemessen.

## 5. Kontextfenster‑Erklärung

- 16384 Tokens wurden auf dem MacBook Pro M4 Pro mit 24 GB Unified Memory erfolgreich verwendet. Allgemeine Stabilität und Performance bei langen Aufgaben sind nicht systematisch nachgewiesen.
- Wir haben 16384 gewählt, weil das Modell auf einem 24 GB Unified Memory‑System problemlos läuft und die Antwortzeit akzeptabel bleibt.

## Optionale Erhöhung über 16K

| Schritt | Beschreibung |
|---------|--------------|
| **Hardware** | Mehr Unified Memory (z. B. 32 GB) oder ein Mac mit mehr GPU‑RAM. |
| **Quantisierung** | MXFP4 unterstützt bis zu 16K, 32K nur mit ausreichendem Speicher. |
| **Backend** | `llama.cpp` kann mit `OLLAMA_CONTEXT_LENGTH=16384` bzw. `32768` konfiguriert werden. |
| **Prüfung** | Nach Änderung von `OLLAMA_CONTEXT_LENGTH` muss Ollama neu gestartet werden. |

## 7. Grenzen des Unified Memory

- **GPU‑Speicher** ist Teil des Unified Memory. Bei 24 GB reicht Platz für Modell + KV‑Cache, aber keine große Auslagerung möglich.
- Für 32K‑Fenster würden mindestens 24 GB benötigt; zusätzlich kann ein **Swap‑Speicher** genutzt werden, jedoch mit Performance‑Einbußen.

---

### Zukunft: Qwen3.8‑27B (NVFP4)

- **Modellgröße**: ~18 GB (NVFP4‑Quantisierung)
- **Backend**: MLX
- **Tokens/s**: ~30,7 Tokens/s (kurzer Benchmark)
- **Problem**: wiederkehrende Metal‑Out‑of‑Memory‑Fehler bei längeren Agentenläufen.

Derzeit bevorzugen wir GPT‑OSS 20B, weil es stabiler auf dem M4 Pro läuft und die GPU ohne Speicher‑Bottleneck arbeitet.

### Erprobung: `qwen3.8:27b` (2026-11-14, beendet)

GPT-OSS 20B bleibt das eingestellte Modell. Qwen wurde zusätzlich getestet;
die Konfiguration wurde danach auf `gpt-oss:20b` zurückgestellt.

- **Umstellung für einen Test**: Modellname in `opencode.json` (`model` und
  Modelleintrag), den drei Profilen in `.opencode/agents/`, `MODEL_NAME` in
  `scripts/doctor.py`, `tests/test_doctor.py` und `AGENTS.md` ersetzen, neue
  OpenCode-Sitzung starten.
- **Modell laut Ollama 0.40.15**: 18,2 GB, 27,8 Mrd. Parameter, NVFP4,
  Runner MLX; Fähigkeiten: Tools, Thinking, Vision. Limits wie bisher:
  16384 Kontext, 2048 Ausgabe.
- **Nicht geprüft**: Zuverlässigkeit der Subagent-Aufrufe und ob 2048
  Ausgabe-Tokens mit Thinking ausreichen; dazu kam es wegen des
  Speicherfehlers nicht.
- **Mögliche kleinere Alternative (ungetestet)**: `qwen3.5:9b-q8_0` (10 GB).

| Datum | Aufgabe | Ergebnis | Auffälligkeiten |
|-------|---------|----------|-----------------|
| 2026-11-14 | `ollama run`, Kurzfragen (15–25 Tokens Prompt) | Erfolgreich, ~26 Tokens/s, Ladezeit 7–11 s | Speicher bereits ohne Kontext am Limit: Spitze 17,55 GiB bei 17,8 GiB Metal-Budget. Erster Prompt nach dem Laden ~10 s Aufwärmzeit. |
| 2026-11-14 | Lesetest Koordinator (`opencode run`, 16384 Kontext) | Gescheitert, kein Arbeiteraufruf | Anfrage mit 513 Tokens lief (Spitze 18,61 GiB). Koordinator-Prompt mit 4563 Tokens brach viermal in Folge beim Einlesen mit Metal-Out-of-Memory ab (HTTP 500), jeweils mit frisch geladenem Modell. |

**Befund 2026-11-14**: Mit Ollama 0.40.15 (MLX) passt `qwen3.8:27b` auf 24 GB
nicht für den Agentenbetrieb: Der Fehler tritt schon beim ersten
Koordinator-Prompt auf, nicht erst bei langen Läufen. Zusätzlich: Die
Ollama-App startet ohne `OLLAMA_CONTEXT_LENGTH` mit 4096 Kontext; das Limit in
`opencode.json` ändert daran nichts (prüfen mit `ollama ps`).
