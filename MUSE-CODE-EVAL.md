# Muse Code — Evaluation (2026-09-19)

**Recommendation: CONDITIONAL GO for a build machine — after Black's explicit approval of account creation + spend tier. NO blind install.**

## What it is
Meta Superintelligence Labs' terminal coding agent. Launched in beta 2026-08-05, graduated to stable 2026-08-31. No GUI — terminal only (TUI) plus headless `muse exec`.

## Capabilities (verified from public sources)
- Plans, edits, runs commands, and validates its own work across large repos.
- Parallel subagents in **isolated git worktrees** — the main working copy stays clean while agents experiment concurrently.
- **Crash-safe local event log**: every API call, tool execution, approval, and file change is logged before it runs; a session resumes exactly where it stopped after a crash.
- Built-in commands: `/plan` (approval-gated plan), `/grill` (stress-tests the plan), `/goal` (drives toward an objective).
- **Workflows** (stable): built-in orchestrator fanning large tasks into parallel subagents, live progress under `/workflows`, stop/restart/cancel/save.
- **Inter-session messaging**: parallel sessions pass messages over a local Unix socket.
- **Rewind**: double-Esc rewinds to an earlier safe checkpoint, with confirmation before reverting code.
- **SDK (developer preview)**: TypeScript library exposing session/tool/permission machinery over the open *Muse Session Protocol* — embeddable in our own tools.
- MCP support, hooks, skills; API-compatible with OpenAI/Anthropic SDKs (one-line provider switch).
- Model: Muse Spark 1.2 by default, 1,048,576-token context window.

Sources: https://www.neowin.net/news/meta-graduates-muse-code-out-of-beta-with-new-features/ · https://www.intelligentliving.co/meta-muse-code-claude-alternative/ · https://github.com/cooperativ-labs/overlord/blob/HEAD/planning/feature-plans/muse-code-harness-fit.md

## Requirements
- **macOS or Linux only** (works on WSL per third-party reports). No native Windows.
- Installer: `curl -fsSL https://dev.meta.ai/install.sh | bash` → drops a `muse` binary into `~/.local/bin/muse`.
- **Auth: a Meta Model API account is required** (browser OAuth or `META_API_KEY` env var). There is no usable free path — usage is metered.

## Cost model
- Metered via Meta Model API. Standard tier reported at **$1.25 / 1M input tokens, $4.25 / 1M output tokens** (same as Spark 1.2 API pricing).
- **WARNING — contributor tier:** some install reports indicate the default sign-in lands on Meta's discounted contributor tier (~$0.10/$0.20 per 1M), whose documented difference is that **prompts and completions are used to train Meta's products**. Do NOT accept this tier for any CWI proprietary code. Standard tier only. (Exact default tier at install time is UNVERIFIED — check before signing in.)

## Fit for the CWI app-factory build loop
- **Strong fit.** The shape matches how we already build: parallel subagent swarms, plan-before-build (`/plan` ≈ our Twenty Minds + brief), crash-safe logs (≈ our runbook/receipt doctrine), headless exec for CI.
- The isolated-worktree fan-out is exactly what our 2-apps-per-week factory wants: multiple builds in flight, no interference.
- The SDK (dev preview) could let us embed Muse Code's session machinery inside our own agent harness later.

## Risks
1. **Remote code execution**: `curl | bash` runs Meta's script unseen. Mitigation: download the script, read it fully, verify checksum/signature if published, then run — never pipe blind.
2. **Spend**: every agent loop meters tokens. An overnight multi-agent build can burn real money unattended. Mitigation: budget caps on the API account, standard tier only.
3. **Beta-adjacent surface**: third-party fit assessments note small docs-vs-binary disagreements (e.g. a documented `muse hooks` subcommand absent from the shipped binary). Treat the first integration as a spike, not production.
4. **Data posture**: code sent to the API leaves the machine. Proprietary catalog/tooling code only on the standard tier ("not used to improve our products").

## Go / no-go
- **GO**, conditionally: install on a Mac or Linux build machine **only after** Black explicitly approves (a) creating a Meta Model API account, (b) the standard (non-training) tier, and (c) a spend cap.
- **NO-GO** on: piping the installer blind, the contributor tier, and any install on a machine holding secrets without reviewing the script first.

## Activation checklist (for Black's yes/no)
1. [ ] Download `https://dev.meta.ai/install.sh`, read it end to end, verify it only installs the `muse` binary.
2. [ ] Create Meta Model API account (Black's action — account creation).
3. [ ] Select **standard tier**; confirm "not used to improve our products" on the pricing page.
4. [ ] Set a monthly spend cap on the account.
5. [ ] Run `muse --version` and one `/plan` spike on a scratch repo before pointing it at real CWI code.

**The single yes/no Black owes:** approve account creation + standard tier + spend cap for one build machine (recommend: his Mac or a Linux box, not this 7GB VM).
