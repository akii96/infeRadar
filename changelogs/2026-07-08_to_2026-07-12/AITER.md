# AITER: PR digest (2026-07-08 to 2026-07-12)

_48 merged, 38 newly opened - source ROCm/AITER, generated 2026-07-12T21:55:19Z_

## TL;DR
- **DeepSeek, Qwen, and GLM** dominated model-specific optimizations, with heavy focus on DeepSeek-V3/R1 (DSv4) and GLM-5.1/5.2. Kimi and MiniMax also saw targeted quantization and MoE work.
- **Aggressive low-bit quantization and MoE** are the primary performance drivers, highlighted by the merger of a massive MXFP4 (A4W4) MoE backend for gfx950, A8W8 FlyDSL implementations, and FP8 blockscale GEMM tunings.
- **Next-gen hardware enablement** is accelerating, with heavy churn on gfx1250 (communication kernels, Gluon BF16 BMM, MoE optimizations) and newly opened work targeting gfx1201 (RDNA4) for FP8/BF16 attention and GEMMs.
- **FlyDSL is becoming mandatory** for MoE tuning, replacing fallback machinery, while Triton/Gluon kernels are seeing rapid iteration for attention (MHA, MLA) and GEMM operations across architectures.

## Most important PRs
- **[#3832](https://github.com/ROCm/aiter/pull/3832)** Introduces a massive MXFP4 (A4W4) MoE backend for gfx950 using FlyDSL. This major architectural addition enables extreme low-bit quantization for models like Kimi, significantly reducing memory bandwidth pressure during MoE routing.
- **[#3422](https://github.com/ROCm/aiter/pull/3422)** Adds comprehensive FP8 blockscale GEMM and FMoE tunings for GLM-5.1 on gfx942 (MI300X/MI325). This maximizes throughput for the GLM family by leveraging hardware-native FP8 capabilities.
- **[#4151](https://github.com/ROCm/aiter/pull/4151)** Implements A8W8 GEMM kernels using FlyDSL. This provides a highly optimized 8-bit weight/activation quantization path critical for serving DeepSeek, GLM, and MiniMax models efficiently.
- **[#4025](https://github.com/ROCm/aiter/pull/4025)** Removes FlyDSL fallback machinery from MoE tuning, making FlyDSL mandatory. This signals a definitive shift towards FlyDSL as the primary engine for performant MoE execution across all major model families.
- **[#4188](https://github.com/ROCm/aiter/pull/4188)** (Newly opened) Brings FlyDSL BF16 attention optimizations and a new FP8 attention implementation to gfx1201 (RDNA4). This represents a significant push to enable high-performance, low-precision attention on upcoming consumer/edge architectures.

## More changes by area

<details>
<summary>Performance & tuning (19)</summary>

- [#4135](https://github.com/ROCm/aiter/pull/4135) reduce A8W4 GEMM2 VGPR pressure for DeepSeek-V4
- [#4192](https://github.com/ROCm/aiter/pull/4192) tune A8W8 GEMM and quantization configs
- [#4199](https://github.com/ROCm/aiter/pull/4199) remove GRID_MN and re-tune A8W8 GEMM for Pro and Flash
- [#4130](https://github.com/ROCm/aiter/pull/4130) update MoE tuned configurations for DeepSeek and GPT-OSS
- [#4202](https://github.com/ROCm/aiter/pull/4202) route decode-M DeepSeek shapes to Triton for A8W8 blockscale GEMM
- [#4095](https://github.com/ROCm/aiter/pull/4095) add tuned configs for GLM-5.2 FP8 PTPC GEMM and MXFP8/MXFP4 MoE
- [#4125](https://github.com/ROCm/aiter/pull/4125) further tune A8W8 GEMM configurations
- [#4093](https://github.com/ROCm/aiter/pull/4093) update afp4wfp4/afp16wfp4 config for Triton async marker
- [#4112](https://github.com/ROCm/aiter/pull/4112) add Qwen3.5 gfx942 tuned GEMM config
- [#3911](https://github.com/ROCm/aiter/pull/3911) add expert=256/topk=8 MXFP4 tuned entries for DeepSeek-V3/R1 on gfx950
- [#4053](https://github.com/ROCm/aiter/pull/4053) optimize Qwen3.5-397B PTPC FP8 MoE performance for batch sizes 64 and 128
- [#4178](https://github.com/ROCm/aiter/pull/4178) guard A8W8 block_size_k 128 to 64 fallback on gfx1250
- [#4140](https://github.com/ROCm/aiter/pull/4140) (opened) tune GFX1201 DSV4-Flash FP16 and FP8 GEMMs for ATOM
- [#4203](https://github.com/ROCm/aiter/pull/4203) (opened) tune DSv4 FP8 A8W8 blockscale BpreShuffle and A16W16 GEMM for gfx950
- [#4196](https://github.com/ROCm/aiter/pull/4196) (opened) improve gfx1250 MoE occupancy and preload GEMM kernel args
- [#4180](https://github.com/ROCm/aiter/pull/4180) (opened) config-gate BLOCK_Q fp8_mqa_logits for DSA indexer prefill on gfx950
- [#4198](https://github.com/ROCm/aiter/pull/4198) (opened) tune MoE A8W4 TP4 configurations
- [#4191](https://github.com/ROCm/aiter/pull/4191) (opened) tune A8W8 GEMM and MoE configurations
- [#4190](https://github.com/ROCm/aiter/pull/4190) (opened) correct A8W8 default config to avoid accumulator spill on gfx950

</details>

<details>
<summary>Kernels & attention (18)</summary>

- [#4200](https://github.com/ROCm/aiter/pull/4200) implement Gluon BF16 BMM for gfx1250
- [#4128](https://github.com/ROCm/aiter/pull/4128) implement pa_prefill_sparse for Gluon on gfx1250
- [#4033](https://github.com/ROCm/aiter/pull/4033) add smooth Q and Hadamard rotation to Qwen Sage attention v1
- [#4104](https://github.com/ROCm/aiter/pull/4104) add QuickReduce RMSNorm fusion kernel
- [#4159](https://github.com/ROCm/aiter/pull/4159) add paged SWA cache-write variant for qk_norm_rope in FlyDSL
- [#3188](https://github.com/ROCm/aiter/pull/3188) add native MLA QH64 FP8 persistent decode kernel for gfx942
- [#4129](https://github.com/ROCm/aiter/pull/4129) refine MLA v4 configurations
- [#4156](https://github.com/ROCm/aiter/pull/4156) update MLA QH16 to support global load KV
- [#4161](https://github.com/ROCm/aiter/pull/4161) (opened) add strided-batched MXFP4/MXFP8 preshuffle batched GEMM for gfx950
- [#4205](https://github.com/ROCm/aiter/pull/4205) (opened) add OPUS gfx950 BF16 FMHA d192x128 kernel
- [#4136](https://github.com/ROCm/aiter/pull/4136) (opened) implement jagged_dense_bmm_broadcast_add for MI300X in FlyDSL
- [#4127](https://github.com/ROCm/aiter/pull/4127) (opened) add Opus PA decode skeleton with self-contained sp3 MFMA kernels
- [#4206](https://github.com/ROCm/aiter/pull/4206) (opened) add FlyDSL blockwise BMM W8A8 for gfx1250
- [#4147](https://github.com/ROCm/aiter/pull/4147) (opened) add MHA Gluon kernel for gfx950
- [#4166](https://github.com/ROCm/aiter/pull/4166) (opened) replace CK FP8 rowwise GEMM with FlyDSL preshuffle kernel
- [#4154](https://github.com/ROCm/aiter/pull/4154) (opened) support causal mask and add init-pattern for ASM MXFP8 MHA on gfx1250
- [#4146](https://github.com/ROCm/aiter/pull/4146) (opened) add fused_add_rmsnorm_pad Gluon equivalent function
- [#4186](https://github.com/ROCm/aiter/pull/4186) (opened) revert MLA v4 refinement

</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#4150](https://github.com/ROCm/aiter/pull/4150) optimize mxscale/MoE for DeepSeek on gfx1250
- [#4152](https://github.com/ROCm/aiter/pull/4152) optimize Opus MoE A8W4 stage2 candidate set
- [#4179](https://github.com/ROCm/aiter/pull/4179) (opened) implement FlyDSL MXMoE v2
- [#4204](https://github.com/ROCm/aiter/pull/4204) (opened) support A8W8 blockscale BpreShuffle GEMM for DeepSeek on gfx942
- [#4165](https://github.com/ROCm/aiter/pull/4165) (opened) implement MoE EP for FlyDSL on gfx1250
- [#4139](https://github.com/ROCm/aiter/pull/4139) (opened) pack fp4/int4/uint4 as single sub-byte elements in containers
- [#4193](https://github.com/ROCm/aiter/pull/4193) (opened) add Gluon support for MXFP4 quant kernel on gfx950 and gfx1250
- [#4170](https://github.com/ROCm/aiter/pull/4170) (opened) fuse activation and quantization for MoE A8W4
- [#4143](https://github.com/ROCm/aiter/pull/4143) (opened) update DeepSeek-V4 MoE and quantization kernels

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#3924](https://github.com/ROCm/aiter/pull/3924) support FlyDSL all2all communication for MoE on gfx950
- [#4153](https://github.com/ROCm/aiter/pull/4153) implement naive communication kernel for gfx1250
- [#4207](https://github.com/ROCm/aiter/pull/4207) (opened) add IFOE cross-node custom all-reduce using fabric handles on gfx1250

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#4122](https://github.com/ROCm/aiter/pull/4122) add get_amdgpu_arch support for The Rock

</details>

<details>
<summary>API & serving (3)</summary>

- [#4157](https://github.com/ROCm/aiter/pull/4157) add environment variable to control kernel preload
- [#4189](https://github.com/ROCm/aiter/pull/4189) rename API components
- [#4158](https://github.com/ROCm/aiter/pull/4158) (opened) remove deprecated offset arg from tdm.async_gather calls on gfx1250

</details>

<details>
<summary>Tests, CI & build (11)</summary>

- [#4079](https://github.com/ROCm/aiter/pull/4079) condense comments in attention tests
- [#4120](https://github.com/ROCm/aiter/pull/4120) sync ATOM Kimi default model name
- [#4185](https://github.com/ROCm/aiter/pull/4185) update Triton version to 89002410
- [#4123](https://github.com/ROCm/aiter/pull/4123) make test log uploads non-blocking
- [#4138](https://github.com/ROCm/aiter/pull/4138) revert non-blocking test log uploads
- [#4116](https://github.com/ROCm/aiter/pull/4116) update FlyDSL to version 0.2.3
- [#4148](https://github.com/ROCm/aiter/pull/4148) skip MI300X 8-GPU multi-GPU tests
- [#4164](https://github.com/ROCm/aiter/pull/4164) modify runner override in ATOM tests
- [#4182](https://github.com/ROCm/aiter/pull/4182) (opened) add SGLang DSV4Pro FP8 1P1D workflow
- [#4184](https://github.com/ROCm/aiter/pull/4184) (opened) add MiniMax FP8 vLLM disagg Spur smoke workflow
- [#4177](https://github.com/ROCm/aiter/pull/4177) (opened) update Triton version to 89002410

</details>

<details>
<summary>Bugfixes (14)</summary>

- [#4131](https://github.com/ROCm/aiter/pull/4131) wrap per_group emit_bf16 fused AR+RMSNorm+quant in a torch.library op
- [#4197](https://github.com/ROCm/aiter/pull/4197) fix FlyDSL JIT compilation on gfx1250
- [#4201](https://github.com/ROCm/aiter/pull/4201) fix pa_decode_sparse and pa_prefill_sparse new async_gather API
- [#4163](https://github.com/ROCm/aiter/pull/4163) fix gfx950 Triton codegen crashes and numeric miscompiles
- [#4194](https://github.com/ROCm/aiter/pull/4194) fix Qwen3.5 397B gfx942 tuned GEMM dispatch
- [#4172](https://github.com/ROCm/aiter/pull/4172) fix OOM in MoE CI tests
- [#4155](https://github.com/ROCm/aiter/pull/4155) add software workaround for setreg hardware bug in FMHA fwd BF16 on gfx1250
- [#4144](https://github.com/ROCm/aiter/pull/4144) (opened) gate persistent MLA decode kernel by batch size
- [#4175](https://github.com/ROCm/aiter/pull/4175) (opened) fix missing CK compile dependencies
- [#4171](https://github.com/ROCm/aiter/pull/4171) (opened) fix review-pr skill v2 dispatch gap rule and timing errors
- [#4195](https://github.com/ROCm/aiter/pull/4195) (opened) floor FP8 e8m0 group amax to avoid zero-scale in fused QK
- [#4145](https://github.com/ROCm/aiter/pull/4145) (opened) fix block pointers only supporting 32-bit error
- [#4141](https://github.com/ROCm/aiter/pull/4141) (opened) fix Gemma 4W4 split-K bug
- [#4181](https://github.com/ROCm/aiter/pull/4181) (opened) fix ragged-K mask in batched A16WFP4 GEMM

</details>

<details>
<summary>Other (3)</summary>

- [#4160](https://github.com/ROCm/aiter/pull/4160) add review-pr Claude Code skill for AITER PRs
- [#4173](https://github.com/ROCm/aiter/pull/4173) shuffle dependencies
- [#4167](https://github.com/ROCm/aiter/pull/4167) (opened) shuffle scale guinterleave

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 15373f56a933982d414abd6cfe24e8d2b9aefbb5325212086f2cbedc4313cc0a -->
