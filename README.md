# mac-tts

A simple HTTP API server for macOS text-to-speech using the native `say` command.

## Installation

### Via Homebrew (recommended)

```bash
brew tap kalijason/tools
brew install mac-tts
brew services start mac-tts
```

### Manual

```bash
pip install flask
python mac_tts.py
```

## Usage

### Start the server

```bash
mac-tts                     # Default: port 5050, voice Meijia
mac-tts -p 8080             # Custom port
mac-tts -v Samantha         # Custom voice
```

### API Endpoints

#### POST /say
Trigger text-to-speech.

```bash
curl -X POST http://localhost:5050/say \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello world", "voice": "Meijia"}'
```

#### GET /health
Health check.

```bash
curl http://localhost:5050/health
# {"status": "ok"}
```

#### GET /voices
List available Chinese voices.

```bash
curl http://localhost:5050/voices
# {"voices": ["Meijia", "Sinji", ...]}
```

## Environment Variables

- `MAC_TTS_PORT` - Server port (default: 5050)
- `MAC_TTS_VOICE` - Default voice (default: Meijia)

## Integration with Home Assistant

Add to `configuration.yaml`:

```yaml
rest_command:
  mac_tts_say:
    url: "http://YOUR_MAC_IP:5050/say"
    method: POST
    content_type: "application/json"
    payload: '{"message": "{{ message }}", "voice": "{{ voice | default(''Meijia'') }}"}'
```

Then call in automations:

```yaml
action: rest_command.mac_tts_say
data:
  message: "外送已抵達"
```

## License

MIT
