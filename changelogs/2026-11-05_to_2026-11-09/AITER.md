# AITER: PR digest (2026-11-05 to 2026-11-09)

_81 merged, 109 newly opened - source ROCm/AITER, generated 2026-11-09T00:40:56Z_

## TL;DR
- **DeepSeek (V4/V4.1-Flash) and Kimi (K3) got the most attention**, followed by Qwen and MiniMax-M3. Most of the work was gfx1250 and gfx950 tuning, MoE routing/quant fusion, and MQA-logits and sparse-MLA kernels.
- **Biggest merged perf and feature work:** a fused MegaMoEV2 kernel (Dispatch + GEMM1 + GEMM2 + Combine in one launch) (`[#6881](https://github.com/ROCm/aiter/pull/6881)`), a gfx950 sparse MLA kernel for fp8 KV cache (`[#7429](https://github.com/ROCm/aiter/pull/7429)`), and an FP8 Flash Attention v2 for gfx942/gfx950 (`[#5577](https://github.com/ROCm/aiter/pull/5577)`).
- **Communication:** Lamport allreduce landed on gfx9 (`[#7452](https://github.com/ROCm/aiter/pull/7452)`). Open PRs extend it to gfx1250 allreduce+RMSNorm (`[#7499](https://github.com/ROCm/aiter/pull/7499)`) and fold a residual add into the Triton all-reduce (`[#7488](https://github.com/ROCm/aiter/pull/7488)`).
- **Open work is dominated by gfx1250 attention and MoE:** MiniMax-M3 paged attention, TP MoE routing folded into activation quant, and mxfp8 Gluon. gfx950 gets a Kimi-K3 KDA target-verify kernel, NVFP4 MoE, and a batch of MLA-decode LDS race fixes.
- **Direction:** bring up gfx1250 and gfx950 for the newest DeepSeek, Kimi and MiniMax models via FlyDSL/Gluon kernels and per-model GEMM/MoE tuning tables. A parallel correctness sweep (padding sentinels, LDS races) is underway.

## Most important PRs
**`[#6881](https://github.com/ROCm/aiter/pull/6881)` MegaMoEV2 fused FlyDSL kernel**
Fuses EP dispatch, both expert GEMMs and combine into a single kernel. This removes the inter-kernel launches and sync boundaries of the MoE pipeline.

**`[#7429](https://github.com/ROCm/aiter/pull/7429)` Sparse MLA kernel for tensor-scale fp8 KV cache (gfx950)**
A custom Gluon sparse MLA kernel that reads a per-tensor-scaled fp8 KV cache. It targets DeepSeek-style sparse attention decode.

**`[#6952](https://github.com/ROCm/aiter/pull/6952)` MXFP4 MQA logits: one API for V4 and V4.1**
Unifies the OPUS MXFP4 MQA-logits path with Table/Free/Prefill schedules across gfx950 and gfx1250. This is the DeepSeek indexer hot path.

**`[#7494](https://github.com/ROCm/aiter/pull/7494)` Kimi-K3 HERD on gfx1250**
Adds K+1 sigmoid top-k and a single route+psum kernel for MoE routing. It cuts the launch count in the Kimi-K3 router.

**`[#5577](https://github.com/ROCm/aiter/pull/5577)` FP8 Flash Attention v2 (gfx942/gfx950)**
A new Triton/Gluon FP8 FA kernel with tuning configs, extending the quantized attention coverage to MI300 and MI350 class hardware.

## More changes by area

<details>
<summary>Performance (10)</summary>

- [#7624](https://github.com/ROCm/aiter/pull/7624) DeepSeek-V4.1-Flash TP2 decode: indexer top-k split gate and router GEMM row
- [#6831](https://github.com/ROCm/aiter/pull/6831) pipeline CSR segments in unsplit OPUS sparse prefill
- [#7080](https://github.com/ROCm/aiter/pull/7080) speed up gfx1250 two-stage AR RMSNorm FP8 amax reduction
- [#7272](https://github.com/ROCm/aiter/pull/7272) optimize DSv4 flash MoE perf on gfx1250
- [#7296](https://github.com/ROCm/aiter/pull/7296) optimize DSv4.1, K3, M3 MoE perf on gfx1250
- [#7238](https://github.com/ROCm/aiter/pull/7238) FlyDSL a8w8 256x256 persistent kernel improvement
- [#7546](https://github.com/ROCm/aiter/pull/7546) tunable HGEMM K-stagger and B streaming loads
- [#7363](https://github.com/ROCm/aiter/pull/7363) reuse stage2 scatter/reduce scratch in the v2 MoE wrapper
- [#6484](https://github.com/ROCm/aiter/pull/6484) fused_moe skips moe_sorting for a registered BM=16 presort
- [#7171](https://github.com/ROCm/aiter/pull/7171) fused bf16 BMM + cat + FP8 quant + head pad for MLA decode

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#6575](https://github.com/ROCm/aiter/pull/6575) MHAv4 per-row block-sparse geometry, LSE and ragged KV on gfx950
- [#6496](https://github.com/ROCm/aiter/pull/6496) gfx950 GDN fused prefill kernel
- [#7375](https://github.com/ROCm/aiter/pull/7375) asm MHA fp8 fwd D192x128 per-tensor varlen on gfx1250
- [#7215](https://github.com/ROCm/aiter/pull/7215) gfx950 sliding-window attention backward
- [#6662](https://github.com/ROCm/aiter/pull/6662) gfx1250 implicit-GEMM conv3d
- [#7205](https://github.com/ROCm/aiter/pull/7205) PA planner batch and capacity as runtime values
- [#6185](https://github.com/ROCm/aiter/pull/6185) aiter.mqa_logits with a tuned Triton/FlyDSL table
- [#7128](https://github.com/ROCm/aiter/pull/7128) OPUS FP4 MQA writer and query scale layouts
- [#7232](https://github.com/ROCm/aiter/pull/7232) add out_dtype to Triton MHA forward
- [#6678](https://github.com/ROCm/aiter/pull/6678) fused_reduce_add_rmsnorm
- [#5913](https://github.com/ROCm/aiter/pull/5913) two-stage Hyper-Connection Gated Residual kernel
- [#7034](https://github.com/ROCm/aiter/pull/7034) KDA cleanup
- [#6990](https://github.com/ROCm/aiter/pull/6990) align batch-prefill full-attention dispatch
- [#7487](https://github.com/ROCm/aiter/pull/7487) fix gfx1250 MHA CK JIT builds and route backward to asm
- [#7472](https://github.com/ROCm/aiter/pull/7472) unified_attention: keep 3D split-KV padding rows from storing stats
- [#7464](https://github.com/ROCm/aiter/pull/7464) align gfx942 QH64 FP8 MLA page-size planning

</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#6464](https://github.com/ROCm/aiter/pull/6464) MXFP4 FlyDSL a8w4 optimization and replacement
- [#6476](https://github.com/ROCm/aiter/pull/6476) MXFP4 dequant H16 requantization
- [#7468](https://github.com/ROCm/aiter/pull/7468) [WIP] MoE fused quant for prefill (token-multidest, compact-scale two-pass)
- [#6552](https://github.com/ROCm/aiter/pull/6552) honour swiglu_limit for BF16 SiLU/SwiGLU on gfx942
- [#6734](https://github.com/ROCm/aiter/pull/6734) fuse 32-point Hadamard rotation into MXFP4 quant and AR+RMSNorm epilogue
- [#5757](https://github.com/ROCm/aiter/pull/5757) Qwen3.8 flash MXFP4 asm MoE
- [#7495](https://github.com/ROCm/aiter/pull/7495) DSv4.1 decoding experiment

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#7433](https://github.com/ROCm/aiter/pull/7433) size custom allreduce pool from per-op AR/AG/RS max-size env vars
- [#7357](https://github.com/ROCm/aiter/pull/7357) clarify fused all-reduce limit units with MAX_BYTES
- [#7126](https://github.com/ROCm/aiter/pull/7126) never share scratch buffers whose zero fill was recorded into a graph

</details>

<details>
<summary>Model support & tuning configs (17)</summary>

- [#7235](https://github.com/ROCm/aiter/pull/7235) Mistral Large 4 gfx950 tuned tables (TP8 + TP4)
- [#7485](https://github.com/ROCm/aiter/pull/7485) Kimi-K3.1 Pro gfx950 BF16 GEMM rows
- [#7234](https://github.com/ROCm/aiter/pull/7234) DeepSeek-V4.1-Flash dense FP8 GEMM tiles (gfx1250)
- [#7366](https://github.com/ROCm/aiter/pull/7366) DeepSeek-V4.1-Flash MX32 FP8 GEMMs at large decode M
- [#7602](https://github.com/ROCm/aiter/pull/7602) retune DeepSeek-V4.1-Flash TP2 decode MoE buckets
- [#7477](https://github.com/ROCm/aiter/pull/7477) preshuffled A8W8 GEMM for DSR1 shapes (gfx1250)
- [#7075](https://github.com/ROCm/aiter/pull/7075) MI350P a4w4 GEMM for Qwen3.8-27B-Quark-AWQ-MXFP4
- [#7383](https://github.com/ROCm/aiter/pull/7383) gfx950 a8w8 blockscale for Qwen3-14B-FP8
- [#7441](https://github.com/ROCm/aiter/pull/7441) gfx950 a4w4 for Qwen3.8-2.4T GDN in_proj_qkvz
- [#7204](https://github.com/ROCm/aiter/pull/7204) Qwen3.8-Flash-Next TP4 prefill BF16 on MI308X
- [#7507](https://github.com/ROCm/aiter/pull/7507) MiniMax-M3 DP4/EP4 dense GEMMs (gfx1250)
- [#7498](https://github.com/ROCm/aiter/pull/7498) MiniMax-M3.1 gfx950 GEMM tuning
- [#7224](https://github.com/ROCm/aiter/pull/7224) Beam FP8 fused MoE configs for gfx950
- [#6985](https://github.com/ROCm/aiter/pull/6985) gfx1151 batched_gemm_a16w16 configs
- [#6982](https://github.com/ROCm/aiter/pull/6982) gfx1151 fused_sigmoid_mul config
- [#6979](https://github.com/ROCm/aiter/pull/6979) gfx1151 RMSNorm config
- [#7257](https://github.com/ROCm/aiter/pull/7257) use gfx1151 MHA prefill config on gfx1150

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#7434](https://github.com/ROCm/aiter/pull/7434) cover the full gfx1250 kernel family for strict AOT wheels
- [#7491](https://github.com/ROCm/aiter/pull/7491) guard Mega-MHC gfx1250 sources by build target
- [#7505](https://github.com/ROCm/aiter/pull/7505) clear HIP sticky error after A0 strict-CO probe failure

</details>

<details>
<summary>Bugfixes (12)</summary>

- [#6578](https://github.com/ROCm/aiter/pull/6578) fix KV addressing, mask scratch and empty splits in gfx950 BF16 32-head MLA
- [#7574](https://github.com/ROCm/aiter/pull/7574) fix LDS race between V reads and R re-layout in gfx950 BF16 MLA
- [#5505](https://github.com/ROCm/aiter/pull/5505) fix hardcoded die and CU counts in Triton kernels
- [#6854](https://github.com/ROCm/aiter/pull/6854) fix uneven split-K in fused a8w8 blockscale GEMMs
- [#7365](https://github.com/ROCm/aiter/pull/7365) drop expert -1 pad routes in the fused TP route/psum kernel
- [#7104](https://github.com/ROCm/aiter/pull/7104) moe_reduce guards the -1 topk_ids sentinel
- [#7601](https://github.com/ROCm/aiter/pull/7601) zero consumed kv in gfx1250 HCA Phase 2 loop
- [#7550](https://github.com/ROCm/aiter/pull/7550) fused_compress_attn zeroes padding kv in Phase 1
- [#7376](https://github.com/ROCm/aiter/pull/7376) skip grouped top-k launches with zero tokens
- [#7551](https://github.com/ROCm/aiter/pull/7551) hide GPUs from AOT replays with empty device lists
- [#7583](https://github.com/ROCm/aiter/pull/7583) fix main CI missing DROPPED_ROUTE_ROW import
- [#7598](https://github.com/ROCm/aiter/pull/7598) target AOT dry run through FLYDSL_GPU_ARCH only

</details>

<details>
<summary>Refactors & other (3)</summary>

- [#7424](https://github.com/ROCm/aiter/pull/7424) move _e8m0_byte_to_f32 into mxfp4_gemm_common
- [#7271](https://github.com/ROCm/aiter/pull/7271) add flyc.compile to skills and cache HERD host launches
- [#7452](https://github.com/ROCm/aiter/pull/7452) Lamport allreduce on gfx9 (see Important)

</details>

<details>
<summary>CI & build (7)</summary>

- [#7490](https://github.com/ROCm/aiter/pull/7490) Release v0.1.28 post1 re-cut from main
- [#7482](https://github.com/ROCm/aiter/pull/7482) evidence-driven PR self-review verdicts
- [#7330](https://github.com/ROCm/aiter/pull/7330) scope test_moe_2stage.py to representative tokens
- [#7340](https://github.com/ROCm/aiter/pull/7340) pin FlyDSL to v0.4.2
- [#7541](https://github.com/ROCm/aiter/pull/7541) skip Flash Attention CI on draft PRs
- [#7491](https://github.com/ROCm/aiter/pull/7491) gfx1250 Mega-MHC build guard (see Hardware)
- plus a few minor related CI updates

</details>

<details>
<summary>Newly opened: attention & MLA (in progress) (24)</summary>

- [#7529](https://github.com/ROCm/aiter/pull/7529) fused Kimi-K3 KDA target-verify kernel (gfx942/gfx950)
- [#7553](https://github.com/ROCm/aiter/pull/7553) gfx1250 FlyDSL paged FMHA
- [#7619](https://github.com/ROCm/aiter/pull/7619) gfx1250 PA decode for MiniMax-M3 (wide softmax steps, wave-pair MTP4)
- [#7618](https://github.com/ROCm/aiter/pull/7618) optimize gfx1250 MiniMax-M3 paged attention and planning
- [#7556](https://github.com/ROCm/aiter/pull/7556) sparse prefill attention on gfx950 (QSA)
- [#7584](https://github.com/ROCm/aiter/pull/7584) group/varlen and sliding window for hd128 opus forward
- [#7594](https://github.com/ROCm/aiter/pull/7594) MHA variant for varlen
- [#7506](https://github.com/ROCm/aiter/pull/7506) gfx950 fp8 varlen MHA forward for MLA prefill
- [#7559](https://github.com/ROCm/aiter/pull/7559) asm MHA bf16 hd256 batch and varlen on gfx1250
- [#7603](https://github.com/ROCm/aiter/pull/7603) more mxfp8 attention support
- [#7578](https://github.com/ROCm/aiter/pull/7578) faster paged-attention decode on gfx950
- [#7566](https://github.com/ROCm/aiter/pull/7566) one query block per short sequence, split-KV for decode
- [#7570](https://github.com/ROCm/aiter/pull/7570) wide split-K reduce for MLA decode/verify
- [#7607](https://github.com/ROCm/aiter/pull/7607) gfx1250 MLA decode: non-power-of-2 splits, BF16 partials
- [#7569](https://github.com/ROCm/aiter/pull/7569) saturate fp8 rope output of fused_qk_rope_concat_and_cache_mla
- [#7537](https://github.com/ROCm/aiter/pull/7537) FP4 row-group MQA logits epilogue and tile maxima
- [#7530](https://github.com/ROCm/aiter/pull/7530) Triton fallback for paged_mxfp4_mqa_logits
- [#7580](https://github.com/ROCm/aiter/pull/7580) retune GLM-5 MQA logits, add GLM-5.3-Flash rows
- [#7517](https://github.com/ROCm/aiter/pull/7517) fp8_mqa_logits optional caller-owned buffer
- [#7539](https://github.com/ROCm/aiter/pull/7539) clamp gfx950 unified attention block-table prefetch
- [#7518](https://github.com/ROCm/aiter/pull/7518) cast strides to int64 in MHA prefill attn_fwd
- [#7510](https://github.com/ROCm/aiter/pull/7510) read fp8_dsv32_mla cache in fnuz on gfx942
- [#7608](https://github.com/ROCm/aiter/pull/7608) gfx1201 flash attention head_dim % 8
- [#7516](https://github.com/ROCm/aiter/pull/7516) gfx942 FP8 head-dim-256 MHA config

</details>

<details>
<summary>Newly opened: MoE, GEMM & quantization (in progress) (36)</summary>

- [#7606](https://github.com/ROCm/aiter/pull/7606) NVFP4 routed-expert MoE for gfx950
- [#7542](https://github.com/ROCm/aiter/pull/7542) Kimi EP32 support
- [#7497](https://github.com/ROCm/aiter/pull/7497) intra-node EP dispatch/combine without mori runtime
- [#7543](https://github.com/ROCm/aiter/pull/7543) fold gfx1250 TP MoE route into activation quant
- [#7547](https://github.com/ROCm/aiter/pull/7547) route gfx1250 TP prefill MoE in one launch
- [#7599](https://github.com/ROCm/aiter/pull/7599) CK 2-stage for gfx950 fp8 block-scale MoE with few rows per expert
- [#7611](https://github.com/ROCm/aiter/pull/7611) FLAT/EMSORT MXFP4 fmoe tiles on padded intermediate widths
- [#7565](https://github.com/ROCm/aiter/pull/7565) rotate SwiGLU output between the two GEMMs
- [#7558](https://github.com/ROCm/aiter/pull/7558) keep Swiglu MXFP4 A4W4 off a numerically broken shape
- [#7501](https://github.com/ROCm/aiter/pull/7501) per-chunk scale line for MX combine
- [#7500](https://github.com/ROCm/aiter/pull/7500) row-strided MXFP4 activations
- [#7486](https://github.com/ROCm/aiter/pull/7486) a16wmix gemm2 reduce epilogue skips sort pad sentinels
- [#7620](https://github.com/ROCm/aiter/pull/7620) BM16 adaptive aux sort; retune kimik3 a8w4
- [#7572](https://github.com/ROCm/aiter/pull/7572) clear_missing_routes over whole route scratch
- [#7496](https://github.com/ROCm/aiter/pull/7496) EP intranode dispatch skips out-of-range expert ids
- [#7586](https://github.com/ROCm/aiter/pull/7586) keep gfx942 asm 1-stage fmoe off weights past 4 GiB
- [#7589](https://github.com/ROCm/aiter/pull/7589) per-arch ck2stages MoE kernel table
- [#7567](https://github.com/ROCm/aiter/pull/7567) fix MoE XCD swizzle on grids not divisible by 8
- [#7605](https://github.com/ROCm/aiter/pull/7605) gfx1250 grouped MoE GEMM output store without TDM
- [#7632](https://github.com/ROCm/aiter/pull/7632) gfx1250 a4w4 MoE decode output store without TDM
- [#7540](https://github.com/ROCm/aiter/pull/7540) fix moe sorting opus on gfx1250
- [#7564](https://github.com/ROCm/aiter/pull/7564) ping-pong Gluon kernel for MXFP4 GEMM (gfx950)
- [#7587](https://github.com/ROCm/aiter/pull/7587) optimize mxfp8 Gluon on gfx1250
- [#7548](https://github.com/ROCm/aiter/pull/7548) gfx1250 TDM HGEMM port
- [#7596](https://github.com/ROCm/aiter/pull/7596) gfx950 A16W16 rectangular tiles for Kimi-K3 shapes
- [#7503](https://github.com/ROCm/aiter/pull/7503) gfx1250 conv3d optimization
- [#7533](https://github.com/ROCm/aiter/pull/7533) batched/fused FP4 GEMMs on emulated FP4 (gfx1101)
- [#7532](https://github.com/ROCm/aiter/pull/7532) gemm_a16wfp4 and gemm_a8wfp4 on emulated FP4
- [#7554](https://github.com/ROCm/aiter/pull/7554) gemm_afp4wfp4 K-tail scale mask fix
- [#7595](https://github.com/ROCm/aiter/pull/7595) gemm_afp4wfp4 BLOCK_SIZE_K fix
- [#7509](https://github.com/ROCm/aiter/pull/7509) fix LDS race in gfx942 A8W8 blockscale GEMM
- [#7616](https://github.com/ROCm/aiter/pull/7616) gfx1250 gemm_a16w16 accumulate epilogue
- [#7591](https://github.com/ROCm/aiter/pull/7591) compute GRID_MN at runtime
- [#7544](https://github.com/ROCm/aiter/pull/7544) pipeline scale loads in fused a8w8 blockscale + a16w16
- [#7489](https://github.com/ROCm/aiter/pull/7489) fused_clamp_act_mul accepts whole quant groups
- [#7629](https://github.com/ROCm/aiter/pull/7629) fused_clamp_act_mul avoids per-row recompiles

</details>

<details>
<summary>Newly opened: MLA decode LDS race fixes (5)</summary>

- [#7621](https://github.com/ROCm/aiter/pull/7621) FP8 QH16 qseqlen2 MLA decode
- [#7622](https://github.com/ROCm/aiter/pull/7622) FP8 QH16 qseqlen1 persistent MLA decode
- [#7623](https://github.com/ROCm/aiter/pull/7623) MFMA operand race in qseqlen4 v3 MLA decode
- [#7617](https://github.com/ROCm/aiter/pull/7617) FP8 QH16 qseqlen1 MLA decode
- [#7613](https://github.com/ROCm/aiter/pull/7613) merge only splits written by gfx950 fp8 gqa16 stage 1

</details>

<details>
<summary>Newly opened: communication, DeepSeek compressor & misc (14)</summary>

- [#7499](https://github.com/ROCm/aiter/pull/7499) gfx1250 Lamport AR+RMSNorm
- [#7488](https://github.com/ROCm/aiter/pull/7488) fold residual add into gfx1250 all-reduce
- [#7555](https://github.com/ROCm/aiter/pull/7555) gfx1250 LL all-gather lines carry 12 bytes and one flag
- [#7573](https://github.com/ROCm/aiter/pull/7573) gfx1250 Mega-MHC XCD-local and clustered split tiles
- [#7575](https://github.com/ROCm/aiter/pull/7575) FlyDSL V4.1 CSA main compressor
- [#7523](https://github.com/ROCm/aiter/pull/7523) validate two-stage DeepSeek-V4 compressor scratch buffer
- [#7524](https://github.com/ROCm/aiter/pull/7524) reject use_fp4_cache in DeepSeek-V4 compressor
- [#7522](https://github.com/ROCm/aiter/pull/7522) honor overlap in two-stage DeepSeek-V4 compressor
- [#7614](https://github.com/ROCm/aiter/pull/7614) gfx950 FP8 blockscale selections for DSv4 decode
- [#7581](https://github.com/ROCm/aiter/pull/7581) retune DSv4.1-Flash EP4 a4w4 MoE rows
- [#7582](https://github.com/ROCm/aiter/pull/7582) add DSv4.1-Flash EP8 a4w4 MoE rows
- [#7576](https://github.com/ROCm/aiter/pull/7576) sample: exponential top bucket maps to positive sample
- [#7612](https://github.com/ROCm/aiter/pull/7612) MHA varlen forward copies zero-stride inputs
- [#7552](https://github.com/ROCm/aiter/pull/7552) getPaddedM falls back to M=16 row

</details>

<details>
<summary>Newly opened: tuning configs (16)</summary>

- [#7492](https://github.com/ROCm/aiter/pull/7492) gfx1201 gemm_a16w16 shape-specific configs
- [#7628](https://github.com/ROCm/aiter/pull/7628) gfx1151 gemm_a16w16 configs and DEFAULT.json re-pick
- [#7577](https://github.com/ROCm/aiter/pull/7577) gfx1201 gemm_a16w4 configs
- [#7502](https://github.com/ROCm/aiter/pull/7502) gfx1201 batched_gemm_a16w16 configs
- [#7627](https://github.com/ROCm/aiter/pull/7627) gfx1150 batched_gemm_a16w16 configs
- [#7585](https://github.com/ROCm/aiter/pull/7585) gfx1201 SonicMoE config
- [#7626](https://github.com/ROCm/aiter/pull/7626) gfx1151 SonicMoE grouped-GEMM buckets
- [#7511](https://github.com/ROCm/aiter/pull/7511) gfx1201 fused_sigmoid_mul config
- [#7597](https://github.com/ROCm/aiter/pull/7597) gfx1201 sparse_mla_dsv4_train config
- [#7625](https://github.com/ROCm/aiter/pull/7625) gfx1151 sparse_mla_dsv4_train num_warps 2
- [#7513](https://github.com/ROCm/aiter/pull/7513) gfx950 gemm_a16w16 for kimik3/glm5/qwen3.5 shapes
- [#7514](https://github.com/ROCm/aiter/pull/7514) gfx1250 a16w16 GEMMs for Kimi K2 on 96 CUs
- [#7515](https://github.com/ROCm/aiter/pull/7515) Kimi-K3 gfx950 BF16 decode rows
- [#7538](https://github.com/ROCm/aiter/pull/7538) per-model A4W4 GEMM configs behind a public API
- [#7549](https://github.com/ROCm/aiter/pull/7549) pack gfx1250 varlen ASM LSE only when returned
- [#7531](https://github.com/ROCm/aiter/pull/7531) mega_moe S1F decode step snapping

</details>

<details>
<summary>Newly opened: CI, build, JIT & tooling (17)</summary>

- [#7526](https://github.com/ROCm/aiter/pull/7526) extract C++ in OPUS generators to jinja templates
- [#7484](https://github.com/ROCm/aiter/pull/7484) route five ops through the JIT provider interface
- [#7600](https://github.com/ROCm/aiter/pull/7600) bump FlyDSL pin to v0.5.0
- [#7508](https://github.com/ROCm/aiter/pull/7508) [DO NOT MERGE] test amd runtime on toolkit runner
- [#7560](https://github.com/ROCm/aiter/pull/7560) area contacts, review guide and merge rules
- [#7563](https://github.com/ROCm/aiter/pull/7563) review-pr: route the design judgment
- [#7615](https://github.com/ROCm/aiter/pull/7615) review-pr: queue notice fix
- [#7568](https://github.com/ROCm/aiter/pull/7568) install amd-mori 1.2.5 for multi-GPU tests
- [#7525](https://github.com/ROCm/aiter/pull/7525) validate-kernel-pr identity gate fix
- [#7571](https://github.com/ROCm/aiter/pull/7571) update ruff version in contribution guidelines
- [#7561](https://github.com/ROCm/aiter/pull/7561) fix AOT mm out_dtype replay on torch 2.9.1
- [#7493](https://github.com/ROCm/aiter/pull/7493) raise a GPU fault from the power-sampling pass
- [#7528](https://github.com/ROCm/aiter/pull/7528) failed arch probe no longer breaks GPU-less imports
- [#7630](https://github.com/ROCm/aiter/pull/7630) add arch_info.is_cdna3()
- plus 3 more minor tooling updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 5d954e4cc75801f7fa77c0775d22f571c85408082a3fcd11c4bde9db36950b95 -->
