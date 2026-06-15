# vllm: PR digest (2026-06-10 to 2026-06-14)

_185 merged, 312 newly opened - source vllm-project/vllm, generated 2026-06-14T22:23:13Z_

## TL;DR
- **Models**: DeepSeek and Gemma dominated this window. DeepSeek V4 saw major in-progress work for hardware-agnostic definitions and PP/PD disaggregated serving, while Gemma gained merged DiffusionGemma support and in-progress Gemma4 ViT/parser rewrites.
- **New Architecture**: A massive newly-opened PR brings support for the MiniMax M3 model, spanning FlashInfer/Triton attention, MoE, and multimodal components.
- **Kernels & Quantization**: Significant performance wins for FP8 and MoE, highlighted by merged Helion kernels for dynamic per-token FP8 quantization and the migration of MoE, Marlin, and Machete kernels to the Torch stable ABI.
- **Distributed & KV Cache**: Disaggregated serving took a leap forward with merged Nixl KV Connector support for pushing KV from prefill to decode, alongside in-progress Mooncake and MoRIIO integrations for TP/PP/PD dispatch.

## Most important PRs
- **`[#45381](https://github.com/vllm-project/vllm/pull/45381)` (Opened) [Model] Add MiniMax M3 support**
  A massive 15k-line addition introducing support for the MiniMax M3 model, wiring up FlashInfer/Triton attention, MoE, and multimodal components across AMD, Intel, and NVIDIA hardware.
- **`[#35264](https://github.com/vllm-project/vllm/pull/35264)` (Merged) [KV Connector]: Support KV push from Prefill to Decode node using Nixl KV Connector**
  Enables pushing KV cache directly from prefill to decode nodes, a major architectural step for disaggregated serving and reducing time-to-first-token in split setups.
- **`[#33790](https://github.com/vllm-project/vllm/pull/33790)` (Merged) [Kernel][Helion][1/N] Add Helion kernel for dynamic_per_token_scaled_fp8_quant**
  Introduces the Helion kernel for dynamic per-token FP8 quantization on NVIDIA GPUs, significantly advancing FP8 inference performance.
- **`[#39612](https://github.com/vllm-project/vllm/pull/39612)` (Merged) [Migration] Migrate GGUF quantization support to plugin**
  Decouples GGUF quantization into a plugin architecture, touching over 50 files and streamlining the core quantization codebase for easier maintenance.
- **`[#45112](https://github.com/vllm-project/vllm/pull/45112)` (Opened) [Draft] DeepSeek V4 PP/PD disaggregated serving with Mooncake**
  Wires up DeepSeek V4 for pipeline-parallel and prefill-decode disaggregated serving using the Mooncake KV store.

## More changes by area

<details>
<summary>Performance (11)</summary>

- `[#44400](https://github.com/vllm-project/vllm/pull/44400)` Enable W4A16 FlyDSL MoE on ROCm
- `[#44899](https://github.com/vllm-project/vllm/pull/44899)` Add Flash-decode split-K decode attention kernel for DeepSeek on ROCm
- `[#45103](https://github.com/vllm-project/vllm/pull/45103)` Fuse inverse-RoPE and cache bf16 wo_a in o-projection for DeepSeek on ROCm
- `[#44572](https://github.com/vllm-project/vllm/pull/44572)` Improve SM90 cutlass fp8 mm performance by 180~290% with odd M swap_ab
- `[#45322](https://github.com/vllm-project/vllm/pull/45322)` Use native DSA indexer decode path for next_n > 2 on SM100
- `[#45566](https://github.com/vllm-project/vllm/pull/45566)` Use bisect for mm feature lookup in model runner v2
- `[#45074](https://github.com/vllm-project/vllm/pull/45074)` Pin MLA chunked-context metadata tensors for non-blocking H2D copies
- `[#45126](https://github.com/vllm-project/vllm/pull/45126)` Add NVIDIA-tuned tile configs and PID swizzling for triton_scaled_mm
- `[#45142](https://github.com/vllm-project/vllm/pull/45142)` Tune fused_moe for Qwen3-Next-80B on H20-3e for 1.5x speedup
- `[#45379](https://github.com/vllm-project/vllm/pull/45379)` Add tuned fused_moe FP8 config for RTX 5090
- `[#45484](https://github.com/vllm-project/vllm/pull/45484)` Lazy-import boto3 to skip ~300ms on cold-start

</details>

<details>
<summary>Kernels & attention (18)</summary>

- `[#45176](https://github.com/vllm-project/vllm/pull/45176)` Migrate Marlin kernels to torch stable ABI
- `[#45304](https://github.com/vllm-project/vllm/pull/45304)` Migrate Machete kernels to torch stable ABI
- `[#41797](https://github.com/vllm-project/vllm/pull/41797)` Add triton diff-kv backend for mimo
- `[#45295](https://github.com/vllm-project/vllm/pull/45295)` Consolidate Marlin thread-tile padding across all dense Marlin paths
- `[#44260](https://github.com/vllm-project/vllm/pull/44260)` Add the QuantizedActivation linear-kernel contract
- `[#44583](https://github.com/vllm-project/vllm/pull/44583)` Add per-region KV transfer classification for mixed full-attn + MLA groups
- `[#45089](https://github.com/vllm-project/vllm/pull/45089)` Use std::bit_cast for type punning in CPU kernels
- `[#45270](https://github.com/vllm-project/vllm/pull/45270)` Add cuteDSL JIT warmup and cache init
- `[#45151](https://github.com/vllm-project/vllm/pull/45151)` Fuse per-group FP8 dynamic quant into Triton attention epilogue
- `[#45111](https://github.com/vllm-project/vllm/pull/45111)` Re-enable cross-layer KV cache layout for MLA via stride-aware kernels
- `[#45573](https://github.com/vllm-project/vllm/pull/45573)` Port MLARoPEKVCacheCatFusionPass to manual fusion
- `[#45227](https://github.com/vllm-project/vllm/pull/45227)` Fix ROCm MLA MTP decode size verification and CUDA-graph padding
- `[#45234](https://github.com/vllm-project/vllm/pull/45234)` Enable ROCm Attention Sinks and Connector-Friendly KV Layouts
- `[#45391](https://github.com/vllm-project/vllm/pull/45391)` Refine CPU attention frontend
- `[#45452](https://github.com/vllm-project/vllm/pull/45452)` Add opt-in two-stream and launch-elision latency optimizations for Kimi-K2.6-NVFP4 decode
- `[#45426](https://github.com/vllm-project/vllm/pull/45426)` Enable DCP on the fp8 mixed-batch path and MTP with full cudagraphs for FlashMLA sparse
- `[#45187](https://github.com/vllm-project/vllm/pull/45187)` Add NVFP4 KV 4-over-6 scale search
- `[#45120](https://github.com/vllm-project/vllm/pull/45120)` Fuse softmax into grouped_topk CUDA kernel

</details>

<details>
<summary>MoE & quantization (15)</summary>

- `[#36902](https://github.com/vllm-project/vllm/pull/36902)` Add Helion kernel for per_token_group_fp8_quant
- `[#44565](https://github.com/vllm-project/vllm/pull/44565)` Migrate MoE kernels to torch stable ABI
- `[#43409](https://github.com/vllm-project/vllm/pull/43409)` Support CPU W4A16 INT4 MoE
- `[#44478](https://github.com/vllm-project/vllm/pull/44478)` Enable oneDNN W8A8 INT8 to run on RISC-V
- `[#45136](https://github.com/vllm-project/vllm/pull/45136)` Support int4 group_size=32 W4A16 MoE on XPU
- `[#44893](https://github.com/vllm-project/vllm/pull/44893)` Pass GateMode.INTERLEAVE for MXFP4 W4A16 fused MoE on ROCm
- `[#44804](https://github.com/vllm-project/vllm/pull/44804)` Add Hybrid CDNA4 swizzle gate for A8W4 MoE on ROCm
- `[#45239](https://github.com/vllm-project/vllm/pull/45239)` Fix n_local_physical_experts bookkeeping in DeepSeek-V2 and Qwen3-MoE
- `[#45567](https://github.com/vllm-project/vllm/pull/45567)` Add fused MXFP8 MoE for gfx94x on ROCm
- `[#45226](https://github.com/vllm-project/vllm/pull/45226)` Route batched expert layout through flat-reshape wrapper for AITER FP8
- `[#45182](https://github.com/vllm-project/vllm/pull/45182)` Integrate TRTLLM BF16 MoE Modular Kernel
- `[#45364](https://github.com/vllm-project/vllm/pull/45364)` Port RMSNormQuantFusionPass to manual fusion for fp8 static per-tensor and dynamic per-token
- `[#45331](https://github.com/vllm-project/vllm/pull/45331)` Add support for mixed input/weight dtype to rms norm quant fusion ops
- `[#45415](https://github.com/vllm-project/vllm/pull/45415)` Complete final _C library kernel migration
- `[#45428](https://github.com/vllm-project/vllm/pull/45428)` Add single-read fast path for fused RMSNorm + dynamic per-token FP8 quant

</details>

<details>
<summary>Model support (13)</summary>

- `[#45163](https://github.com/vllm-project/vllm/pull/45163)` Add DiffusionGemma Support
- `[#45131](https://github.com/vllm-project/vllm/pull/45131)` Deprecate 1st generation Qwen and QwenVL models
- `[#44930](https://github.com/vllm-project/vllm/pull/44930)` Add encoder CUDA graph support to Lfm2VL
- `[#45129](https://github.com/vllm-project/vllm/pull/45129)` Remove Mono-InternVL (InternLM2VEForCausalLM)
- `[#45127](https://github.com/vllm-project/vllm/pull/45127)` Remove obsolete ERNIE models
- `[#45240](https://github.com/vllm-project/vllm/pull/45240)` Fix DeepSeek-V4 MTP sync with upstream fixes on XPU
- `[#45546](https://github.com/vllm-project/vllm/pull/45546)` Implement EAGLE3 support on the AMD MiniMax M3
- `[#45319](https://github.com/vllm-project/vllm/pull/45319)` Enable Dflash support for Qwen3NextForCausalLM targets
- `[#45470](https://github.com/vllm-project/vllm/pull/45470)` Add hardware-agnostic model definition for DeepSeek V4
- `[#45574](https://github.com/vllm-project/vllm/pull/45574)` Add Gemma4 native ViT re-implementation for LoRA and TP compatibility
- `[#45210](https://github.com/vllm-project/vllm/pull/45210)` Add io processor for query/document embeddings from ColBERT
- `[#45284](https://github.com/vllm-project/vllm/pull/45284)` Fuse q/k/v and gate/up linear groups in Transformers backend
- `[#45123](https://github.com/vllm-project/vllm/pull/45123)` Migrate deepseekv2 to vllm/models

</details>

<details>
<summary>Parallelism & scheduling (18)</summary>

- `[#35669](https://github.com/vllm-project/vllm/pull/35669)` Add offloading manager stats
- `[#44193](https://github.com/vllm-project/vllm/pull/44193)` Add KV-Cache multi-tier offloading async batched lookup
- `[#44594](https://github.com/vllm-project/vllm/pull/44594)` Add kvcache watermark to reduce preemptions
- `[#44774](https://github.com/vllm-project/vllm/pull/44774)` Add Mooncake store prefix-cache retention interval for sparse attention
- `[#44733](https://github.com/vllm-project/vllm/pull/44733)` Add parallel-agnostic fs-tier cache for single full-attention group
- `[#42206](https://github.com/vllm-project/vllm/pull/42206)` Add group-aware KV cache capacity to vllm:cache_config_info
- `[#37898](https://github.com/vllm-project/vllm/pull/37898)` Add Marconi-style admission policy for hybrid cache
- `[#44978](https://github.com/vllm-project/vllm/pull/44978)` Reject NCCL-based EPLB communicators with async EPLB
- `[#45230](https://github.com/vllm-project/vllm/pull/45230)` Fix MoRIIO READ-mode stability (completion IDs, DP routing, drain, keepalive)
- `[#45205](https://github.com/vllm-project/vllm/pull/45205)` Support per-group descriptor views for heterogeneous KV cache specs in multi-view nixl connector
- `[#45237](https://github.com/vllm-project/vllm/pull/45237)` Avoid mixed batch on spec-dec D-node via P-to-D handoff
- `[#45395](https://github.com/vllm-project/vllm/pull/45395)` Implement snapshot puncture for distributed attention
- `[#45211](https://github.com/vllm-project/vllm/pull/45211)` Offload NIXL Pull Connector READ submission to a dedicated reader thread
- `[#45228](https://github.com/vllm-project/vllm/pull/45228)` Add MoRIIO multi-node TP prefill→decode dispatch via published host list
- `[#45561](https://github.com/vllm-project/vllm/pull/45561)` Preempt running requests for higher-priority waiting requests at max_num_seqs
- `[#45443](https://github.com/vllm-project/vllm/pull/45443)` Support NIXL hetero block size
- `[#45499](https://github.com/vllm-project/vllm/pull/45499)` Register Mooncake group KV cache by layers
- `[#45349](https://github.com/vllm-project/vllm/pull/45349)` Allow large Mamba aligned batches with single-block prefill cap

</details>

<details>
<summary>API & serving (26)</summary>

- `[#45003](https://github.com/vllm-project/vllm/pull/45003)` Support strict mode for tool calling
- `[#45171](https://github.com/vllm-project/vllm/pull/45171)` Refactor Chat Completions Harmony for non-streaming path
- `[#44624](https://github.com/vllm-project/vllm/pull/44624)` Add Python bridge for Rust tool parsers
- `[#45104](https://github.com/vllm-project/vllm/pull/45104)` Refactor Chat Completions Streaming Harmony and fix bugs
- `[#43606](https://github.com/vllm-project/vllm/pull/43606)` Add `/derender` endpoints for disaggregated postprocessing
- `[#44887](https://github.com/vllm-project/vllm/pull/44887)` Populate `cached_token_count` in Rust Frontend responses
- `[#44552](https://github.com/vllm-project/vllm/pull/44552)` Add seed_oss and step3p5 reasoning parsers to Rust Frontend
- `[#45216](https://github.com/vllm-project/vllm/pull/45216)` Add standalone `granite4` tool parser to Rust Frontend
- `[#44884](https://github.com/vllm-project/vllm/pull/44884)` Extract shared options in route helper params for Rust Frontend
- `[#45431](https://github.com/vllm-project/vllm/pull/45431)` Deprecate ResponsesParser wrapper and inline parsing into ParsableContext
- `[#35022](https://github.com/vllm-project/vllm/pull/35022)` Support structured outputs for beam search
- `[#43965](https://github.com/vllm-project/vllm/pull/43965)` Support continuous_usage_stats stream option in Rust Frontend
- `[#45190](https://github.com/vllm-project/vllm/pull/45190)` Unify Response API to use parser.parse() like Chat Completion API
- `[#44448](https://github.com/vllm-project/vllm/pull/44448)` Add `vllm:tool_call_parser_invocations_total` Prometheus metric
- `[#35415](https://github.com/vllm-project/vllm/pull/35415)` Support prompt parameter in v1/audio/transcriptions for qwen3-asr
- `[#45396](https://github.com/vllm-project/vllm/pull/45396)` Support strict mode for tool calling with ResponsesAPI
- `[#45588](https://github.com/vllm-project/vllm/pull/45588)` Replace legacy Gemma4 parsers with engine-based implementation
- `[#45413](https://github.com/vllm-project/vllm/pull/45413)` Add Streaming Parser Engine and new Qwen3 Parser
- `[#45518](https://github.com/vllm-project/vllm/pull/45518)` Return idempotent signal from /sleep endpoint when engine is already sleeping
- `[#45514](https://github.com/vllm-project/vllm/pull/45514)` Add batch_split_message tokenizer mode for lossless segmented encoding
- `[#45453](https://github.com/vllm-project/vllm/pull/45453)` Add /health/decode forward-progress endpoint
- `[#45569](https://github.com/vllm-project/vllm/pull/45569)` Add input validation to gRPC and HTTP stop_token_ids in Rust Frontend
- `[#45137](https://github.com/vllm-project/vllm/pull/45137)` Add external→internal request-id map for abort() in Rust Frontend
- `[#45551](https://github.com/vllm-project/vllm/pull/45551)` Add /readiness/stages endpoint for model-ready autoscaling
- `[#45512](https://github.com/vllm-project/vllm/pull/45512)` Enforce allowed_tools at execution time for Responses API
- plus 1 more minor API update

</details>

<details>
<summary>Speculative Decoding (11)</summary>

- `[#44586](https://github.com/vllm-project/vllm/pull/44586)` Add DFlash support for MRV2 Spec Decode
- `[#32374](https://github.com/vllm-project/vllm/pull/32374)` Add Dynamic Speculative Decoding for V1
- `[#43805](https://github.com/vllm-project/vllm/pull/43805)` Improve hidden states extraction
- `[#39419](https://github.com/vllm-project/vllm/pull/39419)` Reduce TP communication for large-vocab draft models speculative decoding
- `[#45343](https://github.com/vllm-project/vllm/pull/45343)` Fix MiMo-V2.5-Pro-FP4 DFlash speculative decoding and AL
- `[#45229](https://github.com/vllm-project/vllm/pull/45229)` Relax acceptance for thinking-phase tokens in V1 Spec Decode
- `[#45400](https://github.com/vllm-project/vllm/pull/45400)` Add Grammar spec dec (jump decoding) for structured outputs in MRV2
- `[#45181](https://github.com/vllm-project/vllm/pull/45181)` Support mixed KV page sizes for DFlash
- `[#45450](https://github.com/vllm-project/vllm/pull/45450)` Admit MTP/EAGLE spec-decode steps and sliding-window layers into Triton 3D flash-decoding path
- `[#45369](https://github.com/vllm-project/vllm/pull/45369)` Avoid materializing target probabilities in rejection sampling
- `[#45280](https://github.com/vllm-project/vllm/pull/45280)` Add role-aware optimizations for Spec decoding in PD

</details>

<details>
<summary>Multimodal (7)</summary>

- `[#40660](https://github.com/vllm-project/vllm/pull/40660)` Support ViT full cudagraphs for mllama4
- `[#45106](https://github.com/vllm-project/vllm/pull/45106)` Add PixelPrune visual token pruning for Qwen3-VL
- `[#45545](https://github.com/vllm-project/vllm/pull/45545)` Add Kimi video chunk splitting
- `[#45254](https://github.com/vllm-project/vllm/pull/45254)` Support ViT full CUDA graph for Ernie-4.5-VL image inference
- `[#45203](https://github.com/vllm-project/vllm/pull/45203)` Add lossy keyframe-only video loader (pyav_keyframes)
- `[#45555](https://github.com/vllm-project/vllm/pull/45555)` Add Qwen2-VL/Qwen2.5-VL processor-mapped video loader
- `[#45458](https://github.com/vllm-project/vllm/pull/45458)` Report multimodal token counts in usage.prompt_tokens_details

</details>

<details>
<summary>Hardware & arch (8)</summary>

- `[#45398](https://github.com/vllm-project/vllm/pull/45398)` Add CuMemTagBackend for tag-selective offload
- `[#45370](https://github.com/vllm-project/vllm/pull/45370)` Add Fused K-RoPE + static FP8 per-tensor KV Cache write
- `[#45559](https://github.com/vllm-project/vllm/pull/45559)` Extend skinny gemm N=5 to N=8 cases on GFX12 (RDNA4) using SWMMAC optimization
- `[#45517](https://github.com/vllm-project/vllm/pull/45517)` Take init-time memory snapshot before NCCL init to avoid asymmetric OOM on TP+PP consumer GPUs
- `[#45554](https://github.com/vllm-project/vllm/pull/45554)` Quiesce torch.distributed groups around VMM mutations in cumem
- `[#45565](https://github.com/vllm-project/vllm/pull/45565)` Validate VA/handle invariants and recover from wake-time cuMemMap failures in cumem
- `[#45552](https://github.com/vllm-project/vllm/pull/45552)` Stream-sync before unmap and at wake_up exit to prevent CUDART illegal-memory crash
- `[#45243](https://github.com/vllm-project/vllm/pull/45243)` Enable BF16 on RISC-V VLEN=256 hardware

</details>

<details>
<summary>Tests, CI & build (11)</summary>

- `[#44992](https://github.com/vllm-project/vllm/pull/44992)` Add deprecations for v0.23 and v0.24
- `[#45277](https://github.com/vllm-project/vllm/pull/45277)` Fix CUDA arch build coverage gaps
- `[#45274](https://github.com/vllm-project/vllm/pull/45274)` Add ci-fetch-log.sh to fetch all failed jobs from a build URL or PR number
- `[#44981](https://github.com/vllm-project/vllm/pull/44981)` Unify Rust artifact builds with setuptools-rust
- `[#44823](https://github.com/vllm-project/vllm/pull/44823)` Defer AITER sampler import and isolate server test PYTHONPATH on ROCm
- `[#44923](https://github.com/vllm-project/vllm/pull/44923)` Upgrade CUDA Dockerfiles from GCC 10 to GCC 12 for C++20 compatibility
- `[#45170](https://github.com/vllm-project/vllm/pull/45170)` Move MI300 tests to MI325 until cluster is stabilized
- `[#45586](https://github.com/vllm-project/vllm/pull/45586)` Add E2E test suite for sleep/wake/pause/weight-update lifecycle
- `[#45264](https://github.com/vllm-project/vllm/pull/45264)` Improve Docker image build for IBM Power using prebuilt wheels
- `[#45082](https://github.com/vllm-project/vllm/pull/45082)` Update PyTorch to 2.12.1, torchvision to 0.27.1, triton to 3.7.1
- `[#45246](https://github.com/vllm-project/vllm/pull/45246)` Enable sccache for Rust build under CUDA/ROCm

</details>

<details>
<summary>Bugfixes (20)</summary>

- `[#44243](https://github.com/vllm-project/vllm/pull/44243)` Fix Mamba prefix cache hit rate in PD disaggregation
- `[#44680](https://github.com/vllm-project/vllm/pull/44680)` Validate out-of-vocab token ids in request params for Rust Frontend
- `[#45287](https://github.com/vllm-project/vllm/pull/45287)` Fix Anthropic tool_use content handling dropping args
- `[#44683](https://github.com/vllm-project/vllm/pull/44683)` Fix missing added tokens in hf/fastokens tokenizer for Rust Frontend
- `[#44424](https://github.com/vllm-project/vllm/pull/44424)` Fix CPU memory leak related to not cleaning up old remotes data
- `[#45347](https://github.com/vllm-project/vllm/pull/45347)` Avoid prematurely freeing cached mm encoder outputs
- `[#39091](https://github.com/vllm-project/vllm/pull/39091)` Surface reasoning as content when thinking is unterminated in Nemotron V3
- `[#45025](https://github.com/vllm-project/vllm/pull/45025)` Stop unescaping XML-style tool-call parameter values in Rust Frontend
- `[#45217](https://github.com/vllm-project/vllm/pull/45217)` Initialize missing attributes in mistral eagle
- `[#44921](https://github.com/vllm-project/vllm/pull/44921)` Lazily import the humming quantization backend
- `[#45206](https://github.com/vllm-project/vllm/pull/45206)` Close MooncakeDistributedStore on connector teardown
- `[#44599](https://github.com/vllm-project/vllm/pull/44599)` Fix Mamba CPU Offloading
- `[#43300](https://github.com/vllm-project/vllm/pull/43300)` Fix broken profile_modular_kernel.py
- `[#43877](https://github.com/vllm-project/vllm/pull/43877)` Fix scheduler KV connector stats aggregation
- `[#45286](https://github.com/vllm-project/vllm/pull/45286)` Return 400 for prompt-validation submit errors in Rust Frontend
- `[#44744](https://github.com/vllm-project/vllm/pull/44744)` Fix remote DoS via invalid recovered token reinjection
- `[#45252](https://github.com/vllm-project/vllm/pull/45252)` Fix DoS via prompt_embeds on M-RoPE models
- `[#44814](https://github.com/vllm-project/vllm/pull/44814)` Fix layerwise reload dropping params after a composed weight loader
- `[#45244](https://github.com/vllm-project/vllm/pull/45244)` Fix ImageSize (W,H) order for placeholder token calculation in minicpmv4_6
- plus 70 more minor bugfixes

</details>

<details>
<summary>Refactors (5)</summary>

- `[#44596](https://github.com/vllm-project/vllm/pull/44596)` Extract parsing logic into MistralParser
- `[#45081](https://github.com/vllm-project/vllm/pull/45081)` Remove dead states from chat completion serving
- `[#45011](https://github.com/vllm-project/vllm/pull/45011)` Rename rocm_moe.py to rocm_moe_rdna.py
- `[#45454](https://github.com/vllm-project/vllm/pull/45454)` Remove dead quantization code and tests
- `[#45463](https://github.com/vllm-project/vllm/pull/45463)` Remove `Fp8OnlineLinearMethod` as scheduled

</details>

<details>
<summary>Docs (7)</summary>

- `[#44055](https://github.com/vllm-project/vllm/pull/44055)` Document KV Transfer stat logging and Prometheus metrics
- `[#43756](https://github.com/vllm-project/vllm/pull/43756)` Make non-standard conversation_id payload opt-in for benchmark_serving_multi_turn
- `[#45301](https://github.com/vllm-project/vllm/pull/45301)` Add section about coding style to AGENTS.md
- `[#45262](https://github.com/vllm-project/vllm/pull/45262)` Only enable PR docs builds manually
- `[#45218](https://github.com/vllm-project/vllm/pull/45218)` Add redirect for moved lmcache examples page
- `[#45107](https://github.com/vllm-project/vllm/pull/45107)` Add multi-tenant sleep-mode operational guidance
- `[#45077](https://github.com/vllm-project/vllm/pull/45077)` Add GKE Autopilot deployment & Prometheus monitoring guide

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
