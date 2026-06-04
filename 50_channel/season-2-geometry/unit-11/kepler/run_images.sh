#!/usr/bin/env bash
# run_images.sh — key 추출(PowerShell) + Nano Banana 이미지 생성
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
KEY=$(powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')" | tr -d '\r\n')
if [ -z "$KEY" ]; then echo "GEMINI_API_KEY missing"; exit 1; fi
export GEMINI_API_KEY="$KEY"
export PYTHONIOENCODING=utf-8
echo "KEY_LEN=${#KEY}"
python "$HERE/gen_images.py" "$@"
