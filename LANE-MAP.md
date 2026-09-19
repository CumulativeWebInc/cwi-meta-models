# CWI × Meta Models — Lane Map (2026-09-19)

Black's order: "If they are free add them all." Only one Meta model is free. Everything else is staged, never activated without his word.

## Status board

| Model | Status | CWI lane | Cost |
|---|---|---|---|
| **Muse Glimmer** (30B, Apache 2.0, Hugging Face) | **LIVE — local lane** (Mac runbook verified; VM lane killed by arithmetic) | #1: KingCode Lens on-device agent brain ("Hey KingCode"). Runner-up: App Factory local build agent | **$0** — no API, no account, offline |
| **Muse Spark 1.3** (`muse-spark-1.3`) | **STAGED** — client scaffold ready, no key, no calls | Heavy cloud agent work / app-factory builds | $1.25/$4.25 per 1M in/out (standard tier, verified) |
| **Muse Voice Transcribe** (`muse-voice-transcribe-1.0`) | **STAGED** — client scaffold ready, no key, no calls | iOS voice-note transcription pipeline; interview/podcast transcription | $3.00/1,000 audio-minutes ≈ $0.18/hr (verified) |
| **Muse Image** (`muse-image-1.0`) | **STAGED** — client scaffold ready, no key, no calls | Cover art / IG mosaic tiles / NFT art direction | $0.01/image (verified) |
| **SAM 3.1** (hosted video segmentation) | **STAGED-BUT-FLAGGED** — live calls hard-blocked in scaffold pending official pricing | Video studio segmentation / 3D world | **UNVERIFIED** — do not present as costed |
| **Muse Code** (terminal agent) | **EVALUATED** — conditional GO, not installed | App-factory build machine (Mac/Linux) | Metered API; needs account + spend cap |

## What is live right now
- Glimmer's verified Mac runbook: `ollama run muse-glimmer:30b-mlx` (Ollama ≥0.32.7, MLX engine, Apple Silicon). Weights: `meta-models/Muse-Glimmer-30B` (+ official GGUF quants, ExecuTorch PTE). Apache 2.0 confirmed (LICENSE blob + HF tag). Mac floor: 24GB unified memory (32GB comfortable); 16.8GB smallest quant. Full details + 5-test smoke-eval protocol in `GLIMMER-EVAL.md`.
- Four staged API clients in `clients/`: stdlib-only, key from env at call time, `--dry-run` verified, contributor tier refused in code.

## Cost gates — the yes/no Black owes
1. **Spark 1.3**: activate with $25/mo hard cap (~$11.38/mo at 10 sessions/month assumption)? — YES / NO
2. **Voice Transcribe**: activate with $5/mo cap (~$0.36/mo at 40 voice-notes/month assumption)? — YES / NO
3. **Muse Image**: activate with $5/mo cap (~$0.32/mo at 32 images/month assumption)? — YES / NO
4. **SAM 3.1**: NO ACTION — staged only; recommend the free self-hosted open-weights path (`facebookresearch/sam3`, ~3.5GB, SAM License) in parallel.
5. **Muse Code**: approve account creation + standard tier + spend cap for one build machine? — YES / NO (see `MUSE-CODE-EVAL.md` checklist)

## Standing warnings (do not relax)
- **Contributor tier is never the answer by default**: the discounted Spark tier ($0.10/$0.20 per 1M) trains Meta's products on our prompts/completions. Standard tier only. Scaffolds refuse contributor model IDs in code.
- **No blind installs**: `curl | bash` for Muse Code only after the installer script is downloaded, read, and verified.
- **"Muse" name**: do not put Meta's "Muse" brand on CWI hardware/products (trademark caution, same class as the Glassface kill).

## Kill rules
- Glimmer local lane: kill if `ollama run muse-glimmer:30b-mlx` fails on Black's Mac (Ollama ≥0.32.7), or smoke-eval ≤2/5 after one rework cycle.
- Any staged API model: stays staged (never auto-activates). SAM 3.1 stays blocked until official pricing is verified.
- Muse Code: kill the lane if Black declines the account/spend approval — no workarounds, no free-tier games.

Repo: https://github.com/CumulativeWebInc/cwi-meta-models · Docs: `GLIMMER-EVAL.md`, `API-PRICING.md`, `MUSE-CODE-EVAL.md`, `TWENTY-MINDS-PLAN-2026-09-19.md`, `clients/`.
