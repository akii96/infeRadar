# vllm: PR digest (2026-06-28 to 2026-07-02)

_196 merged, 278 newly opened - source vllm-project/vllm, generated 2026-07-02T11:47:01Z_

## TL;DR
- **Model focus:** DeepSeek saw the most attention, with significant work on DeepSeek-V4/V3.2 including FlashInfer MLA sparse decode context parallelism, DSpark speculative decoding, and FlashMLA FP8 KV cache support. Qwen, Gemma, and GLM5 also received targeted performance and feature updates.
- **Performance & Kernels:** Major kernel additions include the new Helion kernel for `fused_qk_norm_rope`, HPC-Ops attention backend, and extensive FlashInfer MLA optimizations. In-progress work targets RDNA 3.5 quantized GEMM kernels and making the Transformers modeling backend as fast as native vLLM.
- **Architecture & Disaggregation:** Merged a secondary tier implementation for PD (Prefill-Decode) disaggregation, including Mooncake Connector support for GDN (Qwen3.5) and MLA (DeepSeek-V4-Flash).
- **Frontend & Serving:** The Rust frontend gained static HTTPS/mTLS support, a new Harmony Renderer for GPT-OSS, and streaming parser engines. In-progress work brings Cohere Chat V2 API support and DoRA (Weight-Decomposed Low-Rank Adaptation) serving.
- **Speculative Decoding:** Merged DSpark speculative decoding and universal speculative decoding for heterogeneous vocabularies (TLI). In-progress work introduces D-cut (Adaptive Verification Depth Pruning) and MTP speculative decoding under pipeline parallelism.

## Most important PRs
- **[#42285](https://github.com/vllm-project/vllm/pull/42285)** Merges the secondary tier implementation for Prefill-Decode (PD) disaggregation, enabling more flexible KV cache offloading and transfer across nodes.
- **[#44010](https://github.com/vllm-project/vllm/pull/44010)** Introduces the Helion kernel for `fused_qk_norm_rope` on NVIDIA hardware, laying the groundwork for faster fused attention operations.
- **[#46076](https://github.com/vllm-project/vllm/pull/46076)** Adds Decode Context Parallelism (DCP) support for `FLASHINFER_MLA_SPARSE`, significantly improving DeepSeek MLA decode performance.
- **[#47045](https://github.com/vllm-project/vllm/pull/47045)** (Opened) Proposes a massive RDNA 3.5 quantized GEMM kernel implementation for AMD hardware, targeting AWQ and GPTQ quantizations.
- **[#47187](https://github.com/vllm-project/vllm/pull/47187)** (Opened) Aims to make the Transformers modeling backend as fast as native vLLM, potentially unifying model support without sacrificing performance.

## More changes by area

<details>
<summary>Performance (16)</summary>

- [#46703](https://github.com/vllm-project/vllm/pull/46703) Extend NCCL symmetric memory to AllGather and ReduceScatter
- [#46750](https://github.com/vllm-project/vllm/pull/46750) Expand Triton kernel warmup coverage, Qwen
- [#46634](https://github.com/vllm-project/vllm/pull/46634) Expand Triton kernel warmup coverage, DSv4
- [#44313](https://github.com/vllm-project/vllm/pull/44313) Add Fused Shared Expert (FSE) support for GLM-4.5/6/7
- [#44639](https://github.com/vllm-project/vllm/pull/44639) Added tanh AOR for faster gelu activations
- [#45033](https://github.com/vllm-project/vllm/pull/45033) Add AITER FlashAttention MLA prefill backend
- [#46635](https://github.com/vllm-project/vllm/pull/46635) Replace MOE all-reduce with reduce-scatter
- [#45739](https://github.com/vllm-project/vllm/pull/45739) Restore zero-init of swizzled NVFP4 scale buffer to recover Blackwell decode throughput
- [#47391](https://github.com/vllm-project/vllm/pull/47391) (Opened) Optimize padded EAGLE input prep and EAGLE3 layer0 RMSNorm concat
- [#46980](https://github.com/vllm-project/vllm/pull/46980) (Opened) parallelize sub-batch KV cache loading
- [#47006](https://github.com/vllm-project/vllm/pull/47006) (Opened) Replace MOE all-reduce with reduce-scatter
- [#46998](https://github.com/vllm-project/vllm/pull/46998) (Opened) fuse more rmsnorm and all-reduce in qwen3.5
- [#47225](https://github.com/vllm-project/vllm/pull/47225) (Opened) Build Phi4MM Conformer streaming mask on target device
- [#47198](https://github.com/vllm-project/vllm/pull/47198) (Opened) Remove redundant op for GLM 5.2
- [#47202](https://github.com/vllm-project/vllm/pull/47202) (Opened) Add `wq_b` from eager to cuda graph, 11.8%~16.7% TTFT improvement
- [#46935](https://github.com/vllm-project/vllm/pull/46935) (Opened) AsyncTP fusion for dynamic per-group FP8 scaled_mm + comms

</details>

<details>
<summary>Kernels & attention (34)</summary>

- [#46876](https://github.com/vllm-project/vllm/pull/46876) Implement op fusion for GLM5/DSV3.2
- [#46346](https://github.com/vllm-project/vllm/pull/46346) Improve kkt kernel of CuteDSL prefill backend
- [#46020](https://github.com/vllm-project/vllm/pull/46020) add HPC-Ops Attention backend
- [#46182](https://github.com/vllm-project/vllm/pull/46182) CuTeDSL warmup infrastructure, FA4 MLA
- [#47090](https://github.com/vllm-project/vllm/pull/47090) Support FlashMLA FP8 KV cache (Hopper & Blackwell)
- [#46713](https://github.com/vllm-project/vllm/pull/46713) Batch Lookup in C
- [#46621](https://github.com/vllm-project/vllm/pull/46621) Improve Triton JIT diagnostics
- [#46819](https://github.com/vllm-project/vllm/pull/46819) Triton MLA logits workspace
- [#46984](https://github.com/vllm-project/vllm/pull/46984) Use functions instead of PTX for the PDL instruction
- [#47308](https://github.com/vllm-project/vllm/pull/47308) Warmup cross-attn properly in encoder-decoder case
- [#43729](https://github.com/vllm-project/vllm/pull/43729) Support DCP with FlashInfer MLA
- [#47304](https://github.com/vllm-project/vllm/pull/47304) Update DeepGEMM tag to point to latest nv-dev branch for sm120 support
- [#47327](https://github.com/vllm-project/vllm/pull/47327) (Opened) Add dense MHA path for sparse MLA short sequences
- [#47181](https://github.com/vllm-project/vllm/pull/47181) (Opened) Integrate Decode Context Parallel with FlashInfer MLA and other features
- [#47361](https://github.com/vllm-project/vllm/pull/47361) (Opened) Delete PagedAttention
- [#47287](https://github.com/vllm-project/vllm/pull/47287) (Opened) Add AITER sparse paged attention
- [#46963](https://github.com/vllm-project/vllm/pull/46963) (Opened) Use FlashInfer for pre-SM100 NVFP4 KV cache updates
- [#47075](https://github.com/vllm-project/vllm/pull/47075) (Opened) Add Triton warmup compile-key tracing
- [#47055](https://github.com/vllm-project/vllm/pull/47055) (Opened) Feat/oscar pytorch
- [#47279](https://github.com/vllm-project/vllm/pull/47279) (Opened) implement return indexer topk of sparse attention
- [#47343](https://github.com/vllm-project/vllm/pull/47343) (Opened) Use Helion fused-quant kernels by default
- [#47106](https://github.com/vllm-project/vllm/pull/47106) (Opened) Support Nvfp4 Cutedsl Moe Swiglu-oai and Relu2 Activation
- [#47348](https://github.com/vllm-project/vllm/pull/47348) (Opened) Optimize CuTeDSL DCP top-k merge
- [#47355](https://github.com/vllm-project/vllm/pull/47355) (Opened) Overlap DCP sparse MLA indexer work
- [#47141](https://github.com/vllm-project/vllm/pull/47141) (Opened) Topk softplus sqrt
- [#47084](https://github.com/vllm-project/vllm/pull/47084) (Opened) TD operand loads for Mamba2 _bmm_chunk_fwd
- [#47404](https://github.com/vllm-project/vllm/pull/47404) (Opened) Synchronize sparse MLA metadata before graph replay
- [#47205](https://github.com/vllm-project/vllm/pull/47205) (Opened) Tensor-descriptor operand loads for Triton W8A8 scaled_mm
- [#47408](https://github.com/vllm-project/vllm/pull/47408) (Opened) Applies routed_scaling_factor internally
- [#47102](https://github.com/vllm-project/vllm/pull/47102) (Opened) Add Triton Backend for Unlimited-OCR R-SWA
- [#47152](https://github.com/vllm-project/vllm/pull/47152) (Opened) Tensor-descriptor operand loads for W8A8 block-INT8 matmul
- [#47204](https://github.com/vllm-project/vllm/pull/47204) (Opened) Tensor-descriptor activation load for AWQ Triton GEMM
- [#47248](https://github.com/vllm-project/vllm/pull/47248) (Opened) Enable tensor-descriptor Q load for non-power-of-2 GQA
- [#47060](https://github.com/vllm-project/vllm/pull/47060) (Opened) Mirror Triton KV dtype checks in MLA

</details>

<details>
<summary>MoE & quantization (13)</summary>

- [#42920](https://github.com/vllm-project/vllm/pull/42920) Support cpu compressed-tensor w8a8 int8 moe
- [#44977](https://github.com/vllm-project/vllm/pull/44977) Fuse MLA q/kv RMSNorm + FP8 per-token quant in the FP8 attention path
- [#46756](https://github.com/vllm-project/vllm/pull/46756) Add MiniMax-M3 modelopt nvfp4 support
- [#45723](https://github.com/vllm-project/vllm/pull/45723) Plumb gemm1_alpha/beta/clamp_limit into TRT-LLM FP8 MoE
- [#46629](https://github.com/vllm-project/vllm/pull/46629) Add back emulation to available OCP MX backends list
- [#47229](https://github.com/vllm-project/vllm/pull/47229) Better MXFP8 quantization kernel
- [#47226](https://github.com/vllm-project/vllm/pull/47226) (Opened) Integrate flashinfer MoE LoRA
- [#47124](https://github.com/vllm-project/vllm/pull/47124) (Opened) Add W4A16(moe) / MXFP4(linear/moe) Support
- [#47120](https://github.com/vllm-project/vllm/pull/47120) (Opened) Add int4 per-channel embedding quantization
- [#47122](https://github.com/vllm-project/vllm/pull/47122) (Opened) add quant input when prepare for fusedmoe
- [#47145](https://github.com/vllm-project/vllm/pull/47145) (Opened) Dispatch MXFP4 compress kernel to SYCL on XPU
- [#47256](https://github.com/vllm-project/vllm/pull/47256) (Opened) remove is_xxx from moe class
- [#47427](https://github.com/vllm-project/vllm/pull/47427) (Opened) Set TRT-LLM tuning range from token capacity

</details>

<details>
<summary>Model support (16)</summary>

- [#44785](https://github.com/vllm-project/vllm/pull/44785) Add LLaVA-OneVision-2
- [#47263](https://github.com/vllm-project/vllm/pull/47263) Remove AyaVision, MusicFlamingo
- [#42406](https://github.com/vllm-project/vllm/pull/42406) support mamba hybrid models align prefix cache
- [#46564](https://github.com/vllm-project/vllm/pull/46564) Support Unlimited OCR
- [#47143](https://github.com/vllm-project/vllm/pull/47143) Remove Tarsier, Tarsier2
- [#30966](https://github.com/vllm-project/vllm/pull/30966) Migrate GPTBigCode and Starcoder2 to Transformers backend
- [#41026](https://github.com/vllm-project/vllm/pull/41026) Add support for openai/privacy-filter
- [#46806](https://github.com/vllm-project/vllm/pull/46806) Remove mantis
- [#47192](https://github.com/vllm-project/vllm/pull/47192) Support Hy3 token suffix and JSON Schema array types
- [#46740](https://github.com/vllm-project/vllm/pull/46740) Add language-backbone LoRA support for MiniCPM-V 4.6
- [#47271](https://github.com/vllm-project/vllm/pull/47271) (Opened) Add support for OpenPangu V2 model
- [#47207](https://github.com/vllm-project/vllm/pull/47207) (Opened) Migrating Deepseek V3.2 to vllm/models/deepseek_v32/
- [#47416](https://github.com/vllm-project/vllm/pull/47416) (Opened) Add fused Kimi K2.5 image preprocessing
- [#47118](https://github.com/vllm-project/vllm/pull/47118) (Opened) Enable FlashInfer + FP8 KV cache for text-only requests in Gemma 4 multimodal models
- [#47191](https://github.com/vllm-project/vllm/pull/47191) (Opened) Add Ray Data batch VLM inference example with ROCm support
- [#47036](https://github.com/vllm-project/vllm/pull/47036) (Opened) Enable LoRA support for Fuyu

</details>

<details>
<summary>Parallelism & scheduling (38)</summary>

- [#46807](https://github.com/vllm-project/vllm/pull/46807) PD disagg with Mooncake Connector: GDN support (Qwen3.5) and MLA support (Deepseek-V4-Flash)
- [#46781](https://github.com/vllm-project/vllm/pull/46781) Implement block verification for rejection sampling (Spec Decode)
- [#38174](https://github.com/vllm-project/vllm/pull/38174) Universal speculative decoding for heterogeneous vocabularies
- [#38128](https://github.com/vllm-project/vllm/pull/38128) Mask padding in EPLB load recording
- [#46104](https://github.com/vllm-project/vllm/pull/46104) Support SWA + DFlash for MiMo
- [#47093](https://github.com/vllm-project/vllm/pull/47093) DSpark speculators checkpoint support
- [#46786](https://github.com/vllm-project/vllm/pull/46786) Handle tuple hidden states from MTP draft models
- [#43637](https://github.com/vllm-project/vllm/pull/43637) Detect all2all peer fault with fault tolerance backend
- [#44443](https://github.com/vllm-project/vllm/pull/44443) Enable ModelRunner V2 by default for all dense models
- [#47219](https://github.com/vllm-project/vllm/pull/47219) Default FlashInfer allreduce to mnnvl on single node
- [#46450](https://github.com/vllm-project/vllm/pull/46450) Pass `ScheduleEndContext` to `on_schedule_end` hook
- [#46777](https://github.com/vllm-project/vllm/pull/46777) MultiConnector: merge kv_transfer_params dicts across connectors
- [#46968](https://github.com/vllm-project/vllm/pull/46968) Avoid redundant hidden-states gather in draft prefill
- [#47357](https://github.com/vllm-project/vllm/pull/47357) (Opened) Stateful trainer send
- [#47423](https://github.com/vllm-project/vllm/pull/47423) (Opened) CPU Offloading EC Connector
- [#47302](https://github.com/vllm-project/vllm/pull/47302) (Opened) Add MooncakeStoreECConnector for multimodal hidden-state transfer
- [#47320](https://github.com/vllm-project/vllm/pull/47320) (Opened) Decouple stock torch.compile cudagraphs via StockCUDAGraphWrapper
- [#47306](https://github.com/vllm-project/vllm/pull/47306) (Opened) Draft: Xqa specdec
- [#47288](https://github.com/vllm-project/vllm/pull/47288) (Opened) Async preparation for Elastic EP
- [#47131](https://github.com/vllm-project/vllm/pull/47131) (Opened) Add D-cut: Adaptive Verification Depth Pruning for Batched Speculative Decoding
- [#47414](https://github.com/vllm-project/vllm/pull/47414) (Opened) Enable dspark for deepseek v4
- [#47419](https://github.com/vllm-project/vllm/pull/47419) (Opened) Enable DeepSeek-V4 DSpark speculative decoding on AMD
- [#47107](https://github.com/vllm-project/vllm/pull/47107) (Opened) Kick off final block offload at request finish
- [#47216](https://github.com/vllm-project/vllm/pull/47216) (Opened) Add Gemma4-12B DSpark draft model
- [#46994](https://github.com/vllm-project/vllm/pull/46994) (Opened) Support MTP speculative decoding under pipeline parallelism
- [#47111](https://github.com/vllm-project/vllm/pull/47111) (Opened) Adaptive K: Per-position EMA goodput cost model
- [#47021](https://github.com/vllm-project/vllm/pull/47021) (Opened) Avoid reading expired blocks in bidirectional turn-2 read
- [#46942](https://github.com/vllm-project/vllm/pull/46942) (Opened) Enable mm prefix bidi attention support on MRV2
- [#47274](https://github.com/vllm-project/vllm/pull/47274) (Opened) Add `TieringManagerReverseAPI` protocol for P2P secondary tier
- [#47373](https://github.com/vllm-project/vllm/pull/47373) (Opened) Use prefill block content to overwrite decode bad blocks
- [#47063](https://github.com/vllm-project/vllm/pull/47063) (Opened) Support workload identity for objectstore secondary tier
- [#47331](https://github.com/vllm-project/vllm/pull/47331) (Opened) Overlap bonus sampling with target verification via maybe_execute_in_parallel
- [#47317](https://github.com/vllm-project/vllm/pull/47317) (Opened) Apply SWA lookup mask before hashing/key build
- [#47413](https://github.com/vllm-project/vllm/pull/47413) (Opened) Add tier_idx to SecondaryTierManager for per-tier metrics
- [#47070](https://github.com/vllm-project/vllm/pull/47070) (Opened) Support sequence parallel without the need for DP
- [#47377](https://github.com/vllm-project/vllm/pull/47377) (Opened) Add DSpark support for Qwen3.5 target models
- [#46954](https://github.com/vllm-project/vllm/pull/46954) (Opened) Add canonical KV layout fields for TP-agnostic offload

</details>

<details>
<summary>Hardware & arch (14)</summary>

- [#47105](https://github.com/vllm-project/vllm/pull/47105) Support ZE_AFFINITY_MASK passthrough in xpu_disagg_acc_test
- [#47134](https://github.com/vllm-project/vllm/pull/47134) C++ implementation for get_memory_info
- [#43950](https://github.com/vllm-project/vllm/pull/43950) Use aiter mHC pre/post as the default ROCm path
- [#47162](https://github.com/vllm-project/vllm/pull/47162) Remove speculative decoding stream overrides from CPUModelRunner
- [#46433](https://github.com/vllm-project/vllm/pull/46433) Optimize XPU worker shutdown logic to prevent resource leak
- [#46990](https://github.com/vllm-project/vllm/pull/46990) Stabilize high-throughput DBO for DP+EP
- [#47269](https://github.com/vllm-project/vllm/pull/47269) Cross-layer lightning-indexer top-k sharing
- [#46987](https://github.com/vllm-project/vllm/pull/46987) revert weightless change on xpu
- [#47004](https://github.com/vllm-project/vllm/pull/47004) Use ROCm-aware FA availability check for Unlimited-OCR
- [#47321](https://github.com/vllm-project/vllm/pull/47321) (Opened) optimize math functions of VSX power
- [#46992](https://github.com/vllm-project/vllm/pull/46992) (Opened) Keep incompatible KV layouts in separate tensors
- [#47353](https://github.com/vllm-project/vllm/pull/47353) (Opened) Add a guard for EPLB/DBO plus fused share expert conflict
- [#47017](https://github.com/vllm-project/vllm/pull/47017) (Opened) Enable DeepSeek-V4 on gfx11
- [#47393](https://github.com/vllm-project/vllm/pull/47393) (Opened) add index topk interval

</details>

<details>
<summary>API & serving (42)</summary>

- [#45890](https://github.com/vllm-project/vllm/pull/45890) Add static HTTPS and mTLS support for HTTP and gRPC
- [#47265](https://github.com/vllm-project/vllm/pull/47265) Split engine core DTOs into separate modules
- [#47283](https://github.com/vllm-project/vllm/pull/47283) Use enum-backed domain types for engine outputs
- [#47185](https://github.com/vllm-project/vllm/pull/47185) Harmony Responses API Refactor
- [#46800](https://github.com/vllm-project/vllm/pull/46800) Add Harmony Renderer for GPT-OSS
- [#46610](https://github.com/vllm-project/vllm/pull/46610) Add Streaming Parser Engine and new Kimi k2.5/k2.6/k2.7 Parser
- [#44512](https://github.com/vllm-project/vllm/pull/44512) Consolidate scale out entrypoints
- [#46306](https://github.com/vllm-project/vllm/pull/46306) Expose profiler control routes
- [#47101](https://github.com/vllm-project/vllm/pull/47101) Refactor TLS serve path with unified `MaybeTlsListener`
- [#44074](https://github.com/vllm-project/vllm/pull/44074) Pluggable sleep-mode backend abstraction
- [#46846](https://github.com/vllm-project/vllm/pull/46846) Add return_loss_mask to render endpoint
- [#46833](https://github.com/vllm-project/vllm/pull/46833) Start current wave for a stale DP FirstRequest
- [#47040](https://github.com/vllm-project/vllm/pull/47040) Avoid LoRA registry scans without active LoRA requests
- [#46512](https://github.com/vllm-project/vllm/pull/46512) Add error context in tool parser failures
- [#46827](https://github.com/vllm-project/vllm/pull/46827) Keep literal "null" string for string-typed tool params
- [#47076](https://github.com/vllm-project/vllm/pull/47076) DP supervisor using rust frontend
- [#47166](https://github.com/vllm-project/vllm/pull/47166) Coerce completion `max_tokens: null` to default
- [#47243](https://github.com/vllm-project/vllm/pull/47243) Make sleep-mode backend capability flags communicator-agnostic
- [#46482](https://github.com/vllm-project/vllm/pull/46482) MoRIIO toy proxy: support JSON Content-Type for OpenAI clients
- [#47189](https://github.com/vllm-project/vllm/pull/47189) (Opened) Cohere chat v2 api support
- [#47395](https://github.com/vllm-project/vllm/pull/47395) (Opened) Add DoRA support for serving and linear layers
- [#47301](https://github.com/vllm-project/vllm/pull/47301) (Opened) Add detokenization streaming derender for disaggregated serving
- [#47167](https://github.com/vllm-project/vllm/pull/47167) (Opened) poolside_v1: migrate to the declarative parser engine
- [#47363](https://github.com/vllm-project/vllm/pull/47363) (Opened) Demo implementation of extensible kv cache memory
- [#47254](https://github.com/vllm-project/vllm/pull/47254) (Opened) add functiongemma tool parser support
- [#47362](https://github.com/vllm-project/vllm/pull/47362) (Opened) Add TLS certificate hot-reload
- [#47203](https://github.com/vllm-project/vllm/pull/47203) (Opened) Match Python union-type coercion precedence
- [#47176](https://github.com/vllm-project/vllm/pull/47176) (Opened) Validate structured-output requests to match Python
- [#47024](https://github.com/vllm-project/vllm/pull/47024) (Opened) Support OpenAI Responses API namespace tools
- [#47388](https://github.com/vllm-project/vllm/pull/47388) (Opened) Persist and reuse the memory-profiling result across boots
- [#47061](https://github.com/vllm-project/vllm/pull/47061) (Opened) Flush Harmony parser at EOS for Responses API
- [#47379](https://github.com/vllm-project/vllm/pull/47379) (Opened) Use process_eos() to flush HarmonyParser for Responses API
- [#47322](https://github.com/vllm-project/vllm/pull/47322) (Opened) Spec decode per request stats
- [#47313](https://github.com/vllm-project/vllm/pull/47313) (Opened) feat: expose stop reason in token generate responses
- [#46938](https://github.com/vllm-project/vllm/pull/46938) (Opened) Report prefix cache hit rate in vllm bench serve
- [#47402](https://github.com/vllm-project/vllm/pull/47402) (Opened) Add jitter to LoRA adapter_config.json load retries
- [#47155](https://github.com/vllm-project/vllm/pull/47155) (Opened) Avoid GLM4V processor init during startup metadata reads
- [#47173](https://github.com/vllm-project/vllm/pull/47173) (Opened) Add /abort_requests to the RLHF dev API router
- [#47411](https://github.com/vllm-project/vllm/pull/47411) (Opened) Support min_tokens in beam search
- [#47345](https://github.com/vllm-project/vllm/pull/47345) (Opened) Added olmo3 reasoning parser
- [#47148](https://github.com/vllm-project/vllm/pull/47148) (Opened) Add `model_class_overrides` for development and debugging
- [#47289](https://github.com/vllm-project/vllm/pull/47289) (Opened) Recover buffered text from incomplete tool calls at EOS
- [#47112](https://github.com/vllm-project/vllm/pull/47112) (Opened) Enforce max_tool_calls for Responses built-in tools
- [#47053](https://github.com/vllm-project/vllm/pull/47053) (Opened) only materialize tokens when thinking budget is in req
- [#47213](https://github.com/vllm-project/vllm/pull/47213) (Opened) add BROWSER_BACKEND env var support to HarmonyBrowserTool

</details>

<details>
<summary>Tests (23)</summary>

- [#47125](https://github.com/vllm-project/vllm/pull/47125) Simplify unit tests with shared `TestTokenizer`
- [#47250](https://github.com/vllm-project/vllm/pull/47250) Run SageMaker handler-override tests in-process
- [#47110](https://github.com/vllm-project/vllm/pull/47110) Extend renderer/parser roundtrip tests
- [#47003](https://github.com/vllm-project/vllm/pull/47003) Use spawn around the threaded OTLP test
- [#46999](https://github.com/vllm-project/vllm/pull/46999) Explicitly tear down multimodal offline LLMs
- [#41396](https://github.com/vllm-project/vllm/pull/41396) Add Medusa speculative decoding e2e test
- [#47000](https://github.com/vllm-project/vllm/pull/47000) Keep assigned GPU visible for weight transfer
- [#45490](https://github.com/vllm-project/vllm/pull/45490) Make memory sampling less racy in tests and sleep mode
- [#46993](https://github.com/vllm-project/vllm/pull/46993) Clone prefill backend state per metadata builder
- [#42486](https://github.com/vllm-project/vllm/pull/42486) Enable ut qk_norm_rope_fusion
- [#45140](https://github.com/vllm-project/vllm/pull/45140) Adjust kernel unit tests for XPU
- [#47011](https://github.com/vllm-project/vllm/pull/47011) Add transformers version check for openai/privacy-filter
- [#47085](https://github.com/vllm-project/vllm/pull/47085) Make tests/v1/shutdown an importable package
- [#47399](https://github.com/vllm-project/vllm/pull/47399) (Opened) Detect CUDA toolchain/driver PTX mismatch on GB10
- [#47234](https://github.com/vllm-project/vllm/pull/47234) (Opened) Document CPU eviction behavior as reference
- [#47002](https://github.com/vllm-project/vllm/pull/47002) (Opened) Apply xgrammar bitmasks in vLLM on ROCm
- [#47178](https://github.com/vllm-project/vllm/pull/47178) (Opened) Revert moe_sum fp32 kernel to test PD prefix cache flake
- [#47190](https://github.com/vllm-project/vllm/pull/47190) (Opened) Recover GLM-4.7 tool calls missing arg_key start
- [#47262](https://github.com/vllm-project/vllm/pull/47262) (Opened) Add benchmark JSONL append helper
- [#47394](https://github.com/vllm-project/vllm/pull/47394) (Opened) Drop response format for auto tool choice
- [#47038](https://github.com/vllm-project/vllm/pull/47038) (Opened) Drop ngram padding (-1) in guidance validate_tokens
- [#47389](https://github.com/vllm-project/vllm/pull/47389) (Opened) Ignore non-engine DP handshake messages
- plus 1 more minor test update

</details>

<details>
<summary>CI & build (32)</summary>

- [#47032](https://github.com/vllm-project/vllm/pull/47032) Add CPU test dependency pre-commit hooks
- [#46886](https://github.com/vllm-project/vllm/pull/46886) Add ci_base metadata for external cache orchestration
- [#47128](https://github.com/vllm-project/vllm/pull/47128) Move to stable abi since ROCm upgraded to torch 2.11
- [#47338](https://github.com/vllm-project/vllm/pull/47338) Remove unused Dockerfile.nightly_torch
- [#47048](https://github.com/vllm-project/vllm/pull/47048) Move distributed small LM eval to B200
- [#47018](https://github.com/vllm-project/vllm/pull/47018) Enable mypy for tests directory
- [#46930](https://github.com/vllm-project/vllm/pull/46930) Tweak mirrored tests; improve CI base dependency change detection
- [#46683](https://github.com/vllm-project/vllm/pull/46683) Bump flashinfer version to 0.6.13
- [#47342](https://github.com/vllm-project/vllm/pull/47342) Remove torch_nightly mirror tags
- [#47094](https://github.com/vllm-project/vllm/pull/47094) Move LM Eval Large Models (8 GPUs) to mi300 pool
- [#47065](https://github.com/vllm-project/vllm/pull/47065) Move PyTorch Compilation Unit Tests to MI300(gfx942)
- [#45977](https://github.com/vllm-project/vllm/pull/45977) Enable shared loader test
- [#47195](https://github.com/vllm-project/vllm/pull/47195) Bump timeouts of various test groups on AMD CI
- [#47193](https://github.com/vllm-project/vllm/pull/47193) Enable LoRA TP Distributed Test Group In AMD CI
- [#47008](https://github.com/vllm-project/vllm/pull/47008) exclude unsupported models for test_tensor_sechma.py
- [#47222](https://github.com/vllm-project/vllm/pull/47222) Toggle test coredumps on ROCm debug agent
- [#47067](https://github.com/vllm-project/vllm/pull/47067) Soft Fail `Spec Decode Ngram + Suffix` and `Entrypoints Integration (LLM)` AMD Mirrors
- [#33057](https://github.com/vllm-project/vllm/pull/33057) Bump actions/checkout from 6.0.1 to 7.0.0
- [#47376](https://github.com/vllm-project/vllm/pull/47376) Split test_punica_ops into separate pytest invocations for stability
- [#47132](https://github.com/vllm-project/vllm/pull/47132) Mistral label alert
- [#47139](https://github.com/vllm-project/vllm/pull/47139) Bump PyNvVideoCodec version
- [#47030](https://github.com/vllm-project/vllm/pull/47030) (Opened) Enable vLLM DI CI with buildkite/slurm
- [#46978](https://github.com/vllm-project/vllm/pull/46978) (Opened) Towards AMD test parity
- [#47149](https://github.com/vllm-project/vllm/pull/47149) (Opened) Fix CUDA arch coverage checks and scoped kernel feature flags
- [#47378](https://github.com/vllm-project/vllm/pull/47378) (Opened) Bump the minor-update group across 1 directory with 159 updates
- [#47059](https://github.com/vllm-project/vllm/pull/47059) (Opened) Torch Stable ABI pre-commit hook
- [#47180](https://github.com/vllm-project/vllm/pull/47180) (Opened) Add TORCH_NIGHTLY=1 build mode
- [#47182](https://github.com/vllm-project/vllm/pull/47182) (Opened) Changes with respect to relevant cpu tests for ZenDNN
- [#47240](https://github.com/vllm-project/vllm/pull/47240) (Opened) Debug Intel B50 agent
- [#47330](https://github.com/vllm-project/vllm/pull/47330) (Opened) Pin `amd-quark` to 0.12.rc4
- [#47171](https://github.com/vllm-project/vllm/pull/47171) (Opened) Add GSM8K accuracy configs for large NVFP4/INT4 MoEs (H200)
- [#47170](https://github.com/vllm-project/vllm/pull/47170) (Opened) Add GSM8K accuracy configs for Blackwell NVFP4/FP8 models
- [#47186](https://github.com/vllm-project/vllm/pull/47186) (Opened) Bump to AITER v0.1.16.post3

</details>

<details>
<summary>Docs (2)</summary>

- [#45903](https://github.com/vllm-project/vllm/pull/45903) document gRPC interface as insecure for private use only
- [#47009](https://github.com/vllm-project/vllm/pull/47009) Fix docs on main

</details>

<details>
<summary>Bugfixes (100)</summary>

- [#46875](https://github.com/vllm-project/vllm/pull/46875) Ensure tool call or other special tokens don't leak
- [#47015](https://github.com/vllm-project/vllm/pull/47015) Fix transient dependency issues caused by `requirements/common.txt`
- [#45368](https://github.com/vllm-project/vllm/pull/45368) Align LoRA implementation with Punica GPU
- [#46034](https://github.com/vllm-project/vllm/pull/46034) Enable dual-path ViT CUDA graph for Step3-VL
- [#46997](https://github.com/vllm-project/vllm/pull/46997) Pass q/kv dtypes to get_mla_metadata_v1 in FP8 decode
- [#46301](https://github.com/vllm-project/vllm/pull/46301) Fix hidden-state extraction block size for hybrid verifiers
- [#46860](https://github.com/vllm-project/vllm/pull/46860) Fix W8A8 int-quantized scheme selection regression
- [#35076](https://github.com/vllm-project/vllm/pull/35076) Propagate default stop_token_ids to per-request SamplingParams
- [#47126](https://github.com/vllm-project/vllm/pull/47126) Fix beam search candidate indexing when logprobs count varies
- [#43757](https://github.com/vllm-project/vllm/pull/43757) Fix thinking_token_budget not enforced on re-entry
- [#46958](https://github.com/vllm-project/vllm/pull/46958) Revert "[KV Offload] Use background thread for mmap / cpu_tensors pinning"
- [#47010](https://github.com/vllm-project/vllm/pull/47010) prevent image decompression bomb OOM denial of service
- [#46839](https://github.com/vllm-project/vllm/pull/46839) Reject prompt_logprobs for streaming generate
- [#47007](https://github.com/vllm-project/vllm/pull/47007) bound tokenizer work when explicit truncation_side is set
- [#46855](https://github.com/vllm-project/vllm/pull/46855) Fix Mooncake lookup prefixes with DCP > 1
- [#46612](https://github.com/vllm-project/vllm/pull/46612) Raise VLLMValidationError for non-integer logit_bias keys
- [#47062](https://github.com/vllm-project/vllm/pull/47062) Return raw output when Harmony parser ends non-terminal
- [#47135](https://github.com/vllm-project/vllm/pull/47135) Fix empty decoder prompt for Cohere ASR in throughput benchmark
- [#45960](https://github.com/vllm-project/vllm/pull/45960) Seed RayExecutorV2 TCPStore port by DP rank to avoid collisions
- [#47029](https://github.com/vllm-project/vllm/pull/47029) Prevent padding placeholders from reaching embeddings
- plus 80 more minor bugfixes

</details>

<details>
<summary>Refactors (18)</summary>

- [#47058](https://github.com/vllm-project/vllm/pull/47058) Remove more unnecessary `load_weights` methods
- [#44589](https://github.com/vllm-project/vllm/pull/44589) Remove unnecessary `load_weights` methods
- [#44353](https://github.com/vllm-project/vllm/pull/44353) Weight sync refactor + move sparse nccl engine
- [#43373](https://github.com/vllm-project/vllm/pull/43373) Standardize Humming MoE experts + utilities
- [#47140](https://github.com/vllm-project/vllm/pull/47140) Replace `torch.cuda.Event` with `torch.Event`
- [#44825](https://github.com/vllm-project/vllm/pull/44825) Replace `torch.cuda.mem_get_info` with `torch.accelerator.get_memory_info`
- [#46842](https://github.com/vllm-project/vllm/pull/46842) Remove dead minimax allreduce rms kernel
- [#46956](https://github.com/vllm-project/vllm/pull/46956) Remove boilerplate missed by #46820
- [#47371](https://github.com/vllm-project/vllm/pull/47371) (Opened) Revert "Weight sync refactor + move sparse nccl engine"
- [#47097](https://github.com/vllm-project/vllm/pull/47097) (Opened) Revert "[MoE Refactor] Standardize Humming MoE experts + utilities"
- [#47344](https://github.com/vllm-project/vllm/pull/47344) (Opened) Refactor IPC calculation out of gpu_worker
- [#47369](https://github.com/vllm-project/vllm/pull/47369) (Opened) Revert "[CPU][Perf]Added tanh AOR for faster gelu activations."
- [#47034](https://github.com/vllm-project/vllm/pull/47034) (Opened) Revert "[MM][CG] Gemma3 Encoder CUDA Graph"
- [#47329](https://github.com/vllm-project/vllm/pull/47329) (Opened) Remove multiple dead code
- [#47232](https://github.com/vllm-project/vllm/pull/47232) (Opened) Revert "[Platform] Replace `torch.cuda.mem_get_info` with `torch.accelerator.get_memory_info`"
- [#47293](https://github.com/vllm-project/vllm/pull/47293) (Opened) Revert "[Distributed] Default FlashInfer allreduce to mnnvl on single node"
- [#46969](https://github.com/vllm-project/vllm/pull/46969) (Opened) Remove tool_parsers/gemma4_utils.py in favor of Transformers v5 chat parsing API
- [#47370](https://github.com/vllm-project/vllm/pull/47370) (Opened) Revert "[ModelRunner V2] Warmup cross-attn properly in encoder-decoder case"

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: d8f264a42781a9c6aa112dd10b64bf2a244b06eb91c2da5a384251c1a3b4a63f -->
