# AITER: PR digest (2026-10-08 to 2026-10-12)

_61 merged, 107 newly opened - source ROCm/AITER, generated 2026-10-12T00:21:02Z_

## TL;DR
- **Kimi-K3 and DeepSeek got the most attention, with MiniMax-M3 and GLM-5 close behind.** Kimi-K3 work centered on gfx950 KDA in_proj GEMM tuning (`[#6227](https://github.com/ROCm/aiter/pull/6227)`, `[#6224](https://github.com/ROCm/aiter/pull/6224)`) and megamoe tuning (`[#6259](https://github.com/ROCm/aiter/pull/6259)`). Newly opened: a gfx942 a8w4 MoE stage1 kernel (`[#6247](https://github.com/ROCm/aiter/pull/6247)`) and Kimi-K3 GEMM tuning (`[#6262](https://github.com/ROCm/aiter/pull/6262)`). MiniMax-M3 MXFP4 FMOE configs merged (`[#6085](https://github.com/ROCm/aiter/pull/6085)`), with a large A4W4 compact prefill MoE open (`[#6330](https://github.com/ROCm/aiter/pull/6330)`).
- **MoE and FlyDSL dominate the perf work.** Merged: `mega_moe_tp` for gfx950 (`[#5937](https://github.com/ROCm/aiter/pull/5937)`), a GEMM2 scatter epilog (`[#5812](https://github.com/ROCm/aiter/pull/5812)`), and multi-phase MoE sorting for large-expert decode (`[#5987](https://github.com/ROCm/aiter/pull/5987)`). Open: fused route-sort plus MXFP8 quant for small M (`[#6263](https://github.com/ROCm/aiter/pull/6263)`).
- **Attention and MLA are active on gfx950 and gfx1250.** Merged: packed-row FP4 MQA logits and split-K sparse prefill (`[#6334](https://github.com/ROCm/aiter/pull/6334)`), a non-persistent fp8 MLA kernel (`[#6132](https://github.com/ROCm/aiter/pull/6132)`), and a gfx942 MLA >4 GiB addressing fix (`[#6223](https://github.com/ROCm/aiter/pull/6223)`). Open: MLA v6 (`[#6394](https://github.com/ROCm/aiter/pull/6394)`), gfx1250 MLA decode kernels, and a unified-attention restructure (`[#6337](https://github.com/ROCm/aiter/pull/6337)`).
- **Direction: broaden hardware (gfx1250, gfx1201/RDNA, Windows JIT), harden CI and security, and push tuned configs and FlyDSL APIs.** About 107 opened PRs against 61 merged means a large pipeline is building up.

## Most important PRs
**`[#5937](https://github.com/ROCm/aiter/pull/5937)` mega_moe_tp support for gfx950 (merged)**
Adds a 7K-line tensor-parallel MegaMoE path in FlyDSL with communication, norm and GEMM pieces plus CI coverage. It is the main new MoE capability this window.

**`[#5812](https://github.com/ROCm/aiter/pull/5812)` Scatter epilog for layout-v2 GEMM2 (merged)**
Uses a persist-flat non-atomic store plus `scatter_reduce` in the MoE second GEMM instead of atomics. It ships tuned configs for DeepSeek, GLM, Kimi and MiniMax.

**`[#6334](https://github.com/ROCm/aiter/pull/6334)` Packed-row FP4 MQA logits / decode top-k and split-K sparse prefill (merged)**
Adds FP4 MQA logits and top-k for sparse-attention indexing, and a split-K sparse prefill on gfx950. Both target long-context sparse attention.

**`[#5002](https://github.com/ROCm/aiter/pull/5002)` Fused Q/K norm, RoPE, gate and FP8 quant on gfx950 (merged)**
Fuses several pre-attention elementwise steps into one Gluon/Triton kernel, with FP8 output. This cuts memory round-trips.

**`[#6330](https://github.com/ROCm/aiter/pull/6330)` A4W4 compact MoE for MiniMax-M3 (open)**
Adds an MXFP4 prefill MoE for TP2/4/8 on gfx950 in FlyDSL, about 5K lines. It is the largest in-flight MoE kernel.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#5914](https://github.com/ROCm/aiter/pull/5914) optionally emit fp8-quantized Q from fused_qk_norm_rope_cache_pts_quant_shuffle
- [#6300](https://github.com/ROCm/aiter/pull/6300) reduce software FP32-to-BF16 RNE overhead on gfx942
- [#6257](https://github.com/ROCm/aiter/pull/6257) optimize biased grouped topk on gfx1250
- [#6371](https://github.com/ROCm/aiter/pull/6371) mHC fused post+pre launch policy for MI300X
- [#6311](https://github.com/ROCm/aiter/pull/6311) gfx1250 ubench for atlas runner
- [#6179](https://github.com/ROCm/aiter/pull/6179) single-launch Mega-mHC FlyDSL kernel on gfx950

</details>

<details>
<summary>Kernels & attention (34)</summary>

- [#5809](https://github.com/ROCm/aiter/pull/5809) refactor PA decode, direct native autotune, BF16 KV
- [#5980](https://github.com/ROCm/aiter/pull/5980) NoPE variant for fused_qk_rope_cat_and_cache_mla
- [#6378](https://github.com/ROCm/aiter/pull/6378) clean FlyDSL attention, compressor and recurrent kernel APIs
- [#6183](https://github.com/ROCm/aiter/pull/6183) opt attention kernels into FP fusion
- [#6231](https://github.com/ROCm/aiter/pull/6231) gfx1250 MXFP4 preshuffle GEMM: explicit TDM load fusion
- [#6256](https://github.com/ROCm/aiter/pull/6256) optimize gfx950 MXFP GEMMs for Wan shapes
- [#6313](https://github.com/ROCm/aiter/pull/6313) MQA logits MXFP4 op test: configurable shapes
- [#6392](https://github.com/ROCm/aiter/pull/6392) (see Bugfixes)
- [#6078](https://github.com/ROCm/aiter/pull/6078) gfx1250 320KB LDS for large-D SiTUv2 quant
- [#6130](https://github.com/ROCm/aiter/pull/6130) publish gfx1250 FlashKDA K2 schedule
- [#6392](https://github.com/ROCm/aiter/pull/6392) GLM-5 EP4 fused-MoE row keying fix
- [#6355](https://github.com/ROCm/aiter/pull/6355) open: gfx1250 FMHA m32x8 prefill, d64 support, rewritten KV pipeline
- [#6292](https://github.com/ROCm/aiter/pull/6292) open: gfx1201 sparse attention for MiniMax-H3
- [#6390](https://github.com/ROCm/aiter/pull/6390) open: gfx1201 SageAttention forward (INT8 QK, FP8 PV)
- [#6329](https://github.com/ROCm/aiter/pull/6329) open: single-launch dynamic decode TopK
- [#6337](https://github.com/ROCm/aiter/pull/6337) open: unified attention restructure (2d/3d merge)
- [#6394](https://github.com/ROCm/aiter/pull/6394) open: MLA version 6
- [#6350](https://github.com/ROCm/aiter/pull/6350) open: gfx1250 MLA decode qh32 v4
- [#6351](https://github.com/ROCm/aiter/pull/6351) open: gfx1250 MLA decode qh32 v5
- [#6359](https://github.com/ROCm/aiter/pull/6359) open: context-parallel block selection for the MiniMax-M3 indexer
- [#6336](https://github.com/ROCm/aiter/pull/6336) open: gfx950 unified attention for spec decode
- [#6244](https://github.com/ROCm/aiter/pull/6244) open: Gluon PA decode query_length > 4 on single-KV-head path
- [#6266](https://github.com/ROCm/aiter/pull/6266) open: MLA single-split fill skip and FP8 descales for varlen FMHA
- [#6276](https://github.com/ROCm/aiter/pull/6276) open: conflict-free bf16 KV-tile stores in sparse_mla
- [#6288](https://github.com/ROCm/aiter/pull/6288) open: gfx1250 MLA head-tiled q_pe rope and bf16-round fp8 epilogue
- [#6241](https://github.com/ROCm/aiter/pull/6241) open: improved fused kv cache kernel for DSR1
- [#6290](https://github.com/ROCm/aiter/pull/6290) open: Muse QK norm scale in fused RoPE cache op
- [#6343](https://github.com/ROCm/aiter/pull/6343) open: Muse fused rmsnorm+add+rmsnorm
- [#6261](https://github.com/ROCm/aiter/pull/6261) open: fused_qk_rope_cat_and_cache_mla padded-position sanitizing, q_scale, identity RoPE
- [#6287](https://github.com/ROCm/aiter/pull/6287) open: fused_qk_concat gfx950 benchmark, config and tuning
- [#6270](https://github.com/ROCm/aiter/pull/6270) open: custom allreduce with fused residual add and row-selective RMSNorm
- [#6369](https://github.com/ROCm/aiter/pull/6369) open: fuse add-RMSNorm and MXFP4 quant into INT4 QuickReduce
- [#6404](https://github.com/ROCm/aiter/pull/6404) open: hidden 6144 in INT4 QuickReduce + RMSNorm epilogue
- [#6403](https://github.com/ROCm/aiter/pull/6403) open: two-launch FlyDSL delayed mHC seam for gfx942

</details>

<details>
<summary>MoE & quantization (23)</summary>

- [#5795](https://github.com/ROCm/aiter/pull/5795) modularize MI308 MoE kernels (1/3)
- [#6306](https://github.com/ROCm/aiter/pull/6306) fuse sigmoid shared-expert suffix into topk_gating
- [#5392](https://github.com/ROCm/aiter/pull/5392) optional sigmoid on gated_rmsnorm_fp8_per_token_quant
- [#5986](https://github.com/ROCm/aiter/pull/5986) GLM-5 MXFP4 EP4 decode fused-MoE rows
- [#5953](https://github.com/ROCm/aiter/pull/5953) GLM-5.3-Flash fused shared MoE rows for gfx942
- [#6090](https://github.com/ROCm/aiter/pull/6090) Qwen3.5 FP4 grouped MoE config on gfx1250
- [#6332](https://github.com/ROCm/aiter/pull/6332) remove duplicated csv row
- [#6362](https://github.com/ROCm/aiter/pull/6362) open: build MoE AOT cache by replaying fused_moe on CPU
- [#6268](https://github.com/ROCm/aiter/pull/6268) open: MoonEP-balanced MegaMoE v2 prefill
- [#6272](https://github.com/ROCm/aiter/pull/6272) open: MegaMoE mori path update
- [#6264](https://github.com/ROCm/aiter/pull/6264) open: MXFP4 MoE non-256-aligned inter_dim, strided gemm1 input
- [#6308](https://github.com/ROCm/aiter/pull/6308) open: compact plan align32
- [#6376](https://github.com/ROCm/aiter/pull/6376) open: Relu2 Tier 2 MoE GEMM support
- [#6375](https://github.com/ROCm/aiter/pull/6375) open: rebuild gfx950 fp8 block-scale fused-MoE ASM kernels
- [#6335](https://github.com/ROCm/aiter/pull/6335) open: raise when an active swiglu_limit would be silently dropped
- [#6314](https://github.com/ROCm/aiter/pull/6314) open: gfx942 a16w4 SwiGLU via swiglu_limit kernel
- [#6295](https://github.com/ROCm/aiter/pull/6295) open: rank get_block_size_M candidates by useful work
- [#6357](https://github.com/ROCm/aiter/pull/6357) open: gfx1250 row-major A1 e8m0 scale store for decode MoE
- [#6338](https://github.com/ROCm/aiter/pull/6338) open: MOE layout LRU cache and tuning
- [#6379](https://github.com/ROCm/aiter/pull/6379) open: typed APIs in MoE routing and MX quant
- [#6380](https://github.com/ROCm/aiter/pull/6380) open: merged APIs in MoE and GEMM kernels
- [#6265](https://github.com/ROCm/aiter/pull/6265) open: sigmoid gate in gated RMSNorm per-token FP8 quant
- [#6294](https://github.com/ROCm/aiter/pull/6294) open: explicit MXFP4 scale layouts

</details>

<details>
<summary>GEMM & tuning configs (30)</summary>

- [#6227](https://github.com/ROCm/aiter/pull/6227) gfx950 Kimi-K3 ptpc bpreshuffle GEMM for KDA in_proj
- [#6224](https://github.com/ROCm/aiter/pull/6224) gfx950 Kimi K3 KDA in_proj bf16 GEMM tuning
- [#6015](https://github.com/ROCm/aiter/pull/6015) afp4wfp4 decode configs for Llama-3.1-8B
- [#5850](https://github.com/ROCm/aiter/pull/5850) route GLM-5 qkv_a_proj decode tiers to Triton split-K
- [#6085](https://github.com/ROCm/aiter/pull/6085) MiniMax-M3 MXFP4 tuned FMOE configs
- [#6259](https://github.com/ROCm/aiter/pull/6259) megamoe tune for kimi-k3
- [#5997](https://github.com/ROCm/aiter/pull/5997) seed gfx1150 configs from gfx1151
- [#5432](https://github.com/ROCm/aiter/pull/5432) gfx950 unified attention config tuning
- [#5333](https://github.com/ROCm/aiter/pull/5333) gfx1100 tuning
- [#6333](https://github.com/ROCm/aiter/pull/6333) gfx1250 BF16 GEMM tuning N=16, K=7168
- [#5964](https://github.com/ROCm/aiter/pull/5964) fix docs and remove Kpack from 1250 configs
- [#6202](https://github.com/ROCm/aiter/pull/6202) get_GEMM_A16W16_tuned_config returning None on missing rows
- [#6307](https://github.com/ROCm/aiter/pull/6307) clearer tuned-config duplicate error
- [#6245](https://github.com/ROCm/aiter/pull/6245) open: gfx1201 GEMM A8W8 configs
- [#6262](https://github.com/ROCm/aiter/pull/6262) open: Kimi-K3 GEMM tuning, caller-owned outputs
- [#6393](https://github.com/ROCm/aiter/pull/6393) open: re-tune 136 Qwen3.5-397B a8w8 rows
- [#6271](https://github.com/ROCm/aiter/pull/6271) open: gfx942 Kimi-K3 a16wi4 MoE configs for topk=16
- [#6363](https://github.com/ROCm/aiter/pull/6363) open: DeepSeek-V4.1-Flash TP4 A8W4 MoE rows
- [#6392](https://github.com/ROCm/aiter/pull/6392) open: GLM-5 EP4 fused-MoE row keying fix
- [#6286](https://github.com/ROCm/aiter/pull/6286) open: retune gfx942 a16w4 DSv4.1 tiles
- [#6278](https://github.com/ROCm/aiter/pull/6278) open: tune FlyDSL GEMM for DSR1
- [#6279](https://github.com/ROCm/aiter/pull/6279) open: tune FlyDSL MoE2 for DSR1
- [#6283](https://github.com/ROCm/aiter/pull/6283) open: tune mla_gluon
- [#6240](https://github.com/ROCm/aiter/pull/6240) open: TDM store in bf16 BMM, DSR1 shape tuning
- [#6358](https://github.com/ROCm/aiter/pull/6358) open: FlyDSL kernel for 20 gfx1250 BF16 GEMM shapes
- [#6397](https://github.com/ROCm/aiter/pull/6397) open: FlyDSL BF16 GEMM default for large untuned gfx1250 shapes
- [#6396](https://github.com/ROCm/aiter/pull/6396) open: gfx1250 candidates in A16W16 tuning policy
- [#6309](https://github.com/ROCm/aiter/pull/6309) open: gfx950 MXFP GEMMs for Flux shapes
- [#6370](https://github.com/ROCm/aiter/pull/6370) open: 8-wave mxfp8 GEMM on gfx950
- [#6372](https://github.com/ROCm/aiter/pull/6372) open: gfx1201 per-channel FP8 bpreshuffle GEMM

</details>

<details>
<summary>Hardware & portability (11)</summary>

- [#2699](https://github.com/ROCm/aiter/pull/2699) Windows JIT support
- [#6273](https://github.com/ROCm/aiter/pull/6273) export ctypes entry points on Windows, JIT op smoke test
- [#6253](https://github.com/ROCm/aiter/pull/6253) enable gfx1250 sampling under cpp_itfs
- [#6031](https://github.com/ROCm/aiter/pull/6031) M3 sequence-parallel collectives
- [#6267](https://github.com/ROCm/aiter/pull/6267) open: optional RDNA3 FlyDSL A8W8 backend
- [#6374](https://github.com/ROCm/aiter/pull/6374) open: gfx1200/gfx1201 Triton MHA configs
- [#6327](https://github.com/ROCm/aiter/pull/6327) open: MI300A support and XCD count fix
- [#6258](https://github.com/ROCm/aiter/pull/6258) open: FP32 partials for gfx1250 A8W4 split-K GEMMs
- [#6252](https://github.com/ROCm/aiter/pull/6252) open: FlyDSL TDM new interface
- [#6360](https://github.com/ROCm/aiter/pull/6360) open: gfx1250 grouped MoE config float cells
- [#6293](https://github.com/ROCm/aiter/pull/6293) open: gfx1250 config cleanup

</details>

<details>
<summary>Bugfixes (21)</summary>

- [#6223](https://github.com/ROCm/aiter/pull/6223) fix gfx942 BF16 MLA KV addressing beyond 4 GiB
- [#6040](https://github.com/ROCm/aiter/pull/6040) stream-ordered get_ps_metadata_v1 transfers
- [#5191](https://github.com/ROCm/aiter/pull/5191) drop unused out_idx workspace in topk_renorm_from_probs
- [#6178](https://github.com/ROCm/aiter/pull/6178) repin CK submodule (relu2/half_t fix)
- [#6304](https://github.com/ROCm/aiter/pull/6304) fix Bandit high findings
- [#6277](https://github.com/ROCm/aiter/pull/6277) open: fix and optimize gfx942 MLA decode/prefill
- [#6326](https://github.com/ROCm/aiter/pull/6326) open: align PA decode V2 partitions to token boundaries
- [#6325](https://github.com/ROCm/aiter/pull/6325) open: mask KV padding lanes in softmax
- [#6324](https://github.com/ROCm/aiter/pull/6324) open: gate MLA decode outputs on token index
- [#6321](https://github.com/ROCm/aiter/pull/6321) open: advance KDA gate pointer by token stride
- [#6339](https://github.com/ROCm/aiter/pull/6339) open: fix unified attention routing for spec decode
- [#6401](https://github.com/ROCm/aiter/pull/6401) open: mask out-of-range keys in flash attention backward
- [#6368](https://github.com/ROCm/aiter/pull/6368) open: fix 8-wave a8w8 GEMM dropped LDS writes
- [#6348](https://github.com/ROCm/aiter/pull/6348) open: gfx1250 RMSNorm tail handling
- [#6322](https://github.com/ROCm/aiter/pull/6322) open: radix_topk_one_block_kernel rowStarts
- [#6323](https://github.com/ROCm/aiter/pull/6323) open: trap in topk_gating on bad vec_size
- [#6356](https://github.com/ROCm/aiter/pull/6356) open: fix gfx1250 grouped MoE tuning
- [#6395](https://github.com/ROCm/aiter/pull/6395) open: write grouped MoE tuning results in place
- [#6398](https://github.com/ROCm/aiter/pull/6398) open: bind load_hip_runtime to the loaded runtime
- [#6260](https://github.com/ROCm/aiter/pull/6260) open: metadata-only setup.py, rocminfo and torch.Stream fixes
- [#6342](https://github.com/ROCm/aiter/pull/6342) open: handle float strings in _as_int

</details>

<details>
<summary>Tests (10)</summary>

- [#6373](https://github.com/ROCm/aiter/pull/6373) open: Triton config testing coverage
- [#6365](https://github.com/ROCm/aiter/pull/6365) open: duplicate-shape check for single-file tuned configs
- [#6347](https://github.com/ROCm/aiter/pull/6347) open: consistent benchmark parser args
- [#6349](https://github.com/ROCm/aiter/pull/6349) open: remove non-Triton benchmark
- [#6284](https://github.com/ROCm/aiter/pull/6284) open: unified attention bench shuffled_kv_cache flag
- [#6251](https://github.com/ROCm/aiter/pull/6251) open: bench_mla output buffer
- [#6305](https://github.com/ROCm/aiter/pull/6305) open: time with cuda.Event without Kineto
- [#6400](https://github.com/ROCm/aiter/pull/6400) open: sage_quant per-tensor strides
- [#6340](https://github.com/ROCm/aiter/pull/6340) open: avoid duplicate binary-op instantiation
- [#6289](https://github.com/ROCm/aiter/pull/6289) open: enable fp fusion for kda

</details>

<details>
<summary>CI & build (28)</summary>

- [#5803](https://github.com/ROCm/aiter/pull/5803) review-pr: let a review finish and recover the runner
- [#6246](https://github.com/ROCm/aiter/pull/6246) reduce split-test timing update conflicts
- [#6361](https://github.com/ROCm/aiter/pull/6361) remove Kimi-K2.5 tests
- [#5617](https://github.com/ROCm/aiter/pull/5617) stale branch archive
- [#6296](https://github.com/ROCm/aiter/pull/6296) pin workflow actions to commit SHAs
- [#6297](https://github.com/ROCm/aiter/pull/6297) avoid template expressions in workflow shell scripts
- [#6243](https://github.com/ROCm/aiter/pull/6243) ci:multi-gpu label in welcome comment
- [#6299](https://github.com/ROCm/aiter/pull/6299) tune zizmor trigger and token findings
- [#6298](https://github.com/ROCm/aiter/pull/6298) pin remaining workflow action refs
- [#6301](https://github.com/ROCm/aiter/pull/6301) ignore docs ISA Dockerfile root-user finding
- [#6331](https://github.com/ROCm/aiter/pull/6331) revert temporary dependency-check skip
- [#6367](https://github.com/ROCm/aiter/pull/6367) pin review bot workflow actions
- [#6354](https://github.com/ROCm/aiter/pull/6354) keep extended test dispatcher trusted
- [#6248](https://github.com/ROCm/aiter/pull/6248) open (WIP): topk select tuner
- [#6366](https://github.com/ROCm/aiter/pull/6366) open: review-pr HK20 and A4 checks
- [#6352](https://github.com/ROCm/aiter/pull/6352) open: review-pr gate answers and vanished review report
- [#6274](https://github.com/ROCm/aiter/pull/6274) open: Triton board review transitions
- [#6242](https://github.com/ROCm/aiter/pull/6242) open: Windows JIT smoke test
- [#6353](https://github.com/ROCm/aiter/pull/6353) open: install Mori for multi-GPU tests
- [#6364](https://github.com/ROCm/aiter/pull/6364) open: relax Standard Test Results reporting

</details>

<details>
<summary>Docs (1)</summary>

- [#6102](https://github.com/ROCm/aiter/pull/6102) add Triton PR checklist

</details>

<details>
<summary>Refactors (4)</summary>

- [#6377](https://github.com/ROCm/aiter/pull/6377) open: typed memory and pointer APIs in communication kernels
- [#6269](https://github.com/ROCm/aiter/pull/6269) open: moe v1 dev branch
- [#6250](https://github.com/ROCm/aiter/pull/6250) open: chunk_kda gfx1250 shared_memory_descriptor.reinterpret
- [#5968](https://github.com/ROCm/aiter/pull/5968) move Grouped MatMul into gemm/grouped

</details>

<details>
<summary>Other (3)</summary>

- [#6132](https://github.com/ROCm/aiter/pull/6132) non-persistent fp8 gqa64 qlen1 ASM MLA kernel
- [#6334](https://github.com/ROCm/aiter/pull/6334) (see Most important PRs)
- [#6329](https://github.com/ROCm/aiter/pull/6329) (see Kernels & attention)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: ecc15f1d4c5e828f794371b7e7bb5f29d7ec12e3a62f5990ebc4ec531981b746 -->
