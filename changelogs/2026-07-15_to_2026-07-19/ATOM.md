# ATOM: PR digest (2026-07-15 to 2026-07-19)

_35 merged, 12 newly opened - source ROCm/ATOM, generated 2026-07-19T22:12:09Z_

## TL;DR
- **Model Focus:** GLM 5.2 and DeepSeek-V4 dominated this cycle, with major updates to FP8/MXFP4 quantization recipes, MTP optimizations, and KV cache FP8 support.
- **Attention & Kernels:** Significant attention path alignments were merged for SGLang (GLM 5.2), alongside a new prefill coalescer for DP-attention and PCP enablement for DSA models.
- **MoE & Load Balancing:** A massive EPLB expert load pass was merged to improve MoE routing, complemented by load-aware DP request routing for the CoreManager.
- **In Progress:** Large ongoing work to add Attention Context Parallelism (CP) for DSA models and multi-node DP support.

## Most important PRs
- **[#1625](https://github.com/ROCm/ATOM/pull/1625)** introduces an EPLB (Expert Parallel Load Balancer) pass for MoE models, significantly improving expert routing and load distribution across devices.
- **[#1611](https://github.com/ROCm/ATOM/pull/1611)** adds a prefill coalescer for Data Parallel (DP) attention, reducing overhead and improving throughput during the prefill phase, complete with TTFT guards.
- **[#1600](https://github.com/ROCm/ATOM/pull/1600)** implements FP8 KV cache support specifically for DeepSeek-V4, reducing memory footprint and increasing batch size capacity for the model.
- **[#1531](https://github.com/ROCm/ATOM/pull/1531)** optimizes Multi-Token Prediction (MTP) for GLM 5.2 in the `atom-vllm` backend, improving speculative decoding performance and MLA integration.
- **[#1618](https://github.com/ROCm/ATOM/pull/1618)** (Newly opened) proposes Context Parallelism (CP) for attention in DSA models, a major architectural shift to distribute long-context attention across multiple GPUs.

## More changes by area

<details>
<summary>Performance (3)</summary>

- [#1639](https://github.com/ROCm/ATOM/pull/1639) derives V4 decode compress/write plan caps from graph batch size
- [#1465](https://github.com/ROCm/ATOM/pull/1465) optimizes model loading speed for MoE models
- [#1631](https://github.com/ROCm/ATOM/pull/1631) fixes a small concurrent performance gap with atom native for GLM 5.2

</details>

<details>
<summary>Kernels & attention (5)</summary>

- [#1606](https://github.com/ROCm/ATOM/pull/1606) aligns the SGLang attention path with atom for GLM 5.2
- [#1514](https://github.com/ROCm/ATOM/pull/1514) enables PCP (Prefill-Chunking Parallelism) for DSA models
- [#1473](https://github.com/ROCm/ATOM/pull/1473) enables MiniMax M3 FP8 index cache and fuses index_score_kernel with partial_topk kernel
- [#1628](https://github.com/ROCm/ATOM/pull/1628) (Newly opened) aligns the SGLang attention path with atom for M3
- [#1624](https://github.com/ROCm/ATOM/pull/1624) (Newly opened) enables SGL atom PCP

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#1607](https://github.com/ROCm/ATOM/pull/1607) updates the GLM 5.2 FP8/MXFP4 recipe and benchmark configurations
- [#1576](https://github.com/ROCm/ATOM/pull/1576) adds SGLang plugin support for GLM 5.2 FP8 and FP4
- [#1633](https://github.com/ROCm/ATOM/pull/1633) applies MoE pad_align override before creating weights
- [#1614](https://github.com/ROCm/ATOM/pull/1614) adds an architecture check for bias interleave in MoE
- [#1612](https://github.com/ROCm/ATOM/pull/1612) (Newly opened) stabilizes ATOM FP8 no-eager rollout weight sync and CUDA graph lifecycle
- [#1610](https://github.com/ROCm/ATOM/pull/1610) (Newly opened) fixes an expert map issue in the Triton backend

</details>

<details>
<summary>Model support (3)</summary>

- [#1575](https://github.com/ROCm/ATOM/pull/1575) adds Kimi-K2.5 MXFP4 PD disaggregation recipe and updates configurations
- [#1605](https://github.com/ROCm/ATOM/pull/1605) (Newly opened) adds Eagle3 speculative decoding support for gpt-oss-120b
- [#1591](https://github.com/ROCm/ATOM/pull/1591) fixes DeepSeek-V4 SGLang index top-k metadata

</details>

<details>
<summary>Parallelism & scheduling (4)</summary>

- [#1638](https://github.com/ROCm/ATOM/pull/1638) implements load-aware DP request routing for CoreManager
- [#1586](https://github.com/ROCm/ATOM/pull/1586) supports agentic dataset benchmarks under PD disaggregation mode
- [#1635](https://github.com/ROCm/ATOM/pull/1635) skips distributed barriers on single-rank runs
- [#1603](https://github.com/ROCm/ATOM/pull/1603) (Newly opened) adds multi-node Data Parallel (DP) support

</details>

<details>
<summary>API & serving (3)</summary>

- [#1636](https://github.com/ROCm/ATOM/pull/1636) adds `--load_dummy` init modes and improves EP loader/hash-routing robustness
- [#1597](https://github.com/ROCm/ATOM/pull/1597) allows using the `--kv-cache-dtype` kebab-case flag in the UI
- [#1604](https://github.com/ROCm/ATOM/pull/1604) (Newly opened) upgrades the vLLM dependency to version 0.25.1

</details>

<details>
<summary>CI & build (12)</summary>

- [#1626](https://github.com/ROCm/ATOM/pull/1626) (Newly opened) splits the Dockerfile to support different backends
- [#1613](https://github.com/ROCm/ATOM/pull/1613) (Newly opened) modifies atom-vllm benchmark models
- [#1622](https://github.com/ROCm/ATOM/pull/1622) adds retry logic for aiter wheel downloads in CI
- [#1602](https://github.com/ROCm/ATOM/pull/1602) optimizes mesh CI logs and dashboard fonts
- [#1617](https://github.com/ROCm/ATOM/pull/1617) updates GLM 5.2 accuracy and benchmark cases for SGLang
- [#1592](https://github.com/ROCm/ATOM/pull/1592) adds GLM-5.2-MXFP4 TP4/TP8 to ATOMesh CI
- [#1620](https://github.com/ROCm/ATOM/pull/1620) adds a docker override for accuracy validation in SGL+ATOM CI
- [#1609](https://github.com/ROCm/ATOM/pull/1609) updates ATOMesh dashboard series grouping and point details
- [#1629](https://github.com/ROCm/ATOM/pull/1629) updates the MI308 GLM 5.2 recipe and workflow documentation
- [#1637](https://github.com/ROCm/ATOM/pull/1637) adds the online quant command for GLM 5.2 benchmarks
- [#1608](https://github.com/ROCm/ATOM/pull/1608) fixes aiperf installation to preserve the SGLang dependency stack
- [#1623](https://github.com/ROCm/ATOM/pull/1623) (Newly opened) adds an agentic MiniMax-M3 PD+LMCache test case

</details>

<details>
<summary>Docs (1)</summary>

- [#1632](https://github.com/ROCm/ATOM/pull/1632) (Newly opened) sets up the ROCm docs toolchain and publishing workflow

</details>

<details>
<summary>Bugfixes (3)</summary>

- [#1549](https://github.com/ROCm/ATOM/pull/1549) fixes dispatch gap rules, arch-constant FP issues, and P5 timing errors
- [#1596](https://github.com/ROCm/ATOM/pull/1596) forces the aiter unreg collective capture path for DeepSeek-V4 DP+PIECEWISE
- [#1634](https://github.com/ROCm/ATOM/pull/1634) fixes black formatting in `tbo/ubatching.py`

</details>

<details>
<summary>Refactors (1)</summary>

- [#1615](https://github.com/ROCm/ATOM/pull/1615) refactors trace analysis for kernels and quantization

</details>

<details>
<summary>Other (1)</summary>

- [#1627](https://github.com/ROCm/ATOM/pull/1627) updates TBO so any rank 8k opens all

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 629bbb8882c558401470c80972babefc58c1b44c698addd6888b791bd5953c4b -->
