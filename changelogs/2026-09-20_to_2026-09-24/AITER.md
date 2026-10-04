# AITER: PR digest (2026-09-20 to 2026-09-24)

_78 merged, 81 newly opened - source ROCm/AITER, generated 2026-09-24T14:04:49Z_

## TL;DR
- **Kimi-K3 and DeepSeek-V4 got the most model attention**, followed by GLM-5.x and MiniMax-M3. Kimi work was mostly GEMM/FMoE tuning and KDA decode. DeepSeek work covered A4W4/A8W4 MoE configs and a paged-K gather+dequant kernel. GLM-5.3 and MiniMax-M3 are being brought up with new 2-bit and MXFP4 MoE kernels, most of them still open.
- **The biggest merged perf work is low-precision attention and GEMM on gfx950/gfx1250.** This includes mixed MXFP6/MXFP4 GEMMs, FP8 and MXFP4 MQA-logits indexers, a FlyDSL paged-attention tile kernel, and MLA metadata and reduce fixes.
- **MoE is the second big theme.** Merged items are a mega-MoE EP path on gfx1250 with fp8/fp4 combine, register-resident grouped topk, and a GLM-5.2 topk tie fix. Open PRs add relu2 activation, SonicMoE Triton and MI308 MoE refactors.
- **Direction:** gfx950 and gfx1250 are the focus, with FlyDSL, Gluon and OPUS kernels replacing CK/ASM paths. Per-model tuning rows are landing in parallel, and PR review and CI automation is growing.

## Most important PRs
**[#5587](https://github.com/ROCm/aiter/pull/5587) Mixed MXFP6/MXFP4 GEMMs (merged)**
Adds ASM/HIP GEMMs for gfx950 that combine MXFP6 and MXFP4 operands, with tuning entries and tests. This is a large new low-precision GEMM path.

**[#4332](https://github.com/ROCm/aiter/pull/4332) FlyDSL paged-attention Tile kernel (merged)**
Adds a tile-based paged-attention decode kernel in FlyDSL, with CI coverage. It is a major new attention backend.

**[#5447](https://github.com/ROCm/aiter/pull/5447) TDM dispatch for mega-moe EP on gfx1250 (merged)**
Adds TDM-based dispatch for the expert-parallel mega-MoE path. Together with [#5176](https://github.com/ROCm/aiter/pull/5176), which adds fp8/fp4 quantization to the stage2 combine, it moves the gfx1250 MoE path toward production.

**[#4538](https://github.com/ROCm/aiter/pull/4538) gfx950 FP8 MQA logits indexer kernel (merged)**
A FlyDSL kernel for the sparse-attention indexer, which feeds DeepSeek-style top-k selection. Related merged work adds page-size-8 support and persistent CTA scheduling to the Triton paged FP8 MQA kernels.

**[#5728](https://github.com/ROCm/aiter/pull/5728) GLM-5.3 IQ2R 2-bit MoE support (open)**
A very large in-progress PR (+17k) adding 2-bit MoE kernels for GLM-5.3 on gfx950. A sibling, [#5719](https://github.com/ROCm/aiter/pull/5719), covers the Flash variant.

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#5724](https://github.com/ROCm/aiter/pull/5724) size the MLA metadata LDS scratch to the chunk rather than the batch count
- [#5723](https://github.com/ROCm/aiter/pull/5723) persistent CTA scheduling for paged FP8 MQA decode
- [#5700](https://github.com/ROCm/aiter/pull/5700) cut per-iteration address math in the non-preshuffle MQA logits decode kernel
- [#5711](https://github.com/ROCm/aiter/pull/5711) size the MQA logits decode grid to the CU count
- [#5703](https://github.com/ROCm/aiter/pull/5703) argmax takes the split count as an argument instead of a build parameter
- [#5334](https://github.com/ROCm/aiter/pull/5334) topk_gating E=512 prefill dispatch for softmax
- [#5690](https://github.com/ROCm/aiter/pull/5690) FlyDSL gfx950 A8W8 preshuffle GEMM shape coverage
- [#5508](https://github.com/ROCm/aiter/pull/5508) FP8 FMHA split-K for short cached-prefix queries
- [#5736](https://github.com/ROCm/aiter/pull/5736) (open) bound pa_decode_sparse split-K by wave count and tile budget (up to +22%)

</details>

<details>
<summary>Kernels & attention (24)</summary>

- [#5370](https://github.com/ROCm/aiter/pull/5370) Conv3d for Qwen-Image / Wan2.1 VAE on MI35X
- [#4885](https://github.com/ROCm/aiter/pull/4885) FlyDSL HSTU backward kernel
- [#5656](https://github.com/ROCm/aiter/pull/5656) OPUS PA MQA logits MXFP4 for gfx1250
- [#5332](https://github.com/ROCm/aiter/pull/5332) OPUS PA MQA logits MXFP4 for gfx950
- [#5195](https://github.com/ROCm/aiter/pull/5195) swap the gfx950 MLA v4 asm decode kernel
- [#5695](https://github.com/ROCm/aiter/pull/5695) MLA PS mode asm and opus kernels for nhead 12 and 8
- [#5698](https://github.com/ROCm/aiter/pull/5698) lift the 2 GiB limit on mla_reduce_v1 output and LSE
- [#5699](https://github.com/ROCm/aiter/pull/5699) gfx1250 F8GEMM 256x256 split-K and 128x128 AP0/AP1 kernels
- [#5796](https://github.com/ROCm/aiter/pull/5796) AOT-compile the gfx950 FP8 flash-attention forward
- [#5400](https://github.com/ROCm/aiter/pull/5400) FP8 output in gather_kv_b_proj
- [#5718](https://github.com/ROCm/aiter/pull/5718) expose FP8 attention and gather capability checks
- [#5403](https://github.com/ROCm/aiter/pull/5403) bf16 hd=256 fmha forward ASM for gfx950
- [#5376](https://github.com/ROCm/aiter/pull/5376) bf16 hd=256 fmha backward ASM for gfx950
- [#5680](https://github.com/ROCm/aiter/pull/5680) DSv4 paged K gather+dequant kernel
- [#5712](https://github.com/ROCm/aiter/pull/5712) optimize qk_norm_rope_group_quant on gfx1250
- [#4991](https://github.com/ROCm/aiter/pull/4991) optimize inverse rope group quant on gfx1250
- [#5619](https://github.com/ROCm/aiter/pull/5619) fused KDA decode: order conv_state shifts after the tap loads
- [#5768](https://github.com/ROCm/aiter/pull/5768) page size 8 in the preshuffle MQA logits kernel
- [#5430](https://github.com/ROCm/aiter/pull/5430) allocate split-K scratch buffers from a private MemPool
- [#5772](https://github.com/ROCm/aiter/pull/5772) keep the unified-attention block-table stride runtime on gfx950
- [#5746](https://github.com/ROCm/aiter/pull/5746) refresh QH128 sparse-prefill and fix softmax mlog order on gfx1250
- [#5608](https://github.com/ROCm/aiter/pull/5608) benchmark for Norm/Layernorm
- [#5676](https://github.com/ROCm/aiter/pull/5676) benchmark for fused_rmsnorm_add
- [#5731](https://github.com/ROCm/aiter/pull/5731) gfx1250 natural FP4 compressor scatter

</details>

<details>
<summary>MoE & quantization (14)</summary>

- [#5176](https://github.com/ROCm/aiter/pull/5176) fp8/fp4 quant in the mega stage2 combine
- [#5632](https://github.com/ROCm/aiter/pull/5632) register-resident grouped topk for single-group MoE
- [#5658](https://github.com/ROCm/aiter/pull/5658) merge MoE MXFP8 GEMM into the _moe_gemm_a8w8 kernel
- [#5548](https://github.com/ROCm/aiter/pull/5548) 32x32 block-scaled MXFP4 quantization
- [#5531](https://github.com/ROCm/aiter/pull/5531) gfx950 stochastic MXFP4 quantization
- [#5583](https://github.com/ROCm/aiter/pull/5583) a16w4 MXFP4 weights on gfx942
- [#5232](https://github.com/ROCm/aiter/pull/5232) do not route MXFP4 MoE to CK-Tile when inter_dim % 256 != 0
- [#4970](https://github.com/ROCm/aiter/pull/4970) QRInt4 INT4 two-shot all-reduce for gfx942/gfx950
- [#5689](https://github.com/ROCm/aiter/pull/5689) standalone relu2 elementwise kernel for non-gated MoE
- [#5443](https://github.com/ROCm/aiter/pull/5443) tune the non-temporal load hint per tuned fused_moe row
- [#5748](https://github.com/ROCm/aiter/pull/5748) optimize Opus integration flow
- [#5755](https://github.com/ROCm/aiter/pull/5755) gfx942 a16wi4 gemm2 atomic uses fx.atomic_add
- [#5493](https://github.com/ROCm/aiter/pull/5493) mori-ep low-latency kernels and a cached handle set
- [#5672](https://github.com/ROCm/aiter/pull/5672) drop GRID_MN from batched MXFP4 GEMM specialisation keys

</details>

<details>
<summary>Model support & tuning configs (16)</summary>

- [#5691](https://github.com/ROCm/aiter/pull/5691) per-shape GEMM configs for MI308X (gfx942)
- [#5602](https://github.com/ROCm/aiter/pull/5602) GLM-5.3 Flash GEMM configs for gfx950
- [#5702](https://github.com/ROCm/aiter/pull/5702) tune Kimi-K3 BF16 GEMMs for gfx950
- [#5714](https://github.com/ROCm/aiter/pull/5714) revert the kimik3_bf16_tuned_gemm.csv change
- [#5780](https://github.com/ROCm/aiter/pull/5780) revert 13 regressed Kimi-K3 A8W8 rows
- [#5722](https://github.com/ROCm/aiter/pull/5722) DSV4.1 A4W4 fused MoE configs for gfx950
- [#5735](https://github.com/ROCm/aiter/pull/5735) GLM-5.3 fused shared MoE rows
- [#5599](https://github.com/ROCm/aiter/pull/5599) GLM-5.3 routed MoE rows
- [#5641](https://github.com/ROCm/aiter/pull/5641) retune DSR1/V3 FP8 fmoe rows on gfx950
- [#5575](https://github.com/ROCm/aiter/pull/5575) DSPARK a8w8 blockscale bpreshuffle configs
- [#4815](https://github.com/ROCm/aiter/pull/4815) Qwen3.6 35B-A3B FMoE configs for gfx1201
- [#5579](https://github.com/ROCm/aiter/pull/5579) gfx950 wideEP MoE tests for a8w4 DSv4 and a4w4 Kimi K3
- [#5710](https://github.com/ROCm/aiter/pull/5710) prevent DSV4 DPA CI OOM with bounded route workspace buckets
- [#5726](https://github.com/ROCm/aiter/pull/5726) grouped topk tie handling for GLM-5.2 accuracy
- [#5716](https://github.com/ROCm/aiter/pull/5716) run the Kimi-K2.5 perf job nightly only
- [#5697](https://github.com/ROCm/aiter/pull/5697) lower Kimi vLLM GPU memory utilization in CI

</details>

<details>
<summary>Bugfixes (6)</summary>

- [#5749](https://github.com/ROCm/aiter/pull/5749) page size 8 in paged MQA logits, and fix large KV offsets
- [#5572](https://github.com/ROCm/aiter/pull/5572) avoid Python 3.10 source inspection failures in MXFP4 JIT imports
- [#5630](https://github.com/ROCm/aiter/pull/5630) handle 64-aligned A16W16 shards in CK MoE dispatch
- [#5694](https://github.com/ROCm/aiter/pull/5694) uniform trip count for custom_all_reduce block barriers
- [#5734](https://github.com/ROCm/aiter/pull/5734) remove incorrect topk adjustment in get_2stage_cfgs for EP
- [#5545](https://github.com/ROCm/aiter/pull/5545) log with % placeholders instead of f-strings across Triton/Gluon

</details>

<details>
<summary>CI & build (7)</summary>

- [#5666](https://github.com/ROCm/aiter/pull/5666) add aiter-bot, a self-hosted GLM PR reviewer
- [#5785](https://github.com/ROCm/aiter/pull/5785) fix the review-pr agent-timeout envelope
- [#5713](https://github.com/ROCm/aiter/pull/5713) auto-update split test FILE_TIMES
- [#5717](https://github.com/ROCm/aiter/pull/5717) cache the Triton wheelhouse across test jobs
- [#5425](https://github.com/ROCm/aiter/pull/5425) fail Triton test jobs if any kernel autotunes at runtime
- [#5659](https://github.com/ROCm/aiter/pull/5659) re-enable contexted kv attention tests
- [#5753](https://github.com/ROCm/aiter/pull/5753) extend the ATOM watchdog for AITER JIT

</details>

<details>
<summary>Open: new models & MoE / EP kernels (31)</summary>

- [#5719](https://github.com/ROCm/aiter/pull/5719) GLM-5.3-Flash IQ2R 2-bit MoE
- [#5727](https://github.com/ROCm/aiter/pull/5727) WIP MoonEP prefill and decode planning policies
- [#5795](https://github.com/ROCm/aiter/pull/5795) refactor MI308 MoE kernels and enable compile caching
- [#5704](https://github.com/ROCm/aiter/pull/5704) stage1 fused for mega-moe EP on gfx1250
- [#5752](https://github.com/ROCm/aiter/pull/5752) A4W4 MoE prefill with A preshuffle on gfx1250
- [#5814](https://github.com/ROCm/aiter/pull/5814) mega stage1 perf optimization
- [#5810](https://github.com/ROCm/aiter/pull/5810) bind the mori tokoff-ext allocator on the mori dispatch path
- [#5725](https://github.com/ROCm/aiter/pull/5725) SonicMoE pure-Triton grouped GEMM MoE
- [#5817](https://github.com/ROCm/aiter/pull/5817) MiniMax-M3 MXFP8
- [#5788](https://github.com/ROCm/aiter/pull/5788) topk index score for MiniMax-M3
- [#5794](https://github.com/ROCm/aiter/pull/5794) SwiGLU OAI MXFP4 FLAT kernels for MiniMax-M3
- [#5816](https://github.com/ROCm/aiter/pull/5816) SwiGLU OAI MXFP4 FLAT 16x128 kernel for MiniMax-M3
- [#5819](https://github.com/ROCm/aiter/pull/5819) SwiGLU OAI MXFP4 FLAT 16x256 kernel for MiniMax-M3
- [#5758](https://github.com/ROCm/aiter/pull/5758) MiniMax-M3-MXFP4 BF16 tuned GEMM configs
- [#5822](https://github.com/ROCm/aiter/pull/5822) opt-in M3 sequence-parallel collectives and tiled MoE sorting
- [#5750](https://github.com/ROCm/aiter/pull/5750) tuned native group32 A8W8 Triton GEMM for gfx950
- [#5778](https://github.com/ROCm/aiter/pull/5778) Exp/mx32 plain
- [#5812](https://github.com/ROCm/aiter/pull/5812) scatter epilog for layout-v2 GEMM2
- [#5821](https://github.com/ROCm/aiter/pull/5821) tuned decode MoE kernels for the DSv4 mori-EP backend
- [#5706](https://github.com/ROCm/aiter/pull/5706) DSv4 EP16 a4w4 fused-MoE tables
- [#5709](https://github.com/ROCm/aiter/pull/5709) speculative KDA decode on gfx950 for Kimi-K3
- [#5754](https://github.com/ROCm/aiter/pull/5754) FlashKDA in-kernel paged state_cache I/O
- [#5804](https://github.com/ROCm/aiter/pull/5804) kmk3 EP MoE support and gemm2 optimization
- [#5763](https://github.com/ROCm/aiter/pull/5763) gfx950 MXFP4 SiTUv2 FLAT kernels and KK3 fake tuner
- [#5756](https://github.com/ROCm/aiter/pull/5756) restore accurate Kimi-K3 A4W4 FMoE decode tiles
- [#5783](https://github.com/ROCm/aiter/pull/5783) tune a8w8 bpreshuffle for Kimi-K3 KDA gate at tp4
- [#5757](https://github.com/ROCm/aiter/pull/5757) Qwen3.8 flash MXFP4 asm
- [#5820](https://github.com/ROCm/aiter/pull/5820) Qwen3.8 kernels on gfx950
- [#5693](https://github.com/ROCm/aiter/pull/5693) herd_fused_topk drop-in selector for fused_moe 2-stage
- [#5744](https://github.com/ROCm/aiter/pull/5744) avoid layout-v2 stage2 and over-padded tiles under EP
- [#5701](https://github.com/ROCm/aiter/pull/5701) gfx1250 ep8 tuned config setup

</details>

<details>
<summary>Open: attention, MLA & kernels (24)</summary>

- [#5809](https://github.com/ROCm/aiter/pull/5809) refactor PA decode and load CSV tuning results
- [#5762](https://github.com/ROCm/aiter/pull/5762) tuned-config dispatch and delta-race tuner for packed varlen MHA
- [#5761](https://github.com/ROCm/aiter/pull/5761) unify gfx950 and gfx1250 MXFP4 MQA-logits
- [#5733](https://github.com/ROCm/aiter/pull/5733) revert the gfx950 OPUS PA MQA logits MXFP4 change
- [#5798](https://github.com/ROCm/aiter/pull/5798) MHA v4: bf16 sparse, LSE, KV varlen
- [#5707](https://github.com/ROCm/aiter/pull/5707) optimize FP4 MQA prefill and decode on gfx950
- [#5715](https://github.com/ROCm/aiter/pull/5715) Gluon paged-decode attention with sigmoid output gate and group-128 FP8 epilogue
- [#5732](https://github.com/ROCm/aiter/pull/5732) adaptive-blocked K5 prefill h-recurrence in GDN
- [#5692](https://github.com/ROCm/aiter/pull/5692) fix PA gqa16 short-tail PS
- [#5808](https://github.com/ROCm/aiter/pull/5808) gfx1250 MLA qh32 decode ams kernel v2
- [#5811](https://github.com/ROCm/aiter/pull/5811) gfx1250 MLA qh32 decode ams kernel v3
- [#5805](https://github.com/ROCm/aiter/pull/5805) speed up gfx1250 32mx1 MLA sparse-prefill kernels
- [#5776](https://github.com/ROCm/aiter/pull/5776) faster cross-split merge for MLA v4 nm small decode grids
- [#5797](https://github.com/ROCm/aiter/pull/5797) prefill launch config for sparse MLA on gfx950
- [#5721](https://github.com/ROCm/aiter/pull/5721) sparse_mla_fwd on gfx942
- [#5787](https://github.com/ROCm/aiter/pull/5787) CK fmha LLC head grouping on RDNA
- [#5790](https://github.com/ROCm/aiter/pull/5790) tune gfx1201 unified attention for Gemma4 shapes
- [#5782](https://github.com/ROCm/aiter/pull/5782) FP8 MQA logits gfx950 DSA tune
- [#5818](https://github.com/ROCm/aiter/pull/5818) fused m32k4 shuffle quant for ASM a8w8 GEMM on gfx1250
- [#5708](https://github.com/ROCm/aiter/pull/5708) relu2 activation for CK-Tile fused MoE GEMM
- [#5815](https://github.com/ROCm/aiter/pull/5815) FlyDSL fused intranode all-to-all for Ulysses sequence-parallel attention
- [#5774](https://github.com/ROCm/aiter/pull/5774) rotating-buffer GEMM A16W16 benchmark
- [#5720](https://github.com/ROCm/aiter/pull/5720) gfx908 target metadata and GEMM defaults
- [#5800](https://github.com/ROCm/aiter/pull/5800) fix gluon import and tune fused_clamp_act_mul for gfx950

</details>

<details>
<summary>Open: bugfixes & other (26)</summary>

- [#5759](https://github.com/ROCm/aiter/pull/5759) size PS prefill partial buffers from the real token budget
- [#5793](https://github.com/ROCm/aiter/pull/5793) bound K/V loads in the Triton FA decode non-paged split-K tail
- [#5771](https://github.com/ROCm/aiter/pull/5771) assert SPLIT_UNMASKED_LOOP is not used with sliding window
- [#5775](https://github.com/ROCm/aiter/pull/5775) send the real IPC offset in custom_all_reduce instead of 0
- [#5799](https://github.com/ROCm/aiter/pull/5799) re-take the expandable_segments decision at capture time
- [#5807](https://github.com/ROCm/aiter/pull/5807) specialize partial tiles in two-stage custom all-reduce
- [#5813](https://github.com/ROCm/aiter/pull/5813) fix custom_all_reduce CI hang
- [#5747](https://github.com/ROCm/aiter/pull/5747) fix MoE ck2stages dim alignment
- [#5802](https://github.com/ROCm/aiter/pull/5802) route a16w4 SiLU MoE to CK-Tile and apply swiglu_limit
- [#5764](https://github.com/ROCm/aiter/pull/5764) workaround for a1_scale out-of-bounds read in fmoe_fp8_blockscale_g1u1
- [#5801](https://github.com/ROCm/aiter/pull/5801) fix gfx1250 TDM grouped GEMM bias index
- [#5767](https://github.com/ROCm/aiter/pull/5767) mask partial vectors in sampling kernels
- [#5745](https://github.com/ROCm/aiter/pull/5745) guard GroupNorm vectorization at channel boundaries
- [#5742](https://github.com/ROCm/aiter/pull/5742) guard unsupported layouts in unary operator dispatch
- [#5779](https://github.com/ROCm/aiter/pull/5779) remove unintended CK dependency from plain top-k
- [#5740](https://github.com/ROCm/aiter/pull/5740) Gluon MoE compatibility with upstream Triton compiler
- [#5786](https://github.com/ROCm/aiter/pull/5786) make CK fmha kernel generation follow GPU_ARCHS
- [#5773](https://github.com/ROCm/aiter/pull/5773) SMI summary plots and raw-sample timelines
- [#5770](https://github.com/ROCm/aiter/pull/5770) add security scanning workflows
- [#5730](https://github.com/ROCm/aiter/pull/5730) Copilot FlyDSL path instructions and review-pr C5 docs
- [#5803](https://github.com/ROCm/aiter/pull/5803) review-pr 40min agent timeout, retry only transient failures
- [#5784](https://github.com/ROCm/aiter/pull/5784) enable DeepSeek-V4-Pro 2P1D TP8 ATOM DI smoke cases
- [#5751](https://github.com/ROCm/aiter/pull/5751) gfx950 FHMoE tuner on gemm_moe_tune.py

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: cb711d5a9992b793e13da8212296d8931a208935e014959f03c7b3ad52459a8d -->
