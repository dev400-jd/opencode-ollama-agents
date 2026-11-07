# Troubleshooting‑Liste

Im Folgenden findest du bekannte Probleme, typische Fehlermeldungen und Lösungen für die lokale OpenCode‑Ollama‑Umgebung auf macOS.

## 1. `Unable to find application named Ollama`

**Ursache**: Ollama ist nicht im Systempfad oder wurde nicht korrekt installiert.
**Lösung**:
```bash
brew install ollama
export PATH="$PATH:/opt/homebrew/bin"
```

## 2. `could not connect to a running Ollama instance`

**Ursache**: Der Ollama‑Server ist nicht gestartet oder lauscht nicht auf `127.0.0.1:11434`.
**Lösung**:
```bash
ollama serve
# oder prüfen, ob der Prozess läuft
ps aux | grep ollama
```

## 3. Ollama‑Server startet nicht

- Prüfe Log‑Ausgaben: `ollama serve & tail -f ollama.log`
- Stelle sicher, dass keine andere Instanz den Port 11434 nutzt.
- Lösche ggf. die Ollama‑Cache‑Dateien: *Vollständiger Reset löscht Modelle und Konfiguration, für gewöhnliche Verbindungs‑ oder Modellprobleme nicht empfohlen.*

## 4. Port 11434 bereits belegt

```bash
lsof -i :11434
# ggf. Prozess beenden
kill -9 <PID>
```

## 5. OpenCode erkennt das Modell nicht

- Prüfe, ob das Modell im Verzeichnis `~/.ollama/models` vorhanden ist.
- Starte Ollama neu: `killall ollama && ollama serve`
- In OpenCode: `ollama launch opencode --model gpt-oss:20b`

## 6. Metal‑Out‑of‑Memory‑Fehler

- Modellgröße + KV‑Cache überschreitet die verfügbare GPU‑RAM.
- Reduziere `OLLAMA_CONTEXT_LENGTH` auf 8192 oder weniger.
- Schalte Flash‑Attention aus: `export OLLAMA_FLASH_ATTENTION=0`.
- Verwende ein Modell mit kleinerer Quantisierung.

## 7. Zu großes Kontextfenster

- Der Fehler tritt auf, wenn `OLLAMA_CONTEXT_LENGTH` zu hoch gesetzt wurde.
- Setze das Limit zurück: `export OLLAMA_CONTEXT_LENGTH=8192` und starte Ollama neu.

## 8. Modell läuft nicht vollständig auf der GPU

- Prüfe die Ausgabe von `ollama ps`: GPU‑Flag sollte `true` sein.
- Bei Problemen den `llama.cpp`‑Back‑end‑Build neu konfigurieren: `--metal`.

## 9. Unterschied zwischen MLX und llama.cpp

- **llama.cpp** nutzt Metal (GPU) und ist in C++.
- **MLX** (Apple ML framework) ist Python‑basiert und nutzt ebenfalls GPU.
- In diesem Setup bevorzugen wir **llama.cpp** wegen seiner stabilen Metal‑Implementierung.

## 10. Qwen3.8‑27B (NVFP4) Erfahrungen

- Modellgröße ~18 GB (NVFP4).
- MLX‑Backend liefert ~30,7 Tokens/s bei kurzen Benchmarks.
- Bei längeren Agentenläufen treten regelmäßig Metal‑OOM‑Fehler auf.
- Wir empfehlen, zunächst GPT‑OSS 20B zu verwenden und bei Bedarf Qwen3.8 zu testen, sobald mehr Unified Memory verfügbar ist.

---

### Nächste Schritte

- **Hardware‑Upgrade**: Mehr Unified Memory (32 GB) reduziert GPU‑Memory‑Engpässe.
- **Kontextfenster erhöhen**: Nach Hardware‑Upgrade kann `OLLAMA_CONTEXT_LENGTH` auf 16384 oder 32768 angepasst werden.
- **Monitoring**: Verwende `ollama ps` und `top` zur laufenden Beobachtung von GPU‑ und RAM‑Verbrauch.
