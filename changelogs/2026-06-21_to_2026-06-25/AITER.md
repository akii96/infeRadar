# AITER: PR digest (2026-06-21 to 2026-06-25)

_52 merged, 47 newly opened - source ROCm/AITER, generated 2026-06-25T11:41:08Z_

## TL;DR
- DeepSeek (V3/V4) and MiniMax (M2/M3) dominated this cycle, with a massive push to optimize MXFP4 (a4w4) MoE and MLA performance on next-gen AMD hardware (gfx950/MI350 and gfx1250).
- A new FlyDSL backend for MXFP4 MoE is in flight for gfx950 and gfx942, alongside merged HIP Sort/Quant integrations to reduce routing overhead for Kimi and DeepSeek.
- Significant attention and MLA advancements landed, including sparse prefill Triton/Gluon kernels for gfx950, persistent/split-KV BF16 decode, and MTP support.
- Major kernel fusions were merged for MiniMax (qknorm + allreduce + rope), alongside extensive GEMM tuning (BF16, FP8, blockscale) across DSV4 and MiniMax M3.

## Most important PRs
- **[#3832](https://github.com/ROCm/aiter/pull/3832)** (Newly opened): Adds the MXFP4 (a4w4) MoE backend via FlyDSL for gfx950. This massive 7.6k-line change is a critical enabler for running Kimi and DeepSeek efficiently on MI350 hardware.
- **[#3856](https://github.com/ROCm/aiter/pull/3856)** (Newly opened): Integrates DeepSeek V4 A8W4 decode and adds gfx950 MoE stage 2 kernels. This provides the necessary attention and MoE infrastructure for DSV4 on MI350.
- **[#3825](https://github.com/ROCm/aiter/pull/3825)** (Merged): Implements `k_wave` support for FP4 GEMM1 and tunes configurations for DeepSeek V3/V4. This directly improves throughput for DeepSeek's heavily quantized MoE layers.
- **[#3827](https://github.com/ROCm/aiter/pull/3827)** (Merged): Integrates HIP-based Sort and Quantization into the MoE pipeline. This optimizes the routing and quantization overhead specifically targeted at Kimi models.
- **[#3475](https://github.com/ROCm/aiter/pull/3475)** (Merged): Adds sparse paged attention decode for gfx1250 using the Gluon/Triton backend. This significantly improves decode latency for models leveraging sparse attention patterns.

## More changes by area

<details>
<summary>MoE & Quantization (36)</summary>

- [#3881](https://github.com/ROCm/aiter/pull/3881) adds gfx942 WKC/splitK GEMM paths and updates DSV4 BF16 tuning configs
- [#3851](https://github.com/ROCm/aiter/pull/3851) (open) adds fused MoE route+psum+quant+scatter kernel for grouped MoE on gfx1250
- [#3926](https://github.com/ROCm/aiter/pull/3926) (open) implements FlyDSL MXFP4 MoE for gfx942
- [#3887](https://github.com/ROCm/aiter/pull/3887) fixes MXFP4 tuned config lock to manually selected ones
- [#3764](https://github.com/ROCm/aiter/pull/3764) fixes FlyDSL type-closure incompatibility in mixed MoE kernels
- [#3740](https://github.com/ROCm/aiter/pull/3740) honors CK padding for bpreshuffle padded K
- [#3888](https://github.com/ROCm/aiter/pull/3888) adds AOT pre-compile and low-overhead launch for MXFP4 MoE
- [#3828](https://github.com/ROCm/aiter/pull/3828) brings FlyDSL MXFP4 a4w4 MoE gemm1/gemm2 to parity with the HIP backend
- [#3769](https://github.com/ROCm/aiter/pull/3769) parallelizes standalone main() compile drivers for FlyDSL AOT
- [#3343](https://github.com/ROCm/aiter/pull/3343) adds blockscale HIP-to-Triton fallback and tuning configs for gfx1201 gemm_a8w8
- [#3798](https://github.com/ROCm/aiter/pull/3798) tunes DSV4 config for gemm_a8w8_blockscale on MI450
- [#3843](https://github.com/ROCm/aiter/pull/3843) adds GELU_BIAS epilogue support to hipb_mm
- [#3904](https://github.com/ROCm/aiter/pull/3904) fixes max_m and round_up logic in RadeonFlow
- [#3884](https://github.com/ROCm/aiter/pull/3884) fixes accumulation and cleans up RadeonFlow
- [#3845](https://github.com/ROCm/aiter/pull/3845) refactors module_gated_rmsnorm_quant
- [#3859](https://github.com/ROCm/aiter/pull/3859) adds TP2 MXFP4 fused-MoE configs for Qwen3.5-397B
- [#3861](https://github.com/ROCm/aiter/pull/3861) improves performance of FlyDSL MXFP4 a4w4 MoE
- [#3840](https://github.com/ROCm/aiter/pull/3840) pipelines FP4-out epilog LDS reads for FlyDSL MXFP4 gemm2
- [#3860](https://github.com/ROCm/aiter/pull/3860) arch-guards FP8/BF8 packed-cvt builtins for RDNA3/3.5
- [#3892](https://github.com/ROCm/aiter/pull/3892) uses template function in Opus to get the max of FP8 dtype
- [#3903](https://github.com/ROCm/aiter/pull/3903) enables FP8/BF8 scaled converters on gfx1200/gfx1201/gfx1250
- [#3907](https://github.com/ROCm/aiter/pull/3907) (open) adds gather MoE support for FlyDSL on gfx1250
- [#3835](https://github.com/ROCm/aiter/pull/3835) (open) adds tuned configs for DSV4 a4w4
- [#3871](https://github.com/ROCm/aiter/pull/3871) (open) adds gu interleave support for MoE
- [#3844](https://github.com/ROCm/aiter/pull/3844) (open) adds kernel for rmsnorm and per-token quant
- [#3834](https://github.com/ROCm/aiter/pull/3834) (open) adds kwave support for gfx1250
- [#3876](https://github.com/ROCm/aiter/pull/3876) (open) supports fused shared expert topk append
- [#3914](https://github.com/ROCm/aiter/pull/3914) (open) optimizes MoE in Triton
- [#3897](https://github.com/ROCm/aiter/pull/3897) (open) tunes MoE GEMM for FlyDSL on gfx1250
- [#3893](https://github.com/ROCm/aiter/pull/3893) (open) decouples moe_topk from CK tile by splitting module and headers
- [#3886](https://github.com/ROCm/aiter/pull/3886) (open) adds OAI SwiGLU for per-token FP8 CK XDL 2-stage MoE
- [#3862](https://github.com/ROCm/aiter/pull/3862) (open) corrects padded SEPARATED w13 in BF16 CK-Tile gate-up
- [#3902](https://github.com/ROCm/aiter/pull/3902) (open) adds sigmoid score_mode to flat topk routing path in Triton
- [#3911](https://github.com/ROCm/aiter/pull/3911) (open) adds expert=256/topk=8 MXFP4 tuned entries for DeepSeek-V3/R1 on gfx950
- [#3917](https://github.com/ROCm/aiter/pull/3917) (open) adds INT8 W8A8 GEMM default config for gfx1151
- [#3868](https://github.com/ROCm/aiter/pull/3868) (open) removes from_torch_tensor from quant/norm

</details>

<details>
<summary>Kernels & Attention (24)</summary>

- [#3465](https://github.com/ROCm/aiter/pull/3465) adds MLA metadata parallel path
- [#3823](https://github.com/ROCm/aiter/pull/3823) unifies scale and weight shuffling into shuffle.py
- [#3891](https://github.com/ROCm/aiter/pull/3891) reverts the scale and weight shuffling unification
- [#3900](https://github.com/ROCm/aiter/pull/3900) (open) re-attempts unifying scale and weight shuffling
- [#3874](https://github.com/ROCm/aiter/pull/3874) adds support for MLA persistent/split-KV BF16 decode on gfx950
- [#3304](https://github.com/ROCm/aiter/pull/3304) adds FP8 qh32 seqlen=1 persistent MLA kernel support on gfx950
- [#3855](https://github.com/ROCm/aiter/pull/3855) fixes MLA metadata reduce_partial_map worst-case over-allocation OOM
- [#3879](https://github.com/ROCm/aiter/pull/3879) adds kargs preload to BF16 asm MHA
- [#3826](https://github.com/ROCm/aiter/pull/3826) patches MLA kernel
- [#3848](https://github.com/ROCm/aiter/pull/3848) refactors asm paged attention to assert
- [#3833](https://github.com/ROCm/aiter/pull/3833) (open) adds DSV4 sparse MLA prefill Triton and unifies with MLA Gluon kernel on gfx950
- [#3901](https://github.com/ROCm/aiter/pull/3901) (open) adds FlyDSL MLA reduce decode kernel for gfx942
- [#3913](https://github.com/ROCm/aiter/pull/3913) (open) adds FlyDSL gfx942 FP8 MQA logits indexer kernel and Triton FN/FNUZ fix
- [#3854](https://github.com/ROCm/aiter/pull/3854) (open) adds conv2d implicit GEMM kernel for gfx942
- [#3922](https://github.com/ROCm/aiter/pull/3922) (open) adds NoPE-fp8/RoPE-bf16 sparse prefill for gfx1250
- [#3890](https://github.com/ROCm/aiter/pull/3890) (open) supports MTP for MLA in Gluon
- [#3870](https://github.com/ROCm/aiter/pull/3870) (open) adds FlyDSL BSHD batch-mode dispatch for MHA on gfx1250
- [#3910](https://github.com/ROCm/aiter/pull/3910) (open) fixes gfx950 FP8 persistent MLA folded dispatch
- [#3858](https://github.com/ROCm/aiter/pull/3858) (open) adds split-D forward for non-power-of-2 head_dim in Triton MHA
- [#3841](https://github.com/ROCm/aiter/pull/3841) (open) supports strided q_nope in fused QK RoPE cache for MLA
- [#3923](https://github.com/ROCm/aiter/pull/3923) (open) changes default paged attention reduce kernel from cxx to FlyDSL
- [#3896](https://github.com/ROCm/aiter/pull/3896) (open) fixes HIP FP8 paged-attention kPerHead scale OOB page fault
- [#3915](https://github.com/ROCm/aiter/pull/3915) (open) uses 8 warps for gfx1151 3D decode in unified_attention
- [#3921](https://github.com/ROCm/aiter/pull/3921) (open) updates A8W8 MLA kernels to global-load ckv variant on gfx950

</details>

<details>
<summary>Performance & Tuning (11)</summary>

- [#3895](https://github.com/ROCm/aiter/pull/3895) adds DSV4 BF16 K=4096 GEMM configs for gfx950
- [#3814](https://github.com/ROCm/aiter/pull/3814) adds tuned DSV4-Flash FP8 GEMM configs
- [#3847](https://github.com/ROCm/aiter/pull/3847) adds MiniMax-M3 Eagle BF16 GEMM tuned configs
- [#3898](https://github.com/ROCm/aiter/pull/3898) adds tuned config for MiniMax M3 PTPC FP8 GEMM
- [#3822](https://github.com/ROCm/aiter/pull/3822) adds more tuning for Triton BF16 BMM
- [#3710](https://github.com/ROCm/aiter/pull/3710) tunes DSV4 BF16 GEMM
- [#3836](https://github.com/ROCm/aiter/pull/3836) (open) adds FP32-output untuned GEMM shapes for indexer kv_score
- [#3831](https://github.com/ROCm/aiter/pull/3831) (open) tunes BF16 for GPT-OSS
- [#3882](https://github.com/ROCm/aiter/pull/3882) (open) routes skinny BF16 GEMMs to split-K asm
- [#3927](https://github.com/ROCm/aiter/pull/3927) (open) adds DSV4 LM head shape in BF16 config
- [#3920](https://github.com/ROCm/aiter/pull/3920) (open) improves base_tuner with gfx-aware tuned CSV handling

</details>

<details>
<summary>Parallelism & Distributed (8)</summary>

- [#3650](https://github.com/ROCm/aiter/pull/3650) supports qknorm+allreduce+rope fusion pattern for MiniMax ops
- [#3736](https://github.com/ROCm/aiter/pull/3736) adds qknorm+rope for MiniMax-M2 TP1
- [#3872](https://github.com/ROCm/aiter/pull/3872) adds gemma_norm to add_rmsnorm_quant_kernel
- [#3838](https://github.com/ROCm/aiter/pull/3838) fixes stale IPC addresses by pinning graph-captured tensors
- [#3883](https://github.com/ROCm/aiter/pull/3883) reverts the fix for stale IPC addresses
- [#3899](https://github.com/ROCm/aiter/pull/3899) (open) adds quickreduce int3
- [#3924](https://github.com/ROCm/aiter/pull/3924) (open) supports FlyDSL all2all
- [#3880](https://github.com/ROCm/aiter/pull/3880) (open) fixes AllReduce 1-stage gating condition

</details>

<details>
<summary>API, Tests & CI (15)</summary>

- [#3795](https://github.com/ROCm/aiter/pull/3795) supports shuffle KV cache layout in idxsknorm_shuffle_layout
- [#3777](https://github.com/ROCm/aiter/pull/3777) refactors module_fused_split_gdr_update
- [#3821](https://github.com/ROCm/aiter/pull/3821) drops per-call memset on multi-block radix top-k
- [#3842](https://github.com/ROCm/aiter/pull/3842) adds top_k_first fast path for sampling
- [#3849](https://github.com/ROCm/aiter/pull/3849) auto-rebuilds JIT module on new GPU arch
- [#3912](https://github.com/ROCm/aiter/pull/3912) uses arch FP8 max in per-token quant reference for fused_qknorm
- [#3875](https://github.com/ROCm/aiter/pull/3875) (open) refactors module_groupnorm
- [#3918](https://github.com/ROCm/aiter/pull/3918) (open) fixes AOT deadlock
- [#3919](https://github.com/ROCm/aiter/pull/3919) (open) allows gfx1151 in cpp_itfs JIT arch validation
- [#3717](https://github.com/ROCm/aiter/pull/3717) auto-updates split test FILE_TIMES in CI
- [#3775](https://github.com/ROCm/aiter/pull/3775) detects rocm-core version via rpm in Triton
- [#3605](https://github.com/ROCm/aiter/pull/3605) adds a16w16 GEMM to op tuning workflow in CI
- [#3857](https://github.com/ROCm/aiter/pull/3857) splits Aiter tests from PR head ref in CI
- [#3916](https://github.com/ROCm/aiter/pull/3916) (open) runs vLLM DSV4 and MiniMax M3 on MI350X in CI
- [#3908](https://github.com/ROCm/aiter/pull/3908) (open) runs downstream tests on DO runners in CI

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
