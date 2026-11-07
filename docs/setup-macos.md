# Setup‑Guide für macOS

Dieses Dokument führt dich Schritt für Schritt durch die Einrichtung einer vollständig lokalen KI‑Coding‑Agenten‑Umgebung auf einem **MacBook Pro M4 Pro** (24 GB Unified Memory). Alle Befehle sind kopierbar und an die aktuelle Systemkonfiguration angepasst.

## 1. Hardware & macOS prüfen

```bash
# Betriebssystem
sw_vers

# Apple‑Chip überprüfen
uname -m
# Ergebnis sollte "arm64"
```

Falls du noch nicht mit Apple‑Silicon arbeitest, muss ein M‑Chip vorhanden sein.

## 2. Homebrew prüfen/Installieren

```bash
if ! command -v brew &>/dev/null; then
  echo "Homebrew nicht installiert – Installation wird gestartet …"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
```

Nach der Installation prüfen:

```bash
brew --version
```

## 3. OpenCode installieren & Version prüfen

```bash
brew install opencode
opencode --version
```

## 4. Ollama installieren & Version prüfen

```bash
brew install ollama
ollama version
```

## 5. Ollama‑Server starten

Für die lokale Inferenz muss Ollama laufen. **Beachte**: Ollama lauscht standardmäßig nur auf `127.0.0.1`.

```bash
ollama serve &
```

Der Server startet im Hintergrund. Prüfe den Status:

```bash
ps -ef | grep ollama
```

## 6. GPT‑OSS 20B herunterladen

```bash
ollama pull gpt-oss:20b
```

Dies lädt das Modell aus dem Internet herunter. Nach dem Download ist die Inferenz **offline** möglich.

## 7. Ollama für 8192 Tokens, Flash Attention und Q8‑KV‑Cache konfigurieren

```bash
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KV_CACHE_TYPE=q8_0
export OLLAMA_CONTEXT_LENGTH=8192

# Dann Ollama neu starten, damit die Umgebungsvariablen gelten
killall ollama || true
ollama serve &
```

## 8. Modell lokal testen

```bash
ollama run gpt-oss:20b "Was ist der Zweck dieses Repositories?"
```

Du solltest eine Antwort vom Modell erhalten.

## 9. OpenCode mit Ollama verbinden

```bash
opencode launch opencode --model gpt-oss:20b
```

OpenCode startet die Agenten‑Umgebung und verbindet sich automatisch mit dem lokal laufenden Ollama‑Server.

## 10. OpenCode innerhalb eines Git‑Repos starten

```bash
mkdir my-agent-project && cd my-agent-project
# Git‑Repo initialisieren (oder vorhandenes Repo klonen)
git init

# OpenCode starten – hier ein Beispiel‑Agent verwenden
opencode start
```

## 11. GPU‑Nutzung & Kontext mit `ollama ps` prüfen

```bash
ollama ps
```

Die Ausgabe zeigt, ob das Modell auf der GPU ausgeführt wird, wie viel Speicher verbraucht wird und welche Kontexteinstellung aktiv ist.

## 12. Funktionsfähigkeit anhand eines kleinen Coding‑Agenten‑Tests validieren

```bash
# Beispiel: Git‑Repository initialisieren, .gitignore & README.md erstellen und Commit
opencode run-agent init-repo "Init"

# Prüfen, ob Dateien im Git‑Repository existieren
ls -l
```

Falls alles korrekt funktioniert, solltest du den initialen Commit sehen.

---

### Unterschied zwischen `ollama serve`, `ollama run` und `ollama launch opencode`

| Befehl | Zweck |
|--------|-------|
| `ollama serve` | Startet den Ollama‑Server, der als HTTP‑API-Modell‑Registry fungiert. |
| `ollama run <model>` | Führt eine einzelne Inferenz‑Anfrage an ein bestimmtes Modell aus (kann auch ohne Server laufen). |
| `ollama launch opencode` | Startet OpenCode als Agent und verbindet es automatisch mit dem laufenden Ollama‑Server. |
