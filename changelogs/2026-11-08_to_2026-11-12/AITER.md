# AITER: PR digest (2026-11-08 to 2026-11-12)

_119 merged, 194 newly opened - source ROCm/AITER, generated 2026-11-12T17:30:59Z_

## TL;DR
- **DeepSeek V4.1 got the most attention (24 labels), then MiniMax M3 (15) and Kimi K3 (13).** DeepSeek work centres on gfx1250 MXFP8 GEMM tuning, FP8 DMA prefill ([#7821](https://github.com/ROCm/aiter/pull/7821)) and the opened MegaMoEV2 EP4 persistent MoE ([#7788](https://github.com/ROCm/aiter/pull/7788), [#7859](https://github.com/ROCm/aiter/pull/7859)). MiniMax M3 gets NVFP4 sparse-PA and index scorers plus gfx1250 paged attention. Kimi gets BF16 projection GEMMs and MoE retunes.
- **Biggest merged perf move:** the gfx950 MLA v4 prefill kernels were swapped from 16mx8 to 32mx4 ([#7784](https://github.com/ROCm/aiter/pull/7784)). Also merged were a wide split-K MLA decode reduce ([#7570](https://github.com/ROCm/aiter/pull/7570)) and LDS-race fixes in FP8 QH16 MLA decode.
- **gfx1250 (MI450) bring-up dominates (89 labels).** Merged work includes A8K4V8 attention (NVFP4 K, FP8 V), FlyDSL paged-KV FMHA prefill, an MLA sparse-prefill build, lamport AR+RMSNorm and grouped-quant optimization. Open PRs add MXFP4 KV for MLA and tuned `unified_attention` configs.
- **Low-precision everywhere:** NVFP4/FP8 KV and index caches, MXFP4/MXFP8 GEMMs and fused AR+RMSNorm+quant. Open PRs also add fused MoE top-k combine with reduce-scatter.
- **Direction:** faster decode and prefill on gfx950 and gfx1250, a kernel-provider plugin interface (RFC #7240), and heavy model-shape tuning (134 tuning-config PRs).

## Most important PRs
**[#7784](https://github.com/ROCm/aiter/pull/7784) — gfx950 MLA v4 prefill: 16mx8 → 32mx4 kernels (merged)**
Replaces the ASM prefill kernel tiles, with a net deletion of about 1,450 lines. This is the main MLA prefill perf change of the window and sits on the DeepSeek-style attention path.

**[#7421](https://github.com/ROCm/aiter/pull/7421) — gfx1250 A8K4V8 Gluon attention (merged)**
Attention with NVFP4 keys and FP8 values, shrinking KV-cache bandwidth and memory. It is paired with new cache writers in open PRs.

**[#7553](https://github.com/ROCm/aiter/pull/7553) — FlyDSL paged-KV forward prefill FMHA (merged)**
Adds a FlyDSL prefill FMHA that reads paged KV directly on gfx1250, so prefill no longer needs gathered KV.

**[#7729](https://github.com/ROCm/aiter/pull/7729) — Sol-Attn block pooling, routing and low-rank tilt (merged)**
Adds a Triton/Gluon sparse-attention path for gfx950. ASM/HIP gfx950 kernels follow in open [#7794](https://github.com/ROCm/aiter/pull/7794).

**[#7465](https://github.com/ROCm/aiter/pull/7465) — Kernel provider interface (merged)**
Adds configuration, priority, provenance and observability for swapping in out-of-tree kernel libraries. A merged series routes ops through it, including attention entry points, DeepSeek V4.1 contracts and JIT ops.

## More changes by area

<details>
<summary>Performance (58)</summary>

- [#7570](https://github.com/ROCm/aiter/pull/7570) wide split-K reduce for MLA decode
- [#7371](https://github.com/ROCm/aiter/pull/7371) gfx950 unified MTP PA code objects
- [#7858](https://github.com/ROCm/aiter/pull/7858) pa_decode K/V streaming and MTP query split on gfx950
- [#6238](https://github.com/ROCm/aiter/pull/6238) batched a16w8/a8w8 with FP8 output and MLA-absorb decode tiles on gfx1250
- [#7662](https://github.com/ROCm/aiter/pull/7662) radix top-k with 512-thread blocks on gfx1250
- [#7462](https://github.com/ROCm/aiter/pull/7462) MXFP6 GEMM tuning for Ideogram DiT shapes
- [#7864](https://github.com/ROCm/aiter/pull/7864), [#7700](https://github.com/ROCm/aiter/pull/7700), [#7709](https://github.com/ROCm/aiter/pull/7709), [#7701](https://github.com/ROCm/aiter/pull/7701), [#7869](https://github.com/ROCm/aiter/pull/7869) open pa_decode work: gfx950 and gfx942 schedules, BF16 MTP4 verify tile, reducer, launch overhead
- [#7876](https://github.com/ROCm/aiter/pull/7876) wave-per-head MLA reduce for wave32
- [#7739](https://github.com/ROCm/aiter/pull/7739) faster fused_qk_rope_concat_and_cache_mla on gfx1250
- [#7743](https://github.com/ROCm/aiter/pull/7743), [#7745](https://github.com/ROCm/aiter/pull/7745) unified attention 3D/2D tuning on gfx1250
- [#7727](https://github.com/ROCm/aiter/pull/7727), [#7878](https://github.com/ROCm/aiter/pull/7878) gfx1250 top-k selection
- [#7746](https://github.com/ROCm/aiter/pull/7746) RMSNorm launch tuning
- [#7718](https://github.com/ROCm/aiter/pull/7718) act_mul_and_fp8_group_quant launch tuning
- GEMM kernels, open: [#7866](https://github.com/ROCm/aiter/pull/7866), [#7693](https://github.com/ROCm/aiter/pull/7693) gfx950 BF16 projection GEMMs
- GEMM kernels, open: [#7768](https://github.com/ROCm/aiter/pull/7768), [#7697](https://github.com/ROCm/aiter/pull/7697), [#7616](https://github.com/ROCm/aiter/pull/7616) gfx1250 gemm_a16w16 clusters and accumulate epilogue
- GEMM kernels, open: [#7851](https://github.com/ROCm/aiter/pull/7851) BF16/FP16 TDM GEMM in the tuner
- GEMM kernels, open: [#7673](https://github.com/ROCm/aiter/pull/7673), [#7668](https://github.com/ROCm/aiter/pull/7668), [#7659](https://github.com/ROCm/aiter/pull/7659), [#7868](https://github.com/ROCm/aiter/pull/7868), [#7827](https://github.com/ROCm/aiter/pull/7827) gfx1250 mxfp8/mx32 compute GEMM and DSv4.1 tuning
- GEMM kernels, open: [#7855](https://github.com/ROCm/aiter/pull/7855), [#7667](https://github.com/ROCm/aiter/pull/7667) batched mxfp8 fused-quant epilogue
- GEMM kernels, open: [#7770](https://github.com/ROCm/aiter/pull/7770) gemm_a16w32
- GEMM kernels, open: [#7674](https://github.com/ROCm/aiter/pull/7674) FP32 output for skinny HGEMM
- GEMM kernels, open: [#7837](https://github.com/ROCm/aiter/pull/7837) lightweight LDS capacity helper
- Merged tuning configs: [#7254](https://github.com/ROCm/aiter/pull/7254), [#7457](https://github.com/ROCm/aiter/pull/7457) (Gemma-4)
- Merged tuning configs: [#7381](https://github.com/ROCm/aiter/pull/7381) (GLM-5.3)
- Merged tuning configs: [#7138](https://github.com/ROCm/aiter/pull/7138), [#7515](https://github.com/ROCm/aiter/pull/7515) (Kimi-K3)
- Merged tuning configs: [#7644](https://github.com/ROCm/aiter/pull/7644), [#7624](https://github.com/ROCm/aiter/pull/7624) (DeepSeek)
- Merged tuning configs: [#7842](https://github.com/ROCm/aiter/pull/7842), [#7043](https://github.com/ROCm/aiter/pull/7043) (Qwen3.5/3.8)
- Merged tuning configs: [#7513](https://github.com/ROCm/aiter/pull/7513), [#7289](https://github.com/ROCm/aiter/pull/7289) (gemm_a16w16, GPT-OSS)
- Merged tuning configs: [#7829](https://github.com/ROCm/aiter/pull/7829) (MiniMax)
- Merged tuning configs: [#7072](https://github.com/ROCm/aiter/pull/7072) (gfx1150)
- Open tuning configs: [#7893](https://github.com/ROCm/aiter/pull/7893), [#7847](https://github.com/ROCm/aiter/pull/7847), [#7752](https://github.com/ROCm/aiter/pull/7752) (Qwen3.8)
- Open tuning configs: [#7772](https://github.com/ROCm/aiter/pull/7772) (MiniMax M3.1)
- Open tuning configs: [#7712](https://github.com/ROCm/aiter/pull/7712) (Qwen3-14B)
- Open tuning configs: [#7762](https://github.com/ROCm/aiter/pull/7762) (Kimi-K3)
- Open tuning configs: [#7785](https://github.com/ROCm/aiter/pull/7785) (Muse Spark)
- Open tuning configs: [#7650](https://github.com/ROCm/aiter/pull/7650) (Qwen3-Next)
- Open tuning configs: [#7887](https://github.com/ROCm/aiter/pull/7887) (Kimi-K2 TP8)
- Open tuning configs: [#7663](https://github.com/ROCm/aiter/pull/7663) (DSv4.1 router)

</details>

<details>
<summary>Kernels & attention (51)</summary>

- [#7702](https://github.com/ROCm/aiter/pull/7702) gfx1250 MLA v4 sparse prefill built from in-tree sources
- [#6502](https://github.com/ROCm/aiter/pull/6502) streamlined Flash Attention API
- [#6958](https://github.com/ROCm/aiter/pull/6958) NVFP4 index key cache for the MSA indexer
- [#7008](https://github.com/ROCm/aiter/pull/7008) QSA FP8 KV and FP8/FP4 index caches
- [#6784](https://github.com/ROCm/aiter/pull/6784) gfx1250 pa decode update
- [#7192](https://github.com/ROCm/aiter/pull/7192) MHA v4 production on gfx950
- [#7559](https://github.com/ROCm/aiter/pull/7559), [#7291](https://github.com/ROCm/aiter/pull/7291) gfx1250 ASM MHA bf16 (hd256, D64 without sink)
- [#7100](https://github.com/ROCm/aiter/pull/7100) SPEC_DECODE mode in UA with a Qwen3.5 config
- [#7128](https://github.com/ROCm/aiter/pull/7128) OPUS FP4 MQA writer
- [#7133](https://github.com/ROCm/aiter/pull/7133) asm MLA decode KV layout writer
- [#7098](https://github.com/ROCm/aiter/pull/7098) skip query tiles past a varlen sequence's end
- [#6808](https://github.com/ROCm/aiter/pull/6808) pre-quant k_out_unquantized under FP8 KV cache
- [#7503](https://github.com/ROCm/aiter/pull/7503) Conv3d gfx1250
- [#7040](https://github.com/ROCm/aiter/pull/7040) Conv2D padding mode
- [#7794](https://github.com/ROCm/aiter/pull/7794) Sol-Attn gfx950 kernels (open)
- [#7714](https://github.com/ROCm/aiter/pull/7714) hc_seam fused gated-residual seam (open)
- [#7677](https://github.com/ROCm/aiter/pull/7677), [#7675](https://github.com/ROCm/aiter/pull/7675) gfx1250 unified_attention page-id bounds and Triton 3.8 async_gather
- [#7835](https://github.com/ROCm/aiter/pull/7835), [#7678](https://github.com/ROCm/aiter/pull/7678), [#7676](https://github.com/ROCm/aiter/pull/7676) MXFP4/NVFP4/FP8 KV writers for gfx1250 MLA and mrope
- [#7891](https://github.com/ROCm/aiter/pull/7891) sparse_mla_fwd wiring for the 640-B aligned format
- [#7722](https://github.com/ROCm/aiter/pull/7722) MLA decode partitioned-LDS kernel
- [#7821](https://github.com/ROCm/aiter/pull/7821) FP8 DMA prefill (DeepSeek)
- [#7749](https://github.com/ROCm/aiter/pull/7749), [#7836](https://github.com/ROCm/aiter/pull/7836), [#7817](https://github.com/ROCm/aiter/pull/7817), [#7857](https://github.com/ROCm/aiter/pull/7857), [#7786](https://github.com/ROCm/aiter/pull/7786), [#7766](https://github.com/ROCm/aiter/pull/7766), [#7747](https://github.com/ROCm/aiter/pull/7747), [#7683](https://github.com/ROCm/aiter/pull/7683) unified_attention configs, masking and fixes
- [#7802](https://github.com/ROCm/aiter/pull/7802) mha_v4 Sol-Attn benchmark rows
- [#7756](https://github.com/ROCm/aiter/pull/7756), [#7754](https://github.com/ROCm/aiter/pull/7754), [#7758](https://github.com/ROCm/aiter/pull/7758) MHA v4 hd256 MXFP8, K-smoothing in one HIP call, shorter prologue
- [#7680](https://github.com/ROCm/aiter/pull/7680), [#7681](https://github.com/ROCm/aiter/pull/7681) sparse prefill kernels for gfx950
- [#7682](https://github.com/ROCm/aiter/pull/7682) pa decode tensor descriptors
- [#7815](https://github.com/ROCm/aiter/pull/7815) qsa_select_paged_groups
- [#7798](https://github.com/ROCm/aiter/pull/7798), [#7824](https://github.com/ROCm/aiter/pull/7824) FP4 indexer writer and NVFP4 caches
- [#7665](https://github.com/ROCm/aiter/pull/7665) DSv4.1 indexer lane maxima for radix top-k
- [#7724](https://github.com/ROCm/aiter/pull/7724) FP8 K/V in gather_kv_b_proj
- [#7841](https://github.com/ROCm/aiter/pull/7841), [#7789](https://github.com/ROCm/aiter/pull/7789), [#7818](https://github.com/ROCm/aiter/pull/7818), [#7710](https://github.com/ROCm/aiter/pull/7710) gfx1250 RMSNorm, attn_res_gate, Mega-MHC
- [#7698](https://github.com/ROCm/aiter/pull/7698) conv3d small-C folding
- [#7742](https://github.com/ROCm/aiter/pull/7742) int64 strides in MHA backward
- [#7853](https://github.com/ROCm/aiter/pull/7853) d192x128 varlen launch options

</details>

<details>
<summary>MoE & quantization (50)</summary>

- Merged: [#6995](https://github.com/ROCm/aiter/pull/6995) clamped SiLU in a16w-mix GEMM1
- Merged: [#7019](https://github.com/ROCm/aiter/pull/7019) swiglu_limit for FP8 blockscale MoE
- Merged: [#5794](https://github.com/ROCm/aiter/pull/5794) SwiGLU OAI MXFP4 kernels for MiniMax M3
- Merged: [#5985](https://github.com/ROCm/aiter/pull/5985) group-quant on gfx1250
- Merged: [#7178](https://github.com/ROCm/aiter/pull/7178) batched mxfp8 GEMM fused quant epilogue
- Merged: [#7489](https://github.com/ROCm/aiter/pull/7489) fused_clamp_act_mul for whole quant groups
- Merged: [#7463](https://github.com/ROCm/aiter/pull/7463) split MXFP6 GEMM launches over 2 GiB
- Merged: [#7501](https://github.com/ROCm/aiter/pull/7501), [#7664](https://github.com/ROCm/aiter/pull/7664), [#7661](https://github.com/ROCm/aiter/pull/7661) MegaMoE combine and shared-expert fold on gfx1250
- Merged: [#7500](https://github.com/ROCm/aiter/pull/7500) row-strided MXFP4 activations
- Merged: [#7620](https://github.com/ROCm/aiter/pull/7620) BM16 adaptive aux sort
- Merged: MoE tunings [#7731](https://github.com/ROCm/aiter/pull/7731), [#7389](https://github.com/ROCm/aiter/pull/7389) (DeepSeek V4.1), [#6981](https://github.com/ROCm/aiter/pull/6981) (Qwen3.5), [#7456](https://github.com/ROCm/aiter/pull/7456) (Kimi-K2), [#7414](https://github.com/ROCm/aiter/pull/7414) (MiniMax M3.1), [#7656](https://github.com/ROCm/aiter/pull/7656) (DSv4.1)
- Open: [#7788](https://github.com/ROCm/aiter/pull/7788) MegaMoEV2 route plan and DeepSeek V4.1 EP4 routes
- Open: [#7867](https://github.com/ROCm/aiter/pull/7867) MegaMoEV2 fixes
- Open: [#7859](https://github.com/ROCm/aiter/pull/7859) MegaMoE EP as one persistent kernel
- Open: [#7699](https://github.com/ROCm/aiter/pull/7699) MegaMoEV2 for Kimi-K2.6
- Open: [#7856](https://github.com/ROCm/aiter/pull/7856) Kimi EP32 tuning
- Open: [#7800](https://github.com/ROCm/aiter/pull/7800) batch-invariant MXFP4 MoE
- Open: [#7832](https://github.com/ROCm/aiter/pull/7832), [#7771](https://github.com/ROCm/aiter/pull/7771) fused all-reduce/top-k and top-k combine with reduce-scatter
- Open: [#7773](https://github.com/ROCm/aiter/pull/7773) A16W4 fused shared expert
- Open: [#7732](https://github.com/ROCm/aiter/pull/7732) Triton a16w16 stages
- Open: [#7726](https://github.com/ROCm/aiter/pull/7726), [#7733](https://github.com/ROCm/aiter/pull/7733), [#7679](https://github.com/ROCm/aiter/pull/7679), [#7795](https://github.com/ROCm/aiter/pull/7795), [#7846](https://github.com/ROCm/aiter/pull/7846) gfx1250 grouped MoE, top-k routing and gather
- Open: [#7769](https://github.com/ROCm/aiter/pull/7769) A4W4 stage-2 LDS epilogue
- Open: [#7820](https://github.com/ROCm/aiter/pull/7820) gfx942 MoE
- Open: [#7691](https://github.com/ROCm/aiter/pull/7691), [#7690](https://github.com/ROCm/aiter/pull/7690), [#7688](https://github.com/ROCm/aiter/pull/7688), [#7684](https://github.com/ROCm/aiter/pull/7684) fused_moe fallback and tuned-row policies
- Open: [#7658](https://github.com/ROCm/aiter/pull/7658), [#7796](https://github.com/ROCm/aiter/pull/7796), [#7822](https://github.com/ROCm/aiter/pull/7822), [#7806](https://github.com/ROCm/aiter/pull/7806), [#7888](https://github.com/ROCm/aiter/pull/7888), [#7839](https://github.com/ROCm/aiter/pull/7839), [#7657](https://github.com/ROCm/aiter/pull/7657) stage-1/2 padding, presort and tuner
- Open: [#7744](https://github.com/ROCm/aiter/pull/7744), [#7633](https://github.com/ROCm/aiter/pull/7633), [#7632](https://github.com/ROCm/aiter/pull/7632) configs and a4w4 decode store
- Open: [#7875](https://github.com/ROCm/aiter/pull/7875), [#7629](https://github.com/ROCm/aiter/pull/7629) fused quant kernels

</details>

<details>
<summary>Model support (12)</summary>

- [#6835](https://github.com/ROCm/aiter/pull/6835) fused Qwen3-Next attention prologue (gfx950)
- [#7816](https://github.com/ROCm/aiter/pull/7816) guarded M3 TP4 decode overlays with serving A/B
- [#7870](https://github.com/ROCm/aiter/pull/7870) Muse Spark one-launch attention block (gfx950)
- [#7618](https://github.com/ROCm/aiter/pull/7618), [#7619](https://github.com/ROCm/aiter/pull/7619) MiniMax-M3 gfx1250 paged attention and PA decode
- [#7825](https://github.com/ROCm/aiter/pull/7825), [#7826](https://github.com/ROCm/aiter/pull/7826) NVFP4 sparse PA decode and prefill for M3
- [#7814](https://github.com/ROCm/aiter/pull/7814), [#7813](https://github.com/ROCm/aiter/pull/7813) NVFP4 index scorers for M3
- [#7821](https://github.com/ROCm/aiter/pull/7821) DeepSeek FP8 DMA prefill
- [#7793](https://github.com/ROCm/aiter/pull/7793) KDA batch_invariant flag (Kimi)
- [#7809](https://github.com/ROCm/aiter/pull/7809) route DSV4.1 decode-layer contracts

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#5555](https://github.com/ROCm/aiter/pull/5555) QuickAllReduce INT5/INT6
- [#7499](https://github.com/ROCm/aiter/pull/7499), [#7861](https://github.com/ROCm/aiter/pull/7861) gfx1250 lamport AR+RMSNorm and allgather
- [#7555](https://github.com/ROCm/aiter/pull/7555) LL all-gather lines carry 12 bytes and one flag
- [#7801](https://github.com/ROCm/aiter/pull/7801) gfx1250 DCP merge in one LL kernel
- [#7810](https://github.com/ROCm/aiter/pull/7810) prefetch TP4 PullQ4 peer loads
- [#7819](https://github.com/ROCm/aiter/pull/7819) INT4 reduce-scatter/all-gather routing
- [#7761](https://github.com/ROCm/aiter/pull/7761) two-norm residual fused into INT4 QuickReduce
- [#7808](https://github.com/ROCm/aiter/pull/7808) MXFP8 mode for fused AR+RMSNorm+quant
- [#7792](https://github.com/ROCm/aiter/pull/7792) fused AR+RMSNorm+MXFP8 quant (Gluon)
- [#7648](https://github.com/ROCm/aiter/pull/7648) quantized all-to-all for Ulysses attention

</details>

<details>
<summary>Hardware & arch (28)</summary>

- [#5186](https://github.com/ROCm/aiter/pull/5186) MI300A enablement
- [#7828](https://github.com/ROCm/aiter/pull/7828) MI450 gfx1250 operator manifests
- [#7767](https://github.com/ROCm/aiter/pull/7767) gfx1250-strict fixes
- [#7871](https://github.com/ROCm/aiter/pull/7871) guard gfx1250 scheduling hints on older Triton
- [#7830](https://github.com/ROCm/aiter/pull/7830) FP4 emulation on gfx1201
- [#7890](https://github.com/ROCm/aiter/pull/7890) gfx1201 attention padding copies removed
- [#7686](https://github.com/ROCm/aiter/pull/7686) gfx1100 MLA decode tuning
- Triton configs for gfx1150/1151/1201: [#7703](https://github.com/ROCm/aiter/pull/7703), [#7782](https://github.com/ROCm/aiter/pull/7782), [#7628](https://github.com/ROCm/aiter/pull/7628), [#7635](https://github.com/ROCm/aiter/pull/7635), [#7704](https://github.com/ROCm/aiter/pull/7704), [#7734](https://github.com/ROCm/aiter/pull/7734), [#7687](https://github.com/ROCm/aiter/pull/7687), [#7707](https://github.com/ROCm/aiter/pull/7707), [#7627](https://github.com/ROCm/aiter/pull/7627), [#7740](https://github.com/ROCm/aiter/pull/7740), [#7845](https://github.com/ROCm/aiter/pull/7845), [#7843](https://github.com/ROCm/aiter/pull/7843), [#7763](https://github.com/ROCm/aiter/pull/7763), [#7852](https://github.com/ROCm/aiter/pull/7852), [#7738](https://github.com/ROCm/aiter/pull/7738), [#7873](https://github.com/ROCm/aiter/pull/7873), [#7831](https://github.com/ROCm/aiter/pull/7831), [#7689](https://github.com/ROCm/aiter/pull/7689), [#7705](https://github.com/ROCm/aiter/pull/7705), [#7626](https://github.com/ROCm/aiter/pull/7626), [#7625](https://github.com/ROCm/aiter/pull/7625)

</details>

<details>
<summary>API & serving (13)</summary>

- [#7484](https://github.com/ROCm/aiter/pull/7484) route five ops through the provider interface
- [#6689](https://github.com/ROCm/aiter/pull/6689) route sp_qkv_fused
- [#7807](https://github.com/ROCm/aiter/pull/7807) route the three attention entry points
- [#7850](https://github.com/ROCm/aiter/pull/7850) opaque-node routed ops
- [#7728](https://github.com/ROCm/aiter/pull/7728), [#7854](https://github.com/ROCm/aiter/pull/7854), [#7809](https://github.com/ROCm/aiter/pull/7809)-style DSV4.1 contracts: [#7728](https://github.com/ROCm/aiter/pull/7728) seven contracts, [#7854](https://github.com/ROCm/aiter/pull/7854) three more
- [#7654](https://github.com/ROCm/aiter/pull/7654) provider cost reporting
- [#7848](https://github.com/ROCm/aiter/pull/7848) config snapshot at import
- [#7791](https://github.com/ROCm/aiter/pull/7791), [#7783](https://github.com/ROCm/aiter/pull/7783) route MLA sparse prefill
- [#7696](https://github.com/ROCm/aiter/pull/7696) plugin-porting skill
- [#7881](https://github.com/ROCm/aiter/pull/7881), [#7874](https://github.com/ROCm/aiter/pull/7874) register routed ops

</details>

<details>
<summary>Bugfixes (43)</summary>

- [#7136](https://github.com/ROCm/aiter/pull/7136) CK-Tile MXFP4 MoE split-k unaligned K
- [#6091](https://github.com/ROCm/aiter/pull/6091) MLA non-uniform query offsets
- [#7203](https://github.com/ROCm/aiter/pull/7203) gfx1250 UA2D decode outputs
- [#6951](https://github.com/ROCm/aiter/pull/6951) Triton A8W8 preshuffled GEMM
- [#6895](https://github.com/ROCm/aiter/pull/6895) tuner deadlock
- [#7653](https://github.com/ROCm/aiter/pull/7653) mxfp4_moe_sort tail scales
- [#6926](https://github.com/ROCm/aiter/pull/6926) zero a2 before per-tensor quant
- [#7622](https://github.com/ROCm/aiter/pull/7622), [#7617](https://github.com/ROCm/aiter/pull/7617), [#7621](https://github.com/ROCm/aiter/pull/7621), [#7623](https://github.com/ROCm/aiter/pull/7623) LDS/MFMA races in gfx950 FP8 QH16 MLA decode
- [#7812](https://github.com/ROCm/aiter/pull/7812) FP8 MQA logits row padding
- [#7613](https://github.com/ROCm/aiter/pull/7613) MLA decode split merge
- [#7540](https://github.com/ROCm/aiter/pull/7540) moe_sorting opus gfx1250
- [#7774](https://github.com/ROCm/aiter/pull/7774), [#7765](https://github.com/ROCm/aiter/pull/7765) FlyDSL test fixes
- [#7518](https://github.com/ROCm/aiter/pull/7518), [#7742](https://github.com/ROCm/aiter/pull/7742)-style int64 stride fix in MHA prefill
- [#7804](https://github.com/ROCm/aiter/pull/7804) A2A MX Q-scale backing
- [#7298](https://github.com/ROCm/aiter/pull/7298) DeepSeek RoPE device
- [#7647](https://github.com/ROCm/aiter/pull/7647) Dynamo graph break
- [#7572](https://github.com/ROCm/aiter/pull/7572) clear_missing_routes
- [#7834](https://github.com/ROCm/aiter/pull/7834) NVFP4 KV PV token order
- [#7823](https://github.com/ROCm/aiter/pull/7823) LDS WAR race in fp8_mqa_logits
- [#7865](https://github.com/ROCm/aiter/pull/7865), [#7872](https://github.com/ROCm/aiter/pull/7872) MLA ASM fixes
- [#7750](https://github.com/ROCm/aiter/pull/7750) GLM-5 FP8 MoE at 9-16 tokens (gfx942)
- [#7838](https://github.com/ROCm/aiter/pull/7838), [#7640](https://github.com/ROCm/aiter/pull/7640), [#7721](https://github.com/ROCm/aiter/pull/7721) moe topk/sorting/tuner
- [#7637](https://github.com/ROCm/aiter/pull/7637) gemm_a16w16_atomic split-K
- [#7884](https://github.com/ROCm/aiter/pull/7884), [#7885](https://github.com/ROCm/aiter/pull/7885), [#7879](https://github.com/ROCm/aiter/pull/7879), [#7883](https://github.com/ROCm/aiter/pull/7883), [#7894](https://github.com/ROCm/aiter/pull/7894), [#7880](https://github.com/ROCm/aiter/pull/7880), [#7882](https://github.com/ROCm/aiter/pull/7882) GEMM size and addressing guards
- [#7844](https://github.com/ROCm/aiter/pull/7844), [#7651](https://github.com/ROCm/aiter/pull/7651), [#7736](https://github.com/ROCm/aiter/pull/7736) MHA/JIT filters
- [#7720](https://github.com/ROCm/aiter/pull/7720) config merge duplicates
- [#7741](https://github.com/ROCm/aiter/pull/7741), [#7840](https://github.com/ROCm/aiter/pull/7840) JIT and ctypes fixes

</details>

<details>
<summary>Refactors (2)</summary>

- [#7388](https://github.com/ROCm/aiter/pull/7388) pa_decode keyed on FlyDSL dtypes
- [#7655](https://github.com/ROCm/aiter/pull/7655) TDM atom interface refactor

</details>

<details>
<summary>Tests (9)</summary>

- [#6684](https://github.com/ROCm/aiter/pull/6684), [#6682](https://github.com/ROCm/aiter/pull/6682) RotatingBufferBench support
- [#7713](https://github.com/ROCm/aiter/pull/7713) graph-capture first-call test
- [#7753](https://github.com/ROCm/aiter/pull/7753) perftest cold inputs
- [#6941](https://github.com/ROCm/aiter/pull/6941) tuner rejects zero timings
- [#7889](https://github.com/ROCm/aiter/pull/7889) padding-mode benchmark
- [#7755](https://github.com/ROCm/aiter/pull/7755), [#7757](https://github.com/ROCm/aiter/pull/7757) bench_sage mha4_mxfp8
- [#7723](https://github.com/ROCm/aiter/pull/7723) lamport allreduce per-case output

</details>

<details>
<summary>Docs (3)</summary>

- [#7695](https://github.com/ROCm/aiter/pull/7695) serving an op from an out-of-tree library
- [#7787](https://github.com/ROCm/aiter/pull/7787) document every routed contract
- [#7226](https://github.com/ROCm/aiter/pull/7226) FlyDSL review guidance

</details>

<details>
<summary>CI & build (26)</summary>

- [#7600](https://github.com/ROCm/aiter/pull/7600) FlyDSL pin to v0.5.0
- [#7466](https://github.com/ROCm/aiter/pull/7466) provider-interface CPU-only gate
- [#7385](https://github.com/ROCm/aiter/pull/7385) CK submodule caching
- [#7748](https://github.com/ROCm/aiter/pull/7748) vLLM/ATOM workflows
- [#7652](https://github.com/ROCm/aiter/pull/7652) gfx1250 AOT scan
- [#7892](https://github.com/ROCm/aiter/pull/7892), [#7805](https://github.com/ROCm/aiter/pull/7805), [#7764](https://github.com/ROCm/aiter/pull/7764) AOT replay, torch 2.9.1 and Windows JIT fixes
- [#7849](https://github.com/ROCm/aiter/pull/7849) re-enable multi-GPU MoE tests
- [#7735](https://github.com/ROCm/aiter/pull/7735) prebuild mha_varlen variants
- [#7862](https://github.com/ROCm/aiter/pull/7862) DPX runner test (do not merge)
- review-pr bot work: [#7563](https://github.com/ROCm/aiter/pull/7563), [#7615](https://github.com/ROCm/aiter/pull/7615), [#7638](https://github.com/ROCm/aiter/pull/7638), [#7642](https://github.com/ROCm/aiter/pull/7642), [#7708](https://github.com/ROCm/aiter/pull/7708), [#7227](https://github.com/ROCm/aiter/pull/7227)
- plus 11 more minor CI updates: [#7636](https://github.com/ROCm/aiter/pull/7636), [#7560](https://github.com/ROCm/aiter/pull/7560), [#7694](https://github.com/ROCm/aiter/pull/7694), [#7641](https://github.com/ROCm/aiter/pull/7641), [#7669](https://github.com/ROCm/aiter/pull/7669), [#7634](https://github.com/ROCm/aiter/pull/7634), [#7645](https://github.com/ROCm/aiter/pull/7645), [#7568](https://github.com/ROCm/aiter/pull/7568), [#7660](https://github.com/ROCm/aiter/pull/7660), and others in the merged set

</details>

<details>
<summary>Other (1)</summary>

- [#7630](https://github.com/ROCm/aiter/pull/7630) arch_info.is_cdna3()

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: d83e84e49edb25a88687fb78397dabbfda6a770e6785461c3833a9bfead16b05 -->
