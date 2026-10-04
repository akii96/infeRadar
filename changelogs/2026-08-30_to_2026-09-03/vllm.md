# vllm: PR digest (2026-08-30 to 2026-09-03)

_250 merged, 438 newly opened - source vllm-project/vllm, generated 2026-09-03T13:32:04Z_

## TL;DR
- **DeepSeek, Qwen and Kimi-K3 got the most attention.** DeepSeek-V4 saw the vision model land (`[#54566](https://github.com/vllm-project/vllm/pull/54566)`), the DSv3 router GEMM CUDA kernel retired (`[#54040](https://github.com/vllm-project/vllm/pull/54040)`), and a stream of sparse-MLA/CSA work (SM90 Q8KV8 prefill, ROCm HIP compressor, OPUS prefill) opened. Qwen3.8-Flash-Next support merged (`[#53896](https://github.com/vllm-project/vllm/pull/53896)`) and was followed by fused PLE kernels and QSA indexer tuning. Kimi-K3 got AttnRes, router-GEMM and MLA decode perf work.
- **Perf work centered on small-batch decode and sparse attention.** This included Kimi-K3 low-M router GEMM and prefetch, DSV3 GEMM on strided tensors (12–81% faster, `[#54565](https://github.com/vllm-project/vllm/pull/54565)`), fused embedding, NVFP4 padding init in the quant kernel, and a FlashInfer PCIe IPC all-reduce. Newly opened PRs push prefill-indexer sharding across TP, BS=1 DFlash/DSpark, and CuteDSL BF16 GEMM as the default.
- **Quantization is being re-architected around `QuantKey`.** ModelOpt and Quark dispatch were redesigned, online quantization became configurable, and W4A16 and AutoRound FP8/MXFP8 paths expanded.
- **KV offload/connector hardening.** Mooncake (heterogeneous TP, partial tails, block transfer length) and CPU offload received many bugfixes. Hybrid-model prefix caching with MTP and ReplaySSM is in flight as WIP.
- **Overall direction:** new-model enablement (Qwen3.8, DSv4-Vision, K2-Horizon) plus Blackwell/ROCm kernel tuning, with lots of CI sharding and security-bound bugfixes.

## Most important PRs
**[#53896](https://github.com/vllm-project/vllm/pull/53896) Support Qwen3.8-Flash-Next**
A roughly 19k-line model enablement touching attention, KV cache, MoE, quantization and speculative decode. It adds the QSA sparse-attention path and indexer, so the follow-up PRs (`[#54517](https://github.com/vllm-project/vllm/pull/54517)`, `[#54513](https://github.com/vllm-project/vllm/pull/54513)`) are tuning work on top.

**[#54566](https://github.com/vllm-project/vllm/pull/54566) DeepSeek-V4-Flash-Vision-Exp support**
Adds multimodal DeepSeek-V4 with FlashInfer and MoE integration. ROCm enablement (`[#55107](https://github.com/vllm-project/vllm/pull/55107)`) is already open.

**[#49381](https://github.com/vllm-project/vllm/pull/49381) Redesign ModelOpt LinearMethod classes on QuantKey**
Replaces per-scheme method classes with one generic QuantKey-driven method. `[#52958](https://github.com/vllm-project/vllm/pull/52958)` does the same for Quark, so quant dispatch is converging on a single abstraction.

**[#52017](https://github.com/vllm-project/vllm/pull/52017) B12X causal paged attention backend**
A new attention backend. An open follow-up (`[#54976](https://github.com/vllm-project/vllm/pull/54976)`) adds B12X sparse MLA/DSA.

**[#52506](https://github.com/vllm-project/vllm/pull/52506) FlashInfer ReplaySSM backend for Mamba**
Adds a FlashInfer-backed SSM state-replay path for Mamba/hybrid models. Prefix caching and MTP unification for it are open as WIP (`[#54609](https://github.com/vllm-project/vllm/pull/54609)`, `[#54953](https://github.com/vllm-project/vllm/pull/54953)`).

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#54261](https://github.com/vllm-project/vllm/pull/54261) Make native CUDA AttnRes the SM100 default for Kimi-K3
- [#54697](https://github.com/vllm-project/vllm/pull/54697) Overlap low-M TP8 KDA projections for Kimi-K3
- [#53524](https://github.com/vllm-project/vllm/pull/53524) Prefetch ll_bf16 router weights at M=1 for Kimi-K3
- [#54565](https://github.com/vllm-project/vllm/pull/54565) Enable DSV3 GEMM on inner-contiguous and row-strided tensors
- [#53677](https://github.com/vllm-project/vllm/pull/53677) Fused embedding kernel
- [#53568](https://github.com/vllm-project/vllm/pull/53568) Initialize NVFP4 padding inside the quant kernel
- [#53382](https://github.com/vllm-project/vllm/pull/53382) Tune cooperative topk for medium batch sizes
- [#52033](https://github.com/vllm-project/vllm/pull/52033) Dual-stream decode with hipgraphs on ROCm
- [#54660](https://github.com/vllm-project/vllm/pull/54660) Avoid more h2d copies from non-pinned tensors
- [#55062](https://github.com/vllm-project/vllm/pull/55062) Accumulate Conformer attention scores with baddbmm
- [#53517](https://github.com/vllm-project/vllm/pull/53517) Optimize Dots3 runtime
- [#54537](https://github.com/vllm-project/vllm/pull/54537) Resolve async media across modalities concurrently
- [#51453](https://github.com/vllm-project/vllm/pull/51453) Register Triton W4A16 GEMM as a custom op
- [#54449](https://github.com/vllm-project/vllm/pull/54449) Count the Rust tokenizer vocabulary once at construction

</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#54517](https://github.com/vllm-project/vllm/pull/54517) Fuse Qwen4Exp PLE kernels
- [#54513](https://github.com/vllm-project/vllm/pull/54513) Separate prefill and decode paths for QSA indexer
- [#54251](https://github.com/vllm-project/vllm/pull/54251) Warm up Qwen GDN gated RMSNorm
- [#53147](https://github.com/vllm-project/vllm/pull/53147) Prune Triton sliding-window tiles for Gemma4 multimodal prefixes
- [#54194](https://github.com/vllm-project/vllm/pull/54194) Make prefix-prefill tiling independent of KV page size
- [#51705](https://github.com/vllm-project/vllm/pull/51705) ROCm MLA DCP causal multi-token verification
- [#51171](https://github.com/vllm-project/vllm/pull/51171) Full cudagraphs for AITER MLA spec decode
- [#51724](https://github.com/vllm-project/vllm/pull/51724) Enable W4A16 DSA
- [#52724](https://github.com/vllm-project/vllm/pull/52724) Adaptive verification for FLASHINFER_MLA_SPARSE_DSV4
- [#50175](https://github.com/vllm-project/vllm/pull/50175) Migrate generic MLA metadata and indexing kernels (DSv4 warmup)
- [#53014](https://github.com/vllm-project/vllm/pull/53014) FlashInfer CuTeDSL W4A16 linear
- [#54560](https://github.com/vllm-project/vllm/pull/54560) Hopper LL-GEMM tuning table for Qwen4Exp
- [#52191](https://github.com/vllm-project/vllm/pull/52191) CPU FP16/BF16 persisted GDN state on AMX

</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#51217](https://github.com/vllm-project/vllm/pull/51217) Generalize masked activation for padded layouts
- [#50622](https://github.com/vllm-project/vllm/pull/50622) Split AITER CK and Triton MXFP4 W4A16 into separate ROCm backends
- [#51285](https://github.com/vllm-project/vllm/pull/51285) Targeted online quantization config from user patterns
- [#47434](https://github.com/vllm-project/vllm/pull/47434) AutoRound block-wise FP8
- [#51248](https://github.com/vllm-project/vllm/pull/51248) AutoRound MXFP8 MoE on XPU
- [#44834](https://github.com/vllm-project/vllm/pull/44834) Route Int8 MoE through zentorch on AMD CPU
- [#46872](https://github.com/vllm-project/vllm/pull/46872) Remove a redundant top-k pack kernel in TrtLLM NvFP4 MoE
- [#54427](https://github.com/vllm-project/vllm/pull/54427) Route weight-only NVFP4 checkpoints through W4A16
- [#54722](https://github.com/vllm-project/vllm/pull/54722) Validate FP8 PLE weight scale after loading
- [#49936](https://github.com/vllm-project/vllm/pull/49936) Document FP8 GEMM kernel selection

</details>

<details>
<summary>Model support (6)</summary>

- [#55063](https://github.com/vllm-project/vllm/pull/55063) K2-Horizon model support
- [#54040](https://github.com/vllm-project/vllm/pull/54040) Retire the DSv3 router GEMM CUDA kernel
- [#54373](https://github.com/vllm-project/vllm/pull/54373) Take the DFlash draft RoPE layout from its own config
- [#54533](https://github.com/vllm-project/vllm/pull/54533) Support Sentence Transformers 5.4+ configs
- [#54380](https://github.com/vllm-project/vllm/pull/54380) Honor cap_pixels_per_frame in Qwen3-VL memory profiling
- [#54722](https://github.com/vllm-project/vllm/pull/54722) Qwen4 PLE FP8 scale validation (see MoE & quantization)

</details>

<details>
<summary>Parallelism & scheduling (9)</summary>

- [#53129](https://github.com/vllm-project/vllm/pull/53129) Heterogeneous TP sharing in the Mooncake Store connector
- [#53784](https://github.com/vllm-project/vllm/pull/53784) Pre-shared ncclUniqueId rendezvous for weight transfer
- [#53576](https://github.com/vllm-project/vllm/pull/53576) Opt-in FlashInfer PCIe IPC all-reduce backend
- [#51485](https://github.com/vllm-project/vllm/pull/51485) Release NCCL communicator memory in sleep mode
- [#49445](https://github.com/vllm-project/vllm/pull/49445) Add max_num_queued_reqs and max_num_queued_tokens
- [#54856](https://github.com/vllm-project/vllm/pull/54856) Skip DP sync for uniform speculator decodes (MRV2)
- [#54646](https://github.com/vllm-project/vllm/pull/54646) Freeze gc during V2 CUDA graph capture
- [#53388](https://github.com/vllm-project/vllm/pull/53388) Allow disabling trailing prefix-cache block dropping with spec decode
- [#51689](https://github.com/vllm-project/vllm/pull/51689) Certify attention-only hybrids in the offload portability gate

</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#49925](https://github.com/vllm-project/vllm/pull/49925) ROCm TheRock preview docker updates
- [#52650](https://github.com/vllm-project/vllm/pull/52650) Mooncake build in the ROCm base image
- [#55002](https://github.com/vllm-project/vllm/pull/55002) Mooncake from public wheels in the ROCm image
- [#49209](https://github.com/vllm-project/vllm/pull/49209) XPU batch-invariant matmul and linear kernels
- [#53678](https://github.com/vllm-project/vllm/pull/53678) XPU fused GemmaRMSNorm for eager mode
- [#53734](https://github.com/vllm-project/vllm/pull/53734) Route XPU activation CustomOps to SYCL kernels
- [#53536](https://github.com/vllm-project/vllm/pull/53536) Ensure XPU unquantized linear weight is N-contiguous

</details>

<details>
<summary>API & serving (14)</summary>

- [#52910](https://github.com/vllm-project/vllm/pull/52910) Rust frontend: attribute decoded text to tokens
- [#54492](https://github.com/vllm-project/vllm/pull/54492) Move engine/protocol.py out of the openai folder
- [#54242](https://github.com/vllm-project/vllm/pull/54242) Video embeds input support
- [#54579](https://github.com/vllm-project/vllm/pull/54579) Gate scale-out endpoints behind an opt-in flag
- [#54220](https://github.com/vllm-project/vllm/pull/54220) Allow empty video URLs with multi-modal UUIDs
- [#54241](https://github.com/vllm-project/vllm/pull/54241) Include media_io_kwargs in multimodal hashes
- [#53760](https://github.com/vllm-project/vllm/pull/53760) Rust gRPC audio and video inputs
- [#53056](https://github.com/vllm-project/vllm/pull/53056) Migrate Rust frontend to the new tekken crate
- [#54303](https://github.com/vllm-project/vllm/pull/54303) Bound recursive argument parsers in the Rust frontend
- [#54218](https://github.com/vllm-project/vllm/pull/54218) Let terminal grammars stop under min_tokens
- [#45241](https://github.com/vllm-project/vllm/pull/45241) Site-packages support for reasoning/tool parser plugins
- [#54982](https://github.com/vllm-project/vllm/pull/54982) reasoning_token_count in the reasoning parser
- [#49984](https://github.com/vllm-project/vllm/pull/49984) Request-level preemption count histogram
- [#54794](https://github.com/vllm-project/vllm/pull/54794) Avoid FlashInfer autotune on every source change

</details>

<details>
<summary>Bugfixes (51)</summary>

- [#53532](https://github.com/vllm-project/vllm/pull/53532) Fix eager SimpleCPUOffload cache registration and final flush
- [#52832](https://github.com/vllm-project/vllm/pull/52832) Offload producer partial tails on request finish (Mooncake)
- [#54272](https://github.com/vllm-project/vllm/pull/54272) Fix Mooncake physical-block transfer length
- [#52912](https://github.com/vllm-project/vllm/pull/52912) P2P tier declares REQUEST_LEVEL on the producer leg
- [#52596](https://github.com/vllm-project/vllm/pull/52596) Unlink /dev/shm region after all workers map it
- [#52571](https://github.com/vllm-project/vllm/pull/52571) Preserve aborted P2P loads until abort completes
- [#54872](https://github.com/vllm-project/vllm/pull/54872) Ignore stale async lookup results
- [#54759](https://github.com/vllm-project/vllm/pull/54759) Tracker progress for oversized offers
- [#52923](https://github.com/vllm-project/vllm/pull/52923) Wait for offload keys before storing chunks
- [#52290](https://github.com/vllm-project/vllm/pull/52290) Isolate tiering shutdown failures
- [#50883](https://github.com/vllm-project/vllm/pull/50883) Scale UniformTypeKVCacheSpecs groups by DCP
- [#54647](https://github.com/vllm-project/vllm/pull/54647) Fix DecodeBenchConnector HMA cache-group mapping
- [#54679](https://github.com/vllm-project/vllm/pull/54679) Fix DecodeBench DCP block selection
- [#54803](https://github.com/vllm-project/vllm/pull/54803) Apply adjust_dcp_kv_cache_interleave_size for NixlConnector only
- [#49274](https://github.com/vllm-project/vllm/pull/49274) Make isend_tensor_dict metadata send non-blocking
- [#54436](https://github.com/vllm-project/vllm/pull/54436) Never drop a decoding request from the PP sampled-token broadcast
- [#54962](https://github.com/vllm-project/vllm/pull/54962) Wait for prior PP tensor sends before the next forward
- [#55111](https://github.com/vllm-project/vllm/pull/55111) Account for PCP in multi-node world-size validation
- [#53190](https://github.com/vllm-project/vllm/pull/53190) Fall back when MADV_POPULATE_WRITE is unsupported
- [#54747](https://github.com/vllm-project/vllm/pull/54747) Handle padded routes in CUTLASS MoE permutations
- [#46009](https://github.com/vllm-project/vllm/pull/46009) Preserve unquantized weight storage on ROCm MoE
- [#54048](https://github.com/vllm-project/vllm/pull/54048) Enable cuBLAS out_dtype router GEMM on all CUDA archs
- [#54573](https://github.com/vllm-project/vllm/pull/54573) Fix FSE detection for Quark models
- [#47237](https://github.com/vllm-project/vllm/pull/47237) Fix INC quant method selection for non-quantized layers
- [#50005](https://github.com/vllm-project/vllm/pull/50005) Fix fused attention for DeepSeek-V3.2 / GLM-5.2 under DCP
- [#53574](https://github.com/vllm-project/vllm/pull/53574) Pass contiguous C128A decode topk indices on SM120
- [#54465](https://github.com/vllm-project/vllm/pull/54465) Fix BLHNC addressing for FlashInfer sparse MLA
- [#53821](https://github.com/vllm-project/vllm/pull/53821) Preserve AITER unified-attention metadata during graph replay
- [#53877](https://github.com/vllm-project/vllm/pull/53877) Keep packed GDN decode beta in FP32
- [#54859](https://github.com/vllm-project/vllm/pull/54859) Bump FlashKDA to fix unstable inverse
- [#54781](https://github.com/vllm-project/vllm/pull/54781) Fix an uninitialized local in the Kimi path
- [#54418](https://github.com/vllm-project/vllm/pull/54418) Keep default CUDA graph sizes memory-safe with spec decode
- [#54373](https://github.com/vllm-project/vllm/pull/54373) DFlash draft RoPE layout fix
- [#54044](https://github.com/vllm-project/vllm/pull/54044) Reset cached Mamba align metadata on profiling teardown
- [#54782](https://github.com/vllm-project/vllm/pull/54782) Raise for unavailable piecewise CUDA graphs
- [#54042](https://github.com/vllm-project/vllm/pull/54042) Several CPU bugfixes
- [#54632](https://github.com/vllm-project/vllm/pull/54632) Bound embedding densification before to_dense()
- [#54684](https://github.com/vllm-project/vllm/pull/54684) Bound the validation-error response body
- [#47562](https://github.com/vllm-project/vllm/pull/47562) Drop incomplete tool-call markup in non-streaming
- [#54838](https://github.com/vllm-project/vllm/pull/54838) Implicitly close DeepSeek DSML parameters
- [#54815](https://github.com/vllm-project/vllm/pull/54815) Fix RoPE for DeepSeek-V4 sparse SWA layers
- [#53281](https://github.com/vllm-project/vllm/pull/53281) Fix DeepSeek V4 adjacent user content rendering
- [#54854](https://github.com/vllm-project/vllm/pull/54854) Align DeepSeek V4 developer message handling
- [#53808](https://github.com/vllm-project/vllm/pull/53808) Honor modality-scoped mm_processor_kwargs
- [#54918](https://github.com/vllm-project/vllm/pull/54918) Scope cache hash kwargs by modality
- [#54994](https://github.com/vllm-project/vllm/pull/54994) Handle prefix-covered items in the SHM worker cache
- [#54633](https://github.com/vllm-project/vllm/pull/54633) Route MiniCPM-V video_embeds to the shared vision parser
- [#54501](https://github.com/vllm-project/vllm/pull/54501) Fix MiniCPM-o image processor reuse on Transformers v5
- [#53829](https://github.com/vllm-project/vllm/pull/53829) Fix CohereASR streaming audio-token estimate
- [#54364](https://github.com/vllm-project/vllm/pull/54364) Truncate pooling prompts before padding
- [#54407](https://github.com/vllm-project/vllm/pull/54407) plus [#54509](https://github.com/vllm-project/vllm/pull/54509), [#54539](https://github.com/vllm-project/vllm/pull/54539), [#54692](https://github.com/vllm-project/vllm/pull/54692): keep token offsets, token-id flags and assistant masks consistent with prompt truncation
- plus 12 more minor bugfixes (docs, profiler, renderer, tokenizer, ROCm WSL, benchmark queue time)

</details>

<details>
<summary>Refactors (5)</summary>

- [#52958](https://github.com/vllm-project/vllm/pull/52958) Adopt QuantKey in QuarkConfig and its methods
- [#54262](https://github.com/vllm-project/vllm/pull/54262) Fix mypy typing for M models
- [#54954](https://github.com/vllm-project/vllm/pull/54954) MoE kernels test cleanup
- [#52352](https://github.com/vllm-project/vllm/pull/52352) Shard H100 MoE refactor integration tests
- [#54760](https://github.com/vllm-project/vllm/pull/54760) Replace vocab embeddings in the Transformers backend's recursive_replace

</details>

<details>
<summary>Tests (10)</summary>

- [#53291](https://github.com/vllm-project/vllm/pull/53291) Speed up the quantization test group
- [#53279](https://github.com/vllm-project/vllm/pull/53279) ROCm misc ops and env tests
- [#55057](https://github.com/vllm-project/vllm/pull/55057) ROCm MiniMax reduce RMS kernel coverage
- [#53531](https://github.com/vllm-project/vllm/pull/53531) Batch-invariance tests for Qwen3-VL
- [#53529](https://github.com/vllm-project/vllm/pull/53529) Cover the compiled DeepStack input contract
- [#54893](https://github.com/vllm-project/vllm/pull/54893) MTP placeholder-token regression coverage
- [#54823](https://github.com/vllm-project/vllm/pull/54823) Remove MRV2-specific tests
- [#54991](https://github.com/vllm-project/vllm/pull/54991) Revert flaky test_quark_int8_w8a8_moe
- [#54403](https://github.com/vllm-project/vllm/pull/54403) Stabilize the ROCm sqrt-softplus top-k tie oracle
- plus 2 more minor test updates

</details>

<details>
<summary>CI & build (24)</summary>

- [#52851](https://github.com/vllm-project/vllm/pull/52851) Repository-local OTel tracing helpers
- [#54695](https://github.com/vllm-project/vllm/pull/54695) Calibrate AMD test timeouts from nightly runtimes
- [#54408](https://github.com/vllm-project/vllm/pull/54408) Avoid redundant image pulls in ROCm smoke validation
- [#54852](https://github.com/vllm-project/vllm/pull/54852) Add DSpark evals on ROCm
- [#54817](https://github.com/vllm-project/vllm/pull/54817) Kimi-K3-pruned75-DSpark-TP4 gsm8k eval
- [#53980](https://github.com/vllm-project/vllm/pull/53980) XPU entrypoints test in Intel GPU CI
- [#54751](https://github.com/vllm-project/vllm/pull/54751) Shard CPU jobs above the 24h P90 threshold
- [#54754](https://github.com/vllm-project/vllm/pull/54754) Shard long kernel test groups
- [#54752](https://github.com/vllm-project/vllm/pull/54752) Shard distributed model jobs
- [#52350](https://github.com/vllm-project/vllm/pull/52350) Shard LoRA TP distributed tests
- [#54420](https://github.com/vllm-project/vllm/pull/54420) MIG slice size in H200 job labels
- [#54326](https://github.com/vllm-project/vllm/pull/54326) Mark L4 GPU steps with device: l4
- [#54549](https://github.com/vllm-project/vllm/pull/54549) Mark 1-GPU L4 steps with device: l4
- [#54895](https://github.com/vllm-project/vllm/pull/54895) Use PR head label for the Buildkite branch
- [#50504](https://github.com/vllm-project/vllm/pull/50504) Fix the Ascend NPU test build image
- [#48750](https://github.com/vllm-project/vllm/pull/48750) Build the CPU image against torch nightly
- [#53905](https://github.com/vllm-project/vllm/pull/53905) Bump Transformers to 5.16.1
- [#54827](https://github.com/vllm-project/vllm/pull/54827) Gate PR title check on ready PRs
- [#54898](https://github.com/vllm-project/vllm/pull/54898) Prefetch safetensors weights in AMD CI
- [#54037](https://github.com/vllm-project/vllm/pull/54037) Expand ROCm weight-loading tests
- [#53437](https://github.com/vllm-project/vllm/pull/53437) Preserve diagnostics for unwritable AMD checkouts
- [#54750](https://github.com/vllm-project/vllm/pull/54750) Fix entrypoints coverage
- plus 2 more minor CI updates (auto-labeling, step keys)

</details>

<details>
<summary>Docs (3)</summary>

- [#55019](https://github.com/vllm-project/vllm/pull/55019) Add a Triton kernel-writing skill
- [#54995](https://github.com/vllm-project/vllm/pull/54995) Kernel benchmark sanity references
- plus 2 more minor doc fixes (griffe annotations and warnings)

</details>

<details>
<summary>Other (2)</summary>

- [#54620](https://github.com/vllm-project/vllm/pull/54620) omitted from the visible data (+50 merged PRs not shown)
- Newly opened work (not merged) includes the Qwen3.8 XPU port (`[#55068](https://github.com/vllm-project/vllm/pull/55068)`), GLM-5.3-Flash EPLB and indexer sharding (`[#55119](https://github.com/vllm-project/vllm/pull/55119)`, `[#54951](https://github.com/vllm-project/vllm/pull/54951)`), DSv4 batch-invariant RL kernels (`[#54955](https://github.com/vllm-project/vllm/pull/54955)`, DO NOT MERGE), snapshot lifecycle APIs (`[#54942](https://github.com/vllm-project/vllm/pull/54942)`, `[#54943](https://github.com/vllm-project/vllm/pull/54943)`, `[#54946](https://github.com/vllm-project/vllm/pull/54946)`), and a Triton sparse-MLA fallback for SM12x (`[#54929](https://github.com/vllm-project/vllm/pull/54929)`)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0c75bf13445a6c5ebb07b988888d112d2b6c2f9912dd11cc428c52cf6496e7eb -->
