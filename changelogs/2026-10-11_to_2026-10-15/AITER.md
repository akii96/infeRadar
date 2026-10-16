# AITER: PR digest (2026-10-11 to 2026-10-15)

_119 merged, 116 newly opened - source ROCm/AITER, generated 2026-10-15T14:03:21Z_

## TL;DR
- **Model attention:** DeepSeek (V4.1 / DSR1) and Kimi-K3 lead, followed by GLM-5.x, MiniMax-M3 and Qwen3.5/3.8. Most of it is merged GEMM and fused-MoE tuning, plus MiniMax-M3 indexer kernels and Kimi-K3 KDA work (new, open).
- **Biggest merged perf work:** FP8 mxscale BMM bpreshuffle (`[#4747](https://github.com/ROCm/aiter/pull/4747)`), the FlyDSL comm-fused MoE stage2 reduce-scatter for DSv4 (`[#5907](https://github.com/ROCm/aiter/pull/5907)`), MLA v6 for gfx950/gfx1250 (`[#6394](https://github.com/ROCm/aiter/pull/6394)`), and the ~9.5x faster MXFP4 FMoE AOT tuning (`[#6405](https://github.com/ROCm/aiter/pull/6405)`).
- **Hardware focus:** gfx950 (MI355) and gfx1250 are both heavily targeted, with FlyDSL and Gluon as the main kernel backends. Many tuned-config PRs and MLA/PA asm fixes landed.
- **Opened this window:** large in-progress work includes MegaMoE variants on gfx1250, SonicMoE fwd/bwd, gfx950 BF16 MoE training backward, MHAv4, QSA sparse attention, and a huge MXFP4 integration port (`[#6461](https://github.com/ROCm/aiter/pull/6461)`).
- **Direction:** moving to FlyDSL/Gluon kernels with per-model tuning, while tightening correctness (NaN and tail-handling fixes) and CI.

## Most important PRs
**`[#4747](https://github.com/ROCm/aiter/pull/4747)` FP8 mxscale BMM bpreshuffle optimization (JIT/OPUS)**
Adds an OPUS-based FP8 mxscale batched GEMM with B-preshuffle across gfx942, gfx950 and gfx1250. It targets DeepSeek MLA BMM shapes and is the largest merged kernel change.

**`[#5907](https://github.com/ROCm/aiter/pull/5907)` Comm-fused MoE stage2 reduce-scatter for DSv4 DPA (FlyDSL)**
Fuses the stage2 MoE GEMM with the reduce-scatter communication on gfx950. This removes a separate collective for DeepSeek V4 data-parallel attention.

**`[#6394](https://github.com/ROCm/aiter/pull/6394)` MLA version 6 (ASM/HIP/JIT)**
Updates the MLA asm path for gfx950 and gfx1250, with quantized KV support. It follows `[#6133](https://github.com/ROCm/aiter/pull/6133)`, which adds a gfx1250 QH128 page64 MLA with a unified decode API.

**`[#6405](https://github.com/ROCm/aiter/pull/6405)` MXFP4 FMoE AOT tuning ~9.5x faster on gfx950**
Speeds up CK/FlyDSL MXFP4 fused-MoE tuning, shortening the retune cycle for new MoE models such as GLM.

**`[#6050](https://github.com/ROCm/aiter/pull/6050)` HY4 MXFP8 heterogeneous MoE fusion (FlyDSL)**
Adds a new fused MoE kernel for MXFP8 heterogeneous experts, with tests and CI wiring.

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#6121](https://github.com/ROCm/aiter/pull/6121) fuse gfx1250 gather_kv_b_proj in FlyDSL
- [#6431](https://github.com/ROCm/aiter/pull/6431) MegaMoE stage1: fold ready-order tile wait into scheduler block
- [#6500](https://github.com/ROCm/aiter/pull/6500) cache gfx1250 Gluon MoE A8W4 layouts
- [#6480](https://github.com/ROCm/aiter/pull/6480) cache gfx1250 Gluon MXFP4 preshuffle GEMM layouts
- [#6338](https://github.com/ROCm/aiter/pull/6338) MoE layout LRU cache and tuning
- [#6443](https://github.com/ROCm/aiter/pull/6443) use 1x512 Gluon MXFP4 quant tiles for M<=2
- [#6240](https://github.com/ROCm/aiter/pull/6240) TDM store in bf16 BMM, tuned for DSR1 shapes
- [#6300](https://github.com/ROCm/aiter/pull/6300) default RMSNorm BF16 stores to optimized RNE
- [#6225](https://github.com/ROCm/aiter/pull/6225) move a4w4 aux-sort fused/Opus crossover to 1.33 rows per expert
</details>

<details>
<summary>Kernels & attention (27)</summary>

- [#5626](https://github.com/ROCm/aiter/pull/5626) FlyDSL M3 index score for MiniMax
- [#6359](https://github.com/ROCm/aiter/pull/6359) context-parallel block selection for MiniMax-M3 indexer
- [#6329](https://github.com/ROCm/aiter/pull/6329) single-launch dynamic decode TopK
- [#5715](https://github.com/ROCm/aiter/pull/5715) Gluon paged-decode attention with sigmoid gate and group-128 FP8 epilogue
- [#6226](https://github.com/ROCm/aiter/pull/6226) Gluon mhc_fused_post_pre
- [#6442](https://github.com/ROCm/aiter/pull/6442) optimized Gluon backend for mhc_fused_post_pre
- [#4772](https://github.com/ROCm/aiter/pull/4772) dense BF16 x MXFP4 GEMM in FlyDSL
- [#6101](https://github.com/ROCm/aiter/pull/6101) gfx950 asm GEMM, BF16 activations x FP8 weights for decode
- [#6470](https://github.com/ROCm/aiter/pull/6470) page16 PA_PS kernel and tests
- [#6477](https://github.com/ROCm/aiter/pull/6477) PA PS page16 reduce CO
- [#6473](https://github.com/ROCm/aiter/pull/6473) PA PS page16 CO variants
- [#4968](https://github.com/ROCm/aiter/pull/4968) PA Q/K D192 with asymmetric K/V head dim
- [#5614](https://github.com/ROCm/aiter/pull/5614) fix non-preshuffle MQA paging, retune decode grid
- [#6336](https://github.com/ROCm/aiter/pull/6336) gfx950 unified attention for spec decode
- [#6343](https://github.com/ROCm/aiter/pull/6343) fused rmsnorm + add + rmsnorm (Muse)
- [#6290](https://github.com/ROCm/aiter/pull/6290) Muse QK norm scale in fused RoPE cache op
- [#6288](https://github.com/ROCm/aiter/pull/6288) gfx1250 MLA head-tiled q_pe rope with bf16-round FP8 GEMM epilogue
- [#6276](https://github.com/ROCm/aiter/pull/6276) conflict-free bf16 KV-tile stores in sparse_mla
- [#6042](https://github.com/ROCm/aiter/pull/6042) avoid peeled sparse MLA spill below triton 3.8
- [#6220](https://github.com/ROCm/aiter/pull/6220) gfx942 BF16 MLA persistent decode asm kernel with LSE
- [#6109](https://github.com/ROCm/aiter/pull/6109) tune fused_reduce_qk_norm_rope_swa_write on gfx950
- [#6400](https://github.com/ROCm/aiter/pull/6400) sage_quant uses each tensor's own strides
- [#6169](https://github.com/ROCm/aiter/pull/6169) dispatch LayerNorm to Triton on gfx1250 or ENABLE_CK=0
- [#6250](https://github.com/ROCm/aiter/pull/6250) chunk_kda gfx1250 reinterpret
- [#6289](https://github.com/ROCm/aiter/pull/6289) enable fp fusion for KDA
- [#6017](https://github.com/ROCm/aiter/pull/6017) tune prefill num_warps on gfx950
- [#5624](https://github.com/ROCm/aiter/pull/5624) strided leading dimensions in GDN L2Norm
</details>

<details>
<summary>MoE & quantization (15)</summary>

- [#6165](https://github.com/ROCm/aiter/pull/6165) fused route-sort + MXFP4 activation-quant kernel
- [#4980](https://github.com/ROCm/aiter/pull/4980) A4W4 mega_moe operator
- [#5693](https://github.com/ROCm/aiter/pull/5693) herd_fused_topk selector for fused_moe 2-stage
- [#6131](https://github.com/ROCm/aiter/pull/6131) specialized gfx1250 biased sigmoid top-k
- [#6115](https://github.com/ROCm/aiter/pull/6115) fused G2L LUT extended to 1024 experts
- [#6357](https://github.com/ROCm/aiter/pull/6357) row-major A1 e8m0 scale store for gfx1250 decode MoE
- [#6269](https://github.com/ROCm/aiter/pull/6269) FlyDSL MoE v1 (gfx1250)
- [#4124](https://github.com/ROCm/aiter/pull/4124) torch-free a4w4 GEMM and C++ library build
- [#6472](https://github.com/ROCm/aiter/pull/6472) gemma_norm in fused all-reduce + RMSNorm + per-group FP8 quant
- [#6258](https://github.com/ROCm/aiter/pull/6258) FP32 partials for gfx1250 A8W8 split-K GEMMs
- [#6407](https://github.com/ROCm/aiter/pull/6407) mxfp8 w_scale 1*32 in FlyDSL
- [#6376](https://github.com/ROCm/aiter/pull/6376) Relu2 Tier 2 MoE GEMM (re-submit)
- [#6460](https://github.com/ROCm/aiter/pull/6460) revert of [#6376](https://github.com/ROCm/aiter/pull/6376)
- [#5804](https://github.com/ROCm/aiter/pull/5804) kmk3 EP MoE fix and gemm2 optimization
- [#5873](https://github.com/ROCm/aiter/pull/5873) stop split-K tail at K in blockscale GEMMs
</details>

<details>
<summary>Model support & tuning configs (28)</summary>

- [#6128](https://github.com/ROCm/aiter/pull/6128) Triton/Gluon tuning from the default config json
- [#6245](https://github.com/ROCm/aiter/pull/6245) gfx1201 GEMM A8W8 configs
- [#6156](https://github.com/ROCm/aiter/pull/6156) Qwen3.8-27B bf16 GEMM on gfx950
- [#6033](https://github.com/ROCm/aiter/pull/6033) Qwen3.8-27B a8w8 blockscale B-preshuffle GEMM
- [#6201](https://github.com/ROCm/aiter/pull/6201) Qwen3.8-Flash-Next bf16 GEMM
- [#6393](https://github.com/ROCm/aiter/pull/6393) re-tune 136 unparseable Qwen3.5-397B a8w8 rows
- [#6235](https://github.com/ROCm/aiter/pull/6235) MiniMax-M3 master BF16 GEMM table and ViT projections
- [#6409](https://github.com/ROCm/aiter/pull/6409) Kimi-K3 FP4 shared-expert GEMM
- [#6494](https://github.com/ROCm/aiter/pull/6494) split-K epilogue optimization and Kimi-K3 router/in_proj tune
- [#5903](https://github.com/ROCm/aiter/pull/5903) Kimi-K3 small-M BF16 GEMM
- [#5956](https://github.com/ROCm/aiter/pull/5956) retune Kimi-K3 merged-front shapes for ROCm 10
- [#6438](https://github.com/ROCm/aiter/pull/6438) gfx1250 A4W4 grouped-MoE for Kimi-K3 WideEP
- [#5982](https://github.com/ROCm/aiter/pull/5982) GLM-5.3-Flash TP4 fused KDA in-proj
- [#5994](https://github.com/ROCm/aiter/pull/5994) GLM-5.2-FP8 a8w8 blockscale
- [#6077](https://github.com/ROCm/aiter/pull/6077) GLM-5.3-Flash TP2 fused-MoE
- [#6392](https://github.com/ROCm/aiter/pull/6392) GLM-5 MXFP4 EP4 rows keyed on topk 9
- [#5928](https://github.com/ROCm/aiter/pull/5928) Gemma-4-31B a4w4 blockscale
- [#5960](https://github.com/ROCm/aiter/pull/5960) gfx1101 gemm_a8w8
- [#6190](https://github.com/ROCm/aiter/pull/6190) retune DSV3 fused-shared-expert rows on gfx942
- [#6547](https://github.com/ROCm/aiter/pull/6547) tune a8w8 bpreshuffle GEMMs
- [#6002](https://github.com/ROCm/aiter/pull/6002) sparse MLA prefill tuned for DSv4.1-Flash TP4, attn_sink fix
- [#6293](https://github.com/ROCm/aiter/pull/6293) gfx1250 config cleanup
- [#6396](https://github.com/ROCm/aiter/pull/6396) gfx1250 candidates in A16W16 tuning policy
- [#6365](https://github.com/ROCm/aiter/pull/6365) check single-file tuned configs for duplicate shapes
- [#6495](https://github.com/ROCm/aiter/pull/6495) run only retuned kernels' tests for config-only PRs
- [#6541](https://github.com/ROCm/aiter/pull/6541) key comm-fused MoE winners by GPU model
- [#6517](https://github.com/ROCm/aiter/pull/6517) MORI all-to-all manager creation made demand-driven
- [#5431](https://github.com/ROCm/aiter/pull/5431) torch.symm_mem (mori) transport for custom_ar on gfx1250
</details>

<details>
<summary>Bugfixes (14)</summary>

- [#6422](https://github.com/ROCm/aiter/pull/6422) prevent gfx950 FP8 softmax underflow in MLA
- [#6528](https://github.com/ROCm/aiter/pull/6528) gfx950 page16 short-tail guards in PA
- [#6569](https://github.com/ROCm/aiter/pull/6569) gfx942 PA KV tail for lengths 241-255
- [#5399](https://github.com/ROCm/aiter/pull/5399) ff_a16w16_fused M<=8 launch failure
- [#5972](https://github.com/ROCm/aiter/pull/5972) restore shadowed OPUS A16W16 cache-policy registrations
- [#5936](https://github.com/ROCm/aiter/pull/5936) remove stale MXFP4 MoE aux sources
- [#6467](https://github.com/ROCm/aiter/pull/6467) initialize reverse route indices before Opus sorting
- [#6471](https://github.com/ROCm/aiter/pull/6471) topk_per_row_argmax early return on zero rows
- [#6321](https://github.com/ROCm/aiter/pull/6321) KDA gate pointer advances by token stride
- [#6406](https://github.com/ROCm/aiter/pull/6406) pa_prefill default device leak
- [#6425](https://github.com/ROCm/aiter/pull/6425) megamoe ubench
- [#6491](https://github.com/ROCm/aiter/pull/6491) shuffled kv cache in mla prefill bench
- [#6493](https://github.com/ROCm/aiter/pull/6493) HSTU test dtype failures
- [#6571](https://github.com/ROCm/aiter/pull/6571) skip comm-fused MoE test without MORI CCO
</details>

<details>
<summary>Refactors & cleanup (6)</summary>

- [#6505](https://github.com/ROCm/aiter/pull/6505) move common Triton/Gluon kernels into common/
- [#6378](https://github.com/ROCm/aiter/pull/6378) clean attention, compressor and recurrent kernel APIs
- [#6377](https://github.com/ROCm/aiter/pull/6377) FlyDSL typed memory/pointer API cleanup in comm kernels
- [#5166](https://github.com/ROCm/aiter/pull/5166) diagnose missing rocPRIM headers
- [#6349](https://github.com/ROCm/aiter/pull/6349) remove non-Triton prefill benchmark
- [#6420](https://github.com/ROCm/aiter/pull/6420) sparse prefill bandwidth in TB/s
</details>

<details>
<summary>CI, build & docs (15)</summary>

- [#6352](https://github.com/ROCm/aiter/pull/6352) review-pr answers requester at the gate
- [#6516](https://github.com/ROCm/aiter/pull/6516) review-pr names the withholding gate
- [#6408](https://github.com/ROCm/aiter/pull/6408) auto-update split test times
- [#6006](https://github.com/ROCm/aiter/pull/6006) py3 wheel without prebuilt kernels
- [#6242](https://github.com/ROCm/aiter/pull/6242) Windows smoke test for JIT ops
- [#6466](https://github.com/ROCm/aiter/pull/6466) Windows smoke accuracy diffs
- [#6457](https://github.com/ROCm/aiter/pull/6457) schedule Windows smoke daily
- [#6465](https://github.com/ROCm/aiter/pull/6465) skip OPUS test for unrelated workflow changes
- [#6418](https://github.com/ROCm/aiter/pull/6418) skip OPUS config on draft PRs
- [#6424](https://github.com/ROCm/aiter/pull/6424) bump FlyDSL to 0.4.0
- [#6499](https://github.com/ROCm/aiter/pull/6499) simplify triton docs
- [#5730](https://github.com/ROCm/aiter/pull/5730) Copilot FlyDSL path instructions
- [#6251](https://github.com/ROCm/aiter/pull/6251) bench_mla output buffer
- [#6284](https://github.com/ROCm/aiter/pull/6284) UA bench shuffled_kv_cache flag
- [#6133](https://github.com/ROCm/aiter/pull/6133) gfx1250 QH128 page64 MLA with unified decode API
</details>

<details>
<summary>Newly opened (in progress) (116)</summary>

- [#6461](https://github.com/ROCm/aiter/pull/6461) integration MXFP4 staged main port (~149k lines)
- [#6483](https://github.com/ROCm/aiter/pull/6483) gfx950 SonicMoE forward and backward
- [#6540](https://github.com/ROCm/aiter/pull/6540) FlyDSL all-reduce fusion
- [#6512](https://github.com/ROCm/aiter/pull/6512) gfx950 BF16 MoE training backward
- [#6464](https://github.com/ROCm/aiter/pull/6464) MXFP4 FlyDSL a8w4 optimization and replace
- [#6455](https://github.com/ROCm/aiter/pull/6455) MI355 MLA PS 4-wave FP8 kernel
- [#6550](https://github.com/ROCm/aiter/pull/6550) fused Kimi-K3 KDA whole-layer ops (gfx950, TP8)
- [#6498](https://github.com/ROCm/aiter/pull/6498) KDA chunk_delta_attn backward
- [#6506](https://github.com/ROCm/aiter/pull/6506) fused KDA decode extended to GLM-5.3
- [#6564](https://github.com/ROCm/aiter/pull/6564) gfx1250 MegaMoE fused dispatch+GEMM1 stage-1 kernel
- [#6514](https://github.com/ROCm/aiter/pull/6514) mega_moe_tp unified big-M path
- [#6430](https://github.com/ROCm/aiter/pull/6430) MegaMoE gfx1250 stage switches and mori combine
- [#6525](https://github.com/ROCm/aiter/pull/6525) mega_moe required_vmm_bytes
- [#6556](https://github.com/ROCm/aiter/pull/6556) MegaMoE dispatch payload fix
- [#6558](https://github.com/ROCm/aiter/pull/6558) MoonEP planner and weight pool on gfx1250 MegaMoE
- [#6563](https://github.com/ROCm/aiter/pull/6563) gfx1250 persistent MLA decode with BF16 and TP4/TP2 MTP
- [#6561](https://github.com/ROCm/aiter/pull/6561) gfx1250 QH64 shuffled KV decode
- [#6545](https://github.com/ROCm/aiter/pull/6545) pipelined unshuffled MLA decode on gfx1250
- [#6520](https://github.com/ROCm/aiter/pull/6520) fused Mega-MHC for DeepSeek V4.1
- [#6403](https://github.com/ROCm/aiter/pull/6403) two-launch FlyDSL delayed mHC seam for gfx942
- [#6576](https://github.com/ROCm/aiter/pull/6576) QSA sparse prefill attention for MI308
- [#6469](https://github.com/ROCm/aiter/pull/6469) QSA paged sparse attention kernels
- [#6515](https://github.com/ROCm/aiter/pull/6515) QSA paged MQA logits MFMA scorer
- [#6575](https://github.com/ROCm/aiter/pull/6575) MHAv4 per-row block-sparse geometry on gfx950
- [#6560](https://github.com/ROCm/aiter/pull/6560) MHAv4 split-KV
- [#6534](https://github.com/ROCm/aiter/pull/6534) MHAv4 BSHD input requirement
- [#6580](https://github.com/ROCm/aiter/pull/6580) MHA forward tuning via shared contract
- [#6502](https://github.com/ROCm/aiter/pull/6502) streamline flash attention API
- [#6522](https://github.com/ROCm/aiter/pull/6522) gfx942 FMHA varlen backward for head dims 64..192
- [#6454](https://github.com/ROCm/aiter/pull/6454) gfx1250 MHA bwd kernel integration
- [#6508](https://github.com/ROCm/aiter/pull/6508) MHA FP8 subtiled kernel
- [#6510](https://github.com/ROCm/aiter/pull/6510) 8-wave ping-pong mxfp8 GEMM (gfx1250)
- [#6462](https://github.com/ROCm/aiter/pull/6462) gfx1250 paged attention decode with FP8/BF16
- [#6476](https://github.com/ROCm/aiter/pull/6476) MXFP4 dequant H16 requantization
- [#6458](https://github.com/ROCm/aiter/pull/6458) dual-layout H16 MXFP4 quantization
- [#6527](https://github.com/ROCm/aiter/pull/6527) HERD for GPT-OSS on gfx1250
- [#6549](https://github.com/ROCm/aiter/pull/6549) gfx1250 Gluon a16w16 GEMMs for GPT-OSS 120B
- [#6496](https://github.com/ROCm/aiter/pull/6496) gfx950 GDN fused prefill kernel
- [#6488](https://github.com/ROCm/aiter/pull/6488) fused GDN decode for any value/key head ratio
- [#6421](https://github.com/ROCm/aiter/pull/6421) conv3d LDS reuse on gfx950
- [#6427](https://github.com/ROCm/aiter/pull/6427) GLM-5.2 QKV proj optimization
- [#6426](https://github.com/ROCm/aiter/pull/6426) GLM-5.2 o_proj optimization
- [#6552](https://github.com/ROCm/aiter/pull/6552) gfx942 a16wmix/a16w16 swiglu_limit
- [#6484](https://github.com/ROCm/aiter/pull/6484) fused_moe takes precomputed BM=16 sort
- [#6485](https://github.com/ROCm/aiter/pull/6485) a4w4 adaptive aux sort accumulates into caller's output
- [#6437](https://github.com/ROCm/aiter/pull/6437) gemm_a8w8_bpreshuffle_out
- [#6538](https://github.com/ROCm/aiter/pull/6538) tuned_gemm writes a16w16 into caller-owned buffer
- [#6416](https://github.com/ROCm/aiter/pull/6416) fused_indexed_gated_residual (Triton/Gluon)
- [#6417](https://github.com/ROCm/aiter/pull/6417) fused_indexed_gated_residual (HIP/JIT)
- [#6504](https://github.com/ROCm/aiter/pull/6504) Triton Conv2D padding primitives
- [#6551](https://github.com/ROCm/aiter/pull/6551) GEMM benchmark rotating buffers
- [#6501](https://github.com/ROCm/aiter/pull/6501) fused_bmm_rope_kv_cache tuning
- [#6487](https://github.com/ROCm/aiter/pull/6487) Gluon PA benchmark for asymmetric K/V
- [#6434](https://github.com/ROCm/aiter/pull/6434) PA decode PS split on whole partitions
- [#6453](https://github.com/ROCm/aiter/pull/6453) PA decode fills GPU in get_recommended_splits
- [#6445](https://github.com/ROCm/aiter/pull/6445) Gluon PA decode ragged query
- [#6444](https://github.com/ROCm/aiter/pull/6444) PA decode PS reduce query_start_loc
- [#6451](https://github.com/ROCm/aiter/pull/6451) Triton paged MQA logits (B, next_n) context lengths
- [#6450](https://github.com/ROCm/aiter/pull/6450) FlyDSL paged MQA logits (B, next_n) context lengths
- [#6533](https://github.com/ROCm/aiter/pull/6533) OPUS FP4 MQA writer and query scale layouts
- [#6404](https://github.com/ROCm/aiter/pull/6404) hidden 6144 in INT4 QuickReduce + RMSNorm epilogue
- [#6570](https://github.com/ROCm/aiter/pull/6570) max tp64 on all-gather
- [#6446](https://github.com/ROCm/aiter/pull/6446) ar_ll128_unroll2 hang fix
- [#6398](https://github.com/ROCm/aiter/pull/6398) bind load_hip_runtime to loaded HIP runtime
- [#6511](https://github.com/ROCm/aiter/pull/6511) deterministic MXFP4 MoE stage2 epilogue
- [#6568](https://github.com/ROCm/aiter/pull/6568) initialize padded MoE scratch (gfx950 a8w4)
- [#6519](https://github.com/ROCm/aiter/pull/6519) bound scatter-reduce staging reads
- [#6478](https://github.com/ROCm/aiter/pull/6478) SwiGLU CK-Tile MXFP4 dispatch fix
- [#6395](https://github.com/ROCm/aiter/pull/6395) grouped MoE tuning results written in place
- [#6532](https://github.com/ROCm/aiter/pull/6532) report online fmoe tune failures
- [#6572](https://github.com/ROCm/aiter/pull/6572) grouped fmoe tuner fp32 topk weights
- [#6468](https://github.com/ROCm/aiter/pull/6468) Qwen3.8 TP=8 MXFP4 MoE aux kernel codegen
- [#6526](https://github.com/ROCm/aiter/pull/6526) gfx1250 prequantized a1 row copy, 8-wave gemm1 for EP4
- [#6567](https://github.com/ROCm/aiter/pull/6567) optimize FlyDSL grouped MoE kernels
- [#6537](https://github.com/ROCm/aiter/pull/6537) FlyDSL MoE v2
- [#6543](https://github.com/ROCm/aiter/pull/6543) FlyDSL Kimi K2 Thinking kernel
- [#6419](https://github.com/ROCm/aiter/pull/6419) a4w4 triton_preshuffle routing, Qwen3.8-27B rows
- [#6456](https://github.com/ROCm/aiter/pull/6456) zero-pad XQ to padded weight K for a8w8 bpreshuffle
- [#6539](https://github.com/ROCm/aiter/pull/6539) cross-wave LDS race in 8-wave GEMM
- [#6475](https://github.com/ROCm/aiter/pull/6475) mask V page tail in unified_attention
- [#6566](https://github.com/ROCm/aiter/pull/6566) zero empty decode rows in unified attention
- [#6581](https://github.com/ROCm/aiter/pull/6581) normalize Gluon split constexpr values
- [#6428](https://github.com/ROCm/aiter/pull/6428) NaN dq in Triton MHA backward
- [#6401](https://github.com/ROCm/aiter/pull/6401) mask out-of-range keys in non-causal flash attention backward
- [#6486](https://github.com/ROCm/aiter/pull/6486) Gluon PA AOT compatibility for asymmetric K/V
- [#6524](https://github.com/ROCm/aiter/pull/6524) gfx942 BF16 decode dispatch for GQA 64
- [#6481](https://github.com/ROCm/aiter/pull/6481) gfx950 MLA KV addressing
- [#6536](https://github.com/ROCm/aiter/pull/6536) gfx950 bf16 opus MLA decode with named-register pins
- [#6577](https://github.com/ROCm/aiter/pull/6577) SGPR counts in gfx950 QH16 MLA metadata
- [#6578](https://github.com/ROCm/aiter/pull/6578) gfx950 BF16 32-head MLA KV addressing
- [#6579](https://github.com/ROCm/aiter/pull/6579) JIT build hang on zombie lock holder
- [#6397](https://github.com/ROCm/aiter/pull/6397) FlyDSL BF16 GEMM default for large untuned gfx1250 shapes
- [#6530](https://github.com/ROCm/aiter/pull/6530) Kimi-K3 gfx1250 mxfp8_128 blockscale tuning
- [#6573](https://github.com/ROCm/aiter/pull/6573) gfx1250 Kimi-K2 TP8 Gluon GEMM
- [#6410](https://github.com/ROCm/aiter/pull/6410) Kimi-K3 A8W8 bpreshuffle configs
- [#6411](https://github.com/ROCm/aiter/pull/6411) Kimi-K3 BF16 GEMM configs
- [#6435](https://github.com/ROCm/aiter/pull/6435) GLM-5.3-Flash MXFP4 fused-MoE configs
- [#6535](https://github.com/ROCm/aiter/pull/6535) MI300A GLM-5.3 FP8 configs
- [#6436](https://github.com/ROCm/aiter/pull/6436) GLM-5.3 Flash router GEMM
- [#6523](https://github.com/ROCm/aiter/pull/6523) GLM-5.2 MTP verify configs
- [#6529](https://github.com/ROCm/aiter/pull/6529) MiniMax-M3 TP=2 decode FMOE shapes
- [#6531](https://github.com/ROCm/aiter/pull/6531) MiniMax-M3 ViT BF16 GEMM
- [#6509](https://github.com/ROCm/aiter/pull/6509) Qwen3 480B bf16 GEMM
- [#6546](https://github.com/ROCm/aiter/pull/6546) Llama-3.1-405B MXFP4 TP8 AFP4WFP4 GEMM
- [#6521](https://github.com/ROCm/aiter/pull/6521) retune AFP4WFP4 N=4096, K=14336
- [#6507](https://github.com/ROCm/aiter/pull/6507) Muse projection GEMM tuning
- [#6433](https://github.com/ROCm/aiter/pull/6433) DSV4.1 Flash TP4 a8w4 FMoE
- [#6544](https://github.com/ROCm/aiter/pull/6544) DSR1 FP4 TP8 fused MoE
- [#6557](https://github.com/ROCm/aiter/pull/6557) DeepSeek-R1 FP4 MoE tiles for gfx1250
- [#6555](https://github.com/ROCm/aiter/pull/6555) Triton tuning relative to default
- [#6553](https://github.com/ROCm/aiter/pull/6553) tuning preempt local best
- [#6554](https://github.com/ROCm/aiter/pull/6554) tuning search space
- [#6482](https://github.com/ROCm/aiter/pull/6482) pretune fails on tuner errors
- [#6479](https://github.com/ROCm/aiter/pull/6479) test_topk_row_prefill failure reporting
- [#6513](https://github.com/ROCm/aiter/pull/6513) Windows smoke test fails without GPU
- [#6542](https://github.com/ROCm/aiter/pull/6542) CLAUDE.md file precedence
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: bfc341580a8fcde9ec1cdbe5910ccd270b7e509374bd8c0729cf99d53418316c -->
