# ATOM: PR digest (2026-08-23 to 2026-08-27)

_28 merged, 41 newly opened - source ROCm/ATOM, generated 2026-08-27T20:09:30Z_

## TL;DR
- **Models & Direction:** DeepSeek (V4) and GLM (5.2/5.3) dominated model-specific work, alongside new support for Kimi-K3, Qwen3.8, and MiniMax-H3/M3. The overarching focus this cycle is heavily scaling Distributed Context Parallelism (DCP) and Multi-Head Latent Attention (MLA) for massive-context workloads.
- **Performance & Attention:** Significant kernel wins landed, including a new CPP-prefill to DCP-decode KV transfer planner, persistent sparse MLA DCP for GLM-5.2, and FP8 block attention routed through the target's ASM decode kernel.
- **Speculative Decoding:** Speculative decoding saw major latency improvements by warming draft forwards at target-captured batch sizes and integrating DSpark speculative decoding under DCP.
- **MoE & Quantization:** MoE and quantization advanced with newly opened Gluon MoE Expert/Tensor Parallelism backends, SwiGLU activation for Triton MoE on GFX1250, and merged Qwen3.5 block-FP8 correctness fixes.
- **Memory Architecture:** Massive in-progress memory shifts include a new paged state cache, a state checkpoint superblock, and LMCache offloading for Kimi-K3 to handle extreme memory pressure.

## Most important PRs
- **[#1836](https://github.com/ROCm/ATOM/pull/1836)** Merged a massive 11k-line diffusion subsystem, expanding the engine beyond text to support MiniMax-H3 video and audio generation.
- **[#2053](https://github.com/ROCm/ATOM/pull/2053)** Opened a 10k-line integration for LMCache offloading on Kimi-K3, a critical architectural shift for managing memory pressure in massive-context deployments.
- **[#2042](https://github.com/ROCm/ATOM/pull/2042)** Merged a major speculative decoding performance win that warms every draft forward at the exact batch size the target captured, optimizing AITER and Triton kernel utilization.
- **[#2008](https://github.com/ROCm/ATOM/pull/2008)** Opened a core architectural feature for distributed context, introducing a KV transfer planner that bridges CPP-prefill and DCP-decode phases.
- **[#2001](https://github.com/ROCm/ATOM/pull/2001)** Merged a critical optimization for Distributed Context Parallelism (DCP) scaling, adding query replication, project-before-merge, and an all-to-all merge backend.

## More changes by area

<details>
<summary>Performance (10)</summary>

- [#1989](https://github.com/ROCm/ATOM/pull/1989) cuts host work between two forwards for v4
- [#2016](https://github.com/ROCm/ATOM/pull/2016) adds session-aware routing and post-prefill decode protection for DPA
- [#1858](https://github.com/ROCm/ATOM/pull/1858) skips kvcache tensor allocation for shared indexer KV
- [#1991](https://github.com/ROCm/ATOM/pull/1991) stops the collector from walking a heap it never reclaims
- [#2020](https://github.com/ROCm/ATOM/pull/2020) prevents merge_chunk from rebuilding the whole backlog on every merge
- [#1980](https://github.com/ROCm/ATOM/pull/1980) raises GC thresholds in the EngineCore and ModelRunner
- [#1911](https://github.com/ROCm/ATOM/pull/1911) takes the MLA decode KV-split budget from the machine instead of a hardcoded limit
- [#2050](https://github.com/ROCm/ATOM/pull/2050) reduces memory pressure raised by multiple comm groups initialization
- [#2019](https://github.com/ROCm/ATOM/pull/2019) reduces memory pressure raised by multiple comm groups initialization
- [#2039](https://github.com/ROCm/ATOM/pull/2039) syncs forward metadata over device groups for DPA
</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#2026](https://github.com/ROCm/ATOM/pull/2026) merges a reconstruction piecewise core with a piecewise attention compressor
- [#2009](https://github.com/ROCm/ATOM/pull/2009) implements FP8 block attention through the target's ASM decode kernel
- [#2003](https://github.com/ROCm/ATOM/pull/2003) replaces `tl.make_block_ptr` with plain pointer arithmetic for Triton 3.8 compatibility
- [#2055](https://github.com/ROCm/ATOM/pull/2055) fuses DCP indexer small ops and fixes non-persistent paths
- [#2015](https://github.com/ROCm/ATOM/pull/2015) optimizes the attention residual for Kimi-K3
- [#2033](https://github.com/ROCm/ATOM/pull/2033) supports DSpark speculative decoding under DCP for vLLM K3
- [#2011](https://github.com/ROCm/ATOM/pull/2011) integrates the AITER MK1 persistent decoder
- [#2023](https://github.com/ROCm/ATOM/pull/2023) optionally runs sparse MLA on AITER's Gluon kernel
</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#1985](https://github.com/ROCm/ATOM/pull/1985) fixes Qwen3.5 block-FP8 correctness under vLLM full CUDA graphs
- [#2047](https://github.com/ROCm/ATOM/pull/2047) implements a Gluon MoE Expert Parallelism (EP) backend
- [#2046](https://github.com/ROCm/ATOM/pull/2046) implements a Gluon MoE Tensor Parallelism (TP) backend
- [#2028](https://github.com/ROCm/ATOM/pull/2028) improves FP8 rollout weight synchronization and CUDA Graph stability for Lumen-RL
- [#2027](https://github.com/ROCm/ATOM/pull/2027) enables SwiGLU activation for Triton MoE dense shared experts on GFX1250
- [#2010](https://github.com/ROCm/ATOM/pull/2010) routes fake-eplb on a zero router correction bias
- [#2018](https://github.com/ROCm/ATOM/pull/2018) allows the MoE dispatch wire to be chosen for the FP4 GEMM it feeds
</details>

<details>
<summary>Model support (5)</summary>

- [#2048](https://github.com/ROCm/ATOM/pull/2048) supports Qwen3.8 Flash Next
- [#2051](https://github.com/ROCm/ATOM/pull/2051) adds the GLM-5.3-Flash text path on MI355X
- [#2061](https://github.com/ROCm/ATOM/pull/2061) adds GLM-5.3 flash support
- [#1995](https://github.com/ROCm/ATOM/pull/1995) adds a persistent path for DCP GLM-5.2
- [#2057](https://github.com/ROCm/ATOM/pull/2057) enables persistent sparse MLA DCP for GLM-5.2
</details>

<details>
<summary>Parallelism & scheduling (6)</summary>

- [#1603](https://github.com/ROCm/ATOM/pull/1603) adds multi-node data parallelism support
- [#2000](https://github.com/ROCm/ATOM/pull/2000) synchronizes prefill/decode sends with offload save completions
- [#2040](https://github.com/ROCm/ATOM/pull/2040) fixes admission to count KV blocks globally against a per-rank pool
- [#2007](https://github.com/ROCm/ATOM/pull/2007) supports dynamic chunked pipeline parallelism
- [#2037](https://github.com/ROCm/ATOM/pull/2037) supports v4 mixed-schedule large concurrency optimizations
- [#2054](https://github.com/ROCm/ATOM/pull/2054) implements DCP KV transfer
</details>

<details>
<summary>Hardware & arch (2)</summary>

- [#2024](https://github.com/ROCm/ATOM/pull/2024) introduces a state checkpoint superblock
- [#2045](https://github.com/ROCm/ATOM/pull/2045) introduces a paged state cache
</details>

<details>
<summary>API & serving (4)</summary>

- [#1992](https://github.com/ROCm/ATOM/pull/1992) refactors OpenAI serving to use one reader per wire format for both delivery modes
- [#2043](https://github.com/ROCm/ATOM/pull/2043) conforms MiniMax-M3 serving to the OpenAI API
- [#1990](https://github.com/ROCm/ATOM/pull/1990) adds a fourth consumer of token IDs to the engine and guards the next one
- [#2041](https://github.com/ROCm/ATOM/pull/2041) fixes an issue where rejected requests never reached the waiting client
</details>

<details>
<summary>Bugfixes (11)</summary>

- [#1993](https://github.com/ROCm/ATOM/pull/1993) includes DP dummies in staging lifetime
- [#2012](https://github.com/ROCm/ATOM/pull/2012) truncates speculative batches at max_tokens for MTP
- [#2004](https://github.com/ROCm/ATOM/pull/2004) fixes Kimi-K3 DSpark integration
- [#2006](https://github.com/ROCm/ATOM/pull/2006) takes dp_size into account when preparing top-k buffers in DPA TP-MoE scenarios
- [#2036](https://github.com/ROCm/ATOM/pull/2036) forwards DCP indexer buffers through the sparse attention bridge
- [#1988](https://github.com/ROCm/ATOM/pull/1988) ensures pipeline-parallel-aware init no longer breaks raw IPC input pools
- [#1994](https://github.com/ROCm/ATOM/pull/1994) fixes the PD prefix cache for DCP
- [#1996](https://github.com/ROCm/ATOM/pull/1996) aligns the DeepSeek-V4 bridge with the geometry/dest_rows API
- [#2060](https://github.com/ROCm/ATOM/pull/2060) decodes on the gathered head width and fixes K3's missing QREP q_proj override
- [#2049](https://github.com/ROCm/ATOM/pull/2049) fixes DeepSeek-V4 PCP with MTP
- [#2044](https://github.com/ROCm/ATOM/pull/2044) marks DP lockstep dummy batches as dummy runs
</details>

<details>
<summary>Tests (1)</summary>

- [#2002](https://github.com/ROCm/ATOM/pull/2002) adds DeepSeek-V4-Pro EPLB and MegaMoE benchmarks at c=512/4096
</details>

<details>
<summary>CI & build (6)</summary>

- [#1997](https://github.com/ROCm/ATOM/pull/1997) updates Mega v2 benchmarks
- [#1999](https://github.com/ROCm/ATOM/pull/1999) updates Mega v2 benchmarks
- [#2038](https://github.com/ROCm/ATOM/pull/2038) submits plugin accuracy jobs through Slurm
- [#2056](https://github.com/ROCm/ATOM/pull/2056) uses two figures for Atomesh interactivity metrics
- [#2005](https://github.com/ROCm/ATOM/pull/2005) tests the Spur GHA smoke workflow
- [#2013](https://github.com/ROCm/ATOM/pull/2013) fixes ATOM and SGLang release Docker builds
</details>

<details>
<summary>Docs (3)</summary>

- [#1998](https://github.com/ROCm/ATOM/pull/1998) adds documentation for Streaming Online Quantization
- [#2052](https://github.com/ROCm/ATOM/pull/2052) clarifies no-tools parser behavior and improves documentation
- [#2059](https://github.com/ROCm/ATOM/pull/2059) fixes a duplicated table on the ATOM overview
</details>

<details>
<summary>Refactors (1)</summary>

- [#2058](https://github.com/ROCm/ATOM/pull/2058) lets QKNormRopeOut produce its own custom-op return
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 1d53a2f7c985e1d560b6f5b43e67a4f7b53053be27e7bf674da90db430b25fb7 -->
