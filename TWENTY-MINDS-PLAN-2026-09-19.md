# Twenty Minds — Meta models integration plan (2026-09-19)

Decision: "Do we integrate Meta's models as (A) Glimmer-local-first with API models staged, or (B) skip local and stage everything behind future API keys?"

Facts (max 5):
1. Only Muse Glimmer is $0/free — Apache 2.0 open weights (30B, quantized <20GB), released 2026-08-10 on Hugging Face; every other Meta model needs a paid Meta Model API key.
2. This VM has 7GB RAM and no GPU — it cannot hold or run Glimmer's ~20GB quantized weights; Black's Mac is the only verified local run target.
3. Hard lines: no spending, no API keys created, no accounts, and no "contributor"/discount tier that trains on our data — that needs Black's explicit word.
4. Muse Code is a beta terminal agent installed via `curl -fsSL https://dev.meta.ai/install.sh | bash` (macOS/Linux) — needs evaluation before any install.
5. CWI lanes ready to receive: KingCode Lens on-device agent brain (needs local), app-factory build loop, voice-note transcription pipeline, cover-art/NFT art direction, video studio segmentation.

### Verdicts (one sentence + one risk each)
1. Skeptic — Go with (A) because the "free" claim for API models is marketing fiction — the moment a key exists, spend exists, and nobody bills $0 forever.
   Risk: Glimmer-on-Mac may never actually run if Black never sits down to install it, making (A) a plan that dies on his desk.
2. Data scientist — Go with (A); Glimmer is the only lane with a verifiable $0 cost function and a measurable smoke eval, while API lanes carry cost per token with no spend data.
   Risk: we have no Mac hardware data — throughput and stability on his machine are unverified until he runs the runbook.
3. User advocate — Go with (A); Black said "if they are free add them all" and the free one is the only one he can touch today without opening his wallet.
   Risk: staging four API models he can't use yet may read as inventory without results — the thing his "no zeros" law punishes.
4. Contrarian — Go with (B); a runbook for a machine we can't test is a hope document, and staged API scaffolds at least compile into something shippable when the keys come.
   Risk: (B) normalizes paying Meta later, and the contributor-tier discount is a trap that monetizes our code as training data.
5. Engineer — Go with (A); thin API scaffolds are trivial to build and Glimmer's Mac runbook is a bounded, testable artifact, while (B) couples us to an API we can't even smoke-test.
   Risk: the scaffolds rot without a key — an untested client is a rumor of integration, not an integration.
6. Economist — Go with (A); Glimmer's marginal cost is exactly zero forever, while API models compound per-token spend on every agent loop we automate.
   Risk: Glimmer's capability-per-dollar is unverified — a weak local model burns the most expensive resource, Black's time.
7. Security reviewer — Go with (A); local Glimmer keeps code, voice, and catalog data on-device, while API routes ship our material to Meta's pipes.
   Risk: the curl|bash installer for Muse Code is a remote-code-execution vector if we don't pin and verify it first.
8. Child-of-five explainer — Go with (A): "the free one works on your computer, the others cost money later."
   Risk: a five-year-old would also ask why the free one isn't running yet, and we don't have a good answer.
9. 10-year historian — Go with (A); in 2036 the record shows whether CWI owned its intelligence locally, not whether it staged four API clients.
   Risk: historians romanticize local-first and forget the years Glimmer-class models lagged the frontier on hard tasks.
10. Devil's accountant — Go with (A); true cost of (B) is spend + key management + data exposure, while (A)'s cost is one Mac install afternoon.
    Risk: that "one afternoon" has no owner yet — unowned costs are the ones that never get paid.
11. Field operator — Go with (A); I can verify Glimmer's Hugging Face page, license, and footprint from here, but I can't verify a single API claim without a key.
    Risk: my Tuesday becomes runbook support for Black's Mac — an interrupt-driven lane with no kill rule on my time.
12. Systems thinker — Go with (A); a local always-on agent becomes infrastructure every other lane can call for free, while API lanes add per-call latency and cost to every loop.
    Risk: the free local lane becomes the bottleneck everything queues on, and we never priced its throughput.
13. Risk underwriter — Go with (A); the tail risk in (B) is an API bill or a training-data leak via the contributor tier, while (A)'s worst case is a wasted afternoon.
    Risk: underwriting only downside misses the upside tail — Spark 1.3 on the app factory might 10x build velocity, which we'd never learn staged.
14. Open-source maintainer — Go with (A); Apache 2.0 Glimmer is forkable, auditable, and documentable for strangers, while API scaffolds are vendor docs with extra steps.
    Risk: our repo documenting Meta's pricing could go stale — vendor facts rot faster than code.
15. Negotiator — Go with (A); owning the local lane gives us walk-away leverage — we never *need* Meta's API, so we negotiate usage from strength.
    Risk: leverage we never exercise is theater; Meta knows a staged scaffold is one key away from spend.
16. Time traveler (2036) — Go with (A); looking back, the local-first agents were the move — the API bills were the trap everyone else fell into.
    Risk: nostalgia bias — the traveler remembers the philosophy, not the quarter Glimmer couldn't debug a real repo.
17. First-principles physicist — Go with (A); what must be true is that compute we own costs nothing marginal and compute we rent meters everything — the physics favors local.
    Risk: physics also says a 30B model on a laptop is not a frontier model — capability is bounded by the same physics.
18. Ethicist — Go with (A); contributor tiers that train on a label's code and catalog without clear consent are extractive, and our stance should be explicit refusal by default.
    Risk: moral clarity can masquerade as strategy — refusing the cheap tier on principle doesn't make Glimmer good enough.
19. Competitor analyst — Go with (A); competitors will all be API-metered, so a $0 local agent fleet is the one lane they can't price-match.
    Risk: the lane they can't price-match is also the lane where Meta open-sourced the model to commoditize everyone, including us.
20. Black's chair — Go with (A); results only, $0 path first, verify before asserting — Glimmer runs locally for free, API models wait for his key and his word, nothing ships as a simulation.
    Risk: his "add them all" order meets my "no spending" law — the staging work must never read as pressure to buy.

### Synthesis
- Decision: (A) — Glimmer-local-first with verified Mac runbook, four API models staged as zero-dep client scaffolds with standard-tier-only activation plans, Muse Code evaluated (no blind install).
- Why: the economist's zero marginal cost forever, the security reviewer's on-device data posture, and Black's chair's $0-first, verify-before-asserting read converged — the free lane is real and the paid lanes are honestly staged, not faked.
- Dissent recorded: the contrarian's strongest minority — an untested runbook on a machine we can't reach is a hope document, and staged API scaffolds rot without keys; mitigate by making the runbook executable verbatim and the scaffolds importable/testable without a key.
- Confidence: medium — the single fact that would change it: Glimmer's measured throughput and agent-task quality on Black's actual Mac (unknown until he runs the runbook).
- Changed the pre-run lean? no — the lean was already (A) from Black's "if they are free add them all"; this is the first run on this decision stream.
