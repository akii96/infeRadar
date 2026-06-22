# vllm: PR digest (2026-06-17 to 2026-06-21)

_151 merged, 276 newly opened - source vllm-project/vllm, generated 2026-06-21T22:24:50Z_

## TL;DR
- **DeepSeek V4 and MiniMax-M3** dominated model-specific work. DeepSeek V4 saw merged functional fixes on AMD, KV cache packing, and flashinfer sparse index cache optimizations, plus newly opened work on Mooncake PP/PD shared KV metadata and sparse attention DCP. MiniMax-M3 gained FP8 sparse GQA, MXFP4 support, and significant in-flight MXFP8 dense-linear and grouped-MoE GEMM optimizations.
- **Attention & Kernels:** Merged a new Helion kernel for dynamic per-token RMSNorm quantization and finalized the `_C` library kernel migration. In-flight work includes a massive RWKV7 Albatross implementation, CuTeDSL warmup infrastructure, and Hopper sparse MLA via `FLASH_ATTN_MLA_SPARSE`.
- **Speculative Decoding:** Added support for mixed KV page sizes in DFlash and Qwen3 architecture support for EAGLE3. In-flight work brings EAGLE3 support to pipeline parallelism and DFlash to CPU.
- **Distributed & KV Offloading:** Significant enhancements to Mooncake and KV offloading, including async lookups to reduce scheduler overhead, compact chunk-hash keys, and newly opened MoRIIO flexible prefill-TP rank selection for heterogeneous TP/DP reads.
- **Frontend & API:** Merged a new Streaming Parser Engine with GLM4.7/5.1/5.2 support, reasoning/tool parsing for `/derender`, and prompt-only completions in the Rust frontend.

## Most important PRs
- **[#46269](https://github.com/vllm-project/vllm/pull/46269)** Adds comprehensive support for the RWKV7 Albatross architecture, introducing a massive set of custom CUDA kernels and integration for the new linear RNN model.
- **[#34432](https://github.com/vllm-project/vllm/pull/34432)** Introduces the Helion kernel for `rms_norm_dynamic_per_token_quant`, significantly optimizing dynamic per-token quantization for RMSNorm operations on NVIDIA hardware.
- **[#45915](https://github.com/vllm-project/vllm/pull/45915)** Implements a new Streaming Parser Engine alongside parsers for GLM4.7, GLM5.1, and GLM5.2, improving the handling of streaming tool calls and reasoning transitions.
- **[#40601](https://github.com/vllm-project/vllm/pull/40601)** Refactors Intel Neural Compressor (INC) quantization into a dedicated package with an `INCScheme` orchestrator, cleaning up the quantization architecture for XPU.
- **[#46116](https://github.com/vllm-project/vllm/pull/46116)** Introduces MoRIIO flexible prefill-TP rank selection, enabling heterogeneous Tensor Parallelism to Data Parallelism (TP<->DP) reads for KV-transfer, crucial for disaggregated serving efficiency.

## More changes by area

<details>
<summary>Performance (18)</summary>

- [#41992](https://github.com/vllm-project/vllm/pull/41992) Support ViT full CUDA graph for Kimi-VL
- [#45826](https://github.com/vllm-project/vllm/pull/45826) Rust Frontend O(n) argument scan in tool parser
- [#44577](https://github.com/vllm-project/vllm/pull/44577) Pack KV caches into contiguous per-block allocations for DeepSeek V4
- [#45969](https://github.com/vllm-project/vllm/pull/45969) Compact chunk-hash keys and zero-copy lookup wire format for Mooncake
- [#45659](https://github.com/vllm-project/vllm/pull/45659) Async lookup to reduce scheduler overhead for Mooncake
- [#45863](https://github.com/vllm-project/vllm/pull/45863) DSv4 flashinfer sparse index cache for metadata, 2%~4% TTFT improvement
- [#46026](https://github.com/vllm-project/vllm/pull/46026) Optimize Qwen3-VL multi-video prompt processing
- [#45743](https://github.com/vllm-project/vllm/pull/45743) Tune Triton indexer score decode for spec-decode
- [#45309](https://github.com/vllm-project/vllm/pull/45309) Optimize dsv4 cudagraph by reducing `eager_break_during_capture`
- [#45972](https://github.com/vllm-project/vllm/pull/45972) Revert "[DSV4 Perf] Optimize dsv4 cudagraph by reducing `eager_break_during_capture`"
- [#45840](https://github.com/vllm-project/vllm/pull/45840) Skip/shrink all_token_ids copy in scheduler for non-async and V2 runner
- [#45854](https://github.com/vllm-project/vllm/pull/45854) Minimax-M3: Enable fp8_per_channel for bf16 weights on mi300x
- [#45988](https://github.com/vllm-project/vllm/pull/45988) Remove unused loggers in `reasoning/`
- [#46048](https://github.com/vllm-project/vllm/pull/46048) Add prefix caching support for 'all' mode in Qwen3.5
- [#45916](https://github.com/vllm-project/vllm/pull/45916) Add Triton split-KV paged decode fallback for gfx12
- [#46112](https://github.com/vllm-project/vllm/pull/46112) Reduce update_from_output CPU overhead for decode batches
- [#46117](https://github.com/vllm-project/vllm/pull/46117) MXFP8 dense-linear + grouped-MoE GEMM optimizations for MiniMax-M3
- [#46123](https://github.com/vllm-project/vllm/pull/46123) FlyDSL BF16 MoE for MiniMax-M3 MXFP8 emulation via --moe-backend aiter
- [#46005](https://github.com/vllm-project/vllm/pull/46005) Support ViT full CUDA graph for DeepSeek-VL2
- [#46065](https://github.com/vllm-project/vllm/pull/46065) Directly Implement AITER Custom All-reduce in CudaCommunicator
- [#45886](https://github.com/vllm-project/vllm/pull/45886) Add user-configurable global/local token budgets for dual-path ViT CUDA graph
- [#46184](https://github.com/vllm-project/vllm/pull/46184) Use flydsl moe with Minimax-M3 mxfp8 weights on gfx950
- [#46051](https://github.com/vllm-project/vllm/pull/46051) Use dedicated runtime for HTTP/request-processing/ZMQ
- [#46103](https://github.com/vllm-project/vllm/pull/46103) TP-shard Lightning indexer prefill
- [#46063](https://github.com/vllm-project/vllm/pull/46063) MiniMax-M3 MXFP8 gemm/group gemm dispatch AITER
- [#46035](https://github.com/vllm-project/vllm/pull/46035) Sparse-attention Triton kernel optimizations for MiniMax-M3
- [#45971](https://github.com/vllm-project/vllm/pull/45971) Parallelize KV load with a receive-thread pool
- [#46172](https://github.com/vllm-project/vllm/pull/46172) Optimize rocm aiter sparse mla indexer
- [#46122](https://github.com/vllm-project/vllm/pull/46122) Optimize aiter moe for DeepSeekV4
- [#46202](https://github.com/vllm-project/vllm/pull/46202) Enable chunked prefill and prefix caching for qwen3.5
</details>

<details>
<summary>Kernels & attention (18)</summary>

- [#45744](https://github.com/vllm-project/vllm/pull/45744) Enable FP8 sparse GQA for M3
- [#44109](https://github.com/vllm-project/vllm/pull/44109) Add weightless RMSNorm CUDA kernels for has_weight=False
- [#46006](https://github.com/vllm-project/vllm/pull/46006) Add PDL support for DeepGEMM kernel
- [#45232](https://github.com/vllm-project/vllm/pull/45232) make custom mask mods fully cudagraphable
- [#42996](https://github.com/vllm-project/vllm/pull/42996) Add PDL support for DeepGEMM kernel
- [#45999](https://github.com/vllm-project/vllm/pull/45999) Revert "[Kernel] Add PDL support for DeepGEMM kernel"
- [#46076](https://github.com/vllm-project/vllm/pull/46076) support dcp for FLASHINFER_MLA_SPARSE
- [#46178](https://github.com/vllm-project/vllm/pull/46178) Support DCP for DeepSeek Sparse Attention
- [#45892](https://github.com/vllm-project/vllm/pull/45892) Minimax-M3 BF16/FP8 Indexer using MSA
- [#46020](https://github.com/vllm-project/vllm/pull/46020) add HPC-Ops Attention backend
- [#46182](https://github.com/vllm-project/vllm/pull/46182) CuTeDSL warmup infrastructure, FA4 MLA
- [#46167](https://github.com/vllm-project/vllm/pull/46167) Add runtime monitor for post-warmup CuTeDSL compilation
- [#46186](https://github.com/vllm-project/vllm/pull/46186) Enable RDNA3 W4A16 GEMM kernels on gfx1151
- [#46000](https://github.com/vllm-project/vllm/pull/46000) MLA prefill per-group FP8 fused output
- [#46189](https://github.com/vllm-project/vllm/pull/46189) Add FLASH_ATTN_MLA_SPARSE backend for Hopper sparse MLA
- [#46273](https://github.com/vllm-project/vllm/pull/46273) Add fused SiLU+Mul+PerTokenQuant CUDA kernel
- [#45881](https://github.com/vllm-project/vllm/pull/45881) Add XPU support for MSA sparse-attention path + tune gemma_rmsnorm for BMG
- [#46166](https://github.com/vllm-project/vllm/pull/46166) Add Vedic 4-bit matmul for MLA attention on CPU
- [#45946](https://github.com/vllm-project/vllm/pull/45946) Use Triton tensor descriptor for output store in lightning attention
- [#46087](https://github.com/vllm-project/vllm/pull/46087) Start SWA/chunked KV-tile loop at first allowed key
- [#45883](https://github.com/vllm-project/vllm/pull/45883) Support FlashQLA backend for qwen3.5
- [#46275](https://github.com/vllm-project/vllm/pull/46275) Enable split sparse decode on gfx942 for DSV4
- [#45991](https://github.com/vllm-project/vllm/pull/45991) Add DeepSeek-V4 fuse_index_q SYCL kernel path
</details>

<details>
<summary>MoE & quantization (11)</summary>

- [#45896](https://github.com/vllm-project/vllm/pull/45896) MiniMax-M3-MXFP4 support added
- [#46001](https://github.com/vllm-project/vllm/pull/46001) Support TEP=16 for the block-FP8 shared expert
- [#43853](https://github.com/vllm-project/vllm/pull/43853) Enable Flashinfer non-gated MoE bf16
- [#44626](https://github.com/vllm-project/vllm/pull/44626) Tag per-channel FP8 weights as PER_CHANNEL so AITER pre-shuffled GEMM is selected
- [#45924](https://github.com/vllm-project/vllm/pull/45924) add HPC-Ops MoE backend
- [#46206](https://github.com/vllm-project/vllm/pull/46206) Enable DeepSeek V4 EPLB across platforms
- [#46031](https://github.com/vllm-project/vllm/pull/46031) NVFP4 dispatch for fused RoPE quantization
- [#45875](https://github.com/vllm-project/vllm/pull/45875) Mxfp8 mtp triton tile tuning
- [#45949](https://github.com/vllm-project/vllm/pull/45949) Add tuned fused_moe config for Qwen3-Coder-Next-FP8 on NVIDIA GB10
- [#45894](https://github.com/vllm-project/vllm/pull/45894) Minimax m3 mxfp4 on 45794
- [#45994](https://github.com/vllm-project/vllm/pull/45994) Pass quant config to Qwen3Next embeddings
- [#45910](https://github.com/vllm-project/vllm/pull/45910) Normalize reshape shapes before RMS quant fusion
- [#45942](https://github.com/vllm-project/vllm/pull/45942) Add native MXFP4 (W4A4) MoE backend for gfx950
</details>

<details>
<summary>Model support (8)</summary>

- [#45990](https://github.com/vllm-project/vllm/pull/45990) Remove BambaForCausalLM
- [#43132](https://github.com/vllm-project/vllm/pull/43132) Add Qwen3 architecture support for EAGLE3
- [#45555](https://github.com/vllm-project/vllm/pull/45555) Add Qwen2-VL/Qwen2.5-VL processor-mapped video loader
- [#45993](https://github.com/vllm-project/vllm/pull/45993) Remove MiniMaxText01, MiniMaxVL01, MiniMaxForCausalLM
- [#45982](https://github.com/vllm-project/vllm/pull/45982) Add experimental MinerU-Diffusion model support
- [#46155](https://github.com/vllm-project/vllm/pull/46155) Alternative bounded sampler path with A100 serving validation for DiffusionGemma
- [#46126](https://github.com/vllm-project/vllm/pull/46126) Add Voice Activity Detection (VAD)
- [#46286](https://github.com/vllm-project/vllm/pull/46286) Upstream State-Aware Monolingual Constraints for DeepSeek-R1
- [#45927](https://github.com/vllm-project/vllm/pull/45927) Support per-video use_audio_in_video for Qwen Omni
- [#45944](https://github.com/vllm-project/vllm/pull/45944) Enable tower/connector LoRA for Qwen2-Audio via a native audio encoder
</details>

<details>
<summary>Parallelism & scheduling (23)</summary>

- [#45181](https://github.com/vllm-project/vllm/pull/45181) Support mixed KV page sizes for DFlash
- [#46039](https://github.com/vllm-project/vllm/pull/46039) Support MiniMax-M3 mixed KV layouts in MoRIIO READ mode
- [#39726](https://github.com/vllm-project/vllm/pull/39726) SimpleCPUOffloadConnector: Add support for reset_cache()
- [#39831](https://github.com/vllm-project/vllm/pull/39831) SimpleCPUOffloadConnector PCP + DCP support
- [#46205](https://github.com/vllm-project/vllm/pull/46205) Support packed HMA KV cache layout
- [#45444](https://github.com/vllm-project/vllm/pull/45444) Skip KV lookup for non-reachable SWA blocks in Mooncake
- [#45595](https://github.com/vllm-project/vllm/pull/45595) Avoid blocking the engine to flush offloads on idle
- [#45757](https://github.com/vllm-project/vllm/pull/45757) Guard CPU eviction check
- [#46004](https://github.com/vllm-project/vllm/pull/46004) Support DeepSeek V4 Mooncake PP/PD shared KV metadata
- [#46090](https://github.com/vllm-project/vllm/pull/46090) Support DFlash speculative decoding for GDN models on CPU
- [#45985](https://github.com/vllm-project/vllm/pull/45985) Support Eagle3 speculative decoding with Pipeline Parallelism
- [#45939](https://github.com/vllm-project/vllm/pull/45939) add partial prefix cache primitives
- [#45934](https://github.com/vllm-project/vllm/pull/45934) support pp+mtp & pp+eagle3
- [#45880](https://github.com/vllm-project/vllm/pull/45880) Support pipeline-parallel prefill in push mode for NIXL
- [#46251](https://github.com/vllm-project/vllm/pull/46251) Decoupling block_size from allocation block size
- [#46145](https://github.com/vllm-project/vllm/pull/46145) Enable Decode Context Parallelism for sparse MLA
- [#46019](https://github.com/vllm-project/vllm/pull/46019) Detect and clean up stalled transfer jobs
- [#45951](https://github.com/vllm-project/vllm/pull/45951) implement ngram-cpu in MRV2
- [#45953](https://github.com/vllm-project/vllm/pull/45953) Make Dynamic SD comatible with Full Cuda Graphs
- [#46210](https://github.com/vllm-project/vllm/pull/46210) add torchcomms backend for xpu support
- [#45964](https://github.com/vllm-project/vllm/pull/45964) Query replication for MLA decode
- [#45966](https://github.com/vllm-project/vllm/pull/45966) Pre-reserve packed A2A decode workspace
- [#46234](https://github.com/vllm-project/vllm/pull/46234) Release NCCL communicator memory in sleep mode
- [#46289](https://github.com/vllm-project/vllm/pull/46289) Reclaim KV blocks leaked by aborted remote KV recv
- [#45947](https://github.com/vllm-project/vllm/pull/45947) Enable cross layers KV Cache in Model Runner V2
- [#46011](https://github.com/vllm-project/vllm/pull/46011) Drop stale scheduler requests before scheduling
- [#46216](https://github.com/vllm-project/vllm/pull/46216) Maintain evictable list in LRUCachePolicy
- [#46252](https://github.com/vllm-project/vllm/pull/46252) Gate packed HMA KV cache on cross-layer config
- [#46008](https://github.com/vllm-project/vllm/pull/46008) Send KV to D when prefill first token is a stop token
- [#46217](https://github.com/vllm-project/vllm/pull/46217) Place remainder PP layers on the last stage(s)
</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#44991](https://github.com/vllm-project/vllm/pull/44991) Skip Triton kernel monkey-patches when Triton-CPU is available
- [#46135](https://github.com/vllm-project/vllm/pull/46135) Enable fp16 support for PowerPC
- [#46110](https://github.com/vllm-project/vllm/pull/46110) Detect ROCm via KFD topology when amdsmi cannot enumerate GPUs
- [#46226](https://github.com/vllm-project/vllm/pull/46226) Set per-worker ZE_AFFINITY_MASK for workers
</details>

<details>
<summary>API & serving (22)</summary>

- [#45026](https://github.com/vllm-project/vllm/pull/45026) Stop setting CUDA_VISIBLE_DEVICES internally in vLLM, add device_ids arg
- [#45919](https://github.com/vllm-project/vllm/pull/45919) Add reasoning/tool parsing to /derender + fix byte-fallback FFFD
- [#44938](https://github.com/vllm-project/vllm/pull/44938) Rust Frontend Support prompt-only completions
- [#45957](https://github.com/vllm-project/vllm/pull/45957) Add labeled metrics support for KV Offloading
- [#40912](https://github.com/vllm-project/vllm/pull/40912) Report cache usage in Anthropic /v1/messages API
- [#44801](https://github.com/vllm-project/vllm/pull/44801) Rust Frontend: Add `/get_world_size` route with static parallel size
- [#45950](https://github.com/vllm-project/vllm/pull/45950) Return model metadata fields in /v1/models
- [#45805](https://github.com/vllm-project/vllm/pull/45805) Support hybrid/external DP LB in Python supervised bootstrap
- [#44382](https://github.com/vllm-project/vllm/pull/44382) Add /abort_requests endpoint
- [#45848](https://github.com/vllm-project/vllm/pull/45848) Add serde defaults for omit_defaults fields in `EngineCoreSamplingParams`
- [#45737](https://github.com/vllm-project/vllm/pull/45737) Expose CPU cache usage metric
- [#45876](https://github.com/vllm-project/vllm/pull/45876) Validate tokenized bad_words vocabulary range
- [#45868](https://github.com/vllm-project/vllm/pull/45868) Various model/config compatibility fixes
- [#46099](https://github.com/vllm-project/vllm/pull/46099) Remove dead prepare_structured_tag override in Cohere parser
- [#44638](https://github.com/vllm-project/vllm/pull/44638) return routed_experts on streaming generate responses
- [#44446](https://github.com/vllm-project/vllm/pull/44446) Migration to support quantized model by default [5/N]
- [#45877](https://github.com/vllm-project/vllm/pull/45877) Port DeepSeek V4 to streaming parser engine framework
- [#46146](https://github.com/vllm-project/vllm/pull/46146) Add routed experts statistics collection with REST API
- [#45893](https://github.com/vllm-project/vllm/pull/45893) Replace xgrammar's built-in structural tag with vLLM's implementation
- [#45890](https://github.com/vllm-project/vllm/pull/45890) Add static HTTPS and mTLS support in Rust Frontend
- [#46007](https://github.com/vllm-project/vllm/pull/46007) Add Orthrus speculative decoding support
- [#45945](https://github.com/vllm-project/vllm/pull/45945) Add metric label and tiering plumbing support for KV Offloading
- [#45981](https://github.com/vllm-project/vllm/pull/45981) Version prefix-cache keys for local runtime LoRA reloads
- [#45958](https://github.com/vllm-project/vllm/pull/45958) Add basic offloading metrics
- [#45959](https://github.com/vllm-project/vllm/pull/45959) Add tiering metric plumbing
- [#46057](https://github.com/vllm-project/vllm/pull/46057) Integrate `xgrammar-structural-tag` for `strict` and `required` tool calling
- [#45948](https://github.com/vllm-project/vllm/pull/45948) Add optional persistent disk cache for compiled xgrammar grammars
- [#46129](https://github.com/vllm-project/vllm/pull/46129) Support `truncate_prompt_tokens` and `truncation_side` in Rust Frontend
- [#46081](https://github.com/vllm-project/vllm/pull/46081) Add /tokenizer_info endpoint
- [#46306](https://github.com/vllm-project/vllm/pull/46306) expose profiler control routes in Rust frontend
- [#46219](https://github.com/vllm-project/vllm/pull/46219) Support echo for token-ID completion prompts
- [#46153](https://github.com/vllm-project/vllm/pull/46153) Add explicit video frame index selection
- [#46137](https://github.com/vllm-project/vllm/pull/46137) Support thinking_token_budget for chat and completions
- [#46279](https://github.com/vllm-project/vllm/pull/46279) Support `--max-log-len` in Rust Frontend
- [#46085](https://github.com/vllm-project/vllm/pull/46085) Add aot_eager backend for piecewise compilation
- [#46052](https://github.com/vllm-project/vllm/pull/46052) Add opt-in native-tls crypto backend for the Rust frontend
</details>

<details>
<summary>Tests (15)</summary>

- [#45679](https://github.com/vllm-project/vllm/pull/45679) Add request_finished fence population tests for offloading scheduler
- [#45996](https://github.com/vllm-project/vllm/pull/45996) Make FP32 Gumbel sampling more accurate
- [#45708](https://github.com/vllm-project/vllm/pull/45708) Add Qwen3 streaming parser delta boundary cases
- [#45873](https://github.com/vllm-project/vllm/pull/45873) Validate Cohere Embed Mixed Content Payloads
- [#45905](https://github.com/vllm-project/vllm/pull/45905) Remove dummy worker-side stats from OffloadingConnector
- [#46044](https://github.com/vllm-project/vllm/pull/46044) Disable parallel-agnostic fs-tier cache on V2 model runner
- [#45857](https://github.com/vllm-project/vllm/pull/45857) Update deepgemm log
- [#46241](https://github.com/vllm-project/vllm/pull/46241) Replace InternVL2-1B with InternVL3-1B in test_pipeline_parallel.py
- [#46176](https://github.com/vllm-project/vllm/pull/46176) Use vLLM's fp8 quant max in AITER hipBLASLt accuracy test
- [#45933](https://github.com/vllm-project/vllm/pull/45933) Add mixed serving boundary benchmark
- [#46064](https://github.com/vllm-project/vllm/pull/46064) Add unit test for _fwd_kernel_ep_scatter_1
- [#46171](https://github.com/vllm-project/vllm/pull/46171) Add unit tests for IdentityReasoningParser
- [#46274](https://github.com/vllm-project/vllm/pull/46274) Add Qwen3 streaming tool-call regression tests
- [#45874](https://github.com/vllm-project/vllm/pull/45874) Add test suite for PoolsideV1ReasoningParser
- [#46128](https://github.com/vllm-project/vllm/pull/46128) Add unit test for ep_gather kernel
- [#45899](https://github.com/vllm-project/vllm/pull/45899) Add unit test for chunk_scaled_dot_kkt_fwd kernel
- [#46061](https://github.com/vllm-project/vllm/pull/46061) Add unit test for apply_expert_map kernel
- [#46059](https://github.com/vllm-project/vllm/pull/46059) Add unit test for l2norm_fwd_kernel1 and l2norm_fwd_kernel2
- [#46134](https://github.com/vllm-project/vllm/pull/46134) Add unit test for merge_attn_states kernel
- [#46068](https://github.com/vllm-project/vllm/pull/46068) Reject negative values for max_logprobs and long_prefill_token_threshold
- [#46073](https://github.com/vllm-project/vllm/pull/46073) Add unit test for per_token_quant_int8 kernel
- [#45931](https://github.com/vllm-project/vllm/pull/45931) Disable TileLang MHC dispatch on gfx942
- [#45963](https://github.com/vllm-project/vllm/pull/45963) Disable dynamic speculative decoding when DP is enabled
- [#46013](https://github.com/vllm-project/vllm/pull/46013) Expose vllm.inputs.data for Ray Data LLM compatibility
- [#46267](https://github.com/vllm-project/vllm/pull/46267) Resurrect test_rocm_mxfp4_moe_oracle
- [#46160](https://github.com/vllm-project/vllm/pull/46160) Skip unsupported test cases on ROCm
- [#45921](https://github.com/vllm-project/vllm/pull/45921) Enable test_silu_mul_fp8_quant_deep_gemm on XPU
</details>

<details>
<summary>CI & build (14)</summary>

- [#46173](https://github.com/vllm-project/vllm/pull/46173) Migrate test_openai_schema.py to schemathesis 4.x
- [#46080](https://github.com/vllm-project/vllm/pull/46080) Fix Kernels Attention test groups
- [#44650](https://github.com/vllm-project/vllm/pull/44650) add model runner v2 into CI
- [#45970](https://github.com/vllm-project/vllm/pull/45970) move lora%N test to mi300 and gate
- [#46298](https://github.com/vllm-project/vllm/pull/46298) Fix gfx942 Kernels MoE test group
- [#43802](https://github.com/vllm-project/vllm/pull/43802) Enable mxfp4 lora test for ROCm platform gfx950
- [#46024](https://github.com/vllm-project/vllm/pull/46024) Fix e2e core test group
- [#40367](https://github.com/vllm-project/vllm/pull/40367) bump up vllm-xpu-kernels v0.1.10 and upgrade 2618 umd
- [#46109](https://github.com/vllm-project/vllm/pull/46109) Skip Qwen3.5-35B-A3B-MXFP4-AITER-TP2 for non gfx950
- [#45967](https://github.com/vllm-project/vllm/pull/45967) skip test_double_aiter_rms_quant_fusion
- [#45865](https://github.com/vllm-project/vllm/pull/45865) Run pre-commit on self-hosted vllm-runners
- [#40287](https://github.com/vllm-project/vllm/pull/40287) Update nixl to v0.10.1 in Dockerfile
- [#45654](https://github.com/vllm-project/vllm/pull/45654) Avoid duplicate ViT CG test introduced by accident
- [#46053](https://github.com/vllm-project/vllm/pull/46053) Temporarily remove markmc from CODEOWNERS
- [#46180](https://github.com/vllm-project/vllm/pull/46180) Pin `test_rocm_compressed_tensors_w8a8` to TRITON_ATTN
- [#45870](https://github.com/vllm-project/vllm/pull/45870) fix server test file path
- [#45843](https://github.com/vllm-project/vllm/pull/45843) Pin NIXL to 1.2.0
- [#46017](https://github.com/vllm-project/vllm/pull/46017) Improvement of Docker image build for IBM Power
- [#46098](https://github.com/vllm-project/vllm/pull/46098) Bump the minor-update group across 1 directory with 144 updates
- [#46089](https://github.com/vllm-project/vllm/pull/46089) First Attempt at Pod Snapshotting
- [#45973](https://github.com/vllm-project/vllm/pull/45973) switch to ubuntu 24.04 as base image
</details>

<details>
<summary>Docs (6)</summary>

- [#45762](https://github.com/vllm-project/vllm/pull/45762) Update stale LMCache examples
- [#45975](https://github.com/vllm-project/vllm/pull/45975) Move CI failure diagnosis docs into ci-fails-buildkite skill
- [#45279](https://github.com/vllm-project/vllm/pull/45279) add docs for selective offload
- [#46181](https://github.com/vllm-project/vllm/pull/46181) Fix dead link in docs
- [#46197](https://github.com/vllm-project/vllm/pull/46197) Add Qwen3 forced alignment online example
- [#46229](https://github.com/vllm-project/vllm/pull/46229) add AFK integration
- [#46248](https://github.com/vllm-project/vllm/pull/46248) Clarify prefix caching metrics and APC verification workflow
</details>

<details>
<summary>Bugfixes (82)</summary>

- [#42727](https://github.com/vllm-project/vllm/pull/42727) Fix AWQ dequantize on Intel XPU and refactor AutoAWQ config
- [#45681](https://github.com/vllm-project/vllm/pull/45681) Functional fixes for DeepSeek V4 on MI300X/MI325X
- [#45852](https://github.com/vllm-project/vllm/pull/45852) Pre-initialise streaming reasoning state when prompt ends inside an open `<|channel>`
- [#45935](https://github.com/vllm-project/vllm/pull/45935) Fix MiniMaxM2ForCausalLM perf regression
- [#42120](https://github.com/vllm-project/vllm/pull/42120) Fix corrupt outputs in MoE FP8 LoRA responses
- [#46159](https://github.com/vllm-project/vllm/pull/46159) Fix U+FFFD leak at reasoning-to-content transition in engine parsers
- [#45823](https://github.com/vllm-project/vllm/pull/45823) Defer `on_request_finished` until in-flight transfers drain
- [#45747](https://github.com/vllm-project/vllm/pull/45747) Fix rocm_aiter_per_tensor_quant custom op aliasing
- [#45879](https://github.com/vllm-project/vllm/pull/45879) Fix NixlConnector handshake block_len validation for GQA-replicated KV heads
- [#45675](https://github.com/vllm-project/vllm/pull/45675) Upgrade Starlette to >= 1.0.1 to fix CVE-2026-48710
- [#44602](https://github.com/vllm-project/vllm/pull/44602) preserve inline system message position for prefix caching
- [#46025](https://github.com/vllm-project/vllm/pull/46025) auto-detect template support for mid-conversation system messages
- [#45196](https://github.com/vllm-project/vllm/pull/45196) Validate DefaultModelLoader / LoadConfig and fail with clear errors
- [#46231](https://github.com/vllm-project/vllm/pull/46231) Defer offload reads while transfers are pending
- [#43984](https://github.com/vllm-project/vllm/pull/43984) Handle non-finite numbers in coerce_to_schema_type
- [#45895](https://github.com/vllm-project/vllm/pull/45895) Indexer init skip and MTP TopK share for iteration
- [#45832](https://github.com/vllm-project/vllm/pull/45832) Fix parsing when thinking is disabled
- [#45371](https://github.com/vllm-project/vllm/pull/45371) Disable Mooncake TP put-striding when DCP > 1
- [#45255](https://github.com/vllm-project/vllm/pull/45255) Fix gridDim.y overflow for large row counts
- [#45589](https://github.com/vllm-project/vllm/pull/45589) Fix MoE model load OOM in FlashInfer_TRTLLM backend with sleep mode
- [#45361](https://github.com/vllm-project/vllm/pull/45361) Fix INT8 per-token-head KV cache rounding in Triton reshape-and-cache
- [#46038](https://github.com/vllm-project/vllm/pull/46038) Fall back to Pydantic loc for param in validation errors
- [#45466](https://github.com/vllm-project/vllm/pull/45466) Check output alignment in vectorize_with_alignment
- [#45720](https://github.com/vllm-project/vllm/pull/45720) Fix MiniMax-M3 FP8 KV cache dtype
- [#45195](https://github.com/vllm-project/vllm/pull/45195) Clean up compiled-model bytecode hooks on VllmRunner exit
- [#46305](https://github.com/vllm-project/vllm/pull/46305) Fix multi-video crash with list-valued fps/num_frames
- [#45782](https://github.com/vllm-project/vllm/pull/45782) Fallback GFX942 sparse MLA ops to Triton
- [#46199](https://github.com/vllm-project/vllm/pull/46199) Move extract_layer_index back inside is_v32 guard
- [#46070](https://github.com/vllm-project/vllm/pull/46070) Revert #42379 to fix CI `Multi-Modal Models (Extended Generation 1)`
- [#43179](https://github.com/vllm-project/vllm/pull/43179) Fix _riscv_supports_rvv_vlen128() to detect RVV on hardware without zvl flags
- [#46091](https://github.com/vllm-project/vllm/pull/46091) Fix empty tool block silently dropping subsequent content
- [#46254](https://github.com/vllm-project/vllm/pull/46254) Fix NVFP4/OCP MX MoE emulation
- [#46047](https://github.com/vllm-project/vllm/pull/46047) Fix Qwen3 latent bug in partial params dropping values containing `<`
- [#45040](https://github.com/vllm-project/vllm/pull/45040) Don't reject fp8_e5m2 KV cache for non-fp8 quantized checkpoints
- [#45794](https://github.com/vllm-project/vllm/pull/45794) MiniMax-M3 (AMD): add packed_modules_mapping and pass swiglu…
- [#44468](https://github.com/vllm-project/vllm/pull/44468) Fix test_spec_decode_logprobs: use FLASH_ATTN for XPU in GPU_DETERMINISM_KWARGS
- [#44469](https://github.com/vllm-project/vllm/pull/44469) Fix test_logprobs_e2e import error: pin lm-eval[api]>=0.4.12
- [#45656](https://github.com/vllm-project/vllm/pull/45656) Restore is_sym guard for zp in GPTQ/CT MoE to fix symmetric quant regression
- [#45706](https://github.com/vllm-project/vllm/pull/45706) Fix probabilistic draft probs test attention backend
- [#45908](https://github.com/vllm-project/vllm/pull/45908) enforce audio decode duration limit in chat completions path
- [#45448](https://github.com/vllm-project/vllm/pull/45448) Complete one-shot fused all-reduce PDL at end to avoid NaN
- [#45093](https://github.com/vllm-project/vllm/pull/45093) Fix Stale Encoder Cache After Weight Update
- [#46125](https://github.com/vllm-project/vllm/pull/46125) Revert "Fix Stale Encoder Cache After Weight Update"
- [#45917](https://github.com/vllm-project/vllm/pull/45917) Pass TP group to FlashInfer all-reduce fusion
- [#45849](https://github.com/vllm-project/vllm/pull/45849) fix hidden states nan for hybrid attention models
- [#45941](https://github.com/vllm-project/vllm/pull/45941) Fix SD LoRA
- [#46222](https://github.com/vllm-project/vllm/pull/46222) Bugfix ROCm Sparse Indexer
- [#44912](https://github.com/vllm-project/vllm/pull/44912) Fix FP8 per-tensor scale rank mismatch causing Inductor assertion failure
- [#45509](https://github.com/vllm-project/vllm/pull/45509) Fix Language Models Test (Extended Generation) failures
- [#45831](https://github.com/vllm-project/vllm/pull/45831) Fix DSV4 disaggregated serving
- [#44665](https://github.com/vllm-project/vllm/pull/44665) Fix memory pointer overflow in Mamba state buffers
- [#42332](https://github.com/vllm-project/vllm/pull/42332) Fixes MiniCPM-O resampler device placement to avoid tensor device mismatch
- [#45867](https://github.com/vllm-project/vllm/pull/45867) Render reasoning on assistant turns without tool_calls
- [#35530](https://github.com/vllm-project/vllm/pull/35530) Fix stale doc URL and docstring module path
- [#43958](https://github.com/vllm-project/vllm/pull/43958) Fix FP8 block-scaled scheme selection on non-CUDA platforms
- [#46046](https://github.com/vllm-project/vllm/pull/46046) Fix VRAM not freed in test_phi3v
- [#45312](https://github.com/vllm-project/vllm/pull/45312) Reject unsupported compressed tensors KV cache schemes
- [#45897](https://github.com/vllm-project/vllm/pull/45897) Fix scheduler plugin test
- [#45913](https://github.com/vllm-project/vllm/pull/45913) Use Salesforce/wikitext for ppl tests
- [#44725](https://github.com/vllm-project/vllm/pull/44725) Fix Anthropic count_tokens decorator order driving server load negative
- [#46095](https://github.com/vllm-project/vllm/pull/46095) Fix MRv2 memory leak test
- [#46198](https://github.com/vllm-project/vllm/pull/46198) Guard model_config access in _log_compilation_config
- [#46243](https://github.com/vllm-project/vllm/pull/46243) Fix min_tokens off-by-one in the V2 GPU sampler
- [#46120](https://github.com/vllm-project/vllm/pull/46120) resolve vLLM performance and API issues
- [#46290](https://github.com/vllm-project/vllm/pull/46290) Fix MoRIIO WRITE mode for mixed KV layouts
- [#45909](https://github.com/vllm-project/vllm/pull/45909) defer reasoning→tool transition when boundary token tex…
- [#46285](https://github.com/vllm-project/vllm/pull/46285) Handle missing req_id in `update_from_output()` with PP + tool-calling
- [#46215](https://github.com/vllm-project/vllm/pull/46215) Warm up Triton kernels before JIT monitor
- [#46288](https://github.com/vllm-project/vllm/pull/46288) Don't override an explicit text_config.tie_word_embeddings on transformers v5 multimodal configs
- [#46271](https://github.com/vllm-project/vllm/pull/46271) Fix for issue #15697
- [#45984](https://github.com/vllm-project/vllm/pull/45984) Fix thinking_token_budget not enforced after natural </think> re-entry
- [#46238](https://github.com/vllm-project/vllm/pull/46238) Disable FlashInfer autotune for trtllm_bf16_moe on SM100 during warmup
- [#46284](https://github.com/vllm-project/vllm/pull/46284) Fix KV offload request-finished lifecycle contract
- [#46278](https://github.com/vllm-project/vllm/pull/46278) Fix SimpleCPUOffloadConnector GPU->CPU store race
- [#46301](https://github.com/vllm-project/vllm/pull/46301) Fix hidden-state extraction block size for hybrid verifiers
- [#46127](https://github.com/vllm-project/vllm/pull/46127) Make Kimi's tool parser accept numeric only tool call IDs
- [#46034](https://github.com/vllm-project/vllm/pull/46034) Enable dual-path ViT CUDA graph for Step3-VL
- [#46151](https://github.com/vllm-project/vllm/pull/46151) Revert "Fix corrupt outputs in MoE FP8 LoRA responses"
- [#46157](https://github.com/vllm-project/vllm/pull/46157) Fix segfault in mixed-batch GQA attention scheduling
- [#46213](https://github.com/vllm-project/vllm/pull/46213) Fix Qwen3-Omni audio-in-video image/video merge crash
- [#46211](https://github.com/vllm-project/vllm/pull/46211) Parse compact sentence-transformers pooling_mode
- [#46212](https://github.com/vllm-project/vllm/pull/46212) Fix DiffusionGemma self-conditioning with tensor parallelism
- [#46233](https://github.com/vllm-project/vllm/pull/46233) Quiet weight prefetch logs during shutdown
- [#46140](https://github.com/vllm-project/vllm/pull/46140) Fix fireredlid compatibility
- [#46023](https://github.com/vllm-project/vllm/pull/46023) Release in-process LLM resources on deletion
- [#46032](https://github.com/vllm-project/vllm/pull/46032) Add support for SWA draft models in speculative decoding
- [#46162](https://github.com/vllm-project/vllm/pull/46162) Forward upstream error message in Anthropic streaming converter
- [#46177](https://github.com/vllm-project/vllm/pull/46177) Support tensor parallelism for DiffusionGemma
- [#46139](https://github.com/vllm-project/vllm/pull/46139) Defer KV offload re-admit with pending jobs
- [#46082](https://github.com/vllm-project/vllm/pull/46082) Defer re-admission of preempted request with in-flight offloading stores
- [#46203](https://github.com/vllm-project/vllm/pull/46203) Fix cumem sleep and teardown
- [#46093](https://github.com/vllm-project/vllm/pull/46093) Fix Cohere embed billed image token accounting for mixed-content inputs
- [#45887](https://github.com/vllm-project/vllm/pull/45887) Gemma 4: stack variable-length audio clips for multi-audio prompts
- [#46142](https://github.com/vllm-project/vllm/pull/46142) Fix tests to not dispatch on `UNFUSED_TRITON` backend on MI300
- [#46257](https://github.com/vllm-project/vllm/pull/46257) DeepSeek-V4 tokenizer: honor add_generation_prompt and continue_final_message
- [#46152](https://github.com/vllm-project/vllm/pull/46152) resolve #38736 — [Transformers v5] Tarsier2ForConditionalGeneration
- [#46281](https://github.com/vllm-project/vllm/pull/46281) Align hybrid model prefix cache hit lengths to prevent block missing on EAGLE
- [#45923](https://github.com/vllm-project/vllm/pull/45923) Revert "[FlexAttention] make custom mask mods fully cudagraphable"
- [#46150](https://github.com/vllm-project/vllm/pull/46150) Revert "[bugfix]Indexer init skip and MTP TopK share for iteration"
- [#46147](https://github.com/vllm-project/vllm/pull/46147) resolve #38425 — [Transformers v5] InternVL2
- [#46276](https://github.com/vllm-project/vllm/pull/46276) weights processing memory reduction for MoE models on NVidia hardware
- [#46287](https://github.com/vllm-project/vllm/pull/46287) fix(lora): contain filesystem resolver paths
- [#46003](https://github.com/vllm-project/vllm/pull/46003) Support MTP speculative decoding with pipeline parallelism on the PD producer side
- [#46086](https://github.com/vllm-project/vllm/pull/46086) Fix v2 mrope `ValueError: Error during index put operation`
- [#46067](https://github.com/vllm-project/vllm/pull/46067) Fix dangling decode scratch when workspace grows after cudagraph capture
- [#46114](https://github.com/vllm-project/vllm/pull/46114) Fix chunk alignment when using context parallelism with TRITON_MLA
- [#46170](https://github.com/vllm-project/vllm/pull/46170) Avoid mutating tool parameters in _get_tool_schema_defs
- [#46108](https://github.com/vllm-project/vllm/pull/46108) ColQwen3.5: fix retrieval correctness
- [#46196](https://github.com/vllm-project/vllm/pull/46196) resolve model chat template before deciding inline-system merge
- [#46194](https://github.com/vllm-project/vllm/pull/46194) Anchor "Dynamo bytecode transform" OTEL span to wall-clock time
- [#46225](https://github.com/vllm-project/vllm/pull/46225) Strip special tokens in non-streaming engine parsing
- [#46236](https://github.com/vllm-project/vllm/pull/46236) Raise actionable error instead of bare assert for group-size/TP mismatch
- [#46115](https://github.com/vllm-project/vllm/pull/46115) MoRIIO toy P/D proxy: fix DP-rank index aliasing
- [#46066](https://github.com/vllm-project/vllm/pull/46066) Fix num_output_placeholders underflow with async scheduling + spec decode
- [#46195](https://github.com/vllm-project/vllm/pull/46195) Fix PP broadcast hangs when a GPU device error occurs on a peer worker
- [#45978](https://github.com/vllm-project/vllm/pull/45978) Honor override_generation_config for special tokens
- [#46292](https://github.com/vllm-project/vllm/pull/46292) resolve issue #42426
- [#45960](https://github.com/vllm-project/vllm/pull/45960) Seed RayExecutorV2 TCPStore port by DP rank to avoid collisions
- [#46294](https://github.com/vllm-project/vllm/pull/46294) resolve issue #22519
- [#46015](https://github.com/vllm-project/vllm/pull/46015) parse compact sentence-transformer pooling mode
- [#46280](https://github.com/vllm-project/vllm/pull/46280) YaRN RoPE: honor explicit attention_factor from the rope config
- [#46132](https://github.com/vllm-project/vllm/pull/46132) Handle GPU/MIG UUIDs in CUDA_VISIBLE_DEVICES
- [#46050](https://github.com/vllm-project/vllm/pull/46050) Fix cumem teardown segfault via ordered MemPool release
- [#46149](https://github.com/vllm-project/vllm/pull/46149) Structural-tag grammar omits reasoning prefix
- [#46154](https://github.com/vllm-project/vllm/pull/46154) Fix mixed-batch GQA decode detection
- [#46002](https://github.com/vllm-project/vllm/pull/46002) Do not select FA4 (CuTe SM100 kernel) on SM120
- [#45952](https://github.com/vllm-project/vllm/pull/45952) Reject float16 in Marlin MXFP8 kernel selection
- [#45891](https://github.com/vllm-project/vllm/pull/45891) Fix reasoning-end detection to check prompt tail only
- [#45965](https://github.com/vllm-project/vllm/pull/45965) Add stability window to DiffusionGemma to match HF stability_threshold semantics
- [#46124](https://github.com/vllm-project/vllm/pull/46124) Parse MiniMax M3 visible reasoning markers
- [#46304](https://github.com/vllm-project/vllm/pull/46304) Skip stale KV xfer finish notifications for already-freed requests
- [#46207](https://github.com/vllm-project/vllm/pull/46207) improve DCP/PCP error messages with actionable guidance
- [#46223](https://github.com/vllm-project/vllm/pull/46223) Fix Nixl/Mooncake/Offloading connectors forcing HND layout for MSA-based models
</details>

<details>
<summary>Refactors (5)</summary>

- [#44681](https://github.com/vllm-project/vllm/pull/44681) Remove dead cutlass mxfp8 code
- [#45415](https://github.com/vllm-project/vllm/pull/45415) final _C library kernel migration
- [#45454](https://github.com/vllm-project/vllm/pull/45454) Remove dead quantization code and tests
- [#46102](https://github.com/vllm-project/vllm/pull/46102) Harmony Responses API Refactor to use HarmonyParser
- [#46022](https://github.com/vllm-project/vllm/pull/46022) Refactor ServingTokenization entrypoint
- [#45976](https://github.com/vllm-project/vllm/pull/45976) Refactor w4a8 MoE Oracle to OOP
- [#46030](https://github.com/vllm-project/vllm/pull/46030) Responses API parser state into conversation context
- [#45936](https://github.com/vllm-project/vllm/pull/45936) Consolidate ZMQ context manager
- [#46096](https://github.com/vllm-project/vllm/pull/46096) Generalize use of `WhisperModelState`
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
