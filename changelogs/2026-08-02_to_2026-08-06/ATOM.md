# ATOM: PR digest (2026-08-02 to 2026-08-06)

_27 merged, 25 newly opened - source ROCm/ATOM, generated 2026-08-06T11:46:20Z_

## TL;DR
- **Model Focus**: DeepSeek (V4/R1) and GLM (5/5.2) saw the most activity, alongside heavy enablement for Kimi-K3 and Minimax-M3.
- **KV Cache Architecture**: A massive in-progress rewrite introduces content-addressed per-request state to ensure correct prefix caching for stateful models.
- **Speculative Decoding**: Significant advancements in Multi-Token Prediction (MTP) and DSpark, including bridging Dynamic Context Parallelism (DCP) with MTP and enabling DSpark for Kimi-K3.
- **Performance & Hardware**: Merged dual-stream execution for Kimi-K3 shared experts, QK norm RoPE cache fusion for Qwen3, and fixes for DeepSeek-V4 MXFP4 swizzling on AMD gfx942.
- **Overall Direction**: The engine is rapidly maturing its speculative decoding pipelines and advanced KV cache management (LMCache/SparseKV) to support next-gen MoE models on AMD hardware, while upgrading the core vLLM backend to 0.26.1.

## Most important PRs
- **[#1771](https://github.com/ROCm/ATOM/pull/1771)** (Opened): Radically overhauls the KV cache to use content-addressed per-request state, fixing prefix cache hits for stateful models (+13k lines).
- **[#1779](https://github.com/ROCm/ATOM/pull/1779)** (Opened): Introduces major SparseKV cache optimizations specifically targeting GLM-5.2 agentic tasks (+2.8k lines).
- **[#1746](https://github.com/ROCm/ATOM/pull/1746)** (Merged): Switches Dynamic Context Parallelism (DCP) decode to persistent PagedAttention and makes DCP compatible with Multi-Token Prediction (MTP).
- **[#1752](https://github.com/ROCm/ATOM/pull/1752)** (Merged): Delivers a performance win for Kimi-K3 by enabling dual-stream execution for shared experts and fusing operations.
- **[#1794](https://github.com/ROCm/ATOM/pull/1794)** (Opened): Upgrades the underlying vLLM framework integration to version 0.26.1, bringing upstream features and fixes to the ATOM plugin.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#1758](https://github.com/ROCm/ATOM/pull/1758) optimizes DSpark piecewise dummy decode to avoid eager fallback and improve low-concurrency performance (Merged)
- [#1766](https://github.com/ROCm/ATOM/pull/1766) enables QK norm RoPE cache fusion for dense models like Qwen3 (Merged)
- [#1788](https://github.com/ROCm/ATOM/pull/1788) optimizes attention residual reference FLA and fuses surrounding operations (Opened)
- [#1795](https://github.com/ROCm/ATOM/pull/1795) adds DeepSeek-V4 WOA MXScale BMM support (Opened)

</details>

<details>
<summary>Model support (12)</summary>

- [#1727](https://github.com/ROCm/ATOM/pull/1727) fixes multiple issues to pass Kimi-K3 KVV validation (Merged)
- [#1757](https://github.com/ROCm/ATOM/pull/1757) enables Minimax-M3 MTP in SGLang and fixes M3 errors from SGLang updates (Merged)
- [#1772](https://github.com/ROCm/ATOM/pull/1772) restores DeepSeek-R1 TP4 accuracy in SGLang (Merged)
- [#1773](https://github.com/ROCm/ATOM/pull/1773) enables align-mode Mamba prefix caching for Kimi-K3 in vLLM-ATOM (Opened)
- [#1782](https://github.com/ROCm/ATOM/pull/1782) adds Kimi-K3 multi-model documentation and tests (Opened)
- [#1783](https://github.com/ROCm/ATOM/pull/1783) adds Kimi-K3 to precheckin and nightly tests (Opened)
- [#1786](https://github.com/ROCm/ATOM/pull/1786) supports GLM-5 and GLM-5.2 in rtpllm (Opened)
- [#1789](https://github.com/ROCm/ATOM/pull/1789) supports DSpark speculative decoding for Kimi-K3 in vLLM-ATOM (Opened)
- [#1805](https://github.com/ROCm/ATOM/pull/1805) enables DSpark speculative decoding for Kimi-K3 on vLLM 0.26 (Opened)
- [#1806](https://github.com/ROCm/ATOM/pull/1806) supports Kimi-K3 DSpark PS MLA and draft model causal False (Opened)
- [#1809](https://github.com/ROCm/ATOM/pull/1809) fixes DeepSeek-V4 accuracy error (Opened)
- [#1816](https://github.com/ROCm/ATOM/pull/1816) enables persistent decode for GLM-5.2 DPA (Opened)

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#1775](https://github.com/ROCm/ATOM/pull/1775) binds DeepSeek-V4 plugin compressor quantization metadata (Merged)
- [#1777](https://github.com/ROCm/ATOM/pull/1777) adds online quantization best practices documentation (Opened)
- [#1781](https://github.com/ROCm/ATOM/pull/1781) enables DCP with FP8 MTP (Opened)
- [#1793](https://github.com/ROCm/ATOM/pull/1793) fixes gfx942 dtype-dialect and MXFP4 swizzling for DeepSeek-V4-Flash (Opened)
- [#1798](https://github.com/ROCm/ATOM/pull/1798) guards GLM flat FMoE on MI308 hardware (Opened)
- [#1814](https://github.com/ROCm/ATOM/pull/1814) adds MegaMoE v2 benchmarks (Merged)

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#1802](https://github.com/ROCm/ATOM/pull/1802) optimizes prefix cache usage and adds logging for block pool occupancy (Merged)
- [#1808](https://github.com/ROCm/ATOM/pull/1808) adds reliable DP/TP collective RPC support for ATOM workers (Opened)
- [#1811](https://github.com/ROCm/ATOM/pull/1811) enables stable top-k for tensor parallel GLM-DSA (Opened)

</details>

<details>
<summary>API & serving (4)</summary>

- [#1706](https://github.com/ROCm/ATOM/pull/1706) adds chat template support (Merged)
- [#1770](https://github.com/ROCm/ATOM/pull/1770) adds periodic engine status logging in server mode (Opened)
- [#1803](https://github.com/ROCm/ATOM/pull/1803) fixes streaming role chunk to match OpenAI/vLLM shape by including `content=""` (Opened)
- [#1810](https://github.com/ROCm/ATOM/pull/1810) accepts Anthropic-style chat tools in the OpenAI frontend (Opened)

</details>

<details>
<summary>Bugfixes (9)</summary>

- [#1725](https://github.com/ROCm/ATOM/pull/1725) fixes LMCache write-back issues (Merged)
- [#1774](https://github.com/ROCm/ATOM/pull/1774) fixes mark trace for separated capture batch size profiler (Merged)
- [#1780](https://github.com/ROCm/ATOM/pull/1780) fixes random IMA issues (Opened)
- [#1792](https://github.com/ROCm/ATOM/pull/1792) fixes vLLM runtime CUDA graph mode (Merged)
- [#1796](https://github.com/ROCm/ATOM/pull/1796) fixes GLM-5.2 nshot20 accuracy (Merged)
- [#1799](https://github.com/ROCm/ATOM/pull/1799) aligns DeepSeek-V4 compressed KV block geometry in SGLang (Merged)
- [#1801](https://github.com/ROCm/ATOM/pull/1801) fixes GLM-5.2 PCP from 2 to 4 in nightly tests (Merged)
- [#1804](https://github.com/ROCm/ATOM/pull/1804) reuses vLLM PyNccl communicator in the plugin (Opened)
- [#1807](https://github.com/ROCm/ATOM/pull/1807) prevents KV corruption on LMCache reload (Merged)

</details>

<details>
<summary>CI & build (9)</summary>

- [#1740](https://github.com/ROCm/ATOM/pull/1740) supports SWE-bench lite precision validation (Merged)
- [#1778](https://github.com/ROCm/ATOM/pull/1778) adds acceptance rate check in MTP workflow cases (Merged)
- [#1671](https://github.com/ROCm/ATOM/pull/1671) adds manual OOB selection and Minimax-M3 for SGLang MI355 benchmark (Merged)
- [#1776](https://github.com/ROCm/ATOM/pull/1776) refines benchmark schedules and dispatch options (Merged)
- plus 5 more minor CI and benchmark updates ([#1785](https://github.com/ROCm/ATOM/pull/1785), [#1787](https://github.com/ROCm/ATOM/pull/1787), [#1800](https://github.com/ROCm/ATOM/pull/1800), [#1815](https://github.com/ROCm/ATOM/pull/1815), [#1817](https://github.com/ROCm/ATOM/pull/1817))

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: eebfeb83913630cbfd05be79a9a9c7b391b5e765677eac12d9711ea2706cac77 -->
