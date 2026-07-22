# AITER: PR digest (2026-07-05 to 2026-07-09)

_47 merged, 46 newly opened - source ROCm/AITER, generated 2026-07-09T11:58:11Z_

## TL;DR
*   **DeepSeek (v4) and GLM (5.1/5.2)** dominated model-specific work, with major performance wins in MLA (Multi-Head Latent Attention) and MoE throughput.
*   **Extreme Quantization:** Heavy focus on MXFP4 (a4w4) and FP8 blockscale for MoE backends, specifically targeting memory bandwidth reduction for serving Kimi and DeepSeek.
*   **Kernel Infrastructure:** Significant expansion including the first Triton Conv kernels, fused QK-norm-RoPE, and new Opus/Gluon/FlyDSL backends to reduce compile times.
*   **Hardware Enablement:** Aggressively targeting next-gen AMD architectures (gfx950, gfx1250) alongside MI300X (gfx942), with new communication and preshuffle kernels.
*   **Overall Direction:** Solidifying low-precision MoE and MLA performance for frontier models on next-gen AMD hardware, while migrating kernels to faster-compiling backends.

## Most important PRs
*   **[#3832](https://github.com/ROCm/aiter/pull/3832)** Introduces the MXFP4 (a4w4) MoE backend for gfx950 using FlyDSL. This significantly reduces memory bandwidth requirements for serving heavily quantized models like Kimi.
*   **[#3422](https://github.com/ROCm/aiter/pull/3422)** Adds FP8 blockscale GEMM and FMoE tunings for GLM-5.1 on gfx942 (MI300X/MI325), directly improving throughput and latency for the GLM family.
*   **[#3833](https://github.com/ROCm/aiter/pull/3833)** Implements DeepSeek v4 sparse MLA prefill in Triton and unifies it with the Gluon kernel on gfx950, delivering a critical performance win for DeepSeek's attention architecture.
*   **[#2886](https://github.com/ROCm/aiter/pull/2886)** Merges the first set of Triton-based Convolution kernels into AITER, expanding operator coverage beyond standard transformer blocks.
*   **[#4113](https://github.com/ROCm/aiter/pull/4113)** (Newly opened) Implements BF16 Jagged Dense BMM Backward in FlyDSL. This massive 11k-line addition lays the groundwork for efficient training of jagged sequences.

## More changes by area

<details>
<summary>Performance (17)</summary>

*   [#4105](https://github.com/ROCm/aiter/pull/4105) adds refactoring and fused GEMM benchmarks and configs
*   [#4135](https://github.com/ROCm/aiter/pull/4135) reduces a8w4 GEMM2 VGPR pressure for DeepSeek v4 in FlyDSL MoE
*   [#3946](https://github.com/ROCm/aiter/pull/3946) updates tuned MoE configs for DeepSeek and GLM
*   [#4089](https://github.com/ROCm/aiter/pull/4089) optimizes QK norm RoPE quantization for gfx1250
*   [#4095](https://github.com/ROCm/aiter/pull/4095) adds tuned configs for GLM-5.2 FP8 PTPC GEMM and MXFP8/MXFP4 MoE
*   [#4125](https://github.com/ROCm/aiter/pull/4125) tunes Shaoclee/a8w8 Triton kernels for gfx1250
*   [#4043](https://github.com/ROCm/aiter/pull/4043) optimizes DeepSeek v4 FP8 quant with fused compress attention and QK norm RoPE
*   [#4096](https://github.com/ROCm/aiter/pull/4096) skips valid_split_count fill for MLA v4 nm
*   [#4109](https://github.com/ROCm/aiter/pull/4109) tunes a8w8 blockscale GEMM preshuffle (M=32) for Triton/Gluon on gfx1250
*   [#4112](https://github.com/ROCm/aiter/pull/4112) adds Qwen3.5 gfx942 tuned GEMM config
*   [#4151](https://github.com/ROCm/aiter/pull/4151) (opened) tunes a8w8 DSL for DeepSeek, GLM, and MiniMax
*   [#4140](https://github.com/ROCm/aiter/pull/4140) (opened) adds tuned GFX1201 DSV4-Flash FP16 and FP8 GEMMs for ATOM
*   [#4150](https://github.com/ROCm/aiter/pull/4150) (opened) optimizes mxscale/MoE on gfx1250 for DeepSeek v4
*   [#4130](https://github.com/ROCm/aiter/pull/4130) (opened) updates MoE tuned configs for DeepSeek and GPT-OSS
*   [#4152](https://github.com/ROCm/aiter/pull/4152) (opened) optimizes Opus MoE a8w4 stage2 candidate set
*   [#4103](https://github.com/ROCm/aiter/pull/4103) (opened) tunes DSv4 TP4 FP8 a8w8 blockscale BpreShuffle GEMM for gfx950
*   [#4093](https://github.com/ROCm/aiter/pull/4093) (opened) updates afp4wfp4 config for Triton async marker
</details>

<details>
<summary>Kernels & attention (20)</summary>

*   [#4059](https://github.com/ROCm/aiter/pull/4059) implements OPUS RMSNorm backend to reduce compile time
*   [#4015](https://github.com/ROCm/aiter/pull/4015) adds fused QK norm RoPE 1-way FP8 per-head kernel
*   [#4128](https://github.com/ROCm/aiter/pull/4128) implements pa_prefill_sparse for Triton/Gluon on gfx1250
*   [#3913](https://github.com/ROCm/aiter/pull/3913) adds FlyDSL gfx942 FP8 MQA logits indexer kernel and fixes Triton FN/FNUZ
*   [#4115](https://github.com/ROCm/aiter/pull/4115) optimizes mhc on gfx12xx
*   [#4102](https://github.com/ROCm/aiter/pull/4102) supports GemmaRMSNorm in fused_qk_norm_mrope with FP8 KV on gfx1201
*   [#4129](https://github.com/ROCm/aiter/pull/4129) refines MLA v4 co kernel
*   [#4127](https://github.com/ROCm/aiter/pull/4127) (opened) adds Opus PA decode skeleton with self-contained sp3 MFMA kernels
*   [#4083](https://github.com/ROCm/aiter/pull/4083) (opened) refines MLA v4 co for gfx1250
*   [#4136](https://github.com/ROCm/aiter/pull/4136) (opened) adds FlyDSL jagged_dense_bmm_broadcast_add for MI300X
*   [#4147](https://github.com/ROCm/aiter/pull/4147) (opened) adds MHA Gluon kernel for gfx950
*   [#4114](https://github.com/ROCm/aiter/pull/4114) (opened) adds FlyDSL gemm_decode small-M dense GEMM kernels
*   [#4098](https://github.com/ROCm/aiter/pull/4098) (opened) implements MiniMax FP8 index cache write
*   [#4146](https://github.com/ROCm/aiter/pull/4146) (opened) adds fused_add_rmsnorm_pad Gluon equivalent function for gfx1250
*   [#4157](https://github.com/ROCm/aiter/pull/4157) (opened) adds dev/env controls for kernel preload
*   [#4159](https://github.com/ROCm/aiter/pull/4159) (opened) adds paged SWA cache-write variant for FlyDSL QK norm RoPE
*   [#4143](https://github.com/ROCm/aiter/pull/4143) (opened) adds miscellaneous DeepSeek v4 kernel updates for gfx1250
*   [#4088](https://github.com/ROCm/aiter/pull/4088) (opened) folds gqa=64 sparse-MLA decode through the gqa=16 kernel
*   [#4158](https://github.com/ROCm/aiter/pull/4158) (opened) removes deprecated offset arg from tdm.async_gather calls on gfx1250
*   [#4156](https://github.com/ROCm/aiter/pull/4156) (opened) updates MLA qh16 to support global load KV on gfx950
</details>

<details>
<summary>MoE & quantization (13)</summary>

*   [#3816](https://github.com/ROCm/aiter/pull/3816) refactors a8w8 blockscale GEMM and adds gfx1250 preshuffle in Triton
*   [#3985](https://github.com/ROCm/aiter/pull/3985) optimizes TopK gating kernel for gfx950 and gfx1250
*   [#4025](https://github.com/ROCm/aiter/pull/4025) makes FlyDSL mandatory for MoE tuning by removing fallback machinery
*   [#3562](https://github.com/ROCm/aiter/pull/3562) uses async loads for x_scales in MoE a8w4 and preshuffles weights in Gluon
*   [#4085](https://github.com/ROCm/aiter/pull/4085) adds DeepSeek v4 support for HERD in Gluon on gfx1250
*   [#4001](https://github.com/ROCm/aiter/pull/4001) implements MXFP4 flat for gfx950
*   [#4134](https://github.com/ROCm/aiter/pull/4134) (opened) supports a8w8 blockscale bpreshuffle GEMM in FlyDSL for gfx1250
*   [#4161](https://github.com/ROCm/aiter/pull/4161) (opened) adds strided-batched MXFP4/MXFP8 preshuffle batched GEMM for gfx950
*   [#4139](https://github.com/ROCm/aiter/pull/4139) (opened) packs fp4_t/int4_t/uint4_t as one sub-byte element in OPUS
*   [#4087](https://github.com/ROCm/aiter/pull/4087) (opened) fuses MoE1, activation, and quantization for DeepSeek v4 in Gluon
*   [#4124](https://github.com/ROCm/aiter/pull/4124) (opened) adds torch-free a4w4 GEMM and C++ library build
*   [#4097](https://github.com/ROCm/aiter/pull/4097) (opened) enables MXFP8 intermediate route-out for FlyDSL stage2 MoE on gfx950
*   [#4118](https://github.com/ROCm/aiter/pull/4118) (opened) implements ATOM MXFP4 scale shuffle
</details>

<details>
<summary>Parallelism & scheduling (7)</summary>

*   [#3924](https://github.com/ROCm/aiter/pull/3924) supports FlyDSL all2all communication
*   [#4153](https://github.com/ROCm/aiter/pull/4153) adds naive implementation of gfx1250 communication kernel
*   [#3899](https://github.com/ROCm/aiter/pull/3899) adds quickreduce int3 for distributed communication
*   [#4110](https://github.com/ROCm/aiter/pull/4110) supports emit_bf16 for per-token fused AllReduce, RMSNorm, and FP8 quant
*   [#4104](https://github.com/ROCm/aiter/pull/4104) (opened) adds QuickReduce RMSNorm fusion kernel
*   [#4084](https://github.com/ROCm/aiter/pull/4084) (opened) eliminates end_sync in custom allreduce by delaying input tensor release
*   [#4081](https://github.com/ROCm/aiter/pull/4081) (opened) increases process group timeout from 600s to 1200s
</details>

<details>
<summary>Hardware & arch (1)</summary>

*   [#4122](https://github.com/ROCm/aiter/pull/4122) adds get_getamdgpu_arch to support The Rock
</details>

<details>
<summary>Tests (2)</summary>

*   [#4092](https://github.com/ROCm/aiter/pull/4092) adds tuned config cross-file shape-collision guard and skill
*   [#4154](https://github.com/ROCm/aiter/pull/4154) (opened) adds const QKV test for ASM MXFP8 MHA on gfx1250
</details>

<details>
<summary>CI & build (11)</summary>

*   [#4160](https://github.com/ROCm/aiter/pull/4160) adds review-pr Claude Code skill for AITER PRs
*   [#4094](https://github.com/ROCm/aiter/pull/4094) auto-updates split test FILE_TIMES
*   [#4120](https://github.com/ROCm/aiter/pull/4120) syncs ATOM Kimi default model name
*   [#4091](https://github.com/ROCm/aiter/pull/4091) pins requirements.txt versions to reduce supply-chain risk
*   [#4123](https://github.com/ROCm/aiter/pull/4123) makes test log uploads non-blocking
*   [#4138](https://github.com/ROCm/aiter/pull/4138) reverts making test log uploads non-blocking
*   [#4148](https://github.com/ROCm/aiter/pull/4148) skips MI300X 8-GPU multi-GPU tests
*   [#4100](https://github.com/ROCm/aiter/pull/4100) (opened) adds ATOM DI CI smoke workflow
*   [#4101](https://github.com/ROCm/aiter/pull/4101) (opened) adds release test for Triton release_tmp index and afp4wfp4 gfx950 config
*   [#4121](https://github.com/ROCm/aiter/pull/4121) (opened) reproduces ATOM CI error with CK update
*   [#4116](https://github.com/ROCm/aiter/pull/4116) (opened) updates FlyDSL to 0.2.3
</details>

<details>
<summary>Bugfixes (15)</summary>

*   [#4131](https://github.com/ROCm/aiter/pull/4131) wraps per_group emit_bf16 fused AR+RMSNorm+quant in a torch.library op
*   [#4106](https://github.com/ROCm/aiter/pull/4106) fixes py3.10 wheel build broken by pandas pin
*   [#4090](https://github.com/ROCm/aiter/pull/4090) avoids shell=True with interpolated paths in JIT build utils
*   [#4099](https://github.com/ROCm/aiter/pull/4099) fixes undeclared flag_color in TWOSHOT_DISPATCH_TP2_ONLY
*   [#3988](https://github.com/ROCm/aiter/pull/3988) fixes MI350 MLA PS mode BF16 address over 32bit and random NaN error
*   [#4070](https://github.com/ROCm/aiter/pull/4070) fixes max_fp8 from 240 to 448 for gfx950
*   [#4086](https://github.com/ROCm/aiter/pull/4086) (opened) fixes Gluon APIs for gfx1250
*   [#4117](https://github.com/ROCm/aiter/pull/4117) (opened) fixes ragged split_indptr short-seq for MLA v4 nm
*   [#4144](https://github.com/ROCm/aiter/pull/4144) (opened) gates persistent MLA decode kernel by batch size
*   [#4108](https://github.com/ROCm/aiter/pull/4108) (opened) fixes a8w4 CDNA4 scale addressing for padded MoE shapes
*   [#4145](https://github.com/ROCm/aiter/pull/4145) (opened) fixes block pointers only supporting 32-bit error on gfx1250
*   [#4163](https://github.com/ROCm/aiter/pull/4163) (opened) fixes gfx950 Triton codegen crashes and numeric miscompiles
*   [#4082](https://github.com/ROCm/aiter/pull/4082) (opened) synchronizes custom collectives before return
*   [#4141](https://github.com/ROCm/aiter/pull/4141) (opened) fixes Gemma 4w4 split-k bug
*   [#4155](https://github.com/ROCm/aiter/pull/4155) (opened) adds software workaround for setreg hardware bug in FMHA fwd BF16 on gfx1250
</details>

<details>
<summary>Refactors (2)</summary>

*   [#4079](https://github.com/ROCm/aiter/pull/4079) condenses comments in attention kernels
*   [#4107](https://github.com/ROCm/aiter/pull/4107) (opened) refactors Opus MoE stage2 pipeline and generated TUs
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f181e617062dab2a5a37085f858c3fafd6450fa194d579a4f7d27d0585fbad25 -->
