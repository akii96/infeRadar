# AITER: PR digest (2026-06-03 to 2026-06-08)

_67 merged, 49 newly opened - source ROCm/AITER, generated 2026-06-10T15:31:27Z_

## TL;DR
*   **Model Focus:** DeepSeek and Kimi dominated this cycle, with significant attention also given to GLM and GPT-OSS architectures.
*   **Hardware Enablement:** A massive push for next-generation AMD hardware, with heavy enablement and tuning for gfx1250 (RDNA4/MI400) and gfx950 (MI350) architectures across Triton, Gluon, and FlyDSL backends.
*   **Extreme Quantization & MoE:** Major performance wins landed for A8W4, A8W8, MXFP4, and MXFP8 quantization schemes, particularly targeting MoE GEMMs, fused Allreduce/RMSNorm, and EP/TP routing optimizations.
*   **Attention & Prefill Wins:** Significant latency improvements for prefill via new chunked Gated Delta Rule (GDN/GDR) kernels, alongside custom Multi-Head Attention (MHA) implementations tuned specifically for DeepSeek-V3 and Kimi K2.

## Most important PRs
*   **[#3491](https://github.com/ROCm/aiter/pull/3491)** Delivers a complete pipeline family for A16W16 to BF16 GEMMs on gfx942 and gfx950, providing a massive foundational performance update critical for DeepSeek, Kimi, and Qwen.
*   **[#3576](https://github.com/ROCm/aiter/pull/3576)** Implements a custom FlyDSL Multi-Head Attention kernel with a `qkdim` of 192, specifically tuned to maximize DeepSeek-V3 and Kimi K2 performance on gfx1250.
*   **[#2774](https://github.com/ROCm/aiter/pull/2774)** Adds a new HIP kernel for chunked Gated Delta Rule (GDN) forward passes, significantly optimizing prefill performance and Triton kernel implementations for AWS deployments.
*   **[#3587](https://github.com/ROCm/aiter/pull/3587)** Introduces the first end-to-end version of a 2-mode MoE pipeline for gfx1250, heavily utilizing FlyDSL and CK backends to optimize kernel launches and memory traffic.
*   **[#3292](https://github.com/ROCm/aiter/pull/3292)** Optimizes MXFP8 GEMM and A8W4 MoE kernels using Triton and ATOM, delivering major quantization performance wins across gfx942, gfx950, and gfx1250 architectures.

## More changes by area

<details>
<summary>Performance (17)</summary>

- [#3469](https://github.com/ROCm/aiter/pull/3469) full re-tuning for mixed stream-k a16w16 GEMM and co-issue enhancements
- [#3247](https://github.com/ROCm/aiter/pull/3247) defer q_descale * k_descale in SAGE attention no-mask kernel to fuse with row-max subtract
- [#3423](https://github.com/ROCm/aiter/pull/3423) add Triton MHA tuning config for gfx1151
- [#3519](https://github.com/ROCm/aiter/pull/3519) tune Kimi 2.5 A8W8 BPreshuffle GEMMs
- [#3539](https://github.com/ROCm/aiter/pull/3539) revert Kimi 2.5 A8W8 BPreshuffle GEMMs tuning
- [#3487](https://github.com/ROCm/aiter/pull/3487) tune DeepSeek V3.2 PTPC A8W8 MoE
- [#3533](https://github.com/ROCm/aiter/pull/3533) revert DeepSeek V3.2 PTPC A8W8 MoE tuning
- [#3534](https://github.com/ROCm/aiter/pull/3534) revert DeepSeek V3.2 PTPC A8W8 MoE tuning (duplicate)
- [#3287](https://github.com/ROCm/aiter/pull/3287) add Kimi K2.5/K2.6 FP4 fused MoE tunings for TP2
- [#3613](https://github.com/ROCm/aiter/pull/3613) update tuning config for mHC_post_pre kernel on gfx1250
- [#3612](https://github.com/ROCm/aiter/pull/3612) update UA3D tuning config for gfx1250
- [#3568](https://github.com/ROCm/aiter/pull/3568) add and tune fused GEMM A8W8 blockscale A16W16 benchmark on gfx950
- [#3580](https://github.com/ROCm/aiter/pull/3580) add tuned entries for GPT-OSS shapes in gfx950 MoE A8W4
- [#3529](https://github.com/ROCm/aiter/pull/3529) add GLM-4.7-FP8 FMOE configs for EP=4 and fused shared expert on MI355x
- [#3603](https://github.com/ROCm/aiter/pull/3603) use fused silu_and_mul for CK-Tile interleaved post-activation
- [#3545](https://github.com/ROCm/aiter/pull/3545) optimize moe_fused_gate kernel for MI300X
- [#3549](https://github.com/ROCm/aiter/pull/3549) remove redundant __syncthreads() in allreduce block reduce

</details>

<details>
<summary>Kernels & attention (17)</summary>

- [#3106](https://github.com/ROCm/aiter/pull/3106) add PTPC FP8 GEMM via FlyDSL for gfx1250
- [#3281](https://github.com/ROCm/aiter/pull/3281) implement MHA backward pass for MI400
- [#3402](https://github.com/ROCm/aiter/pull/3402) add stage-1 only kernel wrapper for MLA decode on gfx950
- [#3542](https://github.com/ROCm/aiter/pull/3542) implement full decode and merged fp32 LSE for MLA on gfx950
- [#3555](https://github.com/ROCm/aiter/pull/3555) optimize LSE store and support small context lengths (1-256) for MLA on gfx950
- [#3501](https://github.com/ROCm/aiter/pull/3501) support gfx1250 in DeepGEMM FP8 paged MQA logits
- [#3499](https://github.com/ROCm/aiter/pull/3499) add correct varlen causal kernel for FP8 MHA on gfx950
- [#3583](https://github.com/ROCm/aiter/pull/3583) implement FP8 sparse paged prefill attention using DeepSeek-V4 layout
- [#3602](https://github.com/ROCm/aiter/pull/3602) optimize GDR prefill chunk_gdn_fwd_h for MI35X via FlyDSL
- [#3564](https://github.com/ROCm/aiter/pull/3564) clean up pa_mqa_logits (DeepGEMM attention) benchmark and tests
- [#3557](https://github.com/ROCm/aiter/pull/3557) enable paged-attention on gfx1201 (RDNA4) via WMMA
- [#3606](https://github.com/ROCm/aiter/pull/3606) correct final_lse in PS MLA prefill kernel for chunked prefill
- [#3609](https://github.com/ROCm/aiter/pull/3609) add GLM GQA FP8 KV paged attention test
- [#3546](https://github.com/ROCm/aiter/pull/3546) implement new grid layout for fused_qk_rope_cat_and_cache_mla
- [#3567](https://github.com/ROCm/aiter/pull/3567) implement non-MLA fused_kv_cache for gfx1250
- [#3392](https://github.com/ROCm/aiter/pull/3392) adapt AITER to CK changes from rocm-libraries
- [#3531](https://github.com/ROCm/aiter/pull/3531) revert AITER adaptation to CK changes

</details>

<details>
<summary>MoE & quantization (19)</summary>

- [#3547](https://github.com/ROCm/aiter/pull/3547) introduce block-MoE fusion using the FlyDSL backend
- [#3575](https://github.com/ROCm/aiter/pull/3575) implement qmoe 2-mode end-to-end v1 for gfx1250
- [#3359](https://github.com/ROCm/aiter/pull/3359) implement preshuffled MXFP4 GEMM for gfx1250 via Gluon
- [#3504](https://github.com/ROCm/aiter/pull/3504) optimize A8W4 MoE for decode
- [#3377](https://github.com/ROCm/aiter/pull/3377) fix tuned-key and implement EP reduce path with masked gather for FlyDSL MoE
- [#3589](https://github.com/ROCm/aiter/pull/3589) fix fast-path performance regressions for grouped MoE on gfx1250
- [#3334](https://github.com/ROCm/aiter/pull/3334) compensate softmax_lse for K-smoothing shift in SAGE to enable ring-attention
- [#3353](https://github.com/ROCm/aiter/pull/3353) add per-batch/head FP8 quant ops for fused QK norm/rope and V
- [#3229](https://github.com/ROCm/aiter/pull/3229) add fused Allreduce + RMSNorm + MXFP4 quant
- [#3522](https://github.com/ROCm/aiter/pull/3522) integrate DeepSeek R1 GroupedTopk and Sigmoid routing into DS routing
- [#3492](https://github.com/ROCm/aiter/pull/3492) enable stride-aware KV-cache block dim for non-contiguous layouts in fused quant shuffle
- [#3541](https://github.com/ROCm/aiter/pull/3541) add fused QK/KV norm + RoPE + group-quant ops
- [#3562](https://github.com/ROCm/aiter/pull/3562) use async loads for x_scales in MoE A8W4 and preshuffle weights
- [#3610](https://github.com/ROCm/aiter/pull/3610) update MoE 2-mode end-to-end v1 for gfx1250
- [#3548](https://github.com/ROCm/aiter/pull/3548) implement production EP and pure-TP-pad stack for Step-3.5-Flash-FP8
- [#3553](https://github.com/ROCm/aiter/pull/3553) add EP support to two-stage MoE op tests
- [#3537](https://github.com/ROCm/aiter/pull/3537) re-add EP prefill optimization for DeepSeek
- [#3616](https://github.com/ROCm/aiter/pull/3616) update MXFP4 implementation for gfx1250
- [#3611](https://github.com/ROCm/aiter/pull/3611) support padded K for A8W8 bpreshuffle GEMM

</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#3403](https://github.com/ROCm/aiter/pull/3403) reject Opus GEMM 4G on gfx950
- [#3444](https://github.com/ROCm/aiter/pull/3444) add gfx1250 Gluon fused RMSNorm kernel
- [#3517](https://github.com/ROCm/aiter/pull/3517) enable OPUS features for gfx1250
- [#3461](https://github.com/ROCm/aiter/pull/3461) support global load for MLA quantization on gfx950

</details>

<details>
<summary>API & serving (4)</summary>

- [#3516](https://github.com/ROCm/aiter/pull/3516) implement per-stream workspace ownership for TBO in opus_gemm splitk
- [#3598](https://github.com/ROCm/aiter/pull/3598) use dwordx4 for gather in FlyDSL MoE
- [#3536](https://github.com/ROCm/aiter/pull/3536) add HIP fused mHC post-pre path
- [#3607](https://github.com/ROCm/aiter/pull/3607) use flyc.compile for MoE kernel fast dispatch

</details>

<details>
<summary>Refactors (3)</summary>

- [#3482](https://github.com/ROCm/aiter/pull/3482) move non-hipblaslt bf16 GEMM tuning to csrc/gemm_a16w16
- [#3559](https://github.com/ROCm/aiter/pull/3559) refactor module_aiter_operator
- [#3585](https://github.com/ROCm/aiter/pull/3585) refactor MoE legacy unit tests into per-quant smoke sweep

</details>

<details>
<summary>Bugfixes (15)</summary>

- [#3498](https://github.com/ROCm/aiter/pull/3498) honor real paged KV block stride for non-contiguous cache in Triton decode
- [#3528](https://github.com/ROCm/aiter/pull/3528) fix dsv4_rotate (Hadamard) and top_k_per_row on wave32
- [#3385](https://github.com/ROCm/aiter/pull/3385) fix FlyDSL chunk_gdn_h AOT compilation failure
- [#3554](https://github.com/ROCm/aiter/pull/3554) fix multithread_reduce_max_dpp on gfx1250
- [#3524](https://github.com/ROCm/aiter/pull/3524) fix OPUS warning on gfx1250
- [#3509](https://github.com/ROCm/aiter/pull/3509) fix GPT-OSS unified attention unbounded error
- [#3514](https://github.com/ROCm/aiter/pull/3514) add missing end_sync barrier in cross_device_reduce_1stage
- [#3532](https://github.com/ROCm/aiter/pull/3532) bound registration-barrier deadlock and harden tune() reporting for MoE
- [#3617](https://github.com/ROCm/aiter/pull/3617) fix pa_mqa_logits MI300X divide-by-zero for small TileQCount
- [#3530](https://github.com/ROCm/aiter/pull/3530) add torch compile guard and fix TDM descriptor in routing.py
- [#3556](https://github.com/ROCm/aiter/pull/3556) fix e8m0 conversion to fp32
- [#3518](https://github.com/ROCm/aiter/pull/3518) route SwiGLU MXFP4 unshuffled weights to CK-Tile instead of CK2stages
- [#3538](https://github.com/ROCm/aiter/pull/3538) pre-zero output when inter_dim_pad > 0 in flydsl_moe_stage1
- [#3601](https://github.com/ROCm/aiter/pull/3601) fix assert in Triton fused_kv_cache
- [#3604](https://github.com/ROCm/aiter/pull/3604) fix deepgemm_fp8_paged_mqa_logits kernel input parameter mismatch

</details>

<details>
<summary>CI & build (23)</summary>

- [#3572](https://github.com/ROCm/aiter/pull/3572) fix multi-Python wheels build and publish versioned S3 manifest
- [#3447](https://github.com/ROCm/aiter/pull/3447) auto-update split test FILE_TIMES
- [#3550](https://github.com/ROCm/aiter/pull/3550) add timeouts for artifact downloads
- [#3561](https://github.com/ROCm/aiter/pull/3561) add fallback Triton wheel download
- [#3563](https://github.com/ROCm/aiter/pull/3563) extend large artifact download timeouts
- [#3485](https://github.com/ROCm/aiter/pull/3485) bump FlyDSL version to 0.2.0
- [#3584](https://github.com/ROCm/aiter/pull/3584) retry Aiter wheel artifact download
- [#3512](https://github.com/ROCm/aiter/pull/3512) use Triton wheelhouse for multi-GPU tests
- [#3592](https://github.com/ROCm/aiter/pull/3592) schedule daily tuning tests
- [#3497](https://github.com/ROCm/aiter/pull/3497) skip Flash attention v3 tests on RDNA
- [#3590](https://github.com/ROCm/aiter/pull/3590) install dependencies for vLLM benchmark wheel
- [#3511](https://github.com/ROCm/aiter/pull/3511) remove internal pip index from vLLM benchmark
- [#3544](https://github.com/ROCm/aiter/pull/3544) set ATOM image build timeout
- [#3535](https://github.com/ROCm/aiter/pull/3535) add Radeon GPU CI smoke test
- [#3596](https://github.com/ROCm/aiter/pull/3596) add FFM aiter UT workflow
- [#3578](https://github.com/ROCm/aiter/pull/3578) add paired-release validation gate workflow (AITER+ATOM matrix)
- [#3552](https://github.com/ROCm/aiter/pull/3552) reuse prepared Aiter source in test jobs
- [#3571](https://github.com/ROCm/aiter/pull/3571) add MoRI EP accuracy gate for sglang-downstream
- [#3600](https://github.com/ROCm/aiter/pull/3600) update flydsl to 0.2.0.dev20260608
- [#3573](https://github.com/ROCm/aiter/pull/3573) add retry logic for Aiter wheel artifact downloads
- [#3510](https://github.com/ROCm/aiter/pull/3510) enable DeepSeek-V3.2 accuracy in sglang downstream test
- [#3523](https://github.com/ROCm/aiter/pull/3523) add GLM-5-MXFP4 accuracy gate
- [#3605](https://github.com/ROCm/aiter/pull/3605) add a16w16 GEMM to op tuning workflow

</details>

<details>
<summary>Other (9)</summary>

- [#3502](https://github.com/ROCm/aiter/pull/3502) remove dead code in module_pa
- [#3507](https://github.com/ROCm/aiter/pull/3507) remove dead code in module_pa_ragged
- [#3508](https://github.com/ROCm/aiter/pull/3508) remove dead code in module_pa_v1
- [#3455](https://github.com/ROCm/aiter/pull/3455) validate paged_attention input
- [#3540](https://github.com/ROCm/aiter/pull/3540) rebuild 32x384 kernel from new sources
- [#3503](https://github.com/ROCm/aiter/pull/3503) add LRU cache for FlyDSL a16w16 GEMM compile
- [#3593](https://github.com/ROCm/aiter/pull/3593) add AITER_MOE_FORCE_BF16_ACT to force bf16 activations
- [#3591](https://github.com/ROCm/aiter/pull/3591) always use fp4x2 for swiglu separated per_1x32 path
- [#3615](https://github.com/ROCm/aiter/pull/3615) skip dead zero-fill on split-K MoE stage1 buffer

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
