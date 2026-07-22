# sglang: PR digest (2026-07-08 to 2026-07-12)

_205 merged, 273 newly opened - source sgl-project/sglang, generated 2026-07-12T22:18:28Z_

## TL;DR
- **Model Focus**: DeepSeek (38 PRs) and GLM (12 PRs) dominated model-specific work, with significant attention on DeepSeek-V4 (unified-KV HiCache, FP8 quant, dual-stream MoE) and GLM-5.2 (DSA Cache Layer Split, DSpark verify). MiniMax-M3 and Pi0.5 also saw major merges.
- **Performance & Kernels**: A massive refactor is underway to consolidate scattered Triton, Cutlass, and FlashInfer kernels into a unified `sglang.kernels` namespace (RFC #29630).
- **Speculative Decoding**: Merged support for CPU speculative decoding, while in-progress work targets DSpark compact verify for GLM-5.2 and DeepEP integration.
- **Diffusion & Multimodal**: Heavy investment in diffusion models, merging Pi0.5 support, breakable CUDA graphs (BCG) for DiTs, and GLM Image AR backend, with DreamZero action generation newly opened.
- **Overall Direction**: The engine is heavily optimizing for next-gen architectures (DeepSeek-V4, GLM-5.2) with advanced speculative decoding (DSpark), unified kernel management, and expanding its multimodal/diffusion footprint.

## Most important PRs
- **[#28715](https://github.com/sgl-project/sglang/pull/28715)** Adds comprehensive support for the MiniMax-M3 model. This includes vision-language capabilities, function calling, and FP8 quantization.
- **[#30633](https://github.com/sgl-project/sglang/pull/30633)** Introduces support for the Pi0.5 diffusion model. This expands the engine's multimodal and diffusion capabilities.
- **[#30044](https://github.com/sgl-project/sglang/pull/30044)** Executes Phase 2 of RFC #29630 by migrating scattered `triton_ops` into a centralized `sglang.kernels` namespace. This standardizes kernel management across backends.
- **[#30720](https://github.com/sgl-project/sglang/pull/30720)** (Newly opened) A massive in-progress PR enabling DSpark compact verify functionality for GLM-5.2. This will significantly advance speculative decoding performance for the GLM family.
- **[#27436](https://github.com/sgl-project/sglang/pull/27436)** Enables breakable CUDA graphs (BCG) for diffusion DiTs. This optimizes execution overhead and memory usage for diffusion workloads.

## More changes by area

<details>
<summary>Performance (11)</summary>

- [#27926](https://github.com/sgl-project/sglang/pull/27926) [DSV4] perf: Make FP8 quant output tensor contiguous
- [#30449](https://github.com/sgl-project/sglang/pull/30449) [Cherry-pick to release/v0.5.15] [DSV4] perf: Make FP8 quant output tensor contiguous ([#27926](https://github.com/sgl-project/sglang/pull/27926))
- [#30580](https://github.com/sgl-project/sglang/pull/30580) Lazy load TileLang MHC kernels
- [#30878](https://github.com/sgl-project/sglang/pull/30878) perf: reuse MoonViT FA3 max-seqlen metadata
- [#28982](https://github.com/sgl-project/sglang/pull/28982) fix(mtp): avoid mtp perf regression in deepseek when enable eplb
- [#30797](https://github.com/sgl-project/sglang/pull/30797) (Opened) [GDN] Fuse the linear-attention prefill prologue and cut per-layer host overhead
- [#30503](https://github.com/sgl-project/sglang/pull/30503) (Opened) [Perf][CP]: optimize glm5.2 prefill performance using comm-comp overlap triton kernels
- [#30947](https://github.com/sgl-project/sglang/pull/30947) (Opened) [1/3] [EAGLE] perf: Fuse topk=1 draft postprocess
- [#30948](https://github.com/sgl-project/sglang/pull/30948) (Opened) [2/3] [EAGLE] perf: Fuse TP vocab-parallel embedding
- [#30511](https://github.com/sgl-project/sglang/pull/30511) (Opened) [HiCache] Merge HiCache event checks to reduce decode overhead
- [#30949](https://github.com/sgl-project/sglang/pull/30949) (Opened) [3/3] [EAGLE] perf: Remove redundant draft capture input staging
</details>

<details>
<summary>Kernels & attention (53)</summary>

- [#30249](https://github.com/sgl-project/sglang/pull/30249) [mem_cache][6/N] refactor: move MHA host-pool into pool_host/mha.py
- [#29421](https://github.com/sgl-project/sglang/pull/29421) [Feat][GLM5.2] Add DSA Cache Layer Split under Prefill CP
- [#30711](https://github.com/sgl-project/sglang/pull/30711) [Refactor] Split DeepSeek-V4 MQALayer into a reusable attention base
- [#30478](https://github.com/sgl-project/sglang/pull/30478) Add DCP to runtime parallel context
- [#30489](https://github.com/sgl-project/sglang/pull/30489) [refactor] Move the EP dispatcher and fusion-workspace manager state onto ctx.resources
- [#29734](https://github.com/sgl-project/sglang/pull/29734) [GDN] Auto-select FlashInfer GDN prefill on validated SM100 configs
- [#30842](https://github.com/sgl-project/sglang/pull/30842) Revert "[Spec] Anchor GLM-5.2 MTP IndexShare topk on the draft-extend…"
- [#28527](https://github.com/sgl-project/sglang/pull/28527) [Diffusion][CPU] Adding AMX optimizations for CPU platform
- [#30716](https://github.com/sgl-project/sglang/pull/30716) [Diffusion] Revert CPU AMX optimizations
- [#28788](https://github.com/sgl-project/sglang/pull/28788) [AMD] Fix int32 offset overflow in Triton decode-attention kernels
- [#30708](https://github.com/sgl-project/sglang/pull/30708) [style] Extract init-static values in forward path
- [#30695](https://github.com/sgl-project/sglang/pull/30695) [Refactor] Make DeepSeek-V4 attention backend tolerate an absent CPU seq_lens mirror
- [#30896](https://github.com/sgl-project/sglang/pull/30896) [Fix] Unify ForwardBatch extend lens cpu fields to their declared list type
- [#30255](https://github.com/sgl-project/sglang/pull/30255) Fix DSV4 prefill large Triton recompilation idle across context lengths
- [#30439](https://github.com/sgl-project/sglang/pull/30439) Fix FA3 prefill CP NaNs
- [#30465](https://github.com/sgl-project/sglang/pull/30465) [Cherry-pick to release/v0.5.15] Fix FA3 prefill CP NaNs ([#30439](https://github.com/sgl-project/sglang/pull/30439))
- [#30629](https://github.com/sgl-project/sglang/pull/30629) [NPU]Fix npu import cutlass error
- [#30454](https://github.com/sgl-project/sglang/pull/30454) [NPU] fix npu import cutlass error
- [#30627](https://github.com/sgl-project/sglang/pull/30627) Fix CuTe DSL DSA paged MQA export
- [#29479](https://github.com/sgl-project/sglang/pull/29479) [AMD] fix dsv4 indexer dtype dispatch on gfx950
- [#30725](https://github.com/sgl-project/sglang/pull/30725) [Cherry-pick to release/v0.5.15] [AMD] fix dsv4 indexer dtype dispatch on gfx950 ([#29479](https://github.com/sgl-project/sglang/pull/29479))
- [#30729](https://github.com/sgl-project/sglang/pull/30729) [Cherry-pick to release/v0.5.15] [AMD] Fix DeepSeekV4 server cutlass error (#30374)
- [#30589](https://github.com/sgl-project/sglang/pull/30589) [NPU][bugfix] Fix NPU KernelLaunch Failure in rotate_input_ids_triton with Empty Batch
- [#30628](https://github.com/sgl-project/sglang/pull/30628) [NPU][bugfix] Fix NPU KernelLaunch Failure in rotate_input_ids_triton with Empty Batch
- [#29729](https://github.com/sgl-project/sglang/pull/29729) Add opt-in SGLANG_ROPE_CACHE_FP32 to keep RoPE cache in fp32 on non-CUDA
- [#30579](https://github.com/sgl-project/sglang/pull/30579) [Tiny] Fix docstring in CP abstractions
- [#30501](https://github.com/sgl-project/sglang/pull/30501) (Opened) KV Cache Shard with Sequence Split
- [#30575](https://github.com/sgl-project/sglang/pull/30575) (Opened) [AMD] Enable Fast Triton Sparse MLA backend
- [#30792](https://github.com/sgl-project/sglang/pull/30792) (Opened) [Kernel] Migrate DSA + DSV4 attention kernels to sglang.kernels (RFC #29630, Phase 2.5, 5/7)
- [#30514](https://github.com/sgl-project/sglang/pull/30514) (Opened) [DSA] Integrate Q8KV8 FP8 Sparse MLA Prefill into the DSA Backend (DeepSeek-V3.2)
- [#30546](https://github.com/sgl-project/sglang/pull/30546) (Opened) [DSA] Opt-in MXFP4 index-K cache for GLM-5.x / DeepSeek-V3.2 (port of #26209), with fused-kernel MXFP4 mode
- [#30756](https://github.com/sgl-project/sglang/pull/30756) (Opened) Integrate pplx a2a backend
- [#30825](https://github.com/sgl-project/sglang/pull/30825) (Opened) [FullCG] Support chunked cached-prefix prefill
- [#30482](https://github.com/sgl-project/sglang/pull/30482) (Opened) [4/N][CP] Support interleave strategy for cp v2
- [#30885](https://github.com/sgl-project/sglang/pull/30885) (Opened) [Feature] Support DeepSeek V4 in PDMux
- [#30444](https://github.com/sgl-project/sglang/pull/30444) (Opened) Support decode context parallel for DeepSeek MLA on the triton attention backend
- [#30469](https://github.com/sgl-project/sglang/pull/30469) (Opened) [AMD] Enable MLA DCP for aiter backend
- [#30807](https://github.com/sgl-project/sglang/pull/30807) (Opened) [trtllm_mla] Fuse cuda-graph metadata rebuild into one triton kernel
- [#30787](https://github.com/sgl-project/sglang/pull/30787) (Opened) [Kernel] Migrate top-level srt/layers stray kernels to sglang.kernels (RFC #29630, Phase 2.5, 3/7)
- [#30540](https://github.com/sgl-project/sglang/pull/30540) (Opened) [Attention Backend] Add HPC-Ops attention backend
- [#30923](https://github.com/sgl-project/sglang/pull/30923) (Opened) [DSA] Compact indexer K cache: drop slots for skip_topk (shared) layers (+15.8% KV capacity on GLM-5.2)
- [#30839](https://github.com/sgl-project/sglang/pull/30839) (Opened) [bug-fix] Stabilize GLM-5.2 MTP IndexShare across PD and CUDA graph replay
- [#30789](https://github.com/sgl-project/sglang/pull/30789) (Opened) [Kernel] Migrate generic attention kernels to sglang.kernels (RFC #29630, Phase 2.5, 4/7)
- [#30715](https://github.com/sgl-project/sglang/pull/30715) (Opened) [AMD] [GLM5] Fuse DSA indexer query Hadamard + FP8 quant into one Triton kernel (gfx950)
- [#30898](https://github.com/sgl-project/sglang/pull/30898) (Opened) Enable breakable prefill CUDA graph for DP attention
- [#30793](https://github.com/sgl-project/sglang/pull/30793) (Opened) [Kernel] Migrate linear-attention, MiniMax-sparse and diffusion kernels to sglang.kernels (RFC #29630, Phase 2.5, 6/7)
- [#30795](https://github.com/sgl-project/sglang/pull/30795) (Opened) [Kernel] Relocate vendored fla and mamba kernel trees to sglang.kernels (RFC #29630, Phase 2.5, 7/7)
- [#30830](https://github.com/sgl-project/sglang/pull/30830) (Opened) refactor(attn): decouple TRTLLM MHA backends from FlashInfer
- [#30916](https://github.com/sgl-project/sglang/pull/30916) (Opened) Fix dp-attention + speculative decoding crashes in flashinfer MLA backend
- [#30578](https://github.com/sgl-project/sglang/pull/30578) (Opened) feat: flush decode KV only for prefill reads on extend requests
- [#30451](https://github.com/sgl-project/sglang/pull/30451) (Opened) [NPU] FIX CMB illusion of garbled characters acc problems, in prefix cache mtp scenarios.
- [#30922](https://github.com/sgl-project/sglang/pull/30922) (Opened) [DSA] Skip building the Indexer on skip_topk (shared) layers
- [#30862](https://github.com/sgl-project/sglang/pull/30862) (Opened) kda: track mamba states for the radix cache
- [#30861](https://github.com/sgl-project/sglang/pull/30861) (Opened) kda: pack q/k/v extend conv into a single causal_conv1d_fn call
- [#30519](https://github.com/sgl-project/sglang/pull/30519) (Opened) [AMD] [GLM5] fp8 MLA absorbed bmm for GLM-5.2 on gfx950
- [#30950](https://github.com/sgl-project/sglang/pull/30950) (Opened) Fix mamba conv state dtype defaulting to bfloat16 for FP16 hybrid linear-attention models
- [#30732](https://github.com/sgl-project/sglang/pull/30732) (Opened) mhc: portable Triton hc_split_sinkhorn fallback for non-TileLang bac…
- [#30753](https://github.com/sgl-project/sglang/pull/30753) (Opened) [KDA] Fuse o_proj + MLP AllReduce with the next RMSNorm via LayerCommunicator
- [#30474](https://github.com/sgl-project/sglang/pull/30474) (Opened) [sglang-miles] Allocate DSA cuda-graph page_table and flashmla_metadata in TMS cuda_graph region
- [#30915](https://github.com/sgl-project/sglang/pull/30915) (Opened) [Feature] Megatron LayerNorm sequence parallelism (--enable-layernorm-sp)
</details>

<details>
<summary>MoE & quantization (44)</summary>

- [#30802](https://github.com/sgl-project/sglang/pull/30802) [refactor] Move MLP collective flags onto ForwardFlags
- [#30347](https://github.com/sgl-project/sglang/pull/30347) [refactor] Collect MoE and DP-attention runtime state into typed flag groups
- [#30866](https://github.com/sgl-project/sglang/pull/30866) Tune VLM MoE paths
- [#30646](https://github.com/sgl-project/sglang/pull/30646) Improve EPLB dispatch handling and diagnostics
- [#29275](https://github.com/sgl-project/sglang/pull/29275) Fix gfx95 bpreshuffle FP8 activation scale layout
- [#30724](https://github.com/sgl-project/sglang/pull/30724) [Cherry-pick to release/v0.5.15] Fix gfx95 bpreshuffle FP8 activation scale layout ([#29275](https://github.com/sgl-project/sglang/pull/29275))
- [#25694](https://github.com/sgl-project/sglang/pull/25694) [Quantization][Bugfix]: Join multi-arg RuntimeError in Quark _check_scheme_supported
- [#25519](https://github.com/sgl-project/sglang/pull/25519) [Quantization][bugfix] Correct E8M0 NaN-sentinel detection in e8m0_to_f32
- [#30450](https://github.com/sgl-project/sglang/pull/30450) Fix FlashInfer A2A IMA by DP-synchronizing the decode graph bucket (#30242)
- [#30387](https://github.com/sgl-project/sglang/pull/30387) Fix zero expert routed ids for MoE backends
- [#28658](https://github.com/sgl-project/sglang/pull/28658) [AMD] Fuse shared-expert sigmoid + bf16->fp32 cast into the MoE append kernel (3 kernels -> 1)
- [#30829](https://github.com/sgl-project/sglang/pull/30829) [eplb] chunk expert-weight P2P on CUDA to prevent NCCL rebalance hang
- [#30460](https://github.com/sgl-project/sglang/pull/30460) [DeepSeek V2] Reorder dual-stream MoE to main-first to avoid CUDA graph stream explosion
- [#30714](https://github.com/sgl-project/sglang/pull/30714) [Cherry-pick to release/v0.5.15] [DeepSeek V2] Reorder dual-stream MoE to main-first to avoid CUDA graph stream explosion ([#30460](https://github.com/sgl-project/sglang/pull/30460))
- [#29030](https://github.com/sgl-project/sglang/pull/29030) [NPU] use standalone group for moe ep
- [#30721](https://github.com/sgl-project/sglang/pull/30721) [NPU] use standalone group for moe ep
- [#30828](https://github.com/sgl-project/sglang/pull/30828) Make the mxfp8 MoE runner backend list extensible
- [#30726](https://github.com/sgl-project/sglang/pull/30726) [Cherry-pick to release/v0.5.15] [AMD] [MORI-EP] Skip LocalExpertCount kernel in decode graph when not recording (#30302)
- [#25467](https://github.com/sgl-project/sglang/pull/25467) [Quantization] Update error message strings with correct framework name in Quark/compressed-tensors
- [#30727](https://github.com/sgl-project/sglang/pull/30727) [Cherry-pick to release/v0.5.15] [AMD] Cap DSV4 Flash max_total_num_tokens (#30313)
- [#30443](https://github.com/sgl-project/sglang/pull/30443) [NVIDIA] Allow modelopt_mixed quantization with flashinfer_cutedsl MoE runner
- [#30426](https://github.com/sgl-project/sglang/pull/30426) [Tiny] Fix Import Error for Pure TP config with flashinfer_mxfp4
- [#30667](https://github.com/sgl-project/sglang/pull/30667) refactor topk part for npu.
- [#29480](https://github.com/sgl-project/sglang/pull/29480) [NPU] Add extra topk_weights input in deepep ll dispatch
- [#30448](https://github.com/sgl-project/sglang/pull/30448) (Opened) Refactor FP4 quantization and remove deprecated JIT kernels
- [#30924](https://github.com/sgl-project/sglang/pull/30924) (Opened) [JIT] Trait-driven per_token_group_quant_v3: unify the quant kernel family (flat + masked)
- [#30553](https://github.com/sgl-project/sglang/pull/30553) (Opened) [2/N] elastic-ep: Enable EPLB after scale-up
- [#30786](https://github.com/sgl-project/sglang/pull/30786) (Opened) [Kernel] Migrate scattered MoE kernels to sglang.kernels (RFC #29630, Phase 2.5, 2/7)
- [#30768](https://github.com/sgl-project/sglang/pull/30768) (Opened) :construction: [WIP][llm][npu][quant] Add W8A8 MXFP8 quantization for Qwen3 MoE on Ascend NPU
- [#30784](https://github.com/sgl-project/sglang/pull/30784) (Opened) [Kernel] Migrate scattered quantization kernels to sglang.kernels (RFC #29630, Phase 2.5, 1/7)
- [#30541](https://github.com/sgl-project/sglang/pull/30541) (Opened) [MoE Backend] Add HPC-Ops FP8 MoE runner backend
- [#30888](https://github.com/sgl-project/sglang/pull/30888) (Opened) [Bugfix] Support gated ModelOpt NVFP4 MoE intermediate padding
- [#30565](https://github.com/sgl-project/sglang/pull/30565) (Opened) [AMD] [GLM5] Fix MTP layer_quant_config in-place mutation + add nextn Quark-exclude unit test
- [#30952](https://github.com/sgl-project/sglang/pull/30952) (Opened) Auto-select DeepSeek V4 FP4 MoE backends
- [#30761](https://github.com/sgl-project/sglang/pull/30761) (Opened) [RL] update_weights_from_disk: load quantized checkpoints like initial loading
- [#30749](https://github.com/sgl-project/sglang/pull/30749) (Opened) [RL] update_weights_from_disk: load quantized checkpoints like initial loading
- [#30895](https://github.com/sgl-project/sglang/pull/30895) (Opened) [Bugfix] Fix Qwen MoE CUDA graph padding rows
- [#30603](https://github.com/sgl-project/sglang/pull/30603) (Opened) feat: batch-invariant deterministic inference for DeepSeek MoE on FA4 + DeepGEMM + DeepEP
- [#30864](https://github.com/sgl-project/sglang/pull/30864) (Opened) nextn: extend the fp8 ignore-list with the sglang nextn prefix
- [#30552](https://github.com/sgl-project/sglang/pull/30552) (Opened) [NVIDIA] Extend modelopt_fp4-only MoE heuristics to NVFP4-expert modelopt_mixed
- [#30681](https://github.com/sgl-project/sglang/pull/30681) (Opened) Support serving FP8 MoE on Ampere via Marlin W8A16
- [#30900](https://github.com/sgl-project/sglang/pull/30900) (Opened) [Quantization][Bugfix] Fix bug related to fp8 max on gfx95x for per-token-group quant (ROCm)
- [#30794](https://github.com/sgl-project/sglang/pull/30794) (Opened) Use DeepGEMM deduplication API
- [#30939](https://github.com/sgl-project/sglang/pull/30939) (Opened) Fix HashTopK empty output shapes
- [#30688](https://github.com/sgl-project/sglang/pull/30688) (Opened) Fix MoE functionality on RDNA (gfx1100/gfx1201) via Python-level fallback dispatch
- [#30706](https://github.com/sgl-project/sglang/pull/30706) (Opened) feat(moriep): add fp4 combine dtype (SGLANG_MORI_COMBINE_DTYPE=fp4)
</details>

<details>
<summary>Model support (34)</summary>

- [#27168](https://github.com/sgl-project/sglang/pull/27168) [diffusion] feat: support action output for cosmos3
- [#25381](https://github.com/sgl-project/sglang/pull/25381) [Diffusion] SGLang backend for GLM Image AR. Step 1 - Separate server
- [#29742](https://github.com/sgl-project/sglang/pull/29742) [diffusion] Fix Z-Image accuracy
- [#27757](https://github.com/sgl-project/sglang/pull/27757) Fix Mistral GSM8K chat eval
- [#29777](https://github.com/sgl-project/sglang/pull/29777) [diffusion] Support SP for Krea-2
- [#30361](https://github.com/sgl-project/sglang/pull/30361) [diffusion] support LingBot-World 2.0
- [#30396](https://github.com/sgl-project/sglang/pull/30396) Fix garbage output for bare-tekken Mistral checkpoints (e.g. Leanstral)
- [#30265](https://github.com/sgl-project/sglang/pull/30265) [AMD] Fix GLM-5.2 MTP Quark excludes
- [#29218](https://github.com/sgl-project/sglang/pull/29218) [Spec] DFlash: support pure-MLA targets with an fp8 KV cache (Kimi-K2.x-NVFP4)
- [#27576](https://github.com/sgl-project/sglang/pull/27576) [diffusion] doc: update Cosmos3 cookbook
- [#29883](https://github.com/sgl-project/sglang/pull/29883) [BUG] fix strip streaming empty-string suffix from DSV4 tool arguments
- [#30782](https://github.com/sgl-project/sglang/pull/30782) Add diffusion BCG prompt conditioning guard
- [#26505](https://github.com/sgl-project/sglang/pull/26505) [Fix] mm processor double bos
- [#28926](https://github.com/sgl-project/sglang/pull/28926) [diffusion]: enable RL rollout path for LTX-2.3 post-training
- [#30602](https://github.com/sgl-project/sglang/pull/30602) [Fix] Prevent silent VLM server crash when /dev/shm is exhausted during multimodal feature transport
- [#30791](https://github.com/sgl-project/sglang/pull/30791) [diffusion][docs] sync cookbook and log hygiene
- [#30826](https://github.com/sgl-project/sglang/pull/30826) Update GLM-5.2 NVFP4 cookbook
- [#30006](https://github.com/sgl-project/sglang/pull/30006) Fix prefill CUDA graph disabled for deeply-nested multimodal models
- [#30518](https://github.com/sgl-project/sglang/pull/30518) [diffusion] rename for lingbot world v2
- [#30679](https://github.com/sgl-project/sglang/pull/30679) (Opened) [Diffusion] Add DreamZero action generation support
- [#30614](https://github.com/sgl-project/sglang/pull/30614) (Opened) docs: Add Ascend A2 & A3 support and benchmark placeholders for diffusion models
- [#30805](https://github.com/sgl-project/sglang/pull/30805) (Opened) [DSv4] Integrate TRT-LLM DSv4 Attention for SM100/103
- [#30930](https://github.com/sgl-project/sglang/pull/30930) (Opened) feat: add Seed-OSS (SeedOssForCausalLM) model support
- [#30869](https://github.com/sgl-project/sglang/pull/30869) (Opened) Fix Kimi-VL encoder parallelism
- [#30536](https://github.com/sgl-project/sglang/pull/30536) (Opened) [Cosmos3] Add cosmos3 Reasoner to llm only inference
- [#30683](https://github.com/sgl-project/sglang/pull/30683) (Opened) [NPU] [Diffusion] T2I GLM-Image dynamic batching support
- [#30486](https://github.com/sgl-project/sglang/pull/30486) (Opened) [diffusion] RL rollout support for the Cosmos3 pipeline
- [#30487](https://github.com/sgl-project/sglang/pull/30487) (Opened) [diffusion] Support Ideogram TurboTime LoRA inference
- [#30889](https://github.com/sgl-project/sglang/pull/30889) (Opened) feat: enable piecewise prefill graph for Kimi K2.5/K2.7
- [#30812](https://github.com/sgl-project/sglang/pull/30812) (Opened) [AMD] GLM-5.1-FP8: MI300X benchmarks + FP8 cells
- [#30909](https://github.com/sgl-project/sglang/pull/30909) (Opened) [HiSparse] Fix inflated full token usage for DeepSeek V4
- [#30456](https://github.com/sgl-project/sglang/pull/30456) (Opened) [NemotronH] Load shared embed_tokens/lm_head in MTP draft weights
- [#30610](https://github.com/sgl-project/sglang/pull/30610) (Opened) Fix Mistral Large 3 EAGLE DSA detection
- [#30741](https://github.com/sgl-project/sglang/pull/30741) (Opened) Prewarm DSV4 MHC post kernel at model load
</details>

<details>
<summary>Parallelism & scheduling (58)</summary>

- [#25372](https://github.com/sgl-project/sglang/pull/25372) [PDD] Add true request retraction for PDD
- [#30855](https://github.com/sgl-project/sglang/pull/30855) support DSV4 NPU PD disaggregation
- [#29408](https://github.com/sgl-project/sglang/pull/29408) Avoid implicit field-based side channel in Scheduler planning
- [#30408](https://github.com/sgl-project/sglang/pull/30408) Fix DSV4 HiSparse SWA tail allocation forwarding
- [#30574](https://github.com/sgl-project/sglang/pull/30574) [kv canary] Support UnifiedRadixCache in kv-canary and bracket nested model.forward
- [#30626](https://github.com/sgl-project/sglang/pull/30626) [UnifiedTree]: Sync mamba int8 checkpoint
- [#30461](https://github.com/sgl-project/sglang/pull/30461) [DSV4] Fix draft SWA transfer for disaggregated MTP
- [#29407](https://github.com/sgl-project/sglang/pull/29407) Localize cur_batch field in Scheduler to avoid field-based state access
- [#29405](https://github.com/sgl-project/sglang/pull/29405) Fix pipeline-parallel abort missing in-flight requests in non-current microbatch slots
- [#30747](https://github.com/sgl-project/sglang/pull/30747) Fix: add grammar sync in PP for structured output
- [#30737](https://github.com/sgl-project/sglang/pull/30737) test(disagg): set MC_GID_INDEX on RoCE hosts so mooncake KV transfer works
- [#30440](https://github.com/sgl-project/sglang/pull/30440) feat(grpc): support disaggregated generation requests
- [#29834](https://github.com/sgl-project/sglang/pull/29834) Fix scheduler crash on prefill-unreachable decode abort
- [#30409](https://github.com/sgl-project/sglang/pull/30409) Make CUDA graph disabling PD-role-aware (prefill/decode)
- [#30310](https://github.com/sgl-project/sglang/pull/30310) Increase the KV cache pool when using indexShare by 15%
- [#30472](https://github.com/sgl-project/sglang/pull/30472) Revert "Increase the KV cache pool when using indexShare by 15% ([#30310](https://github.com/sgl-project/sglang/pull/30310))"
- [#30707](https://github.com/sgl-project/sglang/pull/30707) [style] Extract init-static values in scheduler hot path
- [#30339](https://github.com/sgl-project/sglang/pull/30339) [AMD] Fix stale SWA ring buffer on radix prefix reuse for DeepSeek-V4 with unified_kv backend
- [#27546](https://github.com/sgl-project/sglang/pull/27546) fix(pd): do not abort when req.disagg_prefill_dp_rank is used
- [#30636](https://github.com/sgl-project/sglang/pull/30636) [UnifiedTree]: Sync Replay SSM
- [#29406](https://github.com/sgl-project/sglang/pull/29406) Stop reading cur_batch in is_fully_idle and abort_request
- [#30844](https://github.com/sgl-project/sglang/pull/30844) bugfix: add NPU to send_first check to prevent PP ring deadlock
- [#30545](https://github.com/sgl-project/sglang/pull/30545) (Opened) [PD] Support staging buffer with radix cache and radix-prefix pre-transfer
- [#30728](https://github.com/sgl-project/sglang/pull/30728) (Opened) Add Mooncake Store file-level weight connector for SGLang
- [#30581](https://github.com/sgl-project/sglang/pull/30581) (Opened) [HiCache] Make host size a per-rank total memory budget
- [#30723](https://github.com/sgl-project/sglang/pull/30723) (Opened) [PD] Fix parallel sampling with disaggregated serving
- [#30543](https://github.com/sgl-project/sglang/pull/30543) (Opened) [AMD] WIP - Amd/kimik26 disagg decodemeta
- [#30652](https://github.com/sgl-project/sglang/pull/30652) (Opened) fix deepseekv4-pd-hisparse memory pool bug
- [#30551](https://github.com/sgl-project/sglang/pull/30551) (Opened) fix(pd): propagate aborted requests and clean up Mooncake rooms
- [#30775](https://github.com/sgl-project/sglang/pull/30775) (Opened) [RFC] Pipeline parallelism x speculative decoding (EAGLE/MTP) compatibility
- [#30899](https://github.com/sgl-project/sglang/pull/30899) (Opened) [Bugfix] fix(hicache): wait for decode offload before retraction
- [#30796](https://github.com/sgl-project/sglang/pull/30796) (Opened) feat(hicache): retain hinted prompt KV in Mooncake L3
- [#30497](https://github.com/sgl-project/sglang/pull/30497) (Opened) [DSV4] Enable overlap scheduling for online C128 MTP
- [#30507](https://github.com/sgl-project/sglang/pull/30507) (Opened) Add QoS-aware cache policy
- [#30637](https://github.com/sgl-project/sglang/pull/30637) (Opened) Fix NIXL bootstrap handling for foreign traffic
- [#30531](https://github.com/sgl-project/sglang/pull/30531) (Opened) Reland "Increase the KV cache pool when using indexShare by 15% ([#30310](https://github.com/sgl-project/sglang/pull/30310))"
- [#30762](https://github.com/sgl-project/sglang/pull/30762) (Opened) fix(hicache/umbp): support DeepSeek-V4 hybrid HostPoolGroup (multi-po…
- [#30769](https://github.com/sgl-project/sglang/pull/30769) (Opened) [PD] Add decode-side bootstrap timeout cleanup for Mooncake
- [#30951](https://github.com/sgl-project/sglang/pull/30951) (Opened) [PD] Improve optimistic prefill
- [#30748](https://github.com/sgl-project/sglang/pull/30748) (Opened) Route PD server warmup to every DP rank
- [#30658](https://github.com/sgl-project/sglang/pull/30658) (Opened) [HiCache] Optimize HiCache host pool free-list release
- [#30850](https://github.com/sgl-project/sglang/pull/30850) (Opened) [HiCache]fix: hybrid-mamba prefix ending at chunk boundary is never backed up
- [#30833](https://github.com/sgl-project/sglang/pull/30833) (Opened) Allocate single-node DP-attention ports from a free block to avoid collisions
- [#30806](https://github.com/sgl-project/sglang/pull/30806) (Opened) [Feature] Add sjf schedule policy: shortest-job-first with aging for prefill-only
- [#30674](https://github.com/sgl-project/sglang/pull/30674) (Opened) Fix missed hisparse release and stale field cleanup in pause retract
- [#30669](https://github.com/sgl-project/sglang/pull/30669) (Opened) Remove dead ScheduleBatch fields and avoid inplace seq_lens bump
- [#30890](https://github.com/sgl-project/sglang/pull/30890) (Opened) fix(disagg): require extra-state transfer success for Mooncake prefill
- [#30673](https://github.com/sgl-project/sglang/pull/30673) (Opened) Fix non-existent abort mode in Scheduler.pause_generation and inline retract_all
- [#30676](https://github.com/sgl-project/sglang/pull/30676) (Opened) Avoid implicit running_batch access in dllm and pdmux scheduling
- [#30692](https://github.com/sgl-project/sglang/pull/30692) (Opened) Fix decode receiver cleanup bookkeeping
- [#30912](https://github.com/sgl-project/sglang/pull/30912) (Opened) feat(sglang-miles): Support aborting requests by rid prefix
- [#30457](https://github.com/sgl-project/sglang/pull/30457) (Opened) Support scheduler_recv_interval (recv skipper) under DP-attention
- [#30651](https://github.com/sgl-project/sglang/pull/30651) (Opened) cookbook(deepseek-v4): add MORI disagg backend for AMD + bump MI355X image
- [#30757](https://github.com/sgl-project/sglang/pull/30757) (Opened) [PD] Fix HiSparse + SWA decode hang/rejection for long inputs
- [#30521](https://github.com/sgl-project/sglang/pull/30521) (Opened) [fix] Prefill delayer: make queue-timeout release deterministic across ranks
- [#30929](https://github.com/sgl-project/sglang/pull/30929) (Opened) Support decode radix cache on DeepSeek-V4 (hybrid-SWA, SWA-tail prealloc)
- [#30893](https://github.com/sgl-project/sglang/pull/30893) (Opened) [Refactor] Unify HiSparse device-pool mapping internals
- [#30468](https://github.com/sgl-project/sglang/pull/30468) (Opened) Using UnifiedRadixTree by default for SWA, Mamba, and DSA models
- [#30908](https://github.com/sgl-project/sglang/pull/30908) (Opened) [Feature] Release PyNccl communicator memory in sleep mode
- [#30882](https://github.com/sgl-project/sglang/pull/30882) (Opened) [HiCache]fix: hybrid-mamba final snapshot is unmatchable for page-aligned prompts
</details>

<details>
<summary>Speculative Decoding (20)</summary>

- [#30857](https://github.com/sgl-project/sglang/pull/30857) [Spec] Extract shared draft worker construction and generalize draft sampler capture
- [#30944](https://github.com/sgl-project/sglang/pull/30944) [Spec] Add kill-switch env for draft-extend CUDA graph capture
- [#30235](https://github.com/sgl-project/sglang/pull/30235) [Intel GPU] xpu_piecewise: fall back to eager when PCG capture stream is unset
- [#30680](https://github.com/sgl-project/sglang/pull/30680) Fix DFlash mamba verify init ordering
- [#30435](https://github.com/sgl-project/sglang/pull/30435) [Fix] Chain the seq_lens publish event records so prebuilt seeding keeps the forward fence
- [#30853](https://github.com/sgl-project/sglang/pull/30853) [Spec] Enable draft extend cuda graph for DeepSeek-V4 attention backend
- [#30513](https://github.com/sgl-project/sglang/pull/30513) (Opened) [Spec] DSpark support PD and DeepEP
- [#30466](https://github.com/sgl-project/sglang/pull/30466) (Opened) [Spec] Distributed argmax for greedy EAGLE draft over TP (multimem NVLink scatter)
- [#30776](https://github.com/sgl-project/sglang/pull/30776) (Opened) [Spec] Add LFM2 / LFM2-MoE DSpark draft-model support
- [#30852](https://github.com/sgl-project/sglang/pull/30852) (Opened) [Spec] Reject DSpark speculators-convention checkpoints instead of silently degrading accept length
- [#30672](https://github.com/sgl-project/sglang/pull/30672) (Opened) Avoid mutating ScheduleBatch fields in place
- [#30548](https://github.com/sgl-project/sglang/pull/30548) (Opened) Speculative Decoding support for intel_xpu attention backend on XPU target
- [#30877](https://github.com/sgl-project/sglang/pull/30877) (Opened) [feat] [spec decoding] support STANDALONE spec decoding with DP attention
- [#30684](https://github.com/sgl-project/sglang/pull/30684) (Opened) [Spec] DSpark support glm5.2-dspark
- [#30745](https://github.com/sgl-project/sglang/pull/30745) (Opened) [AMD] Support DeepSeek V4 DSpark on AMD platform
- [#30746](https://github.com/sgl-project/sglang/pull/30746) (Opened) [Bugfix] Fix CUDA graph lookup when padding is disabled
- [#30554](https://github.com/sgl-project/sglang/pull/30554) (Opened) [Spec] Size shared logits buffer for adaptive candidates
- [#30524](https://github.com/sgl-project/sglang/pull/30524) (Opened) [NPU] eagle3 support modelslim quarot
- [#30774](https://github.com/sgl-project/sglang/pull/30774) (Opened) [PP] Fix proxy tensor buffer sizing and refresh for speculative verify
- [#30937](https://github.com/sgl-project/sglang/pull/30937) (Opened) fix: avoid double KV release on disaggregated prefill grammar errors
</details>

<details>
<summary>Hardware & arch (12)</summary>

- [#28534](https://github.com/sgl-project/sglang/pull/28534) [AMD] Enable JIT staged HiCache write-back and fix CPU-index crash
- [#29417](https://github.com/sgl-project/sglang/pull/29417) [AMD] Enable unified-KV HiCache on DeepSeek-V4
- [#30604](https://github.com/sgl-project/sglang/pull/30604) [CPU] update fla.cpp to support when num_head_v is not multiples of 16
- [#30843](https://github.com/sgl-project/sglang/pull/30843) [DOCS][NPU]update npu support features and models
- [#30504](https://github.com/sgl-project/sglang/pull/30504) [NPU] [DOC] Remove unsupported options of features on Ascend NPU
- [#30647](https://github.com/sgl-project/sglang/pull/30647) [NPU] [DOC] remove unsupported models from Ascend NPU models list
- [#30577](https://github.com/sgl-project/sglang/pull/30577) [NPU] [DOC] fix model name error on Ascend NPU
- [#30638](https://github.com/sgl-project/sglang/pull/30638) [NPU][bugfix] Fix post_capture_active TypeError on NPU by adding param to NPUMHATokenToKVPool
- [#30838](https://github.com/sgl-project/sglang/pull/30838) (Opened) [JIT] Refactor dtype traits into DTypeTrait and unify warp reductions
- [#30767](https://github.com/sgl-project/sglang/pull/30767) (Opened) [NPU] [DOC] Optimize and fix docs issues on Ascend NPU
- [#30705](https://github.com/sgl-project/sglang/pull/30705) (Opened) [Diffusion] Support SM12.x GPUs (RTX PRO 6000 Blackwell / RTX 50xx / DGX Spark GB10)
- [#30562](https://github.com/sgl-project/sglang/pull/30562) (Opened) [sgl-kernel] Let import survive a missing common_ops binary via SGLANG_KERNEL_ALLOW_MISSING_OPS (GB10 / SM121)
</details>

<details>
<summary>API & serving (29)</summary>

- [#30366](https://github.com/sgl-project/sglang/pull/30366) [RL] Add /pull_weights: engine-side pull of published weights into a host-local checkpoint (sglang-miles)
- [#30463](https://github.com/sgl-project/sglang/pull/30463) [Bugfix] Map reasoning_effort=low to Nemotron-3 Super low_effort + warn on unsupported levels
- [#30623](https://github.com/sgl-project/sglang/pull/30623) [Refactor] Share chat encoding dispatch between serving and offline tools
- [#30573](https://github.com/sgl-project/sglang/pull/30573) Configurable decode retraction order
- [#30630](https://github.com/sgl-project/sglang/pull/30630) [tokenizer] Support pluggable tokenizer worker class in multi-tokenizer mode
- [#30811](https://github.com/sgl-project/sglang/pull/30811) Support priority request header override
- [#30499](https://github.com/sgl-project/sglang/pull/30499) [lora] Support GDN in_proj_ba adapters for Qwen3.5
- [#30643](https://github.com/sgl-project/sglang/pull/30643) Fix TiktokenTokenizer missing num_special_tokens_to_add
- [#30783](https://github.com/sgl-project/sglang/pull/30783) (Opened) feat(scheduler): extend NVTX markers, add env vars, latency tracker, …
- [#30650](https://github.com/sgl-project/sglang/pull/30650) (Opened) Ref aware unified kv buffer
- [#30827](https://github.com/sgl-project/sglang/pull/30827) (Opened) feat: add cache salt support to KV cache events
- [#30771](https://github.com/sgl-project/sglang/pull/30771) (Opened) fix(frontend): offload blocking request preprocessing
- [#30621](https://github.com/sgl-project/sglang/pull/30621) (Opened) Fix image URL response for multiple outputs
- [#30876](https://github.com/sgl-project/sglang/pull/30876) (Opened) feat(tokenizer): tokenize chat prompts once instead of twice
- [#30894](https://github.com/sgl-project/sglang/pull/30894) (Opened) Validate PD top logprobs metadata limit
- [#30823](https://github.com/sgl-project/sglang/pull/30823) (Opened) [Bugfix] Handle missing chat encoding configs
- [#30904](https://github.com/sgl-project/sglang/pull/30904) (Opened) feat: unify multimodal feature transport
- [#30481](https://github.com/sgl-project/sglang/pull/30481) (Opened) fix(function_call): stop leaking truncated tool-call markup into non-streaming content
- [#30917](https://github.com/sgl-project/sglang/pull/30917) (Opened) Add return_token_ids support to completions and chat completions APIs
- [#30693](https://github.com/sgl-project/sglang/pull/30693) (Opened) [Feature] Add --gc-freeze-on-idle: move the long-lived heap out of GC scan scope
- [#30533](https://github.com/sgl-project/sglang/pull/30533) (Opened) more fixes for Nemotron 3 parser for tool call and force nonempty content
- [#30530](https://github.com/sgl-project/sglang/pull/30530) (Opened) [router] Break the SSE pump on client disconnect even while the upstream is pending
- [#30832](https://github.com/sgl-project/sglang/pull/30832) (Opened) Add 'anyOf' schema support for qwen3_coder tool call parser
- [#30801](https://github.com/sgl-project/sglang/pull/30801) (Opened) fix: prevent SSRF, arbitrary file read, and API key leak
- [#30467](https://github.com/sgl-project/sglang/pull/30467) (Opened) [server_args] Fix YAML options with deprecated aliases
- [#30682](https://github.com/sgl-project/sglang/pull/30682) (Opened) [BugFix] Preserve worker fanout when skip-tokenizer-init is enabled
- [#30799](https://github.com/sgl-project/sglang/pull/30799) (Opened) fix: validate chat_template with ImmutableSandboxedEnvironment (CVE-2…
- [#30560](https://github.com/sgl-project/sglang/pull/30560) (Opened) fix(server_args): normalize log level so uvicorn accepts it
- [#30903](https://github.com/sgl-project/sglang/pull/30903) (Opened) feat: log multimodal encoder DP tradeoffs
</details>

<details>
<summary>Tests, CI & build (58)</summary>

- [#30690](https://github.com/sgl-project/sglang/pull/30690) [misc] Remove unit test cases that fail the admission criteria
- [#30703](https://github.com/sgl-project/sglang/pull/30703) [misc] Remove unit test cases that fail the admission criteria (round 2)
- [#30713](https://github.com/sgl-project/sglang/pull/30713) [misc] Remove unit test cases that fail the admission criteria (round 3)
- [#28524](https://github.com/sgl-project/sglang/pull/28524) [sglang-miles] Cherrypick dumper & dump-comparator changes
- [#30654](https://github.com/sgl-project/sglang/pull/30654) Support per-regex diff-threshold predicates in the tensor comparator
- [#30121](https://github.com/sgl-project/sglang/pull/30121) [Apple Silicon] [CI] Move the MLX lane to the check-changes + pr-gate composite
- [#30386](https://github.com/sgl-project/sglang/pull/30386) [AMD] Run MI355X disaggregation Nightly Test with runtime checkout code mechanism
- [#30656](https://github.com/sgl-project/sglang/pull/30656) Cap diagnostic detail computation for failing tensors
- [#30615](https://github.com/sgl-project/sglang/pull/30615) [Bench] Add fixed-prompt mode and per-request spec accept length metrics
- [#30879](https://github.com/sgl-project/sglang/pull/30879) bench: support random image resolutions
- [#30307](https://github.com/sgl-project/sglang/pull/30307) [AMD] add dedicated jit-kernel-benchmark-test-amd stage + register portable JIT benches
- [#29939](https://github.com/sgl-project/sglang/pull/29939) Update test repository case scripts to the main community
- [#30657](https://github.com/sgl-project/sglang/pull/30657) Support grad injection and step override in the dumper's model dump
- [#30212](https://github.com/sgl-project/sglang/pull/30212) [AMD] Register 3 ROCm-portable JIT kernel tests for AMD CI
- [#30927](https://github.com/sgl-project/sglang/pull/30927) Gate Rust extension builds
- [#30709](https://github.com/sgl-project/sglang/pull/30709) [style] Extract init-static values in tokenizer + multimodal path
- [#30606](https://github.com/sgl-project/sglang/pull/30606) [Fix] Serialize FanOutCommunicator queueing calls with a FIFO-fair asyncio.Lock
- [#30897](https://github.com/sgl-project/sglang/pull/30897) Handle coredump dirs and cache hit updates
- plus 40 more minor CI, test, and benchmark updates
</details>

<details>
<summary>Refactors (14)</summary>

- [#30483](https://github.com/sgl-project/sglang/pull/30483) Enhance mechanical refactor proof construction and verification skill
- [#30493](https://github.com/sgl-project/sglang/pull/30493) [refactor] Retire the legacy config accessor and the remaining process singletons
- [#30346](https://github.com/sgl-project/sglang/pull/30346) [refactor] Read resolved config from server_args fields; retire the flags mirror tier
- [#30492](https://github.com/sgl-project/sglang/pull/30492) [refactor] Adopt get_parallel() everywhere and close out the parallel wrapper surface
- [#30299](https://github.com/sgl-project/sglang/pull/30299) [refactor] Move model-capability adjustments into the resolution pipeline
- [#30525](https://github.com/sgl-project/sglang/pull/30525) refactor(load-snapshot): build LoadSnapshot directly, drop legacy get_loads IPC
- [#30348](https://github.com/sgl-project/sglang/pull/30348) [refactor] ctx.resources: named slots, stream leases, and workspace buffer leases
- [#30447](https://github.com/sgl-project/sglang/pull/30447) [diffusion] Reorganize runtime utility modules
- [#30490](https://github.com/sgl-project/sglang/pull/30490) [refactor] Add the per-forward flags tier: ctx.forward
- [#30491](https://github.com/sgl-project/sglang/pull/30491) [refactor] Split the DP gathered-buffer state between flags.dp and ctx.forward
- [#30653](https://github.com/sgl-project/sglang/pull/30653) [Bugfix] Migrate retired parallel accessors
- [#30585](https://github.com/sgl-project/sglang/pull/30585) (Opened) [DO NOT MERGE] update mech refactor verify skills
- [#30616](https://github.com/sgl-project/sglang/pull/30616) (Opened) [mem_cache][7/N] refactor: move MLATokenToKVPoolHost to pool_host.mla
- [#30544](https://github.com/sgl-project/sglang/pull/30544) (Opened) [refactor] hoist force_nonempty_content into BaseReasoningFormatDetector
</details>

<details>
<summary>Docs (9)</summary>

- [#27551](https://github.com/sgl-project/sglang/pull/27551) [dLLM] Make FDFO a framework capability for all dLLM algorithms
- [#30494](https://github.com/sgl-project/sglang/pull/30494) [docs] Add the sglang-runtime-context skill
- [#28978](https://github.com/sgl-project/sglang/pull/28978) Enhance large class styles and code styles
- [#30146](https://github.com/sgl-project/sglang/pull/30146) Disable multi-threaded load by default when prefetch is on
- [#30608](https://github.com/sgl-project/sglang/pull/30608) [misc] Add unit test admission criteria to agent rules
- [#30751](https://github.com/sgl-project/sglang/pull/30751) (Opened) docs: migrate Release Lookup tool to Mintlify and auto-refresh its index
- [#30520](https://github.com/sgl-project/sglang/pull/30520) (Opened) [Cookbook][CPU]Update CPU model support info in Cookbook
- [#30571](https://github.com/sgl-project/sglang/pull/30571) (Opened) docs: sync LMSYS SGLang blog cards
- [#30836](https://github.com/sgl-project/sglang/pull/30836) (Opened) docs: add community health files (CONTRIBUTING.md, CHANGELOG.md)
</details>

<details>
<summary>Bugfixes (9)</summary>

- [#30584](https://github.com/sgl-project/sglang/pull/30584) Fix diffusion BCG lifetime and add Z-Image-Turbo CI
- [#30645](https://github.com/sgl-project/sglang/pull/30645) [DSA] Fix top-k v2 emitting invalid indices under tie overflow / inf scores (IMA in FA3 sparse decode)
- [#30698](https://github.com/sgl-project/sglang/pull/30698) [Cherry-pick to release/v0.5.15] [DSA] Fix top-k v2 emitting invalid indices under tie overflow / inf scores (IMA in FA3 sparse decode) ([#30645](https://github.com/sgl-project/sglang/pull/30645))
- [#30847](https://github.com/sgl-project/sglang/pull/30847) [Fix] Guard kernel OOB accesses and harden runtime edge cases
- [#30512](https://github.com/sgl-project/sglang/pull/30512) [DSA] Fix IMA in fused top-k v2: write all output slots on tie overflow
- [#30559](https://github.com/sgl-project/sglang/pull/30559) [Cherry-pick to release/v0.5.15] [DSA] Fix IMA in fused top-k v2: write all output slots on tie overflow ([#30512](https://github.com/sgl-project/sglang/pull/30512))
- [#30557](https://github.com/sgl-project/sglang/pull/30557) [AMD] Fix AITER custom all-gather CUDA-graph capture crash under torch_memory_saver
- [#30730](https://github.com/sgl-project/sglang/pull/30730) [Cherry-pick to release/v0.5.15] [AMD] Fix AITER custom all-gather CUDA-graph capture crash under torch_memory_saver ([#30557](https://github.com/sgl-project/sglang/pull/30557))
- [#30699](https://github.com/sgl-project/sglang/pull/30699) [Tiny] Fix Lint in [#30645](https://github.com/sgl-project/sglang/pull/30645)
- [#30704](https://github.com/sgl-project/sglang/pull/30704) [Cherry-pick to release/v0.5.15] [Tiny] Fix Lint in [#30645](https://github.com/sgl-project/sglang/pull/30645) ([#30699](https://github.com/sgl-project/sglang/pull/30699))
- [#30892](https://github.com/sgl-project/sglang/pull/30892) (Opened) [Fix] Check paged allocator capacity before kernel launch
- [#30804](https://github.com/sgl-project/sglang/pull/30804) (Opened) fix: replace raw pickle.loads with safe_pickle_loads in 13 distribute…
- [#30798](https://github.com/sgl-project/sglang/pull/30798) (Opened) fix: replace unsafe pickle/dill deserialization with SafeUnpickler
</details>

<details>
<summary>Other (14)</summary>

- [#30586](https://github.com/sgl-project/sglang/pull/30586) Move breakable CUDA graph back into model_executor/runner_backend_utils
- [#29716](https://github.com/sgl-project/sglang/pull/29716) feat(mem_cache): add client-side metadata cache for HiCacheFile storage
- [#30871](https://github.com/sgl-project/sglang/pull/30871) Add VLM prefill profiler ranges
- [#30834](https://github.com/sgl-project/sglang/pull/30834) [cuda-graph] Size breakable-graph shared buffer from warmup output; slice by produced row count
- [#30710](https://github.com/sgl-project/sglang/pull/30710) [style] Extract init-static values in memory-cache path
- [#27918](https://github.com/sgl-project/sglang/pull/27918) [BCG] Restore Qwen3.5 MRoPE fusion under breakable CUDA graph
- [#30702](https://github.com/sgl-project/sglang/pull/30702) Make KvVmmArena JIT stub unique per process
- [#30323](https://github.com/sgl-project/sglang/pull/30323) Use FP32 logits in MoEGate fallbacks
- [#30675](https://github.com/sgl-project/sglang/pull/30675) (Opened) Rewrite pause_generation retract path as req-level release and requeue for clarity
- [#30670](https://github.com/sgl-project/sglang/pull/30670) (Opened) Pass per-forward overrides to ForwardBatch.init_new as explicit arguments
- [#30535](https://github.com/sgl-project/sglang/pull/30535) (Opened) [hicache]: add mamba_io_kernel
- [#30738](https://github.com/sgl-project/sglang/pull/30738) (Opened) [Bugfix] Prevent HiCache KV publication beyond sidecar coverage
- [#30736](https://github.com/sgl-project/sglang/pull/30736) (Opened) fix: support non-128-aligned element sizes in HiCache JIT
- [#30607](https://github.com/sgl-project/sglang/pull/30607) (Opened) [SUPA][1/N] Add device detection and check_env support
- [#30913](https://github.com/sgl-project/sglang/pull/30913) (Opened) feat(sglang-miles): Support upsert when loading adapters from tensors/distributed
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0e6f97dcefed22a70635af4173d5759e5386846f250c6d35075fe69930887767 -->
