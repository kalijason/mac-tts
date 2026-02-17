#!/usr/bin/env python3
"""
Mac TTS API - HTTP server for macOS text-to-speech
Receives HTTP POST requests and triggers macOS `say` command
"""

import subprocess
import os
import argparse
from flask import Flask, request, jsonify

app = Flask(__name__)

DEFAULT_VOICE = os.environ.get("MAC_TTS_VOICE", "Meijia")
DEFAULT_PORT = int(os.environ.get("MAC_TTS_PORT", "5050"))


@app.route("/say", methods=["POST"])
def say():
    """
    Trigger TTS notification
    
    POST /say {"message": "Hello", "voice": "Meijia"}
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    voice = data.get("voice", DEFAULT_VOICE)

    if not message:
        return jsonify({"error": 'Missing "message" parameter'}), 400

    try:
        result = subprocess.run(
            ["say", "-v", voice, message],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return jsonify({"success": True, "message": message, "voice": voice})
        else:
            return jsonify({"success": False, "error": result.stderr}), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Speech timeout"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


@app.route("/voices", methods=["GET"])
def voices():
    """List available Chinese voices"""
    try:
        result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
        chinese_voices = [
            line.split()[0]
            for line in result.stdout.strip().split("\n")
            if "zh_TW" in line or "zh_CN" in line
        ]
        return jsonify({"voices": chinese_voices})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    parser = argparse.ArgumentParser(description="Mac TTS HTTP API Server")
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT, help="Port to listen on")
    parser.add_argument("-v", "--voice", default=DEFAULT_VOICE, help="Default voice")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    args = parser.parse_args()

    global DEFAULT_VOICE
    DEFAULT_VOICE = args.voice

    print(f"🔊 Mac TTS API starting on http://{args.host}:{args.port}")
    print(f"   Default voice: {DEFAULT_VOICE}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
