# vllm: PR digest (2026-08-16 to 2026-08-20)

_195 merged, 360 newly opened - source vllm-project/vllm, generated 2026-08-20T09:43:42Z_

## TL;DR
- **DeepSeek** models dominated the window, receiving major performance upgrades including a new AMX-only high-performance MLA backend for CPUs and Triton sparse-MLA decode optimizations for AMD ROCm.
- **Attention & Kernels** saw heavy churn, notably consolidating context parallel attention ops and introducing FlashInfer ReplaySSM state caching for Mamba models.
- **MoE & Quantization** work included standardizing fused shared expert optimization selection and expanding support for W4A16 and FP8 formats across AMD and NVIDIA hardware.
- **Overall direction** points toward deep hardware-specific optimizations (AMX, ROCm gfx950, Intel XPU) and maturing speculative decoding and KV cache offloading infrastructure.

## Most important PRs
- **[#52616](https://github.com/vllm-project/vllm/pull/52616)** Adds an AMX-only high-performance Multi-Head Latent Attention (MLA) backend for DeepSeek V2/V3/R1 on CPUs, significantly boosting inference speed for these models on Intel hardware.
- **[#52212](https://github.com/vllm-project/vllm/pull/52212)** Optimizes Triton sparse-MLA decode performance for DeepSeek V4 on AMD ROCm (gfx950), improving throughput for sparse attention.
- **[#50174](https://github.com/vllm-project/vllm/pull/50174)** Introduces a new provider registry and orchestration infrastructure for JIT warmup, reducing startup overhead and standardizing warmup across different backends.
- **[#52839](https://github.com/vllm-project/vllm/pull/52839)** Consolidates context parallel attention operations, simplifying the FlashInfer backend integration and improving maintainability for distributed attention.
- **[#52962](https://github.com/vllm-project/vllm/pull/52962)** (In-progress) Adds support for quantized FlashInfer ReplaySSM state caching, which will improve memory efficiency and performance for Mamba-based models.

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#52737](https://github.com/vllm-project/vllm/pull/52737) Fuse DeepSeek-V4 mHC post/pre and RMSNorm with AITER
- [#51885](https://github.com/vllm-project/vllm/pull/51885) Reduce eager-mode reconfiguration downtime for Elastic EP
- [#52329](https://github.com/vllm-project/vllm/pull/52329) Cache logits-processing request state in ModelRunnerV2
- [#52573](https://github.com/vllm-project/vllm/pull/52573) Skip unused request-local reasoners in structured output
- [#53004](https://github.com/vllm-project/vllm/pull/53004) Speed up ROCm AITER QK norm RoPE KV cache fusion test
- [#51114](https://github.com/vllm-project/vllm/pull/51114) Optimize deepep_v2 receiver CPU overhead
- [#52084](https://github.com/vllm-project/vllm/pull/52084) Optimize sparse top-k metadata kernels for higher prefill throughput
- [#52458](https://github.com/vllm-project/vllm/pull/52458) Update FlashKDA for automatic K2 V-split
- [#52606](https://github.com/vllm-project/vllm/pull/52606) Kimi-K3 Fused kernels for KDA prefill
- [#52696](https://github.com/vllm-project/vllm/pull/52696) Use FP16 logits for sparse indexer in MLA
- [#52664](https://github.com/vllm-project/vllm/pull/52664) Integrate aiter indexer scoring and top-k kernels into MiniMax-M3 sparse attention path
- [#52789](https://github.com/vllm-project/vllm/pull/52789) Support internal prefill checkpoints for Mamba prefix caching
- [#52963](https://github.com/vllm-project/vllm/pull/52963) Optimize sparse GQA prefill attention for MiniMax-M3 on ROCm
- [#52882](https://github.com/vllm-project/vllm/pull/52882) Optimize DeepSeek V4 C4A top-k with AITER
- [#52556](https://github.com/vllm-project/vllm/pull/52556) Vectorize EPLB packing across MoE layers
- [#53027](https://github.com/vllm-project/vllm/pull/53027) Fuse GLM indexer attention projections
- [#52774](https://github.com/vllm-project/vllm/pull/52774) Backfill divergent local hybrid hits from the offloading connector
- [#52849](https://github.com/vllm-project/vllm/pull/52849) Enable AITER PA gluon decode for MiniMax-M3 MTP and dense layers
- [#52494](https://github.com/vllm-project/vllm/pull/52494) Fuse MLA q/kv RMSNorm in AMD Kimi-K3 MLA wrapper
- [#52983](https://github.com/vllm-project/vllm/pull/52983) W4A16 magic-bias dequant + scale hoist for gfx90a
- [#52619](https://github.com/vllm-project/vllm/pull/52619) Enable medium-skinny dispatch in RDNAHybridW4A16LinearKernel
- [#52875](https://github.com/vllm-project/vllm/pull/52875) Render plain completion stream deltas from a template

</details>

<details>
<summary>Kernels & attention (33)</summary>

- [#52368](https://github.com/vllm-project/vllm/pull/52368) Simplify B12X linear kernels and warmup
- [#52208](https://github.com/vllm-project/vllm/pull/52208) Add Aiter ops tests for ROCm
- [#52046](https://github.com/vllm-project/vllm/pull/52046) Add pcp support in dsv3.2 for NVIDIA
- [#48484](https://github.com/vllm-project/vllm/pull/48484) Replicated embedding and norm fusion for DSV3 flat model
- [#52861](https://github.com/vllm-project/vllm/pull/52861) Route DSA models to the CUDA non-compiled path
- [#46514](https://github.com/vllm-project/vllm/pull/46514) FlashMLA sparse: DCP on the fp8_ds_mla mixed-batch path + MTP
- [#49688](https://github.com/vllm-project/vllm/pull/49688) Enable C++ causal_conv1d GDN path and float32 SSM cache on non-AMX AVX-512BF16 CPUs
- [#52539](https://github.com/vllm-project/vllm/pull/52539) Support Qwen head ratios in fused GDN MTP
- [#52381](https://github.com/vllm-project/vllm/pull/52381) Harden DeepSeek V3.2 fused kernel grids
- [#52217](https://github.com/vllm-project/vllm/pull/52217) Vectorize sparse MLA mask loads
- [#52078](https://github.com/vllm-project/vllm/pull/52078) Avoid redundant mask compute in GDN metadata build
- [#52763](https://github.com/vllm-project/vllm/pull/52763) Attention test speedup for ROCm
- [#52566](https://github.com/vllm-project/vllm/pull/52566) Restore Torch defaults and type DSV4 scratch buffers for ROCm
- [#52775](https://github.com/vllm-project/vllm/pull/52775) SM120: stop routing misaligned-M blockwise FP8 GEMMs to the small-M swapAB config
- [#53060](https://github.com/vllm-project/vllm/pull/53060) Turboquant decode attention optimization
- [#52928](https://github.com/vllm-project/vllm/pull/52928) Add FlashInfer ReplaySSM support for MTP
- [#52955](https://github.com/vllm-project/vllm/pull/52955) Sm89 attention/kernels docs
- [#52506](https://github.com/vllm-project/vllm/pull/52506) Add FlashInfer ReplaySSM backend
- [#52863](https://github.com/vllm-project/vllm/pull/52863) Publish replicated KV updates through PyTorch symmetric memory
- [#52971](https://github.com/vllm-project/vllm/pull/52971) Export prefill checkpoints in a single FlashKDA pass for Kimi K3
- [#52760](https://github.com/vllm-project/vllm/pull/52760) Share HiSparse host cache across TP ranks
- [#53053](https://github.com/vllm-project/vllm/pull/53053) Extend GEMM-RS to GEMM-AR for Kimi-K3
- [#52980](https://github.com/vllm-project/vllm/pull/52980) SM100 Hdim 256 optimized
- [#52676](https://github.com/vllm-project/vllm/pull/52676) Enable fused QK-norm + partial MRoPE + gate for Qwen3.6
- [#52516](https://github.com/vllm-project/vllm/pull/52516) Fix Mooncake heterogeneous TP with replicated GQA heads
- [#52628](https://github.com/vllm-project/vllm/pull/52628) Enable fused AR draft metadata updates for DeepSeek V4
- [#52668](https://github.com/vllm-project/vllm/pull/52668) Add a bf16x3 router GEMM for fp32 gate weights on ROCm
- [#52582](https://github.com/vllm-project/vllm/pull/52582) Avoid overlapping stores in XPU KV cache kernel
- [#52905](https://github.com/vllm-project/vllm/pull/52905) Promote BF16 causal-conv operands before accumulation
- [#53036](https://github.com/vllm-project/vllm/pull/53036) Enable varlen Mamba2 decode for adaptive verification
- [#52828](https://github.com/vllm-project/vllm/pull/52828) Truncate all full-attention groups to the shared prefix-cache hit
- [#52611](https://github.com/vllm-project/vllm/pull/52611) Fix causal_conv1d Alignment Specialization Race Condition
- [#53014](https://github.com/vllm-project/vllm/pull/53014) Add Flashinfer cutedsl w4a16 linear

</details>

<details>
<summary>MoE & quantization (29)</summary>

- [#51695](https://github.com/vllm-project/vllm/pull/51695) Standardize and abstract fused shared expert optimization selection
- [#52502](https://github.com/vllm-project/vllm/pull/52502) Add GB10 fused-MoE fp8 tuning configs
- [#48918](https://github.com/vllm-project/vllm/pull/48918) Support Humming for WNA16 MoE
- [#52704](https://github.com/vllm-project/vllm/pull/52704) Fix OCP MX MoE emulation silently skipping mxfp6 activation QDQ
- [#51924](https://github.com/vllm-project/vllm/pull/51924) Refine FlashInfer one-sided All2All integration for MoE
- [#52182](https://github.com/vllm-project/vllm/pull/52182) Remove VLLM_TEST_FORCE_FP8_MARLIN to replace with linear_backend/moe_backend
- [#52550](https://github.com/vllm-project/vllm/pull/52550) Unify indexer cache dtype under attention_config.indexer_kv_dtype
- [#52647](https://github.com/vllm-project/vllm/pull/52647) Expand AITER W4A4 MoE Coverage for ROCm
- [#37835](https://github.com/vllm-project/vllm/pull/37835) Add UE8M0 scale packing for Triton silu_mul_quant
- [#51021](https://github.com/vllm-project/vllm/pull/51021) Gate Torch FP8 scaled-MM on architecture support for ROCm
- [#52603](https://github.com/vllm-project/vllm/pull/52603) Remove the dead ocp_mx_scheme branch from moe_kernel_quantize_input
- [#52002](https://github.com/vllm-project/vllm/pull/52002) Restore int8 grouped WNA16 MoE support in compressed-tensors
- [#52584](https://github.com/vllm-project/vllm/pull/52584) Support CUTLASS W4A8 MoE with DeepEP low latency
- [#52705](https://github.com/vllm-project/vllm/pull/52705) Integrate DeepGEMM NVFP4 MegaMoE with fused shared experts
- [#52985](https://github.com/vllm-project/vllm/pull/52985) Fused Triton W8A16 fp8 GEMM for gfx90a
- [#52974](https://github.com/vllm-project/vllm/pull/52974) Triton NVFP4 W4A16 GEMM for gfx90a
- [#52652](https://github.com/vllm-project/vllm/pull/52652) Tensor-descriptor path for fused_moe_kernel_gptq_awq (int4) on XPU
- [#52752](https://github.com/vllm-project/vllm/pull/52752) Add MI300X FP8 tuned configs for Qwen3.8-27B-FP8
- [#52958](https://github.com/vllm-project/vllm/pull/52958) Adopt QuantKey in QuarkConfig for weight and act quant keys
- [#53040](https://github.com/vllm-project/vllm/pull/53040) Fuse shared experts into MegaMoE for DSV4
- [#52799](https://github.com/vllm-project/vllm/pull/52799) Add Humming backend support to CT WNA16 MoE
- [#52798](https://github.com/vllm-project/vllm/pull/52798) Use canonical N-first weight format for CT WNA16 MoE
- [#52670](https://github.com/vllm-project/vllm/pull/52670) Pluggable KV Cache Data Types
- [#53065](https://github.com/vllm-project/vllm/pull/53065) Tune Triton fused MoE for Intel XPU
- [#52831](https://github.com/vllm-project/vllm/pull/52831) Support ROCm aiter fusion of per tensor quant + rmsnorm
- [#52781](https://github.com/vllm-project/vllm/pull/52781) DeepEP v2: async finalize to overlap shared experts with combine
- [#52813](https://github.com/vllm-project/vllm/pull/52813) Support ModelOpt layer-wise mixed KV cache
- [#52890](https://github.com/vllm-project/vllm/pull/52890) Restore CUDA support for 2-bit and 3-bit AutoRound formats
- [#53068](https://github.com/vllm-project/vllm/pull/53068) Implement Fp8Config shared-expert FSE compatibility check

</details>

<details>
<summary>Model support (13)</summary>

- [#52706](https://github.com/vllm-project/vllm/pull/52706) Add GraniteSWA and GraniteMoeSWA via existing Granite
- [#50156](https://github.com/vllm-project/vllm/pull/50156) Misc changes to cohere model definitions
- [#49788](https://github.com/vllm-project/vllm/pull/49788) Enable LoRA support for tower and connector in LlavaNextForConditionalGeneration
- [#53021](https://github.com/vllm-project/vllm/pull/53021) Remove unused DeepseekV32Indexer forward
- [#52948](https://github.com/vllm-project/vllm/pull/52948) Support bidirectional (encoder-only) attention for DeepSeek
- [#52425](https://github.com/vllm-project/vllm/pull/52425) Support Transformers pooling model
- [#52197](https://github.com/vllm-project/vllm/pull/52197) Support DSpark configs with architectures=DSparkDraftModel + model_type=qwen3
- [#52929](https://github.com/vllm-project/vllm/pull/52929) Add NemotronH_Omni_Reasoning_V3 as a supported Nemotron architecture
- [#52534](https://github.com/vllm-project/vllm/pull/52534) Add A100 (SM_80) deployment support for GLM-5.2
- [#52772](https://github.com/vllm-project/vllm/pull/52772) Add support for new Cohere Compass model
- [#52560](https://github.com/vllm-project/vllm/pull/52560) Add Qwen3-Omni DSpark support
- [#52749](https://github.com/vllm-project/vllm/pull/52749) Enable LoRA support for tower and connector in Llama Nemotron VL
- [#52754](https://github.com/vllm-project/vllm/pull/52754) Add --video-max-pixels-per-frame to make Qwen3-VL video cost duration-proportional

</details>

<details>
<summary>Parallelism & scheduling (27)</summary>

- [#52372](https://github.com/vllm-project/vllm/pull/52372) Reference GPU blocks for in-flight store jobs and key the store ledger by store_job_id
- [#52466](https://github.com/vllm-project/vllm/pull/52466) Add decode offloading to Mooncake Store consumers
- [#50493](https://github.com/vllm-project/vllm/pull/50493) Support DCP partial prefix cache hit for Kimi-K3
- [#52216](https://github.com/vllm-project/vllm/pull/52216) Promote prefix_cache_retention_interval to an argument and change the default to 0
- [#51875](https://github.com/vllm-project/vllm/pull/51875) Make prefix-cache NONE_HASH deterministic by default
- [#49532](https://github.com/vllm-project/vllm/pull/49532) Support EC connector KV Offloading on XPU
- [#52514](https://github.com/vllm-project/vllm/pull/52514) Add CuMemAllocator.discard() for tag-selective GPU memory release
- [#52697](https://github.com/vllm-project/vllm/pull/52697) Allow KV consumers to omit MM embeddings
- [#52998](https://github.com/vllm-project/vllm/pull/52998) Enable FlashInfer all-reduce by default
- [#52770](https://github.com/vllm-project/vllm/pull/52770) ECZmqConnector
- [#52615](https://github.com/vllm-project/vllm/pull/52615) Rename kv_offload block to chunk
- [#52856](https://github.com/vllm-project/vllm/pull/52856) Support FP8 block quant AsyncTP collective fusion on XPU
- [#53022](https://github.com/vllm-project/vllm/pull/53022) Add static expert maps for DeepSeek V4 EPLB
- [#52917](https://github.com/vllm-project/vllm/pull/52917) Adaptive spin grace + bounded arch waits for shm_broadcast
- [#52711](https://github.com/vllm-project/vllm/pull/52711) Mooncake DCP: Chunk-Derived Namespace for KV Cache Store
- [#52683](https://github.com/vllm-project/vllm/pull/52683) Support for W8A8-FP8 static GEMM collective fusion on XPU
- [#53067](https://github.com/vllm-project/vllm/pull/53067) Add scheduler context for lazy block access in KV Connector
- [#52641](https://github.com/vllm-project/vllm/pull/52641) Add contention-aware expert migration batching for EPLB
- [#52678](https://github.com/vllm-project/vllm/pull/52678) Pack disk backend slots into a single flat buffer for O_DIRECT alignment
- [#52859](https://github.com/vllm-project/vllm/pull/52859) Add lifecycle tracing for NIXL push and pull
- [#52497](https://github.com/vllm-project/vllm/pull/52497) Add rank-local IPC weight updates for RL
- [#52555](https://github.com/vllm-project/vllm/pull/52555) Opt-in custom all-reduce max size for same-node TP=2
- [#52655](https://github.com/vllm-project/vllm/pull/52655) Support token-range cache salt regions in block hashing
- [#52527](https://github.com/vllm-project/vllm/pull/52527) Report shared-prefix tokens lost to a missing sparse-retention checkpoint
- [#52731](https://github.com/vllm-project/vllm/pull/52731) Report KV load tier in cache events for MooncakeStore
- [#53007](https://github.com/vllm-project/vllm/pull/53007) Add option to select different backend for sliding window layers
- [#53078](https://github.com/vllm-project/vllm/pull/53078) Mooncake: heterogeneous-TP support for hybrid GDN/Mamba models

</details>

<details>
<summary>Speculative decoding (9)</summary>

- [#42963](https://github.com/vllm-project/vllm/pull/42963) Support prompt embeds in ModelRunnerV2
- [#52188](https://github.com/vllm-project/vllm/pull/52188) Support Kimi-K3 DCP with DSpark
- [#52559](https://github.com/vllm-project/vllm/pull/52559) Add graph-aware adaptive K for DFlash
- [#52816](https://github.com/vllm-project/vllm/pull/52816) DFlash2: local convolution + candidate selector
- [#52548](https://github.com/vllm-project/vllm/pull/52548) Honor positive dynamic K in autoregressive drafting
- [#52522](https://github.com/vllm-project/vllm/pull/52522) Batch-invariant support for speculative decoding
- [#52783](https://github.com/vllm-project/vllm/pull/52783) Enable adaptive DSpark on SM100 sparse MLA
- [#52782](https://github.com/vllm-project/vllm/pull/52782) Add NVTX/torch-profiler annotations to V2 model runner and DFlash speculator
- [#53052](https://github.com/vllm-project/vllm/pull/53052) Support EAGLE3 for Sarvam

</details>

<details>
<summary>API & serving (30)</summary>

- [#52131](https://github.com/vllm-project/vllm/pull/52131) Move api_server.py out openai folder
- [#52309](https://github.com/vllm-project/vllm/pull/52309) Consolidate entrypoint middleware
- [#52575](https://github.com/vllm-project/vllm/pull/52575) Simplify data-parallel size ownership in Rust Frontend
- [#52671](https://github.com/vllm-project/vllm/pull/52671) Wait for all utility calls to finish in Rust Frontend
- [#52281](https://github.com/vllm-project/vllm/pull/52281) Give EngineCore cleanup grace after request abort
- [#52031](https://github.com/vllm-project/vllm/pull/52031) Advertise LoRA capabilities in Rust Frontend gRPC
- [#48290](https://github.com/vllm-project/vllm/pull/48290) Enable MRV2 for pooling models by default
- [#52867](https://github.com/vllm-project/vllm/pull/52867) Use semantic task validation errors in Pooling
- [#52703](https://github.com/vllm-project/vllm/pull/52703) Add routed expert prompt offset in Rust Frontend RL
- [#52896](https://github.com/vllm-project/vllm/pull/52896) Add Anthropic Messages API request surface and count_tokens
- [#53054](https://github.com/vllm-project/vllm/pull/53054) Add HY3 unified parser and local XGrammar structural-tag builder
- [#52876](https://github.com/vllm-project/vllm/pull/52876) Add separate post-thinking sampling parameters
- [#52505](https://github.com/vllm-project/vllm/pull/52505) Write run-batch responses incrementally instead of at the end
- [#52658](https://github.com/vllm-project/vllm/pull/52658) Add Hunyuan A13B reasoning parser
- [#52841](https://github.com/vllm-project/vllm/pull/52841) Add ERNIE 4.5 tool and reasoning parsers
- [#52900](https://github.com/vllm-project/vllm/pull/52900) Add LFM2 tool parser
- [#52910](https://github.com/vllm-project/vllm/pull/52910) Attribute decoded text to tokens in Rust Frontend
- [#52579](https://github.com/vllm-project/vllm/pull/52579) Add Olmo3 tool parser
- [#52723](https://github.com/vllm-project/vllm/pull/52723) Expose routed expert traces over gRPC in Rust Frontend
- [#52677](https://github.com/vllm-project/vllm/pull/52677) Break repeating reasoning loops by forcing the reasoning end sequence
- [#52864](https://github.com/vllm-project/vllm/pull/52864) Add structured sleep responses and weight info tests
- [#52840](https://github.com/vllm-project/vllm/pull/52840) Add LoRA lifecycle control in Rust Frontend gRPC
- [#52739](https://github.com/vllm-project/vllm/pull/52739) Map unsupported reasoning_effort to nearest supported level
- [#53044](https://github.com/vllm-project/vllm/pull/53044) Support --generation-config vllm in Rust Frontend
- [#52721](https://github.com/vllm-project/vllm/pull/52721) Decode routed expert EngineCore output in Rust Frontend
- [#52699](https://github.com/vllm-project/vllm/pull/52699) Add Gate/Prove ActionBoundary guardrail and Action Ledger exporter
- [#52946](https://github.com/vllm-project/vllm/pull/52946) Add Step3p5 tool parser
- [#52574](https://github.com/vllm-project/vllm/pull/52574) Add MiniMax M2 append-think reasoning parser
- [#52886](https://github.com/vllm-project/vllm/pull/52886) Recover incomplete Kimi K3 calls at outer boundaries in Rust Frontend
- [#52629](https://github.com/vllm-project/vllm/pull/52629) Add a prefix-caching x tool-calling gate

</details>

<details>
<summary>Multimodal (9)</summary>

- [#49155](https://github.com/vllm-project/vllm/pull/49155) Reorganize video decoder backends
- [#53064](https://github.com/vllm-project/vllm/pull/53064) Remove InputPreprocessor
- [#52827](https://github.com/vllm-project/vllm/pull/52827) Keep more metadata tensors on CPU
- [#52041](https://github.com/vllm-project/vllm/pull/52041) Skip broadcasting mm tensor data to workers for prefix-cache-covered items
- [#50400](https://github.com/vllm-project/vllm/pull/50400) Fused vision q/k roper kernel for Kimi
- [#52722](https://github.com/vllm-project/vllm/pull/52722) Accept preprocessed multimodal gRPC features in Rust Frontend
- [#52925](https://github.com/vllm-project/vllm/pull/52925) Skip redundant placeholder scan when token match succeeds
- [#52598](https://github.com/vllm-project/vllm/pull/52598) Add torchaudio backend to AudioResampler
- [#52769](https://github.com/vllm-project/vllm/pull/52769) Support torch.compile for SigLIP embeddings

</details>

<details>
<summary>Bugfixes (128)</summary>

- [#51459](https://github.com/vllm-project/vllm/pull/51459) Fix and extend PR/issue auto-labeling
- [#50729](https://github.com/vllm-project/vllm/pull/50729) Fix overlapping state copy race in Mamba
- [#51824](https://github.com/vllm-project/vllm/pull/51824) Fix vLLM crash at startup when DeepEP v2 is used with --enforce-eager with TRTLLM Bf16
- [#51863](https://github.com/vllm-project/vllm/pull/51863) Check readiness before tokenizer init in rust vllm-bench
- [#52126](https://github.com/vllm-project/vllm/pull/52126) Prevent PyNvVideoCodec decoder slot limit bypass via ClassVar shadowing
- [#51823](https://github.com/vllm-project/vllm/pull/51823) Validate BGE-M3 combined task ownership
- [#52401](https://github.com/vllm-project/vllm/pull/52401) Pick the DeepSeek V4 eager cudagraph region per model runner
- [#51481](https://github.com/vllm-project/vllm/pull/51481) Don't assume the engines started when forwarding a wake
- [#52608](https://github.com/vllm-project/vllm/pull/52608) Release the shared ColBERT engine before test_colbert_hf_comparison
- [#52394](https://github.com/vllm-project/vllm/pull/52394) Raise VLLMValidationError from structured output validators
- [#45807](https://github.com/vllm-project/vllm/pull/45807) Report stop_sequence stop_reason in Anthropic Messages API
- [#52622](https://github.com/vllm-project/vllm/pull/52622) Return 4xx for client-caused errors in /detokenize
- [#47272](https://github.com/vllm-project/vllm/pull/47272) Reserve the KV null block when validating max_model_len
- [#52246](https://github.com/vllm-project/vllm/pull/52246) Return 4xx for client-caused errors in /v1/messages
- [#48608](https://github.com/vllm-project/vllm/pull/48608) Video loading: sample over presentable frames, not header sample count
- [#52419](https://github.com/vllm-project/vllm/pull/52419) Keep EAGLE cache registration on the partial-hash-hit path
- [#51426](https://github.com/vllm-project/vllm/pull/51426) Fix GLM-5.2 chat template rendering parity in Rust Frontend
- [#52491](https://github.com/vllm-project/vllm/pull/52491) Fix encoder round-robin fan-out
- [#52311](https://github.com/vllm-project/vllm/pull/52311) Fix off-by-one in bad_words draft-prefix matching
- [#52436](https://github.com/vllm-project/vllm/pull/52436) DSpark: fix the grammar bitmask mapping when the draft budget is zero
- [#51852](https://github.com/vllm-project/vllm/pull/51852) Take an attention group's query head count from its layers
- [#48109](https://github.com/vllm-project/vllm/pull/48109) Fix Mamba state pointer overflow on XPU
- [#52528](https://github.com/vllm-project/vllm/pull/52528) Guard remaining before-validators against non-object JSON bodies
- [#53017](https://github.com/vllm-project/vllm/pull/53017) Fix draft logits cache column stride in gumbel_sample
- [#52844](https://github.com/vllm-project/vllm/pull/52844) Reject n > 1 in the /inference/v1/generate route
- [#52112](https://github.com/vllm-project/vllm/pull/52112) Fix a few int4/int8 quantization errors on ROCm
- [#52626](https://github.com/vllm-project/vllm/pull/52626) Fix DeepSeek V4 mHC broadcast buffer for weight sync
- [#52805](https://github.com/vllm-project/vllm/pull/52805) Stop XGrammar token batches at termination
- [#48998](https://github.com/vllm-project/vllm/pull/48998) Fix Triton W4A16 bug in determining if transpose is required for GPTQ/AutoGPTQ
- [#52523](https://github.com/vllm-project/vllm/pull/52523) Redact api_key in startup logs and compile cache factors
- [#52966](https://github.com/vllm-project/vllm/pull/52966) Support CT block FP8 with Marlin
- [#51368](https://github.com/vllm-project/vllm/pull/51368) Fix DeepSeek V4 mHC broadcast buffer for dummy load
- [#52385](https://github.com/vllm-project/vllm/pull/52385) Account for local DP workers in startup thread allocation
- [#51632](https://github.com/vllm-project/vllm/pull/51632) Fix Triton fused shared expert alignment on ROCm
- [#52825](https://github.com/vllm-project/vllm/pull/52825) Run the serve arg checks for vllm launch too
- [#52430](https://github.com/vllm-project/vllm/pull/52430) Align parser enable_thinking default with template for Gemma4
- [#50809](https://github.com/vllm-project/vllm/pull/50809) Sync mamba_block_size via EngineCoreReadyResponse
- [#52690](https://github.com/vllm-project/vllm/pull/52690) Restore model info caching for package backends
- [#46175](https://github.com/vllm-project/vllm/pull/46175) Accept logprobs=-1 in the Completion API
- [#47640](https://github.com/vllm-project/vllm/pull/47640) Guard None group members in expand_packed_lora
- [#53071](https://github.com/vllm-project/vllm/pull/53071) Return HTTP 400 instead of 501 for unknown chat roles in DeepSeek encoders
- [#52050](https://github.com/vllm-project/vllm/pull/52050) Temporarily disable FA4 head-dim 256
- [#52399](https://github.com/vllm-project/vllm/pull/52399) Return all choices from /inference/v1/generate when n > 1
- [#52512](https://github.com/vllm-project/vllm/pull/52512) Do not use Dense MHA for GLM-5.2
- [#52482](https://github.com/vllm-project/vllm/pull/52482) Ignore stale same-step encoder cache evictions
- [#49996](https://github.com/vllm-project/vllm/pull/49996) Reject string schemas that mix pattern/format with length bounds
- [#52702](https://github.com/vllm-project/vllm/pull/52702) Reject scale below the minimum data parallel size
- [#52730](https://github.com/vllm-project/vllm/pull/52730) Fix hf runner on XPU
- [#52632](https://github.com/vllm-project/vllm/pull/52632) DeepEP-V2: expert_tokens_meta must be None on the decode/cudagraph path
- [#52648](https://github.com/vllm-project/vllm/pull/52648) Guard the MXFP8 FlashInfer path on FlashInfer availability
- [#52952](https://github.com/vllm-project/vllm/pull/52952) Guard _load_ov2_processor with resolve_trust_remote_code
- [#50082](https://github.com/vllm-project/vllm/pull/50082) Add Kimi K3 MoE support to benchmark_moe.py
- [#52174](https://github.com/vllm-project/vllm/pull/52174) Add forward_xpu to XDRotaryEmbedding for HunyuanOCR on XPU
- [#52441](https://github.com/vllm-project/vllm/pull/52441) Keep Gemma 4 video frame counts on CPU
- [#51395](https://github.com/vllm-project/vllm/pull/51395) Disable dense prefill for FlashInfer sparse MLA
- [#52160](https://github.com/vllm-project/vllm/pull/52160) Fix group numbering in Case 3 of hybrid_kv_cache_manager.md
- [#52981](https://github.com/vllm-project/vllm/pull/52981) Fix CPU platform pre-commit formatting
- [#52356](https://github.com/vllm-project/vllm/pull/52356) Skip FP8 MLA prefill PS-metadata build for chunked-context batches
- [#51585](https://github.com/vllm-project/vllm/pull/51585) Preserve CPU query offsets during capture
- [#52939](https://github.com/vllm-project/vllm/pull/52939) Update distributed DP API server test path
- [#53026](https://github.com/vllm-project/vllm/pull/53026) Fix nonexistent dependency for data-parallel example test selection
- [#52492](https://github.com/vllm-project/vllm/pull/52492) Keep indexer scoring in breakable graphs
- [#52842](https://github.com/vllm-project/vllm/pull/52842) Complete DeepSeek-V4 FSE test fixture contract
- [#48850](https://github.com/vllm-project/vllm/pull/48850) Add embedding_modules for Qwen3.5 CausalLM
- [#52588](https://github.com/vllm-project/vllm/pull/52588) Fix incorrect --custom-skip-chat-template flag reference
- [#52552](https://github.com/vllm-project/vllm/pull/52552) Fix lora_base_layer / routed_experts order in expert param mapping
- [#52812](https://github.com/vllm-project/vllm/pull/52812) Rename kv_offload_tiering_block_{queries,hits} to chunk
- [#52578](https://github.com/vllm-project/vllm/pull/52578) Fix accident pre-commit breakage due to concurrent merge
- [#52692](https://github.com/vllm-project/vllm/pull/52692) Remove stale image embedding scaling for PaliGemma
- [#52161](https://github.com/vllm-project/vllm/pull/52161) Detect all attention-spelling variants in ModelConfig.is_hybrid
- [#52044](https://github.com/vllm-project/vllm/pull/52044) Handle DeepseekV4ForCausalLM in benchmark_moe get_model_params
- [#53075](https://github.com/vllm-project/vllm/pull/53075) Add asyncio-based multi_turn benchmark v2 to fix deadlock
- [#52642](https://github.com/vllm-project/vllm/pull/52642) Fix apply_vllm_mapper crash on dict-valued Quark algo_config
- [#52883](https://github.com/vllm-project/vllm/pull/52883) DFlash2: accept unquantized linear LM heads in the candidate selector
- [#52755](https://github.com/vllm-project/vllm/pull/52755) Fix silently dropping Mooncake/NIXL KV-connector telemetry
- [#52865](https://github.com/vllm-project/vllm/pull/52865) Fix DeepSeek V4 and V3.2 tool argument streaming
- [#52645](https://github.com/vllm-project/vllm/pull/52645) Recover DeepSeek V4 tool calls with malformed DSML wrappers
- [#52921](https://github.com/vllm-project/vllm/pull/52921) Align CPU offload pool size across PP/spec-decode workers
- [#52941](https://github.com/vllm-project/vllm/pull/52941) Fix DeepSeek V4 mHC TileLang warmup for nvidia
- [#52838](https://github.com/vllm-project/vllm/pull/52838) Fix GPU-CPU KV transfer fault in OffloadingConnector
- [#52530](https://github.com/vllm-project/vllm/pull/52530) Fail requests the KV cache pool can never hold instead of retrying them forever
- [#52717](https://github.com/vllm-project/vllm/pull/52717) Keep pipelined streaming continuations off the waiting queue
- [#52604](https://github.com/vllm-project/vllm/pull/52604) Own prepared B12x W4A16 weights
- [#52621](https://github.com/vllm-project/vllm/pull/52621) Honor stop strings in beam search
- [#52495](https://github.com/vllm-project/vllm/pull/52495) Count SWA in-flight KV once per pool, not per request
- [#52832](https://github.com/vllm-project/vllm/pull/52832) Offload producer partial tails on request finish
- [#52915](https://github.com/vllm-project/vllm/pull/52915) Pad sub-block FP8 tensor-parallel shards
- [#52734](https://github.com/vllm-project/vllm/pull/52734) Enable Qwen3.8-27B LM-only mode without vision tower
- [#53000](https://github.com/vllm-project/vllm/pull/53000) Fix multicast mailbox publication
- [#52771](https://github.com/vllm-project/vllm/pull/52771) OffloadingConnector: stop zeroing offload hits under MTP/EAGLE spec decode
- [#52780](https://github.com/vllm-project/vllm/pull/52780) Fall back from monolithic NVFP4 for simulated routing
- [#52478](https://github.com/vllm-project/vllm/pull/52478) Fix intermittent GPU memory fault during sleep-mode wake-up
- [#52651](https://github.com/vllm-project/vllm/pull/52651) Fix GPTQ MoE loading under moe_wna16 on XPU
- [#52920](https://github.com/vllm-project/vllm/pull/52920) Skip NIXL/UCX on x86 CPUs without AVX instead of crashing
- [#52643](https://github.com/vllm-project/vllm/pull/52643) Encode special tokens found in text for MistralCommonBackend in multimodal processors
- [#52804](https://github.com/vllm-project/vllm/pull/52804) Cache Hit Rate with KIMI + RHAI Dspark
- [#53087](https://github.com/vllm-project/vllm/pull/53087) Bound primary HIT_PENDING waits in KV Offload
- [#52942](https://github.com/vllm-project/vllm/pull/52942) Fix stale mamba/GDN states with ngram spec decode on hybrid
- [#53006](https://github.com/vllm-project/vllm/pull/53006) Fix response_format strict=false for Chat Completions and Responses API
- [#52893](https://github.com/vllm-project/vllm/pull/52893) Skip MiniMax-M3 AITER sparse PA under spec decode
- [#53074](https://github.com/vllm-project/vllm/pull/53074) Isolate hidden-state cache from DeepSeek-V4 MLA groups
- [#52978](https://github.com/vllm-project/vllm/pull/52978) Hoist trailing Anthropic system messages
- [#52766](https://github.com/vllm-project/vllm/pull/52766) Fix Transformers modelling backend RMSNormFuser.fuse performance
- [#52545](https://github.com/vllm-project/vllm/pull/52545) Fail closed when selected precompiled CUDA variant is unavailable
- [#52914](https://github.com/vllm-project/vllm/pull/52914) Synchronize the device on pause completion
- [#52487](https://github.com/vllm-project/vllm/pull/52487) Reload speculative draft weights after Level 2 sleep wake
- [#52596](https://github.com/vllm-project/vllm/pull/52596) Unlink /dev/shm region after all workers map it
- [#53058](https://github.com/vllm-project/vllm/pull/53058) Anthropic API: honor the thinking request parameter
- [#52750](https://github.com/vllm-project/vllm/pull/52750) Emit CUDA Graph metrics in GPU Model Runner V2
- [#52932](https://github.com/vllm-project/vllm/pull/52932) Reorder packed patches from block-major to raster before the vision tower
- [#52698](https://github.com/vllm-project/vllm/pull/52698) Gate async-scheduling output-token-id repair on a declared logitsproc capability
- [#52720](https://github.com/vllm-project/vllm/pull/52720) Support MistralCommonBackend tokenizers in the xgrammar structured-output backend
- [#52874](https://github.com/vllm-project/vllm/pull/52874) Mistral3: derive placeholder grid from processed pixel_values
- [#53080](https://github.com/vllm-project/vllm/pull/53080) Separate target and draft scheduling budgets
- [#52709](https://github.com/vllm-project/vllm/pull/52709) Zero packed KV blocks once from the backing sorage base
- [#52765](https://github.com/vllm-project/vllm/pull/52765) Fix async scheduling stale output and dual-scheduling race in resumable streaming sessions
- [#53059](https://github.com/vllm-project/vllm/pull/53059) Reject shape-aliased prefills in uniform-decode classification
- [#53038](https://github.com/vllm-project/vllm/pull/53038) Fix int32 overflow in LoRA Triton kernel pointer arithmetic
- [#52862](https://github.com/vllm-project/vllm/pull/52862) Defer Inductor compile-time autotuning to avoid fatal profile_run abort
- [#52529](https://github.com/vllm-project/vllm/pull/52529) Only echo the assistant turn in batched chat completions
- [#52779](https://github.com/vllm-project/vllm/pull/52779) Support PCP producers in NIXL KV Connector
- [#53023](https://github.com/vllm-project/vllm/pull/53023) Fix MultiConnector accuracy test lifecycle
- [#52759](https://github.com/vllm-project/vllm/pull/52759) Surface TorchCodec video decode failures as client errors
- [#53002](https://github.com/vllm-project/vllm/pull/53002) Use group geometry for FlashAttention metadata
- [#52571](https://github.com/vllm-project/vllm/pull/52571) Preserve aborted loads until abort completion
- [#52649](https://github.com/vllm-project/vllm/pull/52649) Skip quantizing undeclared Quark MTP layers
- [#52936](https://github.com/vllm-project/vllm/pull/52936) Ignore stale per-engine coordinator stats
- [#53078](https://github.com/vllm-project/vllm/pull/53078) Mooncake: heterogeneous-TP support for hybrid GDN/Mamba models

</details>

<details>
<summary>CI & build (34)</summary>

- [#52570](https://github.com/vllm-project/vllm/pull/52570) Reduce more duplicate runner startup in tests
- [#52976](https://github.com/vllm-project/vllm/pull/52976) Standardize AMD test job labels by device
- [#52264](https://github.com/vllm-project/vllm/pull/52264) Improve Kubernetes failure diagnostics for AMD
- [#52659](https://github.com/vllm-project/vllm/pull/52659) Standardize test job labels by device
- [#52822](https://github.com/vllm-project/vllm/pull/52822) Add AMD CI Pull-Request Commands
- [#51592](https://github.com/vllm-project/vllm/pull/51592) Align speed-bench CLI flags with Python and add flag parity test
- [#41100](https://github.com/vllm-project/vllm/pull/41100) Extended Fused MoE and FP8 MoE test support for ROCm
- [#52672](https://github.com/vllm-project/vllm/pull/52672) Upgrade requirements/test/xpu.txt
- [#40938](https://github.com/vllm-project/vllm/pull/40938) Move ROCm AITER quantization tests
- [#49514](https://github.com/vllm-project/vllm/pull/49514) Use the same-build wheel in Python-only CI
- [#44969](https://github.com/vllm-project/vllm/pull/44969) Gating more ROCm tests
- [#52593](https://github.com/vllm-project/vllm/pull/52593) Propagate vLLM version to Rust binaries
- [#52417](https://github.com/vllm-project/vllm/pull/52417) Avoid duplicate runner startup for multimodal test
- [#52256](https://github.com/vllm-project/vllm/pull/52256) Enable ViT CUDA graph tests on AMD gfx950 GPUs
- [#51208](https://github.com/vllm-project/vllm/pull/51208) Add LMCache kv-connector installation and runtime packages to docker image
- [#52810](https://github.com/vllm-project/vllm/pull/52810) Prevent Git maintenance races during shallow fetches
- [#52293](https://github.com/vllm-project/vllm/pull/52293) Enable fused KDA decode on gfx942 (MI325X)
- [#52325](https://github.com/vllm-project/vllm/pull/52325) Shard Humming A100 eval
- [#52797](https://github.com/vllm-project/vllm/pull/52797) Upgrade huggingface-hub to 1.28.0
- [#52633](https://github.com/vllm-project/vllm/pull/52633) Register CPU CI "VLLM_CPU_CI_ENV" environment variable
- [#52681](https://github.com/vllm-project/vllm/pull/52681) Upgrade Flashinfer version to 0.6.17
- [#52569](https://github.com/vllm-project/vllm/pull/52569) Update xpu-manager to v2.1.0
- [#44284](https://github.com/vllm-project/vllm/pull/44284) Relax CuPy constraint to only exclude 14.1.0
- [#52801](https://github.com/vllm-project/vllm/pull/52801) Add InstantTensor to CUDA dependencies
- [#52819](https://github.com/vllm-project/vllm/pull/52819) Bump triton 3.7 commit for ROCm
- [#52904](https://github.com/vllm-project/vllm/pull/52904) Downgrade sentencepiece on XPU
- [#52851](https://github.com/vllm-project/vllm/pull/52851) Add repository-local OTel tracing helpers
- [#52635](https://github.com/vllm-project/vllm/pull/52635) Start migrating the CPU extension to the libtorch stable ABI
- [#52790](https://github.com/vllm-project/vllm/pull/52790) Bump the minor-update group across 1 directory with 175 updates
- [#52572](https://github.com/vllm-project/vllm/pull/52572) Replace shellcheck script with shellcheck-py hook
- [#52547](https://github.com/vllm-project/vllm/pull/52547) Bound native and single-node test teardown for AMD
- [#52892](https://github.com/vllm-project/vllm/pull/52892) Replace external protoc with pure Rust lib protox
- [#52748](https://github.com/vllm-project/vllm/pull/52748) Amd cpu ci minimal reuse
- [#52650](https://github.com/vllm-project/vllm/pull/52650) Add mooncake build to rocm base image

</details>

<details>
<summary>Tests (11)</summary>

- [#52144](https://github.com/vllm-project/vllm/pull/52144) Add pause/resume E2E tests
- [#51968](https://github.com/vllm-project/vllm/pull/51968) Make tests device-agnostic on XPU
- [#51647](https://github.com/vllm-project/vllm/pull/51647) Pad non-aligned AITER MLA heads
- [#52313](https://github.com/vllm-project/vllm/pull/52313) Avoid false target matches for unsupported module types
- [#48628](https://github.com/vllm-project/vllm/pull/48628) Increase the coverage of prefill DBO in test_dbo.py
- [#46434](https://github.com/vllm-project/vllm/pull/46434) Enable modular OAI Triton MoE tests
- [#53035](https://github.com/vllm-project/vllm/pull/53035) Skip test_fused_shared_expert.py on XPU
- [#52565](https://github.com/vllm-project/vllm/pull/52565) Avoid forcing FlashAttention in the ColPali pooling test
- [#52496](https://github.com/vllm-project/vllm/pull/52496) Fit small KV-offload evals within shared memory
- [#52902](https://github.com/vllm-project/vllm/pull/52902) Router tests
- [#52764](https://github.com/vllm-project/vllm/pull/52764) Overlap renderer warmup and engine core initialization

</details>

<details>
<summary>Docs (7)</summary>

- [#52303](https://github.com/vllm-project/vllm/pull/52303) Update installation documentation for ROCm
- [#52937](https://github.com/vllm-project/vllm/pull/52937) Fix docs build
- [#50492](https://github.com/vllm-project/vllm/pull/50492) Add MatrixHub as a model loading source
- [#52726](https://github.com/vllm-project/vllm/pull/52726) Update Gaudi HPU committers
- [#53045](https://github.com/vllm-project/vllm/pull/53045) Weight reload and streaming quantization units
- [#53082](https://github.com/vllm-project/vllm/pull/53082) Make sleep a pure memory-state transition
- [#52967](https://github.com/vllm-project/vllm/pull/52967) Add NIXL connector metrics aggregation documentation

</details>

<details>
<summary>Refactors (3)</summary>

- [#52221](https://github.com/vllm-project/vllm/pull/52221) Remove dead code for quantization
- [#52821](https://github.com/vllm-project/vllm/pull/52821) Remove dead code quantization 2
- [#52282](https://github.com/vllm-project/vllm/pull/52282) Harden RemoteVLLMServer GPU cleanup checks

</details>

<details>
<summary>Other (7)</summary>

- [#52836](https://github.com/vllm-project/vllm/pull/52836) Revert DSv4 eager workspace reuse
- [#52987](https://github.com/vllm-project/vllm/pull/52987) Revert "[Kernel] Gemma-4 FA4 FP8 Kernel"
- [#51318](https://github.com/vllm-project/vllm/pull/51318) Revert adaptive C128A metadata packing
- [#52881](https://github.com/vllm-project/vllm/pull/52881) Revert incorrect MM keep_on_cpu=True changes
- [#51781](https://github.com/vllm-project/vllm/pull/51781) Fill in the missing backend parameter for torch.compile
- [#52625](https://github.com/vllm-project/vllm/pull/52625) Guard on_gfx1250 call with rocm platform
- [#52908](https://github.com/vllm-project/vllm/pull/52908) Restore test-only FP8 Marlin selection

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 15d3243b4499f5298a9863a57d86b87c282b09042d181291fb290e041601862d -->
