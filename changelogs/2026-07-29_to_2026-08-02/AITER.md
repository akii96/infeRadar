# AITER: PR digest (2026-07-29 to 2026-08-02)

_31 merged, 61 newly opened - source ROCm/AITER, generated 2026-08-02T22:00:09Z_

## TL;DR
* **Models & Focus**: Kimi (K3, K2.5/2.6) and DeepSeek (V4, OPUS) dominated this cycle, driving massive kernel optimizations in MoE, quantization, and Multi-Head Latent Attention (MLA).
* **MoE & Quantization**: Major architectural push for fused heterogeneous MXFP4/FP8 shared-expert MoE (FHMoE) via FlyDSL, alongside new production A8W4 MoE stage1 kernels and a faster a16w4 SiTUv2 kernel for Kimi.
* **Attention & MLA**: DeepSeek MLA saw significant tuning, including split-major grid scheduling, FP4/FP8 KV cache support, and critical fixes for large `page_id` KV addressing (>2GB).
* **Hardware & Frameworks**: Heavy tuning for AMD gfx950 and gfx1250 architectures using FlyDSL and Gluon/Triton backends, particularly for GEMM layout refactoring and kernel fusions.

## Most important PRs
* **[#4269](https://github.com/ROCm/aiter/pull/4269)** Introduces fused heterogeneous MXFP4/FP8 shared-expert MoE (FHMoE) via FlyDSL. This massive addition shares mixed-MoE kernel builders to streamline quantized MoE execution.
* **[#4502](https://github.com/ROCm/aiter/pull/4502)** Replaces the existing a16w4 (bf16 activation x MXFP4 weight) SiTUv2 kernel with a faster, corrected implementation specifically tuned for Kimi models (currently in progress).
* **[#4464](https://github.com/ROCm/aiter/pull/4464)** Ships production-ready A8W4 MoE stage1 kernels for DeepSeek OPUS on gfx950, heavily tuning the GEMM and quantization paths.
* **[#4430](https://github.com/ROCm/aiter/pull/4430)** Adds a specialized ds32 OPUS kernel for DeepSeek's Multi-Head Latent Attention (MLA) in prompt-sharing (PS) mode, targeting the `nhead*qseqlen=128` edge case (currently in progress).
* **[#4511](https://github.com/ROCm/aiter/pull/4511)** Implements MXFP8 paged attention MQA logits for DeepSeek OPUS on gfx950 and gfx1250, expanding low-precision attention support (currently in progress).

## More changes by area

<details>
<summary>MoE & quantization (26)</summary>

- [#4394](https://github.com/ROCm/aiter/pull/4394) refactors and rebases gfx1250 FlyDSL/HIP MoE and quantization kernels
- [#4374](https://github.com/ROCm/aiter/pull/4374) refactors gfx1250 FlyDSL GEMMs to use a layout-based API
- [#4475](https://github.com/ROCm/aiter/pull/4475) unifies and renames A8W8 GEMM kernels for gfx1250 FlyDSL
- [#4428](https://github.com/ROCm/aiter/pull/4428) adds `inverse_rope_group_quant` op for DeepSeek-V4 `wo_a` input
- [#4459](https://github.com/ROCm/aiter/pull/4459) refactors tiny MoE and quantization kernels in FlyDSL
- [#4434](https://github.com/ROCm/aiter/pull/4434) refactors `module_rmsnorm_quant` and removes torch dependencies
- [#4312](https://github.com/ROCm/aiter/pull/4312) enables stride-aware indexing for fused QK norm RoPE cache PTS quant shuffle
- [#3886](https://github.com/ROCm/aiter/pull/3886) adds OAI SwiGLU for per-token FP8 CK XDL 2-stage MoE
- [#4429](https://github.com/ROCm/aiter/pull/4429) fixes FlyDSL AOT to map SiTUv2 activation in MoE CSV parsing
- [#4454](https://github.com/ROCm/aiter/pull/4454) adds 640-expert top-8 ASM kernels for gfx942/gfx950
- [#4417](https://github.com/ROCm/aiter/pull/4417) fixes large-token FlyDSL MoE launch and output limits
- [#4406](https://github.com/ROCm/aiter/pull/4406) prevents scale out-of-bounds in A8W8 blockscale GEMM and supports Triton 3.6
- [#4438](https://github.com/ROCm/aiter/pull/4438) fixes DeepSeek-V4 rotate-quant kernels to use `vec_size=32` for `dim=1024`
- [#4449](https://github.com/ROCm/aiter/pull/4449) fixes 32-bit GU offsets overflow in MoE/quant kernels
- [#4439](https://github.com/ROCm/aiter/pull/4439) opens work on "megamoe" distributed MoE kernels via FlyDSL
- [#4446](https://github.com/ROCm/aiter/pull/4446) opens `moe_a16w4` Gluon kernel for gfx1250
- [#4460](https://github.com/ROCm/aiter/pull/4460) opens support for softmax with `need_renorm` in top-K gating
- [#4482](https://github.com/ROCm/aiter/pull/4482) opens fix for gfx1250 grouped-MoE expert scan above 512 experts and computes SiTUv2
- [#4471](https://github.com/ROCm/aiter/pull/4471) opens support for SiTUv2 in the packed-int4 MoE stage1 epilogue via FlyDSL
- [#4463](https://github.com/ROCm/aiter/pull/4463) opens an opt-in a4w4 SiTUv2 MoE path and fixes tuner defects
- [#4451](https://github.com/ROCm/aiter/pull/4451) opens workaround for all-zero fused MoE output at `block_m=32`
- [#4448](https://github.com/ROCm/aiter/pull/4448) opens plumbing for split-K through the a8w8 blockscale bpreshuffle GEMM
- [#4506](https://github.com/ROCm/aiter/pull/4506) opens fix for silent row-major `transpose_scale` in fused RMS FP8 group quant
- [#4510](https://github.com/ROCm/aiter/pull/4510) opens fix to honor `b_nt` in mixed-MoE stage-2 weight loads and retunes Kimi-K3 rows
- [#4500](https://github.com/ROCm/aiter/pull/4500) opens EP MoE updates for Triton/Gluon on gfx9 and gfx12
- [#4467](https://github.com/ROCm/aiter/pull/4467) opens bounds checking for packed FP4 output stores in `module_rmsnorm_quant`

</details>

<details>
<summary>Kernels & attention (22)</summary>

- [#4501](https://github.com/ROCm/aiter/pull/4501) cleans up FlyDSL attention and norm kernels
- [#4402](https://github.com/ROCm/aiter/pull/4402) vendors `buffer_ops/vector` into AITER for FlyDSL
- [#4341](https://github.com/ROCm/aiter/pull/4341) fixes MLA to refresh qh16 FP8 persistent decode HSACO for large `page_id`
- [#4373](https://github.com/ROCm/aiter/pull/4373) adds a thin sparse attention operator for CK/VSA
- [#4342](https://github.com/ROCm/aiter/pull/4342) fixes `fused_qk_rope_concat_and_cache_mla` for DCP
- [#4412](https://github.com/ROCm/aiter/pull/4412) supports `nhead=96` for MLA in Gluon
- [#4044](https://github.com/ROCm/aiter/pull/4044) optimizes unified attention for Gemma-4-31b in Triton
- [#4441](https://github.com/ROCm/aiter/pull/4441) opens HSTU forward kernel via FlyDSL
- [#4466](https://github.com/ROCm/aiter/pull/4466) opens FWD split KV for gfx942
- [#4491](https://github.com/ROCm/aiter/pull/4491) opens gfx950 packed BF16 GDN decode kernel
- [#4473](https://github.com/ROCm/aiter/pull/4473) opens OPUS hd192 hybrid buffer path for large KV (>4GiB)
- [#4452](https://github.com/ROCm/aiter/pull/4452) opens refresh of gfx950 MLA HSACO for large `page_id` KV addressing
- [#4450](https://github.com/ROCm/aiter/pull/4450) opens optimizations for 12-head Gluon MLA split scheduling
- [#4462](https://github.com/ROCm/aiter/pull/4462) opens fix for `mha_varlen_fwd` paged codegen branch
- [#4509](https://github.com/ROCm/aiter/pull/4509) opens split-major grid and blocked stage-2 reduce for Kimi-K3 small-nhead decode
- [#4488](https://github.com/ROCm/aiter/pull/4488) opens regression test for the >2GB KV cache path in Gluon MLA
- [#4445](https://github.com/ROCm/aiter/pull/4445) opens re-enabling of FP4 KV cache for UA and MLA on gfx12
- [#4440](https://github.com/ROCm/aiter/pull/4440) opens support for block sizes > 1 in paged MQA logits for DeepSeek-V4
- [#4480](https://github.com/ROCm/aiter/pull/4480) opens FP8 KV cache support for small-head MLA decode on gfx950
- [#4507](https://github.com/ROCm/aiter/pull/4507) opens sizing of `NUM_KV_SPLITS` from the page table in Gluon MLA
- [#4436](https://github.com/ROCm/aiter/pull/4436) opens adaptation of FlyDSL kernels to internal LLVM ROCDL API changes
- [#4474](https://github.com/ROCm/aiter/pull/4474) opens fix for int32 KV-offset overflow in `_mla_gluon` >2GB path

</details>

<details>
<summary>Performance & tuning (22)</summary>

- [#4410](https://github.com/ROCm/aiter/pull/4410) merges v2 tuning configurations for FlyDSL/HIP MoE and GEMM
- [#4253](https://github.com/ROCm/aiter/pull/4253) tunes DeepSeek-V4 Pro EP (TP1 shape) for Triton/Gluon on gfx12
- [#4435](https://github.com/ROCm/aiter/pull/4435) adds Kimi-K3 GEMM and MoE tuned configs
- [#4485](https://github.com/ROCm/aiter/pull/4485) adds Qwen3.5-397B-A17B-MXFP4 a16w4 tuned fmoe config
- [#4307](https://github.com/ROCm/aiter/pull/4307) ports BM16 for Kimi-K2.5/K2.6 FP4 decode gemm2, yielding +3~13% throughput
- [#4443](https://github.com/ROCm/aiter/pull/4443) opens optimization for MXFP4 MoE decode with fused sorting, quantization, and compact scales
- [#4495](https://github.com/ROCm/aiter/pull/4495) opens fusion of Kimi-K3 KDA decode and `f_b` projection in FlyDSL
- [#4504](https://github.com/ROCm/aiter/pull/4504) opens fusion of Kimi-K3 FP8 pre-route projections
- [#4498](https://github.com/ROCm/aiter/pull/4498) opens fusion of Kimi-K3 B1 BF16 pre-route projections on gfx950
- [#4433](https://github.com/ROCm/aiter/pull/4433) opens fusion of A2 quant for DeepSeek-V4 FlyDSL EP
- [#4496](https://github.com/ROCm/aiter/pull/4496) opens fusion of Kimi-K3 B1 latent MoE tail
- [#4503](https://github.com/ROCm/aiter/pull/4503) opens Kimi-K3 FP8 latent MoE tail
- [#4499](https://github.com/ROCm/aiter/pull/4499) opens optimization for Kimi-K3 KDA group64 projection on gfx950
- [#4497](https://github.com/ROCm/aiter/pull/4497) opens fusion of Kimi-K3 MLA output gate on gfx950
- [#4470](https://github.com/ROCm/aiter/pull/4470) opens fine-grained tuning based on M for gfx1250 MoE/GEMM
- [#4469](https://github.com/ROCm/aiter/pull/4469) opens tuning for gfx950 GEMM A16W16 configs for Triton TOT
- [#4453](https://github.com/ROCm/aiter/pull/4453) opens tuning for `batched_gemm_a8w8` per-token-group for large M on gfx950
- [#4489](https://github.com/ROCm/aiter/pull/4489) opens GLM-5.2 dense tuned configs for gfx950
- [#4493](https://github.com/ROCm/aiter/pull/4493) opens gfx1101 tuning config for Triton MHA
- [#4487](https://github.com/ROCm/aiter/pull/4487) opens `block_m=64` for DSpark verify-step token in Kimi-K3 SiTUv2 MoE
- [#4476](https://github.com/ROCm/aiter/pull/4476) opens tuning for dpskv4 flash TP4 GEMM for gfx942
- [#4479](https://github.com/ROCm/aiter/pull/4479) opens tuning for Kimi-K3 prefill GEMMs for gfx950

</details>

<details>
<summary>Parallelism & distributed (3)</summary>

- [#4421](https://github.com/ROCm/aiter/pull/4421) refactors `module_quick_all_reduce` and removes torch dependencies
- [#4082](https://github.com/ROCm/aiter/pull/4082) synchronizes custom collectives before return
- [#4478](https://github.com/ROCm/aiter/pull/4478) opens forwarding of `transpose_scale` through fused AllReduce + RMSNorm per-group quant

</details>

<details>
<summary>Tests, CI & build (5)</summary>

- [#4468](https://github.com/ROCm/aiter/pull/4468) extends multi-GPU test timeout
- [#4444](https://github.com/ROCm/aiter/pull/4444) opens addition of SDXL 1.0 conv2d shapes to `conv_shapes.json`
- [#4458](https://github.com/ROCm/aiter/pull/4458) opens extended test workflow to CI
- [#4484](https://github.com/ROCm/aiter/pull/4484) opens Flash Attention CK CI smoke test
- [#4431](https://github.com/ROCm/aiter/pull/4431) opens bump of FlyDSL dependency to 0.3.0

</details>

<details>
<summary>API & misc (9)</summary>

- [#4486](https://github.com/ROCm/aiter/pull/4486) opens C++ `paged_attention_ragged` entry point and tests
- [#4465](https://github.com/ROCm/aiter/pull/4465) opens optimization for ctypes marshalling
- [#4461](https://github.com/ROCm/aiter/pull/4461) opens support for per-token/per-channel scales in `wvSplitKQ`
- [#4494](https://github.com/ROCm/aiter/pull/4494) opens fix for ASM split-K semaphore deadlock under CUDA graph capture
- [#4432](https://github.com/ROCm/aiter/pull/4432) opens fix for MHC HC-slice indexing to use `residual.stride(1)`
- [#4447](https://github.com/ROCm/aiter/pull/4447) opens fix to set the `_get_config` memo only after the config JSON loads in Triton
- [#4508](https://github.com/ROCm/aiter/pull/4508) opens fix for Python 3.14 compatibility issue with `aggregate` in Triton/Gluon
- [#4481](https://github.com/ROCm/aiter/pull/4481) opens parallelization of `gather_kv_b_proj` context chunks
- [#4512](https://github.com/ROCm/aiter/pull/4512) opens resolution of gfx1100 targets across JIT paths

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: ac8b94287f7f3736261d0f84a6bccf01b3b47e8a519fdcb0b184be80c9156a3a -->
