#!/usr/bin/env python3
"""
Meta SAM 3.1 — thin client scaffold (STAGED, PRICING UNVERIFIED).

Model: SAM 3.1 — video/object detection, segmentation and tracking. Object
Multiplex: up to 16 objects processed in a single pass (~7x faster than SAM 3
at 128 objects on a single H100 per Meta's tests). Text-prompted detection +
segmentation + tracking; up to 16 objects tracked per frame on the hosted API.

PRICING STATUS: UNVERIFIED at official level (2026-09-19). A single
third-party aggregation chain (BlockBeats via KuCoin news, ~11h old) reports
Meta Model API hosting at:
  Image segmentation: $2.5 / 1,000 images ($0.0025/image)
  Video segmentation:  $0.2 / 1,000 frames
The official Meta pricing page could not be fetched during research — recheck
https://ai.developer.meta.com/docs/getting-started/pricing-rate-limits before
any activation. Until then this lane stays STAGED ONLY, never presented as
costed.

FREE PATH EXISTS: SAM 3.1 is ALSO open-weights (facebookresearch/sam3,
sam3.1_multiplex.pt ~3.5 GB, SAM License) — self-hosting on a GPU (16GB+ VRAM
recommended) costs $0 in API fees. For CWI video-studio use, self-hosted may
dominate the hosted API once a GPU is available.

Endpoint shape: reported as hosted via OpenAI SDK with text prompts (exact
path NOT published by any source found). The constant below is a PLACEHOLDER —
do not use against a real API until Meta documents it. --dry-run only.

CONTRIBUTOR-TIER WARNING: no contributor/data-training tier reported. CWI
policy is fixed: NEVER opt in.

Auth: API key read ONLY from the META_MODEL_API_KEY env var at call time.
No key is stored, written, or logged by this script. No key exists yet.

Usage:
  python3 sam31.py --dry-run ./clip.mp4 "the rapper on stage"
"""

import argparse
import json
import os
import sys
import urllib.request

BASE_URL = "https://api.meta.ai/v1"
# PLACEHOLDER — exact Meta Model API path for SAM 3.1 was not published by any
# source found. DO NOT call against this; wait for Meta docs.
SAM_SEGMENT_PATH = "/sam/segment"  # UNCONFIRMED PLACEHOLDER

MODEL_ID = "sam-3.1"

# --- contributor-tier block: never relax ---
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


def build_request(video_path: str, text_prompt: str) -> dict:
    _check_model_id(MODEL_ID)
    return {
        "method": "POST",
        "url": BASE_URL + SAM_SEGMENT_PATH,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "model": MODEL_ID,
            "video_path": os.path.basename(video_path),
            "text_prompt": text_prompt,
            "max_tracked_objects": 16,
            # NOTE: hosted API accepts text prompts only (per BlockBeats);
            # box/point visual prompts are open-weights-only for now.
        },
    }


def dry_run(video_path: str, text_prompt: str) -> None:
    req = build_request(video_path, text_prompt)
    print("=== DRY RUN — nothing is sent ===")
    print("WARNING: endpoint path is a PLACEHOLDER — never call it until Meta "
          "documents the real path. Pricing UNVERIFIED.")
    print(f"METHOD  {req['method']}")
    print(f"URL     {req['url']}")
    print("HEADERS Authorization: Bearer <META_MODEL_API_KEY from env>")
    print("BODY    " + json.dumps(req["body"], indent=2))
    print("ESTIMATE: unverified — reported $0.2/1,000 frames (unconfirmed); "
          "self-hosted open weights cost $0 in API fees.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Meta SAM 3.1 client scaffold (staged)")
    ap.add_argument("video", help="video file to segment/track")
    ap.add_argument("prompt", help="text prompt describing the object to track")
    ap.add_argument("--dry-run", action="store_true", help="print request, send nothing")
    args = ap.parse_args()

    if not os.path.isfile(args.video):
        print(f"ERROR: not a file: {args.video}", file=sys.stderr)
        sys.exit(1)

    print("NOTICE: SAM 3.1 hosted-API pricing and endpoint are UNVERIFIED. "
          "Live calls stay disabled until Meta's docs confirm them.")
    if args.dry_run:
        dry_run(args.video, args.prompt)
        return

    print("REFUSED: live SAM 3.1 calls are blocked pending official pricing/"
          "endpoint confirmation. This is a staging scaffold only.",
          file=sys.stderr)
    sys.exit(4)


if __name__ == "__main__":
    main()
