# AITER: PR digest (2026-06-17 to 2026-06-21)

_39 merged, 36 newly opened - source ROCm/AITER, generated 2026-06-21T22:17:28Z_

## TL;DR
*   **Model Focus**: DeepSeek (v3/v4) dominated tuning and kernel work, alongside significant attention for Kimi and MiniMax-M3.
*   **Hardware & Arch**: Massive push for next-gen AMD hardware, with extensive kernel porting and tuning for gfx1250 (MI450, wave32) and gfx950 (MI350X).
*   **MoE & Quantization**: Major strides in low-precision MoE, including merged FlyDSL a4w4 MoE support and in-progress MXFP8 prefill MoE JIT kernels for gfx950.
*   **Attention & MLA**: Significant MLA (Multi-head Latent Attention) upgrades, including v3 for gfx1250 and BF16 context parallel round-robin support for MI350.

## Most important PRs
*   [#3804](https://github.com/ROCm/aiter/pull/3804): **Ports FlyDSL `qk_norm_rope_quant` and `compress_attn` to gfx1250 (wave32).** This massive 5k-line addition brings critical fused attention and quantization kernels to next-gen AMD hardware.
*   [#3788](https://github.com/ROCm/aiter/pull/3788): **Integrates FlyDSL a4w4 MoE onto the `randomflow_pr` branch.** Enables highly optimized low-precision MoE execution for Kimi, coexisting with the existing HIP backend.
*   [#3800](https://github.com/ROCm/aiter/pull/3800): **Adds JIT `grouped_gemm_mxfp8` for MXFP8 prefill MoE on gfx950.** A major newly-opened 7k-line PR that significantly accelerates FP8 MoE throughput for MI350X architectures.
*   [#3750](https://github.com/ROCm/aiter/pull/3750): **Implements BF16 context parallel round-robin support for MLA on MI350.** Enhances distributed Multi-head Latent Attention performance by optimizing cross-device token routing.
*   [#3791](https://github.com/ROCm/aiter/pull/3791): **Fuses custom AllReduce with MHC post-processing for Tensor Parallel paths.** Reduces communication overhead and kernel launch latency for distributed inference.

## More changes by area

<details>
<summary>Performance & Tuning (18)</summary>

*   [#3808](https://github.com/ROCm/aiter/pull/3808) Add Triton DSV4 BMM config for gfx950
*   [#3636](https://github.com/ROCm/aiter/pull/3636) Add tuned DSv4 a8w8_blockscale GEMM for gfx950 (MI350X)
*   [#3780](https://github.com/ROCm/aiter/pull/3780) Add tuned BF16 GEMM configs for gfx950
*   [#3603](https://github.com/ROCm/aiter/pull/3603) Use fused `silu_and_mul` for CK-Tile interleaved post-activation
*   [#3755](https://github.com/ROCm/aiter/pull/3755) Add tuning config for MiniMax-M3 MoE
*   [#3784](https://github.com/ROCm/aiter/pull/3784) Add Triton DSV4 BMM config for gfx1250
*   [#3529](https://github.com/ROCm/aiter/pull/3529) Add GLM-4.7-FP8 FMOE configs for EP=4 and fused shared expert
*   [#3768](https://github.com/ROCm/aiter/pull/3768) Support HIP MHC on wave32 platform
*   [#3458](https://github.com/ROCm/aiter/pull/3458) Raise fused AllReduce 1-stage limit to cover conc64
*   [#3825](https://github.com/ROCm/aiter/pull/3825) (Opened) Support `k_wave` for FP4 gemm1 and tune for DSv3/v4
*   [#3774](https://github.com/ROCm/aiter/pull/3774) (Opened) Optimize conc1 MoE for gfx1250
*   [#3814](https://github.com/ROCm/aiter/pull/3814) (Opened) Add tuned DSV4-Flash FP8 GEMM configs
*   [#3822](https://github.com/ROCm/aiter/pull/3822) (Opened) Tune BF16 BMM further
*   [#3790](https://github.com/ROCm/aiter/pull/3790) (Opened) Add DSV4 config for BF16 GEMM on gfx1250
*   [#3817](https://github.com/ROCm/aiter/pull/3817) (Opened) Optimize fused AllReduce + RMSNorm
*   [#3798](https://github.com/ROCm/aiter/pull/3798) (Opened) Tune DSv4 config for `gemm_a8w8_blockscale` on MI450
*   [#3809](https://github.com/ROCm/aiter/pull/3809) (Opened) Add tuned FlyDSL fused-MoE config for Qwen3.5-397B MXFP4
*   [#3781](https://github.com/ROCm/aiter/pull/3781) (Opened) Use vectorized LDS loads for `mhc_pre_gemm_sqrsum` on gfx942
</details>

<details>
<summary>Kernels & attention (18)</summary>

*   [#3754](https://github.com/ROCm/aiter/pull/3754) Add fused attention preprocessing op for MiniMax-M3
*   [#3759](https://github.com/ROCm/aiter/pull/3759) Implement K-split `compress_attn` for latency-bound CSA decode
*   [#3500](https://github.com/ROCm/aiter/pull/3500) Implement MLA v3 for gfx1250
*   [#3794](https://github.com/ROCm/aiter/pull/3794) Support Paged Attention on MI450
*   [#3821](https://github.com/ROCm/aiter/pull/3821) Drop per-call memset on multi-block radix top-k via persistent workspace
*   [#3792](https://github.com/ROCm/aiter/pull/3792) Add `gemma_norm` for AllReduce + norm fusion
*   [#3776](https://github.com/ROCm/aiter/pull/3776) Fuse decode SWA cache-write into `qk_norm_rope_quant`
*   [#3787](https://github.com/ROCm/aiter/pull/3787) (Opened) Port `compress_attn` kernels to gfx1250
*   [#3803](https://github.com/ROCm/aiter/pull/3803) (Opened) Add multi-backend prefill `causal_conv1d` kernels for GDN
*   [#3823](https://github.com/ROCm/aiter/pull/3823) (Opened) Unify scale and weight shuffling into `shuffle.py`
*   [#3795](https://github.com/ROCm/aiter/pull/3795) (Opened) Support shuffling KV cache layout in `idxsknorm_shuffle_layout`
*   [#3785](https://github.com/ROCm/aiter/pull/3785) (Opened) Add FP32 RMSNorm output for fused QK group quant
*   [#3801](https://github.com/ROCm/aiter/pull/3801) (Opened) Extract C++ kernel code to Jinja template files
*   [#3777](https://github.com/ROCm/aiter/pull/3777) (Opened) Refactor `module_fused_split_gdr_update`
*   [#3769](https://github.com/ROCm/aiter/pull/3769) (Opened) Parallelize standalone FlyDSL AOT compile drivers
*   [#3813](https://github.com/ROCm/aiter/pull/3813) (Opened) Simplify `ck_gemm_a8w8_blockscale` specialization construction
*   [#3826](https://github.com/ROCm/aiter/pull/3826) (Opened) Patch MLA kernel for gfx1250
*   [#3816](https://github.com/ROCm/aiter/pull/3816) (Opened) Refactor a8w8 blockscale GEMM and add gfx1250 preshuffle
</details>

<details>
<summary>MoE & quantization (9)</summary>

*   [#3756](https://github.com/ROCm/aiter/pull/3756) Support n32k4 layout for MoE GEMM
*   [#3811](https://github.com/ROCm/aiter/pull/3811) Fix MXFP8 support in mixed MX 2-stage pipeline
*   [#3820](https://github.com/ROCm/aiter/pull/3820) Fuse FP8 quantization into `rope_rotate_activation`
*   [#3810](https://github.com/ROCm/aiter/pull/3810) (Opened) Port FlyDSL block MoE fusion
*   [#3783](https://github.com/ROCm/aiter/pull/3783) (Opened) Add decode small-M MX-FP8 GEMM and GroupGEMM kernels for gfx950
*   [#3827](https://github.com/ROCm/aiter/pull/3827) (Opened) Integrate HIP Sort/Quant into MoE Pipeline
*   [#3767](https://github.com/ROCm/aiter/pull/3767) (Opened) Limit MoE group GEMM SwiGLU for DSv4 on gfx1250
*   [#3815](https://github.com/ROCm/aiter/pull/3815) (Opened) Add FP8 unified-KV prefix for `pa_sparse_prefill_opus` on gfx950
*   [#3828](https://github.com/ROCm/aiter/pull/3828) (Opened) Bring FlyDSL MXFP4 a4w4 MoE gemm1/gemm2 to parity with HIP
</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

*   [#3765](https://github.com/ROCm/aiter/pull/3765) Unlock 80-tokens limit for 1-stage AllReduce fusion
*   [#3728](https://github.com/ROCm/aiter/pull/3728) Enable Prefill Context Parallel (PCP)
*   [#3802](https://github.com/ROCm/aiter/pull/3802) (Opened) Implement AllReduce PoC for gfx1250
</details>

<details>
<summary>Bugfixes (13)</summary>

*   [#3677](https://github.com/ROCm/aiter/pull/3677) Fix fused MoE padded-token NaNs by zeroing quant output for zero routing
*   [#3796](https://github.com/ROCm/aiter/pull/3796) Fix async `waitcnt` for HIP MHC and tune gfx12xx config
*   [#3760](https://github.com/ROCm/aiter/pull/3760) Fix hardcoded CU count in MLA/indexer Triton kernels
*   [#3793](https://github.com/ROCm/aiter/pull/3793) Load fused-SWA `batch_id_per_token` as int32 instead of int64
*   [#3741](https://github.com/ROCm/aiter/pull/3741) Fix crash for DeepSeek v4 MoE unsupported scales/output dtype
*   [#3819](https://github.com/ROCm/aiter/pull/3819) Fix Triton wheel default ROCm fallback in CI
*   [#3782](https://github.com/ROCm/aiter/pull/3782) Launch MTP ASM with block table batch for Paged Attention
*   [#3764](https://github.com/ROCm/aiter/pull/3764) (Opened) Fix FlyDSL type-closure incompatibility in mixed MoE kernels
*   [#3818](https://github.com/ROCm/aiter/pull/3818) (Opened) Fix FlyDSL MoE 4GiB limit issue
*   [#3773](https://github.com/ROCm/aiter/pull/3773) (Opened) Fix top-k decode dispatch sequence length
*   [#3805](https://github.com/ROCm/aiter/pull/3805) (Opened) Deduplicate fused/non-fused stage 1 separately in FMoE tuning
*   [#3766](https://github.com/ROCm/aiter/pull/3766) (Opened) Fix `batched_gemm_a16wfp4` split-K garbage output for small M
*   [#3771](https://github.com/ROCm/aiter/pull/3771) (Opened) Disable EP topk-1 strip
</details>

<details>
<summary>CI, Build & Docs (9)</summary>

*   [#3748](https://github.com/ROCm/aiter/pull/3748) Optimize Paged Attention build packaging
*   [#3786](https://github.com/ROCm/aiter/pull/3786) Update FlyDSL README documentation
*   [#3753](https://github.com/ROCm/aiter/pull/3753) Bump FlyDSL dependency to 0.2.1
*   [#3789](https://github.com/ROCm/aiter/pull/3789) Pin `triton==3.7.0` and `triton-kernels==1.0.0` for wheels
*   [#3779](https://github.com/ROCm/aiter/pull/3779) Limit downstream test parallelism in CI
*   [#3797](https://github.com/ROCm/aiter/pull/3797) Run SGLang performance tests only on nightly CI
*   [#3799](https://github.com/ROCm/aiter/pull/3799) Cap Triton shard runtime in CI
*   [#3775](https://github.com/ROCm/aiter/pull/3775) (Opened) Detect rocm-core version via rpm on RPM-based systems
*   [#3763](https://github.com/ROCm/aiter/pull/3763) (Opened) Update FlyDSL to 0.2.2.dev658
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
