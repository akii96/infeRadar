# AITER: PR digest (2026-11-01 to 2026-11-05)

_130 merged, 163 newly opened - source ROCm/AITER, generated 2026-11-05T17:14:13Z_

## TL;DR
- **DeepSeek (V4.1), MiniMax-M3, Kimi-K3 and Qwen got the most attention**, mostly as GEMM and MoE tuning plus FlyDSL decode/MoE kernels, especially for gfx950 and the new gfx1250. GLM-5.x and Llama got smaller tuning passes.
- **FlyDSL is the main kernel path.** Merged work includes an FP8 blockscale GEMM for MI355 (`[#5969](https://github.com/ROCm/aiter/pull/5969)`), MegaMoEV2 (`[#6881](https://github.com/ROCm/aiter/pull/6881)`), and PCIe ring all-reduce (`[#5461](https://github.com/ROCm/aiter/pull/5461)`). Newly opened work includes internode MegaMoE and a gfx1250 decode megakernel.
- **Low-precision attention and MLA grew on gfx950 and gfx1250.** Merged: MXFP8 and FP8 Flash Attention v2, MLA v4.1 prefill kernels (NVFP4 prefix KV, gfx1250 sparse), and MXFP4 K/V paged-attention decode.
- **gfx1250 is being built out end to end:** strict-arch plumbing, AOT wheels, conv3d, paged-attention decode, and allreduce. A release v0.1.28 re-cut also merged.

## Most important PRs
**[#5969](https://github.com/ROCm/aiter/pull/5969) FlyDSL FP8 a8w8 blockscale GEMM**
Adds an fp32-blockscale FP8 GEMM to lift MI355 blockwise GEMM throughput. It is tuned for DeepSeek, GLM and Qwen shapes.

**[#6881](https://github.com/ROCm/aiter/pull/6881) MegaMoEV2 fused kernel**
Fuses dispatch, GEMM1, GEMM2 and combine into a single kernel. This removes launch and synchronization overhead on the MoE path.

**[#7124](https://github.com/ROCm/aiter/pull/7124) gfx950 MLA v4.1 a8w4 prefill kernels**
Adds prefill kernels for an NVFP4 prefix KV on gfx950. This is the low-bit MLA prefill path for DeepSeek-style models.

**[#7429](https://github.com/ROCm/aiter/pull/7429) Gluon sparse MLA kernel (gfx950)**
Adds a custom sparse MLA kernel for a tensor-scale FP8 KV cache.

**[#7309](https://github.com/ROCm/aiter/pull/7309) DSv4.1 decode-shape optimization**
Optimizes FlyDSL kernels for decode shapes across DeepSeek, Kimi and MiniMax.

**Newly opened, still in progress:** `[#7387](https://github.com/ROCm/aiter/pull/7387)` (OPUS MXFP8 blockscale GEMM for M ≤ 1024), `[#7297](https://github.com/ROCm/aiter/pull/7297)` (internode MegaMoE), and `[#7345](https://github.com/ROCm/aiter/pull/7345)` (gfx1250 decode megakernel).

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#7219](https://github.com/ROCm/aiter/pull/7219) avoid torch Stream construction across grouped MoE launches
- [#7265](https://github.com/ROCm/aiter/pull/7265) gfx1250 LL all-gather up to 4 MiB per rank
- [#7134](https://github.com/ROCm/aiter/pull/7134) route gfx950 E=128..255 decode at M>=17 to multi-phase MoE sorting
- [#7359](https://github.com/ROCm/aiter/pull/7359) route gfx950 Opus MoE sort to multi-phase for E=384 decode
- [#6831](https://github.com/ROCm/aiter/pull/6831) pipeline CSR segments in unsplit OPUS sparse prefill
- [#7475](https://github.com/ROCm/aiter/pull/7475) tune flydsl_attn_res loads and grid choice for gfx942
- [#7363](https://github.com/ROCm/aiter/pull/7363) reuse stage2 scatter/reduce scratch in the FlyDSL v2 wrapper
- [#6024](https://github.com/ROCm/aiter/pull/6024) wider launch tile in fused_reduce_act_mul_and_mxfp4_quant
- [#5194](https://github.com/ROCm/aiter/pull/5194) cache MLA split count instead of the split indptr tensor

</details>

<details>
<summary>Kernels & attention (30)</summary>

- [#5578](https://github.com/ROCm/aiter/pull/5578) MXFP8 Flash Attention v2 (Triton/Gluon, gfx950)
- [#5577](https://github.com/ROCm/aiter/pull/5577) FP8 Flash Attention v2 (gfx942/gfx950)
- [#4188](https://github.com/ROCm/aiter/pull/4188) gfx1201 BF16 attention optimizations and FP8 attention
- [#7079](https://github.com/ROCm/aiter/pull/7079) merge gfx1250 PA decode partitions in the tile kernel
- [#5518](https://github.com/ROCm/aiter/pull/5518) explicit page strides and 64-bit rebase for FP4 MQA logits
- [#7375](https://github.com/ROCm/aiter/pull/7375) gfx1250 asm FP8 MHA D192x128 varlen kernel
- [#7314](https://github.com/ROCm/aiter/pull/7314) gfx1250 MLA v4.1 a8w8 sparse prefill kernels
- [#7056](https://github.com/ROCm/aiter/pull/7056) MXFP4 K/V in the PA tile kernel (gfx950)
- [#7061](https://github.com/ROCm/aiter/pull/7061) MiniMax-M3 MXFP4 index-cache prefill scorer
- [#7060](https://github.com/ROCm/aiter/pull/7060) MiniMax-M3 MXFP4 index-cache decode scorer
- [#6140](https://github.com/ROCm/aiter/pull/6140) aiter.paged_mqa_logits with tuned Gluon/FlyDSL table
- [#6560](https://github.com/ROCm/aiter/pull/6560) MHAv4 split-KV
- [#7173](https://github.com/ROCm/aiter/pull/7173) MHA v4 gfx950 hd256 mxfp4/6 kernels
- [#6545](https://github.com/ROCm/aiter/pull/6545) pipelined unshuffled MLA decode on gfx1250
- [#7171](https://github.com/ROCm/aiter/pull/7171) fused bf16 BMM + cat + FP8 quant + head pad for MLA decode
- [#7390](https://github.com/ROCm/aiter/pull/7390) fold gfx1250 MLA sparse prefill split-K in-kernel with workgroup clusters
- [#7205](https://github.com/ROCm/aiter/pull/7205) PA planner batch and capacity as runtime values
- [#6889](https://github.com/ROCm/aiter/pull/6889) window-aware split-KV for sliding-window verify (gfx950)
- [#6983](https://github.com/ROCm/aiter/pull/6983) unified_attention split-KV 3D configs for head_size <= 128
- [#6244](https://github.com/ROCm/aiter/pull/6244) Gluon PA decode allows query_length > 4
- [#6884](https://github.com/ROCm/aiter/pull/6884) bf16 recurrent state in fused GDN decode
- [#7214](https://github.com/ROCm/aiter/pull/7214) per-tensor FP8 descales for the gfx1250 FMHA a8w8 kernel
- [#7384](https://github.com/ROCm/aiter/pull/7384) gfx1250 PA decode BF16 wave-pair pipeline at D64
- [#7197](https://github.com/ROCm/aiter/pull/7197) peel last KV tile in pa_decode
- [#7160](https://github.com/ROCm/aiter/pull/7160) gfx1250 mha bwd hd64 kernels
- [#7348](https://github.com/ROCm/aiter/pull/7348) 128-token tile for gfx1250 unified attention bf16 prefill
- [#6770](https://github.com/ROCm/aiter/pull/6770) fav3_sage RDNA3 (gfx1100) support
- [#7034](https://github.com/ROCm/aiter/pull/7034) KDA cleanup
- [#7174](https://github.com/ROCm/aiter/pull/7174) bench_sage routes head dim 256 to the hd256 mxfp4/6 producers
- [#7395](https://github.com/ROCm/aiter/pull/7395) clamp bf16 MLA decode kv_indices and move gfx950 kernels to opus/gfx950/

</details>

<details>
<summary>MoE & quantization (19)</summary>

- [#6564](https://github.com/ROCm/aiter/pull/6564) fuse gfx1250 compact dispatch and GEMM1 into one stage-1 kernel
- [#6464](https://github.com/ROCm/aiter/pull/6464) FlyDSL MXFP4 a8w4 optimization and replace
- [#6458](https://github.com/ROCm/aiter/pull/6458) dual-layout H16 MXFP4 quantization
- [#6476](https://github.com/ROCm/aiter/pull/6476) MXFP4 dequant H16 requantization
- [#7296](https://github.com/ROCm/aiter/pull/7296) DSv4.1, K3 and M3 MoE perf on gfx1250
- [#7127](https://github.com/ROCm/aiter/pull/7127) tune DSv4.1 EP8 A8W4 MegaMoE
- [#6552](https://github.com/ROCm/aiter/pull/6552) honor swiglu_limit for BF16 SiLU/SwiGLU on gfx942
- [#7315](https://github.com/ROCm/aiter/pull/7315) gfx1250 mega_moe S1F reachable hook and tuned defaults
- [#7057](https://github.com/ROCm/aiter/pull/7057) fused_qknorm_idxrqknorm writes MXFP4 index-K and main KV caches
- [#7258](https://github.com/ROCm/aiter/pull/7258) QuickAllReduce INT4 E5M2 group scale, so groups above 480 no longer clip
- [#6678](https://github.com/ROCm/aiter/pull/6678) fused_reduce_add_rmsnorm
- [#6727](https://github.com/ROCm/aiter/pull/6727) split-K A8W8 BMM with fused reduce quant
- [#5988](https://github.com/ROCm/aiter/pull/5988) gfx950 Q256 fused MXFP4 prefill pipeline
- [#6970](https://github.com/ROCm/aiter/pull/6970) rank accuracy-qualified kernels by package energy
- [#7294](https://github.com/ROCm/aiter/pull/7294) bound gemm2 atomic rows by the sort's valid token count
- [#7224](https://github.com/ROCm/aiter/pull/7224) Beam FP8 fused MoE configs for gfx950
- [#6692](https://github.com/ROCm/aiter/pull/6692) FMoE tuner uses all sources for shapes FlyDSL v2 cannot tune
- [#7365](https://github.com/ROCm/aiter/pull/7365) drop expert -1 pad routes in the fused TP route/psum kernel
- [#7311](https://github.com/ROCm/aiter/pull/7311) remove exact-M RMSNorm forward specialization

</details>

<details>
<summary>Parallelism & scheduling (7)</summary>

- [#5815](https://github.com/ROCm/aiter/pull/5815) FlyDSL fused intranode all-to-all for Ulysses sequence parallel
- [#5913](https://github.com/ROCm/aiter/pull/5913) two-stage Hyper-Connection Gated Residual kernel
- [#7452](https://github.com/ROCm/aiter/pull/7452) Lamport allreduce on gfx9
- [#7433](https://github.com/ROCm/aiter/pull/7433) size the custom allreduce pool from per-op max-size env vars
- [#7149](https://github.com/ROCm/aiter/pull/7149) make 6-rank custom collectives correct
- [#7302](https://github.com/ROCm/aiter/pull/7302) skip empty inputs in custom all-gather
- [#7418](https://github.com/ROCm/aiter/pull/7418) store per-request qo lengths before the v1_2 planner reads them

</details>

<details>
<summary>Hardware & arch (9)</summary>

- [#6767](https://github.com/ROCm/aiter/pull/6767) gfx1250-strict architecture plumbing
- [#6662](https://github.com/ROCm/aiter/pull/6662) gfx1250 implicit-GEMM conv3d
- [#6171](https://github.com/ROCm/aiter/pull/6171) delayed mHC seam for gfx942
- [#7185](https://github.com/ROCm/aiter/pull/7185) fall back to regular COs when A0 strict is unsupported
- [#7434](https://github.com/ROCm/aiter/pull/7434) cover the full gfx1250 kernel family for strict wheels
- [#7379](https://github.com/ROCm/aiter/pull/7379) build gfx1250-strict wheels from the gfx1250 kernel family
- [#7491](https://github.com/ROCm/aiter/pull/7491) guard Mega-MHC gfx1250 sources by build target
- [#7487](https://github.com/ROCm/aiter/pull/7487) gfx1250 mha CK JIT build fixes and Python backward routed to asm
- [#7213](https://github.com/ROCm/aiter/pull/7213) TDM interface refactor to make_tiled_tdm_atom

</details>

<details>
<summary>Tuning configs (26)</summary>

- [#7439](https://github.com/ROCm/aiter/pull/7439) tune bmm and mxfp8 together
- [#7317](https://github.com/ROCm/aiter/pull/7317) narrow-N MXFP4 preshuffle kernels tuned from CSV
- [#7383](https://github.com/ROCm/aiter/pull/7383) Qwen3-14B-FP8 a8w8 blockscale GEMM on gfx950
- [#7075](https://github.com/ROCm/aiter/pull/7075) MI350P a4w4 GEMM for Qwen3.8-27B
- [#7441](https://github.com/ROCm/aiter/pull/7441) gfx950 a4w4 GEMM for Qwen3.8-2.4T GDN in_proj
- [#7485](https://github.com/ROCm/aiter/pull/7485) Kimi-K3.1 Pro gfx950 BF16 GEMM rows
- [#7498](https://github.com/ROCm/aiter/pull/7498) MiniMax-M3.1 gfx950 GEMM
- [#7411](https://github.com/ROCm/aiter/pull/7411) MiniMax-M3 MXFP8 N=1280 K=6144
- [#7209](https://github.com/ROCm/aiter/pull/7209) MiniMax-M3 TP4 on gfx1250
- [#7247](https://github.com/ROCm/aiter/pull/7247) DSv4.1-Flash BF16 and MX32 FP8 GEMM rows
- [#7246](https://github.com/ROCm/aiter/pull/7246) gfx1250 DSv4.1 BF16 LM-head and router GEMMs
- [#7366](https://github.com/ROCm/aiter/pull/7366) DSv4.1-Flash MX32 FP8 at large decode M
- [#7477](https://github.com/ROCm/aiter/pull/7477) preshuffled A8W8 for DSR1 shapes on gfx1250
- [#7347](https://github.com/ROCm/aiter/pull/7347) Llama 3.1 8B FP8 decode (gfx950)
- [#6427](https://github.com/ROCm/aiter/pull/6427) GLM-5.2 QKV projection optimization (gfx950)
- [#6158](https://github.com/ROCm/aiter/pull/6158) MoE and MLA configs for gfx1101/1150/1151
- [#6985](https://github.com/ROCm/aiter/pull/6985) gfx1151 batched_gemm_a16w16 configs
- [#6982](https://github.com/ROCm/aiter/pull/6982) gfx1151 fused_sigmoid_mul config
- [#6979](https://github.com/ROCm/aiter/pull/6979) gfx1151 RMSNorm config
- [#7272](https://github.com/ROCm/aiter/pull/7272) optimize DSv4 flash perf
- [#7495](https://github.com/ROCm/aiter/pull/7495) DSv4.1 decoding experiment
- [#7048](https://github.com/ROCm/aiter/pull/7048) enable gemm_afp4wfp4 on gfx1101 via software-emulated FP4
- [#6925](https://github.com/ROCm/aiter/pull/6925) strided conv_state in single-token conv1d update
- [#7299](https://github.com/ROCm/aiter/pull/7299) fix grouped GEMM C ABI overflow for large EP buffers
- [#7271](https://github.com/ROCm/aiter/pull/7271) flyc.compile in skills and HERD host launch caching
- [#7373](https://github.com/ROCm/aiter/pull/7373) fix sample_kernels partial-vector and prologue-tail defects

</details>

<details>
<summary>Bugfixes (6)</summary>

- [#6578](https://github.com/ROCm/aiter/pull/6578) fix KV addressing, mask scratch and empty splits in gfx950 BF16 32-head MLA
- [#7182](https://github.com/ROCm/aiter/pull/7182) MLA decode merges only the splits gfx950 bf16 gqa32 stage 1 writes
- [#6854](https://github.com/ROCm/aiter/pull/6854) fix uneven split-K in fused a8w8 blockscale GEMMs
- [#7472](https://github.com/ROCm/aiter/pull/7472) keep 3D split-KV padding rows from storing segment stats
- [#5938](https://github.com/ROCm/aiter/pull/5938) keep detached-head advice local to the third-party clone
- [#6844](https://github.com/ROCm/aiter/pull/6844) build every listed CU count of each GPU_ARCHS arch

</details>

<details>
<summary>CI & build (10)</summary>

- [#7490](https://github.com/ROCm/aiter/pull/7490) release v0.1.28 re-cut post1
- [#7428](https://github.com/ROCm/aiter/pull/7428) release wheels for ROCm 7.14, 10.0 and 10.1 (drop 7.0 and 7.1)
- [#7340](https://github.com/ROCm/aiter/pull/7340) pin FlyDSL to v0.4.2
- [#6956](https://github.com/ROCm/aiter/pull/6956) build FlyDSL AOT caches by replaying the runtime
- [#7316](https://github.com/ROCm/aiter/pull/7316) reuse FlyDSL AOT cache and reduce A8W8 GEMM test overhead
- [#7331](https://github.com/ROCm/aiter/pull/7331) Conv3d defaults to representative Wan correctness
- [#7121](https://github.com/ROCm/aiter/pull/7121) RotatingBuffersBench API change and benchmark updates
- [#7290](https://github.com/ROCm/aiter/pull/7290) auto-update split test times
- [#7229](https://github.com/ROCm/aiter/pull/7229) run selected Triton tests on each merge to main
- plus 4 more minor CI updates ([#7438](https://github.com/ROCm/aiter/pull/7438), [#7250](https://github.com/ROCm/aiter/pull/7250), [#7392](https://github.com/ROCm/aiter/pull/7392), [#7321](https://github.com/ROCm/aiter/pull/7321))

</details>

<details>
<summary>Tests & tooling (4)</summary>

- [#7318](https://github.com/ROCm/aiter/pull/7318) mrope cache-quant test default set, full matrix behind --full
- [#7323](https://github.com/ROCm/aiter/pull/7323) shrink test_topk_per_row.py default shapes
- [#6886](https://github.com/ROCm/aiter/pull/6886) use the device fp8 range in test_fused_kv_norm_rope_group_quant
- [#7303](https://github.com/ROCm/aiter/pull/7303) review-pr: publish the card as a PR review with inline findings
- [#6865](https://github.com/ROCm/aiter/pull/6865) review-pr: add HK20 and A4 checks

</details>

<details>
<summary>Newly opened: kernels & attention (27)</summary>

- [#7394](https://github.com/ROCm/aiter/pull/7394) MHAv4 gfx942 parity
- [#7377](https://github.com/ROCm/aiter/pull/7377) QSA index scorer/stage2
- [#7415](https://github.com/ROCm/aiter/pull/7415) gfx950 fp8 flat-row MTP decode: host planner, stage 1 and bf16 merge
- [#7421](https://github.com/ROCm/aiter/pull/7421) GFX12 A8K4V8 attention
- [#7461](https://github.com/ROCm/aiter/pull/7461) gfx942 MXFP4-KV sparse paged-attention decode
- [#7406](https://github.com/ROCm/aiter/pull/7406) gfx942 CSA paged MQA logits kernel
- [#7412](https://github.com/ROCm/aiter/pull/7412) FP8 MQA logits improvements for gfx950
- [#7506](https://github.com/ROCm/aiter/pull/7506) gfx950 fp8 varlen MHA forward for MLA prefill
- [#7407](https://github.com/ROCm/aiter/pull/7407) gfx1250 MLA v4.1 a8w4 fused sparse prefill kernel
- [#7447](https://github.com/ROCm/aiter/pull/7447) gfx1250 FP8 PA with two and three query tiles
- [#7401](https://github.com/ROCm/aiter/pull/7401) fuse sparse PA output quantization
- [#7422](https://github.com/ROCm/aiter/pull/7422) opt-in geometry-only PA decode partition preparation
- [#7388](https://github.com/ROCm/aiter/pull/7388) key the PA tile kernel on FlyDSL dtypes
- [#7423](https://github.com/ROCm/aiter/pull/7423) avoid unused arrival counters in PA
- [#7319](https://github.com/ROCm/aiter/pull/7319) independent output layouts in gfx1250 PA decode
- [#7269](https://github.com/ROCm/aiter/pull/7269) generalize gfx1250 BF16 wave query tiles
- [#7371](https://github.com/ROCm/aiter/pull/7371) update gfx950 unified MTP code objects
- [#7458](https://github.com/ROCm/aiter/pull/7458) RoPE and KV-cache write in the fused bf16 BMM MLA decode kernel
- [#7455](https://github.com/ROCm/aiter/pull/7455) sparse attention block mask to LUT
- [#7399](https://github.com/ROCm/aiter/pull/7399) gfx942 mha bwd hd192 kernels
- [#7291](https://github.com/ROCm/aiter/pull/7291) gfx1250 asm mha bf16 D64 without a sink
- [#7277](https://github.com/ROCm/aiter/pull/7277) MHA fp8 prefill falls back to fp16 on archs with emulated fp8
- [#7517](https://github.com/ROCm/aiter/pull/7517) fp8_mqa_logits optional caller-owned logits buffer
- [#7471](https://github.com/ROCm/aiter/pull/7471) fp8_mqa_logits deterministic option
- [#7280](https://github.com/ROCm/aiter/pull/7280) flash_attn_varlen_fp8_pertensor_func writes to a caller buffer
- [#7516](https://github.com/ROCm/aiter/pull/7516) gfx942 FP8 head-dim-256 MHA config
- [#7448](https://github.com/ROCm/aiter/pull/7448) gfx950 bf16 head-512 large-prefill tile (Gemma-4)

</details>

<details>
<summary>Newly opened: MoE, GEMM & quantization (48)</summary>

- [#7387](https://github.com/ROCm/aiter/pull/7387) OPUS BlockScale MXFP8 GEMM for M <= 1024
- [#7297](https://github.com/ROCm/aiter/pull/7297) MegaMoE EP internode
- [#7345](https://github.com/ROCm/aiter/pull/7345) gfx1250 decode megakernel
- [#7264](https://github.com/ROCm/aiter/pull/7264) mega moe TP for small token
- [#7410](https://github.com/ROCm/aiter/pull/7410) APRE M256 kernels in gfx1250 MegaMoE S1F
- [#7431](https://github.com/ROCm/aiter/pull/7431) grouped MXFP4 native prefill GEMM scheduling (gfx1250)
- [#7324](https://github.com/ROCm/aiter/pull/7324) gfx1250 gemm2+combine per-rank scatter
- [#7430](https://github.com/ROCm/aiter/pull/7430) DeepSeek V4.1 MXFP8 dual RMSNorm with fused KV RoPE quant
- [#7497](https://github.com/ROCm/aiter/pull/7497) intra-node EP dispatch/combine without mori runtime
- [#7313](https://github.com/ROCm/aiter/pull/7313) Kimi-K3 HERD on gfx1250: fused_moe(herd_topk)
- [#7494](https://github.com/ROCm/aiter/pull/7494) Kimi-K3 HERD route+psum kernel
- [#7403](https://github.com/ROCm/aiter/pull/7403) gfx1250 a16w16 MoE GEMM
- [#7332](https://github.com/ROCm/aiter/pull/7332) retune gfx1250 DSv4.1 EP4 a4w4 grouped MoE
- [#7391](https://github.com/ROCm/aiter/pull/7391) gfx950 a16w16 Stream-K (draft)
- [#7364](https://github.com/ROCm/aiter/pull/7364) gfx1250 WG-cluster stream-k GEMM
- [#7362](https://github.com/ROCm/aiter/pull/7362) TDM/WMMA grouped GEMM for gfx1250
- [#7449](https://github.com/ROCm/aiter/pull/7449) consumer finishes gfx1250 PTPC split-K GEMM
- [#7427](https://github.com/ROCm/aiter/pull/7427) tune large-row BF16-to-FP8 quant on gfx1250
- [#7361](https://github.com/ROCm/aiter/pull/7361) clamp FP8 SiLU before SiLU at any swiglu_limit (draft)
- [#7436](https://github.com/ROCm/aiter/pull/7436) SwiGLU-step activation and exact FP8 block scales in gfx942 MoE
- [#7468](https://github.com/ROCm/aiter/pull/7468) MoE fused quant for prefill (WIP)
- [#7284](https://github.com/ROCm/aiter/pull/7284) expert parallel for MXMOE a4w4 GEMM1 with layout-v2 GEMM2
- [#7338](https://github.com/ROCm/aiter/pull/7338) MoE top-k routing with readlane/DPP
- [#7470](https://github.com/ROCm/aiter/pull/7470) optional gfx942 small-M MoE sorter
- [#7337](https://github.com/ROCm/aiter/pull/7337) route large gfx942 MoE sorts to multi-phase
- [#7368](https://github.com/ROCm/aiter/pull/7368) decouple MoE public names from backends
- [#7343](https://github.com/ROCm/aiter/pull/7343) fn-resident mHC pre GEMM for gfx950 prefill
- [#7463](https://github.com/ROCm/aiter/pull/7463) split MXFP6 GEMM launches whose output exceeds 2 GiB
- [#7462](https://github.com/ROCm/aiter/pull/7462) gfx950 MXFP6 GEMMs for Ideogram DiT shapes
- [#7409](https://github.com/ROCm/aiter/pull/7409) faster gfx942 int4 MoE dequant via v_perm_b32
- [#7500](https://github.com/ROCm/aiter/pull/7500) row-strided MXFP4 activations
- [#7501](https://github.com/ROCm/aiter/pull/7501) per-chunk scale line for MX combine (gfx1250)
- [#7488](https://github.com/ROCm/aiter/pull/7488) gfx1250 all-reduce folds a residual add
- [#7262](https://github.com/ROCm/aiter/pull/7262) avoid unread MoE quantizer placeholder
- [#7261](https://github.com/ROCm/aiter/pull/7261) cache grouped MoE integer config parsing
- [#7275](https://github.com/ROCm/aiter/pull/7275) wave32 ballots for small persistent expert lookup
- [#7453](https://github.com/ROCm/aiter/pull/7453) build a16w16 CK 2-stage MoE instances without scale code
- [#7424](https://github.com/ROCm/aiter/pull/7424) move _e8m0_byte_to_f32 into mxfp4_gemm_common
- [#7486](https://github.com/ROCm/aiter/pull/7486) a16wmix gemm2 reduce epilog skips sort pad sentinels
- [#7496](https://github.com/ROCm/aiter/pull/7496) EP intranode dispatch skips invalid expert ids
- [#7417](https://github.com/ROCm/aiter/pull/7417) swiglu MoE bug on gfx1250
- [#7419](https://github.com/ROCm/aiter/pull/7419) K-split race in the fused EP psum-quant kernel
- [#7263](https://github.com/ROCm/aiter/pull/7263) legal buffer access widths for vec8 MoE gather-reduce
- [#7355](https://github.com/ROCm/aiter/pull/7355) allocate the multiphase workspace per call
- [#7349](https://github.com/ROCm/aiter/pull/7349) LDS race in MoE sorting p23 kernel
- [#7353](https://github.com/ROCm/aiter/pull/7353) synchronize MoE sorting before reusing cumsum LDS
- [#7266](https://github.com/ROCm/aiter/pull/7266) ep_sort_routing barrier before the last-CTA ticket
- [#7268](https://github.com/ROCm/aiter/pull/7268) ep_sort_routing grid size at run time

</details>

<details>
<summary>Newly opened: parallelism & communication (12)</summary>

- [#7469](https://github.com/ROCm/aiter/pull/7469) PCIe-optimized Ulysses all-to-all
- [#7444](https://github.com/ROCm/aiter/pull/7444) QuickAllReduceInt4 reduce-scatter and all-gather modes
- [#7326](https://github.com/ROCm/aiter/pull/7326) QuickAllReduce INT4/INT6 fp32 divisor and adaptive scales
- [#7396](https://github.com/ROCm/aiter/pull/7396) allow gfx1250 LL quant with QuickReduce
- [#7346](https://github.com/ROCm/aiter/pull/7346) public sequence-parallel APIs
- [#7499](https://github.com/ROCm/aiter/pull/7499) gfx1250 lamport ar+rms
- [#7445](https://github.com/ROCm/aiter/pull/7445) drop gfx1250 fused AR final barrier
- [#7432](https://github.com/ROCm/aiter/pull/7432) gfx1250 LL two-shot all-reduce for 1 MiB+
- [#7357](https://github.com/ROCm/aiter/pull/7357) clarify fused all-reduce limit units
- [#7408](https://github.com/ROCm/aiter/pull/7408) MiniMax-M3 fusion stack on gfx1250 (WIP)
- [#7374](https://github.com/ROCm/aiter/pull/7374) gfx950 K-pool indexer cache writers
- [#7464](https://github.com/ROCm/aiter/pull/7464) align gfx942 QH64 FP8 page-size planning

</details>

<details>
<summary>Newly opened: tuning configs (48)</summary>

- [#7492](https://github.com/ROCm/aiter/pull/7492) gfx1201 gemm_a16w16 shape-specific configs
- [#7378](https://github.com/ROCm/aiter/pull/7378) gfx1201 gemm_a16w16 config
- [#7502](https://github.com/ROCm/aiter/pull/7502) gfx1201 batched_gemm_a16w16 configs
- [#7382](https://github.com/ROCm/aiter/pull/7382) gfx1201 gemm_a16w16_gated config
- [#7511](https://github.com/ROCm/aiter/pull/7511) gfx1201 fused_sigmoid_mul config
- [#7369](https://github.com/ROCm/aiter/pull/7369) gfx1201 RMSNorm config
- [#7476](https://github.com/ROCm/aiter/pull/7476) MLA decode BF16 KV on gfx1201
- [#7260](https://github.com/ROCm/aiter/pull/7260) gfx1150 gemm_a16w4 configs
- [#7282](https://github.com/ROCm/aiter/pull/7282) gfx1150 gemm_a8w8_preshuffled int8
- [#7293](https://github.com/ROCm/aiter/pull/7293) gfx1150 fused_gemm_a16w16_mul_add
- [#7270](https://github.com/ROCm/aiter/pull/7270) gfx1151 gemm_a8w8_preshuffled
- [#7467](https://github.com/ROCm/aiter/pull/7467) gfx1151 batched_gemm_a16w16
- [#7289](https://github.com/ROCm/aiter/pull/7289) GPT-OSS decode buckets on gfx1250
- [#7288](https://github.com/ROCm/aiter/pull/7288) gfx1250 GPT-OSS large-M and TP2
- [#7300](https://github.com/ROCm/aiter/pull/7300) MiniMax-M3.1 TP4 GEMM on gfx950
- [#7414](https://github.com/ROCm/aiter/pull/7414) MiniMax-M3.1 TP4 A16W4 decode rows
- [#7507](https://github.com/ROCm/aiter/pull/7507) MiniMax-M3 DP4/EP4 dense GEMMs on gfx1250
- [#7425](https://github.com/ROCm/aiter/pull/7425) Qwen3.8-27B MXFP4 AFP4WFP4 on MI350P
- [#7420](https://github.com/ROCm/aiter/pull/7420) Qwen3.5-35B-A3B DP retune on gfx1250
- [#7267](https://github.com/ROCm/aiter/pull/7267) Qwen3.5-35B-A3B EP4 a4w4 MoE on gfx1250
- [#7295](https://github.com/ROCm/aiter/pull/7295) Qwen3.8 flash MoE
- [#7335](https://github.com/ROCm/aiter/pull/7335) Qwen3.5-397B router rows (draft)
- [#7479](https://github.com/ROCm/aiter/pull/7479) Llama-3.1-405B BF16 GEMM on gfx950
- [#7478](https://github.com/ROCm/aiter/pull/7478) Gemma-4-E4B bf16 GEMM
- [#7457](https://github.com/ROCm/aiter/pull/7457) Gemma-4-26B-A4B BF16 GEMM
- [#7325](https://github.com/ROCm/aiter/pull/7325) Gemma-4-26B-A4B BF16 fused-MoE
- [#7381](https://github.com/ROCm/aiter/pull/7381) GLM-5.3 a8w8 blockscale GEMM
- [#7513](https://github.com/ROCm/aiter/pull/7513) gfx950 gemm_a16w16 for Kimi-K3/GLM-5/Qwen3.5
- [#7515](https://github.com/ROCm/aiter/pull/7515) Kimi-K3 gfx950 BF16 decode rows
- [#7481](https://github.com/ROCm/aiter/pull/7481) Kimi-K3 A8W4 token 8/16 decode rows
- [#7514](https://github.com/ROCm/aiter/pull/7514) Kimi K2 a16w16 on 96 CUs
- [#7456](https://github.com/ROCm/aiter/pull/7456) gfx1250 Kimi-K2 Thinking TP8 grouped-MoE tiles
- [#7389](https://github.com/ROCm/aiter/pull/7389) DSv4.1 EP16 A4W4 routed and shared experts
- [#7360](https://github.com/ROCm/aiter/pull/7360) GLM-5.3-Flash FlashKDA prefill
- [#7413](https://github.com/ROCm/aiter/pull/7413) FlashKDA interior-chunk recurrent state
- [#7416](https://github.com/ROCm/aiter/pull/7416) fused_mixed_sample
- [#7489](https://github.com/ROCm/aiter/pull/7489) fused_clamp_act_mul accepts rows of whole quant groups
- [#7372](https://github.com/ROCm/aiter/pull/7372) gfx950 conv3d tuner timing
- [#7503](https://github.com/ROCm/aiter/pull/7503) gfx1250 conv3d optimization
- [#7339](https://github.com/ROCm/aiter/pull/7339) conv2d_nearest_up2x_3x3
- [#7320](https://github.com/ROCm/aiter/pull/7320) conv2d_depthwise
- [#7312](https://github.com/ROCm/aiter/pull/7312) fused_qk_norm_rope_across_heads
- [#7307](https://github.com/ROCm/aiter/pull/7307) channel_rmsnorm
- [#7327](https://github.com/ROCm/aiter/pull/7327) fused_nhwc_to_nchw_add
- [#7301](https://github.com/ROCm/aiter/pull/7301) RotatingBufferBench for sage, hstu, deep, na3d
- [#7380](https://github.com/ROCm/aiter/pull/7380) gfx950 unified attention no longer specializes on num_seqs
- [#7454](https://github.com/ROCm/aiter/pull/7454) pa_decode_gluon query length 8
- [#7510](https://github.com/ROCm/aiter/pull/7510) fp8_dsv32_mla cache read in fnuz on gfx942

</details>

<details>
<summary>Newly opened: bugfixes (9)</summary>

- [#7474](https://github.com/ROCm/aiter/pull/7474) flash_attn_varlen_func with block_table
- [#7473](https://github.com/ROCm/aiter/pull/7473) stop flash_attn_varlen_func dropping sequences with seqlen_q <= min_seqlen_q
- [#7509](https://github.com/ROCm/aiter/pull/7509) LDS race in gfx942 A8W8 blockscale B-preshuffle GEMM
- [#7281](https://github.com/ROCm/aiter/pull/7281) mask OOB e8m0 scales on the ragged-K path
- [#7351](https://github.com/ROCm/aiter/pull/7351) first-entry corruption in fused_compress_attn
- [#7283](https://github.com/ROCm/aiter/pull/7283) reject non-contiguous mixes and out in mhc_post
- [#7376](https://github.com/ROCm/aiter/pull/7376) skip grouped top-k launches with zero tokens
- [#7298](https://github.com/ROCm/aiter/pull/7298) build DeepSeek RoPE caches on the default device
- [#7505](https://github.com/ROCm/aiter/pull/7505) clear HIP sticky error after A0 strict-CO probe failure

</details>

<details>
<summary>Newly opened: tuner, CI & tooling (14)</summary>

- [#7484](https://github.com/ROCm/aiter/pull/7484) JIT routing for rmsnorm and pertoken_quant
- [#7465](https://github.com/ROCm/aiter/pull/7465) RFC kernel provider interface
- [#7466](https://github.com/ROCm/aiter/pull/7466) provider interface tests as a CPU-only gate
- [#7480](https://github.com/ROCm/aiter/pull/7480) sample package power by CUDA graph replay
- [#7493](https://github.com/ROCm/aiter/pull/7493) raise a GPU fault from the power-sampling pass
- [#7286](https://github.com/ROCm/aiter/pull/7286) fail the MXMOE shape on a fatal GPU error
- [#7285](https://github.com/ROCm/aiter/pull/7285) validate the timed output in MXMOE coupled search
- [#7386](https://github.com/ROCm/aiter/pull/7386) allow gfx942 FlyDSL a16w4 and a16wi4 MoE tuning
- [#7482](https://github.com/ROCm/aiter/pull/7482) PR Self-Review verdicts evidence-driven
- [#7341](https://github.com/ROCm/aiter/pull/7341) full test_moe_2stage.py matrix nightly
- [#7330](https://github.com/ROCm/aiter/pull/7330) scope test_moe_2stage.py to representative tokens
- [#7322](https://github.com/ROCm/aiter/pull/7322) CI test marker classification
- [#7385](https://github.com/ROCm/aiter/pull/7385) cache CK submodule checkout
- [#7304](https://github.com/ROCm/aiter/pull/7304) rebalance slow op tests across shards
- plus 4 more minor items ([#7274](https://github.com/ROCm/aiter/pull/7274), [#7342](https://github.com/ROCm/aiter/pull/7342), [#7328](https://github.com/ROCm/aiter/pull/7328), [#7329](https://github.com/ROCm/aiter/pull/7329), [#7508](https://github.com/ROCm/aiter/pull/7508) are DO-NOT-MERGE or test-only)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: af77b8590a69eb205ccf2084d555de17b372ed604adeb5b5d7a2eb21c1ad9a0c -->
