# sglang: PR digest (2026-07-12 to 2026-07-16)

_233 merged, 313 newly opened - source sgl-project/sglang, generated 2026-07-16T11:24:57Z_

## TL;DR
- **Model Focus**: DeepSeek (V4) and GLM (5.2) dominated this cycle, with major work on SM90 NVFP4 KV-cache, MTP index sharing, and DeepSeek V4 BF16 compress state. MiniMax and Qwen also saw targeted attention.
- **Speculative Decoding**: Merged "DSpark", a new confidence-scheduled speculative decoding engine, alongside heavy in-flight work extending it to PD, DeepEP, and LFM2. EAGLE also received significant draft-tree verification and fusion optimizations.
- **Kernel Architecture**: Executed a massive, multi-phase migration of scattered attention, MoE, and quantization kernels into a unified `sglang.kernels` namespace (RFC #29630), standardizing the backend interface across Triton, Cutlass, and FlashInfer.
- **Quantization & MoE**: Refactored FP4 quantization, removed deprecated JIT kernels, and merged a new Humming quantization kernel. In-flight work is bringing MegaMoE NVFP4 and MXFP8 support through FlashInfer.
- **New Capabilities**: Opened a massive PR introducing Inkling support, alongside merged support for LongLive 2.0 diffusion models and JetBrains' Mellum v2.

## Most important PRs
- **[#30261](https://github.com/sgl-project/sglang/pull/30261)** `[Spec] Add DSpark: confidence-scheduled speculative decoding`: Introduces a major new speculative decoding backend that schedules verification based on confidence, deeply integrating with FlashInfer and the scheduler.
- **[#31358](https://github.com/sgl-project/sglang/pull/31358)** `Inkling support`: A massive 55k-line in-progress PR introducing comprehensive support for the Inkling model family across attention, MoE, and quantization components.
- **[#30448](https://github.com/sgl-project/sglang/pull/30448)** `Refactor FP4 quantization and remove deprecated JIT kernels`: Cleans up the quantization stack by standardizing FP4 implementations across Cutlass and FlashInfer, dropping legacy JIT paths.
- **[#30784](https://github.com/sgl-project/sglang/pull/30784)** `[Kernel] Migrate scattered quantization kernels to sglang.kernels`: The tip of the spear for a massive 7-part refactor that centralizes all custom kernels (attention, MoE, quantization, MLA) into a unified namespace.
- **[#31269](https://github.com/sgl-project/sglang/pull/31269)** `[Deepseek v4 & GLM-5.2] SM90 nvfp4 kvcache`: Brings highly optimized NVFP4 KV-cache support to Hopper architectures for the two most heavily used model families this cycle.

## More changes by area

<details>
<summary>Performance (20)</summary>

- [#28983](https://github.com/sgl-project/sglang/pull/28983) Enable SGLANG_OPT_FP8_WO_A_GEMM on Hopper for DeepSeek V4
- [#29669](https://github.com/sgl-project/sglang/pull/29669) Skip MXFP8 autotune on dense GEMM to avoid IMA
- [#30580](https://github.com/sgl-project/sglang/pull/30580) Lazy load TileLang MHC kernels
- [#30866](https://github.com/sgl-project/sglang/pull/30866) Tune VLM MoE paths
- [#30871](https://github.com/sgl-project/sglang/pull/30871) Add VLM prefill profiler ranges
- [#30878](https://github.com/sgl-project/sglang/pull/30878) Reuse MoonViT FA3 max-seqlen metadata
- [#30947](https://github.com/sgl-project/sglang/pull/30947) Fuse topk=1 draft postprocess for EAGLE
- [#30948](https://github.com/sgl-project/sglang/pull/30948) Fuse TP vocab-parallel embedding for EAGLE
- [#30949](https://github.com/sgl-project/sglang/pull/30949) Remove redundant draft capture input staging for EAGLE
- [#30959](https://github.com/sgl-project/sglang/pull/30959) Port flashinfer trtllm mnnvl fused allreduce to jit_kernel with small-batch specialization
- [#31049](https://github.com/sgl-project/sglang/pull/31049) Rewrite JIT custom all-reduce (v2) with decoupled kernel/storage design
- [#31079](https://github.com/sgl-project/sglang/pull/31079) Reduce tensor-parallel logits communication with a rank-0 gather
- [#31227](https://github.com/sgl-project/sglang/pull/31227) Shard Kimi DP image feature transport
- [#31284](https://github.com/sgl-project/sglang/pull/31284) Parallelize compute_position prefix-sum for large batch attention
- [#31301](https://github.com/sgl-project/sglang/pull/31301) Avoid temporary VLM encoder gather padding
- [#31304](https://github.com/sgl-project/sglang/pull/31304) Improve CPU silu performance by replacing fp32 div with rcp14
- [#31318](https://github.com/sgl-project/sglang/pull/31318) Avoid redundant Kimi vision projection copies
- [#31329](https://github.com/sgl-project/sglang/pull/31329) Fuse speculative relay scatter for EAGLE
- [#31341](https://github.com/sgl-project/sglang/pull/31341) Optimize HiSparse small-batch performance with multi-CTA cache sharding
- [#31438](https://github.com/sgl-project/sglang/pull/31438) Parallelize Qwen multimodal preprocessing

</details>

<details>
<summary>Kernels & attention (27)</summary>

- [#29589](https://github.com/sgl-project/sglang/pull/29589) Make FA3/FA4 sync-free for all backends and phases
- [#29690](https://github.com/sgl-project/sglang/pull/29690) Fuse preprocess kernels of trtllm-gen attention
- [#29692](https://github.com/sgl-project/sglang/pull/29692) Use fused A GEMM for fc1_latent_proj in NemotronH
- [#30012](https://github.com/sgl-project/sglang/pull/30012) Use BF16 instead of FP32 for DSv4 indexer score computation
- [#30113](https://github.com/sgl-project/sglang/pull/30113) Add FlashInfer SM100 KDA decode and MTP target_verify backend
- [#30169](https://github.com/sgl-project/sglang/pull/30169) Fuse SM100 CuteDSL prefill state I/O into the chunk h kernel
- [#30787](https://github.com/sgl-project/sglang/pull/30787) Migrate top-level srt/layers stray kernels to sglang.kernels
- [#30789](https://github.com/sgl-project/sglang/pull/30789) Migrate generic attention kernels to sglang.kernels
- [#30792](https://github.com/sgl-project/sglang/pull/30792) Migrate DSA and DSV4 attention kernels to sglang.kernels
- [#30793](https://github.com/sgl-project/sglang/pull/30793) Migrate linear-attention, MiniMax-sparse, and diffusion kernels to sglang.kernels
- [#30795](https://github.com/sgl-project/sglang/pull/30795) Relocate vendored fla and mamba kernel trees to sglang.kernels
- [#30898](https://github.com/sgl-project/sglang/pull/30898) Enable breakable prefill CUDA graph for DP attention
- [#30967](https://github.com/sgl-project/sglang/pull/30967) Add MTP cache mode for final-state recompute with FlashInfer integration
- [#30971](https://github.com/sgl-project/sglang/pull/30971) Support fp8 attention GEMMs on SM100 for MiniMax M3
- [#31020](https://github.com/sgl-project/sglang/pull/31020) Add FlashQLA GDN prefill kernel backend
- [#31050](https://github.com/sgl-project/sglang/pull/31050) Preserve attention LSE through the custom-op boundary for FullCG
- [#31087](https://github.com/sgl-project/sglang/pull/31087) Dispatch indexer topk_transform_512 through DSATopKBackend for DSV4
- [#31091](https://github.com/sgl-project/sglang/pull/31091) Support any exact v/k head ratio in the fused GDN qkvzba split
- [#31115](https://github.com/sgl-project/sglang/pull/31115) Add opt-in deterministic CuTe-DSL DSA top-k backend
- [#31172](https://github.com/sgl-project/sglang/pull/31172) Hoist GDN extend preparation across layers
- [#31190](https://github.com/sgl-project/sglang/pull/31190) Add SM89 FP8 paged indexer operator for DSA
- [#31197](https://github.com/sgl-project/sglang/pull/31197) Fuse absorbed-MLA kv_b_proj LoRA correction
- [#31241](https://github.com/sgl-project/sglang/pull/31241) Refine fused A GEMM dispatch
- [#31420](https://github.com/sgl-project/sglang/pull/31420) Add VSA flex/flashv4 support
- [#31432](https://github.com/sgl-project/sglang/pull/31432) Add TBO support for DeepSeek V4 hisparse
- [#31435](https://github.com/sgl-project/sglang/pull/31435) Add shared KV cache for GLM-5.2 prefill CP
- [#31446](https://github.com/sgl-project/sglang/pull/31446) Add MHA hisparse support for MiniMax M3

</details>

<details>
<summary>MoE & quantization (20)</summary>

- [#23754](https://github.com/sgl-project/sglang/pull/23754) Add humming quantization kernel
- [#25663](https://github.com/sgl-project/sglang/pull/25663) Refactor Ascend MoE implementation to align with community design
- [#27350](https://github.com/sgl-project/sglang/pull/27350) Support Waterfill with MegaMoE backend
- [#28220](https://github.com/sgl-project/sglang/pull/28220) Use CuTe DSL backend for FlashInfer per-token NVFP4 quantization
- [#28309](https://github.com/sgl-project/sglang/pull/28309) Support Flashinfer one-sided A2A and CuteDSL MoE for Nemotron Ultra
- [#30438](https://github.com/sgl-project/sglang/pull/30438) Delete CUTLASS FP8 blockwise for SM90/SM100, move SM120 to JIT, add SwapAB
- [#30706](https://github.com/sgl-project/sglang/pull/30706) Add fp4 combine dtype for MoRI-EP
- [#30786](https://github.com/sgl-project/sglang/pull/30786) Migrate scattered MoE kernels to sglang.kernels
- [#30924](https://github.com/sgl-project/sglang/pull/30924) Unify the JIT per_token_group_quant kernel family
- [#30952](https://github.com/sgl-project/sglang/pull/30952) Auto-select DeepSeek V4 FP4 MoE backends
- [#31017](https://github.com/sgl-project/sglang/pull/31017) Add DeepSeek-reference 1e-20 epsilon to top-k renormalization
- [#31109](https://github.com/sgl-project/sglang/pull/31109) Remove QServe and FBGEMM FP8 quantization
- [#31213](https://github.com/sgl-project/sglang/pull/31213) Keep GlmMoeDsa MoE e_score_correction_bias in fp32 for GLM-5.2
- [#31220](https://github.com/sgl-project/sglang/pull/31220) Support modelopt_fp4 checkpoints that quantize attention for Qwen3.5-MoE
- [#31282](https://github.com/sgl-project/sglang/pull/31282) Support mixed MXFP8 and NVFP4 modelopt checkpoints
- [#31330](https://github.com/sgl-project/sglang/pull/31330) Support FP32 NVFP4 global scale in Marlin
- [#31370](https://github.com/sgl-project/sglang/pull/31370) Fold padded-topk_ids fill into fused shared-experts append+remap
- [#31382](https://github.com/sgl-project/sglang/pull/31382) Support FlashInfer CuTe DSL for online NVFP4 draft MoE in Qwen3.5
- [#31408](https://github.com/sgl-project/sglang/pull/31408) Add MegaMOE NVFP4 and MXFP8 support through FlashInfer
- [#31429](https://github.com/sgl-project/sglang/pull/31429) Add FP8 DeepEP dispatch for humming MoE backend

</details>

<details>
<summary>Model support (28)</summary>

- [#27375](https://github.com/sgl-project/sglang/pull/27375) Add support for JetBrains' Mellum v2 code generation model
- [#27639](https://github.com/sgl-project/sglang/pull/27639) Support LongLive 2.0 T2V and I2V inference
- [#29191](https://github.com/sgl-project/sglang/pull/29191) Support hybrid models in NIXL hicache backend
- [#29609](https://github.com/sgl-project/sglang/pull/29609) Support BF16 Compress State for Online C128 in DeepSeek-V4
- [#30036](https://github.com/sgl-project/sglang/pull/30036) Support RL rollout for the Wan pipeline via per-request scheduler switch
- [#30535](https://github.com/sgl-project/sglang/pull/30535) Add mamba_io_kernel
- [#30620](https://github.com/sgl-project/sglang/pull/30620) Allow prefill breakable CUDA graph for Qwen3.5 via multimodal opt-in
- [#30889](https://github.com/sgl-project/sglang/pull/30889) Enable piecewise prefill graph for Kimi K2.5/K2.7
- [#30915](https://github.com/sgl-project/sglang/pull/30915) Support Megatron LayerNorm sequence parallelism
- [#30930](https://github.com/sgl-project/sglang/pull/30930) Add Seed-OSS (SeedOssForCausalLM) model support
- [#30988](https://github.com/sgl-project/sglang/pull/30988) Support LoRA under the breakable/full prefill CUDA graph
- [#30992](https://github.com/sgl-project/sglang/pull/30992) Support GLM-5.2 MTP index sharing with prefill CP
- [#31027](https://github.com/sgl-project/sglang/pull/31027) Support n>1 outputs for GLM-Image generation
- [#31029](https://github.com/sgl-project/sglang/pull/31029) Add LoRA IPC weight sync via lora_merge mode for Diffusion
- [#31041](https://github.com/sgl-project/sglang/pull/31041) Add LFM2 and LFM2-MoE DSpark speculative decoding support
- [#31047](https://github.com/sgl-project/sglang/pull/31047) Support GLM-5.2 DSpark draft config
- [#31059](https://github.com/sgl-project/sglang/pull/31059) Support configurable conv-window layouts for Mamba
- [#31081](https://github.com/sgl-project/sglang/pull/31081) Skip Qwen3-derived vision towers when multimodal is disabled
- [#31082](https://github.com/sgl-project/sglang/pull/31082) Skip Qwen3 Omni multimodal towers when disabled
- [#31106](https://github.com/sgl-project/sglang/pull/31106) Support GLM-5.2 MTP index sharing with prefill CP (cherry-pick)
- [#31176](https://github.com/sgl-project/sglang/pull/31176) Broadcast per-prompt conditioning to the sample batch for multi-output diffusion
- [#31177](https://github.com/sgl-project/sglang/pull/31177) Support fal Ideogram V4 Fast and Instant
- [#31233](https://github.com/sgl-project/sglang/pull/31233) Opt in Qwen and Wan multi-output conditioning expansion
- [#31251](https://github.com/sgl-project/sglang/pull/31251) Support GLM-5.2 FP8 based model with LoRA
- [#31276](https://github.com/sgl-project/sglang/pull/31276) Support PLaMo3 from Preferred Networks
- [#31320](https://github.com/sgl-project/sglang/pull/31320) Support distributed inference pipeline for GLM-Image on NPU
- [#31372](https://github.com/sgl-project/sglang/pull/31372) Add minimal DFLASH support for Inkling
- [#31391](https://github.com/sgl-project/sglang/pull/31391) Enable Kimi multimodal breakable prefill CUDA graph replay
- [#31414](https://github.com/sgl-project/sglang/pull/31414) Add DSpark dense draft model

</details>

<details>
<summary>Parallelism & scheduling (46)</summary>

- [#27408](https://github.com/sgl-project/sglang/pull/27408) Return top-p/top-k sampling mask/nucleas
- [#29427](https://github.com/sgl-project/sglang/pull/29427) Introduce req.kv container for coupled owned kv field lifecycle
- [#29428](https://github.com/sgl-project/sglang/pull/29428) Decouple cache backend from owned committed kv details
- [#29429](https://github.com/sgl-project/sglang/pull/29429) Let the presence of req.kv indicate the existence of owned kv resources
- [#29431](https://github.com/sgl-project/sglang/pull/29431) Extract allocation logic from mem_cache/common.py for parallel variants
- [#30182](https://github.com/sgl-project/sglang/pull/30182) Empty _REQ_TYPES_WITH_OPAQUE_FIELDS on the msgpack IPC path
- [#30352](https://github.com/sgl-project/sglang/pull/30352) Handle NIXL abort notifications
- [#30365](https://github.com/sgl-project/sglang/pull/30365) Remove per-step seqlen D2H from speculative to make overlap scheduler work
- [#30457](https://github.com/sgl-project/sglang/pull/30457) Support scheduler_recv_interval under DP-attention
- [#30468](https://github.com/sgl-project/sglang/pull/30468) Use UnifiedRadixTree by default for SWA, Mamba, and DSA models
- [#30675](https://github.com/sgl-project/sglang/pull/30675) Rewrite pause_generation retract path as req-level release and requeue
- [#30748](https://github.com/sgl-project/sglang/pull/30748) Route PD server warmup to every DP rank
- [#30908](https://github.com/sgl-project/sglang/pull/30908) Release PyNccl communicator memory in sleep mode
- [#30944](https://github.com/sgl-project/sglang/pull/30944) Add kill-switch env for draft-extend CUDA graph capture
- [#30951](https://github.com/sgl-project/sglang/pull/30951) Improve optimistic prefill in PD
- [#30966](https://github.com/sgl-project/sglang/pull/30966) Support PD and DeepEP+DeepGEMM in DSpark
- [#31024](https://github.com/sgl-project/sglang/pull/31024) Implement query_storage_hit_length for decode-side HiCache
- [#31034](https://github.com/sgl-project/sglang/pull/31034) Support speculative target verification in KDA
- [#31057](https://github.com/sgl-project/sglang/pull/31057) Add semantic KV cache reuse via a pluggable fuzzy-match radix backend
- [#31069](https://github.com/sgl-project/sglang/pull/31069) Add DFLASH EAGLE-style draft-tree verification
- [#31090](https://github.com/sgl-project/sglang/pull/31090) Enable sync-free spec via device-side draft-extend for flashmla
- [#31097](https://github.com/sgl-project/sglang/pull/31097) Add DeepSeek-V4 decode radix cache with MTP support for P/D Disagg
- [#31136](https://github.com/sgl-project/sglang/pull/31136) Add page_blob_direct layout for HiCache
- [#31139](https://github.com/sgl-project/sglang/pull/31139) Enable speculative decoding (eagle_worker_v2) under PP
- [#31148](https://github.com/sgl-project/sglang/pull/31148) Introduce WeightUpdater and WeightExporter components
- [#31153](https://github.com/sgl-project/sglang/pull/31153) Introduce RemoteInstanceWeightTransporter component
- [#31154](https://github.com/sgl-project/sglang/pull/31154) Introduce NgramEmbeddingManager component
- [#31161](https://github.com/sgl-project/sglang/pull/31161) Introduce ModelRunner.ps ParallelState
- [#31170](https://github.com/sgl-project/sglang/pull/31170) Add prefix_affinity load balancing for DP-attention
- [#31173](https://github.com/sgl-project/sglang/pull/31173) Stride KV token->page indices on device before D2H copy
- [#31181](https://github.com/sgl-project/sglang/pull/31181) Support Mamba branching in Unified Radix Cache with HiCache
- [#31188](https://github.com/sgl-project/sglang/pull/31188) Bound Decode-to-Prefill metadata sends
- [#31217](https://github.com/sgl-project/sglang/pull/31217) Improve robustness and failure handling for Disagg StagingBuffer
- [#31230](https://github.com/sgl-project/sglang/pull/31230) Add a per-path cap for cached states in Mamba
- [#31238](https://github.com/sgl-project/sglang/pull/31238) Replace draft-tail stream with enumeration buffer for decoupled spec data plane
- [#31244](https://github.com/sgl-project/sglang/pull/31244) Converge DP-attention spec width scaling onto num_tokens_per_req
- [#31245](https://github.com/sgl-project/sglang/pull/31245) Key DP-attention graph admission on raw sync request counts
- [#31255](https://github.com/sgl-project/sglang/pull/31255) Split the capture width from num_tokens_per_req and gate replay on it
- [#31256](https://github.com/sgl-project/sglang/pull/31256) Make num_tokens_per_req Optional for ragged capture
- [#31294](https://github.com/sgl-project/sglang/pull/31294) Skip no-op EAGLE sampling renormalization
- [#31305](https://github.com/sgl-project/sglang/pull/31305) Add paged LoRA memory pool with page-level eviction
- [#31315](https://github.com/sgl-project/sglang/pull/31315) Avoid repeated Mooncake gets after stale hits in HiCache
- [#31328](https://github.com/sgl-project/sglang/pull/31328) Add correctness-first Domino support to DFlash V2
- [#31335](https://github.com/sgl-project/sglang/pull/31335) Support alloc-page-aligned memory management
- [#31395](https://github.com/sgl-project/sglang/pull/31395) Interleave decode passes between mixed prefills
- [#31422](https://github.com/sgl-project/sglang/pull/31422) Add DSpark compact-verify on DSA backends and sync-free verify-all
- [#31427](https://github.com/sgl-project/sglang/pull/31427) Protect HiRadix host KV until load-back ack
- [#31443](https://github.com/sgl-project/sglang/pull/31443) Apply all-or-nothing strategy for hybrid model's prefetching in HiCache

</details>

<details>
<summary>Hardware & arch (23)</summary>

- [#26852](https://github.com/sgl-project/sglang/pull/26852) Reuse fused FP8 KV cache write on standard aiter prefill/decode for AMD
- [#27873](https://github.com/sgl-project/sglang/pull/27873) Use sgl-kernel implementation of fused_q_indexer_rope_hadamard_quant on Intel XPU
- [#28059](https://github.com/sgl-project/sglang/pull/28059) Support fp8_paged_mqa_logits_triton from sgl-kernel on Intel XPU
- [#28113](https://github.com/sgl-project/sglang/pull/28113) Route pin memory availability through current_platform
- [#28428](https://github.com/sgl-project/sglang/pull/28428) Use sgl-kernel implementation of silu_and_mul_clamp on Intel XPU
- [#30238](https://github.com/sgl-project/sglang/pull/30238) Support two batch overlap with MTP on DeepSeekV4 for AMD
- [#30622](https://github.com/sgl-project/sglang/pull/30622) Remove ROCm page_first+kernel to layer_first HiCache fallback
- [#30651](https://github.com/sgl-project/sglang/pull/30651) Add MORI disagg backend for AMD and bump MI355X image
- [#30964](https://github.com/sgl-project/sglang/pull/30964) Support DeepSeek V4 DSpark on AMD HIP platform
- [#30980](https://github.com/sgl-project/sglang/pull/30980) Add full backend support for prefill graph on XPU
- [#30993](https://github.com/sgl-project/sglang/pull/30993) Enable a16w4 for Qwen3.5 MXFP4 MoE on AMD
- [#31038](https://github.com/sgl-project/sglang/pull/31038) Route topk_sigmoid and topk_softmax to AOT sgl-kernel-xpu symbols
- [#31040](https://github.com/sgl-project/sglang/pull/31040) Add SWA per-request ring runtime accounting for AMD DSV4 unified_kv
- [#31054](https://github.com/sgl-project/sglang/pull/31054) Support Quark DeepSeek-V4-MXFP4 checkpoints on AMD DSV4 stack
- [#31110](https://github.com/sgl-project/sglang/pull/31110) Bypass scoring_func argument in topk for CPU device
- [#31111](https://github.com/sgl-project/sglang/pull/31111) Add pyxccl direct Intel oneCCL communicator for XPU
- [#31113](https://github.com/sgl-project/sglang/pull/31113) Add NUMA node binding support for Intel XPU
- [#31126](https://github.com/sgl-project/sglang/pull/31126) Enable biased grouped topk for Intel XPU
- [#31137](https://github.com/sgl-project/sglang/pull/31137) Enable gfx1151 (RDNA3.5 / Strix Halo) for single-GPU in sgl-kernel
- [#31171](https://github.com/sgl-project/sglang/pull/31171) Add fused input proj for qwen3.5 on CPU
- [#31191](https://github.com/sgl-project/sglang/pull/31191) Add opt-in FlyDSL prefill GDN chunk kernel path for AMD HIP
- [#31259](https://github.com/sgl-project/sglang/pull/31259) Default RDNA to the Triton attention backend
- [#31307](https://github.com/sgl-project/sglang/pull/31307) Fill non-CUDA coverage for HIP and Ascend NPU backends
- [#31322](https://github.com/sgl-project/sglang/pull/31322) Add FlyDSL MegaMoE backend for DeepSeek MoE on AMD
- [#31323](https://github.com/sgl-project/sglang/pull/31323) Fuse shared-expert append into aiter grouped-topk on AMD GLM5
- [#31324](https://github.com/sgl-project/sglang/pull/31324) Skip DSA decode indexer when kv_len <= index_topk on AMD GLM5
- [#31362](https://github.com/sgl-project/sglang/pull/31362) Add Speculative Decoding with NGRAM support for XPU
- [#31423](https://github.com/sgl-project/sglang/pull/31423) Support DeepEP-Waterfill and LPLB on the MoRI-EP backend for AMD
- [#31428](https://github.com/sgl-project/sglang/pull/31428) Route OOT device-name queries through current_platform

</details>

<details>
<summary>API & serving (18)</summary>

- [#29579](https://github.com/sgl-project/sglang/pull/29579) Add --default-chat-template-kwargs server arg
- [#30897](https://github.com/sgl-project/sglang/pull/30897) Handle coredump dirs and cache hit updates
- [#30904](https://github.com/sgl-project/sglang/pull/30904) Unify multimodal feature transport
- [#30912](https://github.com/sgl-project/sglang/pull/30912) Support aborting requests by rid prefix
- [#30913](https://github.com/sgl-project/sglang/pull/30913) Support upsert when loading adapters from tensors/distributed
- [#30917](https://github.com/sgl-project/sglang/pull/30917) Add return_token_ids support to completions and chat completions APIs
- [#30962](https://github.com/sgl-project/sglang/pull/30962) Add opt-in chat content sanitization
- [#30969](https://github.com/sgl-project/sglang/pull/30969) Add /abort_request proxy to mini LB
- [#31055](https://github.com/sgl-project/sglang/pull/31055) Add Streaming ASR sliding window, server-side VAD, and segment-streaming mode
- [#31076](https://github.com/sgl-project/sglang/pull/31076) Add native gRPC sidecar module launcher
- [#31077](https://github.com/sgl-project/sglang/pull/31077) Add per-request lifecycle tracing
- [#31219](https://github.com/sgl-project/sglang/pull/31219) Add optional uint16/uint8 routed-experts wire encoding
- [#31253](https://github.com/sgl-project/sglang/pull/31253) Support multi-LoRA RL integration with abort by rid prefix and LoRA upsert
- [#31272](https://github.com/sgl-project/sglang/pull/31272) Stamp selected worker on dispatch-stage errors via Server-Timing
- [#31281](https://github.com/sgl-project/sglang/pull/31281) Make server relaunches robust to slow GPU teardown
- [#31345](https://github.com/sgl-project/sglang/pull/31345) Segment encode_batch for long RAG in tokenizer
- [#31389](https://github.com/sgl-project/sglang/pull/31389) Add configurable FlashInfer autotune skips
- [#31412](https://github.com/sgl-project/sglang/pull/31412) Add token-weighted prefix cache hit rate panel to dashboard

</details>

<details>
<summary>Bugfixes (67)</summary>

- [#26411](https://github.com/sgl-project/sglang/pull/26411) Measure load-back duration with CUDA events in HiCache
- [#27998](https://github.com/sgl-project/sglang/pull/27998) Fix Mamba spec-v2 + extra_buffer crash
- [#29007](https://github.com/sgl-project/sglang/pull/29007) Fix MoE TP allreduce to use NCCL symmetric memory
- [#29151](https://github.com/sgl-project/sglang/pull/29151) Fix ModelOpt NVFP4 scalar scales for merged linears
- [#29430](https://github.com/sgl-project/sglang/pull/29430) Fix abusing presence of req.req_pool_idx
- [#29432](https://github.com/sgl-project/sglang/pull/29432) Fix bookkeeping fields not encapsulated with real allocations
- [#29508](https://github.com/sgl-project/sglang/pull/29508) Fix quickreduce acc error in cudagraph mode
- [#29909](https://github.com/sgl-project/sglang/pull/29909) Fix Hunyuan3 model where MoE's routing_scaling_ratio is missing on NPU
- [#29929](https://github.com/sgl-project/sglang/pull/29929) Fix FlashInfer A2A top-k ID dtype
- [#30331](https://github.com/sgl-project/sglang/pull/30331) Load HunyuanV3 NextN final_layernorm into the draft head's output norm
- [#30351](https://github.com/sgl-project/sglang/pull/30351) Account for KV replication fan-out in transfer-byte metrics
- [#30355](https://github.com/sgl-project/sglang/pull/30355) Fix attention-backend triton for DeepSeek MLA on MI355
- [#30458](https://github.com/sgl-project/sglang/pull/30458) Fix input parameters of swiglu_oai operator on NPU
- [#30533](https://github.com/sgl-project/sglang/pull/30533) Fix Nemotron 3 parser for tool call and force nonempty content
- [#30621](https://github.com/sgl-project/sglang/pull/30621) Fix image URL response for multiple outputs
- [#30673](https://github.com/sgl-project/sglang/pull/30673) Fix non-existent abort mode in Scheduler.pause_generation
- [#30674](https://github.com/sgl-project/sglang/pull/30674) Fix missed hisparse release and stale field cleanup in pause retract
- [#30682](https://github.com/sgl-project/sglang/pull/30682) Preserve tokenizer worker fanout when skip_tokenizer_init is enabled
- [#30839](https://github.com/sgl-project/sglang/pull/30839) Stabilize GLM-5.2 MTP IndexShare across PD and CUDA graph replay
- [#30867](https://github.com/sgl-project/sglang/pull/30867) Fix image benchmark backend parity
- [#30869](https://github.com/sgl-project/sglang/pull/30869) Fix Kimi-VL encoder parallelism
- [#30870](https://github.com/sgl-project/sglang/pull/30870) Avoid TileLang CUDA runtime pollution
- [#30902](https://github.com/sgl-project/sglang/pull/30902) Cap CUDA IPC multimodal pool budget
- [#30909](https://github.com/sgl-project/sglang/pull/30909) Fix inflated full token usage for DeepSeek V4 in HiSparse
- [#30914](https://github.com/sgl-project/sglang/pull/30914) Honor CUDA decode profiling step limits in bench
- [#30916](https://github.com/sgl-project/sglang/pull/30916) Fix dp-attention + speculative decoding crashes in flashinfer MLA backend
- [#30937](https://github.com/sgl-project/sglang/pull/30937) Avoid double KV release on disaggregated prefill grammar errors
- [#30968](https://github.com/sgl-project/sglang/pull/30968) Fix Nemotron ForwardFlags across custom op boundary
- [#30972](https://github.com/sgl-project/sglang/pull/30972) Add support for using MXFP8 datatype in flashinfer A2A communicator
- [#30981](https://github.com/sgl-project/sglang/pull/30981) Support staged write-back for asymmetric MHA in hicache
- [#30982](https://github.com/sgl-project/sglang/pull/30982) Support speculators-convention checkpoints in DSpark
- [#30986](https://github.com/sgl-project/sglang/pull/30986) Fix mamba state corruption and slot leak when load_back aborts
- [#30987](https://github.com/sgl-project/sglang/pull/30987) Fix DeepSeek ForwardFlags across custom op boundary
- [#30990](https://github.com/sgl-project/sglang/pull/30990) Strip think tags split across stream chunks in Trinity reasoning parser
- [#30997](https://github.com/sgl-project/sglang/pull/30997) Fix heterogeneous attn-TP scatter transfer for Qwen3.5
- [#31001](https://github.com/sgl-project/sglang/pull/31001) Fix GLM/DeepSeek NVFP4 + flashinfer_trtllm long-context collapse
- [#31002](https://github.com/sgl-project/sglang/pull/31002) Fix W4A16 NVFP4 ModelOpt Marlin routing
- [#31009](https://github.com/sgl-project/sglang/pull/31009) Hold back think tags split across stream chunks in reasoning parser
- [#31033](https://github.com/sgl-project/sglang/pull/31033) Avoid CUDA grid overflow in recurrent linear attention
- [#31060](https://github.com/sgl-project/sglang/pull/31060) Fix DSA indexer page/token granularity in move_kv_cache
- [#31061](https://github.com/sgl-project/sglang/pull/31061) Fall back to torch MoE top-k sigmoid instead of CUDA-only JIT on XPU
- [#31065](https://github.com/sgl-project/sglang/pull/31065) Fix GLM/DeepSeek NVFP4 + flashinfer_trtllm long-context collapse (cherry-pick)
- [#31075](https://github.com/sgl-project/sglang/pull/31075) Fix optimistic prefill inflight-queue hangs on parked/aborted reqs
- [#31083](https://github.com/sgl-project/sglang/pull/31083) Stabilize GLM-5.2 MTP IndexShare across PD and CUDA graph replay
- [#31089](https://github.com/sgl-project/sglang/pull/31089) Update sgl-kernel imports of relocated fp8_kernel
- [#31092](https://github.com/sgl-project/sglang/pull/31092) Fix post-capture KV sizing for SWA pools
- [#31100](https://github.com/sgl-project/sglang/pull/31100) Fix DP-attention state-capturer crash on cuda_graph_batch=None
- [#31101](https://github.com/sgl-project/sglang/pull/31101) Fix diffusion cookbook overview cards
- [#31105](https://github.com/sgl-project/sglang/pull/31105) Fix fp8 per-channel attention for Kimi-K2.7 on ROCm/gfx95
- [#31119](https://github.com/sgl-project/sglang/pull/31119) Prevent infinite thinking loop from cross-chunk tag truncation in Qwen3 streaming
- [#31123](https://github.com/sgl-project/sglang/pull/31123) Harden top-k v1/v2 kernels against negative padded seq_lens in DSA
- [#31131](https://github.com/sgl-project/sglang/pull/31131) Fix DSV4 JIT build on rocm
- [#31134](https://github.com/sgl-project/sglang/pull/31134) Fix LongCat n-gram embedding in PD-disaggregated scheduler loops
- [#31135](https://github.com/sgl-project/sglang/pull/31135) Fix custom all-reduce deadlock when one communicator is issued from two CUDA streams
- [#31144](https://github.com/sgl-project/sglang/pull/31144) Fix decode hanging forever when a prefill peer dies
- [#31184](https://github.com/sgl-project/sglang/pull/31184) Support all ResponseToolType variants in sgl-model-gateway
- [#31192](https://github.com/sgl-project/sglang/pull/31192) Fix defensive getattr/hasattr usage
- [#31193](https://github.com/sgl-project/sglang/pull/31193) Prevent unknown HTTP paths from overloading Prometheus metrics generation
- [#31203](https://github.com/sgl-project/sglang/pull/31203) Replay VLM decoder with TC prefill graphs
- [#31204](https://github.com/sgl-project/sglang/pull/31204) Skip unsafe automatic prefill graph capture
- [#31211](https://github.com/sgl-project/sglang/pull/31211) Fix processor config loading for object-storage model paths
- [#31212](https://github.com/sgl-project/sglang/pull/31212) Support Kimi K2.7 DP vision encoder
- [#31214](https://github.com/sgl-project/sglang/pull/31214) Fix EAGLE spec-decode verify silently sampling greedy on HIP
- [#31218](https://github.com/sgl-project/sglang/pull/31218) Page-aware move_kv_cache for the DSA indexer cache
- [#31232](https://github.com/sgl-project/sglang/pull/31232) Fix Ministral3 accuracy issue by aligning YaRN RoPE scaling
- [#31247](https://github.com/sgl-project/sglang/pull/31247) Integrate embedding KV-cache-skip fast path into torch_native backend
- [#31270](https://github.com/sgl-project/sglang/pull/31270) Fix draft-extend CUDA graph padding and WAR ordering for DSV4
- [#31290](https://github.com/sgl-project/sglang/pull/31290) Fix DP-attention reduce_scatterv / all_gatherv on XPU
- [#31298](https://github.com/sgl-project/sglang/pull/31298) Warm up Kimi VLM vision encoder at startup
- [#31299](https://github.com/sgl-project/sglang/pull/31299) Fix LPLB fused-IPM kernel sm_*a arch target on Blackwell
- [#31313](https://github.com/sgl-project/sglang/pull/31313) Fix GLM-Image AR model-path to resolve local snapshot subfolder
- [#31326](https://github.com/sgl-project/sglang/pull/31326) Avoid redundant tensor clones in Mamba radix cache
- [#31331](https://github.com/sgl-project/sglang/pull/31331) Resolve router-included endpoint path for metrics
- [#31338](https://github.com/sgl-project/sglang/pull/31338) Fix packed DSA FP8 KV write routing on HIP
- [#31340](https://github.com/sgl-project/sglang/pull/31340) Fix FP8 Triton dtype selection on A100
- [#31343](https://github.com/sgl-project/sglang/pull/31343) Fix MiMo-V2 on Blackwell FA3 fallback and TP-aware audio weight loading
- [#31344](https://github.com/sgl-project/sglang/pull/31344) Reject prefill-only flashmla_auto for --dsa-decode-backend
- [#31346](https://github.com/sgl-project/sglang/pull/31346) Fail fast on fp8_e4m3 KV with tilelang DSA backend on CUDA
- [#31351](https://github.com/sgl-project/sglang/pull/31351) Don't leak partial bot_token bytes in DeepSeek V3/V3.1 streaming detectors
- [#31355](https://github.com/sgl-project/sglang/pull/31355) Fix multimodal input path crashes on non-CUDA machines
- [#31357](https://github.com/sgl-project/sglang/pull/31357) Drain Mooncake transfers before releasing KV pages
- [#31367](https://github.com/sgl-project/sglang/pull/31367) Stamp capture-time num_tokens_per_req in multi-layer EAGLE
- [#31387](https://github.com/sgl-project/sglang/pull/31387) Bound deterministic FlashInfer CUDA-graph decode launches
- [#31392](https://github.com/sgl-project/sglang/pull/31392) Wire the detokenizer soft watchdog into the multi-http-worker event loop
- [#31401](https://github.com/sgl-project/sglang/pull/31401) Fix inkling effort rounding and responses API passthrough
- [#31402](https://github.com/sgl-project/sglang/pull/31402) Fix non-blocking HiCache storage prefetch misses
- [#31403](https://github.com/sgl-project/sglang/pull/31403) Fix RMSNorm on AMD devices without AITER
- [#31419](https://github.com/sgl-project/sglang/pull/31419) Return 404 for unknown models on OpenAI-compatible endpoints
- [#31425](https://github.com/sgl-project/sglang/pull/31425) Fix hicache TP/PP write-through & load-back consensus
- [#31444](https://github.com/sgl-project/sglang/pull/31444) Keep duplicate MCP namespace routing consistent
- [#31447](https://github.com/sgl-project/sglang/pull/31447) Fix overlap scheduling and all-reduce fusion for NVIDIA CC on Blackwell
- [#31456](https://github.com/sgl-project/sglang/pull/31456) Fix modelslim quant tensor name on NPU

</details>

<details>
<summary>Refactors (43)</summary>

- [#30585](https://github.com/sgl-project/sglang/pull/30585) Enhance mechanical-refactor-verify skill with a whole-chain verifier
- [#30616](https://github.com/sgl-project/sglang/pull/30616) Move MLATokenToKVPoolHost to pool_host.mla
- [#30669](https://github.com/sgl-project/sglang/pull/30669) Remove dead ScheduleBatch fields and avoid inplace seq_lens bump
- [#30670](https://github.com/sgl-project/sglang/pull/30670) Pass per-forward overrides to ForwardBatch.init_new as explicit arguments
- [#30672](https://github.com/sgl-project/sglang/pull/30672) Avoid mutating ScheduleBatch fields in place
- [#30676](https://github.com/sgl-project/sglang/pull/30676) Avoid implicit running_batch access in dllm and pdmux scheduling
- [#30677](https://github.com/sgl-project/sglang/pull/30677) Avoid relaying per-step outputs through ScheduleBatch fields
- [#30828](https://github.com/sgl-project/sglang/pull/30828) Make the mxfp8 MoE runner backend list extensible
- [#30973](https://github.com/sgl-project/sglang/pull/30973) Remove a few dead code paths in DSA
- [#30977](https://github.com/sgl-project/sglang/pull/30977) Rename num_tokens_per_bs to num_tokens_per_req
- [#30998](https://github.com/sgl-project/sglang/pull/30998) Remove dead padded_static_len and stale SGLANG_ENABLE_SPEC_V2 references
- [#31008](https://github.com/sgl-project/sglang/pull/31008) Deduplicate spec-v2 worker lifecycle boilerplate into BaseSpecWorker
- [#31013](https://github.com/sgl-project/sglang/pull/31013) Single-source num_tokens_per_req derivation and access
- [#31078](https://github.com/sgl-project/sglang/pull/31078) Consolidate spec-worker weight updates into BaseSpecWorker
- [#31142](https://github.com/sgl-project/sglang/pull/31142) Clarify ModelRunner.dp_size into attn_dp_size
- [#31145](https://github.com/sgl-project/sglang/pull/31145) Clean up ModelRunner by renaming effective-token property
- [#31146](https://github.com/sgl-project/sglang/pull/31146) Extract leaf helpers out of ModelRunner into utility modules
- [#31147](https://github.com/sgl-project/sglang/pull/31147) Extract kv cache dtype configuration into mem_cache
- [#31149](https://github.com/sgl-project/sglang/pull/31149) Extract expert location updating into EPLBManager
- [#31150](https://github.com/sgl-project/sglang/pull/31150) Extract hybrid-arch helpers into configs.hybrid_arch and ModelConfig
- [#31151](https://github.com/sgl-project/sglang/pull/31151) Move LoRA cuda-graph buffers and logging into LoRAManager
- [#31152](https://github.com/sgl-project/sglang/pull/31152) Extract init_torch_distributed and refactor into functions
- [#31155](https://github.com/sgl-project/sglang/pull/31155) Extract load_model helpers into a load_model_utils module
- [#31156](https://github.com/sgl-project/sglang/pull/31156) Extract layer-index setup into a module
- [#31157](https://github.com/sgl-project/sglang/pull/31157) Extract spec aux-hidden-state resolution into a module
- [#31158](https://github.com/sgl-project/sglang/pull/31158) Extract small single-function helpers into modules
- [#31159](https://github.com/sgl-project/sglang/pull/31159) Extract MoE/EP setup into a moe_ep_setup module
- [#31160](https://github.com/sgl-project/sglang/pull/31160) Absorb capturer setup and extract the shared-mooncake gate
- [#31162](https://github.com/sgl-project/sglang/pull/31162) Introduce KVCacheConfigurator and migrate KV-cache config logic
- [#31163](https://github.com/sgl-project/sglang/pull/31163) Extract per-architecture KV-cache pool builders into KVCacheConfigurator
- [#31165](https://github.com/sgl-project/sglang/pull/31165) Drop ModelRunner's duplicated parallel-degree fields
- [#31166](https://github.com/sgl-project/sglang/pull/31166) Narrow component dependencies to injected fields instead of ModelRunner
- [#31167](https://github.com/sgl-project/sglang/pull/31167) Extract attention-backend setup into a module
- [#31168](https://github.com/sgl-project/sglang/pull/31168) Extract cuda-graph setup into a module
- [#31169](https://github.com/sgl-project/sglang/pull/31169) Split initialize() into orchestration helpers
- [#31180](https://github.com/sgl-project/sglang/pull/31180) Move MambaPoolHost to pool_host.mamba
- [#31202](https://github.com/sgl-project/sglang/pull/31202) Delete sgl-kernel AOT bmm_fp8, use flashinfer.bmm_fp8
- [#31222](https://github.com/sgl-project/sglang/pull/31222) Move SchedulerRecvSkipper into scheduler_components
- [#31225](https://github.com/sgl-project/sglang/pull/31225) Remove dead MiniMax M3 artifacts
- [#31254](https://github.com/sgl-project/sglang/pull/31254) Inline DP-attention width scaling
- [#31257](https://github.com/sgl-project/sglang/pull/31257) Extract stateless draft prepare helpers into eagle_worker_common
- [#31292](https://github.com/sgl-project/sglang/pull/31292) Decouple KernelBackend from device
- [#31308](https://github.com/sgl-project/sglang/pull/31308) Remove redundant parameters of build_xxx_stack and others in HiCache
- [#31375](https://github.com/sgl-project/sglang/pull/31375) Extract the shared draft() tail into build_eagle_verify_input
- [#31380](https://github.com/sgl-project/sglang/pull/31380) Consolidate the verify step into eagle_worker_common.run_eagle_verify
- [#31394](https://github.com/sgl-project/sglang/pull/31394) Make TRTLLMHAAttnBackend inherit from AttentionBackend
- [#31439](https://github.com/sgl-project/sglang/pull/31439) Wrap split attention backends once
- [#31453](https://github.com/sgl-project/sglang/pull/31453) Extract complex RoPE implementation to layers/rotary_embedding for MOVA DiT

</details>

<details>
<summary>Docs (22)</summary>

- [#28964](https://github.com/sgl-project/sglang/pull/28964) Remove legacy Sphinx docs/ and finish the Mintlify cutover
- [#29886](https://github.com/sgl-project/sglang/pull/29886) Standardize TorchNPU names throughout documentation
- [#30520](https://github.com/sgl-project/sglang/pull/30520) Update CPU model support info in Cookbook
- [#30571](https://github.com/sgl-project/sglang/pull/30571) Sync LMSYS SGLang blog cards
- [#30767](https://github.com/sgl-project/sglang/pull/30767) Optimize and fix docs issues on Ascend NPU
- [#30996](https://github.com/sgl-project/sglang/pull/30996) Add SRT Slurm PD-disaggregated deployment to DeepSeek-V4 cookbook
- [#31036](https://github.com/sgl-project/sglang/pull/31036) Fix Ascend NPU docs issues found by AIDD
- [#31094](https://github.com/sgl-project/sglang/pull/31094) Remove deprecated Mamba flags and wrong FP8 GEMM docstrings
- [#31104](https://github.com/sgl-project/sglang/pull/31104) Add agent rule to all non-docs READMEs to prevent AI slop
- [#31122](https://github.com/sgl-project/sglang/pull/31122) Add AMD-specific HiCache config for DeepSeek V4 playground
- [#31124](https://github.com/sgl-project/sglang/pull/31124) Note the default dsa-topk-backend on all DSA-model cookbook pages
- [#31129](https://github.com/sgl-project/sglang/pull/31129) Optimize directory structure
- [#31242](https://github.com/sgl-project/sglang/pull/31242) Sync LMSYS SGLang blog cards
- [#31258](https://github.com/sgl-project/sglang/pull/31258) Update qwen3.5 cookbook for AMD
- [#31302](https://github.com/sgl-project/sglang/pull/31302) Fix NPU docs issues found by aidd
- [#31316](https://github.com/sgl-project/sglang/pull/31316) Update model names supported on Ascend NPU
- [#31333](https://github.com/sgl-project/sglang/pull/31333) Document CUDA crash dump output
- [#31360](https://github.com/sgl-project/sglang/pull/31360) Add Inkling cookbook
- [#31363](https://github.com/sgl-project/sglang/pull/31363) Re-benchmark DeepSeek-V4 on sglang 0.5.15
- [#31373](https://github.com/sgl-project/sglang/pull/31373) Align B200 DeepSeek-V4-Pro balanced recipe with MegaMoE
- [#31377](https://github.com/sgl-project/sglang/pull/31377) Add DeepSeek-V4 Pro GB300 FP4 multi-node recipes
- [#31386](https://github.com/sgl-project/sglang/pull/31386) Sync LMSYS SGLang blog cards
- [#31411](https://github.com/sgl-project/sglang/pull/31411) Migrate CP knob to canonical prefill-CP flags in Playground
- [#31452](https://github.com/sgl-project/sglang/pull/31452) Tune DeepSeek-V4 HiCache for MI355X PD

</details>

<details>
<summary>Tests, CI & build (36)</summary>

- [#27106](https://github.com/sgl-project/sglang/pull/27106) Make UTs compatible for XPU
- [#29939](https://github.com/sgl-project/sglang/pull/29939) Update test repository case scripts to the main community
- [#30858](https://github.com/sgl-project/sglang/pull/30858) Fix CUDA 12 Docker dependency resolution
- [#30873](https://github.com/sgl-project/sglang/pull/30873) Fix DeepEP CI test registration
- [#30879](https://github.com/sgl-project/sglang/pull/30879) Support random image resolutions in bench
- [#30901](https://github.com/sgl-project/sglang/pull/30901) Add unit tests for pool_stats_observer
- [#30905](https://github.com/sgl-project/sglang/pull/30905) Fix deterministic inference test coverage
- [#30906](https://github.com/sgl-project/sglang/pull/30906) Add deterministic sampling kernel tests
- [#30911](https://github.com/sgl-project/sglang/pull/30911) Guard ROCm imports without visible GPUs
- [#30918](https://github.com/sgl-project/sglang/pull/30918) Add optional steady-state window for serving metrics
- [#30927](https://github.com/sgl-project/sglang/pull/30927) Gate Rust extension builds
- [#30942](https://github.com/sgl-project/sglang/pull/30942) Pin cmake==4.3.4 in ROCm Dockerfile to fix MoRI gtest_discover build break
- [#30960](https://github.com/sgl-project/sglang/pull/30960) Update CI test est_time values
- [#30978](https://github.com/sgl-project/sglang/pull/30978) Guard ROCm imports without visible GPUs
- [#30984](https://github.com/sgl-project/sglang/pull/30984) Upgrade Python 3.12 + torch 2.11 + triton 3.6.0 in ROCm 7.2.4
- [#30995](https://github.com/sgl-project/sglang/pull/30995) Disable gated Llama-2 EAGLE spec tests to unblock Xeon CPU CI
- [#31035](https://github.com/sgl-project/sglang/pull/31035) Fix CUDA 12 NVIDIA wheel cleanup
- [#31042](https://github.com/sgl-project/sglang/pull/31042) Fix SGLANG_JIT_KERNEL_RUN_FULL_TESTS never activating the nightly full jit-kernel sweep
- [#31068](https://github.com/sgl-project/sglang/pull/31068) Detect and recover hung GPUs in MI35x pre-flight
- [#31074](https://github.com/sgl-project/sglang/pull/31074) Debug dev branch
- [#31088](https://github.com/sgl-project/sglang/pull/31088) Register CPU-bound / triton unit tests for AMD 1-GPU PR CI
- [#31096](https://github.com/sgl-project/sglang/pull/31096) Add unit tests for AMD arch-detection helpers
- [#31112](https://github.com/sgl-project/sglang/pull/31112) Add unit tests for msgspec_utils
- [#31114](https://github.com/sgl-project/sglang/pull/31114) Push test case scripts from test repo to main upstream community repository
- [#31121](https://github.com/sgl-project/sglang/pull/31121) Add unit tests for KV-cache eviction priority strategies
- [#31125](https://github.com/sgl-project/sglang/pull/31125) Disable flaky DSV4-Flash FP4 BCG determinism test
- [#31234](https://github.com/sgl-project/sglang/pull/31234) Strip invisible Unicode format chars from slash-command input
- [#31260](https://github.com/sgl-project/sglang/pull/31260) Stabilize GLM DSA config on ROCm
- [#31297](https://github.com/sgl-project/sglang/pull/31297) Default JIT builds to arch-specific target on Hopper+
- [#31303](https://github.com/sgl-project/sglang/pull/31303) Rebuild sgl-deep-gemm wheels for ABI-sensitive PRs
- [#31342](https://github.com/sgl-project/sglang/pull/31342) Disable CUDA IPC multimodal transport on ROCm in MMMU VLM tests
- [#31371](https://github.com/sgl-project/sglang/pull/31371) Remove nightly registrations redundant with scheduled stage runs
- [#31390](https://github.com/sgl-project/sglang/pull/31390) Build HPC-Ops into the GPU image
- [#31396](https://github.com/sgl-project/sglang/pull/31396) Fix runner utilization report undercounting busy time
- [#31400](https://github.com/sgl-project/sglang/pull/31400) Reduce MoE fused gate CI test sweep
- [#31409](https://github.com/sgl-project/sglang/pull/31409) Route PR CI to MI300 runners
- [#31416](https://github.com/sgl-project/sglang/pull/31416) Guard partition consumers against failed check-changes and degenerate fits
- [#31451](https://github.com/sgl-project/sglang/pull/31451) Add DSpark SPS fit diagnostics
- [#31455](https://github.com/sgl-project/sglang/pull/31455) Bisect target-verify CUDA Graph replay synchronization for DSpark

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: c77504ea7b20e9e27ef5f72f129dfff3321bc02fc20b859a173e0aa8b9befd2f -->
