# vllm: PR digest (2026-07-22 to 2026-07-26)

_156 merged, 304 newly opened - source vllm-project/vllm, generated 2026-07-26T22:11:10Z_

## TL;DR

- **DeepSeek & GLM-5.2 optimizations:** DeepSeek-V4 dominated attention with JIT kernel migrations and sparse-MLA decode buffering. GLM-5.2 saw major Blackwell decode optimizations and owner-sharded PCP history work.
- **Distributed KV Cache & P2P:** Significant architectural shifts in KV management, including a generic P2P secondary tier for peer lookup/serving, and deduplication of replicated MLA KV in shared CPU regions.
- **Attention & Speculative Decoding:** Introduced `ReplaySSM` to cache SSM inputs for faster Mamba2 and Gated DeltaNet standard/speculative decoding. An experimental `ZoomKV` backend was also opened.
- **Rust Frontend Modularization:** Continued extraction of the Rust frontend, moving chat renderers, shared types, and gRPC inference/control services into separate crates.
- **Overall Direction:** Heavy focus on distributed KV scaling (P2P, offloading), next-gen hardware optimization (Blackwell, NVFP4), and hybrid architecture support (MLA+SSM).

## Most important PRs

- **[#48021](https://github.com/vllm-project/vllm/pull/48021) Generic P2P secondary tier: peer lookup and serving via ParentManager**
  Introduces a major architectural addition for distributed KV serving, enabling secondary-tier peer lookup and direct P2P transfers. This lays the groundwork for massive cross-node KV cache scaling.
- **[#48018](https://github.com/vllm-project/vllm/pull/48018) ReplaySSM: cache SSM inputs for faster Mamba2 standard decode**
  Dramatically improves Mamba2 performance by caching SSM inputs during decode. This pattern was also extended to Gated DeltaNet and speculative decoding paths in follow-up work.
- **[#49741](https://github.com/vllm-project/vllm/pull/49741) Add owner-sharded PCP history for up to 4x KV capacity**
  Optimizes GLM-5.2 by sharding prefix-caching (PCP) history across owners. This significantly reduces memory redundancy, claiming up to a 4x increase in effective KV capacity.
- **[#49719](https://github.com/vllm-project/vllm/pull/49719) Add experimental ZoomKV backend**
  Opens a massive new Triton-based attention backend designed for advanced KV cache management and scaling, signaling a major upcoming shift in attention handling.
- **[#49629](https://github.com/vllm-project/vllm/pull/49629) HiSparse: host-resident sparse-MLA decode hot-buffering + GLM-5.2 indexCache opts**
  Implements host-resident hot-buffering for sparse-MLA decode, heavily optimizing memory access patterns for DeepSeek and GLM-5.2 models.

## More changes by area

<details>
<summary>Performance (24)</summary>

- [#48597](https://github.com/vllm-project/vllm/pull/48597) Blackwell decode optimizations for GLM-5.2
- [#49768](https://github.com/vllm-project/vllm/pull/49768) Revert Blackwell decode optimizations for GLM-5.2
- [#48531](https://github.com/vllm-project/vllm/pull/48531) Vectorize prepare_value on the KV load path
- [#49477](https://github.com/vllm-project/vllm/pull/49477) Defer MM embeds loading off the event loop
- [#49531](https://github.com/vllm-project/vllm/pull/49531) Optimize DeepSeek-OCR-2 TTFT
- [#48957](https://github.com/vllm-project/vllm/pull/48957) Skip empty c128 kernel launch for DSv4
- [#49524](https://github.com/vllm-project/vllm/pull/49524) Isolate MM preprocessing on its own executor
- [#48763](https://github.com/vllm-project/vllm/pull/48763) Fix moe reduce_scatter perf regression
- [#49486](https://github.com/vllm-project/vllm/pull/49486) Skip topk and router when not needed for DSv4
- [#48017](https://github.com/vllm-project/vllm/pull/48017) Skip LRU hash-split in free_blocks when prefix caching is off
- [#49396](https://github.com/vllm-project/vllm/pull/49396) Offload derender CPU work to renderer thread pool
- [#49487](https://github.com/vllm-project/vllm/pull/49487) Avoid transient Inkling result allocations
- [#49793](https://github.com/vllm-project/vllm/pull/49793) Optimize MTP draft decoding
- [#49870](https://github.com/vllm-project/vllm/pull/49870) Speed up single-group MoE routing on ROCm
- [#49872](https://github.com/vllm-project/vllm/pull/49872) Speed up large MoE ReLU-squared on gfx90a
- [#49678](https://github.com/vllm-project/vllm/pull/49678) Store FlashInfer sparse physical indices in attention metadata
- [#49670](https://github.com/vllm-project/vllm/pull/49670) Fuse mul_+moe_sum in TopKWeightAndReduceContiguous
- [#49750](https://github.com/vllm-project/vllm/pull/49750) Add RMSNorm uncontiguous support
- [#49390](https://github.com/vllm-project/vllm/pull/49390) Raise Blackwell CUDA graph capture default to 1024
- [#49462](https://github.com/vllm-project/vllm/pull/49462) Add mm_tensor_ipc=cuda_ipc TP-aware GPU transport
- [#49459](https://github.com/vllm-project/vllm/pull/49459) Reload layout-identical weights directly
- [#49436](https://github.com/vllm-project/vllm/pull/49436) Implement 3D-grid tiling of the state-copy Triton kernels
- [#49500](https://github.com/vllm-project/vllm/pull/49500) Skip redundant full-fit admission pass
- [#49607](https://github.com/vllm-project/vllm/pull/49607) Hash videos by source bytes
</details>

<details>
<summary>Kernels & attention (32)</summary>

- [#49627](https://github.com/vllm-project/vllm/pull/49627) Migrate DSv4 JIT kernels to shared warmup contract
- [#49766](https://github.com/vllm-project/vllm/pull/49766) Add Gdn ucache backend
- [#49517](https://github.com/vllm-project/vllm/pull/49517) Optimize PCP KV updates with direct peer stores
- [#49744](https://github.com/vllm-project/vllm/pull/49744) Add Fused QK-Norm + mRoPE for Qwen3-VL-class models
- [#49650](https://github.com/vllm-project/vllm/pull/49650) Centralize CPU causal-conv dispatch
- [#49564](https://github.com/vllm-project/vllm/pull/49564) Add FlashAttention PCP support for GQA on MRv2
- [#49555](https://github.com/vllm-project/vllm/pull/49555) Implement return indexer topk of sparse attention
- [#49410](https://github.com/vllm-project/vllm/pull/49410) Add native AMX-FP8 attention impl for Diamond Rapids
- [#49791](https://github.com/vllm-project/vllm/pull/49791) Optimize small-batch decode GEMMs
- [#49891](https://github.com/vllm-project/vllm/pull/49891) Fix full cudagraph with MTP by using cuda-graph-aware prefill wrapper
- [#49792](https://github.com/vllm-project/vllm/pull/49792) Add a CuTeDSL fused query kernel for SM100
- [#49761](https://github.com/vllm-project/vllm/pull/49761) Add Gemma4 B200 FP8 optimized path
- [#49425](https://github.com/vllm-project/vllm/pull/49425) Add FlashInfer SSD prefill backend for Mamba
- [#49688](https://github.com/vllm-project/vllm/pull/49688) Use C++ causal_conv1d kernels for GDN attention on non-AMX CPUs
- [#49827](https://github.com/vllm-project/vllm/pull/49827) Enable batch-invariant mixed decode and prefill for Qwen GDN
- [#49828](https://github.com/vllm-project/vllm/pull/49828) Add fused silu_and_mul + dynamic per-token FP8 quantization
- [#49598](https://github.com/vllm-project/vllm/pull/49598) Add Kimi Delta Attn(KDA) Support for XPU
- [#49664](https://github.com/vllm-project/vllm/pull/49664) Add torch as xpu linear backend
- [#49465](https://github.com/vllm-project/vllm/pull/49465) Enable triton-cpu path for Turbo-quant algorithm
- [#49755](https://github.com/vllm-project/vllm/pull/49755) Guard sparse-MLA persistent-only path for gqa_ratio=64 fp8
- [#48630](https://github.com/vllm-project/vllm/pull/48630) Avoid rejection sampler OOM by chunking
- [#46340](https://github.com/vllm-project/vllm/pull/46340) Add TD operand loads for batched MoE GEMM on XPU
- [#48993](https://github.com/vllm-project/vllm/pull/48993) Compact MXFP4 indexer KV cache and packed group overlays
- [#47992](https://github.com/vllm-project/vllm/pull/47992) Remove redundant AITER fused_qk_rmsnorm probe
- [#48399](https://github.com/vllm-project/vllm/pull/48399) Simplify KVBlockZeroer index tensor handling
- [#49364](https://github.com/vllm-project/vllm/pull/49364) Always build attn metadata at capture time
- [#49451](https://github.com/vllm-project/vllm/pull/49451) Revert always building attn metadata at capture time
- [#49718](https://github.com/vllm-project/vllm/pull/49718) Add XQA into vLLM
- [#49432](https://github.com/vllm-project/vllm/pull/49432) Simplify encoder cuda graph implementation
- [#49503](https://github.com/vllm-project/vllm/pull/49503) Optimize block verification kernels
- [#49386](https://github.com/vllm-project/vllm/pull/49386) Enable rejection sampling with draft logits by default
- [#49618](https://github.com/vllm-project/vllm/pull/49618) Dispatch non-grouped bias-less topk routing methods to fused path
</details>

<details>
<summary>MoE & quantization (14)</summary>

- [#44120](https://github.com/vllm-project/vllm/pull/44120) Migrate MoeWNA16Method quantization method to MK oracle scheme
- [#48044](https://github.com/vllm-project/vllm/pull/48044) Add Fused Shared Expert Support for AMD Quark DeepSeek-V4
- [#49258](https://github.com/vllm-project/vllm/pull/49258) Support llm-compressor Inkling NVFP4 weights
- [#48050](https://github.com/vllm-project/vllm/pull/48050) Add Quark W4A8 (INT4-FP8) MoE CI coverage
- [#41276](https://github.com/vllm-project/vllm/pull/41276) Add DeepSeek4 CT Quantization Support
- [#49775](https://github.com/vllm-project/vllm/pull/49775) Add FlashInfer CuTe-DSL NVFP4 Quantization
- [#49636](https://github.com/vllm-project/vllm/pull/49636) Add opt-in FlashInfer moe_ep expert backend for DeepSeek-V4
- [#49382](https://github.com/vllm-project/vllm/pull/49382) Add FlashInferW4A16NvFp4LinearKernel
- [#49715](https://github.com/vllm-project/vllm/pull/49715) Support dynamic activation scaling for ModelOpt NVFP4
- [#49764](https://github.com/vllm-project/vllm/pull/49764) Share online weight scales across TP
- [#49580](https://github.com/vllm-project/vllm/pull/49580) Integrate CuTeDSL MoE for ReLU2 NVFP4
- [#49553](https://github.com/vllm-project/vllm/pull/49553) Honor checkpoint per-layer quantization config for Qwen3.5 MTP
- [#49501](https://github.com/vllm-project/vllm/pull/49501) Fix Humming W4 packing for dense INT4 weights
- [#49389](https://github.com/vllm-project/vllm/pull/49389) Remove deprecated calculate_kv_scales runtime KV scale calculation
</details>

<details>
<summary>Model support (13)</summary>

- [#49729](https://github.com/vllm-project/vllm/pull/49729) Remove Plamo2
- [#49786](https://github.com/vllm-project/vllm/pull/49786) Remove Ouro
- [#49803](https://github.com/vllm-project/vllm/pull/49803) Add VaultGemma via Transformers modeling backend
- [#45429](https://github.com/vllm-project/vllm/pull/45429) Support top_k and top_p sampling for DiffusionGemma
- [#49875](https://github.com/vllm-project/vllm/pull/49875) Add minimal native RWKV7 serving support
- [#49698](https://github.com/vllm-project/vllm/pull/49698) Support MiniCPM-RobotTrack
- [#49842](https://github.com/vllm-project/vllm/pull/49842) Support native Transformers ERNIE 4.5 VL
- [#49433](https://github.com/vllm-project/vllm/pull/49433) Add support for Nanbeige4.2
- [#49406](https://github.com/vllm-project/vllm/pull/49406) Add PARD-2 parallel draft model support
- [#49788](https://github.com/vllm-project/vllm/pull/49788) Enable LoRA support for tower and connector in LlavaNext
- [#49819](https://github.com/vllm-project/vllm/pull/49819) Add Cohere2MoE Eagle3 auxiliary hidden states
- [#46837](https://github.com/vllm-project/vllm/pull/46837) Support ViT CUDA Graph for Gemma-4
- [#49811](https://github.com/vllm-project/vllm/pull/49811) Support extract_hidden_states speculation
</details>

<details>
<summary>Parallelism & scheduling (18)</summary>

- [#48906](https://github.com/vllm-project/vllm/pull/48906) Deduplicate replicated MLA KV in the shared CPU region
- [#44428](https://github.com/vllm-project/vllm/pull/44428) Add fault tolerance framework for DP+EP external LB deployments
- [#45321](https://github.com/vllm-project/vllm/pull/45321) Update NCCL to 2.30.7 to enable DeepEPv2
- [#46877](https://github.com/vllm-project/vllm/pull/46877) Add process-checkpoint lifecycle hooks for communicators
- [#49481](https://github.com/vllm-project/vllm/pull/49481) Re-derive full external hits on stored boundaries
- [#49700](https://github.com/vllm-project/vllm/pull/49700) Add Platform Backend interface for out-of-tree devices
- [#49756](https://github.com/vllm-project/vllm/pull/49756) Exchange only sampled final rows after PCP prefill
- [#49502](https://github.com/vllm-project/vllm/pull/49502) Support reliable partial-tail KV offload for sub-block prompts
- [#49762](https://github.com/vllm-project/vllm/pull/49762) Support NIXL P/D for hybrid MLA+SSM models
- [#49506](https://github.com/vllm-project/vllm/pull/49506) Single-key store admission ordered by ending token position
- [#49612](https://github.com/vllm-project/vllm/pull/49612) Support NIXL heterogeneous P/D block sizes for hybrid models
- [#49573](https://github.com/vllm-project/vllm/pull/49573) Add expert backup region and descriptor primitives
- [#49644](https://github.com/vllm-project/vllm/pull/49644) Add disk offloading support to SimpleCPUOffloadConnector
- [#49572](https://github.com/vllm-project/vllm/pull/49572) Support custom initial expert maps
- [#49532](https://github.com/vllm-project/vllm/pull/49532) Support EC connector KV Offloading
- [#49472](https://github.com/vllm-project/vllm/pull/49472) Balance padding vs group count when grouping hybrid KV cache layers
- [#49565](https://github.com/vllm-project/vllm/pull/49565) Make Ray placement group strategy configurable
- [#49858](https://github.com/vllm-project/vllm/pull/49858) Make compact secondary identity TP-independent
</details>

<details>
<summary>Hardware & arch (8)</summary>

- [#49387](https://github.com/vllm-project/vllm/pull/49387) Add `sm_107` for Rubin
- [#49453](https://github.com/vllm-project/vllm/pull/49453) Add MLA backend so DeepSeek-V2/V3 can run on CPU
- [#49470](https://github.com/vllm-project/vllm/pull/49470) Switch vLLM to The Rock when on AMD hardware
- [#49888](https://github.com/vllm-project/vllm/pull/49888) Support AITER paged attention on gfx90a
- [#49818](https://github.com/vllm-project/vllm/pull/49818) Enable NVFP4 KV cache on SM120 (consumer Blackwell)
- [#49408](https://github.com/vllm-project/vllm/pull/49408) WA of topk_softplus_sqrt arg mismatch on XPU
- [#49395](https://github.com/vllm-project/vllm/pull/49395) WA of topk_softmax arg mismatch on XPU
- [#49419](https://github.com/vllm-project/vllm/pull/49419) Add warning for xpu graph limitations
</details>

<details>
<summary>API & serving (34)</summary>

- [#49153](https://github.com/vllm-project/vllm/pull/49153) Parallelize preprocessing within the same request for pooling models
- [#39330](https://github.com/vllm-project/vllm/pull/39330) Add audio support for the Transformers backend
- [#49322](https://github.com/vllm-project/vllm/pull/49322) Move PyNvVideoCodec stuff out of gpu worker
- [#49255](https://github.com/vllm-project/vllm/pull/49255) Add abort control RPC to Rust Frontend
- [#49045](https://github.com/vllm-project/vllm/pull/49045) Extract request preparation from the inference path
- [#49753](https://github.com/vllm-project/vllm/pull/49753) Make PyNvVideoCodec decoder concurrency configurable
- [#48796](https://github.com/vllm-project/vllm/pull/48796) Keep attention backends eligible for text-only serving
- [#48218](https://github.com/vllm-project/vllm/pull/48218) Add encoder cache extension hooks
- [#49247](https://github.com/vllm-project/vllm/pull/49247) Reject incompatible nested runtime overrides
- [#49124](https://github.com/vllm-project/vllm/pull/49124) Improve data-parallel launch validation
- [#49217](https://github.com/vllm-project/vllm/pull/49217) Use VLLMValidationError in chat_utils
- [#49777](https://github.com/vllm-project/vllm/pull/49777) Add DCP Topology Validation
- [#49344](https://github.com/vllm-project/vllm/pull/49344) Fix terminal output logo coloring
- [#49667](https://github.com/vllm-project/vllm/pull/49667) Add paged shared memory storage for mm tensor ipc
- [#49576](https://github.com/vllm-project/vllm/pull/49576) Extract shared chat types into `vllm-chat-types`
- [#49703](https://github.com/vllm-project/vllm/pull/49703) Extract chat renderer to a separate crate
- [#49491](https://github.com/vllm-project/vllm/pull/49491) Add server and model discovery to Rust Frontend
- [#49665](https://github.com/vllm-project/vllm/pull/49665) Standardize request error handling with VLLMError hierarchy
- [#49445](https://github.com/vllm-project/vllm/pull/49445) Add queue size management parameters
- [#49466](https://github.com/vllm-project/vllm/pull/49466) Separate inference and control services in Rust Frontend
- [#49577](https://github.com/vllm-project/vllm/pull/49577) Implement Mask Replay
- [#49885](https://github.com/vllm-project/vllm/pull/49885) Add server-side tool strictness level for auto tool choice
- [#49604](https://github.com/vllm-project/vllm/pull/49604) Add --limit-mm-per-prompt support
- [#49794](https://github.com/vllm-project/vllm/pull/49794) Add /v1/responses/input_tokens endpoint
- [#49754](https://github.com/vllm-project/vllm/pull/49754) Expose stream_interval as req sampling param
- [#49855](https://github.com/vllm-project/vllm/pull/49855) Support --allowed-local-media-path and --allowed-media-domains
- [#49686](https://github.com/vllm-project/vllm/pull/49686) Expose mm hash algothrim selection to cli args
- [#49879](https://github.com/vllm-project/vllm/pull/49879) Support fast engine recovery through weight cache
- [#49458](https://github.com/vllm-project/vllm/pull/49458) Hardware-agnostic model definition via HF transformer backend
- [#49682](https://github.com/vllm-project/vllm/pull/49682) Add multimodal media load metrics
- [#49852](https://github.com/vllm-project/vllm/pull/49852) Enable encoder cuda graph for model runner v2
- [#49713](https://github.com/vllm-project/vllm/pull/49713) Add poolside_v1 reasoning parser
- [#49799](https://github.com/vllm-project/vllm/pull/49799) Add xLAM tool parser to Rust frontend
- [#49608](https://github.com/vllm-project/vllm/pull/49608) Offload raw-prompt preprocessing to renderer thread pool
</details>

<details>
<summary>Bugfixes (110)</summary>

- [#49499](https://github.com/vllm-project/vllm/pull/49499) Keep TP-sharded Mamba state out of the KV-head dedup
- [#48425](https://github.com/vllm-project/vllm/pull/48425) Handle per-group prefix-hit divergence for hybrid models
- [#49221](https://github.com/vllm-project/vllm/pull/49221) Fix blocking handshake call on writer thread
- [#48776](https://github.com/vllm-project/vllm/pull/48776) Support sparse-MLA targets with SWA drafts
- [#44993](https://github.com/vllm-project/vllm/pull/44993) Advance grammar across reasoning boundary
- [#49294](https://github.com/vllm-project/vllm/pull/49294) Ignore empty MLA context chunks during merge
- [#49180](https://github.com/vllm-project/vllm/pull/49180) Restore --skip-tokenizer-init with custom dataset
- [#45224](https://github.com/vllm-project/vllm/pull/45224) Bound idle reader waits and release read slots
- [#49671](https://github.com/vllm-project/vllm/pull/49671) Defer request finalization until final store
- [#49178](https://github.com/vllm-project/vllm/pull/49178) Scope MTP completeness checks outside bucketed updates
- [#47312](https://github.com/vllm-project/vllm/pull/47312) Handle grammar compilation failures to avoid engine crash
- [#49372](https://github.com/vllm-project/vllm/pull/49372) Respect declared attention contract for ColQwen3.5 retrievers
- [#49704](https://github.com/vllm-project/vllm/pull/49704) Support non-uniform page sizes in KVBlockZeroer
- [#49391](https://github.com/vllm-project/vllm/pull/49391) Select earliest-completing stop string in check_stop_strings
- [#49734](https://github.com/vllm-project/vllm/pull/49734) Fall back to buffered I/O without O_DIRECT
- [#47206](https://github.com/vllm-project/vllm/pull/47206) Fix elastic EP scaling accuracy on ROCm
- [#48852](https://github.com/vllm-project/vllm/pull/48852) Fix dropped streaming arguments in Jamba and InternLM2 parsers
- [#48748](https://github.com/vllm-project/vllm/pull/48748) Fix special tokens leaking into reasoning content
- [#49603](https://github.com/vllm-project/vllm/pull/49603) Fix batch invariance rms norm comparison
- [#49805](https://github.com/vllm-project/vllm/pull/49805) Wait for the linear bias before layerwise online processing
- plus 90 more minor bugfixes
</details>

<details>
<summary>Tests, CI & build (60)</summary>

- [#49270](https://github.com/vllm-project/vllm/pull/49270) Prepare AMD mirrors for regating
- [#49726](https://github.com/vllm-project/vllm/pull/49726) Make bare `hugging_face` imports forbidden
- [#49251](https://github.com/vllm-project/vllm/pull/49251) Upgrade NIXL and UCX
- [#48155](https://github.com/vllm-project/vllm/pull/48155) Update PyTorch to 2.13.0, torchvision to 0.28.0, triton to 3.7.1
- [#49257](https://github.com/vllm-project/vllm/pull/49257) Deprecate DinD for MI355 tests
- [#49398](https://github.com/vllm-project/vllm/pull/49398) Add auto label for xpu relate issue
- [#49492](https://github.com/vllm-project/vllm/pull/49492) Add quantization label automation
- [#49223](https://github.com/vllm-project/vllm/pull/49223) Bump Transformers version to 5.14.1
- [#49763](https://github.com/vllm-project/vllm/pull/49763) Force native compile caches onto local disk
- [#48914](https://github.com/vllm-project/vllm/pull/48914) Bump Flashinfer version to 0.6.15
- [#49901](https://github.com/vllm-project/vllm/pull/49901) Refresh tags before building macOS wheel
- [#49431](https://github.com/vllm-project/vllm/pull/49431) Upgrade tpu-inference to v0.25.0
- [#49326](https://github.com/vllm-project/vllm/pull/49326) Bump vllm-flash-attn to C++20-compatible commit
- [#49737](https://github.com/vllm-project/vllm/pull/49737) Drop MORI_GPU_ARCHS so MoRI autodetects the device arch
- [#45117](https://github.com/vllm-project/vllm/pull/45117) Mergify message not on cancelled
- plus 45 more minor CI and test updates
</details>

<details>
<summary>Docs (6)</summary>

- [#49587](https://github.com/vllm-project/vllm/pull/49587) Use `gen-files` for generated docs content
- [#49523](https://github.com/vllm-project/vllm/pull/49523) Update docs and dockerfile for s390x
- [#49782](https://github.com/vllm-project/vllm/pull/49782) Add compile cache volume example to the Docker deployment page
- [#49474](https://github.com/vllm-project/vllm/pull/49474) Re-add Reo.dev analytics beacon
- [#49654](https://github.com/vllm-project/vllm/pull/49654) Fix broken anchor links in serving/pooling/MoE docs
- [#49781](https://github.com/vllm-project/vllm/pull/49781) Fix confusing docstring indentation in nemotron_h.py
</details>

<details>
<summary>Refactors (3)</summary>

- [#49610](https://github.com/vllm-project/vllm/pull/49610) Refactor humming linear and moe backends to use explicit layer configs
- [#49522](https://github.com/vllm-project/vllm/pull/49522) Unify fence field and move fence check after _build_store_jobs
- [#49745](https://github.com/vllm-project/vllm/pull/49745) Remove dead code in multiple files
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: d32d657b36e9f1a76de0a882510c5fb7b3377912aa1201634b04d9392a1a4a3f -->
