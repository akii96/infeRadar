# AITER: PR digest (2026-06-24 to 2026-06-28)

_51 merged, 50 newly opened - source ROCm/AITER, generated 2026-06-28T22:05:36Z_

## TL;DR
* **DeepSeek & Kimi focus**: DeepSeek (v3.2/v4/R1) drove the most activity, specifically targeting MXFP4/FP8 MoE and MLA decode performance on MI350 (gfx950) and MI325X (gfx942). Kimi and MiniMax also saw targeted MoE and GEMM tuning.
* **FlyDSL & Gluon expansion**: Major backend shifts with FlyDSL gaining fused MoE (route+psum+quant+scatter) and all-to-all communication. Gluon added new sparse decode and fused KV cache reshape kernels.
* **MLA & Attention wins**: Significant ASM and HIP-level work for Multi-Head Latent Attention (MLA), including v4 decode for MI350, strided `q_nope` support, and new FlyDSL reduce decode kernels.
* **Quantization & MoE**: Heavy churn around MXFP4 and FP8/BF16 blockscale quantization, particularly for 2-stage MoE dispatch and fused QK/KV norm operations.

## Most important PRs
* **[#3851](https://github.com/ROCm/aiter/pull/3851)** adds a highly-fused FlyDSL kernel for grouped MoE on gfx1250, combining routing, partial sum, quantization, and scatter steps to drastically reduce memory bandwidth overhead.
* **[#3541](https://github.com/ROCm/aiter/pull/3541)** introduces fused QK/KV normalization, RoPE, and group-quantization operations, streamlining the prefill and decode attention pipelines for quantized models.
* **[#3112](https://github.com/ROCm/aiter/pull/3112)** ships the v4 MLA decode ASM kernel specifically optimized for MI350 (gfx950), significantly improving DeepSeek decode performance.
* **[#3926](https://github.com/ROCm/aiter/pull/3926)** (Newly opened) begins porting MXFP4 MoE kernels to the FlyDSL backend for gfx942, critical for next-gen quantized model throughput.
* **[#3803](https://github.com/ROCm/aiter/pull/3803)** implements multi-backend (HIP and FlyDSL) causal Conv1D kernels for prefill, expanding support for Gated Delta Networks (GDN).

## More changes by area

<details>
<summary>Kernels & attention (24)</summary>

- [#3475](https://github.com/ROCm/aiter/pull/3475) Add Gluon sparse PagedAttention decode for gfx1250
- [#3965](https://github.com/ROCm/aiter/pull/3965) Add Triton-based Gluon fused KV cache reshape for gfx1250
- [#3963](https://github.com/ROCm/aiter/pull/3963) Tune Gluon UA2D and add split-K support for gfx1250
- [#3955](https://github.com/ROCm/aiter/pull/3955) Add additional MLA kernels for gfx1250
- [#3841](https://github.com/ROCm/aiter/pull/3841) Support strided q_nope in fused QK RoPE cache for prefill and decode
- [#3874](https://github.com/ROCm/aiter/pull/3874) Add MLA persistent/split-KV BF16 decode on gfx950 for long queries
- [#3426](https://github.com/ROCm/aiter/pull/3426) Add BF16 qh8 qseqlen=2 MLA decode kernel for gfx950
- [#3966](https://github.com/ROCm/aiter/pull/3966) Enable SWA and update asserts for Gluon UA3D on gfx12
- [#3879](https://github.com/ROCm/aiter/pull/3879) Add kargs preload to BF16 ASM MHA kernel
- [#3901](https://github.com/ROCm/aiter/pull/3901) [Opened] Add FlyDSL MLA reduce decode kernel for gfx942
- [#3913](https://github.com/ROCm/aiter/pull/3913) [Opened] Add FlyDSL gfx942 FP8 MQA logits indexer kernel and fix Triton FN/FNUZ
- [#3976](https://github.com/ROCm/aiter/pull/3976) [Opened] Implement Flash Attention backward kernel in FlyDSL
- [#3900](https://github.com/ROCm/aiter/pull/3900) [Opened] Unify scale and weight shuffling into shuffle.py
- [#3890](https://github.com/ROCm/aiter/pull/3890) [Opened] Support Multi-Token Prediction (MTP) for MLA in Gluon
- [#3962](https://github.com/ROCm/aiter/pull/3962) [Opened] Add split-K long-context decode for shuffled FP8 SWA path
- [#3923](https://github.com/ROCm/aiter/pull/3923) [Opened] Change default PagedAttention reduce kernel from CXX to FlyDSL
- [#3944](https://github.com/ROCm/aiter/pull/3944) [Opened] Add JIT build support for FlyDSL PagedAttention reduce
- [#3936](https://github.com/ROCm/aiter/pull/3936) [Opened] Add XCD-aware spatial workgroup mapping for MHA and GQA
- [#3957](https://github.com/ROCm/aiter/pull/3957) [Opened] Add mask=0 kernel for BF16 ASM MHA
- [#3959](https://github.com/ROCm/aiter/pull/3959) [Opened] Add sliding-window decode over shuffled FP8 paged KV
- [#3971](https://github.com/ROCm/aiter/pull/3971) [Opened] Add Gluon attention reduce kernel
- [#3956](https://github.com/ROCm/aiter/pull/3956) [Opened] Support gfx1201 unified attention within LDS limits
- [#3939](https://github.com/ROCm/aiter/pull/3939) [Opened] Map top-left to bottom-right for self-attention
- [#3915](https://github.com/ROCm/aiter/pull/3915) [Opened] Use 8 warps for gfx1151 3D decode in unified attention

</details>

<details>
<summary>MoE & quantization (29)</summary>

- [#3931](https://github.com/ROCm/aiter/pull/3931) Clean up FlyDSL GEMM implementation
- [#3751](https://github.com/ROCm/aiter/pull/3751) Support NoPE-FP8 / RoPE-BF16 sparse prefill attention for DeepSeek-v4 on gfx950
- [#3945](https://github.com/ROCm/aiter/pull/3945) Add end-to-end v1 tests for gfx1250 MoE 2-mode
- [#3968](https://github.com/ROCm/aiter/pull/3968) Revert activation and sorting implementation selection to upstream
- [#3891](https://github.com/ROCm/aiter/pull/3891) Revert unifying scale and weight shuffling into shuffle.py
- [#3914](https://github.com/ROCm/aiter/pull/3914) Optimize Triton MoE kernels
- [#3740](https://github.com/ROCm/aiter/pull/3740) Honor CK padding for bpreshuffle padded K
- [#3888](https://github.com/ROCm/aiter/pull/3888) Add AOT pre-compile and low-overhead launch for MXFP4 MoE
- [#3930](https://github.com/ROCm/aiter/pull/3930) Refactor MoE sorting to align with upstream
- [#3767](https://github.com/ROCm/aiter/pull/3767) Add SwiGLU limit for MoE group GEMM on gfx1250 for DeepSeek-v4
- [#3769](https://github.com/ROCm/aiter/pull/3769) Parallelize standalone main() compile drivers for FlyDSL AOT
- [#3893](https://github.com/ROCm/aiter/pull/3893) Decouple moe_topk from CK tile by splitting module and headers
- [#3872](https://github.com/ROCm/aiter/pull/3872) Add gemma_norm to add_rmsnorm_quant_kernel
- [#3929](https://github.com/ROCm/aiter/pull/3929) Fix gemma_norm for backward compatibility
- [#3892](https://github.com/ROCm/aiter/pull/3892) Use template function in Opus to get max FP8 dtype
- [#3868](https://github.com/ROCm/aiter/pull/3868) Remove from_torch_tensor utility
- [#3903](https://github.com/ROCm/aiter/pull/3903) Enable FP8/BF8 scaled converters on gfx1200/gfx1201/gfx1250
- [#3921](https://github.com/ROCm/aiter/pull/3921) Update A8W8 MLA kernels to global-load CKV variant on gfx950
- [#3969](https://github.com/ROCm/aiter/pull/3969) [Opened] Optimize A8W8 PTPC GEMM kernel in FlyDSL for gfx1250
- [#3907](https://github.com/ROCm/aiter/pull/3907) [Opened] Add gather MoE support in FlyDSL for gfx1250
- [#3918](https://github.com/ROCm/aiter/pull/3918) [Opened] Fix AOT deadlock in MoE
- [#3937](https://github.com/ROCm/aiter/pull/3937) [Opened] Add Gluon MXFP4 fused reduce quant kernel
- [#3970](https://github.com/ROCm/aiter/pull/3970) [Opened] Add Gluon MoE reduce kernel
- [#3941](https://github.com/ROCm/aiter/pull/3941) [Opened] Add FlyDSL MXFP4 GEMM kernel
- [#3886](https://github.com/ROCm/aiter/pull/3886) [Opened] Add OpenAI SwiGLU for per-token FP8 CK XDL 2-stage MoE
- [#3902](https://github.com/ROCm/aiter/pull/3902) [Opened] Add sigmoid score_mode to flat top-K routing path
- [#3972](https://github.com/ROCm/aiter/pull/3972) [Opened] Add GeLU-Tanh activation to no-quant CK 2-stage fused MoE
- [#3975](https://github.com/ROCm/aiter/pull/3975) [Opened] Add BM64 kernel for MoE
- [#3973](https://github.com/ROCm/aiter/pull/3973) [Opened] Fix MoE 2-stage dispatch for non-128-divisible inter_dim

</details>

<details>
<summary>Performance & Tuning (18)</summary>

- [#3881](https://github.com/ROCm/aiter/pull/3881) Add gfx942 WKC/split-K GEMM paths and update DeepSeek-v4 BF16 configs
- [#3895](https://github.com/ROCm/aiter/pull/3895) Add DeepSeek-v4 BF16 K=4096 GEMM configs for gfx950
- [#3465](https://github.com/ROCm/aiter/pull/3465) Add MLA metadata parallel path for performance
- [#3887](https://github.com/ROCm/aiter/pull/3887) Lock MXFP4 tuned config to manually selected ones
- [#3831](https://github.com/ROCm/aiter/pull/3831) Add BF16 GPT-OSS tuning configs for gfx1250
- [#3790](https://github.com/ROCm/aiter/pull/3790) Add DeepSeek-v4 config and kernel_type to BF16 GEMM on gfx1250
- [#3898](https://github.com/ROCm/aiter/pull/3898) Add tuned config for MiniMax M3 PTPC FP8 GEMM
- [#3961](https://github.com/ROCm/aiter/pull/3961) Tune BMM for TP1 and DP on gfx950
- [#3950](https://github.com/ROCm/aiter/pull/3950) Tune config for A8W8 blockscale on gfx1250
- [#3927](https://github.com/ROCm/aiter/pull/3927) Add DeepSeek-v4 LM head shape to BF16 config
- [#3951](https://github.com/ROCm/aiter/pull/3951) [Opened] Add tuned A8W8 blockscale GEMM and FMoE configs for DeepSeek-v3.2 on MI325X
- [#3974](https://github.com/ROCm/aiter/pull/3974) [Opened] Add Qwen3.5-397B MXFP4 A16W16 GEMM tuning configs
- [#3967](https://github.com/ROCm/aiter/pull/3967) [Opened] Tune A8W8 blockscale GEMM on gfx12
- [#3946](https://github.com/ROCm/aiter/pull/3946) [Opened] Update MoE tuned configs for DeepSeek and GLM
- [#3897](https://github.com/ROCm/aiter/pull/3897) [Opened] Tune MoE GEMM for FlyDSL on gfx1250
- [#3911](https://github.com/ROCm/aiter/pull/3911) [Opened] Add expert=256/topk=8 MXFP4 tuned entries for DeepSeek-v3/R1 on gfx950
- [#3920](https://github.com/ROCm/aiter/pull/3920) [Opened] Add gfx-aware tuned CSV handling and column-safe row processing
- [#3917](https://github.com/ROCm/aiter/pull/3917) [Opened] Add INT8 W8A8 GEMM default config for gfx1151

</details>

<details>
<summary>Parallelism & distributed (8)</summary>

- [#3745](https://github.com/ROCm/aiter/pull/3745) Unlock 80-tokens limit for AR fusion 1-stage
- [#3880](https://github.com/ROCm/aiter/pull/3880) Correct AR 1-stage gating condition
- [#3924](https://github.com/ROCm/aiter/pull/3924) [Opened] Support FlyDSL all-to-all communication
- [#3978](https://github.com/ROCm/aiter/pull/3978) [Opened] Avoid scatter reduce copy and add XCD swizzle support
- [#3899](https://github.com/ROCm/aiter/pull/3899) [Opened] Add quickreduce int3 for communication
- [#3938](https://github.com/ROCm/aiter/pull/3938) [Opened] Gate custom all-reduce on XGMI topology
- [#3928](https://github.com/ROCm/aiter/pull/3928) [Opened] Make quick all-reduce flag sync CUDA-graph-safe
- [#3977](https://github.com/ROCm/aiter/pull/3977) [Opened] Correct fake register of fused_allreduce_rmsnorm_quant

</details>

<details>
<summary>Bugfixes (5)</summary>

- [#2642](https://github.com/ROCm/aiter/pull/2642) Enable MXFP4 MoE at TP=4/8 via CKTile a4w4 kernels and quant fixes
- [#3884](https://github.com/ROCm/aiter/pull/3884) Fix accumulation and clean up RadeonFlow
- [#3904](https://github.com/ROCm/aiter/pull/3904) Fix max_m and round_up logic in RadeonFlow
- [#3910](https://github.com/ROCm/aiter/pull/3910) [Opened] Fix gfx950 FP8 persistent MLA folded dispatch
- [#3896](https://github.com/ROCm/aiter/pull/3896) [Opened] Fix HIP FP8 paged-attention kPerHead scale OOB page fault

</details>

<details>
<summary>Refactors & API (3)</summary>

- [#3952](https://github.com/ROCm/aiter/pull/3952) Drop gate_moe in CSV dispatch
- [#3940](https://github.com/ROCm/aiter/pull/3940) [Opened] Add fused_gemm_a16w16_split_cat to Triton
- [#3932](https://github.com/ROCm/aiter/pull/3932) [Opened] Edit aiter_opus_plus.h to use Opus API instead of ASM code

</details>

<details>
<summary>CI, Tests & Build (9)</summary>

- [#3908](https://github.com/ROCm/aiter/pull/3908) Run downstream tests on DO runners
- [#3953](https://github.com/ROCm/aiter/pull/3953) Use system Triton for vLLM benchmarks
- [#3912](https://github.com/ROCm/aiter/pull/3912) Use arch FP8 max in per-token quant reference tests
- [#3943](https://github.com/ROCm/aiter/pull/3943) Remove KV cache assert for old arch for upstream compatibility
- [#3934](https://github.com/ROCm/aiter/pull/3934) [Opened] Parametrize sweep to fix collection-time OOM in test_topk_plain
- [#3954](https://github.com/ROCm/aiter/pull/3954) [Opened] Avoid FP8 KV cache in Kimi vLLM gate
- [#3916](https://github.com/ROCm/aiter/pull/3916) [Opened] Run vLLM DeepSeek-v4 and MiniMax M3 on MI350X
- [#3919](https://github.com/ROCm/aiter/pull/3919) [Opened] Allow gfx1151 in cpp_itfs JIT arch validation
- [#3935](https://github.com/ROCm/aiter/pull/3935) [Opened] Testing CI trigger

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
