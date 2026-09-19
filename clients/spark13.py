#!/usr/bin/env python3
"""
Meta Muse Spark 1.3 — thin client scaffold (STAGED, NOT ACTIVATED).

Model: Muse Spark 1.3 — flagship coding/agentic model, 1,048,576-token context.
Model ID: ``muse-spark-1.3`` on the Meta Model API.
Base URL: https://api.meta.ai/v1   (OpenAI SDK-compatible; also speaks
Anthropic Messages format per Meta's developer blog)

Verified pricing — STANDARD tier (checked 2026-09-19, see API-PRICING.md):
  Input:  $1.25 / 1M tokens
  Output: $4.25 / 1M tokens   (reasoning tokens bill as output)
  Cached input read: $0.15 / 1M tokens
  Web-search grounding: billed separately when used (~$2.50 / 1,000 queries
  per third-party breakdowns — confirm in docs before use)
  Docs: https://ai.developer.meta.com/docs/getting-started/pricing-rate-limits
  Rate limits (reported): standard tier ~3,000 RPM / 4M TPM; US-only during
  public preview. New developer accounts reportedly start with $20 in free
  credits before pay-as-you-go billing.

CONTRIBUTOR-TIER WARNING: Meta offers a discounted "contributor" endpoint
(model id ``muse-spark-1.3-contributor``: $0.10 in / $0.20 out per 1M) whose
price is paid for in TRAINING DATA — prompts and completions may be used to
train future Meta models. Black's standing order: NEVER use it. This client
refuses any ``-contributor`` model identifier. Standard tier keeps prompts
private.

Auth: API key read ONLY from the META_MODEL_API_KEY env var at call time.
No key is stored, written, or logged by this script. No key exists yet — the
API key must be created by Black in the Meta developer console.

Usage:
  python3 spark13.py --dry-run "Summarize this repo"   # prints the request, sends nothing
  META_MODEL_API_KEY=... python3 spark13.py "Summarize this repo"
"""

import argparse
import json
import os
import sys
import urllib.request

BASE_URL = "https://api.meta.ai/v1"
CHAT_PATH = "/chat/completions"
MODEL_ID = "muse-spark-1.3"

# --- contributor-tier block: never relax ---
# The contributor tier ($0.10/$0.20 per 1M) lets Meta train on prompts and
# completions. CWI does not opt into training-data pricing. Any attempt to
# use a contributor model id is a hard error.
CONTRIBUTOR_SUFFIX = "-contributor"


def _get_api_key() -> str:
    key = os.environ.get("META_MODEL_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: META_MODEL_API_KEY is not set. Create the key in the Meta "
            "developer console (Black's approval required); it is read from the "
            "environment at call time and never stored by this script.",
            file=sys.stderr,
        )
        sys.exit(2)
    return key


def _check_model_id(model_id: str) -> None:
    if model_id.endswith(CONTRIBUTOR_SUFFIX):
        print(
            f"REFUSED: '{model_id}' is the contributor/data-training tier. "
            "CWI standard policy: standard tier only. Aborting.",
            file=sys.stderr,
        )
        sys.exit(3)


def build_request(prompt: str, model_id: str = MODEL_ID) -> dict:
    _check_model_id(model_id)
    return {
        "method": "POST",
        "url": BASE_URL + CHAT_PATH,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            # reasoning_effort: minimal|low|medium|high|xhigh (max in partner preview)
            "reasoning_effort": "high",
        },
    }


def dry_run(prompt: str) -> None:
    req = build_request(prompt)
    print("=== DRY RUN — nothing is sent ===")
    print(f"METHOD  {req['method']}")
    print(f"URL     {req['url']}")
    print("HEADERS Authorization: Bearer <META_MODEL_API_KEY from env>")
    print("BODY    " + json.dumps(req["body"], indent=2))
    print("ESTIMATE: ~$" + "%.4f" % (len(prompt.split()) * 1.33 / 1e6 * 1.25),
          "(input tokens approximated at 1.33x word count)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Meta Muse Spark 1.3 client scaffold")
    ap.add_argument("prompt", help="user prompt to send")
    ap.add_argument("--dry-run", action="store_true", help="print request, send nothing")
    args = ap.parse_args()

    if args.dry_run:
        dry_run(args.prompt)
        return

    api_key = _get_api_key()
    req = build_request(args.prompt)
    body = json.dumps(req["body"]).encode("utf-8")
    http_req = urllib.request.Request(
        req["url"], data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + api_key},
    )
    with urllib.request.urlopen(http_req, timeout=300) as resp:
        print(resp.read().decode("utf-8"))


if __name__ == "__main__":
    main()
