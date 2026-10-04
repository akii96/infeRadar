# sglang: PR digest (2026-09-23 to 2026-09-27)

_286 merged, 398 newly opened - source sgl-project/sglang, generated 2026-09-28T00:11:48Z_

## TL;DR
- **DeepSeek V4.1 got the most attention (61 labels)**, with merged work on the DeepSelect JIT kernel ([#40556](https://github.com/sgl-project/sglang/pull/40556)), low-ratio index top-k relocation ([#41125](https://github.com/sgl-project/sglang/pull/41125), [#41291](https://github.com/sgl-project/sglang/pull/41291)), and a stack of AMD gfx950 kernels ([#41019](https://github.com/sgl-project/sglang/pull/41019), [#41018](https://github.com/sgl-project/sglang/pull/41018), [#35619](https://github.com/sgl-project/sglang/pull/35619)). A large AMD serving PR ([#41308](https://github.com/sgl-project/sglang/pull/41308)), a virtual-PP scheduler ([#41212](https://github.com/sgl-project/sglang/pull/41212)) and Hopper perf work ([#41251](https://github.com/sgl-project/sglang/pull/41251), [#40945](https://github.com/sgl-project/sglang/pull/40945)) are still open.
- **Qwen 3.8 Next, MiniMax-M3 and GLM-5.3** drew the most perf work. For Qwen that means many small fusions (PLE gate/conv, CUDA-graph buffer copies, speculative state commits). For MiniMax-M3 it means the AITER Gluon sparse prefill path and a wave64 histogram top-k for decode. GLM-5.3 got the Cute-DSL AR fusion refactor.
- **Layer communicator rework:** a large series ([#41439](https://github.com/sgl-project/sglang/pull/41439) through [#41443](https://github.com/sgl-project/sglang/pull/41443)) moves every layer's boundaries onto declared steps and removes `ScatterMode`. A string of related fixes corrects double-counted or deferred FFN all-reduces.
- **Direction:** consolidating internals (communicator, mem_cache, unified radix cache, test pruning), plus PD, HiCache and kv-sharding, RL weight-update sessions, and diffusion model support.

## Most important PRs
**[#40556](https://github.com/sgl-project/sglang/pull/40556): DeepSeek V4.1 DeepSelect JIT kernel**
Adds a JIT top-k and selection kernel for the V4.1 sparse indexer, with tests and docs. It is the foundation for the V4.1 index path, and the follow-ups [#41125](https://github.com/sgl-project/sglang/pull/41125) and [#41291](https://github.com/sgl-project/sglang/pull/41291) build on it.

**[#39816](https://github.com/sgl-project/sglang/pull/39816): Cute-DSL all-reduce fusion for DeepseekV2-arch models**
Refactors the fused AR + norm path so it also covers GLM-5.3 and other DeepseekV2-derived models. This widens where the fused communication kernel applies.

**[#41439](https://github.com/sgl-project/sglang/pull/41439): Split the layer communicator into a package**
A move-only split that sets up the follow-on refactors. These choose layer boundaries from declarations, defer the FFN all-reduce as `UnreducedOutput`, and remove `ScatterMode` ([#41443](https://github.com/sgl-project/sglang/pull/41443)).

**[#36546](https://github.com/sgl-project/sglang/pull/36546): MiniMax-M3 sparse prefill via AITER Gluon paged attention**
Runs the sparse prefill main attention on AMD through the AITER Gluon paged kernel. It is the main AMD attention-speed change for MiniMax-M3.

**[#36559](https://github.com/sgl-project/sglang/pull/36559): MoE small-batch sorting path with fused MXFP8 quantization**
Adds a Triton small-batch token-sorting path that fuses MXFP8 quantization, cutting launch overhead for decode-sized MoE batches.

## More changes by area

<details>
<summary>Performance (8)</summary>

- [#41305](https://github.com/sgl-project/sglang/pull/41305) speeds up the SANA-Video residual gate add on H200
- [#38978](https://github.com/sgl-project/sglang/pull/38978) reduces decode bootstrap latency with request-owned speculative KV
- [#41061](https://github.com/sgl-project/sglang/pull/41061) lazy-loads built-in model definitions and nixl_ep at startup
- [#34695](https://github.com/sgl-project/sglang/pull/34695) speeds up Wan2.2 DiT FP8 attention per-tensor quantization on AMD
- [#36505](https://github.com/sgl-project/sglang/pull/36505) adds a page-level KV view for gfx950 fp8 page-64 asm prefill
- [#41097](https://github.com/sgl-project/sglang/pull/41097) shares the MoE output all-reduce between models
- [#41196](https://github.com/sgl-project/sglang/pull/41196) carries a deferred FFN all-reduce as UnreducedOutput
- [#40868](https://github.com/sgl-project/sglang/pull/40868) stops deferring the last layer's FFN all-reduce in five models

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#41344](https://github.com/sgl-project/sglang/pull/41344) introduces FA4 into the ViT for SM100/SM103
- [#32269](https://github.com/sgl-project/sglang/pull/32269) adds the XQA backend for spec-decode verify
- [#40854](https://github.com/sgl-project/sglang/pull/40854) chunks the kpool indexer MQA logits by query rows under a memory budget
- [#39059](https://github.com/sgl-project/sglang/pull/39059) tunes Triton sparse MLA on gfx950 and makes split-K workspaces graph-safe
- [#38340](https://github.com/sgl-project/sglang/pull/38340) fuses the MLA q absorb into the RoPE + KV-write kernel on gfx950
- [#40710](https://github.com/sgl-project/sglang/pull/40710) enables the AITER fused FP8 indexer writer for DSA
- [#38876](https://github.com/sgl-project/sglang/pull/38876) adds a Triton packed sparse decode path for QSA on ROCm
- [#39726](https://github.com/sgl-project/sglang/pull/39726) adds the page-unified HiCache KV load-back JIT kernel
- [#40767](https://github.com/sgl-project/sglang/pull/40767) adds an occupancy-preserving L1 carveout preference for JIT kernels
- [#36560](https://github.com/sgl-project/sglang/pull/36560) adds a wave64 histogram-select decode top-k for MiniMax-M3
- [#40041](https://github.com/sgl-project/sglang/pull/40041) fuses the Qwen PLE gate and convolution prep for target verify
- [#41166](https://github.com/sgl-project/sglang/pull/41166) fuses small CUDA graph input buffer copies for Qwen 3.8 Next
- [#41309](https://github.com/sgl-project/sglang/pull/41309) runs an all-valid attention mask on the unmasked kernel
- [#41078](https://github.com/sgl-project/sglang/pull/41078) reads a per-replica sequence at the gather slot that produced it
- [#40425](https://github.com/sgl-project/sglang/pull/40425), [#40405](https://github.com/sgl-project/sglang/pull/40405), [#40490](https://github.com/sgl-project/sglang/pull/40490), [#40384](https://github.com/sgl-project/sglang/pull/40384), [#40386](https://github.com/sgl-project/sglang/pull/40386) and [#40494](https://github.com/sgl-project/sglang/pull/40494) are lossless diffusion fusions (LingBot, Wan VAE, Klein, LongCat, Cosmos3, Joy Image)
- [#35684](https://github.com/sgl-project/sglang/pull/35684) adds MiniMax-H3 Spectrum skip-step and fused RMSNorm/AdaLN

</details>

<details>
<summary>MoE & quantization (12)</summary>

- [#40204](https://github.com/sgl-project/sglang/pull/40204) adds a small-M MXFP4 fused-MoE kernel for gfx950 (Qwen)
- [#36574](https://github.com/sgl-project/sglang/pull/36574) adds MiniMax-M3 MXFP8 dense block convert and aiter MXFP8 MoE on gfx950
- [#35619](https://github.com/sgl-project/sglang/pull/35619) integrates Aiter MegaMoEv2 for DeepSeek-V4
- [#39939](https://github.com/sgl-project/sglang/pull/39939) honors the swiglu_limit clamp in the flashinfer_cutlass runner
- [#38726](https://github.com/sgl-project/sglang/pull/38726) dispatches block-FP8 MoE experts for ModelOpt mixed precision
- [#41377](https://github.com/sgl-project/sglang/pull/41377) honors an explicit triton moe_runner_backend for mxfp8 on ROCm
- [#40996](https://github.com/sgl-project/sglang/pull/40996) adds a tuned dsv4 shape on AMD
- [#41018](https://github.com/sgl-project/sglang/pull/41018) adds gfx950 MXFP8 matmul kernels and fp8-grid producers for dsv4.1
- [#39064](https://github.com/sgl-project/sglang/pull/39064) keeps quantization for mixed Quark Qwen3.5 MTP checkpoints
- [#40754](https://github.com/sgl-project/sglang/pull/40754) restores dropped fused shared-expert weights for Qwen3.8 FP8 on AMD
- [#41074](https://github.com/sgl-project/sglang/pull/41074) loads fused shared-expert LoRA weights and bounds expert indices
- [#41201](https://github.com/sgl-project/sglang/pull/41201) lets a model package supply its DeepEP v2 per-rank prefill dispatch bound

</details>

<details>
<summary>Model support (13)</summary>

- [#34061](https://github.com/sgl-project/sglang/pull/34061) adds DiffusionGemma dLLM serving
- [#41067](https://github.com/sgl-project/sglang/pull/41067) adds native Ming-Image Design and Design-Layer support
- [#41011](https://github.com/sgl-project/sglang/pull/41011) adds native Anima Base v1.0 support
- [#35990](https://github.com/sgl-project/sglang/pull/35990) adds MiniMax-H3 to ComfyUI integrated mode
- [#40568](https://github.com/sgl-project/sglang/pull/40568) adds MiniMax-H3 PDD inference
- [#37213](https://github.com/sgl-project/sglang/pull/37213) enables Qwen3.8-flash-next on XPU
- [#41019](https://github.com/sgl-project/sglang/pull/41019) adds dsv4.1-amd KV cache layouts, FP4 indexer, compressor and router kernels
- [#41120](https://github.com/sgl-project/sglang/pull/41120) adds a .co for the deepseek v4 fp8 decode kernel and a group decode optimization
- [#41049](https://github.com/sgl-project/sglang/pull/41049) sizes DSv4 compressed pools from one per-ratio table
- [#41048](https://github.com/sgl-project/sglang/pull/41048) budgets the DSv4 ratio-2 pair state pool
- [#40468](https://github.com/sgl-project/sglang/pull/40468) keeps the Inkling automatic tool grammar active across the response
- [#41046](https://github.com/sgl-project/sglang/pull/41046) enables Qwen3.8 Flash Next NVFP4 on B200/B300/GB300
- [#41024](https://github.com/sgl-project/sglang/pull/41024) and [#41458](https://github.com/sgl-project/sglang/pull/41458) are DeepSeek-V4 AMD docs and cookbook updates

</details>

<details>
<summary>Parallelism & scheduling (16)</summary>

- [#37442](https://github.com/sgl-project/sglang/pull/37442) adds 8-node AllReduce/AllGather and MNVLS to MSCCL++
- [#33723](https://github.com/sgl-project/sglang/pull/33723) recaptures decode CUDA graphs after elastic-EP scale-up
- [#36389](https://github.com/sgl-project/sglang/pull/36389) supports DP attention in LoRA backends
- [#38652](https://github.com/sgl-project/sglang/pull/38652) adds the LMCache unified radix cache
- [#39478](https://github.com/sgl-project/sglang/pull/39478) supports unified memory decode host pools
- [#40238](https://github.com/sgl-project/sglang/pull/40238) adds decode host receive for custom PD transfer backends
- [#39964](https://github.com/sgl-project/sglang/pull/39964) enables kv-shard Control Plane B
- [#40118](https://github.com/sgl-project/sglang/pull/40118) preserves speculative decoding during prefill across DP ranks
- [#37462](https://github.com/sgl-project/sglang/pull/37462) adds LiLiCorr, a candidate-lattice reranker for DFlash drafts
- [#31362](https://github.com/sgl-project/sglang/pull/31362) adds NGRAM speculative decoding on XPU
- [#41402](https://github.com/sgl-project/sglang/pull/41402) fans drain abort ACKs out to every decode peer
- [#39731](https://github.com/sgl-project/sglang/pull/39731) uses logical token capacity for DCP PD admission
- [#40779](https://github.com/sgl-project/sglang/pull/40779) stops pause_generation and weight updates from deadlocking
- [#40777](https://github.com/sgl-project/sglang/pull/40777) adds RL weight-update sessions and spec draft runner updates
- [#41276](https://github.com/sgl-project/sglang/pull/41276) and [#40988](https://github.com/sgl-project/sglang/pull/40988) unify mem_cache eviction cursors and lock receipts, and drop `is_insert`
- [#40798](https://github.com/sgl-project/sglang/pull/40798) frees rows below the SWA evict floor on all-SWA release

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#40524](https://github.com/sgl-project/sglang/pull/40524) updates CANN to 9.1.0 on NPU
- [#28417](https://github.com/sgl-project/sglang/pull/28417) enables piecewise CUDA graph on NPU
- [#40895](https://github.com/sgl-project/sglang/pull/40895) reverts [#28417](https://github.com/sgl-project/sglang/pull/28417)
- [#40445](https://github.com/sgl-project/sglang/pull/40445) fuses FIA KV-cache writes on NPU
- [#41132](https://github.com/sgl-project/sglang/pull/41132) reverts [#40445](https://github.com/sgl-project/sglang/pull/40445)

</details>

<details>
<summary>API & serving (10)</summary>

- [#41208](https://github.com/sgl-project/sglang/pull/41208) adds a System One compatible /v1/systemone route
- [#38965](https://github.com/sgl-project/sglang/pull/38965) adds setwise scoring to the Score API
- [#41188](https://github.com/sgl-project/sglang/pull/41188) adds CausalLM setwise scoring (batched + --enable-mis)
- [#40826](https://github.com/sgl-project/sglang/pull/40826) adds per-item candidate token scoring and calibration
- [#40932](https://github.com/sgl-project/sglang/pull/40932) and [#41047](https://github.com/sgl-project/sglang/pull/41047) add selected/support sampling logprob modes (the second a cherry-pick)
- [#40986](https://github.com/sgl-project/sglang/pull/40986) and [#41270](https://github.com/sgl-project/sglang/pull/41270) stream sampling masks as per-request arrays (the second a cherry-pick)
- [#41095](https://github.com/sgl-project/sglang/pull/41095) adds opt-in SRT prompt enhancement to diffusion APIs
- [#40766](https://github.com/sgl-project/sglang/pull/40766), [#41221](https://github.com/sgl-project/sglang/pull/41221) and [#41185](https://github.com/sgl-project/sglang/pull/41185) are sgl-router routing, render-default and input_ids tracking updates
- [#41246](https://github.com/sgl-project/sglang/pull/41246) decodes input_ids without untagged buffering in the Rust frontend

</details>

<details>
<summary>Bugfixes (22)</summary>

- [#41423](https://github.com/sgl-project/sglang/pull/41423) gathers a dense FFN input across attention DP and CP in one DP sum
- [#41422](https://github.com/sgl-project/sglang/pull/41422) keeps one copy of CP-replicated rows in the DP gather
- [#41436](https://github.com/sgl-project/sglang/pull/41436) fixes LongCat-Flash under attention DP
- [#41195](https://github.com/sgl-project/sglang/pull/41195) stops counting a deferred FFN sum more than once
- [#41079](https://github.com/sgl-project/sglang/pull/41079) completes the deferred all-reduce before a PP send
- [#41080](https://github.com/sgl-project/sglang/pull/41080) completes the deferred all-reduce before deepstack and aux hidden-state capture
- [#41193](https://github.com/sgl-project/sglang/pull/41193) completes the all-reduce when the flashinfer fused norm declines a batch
- [#41062](https://github.com/sgl-project/sglang/pull/41062) keeps the target's DP sync slot in draft scopes
- [#41179](https://github.com/sgl-project/sglang/pull/41179) fixes mixed chunk prefill with DP speculative coordination
- [#41194](https://github.com/sgl-project/sglang/pull/41194) plans NextN/MTP draft layers as one-layer models
- [#40983](https://github.com/sgl-project/sglang/pull/40983) derives per-runner hybrid SWA layer ids without mutating ModelConfig
- [#41083](https://github.com/sgl-project/sglang/pull/41083) broadcasts requests along attention CP before attention TP
- [#41082](https://github.com/sgl-project/sglang/pull/41082), [#40799](https://github.com/sgl-project/sglang/pull/40799), [#41433](https://github.com/sgl-project/sglang/pull/41433), [#40800](https://github.com/sgl-project/sglang/pull/40800) and [#40801](https://github.com/sgl-project/sglang/pull/40801) fix duplicate sums and aux capture in Step-3.5, LongCat, Falcon-H1 and Nemotron
- [#41328](https://github.com/sgl-project/sglang/pull/41328) fixes LMCache component cursors and per-cache backend selection
- [#41138](https://github.com/sgl-project/sglang/pull/41138) skips the DCP target-verify MLA kernel during FlashInfer autotune
- [#41261](https://github.com/sgl-project/sglang/pull/41261) caches resumed decode-radix requests from root
- [#40621](https://github.com/sgl-project/sglang/pull/40621) fixes multimodal feature offload races
- [#40989](https://github.com/sgl-project/sglang/pull/40989) recovers from stale torch extension locks
- [#34417](https://github.com/sgl-project/sglang/pull/34417) fixes the grouped forward_batch AttributeError by installing the residency manager
- [#40760](https://github.com/sgl-project/sglang/pull/40760) partitions selective CI reruns into matrix jobs
- [#41271](https://github.com/sgl-project/sglang/pull/41271) keeps the sampling mask of a replayed rebootstrap token
- [#37284](https://github.com/sgl-project/sglang/pull/37284) releases the weight-checker snapshot after compare

</details>

<details>
<summary>Refactors (33)</summary>

- [#41243](https://github.com/sgl-project/sglang/pull/41243) restores logical kernel groups and test organization
- [#41425](https://github.com/sgl-project/sglang/pull/41425), [#41438](https://github.com/sgl-project/sglang/pull/41438), [#41440](https://github.com/sgl-project/sglang/pull/41440), [#41441](https://github.com/sgl-project/sglang/pull/41441), [#41429](https://github.com/sgl-project/sglang/pull/41429), [#41420](https://github.com/sgl-project/sglang/pull/41420), [#41424](https://github.com/sgl-project/sglang/pull/41424), [#41417](https://github.com/sgl-project/sglang/pull/41417), [#41419](https://github.com/sgl-project/sglang/pull/41419), [#41421](https://github.com/sgl-project/sglang/pull/41421), [#41426](https://github.com/sgl-project/sglang/pull/41426), [#41435](https://github.com/sgl-project/sglang/pull/41435), [#41431](https://github.com/sgl-project/sglang/pull/41431), [#41442](https://github.com/sgl-project/sglang/pull/41442), [#41418](https://github.com/sgl-project/sglang/pull/41418) and [#41428](https://github.com/sgl-project/sglang/pull/41428) move layer steps and boundaries onto declarations
- [#41252](https://github.com/sgl-project/sglang/pull/41252), [#41257](https://github.com/sgl-project/sglang/pull/41257), [#41255](https://github.com/sgl-project/sglang/pull/41255), [#41254](https://github.com/sgl-project/sglang/pull/41254), [#41253](https://github.com/sgl-project/sglang/pull/41253), [#41191](https://github.com/sgl-project/sglang/pull/41191), [#41084](https://github.com/sgl-project/sglang/pull/41084), [#41081](https://github.com/sgl-project/sglang/pull/41081) and [#41443](https://github.com/sgl-project/sglang/pull/41443) refactor the layer communicator (prepare_attn/mlp, ffn_exit, LayerFacts)
- [#41198](https://github.com/sgl-project/sglang/pull/41198), [#40871](https://github.com/sgl-project/sglang/pull/40871), [#40870](https://github.com/sgl-project/sglang/pull/40870), [#41430](https://github.com/sgl-project/sglang/pull/41430) and [#40867](https://github.com/sgl-project/sglang/pull/40867) move models onto ffn_exit and the standard communicator
- [#41199](https://github.com/sgl-project/sglang/pull/41199), [#41200](https://github.com/sgl-project/sglang/pull/41200), [#41197](https://github.com/sgl-project/sglang/pull/41197) and [#41427](https://github.com/sgl-project/sglang/pull/41427) refine last-layer, FFN-exit and reduction declarations
- [#40869](https://github.com/sgl-project/sglang/pull/40869) compares token layouts instead of group sizes
- [#40638](https://github.com/sgl-project/sglang/pull/40638) reads parallel placement in consumers
- [#40922](https://github.com/sgl-project/sglang/pull/40922) retires the Kimi K3 kernel namespace
- [#40612](https://github.com/sgl-project/sglang/pull/40612) migrates diffusion config registration to each model's config file
- [#40971](https://github.com/sgl-project/sglang/pull/40971) trims server configuration comments
- [#40795](https://github.com/sgl-project/sglang/pull/40795) removes deprecated endpoints, env vars and aliases
- [#41284](https://github.com/sgl-project/sglang/pull/41284) switches to all_gather_single / reduce_scatter_single
- [#40807](https://github.com/sgl-project/sglang/pull/40807) and [#40963](https://github.com/sgl-project/sglang/pull/40963) remove unreachable and unused mem_cache code
- [#41281](https://github.com/sgl-project/sglang/pull/41281) replaces `cache_finished_req` with `insert_req`

</details>

<details>
<summary>Tests (10)</summary>

- [#41215](https://github.com/sgl-project/sglang/pull/41215), [#41297](https://github.com/sgl-project/sglang/pull/41297), [#41286](https://github.com/sgl-project/sglang/pull/41286), [#40924](https://github.com/sgl-project/sglang/pull/40924) and [#40976](https://github.com/sgl-project/sglang/pull/40976) remove dead or implementation-mirroring tests
- [#41280](https://github.com/sgl-project/sglang/pull/41280) and [#41216](https://github.com/sgl-project/sglang/pull/41216) route benchmarks through sgl-eval
- [#41321](https://github.com/sgl-project/sglang/pull/41321) merges the Kimi-Linear PD DCP4 nightly tests
- [#41285](https://github.com/sgl-project/sglang/pull/41285) hardens /rerun-test dispatch
- [#39781](https://github.com/sgl-project/sglang/pull/39781) adds a DeepSeek-V2-Lite FP8 XPU nightly

</details>

<details>
<summary>Other (14)</summary>

- [#40477](https://github.com/sgl-project/sglang/pull/40477) ports chat_parsing core
- [#41125](https://github.com/sgl-project/sglang/pull/41125) moves the low-ratio index top-k into dsv4/low_ratio_indexer
- [#41291](https://github.com/sgl-project/sglang/pull/41291) moves the ratio-1/2 index top-k ops into kernels/ops/attention/dsv4
- [#40242](https://github.com/sgl-project/sglang/pull/40242) resolves HF LoRA targets through model-aware normalization
- [#39379](https://github.com/sgl-project/sglang/pull/39379) sizes dense LoRA buffers from the real shard
- [#40599](https://github.com/sgl-project/sglang/pull/40599), [#36192](https://github.com/sgl-project/sglang/pull/36192), [#34416](https://github.com/sgl-project/sglang/pull/34416) and [#34418](https://github.com/sgl-project/sglang/pull/34418) are diffusion offload, LoRA merge and latent handling updates
- [#40786](https://github.com/sgl-project/sglang/pull/40786), [#37704](https://github.com/sgl-project/sglang/pull/37704), [#40821](https://github.com/sgl-project/sglang/pull/40821) and [#38891](https://github.com/sgl-project/sglang/pull/38891) are RL and KV-hint transport work
- [#40802](https://github.com/sgl-project/sglang/pull/40802) adds forward occupancy metrics
- [#39889](https://github.com/sgl-project/sglang/pull/39889) takes bench prompt length from the server
- [#39660](https://github.com/sgl-project/sglang/pull/39660) shares one head-slice helper across PD backends
- [#38778](https://github.com/sgl-project/sglang/pull/38778) dedups replicated MLA/DSA KV in the UMBP linker
- [#40712](https://github.com/sgl-project/sglang/pull/40712) and [#40960](https://github.com/sgl-project/sglang/pull/40960) demote SWA KV on HiCache write_back and batch buffer-only backups
- [#40512](https://github.com/sgl-project/sglang/pull/40512) and [#41248](https://github.com/sgl-project/sglang/pull/41248) are HiCache and unified-memory fixes
- plus 86 more merged PRs not shown

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 51de387d8b2d045f8162fac9c42053dfa7d626c05a3f6a190c882deab129f682 -->
