# AITER: PR digest (2026-06-28 to 2026-07-02)

_52 merged, 46 newly opened - source ROCm/AITER, generated 2026-07-02T11:35:02Z_

## TL;DR
*   **DeepSeek and Qwen dominated** model-specific work, with major focus on DeepSeek-V4 A8W4/FP4 decode integration and Qwen 3.5 MXFP4 GEMM tuning.
*   **Next-gen hardware enablement** saw massive churn, specifically bringing up MI400 (gfx1250) with F4/F8 GEMM support and MI350 (gfx950) sparse-prefill kernels.
*   **MoE & Quantization** advanced significantly, introducing NVFP4-BF16 mixed-precision 2-stage MoE and making FlyDSL mandatory for MoE tuning.
*   **Attention & MLA** received critical updates, including MLA v4 kargs preload, 32-wave reduce optimizations, and new FlyDSL flash attention backward kernels.

## Most important PRs
*   **[#3856](https://github.com/ROCm/aiter/pull/3856)** (Merged): **[Opus] Add gfx950 MoE stage2 kernels and DSV4 A8W4 decode integration**. Delivers critical stage-2 MoE kernels and A8W4 decode support for DeepSeek-V4 on MI350.
*   **[#3517](https://github.com/ROCm/aiter/pull/3517)** (Merged): **[OPUS] OPUS gfx1250 feature enable**. Massive foundational PR enabling next-gen MI400 (gfx1250) features across the stack, paving the way for F4/F8 GEMM support.
*   **[#4029](https://github.com/ROCm/aiter/pull/4029)** (Opened): **DeepSeek-V4 FP4: fused_compress FP4 scatter + rmsnorm_rope_rotate FP4 KV-cache kernel**. Introduces fused FP4 scatter and KV-cache kernels specifically targeting DeepSeek-V4 performance.
*   **[#4021](https://github.com/ROCm/aiter/pull/4021)** (Opened): **[2-stages MOE][gfx950] Support NVFP4-BF16 mixed-precision 2-stages MOE**. Implements mixed-precision NVFP4/BF16 two-stage MoE for MI350, significantly improving low-precision routing efficiency.
*   **[#3976](https://github.com/ROCm/aiter/pull/3976)** (Opened): **[FlyDSL] Implement flash attention backward kernel**. Adds a native FlyDSL implementation for flash attention backward passes, reducing reliance on Triton/external kernels.

## More changes by area

<details>
<summary>Hardware & Architecture (8)</summary>

- [#3957](https://github.com/ROCm/aiter/pull/3957) adds bf16 asm MHA mask=0 kernel for gfx1250
- [#3994](https://github.com/ROCm/aiter/pull/3994) standardizes V4 batched_gemm_bf16 and compress_attn perf tests for gfx1250
- [#3996](https://github.com/ROCm/aiter/pull/3996) initiates support for MI400 F4GEMM (a4w4)
- [#3998](https://github.com/ROCm/aiter/pull/3998) initiates support for MI400 F8GEMM (a8w8 & a8w4)
- [#4005](https://github.com/ROCm/aiter/pull/4005) adds micro-benchmark for PA decode asm on gfx1250
- [#4004](https://github.com/ROCm/aiter/pull/4004) implements asm MHA mxfp8 for gfx1250
- [#4042](https://github.com/ROCm/aiter/pull/4042) opens FlyDSL jagged_dense_bmm_broadcast_add for gfx942
- [#4056](https://github.com/ROCm/aiter/pull/4056) adds compile guards for gfx1250 features

</details>

<details>
<summary>MoE (Mixture of Experts) (21)</summary>

- [#3871](https://github.com/ROCm/aiter/pull/3871) adds gu interleave support for FlyDSL MoE
- [#3968](https://github.com/ROCm/aiter/pull/3968) reverts RadeonFlow activation and sorting implementation selection to upstream
- [#3914](https://github.com/ROCm/aiter/pull/3914) optimizes MoE in Triton
- [#3918](https://github.com/ROCm/aiter/pull/3918) fixes an AOT deadlock in FlyDSL MoE
- [#3984](https://github.com/ROCm/aiter/pull/3984) reverts the enablement of MXFP4 MoE at TP=4/8 via CKTile
- [#3970](https://github.com/ROCm/aiter/pull/3970) adds Gluon MoE reduce support
- [#4045](https://github.com/ROCm/aiter/pull/4045) fixes MXFP4 MoE epilog LDS aux cleanup in RadeonFlow
- [#3518](https://github.com/ROCm/aiter/pull/3518) routes SwiGLU MXFP4 unshuffled weights to CK-Tile instead of CK2stages
- [#4022](https://github.com/ROCm/aiter/pull/4022) tests A4W4 MXFP4 MoE separated-path correctness and Kimi-K2.5 TP=2 aux shape
- [#3975](https://github.com/ROCm/aiter/pull/3975) adds BM64 kernel to RadeonFlow
- [#4047](https://github.com/ROCm/aiter/pull/4047) fixes Opus MoE atomic fallback for gfx950
- [#3987](https://github.com/ROCm/aiter/pull/3987) opens FlyDSL weight-decompression MoE kernels for Qwen3.5/Hunyuan3 on gfx942
- [#3991](https://github.com/ROCm/aiter/pull/3991) refactors AOT for FlyDSL MoE
- [#4060](https://github.com/ROCm/aiter/pull/4060) adds kernel preload to FlyDSL MoE for gfx1250
- [#3985](https://github.com/ROCm/aiter/pull/3985) optimizes TopK gating kernel
- [#4049](https://github.com/ROCm/aiter/pull/4049) opens Gluon fused dynamic MXFP4 quant MoE sort for gfx1250
- [#4000](https://github.com/ROCm/aiter/pull/4000) optimizes MXFP4 a4w4 MoE dispatch for MiniMax-M2.1
- [#3997](https://github.com/ROCm/aiter/pull/3997) requires KBatch >= 2 for block-fp8 split-k in fused MoE
- [#4041](https://github.com/ROCm/aiter/pull/4041) fixes accuracy for M=1 in Qwen3.5 MoE
- [#3989](https://github.com/ROCm/aiter/pull/3989) adds assertion for OOB check in FlyDSL MoE
- [#4025](https://github.com/ROCm/aiter/pull/4025) removes FlyDSL fallback machinery from MoE tuning, making FlyDSL mandatory

</details>

<details>
<summary>Quantization (9)</summary>

- [#3652](https://github.com/ROCm/aiter/pull/3652) makes allreduce_rmsnorm_quant support transpose_scale for bpreshuffle GEMM
- [#3695](https://github.com/ROCm/aiter/pull/3695) adds MiniMax TP1 GEMM tuned CSV for quantization
- [#3702](https://github.com/ROCm/aiter/pull/3702) adds coalesced LDS-staged store path for mxfp4_moe_sort_kernel
- [#3992](https://github.com/ROCm/aiter/pull/3992) fixes MXFP4 kernel even round method
- [#4030](https://github.com/ROCm/aiter/pull/4030) aligns MXFP4 reference to RNE on non-gfx950 architectures
- [#4018](https://github.com/ROCm/aiter/pull/4018) opens OPUS ATOM mxfp8 16mx8_32nx1 sparse-prefill kernel for DSv4 on gfx950
- [#4054](https://github.com/ROCm/aiter/pull/4054) opens Gluon implementation for gfx950 and gfx1250
- [#4043](https://github.com/ROCm/aiter/pull/4043) enables K-split for CSA group-fp8 scatter in FlyDSL fused_compress_attn
- [#4051](https://github.com/ROCm/aiter/pull/4051) fixes get_dtype_fp8 to return correct fp8 dtype on MI300

</details>

<details>
<summary>Attention & MLA (18)</summary>

- [#3669](https://github.com/ROCm/aiter/pull/3669) makes MLA reduce kernel work on 32-waves devices
- [#3742](https://github.com/ROCm/aiter/pull/3742) adds sliding-window support to flash-attention backward in Triton
- [#3980](https://github.com/ROCm/aiter/pull/3980) adds MI400 MLA unit tests
- [#3971](https://github.com/ROCm/aiter/pull/3971) adds Gluon attention reduce
- [#3773](https://github.com/ROCm/aiter/pull/3773) fixes TopK decode dispatch seqlen
- [#4048](https://github.com/ROCm/aiter/pull/4048) optimizes DeepGEMM MQA logits in Gluon
- [#4002](https://github.com/ROCm/aiter/pull/4002) optimizes Unified Attention 2D short context for gfx1250
- [#4036](https://github.com/ROCm/aiter/pull/4036) opens OPUS FMHA fwd hd128 bf16 kernel
- [#4015](https://github.com/ROCm/aiter/pull/4015) opens fused QK norm RoPE 1-way fp8 per-head kernel
- [#3979](https://github.com/ROCm/aiter/pull/3979) adds whole-block GPT-OSS attention test
- [#4033](https://github.com/ROCm/aiter/pull/4033) opens Qwen Sage attention v1 smooth Q in Triton
- [#4052](https://github.com/ROCm/aiter/pull/4052) optimizes pa_decode_sparse for gfx1250 in Triton
- [#4057](https://github.com/ROCm/aiter/pull/4057) supports V-major (hvk) state layout in decode kernel
- [#4044](https://github.com/ROCm/aiter/pull/4044) optimizes Unified Attention for Gemma-4-31b in Triton
- [#3993](https://github.com/ROCm/aiter/pull/3993) wires is_causal through Python and C++ dispatch for mla_decode_fwd
- [#4026](https://github.com/ROCm/aiter/pull/4026) enables MLA v4 kargs preload for gfx1250
- [#3990](https://github.com/ROCm/aiter/pull/3990) aligns MLA v4 decode ABI with V3 stage1 valid-split slots
- [#3988](https://github.com/ROCm/aiter/pull/3988) supports address over 32bit for MI350 MLA PS mode BF16 case

</details>

<details>
<summary>Distributed & Core Kernels (15)</summary>

- [#3981](https://github.com/ROCm/aiter/pull/3981) supports gemma_norm flag for RMSNorm path
- [#4039](https://github.com/ROCm/aiter/pull/4039) unifies fused AR+RMSNorm+quant public API
- [#3928](https://github.com/ROCm/aiter/pull/3928) makes quick_all_reduce flag sync CUDA-graph-safe
- [#3977](https://github.com/ROCm/aiter/pull/3977) corrects the fake register of fused_allreduce_rmsnorm_quant
- [#4023](https://github.com/ROCm/aiter/pull/4023) fuses split-K GEMM output zeroing into the preceding AR+RMSNorm
- [#4059](https://github.com/ROCm/aiter/pull/4059) opens torch-free OPUS RMSNorm backend to cut module_rmsnorm cold build
- [#4016](https://github.com/ROCm/aiter/pull/4016) adds gdn_chunk_prepare fused intra-chunk GDN prefill prep kernel
- [#4058](https://github.com/ROCm/aiter/pull/4058) adds in-place state scatter + h output to VK chunk in Triton
- [#4037](https://github.com/ROCm/aiter/pull/4037) cleans name in asm GEMM
- [#4031](https://github.com/ROCm/aiter/pull/4031) fixes layout_shifted dropping compile-time shift N under runtime addition
- [#4007](https://github.com/ROCm/aiter/pull/4007) adds __threadfence before cross-block barrier in radix kernel
- [#4014](https://github.com/ROCm/aiter/pull/4014) uses PAIR_VEC_SIZE cos/sin loads in fused_rope_rms_1way_kernel
- [#4034](https://github.com/ROCm/aiter/pull/4034) fixes gfx1250 naming style
- [#4035](https://github.com/ROCm/aiter/pull/4035) fixes asm MHA mxfp8
- [#4024](https://github.com/ROCm/aiter/pull/4024) fixes 3D KV-split issue for gfx1250 in Triton

</details>

<details>
<summary>Tuning & Performance (11)</summary>

- [#3974](https://github.com/ROCm/aiter/pull/3974) adds Qwen3.5-397B MXFP4 a16w16 GEMM tuning configs
- [#4013](https://github.com/ROCm/aiter/pull/4013) reverts the addition of Qwen3.5-397B MXFP4 a16w16 GEMM tuning configs
- [#4017](https://github.com/ROCm/aiter/pull/4017) re-lands Qwen3.5-397B a16w16 GEMM configs without DSv4 conflict
- [#3978](https://github.com/ROCm/aiter/pull/3978) avoids scatter reduce copy and adds addXCD swizzle support in RadeonFlow
- [#3986](https://github.com/ROCm/aiter/pull/3986) routes E>=512 tiny-token decode to MultiPhase block-scan in moe_sorting
- [#4011](https://github.com/ROCm/aiter/pull/4011) adds fixed-tile HGEMM candidate
- [#4040](https://github.com/ROCm/aiter/pull/4040) adds flat + 16x FMoE kernels for GLM5.2-FP8 decode on gfx942
- [#4001](https://github.com/ROCm/aiter/pull/4001) opens gfx950 MXFP4 flat tuning configs
- [#4038](https://github.com/ROCm/aiter/pull/4038) adds tuned configs for GLM-5.2-FP8 block-scale fp8 GEMM and MoE
- [#4053](https://github.com/ROCm/aiter/pull/4053) optimizes Qwen3.5-397B PTPC FP8 MoE performance for batch sizes 64 and 128
- [#3920](https://github.com/ROCm/aiter/pull/3920) fixes gfx-aware tuned CSV handling and column-safe row operations in base_tuner

</details>

<details>
<summary>CI, Tests & Docs (11)</summary>

- [#4061](https://github.com/ROCm/aiter/pull/4061) condenses verbose comments in csrc docs
- plus 10 more minor CI and test updates ([#3982](https://github.com/ROCm/aiter/pull/3982), [#3916](https://github.com/ROCm/aiter/pull/3916), [#4020](https://github.com/ROCm/aiter/pull/4020), [#3983](https://github.com/ROCm/aiter/pull/3983), [#3510](https://github.com/ROCm/aiter/pull/3510), [#4046](https://github.com/ROCm/aiter/pull/4046), [#4008](https://github.com/ROCm/aiter/pull/4008), [#4027](https://github.com/ROCm/aiter/pull/4027), [#4003](https://github.com/ROCm/aiter/pull/4003), [#4019](https://github.com/ROCm/aiter/pull/4019))

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 61d65aa7ac71465f258ef6aec87cf1a77c4c38b348fcec4e89ae382c63bee279 -->
