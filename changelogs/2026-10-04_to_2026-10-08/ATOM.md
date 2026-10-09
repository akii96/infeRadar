# ATOM: PR digest (2026-10-04 to 2026-10-08)

_15 merged, 20 newly opened - source ROCm/ATOM, generated 2026-10-08T16:44:59Z_

## TL;DR
- **DeepSeek-V4 got the most model-specific attention**, with a tuned ASM FP8 decode and HCA on aiter's persistent V4-NM kernel ([#2462](https://github.com/ROCm/ATOM/pull/2462)) and a decode block-table fix ([#2488](https://github.com/ROCm/ATOM/pull/2488)). A DeepSeek-V4.1-Flash vLLM plugin ([#2494](https://github.com/ROCm/ATOM/pull/2494)) and GLM-5.3-Flash with LMCache offload ([#2481](https://github.com/ROCm/ATOM/pull/2481)) are open.
- **Largest merge is [#2479](https://github.com/ROCm/ATOM/pull/2479)**, a 177-file "mono" decode framework with an FP4 index plane. MiniMax-M3 mono follow-ups ([#2483](https://github.com/ROCm/ATOM/pull/2483), [#2485](https://github.com/ROCm/ATOM/pull/2485)) merged, and [#2492](https://github.com/ROCm/ATOM/pull/2492) and [#2493](https://github.com/ROCm/ATOM/pull/2493) are open.
- **MoE perf work centers on MegaMoE and MoRI.** [#2463](https://github.com/ROCm/ATOM/pull/2463) merged DP pad-row masking and configurable decode capacity. [#2474](https://github.com/ROCm/ATOM/pull/2474) and [#2499](https://github.com/ROCm/ATOM/pull/2499) (MoonEP prefill balancing) are open.
- **Attention is moving to DCP.** [#2437](https://github.com/ROCm/ATOM/pull/2437) merged sparse prefill using QREP, and [#2496](https://github.com/ROCm/ATOM/pull/2496) (local indexer prefill) is open. On gfx1250, three MLA-absorb PRs ([#2486](https://github.com/ROCm/ATOM/pull/2486), [#2489](https://github.com/ROCm/ATOM/pull/2489), [#2490](https://github.com/ROCm/ATOM/pull/2490)) cover BF16 and FP8 variants.
- **Direction:** next-gen DeepSeek and MiniMax decode kernels, MoE/EP robustness (EPLB), and operability knobs such as shutdown timeout, logging and stats.

## Most important PRs
**[#2479](https://github.com/ROCm/ATOM/pull/2479) feat(v41): mono decode, FP4 index plane, shared mono framework**
Adds a shared "mono" decode framework with an FP4 index plane for the sparse indexer. It touches aiter, triton, MLA, MoE and quantization paths, and it underpins the MiniMax-M3 and DSV4.1 work.

**[#2462](https://github.com/ROCm/ATOM/pull/2462) [DSV4] Tuned ASM FP8 decode with split plans; HCA on aiter's persistent V4-NM kernel**
Adds tuned ASM FP8 decode with split plans for DeepSeek-V4. The HCA path now runs on aiter's persistent V4-NM kernel, which targets decode latency.

**[#2463](https://github.com/ROCm/ATOM/pull/2463) [Perf] MegaMoE: DP pad-row masking and configurable decode capacity**
Masks padded DP rows in MegaMoE so they do no expert work, and makes decode capacity configurable. This cuts wasted compute and dispatch traffic under data-parallel padding.

**[#2437](https://github.com/ROCm/ATOM/pull/2437) [DCP] sparse prefill use QREP, removing AllGather Q and copy**
Sparse prefill under decode context parallelism now uses a replicated Q. This removes an AllGather and a copy from the MLA prefill path.

**[#2494](https://github.com/ROCm/ATOM/pull/2494) feat(plugin): DeepSeek-V4.1-Flash on the vLLM plugin backend (open)**
A large in-progress PR (33 files) bringing DeepSeek-V4.1-Flash to the vLLM plugin, with attention changes and tests.

## More changes by area

<details>
<summary>Performance (2)</summary>

- [#2474](https://github.com/ROCm/ATOM/pull/2474) open: MoRI v2 fused transport masks DP pad rows via ATOM_MEGA_MASK_PAD_ROWS
- [#2499](https://github.com/ROCm/ATOM/pull/2499) open: MoonEP balances MegaMoE prefill

</details>

<details>
<summary>Kernels & attention (6)</summary>

- [#2493](https://github.com/ROCm/ATOM/pull/2493) open: score the MiniMax-M3 lightning indexer with aiter FlyDSL kernels
- [#2492](https://github.com/ROCm/ATOM/pull/2492) open: expose the mono tensor library with borrowed weights for vLLM (MiniMax-M3)
- [#2496](https://github.com/ROCm/ATOM/pull/2496) open: DCP local indexer prefill
- [#2490](https://github.com/ROCm/ATOM/pull/2490) open: gfx1250 MLA absorb emits ql_nope in the fp8 KV-cache dtype
- [#2486](https://github.com/ROCm/ATOM/pull/2486) open: gfx1250 ATOM_MLA_ABSORB_A16W8 (BF16 activation x FP8 weight)
- [#2489](https://github.com/ROCm/ATOM/pull/2489) open: gfx1250 ATOM_MLA_ABSORB_BF16 keeps absorb weights in BF16

</details>

<details>
<summary>MoE & quantization (3)</summary>

- [#2461](https://github.com/ROCm/ATOM/pull/2461) merged: EPLB skips MoE layers outside the placement map (DSpark drafter)
- [#2467](https://github.com/ROCm/ATOM/pull/2467) open: wire DeepSeek-R1 MoE layer ids into EPLB
- [#2466](https://github.com/ROCm/ATOM/pull/2466) open: preserve gfx1250 MXFP4 scale layouts for Kimi-K3

</details>

<details>
<summary>Model support (2)</summary>

- [#2426](https://github.com/ROCm/ATOM/pull/2426) merged: keep Qwen3.8 Flash full-attn, EP and MTP working on SGLang 0.5.20
- [#2481](https://github.com/ROCm/ATOM/pull/2481) open: GLM-5.3-Flash on ATOM-vLLM with LMCache offload

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#2482](https://github.com/ROCm/ATOM/pull/2482) merged: ATOM_EPLB_MAX_REBALANCES stops rebalancing after N rebalances
- [#2469](https://github.com/ROCm/ATOM/pull/2469) open: scheduler reserves KV for projected decode growth
- [#2475](https://github.com/ROCm/ATOM/pull/2475) merged: ATOM_SHUTDOWN_TIMEOUT_S sets the wait before terminating child processes

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#2500](https://github.com/ROCm/ATOM/pull/2500) open: system-level roofline tool with per-operator drill-down (gfx950)

</details>

<details>
<summary>API & serving (2)</summary>

- [#2471](https://github.com/ROCm/ATOM/pull/2471) open: decode-step engine stats for observability
- [#2470](https://github.com/ROCm/ATOM/pull/2470) open: isolate the atom logger and support ATOM_LOG_LEVEL

</details>

<details>
<summary>CI & build (6)</summary>

- [#2433](https://github.com/ROCm/ATOM/pull/2433) merged: atomesh GLM-5.2 cpp4/dcp4 cases with per-stage LMCache lookup and keep-alive
- [#2480](https://github.com/ROCm/ATOM/pull/2480) merged: locate the Pre Checkin run by commit; add concurrency 1 to the benchmark grid
- [#2330](https://github.com/ROCm/ATOM/pull/2330) merged: pin the SGLang ATOM image transformers to 5.16.1
- [#2478](https://github.com/ROCm/ATOM/pull/2478) merged: install requests for the non-GPU unit tests
- [#2498](https://github.com/ROCm/ATOM/pull/2498) open: force RDMA KV transfer for single-node 1P1D atomesh cells
- [#2497](https://github.com/ROCm/ATOM/pull/2497) open, DO NOT MERGE: re-test CI approval orchestration

</details>

<details>
<summary>Bugfixes (5)</summary>

- [#2483](https://github.com/ROCm/ATOM/pull/2483) merged: zero the mono mailboxes and fence ranks in one FlyDSL launch
- [#2485](https://github.com/ROCm/ATOM/pull/2485) merged: MiniMax-M3 mono rows independent of other rows; pad rows join no expert
- [#2488](https://github.com/ROCm/ATOM/pull/2488) merged: DSV4 publishes decode block tables at the padded running_bs
- [#2495](https://github.com/ROCm/ATOM/pull/2495) open: fix the FP4 sparse indexer output contract
- [#2477](https://github.com/ROCm/ATOM/pull/2477) open: stop long RL runs falling back to eager after ~40 sleep/wake cycles

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 64ec67b425c2378439579b4706eb3f53257f81d8a34199aa0be99116528b2b24 -->
