# vllm: PR digest (2026-07-12 to 2026-07-16)

_157 merged, 263 newly opened - source vllm-project/vllm, generated 2026-07-16T11:11:19Z_

## TL;DR
- **Model focus:** DeepSeek dominated the window with extensive optimizations across V3/V4 (sparse MLA, MXFP4/FP8 MoE, DFlash/DSpark speculative decoding, and specialized routing kernels). Gemma, Qwen, and a new "Inkling" model family also saw significant feature work.
- **KV Cache & Offloading:** A massive architectural shift is underway with newly-opened work on KV cache tiering residency and lifecycle management, supported by merged CPU offloading connectors and clean backend configuration boundaries.
- **Performance & Kernels:** Major kernel additions include a fused DSA indexer Top-k kernel (LiteTopk), a hybrid W4A16 linear kernel for ROCm (Triton prefill + HIP decode), and generic cuteDSL LL BF16 router GEMMs.
- **Speculative Decoding:** Expanded support for DFlash/DSpark on CPU and XPU, integration with AITER sparse paged attention on ROCm, and newly-opened adaptive speculative decoding for ModelRunner V2.
- **Overall Direction:** The engine is heavily optimizing for complex, massive-scale MoE/MLA architectures (like DeepSeek) while building out robust, multi-tiered KV cache management and expanding hardware-specific fast paths (ROCm AITER, XPU, Arm CPU).

## Most important PRs
- **[#48837](https://github.com/vllm-project/vllm/pull/48837)** (newly opened): Introduces comprehensive KV cache tiering residency and lifecycle management. This massive architectural change enables dynamic promotion and eviction of cache blocks across GPU and CPU memory tiers, fundamentally changing how memory is managed for long-context and hybrid models.
- **[#48799](https://github.com/vllm-project/vllm/pull/48799)** (merged): Adds initial support for the Inkling model family. This includes attention, MoE, and multimodal components, paving the way for a new class of models with subsequent in-progress PRs adding TML, LoRA, and MTP support.
- **[#47327](https://github.com/vllm-project/vllm/pull/47327)** (merged): Implements a dense Multi-Head Attention (MHA) path for sparse Multi-Head Latent Attention (MLA) on short sequences. This optimizes prefill performance for DeepSeek models by bypassing sparse overhead when the sequence length doesn't justify it.
- **[#48726](https://github.com/vllm-project/vllm/pull/48726)** (newly opened): Proposes a fused DSA indexer Top-k kernel (LiteTopk) for FlashInfer. This significantly reduces kernel launch overhead and memory traffic during the indexing phase of sparse attention, driving major performance gains.
- **[#40977](https://github.com/vllm-project/vllm/pull/40977)** (merged): Adds a `HybridW4A16LinearKernel` for ROCm hardware. By combining Triton for compute-bound prefills and native HIP for memory-bound skinny decodes, it maximizes throughput and minimizes latency for INT4 quantized models on AMD GPUs.

## More changes by area

<details>
<summary>Performance (29)</summary>

- [#48792](https://github.com/vllm-project/vllm/pull/48792) (newly opened) ReplaySSM: cache SSM inputs for faster Gated DeltaNet standard decode
- [#48637](https://github.com/vllm-project/vllm/pull/48637) (newly opened) INT8 Fused MoE Kernel for Arm CPUs
- [#48597](https://github.com/vllm-project/vllm/pull/48597) (newly opened) GLM-5.2/DSv3.2 Blackwell decode optimizations
- [#48728](https://github.com/vllm-project/vllm/pull/48728) (newly opened) Fuse native FP8 shared expert into AITER MXFP4 MoE for DeepSeek V4
- [#48498](https://github.com/vllm-project/vllm/pull/48498) (newly opened) Add Triton kernel for Gemma3n sparse GELU
- [#48382](https://github.com/vllm-project/vllm/pull/48382) (newly opened) Reload layout-preserving weights directly
- [#48789](https://github.com/vllm-project/vllm/pull/48789) (newly opened) Add Triton Proton profiling backend
- [#48727](https://github.com/vllm-project/vllm/pull/48727) (newly opened) Use AITER tgemm for DeepSeek V4 compressors
- [#48660](https://github.com/vllm-project/vllm/pull/48660) (newly opened) Optimize dsv4 routing using specialized kernel
- [#48581](https://github.com/vllm-project/vllm/pull/48581) (newly opened) Route gfx942 fp8_mqa_logits to AITER's Gluon kernel
- [#48796](https://github.com/vllm-project/vllm/pull/48796) (newly opened) Disable mm_prefix attention when vision inputs are disabled
- [#48442](https://github.com/vllm-project/vllm/pull/48442) (newly opened) Zero-copy torch.Tensor pickling in shm_broadcast MessageQueue
- [#48759](https://github.com/vllm-project/vllm/pull/48759) (newly opened) Optimize TrtLlmLoRAExperts
- [#48544](https://github.com/vllm-project/vllm/pull/48544) (newly opened) Speed up offline prompt tokenization by 2.4x
- [#48531](https://github.com/vllm-project/vllm/pull/48531) (newly opened) Vectorize prepare_value on the KV load path for Mooncake
- [#48825](https://github.com/vllm-project/vllm/pull/48825) (newly opened) Tune h20 moe config e256 n512
- [#48774](https://github.com/vllm-project/vllm/pull/48774) (newly opened) Tune LL BF16 Router GEMM
- [#48735](https://github.com/vllm-project/vllm/pull/48735) (newly opened) Improve `--linear-backend` filtering
- [#48736](https://github.com/vllm-project/vllm/pull/48736) (newly opened) Avoid Triton recompiles for multimodal attention ranges
- [#48737](https://github.com/vllm-project/vllm/pull/48737) (newly opened) Vectorize pooling prompt-token padding in InputBatch
- [#48763](https://github.com/vllm-project/vllm/pull/48763) (newly opened) Fix moe `reduce_scatter` perf regression by removing additional comm
- [#47718](https://github.com/vllm-project/vllm/pull/47718) (merged) Optimize DSv4 two-stage compressor kernel for HCA prefill
- [#48137](https://github.com/vllm-project/vllm/pull/48137) (merged) Remove redundant repeat and copy for dsv4
- [#48385](https://github.com/vllm-project/vllm/pull/48385) (merged) Add pad-aware reduce path
- [#47463](https://github.com/vllm-project/vllm/pull/47463) (merged) Optimize `fused_topk_bias` for DSv4
- [#47006](https://github.com/vllm-project/vllm/pull/47006) (merged) Replace Qwen MOE all-reduce with reduce-scatter
- [#48064](https://github.com/vllm-project/vllm/pull/48064) (merged) Enable FlashInfer MNNVL allreduce RMS quant fusion
- [#45000](https://github.com/vllm-project/vllm/pull/45000) (merged) Fix GDN KKT warmup regression on RDNA
- [#48519](https://github.com/vllm-project/vllm/pull/48519) (merged) Optimize sparse attention prefill kernel for DeepSeek-V4

</details>

<details>
<summary>Kernels & attention (19)</summary>

- [#48605](https://github.com/vllm-project/vllm/pull/48605) (newly opened) Add TRITON_MLA SWA support
- [#48770](https://github.com/vllm-project/vllm/pull/48770) (newly opened) Enable masked MHA for sparse MLA prefills
- [#48619](https://github.com/vllm-project/vllm/pull/48619) (newly opened) Port DeepGemm MHC Kernel to CuTeDSL
- [#48582](https://github.com/vllm-project/vllm/pull/48582) (newly opened) Improve indexer for long-context decode on sm100
- [#48805](https://github.com/vllm-project/vllm/pull/48805) (newly opened) Exhaustive sparse-MLA Triton kernel warmup
- [#48484](https://github.com/vllm-project/vllm/pull/48484) (newly opened) Replicated embedding and norm fusion
- [#48407](https://github.com/vllm-project/vllm/pull/48407) (newly opened) Skip sparse indexer scoring for dense short prefills
- [#48757](https://github.com/vllm-project/vllm/pull/48757) (newly opened) Fuse Transformers Residual Add, RMSNorm, and FP8 Quantization on ROCm
- [#48558](https://github.com/vllm-project/vllm/pull/48558) (newly opened) MXFP4 indexer cache for GLM-5.2 / DSA
- [#48666](https://github.com/vllm-project/vllm/pull/48666) (newly opened) Gemma-4 FA4 FP8 Kernel
- [#42562](https://github.com/vllm-project/vllm/pull/42562) (merged) Add generic cuteDSL LL BF16 router (GEMM)
- [#47287](https://github.com/vllm-project/vllm/pull/47287) (merged) Add AITER sparse paged attention for MiniMax-M3 on ROCm
- [#48512](https://github.com/vllm-project/vllm/pull/48512) (merged) Add Helion kernel benchmark script
- [#47973](https://github.com/vllm-project/vllm/pull/47973) (merged) Add BF16x3 router GEMM
- [#48287](https://github.com/vllm-project/vllm/pull/48287) (merged) Add pad-aware swiglu limit kernel
- [#39058](https://github.com/vllm-project/vllm/pull/39058) (merged) Implement CUDA kernel for ReLUSquaredActivation
- [#48011](https://github.com/vllm-project/vllm/pull/48011) (merged) Make sliding-window support an explicit backend capability
- [#48264](https://github.com/vllm-project/vllm/pull/48264) (merged) Helion kernel lazy registration
- [#47060](https://github.com/vllm-project/vllm/pull/47060) (merged) Mirror Triton KV dtype checks in MLA

</details>

<details>
<summary>MoE & quantization (14)</summary>

- [#48505](https://github.com/vllm-project/vllm/pull/48505) (newly opened) Add MXFP4 expert cache support to DeepSeek V4
- [#48606](https://github.com/vllm-project/vllm/pull/48606) (newly opened) Support Quark AWQ INT4 exports
- [#48548](https://github.com/vllm-project/vllm/pull/48548) (newly opened) Integrate ScaleSweep NVFP4 quantization kernel
- [#48538](https://github.com/vllm-project/vllm/pull/48538) (newly opened) Add `nvfp4_per_token` online MoE quantization
- [#48427](https://github.com/vllm-project/vllm/pull/48427) (newly opened) Requantize serialized MXFP8 linears to FP8 PTPC on ROCm
- [#48476](https://github.com/vllm-project/vllm/pull/48476) (newly opened) MXFP8 weight support and load-time BMM optimization for DeepSeek-V4 on XPU
- [#48460](https://github.com/vllm-project/vllm/pull/48460) (newly opened) Support partial fused MoE LoRA adapters
- [#48552](https://github.com/vllm-project/vllm/pull/48552) (newly opened) Convert awq-packed MoE qweight to gptq-equivalent layout on XPU
- [#48451](https://github.com/vllm-project/vllm/pull/48451) (merged) Add int4 quantization support for emulation moe backend
- [#46390](https://github.com/vllm-project/vllm/pull/46390) (merged) Enable humming w[2-7]a[4,8] inference with compressed-tensors
- [#48632](https://github.com/vllm-project/vllm/pull/48632) (merged) Integrate flashinfer MoE LoRA for BF16 model
- [#47521](https://github.com/vllm-project/vllm/pull/47521) (merged) Support INT2 XPU WOQ Linear
- [#47881](https://github.com/vllm-project/vllm/pull/47881) (merged) Migrate moe sp support to non-torch compiled path for GLM5.2
- [#44462](https://github.com/vllm-project/vllm/pull/44462) (merged) Increase FlashInfer fp8 moe topk to 32

</details>

<details>
<summary>Model support (15)</summary>

- [#48841](https://github.com/vllm-project/vllm/pull/48841) (newly opened) Enable TML inkling on ROCm
- [#48553](https://github.com/vllm-project/vllm/pull/48553) (newly opened) Add LongCat-Next multimodal MoE model support
- [#48686](https://github.com/vllm-project/vllm/pull/48686) (newly opened) Add minimal native RWKV7 serving support
- [#48410](https://github.com/vllm-project/vllm/pull/48410) (newly opened) Add Apertus 1.5 multimodality
- [#48768](https://github.com/vllm-project/vllm/pull/48768) (newly opened) Add Inkling LoRA and MTP support
- [#48791](https://github.com/vllm-project/vllm/pull/48791) (newly opened) Enable sequence pooling for embedding and classification models
- [#48822](https://github.com/vllm-project/vllm/pull/48822) (newly opened) Add breakable CUDA graph support for Inkling
- [#48291](https://github.com/vllm-project/vllm/pull/48291) (merged) Add Cosmos3 Edge Reasoner model
- [#48390](https://github.com/vllm-project/vllm/pull/48390) (merged) Support fp32 lm_head for generation models via head_dtype
- [#48463](https://github.com/vllm-project/vllm/pull/48463) (merged) Add Support for BertForMaskedLM
- [#48594](https://github.com/vllm-project/vllm/pull/48594) (merged) Enable LoRA support for tower and connector in LlavaNextVideo
- [#47991](https://github.com/vllm-project/vllm/pull/47991) (merged) Add RobertaForTokenClassification / XLMRobertaForTokenClassification
- [#48525](https://github.com/vllm-project/vllm/pull/48525) (merged) Support fp32 lm_head on the LoRA path
- [#47568](https://github.com/vllm-project/vllm/pull/47568) (merged) Add sliding window attention support for qwen-eagle3
- [#48775](https://github.com/vllm-project/vllm/pull/48775) (merged) Use unused tokens for image/audio placeholder token ids in Inkling

</details>

<details>
<summary>Parallelism & scheduling (37)</summary>

- [#48715](https://github.com/vllm-project/vllm/pull/48715) (newly opened) Dynamic-fork scheduling, Medusa/MTP spec decode, and InternVL resize
- [#48692](https://github.com/vllm-project/vllm/pull/48692) (newly opened) Adaptive Speculative Decoding initial support
- [#48474](https://github.com/vllm-project/vllm/pull/48474) (newly opened) Add DFlare support and update V2 engine speculative methods
- [#48464](https://github.com/vllm-project/vllm/pull/48464) (newly opened) Add generic imperative KV-connector step lifecycle helpers
- [#48456](https://github.com/vllm-project/vllm/pull/48456) (newly opened) Add explicit layer parallel plans
- [#48409](https://github.com/vllm-project/vllm/pull/48409) (newly opened) Add runtime LoRA weight updates
- [#48679](https://github.com/vllm-project/vllm/pull/48679) (newly opened) Add self-describing events for tier promotions
- [#48392](https://github.com/vllm-project/vllm/pull/48392) (newly opened) DFlash/DSpark draft support under decode context parallelism
- [#48798](https://github.com/vllm-project/vllm/pull/48798) (newly opened) Add tiering offloading metrics
- [#48649](https://github.com/vllm-project/vllm/pull/48649) (newly opened) Add context parallelism for minimax m3 indexer
- [#48804](https://github.com/vllm-project/vllm/pull/48804) (newly opened) Warm Eagle spec-decode Triton kernels at startup
- [#48704](https://github.com/vllm-project/vllm/pull/48704) (newly opened) Support prompt cache retention policies for tiered KV offloading
- [#48414](https://github.com/vllm-project/vllm/pull/48414) (newly opened) Fragment-major canonical CPU layout for KV offload
- [#48488](https://github.com/vllm-project/vllm/pull/48488) (newly opened) Waiting-Queue-Informed LRU for Prefix Cache Eviction
- [#48838](https://github.com/vllm-project/vllm/pull/48838) (newly opened) Add public build_full_block_hash_chain helper for offline prefix-cache analysis
- [#48630](https://github.com/vllm-project/vllm/pull/48630) (newly opened) Avoid rejection sampler OOM by chunking
- [#48479](https://github.com/vllm-project/vllm/pull/48479) (newly opened) Update vendored LMCache connector for current IPCCacheServerKey API
- [#48783](https://github.com/vllm-project/vllm/pull/48783) (newly opened) Make KV-cache dtype support platform-aware
- [#48641](https://github.com/vllm-project/vllm/pull/48641) (newly opened) Stop upcasting logits to fp32 in apply_sampling_params
- [#48657](https://github.com/vllm-project/vllm/pull/48657) (newly opened) Add an explicit sequence_parallel_moe override
- [#48639](https://github.com/vllm-project/vllm/pull/48639) (newly opened) Support loading sample_from_anchor flag from speculators config
- [#47423](https://github.com/vllm-project/vllm/pull/47423) (merged) CPU Offloading EC Connector
- [#48150](https://github.com/vllm-project/vllm/pull/48150) (merged) Define clean backend configuration boundary for KV Offload
- [#46384](https://github.com/vllm-project/vllm/pull/46384) (merged) Support partial prefix cache hit for hybrid model
- [#46090](https://github.com/vllm-project/vllm/pull/46090) (merged) Support DFlash speculative decoding for GDN models on CPU
- [#47782](https://github.com/vllm-project/vllm/pull/47782) (merged) Preserve Marconi caching with selective hybrid cache retention
- [#47636](https://github.com/vllm-project/vllm/pull/47636) (merged) Well-known default host/port env vars and per-DP-rank control port for KVOffload
- [#47677](https://github.com/vllm-project/vllm/pull/47677) (merged) Add DSpark speculative decoding support for DeepSeek-V4 on XPU
- [#42433](https://github.com/vllm-project/vllm/pull/42433) (merged) Add EC Transfer Params
- [#48180](https://github.com/vllm-project/vllm/pull/48180) (merged) Add DCP + Eagle support for Tokenspeed MLA backends
- [#47021](https://github.com/vllm-project/vllm/pull/47021) (merged) Avoid reading expired blocks in bidirectional turn-2 read
- [#47984](https://github.com/vllm-project/vllm/pull/47984) (merged) Support speculative decode with AITER sparse PA on ROCm
- [#48209](https://github.com/vllm-project/vllm/pull/48209) (merged) Vectorize prep xfer list creation
- [#46725](https://github.com/vllm-project/vllm/pull/46725) (merged) Runtime Draft Weight Update for Speculative Decoding
- [#47987](https://github.com/vllm-project/vllm/pull/47987) (merged) Make tiering offload region DP-replica aware
- [#48787](https://github.com/vllm-project/vllm/pull/48787) (merged) Add kv_cache_dtype to speculative_config
- [#46662](https://github.com/vllm-project/vllm/pull/46662) (merged) Optimize TPOT for thinking budget when used with speculative decoding

</details>

<details>
<summary>Hardware & arch (10)</summary>

- [#40714](https://github.com/vllm-project/vllm/pull/40714) (merged) Create Proper Numa topology for s390x CPU
- [#41934](https://github.com/vllm-project/vllm/pull/41934) (merged) Register batch-invariant kernels for XPU
- [#48350](https://github.com/vllm-project/vllm/pull/48350) (merged) Optimize Qwen3.5 on H20
- [#48159](https://github.com/vllm-project/vllm/pull/48159) (merged) Add tuned selective_state_update config for AMD MI350
- [#48373](https://github.com/vllm-project/vllm/pull/48373) (merged) Retune MI355 selective_state_update float32 config
- [#48372](https://github.com/vllm-project/vllm/pull/48372) (merged) Retune MI355 selective_state_update float16 config
- [#48526](https://github.com/vllm-project/vllm/pull/48526) (merged) Re-enable cudagraph memory profiling on ROCm
- [#48440](https://github.com/vllm-project/vllm/pull/48440) (merged) Re-disable CUDA graph memory profiling on ROCm
- [#44849](https://github.com/vllm-project/vllm/pull/44849) (merged) Dispatch fused QK-norm + AllReduce via AITER for MiniMax-M2
- [#48483](https://github.com/vllm-project/vllm/pull/48483) (merged) Lower memory required for capturing cudagraphs for large sizes

</details>

<details>
<summary>API & serving (15)</summary>

- [#48575](https://github.com/vllm-project/vllm/pull/48575) (newly opened) Migrate to hf-hub 1.0 in Rust Frontend
- [#48617](https://github.com/vllm-project/vllm/pull/48617) (newly opened) Add round trip parity test and docs for derender
- [#48543](https://github.com/vllm-project/vllm/pull/48543) (newly opened) Add diarized_json support for MOSS-Transcribe-Diarize
- [#48535](https://github.com/vllm-project/vllm/pull/48535) (newly opened) Populate `num_cache_creation_tokens` in Messages
- [#48781](https://github.com/vllm-project/vllm/pull/48781) (newly opened) Use zero-copy slicing for multimodal tensors in Rust Frontend
- [#48461](https://github.com/vllm-project/vllm/pull/48461) (newly opened) Apply current settings to Harmony continuations
- [#48584](https://github.com/vllm-project/vllm/pull/48584) (newly opened) Add support for truncate_prompt_tokens and truncation_side
- [#48800](https://github.com/vllm-project/vllm/pull/48800) (newly opened) Add hy_v3 reasoning parser
- [#48554](https://github.com/vllm-project/vllm/pull/48554) (merged) Integrate MM audio support in Rust Frontend
- [#43463](https://github.com/vllm-project/vllm/pull/43463) (merged) Expose logprob_token_ids on Python OpenAI endpoints
- [#47741](https://github.com/vllm-project/vllm/pull/47741) (merged) Add Seed-OSS tool parser to Rust Frontend
- [#48034](https://github.com/vllm-project/vllm/pull/48034) (merged) Tolerate whitespace before outer brace in JSON tool-call parsers
- [#48134](https://github.com/vllm-project/vllm/pull/48134) (merged) Limit chat top_logprobs in responses in Rust Frontend
- [#47173](https://github.com/vllm-project/vllm/pull/47173) (merged) Add /abort_requests to the RLHF dev API router
- [#47965](https://github.com/vllm-project/vllm/pull/47965) (merged) Wait for mock engine endpoints before ZMQ connect

</details>

<details>
<summary>Tests (24)</summary>

- [#48571](https://github.com/vllm-project/vllm/pull/48571) (newly opened) Add unit test for chunk_fwd_kernel_o kernel
- [#48640](https://github.com/vllm-project/vllm/pull/48640) (newly opened) Cover Nemotron V3 required XML tool parsing
- [#47666](https://github.com/vllm-project/vllm/pull/47666) (merged) Split cpu_cache_usage_perc into write/read usage gauges
- [#47754](https://github.com/vllm-project/vllm/pull/47754) (merged) Enable KV cache events for HMA models in CPU offloading test
- plus 20 more minor test updates

</details>

<details>
<summary>CI & build (40)</summary>

- [#48761](https://github.com/vllm-project/vllm/pull/48761) (newly opened) Add XPU yaml configuration
- [#48811](https://github.com/vllm-project/vllm/pull/48811) (newly opened) Bump the minor-update group across 1 directory
- [#48818](https://github.com/vllm-project/vllm/pull/48818) (newly opened) Changes for relevant cpu tests and image build for ZenDNN
- [#48646](https://github.com/vllm-project/vllm/pull/48646) (newly opened) Share communication runtime layers across CI and release images
- [#48677](https://github.com/vllm-project/vllm/pull/48677) (newly opened) Upgrade to torch 2.13 for XPU
- [#48472](https://github.com/vllm-project/vllm/pull/48472) (merged) Add SPDX license header to Rust/Protobuf sources
- [#48387](https://github.com/vllm-project/vllm/pull/48387) (merged) Configure MI300 tests for native execution without DinD
- [#46527](https://github.com/vllm-project/vllm/pull/46527) (merged) Cache Rust builds by source inputs on ROCm
- [#44549](https://github.com/vllm-project/vllm/pull/44549) (merged) Replace diskcache to eliminate pickle deserialization
- [#48289](https://github.com/vllm-project/vllm/pull/48289) (merged) Build macOS arm64 CPU wheel natively on the macmini queue
- plus 30 more minor CI updates

</details>

<details>
<summary>Docs (6)</summary>

- [#48790](https://github.com/vllm-project/vllm/pull/48790) (newly opened) Add Pixeltable integration to inference & serving docs
- [#48782](https://github.com/vllm-project/vllm/pull/48782) (newly opened) Expand ModelOpt NVFP4 docs
- [#48497](https://github.com/vllm-project/vllm/pull/48497) (merged) Document pooling config resolution
- [#45437](https://github.com/vllm-project/vllm/pull/45437) (merged) Sync four function docstrings with their signatures
- [#48802](https://github.com/vllm-project/vllm/pull/48802) (merged) Fix error key name
- [#48293](https://github.com/vllm-project/vllm/pull/48293) (merged) Add DeepseekV32ForCausalLM to supported_models.md

</details>

<details>
<summary>Bugfixes (193)</summary>

- [#48642](https://github.com/vllm-project/vllm/pull/48642) (newly opened) Enable fp8_ds_mla dense prefill for Sparse MLA
- [#48550](https://github.com/vllm-project/vllm/pull/48550) (newly opened) Initialize MiniMax M3 reasoning from prompt mode
- [#48425](https://github.com/vllm-project/vllm/pull/48425) (newly opened) Handle per-group prefix-hit divergence for hybrid models with KV connector
- [#48701](https://github.com/vllm-project/vllm/pull/48701) (newly opened) Reduce CuMem weight-load memory
- [#48608](https://github.com/vllm-project/vllm/pull/48608) (newly opened) Fix video loading sample over presentable frames
- [#48459](https://github.com/vllm-project/vllm/pull/48459) (newly opened) Exclude DSpark draft-model KV-cache group from core prefix-cache lookup veto
- [#48438](https://github.com/vllm-project/vllm/pull/48438) (newly opened) Preserve Marlin runtime tensor storage across weight reload
- [#48470](https://github.com/vllm-project/vllm/pull/48470) (newly opened) Validate GPTQ kernel inputs to prevent OOB reads
- [#48413](https://github.com/vllm-project/vllm/pull/48413) (newly opened) Fix MiniCPM-V placeholder replacement and image processor loading
- [#48588](https://github.com/vllm-project/vllm/pull/48588) (newly opened) Pad unaligned N in SM12x CUTLASS blockwise FP8 GEMM
- [#48583](https://github.com/vllm-project/vllm/pull/48583) (merged) Fix concurrent sparse invariant race bypassing CVE remediation
- [#47606](https://github.com/vllm-project/vllm/pull/47606) (merged) Flush engine reasoning parser at engine-reasoning → tool streaming boundary
- [#48631](https://github.com/vllm-project/vllm/pull/48631) (merged) Fix FlashAttention reported MLA dimension support
- [#48167](https://github.com/vllm-project/vllm/pull/48167) (merged) Fix FlashInfer non-causal draft attention on Blackwell
- [#47770](https://github.com/vllm-project/vllm/pull/47770) (merged) Fix Triton W4A16 handling for GPTQ/AutoGPTQ qzeros layout
- [#48261](https://github.com/vllm-project/vllm/pull/48261) (merged) Fix stale attn metadata in speculator prefill cudagraph capture
- [#48481](https://github.com/vllm-project/vllm/pull/48481) (merged) Fix PD async scheduling race condition for hybrid attn models
- [#48262](https://github.com/vllm-project/vllm/pull/48262) (merged) Fix Gemma4 parser channel-less output consistently
- [#44371](https://github.com/vllm-project/vllm/pull/44371) (merged) Preserve unloaded non-persistent buffers during layerwise reload
- [#48671](https://github.com/vllm-project/vllm/pull/48671) (merged) Support heterogeneous QK fusion geometry in Spec Decode
- plus 173 more minor bugfixes

</details>

<details>
<summary>Refactors (6)</summary>

- [#48496](https://github.com/vllm-project/vllm/pull/48496) (newly opened) Remove unnecessary `load_weights` methods
- [#48780](https://github.com/vllm-project/vllm/pull/48780) (newly opened) Remove deepseek dead code
- [#48500](https://github.com/vllm-project/vllm/pull/48500) (newly opened) Move fla to third party
- [#46647](https://github.com/vllm-project/vllm/pull/46647) (merged) Move iteration logging to the frontend
- [#48717](https://github.com/vllm-project/vllm/pull/48717) (merged) Unify `_logical_to_remote_kernel_block_ids`
- [#45781](https://github.com/vllm-project/vllm/pull/45781) (merged) Rename VLLM_TRITON_ATTN_USE_TD to VLLM_TRITON_USE_TD

</details>

<details>
<summary>Other (7)</summary>

- [#48713](https://github.com/vllm-project/vllm/pull/48713) (newly opened) Add eager mode weight hook
- [#48807](https://github.com/vllm-project/vllm/pull/48807) (newly opened) Wrap each kernel_warmup call in try/except
- [#48599](https://github.com/vllm-project/vllm/pull/48599) (newly opened) Move env check function to platform interface
- [#48030](https://github.com/vllm-project/vllm/pull/48030) (merged) Log fully resolved pooling config at startup
- [#48057](https://github.com/vllm-project/vllm/pull/48057) (merged) Improve Matryoshka pooling dimensions validation
- [#48549](https://github.com/vllm-project/vllm/pull/48549) (merged) Clean up "swap_space"
- [#48467](https://github.com/vllm-project/vllm/pull/48467) (merged) Remove force channels_last in Idefics3MultiModalProcessor

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f11c3e19a0fbe74b2486db26a61ebfade3dfb8f0cb9a12dc55f76450b2f07c26 -->
