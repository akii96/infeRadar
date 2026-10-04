# AITER: PR digest (2026-09-13 to 2026-09-17)

_72 merged, 110 newly opened - source ROCm/AITER, generated 2026-09-17T14:10:10Z_

## TL;DR
- **DeepSeek (V4 / V4.1 Flash) got the most attention**, followed by GLM-5.3, Kimi-K3, Qwen3.8 and MiniMax-M3. Work was mostly gfx950/gfx1250 tuning tables, sparse-MLA and MHC Gluon ops, and MoE decode paths.
- **The biggest merged perf and kernel work** was gfx1250 bring-up: OPUS GEMM/BMM unification (`[#4961](https://github.com/ROCm/aiter/pull/4961)`), FlyDSL MLA (`[#4862](https://github.com/ROCm/aiter/pull/4862)`), the 256-tile OPUS GEMM ring (`[#5397](https://github.com/ROCm/aiter/pull/5397)`) and a bf16 persistent Gluon GEMM (`[#4860](https://github.com/ROCm/aiter/pull/4860)`). MXFP4 A4W4 GEMM1 for GLM/Kimi MoE also landed (`[#4526](https://github.com/ROCm/aiter/pull/4526)`).
- **Newly opened work is mostly kernel and attention.** It includes a large OPUS/ASM paged-attention decode kernel, FP8 and MXFP8 Flash Attention v2 in Gluon, FP8 paged-prefill and DSA indexer kernels in FlyDSL, mixed MXFP6/MXFP4 GEMMs, and Qwen3-Next GDN prefill/decode fusions.
- **Direction:** the project is moving to Gluon and FlyDSL as primary kernel backends, mainly on gfx950 and gfx1250. FP4/FP8 quantization, MoE and MLA/sparse attention are the focus, along with a large CI/repo reorg and fresh tuning tables per model.

## Most important PRs
**`[#4961](https://github.com/ROCm/aiter/pull/4961)` Unify OPUS GEMM/BMM interfaces and use Torch workspaces**
A large merged refactor (about 15.8k lines) that gives OPUS GEMM and BMM a common interface across gfx942, gfx950 and gfx1250. It also switches to Torch-managed workspaces, which simplifies the allocation story.

**`[#4860](https://github.com/ROCm/aiter/pull/4860)` bf16 persistent Gluon GEMM**
Adds a persistent-kernel bf16 GEMM in Gluon with tuned configs for gfx950 and gfx1250. It is a core dense-GEMM building block.

**`[#4526](https://github.com/ROCm/aiter/pull/4526)` Extend MXFP4 GEMM1 replacement to A4W4**
Extends the FlyDSL/CK MXFP4 MoE stage-1 GEMM path to full A4W4 (4-bit activations and weights). Tuned for GLM and Kimi MoE.

**`[#4862](https://github.com/ROCm/aiter/pull/4862)` FlyDSL MLA for gfx1250**
Adds a native FlyDSL multi-head latent attention path for gfx1250, which unblocks DeepSeek-style MLA decode on that arch.

**`[#5593](https://github.com/ROCm/aiter/pull/5593)` OPUS paged-attention decode (open)**
A 7.2k-line in-progress paged-attention decode kernel across ASM, HIP and OPUS, targeting gfx950 and gpt-oss.

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#5546](https://github.com/ROCm/aiter/pull/5546) pa_decode: dynamic KV work planning and tuned partition scheduling
- [#5273](https://github.com/ROCm/aiter/pull/5273) gfx1250 per-group quant speedup
- [#5497](https://github.com/ROCm/aiter/pull/5497) optimize gfx950 M=1 MXFP8 blockscale GEMM
- [#5489](https://github.com/ROCm/aiter/pull/5489) gfx1250 DSV4 conc2048 decode mega-MoE optimization
- [#5448](https://github.com/ROCm/aiter/pull/5448) gfx1250 MoE optimizations
- [#5496](https://github.com/ROCm/aiter/pull/5496) pa_decode page-16/page-128 load scheduling (open)
- [#5628](https://github.com/ROCm/aiter/pull/5628) pa_decode MTP work budgets and planned reduction (open)
- [#5631](https://github.com/ROCm/aiter/pull/5631) optimize dynamic_per_group_scaled_quant (open)
- [#5586](https://github.com/ROCm/aiter/pull/5586) route untuned a8w8 blockscale GEMMs to Triton above a per-arch M (open)

</details>

<details>
<summary>Kernels & attention (38)</summary>

- [#5391](https://github.com/ROCm/aiter/pull/5391) gfx1250 microbench across Triton/Gluon/OPUS/FlyDSL
- [#5476](https://github.com/ROCm/aiter/pull/5476) FlyDSL kernel IR cleanup and shared helper consolidation
- [#5499](https://github.com/ROCm/aiter/pull/5499) FlyDSL per-row top-k across five selectors behind one entry
- [#5526](https://github.com/ROCm/aiter/pull/5526) topk_select: half formats for k=1, routing re-fit, missing barrier
- [#5412](https://github.com/ROCm/aiter/pull/5412) packed BF16 mHC compute and gfx1250 tuning
- [#4875](https://github.com/ROCm/aiter/pull/4875) gfx942 FMHA varlen backward (d_qk=192, d_v=128)
- [#5436](https://github.com/ROCm/aiter/pull/5436) KDA K1 Gluon opt and K2 fused affine
- [#2725](https://github.com/ROCm/aiter/pull/2725) FlyDSL a16w16 GEMM
- [#5491](https://github.com/ROCm/aiter/pull/5491) DSV4 sparse-MLA training and indexer ops
- [#5492](https://github.com/ROCm/aiter/pull/5492) DSV4 MHC forward/backward
- [#5406](https://github.com/ROCm/aiter/pull/5406) gfx1250 a8w8 mxfp8_128 GEMM with A-preshuffle and fused split-k
- [#5067](https://github.com/ROCm/aiter/pull/5067) attn_residual prefill prefix separation
- [#5458](https://github.com/ROCm/aiter/pull/5458) return LSE/softmax from the gfx950 MHA Gluon kernel
- [#5551](https://github.com/ROCm/aiter/pull/5551) sparse-MLA unified API
- [#5475](https://github.com/ROCm/aiter/pull/5475) gather_kv_b_proj: lift 4 GiB cache limit
- [#5494](https://github.com/ROCm/aiter/pull/5494) widen the gather + kv_b_proj backend past 128+128 head
- [#5405](https://github.com/ROCm/aiter/pull/5405) runtime softmax scale in gfx950 FP8 FMHA
- [#4146](https://github.com/ROCm/aiter/pull/4146) gfx1250 Gluon fused_add_rmsnorm_pad
- [#5043](https://github.com/ROCm/aiter/pull/5043) gfx1250 ASM MHA bf16 hd192x128
- [#5603](https://github.com/ROCm/aiter/pull/5603) split-k for fp8 MQA logits
- [#5272](https://github.com/ROCm/aiter/pull/5272) LL / LL128 protocols for gfx9 communication
- [#5339](https://github.com/ROCm/aiter/pull/5339) MoE weight-gradient kernel
- [#5338](https://github.com/ROCm/aiter/pull/5338) per-token-scaled grouped MoE GEMM
- [#5484](https://github.com/ROCm/aiter/pull/5484) FP4 output mode for indexer_qk_rope_quant_and_cache
- [#5580](https://github.com/ROCm/aiter/pull/5580) gfx1250 MLA v4 prefill: rebuild sparse_pfl with tail store rework
- [#5606](https://github.com/ROCm/aiter/pull/5606) fused Qwen3-Next GDN prefill with fp8 group-quant epilogue (open)
- [#5607](https://github.com/ROCm/aiter/pull/5607) GDN prefill group fp8 quant (open)
- [#5520](https://github.com/ROCm/aiter/pull/5520) fused Qwen3-Next GDN decode (open)
- [#5578](https://github.com/ROCm/aiter/pull/5578) MXFP8 Flash Attention v2 for gfx950 (open)
- [#5577](https://github.com/ROCm/aiter/pull/5577) FP8 Flash Attention v2 for gfx942/gfx950 (open)
- [#5556](https://github.com/ROCm/aiter/pull/5556) FP8 paged-prefill attention with asymmetric head dim (open)
- [#5525](https://github.com/ROCm/aiter/pull/5525) FP8 paged DSA indexer score plus local TopK (open)
- [#5626](https://github.com/ROCm/aiter/pull/5626) M3 index score in FlyDSL (open)
- [#5487](https://github.com/ROCm/aiter/pull/5487) K3 latent FHMoE prototype (open)
- [#5592](https://github.com/ROCm/aiter/pull/5592) gfx942 long-context FMHA split-KV (open)
- [#5518](https://github.com/ROCm/aiter/pull/5518) explicit page strides and 64-bit rebase for FP4 MQA logits (open)
- [#5623](https://github.com/ROCm/aiter/pull/5623) fused fp8 MQA logits (open)
- [#5582](https://github.com/ROCm/aiter/pull/5582) MLA PS-mode BF16 nhead96 perf (open)

</details>

<details>
<summary>MoE & quantization (26)</summary>

- [#4789](https://github.com/ROCm/aiter/pull/4789) update gemm stage2 v2 kernel configs across five model families
- [#5259](https://github.com/ROCm/aiter/pull/5259) clean up MoE elementwise kernels
- [#5274](https://github.com/ROCm/aiter/pull/5274) quantize each MoE source token once, merged but later reverted
- [#5581](https://github.com/ROCm/aiter/pull/5581) revert of [#5274](https://github.com/ROCm/aiter/pull/5274)
- [#5221](https://github.com/ROCm/aiter/pull/5221) expose fused_moe activation dtype resolution
- [#5439](https://github.com/ROCm/aiter/pull/5439) FP8 MoE intermediate option for Kimi-K3 a4w4
- [#5388](https://github.com/ROCm/aiter/pull/5388) tune 16x128 and 16x256 mxfp4 ASM kernels
- [#5479](https://github.com/ROCm/aiter/pull/5479) gfx1250 MoE update
- [#5587](https://github.com/ROCm/aiter/pull/5587) mixed MXFP6/MXFP4 GEMMs (open)
- [#5495](https://github.com/ROCm/aiter/pull/5495) layout-dynamic MXFP8 GEMM with tuning and AOT (open)
- [#5517](https://github.com/ROCm/aiter/pull/5517) fused routing preamble: new shape and launch-grid scaling (open)
- [#5482](https://github.com/ROCm/aiter/pull/5482) optimize mxfp4 MoE kernels (open)
- [#5507](https://github.com/ROCm/aiter/pull/5507) quantize MoE a1 scale and shuffle on gfx1250 (open)
- [#5531](https://github.com/ROCm/aiter/pull/5531) gfx950 stochastic MXFP4 quantization (open)
- [#5548](https://github.com/ROCm/aiter/pull/5548) 32x32 block-scaled MXFP4 quantization (open)
- [#5538](https://github.com/ROCm/aiter/pull/5538) packed FP4 logical transpose (open)
- [#5549](https://github.com/ROCm/aiter/pull/5549) Silu A16W4 INTERLEAVE fused_moe on gfx950 (open)
- [#5583](https://github.com/ROCm/aiter/pull/5583) MXFP4 weights a16w4 on gfx942 (open)
- [#5632](https://github.com/ROCm/aiter/pull/5632) register-resident biased grouped topk (open)
- [#5588](https://github.com/ROCm/aiter/pull/5588) remove g2l for EP, accept local_expert_hash (open)
- [#5622](https://github.com/ROCm/aiter/pull/5622) bind comm-fused GEMM2 to sorted-inter layout (open)
- [#5542](https://github.com/ROCm/aiter/pull/5542) fused SiLU-and-multiply backward (open)
- [#5571](https://github.com/ROCm/aiter/pull/5571) fmoe runcfg gatemode verify (open)
- [#5532](https://github.com/ROCm/aiter/pull/5532) --fused-expert option for 2-stage MoE tests (open)
- [#5579](https://github.com/ROCm/aiter/pull/5579) gfx950 wideEP MoE test for a8w4 DSV4 and a4w4 Kimi K3 (open)
- [#5493](https://github.com/ROCm/aiter/pull/5493) mori-ep low-latency kernels and cached handle set (open)

</details>

<details>
<summary>Model support & tuning configs (30)</summary>

- [#5350](https://github.com/ROCm/aiter/pull/5350) Qwen3.8-27B MXFP4 tuning (gfx950)
- [#5485](https://github.com/ROCm/aiter/pull/5485) DeepSeek-V4 a8w8 blockscale GEMM tunings (gfx950)
- [#5155](https://github.com/ROCm/aiter/pull/5155) retune Qwen3-VL MXFP4 MoE without stage-2 reduce
- [#5062](https://github.com/ROCm/aiter/pull/5062) CK a8w8 blockscale configs for Gemma-4-31B
- [#5516](https://github.com/ROCm/aiter/pull/5516) gfx942 Gluon GEMM config
- [#5421](https://github.com/ROCm/aiter/pull/5421) GLM-5.3 PTPC qkv a8w8-bpreshuffle rows
- [#5440](https://github.com/ROCm/aiter/pull/5440) DSV4 shared-expert large-M tuning
- [#5144](https://github.com/ROCm/aiter/pull/5144) GLM5.2 per-token FP8 MoE shapes
- [#5468](https://github.com/ROCm/aiter/pull/5468) Kimi-K3 a8w4 fp8 route-out stage2 retune
- [#5602](https://github.com/ROCm/aiter/pull/5602) GLM-5.3 Flash GEMM configs (open)
- [#5585](https://github.com/ROCm/aiter/pull/5585) Qwen3.8-27B TP1 a8w8 blockscale for gfx942 (open)
- [#5557](https://github.com/ROCm/aiter/pull/5557) gfx1151 blockscale tuned JSONs (open)
- [#5610](https://github.com/ROCm/aiter/pull/5610) restore gfx1250 Gluon a16w16 tuned configs (open)
- [#5625](https://github.com/ROCm/aiter/pull/5625) DSv4 a4w4 fused-MoE tuning (open)
- [#5562](https://github.com/ROCm/aiter/pull/5562) DSV4.1 Flash EP4 a8w4 FMoE tuning (open)
- [#5609](https://github.com/ROCm/aiter/pull/5609) DSV4.1 Flash TP4 MoE tuning (open)
- [#5618](https://github.com/ROCm/aiter/pull/5618) DSV4.1 Flash BF16 GEMM tuning (open)
- [#5575](https://github.com/ROCm/aiter/pull/5575) DSPARK a8w8 blockscale bpreshuffle configs (open)
- [#5500](https://github.com/ROCm/aiter/pull/5500) GLM-5.3-Flash a8w8 fused-MoE gfx942 (open)
- [#5599](https://github.com/ROCm/aiter/pull/5599) GLM-5.3 routed MoE row (open)
- [#5514](https://github.com/ROCm/aiter/pull/5514) MXFP4 GLM-5.3 tuning (open)
- [#5523](https://github.com/ROCm/aiter/pull/5523) stop A16W16 pruner from evicting HTI configs (open)
- [#5621](https://github.com/ROCm/aiter/pull/5621) tune gfx950 FP8 MQA prefill dispatch (open)
- [#5598](https://github.com/ROCm/aiter/pull/5598) unified-attention skip-mask for gfx950 hd256 FP8 prefill (open)
- [#5613](https://github.com/ROCm/aiter/pull/5613) tune PA prefill/decode configs for Triton 3.8 regression (open)
- [#5601](https://github.com/ROCm/aiter/pull/5601) gfx1151 gemma4 full-attention prefill tuning (open)
- [#5634](https://github.com/ROCm/aiter/pull/5634) MiniMax-M3 MXFP8 2P1D CI cases (open)
- [#5529](https://github.com/ROCm/aiter/pull/5529) shallow-copy GEMM configs, drop eager log f-strings (open)
- [#5543](https://github.com/ROCm/aiter/pull/5543) token-major layout for GDN prefill h kernel (open)
- [#5510](https://github.com/ROCm/aiter/pull/5510) opt-in segmented affine-scan K5 for long GDN prefills (open)

</details>

<details>
<summary>Parallelism & communication (4)</summary>

- [#5616](https://github.com/ROCm/aiter/pull/5616) gfx1250 ll128 cas2shot (open)
- [#5555](https://github.com/ROCm/aiter/pull/5555) QuickAllReduceInt6 (open)
- [#5604](https://github.com/ROCm/aiter/pull/5604) P2P AR flags with SYSTEM scope and split 1-stage start_sync (open)
- [#5498](https://github.com/ROCm/aiter/pull/5498) adjust quickreduce max block for MI355X (open)

</details>

<details>
<summary>Bugfixes (28)</summary>

- [#4868](https://github.com/ROCm/aiter/pull/4868) guard RDNA unified attention against LDS overflow
- [#5295](https://github.com/ROCm/aiter/pull/5295) skip invalid expert IDs in MoE sorting
- [#5519](https://github.com/ROCm/aiter/pull/5519) select FMoE GEMM2 A addressing by stored buffer size
- [#4916](https://github.com/ROCm/aiter/pull/4916) fix ASM split-K semaphore deadlock under CUDA graph capture
- [#5573](https://github.com/ROCm/aiter/pull/5573) pad MXFP4 A4W4 MoE sort extent to a block_size multiple
- [#5175](https://github.com/ROCm/aiter/pull/5175) Triton 3.8 rmsnorm regression, cap blocked BLOCK_SIZE
- [#5558](https://github.com/ROCm/aiter/pull/5558) MoE routing kernel compile failure
- [#5463](https://github.com/ROCm/aiter/pull/5463) test_mha_v3 mismatched-elements assertion
- [#5528](https://github.com/ROCm/aiter/pull/5528) fix bw formula
- [#5511](https://github.com/ROCm/aiter/pull/5511) EP routing fix
- [#5372](https://github.com/ROCm/aiter/pull/5372) Triton backward autotune dimension keys
- [#5501](https://github.com/ROCm/aiter/pull/5501) gfx1250 Gluon MLA cache launch args
- [#5559](https://github.com/ROCm/aiter/pull/5559) reduce_partial_map over-allocation (open)
- [#5576](https://github.com/ROCm/aiter/pull/5576) missing block_reduce barrier in indexer_qk_rope_quant_and_cache (open)
- [#5614](https://github.com/ROCm/aiter/pull/5614) non-preshuffle MQA paging and large KV offsets (open)
- [#5600](https://github.com/ROCm/aiter/pull/5600) two-step addressing in paged MQA logits kernel (open)
- [#5629](https://github.com/ROCm/aiter/pull/5629) mha_varlen_with_pe miscompile (open)
- [#5561](https://github.com/ROCm/aiter/pull/5561) drain stage-1 LDS-DMA loads before tile barrier (open)
- [#5535](https://github.com/ROCm/aiter/pull/5535) scale FP8 MLA softmax numerators before E4M3 (open)
- [#5627](https://github.com/ROCm/aiter/pull/5627) Triton 3.6 FP8 MQA logits Gluon fix (open)
- [#5630](https://github.com/ROCm/aiter/pull/5630) 64-aligned A16W16 shards in CK dispatch (open)
- [#5480](https://github.com/ROCm/aiter/pull/5480) group quant dispatch for hidden sizes in (4096, 6144] (open)
- [#5505](https://github.com/ROCm/aiter/pull/5505) hardcoded die/CU counts in Triton kernels (open)
- [#5504](https://github.com/ROCm/aiter/pull/5504) hardcoded die/CU counts in FlyDSL kernels (open)
- [#5563](https://github.com/ROCm/aiter/pull/5563) undefine __HIP_NO_HALF_* for gfx942 cold-JIT (open)
- [#5572](https://github.com/ROCm/aiter/pull/5572) Python 3.10 source-inspection failures in MXFP4 JIT imports (open)
- [#5591](https://github.com/ROCm/aiter/pull/5591) repro test for paged-MQA-logits Preshuffle=False OOB (open)
- [#5619](https://github.com/ROCm/aiter/pull/5619) fused KDA decode: order conv_state shifts after tap loads (open)

</details>

<details>
<summary>Refactors & repo reorg (8)</summary>

- [#5567](https://github.com/ROCm/aiter/pull/5567) aiter reorg 7 (open)
- [#5566](https://github.com/ROCm/aiter/pull/5566) aiter reorg 6, moe fusions gdr (open)
- [#5565](https://github.com/ROCm/aiter/pull/5565) aiter reorg 5, attention (open)
- [#5564](https://github.com/ROCm/aiter/pull/5564) aiter reorg 4, gemm topk (open)
- [#5570](https://github.com/ROCm/aiter/pull/5570) aiter reorg 3, infra (open)
- [#5569](https://github.com/ROCm/aiter/pull/5569) aiter reorg 2, fix import (open)
- [#5545](https://github.com/ROCm/aiter/pull/5545) log with % placeholders instead of f-strings (open)
- [#5481](https://github.com/ROCm/aiter/pull/5481) split mla_reduce launcher instantiation across TUs, 121.6s to 7.7s JIT build (open)

</details>

<details>
<summary>Tests (14)</summary>

- [#5423](https://github.com/ROCm/aiter/pull/5423) route test print() output through the aiter logger
- [#5590](https://github.com/ROCm/aiter/pull/5590) take autotuning search out of unit tests
- [#5422](https://github.com/ROCm/aiter/pull/5422) fail on checkAllclose mismatches instead of only logging
- [#5424](https://github.com/ROCm/aiter/pull/5424) no CSV under pytest, no leaked default device
- [#4925](https://github.com/ROCm/aiter/pull/4925) skip fp4 silu_and_mul_quant on non-gfx950
- [#5509](https://github.com/ROCm/aiter/pull/5509) capture FCLK in SMI data for micros
- [#5478](https://github.com/ROCm/aiter/pull/5478) overflow-guarded per-call int32 varlen strides (open)
- [#5624](https://github.com/ROCm/aiter/pull/5624) strided leading dimensions in GDN L2Norm (open)
- [#5608](https://github.com/ROCm/aiter/pull/5608) Norm/Layernorm benchmark (open)
- [#5574](https://github.com/ROCm/aiter/pull/5574) fused_add_rmsnorm_pad benchmark (open)
- [#5539](https://github.com/ROCm/aiter/pull/5539) enable sparse_mla_fwd on gfx942 (open)
- [#5524](https://github.com/ROCm/aiter/pull/5524) test ci:extended-test dispatch (open)
- [#5593](https://github.com/ROCm/aiter/pull/5593) OPUS paged-attention decode (see Most important PRs)
- [#5635](https://github.com/ROCm/aiter/pull/5635) gfx1250 QH128 prefill: avoid padded CSR tail replay (open)

</details>

<details>
<summary>CI & build (22)</summary>

- [#5522](https://github.com/ROCm/aiter/pull/5522) enable ci:extended-test label dispatch
- [#5527](https://github.com/ROCm/aiter/pull/5527) reuse existing extended-test dispatch path
- [#5597](https://github.com/ROCm/aiter/pull/5597) docs onboarding refresh with source-backed reference checks (open)
- [#5536](https://github.com/ROCm/aiter/pull/5536) nightly Triton suite on MI350/MI300X with retry and auto-triage (open)
- [#5617](https://github.com/ROCm/aiter/pull/5617) stale branch archive (open)
- [#5540](https://github.com/ROCm/aiter/pull/5540) stale pull request and branch cleanup (open)
- [#5560](https://github.com/ROCm/aiter/pull/5560) assign a PR to everyone who committed to it (open)
- [#5513](https://github.com/ROCm/aiter/pull/5513) vLLM lm_eval nightly tests (open)
- [#5596](https://github.com/ROCm/aiter/pull/5596) enable 2P1D vLLM DI tests, container v0.29.0 (open)
- [#5488](https://github.com/ROCm/aiter/pull/5488) auto-update split test FILE_TIMES (open)
- [#5568](https://github.com/ROCm/aiter/pull/5568) collect aiter tests recursively (open)
- [#5544](https://github.com/ROCm/aiter/pull/5544) remove committed scratch files (open)
- [#5620](https://github.com/ROCm/aiter/pull/5620) use PR aiter when installing Flash Attention Triton (open)
- [#5584](https://github.com/ROCm/aiter/pull/5584) bump flydsl to 0.3.3.dev903 (open)
- [#5612](https://github.com/ROCm/aiter/pull/5612) bump triton to 7cb7b059 (open)
- [#5605](https://github.com/ROCm/aiter/pull/5605) prebuild: add nmask/nlse bf16 mha_varlen_fwd variant (open)
- plus 4 more minor CI/Triton-index DO-NOT-MERGE pins: [#5533](https://github.com/ROCm/aiter/pull/5533), [#5534](https://github.com/ROCm/aiter/pull/5534), [#5615](https://github.com/ROCm/aiter/pull/5615), [#5524](https://github.com/ROCm/aiter/pull/5524)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 185ef7a245208477a02a36f8734b4ef59cacfc1b71bc0c2a95478ead8e701f1e -->
