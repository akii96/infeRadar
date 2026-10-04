# sglang: PR digest (2026-08-30 to 2026-09-03)

_271 merged, 451 newly opened - source sgl-project/sglang, generated 2026-09-03T13:47:17Z_

## TL;DR
- **DeepSeek (V4) and GLM (5.3-Flash) got the most attention.** Merged work added an AMD FP4 indexer for DSV4 (`[#37353](https://github.com/sgl-project/sglang/pull/37353)`), the SM120 DeepGEMM paged-MQA indexer with FP4 MoE (`[#29927](https://github.com/sgl-project/sglang/pull/29927)`), a fused hc-prenorm Triton kernel, and GLM-5.3 Flash kernels (`[#37477](https://github.com/sgl-project/sglang/pull/37477)`). Open PRs add an MXFP4 KV cache for DSV4 on Hopper, a fused MXFP4 decode attention kernel (JIT), and AMD fp8 unified_kv and HiCache for DSV4.
- **The biggest perf work was kernel fusion and quantization.** Diffusion got Blackwell FP8/NVFP4 fusions for Qwen-Image, FLUX.2 and Wan2.2. There is also a KDA NVFP4 GEMM for SM120 (`[#36865](https://github.com/sgl-project/sglang/pull/36865)`), FlashInfer SM90 MXFP4 W4A8 CUTLASS MoE (`[#34967](https://github.com/sgl-project/sglang/pull/34967)`), and an MXFP4 Kimi K3 MoE on the DeepGEMM runner (`[#34874](https://github.com/sgl-project/sglang/pull/34874)`).
- **Unified memory is a large refactor stream.** It spans KV sub-pools for mamba and hybrid-SWA, dense KV views, reads through fa3, flashinfer, trtllm_mha and flashmla, and DCP support. A parallel `ReqKvInfo` migration moves per-request KV state into a single record.
- **Direction:** a Rust radix-tree core and server, more AMD gfx950/gfx1250 and NPU/XPU enablement, and a big wave of newly opened Qwen-Next/GLM-5.3 rebases and speculative-decode features.

## Most important PRs
**[#32710](https://github.com/sgl-project/sglang/pull/32710) Rust TreeCore radix cache backend**
Adds a Rust radix-tree backend with shared parity tests against the Python implementation. It is the base for a series of follow-ups (external cache linker, SWA branching-point caching) aimed at faster cache management.

**[#35177](https://github.com/sgl-project/sglang/pull/35177) Unified-memory sub-pools for mamba + hybrid-SWA**
Splits one memory pool into separate sub-pools for mamba and sliding-window models. The related PRs `[#34602](https://github.com/sgl-project/sglang/pull/34602)` and `[#34613](https://github.com/sgl-project/sglang/pull/34613)` let attention backends read the unified pool directly.

**[#36865](https://github.com/sgl-project/sglang/pull/36865) KDA NVFP4 GEMM for Qwen3.x on SM120**
Adds an NVFP4 GEMM for the KDA linear-attention layers on consumer Blackwell, a low-precision path for hybrid Qwen models.

**[#34967](https://github.com/sgl-project/sglang/pull/34967) FlashInfer SM90 MXFP4 W4A8 CUTLASS MoE**
Adds a Hopper MoE path with MXFP4 weights and FP8 activations. It cuts weight memory and bandwidth for large MoE serving.

**[#37667](https://github.com/sgl-project/sglang/pull/37667) Native UNO speculative decoding support**
A new speculative-decoding serving mode touching the scheduler, attention and the Triton backend.

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#34198](https://github.com/sgl-project/sglang/pull/34198) AMD: fuse the ROCm KDA decode boundary for Kimi-K3
- [#33838](https://github.com/sgl-project/sglang/pull/33838) AMD: Kimi-K3 MoE optimization
- [#37116](https://github.com/sgl-project/sglang/pull/37116) Qwen-Image: absorb output projection biases
- [#37330](https://github.com/sgl-project/sglang/pull/37330) Reduce tokenizer overhead and offload CUDA VMM publication
- [#36970](https://github.com/sgl-project/sglang/pull/36970) GDN: pick ReplaySSM verify unrolling by shape
- [#37324](https://github.com/sgl-project/sglang/pull/37324) Radix tree walk by offset instead of re-slicing tokens
- [#37070](https://github.com/sgl-project/sglang/pull/37070) Scatter mm embeddings by row to cut transient GPU memory
- [#37203](https://github.com/sgl-project/sglang/pull/37203) Faster lint CI
- [#37576](https://github.com/sgl-project/sglang/pull/37576) GLM-5.3-Flash FP8 speed data

</details>

<details>
<summary>Kernels & attention (22)</summary>

- [#37477](https://github.com/sgl-project/sglang/pull/37477) GLM 5.3 Flash kernels
- [#34693](https://github.com/sgl-project/sglang/pull/34693) Replace dsv3_router_gemm with the unified tiny GEMM
- [#34647](https://github.com/sgl-project/sglang/pull/34647) AMD: 12-head MLA aiter fp8 Gluon decode
- [#33926](https://github.com/sgl-project/sglang/pull/33926) DCP on the trtllm_mla decode path
- [#36890](https://github.com/sgl-project/sglang/pull/36890) Unified memory DCP for Kimi-Linear
- [#37693](https://github.com/sgl-project/sglang/pull/37693) Unified memory DCP for the trtllm_mla family
- [#33722](https://github.com/sgl-project/sglang/pull/33722) Fused-accept state advance for FlashInfer KDA MTP verify
- [#33237](https://github.com/sgl-project/sglang/pull/33237) dsv4: `--dsa-topk-backend flashinfer`
- [#35118](https://github.com/sgl-project/sglang/pull/35118) DSV4 hc-prenorm combine fused in Triton
- [#35546](https://github.com/sgl-project/sglang/pull/35546) EAGLE: prune draft-extend logits to selected rows
- [#37512](https://github.com/sgl-project/sglang/pull/37512) Build the unified read stream without the page-table rectangle
- [#37511](https://github.com/sgl-project/sglang/pull/37511) Size the read-table grid from bs; fuse tombstone scatters
- [#33911](https://github.com/sgl-project/sglang/pull/33911) Generalize the persistent CuTe JIT cache
- [#36735](https://github.com/sgl-project/sglang/pull/36735) Key masks on USPAttention's replicated-prefix path
- [#32218](https://github.com/sgl-project/sglang/pull/32218) FlashInfer: avoid D2H sync for sliding-window lengths
- [#34446](https://github.com/sgl-project/sglang/pull/34446) Fused Qwen3.5 RoPE kernel dropped mrope height and width
- [#36831](https://github.com/sgl-project/sglang/pull/36831) Rename DSA top-k transform entry points
- [#33318](https://github.com/sgl-project/sglang/pull/33318) XPU: SYCL topk_transform
- [#36329](https://github.com/sgl-project/sglang/pull/36329) NPU: strip padding before the FIA kernel
- [#37317](https://github.com/sgl-project/sglang/pull/37317) Raise shape limits in shared FLA and MoE kernels
- [#37550](https://github.com/sgl-project/sglang/pull/37550) Converge the two SWA predicates
- [#37170](https://github.com/sgl-project/sglang/pull/37170) Unified-memory comment cleanup

</details>

<details>
<summary>MoE & quantization (13)</summary>

- [#34874](https://github.com/sgl-project/sglang/pull/34874) MXFP4 experts for Kimi K3 on the DeepGEMM runner
- [#32665](https://github.com/sgl-project/sglang/pull/32665) Extension points for custom MoE runner backends
- [#35120](https://github.com/sgl-project/sglang/pull/35120) FlashInfer CuTe DSL NVFP4 W4A16
- [#37279](https://github.com/sgl-project/sglang/pull/37279) sgl-deep-gemm 0.1.7
- [#37158](https://github.com/sgl-project/sglang/pull/37158) LFM2.5 Triton MoE configs on B300
- [#37159](https://github.com/sgl-project/sglang/pull/37159) GB300 Triton MoE configs for GLM-4.5 FP8
- [#36811](https://github.com/sgl-project/sglang/pull/36811) Avoid zero-bias allocation in fused softmax routing
- [#36407](https://github.com/sgl-project/sglang/pull/36407) Native MoE with noncontiguous top-k IDs
- [#37331](https://github.com/sgl-project/sglang/pull/37331) GPU kernel ordering and MXFP8 dispatch fix
- [#37489](https://github.com/sgl-project/sglang/pull/37489) Preserve FP32 in the SM107 MXFP8 fallback
- [#35883](https://github.com/sgl-project/sglang/pull/35883) Stale GLM MoE routing after runtime weight updates
- [#36922](https://github.com/sgl-project/sglang/pull/36922) Harden checkpoint quantization metadata parsing
- [#32733](https://github.com/sgl-project/sglang/pull/32733) CPU FP8 KV cache

</details>

<details>
<summary>Model support (12)</summary>

- [#37654](https://github.com/sgl-project/sglang/pull/37654) IFM K2 Horizon serving
- [#31041](https://github.com/sgl-project/sglang/pull/31041) LFM2 and LFM2-MoE DSpark speculative decoding
- [#34893](https://github.com/sgl-project/sglang/pull/34893) MiniMax H3 cube sparse attention (diffusion)
- [#37480](https://github.com/sgl-project/sglang/pull/37480) FastH3 with a VSA-H3 attention backend
- [#35703](https://github.com/sgl-project/sglang/pull/35703) Block-FP8 MiniMax-H3 DiT loading
- [#37162](https://github.com/sgl-project/sglang/pull/37162) Fuse FLUX.2 ModelOpt FP8 producers and QKV packing
- [#37123](https://github.com/sgl-project/sglang/pull/37123) Qwen-Image FP8 QKV and Blackwell epilogue
- [#37156](https://github.com/sgl-project/sglang/pull/37156) Qwen-Image FP8 norm and activation quantization
- [#37129](https://github.com/sgl-project/sglang/pull/37129) Qwen-Image residual norm and NVFP4
- [#37144](https://github.com/sgl-project/sglang/pull/37144) Qwen-Image final adaptive LayerNorm
- [#37090](https://github.com/sgl-project/sglang/pull/37090) Cache Qwen-Image modulation across CFG branches
- [#36624](https://github.com/sgl-project/sglang/pull/36624) Cohere Command-A-Plus decode on SM10X

</details>

<details>
<summary>Parallelism & scheduling (17)</summary>

- [#36911](https://github.com/sgl-project/sglang/pull/36911) Size the CUDA graph pool from warmup measurements
- [#36933](https://github.com/sgl-project/sglang/pull/36933) Mixed chunk prefill with spec enabled
- [#36248](https://github.com/sgl-project/sglang/pull/36248) PP prefill CUDA graph proxy tensors
- [#37674](https://github.com/sgl-project/sglang/pull/37674) Extract PP DynamicChunkSizer
- [#37669](https://github.com/sgl-project/sglang/pull/37669) Apply the attention-CP broadcast result in PP chunk profiling
- [#37675](https://github.com/sgl-project/sglang/pull/37675) Broadcast PP chunk-profiling failures
- [#30915](https://github.com/sgl-project/sglang/pull/30915) Megatron LayerNorm sequence parallelism
- [#33614](https://github.com/sgl-project/sglang/pull/33614) Dspark and Dflash state divergence across TP ranks
- [#37274](https://github.com/sgl-project/sglang/pull/37274) Custom policy for adaptive speculative decoding
- [#36752](https://github.com/sgl-project/sglang/pull/36752) Multi-layer EAGLE shared-read event
- [#36897](https://github.com/sgl-project/sglang/pull/36897) Decouple draft capacity from runtime state
- [#37505](https://github.com/sgl-project/sglang/pull/37505) DP attention decode->extend prefix off-by-one
- [#35158](https://github.com/sgl-project/sglang/pull/35158) Unified memory byte-budget sizing and conservation verifier
- [#36723](https://github.com/sgl-project/sglang/pull/36723) Sync-free `free_swa` on page_size 1
- [#36646](https://github.com/sgl-project/sglang/pull/36646) Resolve SWA ownership at enqueue
- [#37481](https://github.com/sgl-project/sglang/pull/37481) Split duplicate insert frees at the SWA eviction floor
- [#36721](https://github.com/sgl-project/sglang/pull/36721) `free_kv_row` for row ranges

</details>

<details>
<summary>Hardware & arch (14)</summary>

- [#36871](https://github.com/sgl-project/sglang/pull/36871) AMD gfx1250 on ROCm 10
- [#37353](https://github.com/sgl-project/sglang/pull/37353) AMD FP4 indexer for DSV4
- [#37660](https://github.com/sgl-project/sglang/pull/37660) AMD FP4 indexer OOR fix
- [#34484](https://github.com/sgl-project/sglang/pull/34484) ROCm QuickReduce fp16 saturation fix
- [#36960](https://github.com/sgl-project/sglang/pull/36960) Cap the DSA MQA-logits budget at AITER's limit
- [#37118](https://github.com/sgl-project/sglang/pull/37118) Define DSA head-gate graph helpers on HIP
- [#37242](https://github.com/sgl-project/sglang/pull/37242) Gate the aiter memory-reserve exemption behind an env var
- [#29927](https://github.com/sgl-project/sglang/pull/29927) SM120 DSV4 DeepGEMM paged-MQA indexer and FP4 MoE
- [#36845](https://github.com/sgl-project/sglang/pull/36845) Restore SM121 correctness for QSA
- [#37035](https://github.com/sgl-project/sglang/pull/37035) MLX startup crash fix
- [#37193](https://github.com/sgl-project/sglang/pull/37193) XPU weekly model enablement
- [#36699](https://github.com/sgl-project/sglang/pull/36699) XPU per-model metrics
- [#36220](https://github.com/sgl-project/sglang/pull/36220) `reindex_device_id` for the device OOT plugin
- [#37146](https://github.com/sgl-project/sglang/pull/37146) NPU paged allocator free-list release

</details>

<details>
<summary>API & serving (16)</summary>

- [#37047](https://github.com/sgl-project/sglang/pull/37047) Contain multimodal feature transport failures
- [#36983](https://github.com/sgl-project/sglang/pull/36983) Recover multimodal decode and processor failures
- [#37043](https://github.com/sgl-project/sglang/pull/37043) Per-request vit graph metadata for qwen-vl
- [#37320](https://github.com/sgl-project/sglang/pull/37320) Alpha-channel images and tool-result media ordering
- [#36630](https://github.com/sgl-project/sglang/pull/36630) Capture masks from sampler support
- [#37029](https://github.com/sgl-project/sglang/pull/37029) Bound stop strings and regex patterns
- [#34187](https://github.com/sgl-project/sglang/pull/34187) Kimi K3 opt-in `force_nonempty_content`
- [#36384](https://github.com/sgl-project/sglang/pull/36384) Streamed LoRA weight updates (miles)
- [#35127](https://github.com/sgl-project/sglang/pull/35127) Extract Anthropic conversion into standalone utils
- [#37327](https://github.com/sgl-project/sglang/pull/37327) Rust server launcher and request validation
- [#37221](https://github.com/sgl-project/sglang/pull/37221) Rust server address and signed env values
- [#37222](https://github.com/sgl-project/sglang/pull/37222) Rust wire schemas in sync
- [#37226](https://github.com/sgl-project/sglang/pull/37226) Rust request defaults and batch header ABI
- [#36994](https://github.com/sgl-project/sglang/pull/36994) Rollout API: return only SDE latents
- [#36101](https://github.com/sgl-project/sglang/pull/36101) Weight cache keyed by GPU UUID
- [#37469](https://github.com/sgl-project/sglang/pull/37469) Real-traffic replay in bench_one_batch_server

</details>

<details>
<summary>Diffusion infra (17)</summary>

- [#37422](https://github.com/sgl-project/sglang/pull/37422) Cumulative extra-high quality tier
- [#37437](https://github.com/sgl-project/sglang/pull/37437) SpargeAttention backend
- [#36824](https://github.com/sgl-project/sglang/pull/36824) Remove component loader capability switches
- [#36875](https://github.com/sgl-project/sglang/pull/36875) Preserve component identity during loading
- [#37004](https://github.com/sgl-project/sglang/pull/37004) Stream native VAE weights directly to GPU
- [#36907](https://github.com/sgl-project/sglang/pull/36907) Enforce component attention backend
- [#36991](https://github.com/sgl-project/sglang/pull/36991) Exact component precision overrides
- [#37049](https://github.com/sgl-project/sglang/pull/37049) Component execution options fail closed
- [#36916](https://github.com/sgl-project/sglang/pull/36916) Detect quantized transformer replacements
- [#36917](https://github.com/sgl-project/sglang/pull/36917) Reject incompatible transformer fallback
- [#37441](https://github.com/sgl-project/sglang/pull/37441) Admit explicit attention backends by capability
- [#35858](https://github.com/sgl-project/sglang/pull/35858) Cache-DiT with layerwise offload
- [#36680](https://github.com/sgl-project/sglang/pull/36680) Qwen-Image TP collectives and attention
- [#37075](https://github.com/sgl-project/sglang/pull/37075) Wan2.2 NVFP4 bias and GELU
- [#37096](https://github.com/sgl-project/sglang/pull/37096) FLUX.2 NVFP4 FC1/SwiGLU/FC2
- [#37112](https://github.com/sgl-project/sglang/pull/37112) FLUX.2 gated residual norm
- [#37141](https://github.com/sgl-project/sglang/pull/37141) FLUX.2 token concat and NVFP4 quant

</details>

<details>
<summary>Refactors (14)</summary>

- [#37210](https://github.com/sgl-project/sglang/pull/37210) black-jupyter to ruff-format
- [#37220](https://github.com/sgl-project/sglang/pull/37220) Split and rename Rust embedded server components
- [#37290](https://github.com/sgl-project/sglang/pull/37290) Rename mem-cache to sglang-radix-tree
- [#37087](https://github.com/sgl-project/sglang/pull/37087) Config round 5.2
- [#37086](https://github.com/sgl-project/sglang/pull/37086) Config round 5.1
- #37245 and similar `ReqKvInfo` moves: [#37164](https://github.com/sgl-project/sglang/pull/37164), [#37094](https://github.com/sgl-project/sglang/pull/37094), [#36982](https://github.com/sgl-project/sglang/pull/36982), [#37078](https://github.com/sgl-project/sglang/pull/37078), [#37108](https://github.com/sgl-project/sglang/pull/37108), [#37167](https://github.com/sgl-project/sglang/pull/37167)
- [#37151](https://github.com/sgl-project/sglang/pull/37151), [#37098](https://github.com/sgl-project/sglang/pull/37098), [#37091](https://github.com/sgl-project/sglang/pull/37091), [#37205](https://github.com/sgl-project/sglang/pull/37205) Unified Cache Linker series (1/N to 4/N)
- [#35245](https://github.com/sgl-project/sglang/pull/35245) Translate the KV write location once at ForwardBatch construction
- [#37299](https://github.com/sgl-project/sglang/pull/37299) Simplify hicache decode offload bookkeeping
- [#36349](https://github.com/sgl-project/sglang/pull/36349) FlyDSL fused norm kernels to the v0.3.0 stable API

</details>

<details>
<summary>Bugfixes (15)</summary>

- [#35154](https://github.com/sgl-project/sglang/pull/35154) Four boot and correctness fixes on hybrid model paths
- [#37560](https://github.com/sgl-project/sglang/pull/37560) Unified SWA non-owner v2p sizing
- [#37307](https://github.com/sgl-project/sglang/pull/37307) Forward the KV-index translator through wrapper backends
- [#35588](https://github.com/sgl-project/sglang/pull/35588) Full prefill CUDA graph padding and EAGLE capture
- [#37243](https://github.com/sgl-project/sglang/pull/37243) GLM-5.3 rebase regressions
- [#37298](https://github.com/sgl-project/sglang/pull/37298) GLM-5.3 Flash CI regressions
- [#37235](https://github.com/sgl-project/sglang/pull/37235) GLM-5.3-flash post-rebase CI regressions
- [#37026](https://github.com/sgl-project/sglang/pull/37026) Isolate hicache decode offload state per request
- [#37166](https://github.com/sgl-project/sglang/pull/37166) Make empty staging rings reusable
- [#37483](https://github.com/sgl-project/sglang/pull/37483) Poll receivers during decode preallocation
- [#37471](https://github.com/sgl-project/sglang/pull/37471) Load Qwen3.5 MTP embedding under PP
- [#35244](https://github.com/sgl-project/sglang/pull/35244) GPT-NeoX fallback and DeepSeek-VL2 KV pool config
- [#37494](https://github.com/sgl-project/sglang/pull/37494) Skip absent radix lock in cache cleanup
- [#37194](https://github.com/sgl-project/sglang/pull/37194) Graceful hicache test server shutdown
- [#37182](https://github.com/sgl-project/sglang/pull/37182) Unreachable FakeReq initialization

</details>

<details>
<summary>Docs & cookbooks (12)</summary>

- [#37655](https://github.com/sgl-project/sglang/pull/37655) K2 Horizon cookbook and H200 results
- [#37723](https://github.com/sgl-project/sglang/pull/37723) K2 Horizon MoE model names
- [#37109](https://github.com/sgl-project/sglang/pull/37109) GLM-5.3-Flash NVFP4 section
- [#37412](https://github.com/sgl-project/sglang/pull/37412) GLM-5.3-Flash NVFP4 benchmark rows
- [#37293](https://github.com/sgl-project/sglang/pull/37293) DeepSeek-V4-Flash-Vision-Exp cookbook
- [#37351](https://github.com/sgl-project/sglang/pull/37351) DeepSeek-V4 NVFP4 options
- [#37479](https://github.com/sgl-project/sglang/pull/37479) DeepSeek-V4 DGX Spark recipe
- [#37492](https://github.com/sgl-project/sglang/pull/37492) DSV4 Flash Vision on GB300
- [#37092](https://github.com/sgl-project/sglang/pull/37092) AMD v4 cookbook
- [#37781](https://github.com/sgl-project/sglang/pull/37781) AMD kimi-k3 cookbook
- [#36987](https://github.com/sgl-project/sglang/pull/36987) Replace the stale diffusion compatibility matrix
- [#35368](https://github.com/sgl-project/sglang/pull/35368) GLM-5.2 NVFP4 AgentX HiCache

</details>

<details>
<summary>Tests & CI (14)</summary>

- [#36979](https://github.com/sgl-project/sglang/pull/36979) Move gpqa and aime25 onto sgl-eval
- [#37504](https://github.com/sgl-project/sglang/pull/37504) Install sgl-eval from PyPI
- [#34074](https://github.com/sgl-project/sglang/pull/34074) Move tests onto the right CI stages
- [#36954](https://github.com/sgl-project/sglang/pull/36954) Bump FlashInfer to 0.6.18
- [#37258](https://github.com/sgl-project/sglang/pull/37258) Build Rust extensions on hosted runners in parallel
- [#37409](https://github.com/sgl-project/sglang/pull/37409) Daily ROCm 10 PR/Nightly Test
- [#37431](https://github.com/sgl-project/sglang/pull/37431) NPU DSV4-Flash / GLM-5.2 / Kimi-K3 gpqa cases
- [#37230](https://github.com/sgl-project/sglang/pull/37230) nightly-xpu-8-gpu suite
- [#37340](https://github.com/sgl-project/sglang/pull/37340) XPU Docker image release workflow
- [#37225](https://github.com/sgl-project/sglang/pull/37225) gfx1250 release image
- [#37647](https://github.com/sgl-project/sglang/pull/37647) Authenticate and retry git clones in install scripts
- [#37380](https://github.com/sgl-project/sglang/pull/37380) Revert AMD GLM-5.3-Flash recipes (#36608)
- [#37484](https://github.com/sgl-project/sglang/pull/37484) and [#37487](https://github.com/sgl-project/sglang/pull/37487) Temporarily remove GLM-5.3 Flash prefill and decode CP
- plus about 70 more minor merged changes not shown

</details>

<details>
<summary>Newly opened, in progress (highlights)</summary>

- [#37138](https://github.com/sgl-project/sglang/pull/37138), [#37137](https://github.com/sgl-project/sglang/pull/37137), [#37136](https://github.com/sgl-project/sglang/pull/37136), [#37135](https://github.com/sgl-project/sglang/pull/37135) DSV4 MXFP4 KV cache stack for Hopper (4 parts)
- [#37778](https://github.com/sgl-project/sglang/pull/37778), [#37413](https://github.com/sgl-project/sglang/pull/37413) AMD DSV4 fp8 unified_kv and HiCache
- [#37798](https://github.com/sgl-project/sglang/pull/37798), [#37796](https://github.com/sgl-project/sglang/pull/37796), [#37797](https://github.com/sgl-project/sglang/pull/37797) quantized KV pools, 2-bit MoE experts and VMM arenas
- [#37500](https://github.com/sgl-project/sglang/pull/37500), [#37570](https://github.com/sgl-project/sglang/pull/37570), [#37213](https://github.com/sgl-project/sglang/pull/37213) Qwen3.8-Flash-Next enablement (NPU, XPU)
- [#37753](https://github.com/sgl-project/sglang/pull/37753) GLM-5.3-Flash LoRA serving for miles
- [#37237](https://github.com/sgl-project/sglang/pull/37237), [#37462](https://github.com/sgl-project/sglang/pull/37462), [#37402](https://github.com/sgl-project/sglang/pull/37402) hybrid, LiLiCorr and ASD speculative decoding
- [#37436](https://github.com/sgl-project/sglang/pull/37436) test cleanup removing about 59K lines

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 50798382cf3cb36afd0a08672d96af3daa2769c8aa5aa39388828fe1d6977e78 -->
