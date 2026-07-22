# vllm: PR digest (2026-07-05 to 2026-07-09)

_195 merged, 282 newly opened - source vllm-project/vllm, generated 2026-07-09T12:08:27Z_

## TL;DR
- **Model focus**: DeepSeek dominated attention (V3.2/V4), with major optimizations for MLA, NVFP4, and FlashInfer integration. Mistral, Qwen, and Llama also saw targeted fixes and speculative decoding improvements.
- **Performance & Kernels**: Significant throughput wins via the Helion kernel for block quantization, TRTLLM BF16 MoE modular kernels, and sequence parallelism without DP. AMD ROCm saw major AITER and TurboQuant KV cache optimizations.
- **Architecture & Speculative Decoding**: Heavy investment in MTP and DSpark speculative decoding, including hybrid drafters and dynamic scheduling.
- **Frontend & Multimodal**: The Rust frontend is expanding with video modality support and beam search. Multimodal added TorchCodec video decoding and paged shared memory storage.
- **Overall Direction**: The engine is rapidly maturing its hardware-specific fast paths (NVIDIA NVFP4/FlashInfer, AMD AITER, Intel XPU) while overhauling the frontend (Rust) and expanding video/multimodal capabilities.

## Most important PRs
- **[#43994](https://github.com/vllm-project/vllm/pull/43994)** Add Helion kernel for silu_and_mul_per_block_quant: Introduces the Helion kernel for block quantization, providing a foundational performance boost for quantized models on NVIDIA hardware.
- **[#41652](https://github.com/vllm-project/vllm/pull/41652)** Add humming moe backend to all dense/moe oracles: Integrates the Humming MoE backend across dense and MoE oracles, improving kernel performance for quantized MoE models on NVIDIA GPUs.
- **[#44880](https://github.com/vllm-project/vllm/pull/44880)** Support MTP speculative decoding for Bailing hybrid models: Adds Multi-Token Prediction (MTP) speculative decoding support, expanding the engine's capability to accelerate hybrid architectures.
- **[#47796](https://github.com/vllm-project/vllm/pull/47796)** Port ATOM attention into vLLM for ROCm DeepSeek V4: Begins porting ATOM attention for DeepSeek V4 on AMD ROCm, a massive 12k+ line effort to optimize single-node decode performance.
- **[#47941](https://github.com/vllm-project/vllm/pull/47941)** P2P NIXL + CPU EC Connector: Introduces a generic P2P secondary tier for KV cache offloading, enabling peer lookup and serving via a new `ParentManager` abstraction.

## More changes by area

<details>
<summary>Performance (27)</summary>

- [#46065](https://github.com/vllm-project/vllm/pull/46065) Directly Implement AITER Custom All-reduce in CudaCommunicator
- [#45182](https://github.com/vllm-project/vllm/pull/45182) Integrate TRTLLM BF16 MoE Modular Kernel
- [#47416](https://github.com/vllm-project/vllm/pull/47416) Add fused Kimi image preprocessing
- [#46117](https://github.com/vllm-project/vllm/pull/46117) MXFP8 dense-linear + grouped-MoE GEMM optimizations for MiniMax-M3
- [#45672](https://github.com/vllm-project/vllm/pull/45672) Bound DiffusionGemma sampler transient via request-tiled logits
- [#47631](https://github.com/vllm-project/vllm/pull/47631) Minimax M3 - Support cross-layer allreduce-norm fusion
- [#47474](https://github.com/vllm-project/vllm/pull/47474) Cache `token_to_req_indices` for dsv4, 5x~6x kernel performance improvement
- [#47070](https://github.com/vllm-project/vllm/pull/47070) Support sequence parallel without the need for DP
- [#47081](https://github.com/vllm-project/vllm/pull/47081) Use blocking CUDA events to avoid busy polling cuda driver lock
- [#47538](https://github.com/vllm-project/vllm/pull/47538) Reduce LMUL pressure in INT4 LUT dequant on RISC-V
- [#47546](https://github.com/vllm-project/vllm/pull/47546) Expand Triton kernel warmup coverage for Qwen
- [#47896](https://github.com/vllm-project/vllm/pull/47896) FlyDSL decode-attention kernel for 4-bit TurboQuant KV cache
- [#48018](https://github.com/vllm-project/vllm/pull/48018) ReplaySSM: cache SSM inputs for faster Mamba2 standard decode
- [#48119](https://github.com/vllm-project/vllm/pull/48119) Support online C128 compression for DeepSeek V4
- [#47979](https://github.com/vllm-project/vllm/pull/47979) SM120 PCIe serving stack: SP/async-TP enablement
- [#47719](https://github.com/vllm-project/vllm/pull/47719) Add Qwen3 AITER fused QKV/RoPE KV-cache path
- [#47757](https://github.com/vllm-project/vllm/pull/47757) Fuse decode QK-RoPE + Q-concat + KV-concat for sparse MLA
- [#47718](https://github.com/vllm-project/vllm/pull/47718) DSv4 two-stage compressor kernel for HCA prefill
- [#47967](https://github.com/vllm-project/vllm/pull/47967) Add KVCrush KV Cache compression for vLLM
- [#47711](https://github.com/vllm-project/vllm/pull/47711) Skip no-op FP32 logits materialization in MRV2
- [#48120](https://github.com/vllm-project/vllm/pull/48120) Stage the postprocess inputs with a single loop over the request list
- [#47985](https://github.com/vllm-project/vllm/pull/47985) Add encoder cache profiling implementation for MRV2
- [#48064](https://github.com/vllm-project/vllm/pull/48064) Enable FlashInfer MNNVL allreduce RMS quant fusion
- [#47622](https://github.com/vllm-project/vllm/pull/47622) Batch KV scale host conversion
- [#47623](https://github.com/vllm-project/vllm/pull/47623) Avoid redundant logprobs list materialization
- [#48110](https://github.com/vllm-project/vllm/pull/48110) Vectorize _copy_mamba_state_block to uint64 for temporal
- [#47842](https://github.com/vllm-project/vllm/pull/47842) Avoid extra reshape kernel in Qwen GDN output projection
</details>

<details>
<summary>Kernels & attention (17)</summary>

- [#47502](https://github.com/vllm-project/vllm/pull/47502) Use tok_sparse_select from MSA instead of triton kernels for Minimax-M3
- [#46942](https://github.com/vllm-project/vllm/pull/46942) Enable mm prefix bidi attention support on MRV2
- [#47433](https://github.com/vllm-project/vllm/pull/47433) HPC_ATTN backend support mtp and dynamic scheduled attention
- [#47408](https://github.com/vllm-project/vllm/pull/47408) Applies routed_scaling_factor internally
- [#43597](https://github.com/vllm-project/vllm/pull/43597) Pass None for unused args in unified attention TD path
- [#47629](https://github.com/vllm-project/vllm/pull/47629) TRITON_MLA_SPARSE backend for SM80/SM121 sparse MLA
- [#48024](https://github.com/vllm-project/vllm/pull/48024) Composite Attention Backends
- [#47942](https://github.com/vllm-project/vllm/pull/47942) Add sparse MLA topology index policy and benchmark
- [#47826](https://github.com/vllm-project/vllm/pull/47826) MLA prefill NVFP4 fused output
- [#47973](https://github.com/vllm-project/vllm/pull/47973) BF16x3 router GEMM
- [#47972](https://github.com/vllm-project/vllm/pull/47972) Support DeepSeek-V4 NVFP4 with emulation kernel
- [#48012](https://github.com/vllm-project/vllm/pull/48012) Allow selecting a different attention backend per KV-cache group
- [#47672](https://github.com/vllm-project/vllm/pull/47672) Enable gluon paged attention decode kernel with shuffle KV cache
- [#47665](https://github.com/vllm-project/vllm/pull/47665) Enable fp8 index cache on the Triton indexer for Minimax-M3
- [#47915](https://github.com/vllm-project/vllm/pull/47915) Enable TokenSpeed MLA DCP decode
- [#47799](https://github.com/vllm-project/vllm/pull/47799) Add Helion eager call-site routing + route per_token_group_fp8_quant
- [#47850](https://github.com/vllm-project/vllm/pull/47850) Return the lse across node in flasmla_sparse
</details>

<details>
<summary>MoE & quantization (12)</summary>

- [#43328](https://github.com/vllm-project/vllm/pull/43328) Enable B12x backend for non-gated MoEs
- [#47427](https://github.com/vllm-project/vllm/pull/47427) FI autotuning: max bucket = max token count
- [#46661](https://github.com/vllm-project/vllm/pull/46661) Allow FlashInfer A2A backends for TRTLLM FP8 MoE Modular
- [#47742](https://github.com/vllm-project/vllm/pull/47742) Add NexusQuant E8 lattice KV cache quantization backend
- [#47939](https://github.com/vllm-project/vllm/pull/47939) Integrate NVFP4 MegaMoE for GLM 5.2
- [#47948](https://github.com/vllm-project/vllm/pull/47948) Add flashinfer.moe_ep NCCL-EP all2all backends
- [#47732](https://github.com/vllm-project/vllm/pull/47732) Add FP8 W8A8 Block kernel configs for NVIDIA GeForce RTX 4090D
- [#47674](https://github.com/vllm-project/vllm/pull/47674) NVFP4 W4A16: fall back to weight-only emulation when Marlin is unavailable
- [#47727](https://github.com/vllm-project/vllm/pull/47727) Support Quark AWQ exported models in AutoAWQConfig
- [#48044](https://github.com/vllm-project/vllm/pull/48044) Fused Shared Expert Support for AMD Quark DeepSeek-V4 Model Checkpoints
- [#47881](https://github.com/vllm-project/vllm/pull/47881) Migrate moe sp support to non-torch compiled path for GLM5.2
- [#47851](https://github.com/vllm-project/vllm/pull/47851) Bound peak memory when repacking FP4 MoE weights for Marlin
</details>

<details>
<summary>Model support (15)</summary>

- [#47729](https://github.com/vllm-project/vllm/pull/47729) Support MOSS-Transcribe-Diarize
- [#47872](https://github.com/vllm-project/vllm/pull/47872) Use native transformers processor and adapt to transformers 5.13 for HunyuanVL
- [#46609](https://github.com/vllm-project/vllm/pull/46609) Add TorchCodec as a video decoding backend
- [#47745](https://github.com/vllm-project/vllm/pull/47745) Enable causal masking for SWA in speculators models
- [#48088](https://github.com/vllm-project/vllm/pull/48088) Paged shared memory storage for multimodal
- [#47708](https://github.com/vllm-project/vllm/pull/47708) Gigachat 3.5 support
- [#47957](https://github.com/vllm-project/vllm/pull/47957) Add Shuka-1 model support
- [#48083](https://github.com/vllm-project/vllm/pull/48083) Add Confident Decoding (phase 1: Llama + core utilities)
- [#47857](https://github.com/vllm-project/vllm/pull/47857) Add LongCat-Flash-Lite (n-gram embedding)
- [#47664](https://github.com/vllm-project/vllm/pull/47664) Native word-level timestamps for Whisper
- [#47750](https://github.com/vllm-project/vllm/pull/47750) Add VidCom2 video token pruning
- [#47856](https://github.com/vllm-project/vllm/pull/47856) Add video decode cache
- [#47625](https://github.com/vllm-project/vllm/pull/47625) Support ViT full CUDA graph for Idefics3 and SmolVLM
- [#47991](https://github.com/vllm-project/vllm/pull/47991) Add RobertaForTokenClassification / XLMRobertaForTokenClassification
- [#47660](https://github.com/vllm-project/vllm/pull/47660) Add EuroBERT embedding model
</details>

<details>
<summary>Parallelism & scheduling (29)</summary>

- [#45880](https://github.com/vllm-project/vllm/pull/45880) Support pipeline-parallel prefill in push mode
- [#47274](https://github.com/vllm-project/vllm/pull/47274) Add `ParentManager` ABC for secondary tier callbacks
- [#47823](https://github.com/vllm-project/vllm/pull/47823) Simplify offload-completion barrier
- [#47914](https://github.com/vllm-project/vllm/pull/47914) Support hybrid (SWA + full attention) DFlash drafters
- [#46544](https://github.com/vllm-project/vllm/pull/46544) Establish tier-owned KV event handling
- [#47063](https://github.com/vllm-project/vllm/pull/47063) Support workload identity for objectstore secondary tier
- [#45963](https://github.com/vllm-project/vllm/pull/45963) Disable dynamic speculative decoding when DP is enabled
- [#47420](https://github.com/vllm-project/vllm/pull/47420) Rotate load-balancer tie-break to avoid systematic engine bias
- [#47849](https://github.com/vllm-project/vllm/pull/47849) Add free block iterator for CPU offload scheduling
- [#47759](https://github.com/vllm-project/vllm/pull/47759) Experimental Qwen3.6 TP3/DCP3 research and DFlash hooks
- [#47809](https://github.com/vllm-project/vllm/pull/47809) Add artifact transfer connector for rollout artifacts
- [#47924](https://github.com/vllm-project/vllm/pull/47924) Compile the decode step e2e incl. KV-cache management
- [#47663](https://github.com/vllm-project/vllm/pull/47663) Stock aot_compile driver: alternate to eval-frame stock torch.compile
- [#48021](https://github.com/vllm-project/vllm/pull/48021) Generic P2P secondary tier: peer lookup and serving via ParentManager
- [#47808](https://github.com/vllm-project/vllm/pull/47808) DSpark capacity reallocation without sampler padding
- [#47984](https://github.com/vllm-project/vllm/pull/47984) Support speculative decode with AITER sparse PA for MiniMax-M3
- [#47981](https://github.com/vllm-project/vllm/pull/47981) Support attention-HMA PP prefill in NixlPushConnector
- [#47806](https://github.com/vllm-project/vllm/pull/47806) Add custom all-reduce suspend hooks for NVIDIA
- [#48042](https://github.com/vllm-project/vllm/pull/48042) Stateful Trainer Send: New Abstractions
- [#47885](https://github.com/vllm-project/vllm/pull/47885) Grammar-aware draft token sampling for structured outputs
- [#47782](https://github.com/vllm-project/vllm/pull/47782) Preserve Marconi caching with selective hybrid cache retention
- [#47686](https://github.com/vllm-project/vllm/pull/47686) Pack PP sampled/counts/draft broadcast into one NCCL op per step
- [#47636](https://github.com/vllm-project/vllm/pull/47636) Well-known default host/port env vars and per-DP-rank control port for KVOffload
- [#47677](https://github.com/vllm-project/vllm/pull/47677) Add DSpark speculative decoding support for DeepSeek-V4
- [#47923](https://github.com/vllm-project/vllm/pull/47923) Emit tier-owned BlockStored events from FS/OBJ secondary tiers
- [#47627](https://github.com/vllm-project/vllm/pull/47627) Domino head for dflash
- [#47837](https://github.com/vllm-project/vllm/pull/47837) Priority-aware KV cache eviction for priority scheduling
- [#48069](https://github.com/vllm-project/vllm/pull/48069) Add tenant ID support to MooncakeStoreConnector
- [#47997](https://github.com/vllm-project/vllm/pull/47997) Add Medusa draft model support
</details>

<details>
<summary>Hardware & arch (17)</summary>

- [#35059](https://github.com/vllm-project/vllm/pull/35059) Add CPU support for Mamba ShortConv
- [#47321](https://github.com/vllm-project/vllm/pull/47321) Optimize math functions of VSX power
- [#46361](https://github.com/vllm-project/vllm/pull/46361) Direct Register Custom Op for ARK on Intel XPU
- [#47685](https://github.com/vllm-project/vllm/pull/47685) Align mixed encoder-decoder KV cache views in V2 runner for ROCm
- [#47945](https://github.com/vllm-project/vllm/pull/47945) Add tuned selective_state_update float16 config for AMD Instinct MI300X
- [#47947](https://github.com/vllm-project/vllm/pull/47947) Add tuned selective_state_update float32 config for AMD Instinct MI300X
- [#47767](https://github.com/vllm-project/vllm/pull/47767) Add tuned selective_state_update config for AMD Instinct MI355
- [#47943](https://github.com/vllm-project/vllm/pull/47943) Add tuned selective_state_update float32 config for AMD Instinct MI355
- [#45243](https://github.com/vllm-project/vllm/pull/45243) Enable BF16 on VLEN=256 hardware for RISC-V
- [#47688](https://github.com/vllm-project/vllm/pull/47688) Route mm_prefix models to Triton attention backend on XPU
- [#47731](https://github.com/vllm-project/vllm/pull/47731) Minimize comment in RocmAttention q_scale check
- [#47962](https://github.com/vllm-project/vllm/pull/47962) Disable fuse_rope_kvcache_cat_mla & qk_norm_rope_ fusion on XPU
- [#47765](https://github.com/vllm-project/vllm/pull/47765) Gemma4 ple hpu layout for GAUDI3
- [#47778](https://github.com/vllm-project/vllm/pull/47778) Add MoE DP/EP support for CPU
- [#47641](https://github.com/vllm-project/vllm/pull/47641) Enable granite-4 model on CPU
- [#47921](https://github.com/vllm-project/vllm/pull/47921) Add AMD NPU vision support for Qwen2.5-VL
- [#48015](https://github.com/vllm-project/vllm/pull/48015) Avoid HIP init at config time via lazy aiter import in Quark OCP-MX
</details>

<details>
<summary>API & serving (33)</summary>

- [#47454](https://github.com/vllm-project/vllm/pull/47454) Add endpoint plugins framework
- [#47444](https://github.com/vllm-project/vllm/pull/47444) Cache metric handles for scheduler & request stats in Rust Frontend
- [#46768](https://github.com/vllm-project/vllm/pull/46768) Add per-request timing `metrics` field to response body of Chat/Completions APIs
- [#47024](https://github.com/vllm-project/vllm/pull/47024) Support OpenAI Responses API namespace tools
- [#46718](https://github.com/vllm-project/vllm/pull/46718) Add runtime monitor for post-warmup TileLang compilation
- [#45958](https://github.com/vllm-project/vllm/pull/45958) Add basic offloading metrics
- [#47388](https://github.com/vllm-project/vllm/pull/47388) Persist and reuse the memory-profiling result across boots
- [#47844](https://github.com/vllm-project/vllm/pull/47844) Handle `continue_final_message` with renderer sentinel in Rust Frontend
- [#46415](https://github.com/vllm-project/vllm/pull/46415) Sanitize server file paths from validation error responses
- [#47787](https://github.com/vllm-project/vllm/pull/47787) Stamp `arrival_time` at the frontend entry in Rust Frontend
- [#47581](https://github.com/vllm-project/vllm/pull/47581) Avoid extra copies for multimodal tensors in Rust Frontend
- [#47608](https://github.com/vllm-project/vllm/pull/47608) Add human-readable integer support for more cli-args
- [#47148](https://github.com/vllm-project/vllm/pull/47148) Add `model_class_overrides` for development and debugging
- [#46793](https://github.com/vllm-project/vllm/pull/46793) Support bad_words in the /v1/completions endpoint
- [#38641](https://github.com/vllm-project/vllm/pull/38641) Log worker exit code when process dies unexpectedly
- [#48107](https://github.com/vllm-project/vllm/pull/48107) Port in vllm-bench to Rust
- [#47959](https://github.com/vllm-project/vllm/pull/47959) Integrate MM video support in Rust Frontend
- [#47705](https://github.com/vllm-project/vllm/pull/47705) Beam search support for completions and chat completions in Rust Frontend
- [#47889](https://github.com/vllm-project/vllm/pull/47889) Enable video modality support for Rust frontend
- [#48033](https://github.com/vllm-project/vllm/pull/48033) Add private service foundation for engine-rpc
- [#47810](https://github.com/vllm-project/vllm/pull/47810) Bootstrap the OpenTelemetry trace exporter in Rust Frontend
- [#47703](https://github.com/vllm-project/vllm/pull/47703) Add --sleep-idle-ttl auto-sleep and wake-on-request
- [#48121](https://github.com/vllm-project/vllm/pull/48121) Expose canonical KV cache group metadata
- [#48048](https://github.com/vllm-project/vllm/pull/48048) Session id plumbing into requests
- [#47699](https://github.com/vllm-project/vllm/pull/47699) Overlap preprocessing and computation for pooling models offline inference
- [#47741](https://github.com/vllm-project/vllm/pull/47741) Add Seed-OSS tool parser in Rust Frontend
- [#48070](https://github.com/vllm-project/vllm/pull/48070) First-class session_id for conversation-aware routing
- [#47633](https://github.com/vllm-project/vllm/pull/47633) Emit spec-required gen_ai.operation.name on request spans
- [#47840](https://github.com/vllm-project/vllm/pull/47840) Make HTTP request body limit configurable via VLLM_HTTP_MAX_JSON_BODY_SIZE
- [#48030](https://github.com/vllm-project/vllm/pull/48030) Log fully resolved pooling config at startup
- [#47852](https://github.com/vllm-project/vllm/pull/47852) Support ec_manager
- [#48034](https://github.com/vllm-project/vllm/pull/48034) Tolerate whitespace before the outer brace in JSON tool-call parsers in Rust Frontend
- [#47965](https://github.com/vllm-project/vllm/pull/47965) Wait for mock engine endpoints before ZMQ connect in Rust Frontend
</details>

<details>
<summary>Tests (31)</summary>

- [#47534](https://github.com/vllm-project/vllm/pull/47534) Use lightweight CPU reference and skip heavy cleanup in punica ops tests
- [#47744](https://github.com/vllm-project/vllm/pull/47744) Pass request context to CPU offload cache policy touch
- [#47946](https://github.com/vllm-project/vllm/pull/47946) Skip DeepEP MoE layer tests without P2P access
- [#47619](https://github.com/vllm-project/vllm/pull/47619) Add DeepSeek V3.2 roundtrip fixture in Rust Frontend
- [#47682](https://github.com/vllm-project/vllm/pull/47682) Limit max-num-seqs in test_lmeval.py for XPU
- [#47406](https://github.com/vllm-project/vllm/pull/47406) Skip fork in kv_sharing_fast_prefill test on XPU
- [#47053](https://github.com/vllm-project/vllm/pull/47053) Only materialize tokens when thinking budget is in req
- [#48014](https://github.com/vllm-project/vllm/pull/48014) Move MRV1 `late_interaction_runner.py` out of MRV2 subtree
- [#47748](https://github.com/vllm-project/vllm/pull/47748) Skip test for checkpoint that was deleted
- [#47922](https://github.com/vllm-project/vllm/pull/47922) Native simulator for KV Cache
- [#47964](https://github.com/vllm-project/vllm/pull/47964) Add streaming/non-streaming parity tests for truncated tool calls
- [#47976](https://github.com/vllm-project/vllm/pull/47976) Add unit test for fused_recurrent_gated_delta_rule kernel
- [#47655](https://github.com/vllm-project/vllm/pull/47655) Add unit tests for gemma4_utils
- [#48062](https://github.com/vllm-project/vllm/pull/48062) Cover parallel sampling output kinds
- [#47679](https://github.com/vllm-project/vllm/pull/47679) Split tiering_lookup_delay into sync/async histograms
- [#47862](https://github.com/vllm-project/vllm/pull/47862) Add unit test for decode_attention Triton kernels
- [#47951](https://github.com/vllm-project/vllm/pull/47951) Skip empty-LoRA path in eager mode when no adapter is active
- [#47927](https://github.com/vllm-project/vllm/pull/47927) Preserve DeepSeek sigmoid grouped routing metadata
- [#47899](https://github.com/vllm-project/vllm/pull/47899) Reject unsafe FlashInfer BF16-Q + spec decode + SWA on SM100
- [#48009](https://github.com/vllm-project/vllm/pull/48009) Unify `_logical_to_remote_kernel_block_ids`
- [#47673](https://github.com/vllm-project/vllm/pull/47673) Report missing CUDA custom ops in is_supported for Marlin FP4
- [#47638](https://github.com/vllm-project/vllm/pull/47638) Normalize list/tuple KV cache input in register_kv_caches
- [#47928](https://github.com/vllm-project/vllm/pull/47928) Account scheduled spec slots on empty output rows
- [#48072](https://github.com/vllm-project/vllm/pull/48072) Add Qwen2-VL multimodal tests for CPU backend and fix incompatibilities
- [#48057](https://github.com/vllm-project/vllm/pull/48057) Validate pooling dimensions with proper error handling
- [#47721](https://github.com/vllm-project/vllm/pull/47721) Add GPT-OSS BF16 expert remap regression test
- [#47662](https://github.com/vllm-project/vllm/pull/47662) Accept input_audio content parts in user messages
- [#47666](https://github.com/vllm-project/vllm/pull/47666) Split cpu_cache_usage_perc into write/read usage gauges
- [#47883](https://github.com/vllm-project/vllm/pull/47883) Add roundtrip fixtures for more chat parsers in Rust Frontend
- [#47925](https://github.com/vllm-project/vllm/pull/47925) Pre-size cudagraph output staging buffers to the max capture descriptor
- [#47987](https://github.com/vllm-project/vllm/pull/47987) Make tiering offload region DP-replica aware
</details>

<details>
<summary>CI & build (20)</summary>

- [#46904](https://github.com/vllm-project/vllm/pull/46904) Refresh ROCm base images when docker rocm_base changes
- [#46017](https://github.com/vllm-project/vllm/pull/46017) Improvement of Docker image build for IBM Power
- [#41359](https://github.com/vllm-project/vllm/pull/41359) Bump Transformers version to 5.10.4
- [#46893](https://github.com/vllm-project/vllm/pull/46893) GSM8K eval integration test for KV offloading
- [#47478](https://github.com/vllm-project/vllm/pull/47478) Adding Rust parity for ROCm
- [#47735](https://github.com/vllm-project/vllm/pull/47735) Unblock more end-to-end test cases in Rust Frontend
- [#47481](https://github.com/vllm-project/vllm/pull/47481) Adding nixl multiconn for ROCm
- [#47880](https://github.com/vllm-project/vllm/pull/47880) Add Intel XPU Docker release pipeline
- [#47687](https://github.com/vllm-project/vllm/pull/47687) Remove global extra index for CPU
- [#47758](https://github.com/vllm-project/vllm/pull/47758) Adjust memory request for tests in Intel GPU CI
- [#47695](https://github.com/vllm-project/vllm/pull/47695) Fix pre-commit check
- [#47591](https://github.com/vllm-project/vllm/pull/47591) Increasing parallelism in Basic Models Tests for ROCm
- [#45313](https://github.com/vllm-project/vllm/pull/45313) Register VLLM_BUILD_* and VLLM_IMAGE_TAG provenance env vars
- [#47730](https://github.com/vllm-project/vllm/pull/47730) Use TTY for AMD CI tests for colored buildkite logs
- [#47897](https://github.com/vllm-project/vllm/pull/47897) Accept ready-run-all-tests label in pre-commit gate
- [#47675](https://github.com/vllm-project/vllm/pull/47675) Add agent tags for Basic Models Tests in Intel GPU CI
- [#47835](https://github.com/vllm-project/vllm/pull/47835) Upgrade tpu-inference to v0.24.0
- [#48091](https://github.com/vllm-project/vllm/pull/48091) Add yaml for XPU
- [#47904](https://github.com/vllm-project/vllm/pull/47904) Bump the minor-update group across 1 directory with 159 updates
- [#48101](https://github.com/vllm-project/vllm/pull/48101) Annotate built Docker image tags on the Buildkite build page
</details>

<details>
<summary>Docs (9)</summary>

- [#47830](https://github.com/vllm-project/vllm/pull/47830) Update usage of `hf` cli for cache list and removal
- [#47784](https://github.com/vllm-project/vllm/pull/47784) Add suggestion on how to incorporate tests in AGENTS MD
- [#47913](https://github.com/vllm-project/vllm/pull/47913) Fix manylinux tag in installation guide
- [#48008](https://github.com/vllm-project/vllm/pull/48008) Fix the docs build
- [#47374](https://github.com/vllm-project/vllm/pull/47374) Surface the --kv-cache-memory suggestion at INFO and document fast-startup knobs
- [#47989](https://github.com/vllm-project/vllm/pull/47989) Remove TeleChatForCausalLM
- [#47044](https://github.com/vllm-project/vllm/pull/47044) `kv_sharing_fast_prefill` correction
- [#47701](https://github.com/vllm-project/vllm/pull/47701) Fix note formatting for pooling models
- [#45813](https://github.com/vllm-project/vllm/pull/45813) Clarify fastokens availability
</details>

<details>
<summary>Bugfixes (129)</summary>

- [#47728](https://github.com/vllm-project/vllm/pull/47728) Free out-of-window blocks on the processed-token basis under async scheduling
- [#46739](https://github.com/vllm-project/vllm/pull/46739) Multiple fixes to w4a8_int8 CPU MoE path
- [#47165](https://github.com/vllm-project/vllm/pull/47165) Return HTTP 422 for unprocessable image URLs instead of 500
- [#47260](https://github.com/vllm-project/vllm/pull/47260) Add resource bounds validation to derender endpoints
- [#42478](https://github.com/vllm-project/vllm/pull/42478) Fix Qwen3-ASR transcription streaming postprocessing
- [#47762](https://github.com/vllm-project/vllm/pull/47762) Fix KV offloading GSM8K eval: prefix caching, CPU reload verification, device fit
- [#44303](https://github.com/vllm-project/vllm/pull/44303) Fix http_requests_total metric recording some 4xx errors as 5xx
- [#47590](https://github.com/vllm-project/vllm/pull/47590) Forward instruction to Jina reranker scoring prompts
- [#47550](https://github.com/vllm-project/vllm/pull/47550) Fix flaky parallel tool-call streaming
- [#47845](https://github.com/vllm-project/vllm/pull/47845) Bound completion prompt list to prevent unbounded engine fan-out
- [#46972](https://github.com/vllm-project/vllm/pull/46972) Store interior chunk-boundary blocks under MTP/Eagle
- [#45352](https://github.com/vllm-project/vllm/pull/45352) Forward callable hf_overrides to the draft model config
- [#47332](https://github.com/vllm-project/vllm/pull/47332) Fix FA4 mm_prefix mask: add sliding window and absolute q_idx for Gemma4
- [#48046](https://github.com/vllm-project/vllm/pull/48046) Use int8 workspace for FlashInfer MLA decode
- [#47259](https://github.com/vllm-project/vllm/pull/47259) Block request-level GPU video backend selection without validation
- [#47158](https://github.com/vllm-project/vllm/pull/47158) Fixed aiter master flag and expert parallelism compatibility on minimax-m3-mxfp8
- [#45207](https://github.com/vllm-project/vllm/pull/45207) Pad Mamba page size instead of scaling block_size
- [#48085](https://github.com/vllm-project/vllm/pull/48085) Fix race condition in KVBlockZeroer
- [#47772](https://github.com/vllm-project/vllm/pull/47772) Align CrossEncoder token type ids after truncation
- [#45418](https://github.com/vllm-project/vllm/pull/45418) Reject sampling params unsupported by diffusion models
- plus 109 more minor bugfixes
</details>

<details>
<summary>Refactors (3)</summary>

- [#47329](https://github.com/vllm-project/vllm/pull/47329) Remove multiple dead code
- [#47786](https://github.com/vllm-project/vllm/pull/47786) Refactor Flashinfer BatchPrefill* / BatchDecode* and trtllm_batch* wrappers' forward paths
- [#47807](https://github.com/vllm-project/vllm/pull/47807) Streamline DeepSeek V4 mHC warmup and remove token-size cap
</details>

<details>
<summary>Other (5)</summary>

- [#47668](https://github.com/vllm-project/vllm/pull/47668) Revert "[Platform] Replace `torch.cuda.Event` with `torch.Event`"
- [#47969](https://github.com/vllm-project/vllm/pull/47969) Remove unused _get_kv_cache_config_deepseek_v4 alias
- [#47970](https://github.com/vllm-project/vllm/pull/47970) Remove router weight upcast for DSv2-related models
- [#47995](https://github.com/vllm-project/vllm/pull/47995) Updated flash_attn GIT_TAG to point to torch Stable ABI FA3 commit
- [#47798](https://github.com/vllm-project/vllm/pull/47798) Revert "Make the Transformers modeling backend as fast as native vLLM"
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 8d179ddfebffb93496d8a0ac474467d01d42884dfd71212171d592c75f0c4614 -->
