# AITER: PR digest (2026-07-15 to 2026-07-19)

_32 merged, 32 newly opened - source ROCm/AITER, generated 2026-07-19T21:55:34Z_

## TL;DR
*   **DeepSeek MLA optimizations** dominated the window, with major Triton routing retunes for decode-M, persistent decode gating, and MI350 (gfx950) PS mode enhancements.
*   **MoE & Quantization** saw heavy investment for low-precision formats. Highlights include a generalized A8W4 stage2 K scheduler, FP4/INT4 packed containers, and a new heterogeneous MXFP4/FP8 fused shared-expert MoE.
*   **Hardware enablement** focused heavily on gfx1250 (RDNA4/MI400) and gfx950 (MI350), adding custom all-reduce gating, TDM deep-prefetch BF16 prefill kernels, and extensive A8W8 blockscale GEMM tuning.
*   **New model support** expanded to include GLM-5.2, MiniMax-M3, Kimi-K2.6, and GPT-OSS, with tailored MoE configs and fused SwiGLU activations.

## Most important PRs
*   **[#4264](https://github.com/ROCm/aiter/pull/4264)** retunes Triton routing for DeepSeek MLA decode-M on gfx950, delivering a massive cold-cache performance overhaul for A8W8 blockscale GEMMs.
*   **[#4260](https://github.com/ROCm/aiter/pull/4260)** vendors the cco-LSA v2 dispatch and combine op-layer into the FlyDSL backend, significantly expanding AITER's MoE dispatch capabilities.
*   **[#4251](https://github.com/ROCm/aiter/pull/4251)** generalizes the MoE A8W4 stage2 K scheduler and effective-K dispatch, improving low-precision MoE scheduling across the OPUS stack.
*   **[#4269](https://github.com/ROCm/aiter/pull/4269)** (newly opened) introduces a heterogeneous MXFP4/FP8 fused shared-expert MoE in FlyDSL, targeting DeepSeek's mixed-precision routing needs.
*   **[#4233](https://github.com/ROCm/aiter/pull/4233)** implements custom all-reduce for gfx1250, gating the transport mechanism by ROCm 7.14 to ensure stable distributed communication.

## More changes by area

<details>
<summary>Performance & Tuning (17)</summary>

- [#4271](https://github.com/ROCm/aiter/pull/4271) tunes MoE A8W4 TP4 configurations for gfx1250
- [#4236](https://github.com/ROCm/aiter/pull/4236) adds GLM5.2-FP8 PTPC GEMM and MoE tuned configs
- [#4267](https://github.com/ROCm/aiter/pull/4267) tunes BF16 GEMM for DeepSeek v4 on gfx1250
- [#4282](https://github.com/ROCm/aiter/pull/4282) fixes bugs and retunes BF16 GEMM on gfx1250
- [#4284](https://github.com/ROCm/aiter/pull/4284) optimizes MLA stage2 cross-split merge kernel with `num_warps=1`
- [#4241](https://github.com/ROCm/aiter/pull/4241) adjusts A8W8 blockscale GEMM config on gfx1250 to avoid e2e hangs
- [#4040](https://github.com/ROCm/aiter/pull/4040) adds flat and 16x FMoE kernels for GLM5.2-FP8 decode on gfx942
- [#4254](https://github.com/ROCm/aiter/pull/4254) (opened) adds MXFP8 GEMM tuning configs in FlyDSL
- [#4246](https://github.com/ROCm/aiter/pull/4246) (opened) tunes and fuses OPUS GEMM split-K on gfx1250
- [#4278](https://github.com/ROCm/aiter/pull/4278) (opened) optimizes MoE prefill performance on gfx1250
- [#4273](https://github.com/ROCm/aiter/pull/4273) (opened) adds a strided-batched BMM variant of A8W8 blockscale bpreshuffle GEMM for gfx1250
- [#4253](https://github.com/ROCm/aiter/pull/4253) (opened) tunes DeepSeek v4 Pro EP (TP1 shape) on gfx1250 and gfx950
- [#4287](https://github.com/ROCm/aiter/pull/4287) (opened) updates tuned MoE configurations
- [#4243](https://github.com/ROCm/aiter/pull/4243) (opened) adds GLM-5.2 tuned configs for A8W8 blockscale bpreshuffle GEMM on gfx950
- [#4270](https://github.com/ROCm/aiter/pull/4270) (opened) enables E2E SGLang inference tuning on gfx1250
- [#4266](https://github.com/ROCm/aiter/pull/4266) (opened) retunes MoE configurations for GLM-5.2 FP4
- [#4261](https://github.com/ROCm/aiter/pull/4261) (opened) adds tuned config for MiMo-V2.5-Pro prefill on MI300X
</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#4258](https://github.com/ROCm/aiter/pull/4258) supports `qseqlen > 4` via 32mx4 kernel for MI350 MLA PS mode
- [#4144](https://github.com/ROCm/aiter/pull/4144) gates persistent MLA decode kernel by batch size
- [#4239](https://github.com/ROCm/aiter/pull/4239) adds global MHA tests for gfx950
- [#4245](https://github.com/ROCm/aiter/pull/4245) fixes NaN leak from OOB KV page-id folding in MLA v4 nm
- [#4217](https://github.com/ROCm/aiter/pull/4217) updates the MLA v4 kernel for gfx1250
- [#4256](https://github.com/ROCm/aiter/pull/4256) moves the `MlaVersion` enum to `module_aiter_core`
- [#4280](https://github.com/ROCm/aiter/pull/4280) (opened) migrates FlyDSL shared memory for attention and GEMM on gfx1201/gfx1250
- [#4279](https://github.com/ROCm/aiter/pull/4279) (opened) optimizes MHC BF16 compute on gfx12xx
- [#4265](https://github.com/ROCm/aiter/pull/4265) (opened) enables conv2d Triton kernels for RDNA3 (gfx1100) and RDNA3.5 (gfx1151)
- [#4268](https://github.com/ROCm/aiter/pull/4268) (opened) adds a fused AdaLN-Zero (layernorm + scale/shift) Triton kernel
- [#4292](https://github.com/ROCm/aiter/pull/4292) (opened) fixes NaN issues when quantizing zero SageAttention V channels in Triton
- [#4293](https://github.com/ROCm/aiter/pull/4293) (opened) corrects ragged paged-MQA causal masks in Triton
- [#4255](https://github.com/ROCm/aiter/pull/4255) (opened) supports paged MQA logits on gfx1201 in Triton
</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#4139](https://github.com/ROCm/aiter/pull/4139) packs FP4, INT4, and UINT4 as single sub-byte elements in containers
- [#3844](https://github.com/ROCm/aiter/pull/3844) adds a HIP kernel for RMSNorm and per-token quantization
- [#4248](https://github.com/ROCm/aiter/pull/4248) writes paged SWA from fused QK norm RoPE for DeepSeek v4
- [#4272](https://github.com/ROCm/aiter/pull/4272) optimizes fused QK norm RoPE group quantization
- [#3656](https://github.com/ROCm/aiter/pull/3656) fixes FMoE run config quantization alignment
- [#3997](https://github.com/ROCm/aiter/pull/3997) requires `KBatch >= 2` for block-FP8 split-K in fused MoE
- [#4249](https://github.com/ROCm/aiter/pull/4249) (opened) adds fused clamped-alpha SwiGLU gate activation for MiniMax-M3 and GPT-OSS
- [#4247](https://github.com/ROCm/aiter/pull/4247) (opened) fixes NaN and Inf inputs in TopK gating
- [#4252](https://github.com/ROCm/aiter/pull/4252) (opened) fixes Expert Map Parallel in Triton MoE
- [#4291](https://github.com/ROCm/aiter/pull/4291) (opened) defines zero-row and padded FP8/INT8 quantization in Triton
</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#4281](https://github.com/ROCm/aiter/pull/4281) (opened) adds TDM deep-prefetch BF16 prefill for QK norm RoPE on gfx1250
- [#4286](https://github.com/ROCm/aiter/pull/4286) (opened) adds TDM deep-prefetch BF16 prefill for QK norm RoPE on gfx1250 (EP variant)
- [#4263](https://github.com/ROCm/aiter/pull/4263) (opened) reduces quad inline ASM and improves BF16 split-K tuning on gfx942
</details>

<details>
<summary>Model support (3)</summary>

- [#4274](https://github.com/ROCm/aiter/pull/4274) (opened) adds MiniMax-M3 to vLLM DI CI
- [#4275](https://github.com/ROCm/aiter/pull/4275) (opened) adds MiniMax-M3 to ATOM DI CI
- [#4276](https://github.com/ROCm/aiter/pull/4276) (opened) adds Kimi-K2.6 to vLLM DI CI
</details>

<details>
<summary>Bugfixes (5)</summary>

- [#4216](https://github.com/ROCm/aiter/pull/4216) fixes rescale, zero padding scale, and mask OOB V in OPUS/ATOM sparse prefill attention
- [#4244](https://github.com/ROCm/aiter/pull/4244) fixes silent tail-row drop in `deepgemm_fp8_paged_mqa_logits` at large output stride
- [#4171](https://github.com/ROCm/aiter/pull/4171) fixes dispatch gap rule, arch-string FP, P5 timing error, and D10b FlyDSL issues
- [#4277](https://github.com/ROCm/aiter/pull/4277) (opened) fixes Dev/gugu GEMM issues on gfx1250
- [#4294](https://github.com/ROCm/aiter/pull/4294) (opened) fixes IPC publication ordering in custom all-reduce on gfx1250
</details>

<details>
<summary>CI & build (6)</summary>

- [#4100](https://github.com/ROCm/aiter/pull/4100) adds ATOM DI CI smoke workflow
- [#4212](https://github.com/ROCm/aiter/pull/4212) auto-updates split test `FILE_TIMES`
- [#4184](https://github.com/ROCm/aiter/pull/4184) adds DeepSeek v3 vLLM disagg Spur smoke workflow
- [#4237](https://github.com/ROCm/aiter/pull/4237) fixes BMM BF16 CI on gfx950
- [#4283](https://github.com/ROCm/aiter/pull/4283) fixes `cktile_epilogue_silu` AOT arg mismatch on release branch
- [#4257](https://github.com/ROCm/aiter/pull/4257) (opened) tracks ATOM main and pin cases to 1p1d in CI
</details>

<details>
<summary>Other (2)</summary>

- [#4262](https://github.com/ROCm/aiter/pull/4262) skips split-K workspace prewarm for non-split-K kids
- [#4250](https://github.com/ROCm/aiter/pull/4250) (opened) adapts prefill GDN with massive HIP/Triton refactoring
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f970d2717cf40705f9ce08062ae42a2f05f551f1a34be4da126e7e65cda56d99 -->
