# OpenCode Ollama Agents – Lokale KI-Coding‑Agenten‑Umgebung

Dieses Repository stellt eine vollständig **lokale** Umgebung bereit, um KI‑Coding‑Agenten mit **OpenCode**, **Ollama** und lokalen Open‑Weight‑Modellen auf einem **MacBook Pro M4 Pro** zu entwickeln, zu testen und zu experimentieren.

## Projektziel

- **Keine kostenpflichtige Modell‑API** – alle Inferenz‑Modelle laufen lokal auf der integrierten Metal‑GPU.
- **Reproduzierbare Einrichtung** – alle Schritte sind als Befehle dokumentiert, sodass Kollegen exakt den gleichen Stand erreichen können.
- **Schneller Start** – ein einfacher Quick‑Start‑Workflow, der sofort einsatzbereit ist.

## Architekturübersicht

```
OpenCode ──► Ollama API (http://127.0.0.1:11434) ──► local GPT‑OSS 20B (llama.cpp + Metal)
```

- **OpenCode** liefert die Agenten‑Logik und die UI.
- **Ollama** dient als lokaler HTTP‑Server, der Modelle verwaltet und inference‑Anfragen entgegennimmt.
- **llama.cpp** wird als Backend eingesetzt und nutzt die **Metal**‑GPU für Beschleunigung.

## Hardware‑ und Softwarevoraussetzungen

| Komponente | Spezifikation | Version |
|------------|--------------|---------|
| Mac | MacBook Pro (M4 Pro, 24 GB Unified Memory) | – |
| macOS | 14.x (Sonoma oder neuer) | – |
| Homebrew | 3.x | – |
| OpenCode | 2.2.4 (geprüft) | – |
| Ollama | 0.40.15 | – |
| Ollama‑Backend | `llama.cpp` | – |
| Modell | `gpt-oss:20b` (MXFP4‑Quantisierung) | – |
| Netzwerk | Internetverbindung zum Modell‑Download | – |

## Getestete Softwareversionen

- macOS 14.x (Sonoma)
- OpenCode v2.2.4
- Ollama v0.40.15
- Modell: gpt-oss:20b
- Laufzeitkontext: 16384 Tokens


1. **Repository klonen**
   ```bash
   git clone https://github.com/your-org/opencode-ollama-agents.git
   cd opencode-ollama-agents
   ```

2. **Ollama installieren und Modell herunterladen**
   ```bash
   brew install ollama
   ollama pull gpt-oss:20b
   ```

3. **Ollama Server starten**
   ```bash
   OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 OLLAMA_CONTEXT_LENGTH=16384 ollama serve
   ```

4. **OpenCode starten**
   ```bash
   ollama launch opencode --model gpt-oss:20b
   ```

> Details are in [docs/setup-macos.md](docs/setup-macos.md).

## Arbeiten mit begrenztem Kontext

Fuer automatische kleine Arbeitspakete ist das Profil `coordinator` mit
`test-worker` fuer Tests und `worker` fuer Code eingerichtet. Sie arbeiten
nacheinander. Start im Repository: `opencode --standalone`.
Alle verwenden lokal `gpt-oss:20b`. Ablauf, Grenzen und Pruefung stehen in
[Kleine Aufgaben mit frischem Kontext](docs/delegation.md).

Die [AGENTS.md](AGENTS.md) führt den lokalen Agenten durch gezielte Änderungen,
Prüfungen und kurze Ergebnisberichte. Starte OpenCode im Repository. Die Regeln
sollen unnötige Dateiausgaben und Wiederholungen reduzieren; ihre Wirkung auf
Kontextverbrauch und Zuverlässigkeit ist noch nicht gemessen.

Bearbeite überschaubare Aufgaben mit klaren Abnahmekriterien. Bei ungefähr
65–70 % Kontextbelegung in der OpenCode-Anzeige kannst du eine Übergabe
vorbereiten lassen. Diese Schwelle ist ein anfänglicher Versuchswert:

> Schreibe den aktuellen Arbeitsstand in `.agent-state.md`: Ziel,
> Abnahmekriterien, geänderte Dateien, verifizierte Befehle und Ergebnisse
> samt Stand, offene Punkte und nächster konkreter Schritt. Ersetze den
> bisherigen Inhalt und bleibe unter ungefähr 200 Wörtern.

Starte anschließend eine neue Sitzung im selben Repository mit:

> Setze die Aufgabe aus `.agent-state.md` fort. Prüfe zuerst den aktuellen
> Git-Stand und die relevanten Dateien; frühere Prüfergebnisse können veraltet sein.

Die Zustandsdatei wird bei Bedarf erstellt und von Git ignoriert. Sie darf
keine Geheimnisse oder vollständigen Logs enthalten. Eine neue Sitzung
übernimmt den alten Gesprächsverlauf nicht automatisch.

### Wirkung überprüfen

Vergleiche dieselbe kleine Aufgabe in getrennten frischen Sitzungen auf
demselben Ausgangsstand, einmal ohne und einmal mit den Projektregeln.
Notiere jeweils die angezeigte Kontextbelegung vor der Aufgabe, nach dem
Lesen und nach Änderung und Prüfung sowie erfolgreiche Prüfungen und nötige
manuelle Eingriffe. Wiederhole den Vergleich, bevor du Verbesserungen ableitest.

Modell und 16K-Laufzeitkonfiguration bleiben dabei gleich. `opencode.json`
legt nun passende Startwerte fuer Kontext und Komprimierung fest; Details
stehen in der Delegationsanleitung. `AGENTS.md` selbst veraendert diese
Einstellungen nicht. Technische
Details: [Projektanweisungen](https://opencode.ai/docs/instructions/) und
[Kontextkomprimierung](https://opencode.ai/docs/compaction/).

## Links zur detaillierten Dokumentation

- [Setup‑Guide für macOS](docs/setup-macos.md)
- [Leistungsdaten & Benchmarks](docs/performance.md)
- [Troubleshooting‑Liste](docs/troubleshooting.md)

---

© 2026 OpenCode Ollama Agents – Alle Rechte vorbehalten.
