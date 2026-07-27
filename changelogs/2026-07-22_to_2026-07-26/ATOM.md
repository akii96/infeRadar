# ATOM: PR digest (2026-07-22 to 2026-07-26)

_32 merged, 15 newly opened - source ROCm/ATOM, generated 2026-07-26T22:19:53Z_

## TL;DR
* **DeepSeek (V4) and GLM (5.2) dominated the window**, with heavy focus on optimizing them for AMD hardware (MI355/gfx950) via SGLang and vLLM plugins.
* **Speculative decoding saw massive improvements**, notably an in-progress DSpark drafter refactor that boosted acceptance rates from 34.9% to 48%, alongside merged Eagle 3.1 support for vLLM.
* **Major architectural merges landed**, including the massive ATOM-RAPIDserve merge and new Decode Context Parallelism (DCP) for Multi-Head Latent Attention (MLA).
* **In-flight work is tackling large-scale memory and routing**, including a massive hybrid Triton KV offload backend and FlyDSL MegaMoE integration.

## Most important PRs
* [#860](https://github.com/ROCm/ATOM/pull/860) **Atom-RAPIDserve merge** - A massive 2.3k-line merged PR bringing RAPIDserve capabilities into ATOM, touching AITer backends, MLA, and distributed attention paths.
* [#1700](https://github.com/ROCm/ATOM/pull/1700) **Refactor DSpark drafter abstraction** - Newly opened PR that aligns DSpark with the Hugging Face reference, driving a massive speculative decoding acceptance rate jump from 34.9% to 48%.
* [#1683](https://github.com/ROCm/ATOM/pull/1683) **Hybrid KV offload bundle backend** - A massive 5.4k-line in-progress Triton backend that splits dense and hybrid KV cache offloading to optimize memory pressure.
* [#1694](https://github.com/ROCm/ATOM/pull/1694) **GLM 5.2 MTP for SGLang** - Newly opened 5k-line PR implementing Multi-Token Prediction (MTP) support for GLM 5.2 within the SGLang ATOM plugin.
* [#847](https://github.com/ROCm/ATOM/pull/847) **Enable MLA Decode Context Parallel (DCP)** - Merged feature that introduces DCP for Multi-Head Latent Attention, significantly improving decode performance for models like DeepSeek.

## More changes by area

<details>
<summary>Performance (3)</summary>

* [#1681](https://github.com/ROCm/ATOM/pull/1681) [Opened] Overlap pure-TP all_reduce on TBO and delay TP for DeepSeek V4
* [#1698](https://github.com/ROCm/ATOM/pull/1698) Optimize DSpark performance
* [#1670](https://github.com/ROCm/ATOM/pull/1670) Enable prefill delayer for DPA TBO with TARGET_FILL=0.9

</details>

<details>
<summary>Kernels & attention (10)</summary>

* [#1695](https://github.com/ROCm/ATOM/pull/1695) [Opened] Implement construct-time determinism for GLM-5.2 sparse-MLA
* [#1628](https://github.com/ROCm/ATOM/pull/1628) Align SGLang M3 attention path with ATOM
* [#1640](https://github.com/ROCm/ATOM/pull/1640) Support DeepSeek-V4 paged-SWA sparse checkpoint prefix-cache retention on gfx950
* [#1680](https://github.com/ROCm/ATOM/pull/1680) [Opened] Enable Prefix Caching (PCP) in SGLang ATOM for GLM 5.2
* [#1655](https://github.com/ROCm/ATOM/pull/1655) Draft model optimization RoPE via AITer fused kernel
* [#1673](https://github.com/ROCm/ATOM/pull/1673) Fix SGLang DeepSeek V4 fp8 KV cache binding
* [#1690](https://github.com/ROCm/ATOM/pull/1690) [Opened] Support ATOM plugin for Qwen3.5 DPxTPx/DPxEPx
* [#1652](https://github.com/ROCm/ATOM/pull/1652) Make PCP compatible with FP8 KVCache for DeepSeek V4
* [#1697](https://github.com/ROCm/ATOM/pull/1697) Fix DSpark mtp3 + DP + PIECEWISE tail-drain hang
* [#1677](https://github.com/ROCm/ATOM/pull/1677) Add fused qk_norm_rope for DSpark

</details>

<details>
<summary>MoE & quantization (9)</summary>

* [#1691](https://github.com/ROCm/ATOM/pull/1691) [Opened] Integrate EPLB v2 mega
* [#1666](https://github.com/ROCm/ATOM/pull/1666) [Opened] Integrate FlyDSL MegaMoE fused EP-MoE
* [#1664](https://github.com/ROCm/ATOM/pull/1664) Enable DeepSeek V4 fp8 KV cache in atom-vllm
* [#1667](https://github.com/ROCm/ATOM/pull/1667) [Opened] Add EPLB v2 feature branch
* [#1459](https://github.com/ROCm/ATOM/pull/1459) Support Quark per-channel dequantization for GPT-OSS
* [#1669](https://github.com/ROCm/ATOM/pull/1669) Change transformers version to 5.12.1 for quantization compatibility
* [#1692](https://github.com/ROCm/ATOM/pull/1692) [Opened] Add documentation explaining online vs offline quantization
* [#1678](https://github.com/ROCm/ATOM/pull/1678) Support mxfp8 online quantization
* [#1674](https://github.com/ROCm/ATOM/pull/1674) Remove AITER_USE_FLYDSL_MOE_SORTING and update GLM 5.2 fp8 online quant command

</details>

<details>
<summary>API & serving (2)</summary>

* [#1201](https://github.com/ROCm/ATOM/pull/1201) Support Eagle 3.1 speculative decoding in vLLM-ATOM
* [#1682](https://github.com/ROCm/ATOM/pull/1682) [Opened] Enable index_share_for_mtp_iteration in native MTP EagleProposer

</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

* [#1699](https://github.com/ROCm/ATOM/pull/1699) [Opened] Add new dp_sticky policy for DP-aware routing in ATOMesh

</details>

<details>
<summary>CI, Tests & Docs (17)</summary>

* [#1675](https://github.com/ROCm/ATOM/pull/1675) [Opened] Add CI case and recipe for GLM 5.2 agentic benchmark
* [#1626](https://github.com/ROCm/ATOM/pull/1626) Split Dockerfile to different backends
* [#1657](https://github.com/ROCm/ATOM/pull/1657) Enhance ATOMesh dashboard with historical trends
* [#1686](https://github.com/ROCm/ATOM/pull/1686) Accept both kebab-case and snake_case for CLI flags
* [#1689](https://github.com/ROCm/ATOM/pull/1689) Report Concurrency, Accept length and Acceptance rate in benchmarks
* [#1693](https://github.com/ROCm/ATOM/pull/1693) Use /mnt/dcgpuval cache mount for accuracy validation for MI355
* [#1671](https://github.com/ROCm/ATOM/pull/1671) [Opened] Add manual OOB selection and Minimax-M3 for SGLang MI355 benchmark
* plus 10 more minor CI, benchmark, and test updates ([#1658](https://github.com/ROCm/ATOM/pull/1658), [#1688](https://github.com/ROCm/ATOM/pull/1688), [#1651](https://github.com/ROCm/ATOM/pull/1651), [#1668](https://github.com/ROCm/ATOM/pull/1668), [#1685](https://github.com/ROCm/ATOM/pull/1685), [#1676](https://github.com/ROCm/ATOM/pull/1676), [#1684](https://github.com/ROCm/ATOM/pull/1684), [#1663](https://github.com/ROCm/ATOM/pull/1663), [#1660](https://github.com/ROCm/ATOM/pull/1660), [#1662](https://github.com/ROCm/ATOM/pull/1662))

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 5735c338b592dd07260b69b07c33386710ee9a72b0021b67ea794af3b00bd6b5 -->
