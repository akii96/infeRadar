# ATOM: PR digest (2026-08-16 to 2026-08-20)

_32 merged, 30 newly opened - source ROCm/ATOM, generated 2026-08-20T09:58:23Z_

## TL;DR
- **Model Focus:** DeepSeek (DSV4), GLM-5.2, and Kimi-K3 dominated this window. Major architectural pushes include rolling out LMCache offloading across all three families and enabling Distributed Checkpoint (DCP) for Sparse MLA/DSA.
- **Performance & Memory:** Significant memory and latency wins landed for v4 state management, highlighted by a 60x cheaper PAGE checkpoint copy and the removal of the reserve floor.
- **Kernels & MoE:** MoE and quantization saw heavy development, notably adding FP4 dispatch with FP8 combine, and fusing shared experts into all-to-all MoE routing.
- **Attention & Spec-Decode:** DSpark speculative decoding received major bubble optimizations via Zero-Overhead Scheduling, alongside new piecewise CUDA graph support for dynamic attention FFNs.
- **Overall Direction:** The engine is aggressively scaling its multi-tenant/multi-process KV cache sharing (LMCache) while rapidly maturing Kimi-K3 support (vision, agentic optimizations, and DSpark integration).

## Most important PRs
- **[#1880](https://github.com/ROCm/ATOM/pull/1880)** feat(lmcache): add DSV4 page and slot offload
  This merged PR brings LMCache offloading to DeepSeek V4, significantly improving multi-tenant memory efficiency by allowing page and slot states to be offloaded via Triton and AITER backends.
- **[#1940](https://github.com/ROCm/ATOM/pull/1940)** k3 agentic optimizations
  A massive newly-opened WIP (13k+ lines) that overhauls Kimi-K3 for agentic workloads, touching Triton, AITER, and MLA components to optimize distributed attention and quantization for agent-heavy traffic.
- **[#1943](https://github.com/ROCm/ATOM/pull/1943)** perf(v4): a smaller PAGE checkpoint image, a 60x cheaper copy, and no reserve floor
  Delivers a massive performance win for v4 memory management by shrinking the checkpoint image and drastically reducing the cost of PAGE copies, freeing up critical VRAM.
- **[#1882](https://github.com/ROCm/ATOM/pull/1882)** Enhance GLM-5.2 with DP attention, prefix cache optimizations, and logging
  Completes major feature support for GLM-5.2 by integrating Data Parallel (DP) attention and optimizing the prefix cache for speculative decoding.
- **[#1832](https://github.com/ROCm/ATOM/pull/1832)** [feat][DCP] Enable DCP for DeepSeek Sparse Attention (DSA / Sparse MLA)
  Enables Distributed Checkpointing (DCP) for DeepSeek's Sparse MLA, a critical distributed feature for scaling DeepSeek models across multiple nodes without losing attention state.

## More changes by area

<details>
<summary>Performance & scheduling (6)</summary>

- [#1861](https://github.com/ROCm/ATOM/pull/1861) Optimizes DSpark speculative decoding bubbles using Zero-Overhead Scheduling and torch.compile
- [#1912](https://github.com/ROCm/ATOM/pull/1912) Prevents the frontend server event loop from stalling between request waves
- [#1937](https://github.com/ROCm/ATOM/pull/1937) Defers draft proposal publication in MTP to improve performance (Newly opened)
- [#1952](https://github.com/ROCm/ATOM/pull/1952) Disables side streams during low-concurrency serving for DSV4 (Newly opened)
- [#1962](https://github.com/ROCm/ATOM/pull/1962) Fuses add and RMS norm operations for Kimi-K3 DSpark (Newly opened)
- [#1911](https://github.com/ROCm/ATOM/pull/1911) Dynamically allocates MLA decode KV-split budgets based on machine capacity instead of a hardcoded limit (Newly opened)

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#1852](https://github.com/ROCm/ATOM/pull/1852) Adds piecewise CUDA graph support for attention FFNs to optimize dynamic DSpark
- [#1881](https://github.com/ROCm/ATOM/pull/1881) Enables dflash in the ATOM plugin
- [#1931](https://github.com/ROCm/ATOM/pull/1931) Adds `cp_kv_cache_interleave_size` for parallel decoding (PD)
- [#1964](https://github.com/ROCm/ATOM/pull/1964) Fuses kernels for Kimi models
- [#1938](https://github.com/ROCm/ATOM/pull/1938) Optimizes the MLA prefill chunk kernel
- [#1958](https://github.com/ROCm/ATOM/pull/1958) Fixes sparse-MLA by unmasking sparse-gather metadata and removing dead arguments
- [#1915](https://github.com/ROCm/ATOM/pull/1915) Fixes DSpark DP-attention by warming the block drafter
- [#1965](https://github.com/ROCm/ATOM/pull/1965) Fuses kernels in KDA (Newly opened)
- [#1967](https://github.com/ROCm/ATOM/pull/1967) Keeps the ragged-lens H2D pinned across all CUDA graph modes in DSpark (Newly opened)
- [#1919](https://github.com/ROCm/ATOM/pull/1919) Integrates the AITER fused KDA decode kernel for Kimi-K3 (Newly opened)
- [#1923](https://github.com/ROCm/ATOM/pull/1923) Swaps the M3 gluon kernel for the flydsl kernel (Newly opened)

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#1691](https://github.com/ROCm/ATOM/pull/1691) Implements Eplb v2 mega for MoE and quantization
- [#1895](https://github.com/ROCm/ATOM/pull/1895) Adds support for FP4 dispatch and FP8 combine in MoE
- [#1966](https://github.com/ROCm/ATOM/pull/1966) Fixes DSV4 to align with the AITER FP4 MQA package move
- [#1917](https://github.com/ROCm/ATOM/pull/1917) Fuses shared experts into the all-to-all MoE routing (Newly opened)
- [#1926](https://github.com/ROCm/ATOM/pull/1926) Pins logical memory for shared experts (Newly opened)
- [#1932](https://github.com/ROCm/ATOM/pull/1932) Fixes MoE to preserve FP8 shuffle metadata (Newly opened)

</details>

<details>
<summary>Model support (14)</summary>

- [#1821](https://github.com/ROCm/ATOM/pull/1821) Adds initial ATOM SGL support for Kimi K3
- [#1899](https://github.com/ROCm/ATOM/pull/1899) Enables DSpark speculative decoding for Kimi-K3 in the ATOM vLLM plugin
- [#1930](https://github.com/ROCm/ATOM/pull/1930) Enables DCP for Kimi-K3 with DSpark
- [#1849](https://github.com/ROCm/ATOM/pull/1849) Enables TBO for DeepSeek R1 in SGL ATOM
- [#1690](https://github.com/ROCm/ATOM/pull/1690) Adds draft ATOM plugin support for Qwen3.5 DPxTPx/DPxEPx
- [#1904](https://github.com/ROCm/ATOM/pull/1904) Fixes accuracy issues in DeepSeek V4
- [#1916](https://github.com/ROCm/ATOM/pull/1916) Removes `AITER_DISABLE_FMHA_OPUS` environment variables for Kimi-K3
- [#1960](https://github.com/ROCm/ATOM/pull/1960) Implements LMCache offloading for Kimi-K3 (Newly opened)
- [#1953](https://github.com/ROCm/ATOM/pull/1953) Adds multiprocess LMCache offload support for GLM-5.2 (Newly opened)
- [#1910](https://github.com/ROCm/ATOM/pull/1910) Adds vision and DSpark draft support to the Kimi-K3 vLLM plugin (Newly opened)
- [#1951](https://github.com/ROCm/ATOM/pull/1951) Supports DCP on the vLLM-ATOM Kimi-K3 integration (Newly opened)
- [#1913](https://github.com/ROCm/ATOM/pull/1913) Enables the vision component for Kimi-K3 in the vLLM plugin (Newly opened)
- [#1941](https://github.com/ROCm/ATOM/pull/1941) Adds the Agentic-K3 recipe documentation and features (Newly opened)
- [#1968](https://github.com/ROCm/ATOM/pull/1968) Restores sparse MLA and DCP for GLM-5.2 after upstream K3 changes broke it (Newly opened)

</details>

<details>
<summary>Distributed & mesh (5)</summary>

- [#1950](https://github.com/ROCm/ATOM/pull/1950) Adds Mooncake GPUDirect RDMA smoke tests for Atomesh PD topology
- [#1925](https://github.com/ROCm/ATOM/pull/1925) Adds Pareto curve and interactivity formulas to the Atomesh dashboard
- [#1909](https://github.com/ROCm/ATOM/pull/1909) Adds mesh entrypoints in a large WIP (Newly opened)
- [#1942](https://github.com/ROCm/ATOM/pull/1942) Implements wideep topology features (Newly opened)
- [#1921](https://github.com/ROCm/ATOM/pull/1921) Fixes Atomesh by registering decode buffers on reachable RDMA rails for cross-rail PD (Newly opened)

</details>

<details>
<summary>API, serving & state (6)</summary>

- [#1948](https://github.com/ROCm/ATOM/pull/1948) Updates speculative decoding to take forced-acceptance targets as lengths on the standard engine schedule
- [#1956](https://github.com/ROCm/ATOM/pull/1956) Fixes LMCache by allocating staging buffers on the first-use stream
- [#1947](https://github.com/ROCm/ATOM/pull/1947) Optimizes state checkpoint porting (Newly opened)
- [#1955](https://github.com/ROCm/ATOM/pull/1955) Vendors a tool parser implementation for batched streaming (Newly opened)
- [#1954](https://github.com/ROCm/ATOM/pull/1954) Implements batched streaming detokenization (Newly opened)
- [#1961](https://github.com/ROCm/ATOM/pull/1961) Fixes the OpenAI frontend so a `<` character in the answer no longer blocks the stream (Newly opened)

</details>

<details>
<summary>CI, build & plugins (8)</summary>

- [#1839](https://github.com/ROCm/ATOM/pull/1839) Upgrades vLLM to 0.26.1
- [#1840](https://github.com/ROCm/ATOM/pull/1840) Upgrades SGLang to v0.5.17
- [#1924](https://github.com/ROCm/ATOM/pull/1924) Upgrades vLLM to 0.27.1
- [#1939](https://github.com/ROCm/ATOM/pull/1939) Updates accuracy and performance test scripts for GLM-5
- [#1936](https://github.com/ROCm/ATOM/pull/1936) Fixes Kimi prefix caching accuracy documentation and bugs
- [#1922](https://github.com/ROCm/ATOM/pull/1922) Gates heavy CI runs with reusable workflows to save compute (Newly opened)
- [#1920](https://github.com/ROCm/ATOM/pull/1920) Skips duplicate heavy CI runs for the same PR SHA (Newly opened)
- [#1933](https://github.com/ROCm/ATOM/pull/1933) Updates CI to prefer commit-specific Aiter S3 manifests (Newly opened)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 4123a76f03b01670d75c07cf8551bff150faea239707c2f3d328604bd3b8822d -->
