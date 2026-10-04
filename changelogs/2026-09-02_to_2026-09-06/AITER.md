# AITER: PR digest (2026-09-02 to 2026-09-06)

_55 merged, 56 newly opened - source ROCm/AITER, generated 2026-09-06T22:47:09Z_

## TL;DR
- **DeepSeek (V4) got the most attention**, followed by Kimi, GLM and MiniMax. The work was mostly gfx950 and gfx1250 tuning: A8W8 blockscale bpreshuffle GEMM configs, FP4 MQA-logits kernels, and MoE fixes. Kimi-K3 a16w4 MoE tiles were retuned.
- **Biggest merged performance work:** the gfx950 A16W16 FlyDSL GEMM refactor with centralized policy selection (`[#5145](https://github.com/ROCm/aiter/pull/5145)`), a FlyDSL FMHA prefill kernel for gfx1250 (`[#5168](https://github.com/ROCm/aiter/pull/5168)`), and a faster FP4 MQA-logits schedule build (`[#5276](https://github.com/ROCm/aiter/pull/5276)`).
- **gfx1250 is being brought up quickly.** The big microbench landing (`[#5239](https://github.com/ROCm/aiter/pull/5239)`) plus several ubench follow-ups came in, and open PRs add per-group quant, once-per-token MoE quantization, and narrow-head MLA sparse-prefill.
- **Open work leans toward new kernels and correctness.** Examples are a FlyDSL a8w8 gather-gemm, MXFP8 convert kernels, a gfx1201 int4 a16w4 GEMM, an FP4 streaming TopK prototype, and several invalid-expert-ID and index-dtype guards in MoE.
- **Overall direction:** FlyDSL and Gluon are replacing legacy paths. Config trees and reprs are being cleaned up, and testing and validation tooling is growing (data-init, JSON summaries, kernel-PR validators).

## Most important PRs
**[#5145](https://github.com/ROCm/aiter/pull/5145) - Refactor gfx950 A16W16 FlyDSL GEMM with centralized policy selection and tuning**
Moves kernel and tile selection for the A16W16 GEMM into one policy layer with tuned configs. This covers the shapes used by the DeepSeek, Kimi, GLM, MiniMax, Qwen, gpt-oss and Llama families.

**[#5168](https://github.com/ROCm/aiter/pull/5168) - FlyDSL FMHA forward-prefill A16W16 kernel for gfx1250**
Adds `fmha_fwd_prefill_m32x8`, a native FlyDSL prefill attention kernel for gfx1250, with CI coverage. It is the main attention path for the new arch.

**[#5239](https://github.com/ROCm/aiter/pull/5239) - Gfx1250/microbench**
A very large change (about 400 files) that lays down the gfx1250 microbenchmark infrastructure across attention, MLA, MoE, GEMM, quant, norm and communication. DeepSeek, GLM and Kimi shapes are covered. It is the baseline for the later ubench PRs.

**[#5088](https://github.com/ROCm/aiter/pull/5088) - Refactor Unified Attention (Triton/Gluon)**
Restructures the unified attention kernels across gfx942, gfx950, gfx1201 and gfx1250, with tests and tuning configs. This sets up a common attention path for several archs.

**[#5011](https://github.com/ROCm/aiter/pull/5011) - FlyDSL Radix-Select TopK path for per-row decode**
Adds a radix-select TopK implementation behind the existing per-row decode interface. It is used for sparse attention index selection.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#5276](https://github.com/ROCm/aiter/pull/5276) build the FP4 MQA-logits prefill schedule in one FlyDSL kernel instead of 25 torch ops
- [#5285](https://github.com/ROCm/aiter/pull/5285) bound the FP4 MQA-logits store with a window-sized V# instead of a compare (DSv4)
- [#5212](https://github.com/ROCm/aiter/pull/5212) scale the MLA auto KV-split count with the machine width
- [#5111](https://github.com/ROCm/aiter/pull/5111) reuse comm groups to save memory

</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#5081](https://github.com/ROCm/aiter/pull/5081) fused SiTUv2 activation + per-token FP8 quant HIP kernel
- [#4712](https://github.com/ROCm/aiter/pull/4712) fused KDA decode kernel (conv1d + recurrence + gated RMSNorm)
- [#5143](https://github.com/ROCm/aiter/pull/5143) extend fused QK norm for MiniMax-M3
- [#5123](https://github.com/ROCm/aiter/pull/5123) DCP TopK merge (HIP/FlyDSL)
- [#5241](https://github.com/ROCm/aiter/pull/5241) gfx1250 attention/MLA microbench
- [#5258](https://github.com/ROCm/aiter/pull/5258) complete DSv4 attention data-init on gfx1250
- [#5106](https://github.com/ROCm/aiter/pull/5106) move sage-attention launch params into the config tree
- [#5215](https://github.com/ROCm/aiter/pull/5215) relax GDR decode test mismatch tolerance

</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#4500](https://github.com/ROCm/aiter/pull/4500) EP MoE changes for gfx9 and gfx12 (Triton/Gluon)
- [#5118](https://github.com/ROCm/aiter/pull/5118) retune Kimi-K3 a16w4 MoE tile geometry
- [#4839](https://github.com/ROCm/aiter/pull/4839) guard against negative expert IDs in MoE sorting
- [#5189](https://github.com/ROCm/aiter/pull/5189) `moe_gemm_a4w4` num_warps 8 to 4 for block_m != 16
- [#4994](https://github.com/ROCm/aiter/pull/4994) fuse stage-1 fp8 quant on the heuristic FlyDSL fallback (DSV4)
- [#5227](https://github.com/ROCm/aiter/pull/5227) revert [#4994](https://github.com/ROCm/aiter/pull/4994)
- [#5248](https://github.com/ROCm/aiter/pull/5248) mega-MoE data init and warmup test

</details>

<details>
<summary>Tuning configs (6)</summary>

- [#5197](https://github.com/ROCm/aiter/pull/5197) a8w8 GEMM tuning with 64-step M for Kimi K3
- [#5283](https://github.com/ROCm/aiter/pull/5283) DSv4 gfx950 FP8 blockscale bpreshuffle for wq_b and wqkv_a
- [#5281](https://github.com/ROCm/aiter/pull/5281) GLM-5.2 a8w8-bpreshuffle rows for live-engine shapes
- [#5284](https://github.com/ROCm/aiter/pull/5284) add M=512 to the DSv4 A8W8 blockscale sweep
- [#5100](https://github.com/ROCm/aiter/pull/5100) config-aware repr for the quant kernels
- [#5099](https://github.com/ROCm/aiter/pull/5099) config-aware repr for the rope and normalization kernels

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#5252](https://github.com/ROCm/aiter/pull/5252) gfx1250 GEMM ubench
- [#5251](https://github.com/ROCm/aiter/pull/5251) gfx1250 ASM GEMM microbench
- [#5257](https://github.com/ROCm/aiter/pull/5257) ubench init controls and SMI monitor
- [#5288](https://github.com/ROCm/aiter/pull/5288) emit ubench summaries as JSON
- [#5291](https://github.com/ROCm/aiter/pull/5291) scope the amdsmi import to the SMI monitor

</details>

<details>
<summary>Tests (7)</summary>

- [#5142](https://github.com/ROCm/aiter/pull/5142) kernel PR validation and structural D9 scanning
- [#5174](https://github.com/ROCm/aiter/pull/5174) rebase the validator onto [#5142](https://github.com/ROCm/aiter/pull/5142) and stop it reporting coverage it did not obtain
- [#5287](https://github.com/ROCm/aiter/pull/5287) rewrite gfx950 HGEMM test to op_test standard
- [#5250](https://github.com/ROCm/aiter/pull/5250) Opus GEMM benchmark update
- [#5245](https://github.com/ROCm/aiter/pull/5245) data-init for `test_mhc`
- [#5253](https://github.com/ROCm/aiter/pull/5253) data-init options for the `qk_norm_rope_quant` test
- [#5154](https://github.com/ROCm/aiter/pull/5154) repr for DiT fused kernels and `round_intermediate` test coverage

</details>

<details>
<summary>CI & build (9)</summary>

- [#5152](https://github.com/ROCm/aiter/pull/5152) bump Triton to 3.8.0
- [#4458](https://github.com/ROCm/aiter/pull/4458) extended test workflow
- [#5198](https://github.com/ROCm/aiter/pull/5198) app token for release refs
- [#5201](https://github.com/ROCm/aiter/pull/5201) respect docker login input in release builds
- [#5204](https://github.com/ROCm/aiter/pull/5204) set release publish repository context
- [#5205](https://github.com/ROCm/aiter/pull/5205) run extended test dispatch on the internal runner
- [#5209](https://github.com/ROCm/aiter/pull/5209) extended tests client_payload change
- [#5222](https://github.com/ROCm/aiter/pull/5222) v0.1.21 cherry-pick of the cudagraph-safe `_fold_seqlen_indptr` fix
- [#5116](https://github.com/ROCm/aiter/pull/5116) remove obsolete availability helpers

</details>

<details>
<summary>Docs (2)</summary>

- [#5085](https://github.com/ROCm/aiter/pull/5085) docs for the single nested config layout
- [#5073](https://github.com/ROCm/aiter/pull/5073) README update

</details>

<details>
<summary>Bugfixes (2)</summary>

- [#5202](https://github.com/ROCm/aiter/pull/5202) make `_fold_seqlen_indptr` cudagraph-safe (avoid scalar H2D copy)
- [#5210](https://github.com/ROCm/aiter/pull/5210) fix stale TopK availability checks

</details>

<details>
<summary>Newly opened: kernels & attention (11)</summary>

- [#5282](https://github.com/ROCm/aiter/pull/5282) prototype FP4 MQA streaming TopK (DSv4, FlyDSL)
- [#5230](https://github.com/ROCm/aiter/pull/5230) 3D neighborhood flash attention (`na3d_flash`)
- [#5223](https://github.com/ROCm/aiter/pull/5223) OPUS bf16 flash-attn: head dim 64, sinks, single-seq varlen (gfx950)
- [#5216](https://github.com/ROCm/aiter/pull/5216) optimize FP8 MQA logits kernel on MI350
- [#5294](https://github.com/ROCm/aiter/pull/5294) `pa_decode_sparse`: pick BLOCK_K by occupancy (up to +43%)
- [#5196](https://github.com/ROCm/aiter/pull/5196) MLA v4 ASM for gfx1250
- [#5195](https://github.com/ROCm/aiter/pull/5195) swap the gfx950 MLA v4 ASM decode kernel
- [#5228](https://github.com/ROCm/aiter/pull/5228) narrow-head MLA sparse-prefill for DSv4 TP (gfx1250)
- [#5199](https://github.com/ROCm/aiter/pull/5199) wave32 for `chunk_gated_delta_rule_fwd_h` (WIP)
- [#5254](https://github.com/ROCm/aiter/pull/5254) group delta-rule ops under a `linear_attention` family
- [#5249](https://github.com/ROCm/aiter/pull/5249) `chunk_kimi_delta_attn` accepts a non-fp32 KDA state

</details>

<details>
<summary>Newly opened: MoE, GEMM & quantization (14)</summary>

- [#5242](https://github.com/ROCm/aiter/pull/5242) TP MoE fusion (WIP)
- [#5207](https://github.com/ROCm/aiter/pull/5207) FlyDSL a8w8 gather-gemm
- [#5235](https://github.com/ROCm/aiter/pull/5235) inter fused stage2 (Kimi, gfx950)
- [#5274](https://github.com/ROCm/aiter/pull/5274) quantize each MoE source token once instead of once per route (gfx1250)
- [#5232](https://github.com/ROCm/aiter/pull/5232) don't route MXFP4 MoE to CK-Tile when inter_dim % 256 != 0
- [#5240](https://github.com/ROCm/aiter/pull/5240) opt-in a16wi4 gemm2 CShuffle epilog
- [#5224](https://github.com/ROCm/aiter/pull/5224) int4 a16w4 GEMM for gfx1201
- [#5203](https://github.com/ROCm/aiter/pull/5203) MXFP8 convert and fast-transpose kernels
- [#5236](https://github.com/ROCm/aiter/pull/5236) fold optional bias into the A6W6 MXFP6 GEMM epilogue
- [#5280](https://github.com/ROCm/aiter/pull/5280) `rowcol_wp_v2` selectable for cktile a8w8-bpreshuffle
- [#5273](https://github.com/ROCm/aiter/pull/5273) gfx1250 per-group quant
- [#5226](https://github.com/ROCm/aiter/pull/5226) `fused_qk_norm_rope_group_quant` opt for gfx1250
- [#5259](https://github.com/ROCm/aiter/pull/5259) clean up MoE elementwise kernels
- [#5221](https://github.com/ROCm/aiter/pull/5221) expose `fused_moe` activation dtype resolution

</details>

<details>
<summary>Newly opened: tuning configs (11)</summary>

- [#5213](https://github.com/ROCm/aiter/pull/5213) FP8 PTPC and BF16 MoE for Qwen3.8-Flash-Next
- [#5219](https://github.com/ROCm/aiter/pull/5219) DSv4 TP8 a8w8 blockscale rows (gfx950)
- [#5279](https://github.com/ROCm/aiter/pull/5279) DSv4 wo_b/wq_b a8w8 blockscale configs
- [#5278](https://github.com/ROCm/aiter/pull/5278) GLM-5.3 a8w8_blockscale tunings (13-61% on low M)
- [#5260](https://github.com/ROCm/aiter/pull/5260) GLM-5.2 BF16 decode GEMM configs (N=6144)
- [#5275](https://github.com/ROCm/aiter/pull/5275) bf16 MoE for K2 horizon 375B
- [#5217](https://github.com/ROCm/aiter/pull/5217) DSV4 A8W8 block-scale configs and RDNA3 fp8 e4m3 dtype fix
- [#5246](https://github.com/ROCm/aiter/pull/5246) Conv2D configs for gfx1101 and gfx1150
- [#5200](https://github.com/ROCm/aiter/pull/5200) PA decode config JSON
- [#5268](https://github.com/ROCm/aiter/pull/5268) record untuned shapes for every GEMM family
- [#5262](https://github.com/ROCm/aiter/pull/5262) tuner builds the result frame once

</details>

<details>
<summary>Newly opened: bugfixes (9)</summary>

- [#5295](https://github.com/ROCm/aiter/pull/5295) skip invalid expert IDs in MoE sorting
- [#5255](https://github.com/ROCm/aiter/pull/5255) reject non-int32 index buffers in the topk kernels
- [#5271](https://github.com/ROCm/aiter/pull/5271) stop the mega_moe reference clamping SwiGLU at swiglu_limit=0
- [#5290](https://github.com/ROCm/aiter/pull/5290) fix `rmsnorm_quant` cross-row reads and writes
- [#5297](https://github.com/ROCm/aiter/pull/5297) route `asm_mla` ctypes failures through the error bridge
- [#5211](https://github.com/ROCm/aiter/pull/5211) mark bf16 `mla_pfl` prefill as causal
- [#5261](https://github.com/ROCm/aiter/pull/5261) split-K OOB fix for afp4wfp4
- [#5220](https://github.com/ROCm/aiter/pull/5220) `pa_sparse_prefill` addresses out with its own strides
- [#5206](https://github.com/ROCm/aiter/pull/5206) fall back to cktile when the CK bpreshuffle instance rejects a shape

</details>

<details>
<summary>Newly opened: other (7)</summary>

- [#5289](https://github.com/ROCm/aiter/pull/5289) review-pr gates and evidence
- [#5269](https://github.com/ROCm/aiter/pull/5269) JIT baton liveness fix under `--network host`
- [#5272](https://github.com/ROCm/aiter/pull/5272) LL and LL128 protocols for gfx9
- [#5194](https://github.com/ROCm/aiter/pull/5194) cache the MLA split count instead of the split indptr tensor
- [#5296](https://github.com/ROCm/aiter/pull/5296) cap the split-k partial-reduction width in `mhc_pre_big_fuse`
- [#5270](https://github.com/ROCm/aiter/pull/5270) fix the default batch size silently disabling tuner checkpointing
- [#5244](https://github.com/ROCm/aiter/pull/5244) FlyDSL GEMM ubench
- [#5237](https://github.com/ROCm/aiter/pull/5237) `test_common` data generation
- [#5218](https://github.com/ROCm/aiter/pull/5218) torch-profiler benchmarking utility
- [#5214](https://github.com/ROCm/aiter/pull/5214) MLA decode kernel name prefix
- [#5208](https://github.com/ROCm/aiter/pull/5208) DO NOT MERGE: extended CI dispatch test

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 05be40796a05825db8f3eed2e90e0d002968da788b4e49e567036d05e6d5bd37 -->
