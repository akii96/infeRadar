# ATOM: PR digest (2026-06-28 to 2026-07-02)

_36 merged, 24 newly opened - source ROCm/ATOM, generated 2026-07-02T11:58:36Z_

## TL;DR
- **DeepSeek-V4 dominated this cycle**, receiving major performance upgrades including merged Multi-Token Prediction (MTP) speculative decoding and Prefill Context Parallelism (PCP), alongside in-progress work for DSpark spec decode and FP8 KV caching.
- **MiniMax-M3 enablement accelerated**, with significant plugin support added for both vLLM and SGLang, including TBO support and fused AllReduce + RMSNorm + quantization kernels.
- **Distributed inference and offloading expanded**, highlighted by a massive new standalone LMCache CPU/NVMe connector to handle KV-cache spilling, plus in-progress MultiConnector support for disaggregated Prefill/Decode.
- **Frontend tool-calling matured**, adding native parsing and support for Qwen3, Hermes, and an in-progress GPT-OSS Harmony parser.
- **Hardware-specific tuning continued**, featuring DP+EP fixes for MI308X (gfx942), Triton batched GEMM gating for MI455 (gfx1250), and cache-stale bypasses for gfx950.

## Most important PRs
- **[#1318](https://github.com/ROCm/ATOM/pull/1318)** (Merged) introduces a standalone LMCache CPU/NVMe KV-cache offload connector. This enables massive context handling by spilling KV blocks to host memory or NVMe storage when GPU VRAM is exhausted.
- **[#1361](https://github.com/ROCm/ATOM/pull/1361)** (Merged) implements Multi-Token Prediction (MTP) speculative decoding for DeepSeek-V4 in the SGLang plugin. This significantly accelerates decode throughput by leveraging DeepSeek's native MTP heads.
- **[#1220](https://github.com/ROCm/ATOM/pull/1220)** (Merged) enables Prefill Context Parallelism (PCP) for DeepSeek-V4. This allows distributing massive prompt prefill phases across multiple GPUs to reduce latency and memory pressure.
- **[#1414](https://github.com/ROCm/ATOM/pull/1414)** (Newly opened) adds DSpark speculative decoding support for DeepSeek-V4. This in-progress work will provide an alternative, highly optimized speculation path for the model.
- **[#1423](https://github.com/ROCm/ATOM/pull/1423)** (Newly opened) fixes a critical prefix-cache corruption issue in DeepSeek-V4 by implementing content-addressed paged Sliding Window Attention (SWA).

## More changes by area

<details>
<summary>Kernels & attention (4)</summary>

- [#1388](https://github.com/ROCm/ATOM/pull/1388) (Newly opened) fuses AllReduce, RMSNorm, and FP8 quantization into a single kernel for DeepSeek and Kimi models to reduce memory bandwidth overhead
- [#1421](https://github.com/ROCm/ATOM/pull/1421) (Newly opened) wires split-K GEMM prezeroing into MLA and MoE decode paths
- [#1290](https://github.com/ROCm/ATOM/pull/1290) (Merged) adds the gluon `pa_decode_sparse` kernel from AITER for GFX12 architectures
- [#1389](https://github.com/ROCm/ATOM/pull/1389) (Newly opened) implements version 2 of the FP8/mixed-precision MLA dispatch logic

</details>

<details>
<summary>MoE & quantization (4)</summary>

- [#1415](https://github.com/ROCm/ATOM/pull/1415) (Merged) enables AllReduce + RMSNorm + quantization fusion for MiniMax-M3
- [#1365](https://github.com/ROCm/ATOM/pull/1365) (Merged) aligns online and offline quantization logic for MoE layers
- [#1403](https://github.com/ROCm/ATOM/pull/1403) (Newly opened) enables FP8 KV cache support for DeepSeek-V4
- [#1411](https://github.com/ROCm/ATOM/pull/1411) (Newly opened) WIP updates to quantization utilities

</details>

<details>
<summary>Model support (8)</summary>

- [#1408](https://github.com/ROCm/ATOM/pull/1408) (Newly opened) enables MiniMax-M3 support in the ATOM vLLM plugin
- [#1395](https://github.com/ROCm/ATOM/pull/1395) (Newly opened) adds MiniMax-M3 support to the SGLang plugin
- [#1373](https://github.com/ROCm/ATOM/pull/1373) (Merged) adds TBO (Tree-Based Optimization) support for MiniMax-M3
- [#1418](https://github.com/ROCm/ATOM/pull/1418) (Merged) adds TBO support specifically for the MiniMax-M3 Eagle variant
- [#1416](https://github.com/ROCm/ATOM/pull/1416) (Merged) adds Qwen3 dense model support to the SGLang plugin
- [#1410](https://github.com/ROCm/ATOM/pull/1410) (Newly opened) enables MiniMax-M3 execution on gfx1250 (MI455)
- [#1166](https://github.com/ROCm/ATOM/pull/1166) (Merged) enables multi-stream execution for DeepSeek-V4 in the vLLM plugin
- [#1196](https://github.com/ROCm/ATOM/pull/1196) (Merged) optimizes the metadata build process for DeepSeek-V4

</details>

<details>
<summary>Parallelism & distributed (2)</summary>

- [#1101](https://github.com/ROCm/ATOM/pull/1101) (Merged) adds Data Parallel (DP) and Expert Parallel (EP) support to the vLLM plugin
- [#1406](https://github.com/ROCm/ATOM/pull/1406) (Newly opened) introduces a MultiConnector to run Prefill/Decode disaggregation (Mooncake/Moriio) alongside LMCache offloading

</details>

<details>
<summary>API & serving (5)</summary>

- [#1431](https://github.com/ROCm/ATOM/pull/1431) (Newly opened) adds tool-calling support using the GPT-OSS Harmony parser
- [#1319](https://github.com/ROCm/ATOM/pull/1319) (Merged) adds tool-call support for Qwen3 (Coder and XML variants)
- [#1427](https://github.com/ROCm/ATOM/pull/1427) (Newly opened) adds a feature to parse Hermes `<tool_call>{json}</tool_call>` formats
- [#1422](https://github.com/ROCm/ATOM/pull/1422) (Merged) exposes prefix-cache hit metrics via `prompt_tokens_details.cached_tokens`
- [#1393](https://github.com/ROCm/ATOM/pull/1393) (Merged) enables DeepSeek-V4 prefix caching in the SGLang ATOM plugin

</details>

<details>
<summary>Bugfixes (15)</summary>

- [#1428](https://github.com/ROCm/ATOM/pull/1428) (Newly opened) fixes DeepSeek-V4 tool calls, client-disconnect cancellation, and a non-stream memory leak
- [#1401](https://github.com/ROCm/ATOM/pull/1401) (Merged) fixes DeepSeek-V4 DP+EP execution on gfx942 (MI308X)
- [#1433](https://github.com/ROCm/ATOM/pull/1433) (Merged) gates Triton `batched_gemm_bf16` to gfx1250 and forces einsum fallback on other architectures
- [#1434](https://github.com/ROCm/ATOM/pull/1434) (Merged) forces `buffer_load` for `qo_indptr` reads to bypass stale K-cache on gfx950
- [#1368](https://github.com/ROCm/ATOM/pull/1368) (Merged) fixes the transfer of the MiniMax-M3 sparse indexer-key cache during disaggregation
- [#1409](https://github.com/ROCm/ATOM/pull/1409) (Newly opened) aligns input norm quantization with attention quantization for Kimi models
- [#1391](https://github.com/ROCm/ATOM/pull/1391) (Newly opened) prevents GLM-5.2-FP8 from using out-of-cudagraph buffers unnecessarily
- [#1381](https://github.com/ROCm/ATOM/pull/1381) (Merged) raises `RLIMIT_NOFILE` at server startup to survive high connection concurrency
- [#1394](https://github.com/ROCm/ATOM/pull/1394) (Merged) raises `RLIMIT_NOFILE` in `benchmark_serving` for high concurrency testing
- [#1437](https://github.com/ROCm/ATOM/pull/1437) (Newly opened) gates prefill scheduling on full batches to protect decode latency
- [#1436](https://github.com/ROCm/ATOM/pull/1436) (Newly opened) fixes a full decode graph error for Qwen3.5
- [#1412](https://github.com/ROCm/ATOM/pull/1412) (Newly opened) adapts the plugin to RTP-LLM's `PyAttentionInputs` host/device field rename
- [#1382](https://github.com/ROCm/ATOM/pull/1382) (Merged) adds a guard check for MLA attention bounds
- [#1384](https://github.com/ROCm/ATOM/pull/1384) (Merged) fixes token bounds conversion in sparse MLA
- [#1432](https://github.com/ROCm/ATOM/pull/1432) (Merged) applies a viable workaround for an MLA attention edge case

</details>

<details>
<summary>CI, Tests & Docs (17)</summary>

- [#1244](https://github.com/ROCm/ATOM/pull/1244) (Merged) adds a new model Prefill/Decode benchmark workflow for mesh topologies
- [#1385](https://github.com/ROCm/ATOM/pull/1385) (Merged) de-inlines the native CI foundation and adds a unit-test gate
- [#1402](https://github.com/ROCm/ATOM/pull/1402) (Newly opened) adds a block-level GPT-OSS attention test using real OAIAttention
- [#1386](https://github.com/ROCm/ATOM/pull/1386) (Newly opened) updates docs to add gfx1200 (Navi 44) alongside gfx1201 for RDNA4 support
- [#1371](https://github.com/ROCm/ATOM/pull/1371) (Merged) adds indexer cache and online quantization for MiniMax-M3 in the ATOM benchmark
- [#1387](https://github.com/ROCm/ATOM/pull/1387) (Newly opened) updates environment variable recipes for Kimi and MiniMax
- [#1424](https://github.com/ROCm/ATOM/pull/1424) (Merged) adds the v4 blog post to documentation
- plus 10 more minor CI updates ([#1429](https://github.com/ROCm/ATOM/pull/1429), [#1405](https://github.com/ROCm/ATOM/pull/1405), [#1404](https://github.com/ROCm/ATOM/pull/1404), [#1420](https://github.com/ROCm/ATOM/pull/1420), [#1413](https://github.com/ROCm/ATOM/pull/1413), [#1425](https://github.com/ROCm/ATOM/pull/1425), [#1397](https://github.com/ROCm/ATOM/pull/1397), [#1390](https://github.com/ROCm/ATOM/pull/1390), [#1399](https://github.com/ROCm/ATOM/pull/1399), [#1430](https://github.com/ROCm/ATOM/pull/1430)) improving benchmark schedules, container cleanup, and adding specific model targets (GLM5.1, Qwen3-32B) to accuracy runs.

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: d27c7fc1a6a1cb0e04e8a13af370e12728333fb967f1f4463abaf0b80f7d77dc -->
