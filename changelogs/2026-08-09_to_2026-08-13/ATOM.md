# ATOM: PR digest (2026-08-09 to 2026-08-13)

_32 merged, 24 newly opened - source ROCm/ATOM, generated 2026-08-13T10:38:29Z_

## TL;DR
- **Models & Perf**: DeepSeek-V4, GLM-5/5.2, and Kimi K3 dominated this window. Major performance work targeted Kimi K3 via DSpark speculative decoding bubble optimization and FP8 KV cache for draft models.
- **KV Cache & State**: A massive architectural shift towards stateful caching is underway. The engine merged content-addressed per-request state for correct prefix hits and opened LMCache NVMe offloading for DeepSeek-V4.
- **Disaggregated Prefill**: Significant progress landed for disaggregated architectures (DPA), including a draft pipeline-parallel prefill node for Multi-Token Prediction (MTP) and DP-aware request routing with sticky policies.
- **Overall Direction**: The repository is heavily optimizing for complex multi-model serving, speculative decoding (DSpark), and massive-scale KV cache offloading, pushing towards zero-overhead scheduling and robust disaggregated prefill/decode.

## Most important PRs
- **[#1771](https://github.com/ROCm/ATOM/pull/1771)** introduces content-addressed per-request state for the KV cache. This massive merged architectural change ensures correct prefix cache hits for stateful models across distributed setups.
- **[#1880](https://github.com/ROCm/ATOM/pull/1880)** (in-progress) implements LMCache NVMe offloading specifically for DeepSeek-V4 pages and slots. This is critical for handling DSV4's massive KV cache footprint without exhausting GPU memory.
- **[#1868](https://github.com/ROCm/ATOM/pull/1868)** drafts a pipeline-parallel prefill node for Multi-Token Prediction (MTP) in disaggregated setups. This merged PR lays the groundwork for scaling speculative decoding prefill across multiple nodes.
- **[#1861](https://github.com/ROCm/ATOM/pull/1861)** (in-progress) optimizes DSpark speculative decoding bubbles via zero-overhead scheduling and `torch.compile` for the draft model, directly targeting latency bottlenecks in Kimi K3 serving.
- **[#1882](https://github.com/ROCm/ATOM/pull/1882)** (in-progress) enhances GLM-5.2 with Data Parallel (DP) attention and prefix cache optimizations, significantly improving throughput and routing efficiency for the GLM family under disaggregated architectures.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#1837](https://github.com/ROCm/ATOM/pull/1837) removes four host-side bottlenecks that idle the GPU at high concurrency
- [#1842](https://github.com/ROCm/ATOM/pull/1842) (opened) fuses the KDA prefill gather, scatter, and output copy for Kimi K3
- [#1876](https://github.com/ROCm/ATOM/pull/1876) (opened) enables FP8 KV cache for the Kimi K3 DSpark draft model
- [#1871](https://github.com/ROCm/ATOM/pull/1871) (opened) improves K3 DSpark performance

</details>

<details>
<summary>Kernels & attention (9)</summary>

- [#1788](https://github.com/ROCm/ATOM/pull/1788) optimizes attention residual reference FLA and fuses surrounding operations
- [#1865](https://github.com/ROCm/ATOM/pull/1865) fixes V4 kernels to allow a V4 pool to have no dense class (supporting V4-Pro + DSpark)
- [#1831](https://github.com/ROCm/ATOM/pull/1831) guards sparse MLA index conversion in attention
- [#1852](https://github.com/ROCm/ATOM/pull/1852) (opened) adds piecewise CUDA graph support for attention FFNs to optimize DSpark dynamic
- [#1889](https://github.com/ROCm/ATOM/pull/1889) (opened) adds FlyDSL attention for M3
- [#1883](https://github.com/ROCm/ATOM/pull/1883) (opened) enables SSM replay for GDN attention and KDA
- [#1887](https://github.com/ROCm/ATOM/pull/1887) (opened) optimizes state cache with replay SSM
- [#1879](https://github.com/ROCm/ATOM/pull/1879) (opened) adds an additional state cache strategy
- [#1881](https://github.com/ROCm/ATOM/pull/1881) (opened) enables dflash in the Atom plugin

</details>

<details>
<summary>Model support (7)</summary>

- [#1782](https://github.com/ROCm/ATOM/pull/1782) enables Kimi K3 multimodel support
- [#1806](https://github.com/ROCm/ATOM/pull/1806) supports Kimi K3 DSpark PS MLA and draft model causal False
- [#1786](https://github.com/ROCm/ATOM/pull/1786) supports GLM-5 and GLM-5.2 in rtpllm
- [#1816](https://github.com/ROCm/ATOM/pull/1816) enables persistent decode for GLM-5.2 DPA
- [#1870](https://github.com/ROCm/ATOM/pull/1870) enables persistent decode for all MLA models under DPA
- [#1843](https://github.com/ROCm/ATOM/pull/1843) (opened) adds K3 DSpark support for ATOM SGL
- [#1877](https://github.com/ROCm/ATOM/pull/1877) (opened) adds GLM-5.2 agentic recipe

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#1855](https://github.com/ROCm/ATOM/pull/1855) refactors DP-aware request handling and LMCache offload support
- [#1699](https://github.com/ROCm/ATOM/pull/1699) adds a new `dp_sticky` policy for DP-aware routing
- [#1886](https://github.com/ROCm/ATOM/pull/1886) (opened) stabilizes disaggregated prefill/decode routing and scheduling for DPA+Mesh
- [#1858](https://github.com/ROCm/ATOM/pull/1858) (opened) skips KV cache tensor allocation for shared indexer KV
- [#1866](https://github.com/ROCm/ATOM/pull/1866) keeps TCP transport off RDMA devices for Mooncake

</details>

<details>
<summary>API & serving (8)</summary>

- [#1851](https://github.com/ROCm/ATOM/pull/1851) validates NVMe offload storage for LMCache
- [#1850](https://github.com/ROCm/ATOM/pull/1850) adds a synthetic (forced) acceptance-rate knob for speculative decoding
- [#1803](https://github.com/ROCm/ATOM/pull/1803) includes `content=""` in streaming role chunks to match OpenAI/vLLM shapes
- [#1873](https://github.com/ROCm/ATOM/pull/1873) (opened) exposes Prometheus metrics for KV-aware routing and modernizes the API
- [#1838](https://github.com/ROCm/ATOM/pull/1838) honors model generation config defaults for Anthropic
- [#1849](https://github.com/ROCm/ATOM/pull/1849) (opened) enables TBO for DPSK R1 in SGL+ATOM
- [#1840](https://github.com/ROCm/ATOM/pull/1840) (opened) upgrades SGLang to v0.5.17
- [#1839](https://github.com/ROCm/ATOM/pull/1839) (opened) upgrades vLLM to 0.26.1

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#1863](https://github.com/ROCm/ATOM/pull/1863) supports Crusoe MI355 runner label alias in Atomesh

</details>

<details>
<summary>MoE & quantization (1)</summary>

- [#1777](https://github.com/ROCm/ATOM/pull/1777) adds online quantization best practices documentation

</details>

<details>
<summary>Bugfixes (7)</summary>

- [#1859](https://github.com/ROCm/ATOM/pull/1859) fixes illegal memory access in DeepSeek-V4 CSA decode top-k under MTP
- [#1857](https://github.com/ROCm/ATOM/pull/1857) fixes trace tags and adds K3 tag
- [#1874](https://github.com/ROCm/ATOM/pull/1874) adds V4 checkpoint capacity headroom to the KV cache
- [#1884](https://github.com/ROCm/ATOM/pull/1884) pins `attn_pre` outputs across graph-to-eager to fix V4 piecewise accuracy
- [#1811](https://github.com/ROCm/ATOM/pull/1811) enables stable top-k for tensor parallel in GLM-DSA
- [#1809](https://github.com/ROCm/ATOM/pull/1809) fixes DeepSeek-V4 accuracy error
- [#1869](https://github.com/ROCm/ATOM/pull/1869) (opened) fixes K3 DSpark issues

</details>

<details>
<summary>Tests, CI & build (9)</summary>

- [#1826](https://github.com/ROCm/ATOM/pull/1826) guards SWE-bench disk usage and reports prefix-cache hit rates
- [#1820](https://github.com/ROCm/ATOM/pull/1820) enables KDA prefill on aiter for Kimi K3
- [#1864](https://github.com/ROCm/ATOM/pull/1864) covers deferred status queue across chunked prefill for MTP
- plus 6 more minor CI/build updates ([#1862](https://github.com/ROCm/ATOM/pull/1862), [#1860](https://github.com/ROCm/ATOM/pull/1860), [#1872](https://github.com/ROCm/ATOM/pull/1872), [#1888](https://github.com/ROCm/ATOM/pull/1888), [#1867](https://github.com/ROCm/ATOM/pull/1867), [#1846](https://github.com/ROCm/ATOM/pull/1846)) fixing torch 2.13 errors, dockerfiles, and vLLM patches

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 12582838f2d75a79e2b7fe8b30756eaf74adc32a8be673407a1ba9060ac1ee3e -->
