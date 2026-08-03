# ATOM: PR digest (2026-07-29 to 2026-08-02)

_27 merged, 24 newly opened - source ROCm/ATOM, generated 2026-08-02T22:27:14Z_

## TL;DR
*   **Frontier Models**: DeepSeek-V4, Kimi-K3, and GLM-5.2 dominated this cycle. Kimi-K3 received day-0 main support and speculative decoding (dspark), while DeepSeek-V4 saw major API/tool-parsing additions and in-progress work on CSA prefix-state caching.
*   **Architecture & Distributed**: Massive architectural shifts landed for distributed inference, notably the merging of Chunked Pipeline Parallelism combined with Prefill-Decode (PD) disaggregation and ATOMesh support.
*   **Performance Wins**: Significant performance improvements merged, including a 2.2x speedup for cold weight loading and highly optimized MLA DCP (Distributed Context Parallelism) utilizing chunked prefill and FP8 KV caching.
*   **Speculative Decoding & MTP**: Multi-Token Prediction (MTP) is a major focus, with EAGLE3 support added for MiniMax-M3, and massive in-progress PRs bringing MTP to both GLM-5.2 and MiniMax-M3.
*   **Overall Direction**: The engine is rapidly maturing its distributed prefill/decode disaggregation and speculative decoding capabilities to support the massive context and throughput demands of the newest frontier models.

## Most important PRs
*   **[#1552](https://github.com/ROCm/ATOM/pull/1552)** introduces Chunked Pipeline Parallelism and Prefill-Decode (PD) disaggregation for ATOMesh. This is a massive architectural upgrade that allows separating compute-heavy prefill from memory-bound decode phases across distributed meshes.
*   **[#1718](https://github.com/ROCm/ATOM/pull/1718)** lands main support for the Kimi-K3 model. This brings full Multi-Head Latent Attention (MLA) and MoE compatibility for the new architecture, establishing day-0 readiness.
*   **[#1701](https://github.com/ROCm/ATOM/pull/1701)** optimizes MLA for Distributed Context Parallelism (DCP). By enabling prefix caching, chunked prefill, and FP8 KV cache, it significantly reduces memory pressure and latency for long-context workloads.
*   **[#1767](https://github.com/ROCm/ATOM/pull/1767)** delivers a 2.2x speedup for cold weight loading and a 1.7x speedup for warm loads. This drastically cuts down model initialization and recovery times across the board.
*   **[#1760](https://github.com/ROCm/ATOM/pull/1760)** (in-progress) brings Multi-Token Prediction (MTP) support to GLM-5.2. This nearly 5,000-line change will enable highly efficient speculative decoding for the GLM family.

## More changes by area

<details>
<summary>Model support (7)</summary>

- [#1741](https://github.com/ROCm/ATOM/pull/1741) adds DeepSeek-V4 native OpenAI/Anthropic/Responses API and DSML tool parser
- [#1733](https://github.com/ROCm/ATOM/pull/1733) implements Kimi-K3 dspark speculative decoding support
- [#1735](https://github.com/ROCm/ATOM/pull/1735) supports Kimi-K3 on vLLM plugin mode
- [#1518](https://github.com/ROCm/ATOM/pull/1518) adds EAGLE3 speculative decoding support for MiniMax-M3
- [#1757](https://github.com/ROCm/ATOM/pull/1757) (in-progress) enables MiniMax-M3 MTP and fixes an M3 error caused by an SGLang update
- [#1747](https://github.com/ROCm/ATOM/pull/1747) (in-progress) supports the GLM-5.2 tool call parser
- [#1738](https://github.com/ROCm/ATOM/pull/1738) (in-progress) adds support for the Qwen3.5x model family

</details>

<details>
<summary>Kernels & attention (5)</summary>

- [#1759](https://github.com/ROCm/ATOM/pull/1759) (in-progress) supports Mamba prefix caching
- [#1769](https://github.com/ROCm/ATOM/pull/1769) (in-progress) implements DeepSeek-V4 CSA prefix-state cache on SWA (native, no arena)
- [#1765](https://github.com/ROCm/ATOM/pull/1765) (in-progress) adds Triton and Gluon support for EP+DP attention on GFX9 and GFX12
- [#1762](https://github.com/ROCm/ATOM/pull/1762) (in-progress) supports GLM-5.2 DP attention
- [#1723](https://github.com/ROCm/ATOM/pull/1723) (in-progress) adds block-level DeepSeek-V4 attention tests using real DeepseekV4Attention

</details>

<details>
<summary>MoE & quantization (5)</summary>

- [#1737](https://github.com/ROCm/ATOM/pull/1737) enables FP8 2-buffer KV transfer for PD disaggregation on DeepSeek-V4
- [#1749](https://github.com/ROCm/ATOM/pull/1749) (in-progress) implements layer-by-layer weight quantization
- [#1752](https://github.com/ROCm/ATOM/pull/1752) (in-progress) enables dual stream for shared experts and specific fusions for Kimi-K3
- [#1739](https://github.com/ROCm/ATOM/pull/1739) (in-progress) fixes DeepSeek-V4 FP8 block128 quantization on MI308 hardware
- [#1731](https://github.com/ROCm/ATOM/pull/1731) (in-progress) fixes the DeepSeek-V4 FP8 compressor for vLLM and SGLang plugins

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#1647](https://github.com/ROCm/ATOM/pull/1647) fixes the scheduler's PD decode admission cap and remote-KV backpressure
- [#1746](https://github.com/ROCm/ATOM/pull/1746) (in-progress) switches DCP decode to persistent PA and makes DCP compatible with MTP
- [#1743](https://github.com/ROCm/ATOM/pull/1743) (in-progress) adds MTP support for blocksizes other than 1

</details>

<details>
<summary>Performance (3)</summary>

- [#1755](https://github.com/ROCm/ATOM/pull/1755) (in-progress) adds a fake Expert Parallel Load Balancer (eplb) for performance testing
- [#1758](https://github.com/ROCm/ATOM/pull/1758) (in-progress) optimizes Dspark piecewise dummy decode to avoid eager fallbacks and improve low-concurrency performance
- [#1766](https://github.com/ROCm/ATOM/pull/1766) (in-progress) enables QK norm RoPE cache fusion for dense models like Qwen3

</details>

<details>
<summary>Bugfixes (12)</summary>

- [#1768](https://github.com/ROCm/ATOM/pull/1768) fixes an issue where the offline output thread dies on the first streamed token
- [#1764](https://github.com/ROCm/ATOM/pull/1764) fixes MTP by recycling the post-final-norm hidden states between draft steps
- [#1717](https://github.com/ROCm/ATOM/pull/1717) validates cached accuracy model shards for SGLang
- [#1750](https://github.com/ROCm/ATOM/pull/1750) fixes Kimi-K3 to run KDA prefill recurrently on gfx1250
- [#1729](https://github.com/ROCm/ATOM/pull/1729) adds a fallback for unwritable HuggingFace cache roots in SGLang
- [#1744](https://github.com/ROCm/ATOM/pull/1744) fixes a Dspark piecewise cudagraph accuracy issue at 512 concurrency
- [#1753](https://github.com/ROCm/ATOM/pull/1753) fixes the SGLang HuggingFace cache fallback mechanism
- [#1721](https://github.com/ROCm/ATOM/pull/1721) fixes GLM-5.2 FP8 MI308 CI by removing online_quant
- [#1727](https://github.com/ROCm/ATOM/pull/1727) (in-progress) applies a large batch of fixes to pass Kimi-K3 KVV validation
- [#1725](https://github.com/ROCm/ATOM/pull/1725) (in-progress) fixes lm_cache write back
- [#1742](https://github.com/ROCm/ATOM/pull/1742) (in-progress) recycles post-final-norm hidden states between MTP draft steps
- [#1751](https://github.com/ROCm/ATOM/pull/1751) (in-progress) forwards extra args in patched_inline_call for torch _dynamo compatibility

</details>

<details>
<summary>API & serving (1)</summary>

- [#1359](https://github.com/ROCm/ATOM/pull/1359) adds a dtype option to the LayerNorm class

</details>

<details>
<summary>CI & build (9)</summary>

- [#1675](https://github.com/ROCm/ATOM/pull/1675) adds CI cases and recipes for the GLM-5.2 agentic benchmark
- [#1740](https://github.com/ROCm/ATOM/pull/1740) (in-progress) supports swebench_lite precision validation
- [#1730](https://github.com/ROCm/ATOM/pull/1730) supports the Crusoe cluster and aligns the bench_serving script on SA
- [#1761](https://github.com/ROCm/ATOM/pull/1761) corrects ATOMesh speculative token arguments in CI
- [#1726](https://github.com/ROCm/ATOM/pull/1726) adds an Agentic Trace item under ISL/OSL
- [#1745](https://github.com/ROCm/ATOM/pull/1745) adds ATOMesh DeepSeek-V4 MTP cases
- [#1728](https://github.com/ROCm/ATOM/pull/1728) updates SGLang and vLLM benchmark schedules
- [#1734](https://github.com/ROCm/ATOM/pull/1734) updates the vLLM benchmark nightly schedule
- [#1763](https://github.com/ROCm/ATOM/pull/1763) (in-progress) adds a weekly full ATOMesh benchmark schedule

</details>

<details>
<summary>Docs (1)</summary>

- [#1732](https://github.com/ROCm/ATOM/pull/1732) adds the Kimi-K3 Day 0 AMD developer article to the News section

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: ee15112678ff4644bc30ab5d05ae77599d2c431b3fe28d2984ba7b1487aa6d94 -->
