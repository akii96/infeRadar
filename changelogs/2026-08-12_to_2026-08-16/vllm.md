# vllm: PR digest (2026-08-12 to 2026-08-16)

_179 merged, 386 newly opened - source vllm-project/vllm, generated 2026-08-16T21:37:56Z_

## TL;DR
*   **DeepSeek & Kimi-K3 dominated attention:** DeepSeek V4/V3.2 saw major performance work with DSpark confidence-scheduled verification, Triton sparse-MLA decode optimizations, and FlyDSL fused mega-MoE backends. Kimi-K3 gained GEMM-RS sequence parallelism and fused KDA decode kernels.
*   **Kernels & Quantization expanded:** Significant kernel additions include B12X dense linear, causal paged attention, and FP4 MoE backends. FlashInfer and TRTLLM integrations advanced with new MXFP8 and MXFP4 linear methods.
*   **Speculative Decoding & Attention:** Speculative decoding capabilities expanded heavily with DSpark adaptive verification, multi-layer MTP support, and a new `suffix_gpu` drafter for async scheduling.
*   **New Models & Core:** Merged native multimodal support for Dots3 NOTE and Muse Glimmer, while newly opened PRs target GLM-5.2 TurboQuant and HSTU. Core architecture is moving toward hardware-agnostic model definitions via HF transformer backends and Mooncake layerwise KV cache transfers.

## Most important PRs
*   **[#51255](https://github.com/vllm-project/vllm/pull/51255)** Adds native multimodal support for the Dots3 NOTE model, expanding vision-language capabilities with custom attention and speculative decoding integrations across AMD and NVIDIA hardware.
*   **[#47808](https://github.com/vllm-project/vllm/pull/47808)** Implements DSpark confidence-scheduled verification for speculative decoding. This provides a highly optimized, cross-backend verification path that dynamically adjusts based on draft confidence to maximize acceptance rates.
*   **[#52079](https://github.com/vllm-project/vllm/pull/52079)** Introduces GEMM-RS (Reduce-Scatter) for sequence parallelism in Kimi-K3, significantly reducing communication overhead during distributed prefill and decode phases on NVIDIA hardware.
*   **[#52472](https://github.com/vllm-project/vllm/pull/52472)** Proposes a GLM-5.2 TurboQuant sparse backend with DCP/MTP support. This in-progress work brings highly optimized, quantized sparse attention to the GLM-5.2 family using Triton.
*   **[#51978](https://github.com/vllm-project/vllm/pull/51978)** Adds layerwise KV cache transfer support via the Mooncake session API. This foundational feature enables efficient, distributed KV cache offloading and sharing across nodes, drastically improving multi-tenant throughput.

## More changes by area

<details>
<summary>Performance (31)</summary>

- [#52212](https://github.com/vllm-project/vllm/pull/52212) Optimize Triton sparse-MLA decode on gfx950
- [#50654](https://github.com/vllm-project/vllm/pull/50654) Kimi-K3 Fused kernel for KDA decode
- [#51674](https://github.com/vllm-project/vllm/pull/51674) Add fused CUDA post-conv MTP decode kernel for Qwen3.5 GDN
- [#51862](https://github.com/vllm-project/vllm/pull/51862) Kimi-K3 Remove prefill pipeline stall in chunk KDA
- [#52331](https://github.com/vllm-project/vllm/pull/52331) Speed up the LoRA test job
- [#51738](https://github.com/vllm-project/vllm/pull/51738) Avoid more GPU<->CPU syncs on the model execution path
- [#52369](https://github.com/vllm-project/vllm/pull/52369) Avoid more GPU<->CPU syncs in multimodal encoders
- [#48223](https://github.com/vllm-project/vllm/pull/48223) Dual-stream decode with hipgraphs
- [#52024](https://github.com/vllm-project/vllm/pull/52024) Revert dual-stream decode with hipgraphs
- [#52277](https://github.com/vllm-project/vllm/pull/52277) Vectorize Cohere binary embedding bit-packing
- [#51311](https://github.com/vllm-project/vllm/pull/51311) Flash kda out kernel for prefill
- [#49793](https://github.com/vllm-project/vllm/pull/49793) Fuse the MTP trailing all-reduce; local-argmax draft tokens
- [#50017](https://github.com/vllm-project/vllm/pull/50017) Chunked prefill paged decode masked load perf
- [#52084](https://github.com/vllm-project/vllm/pull/52084) Optimize sparse top-k metadata kernels for higher prefill throughput
- [#51919](https://github.com/vllm-project/vllm/pull/51919) Cut decode-side TTFT for NIXL P/D
- [#52364](https://github.com/vllm-project/vllm/pull/52364) Enable fused KDA decode for Ling-3.0 (H=32)
- [#52162](https://github.com/vllm-project/vllm/pull/52162) Shard decode requests across PCP ranks
- [#51942](https://github.com/vllm-project/vllm/pull/51942) Fuse all-reduce RMSNorm with packed FP8
- [#52187](https://github.com/vllm-project/vllm/pull/52187) Zero new KV blocks by cache group
- [#52388](https://github.com/vllm-project/vllm/pull/52388) Optimize k3 mamba metadata preparation
- [#52059](https://github.com/vllm-project/vllm/pull/52059) Split MiniMax-M3 prefill index-score K loop
- [#52329](https://github.com/vllm-project/vllm/pull/52329) Cache logits-processing request state
- [#52096](https://github.com/vllm-project/vllm/pull/52096) Reduce AITER MLA FP8 BMM warmup sizes
- [#52468](https://github.com/vllm-project/vllm/pull/52468) Scale num_warps with tile size in Triton reshape-and-cache kernels
- [#52033](https://github.com/vllm-project/vllm/pull/52033) Dual-stream decode with hipgraphs
- [#52080](https://github.com/vllm-project/vllm/pull/52080) Kimi-K3 AMD MLA: fuse the q-a and kv-a RMSNorms
- [#52539](https://github.com/vllm-project/vllm/pull/52539) Support Qwen3.6 head ratio in fused GDN MTP
- [#52494](https://github.com/vllm-project/vllm/pull/52494) Fuse MLA q/kv RMSNorm in AMD Kimi-K3 MLA wrapper
- [#52305](https://github.com/vllm-project/vllm/pull/52305) Use Aiter's CA Output Variant for Kimi-K3
- [#51967](https://github.com/vllm-project/vllm/pull/51967) Optimize global top-k index kernel with compile-time constants
- [#49852](https://github.com/vllm-project/vllm/pull/49852) Enable encoder cuda graph for model runner v2

</details>

<details>
<summary>Kernels & attention (42)</summary>

- [#52016](https://github.com/vllm-project/vllm/pull/52016) Add B12X dense linear backends
- [#51772](https://github.com/vllm-project/vllm/pull/51772) Fuse Kimi-K3 chunked-context K/V packing
- [#52164](https://github.com/vllm-project/vllm/pull/52164) Take the native decode path for MTP=3 on SM90
- [#50534](https://github.com/vllm-project/vllm/pull/50534) Add tuned Mamba SSU configs for Intel Arc Pro B70
- [#51318](https://github.com/vllm-project/vllm/pull/51318) Revert adaptive C128A metadata packing
- [#52005](https://github.com/vllm-project/vllm/pull/52005) Fix mrope.py::apply_interleaved_rope() when torch.compile is used
- [#52030](https://github.com/vllm-project/vllm/pull/52030) Fix packed GDN decode launch for large batch-head grids
- [#51359](https://github.com/vllm-project/vllm/pull/51359) Initialize DeepGemmQuantScaleFMT oracle lazily
- [#52118](https://github.com/vllm-project/vllm/pull/52118) Process ragged weights in xpu linear backend
- [#52148](https://github.com/vllm-project/vllm/pull/52148) Fix FlashInfer SM12x prefill with sinks
- [#52139](https://github.com/vllm-project/vllm/pull/52139) Give the AITER MLA decode metadata stub its MLA dims
- [#51216](https://github.com/vllm-project/vllm/pull/51216) Enable preshuffled sparse indexing for 16-token blocks
- [#49139](https://github.com/vllm-project/vllm/pull/49139) Fix persistent top-k histogram reuse after short rows
- [#48666](https://github.com/vllm-project/vllm/pull/48666) Gemma-4 FA4 FP8 Kernel
- [#51913](https://github.com/vllm-project/vllm/pull/51913) Move context_lens_tensor compute into GDN prefill path
- [#52368](https://github.com/vllm-project/vllm/pull/52368) Simplify B12X linear kernels and warmup
- [#52363](https://github.com/vllm-project/vllm/pull/52363) Add manual CUDA RoPE KV-cache fusion for Llama
- [#52017](https://github.com/vllm-project/vllm/pull/52017) Add B12X causal paged attention backend
- [#52506](https://github.com/vllm-project/vllm/pull/52506) Add FlashInfer ReplaySSM
- [#52231](https://github.com/vllm-project/vllm/pull/52231) Support batch invariance on ROCm
- [#52239](https://github.com/vllm-project/vllm/pull/52239) Publish prefill KV directly in MLA layout
- [#52275](https://github.com/vllm-project/vllm/pull/52275) Add adaptive layouts to TRTLLM MXFP8 linear backend
- [#52208](https://github.com/vllm-project/vllm/pull/52208) Add Aiter ops tests
- [#52191](https://github.com/vllm-project/vllm/pull/52191) Support FP16/BF16 persisted GDN state on AMX
- [#52297](https://github.com/vllm-project/vllm/pull/52297) Move GDN common metadata compute out of per-group build
- [#52046](https://github.com/vllm-project/vllm/pull/52046) Add pcp support in dsv3.2
- [#51987](https://github.com/vllm-project/vllm/pull/51987) Revert FlashInfer XQA decode support on SM12x
- [#52516](https://github.com/vllm-project/vllm/pull/52516) Fix Mooncake heterogeneous TP with replicated GQA heads
- [#52019](https://github.com/vllm-project/vllm/pull/52019) Skip stage2 for single-split Triton MLA decode
- [#52402](https://github.com/vllm-project/vllm/pull/52402) DSv4 sparse-attn indexer: native fp8 MFMA + corrected LDS occupancy gate
- [#51915](https://github.com/vllm-project/vllm/pull/51915) Enable GLM-5.2-MXFP4 on the deepseek_v32 path and fix sparse attention correctness
- [#52243](https://github.com/vllm-project/vllm/pull/52243) Fix vllm_c fused_add_rms_norm to match native IR rounding semantics
- [#52157](https://github.com/vllm-project/vllm/pull/52157) Support varlen trtllm-gen decode for adaptive verification
- [#52189](https://github.com/vllm-project/vllm/pull/52189) Fail fast when MLA head dimensions are not supported by the CPU decode kernel
- [#52063](https://github.com/vllm-project/vllm/pull/52063) Avoid AITER FP8 BMM for MLA K projection
- [#52218](https://github.com/vllm-project/vllm/pull/52218) Support speculative decode in Triton MLA
- [#52406](https://github.com/vllm-project/vllm/pull/52406) Support ModelOpt FP8_PB_WO in Kimi-K3 attention
- [#52550](https://github.com/vllm-project/vllm/pull/52550) Unify indexer cache dtype under attention_config.indexer_kv_dtype
- [#51994](https://github.com/vllm-project/vllm/pull/51994) Fix DiffusionGemma silently freezing attention mask under CUDA graph replay
- [#52433](https://github.com/vllm-project/vllm/pull/52433) Enable Gemma4 E4B on Intel XPU with mixed attention backends
- [#52374](https://github.com/vllm-project/vllm/pull/52374) Support attention-free models
- [#51821](https://github.com/vllm-project/vllm/pull/51821) Restore the DeepSeek-V4 input GEMM override point

</details>

<details>
<summary>MoE & quantization (34)</summary>

- [#51624](https://github.com/vllm-project/vllm/pull/51624) Unqualized MoE Backend for Power (VSX)
- [#50597](https://github.com/vllm-project/vllm/pull/50597) Remove special-case SiTU support model-specific gating
- [#51583](https://github.com/vllm-project/vllm/pull/51583) Fold the MXFP4 block scale in 2 instructions instead of 4
- [#50074](https://github.com/vllm-project/vllm/pull/50074) Reuse online NVFP4 MoE kernel across reloads
- [#51793](https://github.com/vllm-project/vllm/pull/51793) Remove dead QuantizationConfig.is_mxfp4_quant
- [#46845](https://github.com/vllm-project/vllm/pull/46845) Fix MiniMax-M3 compressed-tensors FP8 MoE SwiGLU params
- [#52114](https://github.com/vllm-project/vllm/pull/52114) Add Ling hybrid MXFP4 routed experts support
- [#50787](https://github.com/vllm-project/vllm/pull/50787) Route block-quantized FP8 weights to the W8A8 kernel
- [#51860](https://github.com/vllm-project/vllm/pull/51860) Dequantize the fp8 decode query for MLA backends without quant-query support
- [#51872](https://github.com/vllm-project/vllm/pull/51872) Make fp8_min/fp8_max constexpr in _quantize_pad_fp8_kernel
- [#51980](https://github.com/vllm-project/vllm/pull/51980) Update AITER MXFP4 W4A16 tests to the renamed expert_mask
- [#52018](https://github.com/vllm-project/vllm/pull/52018) Add B12X FP4 MoE backend
- [#51918](https://github.com/vllm-project/vllm/pull/51918) Add FlyDSL fused mega-MoE backend for DeepSeek V4
- [#52357](https://github.com/vllm-project/vllm/pull/52357) SM12x Triton fallback for fp8_einsum / o_proj
- [#52032](https://github.com/vllm-project/vllm/pull/52032) Add opt-in dynamic NVFP4 MoE GEMM2 quantization
- [#52429](https://github.com/vllm-project/vllm/pull/52429) Fuse SwiGLU into Triton W13 epilogue
- [#51941](https://github.com/vllm-project/vllm/pull/51941) Accept prequantized DeepGEMM inputs
- [#52195](https://github.com/vllm-project/vllm/pull/52195) Add Stage 1 (CPU-only, reference) BitNet ternary quantization backend
- [#52209](https://github.com/vllm-project/vllm/pull/52209) Add routed expert loading for gpt-oss
- [#52100](https://github.com/vllm-project/vllm/pull/52100) Preserve TP sharding with explicit EP
- [#52196](https://github.com/vllm-project/vllm/pull/52196) Add Stage 1 (CPU-only, reference) int8 quantization utilities for SSM state
- [#52502](https://github.com/vllm-project/vllm/pull/52502) Add GB10 fused-MoE fp8 tuning configs
- [#51925](https://github.com/vllm-project/vllm/pull/51925) Enable optimized FlashInfer add-RMSNorm NVFP4 fusion
- [#52263](https://github.com/vllm-project/vllm/pull/52263) Support AMD Quark per-block FP8 for fused MoE layers
- [#51947](https://github.com/vllm-project/vllm/pull/51947) Reuse packed FP8 logits inputs
- [#51943](https://github.com/vllm-project/vllm/pull/51943) Fuse attention FP8 quantization
- [#52424](https://github.com/vllm-project/vllm/pull/52424) Implement MXFP4 linear method
- [#51924](https://github.com/vllm-project/vllm/pull/51924) Refine FlashInfer one-sided All2All integration
- [#52192](https://github.com/vllm-project/vllm/pull/52192) Add tuned fused_moe config for NVIDIA GB10
- [#52532](https://github.com/vllm-project/vllm/pull/52532) Canonicalize Marlin MoE token order
- [#52383](https://github.com/vllm-project/vllm/pull/52383) Pad MoE activations inside the custom op to fix CUDA-graph corruption
- [#51945](https://github.com/vllm-project/vllm/pull/51945) Reuse fused quantized inputs
- [#51933](https://github.com/vllm-project/vllm/pull/51933) Enable torch as mxfp8 linear backend
- [#52204](https://github.com/vllm-project/vllm/pull/52204) Add FlashInfer TRTLLM MXFP8 linear backend

</details>

<details>
<summary>Model support (23)</summary>

- [#51655](https://github.com/vllm-project/vllm/pull/51655) Add Muse Glimmer model support
- [#49458](https://github.com/vllm-project/vllm/pull/49458) Hardware-agnostic model definition via HF transformer backend (1/N)
- [#48215](https://github.com/vllm-project/vllm/pull/48215) Add tower/connector LoRA support for Ultravox
- [#42662](https://github.com/vllm-project/vllm/pull/42662) Support vision tower LoRA
- [#51831](https://github.com/vllm-project/vllm/pull/51831) Support R3 capture with DeepGEMM MegaMoE
- [#47017](https://github.com/vllm-project/vllm/pull/47017) Enable DeepSeek-V4 on gfx11
- [#52037](https://github.com/vllm-project/vllm/pull/52037) Skip unused Jina V5 output layers
- [#52425](https://github.com/vllm-project/vllm/pull/52425) Support Transformers pooling model
- [#52172](https://github.com/vllm-project/vllm/pull/52172) Disable sequence parallelism for Dots3 NOTE
- [#52534](https://github.com/vllm-project/vllm/pull/52534) Support GLM-5.2 deployment on A100 (SM_80)
- [#52286](https://github.com/vllm-project/vllm/pull/52286) Add HSTU model support to vLLM
- [#52459](https://github.com/vllm-project/vllm/pull/52459) Register model capabilities directly
- [#52236](https://github.com/vllm-project/vllm/pull/52236) Remove FireRedLIDForConditionalGeneration
- [#52355](https://github.com/vllm-project/vllm/pull/52355) Adding embedding layer and lm_head
- [#52015](https://github.com/vllm-project/vllm/pull/52015) Support pipeline parallelism for DiffusionGemma
- [#52185](https://github.com/vllm-project/vllm/pull/52185) Pixtral: use packed multimodal encoder attention
- [#51949](https://github.com/vllm-project/vllm/pull/51949) Enable LoRA support for tower and connector in Cosmos3-Edge
- [#52165](https://github.com/vllm-project/vllm/pull/52165) Detect DeepSeek-V4 DSpark checkpoints from config
- [#52255](https://github.com/vllm-project/vllm/pull/52255) DeepSeek-V4: render request-level tools after the system prompt
- [#52254](https://github.com/vllm-project/vllm/pull/52254) DeepSeek-V4: don't emit an empty `<think></think>` block for reasoningless turns
- [#52321](https://github.com/vllm-project/vllm/pull/52321) Enable google/gemma-4-E2B-it-qat-mobile-ct inference on Intel XPU
- [#52455](https://github.com/vllm-project/vllm/pull/52455) Enable Gemma4 E4B inference on Intel XPU with per-layer heterogeneous head_dim
- [#51653](https://github.com/vllm-project/vllm/pull/51653) Enable V2 model runner for Kimi-K3 on ROCm

</details>

<details>
<summary>Parallelism & scheduling (17)</summary>

- [#49585](https://github.com/vllm-project/vllm/pull/49585) Added Build Connector Worker Meta for EC Connector
- [#50685](https://github.com/vllm-project/vllm/pull/50685) Keep Qwen3Next layer boundaries sequence parallel
- [#51614](https://github.com/vllm-project/vllm/pull/51614) Emit self-describing CPU events at KV-group block granularity
- [#50620](https://github.com/vllm-project/vllm/pull/50620) Include transfer mode (push/pull) in the compatibility hash
- [#51813](https://github.com/vllm-project/vllm/pull/51813) Fix and test EPLB balancedness calculation
- [#51879](https://github.com/vllm-project/vllm/pull/51879) Expose data-parallel topology to offloading backends
- [#51650](https://github.com/vllm-project/vllm/pull/51650) Overlap async-scheduling PP sampled-token broadcast with compute
- [#52101](https://github.com/vllm-project/vllm/pull/52101) BF16 PoC integration of MoonEP balanced EP backend
- [#52466](https://github.com/vllm-project/vllm/pull/52466) Add decode offloading to Mooncake Store consumers
- [#52110](https://github.com/vllm-project/vllm/pull/52110) Support pp in sharded state loader
- [#52464](https://github.com/vllm-project/vllm/pull/52464) Prefix-affinity tie-break in the internal DP load balancer
- [#52230](https://github.com/vllm-project/vllm/pull/52230) Skip encoder CUDA graphs on non-first PP ranks
- [#52099](https://github.com/vllm-project/vllm/pull/52099) Add explicit expert-parallel topology
- [#51988](https://github.com/vllm-project/vllm/pull/51988) Add configurable load-balancing strategy to EPLB
- [#52497](https://github.com/vllm-project/vllm/pull/52497) Add rank-local IPC weight updates
- [#52491](https://github.com/vllm-project/vllm/pull/52491) Fix encoder round-robin fan-out
- [#52152](https://github.com/vllm-project/vllm/pull/52152) Add shared-disk weight transfer backend

</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#51159](https://github.com/vllm-project/vllm/pull/51159) Defer tilelang import
- [#49365](https://github.com/vllm-project/vllm/pull/49365) Detect ROCm wheel variant from environment for precompiled wheels
- [#52514](https://github.com/vllm-project/vllm/pull/52514) Add CuMemAllocator.discard() for tag-selective GPU memory release
- [#50268](https://github.com/vllm-project/vllm/pull/50268) Enable fused bf16→fp32 router GEMM on ROCm
- [#51099](https://github.com/vllm-project/vllm/pull/51099) Fix build: make FP32Vec copy constructors non-explicit
- [#52226](https://github.com/vllm-project/vllm/pull/52226) Decode optimizations for NVIDIA confidential computing
- [#51956](https://github.com/vllm-project/vllm/pull/51956) Register KV offload mmap region as pinned host memory

</details>

<details>
<summary>API & serving (28)</summary>

- [#52261](https://github.com/vllm-project/vllm/pull/52261) Consolidate entrypoint exception handler
- [#45802](https://github.com/vllm-project/vllm/pull/45802) Support count_reasoning_tokens in the Streaming Parser Engine
- [#51316](https://github.com/vllm-project/vllm/pull/51316) Add RL lifecycle control
- [#49577](https://github.com/vllm-project/vllm/pull/49577) Mask Replay
- [#51906](https://github.com/vllm-project/vllm/pull/51906) Add routed-experts prompt offset
- [#52394](https://github.com/vllm-project/vllm/pull/52394) Raise VLLMValidationError from structured output validators
- [#52246](https://github.com/vllm-project/vllm/pull/52246) Return 4xx for client-caused errors in /v1/messages
- [#51463](https://github.com/vllm-project/vllm/pull/51463) Make model optional on all /derender request classes
- [#51931](https://github.com/vllm-project/vllm/pull/51931) Use VLLMValidationError in pooling input validation
- [#52098](https://github.com/vllm-project/vllm/pull/52098) Log output token IDs at DEBUG level
- [#51999](https://github.com/vllm-project/vllm/pull/51999) Warn that --api-key does not gate all endpoints
- [#52145](https://github.com/vllm-project/vllm/pull/52145) Add missing return type annotations in outputs.py
- [#52384](https://github.com/vllm-project/vllm/pull/52384) Preserve skip_special_tokens decoding option
- [#52132](https://github.com/vllm-project/vllm/pull/52132) Enhance engine snapshot management and API lifecycle
- [#52131](https://github.com/vllm-project/vllm/pull/52131) Move api_server.py out openai folder
- [#52505](https://github.com/vllm-project/vllm/pull/52505) Write run-batch responses incrementally instead of at the end
- [#51904](https://github.com/vllm-project/vllm/pull/51904) Support stop strings in the token generate route
- [#52309](https://github.com/vllm-project/vllm/pull/52309) Consolidate entrypoint middleware
- [#51900](https://github.com/vllm-project/vllm/pull/51900) Cap the cumulative length of realtime sessions
- [#52061](https://github.com/vllm-project/vllm/pull/52061) Add native forward-pass metrics emission
- [#51937](https://github.com/vllm-project/vllm/pull/51937) Migrate Hermes tool parser to the new streaming Parser Engine
- [#52133](https://github.com/vllm-project/vllm/pull/52133) Add Hunyuan A13B tool parser
- [#52199](https://github.com/vllm-project/vllm/pull/52199) Add local/external prefix-cache hit breakdown to prompt_tokens_details
- [#52249](https://github.com/vllm-project/vllm/pull/52249) Add operation label to Prometheus latency histograms
- [#52519](https://github.com/vllm-project/vllm/pull/52519) Abort realtime STT on disconnect; harden Anthropic tool JSON
- [#52529](https://github.com/vllm-project/vllm/pull/52529) Only echo the assistant turn in batched chat completions
- [#52418](https://github.com/vllm-project/vllm/pull/52418) Responses streaming: tool-call argument tail interleaved with reasoning/content aborts SSE stream
- [#52528](https://github.com/vllm-project/vllm/pull/52528) Guard remaining before-validators against non-object JSON bodies

</details>

<details>
<summary>Speculative decoding & KV Cache (43)</summary>

- [#51538](https://github.com/vllm-project/vllm/pull/51538) Make DSV4 sparse MLA work end-to-end for plain decode, MTP, and DSpark
- [#51704](https://github.com/vllm-project/vllm/pull/51704) Backend-published KV packing via customize_spec
- [#51865](https://github.com/vllm-project/vllm/pull/51865) Require all requests to be decoding for uniform-decode dispatch
- [#50487](https://github.com/vllm-project/vllm/pull/50487) Tap the pre-norm AttnRes mixture as the Kimi K3 DFlash aux state
- [#50062](https://github.com/vllm-project/vllm/pull/50062) Add KV cache support for multi-layer MTP
- [#51218](https://github.com/vllm-project/vllm/pull/51218) Report FULL_ATTENTION for uniform-base UniformTypeKVCacheSpecs groups
- [#52419](https://github.com/vllm-project/vllm/pull/52419) Keep EAGLE cache registration on the partial-hash-hit path
- [#52311](https://github.com/vllm-project/vllm/pull/52311) Fix off-by-one in bad_words draft-prefix matching
- [#52436](https://github.com/vllm-project/vllm/pull/52436) DSpark: fix the grammar bitmask mapping when the draft budget is zero
- [#51843](https://github.com/vllm-project/vllm/pull/51843) Disable fine-grained prefix-cache hits for incompatible hybrid KV layouts
- [#51256](https://github.com/vllm-project/vllm/pull/51256) Reserve the bonus query slot in DFlash scheduling budget
- [#51840](https://github.com/vllm-project/vllm/pull/51840) Return HIT_PENDING when KV promotion is triggered
- [#52223](https://github.com/vllm-project/vllm/pull/52223) Reapply 50869
- [#51611](https://github.com/vllm-project/vllm/pull/51611) Fix stale rejection_sample_method and synthetic_acceptance_rate
- [#52171](https://github.com/vllm-project/vllm/pull/52171) Declare SupportsEagle3 on KimiLinearForCausalLM
- [#52288](https://github.com/vllm-project/vllm/pull/52288) DSpark: inherit the target's attention backend when the speculative config names none
- [#52356](https://github.com/vllm-project/vllm/pull/52356) Skip FP8 MLA prefill PS-metadata build for chunked-context batches
- [#52097](https://github.com/vllm-project/vllm/pull/52097) Add suffix_gpu drafter for Async Scheduling
- [#52228](https://github.com/vllm-project/vllm/pull/52228) Acceptance estimation for non-dspark adaptive verification
- [#52233](https://github.com/vllm-project/vllm/pull/52233) Cache adaptive verification profiles
- [#52548](https://github.com/vllm-project/vllm/pull/52548) Honor positive dynamic K in autoregressive drafting
- [#52522](https://github.com/vllm-project/vllm/pull/52522) Batch-invariant support for speculative decoding
- [#51981](https://github.com/vllm-project/vllm/pull/51981) Add per-request prefix-cache write policy
- [#52530](https://github.com/vllm-project/vllm/pull/52530) Fail requests the KV cache pool can never hold instead of retrying them forever
- [#52495](https://github.com/vllm-project/vllm/pull/52495) Count SWA in-flight KV once per pool, not per request
- [#52287](https://github.com/vllm-project/vllm/pull/52287) Preserve SWA replay windows after EAGLE tail pop
- [#52244](https://github.com/vllm-project/vllm/pull/52244) Restore hybrid GDN prefix-cache hits under MTP spec decoding
- [#52103](https://github.com/vllm-project/vllm/pull/52103) Carry request provenance through stored events
- [#52022](https://github.com/vllm-project/vllm/pull/52022) Fix store threshold admission counting
- [#52296](https://github.com/vllm-project/vllm/pull/52296) Coordinate mmap host registration
- [#52216](https://github.com/vllm-project/vllm/pull/52216) Promote prefix_cache_retention_interval to an argument
- [#52470](https://github.com/vllm-project/vllm/pull/52470) Abort async store jobs on preemption in Mooncake connector
- [#52273](https://github.com/vllm-project/vllm/pull/52273) Guards on the partial-hash hit retry
- [#52272](https://github.com/vllm-project/vllm/pull/52272) Revalidate exact partial-hash hit boundaries
- [#52087](https://github.com/vllm-project/vllm/pull/52087) Preserve constant effective K schedule semantics
- [#52295](https://github.com/vllm-project/vllm/pull/52295) Sync speculative draft tokens across PP ranks
- [#52477](https://github.com/vllm-project/vllm/pull/52477) Drive grammar masks from GPU logit counts
- [#52072](https://github.com/vllm-project/vllm/pull/52072) Apply suppress_tokens on the Gemma 4 MTP sparse path
- [#52487](https://github.com/vllm-project/vllm/pull/52487) Reload speculative draft weights after Level 2 sleep wake
- [#52220](https://github.com/vllm-project/vllm/pull/52220) Preserve embedded MTP draft runtime settings
- [#52073](https://github.com/vllm-project/vllm/pull/52073) Test extract_hidden_states on NemotronH hybrid models
- [#52269](https://github.com/vllm-project/vllm/pull/52269) DSpark under DCP
- [#52527](https://github.com/vllm-project/vllm/pull/52527) Report shared-prefix tokens lost to a missing sparse-retention checkpoint

</details>

<details>
<summary>Bugfixes (48)</summary>

- [#52003](https://github.com/vllm-project/vllm/pull/52003) Mypy fix for vllm/model_executor/models/[cC][dD]
- [#51139](https://github.com/vllm-project/vllm/pull/51139) Invalidate retained PyNvVideoCodec decoder after failure
- [#52058](https://github.com/vllm-project/vllm/pull/52058) Bound KV block zeroing launch geometry
- [#51120](https://github.com/vllm-project/vllm/pull/51120) Return 400 for invalid PyNvVideoCodec video input
- [#51664](https://github.com/vllm-project/vllm/pull/51664) Fix chart resource references
- [#49613](https://github.com/vllm-project/vllm/pull/49613) Clear empty side on thinking-budget asymmetric SWAP
- [#52092](https://github.com/vllm-project/vllm/pull/52092) Ship triton-cpu wheel and fix several hardcoded pin_memory=True
- [#52401](https://github.com/vllm-project/vllm/pull/52401) Pick the DeepSeek V4 eager cudagraph region per model runner
- [#50221](https://github.com/vllm-project/vllm/pull/50221) Enforce audio decode duration limit in NanoNemotronVL
- [#50595](https://github.com/vllm-project/vllm/pull/50595) Mask request stop tokens in xgrammar until grammar terminates
- [#51796](https://github.com/vllm-project/vllm/pull/51796) Reject NUL byte in structured_outputs.regex
- [#49505](https://github.com/vllm-project/vllm/pull/49505) Avoid repeated layerwise reload warning scans
- [#50874](https://github.com/vllm-project/vllm/pull/50874) Size monolithic routing replay buffer for DP
- [#51989](https://github.com/vllm-project/vllm/pull/51989) Fix Cosmos3-Edge processor after transformers 5.15 release
- [#47692](https://github.com/vllm-project/vllm/pull/47692) Fix --data-parallel-start-rank 0 being treated as unset
- plus 33 more minor bugfixes

</details>

<details>
<summary>Tests, CI & build (53)</summary>

- [#51280](https://github.com/vllm-project/vllm/pull/51280) Solidify entrypoint LLM lifecycle
- [#43107](https://github.com/vllm-project/vllm/pull/43107) Check for GPU<->CPU syncs during CI
- [#51998](https://github.com/vllm-project/vllm/pull/51998) Upstream Cohere parser fixes + tests
- [#50804](https://github.com/vllm-project/vllm/pull/50804) Stabilize tensor IPC multiprocessing tests
- [#51911](https://github.com/vllm-project/vllm/pull/51911) Add registry layer cache to x86 CPU image build
- [#52108](https://github.com/vllm-project/vllm/pull/52108) Add xpu wheel release to release pipeline
- [#51877](https://github.com/vllm-project/vllm/pull/51877) Speed Up ROCm Skinny GEMM Tests
- [#51759](https://github.com/vllm-project/vllm/pull/51759) Publish XPU Triton shim index
- [#49515](https://github.com/vllm-project/vllm/pull/49515) Select CPU platform for native no-GPU jobs
- [#52064](https://github.com/vllm-project/vllm/pull/52064) Mirror external test assets in vLLM S3
- plus 43 more minor CI and test updates

</details>

<details>
<summary>Docs (6)</summary>

- [#51729](https://github.com/vllm-project/vllm/pull/51729) Rewrite weight-transfer docs; standardize examples
- [#51878](https://github.com/vllm-project/vllm/pull/51878) vLLM Recipes conversion: support different data types variants and strategies
- [#52134](https://github.com/vllm-project/vllm/pull/52134) Fix WhisperEncoderLayer.forward docstring in dots3_note
- [#52289](https://github.com/vllm-project/vllm/pull/52289) Update model support information
- [#52259](https://github.com/vllm-project/vllm/pull/52259) Add DBO overlap schedule diagram to dbo.md
- [#52200](https://github.com/vllm-project/vllm/pull/52200) Document NIXL KV connector metrics aggregation semantics

</details>

<details>
<summary>Refactors & Misc (15)</summary>

- [#52221](https://github.com/vllm-project/vllm/pull/52221) Remove dead code for quantization
- [#52147](https://github.com/vllm-project/vllm/pull/52147) Standardise weight tying on ParallelLMHead.tie_weights
- [#51917](https://github.com/vllm-project/vllm/pull/51917) Unify uniform decode token count helper
- [#51251](https://github.com/vllm-project/vllm/pull/51251) Configure custom encoder cache managers from VllmConfig
- [#48684](https://github.com/vllm-project/vllm/pull/48684) Remove override_attention_dtype
- [#52035](https://github.com/vllm-project/vllm/pull/52035) Update DeepGEMM pin to deepseek-ai nv_dev tip
- [#51841](https://github.com/vllm-project/vllm/pull/51841) Avoid long-blocking H2D copies in ViT
- [#52173](https://github.com/vllm-project/vllm/pull/52173) Apply logit softcapping in Transformers modelling backend
- [#52076](https://github.com/vllm-project/vllm/pull/52076) Clearer comments in BlockPool.free_blocks()
- [#52543](https://github.com/vllm-project/vllm/pull/52543) Expose LinearBase geometry on ParallelLMHead so lm_head can be quantized
- [#52281](https://github.com/vllm-project/vllm/pull/52281) Give EngineCore cleanup grace after request abort
- [#52282](https://github.com/vllm-project/vllm/pull/52282) Harden RemoteVLLMServer GPU cleanup checks
- [#51927](https://github.com/vllm-project/vllm/pull/51927) Use common sp utils for Qwen3.5 MoE
- [#52240](https://github.com/vllm-project/vllm/pull/52240) Clarify MXFP4 oracle for gpt-oss vs others
- [#52251](https://github.com/vllm-project/vllm/pull/52251) Add debug stat for zhongxin

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: e97ac44d65c38de58404512fb361c66c0adb9281da3f4b153c03e388e9c097f2 -->
