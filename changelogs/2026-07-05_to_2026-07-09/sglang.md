# sglang: PR digest (2026-07-05 to 2026-07-09)

_187 merged, 270 newly opened - source sgl-project/sglang, generated 2026-07-09T12:17:48Z_

## TL;DR
- **Model Focus**: DeepSeek dominated attention (40 PRs), with significant work on DeepSeek-V4 (DSA indexer optimizations, MTP support) and DeepSeek-V3.2. GLM-5.2 also saw major updates including DSA Cache Layer Split under Prefill Context Parallelism.
- **Performance & Kernels**: Major kernel additions include InfLLM v2 attention kernels, Cute-DSL FP8 MQA logits, and a faster DeepSeek-V4 DSA indexer. FP4 quantization is undergoing a massive refactor to remove deprecated JIT kernels.
- **Speculative Decoding**: Speculative decoding received major upgrades, including merged support for CPU and a massive newly-opened PR introducing DSpark (confidence-scheduled speculative decoding).
- **Architecture & Diffusion**: Breakable CUDA graphs (BCG) were enabled for diffusion DiTs, and new support is in progress for Pi0.5 and MiniCPM-SALA.
- **Refactoring**: A massive full-stack config resolution pipeline refactor is underway, retiring legacy accessors and process singletons to streamline the codebase.

## Most important PRs
- **[#30261](https://github.com/sgl-project/sglang/pull/30261)** introduces DSpark, a confidence-scheduled speculative decoding framework. This massive newly-opened architectural addition aims to improve speculative decoding efficiency across AMD and NVIDIA hardware.
- **[#29383](https://github.com/sgl-project/sglang/pull/29383)** merges InfLLM v2 attention kernels into the core attention backend. This expands the core attention capabilities for NVIDIA GPUs.
- **[#26788](https://github.com/sgl-project/sglang/pull/26788)** optimizes the DeepSeek-V4 DSA indexer with a faster top-k and page-table transform for runtime k <= 2048. This significantly improves prefill performance for DeepSeek models using Torch Compile.
- **[#27862](https://github.com/sgl-project/sglang/pull/27862)** adds speculative decoding support for CPU targets. This broadens the hardware applicability of speculative decoding beyond GPUs, utilizing Triton and Intel XPU optimizations.
- **[#27436](https://github.com/sgl-project/sglang/pull/27436)** enables breakable CUDA graphs (BCG) for diffusion DiTs. This allows dynamic batching and varying sequence lengths in diffusion models without recompiling the entire CUDA graph, improving multimodal throughput.

## More changes by area

<details>
<summary>Performance (13)</summary>

- [#27988](https://github.com/sgl-project/sglang/pull/27988) [Experimental] Full Cuda Graph Support for Prefill
- [#27926](https://github.com/sgl-project/sglang/pull/27926) [DSV4] perf: Make FP8 quant output tensor contiguous
- [#30449](https://github.com/sgl-project/sglang/pull/30449) Cherry-pick [#27926](https://github.com/sgl-project/sglang/pull/27926)
- [#30086](https://github.com/sgl-project/sglang/pull/30086) [diffusion] perf: tp-shard every text/image encoder across the full DiT replica
- [#30503](https://github.com/sgl-project/sglang/pull/30503) [Perf][CP]: optimize glm5.2 prefill performance using comm-comp overlap triton kernels
- [#30388](https://github.com/sgl-project/sglang/pull/30388) [EAGLE] perf: Fuse draft topk1, vocab embedding, and capture staging
- [#30266](https://github.com/sgl-project/sglang/pull/30266) [HiSparse][1/n] Add Dynamic HiSparse Residency to Preserve Small-Batch Decode Performance
- [#30511](https://github.com/sgl-project/sglang/pull/30511) [HiCache] Merge HiCache event checks to reduce decode overhead
- [#30337](https://github.com/sgl-project/sglang/pull/30337) fuse fragment ops to reduce host-bubble
- [#30226](https://github.com/sgl-project/sglang/pull/30226) Reduce top-level sglang import overhead
- [#30603](https://github.com/sgl-project/sglang/pull/30603) feat: batch-invariant deterministic inference for DeepSeek MoE on FA4 + DeepGEMM + DeepEP
- [#30580](https://github.com/sgl-project/sglang/pull/30580) Lazy load TileLang MHC kernels
- [#30404](https://github.com/sgl-project/sglang/pull/30404) [perf] Vectorize text-only extend mrope position computation
- [#30179](https://github.com/sgl-project/sglang/pull/30179) benchmark: add MI300X speed benchmarks for Qwen3.5-4B cookbook

</details>

<details>
<summary>Kernels & attention (25)</summary>

- [#25220](https://github.com/sgl-project/sglang/pull/25220) Cute-DSL FP8 MQA logits
- [#30117](https://github.com/sgl-project/sglang/pull/30117) Support Cutedsl BF16 GEMM JIT kernel
- [#30274](https://github.com/sgl-project/sglang/pull/30274) [DSA] Fold page-table into fused top-k v2
- [#29755](https://github.com/sgl-project/sglang/pull/29755) [Diffusion] cache cross-attn K/V across denoise steps for Helios
- [#30378](https://github.com/sgl-project/sglang/pull/30378) [DSA] Re-enable fused top-k v2 for MTP: clamp padded-row seq_lens to >= 0
- [#30427](https://github.com/sgl-project/sglang/pull/30427) Cherry-pick [#30378](https://github.com/sgl-project/sglang/pull/30378)
- [#29699](https://github.com/sgl-project/sglang/pull/29699) When attention TP for linear and full attention, use Flashinfer allreduce fusion
- [#30140](https://github.com/sgl-project/sglang/pull/30140) [DeepSeek-V4] Enable non-paged indexer by default for large prefill chunks
- [#30436](https://github.com/sgl-project/sglang/pull/30436) Cherry-pick [#30140](https://github.com/sgl-project/sglang/pull/30140)
- [#28658](https://github.com/sgl-project/sglang/pull/28658) [AMD] Fuse shared-expert sigmoid + bf16->fp32 cast into the MoE append kernel
- [#30302](https://github.com/sgl-project/sglang/pull/30302) [AMD] [MORI-EP] Skip LocalExpertCount kernel in decode graph when not recording
- [#29729](https://github.com/sgl-project/sglang/pull/29729) Add opt-in SGLANG_ROPE_CACHE_FP32 to keep RoPE cache in fp32 on non-CUDA
- [#30280](https://github.com/sgl-project/sglang/pull/30280) Delete sgl-kernel AOT router GEMM and fused A GEMM
- [#30247](https://github.com/sgl-project/sglang/pull/30247) Optimize LongCat-Flash router GEMM with an in-tree SM90 bf16xfp32 JIT kernel
- [#30514](https://github.com/sgl-project/sglang/pull/30514) [DSA] Integrate Q8KV8 FP8 Sparse MLA Prefill into the DSA Backend
- [#30546](https://github.com/sgl-project/sglang/pull/30546) [DSA] Opt-in MXFP4 index-K cache for GLM-5.x / DeepSeek-V3.2
- [#30277](https://github.com/sgl-project/sglang/pull/30277) [HiSparse] [Feature] Add Quest runtime sparse attention with breakable CUDA Graph support
- [#30292](https://github.com/sgl-project/sglang/pull/30292) [EAGLE] Fuse topk=1 draft argmax, position advance, and token store into Triton kernels
- [#30342](https://github.com/sgl-project/sglang/pull/30342) [DSA] Add NeoX RoPE branch to indexer fused kernels; re-enable fusion for DeepSeek-V3.2
- [#30535](https://github.com/sgl-project/sglang/pull/30535) add mamba_io_kernel
- [#30540](https://github.com/sgl-project/sglang/pull/30540) [Attention Backend] Add HPC-Ops attention backend
- [#30169](https://github.com/sgl-project/sglang/pull/30169) [GDN/KDA] Fuse SM100 CuteDSL prefill state I/O into the chunk h kernel
- [#30420](https://github.com/sgl-project/sglang/pull/30420) [WIP][DSV4] Breakable CUDA graph for mixed-chunk prefill
- [#30338](https://github.com/sgl-project/sglang/pull/30338) [DSV4] Split mixed-chunk attention: route decode tokens to the fp8 paged MLA kernel
- [#30474](https://github.com/sgl-project/sglang/pull/30474) [sglang-miles] Allocate DSA cuda-graph page_table and flashmla_metadata in TMS cuda_graph region
- [#30385](https://github.com/sgl-project/sglang/pull/30385) make infllm maxpool lookup fast

</details>

<details>
<summary>MoE & quantization (13)</summary>

- [#29997](https://github.com/sgl-project/sglang/pull/29997) Retire the AOT moe_fused_gate / kimi_k2_moe_fused_gate gate kernels
- [#23650](https://github.com/sgl-project/sglang/pull/23650) Add W4A8 MXFP quantization support for Qwen3 Dense on Ascend NPU
- [#27906](https://github.com/sgl-project/sglang/pull/27906) [Model] Support Qwen3.6 ModelOpt mixed NVFP4
- [#27867](https://github.com/sgl-project/sglang/pull/27867) [DSv4] Loading Time Weight Dequant
- [#30313](https://github.com/sgl-project/sglang/pull/30313) [AMD] Cap DSV4 Flash max_total_num_tokens
- [#30443](https://github.com/sgl-project/sglang/pull/30443) [NVIDIA] Allow modelopt_mixed quantization with flashinfer_cutedsl MoE runner
- [#30323](https://github.com/sgl-project/sglang/pull/30323) Use FP32 logits in MoEGate fallbacks
- [#30448](https://github.com/sgl-project/sglang/pull/30448) Refactor FP4 quantization and remove deprecated JIT kernels
- [#30438](https://github.com/sgl-project/sglang/pull/30438) Delete CUTLASS FP8 blockwise for SM90 and SM100, move SM120 to JIT and add SwapAB
- [#30541](https://github.com/sgl-project/sglang/pull/30541) [MoE Backend] Add HPC-Ops FP8 MoE runner backend
- [#30430](https://github.com/sgl-project/sglang/pull/30430) Optimize Nemotron latent MoE shared add
- [#30552](https://github.com/sgl-project/sglang/pull/30552) [NVIDIA] Extend modelopt_fp4-only MoE heuristics to NVFP4-expert modelopt_mixed
- [#30460](https://github.com/sgl-project/sglang/pull/30460) [DeepSeek V2] Reorder dual-stream MoE to main-first to avoid CUDA graph stream explosion

</details>

<details>
<summary>Model support (16)</summary>

- [#30040](https://github.com/sgl-project/sglang/pull/30040) [diffusion] feat: add LingBot realtime prompt, KV window, and lazy VAE controls
- [#29362](https://github.com/sgl-project/sglang/pull/29362) [AMD ]Feat/dsv4 ep tbo prefill
- [#30275](https://github.com/sgl-project/sglang/pull/30275) [Model] Support LongCat 2.0 FP8
- [#29777](https://github.com/sgl-project/sglang/pull/29777) [diffusion] Support SP for Krea-2
- [#30361](https://github.com/sgl-project/sglang/pull/30361) [diffusion] support LingBot-World 2.0
- [#30150](https://github.com/sgl-project/sglang/pull/30150) [diffusion][cache-dit] add dual-transformer Cache-DiT adapter specs
- [#30499](https://github.com/sgl-project/sglang/pull/30499) [lora] Support GDN in_proj_ba adapters for Qwen3.5
- [#28926](https://github.com/sgl-project/sglang/pull/28926) [diffusion]: enable RL rollout path for LTX-2.3 post-training
- [#30633](https://github.com/sgl-project/sglang/pull/30633) [diffusion] model: support Pi0.5
- [#30360](https://github.com/sgl-project/sglang/pull/30360) [Feature] Add MiniCPM-SALA support
- [#30536](https://github.com/sgl-project/sglang/pull/30536) [Cosmos3] Add cosmos3 Reasoner to llm only inference
- [#30298](https://github.com/sgl-project/sglang/pull/30298) [LoRA] Laguna: per-layer LoRA hidden-dim resolution for packed attention
- [#30486](https://github.com/sgl-project/sglang/pull/30486) [diffusion] RL rollout support for the Cosmos3 pipeline
- [#30487](https://github.com/sgl-project/sglang/pull/30487) [diffusion] Support Ideogram TurboTime LoRA inference
- [#30161](https://github.com/sgl-project/sglang/pull/30161) [Gemma4] Support per-request max_soft_tokens (image resolution) via images_config and mm_processor_kwargs
- [#30183](https://github.com/sgl-project/sglang/pull/30183) Support LongCat Flash n-gram embedding config aliases
- [#30377](https://github.com/sgl-project/sglang/pull/30377) Broad model enablement

</details>

<details>
<summary>Parallelism & scheduling (44)</summary>

- [#29701](https://github.com/sgl-project/sglang/pull/29701) Feat/flexkv main connector
- [#28441](https://github.com/sgl-project/sglang/pull/28441) [EPD] Optimize multimodal global cache with paged embedding pool
- [#29421](https://github.com/sgl-project/sglang/pull/29421) [GLM5.2] Add DSA Cache Layer Split under Prefill CP
- [#30157](https://github.com/sgl-project/sglang/pull/30157) Size KV pool after CUDA graph capture
- [#25372](https://github.com/sgl-project/sglang/pull/25372) [PDD] Add true request retraction for PDD
- [#29787](https://github.com/sgl-project/sglang/pull/29787) [Spec] Anchor GLM-5.2 MTP IndexShare topk on the draft-extend step
- [#29218](https://github.com/sgl-project/sglang/pull/29218) [Spec] DFlash: support pure-MLA targets with an fp8 KV cache
- [#30303](https://github.com/sgl-project/sglang/pull/30303) [spec decoding] support rejection sampling in multi layer eagle
- [#30409](https://github.com/sgl-project/sglang/pull/30409) Make CUDA graph disabling PD-role-aware
- [#30310](https://github.com/sgl-project/sglang/pull/30310) Increase the KV cache pool when using indexShare by 15%
- [#30472](https://github.com/sgl-project/sglang/pull/30472) Revert [#30310](https://github.com/sgl-project/sglang/pull/30310)
- [#30531](https://github.com/sgl-project/sglang/pull/30531) Reland "Increase the KV cache pool when using indexShare by 15%"
- [#30471](https://github.com/sgl-project/sglang/pull/30471) [misc] Add CI-only guards for the FutureMap seq_lens relay
- [#29615](https://github.com/sgl-project/sglang/pull/29615) Make mem_fraction_static reserve disaggregation-mode aware
- [#30398](https://github.com/sgl-project/sglang/pull/30398) [WIP] New EPD
- [#30204](https://github.com/sgl-project/sglang/pull/30204) [Spec] Add Qwen3-family DSpark draft model
- [#30416](https://github.com/sgl-project/sglang/pull/30416) [DRAFT]add DCP support for DeepSeek V4
- [#30553](https://github.com/sgl-project/sglang/pull/30553) [2/N] elastic-ep: Enable EPLB after scale-up
- [#30164](https://github.com/sgl-project/sglang/pull/30164) [1/N] elastic-ep: Add runtime EP scale-up
- [#30501](https://github.com/sgl-project/sglang/pull/30501) KV Cache Shard with Sequence Split
- [#30650](https://github.com/sgl-project/sglang/pull/30650) Ref aware unified kv buffer
- [#30417](https://github.com/sgl-project/sglang/pull/30417) Kvtc RFC
- [#30545](https://github.com/sgl-project/sglang/pull/30545) [PD] Support staging buffer with radix cache and radix-prefix pre-transfer
- [#30482](https://github.com/sgl-project/sglang/pull/30482) [4/N][CP] Support interleave strategy for cp v2
- [#30444](https://github.com/sgl-project/sglang/pull/30444) Support decode context parallel for DeepSeek MLA on the triton attention backend
- [#30329](https://github.com/sgl-project/sglang/pull/30329) [PD][NIXL] Propagate prefill transfer failures
- [#30466](https://github.com/sgl-project/sglang/pull/30466) [Spec] Distributed argmax for greedy EAGLE draft over TP
- [#30211](https://github.com/sgl-project/sglang/pull/30211) [diffusion] encoder_parallel: unify encoder folding and batch data-parallel encoding
- [#30393](https://github.com/sgl-project/sglang/pull/30393) [HiCache] Add HiCache draft sidecar pool support for MTP/EAGLE
- [#30581](https://github.com/sgl-project/sglang/pull/30581) [HiCache] Make host size a total memory budget
- [#30194](https://github.com/sgl-project/sglang/pull/30194) [CP] DCP Phase 2: decode-context-parallel strategy + wire backends
- [#30497](https://github.com/sgl-project/sglang/pull/30497) [DSV4] Enable overlap scheduling for online C128 MTP
- [#30392](https://github.com/sgl-project/sglang/pull/30392) [WIP][FEAT] Decouple multimodal global cache from Mooncake
- [#30513](https://github.com/sgl-project/sglang/pull/30513) [Spec] DSpark support PD and DeepEP
- [#30243](https://github.com/sgl-project/sglang/pull/30243) [KDA] Support extra_buffer mamba radix cache for Kimi Linear
- [#30185](https://github.com/sgl-project/sglang/pull/30185) Support DP attention for breakable prefill CUDA graphs
- [#30478](https://github.com/sgl-project/sglang/pull/30478) Add DCP to runtime parallel context
- [#30437](https://github.com/sgl-project/sglang/pull/30437) [Mamba] Support speculative decoding with extra_buffer_lazy
- [#30507](https://github.com/sgl-project/sglang/pull/30507) Add QoS-aware cache policy
- [#30468](https://github.com/sgl-project/sglang/pull/30468) Using UnifiedRadixTree by default for SWA, Mamba, and DSA models
- [#30365](https://github.com/sgl-project/sglang/pull/30365) [DSV4] Remove per-step seqlen D2H from speculative to make overlap scheduler work
- [#30574](https://github.com/sgl-project/sglang/pull/30574) [kv canary] Support UnifiedRadixCache in kv-canary and bracket nested model.forward
- [#30199](https://github.com/sgl-project/sglang/pull/30199) feat(hicache): support separate L2 pool ratios
- [#30578](https://github.com/sgl-project/sglang/pull/30578) feat: flush decode KV only for prefill reads on extend requests
- [#30457](https://github.com/sgl-project/sglang/pull/30457) Support scheduler_recv_interval (recv skipper) under DP-attention

</details>

<details>
<summary>Hardware & arch (31)</summary>

- [#30216](https://github.com/sgl-project/sglang/pull/30216) [CPU] add fused_qk_gemma_norm and refactor norm kernel implementation
- [#28401](https://github.com/sgl-project/sglang/pull/28401) NUMA: probe numactl binding and fall back when --membind is rejected
- [#28527](https://github.com/sgl-project/sglang/pull/28527) [Diffusion][CPU] Adding AMX optimizations for CPU platform
- [#30097](https://github.com/sgl-project/sglang/pull/30097) [MLX] Size the attention KV pool at the compute dtype for quantized models
- [#22660](https://github.com/sgl-project/sglang/pull/22660) Skip redundant moe_sum_reduce for single-expert routing on XPU
- [#30235](https://github.com/sgl-project/sglang/pull/30235) [Intel GPU] xpu_piecewise: fall back to eager when PCG capture stream is unset
- [#30415](https://github.com/sgl-project/sglang/pull/30415) Enable RDNA3/4 (gfx1100/gfx1201) for ROCm kernels
- [#30312](https://github.com/sgl-project/sglang/pull/30312) [NPU]Add support --pre-warm-nccl
- [#30048](https://github.com/sgl-project/sglang/pull/30048) [XPU] Unbreak stage-b: re-add --disable-decode-cuda-graph, quarantine EAGLE3 parity
- [#30237](https://github.com/sgl-project/sglang/pull/30237) [AMD][DeepSeek V4] Set SGLANG_OPT_FLASHMLA_SPARSE_PREFILL to false on hip code path
- [#29480](https://github.com/sgl-project/sglang/pull/29480) [NPU] Add extra topk_weights input in deepep ll dispatch
- [#30156](https://github.com/sgl-project/sglang/pull/30156) [MLX] Split radix KV pool by attention layer type for sliding-window models
- [#30575](https://github.com/sgl-project/sglang/pull/30575) [AMD] Enable Fast Triton Sparse MLA backend
- [#30272](https://github.com/sgl-project/sglang/pull/30272) SM120 DSv4 TP2 enablement
- [#30163](https://github.com/sgl-project/sglang/pull/30163) [Apple Silicon] Add a custom Metal RMSNorm kernel
- [#30236](https://github.com/sgl-project/sglang/pull/30236) [XPU] Support INT4 dense linear (AWQ/GPTQ) for XPU
- [#30318](https://github.com/sgl-project/sglang/pull/30318) [NPU] Add mxfp4-w4a8 quantization support for npu
- [#30319](https://github.com/sgl-project/sglang/pull/30319) [NPU] Add mxfp4-w4a4 quantization support for npu
- [#30317](https://github.com/sgl-project/sglang/pull/30317) [NPU] Add mxfp8-w8a8 moe quantization and deepep new quantization support for npu
- [#30604](https://github.com/sgl-project/sglang/pull/30604) [CPU] update fla.cpp to support when num_head_v is not multiples of 16
- [#30205](https://github.com/sgl-project/sglang/pull/30205) [NPU]Optimize multimodal scatter on NPU
- [#30345](https://github.com/sgl-project/sglang/pull/30345) [WIP][Intel][XPU][LoRA] Enable LoRA on Intel XPU
- [#30548](https://github.com/sgl-project/sglang/pull/30548) Speculative Decoding support for intel_xpu attention backend on XPU target
- [#30273](https://github.com/sgl-project/sglang/pull/30273) [XPU] Enable breakable prefill CUDA graph on XPU
- [#30257](https://github.com/sgl-project/sglang/pull/30257) [AMD][Perf] Add dense-MHA one-shot prefill support paths on gfx950 for DSA models
- [#30524](https://github.com/sgl-project/sglang/pull/30524) [NPU] eagle3 support modelslim quarot
- [#30248](https://github.com/sgl-project/sglang/pull/30248) [WIP][AMD] A/B disable DSV4 Flash C128 state PD transfer
- [#30143](https://github.com/sgl-project/sglang/pull/30143) [qwen3.5][XPU] Enable alt_stream for Qwen3.5 on XPU
- [#30547](https://github.com/sgl-project/sglang/pull/30547) [MLX] Honor --max-running-requests in the model runner stub
- [#30469](https://github.com/sgl-project/sglang/pull/30469) [AMD] Enable MLA DCP for aiter backend
- [#30373](https://github.com/sgl-project/sglang/pull/30373) [Diffusion][CPU] Add GELU kernels and enable RMSNorm CPU path
- [#30519](https://github.com/sgl-project/sglang/pull/30519) [AMD] [GLM5] fp8 MLA absorbed bmm for GLM-5.2 on gfx950

</details>

<details>
<summary>API & serving (23)</summary>

- [#27564](https://github.com/sgl-project/sglang/pull/27564) feat(metrics): add Prometheus metrics for the EPD encoder server
- [#23049](https://github.com/sgl-project/sglang/pull/23049) [Diffusion] Diffusion model support log-requests
- [#30366](https://github.com/sgl-project/sglang/pull/30366) [RL] Add /pull_weights: engine-side pull of published weights
- [#23508](https://github.com/sgl-project/sglang/pull/23508) [gRPC] Native server: launcher + HTTP + server args wiring
- [#29716](https://github.com/sgl-project/sglang/pull/29716) feat(mem_cache): add client-side metadata cache for HiCacheFile storage
- [#30146](https://github.com/sgl-project/sglang/pull/30146) Disable multi-threaded load by default when prefetch is on
- [#30615](https://github.com/sgl-project/sglang/pull/30615) [Bench] Add fixed-prompt mode and per-request spec accept length metrics
- [#30440](https://github.com/sgl-project/sglang/pull/30440) feat(grpc): support disaggregated generation requests
- [#30148](https://github.com/sgl-project/sglang/pull/30148) [diffusion] Pass progressive params through image API
- [#30367](https://github.com/sgl-project/sglang/pull/30367) [RL] Add /pull_weights: engine-side pull of published weights into a host-local checkpoint
- [#30177](https://github.com/sgl-project/sglang/pull/30177) Support returning the last hidden state
- [#30256](https://github.com/sgl-project/sglang/pull/30256) Add Mooncake tenant id support
- [#30434](https://github.com/sgl-project/sglang/pull/30434) [Feature] Support encoding_format="base64" in /v1/embeddings
- [#30141](https://github.com/sgl-project/sglang/pull/30141) [Feature] Add --config-format alias for --model-config-parser
- [#30267](https://github.com/sgl-project/sglang/pull/30267) feat: reject empty/whitespace-only assistant content in chat validation
- [#30330](https://github.com/sgl-project/sglang/pull/30330) [server] Add --stream-response-default-continuous-usage-stats
- [#30607](https://github.com/sgl-project/sglang/pull/30607) [SUPA][1/N] Add device detection and check_env support
- [#30530](https://github.com/sgl-project/sglang/pull/30530) [router] Break the SSE pump on client disconnect even while the upstream is pending
- [#30573](https://github.com/sgl-project/sglang/pull/30573) Configurable decode retraction order
- [#30264](https://github.com/sgl-project/sglang/pull/30264) [Feature] Per-request disable_speculative_decoding sampling param
- [#30630](https://github.com/sgl-project/sglang/pull/30630) [tokenizer] Support pluggable tokenizer worker class in multi-tokenizer mode
- [#30533](https://github.com/sgl-project/sglang/pull/30533) more fixes for Nemotron 3 parser for tool call and force nonempty content
- [#30429](https://github.com/sgl-project/sglang/pull/30429) feat: Clean up shared memory and CUDA host registrations in HostSharedMemoryManager on shutdown

</details>

<details>
<summary>Tests (32)</summary>

- [#30384](https://github.com/sgl-project/sglang/pull/30384) Fix DSA top-k v2 test metadata
- [#25364](https://github.com/sgl-project/sglang/pull/25364) Add Accuracy Benchmark for OCR models
- [#29331](https://github.com/sgl-project/sglang/pull/29331) [NPU] Add new diffusion tests
- [#29440](https://github.com/sgl-project/sglang/pull/29440) [MLX] Add correctness tests for qwen2_moe and qwen3_moe
- [#29215](https://github.com/sgl-project/sglang/pull/29215) [bench] Add agentic-trace multi-turn dataset to bench_serving
- plus 27 more minor test updates

</details>

<details>
<summary>CI & build (26)</summary>

- [#29403](https://github.com/sgl-project/sglang/pull/29403) feat: sync npu nightly test improvements
- [#29855](https://github.com/sgl-project/sglang/pull/29855) [AMD][DI][CI] 3/N Add Kimi K2.6 FP8 MI355X 1P1D nightly recipes
- [#30386](https://github.com/sgl-project/sglang/pull/30386) [AMD] Run MI355X disaggregation Nightly Test
- [#30309](https://github.com/sgl-project/sglang/pull/30309) [AMD] ci: run multimodal_gen unit suite on AMD
- [#30307](https://github.com/sgl-project/sglang/pull/30307) [AMD] add dedicated jit-kernel-benchmark-test-amd stage
- plus 21 more minor CI updates

</details>

<details>
<summary>Docs (26)</summary>

- [#30201](https://github.com/sgl-project/sglang/pull/30201) cookbook: add Hunyuan 3 (Hy3) Day-0 page
- [#29912](https://github.com/sgl-project/sglang/pull/29912) Remove retired DSA env paths
- [#29404](https://github.com/sgl-project/sglang/pull/29404) Add DeepReinforce Ornith-1.0 to cookbook
- [#30320](https://github.com/sgl-project/sglang/pull/30320) [Doc] Add LongCat 2.0 FP8 cookbook
- [#30214](https://github.com/sgl-project/sglang/pull/30214) docs(cookbook): total throughput per GPU + percentile latency labels
- plus 21 more minor documentation updates

</details>

<details>
<summary>Bugfixes (98)</summary>

- [#29742](https://github.com/sgl-project/sglang/pull/29742) [diffusion] Fix Z-Image accuracy
- [#28534](https://github.com/sgl-project/sglang/pull/28534) [AMD] Enable JIT staged HiCache write-back and fix CPU-index crash
- [#30181](https://github.com/sgl-project/sglang/pull/30181) [MLX] Fix single-token chunked-prefill continuation misrouted as decode
- [#30241](https://github.com/sgl-project/sglang/pull/30241) [diffusion] Fix ragged-caption dynamic-batching accuracy bug in Ernie-Image
- [#30461](https://github.com/sgl-project/sglang/pull/30461) [DSV4] Fix draft SWA transfer for disaggregated MTP
- plus 93 more minor bugfixes

</details>

<details>
<summary>Refactors (28)</summary>

- [#30483](https://github.com/sgl-project/sglang/pull/30483) Enhance mechanical refactor proof construction and verification skill
- [#30137](https://github.com/sgl-project/sglang/pull/30137) Config resolution pipeline: full-stack review
- [#30249](https://github.com/sgl-project/sglang/pull/30249) refactor: move MHA host-pool into pool_host/mha.py
- [#30180](https://github.com/sgl-project/sglang/pull/30180) Cleanup: relocate temp_set_env and consolidate multi-device/CUDA helpers
- [#30281](https://github.com/sgl-project/sglang/pull/30281) Rename tree variables to cache in unittest
- plus 23 more minor refactoring updates

</details>

<details>
<summary>Other (1)</summary>

- [#30159](https://github.com/sgl-project/sglang/pull/30159) [diffusion] Clean up duplicate helper definitions

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: ac1ca5edb01df14bff10693952e8bcc118959c77a38905f11b07b7b4913290d3 -->
