#!/usr/bin/env python3
"""
Meta Muse Image — thin client scaffold (STAGED, NOT ACTIVATED).

Model: Muse Image — agentic image model. Plans each request, calls tools
(web search for factual accuracy), self-corrects and refines output. Text-
to-image, single/multi-image editing, multi-reference composition, recurring
character/location references — all through one model.
Model ID: ``muse-image-1.0`` on the Meta Model API (released 2026-08-26).

Verified pricing (checked 2026-09-19, see API-PRICING.md):
  $0.01 per generated image (1,000 outputs = $10)
  Caveat: real cost per *approved* asset is higher when reruns/alternatives
  are needed — self-correction loops bill each generation.
  Docs: https://ai.developer.meta.com/docs/getting-started/pricing-rate-limits

Endpoint shape: OpenAI-compatible image endpoint for generation/editing, plus
a Responses API for conversational workflows (per zeniteq.com). Exact path is
modeled on the OpenAI convention (/v1/images/generations) — CONFIRM against
Meta docs before first real call; --dry-run prints it for review.

CONTRIBUTOR-TIER WARNING: no contributor/data-training tier has been reported
for Muse Image. If Meta adds one, CWI policy is fixed: NEVER opt in — update
this file to refuse it before any activation.

Auth: API key read ONLY from the META_MODEL_API_KEY env var at call time.
No key is stored, written, or logged by this script. No key exists yet — key
creation requires Black's approval.

Usage:
  python3 muse_image.py --dry-run "album cover art, alt-rap, neon"  # prints request
  META_MODEL_API_KEY=... python3 muse_image.py "album cover art, alt-rap, neon" \
      --reference cover.png --out ./render.png
"""

import argparse
import base64
import json
import os
import sys
import urllib.request

BASE_URL = "https://api.meta.ai/v1"
# Modeled on the OpenAI-compatible convention per zeniteq.com's writeup;
# CONFIRM exact path in Meta's image docs before first live call.
IMAGES_GENERATE_PATH = "/images/generations"

MODEL_ID = "muse-image-1.0"

# --- contributor-tier block: never relax ---
# No contributor tier reported for this model. If one ever appears, the CWI
# rule is fixed: data-for-discount pricing is never acceptable.
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


def build_request(prompt: str, reference_paths: list | None = None) -> dict:
    _check_model_id(MODEL_ID)
    body = {"model": MODEL_ID, "prompt": prompt, "n": 1}
    refs = []
    for path in reference_paths or []:
        with open(path, "rb") as fh:
            refs.append(base64.b64encode(fh.read()).decode("ascii"))
    if refs:
        body["reference_images"] = refs
    return {
        "method": "POST",
        "url": BASE_URL + IMAGES_GENERATE_PATH,
        "headers": {"Content-Type": "application/json"},
        "body": body,
    }


def dry_run(prompt: str, reference_paths: list | None = None) -> None:
    req = build_request(prompt, reference_paths)
    print("=== DRY RUN — nothing is sent ===")
    print("NOTE: endpoint path is OpenAI-convention modeling — confirm in Meta docs.")
    print(f"METHOD  {req['method']}")
    print(f"URL     {req['url']}")
    print("HEADERS Authorization: Bearer <META_MODEL_API_KEY from env>")
    print(f"REFS    {reference_paths or []}")
    print("BODY    " + json.dumps(
        {k: ("<base64 bytes>" if k == "reference_images" else v)
         for k, v in req["body"].items()}, indent=2))
    print("ESTIMATE: $0.01 per generated image; reruns/alternatives bill separately.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Meta Muse Image client scaffold")
    ap.add_argument("prompt", help="image generation/edit prompt")
    ap.add_argument("--reference", action="append", default=[],
                    help="reference image path (repeatable)")
    ap.add_argument("--out", default="./muse_image_out.json",
                    help="where to write the JSON response")
    ap.add_argument("--dry-run", action="store_true", help="print request, send nothing")
    args = ap.parse_args()

    for path in args.reference:
        if not os.path.isfile(path):
            print(f"ERROR: not a file: {path}", file=sys.stderr)
            sys.exit(1)

    if args.dry_run:
        dry_run(args.prompt, args.reference)
        return

    api_key = _get_api_key()
    req = build_request(args.prompt, args.reference)
    body = json.dumps(req["body"]).encode("utf-8")
    http_req = urllib.request.Request(
        req["url"], data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + api_key},
    )
    with urllib.request.urlopen(http_req, timeout=300) as resp:
        payload = resp.read()
    with open(args.out, "wb") as fh:
        fh.write(payload)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
