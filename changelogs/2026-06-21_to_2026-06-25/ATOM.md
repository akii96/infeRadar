# ATOM: PR digest (2026-06-21 to 2026-06-25)

_41 merged, 20 newly opened - source ROCm/ATOM, generated 2026-06-25T12:00:17Z_

## TL;DR
*   **Model Focus:** Massive push for MiniMax-M3 enablement, including native MXFP4/MXFP8 support, Gluon Paged Attention, and Eagle speculative decoding optimizations. DeepSeek (v4/R1) and Qwen (3/3.5/3.6) also saw significant attention and accuracy fixes.
*   **Attention & Kernels:** Major upgrades to attention backends, notably adding RTP-LLM plugin support for GLM5-FP8, enabling TBO decode for DeepSeek v4, and replacing einsum with Triton BMM for DeepSeek v4.
*   **Hardware Expansion:** Expanding support for AMD's newer architectures, bringing Mistral-3 and Qwen3-8B-FP8 to RDNA4 (gfx1201) and Qwen3.6 to RDNA3.5 (gfx1151) via native Triton attention.
*   **Memory & Distributed:** Significant architectural work on memory offloading, highlighted by an in-progress standalone LMCache CPU/NVMe KV-offload connector and merged NUMA-aware CPU/memory binding for Prompt Disaggregation (PD).

## Most important PRs
*   **[#1289](https://github.com/ROCm/ATOM/pull/1289)** Integrates GLM5 into the RTP-LLM plugin, adding FP8 quantization and Multi-Head Latent Attention (MLA) support to enable high-performance serving for the GLM5 family.
*   **[#1305](https://github.com/ROCm/ATOM/pull/1305)** Introduces native MXFP4 support for the MiniMax-M3 model via the AITer backend, unlocking highly quantized MoE execution and significantly reducing memory bandwidth requirements.
*   **[#1318](https://github.com/ROCm/ATOM/pull/1318)** (Newly opened) Proposes a standalone LMCache connector to offload KV caches to CPU or NVMe, which will drastically expand effective context capacity for memory-bound deployments.
*   **[#811](https://github.com/ROCm/ATOM/pull/811)** Brings native Triton attention support to RDNA4 (gfx1201), enabling Mistral-3 and Qwen3-8B-FP8 execution on the new hardware architecture.
*   **[#1334](https://github.com/ROCm/ATOM/pull/1334)** Implements a Gluon-based Paged Attention kernel with a shuffle layout specifically optimized for MiniMax-M3's memory access patterns, improving overall attention throughput.

## More changes by area

<details>
<summary>Performance & Speculative Decoding (7)</summary>

- [#1320](https://github.com/ROCm/ATOM/pull/1320) [Merged] Optimizes Eagle speculative decoding for MiniMax-M3
- [#1303](https://github.com/ROCm/ATOM/pull/1303) [Merged] Further ATOM Eagle optimizations for MiniMax-M3
- [#1333](https://github.com/ROCm/ATOM/pull/1333) [Opened] Enables and optimizes the MiniMax-M3 Eagle path
- [#1331](https://github.com/ROCm/ATOM/pull/1331) [Merged] Enables Eagle3 MHA draft KV cache transfer for Prompt Disaggregation (PD)
- [#1340](https://github.com/ROCm/ATOM/pull/1340) [Merged] Adds NUMA-aware CPU/memory binding for PD Single Node optimization
- [#1308](https://github.com/ROCm/ATOM/pull/1308) [Merged] Supports PD disaggregation on a single node
- [#1304](https://github.com/ROCm/ATOM/pull/1304) [Merged] Cleans up MoE implementation and improves performance

</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#1275](https://github.com/ROCm/ATOM/pull/1275) [Merged] Supports TBO decode in DeepSeek v4
- [#1270](https://github.com/ROCm/ATOM/pull/1270) [Merged] Replaces einsum with Triton BMM for DeepSeek v4
- [#1301](https://github.com/ROCm/ATOM/pull/1301) [Merged] Adds AITer MLA test implementations
- [#1326](https://github.com/ROCm/ATOM/pull/1326) [Merged] Supports `local_argmax_pack` kernel for MiniMax-M3
- [#1343](https://github.com/ROCm/ATOM/pull/1343) [Merged] Fixes v4 prefill SWA write in attention kernels
- [#1252](https://github.com/ROCm/ATOM/pull/1252) [Merged] Skips sparse MLA fast metadata for unsupported heads in SGLang
- [#1309](https://github.com/ROCm/ATOM/pull/1309) [Merged] Sets sink to FP32 for prompt-stage decode ASM
- [#1269](https://github.com/ROCm/ATOM/pull/1269) [Merged] Enables PA ASM for MHA decode
- [#1348](https://github.com/ROCm/ATOM/pull/1348) [Merged] Fixes missing block table attribute in `AttentionMetaData`
- [#1354](https://github.com/ROCm/ATOM/pull/1354) [Opened] Supports index cache for MiniMax-M3 in AITer backend
- [#1314](https://github.com/ROCm/ATOM/pull/1314) [Opened] Implements Qwen3.5/3.6 BF16 on RDNA3.5 via native Triton attention
- [#1324](https://github.com/ROCm/ATOM/pull/1324) [Opened] Enables TBO for MiniMax-M3
- [#1345](https://github.com/ROCm/ATOM/pull/1345) [Opened] Routes prefix-cache-hit prefill through sink ASM MHA kernel

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#1335](https://github.com/ROCm/ATOM/pull/1335) [Merged] Adds MXFP8 support for MiniMax-M3 MoE
- [#1297](https://github.com/ROCm/ATOM/pull/1297) [Merged] Updates ATOM shuffle scale for MoE
- [#1336](https://github.com/ROCm/ATOM/pull/1336) [Opened] Implements low-bit expert parallelism (EP)
- [#1337](https://github.com/ROCm/ATOM/pull/1337) [Opened] Adds online INT8 W8A8 for Qwen3.6 27B/35B on RDNA3.5 with MTP
- [#1341](https://github.com/ROCm/ATOM/pull/1341) [Opened] Adds a new backend interface for MoE
- [#1353](https://github.com/ROCm/ATOM/pull/1353) [Opened] Fixes weight scale shape conversion for quantization

</details>

<details>
<summary>Model support & API (6)</summary>

- [#1126](https://github.com/ROCm/ATOM/pull/1126) [Merged] Documents DeepSeek R1 MXFP4 v2 recipe
- [#1317](https://github.com/ROCm/ATOM/pull/1317) [Opened] Adds base MiniMax-M3 (MXFP4/AttnFP8) model support
- [#1342](https://github.com/ROCm/ATOM/pull/1342) [Opened] Enables MiniMax-M3 vLLM plugin path
- [#1319](https://github.com/ROCm/ATOM/pull/1319) [Opened] Adds tool-call support for Qwen3 (coder/xml) in the frontend
- [#1310](https://github.com/ROCm/ATOM/pull/1310) [Opened] Supports model runner v2 on Qwen-next
- [#1344](https://github.com/ROCm/ATOM/pull/1344) [Opened] Gates AR+RMSNorm fusion on environment variable for MiniMax-M3

</details>

<details>
<summary>Bugfixes (5)</summary>

- [#1321](https://github.com/ROCm/ATOM/pull/1321) [Merged] Fixes Qwen3.5 accuracy issues in the plugin
- [#1351](https://github.com/ROCm/ATOM/pull/1351) [Opened] Fixes Qwen3.5-35B accuracy via Triton attention
- [#1322](https://github.com/ROCm/ATOM/pull/1322) [Merged] Pauses GC during CUDAGraph capture to prevent Triton finalizer aborts
- [#1339](https://github.com/ROCm/ATOM/pull/1339) [Merged] Fixes GC pause during CUDAGraph capture
- [#1299](https://github.com/ROCm/ATOM/pull/1299) [Merged] Restores QKV shape guard and hardens compile-cache frozen-path guard

</details>

<details>
<summary>CI, Tests & Docs (19)</summary>

- [#1316](https://github.com/ROCm/ATOM/pull/1316) [Opened] Adds KV-events block token_offset, sequence numbers, and replay tests
- [#1332](https://github.com/ROCm/ATOM/pull/1332) [Merged] Makes profile stop timeout configurable via `ATOM_PROFILER_TIMEOUT`
- [#1307](https://github.com/ROCm/ATOM/pull/1307) [Merged] Disables prefix caching and enforces `max_model_len` in scripts
- plus 16 more minor CI, benchmark, and runner updates for MI308/MI350/MI355 architectures ([#1224](https://github.com/ROCm/ATOM/pull/1224), [#1346](https://github.com/ROCm/ATOM/pull/1346), [#1311](https://github.com/ROCm/ATOM/pull/1311), [#1293](https://github.com/ROCm/ATOM/pull/1293), [#1288](https://github.com/ROCm/ATOM/pull/1288), [#1323](https://github.com/ROCm/ATOM/pull/1323), [#1329](https://github.com/ROCm/ATOM/pull/1329), [#1285](https://github.com/ROCm/ATOM/pull/1285), [#1328](https://github.com/ROCm/ATOM/pull/1328), [#1312](https://github.com/ROCm/ATOM/pull/1312), [#1325](https://github.com/ROCm/ATOM/pull/1325), [#1315](https://github.com/ROCm/ATOM/pull/1315), [#1313](https://github.com/ROCm/ATOM/pull/1313), [#1352](https://github.com/ROCm/ATOM/pull/1352), [#1350](https://github.com/ROCm/ATOM/pull/1350), [#1349](https://github.com/ROCm/ATOM/pull/1349))

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
