# sglang: PR digest (2026-08-05 to 2026-08-09)

_280 merged, 295 newly opened - source sgl-project/sglang, generated 2026-08-09T21:54:16Z_

## TL;DR
- **Model Focus**: DeepSeek (V4 DSpark on AMD, CP V2 strategy, FlashInfer mHC fusion), MiniMax (H3 SageAttention, M3 MXFP8 MoE), and GLM (GLM-Image batching, GLM-5.2 MXFP4) saw the most activity.
- **Diffusion & Multimodal**: Massive push on diffusion models (FLUX.1, Wan, ERNIE-Image, Z-Image, Sana) with bit-exact fused kernels (LayerNorm+modulate, RMSNorm) and fast paths, yielding significant end-to-end latency reductions (e.g., H200 FLUX.1 and Wan VAE).
- **Speculative Decoding & Caching**: Expanded HiCache to support packed/sidecar draft caches for MTP/EAGLE/DSpark, and introduced Facade DSA index-cache for MTP top-k reuse.
- **Kernels & Hardware**: Added SM120 MXFP8 dense GEMM via FlashInfer CUTLASS, separated ROCm-specific DeepSeek MHA/MLA forward paths, and unified BaseFusedOp/MultiPlatformOp dispatch.
- **Overall Direction**: The engine is heavily optimizing multimodal/diffusion serving with fused Triton kernels, while advancing speculative decoding (DSpark, MTP) and hardware-specific MoE/MLA paths for DeepSeek and MiniMax.

## Most important PRs
- **[#32365](https://github.com/sgl-project/sglang/pull/32365)**: Integrates native Rust-based multimodal processing for Qwen VL via `sglang-mm`, moving vision feature extraction and transport out of Python for better end-to-end performance.
- **[#33327](https://github.com/sgl-project/sglang/pull/33327)**: Introduces cross-node sequence parallelism for diffusion models by composing Ulysses and Ring attention, enabling massive context scaling across multi-GPU setups.
- **[#30393](https://github.com/sgl-project/sglang/pull/30393)**: Upgrades HiCache to support packed and sidecar draft caches for MTP, EAGLE, and DSpark, significantly improving memory efficiency during speculative decoding.
- **[#33208](https://github.com/sgl-project/sglang/pull/33208)**: Replaces the Triton MXFP8 dense GEMM path with FlashInfer CUTLASS for NVIDIA SM120 (Blackwell), optimizing quantization performance on next-generation hardware.
- **[#34171](https://github.com/sgl-project/sglang/pull/34171)**: (Newly opened) Proposes AdaFlash adaptive verification for DFlash speculative decoding, dynamically tuning verification steps to maximize acceptance rates.

## More changes by area

<details>
<summary>Performance (25)</summary>

- [#34125](https://github.com/sgl-project/sglang/pull/34125) Bit-exact data-movement elimination for the Wan causal VAE decoder
- [#34008](https://github.com/sgl-project/sglang/pull/34008) GLM-Image bit-exact fused aten LayerNorm+modulate / qk-LN
- [#34004](https://github.com/sgl-project/sglang/pull/34004) FLUX.1 fused adaLN modulate + RoPE cache hoist
- [#33960](https://github.com/sgl-project/sglang/pull/33960) Speed up TP and FSDP checkpoint loading
- [#31958](https://github.com/sgl-project/sglang/pull/31958) Compute input logprobs without materializing the full-vocab log-softmax
- [#33854](https://github.com/sgl-project/sglang/pull/33854) ERNIE-Image bit-exact fused RMSNorm+scale/shift
- [#33546](https://github.com/sgl-project/sglang/pull/33546) Wan VAE RMSNorm+SiLU fusion
- [#29677](https://github.com/sgl-project/sglang/pull/29677) Compact Triton extend-attention for ragged prefill (AMD/HIP-only)
- [#33822](https://github.com/sgl-project/sglang/pull/33822) Ideogram 4: fuse RMSNorm modulate/gate chains
- [#33886](https://github.com/sgl-project/sglang/pull/33886) Z-Image bit-exact fused qk-norm
- [#34126](https://github.com/sgl-project/sglang/pull/34126) FLUX.1: route the adaLN LN+modulate sites through the bit-exact fused LayerNorm+modulate kernel
- [#33819](https://github.com/sgl-project/sglang/pull/33819) FLUX.1 bit-exact residual-gate fast path + tanh-GELU epilogue
- [#33818](https://github.com/sgl-project/sglang/pull/33818) Generalize the FLUX.2 VAE decoder fast path to AutoencoderKL
- [#33734](https://github.com/sgl-project/sglang/pull/33734) ERNIE-Image bit-exact residual-gate fast path
- [#33823](https://github.com/sgl-project/sglang/pull/33823) FLUX.2 bit-exact residual-gate fast path
- [#33954](https://github.com/sgl-project/sglang/pull/33954) Build Qwen's masked varlen metadata host-side
- [#33839](https://github.com/sgl-project/sglang/pull/33839) Avoid temporary extend state copies in Mamba/GDN backend
- [#34014](https://github.com/sgl-project/sglang/pull/34014) Improve M3 performance on MI350
- [#33880](https://github.com/sgl-project/sglang/pull/33880) Reduce MiniMax H3 MPS memory pressure
- [#33873](https://github.com/sgl-project/sglang/pull/33873) Fuse MLA value projection with MXFP4 output quantization
- [#33907](https://github.com/sgl-project/sglang/pull/33907) Free out-of-window SWA pages without a device sync
- [#33950](https://github.com/sgl-project/sglang/pull/33950) Quantize TRTLLM MLA prefill Q once for chunked-prefix attention
- [#33952](https://github.com/sgl-project/sglang/pull/33952) Materialize Qwen encoder-DP features on owner ranks
- [#34066](https://github.com/sgl-project/sglang/pull/34066) Batch lazy-compaction mapping lookup
- [#33664](https://github.com/sgl-project/sglang/pull/33664) Simplify text-only mrope positions calculation

</details>

<details>
<summary>Kernels & attention (41)</summary>

- [#34085](https://github.com/sgl-project/sglang/pull/34085) Clean up diffusion kernels and shared fast paths
- [#31531](https://github.com/sgl-project/sglang/pull/31531) Separate ROCm-specific DeepSeek MHA and MLA forward paths
- [#33205](https://github.com/sgl-project/sglang/pull/33205) Unify BaseFusedOp and MultiPlatformOp dispatch
- [#32667](https://github.com/sgl-project/sglang/pull/32667) Add K/V-gather sequence parallel attention
- [#33903](https://github.com/sgl-project/sglang/pull/33903) Replace helion kernels with plain Triton for silu_and_mul
- [#28609](https://github.com/sgl-project/sglang/pull/28609) Facade DSA index-cache: MTP topk-reuse state + index-K storage
- [#33400](https://github.com/sgl-project/sglang/pull/33400) Move JIT kernels into namespace sglang
- [#33981](https://github.com/sgl-project/sglang/pull/33981) Add K3 verified mla kernel for DSpark on triton backend
- [#30964](https://github.com/sgl-project/sglang/pull/30964) Support DeepSeek V4 DSpark on AMD HIP platform
- [#33702](https://github.com/sgl-project/sglang/pull/33702) Add Sol-Attn sparse attention backend for diffusion
- [#34015](https://github.com/sgl-project/sglang/pull/34015) Sana: bit-exact fused aten LayerNorm+modulate under BCG
- [#33599](https://github.com/sgl-project/sglang/pull/33599) Fuse Kimi-K3 attn-residual aggregation
- [#34033](https://github.com/sgl-project/sglang/pull/34033) [Cherry-pick] Fuse Kimi-K3 attn-residual aggregation
- [#34045](https://github.com/sgl-project/sglang/pull/34045) Add registered short-conv tests and backend extensions
- [#33363](https://github.com/sgl-project/sglang/pull/33363) Unify MLA `scaling` init and remove dead buffer / scaling code
- [#33575](https://github.com/sgl-project/sglang/pull/33575) Rebuild the shared RoPE cache entry when its buffers are dead
- [#33703](https://github.com/sgl-project/sglang/pull/33703) Add SageAttention packed varlen path for MiniMax-H3
- [#28267](https://github.com/sgl-project/sglang/pull/28267) Add causal conv1d for NPU
- [#33532](https://github.com/sgl-project/sglang/pull/33532) Support CP V2 Strategy for dsv4
- [#33616](https://github.com/sgl-project/sglang/pull/33616) Add flashinfer mHC fusion for DSV4
- [#34059](https://github.com/sgl-project/sglang/pull/34059) End-to-end context-parallel prefill for hybrid linear models
- [#33647](https://github.com/sgl-project/sglang/pull/33647) Add FlashInfer CAKE prefill and decode backends
- [#34148](https://github.com/sgl-project/sglang/pull/34148) SubBlock: training-free block-sparse attention for the DiT
- [#33746](https://github.com/sgl-project/sglang/pull/33746) Combine Kimi-K3 ASM attn-residual
- [#33993](https://github.com/sgl-project/sglang/pull/33993) AITER fp8 ASM MLA decode + store-time fp8 mirror pool (Dsv4)
- [#33911](https://github.com/sgl-project/sglang/pull/33911) Generalize persistent CuTe JIT cache
- [#33815](https://github.com/sgl-project/sglang/pull/33815) Add diffusion rotary embedding kernel for CPU
- [#33816](https://github.com/sgl-project/sglang/pull/33816) Skip invalid-index stores in DeepSeek-V4 fused KV cache store kernels
- [#33686](https://github.com/sgl-project/sglang/pull/33686) Parallelize HiSparse host KV miss copies for small decode batches
- [#33623](https://github.com/sgl-project/sglang/pull/33623) Fuse MLA gate projection into QKV-A GEMM
- [#34165](https://github.com/sgl-project/sglang/pull/34165) Fuse pending AttnRes add into direct all-gather
- [#34162](https://github.com/sgl-project/sglang/pull/34162) Add SageAttention3 packed varlen path for MiniMax-H3
- [#33635](https://github.com/sgl-project/sglang/pull/33635) Adapt the Mellum2-12B-A2.5B-Thinking model on Ascend NPU
- [#33661](https://github.com/sgl-project/sglang/pull/33661) Fully support MLA in BCG
- [#33831](https://github.com/sgl-project/sglang/pull/33831) Support the mask-filling draft convention for DSpark
- [#34129](https://github.com/sgl-project/sglang/pull/34129) Use optional AITER BLOCK_Q MQA logits for GLM5 on AMD
- [#34093](https://github.com/sgl-project/sglang/pull/34093) Pass logits_soft_cap at plan time for FlashInfer
- [#33881](https://github.com/sgl-project/sglang/pull/33881) Split zero-KV fixup by alignment
- [#34172](https://github.com/sgl-project/sglang/pull/34172) LTX-2 quality=high fused RMSNorm+modulate + FFN GELU epilogue
- [#34180](https://github.com/sgl-project/sglang/pull/34180) Clean up shared bitexact gates, helpers, and stale naming
- [#34134](https://github.com/sgl-project/sglang/pull/34134) Integrate the CuTe DSL allreduce fusion from FlashInfer and tune for GLM-5.2

</details>

<details>
<summary>MoE & quantization (22)</summary>

- [#33889](https://github.com/sgl-project/sglang/pull/33889) Make the shared-experts-fusion decision a per-runner value
- [#32341](https://github.com/sgl-project/sglang/pull/32341) Add LingBot-Video MoE 30B T2V support
- [#32581](https://github.com/sgl-project/sglang/pull/32581) Quant-VideoGen PRQ KV-cache quantization
- [#33471](https://github.com/sgl-project/sglang/pull/33471) Add flashinfer rmsnorm + quant fusion support SM90, SM100, SM120
- [#33115](https://github.com/sgl-project/sglang/pull/33115) Support online MoE weight quantization for ModelOpt FP4
- [#32120](https://github.com/sgl-project/sglang/pull/32120) Add GLM-5.2 MXFP4 1P1D DI/CI recipes
- [#32395](https://github.com/sgl-project/sglang/pull/32395) Single-launch moe_align for tiny batches with many experts
- [#33474](https://github.com/sgl-project/sglang/pull/33474) Select DeepGEMM standard layouts by memory budget
- [#33469](https://github.com/sgl-project/sglang/pull/33469) Support scalar scale A for fp8_gemm
- [#32538](https://github.com/sgl-project/sglang/pull/32538) Support ModelOpt MXFP8 checkpoints
- [#34131](https://github.com/sgl-project/sglang/pull/34131) Serve tiny-batch moe_align on the pair axis, at any expert count
- [#34072](https://github.com/sgl-project/sglang/pull/34072) Add experimental FlashInfer AlphaMoE W8A8 backend
- [#33884](https://github.com/sgl-project/sglang/pull/33884) Run native MXFP4 MoE with humming for hopper
- [#33684](https://github.com/sgl-project/sglang/pull/33684) Support static DP/EP layouts for Weight Cache
- [#33942](https://github.com/sgl-project/sglang/pull/33942) Enable FlashInfer TRT-LLM MXFP8 MoE and optimize SwiGLU/MSA prefill for MiniMax-M3
- [#33957](https://github.com/sgl-project/sglang/pull/33957) Support FlashInfer TRT-LLM MXFP8 MoE for MiniMax-M3
- [#34136](https://github.com/sgl-project/sglang/pull/34136) Add online FP8 support for Krea-2
- [#33681](https://github.com/sgl-project/sglang/pull/33681) Support FP8 Qwen3-VL text encoder for MiniMax-H3
- [#33838](https://github.com/sgl-project/sglang/pull/33838) Optimize Kimi-K3 MoE performance
- [#33905](https://github.com/sgl-project/sglang/pull/33905) Pad MoE expert weight row stride to avoid L3 aliasing
- [#34164](https://github.com/sgl-project/sglang/pull/34164) Write CuTeDSL output directly into FlashInfer A2A workspace
- [#33108](https://github.com/sgl-project/sglang/pull/33108) Add inkling-small MoE support for sm_121

</details>

<details>
<summary>Model support (13)</summary>

- [#33691](https://github.com/sgl-project/sglang/pull/33691) Support Intern-S2-Mobius
- [#33140](https://github.com/sgl-project/sglang/pull/33140) Add official DSV4 reasoning effort support
- [#31477](https://github.com/sgl-project/sglang/pull/31477) Enable fused TopK for GLM-5.2 MTP IndexShare
- [#33829](https://github.com/sgl-project/sglang/pull/33829) Complete dots.note.omni support with native encoders, video preprocessing, and MTP decoding
- [#33972](https://github.com/sgl-project/sglang/pull/33972) Add TeleChat4 support with fused mHC backends
- [#34061](https://github.com/sgl-project/sglang/pull/34061) Support DiffusionGemma serving
- [#33982](https://github.com/sgl-project/sglang/pull/33982) Add TeleChat4 model support
- [#33648](https://github.com/sgl-project/sglang/pull/33648) Add K-EXAONE-2.0-750B-A37B support
- [#34007](https://github.com/sgl-project/sglang/pull/34007) Serve Kimi-K3 on gfx942: moonmath MLA multi-query verify, MXFP4 MoE, chunked prefix KV
- [#33673](https://github.com/sgl-project/sglang/pull/33673) Add MiniMax-M3 DSpark support
- [#33919](https://github.com/sgl-project/sglang/pull/33919) Add Qwen3.5-397B-A17B MXFP4 1P1D DI/CI recipes
- [#33937](https://github.com/sgl-project/sglang/pull/33937) Support DeepSeek-V4-Flash-0731 on sm89
- [#34130](https://github.com/sgl-project/sglang/pull/34130) Backfill DeepSeek V4 compress_ratios from compress_rates

</details>

<details>
<summary>Parallelism & scheduling (36)</summary>

- [#33899](https://github.com/sgl-project/sglang/pull/33899) Add CUDA VMM multimodal feature transport
- [#33468](https://github.com/sgl-project/sglang/pull/33468) Remove the HiMambaRadixTree that is no longer in use
- [#32415](https://github.com/sgl-project/sglang/pull/32415) Split multimodal scheduling from mm_utils
- [#30683](https://github.com/sgl-project/sglang/pull/30683) Batch GLM-Image AR requests
- [#33587](https://github.com/sgl-project/sglang/pull/33587) Align WAR fences with CUDA graph metadata reads
- [#33725](https://github.com/sgl-project/sglang/pull/33725) Support data-parallel serving (--dp-size)
- [#30545](https://github.com/sgl-project/sglang/pull/30545) Support radix cache for Disagg StagingBuffer
- [#33777](https://github.com/sgl-project/sglang/pull/33777) Reclaim duplicated host copy first under host pressure
- [#33421](https://github.com/sgl-project/sglang/pull/33421) Enable BCG under TP
- [#33965](https://github.com/sgl-project/sglang/pull/33965) Make scheduler RPC deadlines explicit
- [#33667](https://github.com/sgl-project/sglang/pull/33667) Pack Ulysses Q/K/V input all-to-all into one collective + reusable a2a staging buffers
- [#33477](https://github.com/sgl-project/sglang/pull/33477) Reuse batched Mamba boundary mask
- [#33475](https://github.com/sgl-project/sglang/pull/33475) Batch scheduler cache frees
- [#33928](https://github.com/sgl-project/sglang/pull/33928) Make ring admission a backend capability
- [#33885](https://github.com/sgl-project/sglang/pull/33885) Enable breakable CUDA graph for LTX-2
- [#33580](https://github.com/sgl-project/sglang/pull/33580) Complete the tree-core interface boundary for Unified Radix Cache
- [#33403](https://github.com/sgl-project/sglang/pull/33403) Honor explicit min-free-slots thresholds
- [#33348](https://github.com/sgl-project/sglang/pull/33348) Match the replicated draft KV pool's page granularity to its allocator
- [#33762](https://github.com/sgl-project/sglang/pull/33762) [Cherry-pick] Match the replicated draft KV pool's page granularity to its allocator
- [#34166](https://github.com/sgl-project/sglang/pull/34166) Window-bounded SWA KV storage and in-graph sampling for MLX
- [#33651](https://github.com/sgl-project/sglang/pull/33651) Unified KV Cache Layout in L3
- [#33863](https://github.com/sgl-project/sglang/pull/33863) Support PD + DSpark for PP
- [#33767](https://github.com/sgl-project/sglang/pull/33767) Support Kimi-K3 DCP decode offload to Mooncake L3
- [#33856](https://github.com/sgl-project/sglang/pull/33856) Add a unified post-hoc sparsity framework with StreamingLLM visibility
- [#33874](https://github.com/sgl-project/sglang/pull/33874) Commit real KV allocations for chained decode steps for MLX
- [#33959](https://github.com/sgl-project/sglang/pull/33959) Add bounded consistent hashing with an absolute load gap
- [#33728](https://github.com/sgl-project/sglang/pull/33728) Scale at DP-attention replica granularity
- [#33926](https://github.com/sgl-project/sglang/pull/33926) Support decode context parallelism on the trtllm_mla decode path
- [#33674](https://github.com/sgl-project/sglang/pull/33674) Add KVFlow workflow-aware prefix-cache eviction
- [#34012](https://github.com/sgl-project/sglang/pull/34012) Add Agentic-Aware Tail-Optimized LRU eviction to the unified radix cache
- [#34046](https://github.com/sgl-project/sglang/pull/34046) Support SWA host cache sizing and coexistence reclaim
- [#33807](https://github.com/sgl-project/sglang/pull/33807) Support pipeline-parallel prefill with Mooncake staging buffer
- [#33870](https://github.com/sgl-project/sglang/pull/33870) Support Prefill TP+CP for DSpark
- [#33639](https://github.com/sgl-project/sglang/pull/33639) Support Mamba branching in Unified Radix Cache with HiCache
- [#33804](https://github.com/sgl-project/sglang/pull/33804) Enable chunked prefill scnearios for XPU with UT
- [#34058](https://github.com/sgl-project/sglang/pull/34058) Bound consecutive prefills to protect decode

</details>

<details>
<summary>API & serving (17)</summary>

- [#32689](https://github.com/sgl-project/sglang/pull/32689) Responses support
- [#32588](https://github.com/sgl-project/sglang/pull/32588) Add generation request semantics
- [#33668](https://github.com/sgl-project/sglang/pull/33668) [Cherry-pick] Add generation request semantics
- [#33378](https://github.com/sgl-project/sglang/pull/33378) Add GLM Image usage report
- [#33787](https://github.com/sgl-project/sglang/pull/33787) Gate /health and /health_generate on warmup completion
- [#33138](https://github.com/sgl-project/sglang/pull/33138) Implement random tie breadking for cache_aware sglang router policy
- [#22867](https://github.com/sgl-project/sglang/pull/22867) Add language_model_only parameter support for Qwen35
- [#33729](https://github.com/sgl-project/sglang/pull/33729) Expose multi-choice generation streams
- [#34127](https://github.com/sgl-project/sglang/pull/34127) Add output logprobs support for harmony and streaming
- [#33977](https://github.com/sgl-project/sglang/pull/33977) Router session stats
- [#34132](https://github.com/sgl-project/sglang/pull/34132) Report abort reasons and terminal outcomes
- [#33938](https://github.com/sgl-project/sglang/pull/33938) Add opt-in --source-label-header to record a source metric label
- [#33799](https://github.com/sgl-project/sglang/pull/33799) Expose O(1) session radix cache pressure metrics
- [#34185](https://github.com/sgl-project/sglang/pull/34185) Abort in-flight requests by caller-declared start weight version
- [#34137](https://github.com/sgl-project/sglang/pull/34137) Add bucket range config parsing, validation, and selection
- [#34170](https://github.com/sgl-project/sglang/pull/34170) Add FastSafetensors sharded-state loader
- [#34064](https://github.com/sgl-project/sglang/pull/34064) Optimize ordinary model weight loading

</details>

<details>
<summary>Hardware & arch (10)</summary>

- [#33724](https://github.com/sgl-project/sglang/pull/33724) Improve the execution efficiency and maintainability of pr‑test‑npu
- [#32505](https://github.com/sgl-project/sglang/pull/32505) Add unit tests for ascend_torch_native_backend and mla_preprocess
- [#33976](https://github.com/sgl-project/sglang/pull/33976) Upgrade recommendeded sglang version on Ascend NPU
- [#30883](https://github.com/sgl-project/sglang/pull/30883) Add qknorm_rope support for Flux on XPU
- [#33626](https://github.com/sgl-project/sglang/pull/33626) Add unit tests for utils, CMO, memory pool, and allocator for NPU
- [#33676](https://github.com/sgl-project/sglang/pull/33676) Support DeepSeek-V4 DSpark speculative decoding on NPU
- [#33685](https://github.com/sgl-project/sglang/pull/33685) Reorganize test output/log directory structure with workflow context for NPU CI
- [#34140](https://github.com/sgl-project/sglang/pull/34140) Enable stochastic tree verification on ROCm
- [#33979](https://github.com/sgl-project/sglang/pull/33979) Size DSV4 C4 device pool by request capacity for NPU
- [#33939](https://github.com/sgl-project/sglang/pull/33939) Add gfx1151 (Strix Halo / Ryzen AI MAX+) Docker image for ROCm

</details>

<details>
<summary>Bugfixes (78)</summary>

- [#33417](https://github.com/sgl-project/sglang/pull/33417) Fix deterministic inference for Inkling
- [#32999](https://github.com/sgl-project/sglang/pull/32999) Fix GLM-Image resolution alignment
- [#33758](https://github.com/sgl-project/sglang/pull/33758) Stop/EOS inside a spec accept run beats the max_new_tokens finish
- [#32858](https://github.com/sgl-project/sglang/pull/32858) Fix DCP KV head mapping for GQA models
- [#33543](https://github.com/sgl-project/sglang/pull/33543) Fix Nemotron W4A16 NVFP4 MoE backend
- [#33764](https://github.com/sgl-project/sglang/pull/33764) Fix the router GEMM inaccuracy when using _front_w in Kimi-K3
- [#33906](https://github.com/sgl-project/sglang/pull/33906) Fix prefill CP graph overflow with larger bucket search
- [#33969](https://github.com/sgl-project/sglang/pull/33969) Stop RunAI Model Streamer's rank-discovery collective from firing on independent per-rank loads
- [#33379](https://github.com/sgl-project/sglang/pull/33379) Fix _pa_swa_prefill_lens off-by-one in FlashAttentionBackend
- [#33666](https://github.com/sgl-project/sglang/pull/33666) Size the mamba pool per pipeline stage, not per whole model
- [#34035](https://github.com/sgl-project/sglang/pull/34035) [Cherry-pick] Size the mamba pool per pipeline stage, not per whole model
- [#34067](https://github.com/sgl-project/sglang/pull/34067) Fix batched KV free aliasing
- [#33558](https://github.com/sgl-project/sglang/pull/33558) Fix YaRN mscale double-application in rope config
- [#33352](https://github.com/sgl-project/sglang/pull/33352) Always capture default prefill CUDA graph
- [#33123](https://github.com/sgl-project/sglang/pull/33123) Fix broken Nemotron DP attention
- [#32700](https://github.com/sgl-project/sglang/pull/32700) Restrict the SWA chunk-cap escape hatch to true head-of-line livelock
- [#33785](https://github.com/sgl-project/sglang/pull/33785) Fix Mistral-Large-3 EAGLE draft skipping DeepseekV2Model.__init__
- [#33875](https://github.com/sgl-project/sglang/pull/33875) Fix 4/8-step distilled MiniMax-H3 Turbo LoRA merge
- [#33864](https://github.com/sgl-project/sglang/pull/33864) Fix MiniMax-H3 text encoder device mismatch under --text-encoder-cpu-offload
- [#32685](https://github.com/sgl-project/sglang/pull/32685) Update weight from tensor detects device by uuid
- plus 58 more minor bugfixes

</details>

<details>
<summary>Refactors (17)</summary>

- [#34081](https://github.com/sgl-project/sglang/pull/34081) Retire the published ServerArgs read from business code
- [#33490](https://github.com/sgl-project/sglang/pull/33490) Retire ServerArgs.override in favour of derive()
- [#33491](https://github.com/sgl-project/sglang/pull/33491) Resolve the draft worker's config per runner, not on a copy
- [#33887](https://github.com/sgl-project/sglang/pull/33887) Retire ServerArgs.derive; per-runner values are constructor arguments
- [#33492](https://github.com/sgl-project/sglang/pull/33492) The draft runner carries its own attention backend
- [#34080](https://github.com/sgl-project/sglang/pull/34080) Retire the hidden global fallbacks and the mamba-extra-buffer instance reads
- [#33488](https://github.com/sgl-project/sglang/pull/33488) Retire the alias-form process-global config reads
- [#33489](https://github.com/sgl-project/sglang/pull/33489) Template-detected parsers go to the engine's control-plane overlay
- [#33888](https://github.com/sgl-project/sglang/pull/33888) Delete the dead get_server_args() bindings across the repo
- [#33925](https://github.com/sgl-project/sglang/pull/33925) Route DCP topology reads through get_parallel()
- [#33843](https://github.com/sgl-project/sglang/pull/33843) Consolidate pipeline core hygiene
- [#33844](https://github.com/sgl-project/sglang/pull/33844) Simplify disaggregation transport hygiene
- [#33845](https://github.com/sgl-project/sglang/pull/33845) Centralize entrypoint API hygiene
- [#34158](https://github.com/sgl-project/sglang/pull/34158) Clean up logits processor helpers
- [#33790](https://github.com/sgl-project/sglang/pull/33790) Refactor dcp attn comm group
- [#33894](https://github.com/sgl-project/sglang/pull/33894) Refactor error responses into shared utils::response helpers
- [#33910](https://github.com/sgl-project/sglang/pull/33910) Refactor staging registration metadata fields

</details>

<details>
<summary>Tests, CI & build (57)</summary>

- [#33752](https://github.com/sgl-project/sglang/pull/33752) Re-enable a pruned Inkling LoRA unit-test set
- [#34070](https://github.com/sgl-project/sglang/pull/34070) Trim redundant nightly test registrations
- [#33619](https://github.com/sgl-project/sglang/pull/33619) Speed up dependency install: dual-ABI Rust ext cache and prevalidation pruning
- [#33756](https://github.com/sgl-project/sglang/pull/33756) Collapse the EAGLE launch matrix and the scoring engine boots on the per-commit runners
- [#33832](https://github.com/sgl-project/sglang/pull/33832) Remove profiling from nightly tests
- [#33745](https://github.com/sgl-project/sglang/pull/33745) Fold duplicate-server suites and prune the retract matrix on 1-gpu-5090
- [#33498](https://github.com/sgl-project/sglang/pull/33498) Build and release sgl-deep-ep wheels
- [#33932](https://github.com/sgl-project/sglang/pull/33932) Install DeepEP from release wheels
- [#33654](https://github.com/sgl-project/sglang/pull/33654) Move CPU-only unit tests to the CPU suite and trim dead 5090 registrations
- [#33641](https://github.com/sgl-project/sglang/pull/33641) Merge tokenizer worker tests and drop redundant triton attention e2e
- plus 47 more minor CI and test updates

</details>

<details>
<summary>Docs (18)</summary>

- [#33556](https://github.com/sgl-project/sglang/pull/33556) Add Ling-3.0-flash cookbook
- [#32323](https://github.com/sgl-project/sglang/pull/32323) Fill Qwen3.5 speed benchmarks
- [#34143](https://github.com/sgl-project/sglang/pull/34143) Refresh skills for latest runtime
- [#33704](https://github.com/sgl-project/sglang/pull/33704) Parallelism overview — how CFG/TP/Ulysses/ring compose
- [#33850](https://github.com/sgl-project/sglang/pull/33850) Retire released warmup and decoder flags
- [#33851](https://github.com/sgl-project/sglang/pull/33851) Validate and document Spectrum controls
- [#33849](https://github.com/sgl-project/sglang/pull/33849) Gate fast VAE paths by quality
- [#32434](https://github.com/sgl-project/sglang/pull/32434) Consolidate compiled-kernel caches under SGLANG_CACHE_DIR
- [#33712](https://github.com/sgl-project/sglang/pull/33712) Add HiCache + Mooncake cells for Ling-3.0-flash
- [#33882](https://github.com/sgl-project/sglang/pull/33882) Ling-3.0-flash cookbook — serve native 256K, drop YaRN override
- plus 8 more minor documentation updates

</details>

<details>
<summary>Other (26)</summary>

- [#31491](https://github.com/sgl-project/sglang/pull/31491) Feat/spectrum
- [#33775](https://github.com/sgl-project/sglang/pull/33775) Capture-safe pynccl all-to-all
- [#33936](https://github.com/sgl-project/sglang/pull/33936) Auto-select CUDA VMM on multi-node MNNVL
- [#33653](https://github.com/sgl-project/sglang/pull/33653) Gate multimodal feature transport by model capability
- [#33120](https://github.com/sgl-project/sglang/pull/33120) Warn on risky serving-time Triton work
- [#33826](https://github.com/sgl-project/sglang/pull/33826) Revert "Warn on risky serving-time Triton work"
- [#34160](https://github.com/sgl-project/sglang/pull/34160) Revert parallel request lifecycle tracking from [#32588](https://github.com/sgl-project/sglang/pull/32588)
- [#33898](https://github.com/sgl-project/sglang/pull/33898) Render tool-result media instead of coercing content to str
- [#31300](https://github.com/sgl-project/sglang/pull/31300) Add srt_empty extra group for device-agnostic install
- [#33707](https://github.com/sgl-project/sglang/pull/33707) Derive H3 attention admission from backend capabilities
- [#34036](https://github.com/sgl-project/sglang/pull/34036) Resolve the ragged-verify graph tier at a single point
- [#34038](https://github.com/sgl-project/sglang/pull/34038) Resolve the ragged-verify graph tier at a single point
- [#33908](https://github.com/sgl-project/sglang/pull/33908) Reland serving-time Triton load diagnostics
- [#33613](https://github.com/sgl-project/sglang/pull/33613) Remove revoke queue after hit-then-alloc refactoring
- [#32900](https://github.com/sgl-project/sglang/pull/32900) Propagate semantic group names to PyTorch process groups
- [#33848](https://github.com/sgl-project/sglang/pull/33848) Resolve IPC A2A peers from process groups
- [#33595](https://github.com/sgl-project/sglang/pull/33595) Measure prefill busy time between launches
- [#32556](https://github.com/sgl-project/sglang/pull/32556) Autotune flashinfer extend buckets at warmup
- [#34124](https://github.com/sgl-project/sglang/pull/34124) perf_logger: SYNC_STAGE_PROFILING must drain the GPU queue for stage records too
- [#32388](https://github.com/sgl-project/sglang/pull/32388) Observability enhancement for HiCache
- [#24370](https://github.com/sgl-project/sglang/pull/24370) Profiling Enhancements [1/3]: cuda graph profile traces
- [#33997](https://github.com/sgl-project/sglang/pull/33997) WIP
- [#33895](https://github.com/sgl-project/sglang/pull/33895) Move the PD bootstrap registry under api_server::disaggregation
- [#34031](https://github.com/sgl-project/sglang/pull/34031) Make ForwardBatch the single channel for the ragged-verify layout
- [#34188](https://github.com/sgl-project/sglang/pull/34188) Rust Kimi-K3 image preprocessing in sglang-mm (library mode)
- [#34001](https://github.com/sgl-project/sglang/pull/34001) Minimax-m3 dspark sglang 0.5.16
- [#33718](https://github.com/sgl-project/sglang/pull/33718) Route empty_cache and synchronize through current_platform
- [#33108](https://github.com/sgl-project/sglang/pull/33108) Add inkling-small MoE support for sm_121
- [#33966](https://github.com/sgl-project/sglang/pull/33966) Load community EAGLE drafts without repackaging the checkpoint

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 572e2303ed06c12194f244097354b98c0c225bc7cd15a1b7413ab56fc09394e4 -->
