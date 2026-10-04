# ATOM: PR digest (2026-08-30 to 2026-09-03)

_33 merged, 17 newly opened - source ROCm/ATOM, generated 2026-09-03T13:48:17Z_

## TL;DR
- **Kimi-K3 and DeepSeek-V4 got the most attention.** K3 saw LMCache offload ([#2053](https://github.com/ROCm/ATOM/pull/2053)), fused act+fp8 per-token quant ([#2089](https://github.com/ROCm/ATOM/pull/2089)) and DCP decode work. DSV4 saw decode-indptr, MTP and EPLB/MegaMoE benchmark work. A new model, GLM-5.3-Flash, landed on MI355X ([#2051](https://github.com/ROCm/ATOM/pull/2051)).
- **The biggest performance work was in MLA and DSA decode with decode context parallelism (DCP).** It fuses the prefill context reorg, dequant and kv_b_proj ([#2113](https://github.com/ROCm/ATOM/pull/2113)), scores the sparse indexer per query token to unblock MTP ([#2118](https://github.com/ROCm/ATOM/pull/2118)), and offers an opt-in fused top-k merge ([#2087](https://github.com/ROCm/ATOM/pull/2087)). [#2101](https://github.com/ROCm/ATOM/pull/2101) and [#2120](https://github.com/ROCm/ATOM/pull/2120) trim DSV4 decode overhead.
- **Speculative decode and MTP are being hardened.** Merged: [#2049](https://github.com/ROCm/ATOM/pull/2049) (DSV4 PCP with MTP) and [#2100](https://github.com/ROCm/ATOM/pull/2100) (fused draft eltwise in cudagraph mode). Open: [#2116](https://github.com/ROCm/ATOM/pull/2116) (capture MTP step zero), [#2128](https://github.com/ROCm/ATOM/pull/2128) (DP-vocab-sharded argmax) and the MiniMax-M3 EAGLE3 fixes.
- **Overall direction:** long-context and large-scale serving (DCP/PCP, KV offload, PD transfer, communication-fused MoE) plus Triton 3.8 compatibility, with a heavy CI and benchmark presence.

## Most important PRs
**[#2053](https://github.com/ROCm/ATOM/pull/2053) — Kimi-K3 LMCache offload**
Adds KV-cache offload to LMCache for K3, spanning attention, MLA, distributed and plugin code with tests and docs. It is the largest merged change. [#2132](https://github.com/ROCm/ATOM/pull/2132), a not-ready refactor of it, is already open.

**[#2051](https://github.com/ROCm/ATOM/pull/2051) — GLM-5.3-Flash (glm5_next) text path on MI355X**
Brings up a new model family on aiter and Triton backends with MLA, MoE and attention paths, plus CI and tests.

**[#2088](https://github.com/ROCm/ATOM/pull/2088) — Settle a step's shape once**
A cross-cutting rework of per-step shape handling across MLA, MoE, attention and speculative decode. It also fixes three defects that the old handling exposed.

**[#2118](https://github.com/ROCm/ATOM/pull/2118) — DSA/DCP sparse decode indexer scored per query token**
Fixes the indexer to score each query token separately, which unblocks MTP with DCP. It is paired with [#2102](https://github.com/ROCm/ATOM/pull/2102) (CUDA-graph metadata fix) and [#2087](https://github.com/ROCm/ATOM/pull/2087).

**[#2101](https://github.com/ROCm/ATOM/pull/2101) — DSV4 decode indptrs built on device**
Builds the decode indptrs on the GPU and bounds compression work per token. This removes host-side overhead in the decode path.

## More changes by area

<details>
<summary>Performance (3)</summary>

- [#2120](https://github.com/ROCm/ATOM/pull/2120) fold the MLA query-head pad into the fused q write
- [#2089](https://github.com/ROCm/ATOM/pull/2089) fuse activation and fp8 per-token quant for K3 dense/shared MLP and full attention
- [#1965](https://github.com/ROCm/ATOM/pull/1965) fuse kernels in KDA

</details>

<details>
<summary>Kernels & attention (7)</summary>

- [#2003](https://github.com/ROCm/ATOM/pull/2003) replace tl.make_block_ptr with plain pointer arithmetic for Triton 3.8
- [#2113](https://github.com/ROCm/ATOM/pull/2113) fuse prefill context reorg, dequant and kv_b_proj into one kernel in DCP, using the custom AllGather
- [#2060](https://github.com/ROCm/ATOM/pull/2060) decode on the gathered head width for K3 DCP
- [#2087](https://github.com/ROCm/ATOM/pull/2087) opt-in fused DCP decode top-k merge for DSA
- [#2077](https://github.com/ROCm/ATOM/pull/2077) DSV4 bf16 opus attention on gfx1250
- [#1919](https://github.com/ROCm/ATOM/pull/1919) integrate aiter fused KDA decode kernel
- [#2133](https://github.com/ROCm/ATOM/pull/2133) revert [#1919](https://github.com/ROCm/ATOM/pull/1919)

</details>

<details>
<summary>MoE & quantization (3)</summary>

- [#2018](https://github.com/ROCm/ATOM/pull/2018) mori-v2: choose the MoE dispatch wire format for the fp4 GEMM it feeds
- [#2095](https://github.com/ROCm/ATOM/pull/2095) route gfx1250 wo_a grouped LoRA through the FlyDSL A8W8 BMM
- [#2098](https://github.com/ROCm/ATOM/pull/2098) zero packed fp4x2 dummy weights through a byte-view fallback in the loader

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#2049](https://github.com/ROCm/ATOM/pull/2049) fix DSV4 PCP with MTP
- [#2100](https://github.com/ROCm/ATOM/pull/2100) remove a copy and fuse eltwise in the draft module in cudagraph mode (GLM5.2 MTP)
- [#1770](https://github.com/ROCm/ATOM/pull/1770) periodic engine status log

</details>

<details>
<summary>API & serving (2)</summary>

- [#2109](https://github.com/ROCm/ATOM/pull/2109) fix output text for runs with synthetic accept
- [#2092](https://github.com/ROCm/ATOM/pull/2092) log the KV transfer hot path at debug instead of info

</details>

<details>
<summary>Bugfixes (2)</summary>

- [#2102](https://github.com/ROCm/ATOM/pull/2102) fix sparse indexer local context metadata for CUDA graphs under DCP
- [#2090](https://github.com/ROCm/ATOM/pull/2090) guard the new per-seq q-cum slice on kv_last_page_lens in MLA

</details>

<details>
<summary>CI & build (10)</summary>

- [#2115](https://github.com/ROCm/ATOM/pull/2115) change the atom-plugin CI runner label
- [#2099](https://github.com/ROCm/ATOM/pull/2099) prevent benchmark dashboard history loss
- [#2103](https://github.com/ROCm/ATOM/pull/2103) store model download locks and staging under /tmp
- [#2104](https://github.com/ROCm/ATOM/pull/2104) lower gpu-memory-utilization to 0.85 for EPLB MegaMoE c=4096
- [#2002](https://github.com/ROCm/ATOM/pull/2002) add DeepSeek-V4-Pro EPLB + MegaMoE benchmark case at c=512/4096
- [#2093](https://github.com/ROCm/ATOM/pull/2093) DSV4 EPLB MegaMoE c512/c4096 bench
- [#2094](https://github.com/ROCm/ATOM/pull/2094) DSV4 EPLB MegaMoE c512/c4096 bench (duplicate)
- [#2096](https://github.com/ROCm/ATOM/pull/2096) DSV4 EPLB MegaMoE c512/c4096 bench follow-up
- plus 2 more minor CI updates are covered under newly opened work below

</details>

<details>
<summary>Newly opened: in progress (17)</summary>

- [#2111](https://github.com/ROCm/ATOM/pull/2111) Rust-owned Atomesh standalone EngineCore transport
- [#2132](https://github.com/ROCm/ATOM/pull/2132) refactor K3 LMCache (not ready)
- [#2110](https://github.com/ROCm/ATOM/pull/2110) native RCCL DEP transport for MoE
- [#2121](https://github.com/ROCm/ATOM/pull/2121) MLA/indexer cache transfer for PD in the P-CPP/D-DCP scenario
- [#2106](https://github.com/ROCm/ATOM/pull/2106) allocate the Eagle3 MHA draft KV pool in flash layout for MiniMax-M3
- [#2116](https://github.com/ROCm/ATOM/pull/2116) capture DeepSeek-V4 MTP step zero
- [#2114](https://github.com/ROCm/ATOM/pull/2114) AITer communication-fused MoE for DSV4
- [#2112](https://github.com/ROCm/ATOM/pull/2112) define a profiler window
- [#2125](https://github.com/ROCm/ATOM/pull/2125) PCP: shard shared_experts on the folded TP grid and sync sampled ids outside the speculative branch
- [#2131](https://github.com/ROCm/ATOM/pull/2131) Kimi-K3 AgentX recipe
- [#2128](https://github.com/ROCm/ATOM/pull/2128) DP-vocab-sharded greedy argmax for speculative drafting
- [#2122](https://github.com/ROCm/ATOM/pull/2122) MiniMax-M3: unblock fp8 KV cache and EAGLE3 spec decode on the vLLM plugin
- [#2117](https://github.com/ROCm/ATOM/pull/2117) update the GLM5.2 agentic recipe
- [#2126](https://github.com/ROCm/ATOM/pull/2126) fix Kimi-K3 piecewise cudagraph
- [#2097](https://github.com/ROCm/ATOM/pull/2097) enable HIP dma-buf MR in the Mooncake release image
- [#2130](https://github.com/ROCm/ATOM/pull/2130) make the Kimi-K3 KDA temporal state dtype configurable
- [#2129](https://github.com/ROCm/ATOM/pull/2129) cap cudagraph capture size to fix Kimi-K3 DSpark DCP8 OOM in plugin CI

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 3c213c0e488c95320d34f0302f3ffbb5abb894bd1deeba879a45d507ec322db7 -->
