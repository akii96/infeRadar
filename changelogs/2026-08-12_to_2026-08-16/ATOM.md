# ATOM: PR digest (2026-08-12 to 2026-08-16)

_36 merged, 26 newly opened - source ROCm/ATOM, generated 2026-08-16T21:53:49Z_

## TL;DR
- **DeepSeek-V4 & Kimi K3 dominate**: Major pushes for DeepSeek-V4 (PAGE-backed state checkpoints, massive in-flight LMcache offloading) and Kimi K3 / DSpark (FP8 KV cache, speculative decoding, vision support).
- **Performance & Scheduling**: Significant wins in DSpark bubble optimization via Zero-Overhead Scheduling and frontend/server event loop unblocking to prevent stalling between request waves.
- **Attention & MLA**: Upgraded core vLLM to 0.26.1, enabled persistent decode for all MLA models under DPA, and advancing SSM replay for GDN attention.
- **Architecture**: Advancing disaggregated prefill with MTP (Multi-Token Prediction) draft support on Pipeline Parallel (PP) prefill nodes.

## Most important PRs
- **[#1894](https://github.com/ROCm/ATOM/pull/1894)** implements PAGE-backed state checkpoints for DeepSeek-V4. This significantly improves memory management and state recovery for DSV4 workloads.
- **[#1839](https://github.com/ROCm/ATOM/pull/1839)** upgrades the core vLLM dependency to 0.26.1. This brings in upstream features and fixes across the attention, MLA, and plugin components.
- **[#1861](https://github.com/ROCm/ATOM/pull/1861)** optimizes DSpark scheduling bubbles using Zero-Overhead Scheduling (N-2 ell) and `torch.compile`. This reduces latency for draft models during speculative decoding.
- **[#1876](https://github.com/ROCm/ATOM/pull/1876)** enables FP8 KV cache for the Kimi K3 DSpark draft model. This drastically reduces memory pressure and improves throughput for speculative decoding.
- **[#1880](https://github.com/ROCm/ATOM/pull/1880)** (newly opened) introduces LMcache page and slot offloading for DeepSeek-V4. This massive 26k-line architectural change will allow spilling KV state to slower memory tiers.

## More changes by area

<details>
<summary>Performance (5)</summary>

- [#1906](https://github.com/ROCm/ATOM/pull/1906) unwedges the request socket to push metrics and merge backlogged SSE chunks
- [#1907](https://github.com/ROCm/ATOM/pull/1907) batches tokenizer calls for building random datasets, yielding a 5.25x speedup
- [#1912](https://github.com/ROCm/ATOM/pull/1912) stops the frontend/server event loop from stalling between request waves
- [#1871](https://github.com/ROCm/ATOM/pull/1871) (newly opened) optimizes Kimi K3 DSpark performance for ATOM SGL
- [#1911](https://github.com/ROCm/ATOM/pull/1911) (newly opened) scales the MLA KV-split budget past 16 on the persistent decode path

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#1788](https://github.com/ROCm/ATOM/pull/1788) optimizes attention res ref fla and fuses surrounding components
- [#1865](https://github.com/ROCm/ATOM/pull/1865) allows V4 pools to have no dense class for V4-Pro plus DSpark
- [#1831](https://github.com/ROCm/ATOM/pull/1831) guards sparse MLA index conversion
- [#1884](https://github.com/ROCm/ATOM/pull/1884) pins attn_pre outputs across graph-to-eager to fix V4 piecewise accuracy
- [#1890](https://github.com/ROCm/ATOM/pull/1890) (newly opened) fuses block-banking cat into the attn_res kernel
- [#1889](https://github.com/ROCm/ATOM/pull/1889) (newly opened) adds flydsl attention for m3
- [#1893](https://github.com/ROCm/ATOM/pull/1893) (newly opened) routes KDA prefill through the FlyDSL AITER kernel
- [#1883](https://github.com/ROCm/ATOM/pull/1883) (newly opened) enables SSM replay for GDN attention and KDA
- [#1879](https://github.com/ROCm/ATOM/pull/1879) (newly opened) adds an additional statecache strategy
- [#1887](https://github.com/ROCm/ATOM/pull/1887) (newly opened) optimizes state cache with replayssm
- [#1881](https://github.com/ROCm/ATOM/pull/1881) (newly opened) enables dflash in the ATOM plugin

</details>

<details>
<summary>MoE & quantization (3)</summary>

- [#1691](https://github.com/ROCm/ATOM/pull/1691) implements Eplb v2 mega for MoE and quantization
- [#1900](https://github.com/ROCm/ATOM/pull/1900) drops top-k from the mori dispatch trim bound in fused MoE
- [#1895](https://github.com/ROCm/ATOM/pull/1895) (newly opened) supports FP4 dispatch and FP8 combine

</details>

<details>
<summary>Model support (11)</summary>

- [#1877](https://github.com/ROCm/ATOM/pull/1877) adds the GLM-5.2 agentic recipe
- [#1806](https://github.com/ROCm/ATOM/pull/1806) supports Kimi K3 Dspark PS MLA and draft model casual False
- [#1738](https://github.com/ROCm/ATOM/pull/1738) supports Qwen 3.5x models
- [#1820](https://github.com/ROCm/ATOM/pull/1820) enables KDA prefill on AITER for Kimi K3
- [#1811](https://github.com/ROCm/ATOM/pull/1811) enables stable top-k for tensor parallel in GLM DSA
- [#1882](https://github.com/ROCm/ATOM/pull/1882) (newly opened) enhances GLM-5.2 with DP attention, prefix cache optimizations, and logging
- [#1899](https://github.com/ROCm/ATOM/pull/1899) (newly opened) adds Kimi K3 DSpark speculative decoding for the ATOM vLLM plugin
- [#1910](https://github.com/ROCm/ATOM/pull/1910) (newly opened) adds Kimi K3 vLLM plugin vision and DSpark draft support
- [#1908](https://github.com/ROCm/ATOM/pull/1908) (newly opened) enables Cohere Command-R on ATOM
- [#1901](https://github.com/ROCm/ATOM/pull/1901) (newly opened) adds support for Qwen 3.8
- [#1913](https://github.com/ROCm/ATOM/pull/1913) (newly opened) enables the K3 vision part in the vLLM plugin

</details>

<details>
<summary>Parallelism & scheduling (9)</summary>

- [#1868](https://github.com/ROCm/ATOM/pull/1868) implements MTP for disaggregated prefill on a PP prefill node
- [#1850](https://github.com/ROCm/ATOM/pull/1850) adds a synthetic forced acceptance-rate knob for speculative decoding
- [#1874](https://github.com/ROCm/ATOM/pull/1874) adds V4 checkpoint capacity headroom for KV cache
- [#1866](https://github.com/ROCm/ATOM/pull/1866) keeps TCP transport off RDMA devices for Mooncake
- [#1501](https://github.com/ROCm/ATOM/pull/1501) enables DP routing for chat completions
- [#1898](https://github.com/ROCm/ATOM/pull/1898) includes CPU-offloaded prefix hits in request usage for the scheduler
- [#1870](https://github.com/ROCm/ATOM/pull/1870) enables persistent decode for all MLA models under DPA
- [#1909](https://github.com/ROCm/ATOM/pull/1909) (newly opened) adds mesh entrypoints
- [#1892](https://github.com/ROCm/ATOM/pull/1892) (newly opened) allows passing token ids to /v1/completions

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#1903](https://github.com/ROCm/ATOM/pull/1903) (newly opened) adds Gluon MXFP8 GEMM support for GFX12

</details>

<details>
<summary>API & serving (3)</summary>

- [#1803](https://github.com/ROCm/ATOM/pull/1803) includes content="" in streaming role chunks to match OpenAI/vLLM shapes
- [#1886](https://github.com/ROCm/ATOM/pull/1886) stabilizes ATOM mesh routing sticky and scheduling
- [#1873](https://github.com/ROCm/ATOM/pull/1873) (newly opened) exposes Prometheus metrics for KV-aware routing and modernizes the API

</details>

<details>
<summary>Bugfixes (6)</summary>

- [#1904](https://github.com/ROCm/ATOM/pull/1904) fixes DeepSeek-V4 accuracy
- [#1902](https://github.com/ROCm/ATOM/pull/1902) fixes V4 piecewise graph pool accuracy issues
- [#1859](https://github.com/ROCm/ATOM/pull/1859) fixes illegal memory access in CSA decode top-k under MTP for DeepSeek-V4
- [#1809](https://github.com/ROCm/ATOM/pull/1809) fixes DeepSeek-V4 accuracy errors
- [#1891](https://github.com/ROCm/ATOM/pull/1891) (newly opened) fixes a CI error for ATOM SGL
- [#1869](https://github.com/ROCm/ATOM/pull/1869) (newly opened) fixes K3 DSpark

</details>

<details>
<summary>CI & build (8)</summary>

- [#1783](https://github.com/ROCm/ATOM/pull/1783) adds K3 to precheckin and nightly tests
- [#1862](https://github.com/ROCm/ATOM/pull/1862) decouples OOT SGLang for Docker releases
- [#1896](https://github.com/ROCm/ATOM/pull/1896) recovers the base image to torch2.10
- [#1905](https://github.com/ROCm/ATOM/pull/1905) changes the base image for Docker releases
- [#1864](https://github.com/ROCm/ATOM/pull/1864) covers the deferred status queue across chunked prefill in MTP tests
- [#1867](https://github.com/ROCm/ATOM/pull/1867) (newly opened) adds a new torch base docker
- [#1872](https://github.com/ROCm/ATOM/pull/1872) (newly opened) changes the CI scope for 0.5.17
- [#1888](https://github.com/ROCm/ATOM/pull/1888) (newly opened) removes a vLLM patch

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 7175caefb6d7df9bce24fe99f72d4d5c1fc00f686e7655e3fc5a1344f6a57680 -->
