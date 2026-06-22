# ATOM: PR digest (2026-06-17 to 2026-06-21)

_37 merged, 25 newly opened - source ROCm/ATOM, generated 2026-06-21T22:32:10Z_

## TL;DR
*   **Model Focus**: Heavy emphasis on **MiniMax-M3**, **DeepSeek (v4)**, and **Qwen3.5/Qwen-next**. Significant plugin architecture work landed to support these families.
*   **Attention & Kernels**: Assembly-level Paged Attention (PA) via AITER is being aggressively rolled out for prefill and decode paths, specifically targeting MiniMax-M3 and MI450 architectures.
*   **MoE & Quantization**: Major expansion of MXFP4 and MXFP8 quantization paths, including new Triton MoE kernels for DeepSeek v4 and dedicated BF16 MoE routing for MiniMax-M3.
*   **Speculative Decoding**: Native ATOM EAGLE3 speculative decoding is now enabled for MiniMax-M3, driving generation latency improvements.
*   **Fusions**: Continued push on memory-bandwidth-saving fusions, notably fusing V4 decode SWA cache-writes and combining `allreduce` with various `norm` operations across models.

## Most important PRs
*   **[#925](https://github.com/ROCm/ATOM/pull/925)** Integrates the RTP-LLM plugin and adds support for Qwen3.5 MoE, significantly expanding model serving capabilities and routing.
*   **[#1289](https://github.com/ROCm/ATOM/pull/1289)** (Opened) Drafts RTP-LLM plugin support for GLM-5 using FP8 quantization, paving the way for high-throughput GLM deployments.
*   **[#1263](https://github.com/ROCm/ATOM/pull/1263)** Adopts AITER assembly-level Paged Attention (PA) for both prefill and decode paths on MiniMax-M3, driving major throughput improvements.
*   **[#1256](https://github.com/ROCm/ATOM/pull/1256)** Enables native ATOM EAGLE3 speculative decoding for MiniMax-M3, directly targeting generation latency reduction.
*   **[#1183](https://github.com/ROCm/ATOM/pull/1183)** Implements `kv_buffer` shuffled Multi-Head Latent Attention (MLA) for GFX12 architectures using Triton and Gluon backends.

## More changes by area

<details>
<summary>Performance & Fusions (8)</summary>

- [#1272](https://github.com/ROCm/ATOM/pull/1272) Fuse V4 decode SWA cache-write into `qk_norm_rope_maybe_quant`
- [#1226](https://github.com/ROCm/ATOM/pull/1226) Enable `allreduce_norm_quant` fusion for Kimi K25
- [#1248](https://github.com/ROCm/ATOM/pull/1248) Add fused `topk_gating` for MoE routing
- [#1231](https://github.com/ROCm/ATOM/pull/1231) Add `allreduce` + `rmsnorm` fusion for Qwen
- [#1298](https://github.com/ROCm/ATOM/pull/1298) Fuse indexer Q FP8 quantization into `rope_rotate_activation`
- [#1279](https://github.com/ROCm/ATOM/pull/1279) Add `gemma_norm` + `allreduce` fusion for MiniMax-M3
- [#1261](https://github.com/ROCm/ATOM/pull/1261) (Opened) Add `gemma_norm` + `allreduce` fusion for MiniMax-M3
- [#1273](https://github.com/ROCm/ATOM/pull/1273) (Opened) Support norm FP32 and BF16 output
</details>

<details>
<summary>Kernels & attention (10)</summary>

- [#1213](https://github.com/ROCm/ATOM/pull/1213) Add MI450 Paged Attention (PA) assembly support
- [#1249](https://github.com/ROCm/ATOM/pull/1249) Support model runner v2 on Qwen-next
- [#1271](https://github.com/ROCm/ATOM/pull/1271) (Opened) Implement FP8/mixed MLA dispatch
- [#1241](https://github.com/ROCm/ATOM/pull/1241) (Opened) Fix accuracy for AITER assembly Paged Attention
- [#1301](https://github.com/ROCm/ATOM/pull/1301) (Opened) Add MLA test implementations
- [#1280](https://github.com/ROCm/ATOM/pull/1280) (Opened) Work in progress on MLA kernels
- [#1242](https://github.com/ROCm/ATOM/pull/1242) (Opened) Draft implementation for Paged Attention
- [#1290](https://github.com/ROCm/ATOM/pull/1290) (Opened) Add Gluon `pa_decode_sparse` from AITER for GFX12
- [#1269](https://github.com/ROCm/ATOM/pull/1269) (Opened) Enable PA assembly for MHA decode
- [#1270](https://github.com/ROCm/ATOM/pull/1270) (Opened) Replace einsum with Triton BMM for DeepSeek V4
</details>

<details>
<summary>MoE & quantization (8)</summary>

- [#1246](https://github.com/ROCm/ATOM/pull/1246) Route BF16 MoE through dedicated `MiniMaxM3Bf16Experts`
- [#1292](https://github.com/ROCm/ATOM/pull/1292) Support MXFP8 quantization path
- [#1260](https://github.com/ROCm/ATOM/pull/1260) Support GLM-5.2 IndexShare (FP8) in `glm_moe_dsa`
- [#1294](https://github.com/ROCm/ATOM/pull/1294) Fix TP8 accuracy issue for MXFP4 and MXFP8
- [#1275](https://github.com/ROCm/ATOM/pull/1275) (Opened) Support TBO decode in DeepSeek V4 MoE
- [#1277](https://github.com/ROCm/ATOM/pull/1277) (Opened) Add MXFP8 x MXFP4 Triton MoE for DeepSeek V4
- [#1284](https://github.com/ROCm/ATOM/pull/1284) (Opened) Work in progress on MoE quantization
- [#1297](https://github.com/ROCm/ATOM/pull/1297) (Opened) Implement ATOM shuffle scale for MoE
</details>

<details>
<summary>Model support & Speculative Decoding (2)</summary>

- [#1283](https://github.com/ROCm/ATOM/pull/1283) (Opened) Support EAGLE3 speculative decoding for MiniMax-M3 in vLLM-ATOM
- [#1303](https://github.com/ROCm/ATOM/pull/1303) (Opened) Optimize EAGLE3 implementation for MiniMax-M3
</details>

<details>
<summary>CI, Tests & Benchmarks (18)</summary>

- [#1281](https://github.com/ROCm/ATOM/pull/1281) Parallelize SGLang GPU benchmarks and unify container run flags
- [#1008](https://github.com/ROCm/ATOM/pull/1008) Release MI308 benchmark results to dashboard
- [#1244](https://github.com/ROCm/ATOM/pull/1244) (Opened) Add model prefill/decode benchmark workflow for ATOM mesh
- [#1254](https://github.com/ROCm/ATOM/pull/1254) Add actionlint workflow check
- [#1287](https://github.com/ROCm/ATOM/pull/1287) Add atomesh model CI for nightly runs
- [#1258](https://github.com/ROCm/ATOM/pull/1258) Modify SGL accuracy schedule time and update DeepSeek-R1 topology
- [#1268](https://github.com/ROCm/ATOM/pull/1268) Modify atom-sglang-benchmark model priority for schedule mode
- [#1259](https://github.com/ROCm/ATOM/pull/1259) Add environment variable for allreduce 1-stage threshold
- [#1255](https://github.com/ROCm/ATOM/pull/1255) Lock GPU clock to 2400MHz for benchmark determinism
- [#1250](https://github.com/ROCm/ATOM/pull/1250) Add CPU affinity per rank
- [#1265](https://github.com/ROCm/ATOM/pull/1265) Restrict benchmarks to only use CPU affinity
- [#1247](https://github.com/ROCm/ATOM/pull/1247) Change model cache mount for AAC machine
- [#1274](https://github.com/ROCm/ATOM/pull/1274) Update model cache path for vllm-atom accuracy workflow
- [#1243](https://github.com/ROCm/ATOM/pull/1243) Modify qwen3-next-80b-a3b-fp8 threshold in nightly vLLM
- [#1288](https://github.com/ROCm/ATOM/pull/1288) (Opened) Cancel slurm job before exit in mesh CI
- [#1293](https://github.com/ROCm/ATOM/pull/1293) (Opened) Modify model cache mount direction for atom-sgl-accuracy
- [#1285](https://github.com/ROCm/ATOM/pull/1285) (Opened) Use workspace DOCKER_CONFIG and BUILDKIT_TMPDIR on self-hosted runner
- [#1253](https://github.com/ROCm/ATOM/pull/1253) Resolve merge conflict
</details>

<details>
<summary>Bugfixes (5)</summary>

- [#1240](https://github.com/ROCm/ATOM/pull/1240) Fix accuracy for MiniMax-M3 MXFP4 on AMD
- [#1252](https://github.com/ROCm/ATOM/pull/1252) (Opened) Skip sparse MLA fast metadata for unsupported heads in SGLang
- [#1299](https://github.com/ROCm/ATOM/pull/1299) (Opened) Restore `qkv<=256` shape guard and harden compile-cache frozen-path guard for MiniMax
- [#1300](https://github.com/ROCm/ATOM/pull/1300) (Opened) Duplicate of [#1299](https://github.com/ROCm/ATOM/pull/1299) restoring shape guards
- [#1266](https://github.com/ROCm/ATOM/pull/1266) Minor fix
</details>

<details>
<summary>Docs & Misc (6)</summary>

- [#1291](https://github.com/ROCm/ATOM/pull/1291) Update recipe documentation
- [#1295](https://github.com/ROCm/ATOM/pull/1295) Disable prefix caching in MiniMax-M3 FP4 and EAGLE3 recipe scripts
- [#1262](https://github.com/ROCm/ATOM/pull/1262) Cache `cos_sin_cache`
- [#1278](https://github.com/ROCm/ATOM/pull/1278) Make BF16 gate
- [#1257](https://github.com/ROCm/ATOM/pull/1257) Use `fused_qknorm_idxrqknorm` for MiniMax-M3
- [#1282](https://github.com/ROCm/ATOM/pull/1282) (Opened) Merge build sparse block into top-k
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
