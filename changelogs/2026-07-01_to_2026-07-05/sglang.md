# sglang: PR digest (2026-07-01 to 2026-07-05)

_174 merged, 200 newly opened - source sgl-project/sglang, generated 2026-07-05T22:19:06Z_

## TL;DR
- **DeepSeek-V4 & Architecture:** DeepSeek models dominated attention, gaining FlashMLA sparse prefill by default, shared expert fusion for DeepEP/MegaMOE, and non-paged indexers for long-context prefill.
- **Memory & Caching:** Major memory management upgrades landed, including a unified memory pool for hybrid Mamba/SWA models and a tiered DRAM+SSD L3 storage backend (HiCache) for AMD. A massive Radix Cache split is also in progress.
- **Kernels & MoE:** Kernel consolidation is a major theme. Ungrouped and grouped MoE gate/topk were merged onto a single Triton router (beating AOT on Hopper), and a massive refactor is migrating scattered Triton ops into a unified `sglang.kernels` namespace. Work also began on "Paged Experts" to serve MoE models exceeding VRAM.
- **Hardware & Ecosystem:** The engine is rapidly maturing its multi-hardware support (AMD MI355X, Intel XPU, Ascend NPU, Apple MLX) and speculative decoding capabilities (DSpark temperature sampling, DDTree).

## Most important PRs
**[#29678](https://github.com/sgl-project/sglang/pull/29678)** Unified memory pool for hybrid Mamba / SWA models. This major feature enables efficient memory sharing for hybrid architectures, critical for next-gen models.
**[#29771](https://github.com/sgl-project/sglang/pull/29771)** Consolidate ungrouped + grouped gate/topk onto one Triton router. Replaces AOT kernels with a unified Triton implementation that is faster on B200/H100/H200 and achieves parity with FlashInfer.
**[#25377](https://github.com/sgl-project/sglang/pull/25377)** Add UMBP tiered DRAM + SSD L3 storage backend with hugepage host allocator. Brings high-performance HiCache tiered storage to AMD hardware.
**[#29971](https://github.com/sgl-project/sglang/pull/29971)** (Newly opened) Paged Experts: serve MoE models larger than VRAM. Introduces a mechanism to page MoE experts in and out of GPU memory, enabling massive models on limited hardware.
**[#30137](https://github.com/sgl-project/sglang/pull/30137)** Config resolution pipeline full-stack review. The capstone of a massive 10-PR refactor that completely overhauls how model configurations, overrides, and server arguments are resolved and dispatched.

## More changes by area

<details>
<summary>Performance (10)</summary>

- [#30107](https://github.com/sgl-project/sglang/pull/30107) [diffusion] perf: add unified SP shard helpers and zero-copy tail-pad attention
- [#30016](https://github.com/sgl-project/sglang/pull/30016) [diffusion] feat: performance_mode=speed enables torch.compile by default
- [#29970](https://github.com/sgl-project/sglang/pull/29970) perf: add dLLM consumer-sufficient TP vocab state
- [#30086](https://github.com/sgl-project/sglang/pull/30086) [diffusion] perf: tp-shard every text/image encoder across the full DiT replica (any parallelism)
- [#29804](https://github.com/sgl-project/sglang/pull/29804) [Apple Silicon] [MLX] Fuse MoE combine multiply-reduce into one Metal kernel
- [#29921](https://github.com/sgl-project/sglang/pull/29921) perf(triton): avoid per-step D2H .item() sync in cuda-graph loc translate
- [#29825](https://github.com/sgl-project/sglang/pull/29825) perf: use torch.empty for HiCache dummy read buffers to skip a memset
- [#30024](https://github.com/sgl-project/sglang/pull/30024) perf(sgl-kernel): default block_quota=16 for MLA page_first KV gather
- [#29946](https://github.com/sgl-project/sglang/pull/29946) Fix : fall back to NCCL all-reduce for symm-mem during CUDA graph capture
- [#30179](https://github.com/sgl-project/sglang/pull/30179) benchmark: add MI300X speed benchmarks for Qwen3.5-4B cookbook

</details>

<details>
<summary>Kernels & attention (38)</summary>

- [#29365](https://github.com/sgl-project/sglang/pull/29365) [CP] Consolidate decode-context-parallel (DCP) helpers into layers/dcp/
- [#29867](https://github.com/sgl-project/sglang/pull/29867) feat(short-conv): shared ShortConvAttnBackend for ZAYA1 CCA + LFM2 short conv
- [#29053](https://github.com/sgl-project/sglang/pull/29053) [XPU] Enable XPU graph support (decode full-graph + prefill tc_piecewise)
- [#29843](https://github.com/sgl-project/sglang/pull/29843) [trtllm_mha] Fuse cuda-graph metadata rebuild into one triton kernel
- [#29619](https://github.com/sgl-project/sglang/pull/29619) [DeepSeek-V4] Add an opt-in non-paged indexer for long-context prefill
- [#29472](https://github.com/sgl-project/sglang/pull/29472) [KDA] Add FlashKDA prefill backend for safe-gate KDA linear attention
- [#29779](https://github.com/sgl-project/sglang/pull/29779) Share one logits output buffer across prefill/decode/draft cuda-graph runners
- [#29885](https://github.com/sgl-project/sglang/pull/29885) [DeepSeek V4] Cover both dense and sparse prefill paths in the compress attention unittest
- [#29945](https://github.com/sgl-project/sglang/pull/29945) Move deferred mamba cow and clear
- [#29161](https://github.com/sgl-project/sglang/pull/29161) [Fix]: Defer DSA MLA CP KV gather for fp8 trtllm prefill in PD mode
- [#29551](https://github.com/sgl-project/sglang/pull/29551) sgl-kernel: bump sgl-attn for varlen num_splits OOM fix
- [#29901](https://github.com/sgl-project/sglang/pull/29901) [RFC] Radix Cache Split
- [#29847](https://github.com/sgl-project/sglang/pull/29847) [Feature] Add DSA CP shared KV cache
- [#30156](https://github.com/sgl-project/sglang/pull/30156) [MLX] Split radix KV pool by attention layer type for sliding-window models
- [#30044](https://github.com/sgl-project/sglang/pull/30044) [Kernel] Introduce sglang.kernels namespace and migrate scattered triton_ops kernels (RFC #29630, Phase 2)
- [#29997](https://github.com/sgl-project/sglang/pull/29997) [MoE] Retire the AOT moe_fused_gate / kimi_k2_moe_fused_gate gate kernels (#26771)
- [#29839](https://github.com/sgl-project/sglang/pull/29839) feat: integrate hpc-ops attention and MoE backends
- [#30091](https://github.com/sgl-project/sglang/pull/30091) [MLX] Windowed per-request KV cache for sliding-window layers
- [#30117](https://github.com/sgl-project/sglang/pull/30117) Support BF16 GEMM JIT kernel
- [#30113](https://github.com/sgl-project/sglang/pull/30113) [KDA] Add FlashInfer SM100 KDA decode + MTP (target_verify) backend
- [#30169](https://github.com/sgl-project/sglang/pull/30169) [GDN/KDA] Fuse SM100 CuteDSL prefill state I/O into the chunk h kernel
- [#29985](https://github.com/sgl-project/sglang/pull/29985) [Do Not Merge][BCG][2/N] Enable DSV4 prefill BCG: two-pass capture + DSV4-aware mem reserve
- [#29826](https://github.com/sgl-project/sglang/pull/29826) [Feature] Add DPSK V4 multi-head tiled FlashMLA sparse decode kernel
- [#29930](https://github.com/sgl-project/sglang/pull/29930) Feat(CP LayerSplit): layer-split prefill KV cache across CP ranks (L2/L3 HiCache, PD prefill)
- [#30090](https://github.com/sgl-project/sglang/pull/30090) [diffusion] Add dynamic cuDNN SDPA attention backend
- [#30123](https://github.com/sgl-project/sglang/pull/30123) [rope] Fix OOB cos/sin loads in fused MRoPE triton kernel for interleaved + partial rotary
- [#30089](https://github.com/sgl-project/sglang/pull/30089) [SRT] Add dynamic cuDNN SDPA for vision attention
- [#30140](https://github.com/sgl-project/sglang/pull/30140) [DeepSeek-V4] Enable non-paged indexer by default for large prefill chunks
- [#29865](https://github.com/sgl-project/sglang/pull/29865) Support alternative BF16 GEMM
- [#29858](https://github.com/sgl-project/sglang/pull/29858) Build SWA window kv buffers for the EAGLE draft-extend cuda-graph path
- [#30144](https://github.com/sgl-project/sglang/pull/30144) [XPU] Enable fused GDN QKV split Triton kernel on XPU
- [#29973](https://github.com/sgl-project/sglang/pull/29973) [FIX] Prevent Lightning Attention extra-buffer mamba state corruption
- [#29787](https://github.com/sgl-project/sglang/pull/29787) [Spec] Anchor GLM-5.2 MTP IndexShare topk on the draft-extend step
- [#29786](https://github.com/sgl-project/sglang/pull/29786) [NPU] Support chunked prefill for DeepSeek-V4
- [#30012](https://github.com/sgl-project/sglang/pull/30012) [DSv4] Use BF16 instead of FP32 for indexer score computation
- [#29959](https://github.com/sgl-project/sglang/pull/29959) [DSA][GLM5.2] Index Share for MHA
- [#27914](https://github.com/sgl-project/sglang/pull/27914) [Intel GPU] DeepSeek V4 6/N: use sgl-kernel implemetation of flash_mla_with_kvcache on XPU
- [#29775](https://github.com/sgl-project/sglang/pull/29775) [DeepSeek V4] Enable FlashMLA sparse prefill by default

</details>

<details>
<summary>MoE & quantization (17)</summary>

- [#29937](https://github.com/sgl-project/sglang/pull/29937) [NPU] [DOC] add missing DEEP_NORMAL_MODE_USE_INT8_QUANT for w8a8+deepep scenarios
- [#27349](https://github.com/sgl-project/sglang/pull/27349) Support DSV4 shared expert fusion for DeepEP and MegaMOE
- [#29659](https://github.com/sgl-project/sglang/pull/29659) [LFM2-MoE] Support Transformers v5 packed MoE expert weights
- [#29992](https://github.com/sgl-project/sglang/pull/29992) FlashInfer Backend for MXFP8 Grouped Quantization
- [#29848](https://github.com/sgl-project/sglang/pull/29848) Experiment: materialize MoE weights before copy
- [#29983](https://github.com/sgl-project/sglang/pull/29983) Auto-select MoE runner backend for DeepSeek V4 FP4 experts
- [#29761](https://github.com/sgl-project/sglang/pull/29761) [Bugfix] compressed-tensors WNA16 MoE: don't assume a "Linear" config group
- [#26255](https://github.com/sgl-project/sglang/pull/26255) [fix] Add support for flashinfer MOE A2A to Qwen3 BF16 model path
- [#29855](https://github.com/sgl-project/sglang/pull/29855) [AMD][DI][CI] 3/N Add Kimi K2.6 FP8 MI355X 1P1D nightly recipes
- [#29988](https://github.com/sgl-project/sglang/pull/29988) [dsv4] Trigger MHC prenorm prewarm at weight-load time with rank sync
- [#29956](https://github.com/sgl-project/sglang/pull/29956) Fix UE8M0 scale rounding for DeepGEMM
- [#29694](https://github.com/sgl-project/sglang/pull/29694) [AMD] Fix int8 per-token quant Triton portability + register test for AMD nightly CI
- [#29856](https://github.com/sgl-project/sglang/pull/29856) Fix BF16 routing bias dtype for TRT-LLM MoE
- [#29931](https://github.com/sgl-project/sglang/pull/29931) Fix NVFP4 Marlin MoE Backend routed scaling on Hopper
- [#29797](https://github.com/sgl-project/sglang/pull/29797) fix: drop stale mxfp4 marlin scales after repack
- [#30029](https://github.com/sgl-project/sglang/pull/30029) Fix kv_b_proj channel scale broadcast when reshape hasn't run yet
- [#29981](https://github.com/sgl-project/sglang/pull/29981) [BCG][1/N] Route RMSNorm to fp32 forward_native under breakable prefill

</details>

<details>
<summary>Model support (25)</summary>

- [#30040](https://github.com/sgl-project/sglang/pull/30040) [diffusion] feat: add LingBot realtime prompt, KV window, and lazy VAE controls
- [#29708](https://github.com/sgl-project/sglang/pull/29708) [KDA-Pilot] Add LTX2 QKNorm split-RoPE CUDA fast path
- [#29631](https://github.com/sgl-project/sglang/pull/29631) [diffusion][cache-dit] add cache-dit support for Ideogram 4
- [#23049](https://github.com/sgl-project/sglang/pull/23049) [Diffusion] Diffusion model support log-requests
- [#29667](https://github.com/sgl-project/sglang/pull/29667) Add fused EH norm for DeepSeek NextN
- [#29446](https://github.com/sgl-project/sglang/pull/29446) Add Laguna XS.2.1 DFlash support to SGLang
- [#29932](https://github.com/sgl-project/sglang/pull/29932) add mimo-v2-flash model tutorial
- [#29905](https://github.com/sgl-project/sglang/pull/29905) docs: add Qwen3.6-27B-NVFP4 variant to cookbook
- [#29544](https://github.com/sgl-project/sglang/pull/29544) docs: add PD disaggregation to GLM-5.2 cookbook playground
- [#29645](https://github.com/sgl-project/sglang/pull/29645) Support real draft tokens to simulated acceptance
- [#29788](https://github.com/sgl-project/sglang/pull/29788) [minimax m3] npu adaptor
- [#30115](https://github.com/sgl-project/sglang/pull/30115) [Model] Support RWKV-7 (Goose)
- [#29972](https://github.com/sgl-project/sglang/pull/29972) Add MiMo V2.5 zigzag CP-v2 support
- [#30175](https://github.com/sgl-project/sglang/pull/30175) [Fix] Populate n-gram embedding token table in PD-disaggregation event loops (LongCat-2.0)
- [#30042](https://github.com/sgl-project/sglang/pull/30042) support LongCat2.0
- [#29850](https://github.com/sgl-project/sglang/pull/29850) Support MOSS-Transcribe-Diarize model and adapter
- [#30050](https://github.com/sgl-project/sglang/pull/30050) [MLX] Support gpt-oss: sliding-window attention, attention sinks, sm_scale
- [#30171](https://github.com/sgl-project/sglang/pull/30171) [diffusion] Fuse Wan VAE RMSNorm SiLU
- [#30170](https://github.com/sgl-project/sglang/pull/30170) [diffusion] Fuse ERNIE AdaLN residual path
- [#30161](https://github.com/sgl-project/sglang/pull/30161) [Gemma4] Support per-request max_soft_tokens (image resolution) via images_config and mm_processor_kwargs
- [#29892](https://github.com/sgl-project/sglang/pull/29892) Support GLM-5.2 moe router use FP32
- [#30056](https://github.com/sgl-project/sglang/pull/30056) model(lfm2): implement get_hidden_dim to enable LoRA on out_proj/in_proj
- [#30183](https://github.com/sgl-project/sglang/pull/30183) Support LongCat Flash n-gram embedding config aliases
- [#30150](https://github.com/sgl-project/sglang/pull/30150) [diffusion][cache-dit] add dual-transformer Cache-DiT adapter specs
- [#29963](https://github.com/sgl-project/sglang/pull/29963) Add B200 NVFP4 MTP deployment to DeepSeek-R1 cookbook recipe

</details>

<details>
<summary>Parallelism & scheduling (35)</summary>

- [#28612](https://github.com/sgl-project/sglang/pull/28612) Optimize C128 state pool allocation using request state pool
- [#29784](https://github.com/sgl-project/sglang/pull/29784) [AMD][DI][CI] 2/N Add DSV4 DP8/EP8 and MTP MI355X 1P1D nightly recipes
- [#28287](https://github.com/sgl-project/sglang/pull/28287) [HiCache] Optimize HiCache hash generation with bulk token byte conversion
- [#29621](https://github.com/sgl-project/sglang/pull/29621) Extract reusable VMM shareable-handle helpers from register_graph_inputs
- [#29595](https://github.com/sgl-project/sglang/pull/29595) [Spec] Enable FlashInfer autotune for spec draft
- [#29842](https://github.com/sgl-project/sglang/pull/29842) pad customized_info for mixed output batches
- [#29817](https://github.com/sgl-project/sglang/pull/29817) [HiCache] write_back policy refinement
- [#29354](https://github.com/sgl-project/sglang/pull/29354) [bug6] clear stale mamba cow source on rematch
- [#29881](https://github.com/sgl-project/sglang/pull/29881) Avoid logits multimem all-gather on cross-node TP groups
- [#30164](https://github.com/sgl-project/sglang/pull/30164) [1/N] elastic-ep: Add runtime EP scale-up
- [#29907](https://github.com/sgl-project/sglang/pull/29907) Add DDTree speculative decoding
- [#30004](https://github.com/sgl-project/sglang/pull/30004) [diffusion] feat: per-layer TP shard planner for DiT linears (--dit-tp-plan)
- [#30052](https://github.com/sgl-project/sglang/pull/30052) [AMD][DI][CI] 4/N Add mooncake KV-transfer legs to MI355X disaggregation nightly
- [#30157](https://github.com/sgl-project/sglang/pull/30157) Size KV pool after CUDA graph capture (opt-in)
- [#29879](https://github.com/sgl-project/sglang/pull/29879) Add forward-pass decode interference metrics
- [#29968](https://github.com/sgl-project/sglang/pull/29968) [Spec][5/N] Decoupled speculative decoding: role validation + dispatch
- [#30036](https://github.com/sgl-project/sglang/pull/30036) [diffusion] Support RL rollout for the Wan pipeline via a per-request scheduler switch
- [#30095](https://github.com/sgl-project/sglang/pull/30095) [PP] Carry TP-sharded flag in proxy-tensor metadata to fix #30015
- [#30058](https://github.com/sgl-project/sglang/pull/30058) [PP] Add all_gather_exclude to send/recv_tensor_dict for TP-sharded tensors
- [#29868](https://github.com/sgl-project/sglang/pull/29868) [Spec][4/N] Decoupled speculative decoding: ignore_decode_budget for the drafter engine
- [#29898](https://github.com/sgl-project/sglang/pull/29898) Fix PrefillDelayer deadlock: bound the "all"-branch delay by max_delay_passes
- [#30060](https://github.com/sgl-project/sglang/pull/30060) Avoid blocking scheduler on health check send
- [#29859](https://github.com/sgl-project/sglang/pull/29859) [HiCache] Unified Mooncake Registration for Logical Anchors and Draft Pools
- [#29923](https://github.com/sgl-project/sglang/pull/29923) Emit HiCache L3 KV events
- [#29948](https://github.com/sgl-project/sglang/pull/29948) [HiCache] Emit KV cache events for completed L3 storage backups
- [#30096](https://github.com/sgl-project/sglang/pull/30096) [DFLASH] Support grammar-constrained decoding in speculative verify
- [#29917](https://github.com/sgl-project/sglang/pull/29917) [Spec] Add DSpark speculative decoding for Qwen3
- [#29938](https://github.com/sgl-project/sglang/pull/29938) [Spec]Support Temperature Sampling（target-only and rejection sampling）for DSpark
- [#30026](https://github.com/sgl-project/sglang/pull/30026) Add deterministic inference for eagle parity test
- [#30027](https://github.com/sgl-project/sglang/pull/30027) Avoid blocking EAGLE grammar mask uploads
- [#29211](https://github.com/sgl-project/sglang/pull/29211) [disagg] Fix KV-event publisher port collision under pure data parallelism
- [#29860](https://github.com/sgl-project/sglang/pull/29860) Fix SWA eviction tombstoning the last leaf
- [#30139](https://github.com/sgl-project/sglang/pull/30139) [Fix] Skip cross-node probe in MultimemAllGatherer on single-node runs (fixes mooncake EP segfault)
- [#29834](https://github.com/sgl-project/sglang/pull/29834) Fix scheduler crash on prefill-unreachable decode abort
- [#30031](https://github.com/sgl-project/sglang/pull/30031) Fix stale decode offload state on host allocation failure

</details>

<details>
<summary>Hardware & arch (47)</summary>

- [#29807](https://github.com/sgl-project/sglang/pull/29807) Add XPU CI job monitor workflow
- [#29447](https://github.com/sgl-project/sglang/pull/29447) [CI] Add per-stage NVIDIA model inventory tool
- [#29791](https://github.com/sgl-project/sglang/pull/29791) [diffusion] Add 5090 diffusion consumer GPU guard
- [#23180](https://github.com/sgl-project/sglang/pull/23180) Speculative decoding support on XPU
- [#28908](https://github.com/sgl-project/sglang/pull/28908) [Intel XPU] Initially add nightly GSM8K accuracy tests for Llama-3.1-8B (TP=2) and Qwen3-32B (TP=4)
- [#29497](https://github.com/sgl-project/sglang/pull/29497) [CPU] Fix model failures on Xeon
- [#29458](https://github.com/sgl-project/sglang/pull/29458) Enable Breakable Cuda Graph as Default
- [#29691](https://github.com/sgl-project/sglang/pull/29691) [Apple Silicon] [CI] Add model-free unit-test workflow on macos-26
- [#29217](https://github.com/sgl-project/sglang/pull/29217) [MLX] Fix step-bounded profiling for bench tools on Apple Silicon
- [#29822](https://github.com/sgl-project/sglang/pull/29822) [AMD] Accept ROCm tensors in JIT kernel TensorMatcher + register 4 kernel tests
- [#29409](https://github.com/sgl-project/sglang/pull/29409) [AMD] Split qwen3.5 triton DCP test into its own nightly job
- [#29503](https://github.com/sgl-project/sglang/pull/29503) NPU case rl update weights for tensor load_format == None and flatten bucket
- [#29680](https://github.com/sgl-project/sglang/pull/29680) [AMD] Register 2 CPU/ROCm-safe tests for AMD 1-GPU PR CI
- [#29908](https://github.com/sgl-project/sglang/pull/29908) [Apple Silicon] Add labeler config
- [#29726](https://github.com/sgl-project/sglang/pull/29726) [AMD] Rebalance stage-c-large-8-gpu-mi35x partitions to fix 60-min timeout
- [#29782](https://github.com/sgl-project/sglang/pull/29782) [AMD] Register 3 unit mem_cache + utils tests for stage-b-test-1-gpu-small-amd
- [#29681](https://github.com/sgl-project/sglang/pull/29681) fix(mlx): default prefill_aware_swa=False on MlxModelRunnerStub
- [#29999](https://github.com/sgl-project/sglang/pull/29999) [NPU] bugfix for Base class add mamba_track_indices parameter
- [#27915](https://github.com/sgl-project/sglang/pull/27915) [Intel GPU] DeepSeek V4 7/N: Support fused_rope_inplace on XPU using triton
- [#30014](https://github.com/sgl-project/sglang/pull/30014) [AMD] Temporarily disabled: every-6-hours rocm 7.2 test
- [#29799](https://github.com/sgl-project/sglang/pull/29799) support rust sglang server
- [#30163](https://github.com/sgl-project/sglang/pull/30163) [Apple Silicon] Add a custom Metal RMSNorm kernel
- [#29949](https://github.com/sgl-project/sglang/pull/29949) [Apple Silicon][MPS] Cap memory reporting to Metal's recommended working set
- [#29935](https://github.com/sgl-project/sglang/pull/29935) [Feature][Intel XPU] Add memory saver support for Intel XPU via upstream torch_memory_saver
- [#30116](https://github.com/sgl-project/sglang/pull/30116) fix: Guard cuda_runtime.h includes with USE_ROCM for HIP/ROCm compatibility
- [#29832](https://github.com/sgl-project/sglang/pull/29832) [AMD] Enable mamba extra_buffer on ROCm + shared-prefix donate correctness test
- [#29895](https://github.com/sgl-project/sglang/pull/29895) [Platform] Route OOT available-memory queries through current_platform
- [#30143](https://github.com/sgl-project/sglang/pull/30143) [qwen3.5][XPU] Enable alt_stream for Qwen3.5 on XPU
- [#30003](https://github.com/sgl-project/sglang/pull/30003) Experiment: AMD DSV4 CPU affinity and NUMA diagnostics
- [#30121](https://github.com/sgl-project/sglang/pull/30121) [Apple Silicon] [CI] Move the MLX lane to the check-changes + pr-gate composite
- [#30008](https://github.com/sgl-project/sglang/pull/30008) [AMD] WIP - Set REQUEST_TIMEOUT=30 for AMD to deflake multimodal tests
- [#30048](https://github.com/sgl-project/sglang/pull/30048) [XPU] Unbreak stage-b: re-add --disable-decode-cuda-graph, quarantine EAGLE3 parity
- [#30087](https://github.com/sgl-project/sglang/pull/30087) [NPU] ascend support decode radix cache
- [#29800](https://github.com/sgl-project/sglang/pull/29800) feat(scripts): prefill CUDA graph + deterministic MTP for AMD MI355X — decode +15-20%, HumanEval +10%
- [#30097](https://github.com/sgl-project/sglang/pull/30097) [MLX] Size the attention KV pool at the compute dtype for quantized models
- [#27835](https://github.com/sgl-project/sglang/pull/27835) [bugfix][AMD] Disable aiter allreduce+RMSNorm fusion under DP attention / EP
- [#28787](https://github.com/sgl-project/sglang/pull/28787) [AMD] Fix RMSNorm batch-invariance on ROCm under deterministic inference
- [#29918](https://github.com/sgl-project/sglang/pull/29918) [AMD] Gate broken CK block-FP8 GEMM shapes to aiter-triton-GEMM to fix ROCm 7.0 Qwen3.5 accuracy
- [#29829](https://github.com/sgl-project/sglang/pull/29829) [NPU] Fix block_table batch size mismatch in GLM-4.7-Flash DeepEP + MTP without CUDA Graphs
- [#29166](https://github.com/sgl-project/sglang/pull/29166) [Fix]: Inline H2D during CUDA graph capture to avoid stream isolation in Offloader
- [#29756](https://github.com/sgl-project/sglang/pull/29756) [AMD] Fix MiniMax M3 state transfer in Mori PD
- [#29381](https://github.com/sgl-project/sglang/pull/29381) [NPU] Fix glm 4.6v
- [#30001](https://github.com/sgl-project/sglang/pull/30001) [NPU] bugfix for dsv4 memory pool
- [#29853](https://github.com/sgl-project/sglang/pull/29853) bugfix for npu Grok2 model --detokenizer without all special ids
- [#29672](https://github.com/sgl-project/sglang/pull/29672) [amd][diffusion] Fix causal Conv3D cat/pad fusion crashes for wan2.2 t2v
- [#30017](https://github.com/sgl-project/sglang/pull/30017) [MPS] Fix diffusion output stability
- [#29876](https://github.com/sgl-project/sglang/pull/29876) [AMD] Fix EAGLE speculative decoding with DSA backend on gfx950 (MI355X)

</details>

<details>
<summary>API & serving (16)</summary>

- [#29915](https://github.com/sgl-project/sglang/pull/29915) [router] Log every engine /abort_request with a router_reason label + Prom counter
- [#29684](https://github.com/sgl-project/sglang/pull/29684) [passthrough] engine: zstd request-body decompression + header overrides
- [#29920](https://github.com/sgl-project/sglang/pull/29920) feat(parser): resolve special-token suffix at runtime for compatibility
- [#29810](https://github.com/sgl-project/sglang/pull/29810) [Feature] Add OpenAI-compatible tokenize endpoints
- [#30023](https://github.com/sgl-project/sglang/pull/30023) [tracing] sglang tracing v2: support exporting tracing data asynchronously
- [#30177](https://github.com/sgl-project/sglang/pull/30177) Support returning the last hidden state
- [#30046](https://github.com/sgl-project/sglang/pull/30046) [router] Add --worker-api-key for introspection and KV-event discovery against api-key workers
- [#30141](https://github.com/sgl-project/sglang/pull/30141) [Feature] Add --config-format alias for --model-config-parser (Mistral vLLM parity, part 1 of #28020)
- [#30043](https://github.com/sgl-project/sglang/pull/30043) [Anthropic] Default thinking off when the thinking field is absent
- [#29703](https://github.com/sgl-project/sglang/pull/29703) [Anthropic] Fix missing cache_read_input_tokens in streaming responses
- [#29882](https://github.com/sgl-project/sglang/pull/29882) fix: populate batch req rids and per-request http_worker_ipc for mult…
- [#29818](https://github.com/sgl-project/sglang/pull/29818) Fix http connections gauge leak
- [#29820](https://github.com/sgl-project/sglang/pull/29820) fix(openai): return 400 for negative token ids in /v1/detokenize
- [#29894](https://github.com/sgl-project/sglang/pull/29894) Fix /server_info 500 error when load_format is set to a custom loader class
- [#29947](https://github.com/sgl-project/sglang/pull/29947) fix(kimik2): stop end-marker straddle leaking into streamed tool args
- [#29975](https://github.com/sgl-project/sglang/pull/29975) fix(function_call): skip non-object JSON entries in parse_base_json

</details>

<details>
<summary>Refactors (25)</summary>

- [#30151](https://github.com/sgl-project/sglang/pull/30151) [refactor] Reorder ServerArgs sections common-first; inline LLAMA4/MIMO_V2 arch tuples
- [#30073](https://github.com/sgl-project/sglang/pull/30073) [refactor] Migrate the attention_backend resolution chain (stack 11/15)
- [#30076](https://github.com/sgl-project/sglang/pull/30076) [refactor] Migrate the DeepSeek family and the parallel-request chains (stack 14/15)
- [#30075](https://github.com/sgl-project/sglang/pull/30075) [refactor] Migrate the moe_runner_backend / quantization resolution chains (stack 13/15)
- [#30074](https://github.com/sgl-project/sglang/pull/30074) [refactor] Migrate the page_size resolution chain (stack 12/15)
- [#29852](https://github.com/sgl-project/sglang/pull/29852) [diffusion] refactor: refactor cuda attention backend resolver
- [#30067](https://github.com/sgl-project/sglang/pull/30067) [refactor] Add the declarative model-override registry and resolution gate (stack 5/15)
- [#29770](https://github.com/sgl-project/sglang/pull/29770) chore: cleanup garbage code
- [#30066](https://github.com/sgl-project/sglang/pull/30066) [refactor] Add the resolved-flags tier + resolvable-field metadata (stack 4/15)
- [#30118](https://github.com/sgl-project/sglang/pull/30118) [diffusion] Refactor diffusion weight load planning
- [#30072](https://github.com/sgl-project/sglang/pull/30072) [refactor] Add the post-process resolution stage; migrate sampling_backend (stack 10/15)
- [#30069](https://github.com/sgl-project/sglang/pull/30069) [refactor] Migrate the first override families: Mistral/Pixtral dtype, MiniMaxM2, MiMoV2 (stack 7/15)
- [#30070](https://github.com/sgl-project/sglang/pull/30070) [refactor] Add predicate-keyed registration; migrate the Step3p family (stack 8/15)
- [#30071](https://github.com/sgl-project/sglang/pull/30071) [refactor] Sweep disable_hybrid_swa_memory writers; close the dtype family (stack 9/15)
- [#30064](https://github.com/sgl-project/sglang/pull/30064) [refactor] Move ServerArgs ownership into the runtime context (stack 2/15)
- [#30068](https://github.com/sgl-project/sglang/pull/30068) [refactor] Wire the config resolution pipeline (dispatch, stash, dual-apply, publish) (stack 6/15)
- [#30065](https://github.com/sgl-project/sglang/pull/30065) [refactor] Soft-deprecate the legacy global ServerArgs accessors + ratchet (stack 3/15)
- [#30077](https://github.com/sgl-project/sglang/pull/30077) [refactor] Rename Arg.model_overridable to Arg.resolvable (stack 15/15)
- [#30063](https://github.com/sgl-project/sglang/pull/30063) [refactor] Add a read-through server_args accessor to RuntimeContext (stack 1/15)
- [#30180](https://github.com/sgl-project/sglang/pull/30180) Cleanup: relocate temp_set_env and consolidate multi-device/CUDA helpers in common.py
- [#30103](https://github.com/sgl-project/sglang/pull/30103) [diffusion] Defer VAE offload cleanup after response
- [#30005](https://github.com/sgl-project/sglang/pull/30005) refactor: make time_stats msgpack-native
- [#29952](https://github.com/sgl-project/sglang/pull/29952) refactor: make customized_info msgpack-native (drop PickleWrapper)
- [#30114](https://github.com/sgl-project/sglang/pull/30114) [refactor] Rename chunked_req_to_exclude to reqs_to_exclude
- [#29969](https://github.com/sgl-project/sglang/pull/29969) fix(nixl): prevent read-during-write via atomic temp file rename

</details>

<details>
<summary>Tests, CI & build (16)</summary>

- [#29884](https://github.com/sgl-project/sglang/pull/29884) [Doc] Cookbook: Laguna-XS-2.1 (DFlash low-latency + high-throughput)
- [#29831](https://github.com/sgl-project/sglang/pull/29831) [diffusion] Prefer official diffusion consistency GT
- [#29636](https://github.com/sgl-project/sglang/pull/29636) [Kernel] Strengthen kernel shape coverage
- [#29824](https://github.com/sgl-project/sglang/pull/29824) [diffusion] CI: tighten multimodal-gen consistency thresholds
- [#29290](https://github.com/sgl-project/sglang/pull/29290) [AMD] Cover DeepSeek-R1 MXFP4 TP4 MTP nightly CI
- [#29872](https://github.com/sgl-project/sglang/pull/29872) [sglang-miles] Cherry-pick #28371: [LoRA] Fix chunked SGMV (csgmv) CUDA graph segment replay
- [#29789](https://github.com/sgl-project/sglang/pull/29789) chore: clean diffusion dead code
- [#27704](https://github.com/sgl-project/sglang/pull/27704) [Diffusion] Add profiling support and fix VBench dataset handling in bench_offline_throughput
- [#29554](https://github.com/sgl-project/sglang/pull/29554) Upgrading tvm-ffi/sgl-deep-gemm/tilelang
- [#28190](https://github.com/sgl-project/sglang/pull/28190) fix(precision): do not promote failed runs to the comparison baseline
- [#29844](https://github.com/sgl-project/sglang/pull/29844) [CI] Revert ModelOpt NVFP4 threshold relax
- [#29926](https://github.com/sgl-project/sglang/pull/29926) Fix Diffusion GT generation pipelines
- [#29986](https://github.com/sgl-project/sglang/pull/29986) [AMD]: hot-patch transformers dynamic_module_utils symlink bug
- [#27730](https://github.com/sgl-project/sglang/pull/27730) [AMD]: docker(rocm) bump Mooncake to latest main + enable multi-protocol
- [#29816](https://github.com/sgl-project/sglang/pull/29816) [AMD] Update ROCm AITER pin to 9127c94
- plus 24 more minor CI and test updates

</details>

<details>
<summary>Docs (15)</summary>

- [#29828](https://github.com/sgl-project/sglang/pull/29828) glm5.2 on ascend doc (new version)
- [#29911](https://github.com/sgl-project/sglang/pull/29911) [XPU] Remove redundant xpu graph backend and make xpu graph opt-in by default
- [#29871](https://github.com/sgl-project/sglang/pull/29871) [chore] Add no-getattr rule; refine no-dataclasses rule
- [#29793](https://github.com/sgl-project/sglang/pull/29793) [NPU]Modify --lora-backend & --moe-runner-backend description.
- [#30011](https://github.com/sgl-project/sglang/pull/30011) [DOC] [NPU] update supported features on ascend npu
- [#30149](https://github.com/sgl-project/sglang/pull/30149) [chore] Remove the stack-review placeholder file
- [#29827](https://github.com/sgl-project/sglang/pull/29827) [Doc] Tiny update dsv4 doc
- [#30109](https://github.com/sgl-project/sglang/pull/30109) docs: simplify diffusion new model guide
- [#29991](https://github.com/sgl-project/sglang/pull/29991) [docs] Multi-node deployment: add PD disaggregation and Apptainer examples for SLURM
- [#29854](https://github.com/sgl-project/sglang/pull/29854) docs: complete production metrics reference
- [#30028](https://github.com/sgl-project/sglang/pull/30028) Warn when Dumper may capture CUDA graph outputs
- [#29944](https://github.com/sgl-project/sglang/pull/29944) docs: document S3-compatible endpoints with Tigris example
- [#29886](https://github.com/sgl-project/sglang/pull/29886) [Doc]Standardize the names of PyTorch NPU-related software throughout the documentation
- [#29941](https://github.com/sgl-project/sglang/pull/29941) docs: Added pending support warning for DiffusionGemma Cookbook
- [#29953](https://github.com/sgl-project/sglang/pull/29953) docs: fix README news date

</details>

<details>
<summary>Bugfixes (47)</summary>

- [#30110](https://github.com/sgl-project/sglang/pull/30110) [diffusion] fix: shut down diffusion workers on serve exit
- [#29271](https://github.com/sgl-project/sglang/pull/29271) fix: make write_token dynamic
- [#30111](https://github.com/sgl-project/sglang/pull/30111) [Fix] Fix DSA indexer fusion for NeoX RoPE
- [#28676](https://github.com/sgl-project/sglang/pull/28676) [RL] fix deepseek v4 MXFP8 flashinfer_trtllm_routed MoE weight update
- [#27923](https://github.com/sgl-project/sglang/pull/27923) Fix MambaPool.clear_slots OOM by replacing expand-based tensor allocation with scalar zeroing
- [#29943](https://github.com/sgl-project/sglang/pull/29943) Fix shared logits buffer for reduced-vocab draft models
- [#30039](https://github.com/sgl-project/sglang/pull/30039) [diffusion] CI: fix AMD diffusion CI import
- [#29866](https://github.com/sgl-project/sglang/pull/29866) Fix capture-mode detection during breakable CUDA graph capture
- [#30079](https://github.com/sgl-project/sglang/pull/30079) [MoE] Fix moe_fused_gate out-of-range expert id on all-NaN rows (fixes eagle_dp_attention crash)
- [#30053](https://github.com/sgl-project/sglang/pull/30053) [BugFix] Release HiCache prefetch resources on disagg-prefill bootstrap-queue abort
- [#29977](https://github.com/sgl-project/sglang/pull/29977) `session_id` dataclass field should not put in msgpack struct
- [#30154](https://github.com/sgl-project/sglang/pull/30154) [fix] Reconcile the legacy-getter ratchet baseline after racing merges
- [#29823](https://github.com/sgl-project/sglang/pull/29823) [HiCache]fix draft host pool allocator type
- [#29978](https://github.com/sgl-project/sglang/pull/29978) [PD] Fix permanent transfer hang on lost staging control messages (mooncake/NIXL staging)
- [#30181](https://github.com/sgl-project/sglang/pull/30181) [MLX] Fix single-token chunked-prefill continuation misrouted as decode
- [#29888](https://github.com/sgl-project/sglang/pull/29888) [Bugfix] NVILA: fix video request crash from stale .asnumpy()
- [#30124](https://github.com/sgl-project/sglang/pull/30124) Fix LoRA prefix reuse with decode CUDA graph
- [#30108](https://github.com/sgl-project/sglang/pull/30108) [Fix] Torch-allocate dsv4 compress-plan out-params for stream-ordered lifetime
- [#30022](https://github.com/sgl-project/sglang/pull/30022) fix: serialize FanOutCommunicator queueing calls with a lock
- [#30078](https://github.com/sgl-project/sglang/pull/30078) Fix ModelOpt mixed-precision NVFP4 routing
- [#30167](https://github.com/sgl-project/sglang/pull/30167) Fix MiMo-V2 on Blackwell: FA3 fallback and auto-select attention backend
- [#30104](https://github.com/sgl-project/sglang/pull/30104) [Bugfix] integer overflow in top-k sampling
- [#29883](https://github.com/sgl-project/sglang/pull/29883) [BUG] fix strip streaming empty-string suffix from DSV4 tool arguments
- [#29896](https://github.com/sgl-project/sglang/pull/29896) fix(config): derive scaling in the KimiVL, MiniCPM3, and DeepseekVL2 MLA branches
- [#29916](https://github.com/sgl-project/sglang/pull/29916) Fix stale _attn_sink_local cache after RL weight updates
- [#29984](https://github.com/sgl-project/sglang/pull/29984) Fix race on shared ZMQ sockets in mooncake KV manager senders
- [#29813](https://github.com/sgl-project/sglang/pull/29813) [sgl-model-gateway] fix tokenizer load blocking /health on tokio worker thread
- [#30119](https://github.com/sgl-project/sglang/pull/30119) Fix DFlash draft model crash with modelopt_mixed quantization
- [#29936](https://github.com/sgl-project/sglang/pull/29936) fix(nvila): remap vision_tower.vision_model.* weights for flattened SiglipVisionModel
- [#29909](https://github.com/sgl-project/sglang/pull/29909) [Debug][NPU] Fix Hunyuan3 model where MoE's routing_scaling_ratio is missing on NPU
- [#29996](https://github.com/sgl-project/sglang/pull/29996) Fix device mismatch when mixing JPEG (GPU-decoded) and other type (CP…
- [#29890](https://github.com/sgl-project/sglang/pull/29890) fix(config): treat v_head_dim=0 as unset when deriving model shapes (deepseek-vl2-tiny warmup crash)
- [#29989](https://github.com/sgl-project/sglang/pull/29989) [diffusion] fix: slice img_shapes per-sample in rollout response extractor
- [#30006](https://github.com/sgl-project/sglang/pull/30006) Fix prefill CUDA graph disabled for deeply-nested multimodal models
- [#30034](https://github.com/sgl-project/sglang/pull/30034) Fix HIP import for 5090 diffusion canary
- [#29933](https://github.com/sgl-project/sglang/pull/29933) fix(eval): extract GSM8K answer from first #### marker, not last number
- [#30030](https://github.com/sgl-project/sglang/pull/30030) Fix DP sync DSV4 SWA cache loc sizing
- [#29940](https://github.com/sgl-project/sglang/pull/29940) Fix conv_state_indices handling and add mamba_track_indices parameter
- [#30102](https://github.com/sgl-project/sglang/pull/30102) Fix/pdmux merge batch stream sync
- [#30125](https://github.com/sgl-project/sglang/pull/30125) [MLX] Fix FakeOverlapScheduler test stub broken by forward_ct accounting
- [#29887](https://github.com/sgl-project/sglang/pull/29887) fix bugs with pp in get kv_buffer_shape
- [#29961](https://github.com/sgl-project/sglang/pull/29961) Fix PDMux prefill commit stream dependency
- [#30094](https://github.com/sgl-project/sglang/pull/30094) fix(multiplex): use ParallelState fields in pdmux mixin
- [#29934](https://github.com/sgl-project/sglang/pull/29934) Fix event-loop-blocking `requests.get` in `remote_instance_transfer_engine_info`
- [#29795](https://github.com/sgl-project/sglang/pull/29795) fix(sampling): health check sample cant affect batch sample info
- [#30038](https://github.com/sgl-project/sglang/pull/30038) Fix duplicate FPM binding across attention CP ranks
- [#29830](https://github.com/sgl-project/sglang/pull/29830) [core/loader] Fix presharded cache-key gaps: moe_dense_tp_size, EPLB with structural signature

</details>

<details>
<summary>Other (18)</summary>

- [#29995](https://github.com/sgl-project/sglang/pull/29995) [Spec] Remove the ServerArgs clone + global save/restore hack from DFlashWorkerV2
- [#20072](https://github.com/sgl-project/sglang/pull/20072) [CPU] Padding for dim divisibility in TP3/6 cases
- [#29615](https://github.com/sgl-project/sglang/pull/29615) Make mem_fraction_static reserve disaggregation-mode aware
- [#29758](https://github.com/sgl-project/sglang/pull/29758) Remove transformers 5.12.1 dead-code workarounds
- [#30153](https://github.com/sgl-project/sglang/pull/30153) Remove `# fmt: off` from environ.py Envs class
- [#30018](https://github.com/sgl-project/sglang/pull/30018) [Fix] Turn off dsa indexer fusion by default
- [#30088](https://github.com/sgl-project/sglang/pull/30088) [DSA] Disable indexer fusion by default to restore DeepSeek-V3.2 accuracy
- [#30101](https://github.com/sgl-project/sglang/pull/30101) Adjust KL_THRESHOLD for log probability calculations
- [#30182](https://github.com/sgl-project/sglang/pull/30182) Empty `_REQ_TYPES_WITH_OPAQUE_FIELDS` on the msgpack IPC path (#29465 Task 4)
- [#29912](https://github.com/sgl-project/sglang/pull/29912) Remove retired DSA env paths
- [#30146](https://github.com/sgl-project/sglang/pull/30146) Disable multi-threaded load by default when prefetch is on
- [#30013](https://github.com/sgl-project/sglang/pull/30013) For hybrid sliding-window (SWA) models the SWA KV pool is small and quickly
- [#27060](https://github.com/sgl-project/sglang/pull/27060) feat(hicache): Use NIXL path-mode
- [#30098](https://github.com/sgl-project/sglang/pull/30098) [codex] preserve kv canary across HiCache L2
- [#29815](https://github.com/sgl-project/sglang/pull/29815) feat: early validation for Ascend FIA page_size alignment
- [#29927](https://github.com/sgl-project/sglang/pull/29927) [SM120] DeepSeek-V4: DeepGEMM paged-MQA indexer +FP4 MoE+ page-split
- [#30148](https://github.com/sgl-project/sglang/pull/30148) [diffusion] Pass progressive params through image API
- [#30092](https://github.com/sgl-project/sglang/pull/30092) fix(config): read num_nextn_predict_layers from the outer hf_config as fallback

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 4a471f9d2cb78813313f2c6507b009e042fdf7d249da6bc5e62e984811fab813 -->
