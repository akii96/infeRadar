# vllm: PR digest (2026-06-03 to 2026-06-08)

_181 merged, 298 newly opened - source vllm-project/vllm, generated 2026-06-10T15:53:05Z_

## TL;DR
- **DeepSeek models** dominated attention, with major additions like the TRTLLM generation attention kernel, XPU decode paths, and fused MLA/MoE optimizations for V4.
- **Gemma4** saw significant feature expansion, adding MTP (Multi-Token Prediction) speculative decoding and Unified (encoder-free) multimodal support.
- **Performance & Architecture** took a leap forward with a massive attention backend refactor to standardize KV cache layouts, FusedMoE/MoERunner inversion, and Triton-based NVFP4 / KVarN quantization.
- **Hardware support** broadened via AMD ROCm optimizations (W4A16 HIP kernels, Aiter integration) and Intel XPU enhancements (transparent sleep, block-scaled W8A8).
- **Overall direction** points toward deep optimization of MoE/MLA architectures, disaggregated serving (Nixl/Mooncake connectors), and unified attention backends across diverse hardware.

## Most important PRs
- **[#41184](https://github.com/vllm-project/vllm/pull/41184)** [MoE Refactor] FusedMoE/MoERunner inversion refactor
  Inverts the FusedMoE and MoERunner abstractions to streamline MoE execution across backends (FlashInfer, Triton) and hardware, simplifying the addition of new quantization schemes.
- **[#43827](https://github.com/vllm-project/vllm/pull/43827)** [DSv4] Adding TRTLLM gen attention kernel
  Integrates the TensorRT-LLM generation attention kernel for DeepSeek V4, significantly boosting decode performance for DeepSeek's MLA architecture on AMD and NVIDIA GPUs.
- **[#44580](https://github.com/vllm-project/vllm/pull/44580)** Attention backend refactor
  A massive ongoing overhaul of the attention backend architecture to standardize KV cache layouts and unify FlashInfer and Triton implementations, paving the way for cross-backend optimizations.
- **[#44581](https://github.com/vllm-project/vllm/pull/44581)** [Feature] KVarN: Variance-Normalized KV-Cache Quantization (4-bit K, 2-bit V)
  Introduces a novel variance-normalized KV cache quantization scheme using Triton, aggressively compressing the KV cache footprint while maintaining model quality.
- **[#44891](https://github.com/vllm-project/vllm/pull/44891)** perf: add push-based allreduce for small tensor reductions
  Implements a push-based custom all-reduce kernel for small tensors, reducing communication latency in tensor-parallel setups and directly improving end-to-end decode throughput.

## More changes by area

<details>
<summary>Performance (23)</summary>

- [#44075](https://github.com/vllm-project/vllm/pull/44075) Fused MoE W4A16 HIP kernel for AMD RDNA3 (gfx1100)
- [#44700](https://github.com/vllm-project/vllm/pull/44700) Split mixed prefill+decode batches: route decodes to the recurrent kernel
- [#44251](https://github.com/vllm-project/vllm/pull/44251) Add tuned selective_state_update configs for H200 and RTX PRO
- [#42191](https://github.com/vllm-project/vllm/pull/42191) Apply single-pass min_larger finding and binary search in Triton Top-p path
- [#42212](https://github.com/vllm-project/vllm/pull/42212) Triton fast path for small CPU→GPU swap_blocks_batch in the offloading connector
- [#41759](https://github.com/vllm-project/vllm/pull/41759) Support ViT full CUDA graph for InternVL
- [#44212](https://github.com/vllm-project/vllm/pull/44212) Improve multimodal item handling from O(n) to O(log n) per step
- [#41002](https://github.com/vllm-project/vllm/pull/41002) Use workspace manager for sparse indexer allocations
- [#44400](https://github.com/vllm-project/vllm/pull/44400) Enable W4A16 FlyDSL MoE
- [#44786](https://github.com/vllm-project/vllm/pull/44786) Reduce multimodal preprocessing cache contention
- [#44899](https://github.com/vllm-project/vllm/pull/44899) Flash-decode split-K decode attention kernel
- [#44394](https://github.com/vllm-project/vllm/pull/44394) Add PaddleOCR-VL encoder CUDA graph support
- [#44606](https://github.com/vllm-project/vllm/pull/44606) Maybe improve sparse topk heuristic
- [#44639](https://github.com/vllm-project/vllm/pull/44639) Added tanh AOR for faster gelu activations
- [#44572](https://github.com/vllm-project/vllm/pull/44572) SM90 cutlass fp8 mm supports odd M by swap_ab, 180~290% kernel performance improvement
- [#44584](https://github.com/vllm-project/vllm/pull/44584) Triton unified attention: window-align the KV-tile iteration for sliding-window / chunked attention
- [#44677](https://github.com/vllm-project/vllm/pull/44677) DBO ++: Overlap TP all-reduce with compute
- [#44474](https://github.com/vllm-project/vllm/pull/44474) Optimize multimodal embedding merger with static shape pattern for XLA and CUDA Graphs
- [#44818](https://github.com/vllm-project/vllm/pull/44818) Add H200 BF16 fused MoE configs for Gemma4 (E=128,N=704)
- [#44594](https://github.com/vllm-project/vllm/pull/44594) Add kvcache watermark to reduce preemptions
- [#44397](https://github.com/vllm-project/vllm/pull/44397) Improve use_cascade_attention mechanism
- [#44524](https://github.com/vllm-project/vllm/pull/44524) Perf/wna16 batched marlin block size
- [#42646](https://github.com/vllm-project/vllm/pull/42646) Add gemma RMS AR fusion

</details>

<details>
<summary>Kernels & attention (39)</summary>

- [#42953](https://github.com/vllm-project/vllm/pull/42953) Add DeepSeek-V4 XPU attention decode path
- [#44569](https://github.com/vllm-project/vllm/pull/44569) Refactor DeepseekV4Attention
- [#43556](https://github.com/vllm-project/vllm/pull/43556) Mamba attention module refactor - LINEAR
- [#44365](https://github.com/vllm-project/vllm/pull/44365) Migrate custom all-reduce, DeepSeek V4 fused MLA, MiniMax reduce-RMS, and MXFP8 MoE to libtorch stable ABI
- [#44699](https://github.com/vllm-project/vllm/pull/44699) Decouple DS V4 Sparse MLA Metadata from DS V3.2
- [#40426](https://github.com/vllm-project/vllm/pull/40426) Integrate Aiter hipBLASLt GEMM online tuning
- [#44471](https://github.com/vllm-project/vllm/pull/44471) Add unit tests for pooler head classes
- [#44230](https://github.com/vllm-project/vllm/pull/44230) Optimize the compressor 128 split cutedsl kernel
- [#44334](https://github.com/vllm-project/vllm/pull/44334) Migrate cuda_view and silu_and_mul_per_block_quant kernels to torch stale ABI
- [#42758](https://github.com/vllm-project/vllm/pull/42758) Enable perf_token_group_quant/_C_stable_libtorch for ROCm
- [#42443](https://github.com/vllm-project/vllm/pull/42443) Refactor CT NVFP4 linear to use a single class
- [#40470](https://github.com/vllm-project/vllm/pull/40470) Extract KV-cache update from CPU attention backend
- [#44561](https://github.com/vllm-project/vllm/pull/44561) Move more ops out of eager breakpoint
- [#42838](https://github.com/vllm-project/vllm/pull/42838) Replace torch.cat in sparse-MLA forward_mqa with fused concat_mla_q
- [#44393](https://github.com/vllm-project/vllm/pull/44393) Standardize kv layout to blocks first
- [#44674](https://github.com/vllm-project/vllm/pull/44674) Enable permute_cols for ROCm
- [#43759](https://github.com/vllm-project/vllm/pull/43759) Fallback to TRITON_ATTN for vit attn on xpu when use float32 dtype
- [#44805](https://github.com/vllm-project/vllm/pull/44805) Added extra_repr() to pooler classes to improve debuggability
- [#44458](https://github.com/vllm-project/vllm/pull/44458) Standardize KV cache layout
- [#44501](https://github.com/vllm-project/vllm/pull/44501) Quant Scaled MM Per (Tensor/token/channel) FP8/INT8 kernel in CuTeDSL
- [#44573](https://github.com/vllm-project/vllm/pull/44573) Add DeepSeek-V4 DCP decode support
- [#44570](https://github.com/vllm-project/vllm/pull/44570) Combine CompressedTensorsWNA16MarlinMoEMethod with CompressedTensorsWNA16MoEMethod
- [#44459](https://github.com/vllm-project/vllm/pull/44459) Benchmark Helion scaled_mm vs cutlass
- [#44544](https://github.com/vllm-project/vllm/pull/44544) AITER FP8 ASM prefill backend
- [#44857](https://github.com/vllm-project/vllm/pull/44857) Mamba attention module refactor - Final part
- [#44455](https://github.com/vllm-project/vllm/pull/44455) Pack K/V into the content dim across attention backends
- [#44449](https://github.com/vllm-project/vllm/pull/44449) Lwilkinson/kv layout/kv content pack
- [#44518](https://github.com/vllm-project/vllm/pull/44518) Use native packed audio attention for Qwen2.5-Omni to remove standalone flash-attn dependency
- [#44583](https://github.com/vllm-project/vllm/pull/44583) Per-region KV transfer classes for mixed full-attn + MLA groups
- [#44810](https://github.com/vllm-project/vllm/pull/44810) Add optional torchembed RoPE backend
- [#44685](https://github.com/vllm-project/vllm/pull/44685) Add cute helion kernel
- [#44456](https://github.com/vllm-project/vllm/pull/44456) Standardize Mamba cache; drop get_transfer_cache_regions
- [#44385](https://github.com/vllm-project/vllm/pull/44385) Add unit test for chunk_local_cumsum kernels
- [#44381](https://github.com/vllm-project/vllm/pull/44381) Refactor RMSNorm vectorized launch checks
- [#44604](https://github.com/vllm-project/vllm/pull/44604) Optimize fused_add_rms_norm with software pipelining
- [#44733](https://github.com/vllm-project/vllm/pull/44733) Parallel-agnostic fs-tier cache for single full-attention group
- [#44623](https://github.com/vllm-project/vllm/pull/44623) Triton version of SiluAndMulWithClamp
- [#44738](https://github.com/vllm-project/vllm/pull/44738) Optimize rotary embedding cache length
- [#44849](https://github.com/vllm-project/vllm/pull/44849) Dispatch fused QK-norm + AllReduce via AITER

</details>

<details>
<summary>MoE & quantization (29)</summary>

- [#44340](https://github.com/vllm-project/vllm/pull/44340) Support compressed-tensors WNA8O8Int linears and WNInt embeddings
- [#43167](https://github.com/vllm-project/vllm/pull/43167) Remove KV cache scale boilerplate from model weight loading methods
- [#34894](https://github.com/vllm-project/vllm/pull/34894) Add INT8 W4A8 docs and Arm's supported quantization schemes
- [#42832](https://github.com/vllm-project/vllm/pull/42832) Fuse RoPE + static Q FP8 quant on fused RoPE+KV path
- [#44132](https://github.com/vllm-project/vllm/pull/44132) Add online fp8 ptpc
- [#39968](https://github.com/vllm-project/vllm/pull/39968) Add XPU block-scaled W8A8 fp8 path
- [#42139](https://github.com/vllm-project/vllm/pull/42139) Support block_fp8_moe on xpu
- [#44771](https://github.com/vllm-project/vllm/pull/44771) Format moe kernel name and add in kernel list
- [#44122](https://github.com/vllm-project/vllm/pull/44122) Remove dead code fp quant
- [#44367](https://github.com/vllm-project/vllm/pull/44367) Minor cleanup for DeepseekV4MegaMoEExperts
- [#44540](https://github.com/vllm-project/vllm/pull/44540) Add xpu branch in compressed_tensors_moe_w4a4_mxfp4
- [#44389](https://github.com/vllm-project/vllm/pull/44389) Add Triton software NVFP4 KV cache support
- [#44437](https://github.com/vllm-project/vllm/pull/44437) Fuse RMSNorm + MXFP4 quant via AITER Triton kernels (DeepSeek-R1)
- [#44565](https://github.com/vllm-project/vllm/pull/44565) Start Migrate MoE kernels to torch stable ABI
- [#44681](https://github.com/vllm-project/vllm/pull/44681) Remove dead cutlass mxfp8 code
- [#44667](https://github.com/vllm-project/vllm/pull/44667) Fuse NVFP4 weight dequantization with compute in triton kernel for w13/w2 MOE MLP linears
- [#44834](https://github.com/vllm-project/vllm/pull/44834) Route Int8 MoE inference through zentorch on AMD
- [#44564](https://github.com/vllm-project/vllm/pull/44564) SQuat: Subspace-orthogonal KV Cache Quantization
- [#44851](https://github.com/vllm-project/vllm/pull/44851) Add SM120 NVFP4 KV cache support
- [#44562](https://github.com/vllm-project/vllm/pull/44562) Refactor MoE Oracles to use base class MoEKernelOracle
- [#44514](https://github.com/vllm-project/vllm/pull/44514) Deprecate old FP8 online quantization classes
- [#44452](https://github.com/vllm-project/vllm/pull/44452) Delegate finalize output-buffer allocation to prepare_finalize
- [#44924](https://github.com/vllm-project/vllm/pull/44924) Fused MoE design doc
- [#44553](https://github.com/vllm-project/vllm/pull/44553) Add H20-3e FP8 fused-MoE tuned config for E=256,N=512 (Qwen3.6 A3B)
- [#44675](https://github.com/vllm-project/vllm/pull/44675) Add tuned fused_moe config for Nemotron-Super on H200
- [#44932](https://github.com/vllm-project/vllm/pull/44932) Add FP8 KV Cache + FP8 Prefill support with Flashinfer Backend + DCP
- [#44763](https://github.com/vllm-project/vllm/pull/44763) Add weights padding for fp8 per-block online quantization
- [#44523](https://github.com/vllm-project/vllm/pull/44523) Add missing scalar fallback for CPU W4A8 INT4 GEMM
- [#44478](https://github.com/vllm-project/vllm/pull/44478) Enable oneDNN W8A8 INT8 to run on RISC-V

</details>

<details>
<summary>Model support (16)</summary>

- [#44429](https://github.com/vllm-project/vllm/pull/44429) Add Gemma4 Unified (encoder-free) support
- [#44417](https://github.com/vllm-project/vllm/pull/44417) Implement glm46v video loader
- [#43519](https://github.com/vllm-project/vllm/pull/43519) Add model support for granite speech plus
- [#44609](https://github.com/vllm-project/vllm/pull/44609) Support MiniCPMV batched preprocessing
- [#44435](https://github.com/vllm-project/vllm/pull/44435) Add Llama-3.2-3B-Instruct to batch-invariance tested models
- [#44707](https://github.com/vllm-project/vllm/pull/44707) Enable Cohere Mini Code model and update Command A-plus test registry
- [#44588](https://github.com/vllm-project/vllm/pull/44588) Add Command A plus tags for structural tags
- [#44785](https://github.com/vllm-project/vllm/pull/44785) Add LLaVA-OneVision-2 (LlavaOnevision2ForConditionalGeneration)
- [#44787](https://github.com/vllm-project/vllm/pull/44787) Optimize Qwen3-VL image-only preprocessing with compact patches
- [#44776](https://github.com/vllm-project/vllm/pull/44776) Add video modality support for vllm-rs
- [#44930](https://github.com/vllm-project/vllm/pull/44930) Add encoder CUDA graph support to Lfm2VL
- [#44792](https://github.com/vllm-project/vllm/pull/44792) Add Orthrus model support
- [#44590](https://github.com/vllm-project/vllm/pull/44590) Add Thor selective state update configs
- [#44720](https://github.com/vllm-project/vllm/pull/44720) Add Qwen3.6 (dense + MoE) to multimodal ViT CUDA graph support
- [#44412](https://github.com/vllm-project/vllm/pull/44412) Add Qwen3-VL video loader
- [#44598](https://github.com/vllm-project/vllm/pull/44598) Optimize sparse frames decoding for PyAV video backend

</details>

<details>
<summary>Parallelism & scheduling (28)</summary>

- [#44854](https://github.com/vllm-project/vllm/pull/44854) Remove P2pNcclConnector
- [#37505](https://github.com/vllm-project/vllm/pull/37505) Support Pluggable KVCacheSpec
- [#41968](https://github.com/vllm-project/vllm/pull/41968) Add objectstore as a secondary tier to multi-tier kv cache offloading
- [#41980](https://github.com/vllm-project/vllm/pull/41980) Use split_group for pytorch process group creation
- [#41633](https://github.com/vllm-project/vllm/pull/41633) Nixl communicator optimization. Zero-copy transfers
- [#43720](https://github.com/vllm-project/vllm/pull/43720) PP-aware handshake aggregation and intermediate-PP output plumbing
- [#43874](https://github.com/vllm-project/vllm/pull/43874) Initiate deprecation cycle for kv_both role
- [#42554](https://github.com/vllm-project/vllm/pull/42554) Mamba prefix caching mode support
- [#41471](https://github.com/vllm-project/vllm/pull/41471) Remove dead code in tests and parallel_state
- [#42865](https://github.com/vllm-project/vllm/pull/42865) Update lmcache kv_offloading_backend to use LMCacheMPConnector
- [#44454](https://github.com/vllm-project/vllm/pull/44454) Refactor DSV4 KV cache config construction
- [#44287](https://github.com/vllm-project/vllm/pull/44287) Enable HMA models for Tiering Offloading
- [#44661](https://github.com/vllm-project/vllm/pull/44661) Slice_tp_for_transfer
- [#44876](https://github.com/vllm-project/vllm/pull/44876) QKV-split + QK-RMSNorm + RoPE + KV-cache-write fusion
- [#44848](https://github.com/vllm-project/vllm/pull/44848) Enable KimiLinear (KDA/GDN + MLA) PD Separation via NIXL
- [#44794](https://github.com/vllm-project/vllm/pull/44794) FlowPrefill: adaptive sub-chunk preemption for v1 Scheduler
- [#44865](https://github.com/vllm-project/vllm/pull/44865) Reshape the transfer data model: per group specs and offloaded side alignment offset
- [#44528](https://github.com/vllm-project/vllm/pull/44528) Pipeline-parallel support for PD-disaggregated serving with Mooncake connector
- [#44428](https://github.com/vllm-project/vllm/pull/44428) Add fault tolerance framework (simplified) for DP+EP external LB deployments
- [#44915](https://github.com/vllm-project/vllm/pull/44915) Migrate DP Supervisor from Python to Rust
- [#44577](https://github.com/vllm-project/vllm/pull/44577) Pack KV caches into contiguous per-block allocations for DeepSeek V4
- [#44919](https://github.com/vllm-project/vllm/pull/44919) Auto-discover compatible RDMA devices for Mooncake Connector
- [#44558](https://github.com/vllm-project/vllm/pull/44558) Add prefill step cadence for better non-PD DP balancing
- [#44541](https://github.com/vllm-project/vllm/pull/44541) Implement reset_cache for TieringOffloadingManager
- [#44791](https://github.com/vllm-project/vllm/pull/44791) Add prefix-length threshold for lazy SimpleCPUOffloadConnector
- [#44432](https://github.com/vllm-project/vllm/pull/44432) Extract _bucket_layers_by_page_size from DSV4 KV cache config
- [#44774](https://github.com/vllm-project/vllm/pull/44774) Mooncake store: prefix-cache retention interval for sparse attention
- [#44636](https://github.com/vllm-project/vllm/pull/44636) Move DP sync to a dedicated CUDA stream

</details>

<details>
<summary>Speculative decoding (15)</summary>

- [#43241](https://github.com/vllm-project/vllm/pull/43241) Add Gemma4 MTP support
- [#44420](https://github.com/vllm-project/vllm/pull/44420) Add index share feature for DSA MTP
- [#44595](https://github.com/vllm-project/vllm/pull/44595) usage_stats: report more engine, spec-decode, and EP config
- [#44419](https://github.com/vllm-project/vllm/pull/44419) Warn about throughput loss when libiomp5 is not preloaded
- [#44880](https://github.com/vllm-project/vllm/pull/44880) Support MTP speculative decoding for Bailing hybrid models
- [#44698](https://github.com/vllm-project/vllm/pull/44698) Support MTP speculative decoding under pipeline parallelism (PP>1)
- [#44586](https://github.com/vllm-project/vllm/pull/44586) DFlash
- [#44453](https://github.com/vllm-project/vllm/pull/44453) Sharded rejection sampling
- [#44816](https://github.com/vllm-project/vllm/pull/44816) Support peagle spec decode
- [#44673](https://github.com/vllm-project/vllm/pull/44673) Add speculative decoding correctness gate
- [#44597](https://github.com/vllm-project/vllm/pull/44597) Add global cache scope for ngram prompt lookup
- [#44723](https://github.com/vllm-project/vllm/pull/44723) Add MTP (Multi-Token Prediction) draft model support
- [#44510](https://github.com/vllm-project/vllm/pull/44510) Support thinking_token_budget for mrv2
- [#44487](https://github.com/vllm-project/vllm/pull/44487) Add per-request acceptance rate Prometheus histogram
- [#44652](https://github.com/vllm-project/vllm/pull/44652) Non-causal support + relax 3D-launch gate for multi-query verify in unified attention

</details>

<details>
<summary>API & serving (40)</summary>

- [#43778](https://github.com/vllm-project/vllm/pull/43778) Add dynamic LoRA endpoints
- [#44479](https://github.com/vllm-project/vllm/pull/44479) Consolidate online serving utils
- [#43447](https://github.com/vllm-project/vllm/pull/43447) Support selective prefix-cache retention for sliding-window KV cache
- [#44391](https://github.com/vllm-project/vllm/pull/44391) Support include_reasoning=false
- [#43942](https://github.com/vllm-project/vllm/pull/43942) Add /server_info to Rust frontend
- [#44499](https://github.com/vllm-project/vllm/pull/44499) Add /pause, /resume, /is_paused endpoints
- [#44213](https://github.com/vllm-project/vllm/pull/44213) Add Phi-4 mini JSON tool parser
- [#44856](https://github.com/vllm-project/vllm/pull/44856) Refine utility call interfaces
- [#44500](https://github.com/vllm-project/vllm/pull/44500) Skip loading multimodal processor if `--language-model-only` is specified
- [#44244](https://github.com/vllm-project/vllm/pull/44244) Enable reasoning-model (thinking) benchmarking via `--chat-template-kwargs` for client-rendered datasets
- [#44708](https://github.com/vllm-project/vllm/pull/44708) Auto-detect and correct client/server tokenizer mismatch for random dataset
- [#42453](https://github.com/vllm-project/vllm/pull/42453) Support batch invariant rms norm with residual
- [#43774](https://github.com/vllm-project/vllm/pull/43774) Add server router extension hook
- [#44539](https://github.com/vllm-project/vllm/pull/44539) Unify KDA conv states into one cache to match 2-state SSM layout
- [#44442](https://github.com/vllm-project/vllm/pull/44442) Remove FlashInfer version check in topk_topp_sampler
- [#44363](https://github.com/vllm-project/vllm/pull/44363) Freeze garbage collector in workers after model initialization
- [#44530](https://github.com/vllm-project/vllm/pull/44530) Add ColBERT embedding_mode for asymmetric query/document encoding
- [#44445](https://github.com/vllm-project/vllm/pull/44445) Add OpenAI-compatible online Batch and Files API
- [#44713](https://github.com/vllm-project/vllm/pull/44713) Add Granite tool and reasoning parsers
- [#44624](https://github.com/vllm-project/vllm/pull/44624) Add Python bridge for Rust tool parsers
- [#44887](https://github.com/vllm-project/vllm/pull/44887) Populate `cached_token_count` in responses
- [#44535](https://github.com/vllm-project/vllm/pull/44535) Support multiple profiling windows
- [#44404](https://github.com/vllm-project/vllm/pull/44404) Get Detailed MultiModal Data Preprocessing Timing Stats
- [#44664](https://github.com/vllm-project/vllm/pull/44664) Support required function tools for GPT-OSS Harmony
- [#44938](https://github.com/vllm-project/vllm/pull/44938) Support prompt-only completions
- [#44587](https://github.com/vllm-project/vllm/pull/44587) Add Long Audio benchmark and correctness test
- [#44900](https://github.com/vllm-project/vllm/pull/44900) Add --root-path support for reverse proxy routing
- [#44853](https://github.com/vllm-project/vllm/pull/44853) Add Rust frontend contributor guide
- [#44890](https://github.com/vllm-project/vllm/pull/44890) Add release_kv_cache() API
- [#44760](https://github.com/vllm-project/vllm/pull/44760) Support parallel_tool_calls
- [#44633](https://github.com/vllm-project/vllm/pull/44633) Add APC prefix cache hit rate to PD usage details
- [#44402](https://github.com/vllm-project/vllm/pull/44402) Implement fine-grained timing spans for requests
- [#44822](https://github.com/vllm-project/vllm/pull/44822) Feature/cache accounting OpenAI anthropic api
- [#44382](https://github.com/vllm-project/vllm/pull/44382) Add /abort_requests endpoint
- [#44475](https://github.com/vllm-project/vllm/pull/44475) Add prefix cache hit rate to usage details
- [#44612](https://github.com/vllm-project/vllm/pull/44612) Optimize CPU preproc to get 2.5x RTFx via multi-threading
- [#44512](https://github.com/vllm-project/vllm/pull/44512) Consolidate scale out entrypoints
- [#44872](https://github.com/vllm-project/vllm/pull/44872) Add AI Badgr hosted GPU deployment option
- [#44801](https://github.com/vllm-project/vllm/pull/44801) Add `/get_world_size` route with static parallel size
- [#44922](https://github.com/vllm-project/vllm/pull/44922) Add vllm:request_received counter labeled by input modality

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#37149](https://github.com/vllm-project/vllm/pull/37149) Transparent sleep mode support for XPU platform
- [#43689](https://github.com/vllm-project/vllm/pull/43689) Align blocks to page-size
- [#36423](https://github.com/vllm-project/vllm/pull/36423) Support cpu kv offloading and tiering offloading on XPU platform
- [#43838](https://github.com/vllm-project/vllm/pull/43838) Add is_cumem_allocator_available
- [#44465](https://github.com/vllm-project/vllm/pull/44465) Vram semaphore infra

</details>

<details>
<summary>Bugfixes (121)</summary>

- [#43150](https://github.com/vllm-project/vllm/pull/43150) Fix FP64 Gumbel precision coverage
- [#44330](https://github.com/vllm-project/vllm/pull/44330) GPT-OSS instruction rendering
- [#44311](https://github.com/vllm-project/vllm/pull/44311) Fix several hf chat template rendering issues
- [#44560](https://github.com/vllm-project/vllm/pull/44560) Resolve multiple async kv load deadlock
- [#44450](https://github.com/vllm-project/vllm/pull/44450) Fix mrv2 mm lora issue
- [#44559](https://github.com/vllm-project/vllm/pull/44559) Add fetch_audio to MistralCommonFeatureExtractor (transformers>=5.10 compat)
- [#44648](https://github.com/vllm-project/vllm/pull/44648) Fallback to regular abi for ROCm
- [#44493](https://github.com/vllm-project/vllm/pull/44493) Fix Kimi-K2.5 FlashInfer ViT metadata
- [#44103](https://github.com/vllm-project/vllm/pull/44103) Fix per-group block_size/block_hash and group_idx in MooncakeStoreConnector KV events
- [#44253](https://github.com/vllm-project/vllm/pull/44253) Warmup & capture with different attention states for speculator prefill
- [#44410](https://github.com/vllm-project/vllm/pull/44410) Fix VLLMNotFoundError when using LoRA adapter name in pooling
- [#44509](https://github.com/vllm-project/vllm/pull/44509) MiniCPM-V-4.6 video inference crash: placeholder count mismatches visual embedding count
- [#39562](https://github.com/vllm-project/vllm/pull/39562) Fix assertion in MambaManager.allocate_slots()
- [#44347](https://github.com/vllm-project/vllm/pull/44347) Update TrtLLM MoE routing methods
- [#42752](https://github.com/vllm-project/vllm/pull/42752) Honor tool_choice="none" in Chat Completions streaming
- plus 106 more minor bugfixes

</details>

<details>
<summary>Refactors (3)</summary>

- [#43707](https://github.com/vllm-project/vllm/pull/43707) Optimize shutdown logs, easier to follow and consistent
- [#44346](https://github.com/vllm-project/vllm/pull/44346) Suppress SyntaxWarning from ast.literal_eval in tool parsers
- [#44589](https://github.com/vllm-project/vllm/pull/44589) Remove unnecessary `load_weights` methods

</details>

<details>
<summary>Tests, CI & build (45)</summary>

- [#36949](https://github.com/vllm-project/vllm/pull/36949) Optimize ROCm Docker build: registry cache, DeepEP, and ci-bake script
- [#44635](https://github.com/vllm-project/vllm/pull/44635) Speed up docs build
- [#44436](https://github.com/vllm-project/vllm/pull/44436) Add test for Aiter unified attn kernel
- [#42793](https://github.com/vllm-project/vllm/pull/42793) Stage C mirrors
- [#43663](https://github.com/vllm-project/vllm/pull/43663) Add more test cases in Intel GPU CI
- [#44761](https://github.com/vllm-project/vllm/pull/44761) Stabilizing teardown and timeout of flaky tests to prevent rare OOMs
- [#44669](https://github.com/vllm-project/vllm/pull/44669) Allow DP ray placement groups to be set on specific nodes
- [#44819](https://github.com/vllm-project/vllm/pull/44819) Consolidate multimodal entrypoint tests
- [#44591](https://github.com/vllm-project/vllm/pull/44591) Batch auto-abort requests by engine
- [#44046](https://github.com/vllm-project/vllm/pull/44046) Stabilize memory-release in the Hybrid model generation tests
- plus 35 more minor CI updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
