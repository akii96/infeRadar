# ATOM: PR digest (2026-07-19 to 2026-07-23)

_37 merged, 15 newly opened - source ROCm/ATOM, generated 2026-07-23T11:31:21Z_

## TL;DR
- **DeepSeek-V4 dominated the window**, with major feature landings for speculative decoding (DSpark), MoE-Merge+TBO, and FP8 KV cache support on AMD hardware (gfx950).
- **Significant KV cache architectural work** is underway, including a massive newly opened Triton-backed hybrid KV offload backend and merged support for DeepSeek-V4 paged-SWA sparse checkpoint retention.
- **Speculative decoding expanded**, with DeepSeek-V4 DSpark and Eagle 3.1 support now merged, plus native MTP EagleProposer in progress.
- **MoE and parallelism saw major upgrades** with the merge of EPLB v0.9 (Expert Parallel Load Balancer) and load-aware DP request routing, alongside FlyDSL MegaMoE integration in progress.
- **Overall direction** shows heavy performance and feature optimization for DeepSeek-V4 and GPT-OSS models, alongside a major documentation migration to ReadTheDocs.

## Most important PRs
- **[#1414](https://github.com/ROCm/ATOM/pull/1414)** (Merged) **[Spec Decode] Add DeepSeek-V4 DSpark speculative decoding**: Introduces DSpark speculative decoding for DeepSeek-V4, heavily touching attention, kernels, and quantization paths to accelerate generation.
- **[#1683](https://github.com/ROCm/ATOM/pull/1683)** (Newly opened) **[Feature] KV offload: hybrid bundle backend + dense/hybrid split**: A massive architectural addition introducing a Triton-backed hybrid bundle backend for KV offloading and dense/hybrid splitting.
- **[#1553](https://github.com/ROCm/ATOM/pull/1553)** (Merged) **[feat][PCP] Enable PCP MoE-Merge+TBO for DeepSeek V4**: Enables Prefill-Chunking Parallelism (PCP) with MoE-Merge and Tensor-Parallel Overlap (TBO) for DeepSeek V4, significantly improving distributed prefill performance.
- **[#847](https://github.com/ROCm/ATOM/pull/847)** (Merged) **[feat][DCP] Enable MLA DCP (Decode Context Parallel)**: Implements Decode Context Parallelism (DCP) for Multi-Head Latent Attention (MLA) via the AITer backend, optimizing decode phases.
- **[#1638](https://github.com/ROCm/ATOM/pull/1638)** (Merged) **feat: load-aware DP request routing for CoreManager**: Adds load-aware Data Parallel request routing to the CoreManager, improving distributed scheduling efficiency and balancing.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#1639](https://github.com/ROCm/ATOM/pull/1639) derive V4 decode compress/write plan caps from graph_bs
- [#1648](https://github.com/ROCm/ATOM/pull/1648) compute prefill split scalars on host to cut D2H syncs
- [#1670](https://github.com/ROCm/ATOM/pull/1670) enable prefill delayer for DPA TBO with TARGET_FILL=0.9
- [#1681](https://github.com/ROCm/ATOM/pull/1681) (Newly opened) overlap pure-TP all_reduce on TBO + Delay TP for DeepSeek-V4
</details>

<details>
<summary>Kernels & attention (9)</summary>

- [#1628](https://github.com/ROCm/ATOM/pull/1628) align attention path with atom for SGLang M3
- [#1640](https://github.com/ROCm/ATOM/pull/1640) add DeepSeek-V4 paged-SWA sparse checkpoint prefix-cache retention
- [#1655](https://github.com/ROCm/ATOM/pull/1655) draft model optimization RoPE via aiter fused kernel for DSpark
- [#1652](https://github.com/ROCm/ATOM/pull/1652) make PCP compatible with FP8 KVCache for DeepSeek V4
- [#1677](https://github.com/ROCm/ATOM/pull/1677) add fused qk_norm_rope for DSpark
- [#1654](https://github.com/ROCm/ATOM/pull/1654) remove kv_last_len for DeepSeek-V4
- [#1659](https://github.com/ROCm/ATOM/pull/1659) (Newly opened) implement DeepSeek-V4 unified KV pool (SWA↔compress share physical KV)
- [#1641](https://github.com/ROCm/ATOM/pull/1641) (Newly opened) enable Decode Context Parallelism (DCP)
- [#1680](https://github.com/ROCm/ATOM/pull/1680) (Newly opened) enable PCP in SGLang ATOM for glm5.2
</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#1210](https://github.com/ROCm/ATOM/pull/1210) merge EPLB_V_0.9 (Expert Parallel Load Balancer)
- [#1459](https://github.com/ROCm/ATOM/pull/1459) support quark per-channel dequantization
- [#1664](https://github.com/ROCm/ATOM/pull/1664) enable DeepSeek-V4 FP8 KV cache in atom-vllm
- [#1673](https://github.com/ROCm/ATOM/pull/1673) fix SGLang DeepSeek-V4 FP8 KV cache binding
- [#1666](https://github.com/ROCm/ATOM/pull/1666) (Newly opened) integrate FlyDSL MegaMoE fused EP-MoE
- [#1667](https://github.com/ROCm/ATOM/pull/1667) (Newly opened) implement EPLB v2 features
- [#1678](https://github.com/ROCm/ATOM/pull/1678) (Newly opened) support mxfp8 online quantization
</details>

<details>
<summary>Model support & Speculative Decoding (2)</summary>

- [#1201](https://github.com/ROCm/ATOM/pull/1201) support Eagle 3.1 speculative decoding in vLLM-ATOM
- [#1682](https://github.com/ROCm/ATOM/pull/1682) (Newly opened) enable index_share_for_mtp_iteration in native MTP EagleProposer
</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

- [#1647](https://github.com/ROCm/ATOM/pull/1647) (Newly opened) fix PD decode admission cap and remote-KV backpressure in scheduler
</details>

<details>
<summary>Docs (3)</summary>

- [#1656](https://github.com/ROCm/ATOM/pull/1656) migrate stale Sphinx docs to RTD redirects
- [#1650](https://github.com/ROCm/ATOM/pull/1650) apply editorial style pass across all docs using Google developer style guide
- [#1632](https://github.com/ROCm/ATOM/pull/1632) setup ROCm docs toolchain and publishing
</details>

<details>
<summary>CI & build (18)</summary>

- [#1626](https://github.com/ROCm/ATOM/pull/1626) split dockerfile to different backends
- [#1657](https://github.com/ROCm/ATOM/pull/1657) enhance ATOMesh dashboard with historical trends
- [#1658](https://github.com/ROCm/ATOM/pull/1658) support shared NFS model cache for benchmarks
- [#1675](https://github.com/ROCm/ATOM/pull/1675) (Newly opened) add CI case and recipe for glm5.2 agentic benchmark
- [#1671](https://github.com/ROCm/ATOM/pull/1671) (Newly opened) add manual OOB selection and Minimax-M3 for SGLang MI355 benchmark
- plus 13 more minor CI updates
</details>

<details>
<summary>Bugfixes (1)</summary>

- [#1649](https://github.com/ROCm/ATOM/pull/1649) account for non-torch (RCCL) memory in KV cache sizing
</details>

<details>
<summary>Other (2)</summary>

- [#477](https://github.com/ROCm/ATOM/pull/477) add profiling context
- [#1662](https://github.com/ROCm/ATOM/pull/1662) remove test result
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 2bc53005e8059fa7f5cd81dc55b481144c99aa672875ade49dfd043500a4dc68 -->
