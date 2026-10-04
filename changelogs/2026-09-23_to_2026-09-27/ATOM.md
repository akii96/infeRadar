# ATOM: PR digest (2026-09-23 to 2026-09-27)

_28 merged, 26 newly opened - source ROCm/ATOM, generated 2026-09-28T00:12:57Z_

## TL;DR
- Most of the work targets DeepSeek-V4 ("v41"), Kimi-K3, MiniMax-M3 and GLM-5.2. The attention path got the most perf attention: the FP4 MQA indexer, MLA with DCP (decode context parallel), and the paged decode path.
- Merged perf work cuts host and scheduler overhead. Forward block tables are now sent as appends, metadata publication is unified, the loader prefetches under disable_mmap, and the graph's padded tail is folded into the deferred-id kernel.
- Quantization and MoE: Quark NVFP4 loading with online NVFP4→MXFP4 conversion landed ([#2292](https://github.com/ROCm/ATOM/pull/2292)). MoRI low-latency kernels are now reachable through the all2all manager, and a prefill-only mega combine wire is merged. Opened PRs extend mega stage1_fused to the fp4/fp8 dispatch wire and add gfx1250 MXFP8 ASM GEMMs.
- The in-progress work is Ulysses sequence parallelism, DPA with prefill TBO, pp>1 for Kimi-K3, and PD+DCP cache reordering. Alongside it is a heavy LMCache KV-offload hardening and CI/benchmark push.

## Most important PRs
**[#2399](https://github.com/ROCm/ATOM/pull/2399) – unify metadata publication and reuse page tables and Triton kernels**
This is the biggest merged change (+7.5k lines). It publishes metadata once and reuses page tables and Triton kernels across attention, MLA, DCP and speculative-decode paths, cutting per-step host work.

**[#2292](https://github.com/ROCm/ATOM/pull/2292) – Quark NVFP4 loading and online NVFP4→MXFP4 quantization**
It loads Quark-format NVFP4 checkpoints and converts them online to MXFP4. This enables MiniMax-M3 on the Triton MoE path, which suits MXFP4 hardware.

**[#2366](https://github.com/ROCm/ATOM/pull/2366) – route MiniMax-M3 paged decode to aiter's FlyDSL kernel**
Paged decode now goes through aiter's FlyDSL kernel with a work planner, so decode scheduling is planned per step rather than fixed.

**[#2290](https://github.com/ROCm/ATOM/pull/2290) – allow DCP query replication (QREP) with MTP**
It makes DCP query replication work with multi-token-prediction speculative decoding on MLA. This removes a blocker for combining DCP with MTP.

**[#2377](https://github.com/ROCm/ATOM/pull/2377) – page the index plane at the candidate block length (v41)**
The sparse-index plane is now paged at the candidate block length, with a Gluon kernel change. It is a DeepSeek-V4 attention-indexer efficiency gain, and [#2392](https://github.com/ROCm/ATOM/pull/2392) adds a related bound on block maxima by each row's context.

## More changes by area

<details>
<summary>Performance (7)</summary>

- [#2383](https://github.com/ROCm/ATOM/pull/2383) send forward block tables as appends instead of whole tables
- [#2398](https://github.com/ROCm/ATOM/pull/2398) loader prefetch under disable_mmap, one-copy reads, mmap in CI
- [#2368](https://github.com/ROCm/ATOM/pull/2368) fold the graph's padded tail into the deferred-id kernel
- [#2392](https://github.com/ROCm/ATOM/pull/2392) bound v41 candidate block maxima by each row's context
- [#2381](https://github.com/ROCm/ATOM/pull/2381) (open) reduce TP host-control overhead for C16
- [#2386](https://github.com/ROCm/ATOM/pull/2386) (open) split NUMA-bound CPUs into per-GPU physical-core groups
- [#2411](https://github.com/ROCm/ATOM/pull/2411) (open) adapt tuned AITER ASM FP8 decode for dsv4

</details>

<details>
<summary>Kernels & attention (4)</summary>

- [#2334](https://github.com/ROCm/ATOM/pull/2334) integrate gfx1250 FP4 MQA indexer
- [#2348](https://github.com/ROCm/ATOM/pull/2348) build FP4 indexer DCP prefill staging indices once per forward, in one launch
- [#2380](https://github.com/ROCm/ATOM/pull/2380) (open) unfused torch fallback for gather_kv_b_proj
- [#2371](https://github.com/ROCm/ATOM/pull/2371) (open, WIP) reorder MLA cache in P to the DCP layout in D

</details>

<details>
<summary>MoE & quantization (4)</summary>

- [#2228](https://github.com/ROCm/ATOM/pull/2228) reach MoRI's low-latency kernels through the all2all manager
- [#2347](https://github.com/ROCm/ATOM/pull/2347) prefill-only mega combine wire
- [#2384](https://github.com/ROCm/ATOM/pull/2384) (open) enable mega stage1_fused on fp4/fp8 dispatch wire
- [#2390](https://github.com/ROCm/ATOM/pull/2390) (open) opt-in gfx1250 MXFP8 ASM GEMMs for dsv4-ep4

</details>

<details>
<summary>Model support (7)</summary>

- [#2268](https://github.com/ROCm/ATOM/pull/2268) Kimi-K3 (hybrid) LMCache KV offload on the vLLM plugin path
- [#2131](https://github.com/ROCm/ATOM/pull/2131) Kimi-K3 AgentX recipe
- [#2382](https://github.com/ROCm/ATOM/pull/2382) Kimi-K3 AgentX recipe: FP8 prefill attention, PrefillDelayer from C16, capture from bs=1
- [#2373](https://github.com/ROCm/ATOM/pull/2373) enable TP2 DSpark for v41 and add AgentX recipe
- [#2385](https://github.com/ROCm/ATOM/pull/2385) (open) enable qwen3.8-flash MTP in SGL ATOM
- [#2365](https://github.com/ROCm/ATOM/pull/2365) (open) support pp>1 for Kimi-K3
- [#2410](https://github.com/ROCm/ATOM/pull/2410) (open) Qwen3.8-Flash-Next recipe on one MI350X

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#2331](https://github.com/ROCm/ATOM/pull/2331) transfer prefill prompt token ids to decode in PD
- [#2364](https://github.com/ROCm/ATOM/pull/2364) (open) Ulysses sequence parallelism and M3 prefill communication optimization
- [#2376](https://github.com/ROCm/ATOM/pull/2376) (open) v41 DPA and DPA prefill TBO with safe expert outputs
- [#2405](https://github.com/ROCm/ATOM/pull/2405) (open) MORI multi-node and MORI_V2
- [#2414](https://github.com/ROCm/ATOM/pull/2414) (open) add --kv-offload-config independent of --kv-transfer-config

</details>

<details>
<summary>API & serving (1)</summary>

- [#2396](https://github.com/ROCm/ATOM/pull/2396) select an optional AITER wheel for manual agentic runs

</details>

<details>
<summary>Bugfixes (11)</summary>

- [#2305](https://github.com/ROCm/ATOM/pull/2305) memoize external-tier lookup per HBM frontier
- [#2339](https://github.com/ROCm/ATOM/pull/2339) fence dense LMCache saves
- [#2400](https://github.com/ROCm/ATOM/pull/2400) prevent agentic FP8 tail faults and capture AITER wheel identity
- [#2378](https://github.com/ROCm/ATOM/pull/2378) pass merge_attn_states' prefill_tokens_with_context at runtime
- [#2369](https://github.com/ROCm/ATOM/pull/2369) (open) hold the deferred-save clock on the slotted SeqView
- [#2404](https://github.com/ROCm/ATOM/pull/2404) (open) distinguish unmeasured offload profile timings
- [#2406](https://github.com/ROCm/ATOM/pull/2406) (open) include exception type in dense lookup warnings
- [#2412](https://github.com/ROCm/ATOM/pull/2412) (open) reject invalid LMCache lookup scope at startup
- [#2367](https://github.com/ROCm/ATOM/pull/2367) (open) install the draft work plan when warming draft graphs
- [#2403](https://github.com/ROCm/ATOM/pull/2403) (open) store GDN temporal state in the checkpoint's mamba_ssm_dtype
- [#2402](https://github.com/ROCm/ATOM/pull/2402) (open) validate all LMCache Dockerfile pins before writing

</details>

<details>
<summary>CI & build (9)</summary>

- [#2387](https://github.com/ROCm/ATOM/pull/2387) capture CI artifacts and schedule agentic benchmark runs
- [#2346](https://github.com/ROCm/ATOM/pull/2346) weekly V4 no-offload benchmarks and manual GSM8K eval
- [#2395](https://github.com/ROCm/ATOM/pull/2395) ship LMCache wheels as Docker Hub images
- [#2388](https://github.com/ROCm/ATOM/pull/2388) build LMCache ROCm torch 2.10 wheels from any commit
- [#2372](https://github.com/ROCm/ATOM/pull/2372) check container model mount in atom test
- [#2389](https://github.com/ROCm/ATOM/pull/2389) (open) use --spec-decode-acceptance-length for GLM-5.2 agentic cases
- [#2370](https://github.com/ROCm/ATOM/pull/2370) (open) GLM-5.2 1P2D CPP4+DPA4 agentic suites
- [#2374](https://github.com/ROCm/ATOM/pull/2374) (open) avoid restarting tests on PR approval
- [#2375](https://github.com/ROCm/ATOM/pull/2375) (open, DO NOT MERGE) test CI approval orchestration

</details>

<details>
<summary>Docs (1)</summary>

- [#2407](https://github.com/ROCm/ATOM/pull/2407) (open) clarify LMCache MP lookup timeout scope

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: c5603416cbc798c6cdd1a787186392adda71f5d79d7f01e4ef7c7e838bf88297 -->
