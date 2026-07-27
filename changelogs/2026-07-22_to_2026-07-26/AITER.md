# AITER: PR digest (2026-07-22 to 2026-07-26)

_21 merged, 39 newly opened - source ROCm/AITER, generated 2026-07-26T22:03:04Z_

## TL;DR
- **DeepSeek-V4** dominated attention, with major performance wins in FP8/FP4 MoE tuning, MLA decode, and blockscale GEMMs. Kimi, GLM, and Qwen also saw targeted quantization work.
- **Hardware optimization** focused heavily on next-gen AMD architectures, delivering tuned kernels for **gfx950** (MI350X) and **gfx1250**, alongside **gfx942** (MI325X) blockscale GEMM configs.
- **FlyDSL integration** is a major new direction, with massive PRs landing and opening to migrate GEMMs, Paged Attention, and HSTU kernels to the new layout-based API.
- **Quantization and MoE** saw significant needle-moving work, particularly around **MXFP4** support, A8W8/A8W4 blockscale GEMMs, and FMoE stage 2 tuning.

## Most important PRs
- **[#4338](https://github.com/ROCm/aiter/pull/4338)** introduces FlyDSL kernel authoring and trace-analysis skills, establishing a new backend framework for layout-based kernel generation to simplify future maintenance.
- **[#4321](https://github.com/ROCm/aiter/pull/4321)** optimizes the Opus Flash Multi-Head Attention (FMHA) d128 kernel for gfx950, significantly improving attention throughput on next-gen MI350X hardware.
- **[#4198](https://github.com/ROCm/aiter/pull/4198)** tunes A8W4 Tensor Parallel (TP4) MoE configurations for gfx1250, delivering critical performance wins for low-bitwidth quantized MoE inference on RDNA/CDNA next-gen parts.
- **[#4374](https://github.com/ROCm/aiter/pull/4374)** (in-progress) refactors gfx1250 GEMMs to use the new FlyDSL layout-based API, a massive 6000-line migration standardizing DeepSeek quantization and GEMM operations.
- **[#4382](https://github.com/ROCm/aiter/pull/4382)** (in-progress) implements a Paged Sparse Attention Gluon kernel for DeepSeek-V4 on gfx950, targeting memory-efficient, high-throughput attention for sparse models using Triton.

## More changes by area

<details>
<summary>Performance (12)</summary>

- [#3951](https://github.com/ROCm/aiter/pull/3951) tunes DeepSeek-V3.2 gfx942 A8W8 blockscale GEMM and FMoE configs for TP8
- [#4347](https://github.com/ROCm/aiter/pull/4347) tunes Triton blockscale preshuffle configs for DeepSeek-V4-Flash-FP8 decode on gfx942
- [#4352](https://github.com/ROCm/aiter/pull/4352) tunes bf16 GEMM shapes to non-hipblaslt kernels for GPT-OSS
- [#4317](https://github.com/ROCm/aiter/pull/4317) tunes A8W8 GEMM for Qwen3.5 MXFP4-AttnFP8
- [#4298](https://github.com/ROCm/aiter/pull/4298) hoists q/kv data load in fine-grained qk-norm-rope kernel for DeepSeek-V4
- [#4331](https://github.com/ROCm/aiter/pull/4331) tunes DeepSeek-V4 FP8/FP4 FMoE stage2 per token and tightens tuner errRatio
- [#4324](https://github.com/ROCm/aiter/pull/4324) tunes Opus MoE A8W4 stage2 for DeepSeek-V4
- [#4330](https://github.com/ROCm/aiter/pull/4330) autotunes Gluon batched GEMM bf16 for DeepSeek-V4 shapes on gfx1250
- [#4334](https://github.com/ROCm/aiter/pull/4334) runtime-autotunes the gfx942 indexer tile for fp8_mqa_logits
- [#4344](https://github.com/ROCm/aiter/pull/4344) retunes fMoE kernels with FLAT support for GLM-5.2-MXFP4
- [#4361](https://github.com/ROCm/aiter/pull/4361) skips redundant TokenStart/TileStart stores in stage1 for expt_data
- [#4359](https://github.com/ROCm/aiter/pull/4359) swaps cache config for default cases of gfx1250-GEMM-A8W8_BLOCKSCALE

</details>

<details>
<summary>Kernels & attention (14)</summary>

- [#4299](https://github.com/ROCm/aiter/pull/4299) supports causal_conv1d_fwd_split_qkv with channel-last layout in HIP
- [#4345](https://github.com/ROCm/aiter/pull/4345) forces occupancy-only split selection for MLA v4 nm
- [#3732](https://github.com/ROCm/aiter/pull/3732) adds HD256 FMHA FP8 for GFX950
- [#4353](https://github.com/ROCm/aiter/pull/4353) adds mfma16_hip GDR K5 prefill chunk_gdn_fwd_h for MI308
- [#4332](https://github.com/ROCm/aiter/pull/4332) adds FlyDSL paged-attention Tile kernel
- [#4354](https://github.com/ROCm/aiter/pull/4354) adds FlyDSL HSTU Forward kernel
- [#4371](https://github.com/ROCm/aiter/pull/4371) implements FlyDSL version of fused_qk_norm_mrope_3d_cache_pts_quant_shuffle
- [#4348](https://github.com/ROCm/aiter/pull/4348) adds Aiterker 112 asm ptl1 for gfx942
- [#4335](https://github.com/ROCm/aiter/pull/4335) updates asm f4gemm and adds fp8 out support for gfx1250
- [#4366](https://github.com/ROCm/aiter/pull/4366) supports fp32 chunk states in GDN prefill
- [#4357](https://github.com/ROCm/aiter/pull/4357) implements MHA global load for gfx950
- [#4376](https://github.com/ROCm/aiter/pull/4376) adds deterministic tie-break-by-token-id for sparse-MLA indexer top-k
- [#4373](https://github.com/ROCm/aiter/pull/4373) adds thin sparse attention operator for CK/VSA
- [#4388](https://github.com/ROCm/aiter/pull/4388) specializes batch prefill for paged KV layout

</details>

<details>
<summary>MoE & quantization (3)</summary>

- [#4383](https://github.com/ROCm/aiter/pull/4383) adds Gluon support for MXFP4 quant kernel in gfx950 and gfx1250
- [#4370](https://github.com/ROCm/aiter/pull/4370) adds 128x128 block-scales fp8 8wave MoE/GEMM kernels from pyhip for MI355
- [#4362](https://github.com/ROCm/aiter/pull/4362) adds unit-scale FP8 KV cache support to fused_qknorm_idxrqknorm

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#4355](https://github.com/ROCm/aiter/pull/4355) ports silotiger 699 to gfx950
- [#4340](https://github.com/ROCm/aiter/pull/4340) adds native Windows RDNA HIP and CK support
- [#4387](https://github.com/ROCm/aiter/pull/4387) limits attention kernel dispatch to supported GPUs

</details>

<details>
<summary>API & serving (2)</summary>

- [#4270](https://github.com/ROCm/aiter/pull/4270) enables E2E SGLang inference on gfx1250
- [#4378](https://github.com/ROCm/aiter/pull/4378) adds deterministic single-split decode option for reproducible MLA serving

</details>

<details>
<summary>Refactors (4)</summary>

- [#4349](https://github.com/ROCm/aiter/pull/4349) refactors FlyDSL mxfp4_gemm1 memory ops to fx.copy
- [#3875](https://github.com/ROCm/aiter/pull/3875) refactors module_groupnorm
- [#4368](https://github.com/ROCm/aiter/pull/4368) refactors module_moe_asm and removes torch dependency
- [#4379](https://github.com/ROCm/aiter/pull/4379) moves all tuning configs to centralized structure

</details>

<details>
<summary>Bugfixes (11)</summary>

- [#4235](https://github.com/ROCm/aiter/pull/4235) fixes FIPS crash in hash_signature
- [#4337](https://github.com/ROCm/aiter/pull/4337) enhances bf16 asm mha kernel to avoid corner issue
- [#4341](https://github.com/ROCm/aiter/pull/4341) refreshes qh16 fp8 persistent decode HSACO for large page_id in MLA
- [#4375](https://github.com/ROCm/aiter/pull/4375) fixes FlyDSL MoE sorting graph capture break with DP attn + EP
- [#4365](https://github.com/ROCm/aiter/pull/4365) gates gfx942 native qh64 fp8 decode to page_size=64 to fix GPU fault
- [#4342](https://github.com/ROCm/aiter/pull/4342) fixes fused_qk_rope_concat_and_cache_mla for DCP
- [#4385](https://github.com/ROCm/aiter/pull/4385) avoids RDNA4 unified attention LDS overflow in Triton
- [#4389](https://github.com/ROCm/aiter/pull/4389) fixes AITER JIT builds on gfx90a
- [#4343](https://github.com/ROCm/aiter/pull/4343) fixes >4GB a4w4 weight buffer-offset overflow for Kimi k2.6
- [#4346](https://github.com/ROCm/aiter/pull/4346) adds missing end_sync barrier in fused allreduce+rmsnorm kernel
- [#4351](https://github.com/ROCm/aiter/pull/4351) refreshes gfx950 MLA HSACO batch for large page_id

</details>

<details>
<summary>CI & build (4)</summary>

- [#4372](https://github.com/ROCm/aiter/pull/4372) moves ATOM 4GPU jobs to do-mi350x-4
- [#4336](https://github.com/ROCm/aiter/pull/4336) pins GitHub Actions to commit SHAs
- [#4386](https://github.com/ROCm/aiter/pull/4386) updates FlyDSL version for CI
- [#4384](https://github.com/ROCm/aiter/pull/4384) repins CK to fix build/test errors

</details>

<details>
<summary>Tests (1)</summary>

- [#4377](https://github.com/ROCm/aiter/pull/4377) adds benchmark script for MXFP4 quant kernel

</details>

<details>
<summary>Docs (1)</summary>

- [#4303](https://github.com/ROCm/aiter/pull/4303) adds RDNA support in README

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 5dd830815be54777907798db6e815917b81ef994ecec311acbb370160b0d4b21 -->
