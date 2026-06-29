# ATOM: PR digest (2026-06-24 to 2026-06-28)

_33 merged, 23 newly opened - source ROCm/ATOM, generated 2026-06-28T22:22:54Z_

## TL;DR
- **Models:** MiniMax M3 (Eagle speculative decoding, MXFP8, index caching) and GLM5 (FP8 via RTP-LLM) saw the most merged feature work this window.
- **Performance:** Major throughput wins landed via `uvloop` integration for the server hot-path, NUMA-aware CPU/memory binding for single-node prompt disaggregation, and new AllReduce + RMSNorm + FP8 fusions.
- **Hardware/Arch:** A massive in-progress PR is bringing online INT8 W8A8 quantization and Multi-Token Prediction (MTP) to Qwen3.6 on RDNA3.5 (gfx1151).
- **Attention/Kernels:** Continued refinement of prefix caching (chunking, multimodal bypass) and Triton-based flash attention for Qwen3.x ViT.

## Most important PRs
- **[#1289](https://github.com/ROCm/ATOM/pull/1289)** Feat: RTP-LLM plugin GLM5-FP8 support
  Adds comprehensive FP8 quantization and plugin support for the GLM5 model family, touching attention and MLA components to enable high-performance serving.
- **[#1337](https://github.com/ROCm/ATOM/pull/1337)** [gfx1151] Online INT8 W8A8 for Qwen3.6 27B / 35B-A3B on RDNA3.5, with working MTP
  A massive newly opened architectural update (+15k lines) bringing INT8 quantization and Multi-Token Prediction to RDNA3.5 hardware for Qwen3.6.
- **[#1333](https://github.com/ROCm/ATOM/pull/1333)** [MiniMax M3] Enable and Optimize the MiniMax M3 Eagle
  Enables and optimizes Eagle speculative decoding for MiniMax M3, significantly improving generation throughput by integrating specialized attention and backend execution paths.
- **[#1340](https://github.com/ROCm/ATOM/pull/1340)** Add NUMA-aware CPU/memory binding for PD Single Node optimization
  Improves distributed performance by pinning memory and CPU resources, optimizing single-node prompt disaggregation (PD) to reduce cross-socket latency.
- **[#1378](https://github.com/ROCm/ATOM/pull/1378)** perf(server): streaming hot-path optimizations + uvloop; fix gpt-oss embed param naming
  Replaces the default asyncio event loop with `uvloop` and optimizes the streaming hot-path, significantly improving server concurrency and reducing overhead.

## More changes by area

<details>
<summary>Performance (1)</summary>

- [#1388](https://github.com/ROCm/ATOM/pull/1388) newly opened: fuse AllReduce + RMSNorm + FP8 quant for DeepSeek and Kimi
</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#1334](https://github.com/ROCm/ATOM/pull/1334) implement gluon PA with shuffle layout for MiniMax M3
- [#1236](https://github.com/ROCm/ATOM/pull/1236) add prefix chunk and chunk long prefill support for v4
- [#1354](https://github.com/ROCm/ATOM/pull/1354) support index cache for MiniMax M3
- [#1345](https://github.com/ROCm/ATOM/pull/1345) route prefix-cache-hit prefill through sink ASM MHA kernel
- [#1270](https://github.com/ROCm/ATOM/pull/1270) replace einsum with Triton BMM for DeepSeek V4
- [#1357](https://github.com/ROCm/ATOM/pull/1357) newly opened: custom head-dim-tiled Triton flash attention for Qwen3.x ViT on gfx1151
- [#1355](https://github.com/ROCm/ATOM/pull/1355) newly opened: integrate Triton GEMM for attention and MLA
- [#1373](https://github.com/ROCm/ATOM/pull/1373) newly opened: add TBO support for MiniMax M3
</details>

<details>
<summary>MoE & quantization (5)</summary>

- [#1335](https://github.com/ROCm/ATOM/pull/1335) add MXFP8 support for MiniMax M3
- [#1370](https://github.com/ROCm/ATOM/pull/1370) support online quantization for Quark models
- [#1336](https://github.com/ROCm/ATOM/pull/1336) newly opened: implement low bit expert parallelism (EP)
- [#1341](https://github.com/ROCm/ATOM/pull/1341) newly opened: add dedicated backend for MoE
- [#1365](https://github.com/ROCm/ATOM/pull/1365) newly opened: align online and offline quantization paths
</details>

<details>
<summary>Model support (4)</summary>

- [#1319](https://github.com/ROCm/ATOM/pull/1319) support tool-calls for Qwen3 (qwen3_coder/qwen3_xml)
- [#1342](https://github.com/ROCm/ATOM/pull/1342) newly opened: enable MiniMax-M3 vLLM plugin path
- [#1361](https://github.com/ROCm/ATOM/pull/1361) newly opened: implement MTP speculative decoding for ATOM SGL
- [#1372](https://github.com/ROCm/ATOM/pull/1372) newly opened: adapt DeepSeek V4 MTP for vLLM plugin
</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

- [#1308](https://github.com/ROCm/ATOM/pull/1308) support prompt disaggregation (PD) on single node
</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#1386](https://github.com/ROCm/ATOM/pull/1386) newly opened: add gfx1200 (Navi 44) alongside gfx1201 for RDNA4 support
</details>

<details>
<summary>API & serving (1)</summary>

- [#1381](https://github.com/ROCm/ATOM/pull/1381) raise RLIMIT_NOFILE at startup to survive high connection concurrency
</details>

<details>
<summary>Bugfixes (16)</summary>

- [#1343](https://github.com/ROCm/ATOM/pull/1343) fix v4 prefill SWA write
- [#1367](https://github.com/ROCm/ATOM/pull/1367) fix batch stream-chunk dispatch in server
- [#1321](https://github.com/ROCm/ATOM/pull/1321) fix Qwen3.5 accuracy issues
- [#1339](https://github.com/ROCm/ATOM/pull/1339) fix GC pause during CUDAGraph capture to prevent aborts
- [#1375](https://github.com/ROCm/ATOM/pull/1375) fix FP8 MoE weight load on MI308 (gfx942)
- [#1362](https://github.com/ROCm/ATOM/pull/1362) fix GLM MoE DSA to run the MTP layer's own DSA indexer
- [#1351](https://github.com/ROCm/ATOM/pull/1351) newly opened: fix Qwen3.5-35b accuracy
- [#1369](https://github.com/ROCm/ATOM/pull/1369) newly opened: enable TBO support and fix accuracy regressions for Kimi K2.5
- [#1379](https://github.com/ROCm/ATOM/pull/1379) newly opened: fix accuracy drop for long prompts on GLM5.1/5.2
- [#1358](https://github.com/ROCm/ATOM/pull/1358) newly opened: bypass prefix caching for multimodal sequences
- [#1368](https://github.com/ROCm/ATOM/pull/1368) newly opened: transfer MiniMax-M3 sparse indexer-key cache in disaggregation
- plus 5 more minor guard, attribute, and shape conversion fixes ([#1382](https://github.com/ROCm/ATOM/pull/1382), [#1377](https://github.com/ROCm/ATOM/pull/1377), [#1384](https://github.com/ROCm/ATOM/pull/1384), [#1348](https://github.com/ROCm/ATOM/pull/1348), [#1353](https://github.com/ROCm/ATOM/pull/1353))
</details>

<details>
<summary>CI & build (11)</summary>

- [#1385](https://github.com/ROCm/ATOM/pull/1385) native CI foundation de-inlining and unit-test gating
- [#1374](https://github.com/ROCm/ATOM/pull/1374) shard benchmark matrix by variant/scenario and concurrency to dodge GitHub limits
- [#1323](https://github.com/ROCm/ATOM/pull/1323) move ATOM vLLM CI from mi355 to mi350 (gfx950)
- plus 8 more minor CI workflow, runner, and environment variable updates ([#1190](https://github.com/ROCm/ATOM/pull/1190), [#1346](https://github.com/ROCm/ATOM/pull/1346), [#1356](https://github.com/ROCm/ATOM/pull/1356), [#1349](https://github.com/ROCm/ATOM/pull/1349), [#1352](https://github.com/ROCm/ATOM/pull/1352), [#1350](https://github.com/ROCm/ATOM/pull/1350), [#1371](https://github.com/ROCm/ATOM/pull/1371), [#1387](https://github.com/ROCm/ATOM/pull/1387))
</details>

<details>
<summary>Other (3)</summary>

- [#1332](https://github.com/ROCm/ATOM/pull/1332) make profile stop timeout configurable with ATOM_PROFILER_TIMEOUT
- [#1344](https://github.com/ROCm/ATOM/pull/1344) newly opened: gate AR+RMSNorm fusion on ATOM_ENABLE_ALLREDUCE_RMSNORM for MiniMax M3
- [#1359](https://github.com/ROCm/ATOM/pull/1359) newly opened: add dtype option in LayerNorm class
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
