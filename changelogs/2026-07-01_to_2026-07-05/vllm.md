# vllm: PR digest (2026-07-01 to 2026-07-05)

_131 merged, 283 newly opened - source vllm-project/vllm, generated 2026-07-05T22:12:42Z_

## TL;DR
- **DeepSeek V4 & MLA:** DeepSeek V4 saw massive attention, including a merged streaming parser and extensive work on sparse MLA (Multi-Head Latent Attention) optimizations across FlashInfer and Triton backends.
- **Speculative Decoding:** DSpark and DFlash speculative decoding engines received major upgrades, including full CUDA graph support, SWA integration, and enablement for DeepSeek V4 on AMD hardware.
- **Architecture Cleanup:** A major milestone was reached with the deletion of the legacy `PagedAttention` implementation, fully committing to modern attention backends.
- **Frontend Refactor:** The Rust frontend underwent significant structural improvements, splitting engine core DTOs and domain types for better maintainability.
- **MoE & Quantization:** Expanded support for FP8 quantization (AutoRound, MXFP8) and new integrations for DoRA and FlashInfer MoE LoRA.

## Most important PRs
- **[#47361](https://github.com/vllm-project/vllm/pull/47361)** Delete PagedAttention: Removes the legacy `PagedAttention` implementation, fully committing the engine to modern, optimized attention backends like FlashInfer and Triton. (Merged)
- **[#46076](https://github.com/vllm-project/vllm/pull/46076)** [Attention][DSA] support dcp for FLASHINFER_MLA_SPARSE: Unlocks Distributed Context Parallelism (DCP) for sparse Multi-Head Latent Attention (MLA) in FlashInfer, a critical scaling feature for DeepSeek models. (Merged)
- **[#46995](https://github.com/vllm-project/vllm/pull/46995)** [Spec Decode] DSpark: Merges the core DSpark speculative decoding engine, introducing a major new performance path for speculative execution on NVIDIA hardware. (Merged)
- **[#47576](https://github.com/vllm-project/vllm/pull/47576)** [Kernel] ReplaySSM: cache SSM inputs instead of state: A massive architectural shift for Mamba2 that caches SSM inputs rather than state, significantly accelerating both standard and speculative decoding. (Newly opened)
- **[#45877](https://github.com/vllm-project/vllm/pull/45877)** [Frontend] [Parser] Port DeepSeek V4 to streaming parser engine framework: Integrates DeepSeek V4 into the streaming parser, which is crucial for real-time usability and performance of the model. (Merged)

## More changes by area

<details>
<summary>Performance (35)</summary>

- [#44639](https://github.com/vllm-project/vllm/pull/44639) Added tanh AOR for faster gelu activations on CPU
- [#47523](https://github.com/vllm-project/vllm/pull/47523) Speed up chat roundtrip tests in Rust frontend
- [#47198](https://github.com/vllm-project/vllm/pull/47198) Remove redundant op for GLM 5.2
- [#46730](https://github.com/vllm-project/vllm/pull/46730) DSv4 indexer: use platform FP8 dtype for Q-quant on gfx942
- [#47285](https://github.com/vllm-project/vllm/pull/47285) Warm up GLM-5.2 DSA indexer prefill metadata kernel
- [#47540](https://github.com/vllm-project/vllm/pull/47540) Maintain persistent penalty statistics instead of per-step CPU rebuild
- [#47583](https://github.com/vllm-project/vllm/pull/47583) Add opt-in incremental prompt-encoding cache for multi-turn chat
- [#47451](https://github.com/vllm-project/vllm/pull/47451) Add new warmup infrastructure for JITs
- [#47391](https://github.com/vllm-project/vllm/pull/47391) Optimize padded EAGLE input prep and EAGLE3 layer0 RMSNorm concat
- [#47623](https://github.com/vllm-project/vllm/pull/47623) Avoid redundant logprobs list materialization
- [#47622](https://github.com/vllm-project/vllm/pull/47622) Batch KV scale host conversion
- [#47593](https://github.com/vllm-project/vllm/pull/47593) Scale fused MoE default-config M-tile threshold by tokens per expert
- [#47463](https://github.com/vllm-project/vllm/pull/47463) Optimize `fused_topk_bias` for DSv4
- [#47580](https://github.com/vllm-project/vllm/pull/47580) Keep H2D transfers dense in fused-MoE weight loading
- [#47474](https://github.com/vllm-project/vllm/pull/47474) Cache `token_to_req_indices` for dsv4
- [#47631](https://github.com/vllm-project/vllm/pull/47631) Minimax M3 - Support cross-layer allreduce-norm fusion
- [#47546](https://github.com/vllm-project/vllm/pull/47546) Expand Triton kernel warmup coverage for Qwen
- [#46853](https://github.com/vllm-project/vllm/pull/46853) Add Laguna XS.2.1 DFlash drafter support
- [#44297](https://github.com/vllm-project/vllm/pull/44297) Constrain bitmask and trim grammar advance at the reasoning boundary
- [#45953](https://github.com/vllm-project/vllm/pull/45953) Make Dynamic SD compatible with Full Cuda Graphs
- [#38174](https://github.com/vllm-project/vllm/pull/38174) Universal speculative decoding for heterogeneous vocabularies
- [#47383](https://github.com/vllm-project/vllm/pull/47383) Fix int32 offset overflow in block verification kernels
- [#47428](https://github.com/vllm-project/vllm/pull/47428) Fix Mamba2 crash on non-spec-decode
- [#47419](https://github.com/vllm-project/vllm/pull/47419) Enable DeepSeek-V4 DSpark speculative decoding on AMD
- [#47414](https://github.com/vllm-project/vllm/pull/47414) Enable dspark for deepseek v4
- [#47627](https://github.com/vllm-project/vllm/pull/47627) Domino head for dflash
- [#47490](https://github.com/vllm-project/vllm/pull/47490) Never silently override an explicitly configured speculative method
- [#47322](https://github.com/vllm-project/vllm/pull/47322) Spec decode per request stats
- [#47386](https://github.com/vllm-project/vllm/pull/47386) Decouple draft Gumbel stream from acceptance/recovery noise
- [#47352](https://github.com/vllm-project/vllm/pull/47352) Share topk index buffer between draft steps
- [#47377](https://github.com/vllm-project/vllm/pull/47377) Add DSpark support for Qwen3.5 target models
- [#47616](https://github.com/vllm-project/vllm/pull/47616) Trim token_ids/logprobs left past a stop string under speculative decoding
- [#47331](https://github.com/vllm-project/vllm/pull/47331) Overlap bonus sampling with target verification
- [#47460](https://github.com/vllm-project/vllm/pull/47460) Initialize draft CUDA-graph keys for the native draft_model proposer
- [#47093](https://github.com/vllm-project/vllm/pull/47093) DSpark speculators checkpoint support
</details>

<details>
<summary>Kernels & attention (36)</summary>

- [#43232](https://github.com/vllm-project/vllm/pull/43232) Xqa decode kernels
- [#44977](https://github.com/vllm-project/vllm/pull/44977) Fuse MLA q/kv RMSNorm + FP8 per-token quant in the FP8 attention path
- [#47090](https://github.com/vllm-project/vllm/pull/47090) Support FlashMLA FP8 KV cache for GLM5
- [#46104](https://github.com/vllm-project/vllm/pull/46104) Support SWA + DFlash for MiMo
- [#42890](https://github.com/vllm-project/vllm/pull/42890) Support nvfp4 kv with kv-cache-dtype-skip-layers sliding_window
- [#46942](https://github.com/vllm-project/vllm/pull/46942) Enable mm prefix bidi attention support on MRV2
- [#47128](https://github.com/vllm-project/vllm/pull/47128) Move to stable abi since ROCm upgraded to torch 2.11
- [#47332](https://github.com/vllm-project/vllm/pull/47332) Fix FA4 mm_prefix mask for Gemma4
- [#47035](https://github.com/vllm-project/vllm/pull/47035) Fix encoder-decoder cross-attention KV layout aliasing on ROCm
- [#47102](https://github.com/vllm-project/vllm/pull/47102) Add Triton Backend for Unlimited-OCR R-SWA
- [#45844](https://github.com/vllm-project/vllm/pull/45844) Fix CPU split-KV scratchpad sizing
- [#46984](https://github.com/vllm-project/vllm/pull/46984) Use functions instead of PTX for the PDL instruction
- [#47485](https://github.com/vllm-project/vllm/pull/47485) Derive FlashInfer Q dtype from resolved per-group builder state
- [#47308](https://github.com/vllm-project/vllm/pull/47308) Warmup cross-attn properly in encoder-decoder case
- [#47305](https://github.com/vllm-project/vllm/pull/47305) Don't read KV cache past `seq_len` in triton paged attn kernels
- [#47567](https://github.com/vllm-project/vllm/pull/47567) Disable persistent sparse-MLA kernel for chunked-prefill continuations
- [#47511](https://github.com/vllm-project/vllm/pull/47511) DFlash SWA — resolved for personal build
- [#47327](https://github.com/vllm-project/vllm/pull/47327) Add dense MHA path for sparse MLA short sequences
- [#47629](https://github.com/vllm-project/vllm/pull/47629) TRITON_MLA_SPARSE backend for SM80/SM121 sparse MLA
- [#47287](https://github.com/vllm-project/vllm/pull/47287) Add AITER sparse paged attention for MiniMax-M3
- [#47306](https://github.com/vllm-project/vllm/pull/47306) Draft: Xqa specdec
- [#47443](https://github.com/vllm-project/vllm/pull/47443) Select split-K per shape in HPC Attention Decode Backend
- [#47535](https://github.com/vllm-project/vllm/pull/47535) Add opt-in cuda cache update for flash_attn_diffkv
- [#47343](https://github.com/vllm-project/vllm/pull/47343) Use Helion fused-quant kernels by default
- [#47542](https://github.com/vllm-project/vllm/pull/47542) DCP + split-q for speculative decoding support
- [#47527](https://github.com/vllm-project/vllm/pull/47527) Support FlashInfer packed sparse MLA decode on SM120
- [#47348](https://github.com/vllm-project/vllm/pull/47348) Optimize CuTeDSL DCP top-k merge
- [#47502](https://github.com/vllm-project/vllm/pull/47502) Using tok_sparse_select from MSA instead of triton kernels
- [#47525](https://github.com/vllm-project/vllm/pull/47525) Add split-k support to triton_w4a16 gemm kernel
- [#47469](https://github.com/vllm-project/vllm/pull/47469) Route SM100 sparse-indexer decode through varlen paged MQA logits
- [#47587](https://github.com/vllm-project/vllm/pull/47587) Zero TRT-LLM 8x4 FP4 scale padding
- [#47491](https://github.com/vllm-project/vllm/pull/47491) Preserve attention cache hits when Mamba group misses
- [#47323](https://github.com/vllm-project/vllm/pull/47323) Fix OOB scale reads in Triton MXFP4 matmul kernel
- [#47248](https://github.com/vllm-project/vllm/pull/47248) Enable tensor-descriptor Q load for non-power-of-2 GQA
- [#47520](https://github.com/vllm-project/vllm/pull/47520) Derive Triton 3D flash-decoding threshold from SM count
- [#47532](https://github.com/vllm-project/vllm/pull/47532) Fix VLEN detection for RVV attention path on CPU
</details>

<details>
<summary>MoE & quantization (25)</summary>

- [#45368](https://github.com/vllm-project/vllm/pull/45368) Align LoRA implementation with Punica GPU
- [#43645](https://github.com/vllm-project/vllm/pull/43645) Add W8A8 FP8 linear kernel with multi-granularity quant support
- [#46656](https://github.com/vllm-project/vllm/pull/46656) New stable abi cleanup for kernels and MoE
- [#45723](https://github.com/vllm-project/vllm/pull/45723) Plumb gemm1_alpha/beta/clamp_limit into TRT-LLM FP8 MoE
- [#47290](https://github.com/vllm-project/vllm/pull/47290) Lora should not be with MoE SP
- [#47220](https://github.com/vllm-project/vllm/pull/47220) Enable EPLB for Quark OCP MXFP4 MoE
- [#47229](https://github.com/vllm-project/vllm/pull/47229) Better MXFP8 quantization kernel for DSV4
- [#47395](https://github.com/vllm-project/vllm/pull/47395) Add DoRA support for serving and linear layers
- [#47514](https://github.com/vllm-project/vllm/pull/47514) Add MXFP8 Linear Support for INC
- [#47434](https://github.com/vllm-project/vllm/pull/47434) Support AutoRound Format Block-Wise FP8
- [#47226](https://github.com/vllm-project/vllm/pull/47226) Integrate flashinfer MoE LoRA
- [#47553](https://github.com/vllm-project/vllm/pull/47553) Add aiter backend for NVFP4 MOE runtime on gfx950
- [#47392](https://github.com/vllm-project/vllm/pull/47392) Plumb swigluoai activation into FlashInfer b12x MoE
- [#47584](https://github.com/vllm-project/vllm/pull/47584) Rowwise-fp8 draft lm_head for DSpark
- [#47515](https://github.com/vllm-project/vllm/pull/47515) Fix NVFP4 per-half global scale for fused gate_up_proj
- [#47507](https://github.com/vllm-project/vllm/pull/47507) Gemma-4 k_eq_v x compressed-tensors: propagate shard aliases
- [#47599](https://github.com/vllm-project/vllm/pull/47599) Warm up FlashInfer b12x NVFP4 MoE to avoid mid-serving JIT stall
- [#47588](https://github.com/vllm-project/vllm/pull/47588) Avoid Silent Accuracy Corruption in Quark MXFP4 EPLB
- [#47577](https://github.com/vllm-project/vllm/pull/47577) Auto-select FLASHINFER_B12X NVFP4 MoE backend on SM120
- [#47640](https://github.com/vllm-project/vllm/pull/47640) Guard None group members in expand_packed_lora
- [#47611](https://github.com/vllm-project/vllm/pull/47611) Handle older FlashInfer FP8 MoE signatures
- [#47445](https://github.com/vllm-project/vllm/pull/47445) Fix ModelOpt quantization inference for fused siblings
- [#47427](https://github.com/vllm-project/vllm/pull/47427) FI autotuning: max bucket = max token count
- [#47318](https://github.com/vllm-project/vllm/pull/47318) Fix ModelOpt mixed-precision quantization for sparse configs
- [#47237](https://github.com/vllm-project/vllm/pull/47237) Fix INC quantization method selection for non-quantized layers
</details>

<details>
<summary>Model support (22)</summary>

- [#44785](https://github.com/vllm-project/vllm/pull/44785) Add LLaVA-OneVision-2
- [#47263](https://github.com/vllm-project/vllm/pull/47263) Remove AyaVision, MusicFlamingo
- [#30966](https://github.com/vllm-project/vllm/pull/30966) Migrate GPTBigCode and Starcoder2 to the Transformers modeling backend
- [#47192](https://github.com/vllm-project/vllm/pull/47192) Support Hy3 token suffix and JSON Schema array types
- [#47410](https://github.com/vllm-project/vllm/pull/47410) Support GLM-5.2 gate use FP32
- [#47271](https://github.com/vllm-project/vllm/pull/47271) Add support for OpenPangu V2 model
- [#47641](https://github.com/vllm-project/vllm/pull/47641) Enable granite-4 model on cpu
- [#47547](https://github.com/vllm-project/vllm/pull/47547) Allow Gemma4 to use FlashInfer when FA4 is unavailable
- [#47660](https://github.com/vllm-project/vllm/pull/47660) Add EuroBERT embedding model
- [#46806](https://github.com/vllm-project/vllm/pull/46806) Remove mantis
- [#47536](https://github.com/vllm-project/vllm/pull/47536) Use VllmRunner for `voxtral_realtime` tests to avoid OOM on AMD GPU
- [#47071](https://github.com/vllm-project/vllm/pull/47071) Fix pooled Whisper sliding-window KV sizing
- [#47437](https://github.com/vllm-project/vllm/pull/47437) Fix pooled Whisper encoder sliding-window kernel size
- [#47566](https://github.com/vllm-project/vllm/pull/47566) Normalize direct PIL image inputs
- [#47302](https://github.com/vllm-project/vllm/pull/47302) Add MooncakeStoreECConnector for multimodal hidden-state transfer
- [#47416](https://github.com/vllm-project/vllm/pull/47416) Add fused Kimi image preprocessing
- [#47344](https://github.com/vllm-project/vllm/pull/47344) Refactor IPC calculation out of gpu_worker
- [#47625](https://github.com/vllm-project/vllm/pull/47625) Support ViT full CUDA graph for Idefics3 and SmolVLM
- [#47652](https://github.com/vllm-project/vllm/pull/47652) Fix gemma4 unified multi audio
- [#47259](https://github.com/vllm-project/vllm/pull/47259) Block request-level GPU video backend selection without validation
- [#47459](https://github.com/vllm-project/vllm/pull/47459) Fix Gemma4 audio crash with variable-length batched inputs
- [#47581](https://github.com/vllm-project/vllm/pull/47581) Avoid extra copies for multimodal tensors in Rust Frontend
</details>

<details>
<summary>Parallelism & scheduling (29)</summary>

- [#44353](https://github.com/vllm-project/vllm/pull/44353) Weight sync refactor + move sparse nccl engine
- [#47070](https://github.com/vllm-project/vllm/pull/47070) Support sequence parallel without the need for DP
- [#47219](https://github.com/vllm-project/vllm/pull/47219) Default FlashInfer allreduce to mnnvl on single node
- [#47462](https://github.com/vllm-project/vllm/pull/47462) Add DiffusionGemma consumer-sufficient TP vocab state
- [#47357](https://github.com/vllm-project/vllm/pull/47357) Stateful trainer send for RL
- [#47288](https://github.com/vllm-project/vllm/pull/47288) Elastic EP Async preparation
- [#47505](https://github.com/vllm-project/vllm/pull/47505) Guard lmcache_mp_connector state transition with num_external_tokens
- [#47636](https://github.com/vllm-project/vllm/pull/47636) Well-known default host/port env vars and per-DP-rank control port for P2P
- [#47500](https://github.com/vllm-project/vllm/pull/47500) Consume SleepModeBackend capability flags in the worker suspend/resume path
- [#47373](https://github.com/vllm-project/vllm/pull/47373) Use prefill block content to overwrite decode bad blocks
- [#47317](https://github.com/vllm-project/vllm/pull/47317) Apply SWA lookup mask before hashing/key build in Mooncake
- [#47589](https://github.com/vllm-project/vllm/pull/47589) Delegate MNNVL allreduce one-shot selection
- [#47495](https://github.com/vllm-project/vllm/pull/47495) Retry RDMA send-queue-full backpressure instead of failing the read
- [#44074](https://github.com/vllm-project/vllm/pull/44074) Pluggable sleep-mode backend abstraction
- [#47243](https://github.com/vllm-project/vllm/pull/47243) Make sleep-mode backend capability flags communicator-agnostic
- [#47609](https://github.com/vllm-project/vllm/pull/47609) Preserve KV cache dtype in backend shape
- [#47363](https://github.com/vllm-project/vllm/pull/47363) Demo implementation of extensible kv cache memory
- [#47423](https://github.com/vllm-project/vllm/pull/47423) CPU Offloading EC Connector
- [#47475](https://github.com/vllm-project/vllm/pull/47475) Add primary-tier external pinning API for KV offload
- [#47235](https://github.com/vllm-project/vllm/pull/47235) Restore evicted CPU blocks and fix cursor advancement
- [#47556](https://github.com/vllm-project/vllm/pull/47556) Optimize sliding-window prefix-cache miss scan
- [#47234](https://github.com/vllm-project/vllm/pull/47234) Document CPU eviction behavior as reference
- [#47274](https://github.com/vllm-project/vllm/pull/47274) Add `TieringManagerReverseAPI` protocol for P2P secondary tier
- [#47291](https://github.com/vllm-project/vllm/pull/47291) SimpleCPUOffload: order CPU->GPU loads after compute
- [#47653](https://github.com/vllm-project/vllm/pull/47653) SimpleCPUOffload: defer sliding-window mid-flight block free
- [#47638](https://github.com/vllm-project/vllm/pull/47638) Normalize list/tuple KV cache input in register_kv_caches
- [#47272](https://github.com/vllm-project/vllm/pull/47272) Reserve the KV null block when validating max_model_len
- [#47324](https://github.com/vllm-project/vllm/pull/47324) Fix SimpleCPUOffload load-path race
- [#47413](https://github.com/vllm-project/vllm/pull/47413) Add tier_idx to SecondaryTierManager for per-tier metrics
</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#47162](https://github.com/vllm-project/vllm/pull/47162) Remove speculative decoding stream overrides from CPUModelRunner
- [#47447](https://github.com/vllm-project/vllm/pull/47447) Ship examples/ in the CPU release image
- [#47467](https://github.com/vllm-project/vllm/pull/47467) Enable oneDNN ITT task collection by default for CPU primitive-level profiling
- [#47321](https://github.com/vllm-project/vllm/pull/47321) Optimize math functions of VSX power on CPU
- [#47565](https://github.com/vllm-project/vllm/pull/47565) FP32 GEMV for GLM5
- [#47336](https://github.com/vllm-project/vllm/pull/47336) Fix data-parallel EngineCore processes all binding to the same NUMA node
- [#47399](https://github.com/vllm-project/vllm/pull/47399) Detect CUDA toolchain/driver PTX mismatch on GB10
</details>

<details>
<summary>API & serving (49)</summary>

- [#47265](https://github.com/vllm-project/vllm/pull/47265) Split engine core DTOs into separate modules in Rust Frontend
- [#47283](https://github.com/vllm-project/vllm/pull/47283) Use enum-backed domain types for engine outputs and structured outputs
- [#47435](https://github.com/vllm-project/vllm/pull/47435) Improve scheduler stats logging parity in Rust Frontend
- [#47250](https://github.com/vllm-project/vllm/pull/47250) Run SageMaker handler-override tests in-process via TestClient
- [#46306](https://github.com/vllm-project/vllm/pull/46306) Expose profiler control routes in Rust Frontend
- [#47498](https://github.com/vllm-project/vllm/pull/47498) Refine the entrypoint class's inheritance hierarchy
- [#47379](https://github.com/vllm-project/vllm/pull/47379) Recover raw tail when Harmony parser ends non-terminal
- [#47590](https://github.com/vllm-project/vllm/pull/47590) Forward instruction to Jina reranker scoring prompts
- [#46684](https://github.com/vllm-project/vllm/pull/46684) Add repetition_detection support to sampling params in Rust Frontend
- [#47126](https://github.com/vllm-project/vllm/pull/47126) Fix beam search candidate indexing when logprobs count varies
- [#47384](https://github.com/vllm-project/vllm/pull/47384) Fix batch chat endpoint corrupting logprobs when return_token_ids is set
- [#46512](https://github.com/vllm-project/vllm/pull/46512) Add error context in tool parser failures in Rust Frontend
- [#47289](https://github.com/vllm-project/vllm/pull/47289) Recover buffered text from incomplete tool calls at EOS
- [#46966](https://github.com/vllm-project/vllm/pull/46966) Validate Pooling cache_salt Values
- [#46939](https://github.com/vllm-project/vllm/pull/46939) Forward request-level prompt extras for cross-encoder scoring
- [#47529](https://github.com/vllm-project/vllm/pull/47529) Limit `SO_REUSEPORT` to multi-worker serving
- [#47333](https://github.com/vllm-project/vllm/pull/47333) Update request-extras parity for batch chat completion
- [#47082](https://github.com/vllm-project/vllm/pull/47082) Preserve cross-encoder pooling extra kwargs
- [#47615](https://github.com/vllm-project/vllm/pull/47615) Voxtral realtime: opt-in blank-run penalty to break self-sustained silence ruts
- [#47301](https://github.com/vllm-project/vllm/pull/47301) Add detokenization streaming derender for disaggregated serving
- [#47362](https://github.com/vllm-project/vllm/pull/47362) Add TLS certificate hot-reload in Rust Frontend
- [#47454](https://github.com/vllm-project/vllm/pull/47454) Add `vllm.endpoint_plugins` framework
- [#47444](https://github.com/vllm-project/vllm/pull/47444) Cache metric handles for scheduler & request stats in Rust Frontend
- [#47585](https://github.com/vllm-project/vllm/pull/47585) Support custom logits processors in ModelRunner V2
- [#47230](https://github.com/vllm-project/vllm/pull/47230) Return HTTP 422 instead of 500 for image/media URL fetch errors
- [#47563](https://github.com/vllm-project/vllm/pull/47563) Add language control and metadata for Qwen3-ASR realtime ASR
- [#47642](https://github.com/vllm-project/vllm/pull/47642) Add per-request decode debug logging in v1 output processor
- [#47633](https://github.com/vllm-project/vllm/pull/47633) Emit spec-required gen_ai.operation.name on request spans
- [#47439](https://github.com/vllm-project/vllm/pull/47439) Clear response format constraints when tool_choice is auto
- [#47313](https://github.com/vllm-project/vllm/pull/47313) Expose stop reason in token generate responses
- [#47403](https://github.com/vllm-project/vllm/pull/47403) Replace asserts with explicit Type/ValueErrors for robust input validation
- [#47494](https://github.com/vllm-project/vllm/pull/47494) Align sampling validation with Python in Rust Frontend
- [#47562](https://github.com/vllm-project/vllm/pull/47562) Drop incomplete tool-call markup in non-streaming to match streaming
- [#47555](https://github.com/vllm-project/vllm/pull/47555) Coerce scalar tool call arguments and reject malformed JSON
- [#47537](https://github.com/vllm-project/vllm/pull/47537) Reuse function call IDs for Responses API built-in tool outputs
- [#47560](https://github.com/vllm-project/vllm/pull/47560) Allow untyped tool schemas to coerce JSON values
- [#47569](https://github.com/vllm-project/vllm/pull/47569) Treat tool parameter schemas without a type as allowing any type
- [#47632](https://github.com/vllm-project/vllm/pull/47632) Tool schema property with no type field now allows any type
- [#47503](https://github.com/vllm-project/vllm/pull/47503) Accept optional newline before JSON arguments in deepseek_v3 parser
- [#47612](https://github.com/vllm-project/vllm/pull/47612) Accept JSON tool calls in streaming and non-streaming for llama4_pythonic
- [#47630](https://github.com/vllm-project/vllm/pull/47630) Respect allowed_token_ids in beam search
- [#47411](https://github.com/vllm-project/vllm/pull/47411) Support min_tokens in beam search
- [#47613](https://github.com/vllm-project/vllm/pull/47613) Pass sampling params through Anthropic /v1/messages
- [#47662](https://github.com/vllm-project/vllm/pull/47662) Accept input_audio content parts in user messages
- [#47608](https://github.com/vllm-project/vllm/pull/47608) Add human-readable integer support for more cli-args
- [#47530](https://github.com/vllm-project/vllm/pull/47530) Bump llm-multimodal version in Rust Frontend
- [#47501](https://github.com/vllm-project/vllm/pull/47501) Add gigachat3 tool parser in Rust Frontend
- [#47254](https://github.com/vllm-project/vllm/pull/47254) Add functiongemma tool parser support in Rust Frontend
- [#47345](https://github.com/vllm-project/vllm/pull/47345) Added olmo3 reasoning parser in Rust Frontend
</details>

<details>
<summary>Tests, CI & build (37)</summary>

- [#47338](https://github.com/vllm-project/vllm/pull/47338) Remove unused Dockerfile.nightly_torch
- [#47479](https://github.com/vllm-project/vllm/pull/47479) Adding test groups for parity with upstream on ROCm
- [#47551](https://github.com/vllm-project/vllm/pull/47551) Bump `huggingface-hub` from `v1.10.2` to `v1.22.0`
- [#47477](https://github.com/vllm-project/vllm/pull/47477) Adding metadata for ROCm CI
- [#47342](https://github.com/vllm-project/vllm/pull/47342) Remove torch_nightly mirror tags
- [#47197](https://github.com/vllm-project/vllm/pull/47197) Fix various failures on `main`
- [#46456](https://github.com/vllm-project/vllm/pull/46456) intel CI: add quantization and awq case for xpu
- [#47193](https://github.com/vllm-project/vllm/pull/47193) Enable LoRA TP Distributed Test Group In AMD CI
- [#47242](https://github.com/vllm-project/vllm/pull/47242) Fix LoRA testing
- [#47222](https://github.com/vllm-project/vllm/pull/47222) Toggle test coredumps on ROCm debug agent
- [#42486](https://github.com/vllm-project/vllm/pull/42486) Enable ut qk_norm_rope_fusion
- [#47465](https://github.com/vllm-project/vllm/pull/47465) Pin modelscope version to fix test breakage
- [#47208](https://github.com/vllm-project/vllm/pull/47208) Rerun test_engine_log_metrics_ray on Ray GCS startup timeout
- [#47519](https://github.com/vllm-project/vllm/pull/47519) Fix Kernels and Kernels attention test failures on ROCm
- [#47299](https://github.com/vllm-project/vllm/pull/47299) Fix segfault in tracing test
- [#47482](https://github.com/vllm-project/vllm/pull/47482) Adding extract hs 2gpu for ROCm CI
- [#47554](https://github.com/vllm-project/vllm/pull/47554) Allow git operations on previously created work trees
- [#47376](https://github.com/vllm-project/vllm/pull/47376) Split test_punica_ops into separate pytest invocations
- [#47319](https://github.com/vllm-project/vllm/pull/47319) Include NVTX in cuda.txt
- [#47405](https://github.com/vllm-project/vllm/pull/47405) Mv huggingface cache to larger disk in Intel GPU CI
- [#47510](https://github.com/vllm-project/vllm/pull/47510) Fix dependency typo in Intel GPU CI
- [#47663](https://github.com/vllm-project/vllm/pull/47663) Stock aot_compile driver: alternate to eval-frame stock torch.compile
- [#47605](https://github.com/vllm-project/vllm/pull/47605) Bump the minor-update group across 1 directory with 158 updates
- [#47545](https://github.com/vllm-project/vllm/pull/47545) Please ignore. This is to quickly locate CI issue.
- [#47550](https://github.com/vllm-project/vllm/pull/47550) Fix flaky parallel tool-call streaming
- [#47442](https://github.com/vllm-project/vllm/pull/47442) Bump nvidia-cutlass-dsl to 4.6.0 and drop packaging workarounds
- [#47478](https://github.com/vllm-project/vllm/pull/47478) Adding Rust parity for ROCm CI
- [#47330](https://github.com/vllm-project/vllm/pull/47330) Pin `amd-quark` to 0.12.rc4
- [#47484](https://github.com/vllm-project/vllm/pull/47484) Adding rocm multinode proto
- [#47481](https://github.com/vllm-project/vllm/pull/47481) Adding nixl multiconn for ROCm CI
- [#47468](https://github.com/vllm-project/vllm/pull/47468) Remediate vllm-openai dependency vulnerability findings
- [#47240](https://github.com/vllm-project/vllm/pull/47240) Debug Intel B50 agent
- [#47487](https://github.com/vllm-project/vllm/pull/47487) Remove stale xfail marks from min_tokens e2e tests
- [#47534](https://github.com/vllm-project/vllm/pull/47534) Use lightweight CPU reference and skip heavy cleanup in punica ops tests
- [#47539](https://github.com/vllm-project/vllm/pull/47539) Lazily import Qwen warmup dependencies
- [#47278](https://github.com/vllm-project/vllm/pull/47278) Harden DiffusionGemma self-conditioning matmul against torch.compile shape mismatch
- [#47573](https://github.com/vllm-project/vllm/pull/47573) Exclude location-derived path vars from torch.compile cache factors
</details>

<details>
<summary>Bugfixes (39)</summary>

- [#46974](https://github.com/vllm-project/vllm/pull/46974) Ensure all req slots are accounted for when scheduling
- [#44682](https://github.com/vllm-project/vllm/pull/44682) Tolerate out-of-vocab prompt ids in detokenizer
- [#47311](https://github.com/vllm-project/vllm/pull/47311) poolside_v1: accept tool calls without newline after function name
- [#47217](https://github.com/vllm-project/vllm/pull/47217) Keep image bidirectional attention within the sliding window for Gemma4
- [#47062](https://github.com/vllm-project/vllm/pull/47062) Return raw output when Harmony parser ends non-terminal
- [#47135](https://github.com/vllm-project/vllm/pull/47135) Fix empty decoder prompt for Cohere ASR in throughput benchmark
- [#47029](https://github.com/vllm-project/vllm/pull/47029) Prevent padding placeholders from reaching embeddings
- [#47337](https://github.com/vllm-project/vllm/pull/47337) Allow Run:ai memory_limit sentinel values
- [#47472](https://github.com/vllm-project/vllm/pull/47472) Fix Transformers modeling backend usage stats
- [#46037](https://github.com/vllm-project/vllm/pull/46037) Fix crash loading Mamba/Mamba2 checkpoints without an `architectures` field
- [#44461](https://github.com/vllm-project/vllm/pull/44461) Fix token feedback timeout silent hang in Voxtral Realtime
- [#47597](https://github.com/vllm-project/vllm/pull/47597) Preserve default sampling params in batch chat
- [#42748](https://github.com/vllm-project/vllm/pull/42748) Expose usage field in GenerateResponse for disaggregated serving
- [#47031](https://github.com/vllm-project/vllm/pull/47031) Fix GraniteMoeShared weight loading broken by #41184
- [#47483](https://github.com/vllm-project/vllm/pull/47483) Free all model refs on shutdown
- [#46255](https://github.com/vllm-project/vllm/pull/46255) Guard rfind in ernie45 streaming </response> branch
- [#47164](https://github.com/vllm-project/vllm/pull/47164) Skip cooperative top-K on SM120
- [#47407](https://github.com/vllm-project/vllm/pull/47407) Bound MRoPE temporal positions to prevent engine crash
- [#47260](https://github.com/vllm-project/vllm/pull/47260) Add resource bounds validation to derender endpoints
- [#47657](https://github.com/vllm-project/vllm/pull/47657) Keep sub-1 req/s rates positive in bench sweep serve_workload
- [#47656](https://github.com/vllm-project/vllm/pull/47656) Isolate streaming pending-state from non-streaming reasoning end check
- [#47509](https://github.com/vllm-project/vllm/pull/47509) Fix 'Already borrowed' by pooling tokenizer in StructuredOutputManager
- [#47489](https://github.com/vllm-project/vllm/pull/47489) Let terminal grammars stop under min_tokens
- [#47346](https://github.com/vllm-project/vllm/pull/47346) Surface out-of-range token ids as a clear per-request error
- [#47396](https://github.com/vllm-project/vllm/pull/47396) Load per-shard per-tensor FP8 scales for fused GDN in_proj
- [#47400](https://github.com/vllm-project/vllm/pull/47400) Skip cache-served mm items in tower/connector LoRA mapping
- [#47312](https://github.com/vllm-project/vllm/pull/47312) Handle grammar compilation failures to avoid engine crash
- [#47350](https://github.com/vllm-project/vllm/pull/47350) Handle HarmonyError in streaming process_chunk
- [#47617](https://github.com/vllm-project/vllm/pull/47617) Detect reasoning end with accepted MTP tokens
- [#47261](https://github.com/vllm-project/vllm/pull/47261) Respect DeepGemm disable state during warmup
- [#47382](https://github.com/vllm-project/vllm/pull/47382) Fix TPOT accounting for MTP multi-token outputs
- [#47618](https://github.com/vllm-project/vllm/pull/47618) Fix Deepseek v4 flash error due to [#42890](https://github.com/vllm-project/vllm/pull/42890)
- [#47422](https://github.com/vllm-project/vllm/pull/47422) Surface worker init failure root cause to the parent
- [#47621](https://github.com/vllm-project/vllm/pull/47621) Fix collect_env.py crash on Windows/macOS and pip-less uv environments
- [#47512](https://github.com/vllm-project/vllm/pull/47512) Reject routed experts capture for dense models
- [#47209](https://github.com/vllm-project/vllm/pull/47209) Fix Triton "out of resource: shared memory" Error In One-Shot LoRA MoE
- [#47381](https://github.com/vllm-project/vllm/pull/47381) Order uniform decodes first so spec decodes aren't misclassified as prefills
- [#47506](https://github.com/vllm-project/vllm/pull/47506) Reject routed experts capture for dense models
- [#46838](https://github.com/vllm-project/vllm/pull/46838) Correct FlashInfer CUTLASS MoE tuning token bound
</details>

<details>
<summary>Refactors (12)</summary>

- [#47371](https://github.com/vllm-project/vllm/pull/47371) Revert "Weight sync refactor + move sparse nccl engine"
- [#47496](https://github.com/vllm-project/vllm/pull/47496) Revert "Xqa decode kernels"
- [#47604](https://github.com/vllm-project/vllm/pull/47604) Revert "Support nvfp4 kv with kv-cache-dtype-skip-layers sliding_window"
- [#47624](https://github.com/vllm-project/vllm/pull/47624) Revert "[Bugfix][Frontend][gpt-oss] Recover raw tail when Harmony parser ends non-terminal"
- [#47369](https://github.com/vllm-project/vllm/pull/47369) Revert "[CPU][Perf]Added tanh AOR for faster gelu activations."
- [#47497](https://github.com/vllm-project/vllm/pull/47497) Revert "[ModelRunner V2] Enable by default for all dense models"
- [#47232](https://github.com/vllm-project/vllm/pull/47232) Revert "[Platform] Replace `torch.cuda.mem_get_info` with `torch.accelerator.get_memory_info`"
- [#47293](https://github.com/vllm-project/vllm/pull/47293) Revert "[Distributed] Default FlashInfer allreduce to mnnvl on single node"
- [#47431](https://github.com/vllm-project/vllm/pull/47431) Revert "[MoE] Plumb gemm1_alpha/beta/clamp_limit into TRT-LLM FP8 MoE"
- [#47646](https://github.com/vllm-project/vllm/pull/47646) Revert "[Bugfix][Gemma4] Fix FA4 mm_prefix mask: add sliding window and absolute q_idx"
- [#47329](https://github.com/vllm-project/vllm/pull/47329) Remove multiple dead code
- [#47452](https://github.com/vllm-project/vllm/pull/47452) Move Roberta remaining nn.Embedding to VocabParallelEmbedding
</details>

<details>
<summary>Docs (2)</summary>

- [#45903](https://github.com/vllm-project/vllm/pull/45903) Document gRPC interface as insecure for private use only
- [#47517](https://github.com/vllm-project/vllm/pull/47517) Fix VLM2Vec benchmark chat template path
</details>

<details>
<summary>Other (10)</summary>

- [#47155](https://github.com/vllm-project/vllm/pull/47155) Avoid GLM4V processor init during startup metadata reads
- [#47166](https://github.com/vllm-project/vllm/pull/47166) Coerce completion `max_tokens: null` to default
- [#47269](https://github.com/vllm-project/vllm/pull/47269) Cross-layer lightning-indexer top-k sharing for MiniMax-M3
- [#47304](https://github.com/vllm-project/vllm/pull/47304) Update DeepGEMM tag to point to latest nv-dev branch for sm120 support
- [#46482](https://github.com/vllm-project/vllm/pull/46482) MoRIIO toy proxy: support JSON Content-Type for OpenAI clients
- [#47388](https://github.com/vllm-project/vllm/pull/47388) Persist and reuse the memory-profiling result across boots
- [#47655](https://github.com/vllm-project/vllm/pull/47655) Add unit tests for gemma4_utils
- [#47558](https://github.com/vllm-project/vllm/pull/47558) Avoid DeepGEMM import probe on unsupported platforms
- [#47402](https://github.com/vllm-project/vllm/pull/47402) Add jitter to LoRA adapter_config.json load retries
- [#47393](https://github.com/vllm-project/vllm/pull/47393) Add index topk interval for nvidia
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: c9551521db42abc0e4968e24b4b6f8cad5fb5f6a6916fa187327108bc9572814 -->
