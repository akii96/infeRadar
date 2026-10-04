# AITER: PR digest (2026-09-27 to 2026-10-01)

_59 merged, 123 newly opened - source ROCm/AITER, generated 2026-10-01T16:03:20Z_

## TL;DR
- **DeepSeek-V4/V4.1 got the most attention**, followed by Kimi-K3, Qwen3.5/3.8, GLM-5.x and early MiniMax-M3. Merged work was mostly gfx950 and gfx1250 tuned configs, with MXFP8/MXFP4 GEMM and MoE tuning for DSV4.1.
- **Biggest merged kernel work:** a unified gfx950+gfx1250 MXFP4 MQA-logits path (`[#5761](https://github.com/ROCm/aiter/pull/5761)`), a fused Qwen3-Next GDN prefill Gluon kernel (`[#5606](https://github.com/ROCm/aiter/pull/5606)`), the MXFP8 e8m0 GEMM (`[#5896](https://github.com/ROCm/aiter/pull/5896)`), and MHA v4 with sparse/LSE support (`[#5798](https://github.com/ROCm/aiter/pull/5798)`).
- **Open PRs concentrate on FlyDSL MoE and MLA:** batch 1-8 MoE decode and MI308 Down kernels (`[#5973](https://github.com/ROCm/aiter/pull/5973)`, `[#5932](https://github.com/ROCm/aiter/pull/5932)`), a DSV4 fp8 MLA decode (`[#5882](https://github.com/ROCm/aiter/pull/5882)`), mega_moe_tp for gfx950 (`[#5937](https://github.com/ROCm/aiter/pull/5937)`), and MiniMax-M3 sparse decode (`[#6047](https://github.com/ROCm/aiter/pull/6047)`).
- **Direction:** FlyDSL and Gluon are replacing hand-written ASM/CK paths, gfx1250 and gfx950 bring-up continues, and a CI/repo reorganization is moving Triton tests into wrapper folders.

## Most important PRs
**`[#5761](https://github.com/ROCm/aiter/pull/5761)` Unify gfx950+gfx1250 MXFP4 MQA-logits (merged)**
Merges the two arch-specific OPUS/JIT MXFP4 MQA-logits kernels into one implementation. This is the indexer scoring path for sparse attention, and the change is a net -2k lines.

**`[#5606](https://github.com/ROCm/aiter/pull/5606)` Fused Qwen3-Next GDN prefill, gfx950 Gluon (merged)**
Adds a gated-delta-net prefill kernel with an fp8 group-quant epilogue, so quantization no longer needs a separate pass. Targets the Qwen3-Next/3.5/3.8 linear-attention layers.

**`[#5896](https://github.com/ROCm/aiter/pull/5896)` gfx950 MXFP8 e8m0 GEMM + DeepSeek-V4/V4.1 tuned configs (merged)**
Adds a MXFP8 GEMM with e8m0 block scales via FlyDSL/OPUS, plus tuned shapes for the DSV4 family.

**`[#5798](https://github.com/ROCm/aiter/pull/5798)` MHA v4: bf16 sparse, LSE, KV varlen (merged)**
Extends the gfx950 MHA v4 kernel (ASM, HIP, Gluon) with bf16 sparse attention, LSE output and varlen KV. Fills the gaps needed for sparse-attention serving.

**`[#5973](https://github.com/ROCm/aiter/pull/5973)` / `[#5932](https://github.com/ROCm/aiter/pull/5932)` FlyDSL MoE decode and MI308 Down kernels (open)**
Parts 3/3 and 2/3 of a series: batch 1-8 MoE decode and MI308 (gfx942) Down kernels with BF16 support. Both are large (about 12k and 11k lines) and aimed at Kimi, Qwen and MiniMax.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#5652](https://github.com/ROCm/aiter/pull/5652) merged: fold shared-expert gate GEMV into the topk_softmax kernel
- [#5987](https://github.com/ROCm/aiter/pull/5987) open: route gfx950 large-expert decode to multi-phase MoE sorting
- [#5955](https://github.com/ROCm/aiter/pull/5955) open: fuse six-way split-K reduction and q/KV RMSNorm
- [#5914](https://github.com/ROCm/aiter/pull/5914) open: optionally emit fp8-quantized Q from fused_qk_norm_rope_cache_pts_quant_shuffle
- [#6024](https://github.com/ROCm/aiter/pull/6024) open: wider launch tile for fused_reduce_act_mul_and_mxfp4_quant, plus round_to_input_dtype and transpose_scale
- [#5885](https://github.com/ROCm/aiter/pull/5885) merged: optimize the mHC fused kernel for dsv4.1-flash

</details>

<details>
<summary>Kernels & attention (47)</summary>

- [#5952](https://github.com/ROCm/aiter/pull/5952) merged: Triton-based Conv3D kernels
- [#5542](https://github.com/ROCm/aiter/pull/5542) merged: fused SiLU-and-multiply backward
- [#4221](https://github.com/ROCm/aiter/pull/4221) merged: FlyDSL paged MLA indexer
- [#5844](https://github.com/ROCm/aiter/pull/5844) merged: pin gpr and round-robin DCP for persistent MLA PS1 FP8 decode on gfx1250
- [#5805](https://github.com/ROCm/aiter/pull/5805) merged: speed up gfx1250 32mx1 MLA sparse-prefill kernels
- [#5901](https://github.com/ROCm/aiter/pull/5901) merged: inline FlyDSL FP8 FMHA head shapes, drop config CSVs
- [#4963](https://github.com/ROCm/aiter/pull/4963) merged: gfx942 fp8_mqa_logits picks rows_per_block automatically
- [#5877](https://github.com/ROCm/aiter/pull/5877) merged: stop fused_bmm_rope_kv_cache using batched_gemm_a8w8_a_per_token
- [#5847](https://github.com/ROCm/aiter/pull/5847) merged: CK blockscale split-K picks pipeline from per-split loop count
- [#5598](https://github.com/ROCm/aiter/pull/5598) merged: enable unified-attention skip-mask for gfx950 hd256 FP8 prefill
- [#5996](https://github.com/ROCm/aiter/pull/5996) open: FlyDSL QSA indexer scorer + sparse GQA
- [#5913](https://github.com/ROCm/aiter/pull/5913) open: two-stage hyper-connection gated residual kernel
- [#5900](https://github.com/ROCm/aiter/pull/5900) open: gfx1201 SageAttention operators
- [#5995](https://github.com/ROCm/aiter/pull/5995) open: BF16 paged decode for Qwen3.8 QSA sparse attention
- [#5887](https://github.com/ROCm/aiter/pull/5887) open: PA decode tile with Qlen8 and SWA with sink
- [#6026](https://github.com/ROCm/aiter/pull/6026) open: fused KDA decode kernels on gfx950
- [#6037](https://github.com/ROCm/aiter/pull/6037) open: HIP BF16 sparse MLA for GLM-5.3-Flash H64 prefill
- [#6047](https://github.com/ROCm/aiter/pull/6047) open: MiniMax-M3 fused sparse-layer decode
- [#5969](https://github.com/ROCm/aiter/pull/5969) open: a8w8 blockscale GEMM via CK and FlyDSL
- [#5897](https://github.com/ROCm/aiter/pull/5897) open (WIP): compute-bound Gluon a16w16 gfx950 GEMM scheduled by llirSched
- [#6020](https://github.com/ROCm/aiter/pull/6020) open: GFX11 wave32 FlashAttention for gfx1151
- [#5921](https://github.com/ROCm/aiter/pull/5921) open: fp8_mqa_logits derives split target from kernel occupancy
- [#6001](https://github.com/ROCm/aiter/pull/6001) open: fp8_mqa_logits drops host row-pad copies
- [#5925](https://github.com/ROCm/aiter/pull/5925) open: stop serving-time recompiles of _prefill_row_plan_kernel
- [#5992](https://github.com/ROCm/aiter/pull/5992) open: causal conv1d prefill and GDN decode/verify for Qwen3.5/3.8
- [#5993](https://github.com/ROCm/aiter/pull/5993) open: hc_mix kernel for Qwen3.8 hyper-connections
- [#5949](https://github.com/ROCm/aiter/pull/5949) open: faster gfx950 head-256 paged-attention decode with NHD page-64
- [#5978](https://github.com/ROCm/aiter/pull/5978) open: optimize qk norm rope mla seg cache on gfx1250
- [#5985](https://github.com/ROCm/aiter/pull/5985) open: optimize group quant on gfx1250
- [#5977](https://github.com/ROCm/aiter/pull/5977) open: asm mha bf16 hd192x128 with strided q/k/v/out
- [#6034](https://github.com/ROCm/aiter/pull/6034) open: spec-decode support for Gluon KDA
- [#6056](https://github.com/ROCm/aiter/pull/6056) open: GLA changes for Kimi K3
- [#5929](https://github.com/ROCm/aiter/pull/5929) open: gfx950 split-KV 3D attention for head_dim >= 512
- [#6038](https://github.com/ROCm/aiter/pull/6038) open: fused gated RMSNorm + MXFP4 quant
- [#6002](https://github.com/ROCm/aiter/pull/6002) open: faster sparse MLA prefill at low head counts (gfx942)
- [#5980](https://github.com/ROCm/aiter/pull/5980) open: NoPE variant of fused_qk_rope_cat_and_cache_mla
- [#5895](https://github.com/ROCm/aiter/pull/5895) open: gemm_a16w16_atomic accumulates into existing output
- [#6048](https://github.com/ROCm/aiter/pull/6048) open: restore direct-to-LDS scale copies for small-M packed afp8wfp8
- [#6030](https://github.com/ROCm/aiter/pull/6030) open: tile_m=16 for the mHC FP32 fn decode GEMM
- [#5988](https://github.com/ROCm/aiter/pull/5988) open: gfx950 Q256 fused MXFP4 prefill pipeline
- [#5890](https://github.com/ROCm/aiter/pull/5890) open: split plan helper and cost-model split count for MLA v4 nm
- [#6005](https://github.com/ROCm/aiter/pull/6005) open: HGEMM keeps C shuffle in fp32 for fp32 output
- [#5970](https://github.com/ROCm/aiter/pull/5970) open: opt-in hipBLASLt grouped GEMM backend for SonicMoE
- [#5922](https://github.com/ROCm/aiter/pull/5922) open: Inkling model GEMM configs
- [#5968](https://github.com/ROCm/aiter/pull/5968) open: move Grouped MatMul into gemm/grouped
- [#6017](https://github.com/ROCm/aiter/pull/6017) open: tune prefill num_warps on gfx950
- [#5899](https://github.com/ROCm/aiter/pull/5899) open: overlap decode compact plan with dispatch on gfx1250
- [#5934](https://github.com/ROCm/aiter/pull/5934) open: a4w4 prefill v2 on gfx1250

</details>

<details>
<summary>MoE & quantization (28)</summary>

- [#5725](https://github.com/ROCm/aiter/pull/5725) merged: SonicMoE pure-Triton grouped GEMM MoE
- [#5321](https://github.com/ROCm/aiter/pull/5321) merged: Kimi-K3 merged MoE front
- [#5708](https://github.com/ROCm/aiter/pull/5708) merged: relu2 activation in CK-Tile fused MoE GEMM
- [#5763](https://github.com/ROCm/aiter/pull/5763) merged: gfx950 MXFP4 SiTUv2 FLAT kernels
- [#5851](https://github.com/ROCm/aiter/pull/5851) merged: tune MiMo TP8 MXFP4 MoE
- [#5919](https://github.com/ROCm/aiter/pull/5919) merged: tune DSV4.1 TP4 A4W4 fused MoE on gfx950
- [#5904](https://github.com/ROCm/aiter/pull/5904) merged: a8w4 fused-MoE configs for DSV4.1-Flash
- [#5810](https://github.com/ROCm/aiter/pull/5810) merged: bind mori tokoff-ext allocator on the gfx1250 mega_moe dispatch path
- [#5818](https://github.com/ROCm/aiter/pull/5818) merged: gfx1250 MXFP8 1x32 bpreshuffle GEMM
- [#5937](https://github.com/ROCm/aiter/pull/5937) open: mega_moe_tp for gfx950
- [#5907](https://github.com/ROCm/aiter/pull/5907) open: comm fused moe stage2 reducescatter for dsv4 dpa
- [#5906](https://github.com/ROCm/aiter/pull/5906) open: fuse G2L preparation for large expert masks
- [#6036](https://github.com/ROCm/aiter/pull/6036) open: single-launch bitmask MoE sort with optional fused router
- [#6050](https://github.com/ROCm/aiter/pull/6050) open: HY4 MXFP8 heterogeneous MoE fusion
- [#6052](https://github.com/ROCm/aiter/pull/6052) open: MegaMoE stage1_fused/stage2_fused switches and mori combine
- [#5891](https://github.com/ROCm/aiter/pull/5891) open: MiMo MXFP4 EP8/EP16 on gfx950
- [#5884](https://github.com/ROCm/aiter/pull/5884) open: respect GPU_ARCHS for Grouped MoE AOT builds
- [#5966](https://github.com/ROCm/aiter/pull/5966) open: DSV4.1 MoE config file
- [#5967](https://github.com/ROCm/aiter/pull/5967) open: DSV4.1 CK MoE tuning configs
- [#6003](https://github.com/ROCm/aiter/pull/6003) open: DSv4 E=385/topk7 fp8-epilogue decode stage1
- [#6055](https://github.com/ROCm/aiter/pull/6055) open: pin EP gemm1 cluster_m=1 for DSV4 grouped MoE
- [#5986](https://github.com/ROCm/aiter/pull/5986) open: GLM-5 MXFP4 EP4 decode fused-MoE rows
- [#5902](https://github.com/ROCm/aiter/pull/5902) open: retune GLM5 MXFP4 FMoE for gfx950
- [#5953](https://github.com/ROCm/aiter/pull/5953) open: GLM-5.3-Flash fused shared MoE rows for gfx942
- [#6025](https://github.com/ROCm/aiter/pull/6025) open: tune Qwen3.8 mxfp4 con 32/64 with emsort asm
- [#6022](https://github.com/ROCm/aiter/pull/6022) open: fix cktile 2-stage moe_gemm1 heuristic dispatch
- [#5979](https://github.com/ROCm/aiter/pull/5979) open: keep two K tiles per split in blockscale MoE stage-1 split-K
- [#6035](https://github.com/ROCm/aiter/pull/6035) open: remove bad moe gemm wrapper code

</details>

<details>
<summary>Model support & tuned configs (30)</summary>

- [#5836](https://github.com/ROCm/aiter/pull/5836) merged: Qwen3.8-27B gfx950 A4W4 GDN BA shapes
- [#5585](https://github.com/ROCm/aiter/pull/5585) merged: Qwen3.8-27B TP1 a8w8 blockscale for gfx942
- [#5839](https://github.com/ROCm/aiter/pull/5839) merged: gfx942 a8w8 blockscale for Qwen3/3.5/GLM/DSV4
- [#5974](https://github.com/ROCm/aiter/pull/5974) merged: Qwen3.8-Flash-Next PTPC-FP8 and BF16 on gfx942
- [#5783](https://github.com/ROCm/aiter/pull/5783) merged: Kimi-K3 KDA gate a8w8 bpreshuffle at tp4
- [#5830](https://github.com/ROCm/aiter/pull/5830) merged: gfx950 gemm_a16w16 per-shape configs
- [#5998](https://github.com/ROCm/aiter/pull/5998) merged: gfx950 preshuffled AFP4WFP4 N=4608 K=8192
- [#5939](https://github.com/ROCm/aiter/pull/5939) merged: DSR1 gfx1250 bf16 GEMM
- [#6032](https://github.com/ROCm/aiter/pull/6032) merged: gfx1250 A16W16 for Wan2.2 shapes
- [#6028](https://github.com/ROCm/aiter/pull/6028) merged: gfx1250 MXFP4 preshuffle GEMM
- [#4493](https://github.com/ROCm/aiter/pull/4493) merged: gfx1101 MHA config
- [#5790](https://github.com/ROCm/aiter/pull/5790) merged: gfx1201 unified attention for Gemma4 shapes
- [#5956](https://github.com/ROCm/aiter/pull/5956) open: Kimi-K3 prefill merged-front shapes
- [#5903](https://github.com/ROCm/aiter/pull/5903) open: small-M Kimi-K3 BF16 GEMMs
- [#6019](https://github.com/ROCm/aiter/pull/6019) open: Kimi K3 gfx950 bf16 tp8
- [#5982](https://github.com/ROCm/aiter/pull/5982) open: GLM-5.3-Flash TP4 fused KDA in-proj bf16
- [#5994](https://github.com/ROCm/aiter/pull/5994) open: GLM-5.2-FP8 a8w8 blockscale on gfx950
- [#6029](https://github.com/ROCm/aiter/pull/6029) open: DSv4 wq_b/wo_b fp8 blockscale cold-weight rows
- [#6004](https://github.com/ROCm/aiter/pull/6004) open: DSv4 wqkv_a fp8 blockscale configs
- [#6033](https://github.com/ROCm/aiter/pull/6033) open: Qwen3.8-27B TP1 B-preshuffle blockscale on gfx950
- [#5999](https://github.com/ROCm/aiter/pull/5999) open: qwen35 bf16 on gfx1250
- [#6043](https://github.com/ROCm/aiter/pull/6043) open: Qwen3.5-397B bf16 a16w16 on gfx1250
- [#5928](https://github.com/ROCm/aiter/pull/5928) open: Gemma-4-31B a4w4 blockscale on gfx950
- [#5920](https://github.com/ROCm/aiter/pull/5920) open: Gemma4 fp8 prefill unified attention
- [#5926](https://github.com/ROCm/aiter/pull/5926) open: gfx950 prefill tile for head_dim 512 (Gemma 4)
- [#6015](https://github.com/ROCm/aiter/pull/6015) open: Llama-3.1-8B afp4wfp4 decode
- [#6039](https://github.com/ROCm/aiter/pull/6039) open: gfx950 AFP4WFP4 N=8192 K=2560 and N=2560 K=3072
- [#5933](https://github.com/ROCm/aiter/pull/5933) open: gfx950 gemm_a16w16 N=288 K=4096
- [#5981](https://github.com/ROCm/aiter/pull/5981) open: gfx950 FP8 batched GEMM tuning
- [#5961](https://github.com/ROCm/aiter/pull/5961) open: gfx1101 gemm_a16w16

</details>

<details>
<summary>Hardware & arch (8)</summary>

- [#5761](https://github.com/ROCm/aiter/pull/5761) is covered above; this area lists the remaining gfx-specific work
- [#5917](https://github.com/ROCm/aiter/pull/5917) merged: drop no-op kpack from RDNA GEMM configs
- [#5055](https://github.com/ROCm/aiter/pull/5055) merged: gfx12 mxfp8 gemm cga update
- [#5963](https://github.com/ROCm/aiter/pull/5963) merged: fix LDS OOM on mxfp8 Triton GEMM for gfx950
- [#5997](https://github.com/ROCm/aiter/pull/5997) open: seed gfx1150 configs from gfx1151
- [#5960](https://github.com/ROCm/aiter/pull/5960) open: gfx1101 gemm_a8w8 config
- [#6027](https://github.com/ROCm/aiter/pull/6027) open: tune gfx1250 gluon a16w16
- [#5983](https://github.com/ROCm/aiter/pull/5983) open: fix gfx950 FP8 preshuffle shared-memory overflow

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#5965](https://github.com/ROCm/aiter/pull/5965) open: gfx1250 QuickReduce for TP2 and TP4
- [#5918](https://github.com/ROCm/aiter/pull/5918) open: fused all_reduce_add and retuned gfx950 all-reduce dispatch
- [#6031](https://github.com/ROCm/aiter/pull/6031) open: M3 sequence-parallel collectives
- [#6049](https://github.com/ROCm/aiter/pull/6049) open: QuickAllReduce INT4 shared global divisor to avoid E4M3 scale saturation
- [#6000](https://github.com/ROCm/aiter/pull/6000) open: Gemma (1 + w) weights in fused AR+RMSNorm+MXFP4 quant

</details>

<details>
<summary>Bugfixes (29)</summary>

- [#5905](https://github.com/ROCm/aiter/pull/5905) merged: MLA v4 nm test read packed BF16 as FP32
- [#5886](https://github.com/ROCm/aiter/pull/5886) merged: pa_decode compile error with newer Triton
- [#5935](https://github.com/ROCm/aiter/pull/5935) merged: don't write segment softmax state at NUM_SEGMENTS_PER_SEQ == 1
- [#5860](https://github.com/ROCm/aiter/pull/5860) merged: MLA follow-up comment and test fixes
- [#5663](https://github.com/ROCm/aiter/pull/5663) merged: fp8 KV reference in bench_unified_attention
- [#6009](https://github.com/ROCm/aiter/pull/6009) merged: unified attention sglang compatibility
- [#5893](https://github.com/ROCm/aiter/pull/5893) open: gfx950 MLA decode reading wrong KV past 4 GiB
- [#5924](https://github.com/ROCm/aiter/pull/5924) open: guard gfx942 BF16 MLA KV address span
- [#6040](https://github.com/ROCm/aiter/pull/6040) open: stream-order get_ps_metadata_v1 transfers
- [#5910](https://github.com/ROCm/aiter/pull/5910) open: CUDA-graph capturable dropout-free varlen attention
- [#6054](https://github.com/ROCm/aiter/pull/6054) open: diverge on active chunks in topk decode
- [#5915](https://github.com/ROCm/aiter/pull/5915) open: Gluon PA decode causal mask across splits
- [#5909](https://github.com/ROCm/aiter/pull/5909) open: Gluon PA decode VGPR blow-up on Triton 3.8
- [#6042](https://github.com/ROCm/aiter/pull/6042) open: avoid peeled sparse MLA spill below Triton 3.8
- [#6051](https://github.com/ROCm/aiter/pull/6051) open: asymmetric Q/K and V heads in unified attention
- [#6018](https://github.com/ROCm/aiter/pull/6018) open: dynamic_mxfp4_quant launch grid for decode-sized M
- [#6007](https://github.com/ROCm/aiter/pull/6007) open: zero default for masked scales in gemm_afp8wfp8
- [#5972](https://github.com/ROCm/aiter/pull/5972) open: restore shadowed OPUS A16W16 cache-policy registrations
- [#5911](https://github.com/ROCm/aiter/pull/5911) open: duplicate hip_bfloat16 specialization in quant_mxfp6_gemm.cu
- [#5936](https://github.com/ROCm/aiter/pull/5936) open: stale MXFP4 MoE aux generated sources
- [#5948](https://github.com/ROCm/aiter/pull/5948) open: 3D binary-op broadcast guard
- [#5975](https://github.com/ROCm/aiter/pull/5975) open: decouple FP6 packers from Triton availability
- [#6041](https://github.com/ROCm/aiter/pull/6041) open: honor padding_value in HSTU reference
- [#6016](https://github.com/ROCm/aiter/pull/6016) open: align FMoE tuning token buckets with runtime lookup
- [#6013](https://github.com/ROCm/aiter/pull/6013) open: gfx942 FLAT candidates in ASM FMoE tuning
- [#5991](https://github.com/ROCm/aiter/pull/5991) open: missing extension module names in pretune builds
- [#5971](https://github.com/ROCm/aiter/pull/5971) open: fail fast and retry third-party clone failures
- [#5938](https://github.com/ROCm/aiter/pull/5938) open: detached-head advice for third-party clone
- [#5989](https://github.com/ROCm/aiter/pull/5989) open: false ATOM hangs during JIT compilation

</details>

<details>
<summary>Refactors (9)</summary>

- [#5874](https://github.com/ROCm/aiter/pull/5874) merged: consolidate tuning harnesses
- [#5943](https://github.com/ROCm/aiter/pull/5943) merged: move Triton unit tests into wrapper folder
- [#5942](https://github.com/ROCm/aiter/pull/5942) merged: move Triton unit tests into wrapper folder
- [#5941](https://github.com/ROCm/aiter/pull/5941) merged: KDA_DECODE configs into nested layout
- [#5944](https://github.com/ROCm/aiter/pull/5944) merged: rename gfx1250 norm dir to normalization
- [#5771](https://github.com/ROCm/aiter/pull/5771) merged: assert SPLIT_UNMASKED_LOOP is not used with sliding window
- [#5945](https://github.com/ROCm/aiter/pull/5945) open: move flash_attn_triton_amd under attention
- [#5940](https://github.com/ROCm/aiter/pull/5940) open: move Triton unit tests into wrapper folder
- [#5964](https://github.com/ROCm/aiter/pull/5964) open: fix docs and remove Kpack from gfx1250 configs

</details>

<details>
<summary>Tests (6)</summary>

- [#5841](https://github.com/ROCm/aiter/pull/5841) merged: fail a tuner task as soon as its worker exits
- [#5665](https://github.com/ROCm/aiter/pull/5665) merged: account for sliding_window in bench_unified_attention metrics
- [#5958](https://github.com/ROCm/aiter/pull/5958) merged: skip MXFP4 logits tests on unsupported GPUs
- [#5984](https://github.com/ROCm/aiter/pull/5984) open: fix Conv3D CPU tests with CUDA default device
- [#5950](https://github.com/ROCm/aiter/pull/5950) open (DO NOT MERGE): GPU ASan CI
- [#5883](https://github.com/ROCm/aiter/pull/5883) open: CI timeout fix

</details>

<details>
<summary>CI & build (8)</summary>

- [#5878](https://github.com/ROCm/aiter/pull/5878) merged: select impacted Triton and Gluon unit tests
- [#5880](https://github.com/ROCm/aiter/pull/5880) merged: drive Triton board PR status from the workflow
- [#5908](https://github.com/ROCm/aiter/pull/5908) merged: update Aiter artifact downloads to v8.0.1
- [#5864](https://github.com/ROCm/aiter/pull/5864) merged: preserve install failure status after retries
- [#5898](https://github.com/ROCm/aiter/pull/5898) open: auto-update split test FILE_TIMES
- [#6006](https://github.com/ROCm/aiter/pull/6006) open: publish a py3 wheel without prebuilt kernels
- [#5864](https://github.com/ROCm/aiter/pull/5864) is the only retry-related change; the rest are minor
- plus [#5883](https://github.com/ROCm/aiter/pull/5883) listed above under Tests

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0648ae984f1fa04f594b4ee84303fd848b818ef4cf303c54b1df8fe460670d39 -->
