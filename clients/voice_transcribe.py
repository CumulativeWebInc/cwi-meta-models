#!/usr/bin/env python3
"""
Meta Muse Voice Transcribe — thin client scaffold (STAGED, NOT ACTIVATED).

Model: Muse Voice Transcribe — streaming speech-to-text + speaker diarization
(20+ speakers) + turn/endpoint detection in a single model, 70+ languages
trained, 25 extensively validated at launch.
Model ID: ``muse-voice-transcribe-1.0`` on the Meta Model API.

Verified pricing (checked 2026-09-19, see API-PRICING.md):
  $3.00 / 1,000 audio-minutes  ==  ~$0.18 per hour of processed audio
  (streaming and file transcription billed at the same rate)
  Zero-data-retention service reportedly at pricing parity.
  Docs: https://ai.developer.meta.com/docs/getting-started/pricing-rate-limits
  Reported limits: 8 concurrent streams per tenant (default); real-time
  sessions up to 60 minutes before reconnect.

Endpoint shape (reported by third-party writeups; CONFIRM against Meta docs
before first real call):
  Batch file:   POST https://api.meta.ai/v1/asr/transcribe
  Realtime:     WSS  wss://api.meta.ai/v1/asr/realtime
  Both are marked UNCONFIRMED in this scaffold — --dry-run prints them for
  review only.

CONTRIBUTOR-TIER WARNING: at launch, NO contributor/data-training tier exists
for this model — standard audio pricing applies (source: therundown.ai,
2026-09-04). If Meta adds one later, the same rule holds: NEVER opt in, and
update this file to refuse it.

Auth: API key read ONLY from the META_MODEL_API_KEY env var at call time.
No key is stored, written, or logged by this script. No key exists yet — key
creation requires Black's approval.

Usage:
  python3 voice_transcribe.py --dry-run ./note.m4a   # prints request, sends nothing
  META_MODEL_API_KEY=... python3 voice_transcribe.py ./note.m4a
"""

import argparse
import base64
import json
import os
import sys
import urllib.request

BASE_URL = "https://api.meta.ai/v1"
# UNCONFIRMED endpoint paths (from tech-insider.org code block) — verify in
# Meta's ASR docs before any live call; --dry-run never sends.
ASR_TRANSCRIBE_PATH = "/asr/transcribe"   # batch file upload (multipart)
ASR_REALTIME_URL = "wss://api.meta.ai/v1/asr/realtime"  # streaming (not implemented)

MODEL_ID = "muse-voice-transcribe-1.0"

# --- contributor-tier block: never relax ---
# No contributor tier exists for this model at launch. If one ever appears,
# the CWI rule is fixed: data-for-discount pricing is never acceptable.
FORBIDDEN_MODEL_SUFFIXES = ("-contributor",)


def _get_api_key() -> str:
    key = os.environ.get("META_MODEL_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: META_MODEL_API_KEY is not set. It is read from the "
            "environment at call time and never stored by this script.",
            file=sys.stderr,
        )
        sys.exit(2)
    return key


def _check_model_id(model_id: str) -> None:
    for suffix in FORBIDDEN_MODEL_SUFFIXES:
        if model_id.endswith(suffix):
            print(
                f"REFUSED: '{model_id}' is a data-training tier. "
                "CWI standard policy: standard tier only. Aborting.",
                file=sys.stderr,
            )
            sys.exit(3)


def build_request(audio_path: str) -> dict:
    _check_model_id(MODEL_ID)
    with open(audio_path, "rb") as fh:
        audio_bytes = fh.read()
    return {
        "method": "POST",
        "url": BASE_URL + ASR_TRANSCRIBE_PATH,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "model": MODEL_ID,
            "audio": base64.b64encode(audio_bytes).decode("ascii"),
            "filename": os.path.basename(audio_path),
            "diarize": True,          # speaker diarization on
            "endpoint_detection": True,
        },
        "audio_bytes": len(audio_bytes),
    }


def dry_run(audio_path: str) -> None:
    req = build_request(audio_path)
    print("=== DRY RUN — nothing is sent ===")
    print("NOTE: endpoint path UNCONFIRMED — verify against Meta ASR docs first.")
    print(f"METHOD  {req['method']}")
    print(f"URL     {req['url']}")
    print("HEADERS Authorization: Bearer <META_MODEL_API_KEY from env>")
    print(f"FILE    {audio_path} ({req['audio_bytes']} bytes, base64 in body)")
    print("BODY    (audio bytes omitted) " + json.dumps(
        {k: v for k, v in req["body"].items() if k != "audio"}, indent=2))
    print("ESTIMATE: pricing is per audio-minute ($3/1,000 min), "
          "not per token — check file duration.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Meta Muse Voice Transcribe client scaffold")
    ap.add_argument("audio", help="audio file to transcribe")
    ap.add_argument("--dry-run", action="store_true", help="print request, send nothing")
    args = ap.parse_args()

    if not os.path.isfile(args.audio):
        print(f"ERROR: not a file: {args.audio}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        dry_run(args.audio)
        return

    api_key = _get_api_key()
    req = build_request(args.audio)
    body = json.dumps(req["body"]).encode("utf-8")
    http_req = urllib.request.Request(
        req["url"], data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + api_key},
    )
    with urllib.request.urlopen(http_req, timeout=600) as resp:
        print(resp.read().decode("utf-8"))


if __name__ == "__main__":
    main()
