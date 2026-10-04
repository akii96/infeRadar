# AITER: PR digest (2026-09-23 to 2026-09-27)

_63 merged, 78 newly opened - source ROCm/AITER, generated 2026-09-27T23:44:28Z_

## TL;DR
- **DeepSeek (V3/R1/V4.1) got the most attention**, followed by GLM, Kimi, MiniMax and Qwen. Merged work includes a tuned group32 A8W8 Triton GEMM ([#5750](https://github.com/ROCm/aiter/pull/5750)), the DSv4.1-flash mHC fused kernel ([#5824](https://github.com/ROCm/aiter/pull/5824)), and DSV4.1 TP2 A4W4 MoE tuning ([#5852](https://github.com/ROCm/aiter/pull/5852)). A FlyDSL DeepSeek-V4 fp8 MLA decode ([#5882](https://github.com/ROCm/aiter/pull/5882)) is newly opened.
- **GEMM and quantization dominate.** Merged: mixed MXFP6/MXFP4 GEMMs ([#5587](https://github.com/ROCm/aiter/pull/5587)), unified afp8wfp8 Triton/Gluon GEMMs ([#5862](https://github.com/ROCm/aiter/pull/5862)), 32x32 block-scaled MXFP4 quant ([#5548](https://github.com/ROCm/aiter/pull/5548)), and gfx1250 F8GEMM split-K ([#5699](https://github.com/ROCm/aiter/pull/5699)).
- **Attention and MLA are the second theme.** Merged: a Gluon paged-MXFP4 kernel with sparsity ([#5834](https://github.com/ROCm/aiter/pull/5834)), a Gluon unified attention kernel for gfx950 ([#4614](https://github.com/ROCm/aiter/pull/4614)), and fused KDA decode ([#4584](https://github.com/ROCm/aiter/pull/4584)). Several MLA decode and sparse-prefill variants for gfx1250 and gfx950 are open.
- **MoE is moving to FlyDSL and Gluon:** A16W4 Gluon MoE ([#5355](https://github.com/ROCm/aiter/pull/5355)), FP8/FP4 quant in the mega stage2 combine ([#5176](https://github.com/ROCm/aiter/pull/5176)), and MXFP4 MoE tuning. In flight: MiniMax M3 MXFP8/MXFP4 and MiMo EP8/16 work.
- **Direction:** gfx950 and gfx1250 bring-up for new models (Kimi-K3, MiniMax-M3, Qwen3.8, GLM-5.x), with many tuned configs. Open PRs also centralize tuning infrastructure and harden custom all-reduce.

## Most important PRs
**[#5750](https://github.com/ROCm/aiter/pull/5750): Tuned native group32 A8W8 Triton GEMM for gfx950**
Adds a native group-32 scaled A8W8 GEMM with extensive per-shape tuning, aimed at DeepSeek-style block-scaled FP8 linears. This is the largest functional addition this window.

**[#5587](https://github.com/ROCm/aiter/pull/5587): Mixed MXFP6/MXFP4 GEMMs**
Adds ASM/HIP GEMMs for mixed MXFP6 and MXFP4 operands on gfx950, plus build, CI and tuning plumbing. It opens up sub-8-bit mixed-precision paths.

**[#5834](https://github.com/ROCm/aiter/pull/5834): Paged MXFP4 Gluon attention with sparsity**
Adds a paged MXFP4 Gluon attention kernel with sparsity support, plus companion cache, norm and quant kernels for vLLM integration. It targets MXFP4 KV and attention on gfx950.

**[#5176](https://github.com/ROCm/aiter/pull/5176): FP8/FP4 quantization in the mega MoE stage2 combine**
Fuses output quantization into the FlyDSL mega-MoE stage2 combine, and [#5814](https://github.com/ROCm/aiter/pull/5814) optimizes stage1 in the same path. This cuts memory traffic between MoE stages.

**[#4614](https://github.com/ROCm/aiter/pull/4614): Unified Attention Gluon kernel for gfx950**
A new Gluon unified-attention kernel for gfx950 with tuning configs, alongside the fused Gluon KDA decode in [#4584](https://github.com/ROCm/aiter/pull/4584).

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#5724](https://github.com/ROCm/aiter/pull/5724) size MLA metadata LDS scratch to the chunk rather than batch count
- [#5807](https://github.com/ROCm/aiter/pull/5807) specialize partial tiles in two-stage custom all-reduce
- [#5443](https://github.com/ROCm/aiter/pull/5443) tune non-temporal load hint per tuned row in fused_moe
- [#5749](https://github.com/ROCm/aiter/pull/5749) page size 8 for paged MQA logits on both layouts, plus large-KV-offset fix
- [#5768](https://github.com/ROCm/aiter/pull/5768) page size 8 in the preshuffle MQA logits kernel
- [#5482](https://github.com/ROCm/aiter/pull/5482) optimize FlyDSL MXFP4 MoE kernels (Kimi/MiniMax)

</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#5862](https://github.com/ROCm/aiter/pull/5862) unify afp8wfp8 GEMM kernels across gfx942/950/1250
- [#5370](https://github.com/ROCm/aiter/pull/5370) Conv3d for Qwen-Image/Wan2.1 VAE on MI35X via FlyDSL
- [#5754](https://github.com/ROCm/aiter/pull/5754) FlashKDA in-kernel paged state_cache I/O
- [#5195](https://github.com/ROCm/aiter/pull/5195) swap gfx950 ASM MLA v4 nm decode kernel
- [#5796](https://github.com/ROCm/aiter/pull/5796) AOT-compile gfx950 FP8 flash-attention forward
- [#5833](https://github.com/ROCm/aiter/pull/5833) sparse MLA improvements and hardened invalid-index handling
- [#5797](https://github.com/ROCm/aiter/pull/5797) prefill launch config for sparse MLA on gfx950
- [#5695](https://github.com/ROCm/aiter/pull/5695) MLA PS-mode ASM/opus kernels for nhead 12 and 8
- [#5403](https://github.com/ROCm/aiter/pull/5403) bf16 hd=256 forward FMHA ASM kernel for gfx950
- [#5376](https://github.com/ROCm/aiter/pull/5376) bf16 hd=256 fused dKdV+dQ backward ASM kernels for gfx950
- [#5824](https://github.com/ROCm/aiter/pull/5824) mHC fused kernel for DSv4.1-flash
- [#5689](https://github.com/ROCm/aiter/pull/5689) standalone relu2 activation for non-gated MoE
- [#5538](https://github.com/ROCm/aiter/pull/5538) packed FP4 logical transpose

</details>

<details>
<summary>MoE & quantization (12)</summary>

- [#5355](https://github.com/ROCm/aiter/pull/5355) Gluon MoE A16W4 for gfx950
- [#5814](https://github.com/ROCm/aiter/pull/5814) optimize mega stage1 perf
- [#5658](https://github.com/ROCm/aiter/pull/5658) merge MoE MXFP8 GEMM into the _moe_gemm_a8w8 kernel
- [#5548](https://github.com/ROCm/aiter/pull/5548) 32x32 block-scaled MXFP4 quantization
- [#5731](https://github.com/ROCm/aiter/pull/5731) gfx1250 natural FP4 compressor scatter
- [#4991](https://github.com/ROCm/aiter/pull/4991) optimize inverse rope group quant on gfx1250
- [#5480](https://github.com/ROCm/aiter/pull/5480) fix group quant dispatch for hidden sizes in (4096, 6144]
- [#5748](https://github.com/ROCm/aiter/pull/5748) optimize Opus integration flow
- [#5740](https://github.com/ROCm/aiter/pull/5740) Gluon MoE compatible with upstream Triton compiler
- [#5672](https://github.com/ROCm/aiter/pull/5672) drop GRID_MN from batched MXFP4 GEMM specialization keys
- [#5470](https://github.com/ROCm/aiter/pull/5470) enable unshuffled MXFP4 GEMM on gfx1151
- [#5734](https://github.com/ROCm/aiter/pull/5734) remove incorrect topk adjustment for EP in get_2stage_cfgs

</details>

<details>
<summary>Model support & tuned configs (13)</summary>

- [#5758](https://github.com/ROCm/aiter/pull/5758) MiniMax-M3-MXFP4 BF16 GEMM configs
- [#5835](https://github.com/ROCm/aiter/pull/5835) Qwen3.8-2.4T-A95B bf16 GEMM configs
- [#5852](https://github.com/ROCm/aiter/pull/5852) tune DSV4.1 TP2 A4W4 fused MoE
- [#5735](https://github.com/ROCm/aiter/pull/5735) GLM-5.3 fused shared MoE rows
- [#5641](https://github.com/ROCm/aiter/pull/5641) retune DSR1/V3 FP8 fmoe rows
- [#5780](https://github.com/ROCm/aiter/pull/5780) revert 13 regressed Kimi-K3 A8W8 rows
- [#5557](https://github.com/ROCm/aiter/pull/5557) gfx1151 blockscale tuned JSONs
- [#5601](https://github.com/ROCm/aiter/pull/5601) gfx1151 gemma4 attention prefill tuning
- [#5828](https://github.com/ROCm/aiter/pull/5828) gfx1250 gluon a16w16 config for MLA q_b_proj
- [#5876](https://github.com/ROCm/aiter/pull/5876) tune shapes for gfx1250
- [#5726](https://github.com/ROCm/aiter/pull/5726) fix grouped topk tie handling for GLM-5.2 accuracy
- [#5854](https://github.com/ROCm/aiter/pull/5854) rename Triton/Gluon tuning files
- [#5647](https://github.com/ROCm/aiter/pull/5647) drop stale use_aot flag from bench_gemm_afp4wfp4

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#5699](https://github.com/ROCm/aiter/pull/5699) gfx1250 F8GEMM 256x256 split-K and 128x128 AP0/AP1 kernels

</details>

<details>
<summary>Parallelism & scheduling (2)</summary>

- [#5694](https://github.com/ROCm/aiter/pull/5694) uniform trip count for custom_all_reduce block barriers
- [#5813](https://github.com/ROCm/aiter/pull/5813) fix custom_all_reduce CI hang

</details>

<details>
<summary>Bugfixes (4)</summary>

- [#5648](https://github.com/ROCm/aiter/pull/5648) mask the >2GB global_load path in mla_gluon decode (gfx950 IMA)
- [#5759](https://github.com/ROCm/aiter/pull/5759) size PS prefill partial buffers from the real token budget
- [#5746](https://github.com/ROCm/aiter/pull/5746) refresh gfx1250 QH128 sparse prefill and fix softmax mlog order
- [#5838](https://github.com/ROCm/aiter/pull/5838) fix mega ubench

</details>

<details>
<summary>CI & build (7)</summary>

- [#5666](https://github.com/ROCm/aiter/pull/5666) self-hosted GLM PR reviewer
- [#5837](https://github.com/ROCm/aiter/pull/5837) fix comm kernel UT hang in CI
- [#5685](https://github.com/ROCm/aiter/pull/5685) add PRs to the Triton kernels board without labels
- [#5853](https://github.com/ROCm/aiter/pull/5853) one-backend-per-PR docs update
- [#5856](https://github.com/ROCm/aiter/pull/5856) copilot instructions update
- [#5785](https://github.com/ROCm/aiter/pull/5785) review-pr agent-timeout fix
- plus 0 further minor items

</details>

<details>
<summary>Open PRs: new kernels & features (in progress) (21)</summary>

- [#5882](https://github.com/ROCm/aiter/pull/5882) DeepSeek-V4 fp8 MLA decode in a single FlyDSL launch on gfx950
- [#5798](https://github.com/ROCm/aiter/pull/5798) MHA v4: bf16 sparse, LSE, KV varlen
- [#5815](https://github.com/ROCm/aiter/pull/5815) FlyDSL fused intranode all-to-all for Ulysses sequence-parallel attention
- [#5868](https://github.com/ROCm/aiter/pull/5868) unified_attention 2D optional block skipping (BLASST)
- [#5866](https://github.com/ROCm/aiter/pull/5866) prefill KDA for gfx1250
- [#5887](https://github.com/ROCm/aiter/pull/5887) PA decode tile with Qlen8 and SWA with sink
- [#5809](https://github.com/ROCm/aiter/pull/5809) refactor PA decode and load CSV tuning results
- [#5881](https://github.com/ROCm/aiter/pull/5881) fuse GDN gated RMSNorm into out_proj GEMM for decode
- [#5844](https://github.com/ROCm/aiter/pull/5844) nhead=96 and round-robin DCP for MLA PS1 FP8 decode on gfx1250
- [#5808](https://github.com/ROCm/aiter/pull/5808) gfx1250 MLA qh32 decode ams v2
- [#5811](https://github.com/ROCm/aiter/pull/5811) gfx1250 MLA qh32 decode ams v3
- [#5805](https://github.com/ROCm/aiter/pull/5805) speed up gfx1250 32mx1 MLA sparse-prefill
- [#5776](https://github.com/ROCm/aiter/pull/5776) faster cross-split merge for MLA v4 nm
- [#5890](https://github.com/ROCm/aiter/pull/5890) cost-model num_kv_splits pick for MLA v4 nm
- [#5778](https://github.com/ROCm/aiter/pull/5778) Opus mx32 plain GEMM
- [#5818](https://github.com/ROCm/aiter/pull/5818) fused m32k4 shuffle quant for ASM a8w8 on gfx1250
- [#5817](https://github.com/ROCm/aiter/pull/5817) MiniMax M3 MXFP8 MoE
- [#5788](https://github.com/ROCm/aiter/pull/5788) topk index score for MiniMax M3
- [#5822](https://github.com/ROCm/aiter/pull/5822) opt-in M3 sequence-parallel collectives and tiled MoE sorting
- [#5794](https://github.com/ROCm/aiter/pull/5794) SwiGLU OAI MXFP4 FLAT fmoe kernels for MiniMax M3
- [#5820](https://github.com/ROCm/aiter/pull/5820) Qwen3.8 FlyDSL kernels

</details>

<details>
<summary>Open PRs: MoE tuning, fixes and refactors (24)</summary>

- [#5795](https://github.com/ROCm/aiter/pull/5795) refactor MI308 MoE kernels with compilation caching (1/3)
- [#5891](https://github.com/ROCm/aiter/pull/5891) MiMo MXFP4 EP8/EP16 on gfx950
- [#5851](https://github.com/ROCm/aiter/pull/5851) MiMo TP8 MXFP4 MoE tuning
- [#5812](https://github.com/ROCm/aiter/pull/5812) scatter epilog for layout-v2 GEMM2
- [#5804](https://github.com/ROCm/aiter/pull/5804) kmk3 EP MoE and gemm2 optimization
- [#5802](https://github.com/ROCm/aiter/pull/5802) route a16w4 SiLU MoE to CK-Tile and apply swiglu_limit
- [#5825](https://github.com/ROCm/aiter/pull/5825) gfx942 SiLU A16W4 and DSv4.1 Flash tuning
- [#5821](https://github.com/ROCm/aiter/pull/5821) DSv4 decode MoE tuning for mori-EP
- [#5832](https://github.com/ROCm/aiter/pull/5832) keep the MFMA in FP8 for MXFP8 MoE when MX_SCALE_BLOCK_K == 1
- [#5831](https://github.com/ROCm/aiter/pull/5831) moe_gemm_mxfp8 zero-init output and graph-safe routing
- [#5863](https://github.com/ROCm/aiter/pull/5863) expert-parallel support for moe_gemm_a16w4
- [#5884](https://github.com/ROCm/aiter/pull/5884) respect GPU_ARCHS for Grouped MoE AOT builds
- [#5810](https://github.com/ROCm/aiter/pull/5810) bind mori tokoff-ext allocator on gfx1250 mega_moe
- [#5855](https://github.com/ROCm/aiter/pull/5855) MORI multi-node and MORI_V2
- [#5775](https://github.com/ROCm/aiter/pull/5775) send the real IPC offset in custom_all_reduce
- [#5799](https://github.com/ROCm/aiter/pull/5799) re-take the expandable_segments decision at capture time
- [#5893](https://github.com/ROCm/aiter/pull/5893) fix gfx950 MLA decode reading wrong KV past 4 GiB
- [#5848](https://github.com/ROCm/aiter/pull/5848) fix hardcoded die and CU counts in opus kernels
- [#5873](https://github.com/ROCm/aiter/pull/5873) mask split-K tail in blockscale GEMMs
- [#5886](https://github.com/ROCm/aiter/pull/5886) fix pa_decode compile error with newer Triton
- [#5793](https://github.com/ROCm/aiter/pull/5793) bound K/V loads in the Triton FA decode split-K tail
- [#5790](https://github.com/ROCm/aiter/pull/5790) gfx1201 unified attention tuning for Gemma4 shapes and D=1024 fix
- [#5801](https://github.com/ROCm/aiter/pull/5801) fix gfx1250 TDM grouped GEMM bias index
- [#5860](https://github.com/ROCm/aiter/pull/5860) fix stale comments and harden tests for [#5648](https://github.com/ROCm/aiter/pull/5648)

</details>

<details>
<summary>Open PRs: GEMM tuning and tuning infrastructure (19)</summary>

- [#5872](https://github.com/ROCm/aiter/pull/5872) unify GEMM tuning through config lookup
- [#5871](https://github.com/ROCm/aiter/pull/5871) tune GEMM via config lookup
- [#5874](https://github.com/ROCm/aiter/pull/5874) consolidate tuning harnesses
- [#5846](https://github.com/ROCm/aiter/pull/5846) shared mp_tuner typed statuses and central tuning policy
- [#5849](https://github.com/ROCm/aiter/pull/5849) MHA forward tuner: delta race, resume, finalist rounds
- [#5841](https://github.com/ROCm/aiter/pull/5841) fail a tuner task as soon as its worker exits
- [#5830](https://github.com/ROCm/aiter/pull/5830) gfx950 tuned gemm_a16w16 configs
- [#5867](https://github.com/ROCm/aiter/pull/5867) DSR1 GEMM tuning
- [#5839](https://github.com/ROCm/aiter/pull/5839) gfx942 a8w8 blockscale tunings for Qwen3/3.5/GLM/DSV4
- [#5870](https://github.com/ROCm/aiter/pull/5870) Qwen3.8-Flash-Next FP8 configs
- [#5836](https://github.com/ROCm/aiter/pull/5836) Qwen3.8-27B A4W4 GDN BA projection shapes
- [#5783](https://github.com/ROCm/aiter/pull/5783) Kimi-K3 KDA gate a8w8 bpreshuffle tuning
- [#5875](https://github.com/ROCm/aiter/pull/5875) K3 a16w16 shapes tuning
- [#5850](https://github.com/ROCm/aiter/pull/5850) route GLM-5 qkv_a_proj decode tiers to split-K Triton
- [#5885](https://github.com/ROCm/aiter/pull/5885) optimize the mHC fused kernel
- [#5895](https://github.com/ROCm/aiter/pull/5895) gemm_a16w16_atomic accumulates into an existing buffer
- [#5877](https://github.com/ROCm/aiter/pull/5877) stop fused_bmm_rope_kv_cache using batched a8w8 per-token kernel
- [#5774](https://github.com/ROCm/aiter/pull/5774) rotating-buffer GEMM A16W16 benchmark
- [#5847](https://github.com/ROCm/aiter/pull/5847) blockscale split-K pipeline picked from per-split loop count

</details>

<details>
<summary>Open PRs: Triton/Gluon config and misc (14)</summary>

- [#5857](https://github.com/ROCm/aiter/pull/5857) gmm gfx950 large-K/N config
- [#5859](https://github.com/ROCm/aiter/pull/5859) PA decode config-driven v1/v2 dispatch
- [#5858](https://github.com/ROCm/aiter/pull/5858) MHA fwd gfx950 mid_head config
- [#5782](https://github.com/ROCm/aiter/pull/5782) FP8 MQA logits gfx950 DSA tuning
- [#5800](https://github.com/ROCm/aiter/pull/5800) fix gluon import and tune fused_clamp_act_mul
- [#5786](https://github.com/ROCm/aiter/pull/5786) CK fmha kernel generation follows GPU_ARCHS
- [#5787](https://github.com/ROCm/aiter/pull/5787) CK fmha LLC head grouping on RDNA
- [#5779](https://github.com/ROCm/aiter/pull/5779) remove CK dependency from plain top-k
- [#5878](https://github.com/ROCm/aiter/pull/5878) select impacted Triton/Gluon unit tests
- [#5880](https://github.com/ROCm/aiter/pull/5880) Triton board status driven by workflow
- [#5883](https://github.com/ROCm/aiter/pull/5883) CI timeout fix
- [#5784](https://github.com/ROCm/aiter/pull/5784) DeepSeek-V4-Pro 2P1D TP8 ATOM DI smoke cases
- [#5803](https://github.com/ROCm/aiter/pull/5803) review-pr 40min agent timeout and transient-only retry
- [#5864](https://github.com/ROCm/aiter/pull/5864) preserve install failure status after retries

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: ae88c4cd41b661339e3e0a897ec530fd63618018a3b3154bed2f439a1de6b116 -->
