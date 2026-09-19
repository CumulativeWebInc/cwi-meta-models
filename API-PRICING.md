# Meta Model API — CWI Staging Reference

**Status: STAGED, NOT ACTIVATED. $0 spent. No API keys created, no accounts,
no test calls that spend. Activation needs Black's explicit word per lane.**

Research date: 2026-09-19. Recheck before any activation — Meta's pricing page
is the authority: https://ai.developer.meta.com/docs/getting-started/pricing-rate-limits

## Auth (all paid models)

- Key: Meta Model API key, created in the Meta developer console by **Black**.
- Env var: `META_MODEL_API_KEY`, read at call time only; never stored, logged,
  or committed. The four client scaffolds exit with an error if it is unset.
- Transport: `Authorization: Bearer <key>` against `https://api.meta.ai/v1`.
  The API is OpenAI SDK-compatible (chat + Anthropic Messages format also
  supported per Meta's developer blog). US-only during public preview.
- Accounts reportedly start with $20 in free credits before pay-as-you-go
  billing begins (Meta launch announcement, via Reuters 2026-07-09).

## Per-model pricing (standard tier)

| Model | Model ID | Unit | Standard price | Verified? | Source |
|---|---|---|---|---|---|
| Muse Spark 1.3 | `muse-spark-1.3` | 1M tokens in / out | **$1.25 / $4.25** (+$0.15 cached-in) | Yes (multi-source) | Reuters 2026-09-03: https://www.reuters.com/business/meta-debuts-muse-spark-11-with-preview-open-developers-2026-07-09/ · techrepublic 2026-09-04: https://www.techrepublic.com/article/news-meta-muse-spark-1-3-ai-coding-2026/ · docs: https://ai.developer.meta.com/docs/getting-started/pricing-rate-limits |
| Muse Voice Transcribe | `muse-voice-transcribe-1.0` | 1,000 audio-minutes | **$3.00 (≈$0.18/hr)** | Yes (multi-source) | 9to5Mac 2026-09-01: https://9to5mac.com/2026/09/01/meta-launches-muse-voice-transcribe-for-real-time-voice-dictation-on-mac/ · VentureBeat: https://venturebeat.com/technology/meta-prices-muse-voice-transcribe-at-0-18-an-hour-with-real-time-diarization-for-20-speakers-a-steal-for-enterprises |
| Muse Image | `muse-image-1.0` | generated image | **$0.01** | Yes (multi-source) | fal/unite.ai 2026-09-01: https://www.unite.ai/metas-agentic-muse-image-model-lands-on-fal-for-developers/ · zeniteq: https://www.zeniteq.com/meta-muse-image-api-adds-agentic-ai-for-0-01-vv3ybd · OpenRouter: https://openrouter.ai/meta/muse-image |
| SAM 3.1 (hosted) | `sam-3.1` | 1,000 images / 1,000 frames | reported $2.50 / $0.20 | **UNVERIFIED** | Single aggregation chain (BlockBeats via KuCoin, ~2026-09-19): https://www.kucoin.com/news/flash/meta-launches-sam-3-1-api-for-image-and-video-segmentation |

Reported rate limits (third-party; confirm in docs): Spark standard ~3,000
RPM / 4M TPM, contributor 100 RPM; Voice 8 concurrent streams per tenant,
60-minute max real-time sessions; 1,048,576-token context on Spark 1.3
(943,718 max output).

## ⚠️ CONTRIBUTOR-TIER WARNING (standard tier only)

Meta's **contributor tier** (`muse-spark-1.3-contributor`: $0.10 in / $0.20 out
per 1M; cached-in $0.002) is dramatically cheaper **because Meta may use
prompts and completions to train future Meta models** — the discount is paid
in data. Black's standing order: **NEVER use or recommend it.** Every scaffold
in `clients/` hard-refuses any `-contributor` model id. Activation plans use
the standard tier exclusively (kept private, not used for training).

- Voice Transcribe: no contributor tier exists at launch.
- Muse Image / SAM 3.1: no contributor tier reported; the same refusal is
  coded into their scaffolds proactively.

## Cost gates — what Black must approve per lane

### 1. Muse Spark 1.3 → heavy cloud agent work / app-factory builds
Approve: Meta Model API key creation (standard tier only) + a **$25/month hard
spend cap**. Usage assumption: ~10 agent sessions/month, each ~400K input +
150K output tokens (one 2x/week app-factory build cadence). Estimated:
4M in × $1.25 + 1.5M out × $4.25 ≈ **$11.38/month**. Gate: auto-pause if the
cap is approached; contributor endpoint (`-contributor`) permanently banned.

### 2. Muse Voice Transcribe → iOS voice-note transcription + interview/podcast transcription
Approve: key creation + standard audio tier + **$5/month hard cap**.
Assumption: 40 voice notes/month × 3 min = 120 audio-minutes. Estimated:
120/1,000 × $3 = **$0.36/month**. Zero-data-retention service reportedly at
pricing parity — use it where eligible. Gate: cap tripwire at $5.

### 3. Muse Image → cover art / IG tiles / NFT art direction
Approve: key creation + standard tier + **$5/month hard cap**. Assumption:
32 generations/month (12 IG mosaic tiles + 20 art-direction concepts).
Estimated: 32 × $0.01 = **$0.32/month**. Note: reruns/alternatives bill
separately, so agentic self-correction loops must be budgeted per asset.

### 4. SAM 3.1 → video segmentation for the video studio / 3D world
**BLOCKED: pricing UNVERIFIED at official level** — staged only, never
presented as costed. The only published number is a single third-party
aggregation ($2.5/1,000 images, $0.2/1,000 frames). A 10-minute clip at 30fps
(18,000 frames) would cost ~$3.60 at the reported rate, but that figure is NOT
confirmed. Parallel zero-cost path: SAM 3.1 is open-weights
(`facebookresearch/sam3`, ~3.5 GB, SAM License) — self-hosting on a 16GB+ VRAM
GPU costs $0 in API fees and is the likely winner for sustained video-studio
work.

## The four yes/no questions for Black

1. **Spark 1.3:** Activate with a $25/month hard cap (standard tier only) for
   app-factory/agentic builds? — **YES / NO**
2. **Voice Transcribe:** Activate with a $5/month hard cap for the voice-note
   transcription lane? — **YES / NO**
3. **Muse Image:** Activate with a $5/month hard cap for the art lane? —
   **YES / NO**
4. **SAM 3.1:** Hold as staged-only (pricing unverified)? Nothing to approve
   until the official pricing page confirms numbers — **NO ACTION / INVESTIGATE
   SELF-HOSTED PATH**
