# ATOM: PR digest (2026-08-05 to 2026-08-09)

_25 merged, 23 newly opened - source ROCm/ATOM, generated 2026-08-09T21:55:11Z_

## TL;DR
*   **Top Models**: DeepSeek (V4) and GLM (5.2) dominated the window, alongside significant new attention for Kimi K3.
*   **Multimodal Expansion**: A massive newly-opened PR brings a diffusion subsystem to ATOM, targeting MiniMax-H3 video and audio generation.
*   **Attention & Kernels**: Heavy focus on advanced attention variants, merging Multi-Token Prediction (MTP) for GLM 5.2 and opening Device Communication Protocol (DCP) integrations for DeepSeek's Sparse MLA (DSA).
*   **Infrastructure**: Significant upgrades are in progress, notably the bump to vLLM 0.26.x and the addition of reliable DP/TP collective RPCs for distributed workers.

## Most important PRs
**[#1760](https://github.com/ROCm/ATOM/pull/1760)**
Merges comprehensive Multi-Token Prediction (MTP) support for GLM 5.2. This significantly expands the engine's speculative decoding capabilities and throughput for the GLM model family.

**[#1836](https://github.com/ROCm/ATOM/pull/1836)**
Opens a massive 11k-line feature branch to introduce a diffusion subsystem. This expands ATOM into multimodal generation by enabling MiniMax-H3 video and audio generation natively.

**[#1832](https://github.com/ROCm/ATOM/pull/1832)**
Opens support for DCP (Device Communication Protocol) within DeepSeek's Sparse Attention (DSA / Sparse MLA). This aims to heavily optimize distributed attention overhead and scaling for DeepSeek models.

**[#1752](https://github.com/ROCm/ATOM/pull/1752)**
Merges a performance optimization for Kimi K3 that enables dual-stream execution for shared experts and specific kernel fusions. This provides a direct throughput win for MoE routing.

**[#1807](https://github.com/ROCm/ATOM/pull/1807)**
Merges a critical bugfix preventing KV cache corruption during LMCache reloads. This ensures stability and correctness for distributed prefix caching and offloading.

## More changes by area

<details>
<summary>Model support (5)</summary>

- [#1821](https://github.com/ROCm/ATOM/pull/1821) opens initial model support and integration for Kimi K3
- [#1819](https://github.com/ROCm/ATOM/pull/1819) opens vision support targeting vLLM 0.26 compatibility
- [#1794](https://github.com/ROCm/ATOM/pull/1794) opens the core upgrade of vLLM dependencies to version 0.26.1
- [#1805](https://github.com/ROCm/ATOM/pull/1805) opens DSpark speculative decoding support for Kimi K3 on vLLM 0.26
- [#1806](https://github.com/ROCm/ATOM/pull/1806) opens DSpark PS MLA support and draft model causal adjustments for Kimi K3

</details>

<details>
<summary>Performance (4)</summary>

- [#1837](https://github.com/ROCm/ATOM/pull/1837) opens a fix to remove four host-side bottlenecks that idle the GPU at high concurrency
- [#1818](https://github.com/ROCm/ATOM/pull/1818) opens optimizations for prefill KDA execution
- [#1820](https://github.com/ROCm/ATOM/pull/1820) opens an opt-in flag (`ATOM_USE_AITER_KDA`) to run KDA prefill on AITer for Kimi K3
- [#1795](https://github.com/ROCm/ATOM/pull/1795) opens a feature to bypass mxscale BMM for V4 models

</details>

<details>
<summary>Kernels & attention (4)</summary>

- [#1781](https://github.com/ROCm/ATOM/pull/1781) merges DCP enablement for fp8 Multi-Token Prediction (MTP)
- [#1816](https://github.com/ROCm/ATOM/pull/1816) opens persistent decode enablement for GLM-5.2 DPA
- [#1830](https://github.com/ROCm/ATOM/pull/1830) opens opt-in AITer `attn_res_gate` routing via `ATOM_USE_AITER_ATTN_RES`
- [#1831](https://github.com/ROCm/ATOM/pull/1831) opens a guard for sparse MLA index conversions to prevent out-of-bounds errors

</details>

<details>
<summary>MoE & quantization (3)</summary>

- [#1793](https://github.com/ROCm/ATOM/pull/1793) merges gfx942 dtype-dialect and MXFP4 swizzle fixes for DeepSeek-V4-Flash
- [#1798](https://github.com/ROCm/ATOM/pull/1798) opens a guard for GLM flat fmoe execution on MI308 hardware
- [#1833](https://github.com/ROCm/ATOM/pull/1833) opens routing for `wo_a` grouped LoRA through the flydsl a8w4 batched GEMM on gfx1250

</details>

<details>
<summary>Parallelism & scheduling (4)</summary>

- [#1808](https://github.com/ROCm/ATOM/pull/1808) opens reliable DP/TP collective RPC support for ATOM workers
- [#1835](https://github.com/ROCm/ATOM/pull/1835) opens a scheduler fix to unblock decode phases stuck behind long chunked prefills
- [#1804](https://github.com/ROCm/ATOM/pull/1804) merges a fix to reuse the vLLM PyNccl communicator in the plugin layer
- [#1811](https://github.com/ROCm/ATOM/pull/1811) opens stable top-k enablement for tensor parallel GLM-DSA

</details>

<details>
<summary>API & serving (4)</summary>

- [#1810](https://github.com/ROCm/ATOM/pull/1810) merges support for accepting Anthropic-style chat tools in the OpenAI frontend
- [#1803](https://github.com/ROCm/ATOM/pull/1803) opens a fix to include `content=""` in streaming role chunks to match OpenAI/vLLM shapes
- [#1802](https://github.com/ROCm/ATOM/pull/1802) merges prefix cache usage optimizations and adds logging for block pool occupancy
- [#1725](https://github.com/ROCm/ATOM/pull/1725) merges a fix for `lm_cache` write-back behavior

</details>

<details>
<summary>Bugfixes (4)</summary>

- [#1799](https://github.com/ROCm/ATOM/pull/1799) merges an alignment fix for DeepSeek-V4 compressed KV block geometry
- [#1834](https://github.com/ROCm/ATOM/pull/1834) opens a bugfix for a recent GLM 5.2 regression
- [#1809](https://github.com/ROCm/ATOM/pull/1809) opens a fix for DeepSeek-V4 accuracy errors
- [#1796](https://github.com/ROCm/ATOM/pull/1796) merges a fix for GLM 5.2 nshot20 accuracy

</details>

<details>
<summary>Tests, CI & build (15)</summary>

- [#1740](https://github.com/ROCm/ATOM/pull/1740) merges support for swebench_lite precision validation
- [#1814](https://github.com/ROCm/ATOM/pull/1814) merges the Mega v2 benchmark suite
- [#1826](https://github.com/ROCm/ATOM/pull/1826) opens guards for SWE-bench disk usage and adds prefix-cache hit rate reporting
- plus 12 more minor CI and build updates ([#1776](https://github.com/ROCm/ATOM/pull/1776), [#1778](https://github.com/ROCm/ATOM/pull/1778), [#1800](https://github.com/ROCm/ATOM/pull/1800), [#1801](https://github.com/ROCm/ATOM/pull/1801), [#1815](https://github.com/ROCm/ATOM/pull/1815), [#1817](https://github.com/ROCm/ATOM/pull/1817), [#1822](https://github.com/ROCm/ATOM/pull/1822), [#1823](https://github.com/ROCm/ATOM/pull/1823), [#1824](https://github.com/ROCm/ATOM/pull/1824), [#1825](https://github.com/ROCm/ATOM/pull/1825), [#1827](https://github.com/ROCm/ATOM/pull/1827), [#1829](https://github.com/ROCm/ATOM/pull/1829))

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 8a2dc825ab456842b748e9b98fd4dcd7594d4f284ae2a0d99b7fe8275f654f96 -->
