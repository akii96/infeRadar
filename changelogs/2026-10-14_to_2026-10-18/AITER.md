# AITER: PR digest (2026-10-14 to 2026-10-18)

_81 merged, 108 newly opened - source ROCm/AITER, generated 2026-10-18T22:54:51Z_

## TL;DR
- **DeepSeek (V4/V4.1/R1), Kimi-K3, MiniMax-M3 and GLM-5.x** got the most attention. Most of the work is MXFP8/MXFP4 GEMMs and MoE, MLA decode, and tuned configs for gfx950 and the new gfx1250.
- **Biggest merged perf work:** the FP8 mxscale batched-GEMM bpreshuffle rewrite ([#4747](https://github.com/ROCm/aiter/pull/4747)), the 4-wave FP8 MLA persistent-split kernel for MI355 ([#6455](https://github.com/ROCm/aiter/pull/6455)), and a ~9.5x faster MXFP4 FMoE AOT tuner ([#6405](https://github.com/ROCm/aiter/pull/6405)). Packed 2-bit MoE kernels for GLM-5.3 also landed ([#5728](https://github.com/ROCm/aiter/pull/5728)).
- **gfx1250 is the main bring-up target.** Merged: QH64/QH128 MLA decode, a fused QK-norm/RoPE/MLA-cache kernel, and Gluon MoE layout caching. Open: fused MegaMoE dispatch+GEMM1, persistent MLA decode with BF16 and MTP, and MXFP4 a4w4 GEMM.
- **Open pipeline:** a gfx950 BF16 MoE training backward ([#6512](https://github.com/ROCm/aiter/pull/6512)), a fused Mega-MHC for DSv4.1 ([#6520](https://github.com/ROCm/aiter/pull/6520)), fused Kimi-K3 KDA whole-layer ops ([#6550](https://github.com/ROCm/aiter/pull/6550)), and large FlyDSL all-reduce fusion ([#6540](https://github.com/ROCm/aiter/pull/6540)).
- **Direction:** FlyDSL and Gluon are taking over from CK/ASM, with deterministic MoE modes, correctness fixes in ASM PA/MLA, and shared MHA tuning infrastructure.

## Most important PRs
**[#4747](https://github.com/ROCm/aiter/pull/4747) — Fp8 mxscale bmm bpreshuffle opt (merged)**
Large OPUS/JIT rework of FP8 mxscale batched GEMM with preshuffled B, touching gfx942/950/1250 and tuned configs. It targets the DeepSeek MLA batched-GEMM path.

**[#6455](https://github.com/ROCm/aiter/pull/6455) — MI355 MLA PS mode 4-wave FP8 kernel (merged)**
Adds a 4-wave FP8 ASM kernel for persistent-split MLA decode on gfx950, improving FP8 MLA decode occupancy and throughput.

**[#5728](https://github.com/ROCm/aiter/pull/5728) — IQ2R glm53_moe packed 2-bit MoE kernels (merged)**
Packed 2-bit BF16 MoE kernels for GLM-5.3 at TP4/TP8, a very aggressive weight-compression path that cuts memory and bandwidth.

**[#6405](https://github.com/ROCm/aiter/pull/6405) — Accelerate MXFP4 FMoE AOT tuning ~9.5x (merged)**
Cuts gfx950 MXFP4 fused-MoE tuning time by about 9.5x, which speeds up config coverage for new models.

**[#6564](https://github.com/ROCm/aiter/pull/6564) — Fuse gfx1250 compact dispatch + GEMM1 into one stage-1 kernel (open)**
Merges MegaMoE token dispatch with the first expert GEMM on gfx1250. This removes a kernel boundary and intermediate traffic in the WideEP path.

## More changes by area

<details>
<summary>Performance (8)</summary>

- [#6619](https://github.com/ROCm/aiter/pull/6619) optimize FlyDSL PA partition reduction
- [#6121](https://github.com/ROCm/aiter/pull/6121) fuse gfx1250 gather_kv_b_proj in FlyDSL
- [#6500](https://github.com/ROCm/aiter/pull/6500) cache gfx1250 Gluon MoE A8W4 layouts
- [#6453](https://github.com/ROCm/aiter/pull/6453) PA decode uses more splits for small grids
- [#6648](https://github.com/ROCm/aiter/pull/6648) replace contended per-tensor scale atomics with partial reduction (open)
- [#6656](https://github.com/ROCm/aiter/pull/6656) scaled_silu_and_mul splits short batches across workgroups (open)
- [#6597](https://github.com/ROCm/aiter/pull/6597) cache gfx950 A16W16 GEMM param per config (open)
- [#6605](https://github.com/ROCm/aiter/pull/6605) swap A/B in mxfp8 8-wave epilogue for 64-bit stores (open)

</details>

<details>
<summary>Kernels & attention (40)</summary>

- [#6603](https://github.com/ROCm/aiter/pull/6603) add 32x32/128x128 mxfp8 and tune bmm(batch=1)
- [#6407](https://github.com/ROCm/aiter/pull/6407) add mxfp8 w_scale 1x32
- [#5626](https://github.com/ROCm/aiter/pull/5626) M3 index score in FlyDSL
- [#6561](https://github.com/ROCm/aiter/pull/6561) gfx1250 QH64 shuffled KV decode
- [#6133](https://github.com/ROCm/aiter/pull/6133) gfx1250 QH128 page64 MLA with unified decode API
- [#5978](https://github.com/ROCm/aiter/pull/5978) optimized qk-norm-rope MLA cache on gfx1250
- [#6329](https://github.com/ROCm/aiter/pull/6329) single-launch dynamic decode TopK
- [#6469](https://github.com/ROCm/aiter/pull/6469) paged sparse attention (QSA) kernels
- [#4772](https://github.com/ROCm/aiter/pull/4772) dense BF16 x MXFP4 GEMM on gfx950
- [#4968](https://github.com/ROCm/aiter/pull/4968) PA supports Q/K D192 with asymmetric V head dim
- [#6454](https://github.com/ROCm/aiter/pull/6454) gfx1250 MHA bwd kernel integration
- [#6470](https://github.com/ROCm/aiter/pull/6470) page16 PA_PS kernel and tests
- [#6477](https://github.com/ROCm/aiter/pull/6477) PA PS page16 reduce
- [#6473](https://github.com/ROCm/aiter/pull/6473) PA PS page16 CO variants
- [#6220](https://github.com/ROCm/aiter/pull/6220) gfx942 BF16 MLA persistent decode with LSE
- [#6131](https://github.com/ROCm/aiter/pull/6131) gfx1250 biased sigmoid top-k specialization
- [#6169](https://github.com/ROCm/aiter/pull/6169) dispatch LayerNorm to Triton on gfx1250
- [#6283](https://github.com/ROCm/aiter/pull/6283) tune mla_gluon
- [#6109](https://github.com/ROCm/aiter/pull/6109) tune fused_reduce_qk_norm_rope_swa_write
- [#6017](https://github.com/ROCm/aiter/pull/6017) tune prefill num_warps on gfx950
- [#6550](https://github.com/ROCm/aiter/pull/6550) fused Kimi-K3 KDA whole-layer ops (open)
- [#6609](https://github.com/ROCm/aiter/pull/6609) gfx1250 flash KDA Gluon (open)
- [#6563](https://github.com/ROCm/aiter/pull/6563) gfx1250 persistent MLA decode, BF16, TP4/TP2 MTP (open)
- [#6536](https://github.com/ROCm/aiter/pull/6536) rebuild gfx950 bf16 opus MLA decode (open)
- [#6576](https://github.com/ROCm/aiter/pull/6576) QSA sparse prefill for MI308 (open)
- [#6515](https://github.com/ROCm/aiter/pull/6515) QSA paged MQA logits MFMA scorer (open)
- [#6520](https://github.com/ROCm/aiter/pull/6520) fused Mega-MHC for DSv4.1 (open)
- [#6575](https://github.com/ROCm/aiter/pull/6575) MHAv4 per-row block-sparse, LSE, ragged KV (open)
- [#6560](https://github.com/ROCm/aiter/pull/6560) MHAv4 split-KV (open)
- [#6534](https://github.com/ROCm/aiter/pull/6534) MHAv4 requires BSHD inputs (open)
- [#6614](https://github.com/ROCm/aiter/pull/6614) fuse dvdk and dq with split-K pingpong (open)
- [#6522](https://github.com/ROCm/aiter/pull/6522) gfx942 FMHA varlen bwd for head dims 64..192 (open)
- [#6655](https://github.com/ROCm/aiter/pull/6655) packed D256 PA decode for gfx950 (open)
- [#6617](https://github.com/ROCm/aiter/pull/6617) extend packed D256 PA to page16, transposed V, sliding window (open)
- [#6545](https://github.com/ROCm/aiter/pull/6545) pipelined unshuffled MLA decode on gfx1250 (open)
- [#6594](https://github.com/ROCm/aiter/pull/6594) route short sliding-window queries to gfx950 split grid (open)
- [#6626](https://github.com/ROCm/aiter/pull/6626) paged MQA logits 8-token pages (open)
- [#6533](https://github.com/ROCm/aiter/pull/6533) OPUS FP4 MQA writer and query scale layouts (open)
- [#6510](https://github.com/ROCm/aiter/pull/6510) 8-wave ping-pong mxfp8 GEMM (open)
- [#6628](https://github.com/ROCm/aiter/pull/6628) optimize gfx1250 mxfp4 Gluon (open)

</details>

<details>
<summary>MoE & quantization (30)</summary>

- [#6050](https://github.com/ROCm/aiter/pull/6050) HY4 MXFP8 heterogeneous MoE fusion
- [#6165](https://github.com/ROCm/aiter/pull/6165) fused route-sort + MXFP4 activation quant
- [#4980](https://github.com/ROCm/aiter/pull/4980) A4W4 mega_moe operator
- [#6615](https://github.com/ROCm/aiter/pull/6615) MegaMoE scatter keeps planar scale runs on 128 B
- [#6225](https://github.com/ROCm/aiter/pull/6225) move a4w4 aux-sort crossover to 1.33 rows/expert
- [#6472](https://github.com/ROCm/aiter/pull/6472) gemma_norm in fused all-reduce + RMSNorm + FP8 quant
- [#6512](https://github.com/ROCm/aiter/pull/6512) gfx950 BF16 MoE training backward (open)
- [#6514](https://github.com/ROCm/aiter/pull/6514) mega_moe_tp unified big-M path (open)
- [#6558](https://github.com/ROCm/aiter/pull/6558) MoonEP planner and weight pool on gfx1250 MegaMoE (open)
- [#6527](https://github.com/ROCm/aiter/pull/6527) enable HERD on gfx1250 plus GPT-OSS selector (open)
- [#6642](https://github.com/ROCm/aiter/pull/6642) MXFP8 experts on gfx1250 (open)
- [#6567](https://github.com/ROCm/aiter/pull/6567) optimize FlyDSL grouped MoE (open)
- [#6537](https://github.com/ROCm/aiter/pull/6537) FlyDSL MoE v2 (open)
- [#6526](https://github.com/ROCm/aiter/pull/6526) gfx1250 MoE row copy, 8-wave gemm1 (open)
- [#6525](https://github.com/ROCm/aiter/pull/6525) required_vmm_bytes for cco sizing (open)
- [#6511](https://github.com/ROCm/aiter/pull/6511) deterministic MXFP4 MoE stage2 epilogue (open)
- [#6583](https://github.com/ROCm/aiter/pull/6583) deterministic mode for bf16 x MXFP4 MoE (open)
- [#6532](https://github.com/ROCm/aiter/pull/6532) report online fmoe tune failures (open)
- [#6552](https://github.com/ROCm/aiter/pull/6552) honour swiglu_limit on gfx942 (open)
- [#6621](https://github.com/ROCm/aiter/pull/6621) MXFP4 a4w4 GEMM with DSR1 configs on gfx1250 (open)
- [#6607](https://github.com/ROCm/aiter/pull/6607) gfx1250 192x256 no-ps, A4W4 dispatch fix (open)
- [#6582](https://github.com/ROCm/aiter/pull/6582) scale-mode args in hipb_mm (open)
- [#6538](https://github.com/ROCm/aiter/pull/6538) tuned_gemm writes a16w16 into caller buffer (open)
- [#6611](https://github.com/ROCm/aiter/pull/6611) fuse stage-2 input quant into stage-1 epilogue for DSv4.1Flash (open)
- [#6610](https://github.com/ROCm/aiter/pull/6610) bound a8w4 activation quant to live token count (open)
- [#6572](https://github.com/ROCm/aiter/pull/6572) grouped fmoe tuner passes fp32 topk weights (open)
- [#6584](https://github.com/ROCm/aiter/pull/6584) q_head_stride for fused QK-norm + MRoPE + KV-cache (open)
- [#6540](https://github.com/ROCm/aiter/pull/6540) FlyDSL all-reduce fusion (open)
- [#6570](https://github.com/ROCm/aiter/pull/6570) support max tp64 on all-gather (open)
- [#6640](https://github.com/ROCm/aiter/pull/6640) round custom all-reduce BF16 stores to nearest even (open)

</details>

<details>
<summary>Model support & tuning configs (70)</summary>

- [#6235](https://github.com/ROCm/aiter/pull/6235) MiniMax-M3 BF16 GEMM master table and ViT projections
- [#6546](https://github.com/ROCm/aiter/pull/6546) gfx950 AFP4WFP4 configs for Llama-3.1-405B TP8
- [#6549](https://github.com/ROCm/aiter/pull/6549) gfx1250 a16w16 for GPT-OSS 120B
- [#6494](https://github.com/ROCm/aiter/pull/6494) split-K epilogue optimization and Kimi-K3 router tune
- [#6411](https://github.com/ROCm/aiter/pull/6411) Kimi-K3 gfx950 BF16 GEMM
- [#5956](https://github.com/ROCm/aiter/pull/5956) retune Kimi-K3 merged-front shapes for ROCm 10
- [#6271](https://github.com/ROCm/aiter/pull/6271) gfx942 Kimi-K3 a16wi4 MoE topk=16
- [#6438](https://github.com/ROCm/aiter/pull/6438) gfx1250 A4W4 grouped MoE for Kimi-K3 WideEP
- [#5928](https://github.com/ROCm/aiter/pull/5928) Gemma-4-31B a4w4 blockscale tunings
- [#5994](https://github.com/ROCm/aiter/pull/5994) GLM-5.2-FP8 a8w8 blockscale tunings
- [#6521](https://github.com/ROCm/aiter/pull/6521) retune AFP4WFP4 N=4096,K=14336
- [#6547](https://github.com/ROCm/aiter/pull/6547) tune a8w8 bpreshuffle GEMMs
- [#6507](https://github.com/ROCm/aiter/pull/6507) tune Muse projection GEMMs
- [#4234](https://github.com/ROCm/aiter/pull/4234) gfx1100 A16W16 GEMM configs
- [#6588](https://github.com/ROCm/aiter/pull/6588) gfx1100 Conv3D tuning
- [#6531](https://github.com/ROCm/aiter/pull/6531) MiniMax-M3 ViT BF16 GEMM config (open)
- [#6585](https://github.com/ROCm/aiter/pull/6585) MiniMax-M3 AttnFP8 A8W8 configs (open)
- [#6604](https://github.com/ROCm/aiter/pull/6604) MiniMax-M3 non-fused MoE A4W4/A16W4 (open)
- [#6529](https://github.com/ROCm/aiter/pull/6529) MiniMax-M3 TP=2 decode FMOE (open)
- [#6623](https://github.com/ROCm/aiter/pull/6623) Qwen3.8-27B ViT GEMM (open)
- [#6638](https://github.com/ROCm/aiter/pull/6638) Qwen3.8-27B A4W4 on MI350P (open)
- [#6509](https://github.com/ROCm/aiter/pull/6509) Qwen3 480B bf16 GEMM (open)
- [#6612](https://github.com/ROCm/aiter/pull/6612) Qwen3.5 FP8 TP8 fused-MoE (open)
- [#6601](https://github.com/ROCm/aiter/pull/6601) DeepSeek-V4 K=7168 a16w16 (open)
- [#6544](https://github.com/ROCm/aiter/pull/6544) DSR1 FP4 TP8 fused MoE (open)
- [#6557](https://github.com/ROCm/aiter/pull/6557) DSR1 FP4 MoE high-batch decode (open)
- [#6622](https://github.com/ROCm/aiter/pull/6622) v41 tp2 MoE shared-expert fusion (open)
- [#6602](https://github.com/ROCm/aiter/pull/6602) gfx942 blockscale GEMM for GLM-5.3 (open)
- [#6535](https://github.com/ROCm/aiter/pull/6535) MI300A configs for GLM-5.3 FP8 (open)
- [#6573](https://github.com/ROCm/aiter/pull/6573) gfx1250 Gluon for Kimi-K2 TP8 (open)
- [#6595](https://github.com/ROCm/aiter/pull/6595) gfx1250 a16w16 for Kimi K2 (open)
- [#6530](https://github.com/ROCm/aiter/pull/6530) Kimi-K3 gfx1250 mxfp8_128 blockscale (open)
- [#6543](https://github.com/ROCm/aiter/pull/6543) optimize FlyDSL Kimi K2 Thinking kernel (open)
- [#6650](https://github.com/ROCm/aiter/pull/6650) gfx1250 a16w16 for Llama4 Maverick (open)
- [#6649](https://github.com/ROCm/aiter/pull/6649) gfx1250 a16w16 for Qwen3-235B (open)
- [#6652](https://github.com/ROCm/aiter/pull/6652) gfx1250 MXFP4 for Llama3 8B (open)
- [#6653](https://github.com/ROCm/aiter/pull/6653) gfx1250 MXFP4 for Llama3 70B (open)
- [#6654](https://github.com/ROCm/aiter/pull/6654) gfx1250 MXFP4 for Llama3 405B (open)
- [#6593](https://github.com/ROCm/aiter/pull/6593) Muse Spark Open MXFP4 FMoE (open)
- [#6631](https://github.com/ROCm/aiter/pull/6631) draft multi-kernel tuning (open)
- [#6555](https://github.com/ROCm/aiter/pull/6555) tuning relative to default (open)
- [#6553](https://github.com/ROCm/aiter/pull/6553) tuning preempts local best (open)
- [#6554](https://github.com/ROCm/aiter/pull/6554) tuning search space (open)
- [#6580](https://github.com/ROCm/aiter/pull/6580) tune MHA forward across backends (open)
- [#6613](https://github.com/ROCm/aiter/pull/6613) Triton harness tunes MHA tiles (open)
- [#6365](https://github.com/ROCm/aiter/pull/6365) check tuned configs for duplicate shapes
- [#6293](https://github.com/ROCm/aiter/pull/6293) gfx1250 config cleanup
- plus 26 more related config updates folded into the lists above

</details>

<details>
<summary>Parallelism & scheduling (4)</summary>

- [#5799](https://github.com/ROCm/aiter/pull/5799) CustomAllreduce re-decides expandable_segments at capture time
- [#6517](https://github.com/ROCm/aiter/pull/6517) demand-driven MORI all-to-all manager creation
- [#6618](https://github.com/ROCm/aiter/pull/6618) manage v2 CCO through the all2all manager (open)
- [#6624](https://github.com/ROCm/aiter/pull/6624) log MORI all2all handle creation (open)

</details>

<details>
<summary>Bugfixes (30)</summary>

- [#6478](https://github.com/ROCm/aiter/pull/6478) add missing SwiGLU CK-Tile MXFP4 dispatch
- [#6620](https://github.com/ROCm/aiter/pull/6620) keep CK-Tile split-k route, fixes MiniMax-M3 TP8 regression
- [#6422](https://github.com/ROCm/aiter/pull/6422) prevent gfx950 FP8 softmax underflow in MLA
- [#6446](https://github.com/ROCm/aiter/pull/6446) fix ar_ll128_unroll2 hang
- [#6541](https://github.com/ROCm/aiter/pull/6541) key comm-fused MoE winners by GPU model
- [#6392](https://github.com/ROCm/aiter/pull/6392) key GLM-5 MXFP4 EP4 rows on topk 9
- [#5936](https://github.com/ROCm/aiter/pull/5936) remove stale MXFP4 MoE aux sources
- [#6467](https://github.com/ROCm/aiter/pull/6467) initialize reverse route indices before Opus sorting
- [#6528](https://github.com/ROCm/aiter/pull/6528) gfx950 page16 short-tail guards
- [#6569](https://github.com/ROCm/aiter/pull/6569) gfx942 PA KV tail for lengths 241-255
- [#6577](https://github.com/ROCm/aiter/pull/6577) SGPR counts in gfx950 QH16 MLA metadata
- [#6481](https://github.com/ROCm/aiter/pull/6481) gfx950 MLA KV addressing
- [#6589](https://github.com/ROCm/aiter/pull/6589) Windows build args and optional imports
- [#6002](https://github.com/ROCm/aiter/pull/6002) DSv4.1-Flash sparse MLA prefill tuning and attn_sink fix
- [#5399](https://github.com/ROCm/aiter/pull/5399) ff_a16w16_fused M<=8 launch failure
- [#6321](https://github.com/ROCm/aiter/pull/6321) KDA gate pointer token stride
- [#4685](https://github.com/ROCm/aiter/pull/4685) ragged-K regression test for batched_gemm_a16wfp4
- [#6608](https://github.com/ROCm/aiter/pull/6608) GLM-4.7 MHA benchmark head dim
- [#6524](https://github.com/ROCm/aiter/pull/6524) BF16 decode dispatch for GQA 64 (open)
- [#6578](https://github.com/ROCm/aiter/pull/6578) gfx950 BF16 32-head MLA KV addressing (open)
- [#6606](https://github.com/ROCm/aiter/pull/6606) gfx950 GQA16 MTP softmax init (open)
- [#6639](https://github.com/ROCm/aiter/pull/6639) gfx942 fp8 fused-MoE dispatch wrong results (open)
- [#6519](https://github.com/ROCm/aiter/pull/6519) bound scatter-reduce staging reads (open)
- [#6568](https://github.com/ROCm/aiter/pull/6568) init padded MoE scratch to stop NaN (open)
- [#6556](https://github.com/ROCm/aiter/pull/6556) MegaMoE source-indexed payload fix (open)
- [#6539](https://github.com/ROCm/aiter/pull/6539) cross-wave LDS race in 8-wave GEMM (open)
- [#6586](https://github.com/ROCm/aiter/pull/6586) topk_plain multi-block fp16/bf16 correctness (open)
- [#6641](https://github.com/ROCm/aiter/pull/6641) scaled_silu_and_mul scale, saturation, bounds (open)
- [#6592](https://github.com/ROCm/aiter/pull/6592) topk_sigmoid pybind conversion (open)
- [#6629](https://github.com/ROCm/aiter/pull/6629) gfx1250 gemm_a16w16 output past 2**31 bytes (open)

</details>

<details>
<summary>Other bugfixes & small fixes (6)</summary>

- [#6566](https://github.com/ROCm/aiter/pull/6566) zero empty decode rows in unified attention (open)
- [#6581](https://github.com/ROCm/aiter/pull/6581) normalize Gluon split constexpr values (open)
- [#6625](https://github.com/ROCm/aiter/pull/6625) harden shuffled per-token FP8 paged decode (open)
- [#6579](https://github.com/ROCm/aiter/pull/6579) JIT build hang on zombie lock holder (open)
- [#6616](https://github.com/ROCm/aiter/pull/6616) fix -DONLY_FAV3 quoting in backward JIT (open)
- [#6645](https://github.com/ROCm/aiter/pull/6645) query XCC count via HIP for FlyDSL PA (open)

</details>

<details>
<summary>Tests & benchmarks (8)</summary>

- [#6571](https://github.com/ROCm/aiter/pull/6571) skip comm-fused MoE test without MORI CCO
- [#6651](https://github.com/ROCm/aiter/pull/6651) cut perftest iterations in correctness tests (open)
- [#6551](https://github.com/ROCm/aiter/pull/6551) rotating buffers in GEMM Triton benchmark (open)
- [#6635](https://github.com/ROCm/aiter/pull/6635) rot_bufs in bench_fused_* (open)
- [#6636](https://github.com/ROCm/aiter/pull/6636) rot_bufs for rmsnorm, layernorm, rope benches (open)
- [#6600](https://github.com/ROCm/aiter/pull/6600) rot_bufs in bench_mla_* (open)
- [#6637](https://github.com/ROCm/aiter/pull/6637) rot_bufs for attention benchmarks (open)
- [#6633](https://github.com/ROCm/aiter/pull/6633) remove bad mla_decode.py op (open)

</details>

<details>
<summary>CI & build (7)</summary>

- [#6424](https://github.com/ROCm/aiter/pull/6424) bump FlyDSL to 0.4.0
- [#6006](https://github.com/ROCm/aiter/pull/6006) publish a py3 wheel without prebuilt kernels
- [#6516](https://github.com/ROCm/aiter/pull/6516) review-pr bot gating and self-trigger fix
- [#6599](https://github.com/ROCm/aiter/pull/6599) enable Triton test selection script
- [#6505](https://github.com/ROCm/aiter/pull/6505) move common Triton kernels into common/
- [#6309](https://github.com/ROCm/aiter/pull/6309) optimize gfx950 MXFP GEMMs for Flux training shapes
- [#6513](https://github.com/ROCm/aiter/pull/6513) Windows smoke test fails when no GPU is visible (open)

</details>

<details>
<summary>Docs (2)</summary>

- [#6499](https://github.com/ROCm/aiter/pull/6499) simplify Triton docs
- [#6542](https://github.com/ROCm/aiter/pull/6542) update CLAUDE.md file precedence

</details>

<details>
<summary>Other (1)</summary>

- [#6258](https://github.com/ROCm/aiter/pull/6258) FP32 partials for gfx1250 A8W8 split-K GEMMs

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0d3dd544a47151009cf1d212946afa3d1a893af8bf17e26fae4f0c4c3ba9de9a -->
