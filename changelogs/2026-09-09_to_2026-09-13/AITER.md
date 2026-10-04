# AITER: PR digest (2026-09-09 to 2026-09-13)

_72 merged, 70 newly opened - source ROCm/AITER, generated 2026-09-13T22:59:49Z_

## TL;DR
- **Model attention:** DeepSeek (V4 / DSv4, 13 labels) and Kimi (K3, 10) led the window. GLM-5.x, Qwen3.8-Flash-Next and MiniMax-M3 followed, mostly through tuned GEMM/MoE configs and MXFP4/A16W4 MoE paths.
- **Biggest perf work:** FlyDSL is the main vehicle: FP8 flash attention ([#5326](https://github.com/ROCm/aiter/pull/5326)), a MXFP4 GEMM1 replacement extended to A4W4 ([#4526](https://github.com/ROCm/aiter/pull/4526)) and low-M MXFP4 fused-MoE tuning ([#5300](https://github.com/ROCm/aiter/pull/5300)). The Triton/Gluon MHA v4 ([#5335](https://github.com/ROCm/aiter/pull/5335)) and the FP8 MQA logits kernel ([#5216](https://github.com/ROCm/aiter/pull/5216)) are the main attention wins.
- **gfx1250 ramp-up:** 24 labels. It covers MLA sparse-prefill for DSv4, grouped-MoE epilogue speedups, fused QK-norm-rope-quant, and a mega-MoE TDM dispatch (opened).
- **Direction:** Linear-attention (GDN MTP) kernels for Qwen, FlyDSL consolidation, and a lot of per-model tuning configs. Many newly opened PRs are about test hygiene and CI-enforced no-runtime-autotune.

## Most important PRs
**[#4907](https://github.com/ROCm/aiter/pull/4907) - GDN MTP kernels (causal conv1d update + gated delta rule)**
Adds Triton/Gluon/FlyDSL kernels for multi-token-prediction decode in gated-delta-net models. This is the largest merged change, and it includes CI and test wiring.

**[#5326](https://github.com/ROCm/aiter/pull/5326) - FlyDSL FP8 flash attention**
Adds FP8 FMHA on gfx950 covering dense, asymmetric head dims, varlen and KV-split. A follow-up fixes an all-masked-tile NaN ([#5364](https://github.com/ROCm/aiter/pull/5364)).

**[#5335](https://github.com/ROCm/aiter/pull/5335) - MHA v4 refactor and new kernel**
Reworks the Triton/Gluon/ASM/HIP MHA path on gfx950 with a new kernel, fixes and perf tweaks across 28 files.

**[#4526](https://github.com/ROCm/aiter/pull/4526) - MXFP4 GEMM1 replacement extended to A4W4**
Brings the FlyDSL MoE GEMM1 path to A4W4, targeting GLM and Kimi MoE.

**[#5346](https://github.com/ROCm/aiter/pull/5346) - FlyDSL Megamoe AOT fix**
Restores the 5001 ahead-of-time path for mega-MoE (fused comm and MoE).

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#5313](https://github.com/ROCm/aiter/pull/5313) gfx1250 grouped-MoE route, quant and gather-reduce epilogue speedups
- [#5226](https://github.com/ROCm/aiter/pull/5226) fused_qk_norm_rope_group_quant optimization on gfx1250
- [#5448](https://github.com/ROCm/aiter/pull/5448) more FlyDSL MoE optimizations on gfx1250
- [#4761](https://github.com/ROCm/aiter/pull/4761) Triton unified attention prefill/decode optimization
- [#5305](https://github.com/ROCm/aiter/pull/5305) large-M/small-N RMSNorm backward specialization
- [#5038](https://github.com/ROCm/aiter/pull/5038) Triton MoE routing optimizations
- [#5262](https://github.com/ROCm/aiter/pull/5262) tuner builds its result frame once instead of per-row concatenation
- [#5216](https://github.com/ROCm/aiter/pull/5216) FP8 MQA logits kernel optimized for MI350
- [#5441](https://github.com/ROCm/aiter/pull/5441) gfx1201 causal flash-attention optimization with OOB-safe V prefetch

</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#5207](https://github.com/ROCm/aiter/pull/5207) FlyDSL a8w8 gather-gemm
- [#5310](https://github.com/ROCm/aiter/pull/5310) Triton/Gluon MoE GEMM variants and weight-gradient kernel
- [#5280](https://github.com/ROCm/aiter/pull/5280) cktile a8w8-bpreshuffle gains the rowcol_wp_v2 kernel type
- [#5188](https://github.com/ROCm/aiter/pull/5188) fused sigmoid for vLLM
- [#5474](https://github.com/ROCm/aiter/pull/5474) FlyDSL paged-attention edge-case fixes and tuned page-128 support
- [#5475](https://github.com/ROCm/aiter/pull/5475) gather_kv_b_proj lifts the 4 GiB cache limit
- [#5228](https://github.com/ROCm/aiter/pull/5228) narrow-head gfx1250 MLA sparse-prefill kernels for DSv4 TP
- [#5272](https://github.com/ROCm/aiter/pull/5272) LL and LL128 protocols added for gfx9 comms
- [#5214](https://github.com/ROCm/aiter/pull/5214) MLA decode kernel name prefix
- [#5359](https://github.com/ROCm/aiter/pull/5359) designated initializers for FMHA forward args
- [#5367](https://github.com/ROCm/aiter/pull/5367), [#5402](https://github.com/ROCm/aiter/pull/5402) gfx1250 ASM MLA kernels rebuilt
- [#5442](https://github.com/ROCm/aiter/pull/5442) widened gfx950 stable decode TopK gates

</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#5416](https://github.com/ROCm/aiter/pull/5416) gfx12 A4W4 MoE tuning
- [#5240](https://github.com/ROCm/aiter/pull/5240) opt-in a16wi4 gemm2 CShuffle epilog
- [#5395](https://github.com/ROCm/aiter/pull/5395) MiniMax-M3 A16W4 SwiGLU enabled and tuned on gfx950
- [#5467](https://github.com/ROCm/aiter/pull/5467) DSV4 EP48 stage2 tuned for RCCL routing
- [#5357](https://github.com/ROCm/aiter/pull/5357) 64-bit weight offsets in ASM
- [#5314](https://github.com/ROCm/aiter/pull/5314) large-tensor addressing fix in quant and inverse_rope
- [#5433](https://github.com/ROCm/aiter/pull/5433) logs the activated comm-fused-moe runner config

</details>

<details>
<summary>Tuning configs (10)</summary>

- [#5213](https://github.com/ROCm/aiter/pull/5213) FP8 PTPC and BF16 MoE for Qwen3.8-Flash-Next
- [#5343](https://github.com/ROCm/aiter/pull/5343) GLM-5.3-Flash a8w8 blockscale GEMM on gfx942
- [#5349](https://github.com/ROCm/aiter/pull/5349) DSR1 Triton GEMM tuning on gfx1250
- [#4664](https://github.com/ROCm/aiter/pull/4664) DSv4 a8w8 blockscale on three MI355X shapes
- [#5360](https://github.com/ROCm/aiter/pull/5360) Kimi-K3 a8w8 bpreshuffle long-prefill
- [#5275](https://github.com/ROCm/aiter/pull/5275) bf16 MoE for K2 horizon 375B
- [#5459](https://github.com/ROCm/aiter/pull/5459) DSV4 EP48 top-k 6 prefill
- [#5371](https://github.com/ROCm/aiter/pull/5371) gpt-oss N=2880,K=4096 retuned off hipBLASLt for CUDAGraph capture
- [#5162](https://github.com/ROCm/aiter/pull/5162) gfx1250 split-K kept off shapes its reduce cannot address
- [#5323](https://github.com/ROCm/aiter/pull/5323) tuned paths used in gfx1250 combo benchmarks

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#5303](https://github.com/ROCm/aiter/pull/5303) FlyDSL ptr_rsrc and buffer ops moved to a new low-level API
- [#5391](https://github.com/ROCm/aiter/pull/5391) gfx1250 microbench
- [#5311](https://github.com/ROCm/aiter/pull/5311) `--combine both` for the mega_moe ubench

</details>

<details>
<summary>API & serving (2)</summary>

- [#5437](https://github.com/ROCm/aiter/pull/5437) env var to control perf co
- [#5471](https://github.com/ROCm/aiter/pull/5471) W4A16 backend warning printed once

</details>

<details>
<summary>Bugfixes (7)</summary>

- [#3606](https://github.com/ROCm/aiter/pull/3606) final_lse corrected in PS MLA prefill for chunked prefill
- [#4800](https://github.com/ROCm/aiter/pull/4800) transactional blob codegen cache publication
- [#4974](https://github.com/ROCm/aiter/pull/4974) custom_all_reduce RankData slot prediction during graph capture
- [#5261](https://github.com/ROCm/aiter/pull/5261) split-K OOB fix for afp4wfp4
- [#5329](https://github.com/ROCm/aiter/pull/5329) opus half-precision dtype spellings single-sourced
- [#5352](https://github.com/ROCm/aiter/pull/5352) stale MHA config-utils import
- [#5438](https://github.com/ROCm/aiter/pull/5438) trunci AttributeError in qk_norm_rope TDM path

</details>

<details>
<summary>Refactors (4)</summary>

- [#4997](https://github.com/ROCm/aiter/pull/4997) fp4 GEMM gluon moved to _gluon_kernels
- [#5382](https://github.com/ROCm/aiter/pull/5382) absolute imports under ops/triton
- [#5414](https://github.com/ROCm/aiter/pull/5414) shared helper for opt-in autotune configs
- [#5374](https://github.com/ROCm/aiter/pull/5374) shared MHA backend parameterization restored

</details>

<details>
<summary>Tests, CI & docs (10)</summary>

- [#5131](https://github.com/ROCm/aiter/pull/5131) auto-update split test FILE_TIMES
- [#5411](https://github.com/ROCm/aiter/pull/5411) label required for extended tests
- [#5365](https://github.com/ROCm/aiter/pull/5365) CPU isolation vs sglang CPU affinity conflict fixed
- [#5390](https://github.com/ROCm/aiter/pull/5390) aiter logger suppressed under pytest
- [#5381](https://github.com/ROCm/aiter/pull/5381) deprecated kwargs dropped
- [#5419](https://github.com/ROCm/aiter/pull/5419) no autotune for the FA port in unit tests
- [#5394](https://github.com/ROCm/aiter/pull/5394) HSTU reference import fallback
- [#5369](https://github.com/ROCm/aiter/pull/5369) Copilot review rules
- [#5383](https://github.com/ROCm/aiter/pull/5383) torch-free Triton docs
- [#5479](https://github.com/ROCm/aiter/pull/5479) gfx1250 FlyDSL MoE test and tuning update

</details>

<details>
<summary>Newly opened (in progress) (70)</summary>

- [#5461](https://github.com/ROCm/aiter/pull/5461) FlyDSL one- and two-stage ring all-reduce for PCIe
- [#5370](https://github.com/ROCm/aiter/pull/5370) FlyDSL Conv3d for Qwen-Image / Wan2.1 VAE
- [#5447](https://github.com/ROCm/aiter/pull/5447) TDM dispatch for gfx1250 mega-moe EP
- [#5476](https://github.com/ROCm/aiter/pull/5476) kernel IR cleanup and shared helper consolidation
- [#5398](https://github.com/ROCm/aiter/pull/5398) MoE GEMM2 split into mxmoe_g2 with scatter and persist-flat
- [#5363](https://github.com/ROCm/aiter/pull/5363) FlyDSL radix top-k one-block kernel and dispatch refactor
- [#5389](https://github.com/ROCm/aiter/pull/5389) ragged MXFP4 grouped GEMM and wgrad
- [#5481](https://github.com/ROCm/aiter/pull/5481) mla_reduce launcher split across TUs (JIT 121.6s to 7.7s)
- [#5412](https://github.com/ROCm/aiter/pull/5412) packed BF16 mHC with gfx1250 tuning
- [#5454](https://github.com/ROCm/aiter/pull/5454) gfx1250 combined benchmark driver
- [#5487](https://github.com/ROCm/aiter/pull/5487) K3 latent FHMoE eager decode prototype
- [#5455](https://github.com/ROCm/aiter/pull/5455) agent_loop orchestration layer
- [#5456](https://github.com/ROCm/aiter/pull/5456) UT for sparse MLA kernel
- [#5462](https://github.com/ROCm/aiter/pull/5462) MiniMax MXFP8 prefill MoE tuning
- [#5397](https://github.com/ROCm/aiter/pull/5397) opus gemm 256tile ring
- [#5436](https://github.com/ROCm/aiter/pull/5436) KDA K1 gluon and K2 fused affine
- [#5406](https://github.com/ROCm/aiter/pull/5406) gfx1250 a8w8 mxfp8_128 GEMM A-preshuffle and fused split-K
- [#5373](https://github.com/ROCm/aiter/pull/5373) gfx1250 hca_compress optimization
- [#5484](https://github.com/ROCm/aiter/pull/5484) FP4 output mode for indexer_qk_rope_quant_and_cache
- [#5445](https://github.com/ROCm/aiter/pull/5445) per-row top-k kernel sweep
- [#5450](https://github.com/ROCm/aiter/pull/5450) rebase of large MoE expert weights
- [#5384](https://github.com/ROCm/aiter/pull/5384) mla_gluon moved into _gluon_kernels/gfx950
- [#5458](https://github.com/ROCm/aiter/pull/5458) return LSE/softmax from MHA Gluon kernel
- [#5485](https://github.com/ROCm/aiter/pull/5485) DSv4 a8w8 blockscale GEMM tunings for gfx950
- [#5435](https://github.com/ROCm/aiter/pull/5435) a4w4 bench
- [#5482](https://github.com/ROCm/aiter/pull/5482) mxfp4 MoE kernel perf
- [#5424](https://github.com/ROCm/aiter/pull/5424) no CSV under pytest
- [#5423](https://github.com/ROCm/aiter/pull/5423) test print() routed through the aiter logger
- [#5478](https://github.com/ROCm/aiter/pull/5478) overflow-guarded int32 varlen strides
- [#5400](https://github.com/ROCm/aiter/pull/5400) FP8 output in gather_kv_b_proj
- [#5434](https://github.com/ROCm/aiter/pull/5434) MQA logits indexer sweep
- [#5399](https://github.com/ROCm/aiter/pull/5399) ff_a16w16_fused M<=8 launch fix
- [#5420](https://github.com/ROCm/aiter/pull/5420) gfx950 tiles for flash_kda K2 and sparse_attention_dsv4 prefill
- [#5405](https://github.com/ROCm/aiter/pull/5405) runtime softmax scale in FP8 FMHA
- [#5431](https://github.com/ROCm/aiter/pull/5431) torch.symm_mem (mori) transport for custom_ar on gfx1250
- [#5465](https://github.com/ROCm/aiter/pull/5465) row-major a1 scale layout dropped on gfx1250
- [#5470](https://github.com/ROCm/aiter/pull/5470) unshuffled MXFP4 GEMM on gfx1151
- [#5430](https://github.com/ROCm/aiter/pull/5430) split-K scratch buffers shared across CUDA graphs fixed
- [#5404](https://github.com/ROCm/aiter/pull/5404) BM16 SwiGLU path for MiniMax M3
- [#5393](https://github.com/ROCm/aiter/pull/5393) split-K preshuffle buffers kept out of the CUDA graph pool
- [#5409](https://github.com/ROCm/aiter/pull/5409) unified attention prefill configs for head sizes 129+
- [#5385](https://github.com/ROCm/aiter/pull/5385) ck_batched_gemm_bf16 strides derived from tensors
- [#5392](https://github.com/ROCm/aiter/pull/5392) optional sigmoid on gated_rmsnorm_fp8_per_token_quant
- [#5379](https://github.com/ROCm/aiter/pull/5379) Qwen3.8 Flash Next FP8 prefill config on MI308X
- [#5422](https://github.com/ROCm/aiter/pull/5422) checkAllclose mismatches now fail
- [#5427](https://github.com/ROCm/aiter/pull/5427) gather_kv_b_proj Triton 2-byte preshuffled weights
- [#5451](https://github.com/ROCm/aiter/pull/5451) GLM-5.2 TP4 MXFP4 MoE shape
- [#5421](https://github.com/ROCm/aiter/pull/5421) GLM-5.3 PTPC qkv a8w8-bpreshuffle for gfx950
- [#5368](https://github.com/ROCm/aiter/pull/5368) Kimi K3 a8w4 MoE TP8 config (draft)
- [#5432](https://github.com/ROCm/aiter/pull/5432) gfx950 unified attention config tuning
- [#5460](https://github.com/ROCm/aiter/pull/5460) fp8 MoE stage2 output via 64-bit pointers
- [#5425](https://github.com/ROCm/aiter/pull/5425) Triton CI fails on runtime autotune
- [#5403](https://github.com/ROCm/aiter/pull/5403) bf16 hd=256 fmha_fwd ASM for gfx950
- [#5480](https://github.com/ROCm/aiter/pull/5480) group quant dispatch fix for hidden sizes in (4096, 6144]
- [#5440](https://github.com/ROCm/aiter/pull/5440) DSV4 shared-expert large-M tuning
- [#5463](https://github.com/ROCm/aiter/pull/5463) test_mha_v3 mismatch fix
- [#5376](https://github.com/ROCm/aiter/pull/5376) bf16 hd=256 fmha_bwd ASM kernels for gfx950
- [#5428](https://github.com/ROCm/aiter/pull/5428) racy gemm_a16w16 N=256,K=7168 tile replaced
- [#5388](https://github.com/ROCm/aiter/pull/5388) 16x128 and 16x256 mxfp4 ASM kernel tuning
- [#5429](https://github.com/ROCm/aiter/pull/5429) padded V heads kept off num_stages=3 configs
- [#5378](https://github.com/ROCm/aiter/pull/5378) GLM-5.2 native-MTP M=4 projections tuned
- [#5439](https://github.com/ROCm/aiter/pull/5439) FP8 MoE intermediate option for Kimi-K3 a4w4
- [#5415](https://github.com/ROCm/aiter/pull/5415) gfx942 bf16 sliding-window decode tuning
- [#5372](https://github.com/ROCm/aiter/pull/5372) Triton backward autotune dimension keys fixed
- [#5426](https://github.com/ROCm/aiter/pull/5426) perftest timed with CUDA events under pytest
- [#5457](https://github.com/ROCm/aiter/pull/5457) flydsl dependency bumped to 0.3.3.dev889
- [#5468](https://github.com/ROCm/aiter/pull/5468) Kimi-K3 a8w4 fp8 route-out stage2 retune
- [#5443](https://github.com/ROCm/aiter/pull/5443) non-temporal loads kept on the tuned fused_moe path
- [#5452](https://github.com/ROCm/aiter/pull/5452) fp8_mqa_logits FN->FNUZ zero-extend fix on gfx942
- [#5453](https://github.com/ROCm/aiter/pull/5453) fp8_mqa_logits typed shift amounts for shrui

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: aff3cca3ede22bb7514bc046d90d861d1bea827ccfe1fe4e9a70ed59c51b7328 -->
