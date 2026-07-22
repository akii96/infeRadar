# ATOM: PR digest (2026-07-01 to 2026-07-05)

_29 merged, 19 newly opened - source ROCm/ATOM, generated 2026-07-05T22:19:57Z_

## TL;DR
- **DeepSeek-V4** dominated this cycle, gaining Multi-Token Prediction (MTP) speculative decoding, Prefill Context Parallelism (PCP), and in-progress prefix caching.
- **Disaggregated serving (Mesh)** saw major architectural updates, notably enabling MultiConnector to run Prefill/Decode (P/D) alongside LMCache KV offloading.
- **MiniMax-M3** enablement advanced significantly, landing in `atom-vllm` with fused AllReduce + RMSNorm + quantization kernels.
- **API & Frontend** capabilities are expanding rapidly, with merged TLS support and newly opened PRs adding multi-model tool calling (GPT-OSS Harmony, Hermes, GLM, MiniMax).
- **Hardware-specific kernel fixes** landed for AMD architectures, including a K-cache staleness bypass for gfx950 and Triton GEMM gating for gfx1250.

## Most important PRs
- **[#1361](https://github.com/ROCm/ATOM/pull/1361)** (Merged) Implements Multi-Token Prediction (MTP) speculative decoding for DeepSeek-V4, significantly boosting decode throughput.
- **[#1220](https://github.com/ROCm/ATOM/pull/1220)** (Merged) Enables Prefill Context Parallelism (PCP) for DeepSeek-V4, allowing massive prompt processing to scale across multiple GPUs.
- **[#1406](https://github.com/ROCm/ATOM/pull/1406)** (Merged) Introduces MultiConnector support for disaggregated serving, allowing Prefill/Decode separation (mooncake/moriio) to run concurrently with LMCache KV offloading.
- **[#1408](https://github.com/ROCm/ATOM/pull/1408)** (Merged) Enables MiniMax-M3 support in `atom-vllm`, unblocking serving for the M3 architecture.
- **[#1423](https://github.com/ROCm/ATOM/pull/1423)** (Opened) Fixes a critical prefix-cache corruption bug in DeepSeek-V4 by implementing content-addressed paged Sliding Window Attention (SWA).

## More changes by area

<details>
<summary>Performance (2)</summary>

- [#1464](https://github.com/ROCm/ATOM/pull/1464) Adapts `BLOCK_K` dynamically for DeepSeek-V4 `csa_translate_pack`
- [#1465](https://github.com/ROCm/ATOM/pull/1465) Opened: Optimizes general model loading speed for MoE architectures

</details>

<details>
<summary>Kernels & attention (6)</summary>

- [#1355](https://github.com/ROCm/ATOM/pull/1355) Integrates Triton GEMM for quantized models
- [#1379](https://github.com/ROCm/ATOM/pull/1379) Fixes accuracy drop for long prompts in GLM5.1/5.2 via AITER MLA updates
- [#1290](https://github.com/ROCm/ATOM/pull/1290) Adds Gluon `pa_decode_sparse` from AITER for GFX12
- [#1434](https://github.com/ROCm/ATOM/pull/1434) Forces `buffer_load` for `qo_indptr` reads to bypass K-cache staleness on gfx950
- [#1432](https://github.com/ROCm/ATOM/pull/1432) Implements a viable workaround for MLA attention
- [#1468](https://github.com/ROCm/ATOM/pull/1468) Opened: Adds 3-state dump and guard to debug `cu_seqlens_q` staleness

</details>

<details>
<summary>MoE & quantization (4)</summary>

- [#1415](https://github.com/ROCm/ATOM/pull/1415) Fuses AllReduce, RMSNorm, and quantization for MiniMax-M3
- [#1466](https://github.com/ROCm/ATOM/pull/1466) Fixes FP8 indexer `cache_scale` per-layer aliasing in DeepSeek-V4
- [#1459](https://github.com/ROCm/ATOM/pull/1459) Opened: WIP MoE and quantization updates
- [#1458](https://github.com/ROCm/ATOM/pull/1458) Opened: Optimizes native GLM5.2 for FP8/MXFP4

</details>

<details>
<summary>Model support (3)</summary>

- [#1222](https://github.com/ROCm/ATOM/pull/1222) Supports `fused_qknorm_ar_rope` across all tensor parallel sizes for MiniMax-M2
- [#1418](https://github.com/ROCm/ATOM/pull/1418) Adds TBO support for M3-Eagle speculative decoding
- [#1436](https://github.com/ROCm/ATOM/pull/1436) Opened: Fixes full decode graph error for Qwen3.5

</details>

<details>
<summary>Parallelism & scheduling (2)</summary>

- [#1437](https://github.com/ROCm/ATOM/pull/1437) Gates prefill on full batch to protect decode phases in the scheduler
- [#1448](https://github.com/ROCm/ATOM/pull/1448) Opened: Refactors mesh worker registry into layered pools

</details>

<details>
<summary>API & serving (8)</summary>

- [#1129](https://github.com/ROCm/ATOM/pull/1129) Adds TLS support and formats the HTTP server
- [#1422](https://github.com/ROCm/ATOM/pull/1422) Reports prefix-cache hits via `prompt_tokens_details.cached_tokens`
- [#1454](https://github.com/ROCm/ATOM/pull/1454) Opened: Enables prefix caching for DeepSeek-V4 in `atom-vllm`
- [#1451](https://github.com/ROCm/ATOM/pull/1451) Opened: Fixes OOM issue for DeepSeek-V4 in `atom-vllm`
- [#1431](https://github.com/ROCm/ATOM/pull/1431) Opened: Adds tool calling support with GPT-OSS Harmony parser
- [#1443](https://github.com/ROCm/ATOM/pull/1443) Opened: Adds multi-model tool-call parsing and reasoning for GLM, MiniMax-M3, and DSML
- [#1427](https://github.com/ROCm/ATOM/pull/1427) Opened: Parses Hermes `<tool_call>{json}</tool_call>` formats
- [#1441](https://github.com/ROCm/ATOM/pull/1441) Opened: Cancels inference on client disconnect and fixes non-stream request leaks

</details>

<details>
<summary>Tests, CI & build (10)</summary>

- [#1244](https://github.com/ROCm/ATOM/pull/1244) Adds model Prefill/Decode benchmark workflow for ATOMesh
- [#1449](https://github.com/ROCm/ATOM/pull/1449) Adds ATOMesh nightly coverage for Kimi-K2.5 and MiniMax-M3
- [#1445](https://github.com/ROCm/ATOM/pull/1445) Bakes LMCache v0.4.5 (HIP c_ops) into `atom_image` for KV offload
- [#1430](https://github.com/ROCm/ATOM/pull/1430) Opened: Supports Qwen3-32B in SGLang accuracy CI on MI308 (gfx942)
- plus 6 more minor CI updates ([#1429](https://github.com/ROCm/ATOM/pull/1429), [#1452](https://github.com/ROCm/ATOM/pull/1452), [#1425](https://github.com/ROCm/ATOM/pull/1425), [#1450](https://github.com/ROCm/ATOM/pull/1450), [#1461](https://github.com/ROCm/ATOM/pull/1461), [#1457](https://github.com/ROCm/ATOM/pull/1457))

</details>

<details>
<summary>Docs (3)</summary>

- [#1453](https://github.com/ROCm/ATOM/pull/1453) Updates README news for ATOM blogs and MiniMax-M3
- [#1424](https://github.com/ROCm/ATOM/pull/1424) Adds DeepSeek-V4 blog post
- [#1456](https://github.com/ROCm/ATOM/pull/1456) Opened: Adds trace breakdown skill documentation

</details>

<details>
<summary>Bugfixes (4)</summary>

- [#1444](https://github.com/ROCm/ATOM/pull/1444) Emits one spec-decode row per decode sequence in MTP to fix IndexError
- [#1433](https://github.com/ROCm/ATOM/pull/1433) Gates Triton `batched_gemm_bf16` to gfx1250 and falls back to einsum for DeepSeek-V4
- [#1460](https://github.com/ROCm/ATOM/pull/1460) Fixes int32 overflow for DeepSeek-V4 kernels
- [#1455](https://github.com/ROCm/ATOM/pull/1455) Opened: Fixes greedy sampling and sets seed globally

</details>

<details>
<summary>Refactors (1)</summary>

- [#1447](https://github.com/ROCm/ATOM/pull/1447) Opened: Removes legacy proxy, updates docs, and enhances distributed mesh scripts

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0533687f8cf44f5623cfec7f49248a598129df7059642ae1213567febca4cfe3 -->
