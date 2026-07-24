# AITER: PR digest (2026-07-19 to 2026-07-23)

_36 merged, 36 newly opened - source ROCm/AITER, generated 2026-07-23T11:09:26Z_

## TL;DR
- **Model Focus**: DeepSeek (V3.2/V4) led model-specific work, heavily focused on FP8/FP4 fused MoE and A8W8 blockscale GEMM tuning. GLM-5.2, Kimi (K2.5/K2.6), and Qwen3.5 also received targeted MXFP4 and FP8 quantization optimizations.
- **Hardware & Arch**: Next-gen hardware enablement accelerated, with massive kernel drops for **gfx950** (OPUS FMHA, FP8 MX-scale BMMs) and **RDNA4 / gfx1250** (FlyDSL smem migration, native Windows HIP/CK support).
- **FlyDSL Expansion**: FlyDSL is rapidly maturing, with merged shared memory migrations and newly opened PRs adding paged-attention Tile kernels, MI308 prefill support, and trace-analysis tooling.
- **MLA v4 Enhancements**: Multi-Head Latent Attention (MLA) v4 saw critical path optimizations, including zero-copy final outputs, ABI simplifications, and direct Python launching for gfx1250 to bypass C++ host overhead.

## Most important PRs
- **[#4320](https://github.com/ROCm/aiter/pull/4320)** (Opened): Adds OPUS FP8 MX-scale flatmm split-K batched matrix multiply kernels for gfx950. This massive addition significantly expands FP8 quantization support and performance on next-generation AMD hardware.
- **[#4250](https://github.com/ROCm/aiter/pull/4250)** (Merged): Adapts the Gated Delta Rule (GDN) prefill kernel. This introduces substantial backend and Triton integration changes to optimize prefill performance for linear attention models.
- **[#4280](https://github.com/ROCm/aiter/pull/4280)** (Merged): Migrates shared memory management in FlyDSL for gfx1201 and gfx1250. This foundational change optimizes attention, MoE, and quantization kernels specifically for RDNA4 architectures.
- **[#4340](https://github.com/ROCm/aiter/pull/4340)** (Opened): Introduces native Windows support for RDNA architectures using HIP and Composable Kernel (CK). This enables local development, testing, and inference directly on Windows machines.
- **[#4205](https://github.com/ROCm/aiter/pull/4205)** (Merged): Implements a new OPUS-based BF16 fused multi-head attention (FMHA) kernel for d192x128 shapes on gfx950. This targets specific attention latency bottlenecks for models using non-standard head dimensions.

## More changes by area

<details>
<summary>Performance & tuning (21)</summary>

- [#4263](https://github.com/ROCm/aiter/pull/4263) (Merged) Reduce quad inline asm and improve BF16 split-K tuning for OPUS on gfx942
- [#4321](https://github.com/ROCm/aiter/pull/4321) (Merged) Optimize OPUS FMHA d128 kernel for gfx950
- [#3951](https://github.com/ROCm/aiter/pull/3951) (Merged) Tune A8W8 blockscale GEMM and FMoE configs (TP8) for DeepSeek V3.2 on MI325X
- [#4326](https://github.com/ROCm/aiter/pull/4326) (Merged) Add A8W8 blockscale bpreshuffle configs for DeepSeek V4 on gfx950
- [#4270](https://github.com/ROCm/aiter/pull/4270) (Merged) Enable end-to-end SGLang inference and tuning on gfx1250
- [#3917](https://github.com/ROCm/aiter/pull/3917) (Merged) Add INT8 W8A8 GEMM config, fused-MoE forward, and RDNA routing for gfx1151
- [#4309](https://github.com/ROCm/aiter/pull/4309) (Merged) Add batched GEMM A16W16 Triton tuning config for N=1024 K=4096 on gfx942
- [#4243](https://github.com/ROCm/aiter/pull/4243) (Merged) Add GLM-5.2 tuned A8W8 blockscale bpreshuffle configs for gfx950
- [#4298](https://github.com/ROCm/aiter/pull/4298) (Merged) Hoist Q/KV data load in fine-grained QK-norm-RoPE kernel for DeepSeek V4
- [#4331](https://github.com/ROCm/aiter/pull/4331) (Merged) Tighten tuner errRatio and set best-correct stage 2 per token for DeepSeek V4 FP8/FP4 FMoE
- [#3915](https://github.com/ROCm/aiter/pull/3915) (Merged) Use 8 warps for gfx1151 3D decode in unified attention
- [#4324](https://github.com/ROCm/aiter/pull/4324) (Merged) Tune OPUS MoE A8W4 stage 2 for DeepSeek V4 FP8/FP4 FMoE
- [#4322](https://github.com/ROCm/aiter/pull/4322) (Opened) Tune A8W8 blockscale GEMM for RDNA4 (gfx1201)
- [#4330](https://github.com/ROCm/aiter/pull/4330) (Opened) Autotune Gluon batched GEMM BF16 for DeepSeek V4 shapes on gfx1250
- [#4347](https://github.com/ROCm/aiter/pull/4347) (Opened) Add Triton blockscale preshuffle tuned configs for DeepSeek V4 Flash FP8 decode on gfx942
- [#4352](https://github.com/ROCm/aiter/pull/4352) (Opened) Tune BF16 GEMM shapes to non-hipblaslt kernels for GPT-OSS
- [#4334](https://github.com/ROCm/aiter/pull/4334) (Opened) Runtime-autotune the gfx942 indexer tile for FP8 MQA logits
- [#4287](https://github.com/ROCm/aiter/pull/4287) (Opened) Add tuned MoE Triton configurations
- [#4344](https://github.com/ROCm/aiter/pull/4344) (Opened) Retune FMoE kernels with FLAT support for GLM-5.2 MXFP4
- [#4317](https://github.com/ROCm/aiter/pull/4317) (Opened) Tune A8W8 GEMM for Qwen3.5 MXFP4-AttnFP8 model
- [#4314](https://github.com/ROCm/aiter/pull/4314) (Opened) Tune DeepSeek V4 fused MoE for C1/C2/C32/C64 decode in FlyDSL

</details>

<details>
<summary>Kernels & attention (10)</summary>

- [#4353](https://github.com/ROCm/aiter/pull/4353) (Opened) Add mfma16 HIP-only K5 prefill with unified HIP BV select for MI308 in FlyDSL
- [#4332](https://github.com/ROCm/aiter/pull/4332) (Opened) Add paged-attention Tile kernel to FlyDSL
- [#4348](https://github.com/ROCm/aiter/pull/4348) (Opened) Add Aiterker 112 assembly PTL1 kernels for gfx942
- [#4335](https://github.com/ROCm/aiter/pull/4335) (Opened) Update assembly F4GEMM, add FP8 out support, and enhance tests for gfx1250
- [#4299](https://github.com/ROCm/aiter/pull/4299) (Merged) Support causal_conv1d_fwd_split_qkv with channel-last layout in HIP backend
- [#4218](https://github.com/ROCm/aiter/pull/4218) (Merged) Add support for pool indexing of hidden states tensor in Gated Delta Rule prefill kernel
- [#3732](https://github.com/ROCm/aiter/pull/3732) (Merged) Add HD256 FMHA FP8 kernel for gfx950
- [#4239](https://github.com/ROCm/aiter/pull/4239) (Merged) Implement Chefang MHA global kernel for gfx950
- [#4337](https://github.com/ROCm/aiter/pull/4337) (Opened) Enhance BF16 assembly MHA kernel to avoid corner issues on gfx1250
- [#4312](https://github.com/ROCm/aiter/pull/4312) (Opened) Enable stride-aware indexing on top of strided blocks for fused QK-norm-RoPE cache kernels

</details>

<details>
<summary>Multi-Head Latent Attention (MLA) (9)</summary>

- [#4311](https://github.com/ROCm/aiter/pull/4311) (Merged) Enable zero-copy final output for out_16_nosplit=1 in MLA v4 nm
- [#4308](https://github.com/ROCm/aiter/pull/4308) (Merged) Fix MLA non-persistent mode kernel returning LSE error on gfx950
- [#4217](https://github.com/ROCm/aiter/pull/4217) (Merged) Update MLA v4 kernel for gfx1250
- [#4310](https://github.com/ROCm/aiter/pull/4310) (Merged) Remove MLA v4 LTL for gfx1250
- [#4327](https://github.com/ROCm/aiter/pull/4327) (Opened) Drop kv_last_page_lens from ABI and add self-contained BF16 Triton cross-check for MLA v4 nm
- [#4295](https://github.com/ROCm/aiter/pull/4295) (Opened) Launch v4 NM MLA decode HSACO directly from Python for gfx1250
- [#4341](https://github.com/ROCm/aiter/pull/4341) (Opened) Refresh qh16 FP8 persistent decode HSACO for large page_id on gfx950
- [#4345](https://github.com/ROCm/aiter/pull/4345) (Opened) Force occupancy-only split selection (ignoring total_kv) for MLA v4 nm
- [#4351](https://github.com/ROCm/aiter/pull/4351) (Opened) Refresh gfx950 MLA HSACO batch for large page_id

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#4247](https://github.com/ROCm/aiter/pull/4247) (Merged) Fix NaN/Inf inputs in Top-K gating for MoE
- [#4349](https://github.com/ROCm/aiter/pull/4349) (Opened) Migrate MXFP4 GEMM1 memory operations to fx.copy in FlyDSL
- [#4300](https://github.com/ROCm/aiter/pull/4300) (Opened) Align per_1x32 FP4/FP8 dispatch with test_moe_2stage in FMoE run config
- [#4328](https://github.com/ROCm/aiter/pull/4328) (Opened) Add benchmark script for MXFP4 quantization kernel
- [#4292](https://github.com/ROCm/aiter/pull/4292) (Opened) Fix Triton bug to quantize zero SageAttention V channels without NaNs
- [#4291](https://github.com/ROCm/aiter/pull/4291) (Opened) Define zero-row and padded FP8/INT8 quantization in Triton

</details>

<details>
<summary>API, Serving & Framework (3)</summary>

- [#4338](https://github.com/ROCm/aiter/pull/4338) (Merged) Add FlyDSL kernel authoring, code-cleanup, and trace-analysis skills
- [#4306](https://github.com/ROCm/aiter/pull/4306) (Opened) Add basic HIP/CK JIT kernel support in Windows
- [#3919](https://github.com/ROCm/aiter/pull/3919) (Merged) Allow gfx1151 in cpp_itfs JIT architecture validation

</details>

<details>
<summary>Bugfixes (10)</summary>

- [#4220](https://github.com/ROCm/aiter/pull/4220) (Merged) Fix fused_qk_norm_rope_cache_quant build without Composable Kernel (CK)
- [#3805](https://github.com/ROCm/aiter/pull/3805) (Merged) Deduplicate fused and non-fused stage 1 separately in FMoE tuning
- [#4301](https://github.com/ROCm/aiter/pull/4301) (Merged) Retune stale GLM5 BF16 GEMM config for OPUS on gfx942
- [#4235](https://github.com/ROCm/aiter/pull/4235) (Merged) Fix FIPS crash in hash_signature
- [#4293](https://github.com/ROCm/aiter/pull/4293) (Opened) Correct ragged paged-MQA causal masks in Triton
- [#4342](https://github.com/ROCm/aiter/pull/4342) (Opened) Fix fused_qk_rope_concat_and_cache_mla for DCP
- [#4315](https://github.com/ROCm/aiter/pull/4315) (Opened) Handle remainder workgroups in MoE XCD swizzle for FlyDSL
- [#4307](https://github.com/ROCm/aiter/pull/4307) (Opened) Fix decode GEMM2 config correctness with sbm32 kernels for Kimi K2.5/K2.6 FP4
- [#4343](https://github.com/ROCm/aiter/pull/4343) (Opened) Fix >4GB A4W4 weight buffer-offset overflow for Kimi K2.6 in FlyDSL
- [#4346](https://github.com/ROCm/aiter/pull/4346) (Opened) Fix allreduce refill issue in distributed communication

</details>

<details>
<summary>CI, Build & Docs (8)</summary>

- [#4305](https://github.com/ROCm/aiter/pull/4305) (Merged) Default to torch<2.13 and expose torch_pin/torch_index_url on dispatch for CI releases
- [#4224](https://github.com/ROCm/aiter/pull/4224) (Merged) Repin CK to b6759456 and fix CI tests
- [#4313](https://github.com/ROCm/aiter/pull/4313) (Merged) Revert repining of CK to b6759456
- [#4257](https://github.com/ROCm/aiter/pull/4257) (Merged) Track ATOM main and pin cases to 1p1d via --case in CI
- [#4296](https://github.com/ROCm/aiter/pull/4296) (Merged) Fix tag parsing syntax issue in build packaging
- [#4303](https://github.com/ROCm/aiter/pull/4303) (Merged) Add RDNA support documentation to README
- [#4297](https://github.com/ROCm/aiter/pull/4297) (Opened) Auto-update split test FILE_TIMES in CI
- [#4336](https://github.com/ROCm/aiter/pull/4336) (Opened) Pin GitHub Actions to commit SHAs for security

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 4e9d0fd68dbde9ffede702355dced0372fb8af0e13f46afba45e492990e605b6 -->
