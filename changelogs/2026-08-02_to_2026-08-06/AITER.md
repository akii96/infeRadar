# AITER: PR digest (2026-08-02 to 2026-08-06)

_50 merged, 64 newly opened - source ROCm/AITER, generated 2026-08-06T11:23:45Z_

## TL;DR
- **Model focus:** DeepSeek and Kimi dominated this cycle, with secondary focus on GLM and Qwen. Work heavily targeted MLA (Multi-Head Latent Attention) and MoE (Mixture of Experts) optimizations for these architectures.
- **Kernel expansion:** Massive kernel additions landed for the FlyDSL backend, including a v2 MXMoE implementation for gfx950 and new MLA reduce decode kernels for gfx942.
- **Quantization push:** Substantial in-progress work is expanding MXFP4 and A8W4 quantization support across GEMM and MoE paths, particularly targeting gfx1250 and gfx950 architectures.
- **Performance wins:** Key latency improvements merged, notably eliminating device-to-host synchronization in variable-length prefill GDN and optimizing Flash Attention sliding window performance.

## Most important PRs
- **[#4179](https://github.com/ROCm/aiter/pull/4179)** Implements a major v2 rewrite of the MXMoE kernel using FlyDSL for gfx950. This significantly optimizes MoE execution for GLM and other models by refactoring LDS loads and unifying GEMM paths.
- **[#4430](https://github.com/ROCm/aiter/pull/4430)** Adds a specialized DeepSeek v2/v3 MLA kernel for MI350 (gfx950). This handles the `nhead*qseqlen=128` edge case in PS mode, improving DeepSeek decode performance.
- **[#3901](https://github.com/ROCm/aiter/pull/3901)** Introduces a new FlyDSL-based MLA reduce decode kernel specifically targeting MI300 (gfx942) hardware.
- **[#4526](https://github.com/ROCm/aiter/pull/4526)** *(opened)* Massive in-progress refactor extending the MXFP4 GEMM1 replacement strategy to A8W4 quantization. This impacts DeepSeek, Kimi, GLM, and Qwen performance on gfx1250.
- **[#4532](https://github.com/ROCm/aiter/pull/4532)** Delivers a significant performance win by removing device-to-host synchronization overhead during variable-length prefill. It achieves this by utilizing reusable metadata for GDN.

## More changes by area

<details>
<summary>Kernels & attention (24)</summary>

- [#4265](https://github.com/ROCm/aiter/pull/4265) Enable conv2d Triton kernels for RDNA3 and RDNA3.5 (gfx1100/gfx1151)
- [#4335](https://github.com/ROCm/aiter/pull/4335) Update asm f4gemm with fp8 out support for gfx1250
- [#4576](https://github.com/ROCm/aiter/pull/4576) Merge gluon dsv4 attn prefill api entry with pa_prefill_sparse for gfx950
- [#4563](https://github.com/ROCm/aiter/pull/4563) Tune prefill MQA Logits kernel for GLM 5.x
- [#3936](https://github.com/ROCm/aiter/pull/3936) Add XCD-aware spatial workgroup mapping for MHA and GQA
- [#4521](https://github.com/ROCm/aiter/pull/4521) Support cp round robin for MLA PS mode fp8 on gfx950
- [#4602](https://github.com/ROCm/aiter/pull/4602) (opened) Add chunk delta attention optimization
- [#4568](https://github.com/ROCm/aiter/pull/4568) (opened) Add chunk_delta_attn Triton kernels
- [#4511](https://github.com/ROCm/aiter/pull/4511) (opened) Add OPUS mxfp8 pa mqa logits for gfx950
- [#4584](https://github.com/ROCm/aiter/pull/4584) (opened) Implement KDA gluon for gfx1250
- [#4577](https://github.com/ROCm/aiter/pull/4577) (opened) Enable KDA per-channel decay gate in FlyDSL GDR decode for Kimi-K3
- [#4582](https://github.com/ROCm/aiter/pull/4582) (opened) Add CDNA3 (gfx942) decode kernel for Gluon MLA
- [#4572](https://github.com/ROCm/aiter/pull/4572) (opened) Add attn_res Triton kernel for Kimi-K3
- [#4538](https://github.com/ROCm/aiter/pull/4538) (opened) Add gfx950 FP8 MQA logits indexer kernel in FlyDSL
- [#4573](https://github.com/ROCm/aiter/pull/4573) (opened) Support strided GDN decode state routing in FlyDSL
- [#4550](https://github.com/ROCm/aiter/pull/4550) (opened) Read strided q/k/v directly in flydsl_gdr_decode
- [#4523](https://github.com/ROCm/aiter/pull/4523) (opened) Enable chunk-gated-delta-rule-fwd-h on gfx1201
- [#4509](https://github.com/ROCm/aiter/pull/4509) (opened) Split-major grid and blocked stage-2 reduce for Kimi-K3 small-nhead decode
- [#4555](https://github.com/ROCm/aiter/pull/4555) (opened) Add stage2 logits block load for MLA
- [#4579](https://github.com/ROCm/aiter/pull/4579) (opened) Remove block pointers in lean_atten_paged and fix large-KV indexing
- [#4517](https://github.com/ROCm/aiter/pull/4517) (opened) Fix unified_attention num_stages > 1 crash with release_tmp3 on gfx950
- [#4536](https://github.com/ROCm/aiter/pull/4536) (opened) Fix invalid GFX12 architecture guard in unified attention gluon reduce
- [#4545](https://github.com/ROCm/aiter/pull/4545) (opened) Fix Triton cache flooding in _fwd_kernel_stage2_asm
- [#4507](https://github.com/ROCm/aiter/pull/4507) (opened) Size NUM_KV_SPLITS from the page table for Gluon MLA
</details>

<details>
<summary>MoE & quantization (32)</summary>

- [#4527](https://github.com/ROCm/aiter/pull/4527) Refactor and unify GEMM kernels and LDS load for gfx1250 FlyDSL
- [#4475](https://github.com/ROCm/aiter/pull/4475) Unify and rename A8W8 GEMM kernels for gfx1250 FlyDSL
- [#4534](https://github.com/ROCm/aiter/pull/4534) Optimize OPUS MoE SiTUv2 ability for Kimi on gfx950
- [#4564](https://github.com/ROCm/aiter/pull/4564) Add MoE a8w4 async scales for gfx1250
- [#4396](https://github.com/ROCm/aiter/pull/4396) Tune a8w8 gemm for Qwen3.5 MXFP4-AttnFP8 model
- [#4223](https://github.com/ROCm/aiter/pull/4223) Tune and include fuse-aware gfx950 fused GEMM A8W8 blockscale mul_add
- [#3739](https://github.com/ROCm/aiter/pull/3739) Add DSv3-MXFP4 E=33/topk9 fused-MoE shape configs
- [#4554](https://github.com/ROCm/aiter/pull/4554) (opened) Add tuned configs for Qwen3-VL-235B MXFP4 on gfx950
- [#4514](https://github.com/ROCm/aiter/pull/4514) (opened) Add multi-B MoE kernels for ROCm DWDP in FlyDSL
- [#4549](https://github.com/ROCm/aiter/pull/4549) (opened) Add fused online Hadamard rotation and MXFP4 quantization
- [#4596](https://github.com/ROCm/aiter/pull/4596) (opened) Add MoE reduce extract kernel
- [#4595](https://github.com/ROCm/aiter/pull/4595) (opened) Optimize tilesize 128x256x256 for fmoe gemm v2
- [#4597](https://github.com/ROCm/aiter/pull/4597) (opened) Improve tiny kernels for MoE quantization on gfx1250
- [#4562](https://github.com/ROCm/aiter/pull/4562) (opened) Add multicast support for MoE a8w4 on gfx1250 Gluon
- [#4586](https://github.com/ROCm/aiter/pull/4586) (opened) Support sorted intermediate layout for OPUS MoE
- [#4531](https://github.com/ROCm/aiter/pull/4531) (opened) Accept strided flash KV-cache view in mrope cache-quant
- [#4542](https://github.com/ROCm/aiter/pull/4542) (opened) Declare fused_moe/tuned_gemm preshuffled weight layout
- [#4510](https://github.com/ROCm/aiter/pull/4510) (opened) Honor b_nt in mixed-MoE stage-2 and retune configs
- [#4607](https://github.com/ROCm/aiter/pull/4607) (opened) Fuse A4W4 stage1 FP4 quantization for gfx1250
- [#4551](https://github.com/ROCm/aiter/pull/4551) (opened) Enable persistent stage2 grid for large-M mxfp8 in FlyDSL MoE
- [#4603](https://github.com/ROCm/aiter/pull/4603) (opened) Tune Kimi-K3 A4W4 configs for fmoe gemm on gfx950
- [#4592](https://github.com/ROCm/aiter/pull/4592) (opened) Add bf16 gemm config for DSv4 on gfx12
- [#4519](https://github.com/ROCm/aiter/pull/4519) (opened) Fix gfx950 small-M AFP4WFP4 correctness in Triton
- [#4581](https://github.com/ROCm/aiter/pull/4581) (opened) Make blockscale split-K deterministic
- [#4506](https://github.com/ROCm/aiter/pull/4506) Fix transpose_scale in fused_rms_fp8_group_quant
- [#4546](https://github.com/ROCm/aiter/pull/4546) Fix OOB scale descriptor in ptpc fp8 gemm for FlyDSL
- [#4548](https://github.com/ROCm/aiter/pull/4548) Fix a16w4 separated route regression and silent-wrong guards
- [#4463](https://github.com/ROCm/aiter/pull/4463) Add opt-in a4w4 SiTUv2 MoE path and fix SiTUv2 tuner defects
- [#4482](https://github.com/ROCm/aiter/pull/4482) Fix grouped-MoE expert scan above 512 experts and compute SiTUv2 on gfx1250
- [#4543](https://github.com/ROCm/aiter/pull/4543) Fix mxmoe gemm2 bugs for Kimi
- [#4467](https://github.com/ROCm/aiter/pull/4467) Bound packed FP4 output stores in module_rmsnorm_quant
- [#4452](https://github.com/ROCm/aiter/pull/4452) Refresh gfx950 MLA HSACO for large page_id KV addressing
</details>

<details>
<summary>Performance (7)</summary>

- [#4314](https://github.com/ROCm/aiter/pull/4314) Tune DeepSeek V4 fused MoE for C1/C2/C32/C64 decode
- [#4414](https://github.com/ROCm/aiter/pull/4414) Tune MHA config and small-head pipeline pathology
- [#4515](https://github.com/ROCm/aiter/pull/4515) (opened) Reduce short-context FP4 prefill tile size in FlyDSL
- [#4598](https://github.com/ROCm/aiter/pull/4598) (opened) Add gdn_prepare fused intra-chunk GDN prefill prepare kernel
- [#4571](https://github.com/ROCm/aiter/pull/4571) (opened) Optimize group MoE small ops for gfx1250 FlyDSL
- [#4556](https://github.com/ROCm/aiter/pull/4556) (opened) Add opt-in atomic stage2 override for FlyDSL MoE
- [#4558](https://github.com/ROCm/aiter/pull/4558) (opened) Tune a16 kernel dispatch for GLM-5 decode on gfx942 FMoE
</details>

<details>
<summary>Model support (4)</summary>

- [#4570](https://github.com/ROCm/aiter/pull/4570) Add tuned bf16 GEMM config for Qwen3-8B on gfx950
- [#4513](https://github.com/ROCm/aiter/pull/4513) Add MXMoE kernels for Qwen3.5-397B TP2 decode
- [#4552](https://github.com/ROCm/aiter/pull/4552) Route missing Kimi-K3 fused BF16 GEMM to Triton on gfx1250
- [#4547](https://github.com/ROCm/aiter/pull/4547) Cherry-pick fix for custom all-reduce in Qwen3.5_dev
</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#4445](https://github.com/ROCm/aiter/pull/4445) Re-enable FP4 KV cache for UA and MLA on gfx1250
- [#4525](https://github.com/ROCm/aiter/pull/4525) (opened) Add gfx90a to GFX_CU_NUM_MAP
- [#4535](https://github.com/ROCm/aiter/pull/4535) (opened) Add gfx1201 RDNA4 architecture to allowed_archs in aiter_meta
- [#4512](https://github.com/ROCm/aiter/pull/4512) (opened) Resolve gfx1100 targets across JIT paths
- [#4578](https://github.com/ROCm/aiter/pull/4578) (opened) Swap gfx950 kernel to hold 64-bit memory address
</details>

<details>
<summary>Refactors (6)</summary>

- [#4569](https://github.com/ROCm/aiter/pull/4569) Refactor and detorch module_sample
- [#4606](https://github.com/ROCm/aiter/pull/4606) (opened) Refactor tiled-copy and cleanup swiglu/silu_fq/qk_norm_rope/fp8_mqa
- [#4599](https://github.com/ROCm/aiter/pull/4599) (opened) Refactor TDM in HIP backend
- [#4590](https://github.com/ROCm/aiter/pull/4590) (opened) Refactor and detorch module_aiter_unary
- [#4594](https://github.com/ROCm/aiter/pull/4594) (opened) Clean rocprim/hipcub in HIP kernels
- [#4557](https://github.com/ROCm/aiter/pull/4557) (opened) Migrate GEMM kernels to the stable DSL API for gfx1250
</details>

<details>
<summary>Bugfixes (15)</summary>

- [#4540](https://github.com/ROCm/aiter/pull/4540) (opened) Fix GDR reductions for FlyDSL 0.2.4
- [#4537](https://github.com/ROCm/aiter/pull/4537) (opened) Fix three Gluon GEMM correctness bugs and tune Kimi-K3 a16w16 shapes
- [#4587](https://github.com/ROCm/aiter/pull/4587) (opened) Keep get_meta_param's split-offset table alive for captured CUDA graphs
- [#4539](https://github.com/ROCm/aiter/pull/4539) (opened) Cache paged_attention_v1 launch plan to fix batch=1 decode latency
- [#4580](https://github.com/ROCm/aiter/pull/4580) (opened) Guard all OutLogits stores in pa_mqa_logits
- [#4565](https://github.com/ROCm/aiter/pull/4565) (opened) Support mask0 for MI350 MLA ps mode BF16 case
- [#4530](https://github.com/ROCm/aiter/pull/4530) (opened) Fix memory access fault in Triton MOE routing update
- [#4605](https://github.com/ROCm/aiter/pull/4605) (opened) Fix reduce_scatter pynccl path
- [#4560](https://github.com/ROCm/aiter/pull/4560) (opened) Avoid CustomAllreduce when expandable_segments is True
- [#4529](https://github.com/ROCm/aiter/pull/4529) Fix LDS allocation for B-to-LDS FlyDSL Split-K HGEMM
- [#4588](https://github.com/ROCm/aiter/pull/4588) Fix shuffle_scale_moe crashes with UnboundLocalError on gfx942
- [#4474](https://github.com/ROCm/aiter/pull/4474) Fix int32 KV-offset overflow in _mla_gluon >2GB path
- [#4567](https://github.com/ROCm/aiter/pull/4567) Add assert for layernorm weight/input dtype mismatch
- [#4566](https://github.com/ROCm/aiter/pull/4566) (opened) Isolate AITER extensions from HIP interposers
- [#4593](https://github.com/ROCm/aiter/pull/4593) (opened) Drop redundant aiter:: prefix from define schema for torch 2.13
</details>

<details>
<summary>CI & build (9)</summary>

- [#4003](https://github.com/ROCm/aiter/pull/4003) Add Flash attention sliding window tests
- [#4518](https://github.com/ROCm/aiter/pull/4518) Auto-update split test FILE_TIMES
- [#4431](https://github.com/ROCm/aiter/pull/4431) Bump flydsl dependency to 0.3.0
- [#4520](https://github.com/ROCm/aiter/pull/4520) Switch MI300X jobs to OCI runners
- [#4589](https://github.com/ROCm/aiter/pull/4589) Temporarily pin rocm/pytorch:latest image digest
- [#4516](https://github.com/ROCm/aiter/pull/4516) Fix SGLang downstream setup and enable DSV3.2 accuracy
- [#4600](https://github.com/ROCm/aiter/pull/4600) Move multi-GPU tests to DO MI350X runner
- [#4553](https://github.com/ROCm/aiter/pull/4553) Fix mxmoe CI bug during flydsl bump
- [#4559](https://github.com/ROCm/aiter/pull/4559) (opened) Align Ruff version with CI
</details>

<details>
<summary>Docs (1)</summary>

- [#4561](https://github.com/ROCm/aiter/pull/4561) (opened) Fix ISA kernel optimization guide and example scripts
</details>

<details>
<summary>Other (6)</summary>

- [#4465](https://github.com/ROCm/aiter/pull/4465) Optimize ctypes marshalling
- [#4575](https://github.com/ROCm/aiter/pull/4575) Replace KV buffer loads with 64-bit global loads in DSv4 prefill
- [#4508](https://github.com/ROCm/aiter/pull/4508) Fix Python 3.14 compatibility issue with aggregate
- [#4478](https://github.com/ROCm/aiter/pull/4478) Forward transpose_scale through fused AR+RMSNorm per-group quant
- [#4591](https://github.com/ROCm/aiter/pull/4591) Disable amdgpu-early-inline-all for DSv4 sparse prefill
- [#4544](https://github.com/ROCm/aiter/pull/4544) (opened) Default timeout to 100s so dead workers get reaped
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 493c6e046055d6dbeef29786cb616fafc4cf382afdecfa95ef984ec69234103e -->
