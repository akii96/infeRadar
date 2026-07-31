# AITER: PR digest (2026-07-26 to 2026-07-30)

_36 merged, 46 newly opened - source ROCm/AITER, generated 2026-07-30T11:07:46Z_

## TL;DR
*   **DeepSeek (V4) and Kimi (K3/K2.5)** drove the majority of performance work this cycle, with heavy investments in low-precision (FP4/MXFP4/FP8) inference and MoE optimizations.
*   **MoE and quantization** saw massive architectural shifts, including new FlyDSL SiTUv2 kernels, a8w8 blockscale GEMMs, and a large-scale "megamoe" refactor currently in flight.
*   **Attention and MLA (Multi-Head Latent Attention)** capabilities expanded significantly, adding MTP support, new MI350/gfx950 specific kernels, and critical large `page_id` fixes.
*   **Hardware focus** remains tightly coupled to AMD gfx1250 and gfx950, leveraging Triton and Gluon backends to streamline GEMM dispatch and layout-based APIs.

## Most important PRs
*   **[#4397](https://github.com/ROCm/aiter/pull/4397)** (Merged) Introduces FlyDSL SiTUv2 MoE kernels and strided grouped-topk for Kimi-K3. This delivers heavily tuned configurations and activation kernels critical for Kimi's performance on AMD hardware.
*   **[#4374](https://github.com/ROCm/aiter/pull/4374)** (Merged) Refactors gfx1250 FlyDSL GEMMs to use a layout-based API. This architectural shift streamlines blockscale quantization and MoE GEMM dispatch for DeepSeek and other models.
*   **[#4029](https://github.com/ROCm/aiter/pull/4029)** (Merged) Adds fused FP4 scatter and RMSNorm RoPE rotate FP4 KV-cache kernels for DeepSeek-V4. This is a major needle-mover for memory bandwidth and latency in DeepSeek's FP4 inference path.
*   **[#4395](https://github.com/ROCm/aiter/pull/4395)** (Opened) Proposes FlyDSL FP8 MoE kernels (decode weight-decompression and prefill) targeting MI308. This unlocks massive Qwen3.5 (35B/397B) deployments on new hardware.
*   **[#4430](https://github.com/ROCm/aiter/pull/4430)** (Opened) Implements a new MI350 MLA PS mode `ds32` opus kernel for DeepSeek. This optimizes the specific `nhead*qseqlen=128` edge case for better attention throughput.

## More changes by area

<details>
<summary>Performance & Tuning (15)</summary>

- [#4410](https://github.com/ROCm/aiter/pull/4410) Merges v2 tuning configurations for general MoE and GEMM kernels
- [#4253](https://github.com/ROCm/aiter/pull/4253) Adds DeepSeek-V4 Pro EP tuning (TP1 shape) for Triton/Gluon on gfx1250
- [#4379](https://github.com/ROCm/aiter/pull/4379) Streamlines GEMM and MoE configurations across Triton and Gluon backends
- [#4266](https://github.com/ROCm/aiter/pull/4266) Retunes MoE configurations for GLM-5.2 FP4
- [#4307](https://github.com/ROCm/aiter/pull/4307) Ports BM16 for decode gemm2 in Kimi-K2.5/K2.6 FP4, yielding +3-13% throughput
- [#4261](https://github.com/ROCm/aiter/pull/4261) Adds tuned configuration for MiMo-V2.5-Pro prefill on MI300X
- [#4443](https://github.com/ROCm/aiter/pull/4443) (Opened) Optimizes MXFP4 MoE decode with fused sorting, quantization, and compact scales
- [#4433](https://github.com/ROCm/aiter/pull/4433) (Opened) Fuses A2 quantization for DeepSeek-V4 FlyDSL EP
- [#4435](https://github.com/ROCm/aiter/pull/4435) (Opened) Adds Kimi-K3 GEMM and MoE tuned configurations
- [#4396](https://github.com/ROCm/aiter/pull/4396) (Opened) Tunes a8w8 GEMM for Qwen3.5 MXFP4-AttnFP8 models
- [#4399](https://github.com/ROCm/aiter/pull/4399) (Opened) Adds MXFP4 GEMM tuning for gfx1250 via Gluon/Triton
- [#4450](https://github.com/ROCm/aiter/pull/4450) (Opened) Optimizes 12-head Gluon MLA split scheduling
- [#4405](https://github.com/ROCm/aiter/pull/4405) (Opened) Exposes split override for MLA graph decode performance
- [#4453](https://github.com/ROCm/aiter/pull/4453) (Opened) Tunes batched a8w8 GEMM per-token-group for large M on gfx950
- [#4414](https://github.com/ROCm/aiter/pull/4414) (Opened) Tunes MHA configuration to address small-head pipeline pathology
</details>

<details>
<summary>MoE & Quantization (9)</summary>

- [#4210](https://github.com/ROCm/aiter/pull/4210) Supports a8w8 blockscale bpreshuffle GEMM on gfx1250 via FlyDSL
- [#4439](https://github.com/ROCm/aiter/pull/4439) (Opened) Introduces "megamoe" distributed MoE kernels and quantization
- [#4398](https://github.com/ROCm/aiter/pull/4398) (Opened) Implements two-stage a16w4 MoE GEMM in INTERLEAVE-gate mode for GPT-OSS
- [#4407](https://github.com/ROCm/aiter/pull/4407) (Opened) Adds SharedEP MXFP4 kernels via Triton
- [#4428](https://github.com/ROCm/aiter/pull/4428) (Opened) Adds inverse_rope_group_quant op for DeepSeek-V4 wo_a input
- [#4446](https://github.com/ROCm/aiter/pull/4446) (Opened) Adds moe_a16w4 gfx1250 Gluon kernel
- [#4400](https://github.com/ROCm/aiter/pull/4400) (Opened) Implements MXFP4 FMoE emsort for gfx950
- [#4448](https://github.com/ROCm/aiter/pull/4448) (Opened) Plumbs split-K through the a8w8 blockscale bpreshuffle GEMM
- [#4454](https://github.com/ROCm/aiter/pull/4454) (Opened) Adds 640-expert top-8 ASM kernels for gfx942/gfx950
</details>

<details>
<summary>Kernels & Attention (12)</summary>

- [#4230](https://github.com/ROCm/aiter/pull/4230) Supports paged MQA logits FP4 varqlen kernel in FlyDSL
- [#3890](https://github.com/ROCm/aiter/pull/3890) Supports MTP for Multi-Head Latent Attention (MLA) via Gluon
- [#4312](https://github.com/ROCm/aiter/pull/4312) Enables stride-aware indexing on strided blocks for fused QK norm RoPE cache kernels
- [#4412](https://github.com/ROCm/aiter/pull/4412) Supports nhead=96 for MLA in Gluon
- [#4401](https://github.com/ROCm/aiter/pull/4401) (Opened) Adds gfx942 forward split KV attention kernels
- [#4441](https://github.com/ROCm/aiter/pull/4441) (Opened) Adds HSTU forward kernel via FlyDSL
- [#4415](https://github.com/ROCm/aiter/pull/4415) (Opened) Implements length-adaptive deterministic top-k for sparse-MLA indexer
- [#4422](https://github.com/ROCm/aiter/pull/4422) (Opened) Adds fused gated residual, LayerNorm, and scale/shift op for DiT transformers
- [#4387](https://github.com/ROCm/aiter/pull/4387) (Opened) Limits attention kernel dispatch to supported GPUs
- [#4445](https://github.com/ROCm/aiter/pull/4445) (Opened) Re-enables FP4 KV cache for UA and MLA on gfx1250
- [#4440](https://github.com/ROCm/aiter/pull/4440) (Opened) Supports block sizes > 1 in paged MQA logits for DeepSeek-V4
- [#4388](https://github.com/ROCm/aiter/pull/4388) (Opened) Specializes batch prefill for paged KV layout
</details>

<details>
<summary>Refactors (8)</summary>

- [#4402](https://github.com/ROCm/aiter/pull/4402) Vendors buffer_ops/vector into AITER for FlyDSL
- [#4368](https://github.com/ROCm/aiter/pull/4368) Refactors module_moe_asm and removes Torch dependencies
- [#4434](https://github.com/ROCm/aiter/pull/4434) Refactors module_rmsnorm_quant and removes Torch dependencies
- [#4421](https://github.com/ROCm/aiter/pull/4421) Refactors module_quick_all_reduce and removes Torch dependencies
- [#4393](https://github.com/ROCm/aiter/pull/4393) Refactors module_pos_encoding and removes Torch dependencies
- [#4394](https://github.com/ROCm/aiter/pull/4394) (Opened) Massive MoE rebase and refactor across FlyDSL and HIP backends
- [#4459](https://github.com/ROCm/aiter/pull/4459) (Opened) Refactors MoE and quantization components in FlyDSL
- [#4460](https://github.com/ROCm/aiter/pull/4460) (Opened) Refactors top-k gating to support softmax with need_renorm
</details>

<details>
<summary>Bugfixes (21)</summary>

- [#4341](https://github.com/ROCm/aiter/pull/4341) Fixes MLA to refresh qh16 FP8 persistent decode HSACO for large page_id
- [#4375](https://github.com/ROCm/aiter/pull/4375) Fixes FlyDSL MoE sorting graph capture break with DP attention + EP
- [#4342](https://github.com/ROCm/aiter/pull/4342) Fixes fused_qk_rope_concat_and_cache_mla for DCP
- [#4429](https://github.com/ROCm/aiter/pull/4429) Maps SiTUv2 activation in MoE AOT parse_csv
- [#4417](https://github.com/ROCm/aiter/pull/4417) Fixes large-token FlyDSL MoE launch and output limits
- [#3451](https://github.com/ROCm/aiter/pull/3451) Fixes Q UE8M0 quantization and requires FP32 LN params in fused DSv3.2 indexer
- [#4406](https://github.com/ROCm/aiter/pull/4406) Prevents scale out-of-bounds in gemm_a8w8_blockscale and supports Triton 3.6
- [#4343](https://github.com/ROCm/aiter/pull/4343) Fixes >4GB a4w4 weight buffer-offset overflow for Kimi-K2.6
- [#4438](https://github.com/ROCm/aiter/pull/4438) Uses vec_size=32 for dim=1024 rotate-quant kernels in DeepSeek-V4
- [#4082](https://github.com/ROCm/aiter/pull/4082) Synchronizes custom collectives before returning
- [#4346](https://github.com/ROCm/aiter/pull/4346) Adds missing end_sync barrier in fused allreduce+rmsnorm kernel
- [#4452](https://github.com/ROCm/aiter/pull/4452) (Opened) Refreshes gfx950 MLA HSACO for large page_id KV addressing
- [#4451](https://github.com/ROCm/aiter/pull/4451) (Opened) Works around all-zero fused MoE output at block_m=32
- [#4427](https://github.com/ROCm/aiter/pull/4427) (Opened) Fixes large-stride KV address overflow in paged MQA logits
- [#4413](https://github.com/ROCm/aiter/pull/4413) (Opened) Recovers mp_tuner from worker death instead of hanging
- [#4426](https://github.com/ROCm/aiter/pull/4426) (Opened) Fixes gfx1250 a8w4 async gather API
- [#4432](https://github.com/ROCm/aiter/pull/4432) (Opened) Uses residual.stride(1) for MHC HC-slice indexing
- [#4447](https://github.com/ROCm/aiter/pull/4447) (Opened) Sets the _get_config memo only after the config JSON loads
- [#4389](https://github.com/ROCm/aiter/pull/4389) (Opened) Fixes AITER JIT builds on gfx90a
- [#4436](https://github.com/ROCm/aiter/pull/4436) (Opened) Adapts FlyDSL kernels to internal LLVM ROCDL API changes
- [#4449](https://github.com/ROCm/aiter/pull/4449) (Opened) Fixes 32-bit GU offsets overflow
</details>

<details>
<summary>CI, Build & Tests (10)</summary>

- [#4403](https://github.com/ROCm/aiter/pull/4403) Pins Ruff and makes its configuration explicit (massive formatting churn)
- [#4297](https://github.com/ROCm/aiter/pull/4297) Auto-updates split test FILE_TIMES
- [#4408](https://github.com/ROCm/aiter/pull/4408) Upgrades FlyDSL dependency to 0.2.4
- [#4384](https://github.com/ROCm/aiter/pull/4384) Repins CK to f33252ce and fixes build/test errors
- [#4444](https://github.com/ROCm/aiter/pull/4444) (Opened) Adds SDXL 1.0 conv2d shapes to conv_shapes.json
- [#4424](https://github.com/ROCm/aiter/pull/4424) (Opened) Documents and automates the AITER release plan
- [#4418](https://github.com/ROCm/aiter/pull/4418) (Opened) Adds an always-run AITER test gate
- [#4458](https://github.com/ROCm/aiter/pull/4458) (Opened) Adds an extended test workflow
- [#4431](https://github.com/ROCm/aiter/pull/4431) (Opened) Bumps FlyDSL dependency to 0.3.0.dev765
- [#4386](https://github.com/ROCm/aiter/pull/4386) (Opened) Uses FlyDSL dev release for CI validation
</details>

<details>
<summary>Docs (2)</summary>

- [#4392](https://github.com/ROCm/aiter/pull/4392) Corrects errors and discrepancies in the MLA v4 MI355 kernel design documents
- [#4404](https://github.com/ROCm/aiter/pull/4404) Announces Kimi-K3 support in the README News section
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: e0031c3297de336daf52da810edd7fbd3c4a1f5ab4ccd254de43e77fc1aad2f1 -->
