#!/usr/bin/env bash
# run_synth.sh — key 추출(PowerShell) + ElevenLabs 합성 (voice-pool §0.6)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
KEY=$(powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')" | tr -d '\r\n')
if [ -z "$KEY" ]; then echo "ELEVENLABS_API_KEY missing"; exit 1; fi
export ELEVENLABS_API_KEY="$KEY"
export PYTHONIOENCODING=utf-8
echo "KEY_LEN=${#KEY}"
python "$HERE/synth.py" "$@"
