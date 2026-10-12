# ATOM: PR digest (2026-10-08 to 2026-10-12)

_19 merged, 25 newly opened - source ROCm/ATOM, generated 2026-10-12T00:58:26Z_

## TL;DR
- **DeepSeek-V4.1 and Kimi-K3 got the most attention.** Merged work covers FP4 indexer logits, a BF16 decode path, bounded-replay SWA and DSpark sampling. Kimi-K3 gained P/D disaggregation and a faster prefill gated RMSNorm. GLM-5.x and Qwen3.8 / Qwen3.5 also moved.
- **The main perf work is on the sparse-attention and indexer path.** [#2513](https://github.com/ROCm/ATOM/pull/2513) packs FP4 index logits, [#2512](https://github.com/ROCm/ATOM/pull/2512) shards DSpark Markov sampling over TP vocab, and [#2437](https://github.com/ROCm/ATOM/pull/2437) uses QREP for DCP sparse prefill. Open PRs add FlyDSL indexers, BLASST skipping in Triton prefill, and MegaMoE FP8/FP4 wires.
- **The vLLM plugin is a major thread.** [#2236](https://github.com/ROCm/ATOM/pull/2236) upgraded it to vLLM 0.31.0 and merged. Several open PRs bring DSv4.1 to the plugin: model support ([#2494](https://github.com/ROCm/ATOM/pull/2494)), prefix-state restore ([#2503](https://github.com/ROCm/ATOM/pull/2503)), and cudagraph and indexer fixes ([#2502](https://github.com/ROCm/ATOM/pull/2502), [#2501](https://github.com/ROCm/ATOM/pull/2501)).
- **Direction: disaggregated serving, long-context state caching, and AMD kernel stacks.** The work centers on P/D, DCP, ATOMesh CI, and aiter/FlyDSL, plus gfx950, gfx1250 and MI308X targets.

## Most important PRs
**[#2513](https://github.com/ROCm/ATOM/pull/2513) perf(deepseek_v41): packed FP4 index logits and a two-source BF16 decode**
Packs the FP4 sparse-indexer logits and splits BF16 decode into two KV sources. This cuts indexer and decode cost for DSv4.1, and it touches 50 files across attention, quantization and speculative decode.

**[#2332](https://github.com/ROCm/ATOM/pull/2332) feat(kimi-k3): support P/D disaggregation (re-land of #2154)**
Re-lands prefill/decode disaggregation for Kimi-K3, with MLA and attention changes and distributed KV transfer. It is the base for the ATOMesh 2P1D and aggregated CI cells in [#2528](https://github.com/ROCm/ATOM/pull/2528).

**[#2236](https://github.com/ROCm/ATOM/pull/2236) plugin/vllm: upgrade the ATOM vLLM plugin to 0.31.0**
Moves the plugin to vLLM 0.31.0, adapting attention and MLA integration. The rest of the plugin work builds on it.

**[#2507](https://github.com/ROCm/ATOM/pull/2507) feat(v41): decoder SWA bounded replay for prefill**
Adds `--enable-decoder-swa-bounded-replay`, which limits how much sliding-window state is replayed during prefill. Open PR [#2521](https://github.com/ROCm/ATOM/pull/2521) trims the last KV-source layer further.

**[#2418](https://github.com/ROCm/ATOM/pull/2418) perf(qwen4_exp): MI308X optimizations for Qwen3.8-Flash-Next**
Tunes Qwen3.8-Flash-Next on MI308X for both native ATOM and SGLang-ATOM. Open PRs [#2529](https://github.com/ROCm/ATOM/pull/2529) (FlyDSL HC and QSA index CP) and [#2517](https://github.com/ROCm/ATOM/pull/2517) (rtpllm bridge) continue the Qwen3.8 work.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#2458](https://github.com/ROCm/ATOM/pull/2458) optimizes the Kimi-K3 prefill gated RMSNorm pipeline
- [#2512](https://github.com/ROCm/ATOM/pull/2512) samples the DSpark Markov block off the TP vocab shard (merged)
- [#2521](https://github.com/ROCm/ATOM/pull/2521) (open) bounded replay trims the last KV-source layer
- [#2520](https://github.com/ROCm/ATOM/pull/2520) (open) Qwen3.5 decode: fusion, removes copybuffer, optimizes `_replayssm_fwd_kernel`

</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#2437](https://github.com/ROCm/ATOM/pull/2437) DCP sparse prefill uses QREP, removing AllGather of Q and a copy (merged)
- [#2496](https://github.com/ROCm/ATOM/pull/2496) (open) DCP local indexer prefill
- [#2493](https://github.com/ROCm/ATOM/pull/2493) (open) MiniMax-M3 lightning indexer scored with aiter FlyDSL kernels
- [#2492](https://github.com/ROCm/ATOM/pull/2492) (open) MiniMax-M3 mono tensor library with borrowed weights for vLLM
- [#2511](https://github.com/ROCm/ATOM/pull/2511) (open) BLASST block skipping in the Triton prefill path
- [#2514](https://github.com/ROCm/ATOM/pull/2514) (open) adapts FlyDSL paged decode to aiter explicit work plans
- [#2506](https://github.com/ROCm/ATOM/pull/2506) (open) GLM-5.2 uses non-persistent MLA at prefill and drops the MLA metadata build
- [#2510](https://github.com/ROCm/ATOM/pull/2510) (open) Gluon mhc_post_pre for GFX12

</details>

<details>
<summary>MoE & quantization (3)</summary>

- [#2499](https://github.com/ROCm/ATOM/pull/2499) (open) balances MegaMoE prefill with MoonEP
- [#2522](https://github.com/ROCm/ATOM/pull/2522) (open) MegaMoE FlyDSL dispatch with FP8/FP4 wires
- [#2505](https://github.com/ROCm/ATOM/pull/2505) (open) mxfp4 dispatches explicit scale layouts

</details>

<details>
<summary>Model support (7)</summary>

- [#2494](https://github.com/ROCm/ATOM/pull/2494) (open) DeepSeek-V4.1-Flash on the vLLM plugin backend
- [#2503](https://github.com/ROCm/ATOM/pull/2503) (open) DSv4 restores prefix-hit state from checkpoint images in vLLM blocks
- [#2516](https://github.com/ROCm/ATOM/pull/2516) (open) K3 caches prefill checkpoints in spare STATE slots
- [#2517](https://github.com/ROCm/ATOM/pull/2517) (open) rtpllm Qwen3.8 Qwen4Exp plugin bridge
- [#2519](https://github.com/ROCm/ATOM/pull/2519) (open) LMCache enabled for Qwen3.5
- [#2529](https://github.com/ROCm/ATOM/pull/2529) (open) Qwen3.8 FlyDSL HC and long-context QSA index CP
- [#2490](https://github.com/ROCm/ATOM/pull/2490) (open) gfx1250 MLA absorb emits ql_nope in the FP8 KV-cache dtype

</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

- [#2509](https://github.com/ROCm/ATOM/pull/2509) (open) enables MoRI-io connector write mode and fixes spurious issues

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#2500](https://github.com/ROCm/ATOM/pull/2500) (open) system-level roofline tool with per-operator drill-down, targeting gfx950

</details>

<details>
<summary>Bugfixes (8)</summary>

- [#2495](https://github.com/ROCm/ATOM/pull/2495) fixes the FP4 sparse indexer output contract
- [#2451](https://github.com/ROCm/ATOM/pull/2451) GLM5-next MTP verify always writes sparse KV indices, and kpool tail uses the history ring layout
- [#2518](https://github.com/ROCm/ATOM/pull/2518) fixes leaked LMCache MP L1 read locks from an unconsumed async lookup
- [#2498](https://github.com/ROCm/ATOM/pull/2498) fixes the 1P1D nightly: forces RDMA KV transfer, sets the EAGLE3 draft path, moves the InferenceX bench
- [#2524](https://github.com/ROCm/ATOM/pull/2524) escapes literal % in argparse help for Python 3.14
- [#2526](https://github.com/ROCm/ATOM/pull/2526) restores the `--state-checkpoint-demand` help text mangled by [#2524](https://github.com/ROCm/ATOM/pull/2524)
- [#2502](https://github.com/ROCm/ATOM/pull/2502) (open) corrects DSv4 plugin output under the default cudagraph config
- [#2501](https://github.com/ROCm/ATOM/pull/2501) (open) scores 1-token prefill rows on the dense indexer path in the DSv4 plugin

</details>

<details>
<summary>CI & build (6)</summary>

- [#2528](https://github.com/ROCm/ATOM/pull/2528) ATOMesh aggregated-service CI, AgentX runtime fixes, Kimi-K3 2P1D/agg cells
- [#2433](https://github.com/ROCm/ATOM/pull/2433) ATOMesh GLM-5.2 cpp4/dcp4 c56+ cases with per-stage LMCache lookup and keep-alive
- [#2330](https://github.com/ROCm/ATOM/pull/2330) pins the SGLang ATOM image transformers to 5.16.1
- [#2515](https://github.com/ROCm/ATOM/pull/2515) removes Kimi-K2.5 tests
- [#2508](https://github.com/ROCm/ATOM/pull/2508) (open) adds GLM-5.2-MXFP4 2P1D TP8 ATOMesh coverage
- [#2497](https://github.com/ROCm/ATOM/pull/2497) (open) DO NOT MERGE: re-tests CI approval orchestration

</details>

<details>
<summary>Docs (1)</summary>

- [#2504](https://github.com/ROCm/ATOM/pull/2504) DeepSeek v4 PD recipe update

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 31452dae7cf3bc75fc03fd401255a9efc872ef3f8f31d8df5ad9f0b02b008059 -->
