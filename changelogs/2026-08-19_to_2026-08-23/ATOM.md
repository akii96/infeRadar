# ATOM: PR digest (2026-08-19 to 2026-08-23)

_36 merged, 15 newly opened - source ROCm/ATOM, generated 2026-08-23T21:47:46Z_

## TL;DR
* **DeepSeek (DSV4)** dominated the window, landing massive LMCache page/slot offloading and significant FP4 indexer prefill/MQA tuning (specifically targeting gfx950).
* **GLM-5.2** and **Kimi-K3** saw major attention and MLA upgrades, including DP attention, prefix caching, and Distributed Cache Parallelism (DCP) enablement for K3 + DSpark.
* **Performance & Kernels**: Landed MoE shared expert fusion into all-to-all, online weight quantization during load, and host-work overlapping between forwards.
* **Architecture**: A massive refactor of the OpenAI frontend now uses one reader per wire format for both delivery modes, streamlining the mesh/plugin boundaries.

## Most important PRs
* **[#1880](https://github.com/ROCm/ATOM/pull/1880)** - Implements LMCache page and slot offloading for DeepSeek V4, significantly improving cache hit rates and memory efficiency for long-context DSV4 workloads.
* **[#1992](https://github.com/ROCm/ATOM/pull/1992)** - Refactors the OpenAI frontend to use a single reader per wire format across both delivery modes, unifying the mesh, plugin, and distributed boundaries while dropping over 1,200 lines of redundant code.
* **[#1749](https://github.com/ROCm/ATOM/pull/1749)** - Introduces online weight quantization during model loading, reducing disk footprint requirements and streamlining deployment for quantized MoE models.
* **[#1882](https://github.com/ROCm/ATOM/pull/1882)** - Enhances GLM-5.2 with DP attention and prefix cache optimizations, alongside robust logging for speculative decoding and MLA paths.
* **[#1917](https://github.com/ROCm/ATOM/pull/1917)** - Fuses shared experts directly into the all-to-all MoE kernel, reducing launch overhead and improving end-to-end throughput for MoE architectures.

## More changes by area

<details>
<summary>Performance (7)</summary>

- [#1989](https://github.com/ROCm/ATOM/pull/1989) cuts host work between two forwards to improve CPU/GPU overlap
- [#1991](https://github.com/ROCm/ATOM/pull/1991) stops the engine garbage collector from walking unreclaimed heaps
- [#1971](https://github.com/ROCm/ATOM/pull/1971) defaults the native DSV4 indexer cache to FP4
- [#1986](https://github.com/ROCm/ATOM/pull/1986) tunes the FP4 prefill MQA grid for DeepSeek V4
- [#1980](https://github.com/ROCm/ATOM/pull/1980) raises GC thresholds in the EngineCore and ModelRunner
- [#1974](https://github.com/ROCm/ATOM/pull/1974) (Opened) optimizes FP8 and FP4 indexer prefill for DSV4
- [#1952](https://github.com/ROCm/ATOM/pull/1952) (Opened) allows low-concurrency serving to disable side streams for DSV4
</details>

<details>
<summary>Kernels & attention (12)</summary>

- [#1881](https://github.com/ROCm/ATOM/pull/1881) enables dflash for the ATOM plugin
- [#1852](https://github.com/ROCm/ATOM/pull/1852) adds piecewise cudagraph support for Attention FFN to optimize DSpark dynamic
- [#1899](https://github.com/ROCm/ATOM/pull/1899) implements Kimi-K3 DSpark speculative decoding for the ATOM vLLM plugin
- [#1931](https://github.com/ROCm/ATOM/pull/1931) adds `cp_kv_cache_interleave_size` for Distributed Cache Parallelism (DCP)
- [#1930](https://github.com/ROCm/ATOM/pull/1930) enables DCP for Kimi-K3 + DSpark
- [#1951](https://github.com/ROCm/ATOM/pull/1951) supports DCP on the vLLM-ATOM Kimi-K3 integration
- [#1795](https://github.com/ROCm/ATOM/pull/1795) implements V4 without an mxscale BMM
- [#1977](https://github.com/ROCm/ATOM/pull/1977) fuses add and RMS norm for Kimi-K3 DSpark
- [#1967](https://github.com/ROCm/ATOM/pull/1967) keeps ragged-lens H2D pinned in all cudagraph modes and supports dual stream in piecewise
- [#1947](https://github.com/ROCm/ATOM/pull/1947) (Opened) optimizes the state checkpoint port for attention and MLA
- [#1960](https://github.com/ROCm/ATOM/pull/1960) (Opened) implements LMCache offload for Kimi-K3
- [#1962](https://github.com/ROCm/ATOM/pull/1962) (Opened) fuses add and RMS norm for Kimi-K3 DSpark (duplicate/follow-up)
</details>

<details>
<summary>MoE & quantization (2)</summary>

- [#1964](https://github.com/ROCm/ATOM/pull/1964) fuses quantization kernels for Kimi
- [#1965](https://github.com/ROCm/ATOM/pull/1965) (Opened) fuses quantization kernels for KDA
</details>

<details>
<summary>Model support (2)</summary>

- [#1690](https://github.com/ROCm/ATOM/pull/1690) drafts ATOM plugin support for Qwen3.5 DPxTPx/DPxEPx
- [#1953](https://github.com/ROCm/ATOM/pull/1953) (Opened) adds GLM-5.2 multiprocess offload to LMCache
</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#1755](https://github.com/ROCm/ATOM/pull/1755) adds a fake EPLB (Expert Parallel Load Balancer) for performance testing
- [#1948](https://github.com/ROCm/ATOM/pull/1948) updates speculative decoding to take the forced-acceptance target as a length
- [#1978](https://github.com/ROCm/ATOM/pull/1978) (Opened) avoids local copies in the EPLB
</details>

<details>
<summary>API & serving (2)</summary>

- [#1955](https://github.com/ROCm/ATOM/pull/1955) (Opened) vendors a tool parser implementation for the mesh
- [#1946](https://github.com/ROCm/ATOM/pull/1946) (Opened) snapshots PAGE state at the end of prefill for the state cache
</details>

<details>
<summary>Bugfixes (13)</summary>

- [#1990](https://github.com/ROCm/ATOM/pull/1990) fixes engine token ID consumption by adding a fourth consumer and a guard
- [#1976](https://github.com/ROCm/ATOM/pull/1976) fixes DCP + LMCache integration for Kimi-K3
- [#1968](https://github.com/ROCm/ATOM/pull/1968) restores sparse MLA + DCP for GLM-5.2 broken by a gathered-head-width change
- [#1987](https://github.com/ROCm/ATOM/pull/1987) fixes DPA speculative middle chunk collective alignment for agentic workloads
- [#1956](https://github.com/ROCm/ATOM/pull/1956) fixes LMCache to allocate staging buffers on the first-use stream
- [#1979](https://github.com/ROCm/ATOM/pull/1979) fixes the vLLM-ATOM DeepSeek interface
- [#1958](https://github.com/ROCm/ATOM/pull/1958) unmasks sparse-gather metadata and drops dead `produces_output` arg in sparse MLA
- [#1966](https://github.com/ROCm/ATOM/pull/1966) updates DSV4 to follow the AITER FP4 MQA package move
- [#1988](https://github.com/ROCm/ATOM/pull/1988) ensures pipeline-parallel-aware init no longer breaks raw IPC input pools
- [#1985](https://github.com/ROCm/ATOM/pull/1985) (Opened) fixes Qwen3.5 block-FP8 correctness under vLLM FULL cudagraph
- [#1961](https://github.com/ROCm/ATOM/pull/1961) (Opened) fixes an OpenAI frontend issue where a `<` in the answer withheld the stream
- [#1993](https://github.com/ROCm/ATOM/pull/1993) (Opened) fences late draft staging before reuse in the engine
- [#1984](https://github.com/ROCm/ATOM/pull/1984) (Opened) restricts the FP4 indexer default to gfx950 architecture only
</details>

<details>
<summary>CI & build (4)</summary>

- [#1950](https://github.com/ROCm/ATOM/pull/1950) adds a Mooncake GPUDirect RDMA smoke test for the atomesh PD topology
- [#1982](https://github.com/ROCm/ATOM/pull/1982) adds an r0 naive CI test
- [#1983](https://github.com/ROCm/ATOM/pull/1983) updates the Mega v2 benchmark
- [#1973](https://github.com/ROCm/ATOM/pull/1973) (Opened) adds Qwen38 accuracy tests
</details>

<details>
<summary>Other (1)</summary>

- [#1975](https://github.com/ROCm/ATOM/pull/1975) adds Gfx1250 test ep 817
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: de47b0a7c00a67587d3c0d70c2ae6c62e4904f150509aeb64edd9b967c3d88fe -->
