# AITER: PR digest (2026-08-26 to 2026-08-30)

_59 merged, 68 newly opened - source ROCm/AITER, generated 2026-08-30T23:18:50Z_

## TL;DR
- **DeepSeek (V4/DSA/MLA) and GLM (5.2/5.3)** led model attention. DeepSeek work centered on gfx1250 sparse-paged prefill, MLA v4 prefill ASM, and a fused DSA top-k. GLM work was mostly gfx950/gfx942 GEMM and MoE retunes.
- **Biggest perf work:** MHA v4 with block-sparse load-balancing, GQA and gfx950 bf16 / gfx942 i8/fp8 (`[#5005](https://github.com/ROCm/aiter/pull/5005)`, `[#4967](https://github.com/ROCm/aiter/pull/4967)`). Also gfx950 MXFP6 GEMMs (`[#4859](https://github.com/ROCm/aiter/pull/4859)`), the OPUS bf16 GEMM integration (`[#4903](https://github.com/ROCm/aiter/pull/4903)`), and FlyDSL one-stage split-K a8w8 (`[#5007](https://github.com/ROCm/aiter/pull/5007)`).
- **gfx1250 bring-up is the dominant hardware theme** (33 PRs): microbenchmarks, ASM f4/f8 GEMM fixes, MLA code objects, TDM BF16 qk_norm_rope, and mxfp4 MoE sort.
- **Direction:** Triton/Gluon config layout is being unified (nested arch/backend trees, wrapper-side resolution, config-aware repr). In parallel, Kimi-K3 and gfx950 indexer/MQA-logits kernels are in flight.

## Most important PRs
**[#4978](https://github.com/ROCm/aiter/pull/4978) — Dev lumen (merged)**
A 25k-line Triton/Gluon/HIP drop spanning MLA, MoE, GEMM, norm and quant kernels, with DeepSeek-oriented tuning configs and tests. It is the largest single kernel-surface change of the window.

**[#5005](https://github.com/ROCm/aiter/pull/5005) and [#4967](https://github.com/ROCm/aiter/pull/4967) — MHA v4 (merged)**
Add block-sparse MHA v4 with load balancing, plus GQA support, gfx950 bf16 and gfx942 int8/fp8 paths. This broadens the attention backends across MI300/MI350.

**[#4859](https://github.com/ROCm/aiter/pull/4859) — MXFP6 GEMMs (merged)**
Adds ASM/HIP MXFP6 GEMM kernels for gfx950 with tests and tuning. It is a new low-precision GEMM path alongside MXFP4.

**[#4903](https://github.com/ROCm/aiter/pull/4903) — OPUS bf16 GEMM (merged)**
Integrates OPUS bf16 GEMM code objects into the JIT/build for gfx1250 (DeepSeek-tagged). It adds a large new GEMM backend path with tuning data.

**[#5088](https://github.com/ROCm/aiter/pull/5088) — Refactor Unified Attention (open)**
A 27k-line in-progress rewrite of the Triton/Gluon unified attention across gfx942/950/1201/1250. Watch it for decode and prefill performance changes.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#5075](https://github.com/ROCm/aiter/pull/5075) gfx1250 microbench sync, a16w16 4 GiB pre-check and error checking
- [#5076](https://github.com/ROCm/aiter/pull/5076) combined gfx1250 microbench
- [#5004](https://github.com/ROCm/aiter/pull/5004) optimize live-window unified-attention decode (open)
- [#5064](https://github.com/ROCm/aiter/pull/5064) RX 9070 XT wave32 split-K Q4 GEMV for gfx1201 (open)
- [#5067](https://github.com/ROCm/aiter/pull/5067) attn_res PEEL prefill path (open)
- [#5027](https://github.com/ROCm/aiter/pull/5027) head_dim 512 and weightless V-norm in the fused qk_norm_rope_cache quant kernel (open)

</details>

<details>
<summary>Kernels & attention (24)</summary>

- [#4926](https://github.com/ROCm/aiter/pull/4926) MLA v4 prefill ASM kernel
- [#5012](https://github.com/ROCm/aiter/pull/5012) DSv4 sparse paged prefill via prebuilt OPUS kernels on gfx1250
- [#4971](https://github.com/ROCm/aiter/pull/4971) gfx950 hd256 FP8 paged-varlen ASM prefill
- [#4874](https://github.com/ROCm/aiter/pull/4874) MHA C++ README update
- [#4964](https://github.com/ROCm/aiter/pull/4964) fix MLA nhead fold for CP round robin
- [#5065](https://github.com/ROCm/aiter/pull/5065) gfx1250 MLA 64nx1 code objects and launch contract
- [#4659](https://github.com/ROCm/aiter/pull/4659) two fused ops for diffusion transformer blocks
- [#4281](https://github.com/ROCm/aiter/pull/4281) TDM deep-prefetch BF16 prefill for qk_norm_rope
- [#5070](https://github.com/ROCm/aiter/pull/5070) qk_norm_rope EP decode optimization for T512
- [#4869](https://github.com/ROCm/aiter/pull/4869) conv2d optimization for RDNA
- [#4748](https://github.com/ROCm/aiter/pull/4748) ASM gemm a_preshuffle=0 f4/f8 gemm, corner-case fixes
- [#4866](https://github.com/ROCm/aiter/pull/4866) move gluon gemm_a8w8 into gfx950 directory
- [#5007](https://github.com/ROCm/aiter/pull/5007) FlyDSL one-stage split-K a8w8 preshuffle GEMM
- [#5029](https://github.com/ROCm/aiter/pull/5029) mxfp8 gemm bench
- [#5066](https://github.com/ROCm/aiter/pull/5066) fused indexer QK preparation for DCP
- [#5024](https://github.com/ROCm/aiter/pull/5024) CK MHA forward tuning scripts (open)
- [#5046](https://github.com/ROCm/aiter/pull/5046) hand-written gfx950 prefill fp8_mqa_logits (open)
- [#5047](https://github.com/ROCm/aiter/pull/5047) hand-written gfx950 decode fp8_paged_mqa_logits (open)
- [#5048](https://github.com/ROCm/aiter/pull/5048) optimized prefill fp8_mqa_logits for H64D128 (open)
- [#5122](https://github.com/ROCm/aiter/pull/5122) DSA page-table transform fused into cooperative top-k (open)
- [#5123](https://github.com/ROCm/aiter/pull/5123) DCP top-k merge (open)
- [#5043](https://github.com/ROCm/aiter/pull/5043) gfx1250 ASM MHA bf16 hd192x128 (open)
- [#5068](https://github.com/ROCm/aiter/pull/5068) gfx1250 a8w8 mxscale BMM scaffold (open)
- [#5041](https://github.com/ROCm/aiter/pull/5041) batched a8w8 mxscale_128 gemm on gfx1250 (open)

</details>

<details>
<summary>MoE & quantization (17)</summary>

- [#4049](https://github.com/ROCm/aiter/pull/4049) Gluon fused dynamic mxfp4 quant MoE sort for gfx1250
- [#4890](https://github.com/ROCm/aiter/pull/4890) 1x32 mxfp4 ASM kernel
- [#4620](https://github.com/ROCm/aiter/pull/4620) tanh-approx GELU for CK XDL 2-stage MoE
- [#5017](https://github.com/ROCm/aiter/pull/5017) gfx942 a16wi4 f32-to-bf16 pack with lshr-16
- [#5015](https://github.com/ROCm/aiter/pull/5015) require GUGU gu_interleave layout in gfx1250 fused_moe
- [#5037](https://github.com/ROCm/aiter/pull/5037) MoE a8w4 cudagraph updates
- [#5033](https://github.com/ROCm/aiter/pull/5033) tune MoE GEMM A8W8
- [#5028](https://github.com/ROCm/aiter/pull/5028) tune MoE GEMM A8W8 blockscale
- [#5052](https://github.com/ROCm/aiter/pull/5052) a4w4 in test_mega_moe
- [#5001](https://github.com/ROCm/aiter/pull/5001) mega_moe fused stage1 and AOT bundles (open)
- [#5009](https://github.com/ROCm/aiter/pull/5009) radix-select top-k for wide ungrouped routers (open)
- [#5059](https://github.com/ROCm/aiter/pull/5059) gfx1201 BF16 G1U1 large-M Triton MoE path (open)
- [#5081](https://github.com/ROCm/aiter/pull/5081) fused SiTUv2 activation and per-token FP8 quant (open)
- [#5002](https://github.com/ROCm/aiter/pull/5002) Qwen3 Next FP8 QKV preparation (open)
- [#5011](https://github.com/ROCm/aiter/pull/5011) FlyDSL TopK (open)
- [#5058](https://github.com/ROCm/aiter/pull/5058) keep SiLU A4W4 FlyDSL routing opt-in (open)
- [#5038](https://github.com/ROCm/aiter/pull/5038) MoE routing optimizations (open)

</details>

<details>
<summary>Tuning configs (14)</summary>

- [#5069](https://github.com/ROCm/aiter/pull/5069) retune GLM-5.2 a8w8 and BF16 GEMMs on gfx950
- [#5060](https://github.com/ROCm/aiter/pull/5060) GLM-5.3 BF16 GEMM configs on gfx950
- [#5078](https://github.com/ROCm/aiter/pull/5078) M=48 for GLM-5.2 a8w8 bpreshuffle
- [#5045](https://github.com/ROCm/aiter/pull/5045) retune GLM5.2 mxfp4 MoE and fix scale-view cache leak
- [#4906](https://github.com/ROCm/aiter/pull/4906) gfx950 FlyDSL fmoe2 CSV update
- [#4554](https://github.com/ROCm/aiter/pull/4554) Qwen3-VL-235B MXFP4 configs on gfx950
- [#5006](https://github.com/ROCm/aiter/pull/5006) fix GLM5 regression config
- [#5072](https://github.com/ROCm/aiter/pull/5072) GLM-5.2 TP4 a8w8 blockscale on gfx942 (open)
- [#5124](https://github.com/ROCm/aiter/pull/5124) Kimi-K3 a8w8 bpreshuffle and bf16 GEMM tunings (open)
- [#5118](https://github.com/ROCm/aiter/pull/5118) Kimi-K3 a16w4 MoE tile retune (open)
- [#5062](https://github.com/ROCm/aiter/pull/5062) CK a8w8 blockscale for Gemma-4-31B (open)
- [#5117](https://github.com/ROCm/aiter/pull/5117) MXFP6 non-temporal-store variants and Flux configs (open)
- [#5014](https://github.com/ROCm/aiter/pull/5014) gfx1250 hardware and DeepSeek-V4 perf suites
- [#5054](https://github.com/ROCm/aiter/pull/5054) gfx1250 sweep pinning and fixes

</details>

<details>
<summary>Triton/Gluon config layout & infra (30)</summary>

- [#4947](https://github.com/ROCm/aiter/pull/4947) unify gluon a8w8 blockscale config resolution
- [#4948](https://github.com/ROCm/aiter/pull/4948) remove legacy flat-layout fallback
- [#5018](https://github.com/ROCm/aiter/pull/5018) nested layout for conv configs
- [#5019](https://github.com/ROCm/aiter/pull/5019) nested layout for attention configs
- [#5020](https://github.com/ROCm/aiter/pull/5020) nested layout for GMM configs
- [#5021](https://github.com/ROCm/aiter/pull/5021) nested layout for MHC configs
- [#5022](https://github.com/ROCm/aiter/pull/5022) nested layout for MOE configs
- [#5061](https://github.com/ROCm/aiter/pull/5061) consolidate ops/triton utils
- [#5085](https://github.com/ROCm/aiter/pull/5085) docs for nested config layout (open)
- [#5092](https://github.com/ROCm/aiter/pull/5092) absolute imports in wrapper layer (open)
- [#5093](https://github.com/ROCm/aiter/pull/5093) categorized import paths for tests and benchmarks (open)
- [#5094](https://github.com/ROCm/aiter/pull/5094) MOE scale layout from shuffle_scale_moe (open)
- [#5095](https://github.com/ROCm/aiter/pull/5095) config-aware repr, GEMM/conv1d (open)
- [#5097](https://github.com/ROCm/aiter/pull/5097) config-aware repr, attention (open)
- [#5098](https://github.com/ROCm/aiter/pull/5098) config-aware repr, MOE/fusion (open)
- [#5099](https://github.com/ROCm/aiter/pull/5099) config-aware repr, rope/norm (open)
- [#5100](https://github.com/ROCm/aiter/pull/5100) config-aware repr, quant (open)
- [#5101](https://github.com/ROCm/aiter/pull/5101) resolve conv configs in launch layer (open)
- [#5102](https://github.com/ROCm/aiter/pull/5102) resolve attention configs in wrapper (open)
- [#5103](https://github.com/ROCm/aiter/pull/5103) resolve fused-GEMM configs in wrapper (open)
- [#5104](https://github.com/ROCm/aiter/pull/5104) resolve batched-GEMM and FF configs in wrapper (open)
- [#5105](https://github.com/ROCm/aiter/pull/5105) resolve basic-GEMM configs in wrapper (open)
- [#5106](https://github.com/ROCm/aiter/pull/5106) sage-attention launch params into config tree (open)
- [#5010](https://github.com/ROCm/aiter/pull/5010) caller-defined padding cache slot in fused MLA writer (open)
- [#5055](https://github.com/ROCm/aiter/pull/5055) gfx12 mxfp8 gemm CGA update (open)
- [#5053](https://github.com/ROCm/aiter/pull/5053) combine routing early exit (open)
- [#5077](https://github.com/ROCm/aiter/pull/5077) revert of GLM 5.x prefill MQA logits tuning (open)
- [#5113](https://github.com/ROCm/aiter/pull/5113) FlyDSL attn-aux cleanup (open)
- [#5112](https://github.com/ROCm/aiter/pull/5112) FlyDSL gfx1250 MoE aux cleanup with UT (open)
- [#5116](https://github.com/ROCm/aiter/pull/5116) remove obsolete availability helpers (open)

</details>

<details>
<summary>Parallelism & scheduling (2)</summary>

- [#4924](https://github.com/ROCm/aiter/pull/4924) fix raw IPC input pools in init_dist_env
- [#5111](https://github.com/ROCm/aiter/pull/5111) reuse comm groups to save memory (open)

</details>

<details>
<summary>Bugfixes (12)</summary>

- [#4965](https://github.com/ROCm/aiter/pull/4965) topk_gating dropped and out-of-range slots
- [#4995](https://github.com/ROCm/aiter/pull/4995) missing XQ scale barrier in a16 FP8-blockscale fmoe kernels
- [#5034](https://github.com/ROCm/aiter/pull/5034) DSV4 FP4 KV-cache scattered row writes
- [#5087](https://github.com/ROCm/aiter/pull/5087) BF16 FMHA extreme negative logits (open)
- [#5090](https://github.com/ROCm/aiter/pull/5090) fwd_decode LSE store in splitK_reduce (open)
- [#5063](https://github.com/ROCm/aiter/pull/5063) BLOCK_M for large prefill with head_size >= 256 (open)
- [#5121](https://github.com/ROCm/aiter/pull/5121) fp8_mqa_logits buffer-op gating on int32 offset (open)
- [#5035](https://github.com/ROCm/aiter/pull/5035) clamp unified_attention 3D config to LDS budget on gfx1201 (open)
- [#5042](https://github.com/ROCm/aiter/pull/5042) radix top-k lambda arity (open)
- [#5096](https://github.com/ROCm/aiter/pull/5096) missing CK 2-stage headers (open)
- [#5089](https://github.com/ROCm/aiter/pull/5089) FLYDSL_GPU_ARCH LDS limit for gfx950 AOT (open)
- [#5120](https://github.com/ROCm/aiter/pull/5120) guard MLA decode output dtype (open)

</details>

<details>
<summary>Tests (7)</summary>

- [#5050](https://github.com/ROCm/aiter/pull/5050) gfx1250 microbench
- [#5082](https://github.com/ROCm/aiter/pull/5082) AITER_BENCH_TOKENS reaches every op
- [#5084](https://github.com/ROCm/aiter/pull/5084) compare opus, asm and triton in sparse-prefill test (open)
- [#5107](https://github.com/ROCm/aiter/pull/5107) gfx1250 auto-detect stepping and B0-only guard (open)
- [#5025](https://github.com/ROCm/aiter/pull/5025) jdbmm backward pass (open)
- [#5083](https://github.com/ROCm/aiter/pull/5083) CI triton release_tmp2 3.8.0, no-e2e (open, do not merge)
- [#5079](https://github.com/ROCm/aiter/pull/5079) CI triton release_tmp2 3.8.0 with GDN block-ptr fix (open, do not merge)

</details>

<details>
<summary>CI & build (8)</summary>

- [#5008](https://github.com/ROCm/aiter/pull/5008) allow multigpu label to trigger tests
- [#5003](https://github.com/ROCm/aiter/pull/5003) skip MegaMoE v2 multi-GPU tests
- [#5071](https://github.com/ROCm/aiter/pull/5071) FFM bringup test on MI250 build runner
- [#4912](https://github.com/ROCm/aiter/pull/4912) bump flydsl to 0.3.2
- [#5057](https://github.com/ROCm/aiter/pull/5057) mirror PR title tags as labels (open)
- [#5110](https://github.com/ROCm/aiter/pull/5110) drop registry credentials after jobs (open)
- [#5109](https://github.com/ROCm/aiter/pull/5109) avoid direct github.event interpolation in run blocks (open)
- [#5073](https://github.com/ROCm/aiter/pull/5073) README update (open, docs)

</details>

<details>
<summary>Docs (1)</summary>

- [#5051](https://github.com/ROCm/aiter/pull/5051) FlyDSL kernel cleanup skill docs

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f6104e8a03db984687866ae709be4601dd540245cd92a96643bc0beae54132da -->
