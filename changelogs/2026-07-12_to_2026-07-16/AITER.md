# AITER: PR digest (2026-07-12 to 2026-07-16)

_42 merged, 42 newly opened - source ROCm/AITER, generated 2026-07-16T11:00:28Z_

## TL;DR
- **DeepSeek V4 & MLA focus**: DeepSeek dominated this window, highlighted by the massive merged 1st-gen 64/128-head MLA decode kernel for MI35x (gfx950).
- **A8W8 Blockscale GEMM expansion**: Significant performance work landed and opened for A8W8 blockscale BpreShuffle GEMMs across architectures, including MI300X (gfx942) and gfx1250.
- **FlyDSL integration & FP4**: Heavy investment in the FlyDSL backend, including vendoring the cco-LSA v2 MoE dispatch layer and merging new paged MQA logits FP4 kernels.
- **Model & Arch Tuning**: Extensive tuning configs were added for GLM-5.2, MiniMax, Qwen, and GPT-OSS, alongside broad support for next-gen AMD architectures (gfx950, gfx1250).

## Most important PRs
- **[#3459](https://github.com/ROCm/aiter/pull/3459) Introduce the 1st Gen 64 and 128 Heads MLA Decode Kernel for DeepSeek V4 for MI35x**
  This massive merged PR (11k+ lines) delivers the first-generation MLA decode kernel specifically optimized for DeepSeek V4 on the MI35x (gfx950) architecture.
- **[#4260](https://github.com/ROCm/aiter/pull/4260) feat(flydsl): vendor cco-LSA v2 dispatch/combine op-layer into aiter**
  Vendors the FlyDSL cco-LSA v2 dispatch and combine operation layer directly into the repository, significantly improving MoE routing and execution.
- **[#4204](https://github.com/ROCm/aiter/pull/4204) [gfx942][opus] Support A8W8 blockscale BpreShuffle GEMM**
  Brings A8W8 blockscale BpreShuffle GEMM support to the MI300X (gfx942) architecture, enabling highly efficient quantized matrix multiplications for DeepSeek models.
- **[#4210](https://github.com/ROCm/aiter/pull/4210) [gfx1250][FlyDSL] Support a8w8 blockscale bpreshuffle gemm**
  A newly opened PR that extends the A8W8 blockscale BpreShuffle GEMM capabilities to the gfx1250 architecture using the FlyDSL backend.
- **[#3681](https://github.com/ROCm/aiter/pull/3681) [FLYDSL] Support paged mqa logits fp4 kernel**
  Merges a new FlyDSL-based kernel for paged MQA logits using FP4 quantization, pushing the boundaries of low-bitwidth attention performance.

## More changes by area

<details>
<summary>Performance (20)</summary>

- [#4200](https://github.com/ROCm/aiter/pull/4200) adds Gluon BF16 BMM for gfx1250 via Triton
- [#4236](https://github.com/ROCm/aiter/pull/4236) adds tuned FP8 PTPC GEMM and MoE configs for GLM-5.2
- [#4196](https://github.com/ROCm/aiter/pull/4196) improves MoE occupancy and GEMM kernel args preload on gfx1250
- [#4199](https://github.com/ROCm/aiter/pull/4199) removes GRID_MN and retunes A8W8 GEMM for Pro and Flash
- [#4202](https://github.com/ROCm/aiter/pull/4202) routes decode-M DeepSeek shapes to Triton for A8W8 blockscale GEMM
- [#4241](https://github.com/ROCm/aiter/pull/4241) updates A8W8 blockscale GEMM config to avoid end-to-end hangs on gfx1250
- [#4229](https://github.com/ROCm/aiter/pull/4229) adds tuning configs for Yadai MoE EP on gfx1250
- [#4068](https://github.com/ROCm/aiter/pull/4068) enables double-quantization and KV reverse to improve BF16 ASM MHA performance
- [#4254](https://github.com/ROCm/aiter/pull/4254) (opened) adds MXFP8 GEMM tuning configs via FlyDSL
- [#4246](https://github.com/ROCm/aiter/pull/4246) (opened) adds split-K fusion for OPUS GEMM on gfx1250
- [#4206](https://github.com/ROCm/aiter/pull/4206) (opened) adds FlyDSL blockwise W8A8 BMM for gfx1250
- [#4203](https://github.com/ROCm/aiter/pull/4203) (opened) tunes DeepSeek V4 FP8 A8W8 blockscale BpreShuffle and A16W16 GEMMs for gfx950
- [#4222](https://github.com/ROCm/aiter/pull/4222) (opened) tunes A16W16 GEMM for DeepSeek V4 Pro shapes on gfx1250
- [#4253](https://github.com/ROCm/aiter/pull/4253) (opened) tunes DeepSeek V4 Pro EP (TP1 shape) for Gluon Triton
- [#4234](https://github.com/ROCm/aiter/pull/4234) (opened) adds tuned Triton A16W16 GEMM configs for RDNA3 (gfx1100)
- [#4228](https://github.com/ROCm/aiter/pull/4228) (opened) updates tuned FlyDSL MoE kernels for gfx1250
- [#4223](https://github.com/ROCm/aiter/pull/4223) (opened) tunes and includes fuse-aware fused GEMM A8W8 blockscale mul_add for gfx950
- [#4243](https://github.com/ROCm/aiter/pull/4243) (opened) adds GLM-5.2 tuned configs for A8W8 blockscale BpreShuffle GEMM on gfx950
- [#4242](https://github.com/ROCm/aiter/pull/4242) (opened) tunes FlashAttention backward configs for gfx1151
- [#4261](https://github.com/ROCm/aiter/pull/4261) (opened) adds tuned config for MiMo-V2.5-Pro prefill on MI300X

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#4250](https://github.com/ROCm/aiter/pull/4250) (opened) adapts prefill GDN with a major refactor across HIP and Triton backends
- [#4154](https://github.com/ROCm/aiter/pull/4154) adds causal mask support and init-pattern for ASM MXFP8 MHA on gfx1250
- [#4248](https://github.com/ROCm/aiter/pull/4248) writes paged SWA from fused QK norm RoPE for DeepSeek V4
- [#4227](https://github.com/ROCm/aiter/pull/4227) adds forward compatibility to `get_mla_metadata_v1`
- [#4231](https://github.com/ROCm/aiter/pull/4231) adds E8M0 block-scale output to fused RMSNorm quantization
- [#4256](https://github.com/ROCm/aiter/pull/4256) moves `MlaVersion` enum to `module_aiter_core`
- [#4156](https://github.com/ROCm/aiter/pull/4156) updates MLA QH16 to support global load KV on gfx950
- [#4205](https://github.com/ROCm/aiter/pull/4205) (opened) adds OPUS BF16 FMHA d192x128 kernel for gfx950
- [#4221](https://github.com/ROCm/aiter/pull/4221) (opened) implements paged MLA indexer via FlyDSL and Gluon
- [#4230](https://github.com/ROCm/aiter/pull/4230) (opened) supports paged MQA logits FP4 varqlen kernel in FlyDSL
- [#4232](https://github.com/ROCm/aiter/pull/4232) (opened) adds native FP8 MFMA Gluon `fp8_mqa_logits` kernel for MI300X
- [#4218](https://github.com/ROCm/aiter/pull/4218) (opened) adds support for pool indexing of hidden states in gated delta rule prefill kernel
- [#4209](https://github.com/ROCm/aiter/pull/4209) (opened) simplifies QK norm RoPE quant kernels using FlyDSL syntactic sugar
- [#4258](https://github.com/ROCm/aiter/pull/4258) (opened) supports qseqlen > 4 through 32mx4 kernel for MI350 MLA PS mode
- [#4217](https://github.com/ROCm/aiter/pull/4217) (opened) updates MLA v4 kernel for gfx1250
- [#4239](https://github.com/ROCm/aiter/pull/4239) (opened) adds Chefang MHA global kernel for gfx950

</details>

<details>
<summary>MoE & quantization (8)</summary>

- [#4139](https://github.com/ROCm/aiter/pull/4139) packs FP4, INT4, and UINT4 as sub-byte elements in containers for OPUS
- [#4098](https://github.com/ROCm/aiter/pull/4098) implements FP8 index cache writes for MiniMax
- [#3111](https://github.com/ROCm/aiter/pull/3111) adds FMoE run-config mismatch diagnostics
- [#3593](https://github.com/ROCm/aiter/pull/3593) adds opt-in `AITER_MOE_FORCE_BF16_ACT` to force BF16 activations
- [#4225](https://github.com/ROCm/aiter/pull/4225) reverts the `AITER_MOE_FORCE_BF16_ACT` addition
- [#4186](https://github.com/ROCm/aiter/pull/4186) reverts MLA v4 CO refinement
- [#4251](https://github.com/ROCm/aiter/pull/4251) (opened) generalizes MoE A8W4 stage-2 K scheduler and effective-K dispatch for gfx950
- [#4249](https://github.com/ROCm/aiter/pull/4249) (opened) adds fused clamped-alpha SwiGLU gate activation for MiniMax-M3 and GPT-OSS

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#4207](https://github.com/ROCm/aiter/pull/4207) (opened) adds IFOE cross-node custom all-reduce tests
- [#4233](https://github.com/ROCm/aiter/pull/4233) (opened) gates gfx1250 transport for custom all-reduce by ROCm 7.14
- [#4213](https://github.com/ROCm/aiter/pull/4213) (opened) supports adding fused all-reduce

</details>

<details>
<summary>Bugfixes (24)</summary>

- [#4216](https://github.com/ROCm/aiter/pull/4216) fixes rescale, zero padding scale, and mask OOB V in sparse prefill attention
- [#4117](https://github.com/ROCm/aiter/pull/4117) fixes ragged `split_indptr` short-seq and adds OOB/bucket tests for MLA v4
- [#3934](https://github.com/ROCm/aiter/pull/3934) parametrizes sweep in `test_topk_plain` to fix collection-time OOM
- [#4171](https://github.com/ROCm/aiter/pull/4171) fixes dispatch gap rules, arch-string FP, P5 timing errors, and D10b FlyDSL
- [#3656](https://github.com/ROCm/aiter/pull/3656) fixes FMoE run config quantization alignment
- [#4197](https://github.com/ROCm/aiter/pull/4197) fixes FlyDSL JIT compilation on gfx1250
- [#4195](https://github.com/ROCm/aiter/pull/4195) floors FP8 E8M0 group amax to avoid zero-scale in fused QK for DeepSeek V4
- [#3257](https://github.com/ROCm/aiter/pull/3257) shrinks `BLOCK_KV` and `num_stages` in `fp8_mqa_logits` to fit 64KB LDS on MI300X
- [#4201](https://github.com/ROCm/aiter/pull/4201) fixes new `async_gather` API in sparse PA decode and prefill on gfx1250
- [#3997](https://github.com/ROCm/aiter/pull/3997) requires KBatch >= 2 for block-FP8 split-K in fused MoE
- [#4194](https://github.com/ROCm/aiter/pull/4194) fixes Qwen3.5 397B tuned GEMM dispatch on MI300X
- [#4237](https://github.com/ROCm/aiter/pull/4237) fixes BMM BF16 CI on gfx950
- [#3331](https://github.com/ROCm/aiter/pull/3331) fixes activation CLI argument parsing in `test_moe.py`
- [#4245](https://github.com/ROCm/aiter/pull/4245) fixes NaN leak from OOB KV page-ID folding to slot 0 in MLA v4
- [#4208](https://github.com/ROCm/aiter/pull/4208) (opened) applies Black formatting to FlyDSL BMM W8A8 files
- [#4247](https://github.com/ROCm/aiter/pull/4247) (opened) fixes Top-K gating with NaN/Inf inputs
- [#4252](https://github.com/ROCm/aiter/pull/4252) (opened) fixes expert map parallel implementation
- [#4244](https://github.com/ROCm/aiter/pull/4244) (opened) fixes silent tail-row drop in `deepgemm_fp8_paged_mqa_logits` at large output strides
- [#4238](https://github.com/ROCm/aiter/pull/4238) (opened) fixes GEMM A16W8/A8W8 scale regression on gfx950
- [#4214](https://github.com/ROCm/aiter/pull/4214) (opened) fixes `ENABLE_Ck0` comparison error on gfx12
- [#4255](https://github.com/ROCm/aiter/pull/4255) (opened) fixes paged MQA logits support on gfx1201
- [#4220](https://github.com/ROCm/aiter/pull/4220) (opened) fixes `fused_qk_norm_rope_cache_quant` build without CK
- [#4240](https://github.com/ROCm/aiter/pull/4240) (opened) makes `shuffle_scale_moe` arch-agnostic to fix non-gfx950/gfx1250 regressions
- [#4235](https://github.com/ROCm/aiter/pull/4235) (opened) fixes FIPS crash in `hash_signature`

</details>

<details>
<summary>CI & build (7)</summary>

- [#4100](https://github.com/ROCm/aiter/pull/4100) adds ATOM DI CI smoke workflow
- [#4212](https://github.com/ROCm/aiter/pull/4212) auto-updates split test `FILE_TIMES`
- [#4184](https://github.com/ROCm/aiter/pull/4184) adds DeepSeek V3 vLLM disagg Spur smoke workflow
- [#4215](https://github.com/ROCm/aiter/pull/4215) bumps FlyDSL to version 0.2.4
- [#4211](https://github.com/ROCm/aiter/pull/4211) (opened) makes `check-signal` neutral on pre-check failure and gates downstream jobs
- [#4224](https://github.com/ROCm/aiter/pull/4224) (opened) repins CK to `cb859854` and fixes CI tests
- [#4257](https://github.com/ROCm/aiter/pull/4257) (opened) tracks ATOM main and pins cases to 1p1d via `--case`

</details>

<details>
<summary>Tests (1)</summary>

- [#4219](https://github.com/ROCm/aiter/pull/4219) (opened) adds support for test CSVs in FlyDSL MoE

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 2f864c3475b9a9aea6599e8704831c670ee1162b37688d547cc6a716dbc35216 -->
