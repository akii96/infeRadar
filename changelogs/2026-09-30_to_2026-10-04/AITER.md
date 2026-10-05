# AITER: PR digest (2026-09-30 to 2026-10-04)

_59 merged, 123 newly opened - source ROCm/AITER, generated 2026-10-04T23:56:05Z_

## TL;DR
- **DeepSeek (V4.1 / R1 / MLA)** and **Kimi (K3 / KDA)** got the most attention, followed by GLM, Qwen3.8 and MiniMax-M3. Work was mostly gfx950/gfx1250 kernels plus tuned configs.
- **Merged perf work:** a Gluon chunked Kimi Delta Attention kernel for gfx950/gfx1250 ([#5866](https://github.com/ROCm/aiter/pull/5866)), FlyDSL MXFP8 a8w8 blockscale GEMM on gfx950 ([#4951](https://github.com/ROCm/aiter/pull/4951)), and the shared-expert gate GEMV folded into `topk_softmax` ([#5652](https://github.com/ROCm/aiter/pull/5652)).
- **In-flight perf work:** FlyDSL MoE decode and prefill optimizations ([#5973](https://github.com/ROCm/aiter/pull/5973), [#6136](https://github.com/ROCm/aiter/pull/6136), [#6065](https://github.com/ROCm/aiter/pull/6065), [#6064](https://github.com/ROCm/aiter/pull/6064)), new HIP/ASM sparse MLA kernels ([#6037](https://github.com/ROCm/aiter/pull/6037), [#6133](https://github.com/ROCm/aiter/pull/6133), [#6126](https://github.com/ROCm/aiter/pull/6126)), and Gemma-4 unified attention for gfx942 ([#6123](https://github.com/ROCm/aiter/pull/6123), [#6122](https://github.com/ROCm/aiter/pull/6122)).
- **Direction:** gfx1250 bring-up (MXFP4/MXFP8 GEMM, MLA, MoE, FMHA), FlyDSL as the main kernel authoring path, and tuning tables for next-gen model shapes. v0.1.24 release cherry-picks were merged ([#6075](https://github.com/ROCm/aiter/pull/6075)).

## Most important PRs
**[#5866](https://github.com/ROCm/aiter/pull/5866) Gluon Chunked Kimi Delta Attention (gfx950/gfx1250), merged.** It adds a chunked KDA kernel in Gluon, which Kimi K3 linear-attention layers need. It is the largest new kernel merged this window, with tests and tuning configs included.

**[#4951](https://github.com/ROCm/aiter/pull/4951) FlyDSL mxfp8 a8w4/a8w8 blockscale GEMM for gfx950, merged.** It adds a FlyDSL-backed MXFP8 blockscale GEMM alongside the CK path, aimed at DeepSeek-style block-scaled FP8 linears.

**[#5844](https://github.com/ROCm/aiter/pull/5844) Persistent MLA PS1 FP8 decode for gfx1250, merged.** It adds GPR pinning for nhead 96/128 and round-robin DCP to the persistent FP8 decode kernel, speeding up DeepSeek MLA decode on gfx1250.

**[#5652](https://github.com/ROCm/aiter/pull/5652) Fold shared-expert gate GEMV into `topk_softmax`, merged.** Fusing the gate GEMV into the router kernel removes a separate launch from the MoE front end. The change is HIP, with tuning configs.

**[#5973](https://github.com/ROCm/aiter/pull/5973) FlyDSL batch 1-8 MoE decode (3/3), open.** The last part of the small-batch MoE decode optimization series, aimed at Kimi, MiniMax and Qwen on gfx942. It is a large change (~12k lines).

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#6100](https://github.com/ROCm/aiter/pull/6100) fuse router GEMM and top-k softmax into one gfx950 asm kernel
- [#6070](https://github.com/ROCm/aiter/pull/6070) fuse mHC pre RMSNorm with per-token FP8 quant
- [#5987](https://github.com/ROCm/aiter/pull/5987) route gfx950 large-expert decode to multi-phase MoE sorting
- [#6036](https://github.com/ROCm/aiter/pull/6036) single-launch bitmask fused-MoE sort with optional fused router
- [#6074](https://github.com/ROCm/aiter/pull/6074) gfx1250 FMHA prefill: longest-first dispatch and KV split
- [#5978](https://github.com/ROCm/aiter/pull/5978) optimize qk-norm-rope MLA segment cache on gfx1250
- [#5985](https://github.com/ROCm/aiter/pull/5985) optimize group quant on gfx1250
- [#6078](https://github.com/ROCm/aiter/pull/6078) use gfx1250 320KB LDS for large-D SiTUv2 quant
- [#6121](https://github.com/ROCm/aiter/pull/6121) add Kimi-K3 gather_kv_b_proj on gfx1250

</details>

<details>
<summary>Kernels & attention (38)</summary>

- [#5230](https://github.com/ROCm/aiter/pull/5230) (merged) 3D neighborhood flash attention (na3d_flash)
- [#6034](https://github.com/ROCm/aiter/pull/6034) (merged) spec decode support for Gluon KDA
- [#6056](https://github.com/ROCm/aiter/pull/6056) (merged) GLA changes for Kimi K3
- [#5805](https://github.com/ROCm/aiter/pull/5805) (merged) speed up gfx1250 32mx1 MLA sparse-prefill kernels
- [#4221](https://github.com/ROCm/aiter/pull/4221) (merged) FlyDSL paged MLA indexer
- [#6126](https://github.com/ROCm/aiter/pull/6126) (merged) MLA v4 split plan helper and persistent decode kernel
- [#6087](https://github.com/ROCm/aiter/pull/6087) (merged) optimize MLA kernel for DSR1 on gfx1250
- [#5542](https://github.com/ROCm/aiter/pull/5542) (merged) fused SiLU-and-multiply backward
- [#5895](https://github.com/ROCm/aiter/pull/5895) (merged) gemm_a16w16_atomic accumulates into an existing output
- [#6097](https://github.com/ROCm/aiter/pull/6097) (merged) TDM fusion on MXFP4
- [#5858](https://github.com/ROCm/aiter/pull/5858) (merged) MHA fwd gfx950 mid_head config
- [#5665](https://github.com/ROCm/aiter/pull/5665), [#5771](https://github.com/ROCm/aiter/pull/5771), [#5958](https://github.com/ROCm/aiter/pull/5958) (merged) unified-attention bench and assert fixes
- [#6122](https://github.com/ROCm/aiter/pull/6122) temporary PR for unified attention Gemma4
- [#6123](https://github.com/ROCm/aiter/pull/6123) FlyDSL unified attention for gfx942 (Gemma-4)
- [#5996](https://github.com/ROCm/aiter/pull/5996) FlyDSL QSA indexer scorer + sparse GQA
- [#6083](https://github.com/ROCm/aiter/pull/6083) QSA indexer gfx942 improvements
- [#6116](https://github.com/ROCm/aiter/pull/6116) Gluon a8w8 sparse MLA for gfx12
- [#6037](https://github.com/ROCm/aiter/pull/6037) HIP BF16 sparse MLA for GLM-5.3-Flash on gfx950
- [#6047](https://github.com/ROCm/aiter/pull/6047) FlyDSL MiniMax-M3 fused sparse-layer decode
- [#6026](https://github.com/ROCm/aiter/pull/6026) fused KDA decode kernels on gfx950
- [#5992](https://github.com/ROCm/aiter/pull/5992) causal conv1d and GDN kernels for Qwen3.5/3.8
- [#5993](https://github.com/ROCm/aiter/pull/5993) hc_mix kernel for Qwen3.8 hyper-connections
- [#5995](https://github.com/ROCm/aiter/pull/5995) BF16 paged decode entry for Qwen3.8 QSA
- [#6020](https://github.com/ROCm/aiter/pull/6020) GFX11 wave32 FlashAttention for gfx1151
- [#6098](https://github.com/ROCm/aiter/pull/6098) LDS-pipelined MLA variant
- [#6107](https://github.com/ROCm/aiter/pull/6107) get_mla_decode_shape_support
- [#6112](https://github.com/ROCm/aiter/pull/6112) optional kv_len_hint for MLA gluon
- [#6133](https://github.com/ROCm/aiter/pull/6133) gfx1250 QH128 page64 MLA decode
- [#6132](https://github.com/ROCm/aiter/pull/6132) non-persistent fp8 gqa64 qlen1 asm MLA
- [#5977](https://github.com/ROCm/aiter/pull/5977) gfx1250 asm MHA hd192x128 strided q/k/v/out
- [#6099](https://github.com/ROCm/aiter/pull/6099) Gluon PA decode ragged query support
- [#6108](https://github.com/ROCm/aiter/pull/6108) non-causal support in unified attention
- [#6140](https://github.com/ROCm/aiter/pull/6140) aiter.paged_mqa_logits with tuned Gluon/FlyDSL table
- [#6001](https://github.com/ROCm/aiter/pull/6001) fp8_mqa_logits drops host row-pad copies
- [#6130](https://github.com/ROCm/aiter/pull/6130) gfx1250 FlashKDA K2 schedule
- [#6066](https://github.com/ROCm/aiter/pull/6066) gfx1201 MiniMax-H3 multi-GPU ops
- [#5980](https://github.com/ROCm/aiter/pull/5980) fused_qk_rope_cat_and_cache_mla NoPE variant

</details>

<details>
<summary>MoE & quantization (31)</summary>

- [#5934](https://github.com/ROCm/aiter/pull/5934) (merged) FlyDSL a4w4 prefill v2
- [#5708](https://github.com/ROCm/aiter/pull/5708) (merged) relu2 in CK-Tile fused MoE GEMM
- [#5863](https://github.com/ROCm/aiter/pull/5863) (merged) expert-parallel for moe_gemm_a16w4
- [#5832](https://github.com/ROCm/aiter/pull/5832) (merged) MXFP8 MoE keeps MFMA in FP8
- [#5763](https://github.com/ROCm/aiter/pull/5763) (merged) gfx950 MXFP4 SiTUv2 FLAT kernels
- [#5818](https://github.com/ROCm/aiter/pull/5818) (merged) gfx1250 MXFP8 1x32 bpreshuffle GEMM
- [#5667](https://github.com/ROCm/aiter/pull/5667) (merged) a16w4 MoE tuned dispatch and gfx942 DSv4.1 tables
- [#6136](https://github.com/ROCm/aiter/pull/6136) gfx1250 A4W4 MoE prefill with fused GEMM1 quant
- [#6055](https://github.com/ROCm/aiter/pull/6055) pin EP gemm1 cluster_m=1 for DSV4 grouped MoE
- [#6065](https://github.com/ROCm/aiter/pull/6065) exact-M8 MXFP4 GLM MoE route merge
- [#6064](https://github.com/ROCm/aiter/pull/6064) exact-M4 MXFP4 GLM MoE pipeline
- [#6050](https://github.com/ROCm/aiter/pull/6050) HY4 MXFP8 heterogeneous MoE fusion
- [#6052](https://github.com/ROCm/aiter/pull/6052) MegaMoE stage fused switches and mori combine
- [#6127](https://github.com/ROCm/aiter/pull/6127) MegaMoEV2 decode/prefill opts and LDS race fix
- [#5970](https://github.com/ROCm/aiter/pull/5970) hipBLASLt grouped GEMM backend for SonicMoE
- [#6115](https://github.com/ROCm/aiter/pull/6115) extend fused G2L LUT to 1024 experts
- [#6131](https://github.com/ROCm/aiter/pull/6131) gfx1250 exact sigmoid top-k
- [#6106](https://github.com/ROCm/aiter/pull/6106) per-token scale in a8w8 moe gemm
- [#6038](https://github.com/ROCm/aiter/pull/6038) fused gated RMSNorm + MXFP4 quant
- [#6024](https://github.com/ROCm/aiter/pull/6024) fused_reduce_act_mul_and_mxfp4_quant tweaks
- [#6118](https://github.com/ROCm/aiter/pull/6118) multicast for gfx1250 MXFP4
- [#6067](https://github.com/ROCm/aiter/pull/6067) persistent gfx950 f4gemm 256x256
- [#6101](https://github.com/ROCm/aiter/pull/6101) gfx950 asm GEMM with BF16 activations and FP8 weights
- [#5988](https://github.com/ROCm/aiter/pull/5988) gfx950 Q256 fused MXFP4 prefill pipeline
- [#5969](https://github.com/ROCm/aiter/pull/5969) FlyDSL a8w8 blockscale
- [#6060](https://github.com/ROCm/aiter/pull/6060) gfx950 MXFP8 bmm with MiniMax-M3 configs
- [#6049](https://github.com/ROCm/aiter/pull/6049) QuickAllReduce INT4 shared global divisor
- [#6000](https://github.com/ROCm/aiter/pull/6000) Gemma (1+w) weights in fused AR+RMSNorm+MXFP4
- [#5965](https://github.com/ROCm/aiter/pull/5965) gfx1250 QuickReduce for TP2/TP4
- [#6031](https://github.com/ROCm/aiter/pull/6031) M3 sequence-parallel collectives
- [#5975](https://github.com/ROCm/aiter/pull/5975) decouple FP6 packers from Triton

</details>

<details>
<summary>Tuning configs (40)</summary>

- [#5966](https://github.com/ROCm/aiter/pull/5966) dsv41 MoE config file
- [#5967](https://github.com/ROCm/aiter/pull/5967) DSv4.1 CK MoE tunings
- [#6125](https://github.com/ROCm/aiter/pull/6125) gfx950 A8W4 fused_moe for DSv4.1
- [#5904](https://github.com/ROCm/aiter/pull/5904) a8w4 fused-MoE for DeepSeek V4.1-Flash
- [#6003](https://github.com/ROCm/aiter/pull/6003) DSv4 E=385/topk7 fused MoE
- [#6029](https://github.com/ROCm/aiter/pull/6029) DSv4 wq_b / wo_b blockscale GEMMs
- [#6004](https://github.com/ROCm/aiter/pull/6004) DSv4 wqkv_a blockscale GEMM
- [#6005](https://github.com/ROCm/aiter/pull/6005) HGEMM fp32 C shuffle and DSv4 wkv_gate rows
- [#6030](https://github.com/ROCm/aiter/pull/6030) mHC fused post+pre tile_m=16
- [#5939](https://github.com/ROCm/aiter/pull/5939) DSR1 gfx1250 bf16 GEMM
- [#6069](https://github.com/ROCm/aiter/pull/6069) dsr oct 1 tuning
- [#5783](https://github.com/ROCm/aiter/pull/5783) Kimi-K3 KDA gate a8w8 at tp4
- [#6019](https://github.com/ROCm/aiter/pull/6019) k3 gfx950 bf16 tp8
- [#6088](https://github.com/ROCm/aiter/pull/6088) Kimi-K3 ptpc bpreshuffle on gfx1250
- [#6089](https://github.com/ROCm/aiter/pull/6089) Kimi-K3 BF16 decode GEMM
- [#5836](https://github.com/ROCm/aiter/pull/5836) Qwen3.8-27B GDN BA projection
- [#5974](https://github.com/ROCm/aiter/pull/5974) Qwen3.8-Flash-Next PTPC-FP8 gfx942
- [#6033](https://github.com/ROCm/aiter/pull/6033) Qwen3.8-27B TP1 a8w8 blockscale
- [#6039](https://github.com/ROCm/aiter/pull/6039) Qwen3.8-Flash-Next AFP4WFP4 GDN projections
- [#6025](https://github.com/ROCm/aiter/pull/6025) Qwen3.8 mxfp4 emsort asm
- [#6090](https://github.com/ROCm/aiter/pull/6090) Qwen3.5 FP4 grouped MoE on gfx1250
- [#5999](https://github.com/ROCm/aiter/pull/5999) qwen35 bf16 GEMM on gfx1250
- [#6043](https://github.com/ROCm/aiter/pull/6043) Qwen3.5-397B bf16 a16w16 on gfx1250
- [#5994](https://github.com/ROCm/aiter/pull/5994) GLM-5.2-FP8 a8w8 blockscale
- [#5982](https://github.com/ROCm/aiter/pull/5982) GLM-5.3-Flash TP4 KDA in-proj
- [#6077](https://github.com/ROCm/aiter/pull/6077) GLM-5.3-Flash TP2 fused-MoE
- [#5986](https://github.com/ROCm/aiter/pull/5986) GLM-5 MXFP4 EP4 decode MoE
- [#6079](https://github.com/ROCm/aiter/pull/6079) MiniMax-M3 lm_head
- [#6085](https://github.com/ROCm/aiter/pull/6085) MiniMax-M3 TP2 FMOE
- [#6015](https://github.com/ROCm/aiter/pull/6015) Llama-3.1-8B afp4wfp4 decode
- [#5875](https://github.com/ROCm/aiter/pull/5875), [#6032](https://github.com/ROCm/aiter/pull/6032), [#6028](https://github.com/ROCm/aiter/pull/6028) gfx1250 GEMM tunings (k3, Wan2.2, MXFP4)
- [#5933](https://github.com/ROCm/aiter/pull/5933), [#5998](https://github.com/ROCm/aiter/pull/5998), [#6061](https://github.com/ROCm/aiter/pull/6061), [#5981](https://github.com/ROCm/aiter/pull/5981) gfx950 GEMM tunings
- [#5857](https://github.com/ROCm/aiter/pull/5857) gmm gfx950 large-K/N config
- [#5997](https://github.com/ROCm/aiter/pull/5997) seed gfx1150 configs from gfx1151
- [#6128](https://github.com/ROCm/aiter/pull/6128) tuning from default config json
- [#6117](https://github.com/ROCm/aiter/pull/6117) GFX12 MoE tune
- [#6109](https://github.com/ROCm/aiter/pull/6109) fused_reduce_qk_norm_rope_swa_write bench and tune

</details>

<details>
<summary>Bugfixes (28)</summary>

- [#5979](https://github.com/ROCm/aiter/pull/5979) (merged) keep two K tiles per split in blockscale MoE split-K
- [#5886](https://github.com/ROCm/aiter/pull/5886) (merged) pa_decode compile error with newer Triton
- [#5663](https://github.com/ROCm/aiter/pull/5663) (merged) fp8 KV reference in bench_unified_attention
- [#5963](https://github.com/ROCm/aiter/pull/5963) (merged) LDS OOM on mxfp8 gemm
- [#6009](https://github.com/ROCm/aiter/pull/6009) (merged) unified attention sglang compatibility
- [#6129](https://github.com/ROCm/aiter/pull/6129) (merged) custom_all_reduce IPC handle tensors on host
- [#6082](https://github.com/ROCm/aiter/pull/6082) (merged) batched_gemm_a8w8 scale loads in bounds
- [#6007](https://github.com/ROCm/aiter/pull/6007) (merged) zero default for masked scales in gemm_afp8wfp8
- [#5984](https://github.com/ROCm/aiter/pull/5984), [#6080](https://github.com/ROCm/aiter/pull/6080) (merged) Conv3D CPU tests and topk_select restriction
- [#5800](https://github.com/ROCm/aiter/pull/5800) (merged) gluon import fix and fused_clamp_act_mul tune
- [#5790](https://github.com/ROCm/aiter/pull/5790) (merged) gfx1201 unified attention tuning and D=1024 launches
- [#6139](https://github.com/ROCm/aiter/pull/6139) scale gfx942 FP8 FMHA probabilities before conversion
- [#6138](https://github.com/ROCm/aiter/pull/6138) scale gfx942 Sage probabilities before FP8 conversion
- [#6119](https://github.com/ROCm/aiter/pull/6119) mxfp4 moe sort skips invalid ids
- [#6113](https://github.com/ROCm/aiter/pull/6113) force-reduce Stage-2 dispatch
- [#6086](https://github.com/ROCm/aiter/pull/6086) cktile BF16-MXFP4 MoE wrong output
- [#6022](https://github.com/ROCm/aiter/pull/6022) cktile 2stages dispatcher fix
- [#6013](https://github.com/ROCm/aiter/pull/6013) gfx942 FLAT candidates in ASM FMoE tuning
- [#6016](https://github.com/ROCm/aiter/pull/6016) align FMoE tuning buckets with runtime lookup
- [#6091](https://github.com/ROCm/aiter/pull/6091) non-uniform query offsets after head folding
- [#6040](https://github.com/ROCm/aiter/pull/6040) stream-ordered get_ps_metadata_v1
- [#6120](https://github.com/ROCm/aiter/pull/6120) fused gather_kv_b_proj on gfx1250
- [#6081](https://github.com/ROCm/aiter/pull/6081) gfx1250 unified attention faults and NaNs
- [#6002](https://github.com/ROCm/aiter/pull/6002) faster sparse MLA prefill for DSv4.1-Flash; fix attn_sink
- [#6054](https://github.com/ROCm/aiter/pull/6054) diverge on active chunks in topk decode
- [#6095](https://github.com/ROCm/aiter/pull/6095) Triton topk for rows with -inf
- [#6051](https://github.com/ROCm/aiter/pull/6051) asymmetric Q/K and V heads in unified attention
- [#5972](https://github.com/ROCm/aiter/pull/5972) restore shadowed OPUS A16W16 cache-policy registrations
- plus 9 more minor fixes: [#6076](https://github.com/ROCm/aiter/pull/6076), [#6096](https://github.com/ROCm/aiter/pull/6096), [#6092](https://github.com/ROCm/aiter/pull/6092), [#6018](https://github.com/ROCm/aiter/pull/6018), [#6124](https://github.com/ROCm/aiter/pull/6124), [#6041](https://github.com/ROCm/aiter/pull/6041), [#6071](https://github.com/ROCm/aiter/pull/6071), [#5983](https://github.com/ROCm/aiter/pull/5983), [#6042](https://github.com/ROCm/aiter/pull/6042)

</details>

<details>
<summary>Release, CI & build (11)</summary>

- [#6075](https://github.com/ROCm/aiter/pull/6075) (merged) release v0.1.24 cherry-pick of 29 main PRs
- [#5880](https://github.com/ROCm/aiter/pull/5880) (merged) Triton board PR status driven from the workflow
- [#5544](https://github.com/ROCm/aiter/pull/5544) (merged) remove committed scratch files
- [#5989](https://github.com/ROCm/aiter/pull/5989) (merged) ATOM GPU isolation and startup fixes
- [#5864](https://github.com/ROCm/aiter/pull/5864) (merged) preserve install failure status after retries
- [#6006](https://github.com/ROCm/aiter/pull/6006) publish a py3 wheel without prebuilt kernels
- [#5971](https://github.com/ROCm/aiter/pull/5971) fail fast and retry on third-party clone failures
- [#5991](https://github.com/ROCm/aiter/pull/5991) missing extension module names in pretune builds
- [#6102](https://github.com/ROCm/aiter/pull/6102) Triton PR checklist
- [#5942](https://github.com/ROCm/aiter/pull/5942), [#5940](https://github.com/ROCm/aiter/pull/5940) (merged) move Triton unit tests into wrapper folders

</details>

<details>
<summary>Tests & cleanup (5)</summary>

- [#6068](https://github.com/ROCm/aiter/pull/6068) reduce tests
- [#6111](https://github.com/ROCm/aiter/pull/6111) timing controls for test_gemm_a8w8_blockscale
- [#6073](https://github.com/ROCm/aiter/pull/6073) remove bench_gemm_afp4wfp4_pre_quant_atomic
- [#6035](https://github.com/ROCm/aiter/pull/6035) remove bad moe gemm wrapper code
- [#5968](https://github.com/ROCm/aiter/pull/5968) move Grouped MatMul into gemm/grouped

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 3447b2833a3b38f2c53cd3a447382dd8007b6cee4657b48699127bd26e6870b4 -->
