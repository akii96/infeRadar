# AITER: PR digest (2026-07-01 to 2026-07-05)

_41 merged, 32 newly opened - source ROCm/AITER, generated 2026-07-05T22:04:49Z_

## TL;DR
*   **DeepSeek v4 dominated optimization efforts**, with heavy focus on sparse Multi-Head Latent Attention (MLA) prefill, MoE stage 2 kernels, and aggressive low-bit quantization (FP4 KV-cache, A8W4 decode).
*   **Next-gen hardware enablement accelerated**, featuring massive OPUS feature bring-up for `gfx1250` and extensive kernel tuning (mxfp4, mxfp8) for `gfx950`.
*   **MoE and Quantization pipelines matured**, making FlyDSL mandatory for MoE tuning and introducing new fused dynamic mxfp4 sorting kernels via Gluon.
*   **Qwen and GLM families saw targeted tuning**, including Qwen 3.5 FP8 MoE batch-size optimizations and GLM-5.2 FP8 block-scale GEMM configs.
*   **Overall direction**: The engine is aggressively pushing memory and compute boundaries for frontier models (DeepSeek, Qwen) on AMD's newest architectures (`gfx950`, `gfx1250`) through extreme quantization (FP4/FP8) and unified Triton/Gluon attention kernels.

## Most important PRs
*   **[#3856](https://github.com/ROCm/aiter/pull/3856)** Integrates DeepSeek v4 A8W4 decode and MoE stage 2 kernels for the `gfx950` architecture, unlocking critical throughput for this model family.
*   **[#3517](https://github.com/ROCm/aiter/pull/3517)** Enables foundational OPUS features for the upcoming `gfx1250` architecture, adding extensive GEMM and quantization kernel support.
*   **[#4026](https://github.com/ROCm/aiter/pull/4026)** Optimizes Multi-Head Latent Attention (MLA) v4 by preloading kernel arguments, significantly reducing overhead for `gfx1250` deployments.
*   **[#3833](https://github.com/ROCm/aiter/pull/3833)** Unifies the sparse MLA prefill Triton kernel with the Gluon implementation on `gfx950`, streamlining DeepSeek v4 attention paths.
*   **[#4029](https://github.com/ROCm/aiter/pull/4029)** (Newly opened) Introduces FP4 KV-cache support for DeepSeek v4 via a fused compress scatter and RMSNorm RoPE rotate kernel, aggressively reducing memory bandwidth.

## More changes by area

<details>
<summary>MoE & quantization (26)</summary>

- [#3266](https://github.com/ROCm/aiter/pull/3266) adds FlyDSL MoE sorting kernel
- [#4060](https://github.com/ROCm/aiter/pull/4060) adds kernel preload to FlyDSL MoE
- [#3900](https://github.com/ROCm/aiter/pull/3900) unifies scale weight shuffling across attention and MoE
- [#4001](https://github.com/ROCm/aiter/pull/4001) implements mxfp4 flat kernels for gfx950
- [#3970](https://github.com/ROCm/aiter/pull/3970) adds Gluon MoE reduce kernel
- [#3702](https://github.com/ROCm/aiter/pull/3702) tunes coalesced LDS-staged store path for mxfp4 MoE sort
- [#4045](https://github.com/ROCm/aiter/pull/4045) fixes mxfp4 MoE epilog LDS aux cleanup
- [#4022](https://github.com/ROCm/aiter/pull/4022) fixes a4w4 mxfp4 MoE separated-path correctness and Kimi-K2.5 TP=2 aux shape
- [#4063](https://github.com/ROCm/aiter/pull/4063) keeps fp32 per-token scale layout for 2-stage asm stage1
- [#4047](https://github.com/ROCm/aiter/pull/4047) fixes Opus MoE atomic fallback
- [#3986](https://github.com/ROCm/aiter/pull/3986) routes E>=512 tiny-token decode to MultiPhase block-scan for MoE sorting
- [#4080](https://github.com/ROCm/aiter/pull/4080) absorbs module_rmsnorm_quant into the Opus RMSNorm module
- [#4059](https://github.com/ROCm/aiter/pull/4059) implements RMSNorm backend using Opus to reduce compile time
- [#4025](https://github.com/ROCm/aiter/pull/4025) removes FlyDSL fallback machinery from MoE tuning, making FlyDSL mandatory
- [#4049](https://github.com/ROCm/aiter/pull/4049) implements Gluon fused dynamic mxfp4 quant MoE sort for gfx1250
- [#4067](https://github.com/ROCm/aiter/pull/4067) adds tile_m out-of-bounds support for MoE
- [#4038](https://github.com/ROCm/aiter/pull/4038) adds tuned configs for GLM-5.2-FP8 block-scale fp8 GEMM and MoE
- [#4054](https://github.com/ROCm/aiter/pull/4054) implements Gluon quantization for gfx950 and gfx1250
- [#4074](https://github.com/ROCm/aiter/pull/4074) adds GLM-5.2 FP8 MXFP8 (per_1x32) MoE tuned configs
- [#4043](https://github.com/ROCm/aiter/pull/4043) optimizes DeepSeek v4 fp8 quant with fused compress attention and qk_norm_rope
- [#4040](https://github.com/ROCm/aiter/pull/4040) adds flat and 16x FMoE kernels for GLM5.2-FP8 decode on gfx942
- [#4041](https://github.com/ROCm/aiter/pull/4041) fixes accuracy for M=1 in Qwen 3.5 MoE
- [#4053](https://github.com/ROCm/aiter/pull/4053) optimizes Qwen3.5-397B PTPC FP8 MoE performance for batch sizes 64 and 128
- [#4070](https://github.com/ROCm/aiter/pull/4070) fixes max_fp8 from 240 to 448 for gfx950
- [#4030](https://github.com/ROCm/aiter/pull/4030) aligns mxfp4 reference to RNE on non-gfx950 architectures
- [#4051](https://github.com/ROCm/aiter/pull/4051) fixes get_dtype_fp8 to return correct fp8 dtype on MI300

</details>

<details>
<summary>Kernels & attention (27)</summary>

- [#4018](https://github.com/ROCm/aiter/pull/4018) adds mxfp8 16mx8_32nx1 sparse-prefill kernel for DeepSeek v4 on gfx950
- [#4036](https://github.com/ROCm/aiter/pull/4036) adds Opus FMHA forward hd128 bf16 kernel
- [#3669](https://github.com/ROCm/aiter/pull/3669) makes MLA reduce kernel work on 32-waves devices
- [#3990](https://github.com/ROCm/aiter/pull/3990) aligns decode ABI with V3 stage1 valid-split slots for MLA
- [#3981](https://github.com/ROCm/aiter/pull/3981) supports gemma_norm flag for RMSNorm path
- [#4017](https://github.com/ROCm/aiter/pull/4017) re-lands Qwen3.5-397B a16w16 GEMM configs without DeepSeek v4 conflict
- [#4052](https://github.com/ROCm/aiter/pull/4052) optimizes pa_decode_sparse for gfx1250 Triton
- [#3967](https://github.com/ROCm/aiter/pull/3967) tunes A8W8 blockscale GEMM for gfx1250 Triton
- [#3971](https://github.com/ROCm/aiter/pull/3971) adds Gluon attention reduce kernel
- [#4048](https://github.com/ROCm/aiter/pull/4048) optimizes DeepGEMM MQA logits in Gluon
- [#4002](https://github.com/ROCm/aiter/pull/4002) optimizes unified attention 2D short context for gfx1250 Triton
- [#4037](https://github.com/ROCm/aiter/pull/4037) cleans up naming in ASM GEMM
- [#4014](https://github.com/ROCm/aiter/pull/4014) uses PAIR_VEC_SIZE cos/sin loads in fused_rope_rms_1way_kernel
- [#4031](https://github.com/ROCm/aiter/pull/4031) fixes layout_shifted dropping compile-time shift N under runtime addition
- [#4034](https://github.com/ROCm/aiter/pull/4034) fixes gfx1250 naming style in attention
- [#4035](https://github.com/ROCm/aiter/pull/4035) fixes ASM MHA mxfp8
- [#4024](https://github.com/ROCm/aiter/pull/4024) fixes 3D KV-split issue in gfx1250 Triton attention
- [#4042](https://github.com/ROCm/aiter/pull/4042) implements jagged_dense_bmm_broadcast_add (jdbba) in FlyDSL
- [#4033](https://github.com/ROCm/aiter/pull/4033) implements Qwen sage attention v1 smooth q in Triton
- [#4073](https://github.com/ROCm/aiter/pull/4073) optimizes qk norm RoPE quant for gfx1250
- [#4065](https://github.com/ROCm/aiter/pull/4065) implements head-dim-tiled Triton flash attention for ViT on gfx1151
- [#4079](https://github.com/ROCm/aiter/pull/4079) condenses verbose comments in attention kernels
- [#4058](https://github.com/ROCm/aiter/pull/4058) adds in-place state scatter and h output to VK chunk
- [#4057](https://github.com/ROCm/aiter/pull/4057) supports V-major (hvk) state layout in decode kernel
- [#4044](https://github.com/ROCm/aiter/pull/4044) optimizes unified attention for Gemma-4-31b in Triton
- [#4068](https://github.com/ROCm/aiter/pull/4068) enables doubleq and kv reverse in bf16 ASM MHA to improve performance
- [#4083](https://github.com/ROCm/aiter/pull/4083) refines MLA v4 co

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#4039](https://github.com/ROCm/aiter/pull/4039) unifies fused AllReduce + RMSNorm + quant public API
- [#4066](https://github.com/ROCm/aiter/pull/4066) removes in-function import from traced fused_allreduce_rmsnorm_quant
- [#4084](https://github.com/ROCm/aiter/pull/4084) eliminates end_sync in custom AllReduce by delaying input tensor release
- [#4082](https://github.com/ROCm/aiter/pull/4082) synchronizes custom collectives before return
- [#4081](https://github.com/ROCm/aiter/pull/4081) increases process group timeout from 600s to 1200s

</details>

<details>
<summary>CI, Build & Tests (7)</summary>

- [#4056](https://github.com/ROCm/aiter/pull/4056) adds compile guard for gfx1250 features
- [#4020](https://github.com/ROCm/aiter/pull/4020) relaxes FA3 sliding-window fp32 tolerance in Triton tests
- [#4064](https://github.com/ROCm/aiter/pull/4064) fixes MQA CI failure on MI35X
- [#4046](https://github.com/ROCm/aiter/pull/4046) moves SGLang accuracy jobs to nightly CI
- [#4027](https://github.com/ROCm/aiter/pull/4027) gates MI300X CI behind PR label
- [#4072](https://github.com/ROCm/aiter/pull/4072) ensures grouped MoE build respects GPU_ARCHS
- [#4078](https://github.com/ROCm/aiter/pull/4078) backports TDM/named-barrier gate on clang>=22 for ROCm 7.0/7.1

</details>

<details>
<summary>Docs (2)</summary>

- [#4062](https://github.com/ROCm/aiter/pull/4062) condenses verbose comments in Python codebase
- [#4061](https://github.com/ROCm/aiter/pull/4061) condenses verbose comments in C++ codebase

</details>

<details>
<summary>Bugfixes (1)</summary>

- [#4075](https://github.com/ROCm/aiter/pull/4075) fixes int32 overflow in batched_gemm_bf16

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: c9058ffa82cbb3cb71e5adc88490991099ae8b9a240bb4159862b4eb136964a9 -->
