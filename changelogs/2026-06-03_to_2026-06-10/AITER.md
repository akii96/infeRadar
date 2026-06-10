# AITER: PR digest (2026-06-03 to 2026-06-10)

_91 merged, 75 newly opened - source ROCm/AITER, generated 2026-06-10T12:59:48Z_

## TL;DR
* **DeepSeek and Kimi** dominated attention this week, with significant optimizations targeting their specific architectures (v3/v4 and K2/K2.5), alongside notable work on GLM and GPT-OSS.
* **Next-gen hardware enablement** is accelerating, with massive kernel additions for AMD's gfx1250 (MI400) and gfx950 (MI350X) architectures, while continuing to tune gfx942 (MI300X).
* **Low-precision GEMM and MoE** saw the most needle-moving performance work, particularly around MXFP8, MXFP4, A8W4, and A16W16 formats using the Triton, Gluon, and FlyDSL backends.
* **Attention optimizations** delivered major wins for prefill latency, including chunked gated delta rule (GDN) support and MLA decode improvements.
* **Overall direction**: The engine is rapidly maturing its FlyDSL and Gluon backends to squeeze maximum performance out of extreme quantization and MoE routing on upcoming AMD silicon.

## Most important PRs
* **[#3491](https://github.com/ROCm/aiter/pull/3491)** introduces a full OPUS pipeline family for A16W16 BF16 GEMMs on gfx942 and gfx950, significantly expanding low-precision matrix multiplication support for DeepSeek and Kimi.
* **[#3576](https://github.com/ROCm/aiter/pull/3576)** implements a highly optimized FlyDSL MHA kernel with `qkdim=192` specifically targeting DeepSeek v3 and Kimi K2 on gfx1250.
* **[#3292](https://github.com/ROCm/aiter/pull/3292)** delivers major Triton and Gluon optimizations for MXFP8 GEMMs and A8W4 MoE, spanning gfx942, gfx950, and gfx1250 architectures.
* **[#2774](https://github.com/ROCm/aiter/pull/2774)** adds a new HIP kernel for chunked gated delta rule (GDN) forward passes to support prefill, alongside Triton kernel optimizations for AWS deployments.
* **[#3628](https://github.com/ROCm/aiter/pull/3628)** (Newly opened) is a massive 16k-line in-progress effort to land end-to-end 2-mode MoE support on gfx1250 using FlyDSL.

## More changes by area

<details>
<summary>MoE & Quantization (42)</summary>

- [#3587](https://github.com/ROCm/aiter/pull/3587) implements gfx1250 MoE 2-mode end-to-end v1
- [#3106](https://github.com/ROCm/aiter/pull/3106) adds PTPC FP8 GEMM for gfx1250 via FlyDSL
- [#3575](https://github.com/ROCm/aiter/pull/3575) opens WIP for gfx1250 QMoE 2-mode end-to-end
- [#3229](https://github.com/ROCm/aiter/pull/3229) adds fused Allreduce + RMSNorm + MXFP4 quantization
- [#3353](https://github.com/ROCm/aiter/pull/3353) adds per-batch/head FP8 quant ops for fused QK norm/rope and V
- [#3522](https://github.com/ROCm/aiter/pull/3522) integrates DeepSeek R1 GroupedTopk and Sigmoid routing
- [#3582](https://github.com/ROCm/aiter/pull/3582) adds Ragged-M OOB support for PTPC FP8 GEMM on gfx1250
- [#3359](https://github.com/ROCm/aiter/pull/3359) adds MXFP4 preshuffled GEMM for gfx1250 via Gluon
- [#3619](https://github.com/ROCm/aiter/pull/3619) fuses scale route-gather and WMMA preshuffle for FlyDSL grouped MoE
- [#3504](https://github.com/ROCm/aiter/pull/3504) optimizes A8W4 MoE for decode
- [#3377](https://github.com/ROCm/aiter/pull/3377) fixes tuned-key and adds masked gather for FlyDSL MoE EP reduce path
- [#3589](https://github.com/ROCm/aiter/pull/3589) fixes fast-path performance regressions for grouped MoE on gfx1250
- [#3041](https://github.com/ROCm/aiter/pull/3041) adds transpose_scale parameter to Triton fused_flatten_fp8_group_quant
- [#3408](https://github.com/ROCm/aiter/pull/3408) adds no-combine feature to FlyDSL MoE
- [#3620](https://github.com/ROCm/aiter/pull/3620) removes fills in FlyDSL MoE
- [#3598](https://github.com/ROCm/aiter/pull/3598) updates FlyDSL MoE to use dwordx4 gather
- [#3528](https://github.com/ROCm/aiter/pull/3528) fixes DeepSeek v4 Hadamard rotation and top_k_per_row on wave32
- [#3630](https://github.com/ROCm/aiter/pull/3630) introduces new 64x384 kernel for MoE/quantization
- [#3540](https://github.com/ROCm/aiter/pull/3540) rebuilds 32x384 kernel from new sources
- [#3639](https://github.com/ROCm/aiter/pull/3639) opens WIP for gfx1250 MoE 2-mode end-to-end
- [#3547](https://github.com/ROCm/aiter/pull/3547) opens port for FlyDSL block MoE fusion
- [#3541](https://github.com/ROCm/aiter/pull/3541) opens fused QK/KV norm + RoPE + group-quant ops
- [#3629](https://github.com/ROCm/aiter/pull/3629) opens FP8 blockwise batched GEMM for DeepSeek v4 wo_a on MI350X
- [#3537](https://github.com/ROCm/aiter/pull/3537) re-adds EP prefill optimization
- [#3626](https://github.com/ROCm/aiter/pull/3626) opens gfx1250 A8W4 MoE E2E test and FlyDSL comparison
- [#3597](https://github.com/ROCm/aiter/pull/3597) opens support for FP4 gather_kv_b_proj
- [#3562](https://github.com/ROCm/aiter/pull/3562) opens async loads for x_scales in MoE A8W4 and preshuffle weights
- [#3585](https://github.com/ROCm/aiter/pull/3585) refactors MoE legacy unit tests into per-quant smoke sweep
- [#3548](https://github.com/ROCm/aiter/pull/3548) opens production EP and pure-TP-pad stack for Step-3.5-Flash-FP8
- [#3618](https://github.com/ROCm/aiter/pull/3618) optimizes QK norm RoPE quant FlyDSL launch path
- [#3530](https://github.com/ROCm/aiter/pull/3530) adds torch compile guard and TDM descriptor fix in routing
- [#3656](https://github.com/ROCm/aiter/pull/3656) fixes FMoE run config quant alignment
- [#3607](https://github.com/ROCm/aiter/pull/3607) uses flyc.compile for MoE kernel fast dispatch
- [#3553](https://github.com/ROCm/aiter/pull/3553) adds EP support to two-stage MoE op tests
- [#3556](https://github.com/ROCm/aiter/pull/3556) fixes e8m0 conversion to FP32
- [#3603](https://github.com/ROCm/aiter/pull/3603) uses fused silu_and_mul for CK-Tile interleaved post-activation
- [#3518](https://github.com/ROCm/aiter/pull/3518) routes SwiGLU MXFP4 unshuffled weights to CK-Tile instead of CK2stages
- [#3538](https://github.com/ROCm/aiter/pull/3538) fixes pre-zero output when inter_dim_pad > 0 in FlyDSL MoE stage 1
- [#3593](https://github.com/ROCm/aiter/pull/3593) adds opt-in AITER_MOE_FORCE_BF16_ACT to force BF16 activations
- [#3591](https://github.com/ROCm/aiter/pull/3591) forces fp4x2 for SwiGLU separated per_1x32 path
- [#3615](https://github.com/ROCm/aiter/pull/3615) skips dead zero-fill on split-K MoE stage 1 buffer
- [#3661](https://github.com/ROCm/aiter/pull/3661) drops loop carried percentage for Gluon GEMM quantization

</details>

<details>
<summary>Kernels & attention (40)</summary>

- [#3594](https://github.com/ROCm/aiter/pull/3594) adds OPUS gfx942 A16W16 BF16 GEMM pipeline family for DeepSeek v4
- [#3577](https://github.com/ROCm/aiter/pull/3577) unifies attention 2D Gluon kernel
- [#3482](https://github.com/ROCm/aiter/pull/3482) refactors non-hipblaslt BF16 GEMM tuning to csrc/gemm_a16w16
- [#3502](https://github.com/ROCm/aiter/pull/3502) removes dead code in module_pa
- [#3281](https://github.com/ROCm/aiter/pull/3281) adds MHA backward pass for MI400
- [#3403](https://github.com/ROCm/aiter/pull/3403) adds OPUS GEMM 4G reject
- [#3543](https://github.com/ROCm/aiter/pull/3543) enables per-tensor scaled-Q/K/V attention on gfx12
- [#3507](https://github.com/ROCm/aiter/pull/3507) removes dead code in module_pa_ragged
- [#3508](https://github.com/ROCm/aiter/pull/3508) removes dead code in module_pa_v1
- [#3402](https://github.com/ROCm/aiter/pull/3402) adds stage 1 only kernel wrapper for MLA decode on gfx950
- [#3334](https://github.com/ROCm/aiter/pull/3334) compensates softmax_lse for K-smoothing shift in SAGE attention
- [#3444](https://github.com/ROCm/aiter/pull/3444) adds gfx1250 Gluon fused RMSNorm kernel
- [#3542](https://github.com/ROCm/aiter/pull/3542) adds full decode and merged FP32 LSE for MLA on gfx950
- [#3501](https://github.com/ROCm/aiter/pull/3501) supports gfx1250 in DeepGEMM FP8 paged MQA logits
- [#3516](https://github.com/ROCm/aiter/pull/3516) adds per-stream workspace ownership for TBO in OPUS GEMM split-K
- [#3555](https://github.com/ROCm/aiter/pull/3555) optimizes LSE store and supports small ctxlen for MLA on gfx950
- [#3461](https://github.com/ROCm/aiter/pull/3461) supports global load for MLA
- [#3624](https://github.com/ROCm/aiter/pull/3624) fixes FlyDSL GEMM on gfx1250
- [#3558](https://github.com/ROCm/aiter/pull/3558) aligns OPUS GEMM tuning tolerance with other solutions
- [#3621](https://github.com/ROCm/aiter/pull/3621) replaces IS_GFX1250 bool constexpr with ARCH string in pa_mqa_logits
- [#3654](https://github.com/ROCm/aiter/pull/3654) fixes hang issue for GPT-OSS GEMM
- [#3663](https://github.com/ROCm/aiter/pull/3663) fixes hang issue for GPT-OSS GEMM
- [#3509](https://github.com/ROCm/aiter/pull/3509) fixes GPT-OSS unified attention unbounded error
- [#3503](https://github.com/ROCm/aiter/pull/3503) adds LRU cache for FlyDSL A16W16 GEMM compile
- [#3499](https://github.com/ROCm/aiter/pull/3499) adds correct varlen causal kernel for F8 MHA on gfx950
- [#3633](https://github.com/ROCm/aiter/pull/3633) fixes MI355 MHA fwd_v3 hd192x128 kernel wait LDS bug
- [#3581](https://github.com/ROCm/aiter/pull/3581) opens native HIP D64 BF16 split-K forward backend for flash_attn_func
- [#3583](https://github.com/ROCm/aiter/pull/3583) opens FP8 sparse paged prefill attention for DeepSeek v4 layout
- [#3602](https://github.com/ROCm/aiter/pull/3602) opens FlyDSL optimization for GDR prefill chunk_gdn_fwd_h on MI35X
- [#3646](https://github.com/ROCm/aiter/pull/3646) cleans up Triton gfx1250 GEMM A16W16
- [#3564](https://github.com/ROCm/aiter/pull/3564) cleans up pa_mqa_logits benchmark and tests
- [#3557](https://github.com/ROCm/aiter/pull/3557) enables paged-attention on gfx1201 via WMMA
- [#3648](https://github.com/ROCm/aiter/pull/3648) exposes ioffset from opus::gmem::_async_load()
- [#3606](https://github.com/ROCm/aiter/pull/3606) corrects final_lse in PS MLA prefill kernel for chunked prefill
- [#3612](https://github.com/ROCm/aiter/pull/3612) updates UA3D config for Triton Gluon on gfx12
- [#3641](https://github.com/ROCm/aiter/pull/3641) fixes MLA decode accuracy issue with empty KV split on gfx950
- [#3643](https://github.com/ROCm/aiter/pull/3643) removes FP8 varlen MHA async-copy compiler skips
- [#3660](https://github.com/ROCm/aiter/pull/3660) skips pa_decode_bf16_asm off gfx1250
- [#3664](https://github.com/ROCm/aiter/pull/3664) fixes hang issue for GPT-OSS GEMM
- [#3604](https://github.com/ROCm/aiter/pull/3604) fixes DeepGEMM FP8 paged MQA logits kernel input parameter mismatch

</details>

<details>
<summary>Performance (23)</summary>

- [#3469](https://github.com/ROCm/aiter/pull/3469) fully re-tunes mixed stream-k A16W16 GEMM and enhances co-issue
- [#3247](https://github.com/ROCm/aiter/pull/3247) defers q_descale * k_descale in no-mask kernel to fuse with row-max subtract
- [#3519](https://github.com/ROCm/aiter/pull/3519) tunes Kimi 2.5 A8W8 BPreshuffle GEMMs
- [#3539](https://github.com/ROCm/aiter/pull/3539) reverts Kimi 2.5 A8W8 BPreshuffle GEMMs tuning
- [#3423](https://github.com/ROCm/aiter/pull/3423) adds gfx1151 tuning config for Triton MHA
- [#3487](https://github.com/ROCm/aiter/pull/3487) tunes DeepSeek v3.2 PTPC A8W8 MoE
- [#3533](https://github.com/ROCm/aiter/pull/3533) reverts DeepSeek v3.2 PTPC A8W8 MoE tuning
- [#3534](https://github.com/ROCm/aiter/pull/3534) reverts DeepSeek v3.2 PTPC A8W8 MoE tuning
- [#3287](https://github.com/ROCm/aiter/pull/3287) adds Kimi K2.5/K2.6 FP4 fused MoE tunings for TP2
- [#3560](https://github.com/ROCm/aiter/pull/3560) tunes gfx1151 MHA forward default tile config
- [#3608](https://github.com/ROCm/aiter/pull/3608) refines FlyDSL GEMM config selection code
- [#3636](https://github.com/ROCm/aiter/pull/3636) opens DeepSeek v4 A8W8 blockscale tuned GEMM for gfx950
- [#3613](https://github.com/ROCm/aiter/pull/3613) opens mHC_post_pre kernel tuning for Triton Gluon on gfx12
- [#3642](https://github.com/ROCm/aiter/pull/3642) opens tuning for fused GEMM AFP4WFP4 A16W16 on gfx950
- [#3568](https://github.com/ROCm/aiter/pull/3568) opens tuning for fused GEMM A8W8 blockscale A16W16
- [#3616](https://github.com/ROCm/aiter/pull/3616) opens gfx1250 MXFP4 tuning changes
- [#3662](https://github.com/ROCm/aiter/pull/3662) opens tuned files for MiniMax m2.5 PTPC FP8 model
- [#3532](https://github.com/ROCm/aiter/pull/3532) bounds registration-barrier deadlock and hardens tune() reporting
- [#3580](https://github.com/ROCm/aiter/pull/3580) opens gfx950 MoE A8W4 tuned entries for GPT-OSS shapes
- [#3644](https://github.com/ROCm/aiter/pull/3644) opens updated MiniMax m2.5 FMoE tuned configs with new 64x384 kernels
- [#3653](https://github.com/ROCm/aiter/pull/3653) opens Qwen3 32B FP8 tuned configs for MI308X
- [#3545](https://github.com/ROCm/aiter/pull/3545) optimizes moe_fused_gate kernel for MI300X
- [#3529](https://github.com/ROCm/aiter/pull/3529) opens GLM-4.7-FP8 FMoE configs for EP=4 and fused shared expert

</details>

<details>
<summary>Parallelism & scheduling (4)</summary>

- [#3657](https://github.com/ROCm/aiter/pull/3657) supports qknorm+allreduce+rope+group_quant+cache_shuffle_write fusion pattern for MiniMax
- [#3514](https://github.com/ROCm/aiter/pull/3514) adds missing end_sync barrier in cross_device_reduce_1stage
- [#3652](https://github.com/ROCm/aiter/pull/3652) opens allreduce_rmsnorm_quant support for transpose_scale in bpreshuffle GEMM
- [#3549](https://github.com/ROCm/aiter/pull/3549) removes redundant __syncthreads() in allreduce block reduce

</details>

<details>
<summary>API & serving (6)</summary>

- [#3492](https://github.com/ROCm/aiter/pull/3492) enables stride-aware KV-cache block dim for non-contiguous layouts
- [#3498](https://github.com/ROCm/aiter/pull/3498) honors real paged KV block stride in Triton decode
- [#3546](https://github.com/ROCm/aiter/pull/3546) adds new grid layout for fused_qk_rope_cat_and_cache_mla
- [#3567](https://github.com/ROCm/aiter/pull/3567) opens non-MLA fused_kv_cache for Triton on gfx12
- [#3640](https://github.com/ROCm/aiter/pull/3640) opens part 2 of stride-aware KV-cache block dim for non-contiguous layouts
- [#3601](https://github.com/ROCm/aiter/pull/3601) fixes assert in Triton fused_kv_cache

</details>

<details>
<summary>Hardware & arch (21)</summary>

- [#3623](https://github.com/ROCm/aiter/pull/3623) adds HIP mHC_fused_post_pre
- [#3559](https://github.com/ROCm/aiter/pull/3559) refactors module_aiter_operator
- [#3625](https://github.com/ROCm/aiter/pull/3625) refactors module_custom
- [#3595](https://github.com/ROCm/aiter/pull/3595) refactors module_causal_conv1d_update HIP kernel
- [#3455](https://github.com/ROCm/aiter/pull/3455) validates paged_attention input
- [#3622](https://github.com/ROCm/aiter/pull/3622) fixes OPUS GEMM AITER check
- [#3392](https://github.com/ROCm/aiter/pull/3392) adapts AITER to CK changes
- [#3531](https://github.com/ROCm/aiter/pull/3531) reverts AITER adaptation to CK changes
- [#3385](https://github.com/ROCm/aiter/pull/3385) fixes FlyDSL chunk_gdn_h AOT failure
- [#3554](https://github.com/ROCm/aiter/pull/3554) fixes multithread_reduce_max_dpp on gfx1250
- [#3524](https://github.com/ROCm/aiter/pull/3524) fixes OPUS warning on gfx1250
- [#3649](https://github.com/ROCm/aiter/pull/3649) adds environment variable for kernel arg preload
- [#3536](https://github.com/ROCm/aiter/pull/3536) opens HIP fused mHC post-pre path
- [#3517](https://github.com/ROCm/aiter/pull/3517) opens OPUS gfx1250 feature enablement
- [#3627](https://github.com/ROCm/aiter/pull/3627) opens Zhimding gfx1250 MoE 2-mode E2E v1 0609
- [#3610](https://github.com/ROCm/aiter/pull/3610) opens Zhimding gfx1250 MoE 2-mode E2E v1 0608
- [#3651](https://github.com/ROCm/aiter/pull/3651) opens mHC large M support
- [#3609](https://github.com/ROCm/aiter/pull/3609) opens GLM GQA FP8 KV paged attention test
- [#3645](https://github.com/ROCm/aiter/pull/3645) opens environment overrides for unified attention tuning
- [#3617](https://github.com/ROCm/aiter/pull/3617) fixes pa_mqa_logits MI300X divide-by-zero for small TileQCount
- [#3658](https://github.com/ROCm/aiter/pull/3658) fixes HSA OOB in TopP/TopKTopPSamplingFromProbKernel

</details>

<details>
<summary>Tests, CI & build (24)</summary>

- [#3447](https://github.com/ROCm/aiter/pull/3447) auto-updates split test FILE_TIMES
- [#3572](https://github.com/ROCm/aiter/pull/3572) builds multi-Python wheels and publishes versioned S3 manifest
- [#3485](https://github.com/ROCm/aiter/pull/3485) bumps FlyDSL version to 0.2.0
- [#3512](https://github.com/ROCm/aiter/pull/3512) uses Triton wheelhouse for multi-GPU tests
- [#3592](https://github.com/ROCm/aiter/pull/3592) schedules daily tuning tests
- [#3497](https://github.com/ROCm/aiter/pull/3497) skips Flash attention v3 tests on RDNA
- [#3647](https://github.com/ROCm/aiter/pull/3647) maps ATOM MI350X runner label
- [#3596](https://github.com/ROCm/aiter/pull/3596) opens FFM AITER UT workflow
- [#3578](https://github.com/ROCm/aiter/pull/3578) opens paired-release validation gate workflow
- [#3571](https://github.com/ROCm/aiter/pull/3571) opens MoRI EP accuracy gate for sglang downstream
- [#3600](https://github.com/ROCm/aiter/pull/3600) opens FlyDSL update to 0.2.0.dev20260608
- [#3523](https://github.com/ROCm/aiter/pull/3523) opens GLM-5-MXFP4 accuracy gate for sglang downstream
- [#3510](https://github.com/ROCm/aiter/pull/3510) opens DeepSeek-V3.2 accuracy in sglang downstream test
- [#3605](https://github.com/ROCm/aiter/pull/3605) opens A16W16 GEMM to op tuning workflow
- plus 10 more minor CI updates for artifact downloads, timeouts, and dependencies

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
