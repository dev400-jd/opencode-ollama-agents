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
| macOS | 14.x (Monterey, Ventura, oder neuer) | – |
| Homebrew | 3.x | – |
| OpenCode | 0.1.0 (oder neuer) | – |
| Ollama | 0.40.15 | – |
| Ollama‑Backend | `llama.cpp` | – |
| Modell | `gpt-oss:20b` (MXFP4‑Quantisierung) | – |
| Netzwerk | Internetverbindung zum Modell‑Download | – |

## Quickstart

1. **Repository klonen**
   ```bash
   git clone https://github.com/your-org/opencode-ollama-agents.git
   cd opencode-ollama-agents
   ```
2. **Setup‑Guide lesen**
   ```bash
   cat docs/setup-macos.md | less
   ```
3. **Setup ausführen** – folgen Sie den Schritten im Setup‑Guide.
4. **Agenten starten** – nach erfolgreichem Setup starten Sie OpenCode in einem Git‑Repository:
   ```bash
   cd your-project
   opencode start
   ```

> **Hinweis**: Die Modell‑Downloads erfordern eine Internetverbindung. Nach dem Download läuft die Inferenz **offline**.

## Links zur detaillierten Dokumentation

- [Setup‑Guide für macOS](docs/setup-macos.md)
- [Leistungsdaten & Benchmarks](docs/performance.md)
- [Troubleshooting‑Liste](docs/troubleshooting.md)

---

© 2026 OpenCode Ollama Agents – Alle Rechte vorbehalten.
