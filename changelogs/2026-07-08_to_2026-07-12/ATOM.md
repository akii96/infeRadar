# ATOM: PR digest (2026-07-08 to 2026-07-12)

_46 merged, 16 newly opened - source ROCm/ATOM, generated 2026-07-12T22:19:54Z_

## TL;DR
- **DeepSeek-V4** was the primary focus, landing critical fixes for prefix-cache corruption and piecewise cudagraph support, alongside in-progress work for native APIs and PCP MoE-Merge optimizations.
- **GLM-5.2** saw significant movement with merged FP8/MXFP4 optimizations and vLLM plugin support, plus newly opened work to enable Multi-Token Prediction (MTP).
- **Distributed execution** is evolving rapidly, highlighted by a massive in-progress architectural shift to support Chunked Pipeline Parallelism and Prefill-Decode (PD) Disaggregation for ATOMesh.
- **MoE and Quantization** pipelines are being refined for AMD hardware, notably with merged Triton GGUU a8w4 MoE decode paths and incoming GUGU activation+quantization fusion.
- **Overall Direction**: The engine is heavily prioritizing advanced serving features (speculative decoding via EAGLE3, MTP, prefix caching) and distributed mesh stability for next-gen MoE models on MI300/MI350 series hardware.

## Most important PRs
- **[#1423](https://github.com/ROCm/ATOM/pull/1423) fixes prefix-cache corruption in DeepSeek-V4 via content-addressed paged SWA.** This resolves critical memory corruption during distributed execution by ensuring sliding window attention correctly maps cached tokens.
- **[#1552](https://github.com/ROCm/ATOM/pull/1552) introduces Chunked Pipeline Parallelism and Prefill-Decode (PD) Disaggregation for ATOMesh.** This massive newly opened architectural change allows separating prefill and decode phases across different nodes, significantly improving cluster utilization for large models.
- **[#1531](https://github.com/ROCm/ATOM/pull/1531) enables Multi-Token Prediction (MTP) for GLM-5.2 in the vLLM plugin.** This in-progress feature wires up speculative decoding and MLA components to support GLM's MTP draft generation, boosting decode throughput.
- **[#1541](https://github.com/ROCm/ATOM/pull/1541) enables piecewise cudagraphs for non-speculative DeepSeek-V4.** By chunking the graph capture, this reduces CPU overhead and latency during decode steps without hitting memory limits on large MoE models.
- **[#1553](https://github.com/ROCm/ATOM/pull/1553) enables PCP MoE-Merge and Token-Based Optimization (TBO) for DeepSeek-V4.** This newly opened PR optimizes MoE routing and dispatch overhead by merging expert executions and dynamically adjusting based on token density.

## More changes by area

<details>
<summary>MoE & quantization (6)</summary>

- [#1458](https://github.com/ROCm/ATOM/pull/1458) optimize GLM-5.2 FP8/MXFP4
- [#1547](https://github.com/ROCm/ATOM/pull/1547) implement Triton GGUU a8w4 MoE decode path
- [#1409](https://github.com/ROCm/ATOM/pull/1409) align Kimi input norm quantization with attention quantization
- [#1527](https://github.com/ROCm/ATOM/pull/1527) fix DeepSeek-V4 fused shared expert mapping
- [#1548](https://github.com/ROCm/ATOM/pull/1548) fix DeepSeek-V4 MTP fused shared expert mapping
- [#1570](https://github.com/ROCm/ATOM/pull/1570) wire GUGU activation+quantization fusion into Triton decode (newly opened)

</details>

<details>
<summary>Model support (5)</summary>

- [#1496](https://github.com/ROCm/ATOM/pull/1496) support Llama-405B quantization type
- [#1513](https://github.com/ROCm/ATOM/pull/1513) support GLM-5.2 in vLLM plugin mode
- [#1543](https://github.com/ROCm/ATOM/pull/1543) add Qwen3.5 35B PTPC FP8 support
- [#1518](https://github.com/ROCm/ATOM/pull/1518) support EAGLE3 speculative decoding for MiniMax-M3 in vLLM-ATOM (newly opened)
- [#1564](https://github.com/ROCm/ATOM/pull/1564) add MiniMax-M3 FP8 and EAGLE support to ATOM SGLang (newly opened)

</details>

<details>
<summary>API & serving (4)</summary>

- [#1510](https://github.com/ROCm/ATOM/pull/1510) implement automatic orphan reaping to prevent stale IPC/VRAM pinning on parent exit
- [#1454](https://github.com/ROCm/ATOM/pull/1454) enable prefix cache for DeepSeek-V4 in ATOM-vLLM
- [#1563](https://github.com/ROCm/ATOM/pull/1563) implement DeepSeek-V4 native OpenAI/Anthropic API and DSML tool parser (newly opened)
- [#1562](https://github.com/ROCm/ATOM/pull/1562) abort engine requests and free leaked KV on client disconnect (newly opened)

</details>

<details>
<summary>Performance (3)</summary>

- [#1537](https://github.com/ROCm/ATOM/pull/1537) revert changes to stabilize Data Parallel (DP) performance
- [#1542](https://github.com/ROCm/ATOM/pull/1542) skip prefill Token-Based Optimization (TBO) below a minimum token count
- [#1514](https://github.com/ROCm/ATOM/pull/1514) enable PCP for DSA models (newly opened)

</details>

<details>
<summary>Kernels & attention (2)</summary>

- [#1498](https://github.com/ROCm/ATOM/pull/1498) optimize DeepSeek-V4 sparse prefill attention Triton kernel
- [#1509](https://github.com/ROCm/ATOM/pull/1509) implement `pa_prefill_sparse` for Gluon on GFX12

</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

- [#1447](https://github.com/ROCm/ATOM/pull/1447) remove legacy proxy and enhance distributed mesh scripts

</details>

<details>
<summary>Hardware & arch (2)</summary>

- [#1540](https://github.com/ROCm/ATOM/pull/1540) update shuffle weight for GFX1250
- [#1550](https://github.com/ROCm/ATOM/pull/1550) fix GFX950 specific issues (newly opened)

</details>

<details>
<summary>Bugfixes (7)</summary>

- [#1517](https://github.com/ROCm/ATOM/pull/1517) fix DPA KV transfer error on Spur cluster
- [#1505](https://github.com/ROCm/ATOM/pull/1505) fix DPA KV transfer error on Spur cluster
- [#1480](https://github.com/ROCm/ATOM/pull/1480) fix SGLang MiniMax-M3 CUDA graph capture problem
- [#1560](https://github.com/ROCm/ATOM/pull/1560) fix DSA indexer single-source decode_lens to prevent illegal memory access
- [#1526](https://github.com/ROCm/ATOM/pull/1526) align TBO v4_batch_id_per_token buffer to int32 for DeepSeek-V4
- [#1559](https://github.com/ROCm/ATOM/pull/1559) fix AITER/MLA quantization bugs (newly opened)
- [#1551](https://github.com/ROCm/ATOM/pull/1551) fix radix-cache crash on MiniMax-M3 (newly opened)

</details>

<details>
<summary>Refactors (2)</summary>

- [#1544](https://github.com/ROCm/ATOM/pull/1544) general code refactor
- [#1522](https://github.com/ROCm/ATOM/pull/1522) deduplicate prefill density check and drop dead threshold attribute

</details>

<details>
<summary>Docs (3)</summary>

- [#1539](https://github.com/ROCm/ATOM/pull/1539) add review-pr Claude Code skill for ATOM PRs
- [#1566](https://github.com/ROCm/ATOM/pull/1566) add MXFP4 intermediate variable and scheduler delay advice for Kimi-K2
- [#1549](https://github.com/ROCm/ATOM/pull/1549) update review-pr skill v2 with dispatch gap rules and P5 timing errors (newly opened)

</details>

<details>
<summary>CI & build (22)</summary>

- [#1475](https://github.com/ROCm/ATOM/pull/1475) add Spur cluster benchmark support to ATOMesh
- [#1516](https://github.com/ROCm/ATOM/pull/1516) gate heavy PR tests by approval or label
- [#1555](https://github.com/ROCm/ATOM/pull/1555) improve ATOMesh dashboard visualization
- [#1557](https://github.com/ROCm/ATOM/pull/1557) gate MTP acceptance rate alongside gsm8k accuracy
- plus 18 more minor CI updates for benchmarks, permissions, and nightly releases ([#1535](https://github.com/ROCm/ATOM/pull/1535), [#1556](https://github.com/ROCm/ATOM/pull/1556), [#1512](https://github.com/ROCm/ATOM/pull/1512), [#1519](https://github.com/ROCm/ATOM/pull/1519), [#1538](https://github.com/ROCm/ATOM/pull/1538), [#1524](https://github.com/ROCm/ATOM/pull/1524), [#1567](https://github.com/ROCm/ATOM/pull/1567), [#1523](https://github.com/ROCm/ATOM/pull/1523), [#1561](https://github.com/ROCm/ATOM/pull/1561), [#1536](https://github.com/ROCm/ATOM/pull/1536), [#1554](https://github.com/ROCm/ATOM/pull/1554), [#1533](https://github.com/ROCm/ATOM/pull/1533), [#1508](https://github.com/ROCm/ATOM/pull/1508), [#1521](https://github.com/ROCm/ATOM/pull/1521), [#1546](https://github.com/ROCm/ATOM/pull/1546), [#1528](https://github.com/ROCm/ATOM/pull/1528), [#1530](https://github.com/ROCm/ATOM/pull/1530), [#1529](https://github.com/ROCm/ATOM/pull/1529))

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 67b07efa4d6e0fd7accdfee8dc11362e9c8d83fc07e9a7eef24cbea4d2f09545 -->
