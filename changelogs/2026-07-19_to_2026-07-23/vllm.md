# vllm: PR digest (2026-07-19 to 2026-07-23)

_144 merged, 306 newly opened - source vllm-project/vllm, generated 2026-07-23T11:19:49Z_

## TL;DR
*   **DeepSeek dominance:** Major focus on DeepSeek models (V2, V3, V4, R1), including MXFP4 indexer KV caches, query replication for MLA decode, and new CPU/AMD hardware support.
*   **Attention & MRV2:** Significant architectural churn around ModelRunner V2 (MRV2) and Producer-Consumer Pipeline (PCP) for MLA, including a major merge and subsequent revert of virtual-batch PCP, plus new FlashAttention PCP support for GQA.
*   **MoE & Quantization:** Heavy investment in MoE, migrating W4A16 to the MK oracle scheme, adding online MXFP4 quantization, and introducing DeepGEMM BF16 grouped-GEMM MoE backends.
*   **Hardware expansion:** Expanded capabilities with native AMX-FP8 attention for Intel Diamond Rapids CPUs, Granite-4 CPU support, and extensive ROCm AITER sparse MLA additions.
*   **Frontend & Serving:** Continued Rust frontend maturation (extracting shared chat types, adding gRPC server/model discovery) and parallelized preprocessing for pooling models to boost throughput.

## Most important PRs
*   **[#46570](https://github.com/vllm-project/vllm/pull/46570)** & **[#49196](https://github.com/vllm-project/vllm/pull/49196)**: Added MRV2 virtual-batch Producer-Consumer Pipeline (PCP) for MLA, but was quickly reverted, highlighting ongoing stabilization efforts for MLA pipelines.
*   **[#49517](https://github.com/vllm-project/vllm/pull/49517)**: Optimizes PCP KV updates with direct peer stores, a massive architectural change for FlashInfer and attention on NVIDIA hardware (currently in progress).
*   **[#44120](https://github.com/vllm-project/vllm/pull/44120)**: Migrates the `MoeWNA16Method` quantization method to use the new MK oracle scheme, significantly refactoring Triton MoE kernels for better performance.
*   **[#49153](https://github.com/vllm-project/vllm/pull/49153)**: Parallelizes preprocessing within the same request for online serving of pooling models, removing a major frontend bottleneck.
*   **[#49086](https://github.com/vllm-project/vllm/pull/49086)**: Introduces new Triton-based MoE backends for ROCm, enabling int4/int8 weight-only quantization on AMD hardware (currently in progress).

## More changes by area

<details>
<summary>Performance (20)</summary>

- [#47451](https://github.com/vllm-project/vllm/pull/47451) Add new warmup infrastructure for JITs
- [#48531](https://github.com/vllm-project/vllm/pull/48531) Vectorize prepare_value on the KV load path for Mooncake
- [#48957](https://github.com/vllm-project/vllm/pull/48957) Skip empty c128 kernel launch for DeepSeek-V4, improving kernel performance 2x
- [#49396](https://github.com/vllm-project/vllm/pull/49396) Offload derender CPU work to renderer thread pool
- [#49487](https://github.com/vllm-project/vllm/pull/49487) Avoid transient Inkling result allocations to prevent OOM on smaller memory configs
- [#49219](https://github.com/vllm-project/vllm/pull/49219) Fuse GDN decode core for CPU
- [#49194](https://github.com/vllm-project/vllm/pull/49194) Eliminate staging from NCCL symmetric reduce-scatter for MoE
- [#49459](https://github.com/vllm-project/vllm/pull/49459) Reload layout-preserving weights directly in the model loader
- [#49462](https://github.com/vllm-project/vllm/pull/49462) Add mm_tensor_ipc=cuda_ipc TP-aware GPU transport
- [#49371](https://github.com/vllm-project/vllm/pull/49371) Batch Mamba2 prefill SSM state saves into one indexed copy
- [#49436](https://github.com/vllm-project/vllm/pull/49436) Implement 3D-grid tiling of the state-copy Triton kernels
- [#49236](https://github.com/vllm-project/vllm/pull/49236) Optimize workspace reuse for eager break in DeepSeek-V4
- [#49150](https://github.com/vllm-project/vllm/pull/49150) Avoid per-step pinned staging allocation in apply_grammar_bitmask
- [#49171](https://github.com/vllm-project/vllm/pull/49171) Skip logits and sampling for unfinished prefills
- [#49131](https://github.com/vllm-project/vllm/pull/49131) Use shape-adaptive tile config for batch-invariant matmul on SM80
- [#49500](https://github.com/vllm-project/vllm/pull/49500) Skip redundant full-fit admission pass in KV cache
- [#49078](https://github.com/vllm-project/vllm/pull/49078) Load B weights via TMA tensor descriptor on SM90+ for fused_moe
- [#49390](https://github.com/vllm-project/vllm/pull/49390) Raise Blackwell CUDA graph capture default to 1024
- [#49531](https://github.com/vllm-project/vllm/pull/49531) Optimize DeepSeek-OCR-2 TTFT
- [#49160](https://github.com/vllm-project/vllm/pull/49160) Stream sparse-attn compress softmax to cut register pressure for DeepSeek-V4

</details>

<details>
<summary>Kernels & attention (24)</summary>

- [#42569](https://github.com/vllm-project/vllm/pull/42569) Add FlashAttention 4 SM100 FP8 kv cache support
- [#49294](https://github.com/vllm-project/vllm/pull/49294) Ignore empty MLA context chunks during merge
- [#45964](https://github.com/vllm-project/vllm/pull/45964) Implement query replication for MLA decode (DeepSeek-V2/R1 + Kimi-K2.5)
- [#44492](https://github.com/vllm-project/vllm/pull/44492) Populate draft seq_lens_cpu_upper_bound for spec-decode attention metadata
- [#49364](https://github.com/vllm-project/vllm/pull/49364) Always build attn metadata at capture time in MRV2
- [#49427](https://github.com/vllm-project/vllm/pull/49427) Restore `gather_and_maybe_dequant_cache` OOB guard
- [#47268](https://github.com/vllm-project/vllm/pull/47268) Fix non-coalesced HBM access in marlin_int4_fp8_preprocess_kernel_awq
- [#49121](https://github.com/vllm-project/vllm/pull/49121) Experiment with hisparse routed experts
- [#49077](https://github.com/vllm-project/vllm/pull/49077) Support TRITON_ATTN for KV cache dtype fp8 on SM75 to pre-SM89
- [#49358](https://github.com/vllm-project/vllm/pull/49358) Add opt-in FlashInfer TRTLLM-GEN sparse decode for MiniMax-M3
- [#49555](https://github.com/vllm-project/vllm/pull/49555) Implement return indexer topk of sparse attention
- [#49564](https://github.com/vllm-project/vllm/pull/49564) Add FlashAttention PCP support for GQA on MRv2
- [#49425](https://github.com/vllm-project/vllm/pull/49425) Add FlashInfer SSD prefill backend for Mamba
- [#49085](https://github.com/vllm-project/vllm/pull/49085) Add IndexCache support for DeepSeek V4 on Hopper
- [#49263](https://github.com/vllm-project/vllm/pull/49263) Add densemha support to ROCm AITER Sparse MLA
- [#49154](https://github.com/vllm-project/vllm/pull/49154) Pipeline Triton prefill-attention K/V loads for long BF16/FP16 prefills
- [#49331](https://github.com/vllm-project/vllm/pull/49331) Support encoder-only attention in ModelRunner V2
- [#49202](https://github.com/vllm-project/vllm/pull/49202) Fix DiffusionGemma sliding window attention mismatch with transformers
- [#49372](https://github.com/vllm-project/vllm/pull/49372) Respect declared attention contract for ColQwen3.5 retrievers
- [#49199](https://github.com/vllm-project/vllm/pull/49199) Fix MiniMax M3 index_topk kernel for non-power-of-2 num_idx_heads
- [#49357](https://github.com/vllm-project/vllm/pull/49357) Bound FlashMLA sparse decode intermediate tensors size
- [#49494](https://github.com/vllm-project/vllm/pull/49494) Skip generic attention during piecewise CUDA graph capture
- [#49139](https://github.com/vllm-project/vllm/pull/49139) Fix persistent top-k histogram reuse after short rows
- [#49451](https://github.com/vllm-project/vllm/pull/49451) Revert MRV2 always building attn metadata at capture time

</details>

<details>
<summary>MoE & quantization (29)</summary>

- [#44214](https://github.com/vllm-project/vllm/pull/44214) Enable router replay output from FlashInfer monolithic MoE kernel
- [#48044](https://github.com/vllm-project/vllm/pull/48044) Add Fused Shared Expert Support for AMD Quark DeepSeek-V4 Model Checkpoints
- [#48334](https://github.com/vllm-project/vllm/pull/48334) Implement FP8 o_proj with fp8_bmm and load-time scale transpose for XPU
- [#49489](https://github.com/vllm-project/vllm/pull/49489) Make shared NVFP4 MoE scales writable
- [#48563](https://github.com/vllm-project/vllm/pull/48563) Fix ModelOpt mixed-precision MoE config mapping for Gemma4
- [#47122](https://github.com/vllm-project/vllm/pull/47122) Add quant input when preparing for fusedmoe on XPU
- [#49381](https://github.com/vllm-project/vllm/pull/49381) Redesign LinearMethod classes using the generic QuantKey-driven method
- [#49347](https://github.com/vllm-project/vllm/pull/49347) Add online MXFP4 quantization support
- [#49272](https://github.com/vllm-project/vllm/pull/49272) Add opt-in DeepGEMM BF16 grouped-GEMM MoE backend
- [#49321](https://github.com/vllm-project/vllm/pull/49321) Add W4A16 cold-expert CPU offload via in-graph HIP gather
- [#49099](https://github.com/vllm-project/vllm/pull/49099) Improve SM90 NVFP4 Marlin MoE wide-N alignment
- [#49312](https://github.com/vllm-project/vllm/pull/49312) Add optional HPC BF16xFP32 router GEMM
- [#49313](https://github.com/vllm-project/vllm/pull/49313) Online-requant unquantized layers via quantization_config override
- [#49335](https://github.com/vllm-project/vllm/pull/49335) Swizzle mxfp8 activation scales after DP/EP dispatch for FlashInfer CUTLASS
- [#49207](https://github.com/vllm-project/vllm/pull/49207) Respect explicit WNA16 MoE backend
- [#49084](https://github.com/vllm-project/vllm/pull/49084) Add fused-MoE-LoRA non-adapter neutrality regression test
- [#49336](https://github.com/vllm-project/vllm/pull/49336) Fix DBRX MoE weight loading after FusedMoE/MoERunner refactor
- [#49096](https://github.com/vllm-project/vllm/pull/49096) Fix Humming MoE shapes for non-gated activations
- [#49115](https://github.com/vllm-project/vllm/pull/49115) Move FlashInfer MoE autotune before memory profiling and logging
- [#49258](https://github.com/vllm-project/vllm/pull/49258) Support llm-compressor Inkling NVFP4 weights
- [#49184](https://github.com/vllm-project/vllm/pull/49184) Capture routed experts from supported monolithic MoE kernels in MRV2
- [#49087](https://github.com/vllm-project/vllm/pull/49087) Drop redundant zeros_like and use ceil-div grid for zero-expert identity
- [#49553](https://github.com/vllm-project/vllm/pull/49553) Honor checkpoint per-layer quantization config for Qwen3.5 MTP draft layers
- [#49539](https://github.com/vllm-project/vllm/pull/49539) Fix Fused_moe dimension mismatch for Qwen mxfp4 model on ROCM
- [#49501](https://github.com/vllm-project/vllm/pull/49501) Fix Humming W4 packing for dense INT4 weights
- [#49363](https://github.com/vllm-project/vllm/pull/49363) Add FP8 block-scaled GEMM to fp8_gemm benchmark
- [#49465](https://github.com/vllm-project/vllm/pull/49465) Enable triton-cpu path for Turbo-quant algorithm
- [#48917](https://github.com/vllm-project/vllm/pull/48917) Propagate quant_config to LFM2 ShortConv projections
- [#49350](https://github.com/vllm-project/vllm/pull/49350) Skip moe weight padding for eplb on ROCm

</details>

<details>
<summary>Model support (18)</summary>

- [#47641](https://github.com/vllm-project/vllm/pull/47641) Enable granite-4 model on CPU
- [#48993](https://github.com/vllm-project/vllm/pull/48993) Compact MXFP4 indexer KV cache and packed group overlays for DeepSeek
- [#41653](https://github.com/vllm-project/vllm/pull/41653) Add DeepSeek MTP parallel-load tests
- [#45991](https://github.com/vllm-project/vllm/pull/45991) Add DeepSeek-V4 fuse_index_q SYCL kernel path for XPU
- [#49415](https://github.com/vllm-project/vllm/pull/49415) Fix DeepSeek-V4 DSpark draft shared-expert padding for TP > 8
- [#49190](https://github.com/vllm-project/vllm/pull/49190) Fix Cosmos3 Edge checkpoint weights filtering, video loading, and prompt expansion
- [#49292](https://github.com/vllm-project/vllm/pull/49292) Fix Qwen3-VL M-RoPE on the Transformers modeling backend
- [#47298](https://github.com/vllm-project/vllm/pull/47298) Fix Ovis2_5 special tokens for transformers v5
- [#49193](https://github.com/vllm-project/vllm/pull/49193) Restore MiniCPM-V 4.6 ViT QKV weight loader
- [#49433](https://github.com/vllm-project/vllm/pull/49433) Add support for Nanbeige4.2
- [#49120](https://github.com/vllm-project/vllm/pull/49120) Honor fp32 head_dtype in Inkling muP logits
- [#49457](https://github.com/vllm-project/vllm/pull/49457) Add granite swa support
- [#49525](https://github.com/vllm-project/vllm/pull/49525) Fix shared MM text-LoRA mapper fallback for language_model wrappers
- [#49062](https://github.com/vllm-project/vllm/pull/49062) Remove redundant all_gather_interleave in ViT split_qkv
- [#49484](https://github.com/vllm-project/vllm/pull/49484) Fix GLM-4.1V video placeholder token ID handling
- [#49397](https://github.com/vllm-project/vllm/pull/49397) Skip Qwen3 deepstack buffers without vision
- [#49243](https://github.com/vllm-project/vllm/pull/49243) Add gemma-4-E4B-it-assistant to CI gsm8k for GemmaMTP
- [#48952](https://github.com/vllm-project/vllm/pull/48952) Remap Cosmos3 FP8 ModelOpt/Diffusers

</details>

<details>
<summary>Parallelism & scheduling (37)</summary>

- [#48679](https://github.com/vllm-project/vllm/pull/48679) Support self-describing KV events with TieringOffloadingSpec
- [#48425](https://github.com/vllm-project/vllm/pull/48425) Handle per-group prefix-hit divergence for hybrid models with KV connector
- [#48860](https://github.com/vllm-project/vllm/pull/48860) Fix prefix-cache metrics double-counted when a KV connector defers requests
- [#48317](https://github.com/vllm-project/vllm/pull/48317) Count per-group blocks in get_max_concurrency_for_kv_cache_config
- [#49146](https://github.com/vllm-project/vllm/pull/49146) Handle queued request aborts without allocated KV blocks in KV Offloading
- [#48911](https://github.com/vllm-project/vllm/pull/48911) Preserve reachable tails for hybrid SWA groups in KV Offload
- [#47574](https://github.com/vllm-project/vllm/pull/47574) Zero new KV blocks for quantized + sliding-window hybrid caches
- [#49140](https://github.com/vllm-project/vllm/pull/49140) Implement dual-mode graph storage for CUDA graph tensor identity
- [#49506](https://github.com/vllm-project/vllm/pull/49506) Order single-key store admission by ending token position in KV Offload
- [#49502](https://github.com/vllm-project/vllm/pull/49502) Support reliable partial-tail KV offload for sub-block prompts
- [#49138](https://github.com/vllm-project/vllm/pull/49138) Support classical hybrid draft models (LFM2/LFM2.5 short_conv)
- [#49574](https://github.com/vllm-project/vllm/pull/49574) Add chat-aware rolling checkpoints for recurrent prefix caching
- [#49267](https://github.com/vllm-project/vllm/pull/49267) Add runtime LoRA weight updates
- [#49109](https://github.com/vllm-project/vllm/pull/49109) Support MRV2 prefill PCP in Mooncake
- [#49445](https://github.com/vllm-project/vllm/pull/49445) Add `max_num_queued_reqs` and `max_num_queued_tokens` for queue size management
- [#49406](https://github.com/vllm-project/vllm/pull/49406) Add PARD-2 parallel draft model support
- [#49499](https://github.com/vllm-project/vllm/pull/49499) Keep TP-sharded Mamba state out of the KV-head dedup in Mooncake
- [#49123](https://github.com/vllm-project/vllm/pull/49123) Add SparDA lookahead KV connector
- [#49522](https://github.com/vllm-project/vllm/pull/49522) Unify fence field and move fence check after _build_store_jobs in KV Offloading
- [#49342](https://github.com/vllm-project/vllm/pull/49342) Support MRV2 prefill PCP replicas in NIXL
- [#49573](https://github.com/vllm-project/vllm/pull/49573) Add expert backup region and descriptor primitives for EPLB
- [#49572](https://github.com/vllm-project/vllm/pull/49572) Support custom initial expert maps for EPLB
- [#49069](https://github.com/vllm-project/vllm/pull/49069) Propagate EAGLE state across merged Mooncake store groups
- [#49252](https://github.com/vllm-project/vllm/pull/49252) Fix incorrect recompute on KV-load-failure recovery
- [#49145](https://github.com/vllm-project/vllm/pull/49145) Prevent stale partial prefix cache hashes
- [#49266](https://github.com/vllm-project/vllm/pull/49266) Namespace persistent cache by model revision in KV Offload
- [#49472](https://github.com/vllm-project/vllm/pull/49472) Balance padding vs group count when grouping hybrid KV cache layers
- [#49178](https://github.com/vllm-project/vllm/pull/49178) Scope MTP completeness checks outside bucketed updates
- [#48630](https://github.com/vllm-project/vllm/pull/48630) Avoid rejection sampler OOM by chunking in MRV2 Spec Decode
- [#48524](https://github.com/vllm-project/vllm/pull/48524) Fix DFlash fc sized wrong when num_target_layers != num_hidden_layers
- [#48639](https://github.com/vllm-project/vllm/pull/48639) Support loading sample_from_anchor flag from speculators config
- [#47953](https://github.com/vllm-project/vllm/pull/47953) Restrict embedding-width share guard to EAGLE drafts
- [#49071](https://github.com/vllm-project/vllm/pull/49071) Propagate EAGLE mode to SimpleCPU coordinator
- [#49343](https://github.com/vllm-project/vllm/pull/49343) Fix eagle draft max position embeddings
- [#49301](https://github.com/vllm-project/vllm/pull/49301) Bound hidden-state export staging memory
- [#49230](https://github.com/vllm-project/vllm/pull/49230) Validate NIXL speculative config compatibility
- [#49289](https://github.com/vllm-project/vllm/pull/49289) Discard matching subword buffer prefix on `PreLexedTerminal`

</details>

<details>
<summary>Hardware & arch (19)</summary>

- [#49044](https://github.com/vllm-project/vllm/pull/49044) Reenable per commit rocm wheel
- [#49251](https://github.com/vllm-project/vllm/pull/49251) Upgrade NIXL and UCX for ROCm
- [#49208](https://github.com/vllm-project/vllm/pull/49208) Implement CuMem slept-L1 fragmentation accounting
- [#48843](https://github.com/vllm-project/vllm/pull/48843) Set graph_pool_id before FULL CUDA graph capture in ModelRunner V2
- [#49302](https://github.com/vllm-project/vllm/pull/49302) Fix DSA crash under breakable piecewise cudagraphs
- [#47871](https://github.com/vllm-project/vllm/pull/47871) Fix heterogeneous NIXL KV transfer into CPU_ATTN decode workers
- [#47245](https://github.com/vllm-project/vllm/pull/47245) Add sycl path for Mhc on XPU
- [#47295](https://github.com/vllm-project/vllm/pull/47295) Fix GroupCoordinator device_index on XPU
- [#49408](https://github.com/vllm-project/vllm/pull/49408) Workaround topk_softplus_sqrt arg mismatch on XPU
- [#49395](https://github.com/vllm-project/vllm/pull/49395) Workaround topk_softmax arg mismatch on XPU
- [#48444](https://github.com/vllm-project/vllm/pull/48444) Fix WSL circular import from pin_memory warning_once
- [#49410](https://github.com/vllm-project/vllm/pull/49410) Add native AMX-FP8 attention impl for Diamond Rapids
- [#49453](https://github.com/vllm-project/vllm/pull/49453) Add MLA backend so DeepSeek-V2/V3 can run on CPU
- [#49303](https://github.com/vllm-project/vllm/pull/49303) Support Sequence Parallelism for mxfp8 on XPU
- [#49209](https://github.com/vllm-project/vllm/pull/49209) Register matmul and linear batch-invariant kernels for XPU
- [#49183](https://github.com/vllm-project/vllm/pull/49183) Disable DeepGEMM on GH200 to workaround illegal memory access
- [#49387](https://github.com/vllm-project/vllm/pull/49387) Add `sm_107` support for Rubin
- [#49021](https://github.com/vllm-project/vllm/pull/49021) Fix Clang OpenMP build on macOS
- [#49452](https://github.com/vllm-project/vllm/pull/49452) Fix `topk_softplus_sqrt` no-op on non-XPU platforms

</details>

<details>
<summary>API & serving (23)</summary>

- [#48992](https://github.com/vllm-project/vllm/pull/48992) Add engine-aware health reporting to Rust Frontend gRPC
- [#49045](https://github.com/vllm-project/vllm/pull/49045) Extract request preparation from the inference path in Rust Frontend
- [#49255](https://github.com/vllm-project/vllm/pull/49255) Add abort control RPC to Rust Frontend gRPC
- [#49003](https://github.com/vllm-project/vllm/pull/49003) Extract StructuredOutputsParams creation logic from Request.to_sampling_params
- [#48984](https://github.com/vllm-project/vllm/pull/48984) Reject removed pooling parameters
- [#45839](https://github.com/vllm-project/vllm/pull/45839) Support additional sampling parameters for translation API
- [#49144](https://github.com/vllm-project/vllm/pull/49144) Reject non-numeric logprobs with 400 instead of 500
- [#49217](https://github.com/vllm-project/vllm/pull/49217) Use VLLMValidationError in chat_utils content-part validation
- [#49214](https://github.com/vllm-project/vllm/pull/49214) Use VLLMValidationError in chat completion tool and batch validators
- [#49576](https://github.com/vllm-project/vllm/pull/49576) Extract shared chat types into `vllm-chat-types` for Rust Frontend
- [#49491](https://github.com/vllm-project/vllm/pull/49491) Add server and model discovery to Rust Frontend gRPC
- [#49330](https://github.com/vllm-project/vllm/pull/49330) Add --max-waiting-queue-length to bound the waiting queue
- [#49119](https://github.com/vllm-project/vllm/pull/49119) Use OpenAI transcript events for transcription streaming
- [#49526](https://github.com/vllm-project/vllm/pull/49526) Prevent server_load double-decrement on client disconnect
- [#49456](https://github.com/vllm-project/vllm/pull/49456) Report cache usage on Anthropic message_start
- [#49256](https://github.com/vllm-project/vllm/pull/49256) Bound validation-error response size for malformed requests
- [#49541](https://github.com/vllm-project/vllm/pull/49541) Fix Beam Search being slower by a factor of 1000
- [#49111](https://github.com/vllm-project/vllm/pull/49111) Map missing prompt logprobs for single-token prompts in chat and raw generate
- [#49113](https://github.com/vllm-project/vllm/pull/49113) Handle zero-column logprobs payloads without panicking in Rust Frontend
- [#49042](https://github.com/vllm-project/vllm/pull/49042) Fix macro-based content format detection in Rust Frontend
- [#49496](https://github.com/vllm-project/vllm/pull/49496) Fix finish reason for named tool choices in Rust Frontend
- [#49320](https://github.com/vllm-project/vllm/pull/49320) Fix empty logprob_token_ids silently bypassing validation via truthy checks
- [#49466](https://github.com/vllm-project/vllm/pull/49466) Separate inference and control services in Rust Frontend gRPC

</details>

<details>
<summary>Multimodal (13)</summary>

- [#49322](https://github.com/vllm-project/vllm/pull/49322) Move PyNvVideoCodec stuff out of gpu worker
- [#48781](https://github.com/vllm-project/vllm/pull/48781) Use zero-copy slicing for multimodal tensors in Rust Frontend
- [#47985](https://github.com/vllm-project/vllm/pull/47985) Add encoder cache profiling implementation for MRV2
- [#49159](https://github.com/vllm-project/vllm/pull/49159) Allow keeping original image mode for ImageIO
- [#49400](https://github.com/vllm-project/vllm/pull/49400) Rebuild vision chunk UUIDs in async render path
- [#49155](https://github.com/vllm-project/vllm/pull/49155) Reorganize video decoder backends
- [#49432](https://github.com/vllm-project/vllm/pull/49432) Simplify encoder cuda graph implementation
- [#49341](https://github.com/vllm-project/vllm/pull/49341) Send multimodal tensors in auxiliary frames in Rust Frontend
- [#49448](https://github.com/vllm-project/vllm/pull/49448) Fix multimodal streaming-session prefix rehashing
- [#49540](https://github.com/vllm-project/vllm/pull/49540) Fix Qwen3.6-27B multimodal inputs causing InternalServerError due to CUDA OOM
- [#49477](https://github.com/vllm-project/vllm/pull/49477) Defer MM embeds loading off the event loop
- [#49066](https://github.com/vllm-project/vllm/pull/49066) Add documentation for pynvvideocodec video decoding backend
- [#49279](https://github.com/vllm-project/vllm/pull/49279) Allow media placeholder target to be a list of tokens in Rust Frontend

</details>

<details>
<summary>Bugfixes (47)</summary>

- [#48674](https://github.com/vllm-project/vllm/pull/48674) Fix logprobs token-string collision from SentencePiece space
- [#47312](https://github.com/vllm-project/vllm/pull/47312) Handle grammar compilation failures to avoid engine crash
- [#45224](https://github.com/vllm-project/vllm/pull/45224) Bound idle reader waits and release read slots in shm_broadcast
- [#49391](https://github.com/vllm-project/vllm/pull/49391) Select earliest-completing stop string in check_stop_strings
- [#48748](https://github.com/vllm-project/vllm/pull/48748) Fix special tokens (EOS/BOS) leaking into reasoning content
- [#47573](https://github.com/vllm-project/vllm/pull/47573) Exclude location-derived path vars from torch.compile cache factors
- [#45989](https://github.com/vllm-project/vllm/pull/45989) Set vLLM config during weight reload in RL
- [#49485](https://github.com/vllm-project/vllm/pull/49485) Remove SciPy dependency from Inkling scale planning
- [#49297](https://github.com/vllm-project/vllm/pull/49297) Fix NIXL hybrid MLA+mamba heterogeneous TP
- [#49001](https://github.com/vllm-project/vllm/pull/49001) Retry config read to survive concurrent HF cache refresh
- [#49467](https://github.com/vllm-project/vllm/pull/49467) Fix DeepGEMM warmup when using `FlashInferFp8DeepGEMMDynamicBlockScaledKernel`
- [#49234](https://github.com/vllm-project/vllm/pull/49234) Fix test_rocm_quick_reduce.py
- [#49162](https://github.com/vllm-project/vllm/pull/49162) Fix minicpmv mm prompt placeholder parse error
- [#49566](https://github.com/vllm-project/vllm/pull/49566) Propagate retrieve failures in in-tree LMCache fallback adapter
- [#49082](https://github.com/vllm-project/vllm/pull/49082) Skip full GC during EngineCore process exit
- [#49117](https://github.com/vllm-project/vllm/pull/49117) Recover DSML tool calls when the start wrapper token is missing
- [#49264](https://github.com/vllm-project/vllm/pull/49264) Handle AITER unified-attention LDS overflow with Triton fallback
- [#49323](https://github.com/vllm-project/vllm/pull/49323) Fix MRotaryEmbedding Triton kernel hardcoding Neox pairing for GPT-J style models
- [#49521](https://github.com/vllm-project/vllm/pull/49521) Let terminal grammars stop under min_tokens
- [#49318](https://github.com/vllm-project/vllm/pull/49318) Route kimi_k2 streaming through arg_converter so schema type coercion applies
- [#49080](https://github.com/vllm-project/vllm/pull/49080) Validate allowed_token_ids against model output vocab size
- [#49204](https://github.com/vllm-project/vllm/pull/49204) Fix internal LB load-balancing
- [#49233](https://github.com/vllm-project/vllm/pull/49233) Reserve CUDA graph memory in V2 GPU model runner
- [#49081](https://github.com/vllm-project/vllm/pull/49081) Add token-domain bounds check to penalty bincount kernel
- [#49570](https://github.com/vllm-project/vllm/pull/49570) Fix mypy errors in tests and enforce follow-imports=silent
- [#49180](https://github.com/vllm-project/vllm/pull/49180) Restore --skip-tokenizer-init with custom dataset in benchmarks
- [#49426](https://github.com/vllm-project/vllm/pull/49426) Strip content whitespace at tool-call boundaries in streaming
- [#49227](https://github.com/vllm-project/vllm/pull/49227) Mask request stop tokens in xgrammar until grammar terminates
- [#49409](https://github.com/vllm-project/vllm/pull/49409) Do not discard model output when tool_choice defaults to "none"
- [#49274](https://github.com/vllm-project/vllm/pull/49274) Fix send_object being synchronous in isend_tensor_dict
- [#49136](https://github.com/vllm-project/vllm/pull/49136) Avoid nonsense latency intervals for unreached milestones
- [#49520](https://github.com/vllm-project/vllm/pull/49520) Honor per-request StructuredOutputsParams.disable_any_whitespace
- [#49461](https://github.com/vllm-project/vllm/pull/49461) Cap grammar-compile executor workers to avoid CFS throttling in containers
- [#49567](https://github.com/vllm-project/vllm/pull/49567) Preserve whitespace in Step3 parameter values in Tool Parser
- [#49439](https://github.com/vllm-project/vllm/pull/49439) Prevent streaming session deadlock under KV pressure
- [#49107](https://github.com/vllm-project/vllm/pull/49107) Preserve pooling token-ID state during batch reordering
- [#49346](https://github.com/vllm-project/vllm/pull/49346) Accept empty tool call list in case of none required tool_choice
- [#49228](https://github.com/vllm-project/vllm/pull/49228) Ensure previous_text and tokens id accumulation in streaming state
- [#49249](https://github.com/vllm-project/vllm/pull/49249) Tolerate missing opening `<arg_value>` tag in glm47 parser
- [#49134](https://github.com/vllm-project/vllm/pull/49134) Reject contradictory custom-op directives
- [#49287](https://github.com/vllm-project/vllm/pull/49287) Fix OOM and skip graph case in XPU UT
- [#49132](https://github.com/vllm-project/vllm/pull/49132) Release executor and lock fds in ExampleHiddenStates
- [#49549](https://github.com/vllm-project/vllm/pull/49549) Improve compile_sizes cudagraph padding error message
- [#49557](https://github.com/vllm-project/vllm/pull/49557) Mark transfer as failed when check_xfer_state() raises in NIXL
- [#49314](https://github.com/vllm-project/vllm/pull/49314) Fall back to native sampling when flashinfer is absent
- [#49575](https://github.com/vllm-project/vllm/pull/49575) Preserve explicit None when swapping dict values
- [#49306](https://github.com/vllm-project/vllm/pull/49306) Handle MLA fallback during FA4 JIT warmup

</details>

<details>
<summary>Refactors & Other (35)</summary>

- [#44456](https://github.com/vllm-project/vllm/pull/44456) Standardize Mamba cache and drop `get_transfer_cache_regions`
- [#49161](https://github.com/vllm-project/vllm/pull/49161) Bump `xgrammar-structural-tag` and enable local extension
- [#49033](https://github.com/vllm-project/vllm/pull/49033) Revert "[Sampler] Stop upcasting logits to fp32 in apply_sampling_params"
- [#47992](https://github.com/vllm-project/vllm/pull/47992) Remove redundant AITER fused_qk_rmsnorm probe
- [#49244](https://github.com/vllm-project/vllm/pull/49244) Remove old unsupported `max_num_partial_prefills` and `max_long_partial_prefills`
- [#48399](https://github.com/vllm-project/vllm/pull/48399) Simplify KVBlockZeroer index tensor handling
- [#49235](https://github.com/vllm-project/vllm/pull/49235) Remove unused StructuredOutputRequest.status field
- [#49201](https://github.com/vllm-project/vllm/pull/49201) Unify the weight loading lifecycle in Model Loader
- [#49458](https://github.com/vllm-project/vllm/pull/49458) Hardware-agnostic model definition via HF transformer backend
- [#49577](https://github.com/vllm-project/vllm/pull/49577) Implement Mask Replay
- [#49503](https://github.com/vllm-project/vllm/pull/49503) Optimize block verification kernels in Model Runner V2
- [#49389](https://github.com/vllm-project/vllm/pull/49389) Remove deprecated calculate_kv_scales runtime KV scale calculation
- [#49114](https://github.com/vllm-project/vllm/pull/49114) Add CachePolicyFactory for pluggable/external eviction policies
- [#49563](https://github.com/vllm-project/vllm/pull/49563) Make placement group wait timeout configurable
- [#49168](https://github.com/vllm-project/vllm/pull/49168) Cache staging buffer in structured output to fix memory regression
- [#49284](https://github.com/vllm-project/vllm/pull/49284) Apply reasoning.context on the input path
- [#49075](https://github.com/vllm-project/vllm/pull/49075) Enforce max_num_partial_prefills and max_long_partial_prefills in V1 Scheduler
- [#49151](https://github.com/vllm-project/vllm/pull/49151) Load weights outside the CuMem pool and re-home them for sleep mode
- [#49519](https://github.com/vllm-project/vllm/pull/49519) Defer post-load attention weight processing
- [#49565](https://github.com/vllm-project/vllm/pull/49565) Make Ray placement group strategy configurable via VLLM_RAY_PG_STRATEGY
- [#49247](https://github.com/vllm-project/vllm/pull/49247) Reject incompatible nested runtime overrides
- [#49124](https://github.com/vllm-project/vllm/pull/49124) Improve data-parallel launch validation
- [#49337](https://github.com/vllm-project/vllm/pull/49337) Add logs to locate garbled text issue
- [#49167](https://github.com/vllm-project/vllm/pull/49167) Make prefix cache hit-rate sliding window size configurable
- [#48979](https://github.com/vllm-project/vllm/pull/48979) Skip cudagraph/DP padding in topk
- [#49225](https://github.com/vllm-project/vllm/pull/49225) Batching for read/write threads in KV-offload FS
- [#49152](https://github.com/vllm-project/vllm/pull/49152) Batch store/load_block in C for KV-offload FS
- [#49307](https://github.com/vllm-project/vllm/pull/49307) Add vllm:kv_offload_cpu_total_blocks capacity metric
- [#49348](https://github.com/vllm-project/vllm/pull/49348) Use MXFP4 linear kernel abstraction for `aiter` backend
- [#49291](https://github.com/vllm-project/vllm/pull/49291) Fused-kernel support for align-mode DS-conv state migration
- [#49088](https://github.com/vllm-project/vllm/pull/49088) Extend benchmark_moe HF MoE shape parsing beyond Mixtral fallback
- [#49177](https://github.com/vllm-project/vllm/pull/49177) Propagate Flash Attention cache configuration to Ray workers
- [#48938](https://github.com/vllm-project/vllm/pull/48938) Adjust logo to be more friendly to white background terminal
- [#49344](https://github.com/vllm-project/vllm/pull/49344) Fix terminal output logo coloring
- [#47879](https://github.com/vllm-project/vllm/pull/47879) Update qutlass cmake for stable abi

</details>

<details>
<summary>Docs (8)</summary>

- [#49148](https://github.com/vllm-project/vllm/pull/49148) Update XPU docker image documents
- [#49100](https://github.com/vllm-project/vllm/pull/49100) Document blocks_per_chunk in the KV offloading guide
- [#47211](https://github.com/vllm-project/vllm/pull/47211) Fix broken csrc kernel links in fusions doc
- [#47210](https://github.com/vllm-project/vllm/pull/47210) Remove duplicate CodeGeex4 row in XPU model table
- [#47212](https://github.com/vllm-project/vllm/pull/47212) Fix broken protocol link in speech_to_text doc
- [#49299](https://github.com/vllm-project/vllm/pull/49299) Fix XPU compute-runtime driver link version mismatch
- [#49474](https://github.com/vllm-project/vllm/pull/49474) Re-add Reo.dev analytics beacon
- [#49353](https://github.com/vllm-project/vllm/pull/49353) Add Crusoe Managed Inference deployment guide

</details>

<details>
<summary>Tests, CI & build (1)</summary>

- Plus 49 minor CI, build, and test updates (including Rust benchmark integrations, ROCm wheel fixes, XPU test additions, and timeout adjustments).

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: d40d5425f0c324e6e216045874122ac6a9134dde65f44add54c9909853be8a4a -->
