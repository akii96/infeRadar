# vllm: PR digest (2026-08-02 to 2026-08-06)

_183 merged, 295 newly opened - source vllm-project/vllm, generated 2026-08-06T11:33:47Z_

## TL;DR
- **Model Focus**: DeepSeek (V4 Flash, IndexCache, CPU MLA) and Kimi-K3 (ROCm MI325X support, FlashKDA, MoE sharding) dominated model-specific attention, alongside new support for Ling 3.0 and MiniMax-M3.
- **Architecture & Memory**: Major in-progress architectural shifts include a massive newly-opened PR for an extensible (growable) KV cache and merged support for E/P/D (Encoder/Prefill/Decode) disaggregation.
- **Kernels & Quantization**: Significant kernel churn this window, highlighted by newly opened work on ZoomKV and Helion FP8 block-scaled linear kernels for NVIDIA, plus merged AITER MoE/quantization support for AMD ROCm.
- **Overall Direction**: The engine is heavily optimizing for next-gen MoE and MLA architectures (DeepSeek, Kimi) while pushing boundaries on distributed inference (disaggregation, island-aware allreduce) and FP8/MXFP4 quantization across both NVIDIA and AMD hardware.

## Most important PRs
**[#50779](https://github.com/vllm-project/vllm/pull/50779) Extensible (growable) KV cache** (Newly opened)
Re-architects the KV cache to support dynamic growth, touching almost all components to enable flexible memory management and prevent fragmentation.

**[#50914](https://github.com/vllm-project/vllm/pull/50914) Add HelionFP8BlockScaledMMLinearKernel** (Newly opened)
Adds a massive new NVIDIA kernel backend for highly optimized FP8 block-scaled matrix multiplications, significantly boosting throughput for supported models.

**[#51045](https://github.com/vllm-project/vllm/pull/51045) Add Ling 3.0 Flash BF16, MTP, and parser support**
Introduces comprehensive support for the Ling 3.0 model family, including speculative decoding and parser integration for immediate deployment.

**[#38390](https://github.com/vllm-project/vllm/pull/38390) E/P/D disaggregation support**
Implements Encoder/Prefill/Decode disaggregation via the KV connector, a major architectural step for distributed inference efficiency and scaling.

**[#50133](https://github.com/vllm-project/vllm/pull/50133) Migrate unquantized MoE to the modular-kernel experts structure**
Refactors unquantized MoE on CPU to use the modular-kernel experts structure, significantly improving CPU inference architecture and maintainability.

## More changes by area

<details>
<summary>Performance (20)</summary>

- [#50716](https://github.com/vllm-project/vllm/pull/50716) Speed up multimodal placeholder and token-match scanning
- [#50992](https://github.com/vllm-project/vllm/pull/50992) Avoid quadratic ARC batch eviction in KV offload
- [#48825](https://github.com/vllm-project/vllm/pull/48825) Optimize H20 MoE config (e256 n512)
- [#51070](https://github.com/vllm-project/vllm/pull/51070) Combine multiple all-gather operations for K3 SP
- [#50912](https://github.com/vllm-project/vllm/pull/50912) Shard the shared expert for non-mega Kimi-K3 cases
- [#50904](https://github.com/vllm-project/vllm/pull/50904) Use skip top-k for GLM MTP cases
- [#51199](https://github.com/vllm-project/vllm/pull/51199) Add an adaptive prefill delayer for data-parallel serving
- [#50737](https://github.com/vllm-project/vllm/pull/50737) Optimize DSpark Markov head with addmm
- [#51238](https://github.com/vllm-project/vllm/pull/51238) Add O(delta) reasoning-end check for engine parsers
- [#51022](https://github.com/vllm-project/vllm/pull/51022) Downmix audio channels by slicing instead of reducing
- [#51055](https://github.com/vllm-project/vllm/pull/51055) Skip redundant num_accepted_tokens H2D copy after preprocess_mamba
- [#50936](https://github.com/vllm-project/vllm/pull/50936) Skip re-validating reused sampling params in streaming input loop
- [#50790](https://github.com/vllm-project/vllm/pull/50790) Precompute draft-to-target index mapping in eagle/dflash models
- [#51132](https://github.com/vllm-project/vllm/pull/51132) Use RVV FMA in FP32Vec transcendentals and INT4 GEMM on RISC-V
- [#50810](https://github.com/vllm-project/vllm/pull/50810) Consolidate performance benchmark datasets
- [#51155](https://github.com/vllm-project/vllm/pull/51155) Add cached tokens to vllm bench serve
- [#50849](https://github.com/vllm-project/vllm/pull/50849) Support MMVU in throughput benchmark
- [#51030](https://github.com/vllm-project/vllm/pull/51030) Add a timeout per socket without cancelling the full benchmark run
- [#50885](https://github.com/vllm-project/vllm/pull/50885) Capture FULL decode cudagraphs for spec-decode on FlashInfer native path
- [#51253](https://github.com/vllm-project/vllm/pull/51253) Shard Latent MoE up-projection for ROCm path

</details>

<details>
<summary>Kernels & attention (39)</summary>

- [#51165](https://github.com/vllm-project/vllm/pull/51165) Add ZoomKV v020 features and optimizations
- [#50032](https://github.com/vllm-project/vllm/pull/50032) Add MSA speculative decode verification for MiniMax-M3
- [#50294](https://github.com/vllm-project/vllm/pull/50294) Optimize FA4 mm_prefix range lookup
- [#49792](https://github.com/vllm-project/vllm/pull/49792) Add a CuTeDSL fused query kernel for SM100
- [#49791](https://github.com/vllm-project/vllm/pull/49791) Extend CuTe DSL skinny GEMM to GLM-5.2
- [#49453](https://github.com/vllm-project/vllm/pull/49453) Add MLA backend so DeepSeek-V2/V3 can run on CPU
- [#49389](https://github.com/vllm-project/vllm/pull/49389) Remove deprecated calculate_kv_scales runtime KV scale calculation
- [#43615](https://github.com/vllm-project/vllm/pull/43615) Enable AITER and FP8 inference on GFX120x
- [#50980](https://github.com/vllm-project/vllm/pull/50980) Support BF16 KV cache with FP8 weight in HPC attention backend
- [#50157](https://github.com/vllm-project/vllm/pull/50157) Add support for Flashinfer Mamba SSU algorithm selection
- [#50230](https://github.com/vllm-project/vllm/pull/50230) Programmatic dependent launch for DSA decode kernels
- [#50911](https://github.com/vllm-project/vllm/pull/50911) Enable fused non-causal TokenSpeed MLA for DSpark
- [#50818](https://github.com/vllm-project/vllm/pull/50818) Migrate FlashKDA to PyTorch stable ABI
- [#49664](https://github.com/vllm-project/vllm/pull/49664) Add torch as XPU linear backend
- [#50776](https://github.com/vllm-project/vllm/pull/50776) Skip fully masked key blocks in windowed Triton prefill
- [#51054](https://github.com/vllm-project/vllm/pull/51054) Support DeepSeek V4 flash on Turing (SM75)
- [#51244](https://github.com/vllm-project/vllm/pull/51244) Optimize MHC post + HC head + RMSNorm fusions for DeepSeek V4
- [#50907](https://github.com/vllm-project/vllm/pull/50907) Remove stale SDPA and skinny GEMM workarounds on ROCm
- [#51065](https://github.com/vllm-project/vllm/pull/51065) Support causal multi-token decode in TritonMLA
- [#51040](https://github.com/vllm-project/vllm/pull/51040) Extend FP8 asm MLA prefill to non-divisor small head counts
- [#51183](https://github.com/vllm-project/vllm/pull/51183) Write KDA decode output straight into the layer buffer on AMD
- [#50847](https://github.com/vllm-project/vllm/pull/50847) Return Kimi-K3 MLA output directly on ROCm
- [#50855](https://github.com/vllm-project/vllm/pull/50855) Skip fresh Kimi-K3 KDA state copies on ROCm
- [#51171](https://github.com/vllm-project/vllm/pull/51171) Reach FULL cudagraphs for AITER MLA speculative decoding
- [#51159](https://github.com/vllm-project/vllm/pull/51159) Defer tilelang import and relax has_tilelang
- [#51011](https://github.com/vllm-project/vllm/pull/51011) Fix fp8 KV cache decode on the AITER MLA backend
- [#50848](https://github.com/vllm-project/vllm/pull/50848) Fix CUDA graph profiling for long GDN warmups
- [#50903](https://github.com/vllm-project/vllm/pull/50903) Fix divergent warp collectives in partial NeoX QK-Norm+RoPE
- [#50909](https://github.com/vllm-project/vllm/pull/50909) Validate Kimi attention layer configuration
- [#50791](https://github.com/vllm-project/vllm/pull/50791) Size FlashInfer sparse MLA workspace for decode-context-parallel
- [#50870](https://github.com/vllm-project/vllm/pull/50870) Pass kv_cache_dtype as int to avoid stable-ABI host leak
- [#51202](https://github.com/vllm-project/vllm/pull/51202) Skip empty DeepSeek-V4 FlashInfer attention slices
- [#51252](https://github.com/vllm-project/vllm/pull/51252) Size sparse-indexer prefill buffer by compress_ratio for DeepSeek-V4
- [#50480](https://github.com/vllm-project/vllm/pull/50480) Add MLA decode accuracy and determinism tests
- [#51083](https://github.com/vllm-project/vllm/pull/51083) Relax MLA rope+cache test tolerances for bf16
- [#38771](https://github.com/vllm-project/vllm/pull/38771) Fix MLA kv_b_proj activation dtype with Marlin FP8
- [#50567](https://github.com/vllm-project/vllm/pull/50567) Enforce packed rows and op availability in AttnRes dispatch
- [#50915](https://github.com/vllm-project/vllm/pull/50915) Fix macOS build std::sqrt constexpr under libc++
- [#51215](https://github.com/vllm-project/vllm/pull/51215) List Intel XPU attention backends

</details>

<details>
<summary>MoE & quantization (44)</summary>

- [#49375](https://github.com/vllm-project/vllm/pull/49375) Add more AITER quantization/MoE kernel tests for ROCm
- [#44359](https://github.com/vllm-project/vllm/pull/44359) Share apply_moe_activation support metadata
- [#50721](https://github.com/vllm-project/vllm/pull/50721) Enable routed-experts capture for MRV2
- [#40372](https://github.com/vllm-project/vllm/pull/40372) Batch invariant NVFP4 MoE using cutlass
- [#50383](https://github.com/vllm-project/vllm/pull/50383) Shard the K3 Latent-MoE up-projection on large batches
- [#51125](https://github.com/vllm-project/vllm/pull/51125) Size and iterate w13 by shard count for non-gated MoE
- [#49932](https://github.com/vllm-project/vllm/pull/49932) Add block-wise scaled_mm for linear kernels
- [#50029](https://github.com/vllm-project/vllm/pull/50029) Preserve precision in online NVFP4 expert packing
- [#50697](https://github.com/vllm-project/vllm/pull/50697) Fuse shared-expert partial addition into the Lamport collective
- [#48476](https://github.com/vllm-project/vllm/pull/48476) Support MXFP8 linear weights for INC DeepSeek V4 model
- [#50942](https://github.com/vllm-project/vllm/pull/50942) Align TRTLLM MXFP4 autotune buckets
- [#50510](https://github.com/vllm-project/vllm/pull/50510) Support SiTU activation for Kimi-K3
- [#51217](https://github.com/vllm-project/vllm/pull/51217) Generalize masked activation for batched experts
- [#50817](https://github.com/vllm-project/vllm/pull/50817) Enable AITER MXFP4 MoE on gfx942 and optimize tile configurations for MI325X
- [#50876](https://github.com/vllm-project/vllm/pull/50876) Add manual silu quant fusion
- [#51248](https://github.com/vllm-project/vllm/pull/51248) Support AutoRound MXFP8 Qwen3 MoE models on XPU
- [#50949](https://github.com/vllm-project/vllm/pull/50949) Optimize routed FP8/MXFP4 MoE GEMM dispatch on CPU
- [#51006](https://github.com/vllm-project/vllm/pull/51006) Add Platform routing backend interface for MoE
- [#50813](https://github.com/vllm-project/vllm/pull/50813) Enable opt-in K3 SiTUv2 A8W4 routed MoE on Quark
- [#50814](https://github.com/vllm-project/vllm/pull/50814) Cache dequantized MXFP4 fallback weights in Quark
- [#51158](https://github.com/vllm-project/vllm/pull/51158) Enable CUTLASS MXFP4 W4A4 MoE on SM12x
- [#51077](https://github.com/vllm-project/vllm/pull/51077) Support MXFP8 dispatch
- [#51148](https://github.com/vllm-project/vllm/pull/51148) Enable GPTQ and AWQ quantization for s390x
- [#51204](https://github.com/vllm-project/vllm/pull/51204) Select linear backends per quantization
- [#51029](https://github.com/vllm-project/vllm/pull/51029) Forward SwiGLU clamp/alpha/beta in compressed-tensors W4A4 MXFP4 MoE
- [#50844](https://github.com/vllm-project/vllm/pull/50844) Bound token_id before the tid2eid gather in hash-MoE routing
- [#50859](https://github.com/vllm-project/vllm/pull/50859) Hotfix for `memory access fault` errors in AITER triton MOE routing
- [#51038](https://github.com/vllm-project/vllm/pull/51038) Fix MXFP4 conversion for FlashInfer CUTLASS
- [#48929](https://github.com/vllm-project/vllm/pull/48929) Fix MiniMax-M3 NVFP4 inference correctness
- [#50905](https://github.com/vllm-project/vllm/pull/50905) Add aiter per-token FP8 quant roundtrip and RMSNorm determinism tests
- [#51093](https://github.com/vllm-project/vllm/pull/51093) Preserve ModelOpt FP8 weight dimensions
- [#51002](https://github.com/vllm-project/vllm/pull/51002) Guard TrtLlm BF16 MoE LoRA gate on activation type
- [#49558](https://github.com/vllm-project/vllm/pull/49558) Filter packed expert weights during EP loading
- [#50728](https://github.com/vllm-project/vllm/pull/50728) Fix AITER MXFP4 oracle contract
- [#50807](https://github.com/vllm-project/vllm/pull/50807) Fix w4a4 model in INC
- [#48861](https://github.com/vllm-project/vllm/pull/48861) NVFP4 quantization out_dtype should match model dtype
- [#50761](https://github.com/vllm-project/vllm/pull/50761) Preserve MoE correction bias in FP32 for Kimi-K3
- [#50405](https://github.com/vllm-project/vllm/pull/50405) Fix test_kv_scale_reload failed
- [#51177](https://github.com/vllm-project/vllm/pull/51177) Fix chunked prefill requirement for mamba cache mode 'align'
- [#50928](https://github.com/vllm-project/vllm/pull/50928) Pad the MoE intermediate by the effective shard count for Kimi K3
- [#50845](https://github.com/vllm-project/vllm/pull/50845) Bound expert_map gathers on data-derived expert ids
- [#50727](https://github.com/vllm-project/vllm/pull/50727) Fix fused block-scale orientation
- [#50982](https://github.com/vllm-project/vllm/pull/50982) Fall back to torch for unsupported expert counts in topk_softplus_sqrt
- [#51078](https://github.com/vllm-project/vllm/pull/51078) Remove MoE legacy code

</details>

<details>
<summary>Model support (16)</summary>

- [#48250](https://github.com/vllm-project/vllm/pull/48250) Support MLA properly in the Transformers modeling backend
- [#51149](https://github.com/vllm-project/vllm/pull/51149) Add Interns2mobius support
- [#49969](https://github.com/vllm-project/vllm/pull/49969) Add top-k DSpark Markov projection for speculative decoding
- [#50580](https://github.com/vllm-project/vllm/pull/50580) Add DeepSeek V4 0731 reasoning effort prompts & mappings
- [#50688](https://github.com/vllm-project/vllm/pull/50688) Support jina-embeddings-v5-text-nano (EuroBERT encoder backbone)
- [#50524](https://github.com/vllm-project/vllm/pull/50524) Add K-EXAONE-2.0-750B-A37B model support
- [#50424](https://github.com/vllm-project/vllm/pull/50424) Support quantized DSpark Markov heads
- [#51129](https://github.com/vllm-project/vllm/pull/51129) Support Solar Open2 (SolarOpen2ForCausalLM)
- [#51255](https://github.com/vllm-project/vllm/pull/51255) Add Dots3 NOTE language model support
- [#51012](https://github.com/vllm-project/vllm/pull/51012) Move Qwen3.5 to hardware agnostic model definitions
- [#51237](https://github.com/vllm-project/vllm/pull/51237) Add upcoming TeleChat4 model support
- [#51168](https://github.com/vllm-project/vllm/pull/51168) Enable Speculative Decoding for NVIDIA-Nemotron-Parse-2.0
- [#51221](https://github.com/vllm-project/vllm/pull/51221) Add EVS video pruning support for Cosmos3-Edge
- [#51209](https://github.com/vllm-project/vllm/pull/51209) Add IndexCache for DeepSeek-V4
- [#51247](https://github.com/vllm-project/vllm/pull/51247) Fully generalise input embedding handling in Transformers modelling backend
- [#50898](https://github.com/vllm-project/vllm/pull/50898) Support partial layer loading natively using hf_overrides and ignore_patterns

</details>

<details>
<summary>Parallelism & scheduling (14)</summary>

- [#45043](https://github.com/vllm-project/vllm/pull/45043) Support llmd+vllm+mori-ep+mori-io for 2p2d with dp=ep=16 tp=1
- [#50390](https://github.com/vllm-project/vllm/pull/50390) Remove duplicate image preprocessing in EPD and enable preprocess on GPU
- [#44956](https://github.com/vllm-project/vllm/pull/44956) Add store group semantics to Mooncake KV Connector
- [#50507](https://github.com/vllm-project/vllm/pull/50507) Support partial-tail prefix reuse with fine-grained prefix matching
- [#48069](https://github.com/vllm-project/vllm/pull/48069) Add tenant ID support to MooncakeStoreConnector
- [#50902](https://github.com/vllm-project/vllm/pull/50902) Stateful Trainer Send: NCCL + Sparse NCCL [3/N]
- [#50897](https://github.com/vllm-project/vllm/pull/50897) Add lookahead-aware prefix cache hashing for EAGLE-style draft models
- [#51052](https://github.com/vllm-project/vllm/pull/51052) MoRIIO KV transfer of hybrid mamba/KDA recurrent state
- [#50941](https://github.com/vllm-project/vllm/pull/50941) Island-aware hierarchical allreduce for PCIe-only multi-island boxes
- [#51207](https://github.com/vllm-project/vllm/pull/51207) Add Bolins/shm tensor arena
- [#51241](https://github.com/vllm-project/vllm/pull/51241) Add /dev/shm size calculator for tensor parallel deployment
- [#50732](https://github.com/vllm-project/vllm/pull/50732) Emit inactive KV blocks for decode affinity
- [#51243](https://github.com/vllm-project/vllm/pull/51243) Emit self-describing events for partial recurrent blocks in KV offload
- [#50717](https://github.com/vllm-project/vllm/pull/50717) Skip block-size sync for packed KV caches in NIXL

</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#49934](https://github.com/vllm-project/vllm/pull/49934) Unify multiple-path encoder cuda graph support
- [#45254](https://github.com/vllm-project/vllm/pull/45254) Support ViT full CUDA graph for Ernie-4.5-VL image inference
- [#50929](https://github.com/vllm-project/vllm/pull/50929) Support ViT full CUDA graph for Kimi-K2.5
- [#49919](https://github.com/vllm-project/vllm/pull/49919) Explicitly manage torch CPU threads in workers
- [#51007](https://github.com/vllm-project/vllm/pull/51007) Support out-of-tree secondary tier managers via `module_path`
- [#50321](https://github.com/vllm-project/vllm/pull/50321) Support partial secondary-tier load results in KV offload
- [#50841](https://github.com/vllm-project/vllm/pull/50841) Enable tcmalloc for s390x

</details>

<details>
<summary>API & serving (33)</summary>

- [#50289](https://github.com/vllm-project/vllm/pull/50289) Add standalone Rust renderer
- [#50368](https://github.com/vllm-project/vllm/pull/50368) Add multimodal image inference to Rust Frontend gRPC
- [#48048](https://github.com/vllm-project/vllm/pull/48048) Plumbing session id into frontend requests
- [#50448](https://github.com/vllm-project/vllm/pull/50448) Deduplicate request preprocessing for `/tokenize` in Rust Frontend
- [#51089](https://github.com/vllm-project/vllm/pull/51089) Parse request priority from HTTP header
- [#50540](https://github.com/vllm-project/vllm/pull/50540) Align tool rendering for Kimi K3 in Rust Frontend
- [#50868](https://github.com/vllm-project/vllm/pull/50868) Preserve UTF-8 across benchmark stream chunks in Rust
- [#51047](https://github.com/vllm-project/vllm/pull/51047) Add V2 layered semantic trace
- [#51037](https://github.com/vllm-project/vllm/pull/51037) Support stable-window-aware KV reuse for Qwen3-ASR realtime
- [#50945](https://github.com/vllm-project/vllm/pull/50945) Add Model Runner V2 DBO Support for Eager Mode
- [#50783](https://github.com/vllm-project/vllm/pull/50783) Add opt-in segment timestamps to /v1/realtime in Voxtral
- [#51144](https://github.com/vllm-project/vllm/pull/51144) Support dynamic tools from developer messages in Rust Frontend
- [#50919](https://github.com/vllm-project/vllm/pull/50919) Add Worker-Level Timings to MRV2
- [#51085](https://github.com/vllm-project/vllm/pull/51085) Make distributed profiling transactional
- [#51084](https://github.com/vllm-project/vllm/pull/51084) Add Proton CUDA graph attribution to Profiler
- [#50875](https://github.com/vllm-project/vllm/pull/50875) Add Prometheus metrics for multimodal preprocessing pipeline
- [#51027](https://github.com/vllm-project/vllm/pull/51027) Use fastokens for tiktoken models in Rust Frontend
- [#51034](https://github.com/vllm-project/vllm/pull/51034) Add SSE keep-alive comments for idle streaming responses
- [#50723](https://github.com/vllm-project/vllm/pull/50723) Support sparse checkpoint updates through native weight loaders
- [#51178](https://github.com/vllm-project/vllm/pull/51178) Add explicit data-parallel rank routing to Rust Frontend gRPC
- [#50975](https://github.com/vllm-project/vllm/pull/50975) Support assistant message `phase` in Responses API
- [#50884](https://github.com/vllm-project/vllm/pull/50884) Mix per-prompt seeds into seeded SamplingParams in the offline API
- [#51036](https://github.com/vllm-project/vllm/pull/51036) Support repetition_detection as a server-side default
- [#51245](https://github.com/vllm-project/vllm/pull/51245) Correctly report world size for dense DP in Rust Frontend
- [#51251](https://github.com/vllm-project/vllm/pull/51251) Configure custom encoder cache managers from VllmConfig
- [#51235](https://github.com/vllm-project/vllm/pull/51235) Upgrade MiniJinja to 2.22 & remove method lookup workaround in Rust Frontend
- [#50864](https://github.com/vllm-project/vllm/pull/50864) Clamp KV connector match to the prompt suffix in V1 Scheduler
- [#50931](https://github.com/vllm-project/vllm/pull/50931) Enable decoder token-wise pooling in ModelRunner v2
- [#51147](https://github.com/vllm-project/vllm/pull/51147) Skip full OpenAI-server CLI schema for the managed headless engine in Rust Frontend
- [#50878](https://github.com/vllm-project/vllm/pull/50878) Add external metrics providers for stat logger plugins
- [#50998](https://github.com/vllm-project/vllm/pull/50998) Add TTTPS Proof-of-Time provenance middleware example
- [#51104](https://github.com/vllm-project/vllm/pull/51104) Support HF ShareGPT datasets in multi-turn mode in Rust Benchmark
- [#50756](https://github.com/vllm-project/vllm/pull/50756) Allow expert override for insufficient KV cache capacity

</details>

<details>
<summary>Multimodal (18)</summary>

- [#50411](https://github.com/vllm-project/vllm/pull/50411) Fused mm preprocess normalisation on the Device
- [#50800](https://github.com/vllm-project/vllm/pull/50800) Make image selection content-addressed on ROCm
- [#51167](https://github.com/vllm-project/vllm/pull/51167) Add support for `CUDAGraphMode.FULL_DECODE_ONLY` in Voxtral Realtime
- [#50819](https://github.com/vllm-project/vllm/pull/50819) Configure video frame soft-token budget for Gemma4
- [#50417](https://github.com/vllm-project/vllm/pull/50417) Restore multimodal draft capability detection in Model Runner V2
- [#48413](https://github.com/vllm-project/vllm/pull/48413) Fix MiniCPM-V placeholder replacement and image processor loading
- [#50958](https://github.com/vllm-project/vllm/pull/50958) Pad variable-length audio batches for Gemma3n/Gemma4
- [#49397](https://github.com/vllm-project/vllm/pull/49397) Skip Qwen3 deepstack buffers without vision
- [#48420](https://github.com/vllm-project/vllm/pull/48420) Fix Qwen3-Omni crash on video with no audio track
- [#50950](https://github.com/vllm-project/vllm/pull/50950) Resolve seq-cls `num_labels` from the top-level config for multimodal checkpoints
- [#50755](https://github.com/vllm-project/vllm/pull/50755) Classify DeepStream as GPU backend and enforce pixel limits
- [#49056](https://github.com/vllm-project/vllm/pull/49056) Emit a valid media type from encode_{audio,image,video}_url
- [#50250](https://github.com/vllm-project/vllm/pull/50250) Flatten >2D multimodal embeddings, not just 3D
- [#51157](https://github.com/vllm-project/vllm/pull/51157) Pad SigLIP text prompts to the trained sequence length
- [#51139](https://github.com/vllm-project/vllm/pull/51139) Invalidate retained PyNvVideoCodec decoder after failure
- [#50990](https://github.com/vllm-project/vllm/pull/50990) Validate dynamic video sampling metadata
- [#50983](https://github.com/vllm-project/vllm/pull/50983) Preserve the audio duration-limit error through the PyAV fallback
- [#51120](https://github.com/vllm-project/vllm/pull/51120) Return 400 for invalid PyNvVideoCodec video input

</details>

<details>
<summary>Bugfixes (26)</summary>

- [#50649](https://github.com/vllm-project/vllm/pull/50649) Fix Kimi-K3 KDA NaN on mixed batches and racy autotune config
- [#39935](https://github.com/vllm-project/vllm/pull/39935) Fix level-2 sleep/wake/reload with enable_lora=True
- [#51116](https://github.com/vllm-project/vllm/pull/51116) Fall back when MADV_POPULATE_WRITE is unsupported in KV Offload
- [#49230](https://github.com/vllm-project/vllm/pull/49230) Validate NIXL speculative config compatibility
- [#50886](https://github.com/vllm-project/vllm/pull/50886) Fix O(delta) reasoning-end check on the decode path for kimi_k3
- [#49069](https://github.com/vllm-project/vllm/pull/49069) Propagate EAGLE state across merged Mooncake store groups
- [#50802](https://github.com/vllm-project/vllm/pull/50802) Fix AITER all-reduce fusion coverage on ROCm
- [#50906](https://github.com/vllm-project/vllm/pull/50906) Guard sparse MLA masked MHA workspace
- [#50275](https://github.com/vllm-project/vllm/pull/50275) Don't stop an encoder-instance request before its images are encoded
- [#51095](https://github.com/vllm-project/vllm/pull/51095) Fix CI authorization notification fallback
- [#50890](https://github.com/vllm-project/vllm/pull/50890) Skip weight-prefix probe when model has WeightsMapper
- [#50358](https://github.com/vllm-project/vllm/pull/50358) Fail fast with a clear error when CPU offload region exceeds available space
- [#50327](https://github.com/vllm-project/vllm/pull/50327) Fix scalar Mamba state update with int32 mappings
- [#48341](https://github.com/vllm-project/vllm/pull/48341) Auto-enable async scheduling for draft models
- [#50867](https://github.com/vllm-project/vllm/pull/50867) Fuse weightless RMSNorms at their declared width
- [#50183](https://github.com/vllm-project/vllm/pull/50183) Fix NaN handling in rejection sampler tl.argmax
- [#50764](https://github.com/vllm-project/vllm/pull/50764) Constrain Anthropic cache_salt to non-empty
- [#49212](https://github.com/vllm-project/vllm/pull/49212) Dense multinode DP rescope with regression test
- [#50823](https://github.com/vllm-project/vllm/pull/50823) Shard UniformTypeKVCacheSpecs block table width under DCP
- [#50462](https://github.com/vllm-project/vllm/pull/50462) Log KV cache capacity after block-size resolution
- [#50869](https://github.com/vllm-project/vllm/pull/50869) Remove bad startup assertion
- [#50432](https://github.com/vllm-project/vllm/pull/50432) Fix cross-block race on num_accepted in MRv2 align prefix cache
- [#50701](https://github.com/vllm-project/vllm/pull/50701) Fix references to FusedMoE in doc
- [#48061](https://github.com/vllm-project/vllm/pull/48061) Use global data_parallel_index for the DP engine index
- [#50641](https://github.com/vllm-project/vllm/pull/50641) Fix non-contiguous weight transfers in Elastic EP
- - plus 55 more minor bugfixes

</details>

<details>
<summary>Tests, CI & build (16)</summary>

- [#51068](https://github.com/vllm-project/vllm/pull/51068) Prune redundant tests points in `correctness_e2e`
- [#51069](https://github.com/vllm-project/vllm/pull/51069) Prune `PyTorch Compilation Unit Tests`
- [#50839](https://github.com/vllm-project/vllm/pull/50839) Add PPL test for multimodal generation models
- [#51074](https://github.com/vllm-project/vllm/pull/51074) Prune PyTorch Fullgraph Test
- [#51060](https://github.com/vllm-project/vllm/pull/51060) Remove Ubuntu build-stage option from the CUDA dockerfile
- [#51087](https://github.com/vllm-project/vllm/pull/51087) Add run-all comment commands
- [#50840](https://github.com/vllm-project/vllm/pull/50840) Route AWQ linear through choose_mp_linear_kernel
- [#51067](https://github.com/vllm-project/vllm/pull/51067) Install mooncake from official wheels instead of a custom build
- [#50323](https://github.com/vllm-project/vllm/pull/50323) Add option to raise an exception when NaNs are detected in logits
- [#49990](https://github.com/vllm-project/vllm/pull/49990) Resolve revision to commit_hash once per model load
- [#50266](https://github.com/vllm-project/vllm/pull/50266) Add KimiLinear PD in nightlies
- [#51127](https://github.com/vllm-project/vllm/pull/51127) Run control-plane workflows on vLLM runners
- [#50726](https://github.com/vllm-project/vllm/pull/50726) Export Helion benchmark script in test artifacts
- [#51015](https://github.com/vllm-project/vllm/pull/51015) Stabilize GLM-5.2 PCP evaluation
- [#50713](https://github.com/vllm-project/vllm/pull/50713) Solidify speculative decoding E2E coverage
- - plus 25 more minor CI updates

</details>

<details>
<summary>Refactors (9)</summary>

- [#50981](https://github.com/vllm-project/vllm/pull/50981) Refactor throughput and reuse serve's get samples
- [#50285](https://github.com/vllm-project/vllm/pull/50285) Remove multiple dead codes
- [#50940](https://github.com/vllm-project/vllm/pull/50940) Unify routed expert shape configuration
- [#50582](https://github.com/vllm-project/vllm/pull/50582) ROCm Kimi-K3 aiter moe environment variable cleanup
- [#50066](https://github.com/vllm-project/vllm/pull/50066) Make PCPManager construction extensible
- [#51051](https://github.com/vllm-project/vllm/pull/51051) Remove kernel dead code
- [#50758](https://github.com/vllm-project/vllm/pull/50758) Remove attention layer name from unified_kv_cache_update for torch.compile
- [#50973](https://github.com/vllm-project/vllm/pull/50973) Remove layer_name from unified_kv_cache_update
- [#51242](https://github.com/vllm-project/vllm/pull/51242) Remove the XPU branch of topk_softplus_sqrt

</details>

<details>
<summary>Docs (4)</summary>

- [#50828](https://github.com/vllm-project/vllm/pull/50828) Document NIXL KV connector stats semantics
- [#50888](https://github.com/vllm-project/vllm/pull/50888) Add a readiness checklist for new tool-calling models
- [#51215](https://github.com/vllm-project/vllm/pull/51215) List Intel XPU attention backends
- [#50624](https://github.com/vllm-project/vllm/pull/50624) Document `reasoning_content` output removal as a breaking client change

</details>

<details>
<summary>Other (11)</summary>

- [#50879](https://github.com/vllm-project/vllm/pull/50879) Avoid importing `nixl_ep` on every `vllm serve` config
- [#51176](https://github.com/vllm-project/vllm/pull/51176) Revert Avoid importing `nixl_ep` on every `vllm serve` config
- [#50806](https://github.com/vllm-project/vllm/pull/50806) Restore Inkling MTP backend parity
- [#50946](https://github.com/vllm-project/vllm/pull/50946) Register fake meta kernel for fp4_gemm
- [#50547](https://github.com/vllm-project/vllm/pull/50547) Skip the warm up if CompilationMode.NONE
- [#51107](https://github.com/vllm-project/vllm/pull/51107) Use torch.accelerator.empty_host_cache() for host cache clearing
- [#50750](https://github.com/vllm-project/vllm/pull/50750) Remove torch compile warning when using breakable cudagraph
- [#50526](https://github.com/vllm-project/vllm/pull/50526) Alias is_current_stream_capturing to XPU in cuda wrapper
- [#50678](https://github.com/vllm-project/vllm/pull/50678) Move LatentMoERunner
- [#50816](https://github.com/vllm-project/vllm/pull/50816) Require cache_salt to be non-empty via schema
- [#51044](https://github.com/vllm-project/vllm/pull/51044) Improve speculative scheduling budget diagnostics

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: e0b7715f080622191f71fdac784a85bbd5c3a8733750e8e2513219f782324006 -->
