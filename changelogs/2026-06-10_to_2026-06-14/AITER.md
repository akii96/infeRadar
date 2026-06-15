# AITER: PR digest (2026-06-10 to 2026-06-14)

_68 merged, 30 newly opened - source ROCm/AITER, generated 2026-06-14T22:14:53Z_

## TL;DR
- **Model Focus:** MiniMax, GPT-OSS, and DeepSeek saw the most attention, with significant tuning and kernel work for Qwen (including a massive MXFP4 GEMM tuning for Qwen 3.5 397B) and GLM.
- **Hardware & Architecture:** Heavy focus on next-gen architectures (gfx1250 and gfx950/MI350), including new GEMM pipelines for gfx942/MI300X and extensive Triton/Gluon optimizations.
- **Performance & Kernels:** Major additions include a native HIP D64 BF16 split-K forward backend for Flash Attention, fused MoE route-quant-scatter kernels, and complex fusion patterns for MiniMax.
- **Quantization & MoE:** Continued push on low-precision formats (MXFP4, FP8, A8W8, A8W4) and fused MoE operations, including new tuning configs and FlyDSL/Gluon path optimizations.

## Most important PRs
- **[#3594](https://github.com/ROCm/aiter/pull/3594)** introduces a new OPUS A16W16 BF16 GEMM pipeline family specifically tailored for DeepSeek V4 on gfx942 (MI300X). This significantly expands model-specific hardware optimization for large-scale inference.
- **[#3581](https://github.com/ROCm/aiter/pull/3581)** implements a native HIP D64 BF16 split-K forward backend for `flash_attn_func`. This provides a high-performance, native alternative to existing attention kernels for improved latency.
- **[#3665](https://github.com/ROCm/aiter/pull/3665)** adds a fused MoE route-quant-scatter kernel for gfx1250 using FlyDSL and CK backends. This reduces memory bandwidth overhead during the critical MoE routing and quantization phases.
- **[#3693](https://github.com/ROCm/aiter/pull/3693)** (newly opened) proposes massive MXFP4 GEMM tuning configurations specifically for the Qwen 3.5 397B model. This highlights the aggressive push for extreme low-precision inference at scale.
- **[#3707](https://github.com/ROCm/aiter/pull/3707)** (and its revert **[#3709](https://github.com/ROCm/aiter/pull/3709)**) attempts a massive 22k-line end-to-end integration of a 2-mode MoE implementation for gfx1250. Although reverted, it indicates significant ongoing architectural work for next-generation hardware.

## More changes by area

<details>
<summary>Performance & tuning (19)</summary>

- [#3285](https://github.com/ROCm/aiter/pull/3285) adds GLM-4.7-FP8 tuned/untuned BF16 GEMM configs for gfx950
- [#3537](https://github.com/ROCm/aiter/pull/3537) re-adds EP prefill optimization for DeepSeek
- [#3618](https://github.com/ROCm/aiter/pull/3618) optimizes QK norm RoPE quant FlyDSL launch path
- [#3612](https://github.com/ROCm/aiter/pull/3612) updates UA3D config for Triton/Gluon on GFX12
- [#3568](https://github.com/ROCm/aiter/pull/3568) adds and tunes fused GEMM A8W8 blockscale A16W16 benchmark
- [#3676](https://github.com/ROCm/aiter/pull/3676) adds GPT-OSS and DeepSeek GEMM configs for gfx1250
- [#3703](https://github.com/ROCm/aiter/pull/3703) keys FMoE tuned configs by gfx and cu_num to disambiguate architectures
- [#3580](https://github.com/ROCm/aiter/pull/3580) adds tuned entries for GPT-OSS shapes and fallback hardening for gfx950 MoE A8W4
- [#3644](https://github.com/ROCm/aiter/pull/3644) updates MiniMax M2.5 FMoE tuned configs with new 64x384 kernels
- [#3679](https://github.com/ROCm/aiter/pull/3679) adds MiniMax TP1 GEMM tuned CSV
- [#3424](https://github.com/ROCm/aiter/pull/3424) hints head-stride div-by-8 for vectorized global load in Triton MHA
- [#3608](https://github.com/ROCm/aiter/pull/3608) refines FlyDSL GEMM config selection code
- [#3466](https://github.com/ROCm/aiter/pull/3466) optimizes TopK kernel performance
- [#3710](https://github.com/ROCm/aiter/pull/3710) (opened) adds DeepSeek V4 BF16 GEMM tuning
- [#3662](https://github.com/ROCm/aiter/pull/3662) (opened) adds tuned files for MiniMax-M2.5 PTPC FP8 model
- [#3653](https://github.com/ROCm/aiter/pull/3653) (opened) adds Qwen3-32B-FP8 tuned configs for MI308X
- [#3702](https://github.com/ROCm/aiter/pull/3702) (opened) adds coalesced LDS-staged store path for MXFP4 MoE sort kernel
- [#3645](https://github.com/ROCm/aiter/pull/3645) (opened) adds environment overrides for unified attention tuning
- [#3695](https://github.com/ROCm/aiter/pull/3695) (opened) adds MiniMax TP1 GEMM tuned CSV

</details>

<details>
<summary>Kernels & attention (24)</summary>

- [#3039](https://github.com/ROCm/aiter/pull/3039) implements FMHA F16 for gfx1250
- [#3623](https://github.com/ROCm/aiter/pull/3623) adds HIP `mhc_fused_post_pre` kernel
- [#3407](https://github.com/ROCm/aiter/pull/3407) adds new features and performance improvements for Triton GMM kernel
- [#3307](https://github.com/ROCm/aiter/pull/3307) optimizes Gluon blockscale A8W8 GEMM kernel for CDNA4
- [#3657](https://github.com/ROCm/aiter/pull/3657) supports QK-norm + allreduce + RoPE + group-quant + cache-shuffle-write fusion pattern for MiniMax
- [#3668](https://github.com/ROCm/aiter/pull/3668) implements allreduce RMSNorm quant transpose scale
- [#3597](https://github.com/ROCm/aiter/pull/3597) supports FP4 `gather_kv_b_proj`
- [#3688](https://github.com/ROCm/aiter/pull/3688) supports `gather_kv_b_proj` with shuffled KV buffer in Triton/Gluon
- [#3648](https://github.com/ROCm/aiter/pull/3648) exposes `ioffset` from `opus::gmem::_async_load()`
- [#3349](https://github.com/ROCm/aiter/pull/3349) makes Triton Sage MXFP4 return LSE
- [#3251](https://github.com/ROCm/aiter/pull/3251) supports non-interleaved tensor layout in fused reshape causal Conv1D update kernel for Qwen 3.5
- [#3651](https://github.com/ROCm/aiter/pull/3651) adds large M support for MHC
- [#3640](https://github.com/ROCm/aiter/pull/3640) enables stride-aware KV-cache block dim for non-contiguous layouts in fused QK norm RoPE cache PTS quant shuffle
- [#3691](https://github.com/ROCm/aiter/pull/3691) makes RoPE kernels run properly on 32-waves devices
- [#3690](https://github.com/ROCm/aiter/pull/3690) (opened) implements Triton sparse VFA
- [#3672](https://github.com/ROCm/aiter/pull/3672) (opened) adds fused QK RoPE concat and cache MLA with paged NOPE + paged RoPE output
- [#3652](https://github.com/ROCm/aiter/pull/3652) (opened) makes allreduce RMSNorm quant support transpose scale for bpreshuffle GEMM
- [#3681](https://github.com/ROCm/aiter/pull/3681) (opened) adds MQA logits prefill
- [#3669](https://github.com/ROCm/aiter/pull/3669) (opened) makes MLA reduce kernel work on 32-waves devices
- [#3671](https://github.com/ROCm/aiter/pull/3671) (opened) adds static N/K-pad grid skip for `gemm_mxscale_gfx1250`
- [#3699](https://github.com/ROCm/aiter/pull/3699) (opened) handles large QH for MLA in Triton/Gluon
- [#3698](https://github.com/ROCm/aiter/pull/3698) (opened) masks V load and output store by value head size in unified attention
- [#3673](https://github.com/ROCm/aiter/pull/3673) (opened) updates MLA global load
- [#3674](https://github.com/ROCm/aiter/pull/3674) (opened) updates QH64 A16W16 global buffer load to LDS

</details>

<details>
<summary>MoE & quantization (5)</summary>

- [#3408](https://github.com/ROCm/aiter/pull/3408) adds no-combine feature to FlyDSL MoE
- [#3611](https://github.com/ROCm/aiter/pull/3611) supports padded K for A8W8 bpreshuffle GEMM
- [#3685](https://github.com/ROCm/aiter/pull/3685) (opened) implements MoE A8W4 multicast
- [#3700](https://github.com/ROCm/aiter/pull/3700) (opened) opts-in fused stage-1 activation-quant kernel selection for FMoE
- [#3692](https://github.com/ROCm/aiter/pull/3692) (opened) adds DeepSeek gfx1250 MoE support

</details>

<details>
<summary>Parallelism & distributed (2)</summary>

- [#3464](https://github.com/ROCm/aiter/pull/3464) supports all dimensions for reduce-scatter
- [#3680](https://github.com/ROCm/aiter/pull/3680) implements MiniMax TP1 P2

</details>

<details>
<summary>Refactors (4)</summary>

- [#3646](https://github.com/ROCm/aiter/pull/3646) cleans up Triton gfx1250 GEMM A16W16
- [#3696](https://github.com/ROCm/aiter/pull/3696) de-torches `module_fused_qk_norm_mrope_cache_quant_shuffle`
- [#3625](https://github.com/ROCm/aiter/pull/3625) refactors `module_custom`
- [#3595](https://github.com/ROCm/aiter/pull/3595) refactors HIP kernel for `module_causal_conv1d_update`

</details>

<details>
<summary>Bugfixes (23)</summary>

- [#3708](https://github.com/ROCm/aiter/pull/3708) fixes FlyDSL MoE JIT bug on gfx1250
- [#3211](https://github.com/ROCm/aiter/pull/3211) fixes paged-attention kernels to support block_id > 65535 in ASM
- [#3391](https://github.com/ROCm/aiter/pull/3391) fixes HK MLA decode forward per-batch output bounds check and reduce-time per-tile split cap
- [#3684](https://github.com/ROCm/aiter/pull/3684) guards gfx942 BF16WS split-K reduce in OPUS
- [#3622](https://github.com/ROCm/aiter/pull/3622) fixes OPUS GEMM AITER check
- [#3675](https://github.com/ROCm/aiter/pull/3675) fixes MiniMax QK-norm allreduce fusion
- [#3530](https://github.com/ROCm/aiter/pull/3530) adds Torch compile guard and fixes TDM descriptor in routing
- [#3641](https://github.com/ROCm/aiter/pull/3641) fixes MLA decode accuracy issue with empty KV split on gfx950 Gluon
- [#3705](https://github.com/ROCm/aiter/pull/3705) corrects 1-stage tuner data-key mapping and surfaces worker errors for FMoE
- [#3713](https://github.com/ROCm/aiter/pull/3713) fixes no-copy-in DP collectives in CUDA graph via real warmup collective
- [#3601](https://github.com/ROCm/aiter/pull/3601) fixes assert in Triton `fused_kv_cache`
- [#3701](https://github.com/ROCm/aiter/pull/3701) temporarily fixes GPT-OSS MoE tuning
- [#3683](https://github.com/ROCm/aiter/pull/3683) skips unsupported architectures in FlyDSL instead of crashing at import
- [#3654](https://github.com/ROCm/aiter/pull/3654) fixes hang issue in GEMM for GPT-OSS
- [#3663](https://github.com/ROCm/aiter/pull/3663) fixes hang issue in GEMM
- [#3664](https://github.com/ROCm/aiter/pull/3664) fixes hang issue in GEMM
- [#3714](https://github.com/ROCm/aiter/pull/3714) passes `i_os=0` in the async load callsite missed by [#3648](https://github.com/ROCm/aiter/pull/3648)
- [#3633](https://github.com/ROCm/aiter/pull/3633) fixes MI355 MHA fwd_v3 hd192x128 kernel wait LDS bug
- [#3706](https://github.com/ROCm/aiter/pull/3706) (opened) adds prebuild for `pa_ps`
- [#3677](https://github.com/ROCm/aiter/pull/3677) (opened) fixes fused MoE padded-token NaNs by zeroing quant output for zero routing
- [#3658](https://github.com/ROCm/aiter/pull/3658) (opened) fixes HSA OOB in TopP/TopKTopPSamplingFromProbKernel
- [#3656](https://github.com/ROCm/aiter/pull/3656) (opened) fixes FMoE run config quant align
- [#3682](https://github.com/ROCm/aiter/pull/3682) (opened) fixes MLA BF16 16mx4 kernel random NaN error in MI350

</details>

<details>
<summary>Tests, CI & build (9)</summary>

- [#3609](https://github.com/ROCm/aiter/pull/3609) adds GLM GQA FP8 KV paged attention test
- [#3687](https://github.com/ROCm/aiter/pull/3687) adds `fused_rms_mxfp4_quant` to model benchmarking tool
- [#3712](https://github.com/ROCm/aiter/pull/3712) gates grouped MoE gfx1250 test on logits_diff < 0.01
- [#3643](https://github.com/ROCm/aiter/pull/3643) removes FP8 varlen MHA async-copy compiler skips
- [#3660](https://github.com/ROCm/aiter/pull/3660) skips `pa_decode_bf16_asm` off gfx1250
- [#3647](https://github.com/ROCm/aiter/pull/3647) maps ATOM MI350X runner label in CI
- [#3686](https://github.com/ROCm/aiter/pull/3686) (opened) evaluates impact of LLVM bump in Triton compiler
- [#3711](https://github.com/ROCm/aiter/pull/3711) (opened) fixes flaky graph capture tests
- [#3670](https://github.com/ROCm/aiter/pull/3670) (opened) bumps FlyDSL to 0.2.0.dev645

</details>

<details>
<summary>Other (6)</summary>

- [#3649](https://github.com/ROCm/aiter/pull/3649) adds environment variable for kernel arg preload
- [#3697](https://github.com/ROCm/aiter/pull/3697) uses stride check in Triton GEMM
- [#3661](https://github.com/ROCm/aiter/pull/3661) drops the loop carried percentage in Gluon GEMM
- [#3704](https://github.com/ROCm/aiter/pull/3704) disables MXFP4 gfx1250 Gluon path
- [#3694](https://github.com/ROCm/aiter/pull/3694) (opened) passes `--targets` to ck-tile generate.py for non-gfx9 hosts
- [#3667](https://github.com/ROCm/aiter/pull/3667) (opened) guards `v_cvt_pk_fp8_f32` and `v_cvt_pk_bf8_f32` ASM in aiter_opus_plus.h for gfx11 family

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
