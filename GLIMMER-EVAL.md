# Muse Glimmer — Verification + Mac Runbook + Smoke-Eval Protocol

**Agent:** CWI_Data (agent:CWI_Data) — research/eval worker
**Date verified:** 2026-09-19 (all facts from live web sources; nothing from memory)
**Run target:** Black's Mac (Apple Silicon, M-series, model TBD)
**Eval lane:** local open-weight agent brain for CWI

---

## 1. Verified model facts (live sources)

| Fact | Value | Source |
|---|---|---|
| Official repo ID | `meta-models/Muse-Glimmer-30B` | https://huggingface.co/meta-models/Muse-Glimmer-30B |
| Author | Meta Superintelligence Lab | HF model card (API-verified) |
| Release date | 2026-08-10 | Meta research blog; HF API `createdAt: 2026-08-09T17:54` (GGUF repo) |
| License | **Apache 2.0 — CONFIRMED** | HF API `license:apache-2.0` tag + `LICENSE` file present in repo (11,358 bytes, oid `d6456956…`) |
| Architecture | Dense causal LM, ~27.85B params (gguf metadata `total: 27854794240`), distilled from Muse Spark (logit distillation) | HF model card; Meta research blog |
| Context length | **131,072 tokens** (128K) | HF API `gguf.context_length: 131072` |
| Multimodal | Text + image **in**, text out. Dedicated perception encoder. Video = individual frames. No audio. | HF model card; Meta blog ("interleaved text and images", "interpret screenshots, charts, and documents") |
| Tool use | Native — chat template is "Muse Glimmer ATEM Chat Template" with tool-calling protocol (`to=self` reasoning channel, `to=<tool>` tool channels, tool definitions + valid-recipient list in system block) | HF API chat_template |
| Reasoning | Controllable reasoning strengths ("Reasoning strength: low/medium/high") | HF chat template |
| Quantized variants (official, `meta-models/Muse-Glimmer-30B-GGUF`) | See sizes below | HF file-tree API (2026-09-19) |
| Multilingual | 100+ languages | Meta research blog |
| Adoption signal | 97,043 downloads, 337 likes on the GGUF repo (2026-09-19) | HF API |
| Companion repos | `meta-models/Muse-Glimmer-30B-ExecuTorch-PTE` (pre-exported PTEs for CUDA sm80+ptx and Apple Silicon Metal, text-only and text+image, ±DFlash); `meta-models/Muse-Glimmer-30B-assistant` (DFlash drafter); community: `unsloth/Muse-Glimmer-30B-GGUF` (Q8_0 etc.) | HF search / model cards |

### Verified file sizes — official GGUF repo (from live HF file-tree API)

| File | Size (bytes) | Size (GiB) | Notes |
|---|---|---|---|
| `Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf` | 16,756,683,904 | ~15.6 | **Recommended build** — Meta's recommended configuration for most users |
| `Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf` | 19,653,960,832 | ~18.3 | Higher quality, needs 32GB envelope |
| `dflash-Muse-Glimmer-30B-Q4_K_M.gguf` | 1,631,208,128 | ~1.5 | DFlash speculative-decoding drafter |
| `mmproj-Muse-Glimmer-30B-Q4_K_M.gguf` | 1,400,328,928 | ~1.3 | Vision/perception encoder (image input) |
| `LICENSE` | 11,358 | — | Apache 2.0 — present ✓ |
| `USAGE_POLICY.md` | 5,230 | — | Separate Meta usage guidance — **review alongside the license** |

**Agentic capability claims (Meta, vendor-run — treat as directional until re-measured):** MCP-Atlas 75.5, DeepSearch QA 74.6, SWE-Bench strong; trained for failure recovery ("diagnoses the error and retries rather than halt"), multi-step planning, reliable schema-precise tool use.

**Canonical URLs:**
- Model: https://huggingface.co/meta-models/Muse-Glimmer-30B
- GGUF: https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF
- ExecuTorch PTE: https://huggingface.co/meta-models/Muse-Glimmer-30B-ExecuTorch-PTE
- Meta research blog: https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model
- Ollama release (v0.32.7, Glimmer support): https://github.com/ollama/ollama/releases/tag/v0.32.7

---

## 2. License confirmation

**YES — Apache 2.0 confirmed from two independent live checks (2026-09-19):**
1. HF models API returns `license:apache-2.0` tag and `cardData.license: "apache-2.0"` on `meta-models/Muse-Glimmer-30B-GGUF`.
2. A `LICENSE` blob (11,358 bytes) ships in the repo tree.
3. Meta's research blog states verbatim: *"open sourcing the model weights under a permissive Apache 2.0 license."*

Commercial use, modification, and redistribution are permitted under Apache 2.0. Caveat: the repo also ships `USAGE_POLICY.md` — separate Meta guidance to review; it is not a license restriction per the license terms, but read it before shipping a product.

---

## 3. Why the CWI VM cannot run it — local-lane kill

Measured on this VM (2026-09-19):
- **RAM:** 7 GB total, 0 swap (`free -g`)
- **GPU:** none — `/dev/dri` absent, no VGA/3D device
- **Root filesystem:** 7.5 GB total

The *smallest* recommended quantized weight file is **16.8 GB** (KQuant-17GB build); the Dynamic build is 19.7 GB. That exceeds the VM's entire disk, and loading it needs ~17 GB RAM before the KV cache, perception encoder, or DFlash drafter are even loaded.

**Kill rule (local VM lane): KILLED — physically impossible.** No rework cycle; the lane is dead by arithmetic (7 GB RAM vs ~17–20 GB weight footprint, zero GPU). All evaluation and execution move to Black's Mac (runbook below) or the separate API-staged lanes (separate mission, not this eval).

---

## 4. Mac runbook — verified simplest path: **Ollama (MLX engine)**

**Why Ollama:** it is the path Meta and Ollama both verified on launch day. Ollama v0.32.7 shipped first-party Muse Glimmer support via its MLX engine on Apple Silicon, including DFlash speculative decoding and image input ("state-of-the-art performance on Apple Silicon for this model" — ollama/ollama v0.32.7 release notes). One command, no manual weight management. Fallback: llama.cpp (see below).

### 4.1 Prerequisites
- Apple Silicon Mac (M-series). **24 GB unified memory minimum** (Meta FAQ: 24GB works — "M2 Pro and later, or M4 Max and M5 Max"; **32 GB** is the comfortable envelope for long-context agent loops). Below 16 GB: out of luck locally.
- Ollama **v0.32.7 or newer**. Check: `ollama --version`

### 4.2 Install

```bash
# Option A — Homebrew
brew install --cask ollama

# Option B — official download (from ollama/ollama v0.32.7 release notes)
# https://ollama.com/download
```

### 4.3 Run

```bash
# pulls the verified MLX variant and starts an interactive session
ollama run muse-glimmer:30b-mlx
```

That's the whole install. Agent-harness integrations (verified in the Ollama v0.32.7 release notes):

```bash
ollama launch claude --model muse-glimmer:30b-mlx   # Claude Code, local model backend
ollama launch pi    --model muse-glimmer:30b-mlx    # Pi — lightweight coding agent
ollama launch openclaw --model muse-glimmer:30b-mlx # OpenClaw long-running assistant
ollama launch hermes  --model muse-glimmer:30b-mlx  # Hermes personal assistant
```

Non-interactive / scripted (for the eval protocol):

```bash
echo "Your prompt" | ollama run muse-glimmer:30b-mlx
```

Ollama also exposes an OpenAI-compatible API at `http://localhost:11434` — useful for image+text and timing tests (see protocol test d/e).

### 4.4 Fallback path — llama.cpp with official GGUF

Verified facts: official GGUF conversions live at `meta-models/Muse-Glimmer-30B-GGUF`; **llama.cpp build `b10353` or newer is REQUIRED** (Glimmer support merged 2026-08-10, PR #26841). Older builds refuse the architecture.

```bash
./llama-cli --version   # build number must be >= 10353
# if building from source:
grep -c LLM_ARCH_MUSE_GLIMMER src/llama-arch.cpp   # expect >= 1

pip install huggingface_hub   # or: brew install huggingface-cli
huggingface-cli download meta-models/Muse-Glimmer-30B-GGUF \
  --include "Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf" \
  --local-dir ./glimmer
./llama-cli -m ./glimmer/Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf \
  -c 131072 -ngl 99 --temp 0.6 -p "You are a helpful assistant."
```

### 4.5 Expected footprints (estimates — see provenance)

- **Disk:** ~19 GB for the Ollama MLX package *(estimate — Ollama pulls a bundled MLX variant; Meta's underlying weights are 16.8 GB + drafter/encoder)*
- **RAM:** ~17–20 GB resident for weights + KV cache + perception encoder + DFlash drafter within a 24–32 GB envelope *(per Meta FAQ + TechTimes summary of Meta's quantization table)*
- **Throughput on Apple Silicon — third-party measured (mark as estimates, NOT Meta official):**
  - ~**24–28 tok/s**, 4-bit MLX on M4 Max, greedy batch-1 decode (independent 3-way bench 2026-08-15: Core AI 27.43, MLX 27.36, Meta ExecuTorch-Metal 24.00 — john-rocky/apple-silicon-llm-bench)
  - ~**18–26 tok/s**, 8-bit with DFlash speculative decode on M4 Pro (mlx-dspark, medians of 3)
  - ~**18 tok/s**, 8-bit on M-series Max (claude-code-local, MLX native)
  - ~**6–7 tok/s**, 4-bit plain MLX on a 24 GB Mac, no speculation (krill)
  - Meta's own numbers: RTX 5090 **74.9 → 233.4 tok/s** with DFlash (3.1×); Meta measured K-Quant-17GB + drafter on MacBook M4-Max/M5-Max but published no Mac tok/s figure in the blog
- **Practical Mac expectation (estimate): 15–30 tok/s** on an M4-class Mac with ≥24 GB unified memory at 4-bit, with DFlash engaged. Long prompts pay a prefill tax (~50 s to first token on a 4096-token prompt in plain MLX — krill).

---

## 5. Smoke-eval protocol — 5 measured tests (verbatim-runnable)

**Setup:** Ollama running, model pulled (`ollama run muse-glimmer:30b-mlx` once to warm). Run all tests against `http://localhost:11434` via the `/api/generate` endpoint for reproducible timing, or via `ollama run` pipes where noted. Set `"options": {"temperature": 0.2, "num_ctx": 8192}` for deterministic scoring. Record all outputs in `~/workspace/cwi-meta-models/glimmer-eval-results/` (create it).

### Test (a) — Multi-step planning
**What:** does the model sustain a coherent ≥5-step plan?

```bash
cat > /tmp/eval-a.txt <<'EOF'
You are a local agent. Plan and execute this task step by step, showing each step:
A user lands at 6pm with a dead phone battery, no charger, and needs (1) a
20-minute phone charge, (2) dinner within 10 min walk of 200 W 34th St, NYC,
(3) a cab to JFK by 9pm. Budget $80 total. Output numbered steps 1-7 with
costs and times, then a final total. Do not exceed the budget.
EOF
ollama run muse-glimmer:30b-mlx < /tmp/eval-a.txt > /tmp/eval-a.out
```
**Score:** count plan steps present; verify each cost/time is internally consistent; total ≤ $80 and covers all three needs.
**PASS:** ≥6 of 7 steps present AND all three needs addressed AND budget arithmetic correct. **FAIL:** otherwise.

### Test (b) — Tool/function-call accuracy
**What:** does it emit correct tool calls against a schema? Use the API with a tool definition and count exact matches.

```bash
curl -s http://localhost:11434/api/chat -d '{
  "model": "muse-glimmer:30b-mlx",
  "stream": false,
  "options": {"temperature": 0.0},
  "tools": [{"type": "function", "function": {"name": "get_weather",
    "description": "Get weather for a city",
    "parameters": {"type": "object", "properties": {
      "city": {"type": "string"}, "units": {"type": "string", "enum": ["celsius","fahrenheit"]}},
      "required": ["city"]}}}],
  "messages": [{"role": "user", "content":
    "What is the weather in Frederick MD in celsius? Then in fahrenheit?"}]
}' > /tmp/eval-b.json
```
**Score:** inspect `/tmp/eval-b.json` — expect 2 tool_calls, both `get_weather`, args `{"city":"Frederick MD","units":"celsius"}` then `"units":"fahrenheit"`. Repeat for 10 such 2-call prompts (20 calls total; vary city/units phrasing).
**PASS:** ≥18/20 calls correct function name AND valid JSON args AND all required params present (90%). **FAIL:** <18/20.

### Test (c) — Failure recovery
**What:** give it a failing tool, check it diagnoses and retries instead of halting.

```bash
curl -s http://localhost:11434/api/chat -d '{
  "model": "muse-glimmer:30b-mlx",
  "stream": false,
  "options": {"temperature": 0.2},
  "tools": [{"type": "function", "function": {"name": "read_file",
    "description": "Read a file from disk",
    "parameters": {"type": "object", "properties": {"path": {"type": "string"}},
      "required": ["path"]}}}],
  "messages": [
    {"role": "user", "content": "Read /tmp/does-not-exist-xyz.txt and summarize it."},
    {"role": "assistant", "tool_calls": [{"id": "1", "type": "function",
      "function": {"name": "read_file", "arguments": {"path": "/tmp/does-not-exist-xyz.txt"}}}]},
    {"role": "tool", "tool_call_id": "1", "name": "read_file",
      "content": "ERROR: FileNotFoundError: /tmp/does-not-exist-xyz.txt does not exist."},
    {"role": "user", "content": "The tool failed. What do you do next?"}
  ]
}' > /tmp/eval-c.json
```
**Score:** does the response (1) acknowledge the error, (2) propose a concrete alternative (ask for correct path / list directory / suggest fallback) rather than fabricating file contents or halting?
**PASS:** acknowledges error AND does not hallucinate file contents AND proposes ≥1 concrete next action. **FAIL:** fabricates contents or stalls with no action.

### Test (d) — Image + text input
**What:** multimodal — feed a chart/screenshot image + question. (Ollama MLX engine supports image input as of v0.32.7 — verified.)

```bash
# prepare: save any bar chart screenshot as /tmp/eval-chart.png (e.g. screenshot
# of the CWI 1M-streams tracker or any labeled chart with ≥4 data values)
python3 - <<'PY'
import base64, json, urllib.request
img = base64.b64encode(open('/tmp/eval-chart.png','rb').read()).decode()
req = urllib.request.Request('http://localhost:11434/api/generate',
  data=json.dumps({"model": "muse-glimmer:30b-mlx", "stream": False,
    "images": [img],
    "prompt": "Read the values off this chart. List each label with its exact numeric value, one per line."}).encode(),
  headers={'Content-Type': 'application/json'})
print(urllib.request.urlopen(req).read().decode()[:2000])
PY
```
**Score:** compare each listed label/value against ground truth from the source chart.
**PASS:** ≥80% of values correct within ±5%. **FAIL:** <80% or refuses image input (if it refuses, note "image path not functional on this build").

### Test (e) — Throughput
**What:** measure decode speed; confirm it clears a Mac-agentic floor.

```bash
python3 - <<'PY'
import json, time, urllib.request
body = {"model": "muse-glimmer:30b-mlx", "stream": True,
        "prompt": "Write a 200-word technical explanation of speculative decoding."}
t0 = time.time(); n = 0; first = None
req = urllib.request.Request('http://localhost:11434/api/generate',
  data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    for line in r:
        try: d = json.loads(line)
        except Exception: continue
        if d.get('response'):
            if first is None: first = time.time()
            n += len(d['response'].split())
if first: print(f"TTFT: {first-t0:.1f}s | tokens: ~{n} | decode: ~{n/(time.time()-first):.1f} tok/s")
PY
```
Run 3×, take the median.
**PASS:** median decode ≥ **15 tok/s** on M4-class (headroom below the independently measured 24–28 tok/s 4-bit figure; Meta's RTX-5090 numbers are not the bar here). **FAIL:** <15 tok/s median — file under "rework: try DFlash on/off, 3-bit requant, or 32GB machine before killing the lane."

**Overall lane verdict:** 4/5 PASS → lane proceeds. 3/5 → one rework cycle (change quantization/runtime), re-run. ≤2/5 → kill the Mac lane; report the failure table to Black.

---

## 6. Lane pick — #1 CWI lane: **KingCode Lens on-device agent brain**

**Pick: KingCode Lens (Meta Ray-Ban Display glasses) on-device agent brain — the "Hey KingCode" voice agent.**

Glimmer is the single best-fit open weight in the CWI stack for exactly this job, and the fit is architectural, not cosmetic:

1. **Built for the workload.** Glimmer is purpose-trained for always-on local agent loops — multi-step planning, schema-precise tool calls, and *failure recovery* (the capability every on-device agent dies without when a tool call fails mid-session). Those are Meta's own named training targets, verified in the model card.
2. **Sees what the glasses see.** The dedicated perception encoder (text+image in) maps directly onto a glasses camera feed: read a chart, a sign, a document in the wearer's view — interleaved with conversation. Text-out only is fine; the Lens simulator already handles rendering.
3. **Fits the device envelope.** 16.8 GB quantized + drafter + encoder inside a 24–32 GB envelope; runs on Apple Silicon today via Ollama's MLX engine at ~15–30 tok/s (third-party measured) — no cloud, no per-token bill, works offline/airgapped.
4. **License is product-safe.** Apache 2.0 allows commercial use, modification, and redistribution — none of the Llama-era restrictions that complicated downstream agent harnesses. (Review `USAGE_POLICY.md` before shipping.)
5. **Strategic alignment.** Glimmer is a *Meta* model and the Lens line targets *Meta* Ray-Ban hardware — the ecosystem gravity pulls the same direction (Ollama `launch` integrations for Claude Code/Pi/OpenClaw/Hermes show the agent-harness pattern is already proven). It also directly advances the Lens kill rule: real on-face speak → avatar answers-on-lens demo by 2026-10-30.

**Runner-up (not picked):** local build agent for the App Factory — `ollama launch claude --model muse-glimmer:30b-mlx` already makes Glimmer a coding-agent backend, and it's the fastest zero-cost win. But the App Factory lane doesn't need *Glimmer specifically* (any 30B coder works), while the Lens lane needs exactly Glimmer's agent+vision+local combination.

**Caution:** CWI product branding must not reuse the "Muse" name on hardware — it's Meta's own product family name (per standing trademark-screening rule).

---

## 7. Kill rules

| Lane | Rule | Status |
|---|---|---|
| Local VM execution | **KILLED 2026-09-19** — 7 GB RAM / no GPU vs 16.8–19.7 GB quantized weights. Arithmetic, no rework. | ⛔ dead |
| Mac runbook on Black's machine | Kill if `ollama run muse-glimmer:30b-mlx` fails to load on Ollama ≥0.32.7 / Apple Silicon, OR smoke-eval scores ≤2/5 after one rework cycle. 3/5 → rework (quant/runtime), re-run. 4/5 → proceed. | 🟡 pending Black's run |
| API-staged lanes (Together/Fireworks/OpenRouter hosted Glimmer) | **Separate mission** — not evaluated here. Hosted endpoints exist per press coverage; no verification performed in this eval. | ➡️ out of scope |
| Truth discipline | No benchmark number from this doc may be quoted to Black as "Glimmer does X" until re-measured on his Mac via protocol §5. Vendor numbers are vendor-run; third-party numbers are cited with sources. Faking a non-zero is the unforgivable failure. | standing |

---

*Verification log: HF models API + file-tree API (huggingface.co) — repo, license, files, sizes, context, chat template; Meta research blog (research.meta.ai) — release facts, training, capabilities; ollama/ollama v0.32.7 release notes — verified Mac path; third-party benches — mlx-dspark (M4 Pro ~18–26 tok/s), john-rocky/apple-silicon-llm-bench (M4 Max ~24–28 tok/s), krill (24GB Mac ~6–7 tok/s plain), claude-code-local (~18 tok/s). VM specs measured locally. No weights downloaded; no accounts created.*
