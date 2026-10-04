# AITER: PR digest (2026-08-30 to 2026-09-03)

_81 merged, 73 newly opened - source ROCm/AITER, generated 2026-09-03T13:17:59Z_

## TL;DR
- **DeepSeek (V4/DSA) and Kimi (K3) got the most attention.** DeepSeek work covers sparse-MLA prefill, fused DSA top-k and a8w8 block-scale GEMM configs. Kimi work is mostly K3 a8w8, bf16 and a16w4 MoE tuning, plus a FlashKDA prefill kernel (open). GLM-5.2 decode TopK and MiniMax-M3 scoring/QK-norm kernels also landed or are in review.
- **Attention and top-k are where the kernel effort went.** Unified attention was refactored (about 25k lines removed). Several open gfx950 unified-attention variants (tile-loop restructure at -12.8% kernel time, tail-split) are in review. FlyDSL radix-select and decode TopK paths merged.
- **gfx1250 bring-up is the largest hardware push.** It is led by the big microbench merge, a FlyDSL FMHA prefill kernel, mega-MoE with fp8/fp4 dispatch wires, and ASM/OPUS GEMM and MLA work. Open PRs add gfx950 split-K decode GEMMs, MXFP6 GEMMs, gfx1201 int4 a16w4, and MI300A enablement.
- **Direction:** FlyDSL and Gluon kernels are replacing older paths. Triton wrappers are being cleaned up (config-aware `repr`, absolute imports). Release and CI hardening continues, including a v0.1.21 cherry-pick.

## Most important PRs
**[#5239](https://github.com/ROCm/aiter/pull/5239) Gfx1250/microbench**
A huge gfx1250 merge (about 60k lines churned) with microbenchmarks across attention, MLA, MoE, GEMM, quant and communication kernels. It establishes the performance baseline for the new architecture.

**[#5185](https://github.com/ROCm/aiter/pull/5185) Unified attention refactor**
Removes about 25k lines from the Triton/Gluon unified-attention path while keeping gfx942, gfx950, gfx1201 and gfx1250 support. It is the base for the open gfx950 prefill-pipelining PRs.

**[#5173](https://github.com/ROCm/aiter/pull/5173) FlyDSL decode TopK path for GLM-5.2**
Adds a FlyDSL decode TopK path for GLM-5.2, building on the radix-select TopK path in [#5011](https://github.com/ROCm/aiter/pull/5011). Together they speed up sparse-attention index selection at decode.

**[#4787](https://github.com/ROCm/aiter/pull/4787) Minimax M3 scoring and top-k kernels**
Adds optimized JIT HIP kernels for MiniMax-M3 scoring and top-k on gfx950. [#5143](https://github.com/ROCm/aiter/pull/5143) follows with an extended fused QK-norm for the same model.

**[#4984](https://github.com/ROCm/aiter/pull/4984) mega_moe on gfx1250 with quantize-before-dispatch**
Quantizes before dispatch, so the all-to-all moves an fp8 or fp4 wire instead of bf16. This cuts communication volume for expert-parallel MoE.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#5178](https://github.com/ROCm/aiter/pull/5178) avoid zero-initializing the MoE stage1 scale workspace
- [#5027](https://github.com/ROCm/aiter/pull/5027) add head_dim 512 and weightless V-norm to the fused QK-norm/rope/cache/quant kernel
- [#5137](https://github.com/ROCm/aiter/pull/5137) tune A16W16 GEMM with amdgpu-trackers disabled
- [#5111](https://github.com/ROCm/aiter/pull/5111) reuse comm groups to save memory

</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#4712](https://github.com/ROCm/aiter/pull/4712) fused KDA decode kernel (conv1d, recurrence, gated RMSNorm)
- [#5081](https://github.com/ROCm/aiter/pull/5081) fused SiTUv2 activation with per-token FP8 quant
- [#3937](https://github.com/ROCm/aiter/pull/3937) Gluon MXFP4 fused reduce-quant
- [#5113](https://github.com/ROCm/aiter/pull/5113) FlyDSL attention-aux kernel cleanup
- [#5112](https://github.com/ROCm/aiter/pull/5112) FlyDSL MoE aux kernel cleanup, adds unit tests
- [#5041](https://github.com/ROCm/aiter/pull/5041) batched a8w8 mxscale_128 GEMM on gfx1250
- [#5123](https://github.com/ROCm/aiter/pull/5123) DCP top-k merge
- [#5171](https://github.com/ROCm/aiter/pull/5171) GLM-5.2 GCP dev kernels
- [#4958](https://github.com/ROCm/aiter/pull/4958) make aiter_opus_plus.h torch-free, plus mha_v4_quant
- [#5088](https://github.com/ROCm/aiter/pull/5088) Triton/Gluon unified-attention refactor
- [#5106](https://github.com/ROCm/aiter/pull/5106) sage-attention launch params moved into the config tree
- [#5121](https://github.com/ROCm/aiter/pull/5121) fp8_mqa_logits buffer-ops gating fix
- [#5053](https://github.com/ROCm/aiter/pull/5053) combine routing early exit

</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#4617](https://github.com/ROCm/aiter/pull/4617) fused_moe accepts a caller-provided output buffer
- [#5130](https://github.com/ROCm/aiter/pull/5130) moe2 layout rm nkpad
- [#5118](https://github.com/ROCm/aiter/pull/5118) retune Kimi-K3 a16w4 MoE tile geometry
- [#5094](https://github.com/ROCm/aiter/pull/5094) take MOE scale layout from shuffle_scale_moe
- [#5189](https://github.com/ROCm/aiter/pull/5189) moe_gemm_a4w4 num_warps 8 to 4 for block_m != 16
- [#4994](https://github.com/ROCm/aiter/pull/4994) fuse stage-1 fp8 quant on the FlyDSL fallback (DSV4)
- [#5227](https://github.com/ROCm/aiter/pull/5227) revert of [#4994](https://github.com/ROCm/aiter/pull/4994)

</details>

<details>
<summary>Tuning configs (4)</summary>

- [#5197](https://github.com/ROCm/aiter/pull/5197) tune a8w8 GEMM with 64-step M for Kimi-K3
- [#5124](https://github.com/ROCm/aiter/pull/5124) tune Kimi-K3 a8w8 bpreshuffle and bf16 GEMM shapes
- [#5139](https://github.com/ROCm/aiter/pull/5139) fill remaining Kimi-K3 bf16 GEMM shapes
- [#5147](https://github.com/ROCm/aiter/pull/5147) sweep the fp4 dispatch wire in mori_ep

</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#5169](https://github.com/ROCm/aiter/pull/5169) fix topk_per_row compile on gfx1250
- [#5170](https://github.com/ROCm/aiter/pull/5170) sparse-prefill UT follow-up, mla_v4_prefill raised to 16384
- [#5180](https://github.com/ROCm/aiter/pull/5180) stop children shelling out to rocminfo on gfx1250
- [#5248](https://github.com/ROCm/aiter/pull/5248) mega MoE data init and warmup test

</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

- [#5212](https://github.com/ROCm/aiter/pull/5212) scale the auto KV-split count with machine width in MLA metadata

</details>

<details>
<summary>API & serving (3)</summary>

- [#5098](https://github.com/ROCm/aiter/pull/5098) config-aware repr for MOE and fusion kernels
- [#5097](https://github.com/ROCm/aiter/pull/5097) config-aware repr for attention kernels
- [#5095](https://github.com/ROCm/aiter/pull/5095) config-aware repr for GEMM and conv1d kernels
- plus [#5099](https://github.com/ROCm/aiter/pull/5099), [#5100](https://github.com/ROCm/aiter/pull/5100) and [#5154](https://github.com/ROCm/aiter/pull/5154) adding the same `repr` to rope, norm, quant and DiT kernels

</details>

<details>
<summary>Bugfixes (7)</summary>

- [#5202](https://github.com/ROCm/aiter/pull/5202) make `_fold_seqlen_indptr` cudagraph-safe
- [#5222](https://github.com/ROCm/aiter/pull/5222) v0.1.21 cherry-pick of [#5202](https://github.com/ROCm/aiter/pull/5202)
- [#4841](https://github.com/ROCm/aiter/pull/4841) acquire fence for the mb radix barrier last block
- [#5136](https://github.com/ROCm/aiter/pull/5136) clamp the split-K heuristic against divide-by-zero
- [#5210](https://github.com/ROCm/aiter/pull/5210) fix stale TopK availability checks
- [#4950](https://github.com/ROCm/aiter/pull/4950) gated_delta_rule: drop removed tl.make_block_ptr
- [#5215](https://github.com/ROCm/aiter/pull/5215) relax GDR decode test mismatch tolerance

</details>

<details>
<summary>Refactors (6)</summary>

- [#5149](https://github.com/ROCm/aiter/pull/5149) revert Triton parts of [#4978](https://github.com/ROCm/aiter/pull/4978)
- [#4978](https://github.com/ROCm/aiter/pull/4978) Dev lumen (Triton/Gluon/HIP)
- [#5116](https://github.com/ROCm/aiter/pull/5116) remove obsolete availability helpers
- [#5092](https://github.com/ROCm/aiter/pull/5092) absolute imports in the wrapper layer
- [#5093](https://github.com/ROCm/aiter/pull/5093) import tests and benchmarks through categorized paths
- [#5085](https://github.com/ROCm/aiter/pull/5085) docs for the single nested config layout

</details>

<details>
<summary>Tests (11)</summary>

- [#5142](https://github.com/ROCm/aiter/pull/5142) kernel PR validation and structural D9 scanning
- [#5174](https://github.com/ROCm/aiter/pull/5174) validator no longer reports coverage it did not obtain
- [#5084](https://github.com/ROCm/aiter/pull/5084) compare opus, asm and triton in the sparse-prefill test
- [#5241](https://github.com/ROCm/aiter/pull/5241) gfx1250 attention/MLA microbench
- [#5252](https://github.com/ROCm/aiter/pull/5252) GEMM ubench
- [#5251](https://github.com/ROCm/aiter/pull/5251) ASM GEMM microbench for gfx1250
- [#5250](https://github.com/ROCm/aiter/pull/5250) opus GEMM benchmark update
- [#5245](https://github.com/ROCm/aiter/pull/5245) data-init for test_mhc
- [#5253](https://github.com/ROCm/aiter/pull/5253) data-init for the qk_norm_rope_quant test
- [#4458](https://github.com/ROCm/aiter/pull/4458) extended test workflow
- [#5209](https://github.com/ROCm/aiter/pull/5209) extended tests client_payload change

</details>

<details>
<summary>CI & build (11)</summary>

- [#4424](https://github.com/ROCm/aiter/pull/4424) document and automate the release plan
- [#5057](https://github.com/ROCm/aiter/pull/5057) mirror PR title tags as labels
- [#5152](https://github.com/ROCm/aiter/pull/5152) bump triton to 3.8.0
- [#5110](https://github.com/ROCm/aiter/pull/5110) drop registry credentials after jobs on persistent runners
- [#5109](https://github.com/ROCm/aiter/pull/5109) avoid direct github.event interpolation in run blocks
- [#5198](https://github.com/ROCm/aiter/pull/5198) app token for release refs
- [#5201](https://github.com/ROCm/aiter/pull/5201) respect docker login input in release builds
- [#5204](https://github.com/ROCm/aiter/pull/5204) set release publish repository context
- [#5205](https://github.com/ROCm/aiter/pull/5205) run extended test dispatch on internal runner
- [#5134](https://github.com/ROCm/aiter/pull/5134) fix PR title tag workflow syntax
- [#5073](https://github.com/ROCm/aiter/pull/5073) README update

</details>

<details>
<summary>Open PRs: new kernels and GEMM (in progress, 20)</summary>

- [#5140](https://github.com/ROCm/aiter/pull/5140) optimized FlashKDA prefill kernels for gfx950 (Kimi)
- [#5145](https://github.com/ROCm/aiter/pull/5145) refactor gfx950 A16W16 GEMM with centralized policy selection
- [#5148](https://github.com/ROCm/aiter/pull/5148) FlyDSL split-K preshuffle decode GEMM for small M (FP8 and MX)
- [#5168](https://github.com/ROCm/aiter/pull/5168) FlyDSL FMHA forward-prefill for gfx1250
- [#5172](https://github.com/ROCm/aiter/pull/5172) duplicate of the GLM-5.2 decode TopK path
- [#5150](https://github.com/ROCm/aiter/pull/5150) fused MoE routing preamble for MXFP4 decode
- [#5224](https://github.com/ROCm/aiter/pull/5224) int4 a16w4 GEMM for gfx1201
- [#5141](https://github.com/ROCm/aiter/pull/5141) FlyDSL fp8 block-scale GEMM for Qwen3.6-27B prefill
- [#5122](https://github.com/ROCm/aiter/pull/5122) fuse DSA page-table transform into a cooperative top-k
- [#5167](https://github.com/ROCm/aiter/pull/5167) gfx950 DSV4 FlyDSL sparse-MLA prefill
- [#5207](https://github.com/ROCm/aiter/pull/5207) FlyDSL gather-gemm for a8w8
- [#5153](https://github.com/ROCm/aiter/pull/5153) Gluon MHA for gfx950
- [#5158](https://github.com/ROCm/aiter/pull/5158) unified_attention 2-D prefill unmasked bulk plus masked tail
- [#5157](https://github.com/ROCm/aiter/pull/5157) unified_attention straggler split
- [#5216](https://github.com/ROCm/aiter/pull/5216) optimize FP8 MQA logits on MI350
- [#5223](https://github.com/ROCm/aiter/pull/5223) OPUS bf16 flash-attn with head dim 64 and sinks
- [#5190](https://github.com/ROCm/aiter/pull/5190) gfx950 asm MTP-verify attention
- [#5138](https://github.com/ROCm/aiter/pull/5138), [#5236](https://github.com/ROCm/aiter/pull/5236) and [#5117](https://github.com/ROCm/aiter/pull/5117) MXFP6 GEMM variants
- [#5176](https://github.com/ROCm/aiter/pull/5176) fp8/fp4 quant in mega stage2 combine
- [#5235](https://github.com/ROCm/aiter/pull/5235) fused stage2 for MoE

</details>

<details>
<summary>Open PRs: configs, fixes and misc (in progress, 40)</summary>

- [#5246](https://github.com/ROCm/aiter/pull/5246) Conv2D configs for gfx1101 and gfx1150
- [#5217](https://github.com/ROCm/aiter/pull/5217) tuned DSV4 A8W8 block-scale GEMM configs and RDNA3 fp8 e4m3 fix
- [#5219](https://github.com/ROCm/aiter/pull/5219) DSv4 TP8 a8w8 blockscale rows for gfx950
- [#5213](https://github.com/ROCm/aiter/pull/5213) and [#5183](https://github.com/ROCm/aiter/pull/5183) Qwen3.8 tuned configs
- [#5144](https://github.com/ROCm/aiter/pull/5144) GLM5.2 FP8 MoE tuning
- [#5155](https://github.com/ROCm/aiter/pull/5155) Qwen3-VL MXFP4 MoE atomic stage2
- [#5159](https://github.com/ROCm/aiter/pull/5159) drop losing gptoss large-M QKV rows
- [#5200](https://github.com/ROCm/aiter/pull/5200) PA decode config JSON
- [#5186](https://github.com/ROCm/aiter/pull/5186) MI300A enablement
- [#5242](https://github.com/ROCm/aiter/pull/5242) WIP TP MOE fusion
- [#5164](https://github.com/ROCm/aiter/pull/5164) simplify compiler worker fan-out
- [#5254](https://github.com/ROCm/aiter/pull/5254) group delta-rule ops under linear_attention
- [#5132](https://github.com/ROCm/aiter/pull/5132) post-merge fixes for dev-lumen cherry-pick
- [#5232](https://github.com/ROCm/aiter/pull/5232) do not route MXFP4 MoE to CK-Tile when inter_dim % 256 != 0
- [#5206](https://github.com/ROCm/aiter/pull/5206) fall back to cktile when the ck bpreshuffle instance rejects a shape
- [#5175](https://github.com/ROCm/aiter/pull/5175) triton 3.8 rmsnorm regression fix
- [#5211](https://github.com/ROCm/aiter/pull/5211) mark bf16 mla_pfl prefill as causal
- [#5162](https://github.com/ROCm/aiter/pull/5162) gfx1250 split-K guard
- [#5191](https://github.com/ROCm/aiter/pull/5191), [#5120](https://github.com/ROCm/aiter/pull/5120), [#5220](https://github.com/ROCm/aiter/pull/5220), [#5255](https://github.com/ROCm/aiter/pull/5255), [#5126](https://github.com/ROCm/aiter/pull/5126) and [#5194](https://github.com/ROCm/aiter/pull/5194) small safety, dtype and caching fixes
- [#5165](https://github.com/ROCm/aiter/pull/5165), [#5203](https://github.com/ROCm/aiter/pull/5203), [#5177](https://github.com/ROCm/aiter/pull/5177), [#5188](https://github.com/ROCm/aiter/pull/5188), [#5230](https://github.com/ROCm/aiter/pull/5230), [#5199](https://github.com/ROCm/aiter/pull/5199), [#5249](https://github.com/ROCm/aiter/pull/5249) and [#5214](https://github.com/ROCm/aiter/pull/5214) new Triton/Gluon and HIP kernels or fixes
- [#5129](https://github.com/ROCm/aiter/pull/5129), [#5146](https://github.com/ROCm/aiter/pull/5146), [#5182](https://github.com/ROCm/aiter/pull/5182), [#5221](https://github.com/ROCm/aiter/pull/5221), [#5240](https://github.com/ROCm/aiter/pull/5240), [#5195](https://github.com/ROCm/aiter/pull/5195), [#5196](https://github.com/ROCm/aiter/pull/5196), [#5226](https://github.com/ROCm/aiter/pull/5226), [#5228](https://github.com/ROCm/aiter/pull/5228) and [#5127](https://github.com/ROCm/aiter/pull/5127) other kernel, refactor and JIT work
- [#5179](https://github.com/ROCm/aiter/pull/5179), [#5244](https://github.com/ROCm/aiter/pull/5244), [#5237](https://github.com/ROCm/aiter/pull/5237), [#5218](https://github.com/ROCm/aiter/pull/5218), [#5163](https://github.com/ROCm/aiter/pull/5163), [#5166](https://github.com/ROCm/aiter/pull/5166), [#5131](https://github.com/ROCm/aiter/pull/5131) and [#5208](https://github.com/ROCm/aiter/pull/5208) benchmarks, test-data init and CI plumbing

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 639c4e6166412a701049ce926a8e04a534f17819136353eb96c74c6053c48d22 -->
