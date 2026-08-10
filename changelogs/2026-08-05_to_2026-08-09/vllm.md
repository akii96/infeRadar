# vllm: PR digest (2026-08-05 to 2026-08-09)

_198 merged, 279 newly opened - source vllm-project/vllm, generated 2026-08-09T21:44:15Z_

## TL;DR
- **DeepSeek scaling**: DeepSeek models dominated attention this window, with major in-progress work on V4 sparse MLA, IndexCache, and sequence parallelism optimizations.
- **Attention & Kernels**: Significant upgrades to MLA landed, including per-request scheduling for chunked context, alongside massive in-progress work on "HiSparse" (host-resident sparse-MLA decode hot-buffering).
- **Quantization & MoE**: Heavy push on MXFP4 and NVFP4 quantization, including online MXFP4 support and batch-invariant NVFP4 MoE, alongside AMD ROCm AITER integrations.
- **Architecture**: KV cache offloading saw major changes, including disk offloading and Mooncake store group semantics. Bitsandbytes was migrated to an out-of-tree plugin.
- **Direction**: The engine is heavily optimizing for DeepSeek V4 / MLA architectures, standardizing FP4/FP8 MoE pipelines across NVIDIA and AMD, and decoupling heavy dependencies into plugins.

## Most important PRs
**[#50613](https://github.com/vllm-project/vllm/pull/50613)** Implements per-request scheduling for MLA chunked context, allowing finer-grained prefill scheduling for DeepSeek models to improve throughput and reduce latency spikes.
**[#49347](https://github.com/vllm-project/vllm/pull/49347)** Adds online MXFP4 quantization support, enabling on-the-fly conversion of weights to MXFP4 for supported kernels to reduce memory bandwidth without pre-quantized checkpoints.
**[#43529](https://github.com/vllm-project/vllm/pull/43529)** Migrates bitsandbytes support out of the core repository into an out-of-tree plugin, reducing core dependency bloat and establishing a cleaner boundary for third-party quantization backends.
**[#51323](https://github.com/vllm-project/vllm/pull/51323)** (Newly opened) Proposes "HiSparse", a host-resident sparse-MLA decode hot-buffering system to offload and manage MLA state on the CPU host, drastically expanding effective context capacity.
**[#51378](https://github.com/vllm-project/vllm/pull/51378)** (Newly opened) Replaces layerwise weight transfer with modelwise transactions for model reloading, shifting the distributed weight-update mechanism to a bulk transaction model to reduce synchronization stalls.

## More changes by area

<details>
<summary>Performance (27)</summary>

- [#51253](https://github.com/vllm-project/vllm/pull/51253) Shard Latent MoE up-projection for ROCm
- [#51434](https://github.com/vllm-project/vllm/pull/51434) Optimize DeepSeek V3.2 sequence parallelism
- [#50585](https://github.com/vllm-project/vllm/pull/50585) Optimize k3 dspark fused kv (4.5~4.6x kernel perf improvement)
- [#51199](https://github.com/vllm-project/vllm/pull/51199) (Opened) Add an adaptive prefill delayer for data-parallel serving
- [#51437](https://github.com/vllm-project/vllm/pull/51437) (Opened) Kimi-K3 latent-MoE: overlap shared all-reduce with routed up-projection
- [#51519](https://github.com/vllm-project/vllm/pull/51519) (Opened) Add fused-MoE tuned configs for RTX 5090
- [#50992](https://github.com/vllm-project/vllm/pull/50992) Avoid quadratic ARC batch eviction
- [#51458](https://github.com/vllm-project/vllm/pull/51458) Avoid unnecessary GPU<->CPU syncs
- [#50365](https://github.com/vllm-project/vllm/pull/50365) Drop atomic contention in sparse MLA index remap
- [#51070](https://github.com/vllm-project/vllm/pull/51070) Combine multiple all-gather together for SP
- Plus 17 more performance updates: [#51425](https://github.com/vllm-project/vllm/pull/51425), [#50904](https://github.com/vllm-project/vllm/pull/50904), [#51298](https://github.com/vllm-project/vllm/pull/51298), [#48735](https://github.com/vllm-project/vllm/pull/48735), [#50230](https://github.com/vllm-project/vllm/pull/50230), [#51238](https://github.com/vllm-project/vllm/pull/51238), [#51309](https://github.com/vllm-project/vllm/pull/51309), [#51430](https://github.com/vllm-project/vllm/pull/51430), [#51480](https://github.com/vllm-project/vllm/pull/51480), [#51540](https://github.com/vllm-project/vllm/pull/51540), [#51526](https://github.com/vllm-project/vllm/pull/51526), [#51334](https://github.com/vllm-project/vllm/pull/51334), [#51331](https://github.com/vllm-project/vllm/pull/51331), [#51314](https://github.com/vllm-project/vllm/pull/51314), [#51453](https://github.com/vllm-project/vllm/pull/51453), [#51330](https://github.com/vllm-project/vllm/pull/51330), [#51339](https://github.com/vllm-project/vllm/pull/51339)

</details>

<details>
<summary>Kernels & attention (37)</summary>

- [#51165](https://github.com/vllm-project/vllm/pull/51165) (Opened) ZoomKV v020 latest
- [#51270](https://github.com/vllm-project/vllm/pull/51270) (Opened) Add host-resident KV cache offloading for sparse MLA decode
- [#51416](https://github.com/vllm-project/vllm/pull/51416) (Opened) Add FA4 Dense and MLA
- [#51217](https://github.com/vllm-project/vllm/pull/51217) (Opened) Generalize masked activation for padded layouts
- [#51538](https://github.com/vllm-project/vllm/pull/51538) (Opened) Make DSpark work end-to-end with FLASHINFER_MLA_SPARSE_DSV4
- [#51244](https://github.com/vllm-project/vllm/pull/51244) (Opened) Optimize MHC post + HC head + RMSNorm fusions for DeepSeek V4
- [#50294](https://github.com/vllm-project/vllm/pull/50294) Optimize FA4 mm_prefix range lookup
- [#50578](https://github.com/vllm-project/vllm/pull/50578) Use asm decode for non-divisor small head counts in ROCm MLA
- [#49453](https://github.com/vllm-project/vllm/pull/49453) Add MLA backend so DeepSeek-V2/V3 can run on CPU
- [#45187](https://github.com/vllm-project/vllm/pull/45187) Add NVFP4 KV 4-over-6 scale search
- Plus 27 more kernel and attention updates: [#50480](https://github.com/vllm-project/vllm/pull/50480), [#49932](https://github.com/vllm-project/vllm/pull/49932), [#51457](https://github.com/vllm-project/vllm/pull/51457), [#50185](https://github.com/vllm-project/vllm/pull/50185), [#50980](https://github.com/vllm-project/vllm/pull/50980), [#48847](https://github.com/vllm-project/vllm/pull/48847), [#51083](https://github.com/vllm-project/vllm/pull/51083), [#44857](https://github.com/vllm-project/vllm/pull/44857), [#49599](https://github.com/vllm-project/vllm/pull/49599), [#51195](https://github.com/vllm-project/vllm/pull/51195), [#51555](https://github.com/vllm-project/vllm/pull/51555), [#51315](https://github.com/vllm-project/vllm/pull/51315), [#51119](https://github.com/vllm-project/vllm/pull/51119), [#51209](https://github.com/vllm-project/vllm/pull/51209), [#51508](https://github.com/vllm-project/vllm/pull/51508), [#51091](https://github.com/vllm-project/vllm/pull/51091), [#51565](https://github.com/vllm-project/vllm/pull/51565), [#51489](https://github.com/vllm-project/vllm/pull/51489), [#51506](https://github.com/vllm-project/vllm/pull/51506), [#51203](https://github.com/vllm-project/vllm/pull/51203), [#51318](https://github.com/vllm-project/vllm/pull/51318), [#51252](https://github.com/vllm-project/vllm/pull/51252), [#51257](https://github.com/vllm-project/vllm/pull/51257), [#51183](https://github.com/vllm-project/vllm/pull/51183), [#51406](https://github.com/vllm-project/vllm/pull/51406), [#51368](https://github.com/vllm-project/vllm/pull/51368), [#51515](https://github.com/vllm-project/vllm/pull/51515), [#51202](https://github.com/vllm-project/vllm/pull/51202)

</details>

<details>
<summary>MoE & quantization (38)</summary>

- [#49375](https://github.com/vllm-project/vllm/pull/49375) Add More AITER quantization/MoE kernel tests
- [#49610](https://github.com/vllm-project/vllm/pull/49610) Refactor humming linear and moe backends to use explicit layer configs
- [#44359](https://github.com/vllm-project/vllm/pull/44359) Share apply_moe_activation support metadata
- [#40372](https://github.com/vllm-project/vllm/pull/40372) Batch invariant NVFP4 MoE using cutlass
- [#49601](https://github.com/vllm-project/vllm/pull/49601) Copy over `new_data` attributes in `replace_parameter`
- [#49764](https://github.com/vllm-project/vllm/pull/49764) Share online weight scales across TP
- [#47106](https://github.com/vllm-project/vllm/pull/47106) Support Nvfp4 Cutedsl Moe Swiglu-oai and Relu2 Activation
- [#50949](https://github.com/vllm-project/vllm/pull/50949) Optimize routed FP8/MXFP4 MoE GEMM dispatch on CPU
- [#50029](https://github.com/vllm-project/vllm/pull/50029) Preserve precision in online NVFP4 expert packing
- [#48476](https://github.com/vllm-project/vllm/pull/48476) Support MXFP8 linear weights for INC DeepSeek V4 model
- Plus 28 more MoE and quantization updates: [#50905](https://github.com/vllm-project/vllm/pull/50905), [#51093](https://github.com/vllm-project/vllm/pull/51093), [#51495](https://github.com/vllm-project/vllm/pull/51495), [#51125](https://github.com/vllm-project/vllm/pull/51125), [#50937](https://github.com/vllm-project/vllm/pull/50937), [#50833](https://github.com/vllm-project/vllm/pull/50833), [#51002](https://github.com/vllm-project/vllm/pull/51002), [#51411](https://github.com/vllm-project/vllm/pull/51411), [#50405](https://github.com/vllm-project/vllm/pull/50405), [#51442](https://github.com/vllm-project/vllm/pull/51442), [#51294](https://github.com/vllm-project/vllm/pull/51294), [#51563](https://github.com/vllm-project/vllm/pull/51563), [#51285](https://github.com/vllm-project/vllm/pull/51285), [#51569](https://github.com/vllm-project/vllm/pull/51569), [#51392](https://github.com/vllm-project/vllm/pull/51392), [#51248](https://github.com/vllm-project/vllm/pull/51248), [#51265](https://github.com/vllm-project/vllm/pull/51265), [#51274](https://github.com/vllm-project/vllm/pull/51274), [#51332](https://github.com/vllm-project/vllm/pull/51332), [#51477](https://github.com/vllm-project/vllm/pull/51477), [#51568](https://github.com/vllm-project/vllm/pull/51568), [#51473](https://github.com/vllm-project/vllm/pull/51473), [#51158](https://github.com/vllm-project/vllm/pull/51158), [#51407](https://github.com/vllm-project/vllm/pull/51407), [#51419](https://github.com/vllm-project/vllm/pull/51419), [#51204](https://github.com/vllm-project/vllm/pull/51204), [#51398](https://github.com/vllm-project/vllm/pull/51398), [#51148](https://github.com/vllm-project/vllm/pull/51148), [#51415](https://github.com/vllm-project/vllm/pull/51415)

</details>

<details>
<summary>Model support (19)</summary>

- [#51045](https://github.com/vllm-project/vllm/pull/51045) Add Ling 3.0 Flash BF16, MTP, and parser support
- [#51149](https://github.com/vllm-project/vllm/pull/51149) Interns2mobius support
- [#48355](https://github.com/vllm-project/vllm/pull/48355) Extended EPLB support for Mistral Large 3 and additional MoE backends
- [#47972](https://github.com/vllm-project/vllm/pull/47972) Support DeepSeek-V4 AMD Quark NVFP4 with emulation kernel
- [#45254](https://github.com/vllm-project/vllm/pull/45254) Support ViT full CUDA graph for Ernie-4.5-VL image inference
- [#51288](https://github.com/vllm-project/vllm/pull/51288) Add packed DeepSeek-V4 KV zeroer geometry regression
- [#50068](https://github.com/vllm-project/vllm/pull/50068) Enable Qwen3.8 for AMD Rocm
- [#51249](https://github.com/vllm-project/vllm/pull/51249) Add missing fused_qkv_a_proj to Kimi-Linear packed_modules_mapping
- [#51255](https://github.com/vllm-project/vllm/pull/51255) (Opened) Add Dots3 NOTE language model support
- [#51129](https://github.com/vllm-project/vllm/pull/51129) (Opened) Support Solar Open2
- Plus 9 more model support updates: [#51237](https://github.com/vllm-project/vllm/pull/51237), [#51168](https://github.com/vllm-project/vllm/pull/51168), [#51221](https://github.com/vllm-project/vllm/pull/51221), [#51558](https://github.com/vllm-project/vllm/pull/51558), [#51578](https://github.com/vllm-project/vllm/pull/51578), [#51498](https://github.com/vllm-project/vllm/pull/51498), [#51346](https://github.com/vllm-project/vllm/pull/51346), [#51394](https://github.com/vllm-project/vllm/pull/51394), [#51130](https://github.com/vllm-project/vllm/pull/51130)

</details>

<details>
<summary>Parallelism & scheduling (34)</summary>

- [#50902](https://github.com/vllm-project/vllm/pull/50902) Stateful Trainer Send: NCCL + Sparse NCCL [3/N]
- [#50390](https://github.com/vllm-project/vllm/pull/50390) Remove duplicate image preprocessing in EPD and enable preprocess on GPU
- [#44956](https://github.com/vllm-project/vllm/pull/44956) Add store group semantics to Mooncake KV Connector
- [#49644](https://github.com/vllm-project/vllm/pull/49644) Add disk offloading support to SimpleCPUOffloadConnector
- [#50507](https://github.com/vllm-project/vllm/pull/50507) Support partial-tail prefix reuse with fine-grained prefix matching
- [#51243](https://github.com/vllm-project/vllm/pull/51243) Emit self-describing events for partial recurrent blocks
- [#51007](https://github.com/vllm-project/vllm/pull/51007) Support out-of-tree secondary tier managers via `module_path`
- [#48069](https://github.com/vllm-project/vllm/pull/48069) Add tenant ID support to MooncakeStoreConnector
- [#50321](https://github.com/vllm-project/vllm/pull/50321) Support partial secondary-tier load results
- [#51161](https://github.com/vllm-project/vllm/pull/51161) Handle chunked local attention in offloading scheduler
- Plus 24 more parallelism and scheduling updates: [#48061](https://github.com/vllm-project/vllm/pull/48061), [#51358](https://github.com/vllm-project/vllm/pull/51358), [#51414](https://github.com/vllm-project/vllm/pull/51414), [#51479](https://github.com/vllm-project/vllm/pull/51479), [#51520](https://github.com/vllm-project/vllm/pull/51520), [#51267](https://github.com/vllm-project/vllm/pull/51267), [#51207](https://github.com/vllm-project/vllm/pull/51207), [#51241](https://github.com/vllm-project/vllm/pull/51241), [#51527](https://github.com/vllm-project/vllm/pull/51527), [#51375](https://github.com/vllm-project/vllm/pull/51375), [#51384](https://github.com/vllm-project/vllm/pull/51384), [#51324](https://github.com/vllm-project/vllm/pull/51324), [#51301](https://github.com/vllm-project/vllm/pull/51301), [#51548](https://github.com/vllm-project/vllm/pull/51548), [#51317](https://github.com/vllm-project/vllm/pull/51317), [#51377](https://github.com/vllm-project/vllm/pull/51377), [#51485](https://github.com/vllm-project/vllm/pull/51485), [#51532](https://github.com/vllm-project/vllm/pull/51532), [#51448](https://github.com/vllm-project/vllm/pull/51448), [#51576](https://github.com/vllm-project/vllm/pull/51576), [#51228](https://github.com/vllm-project/vllm/pull/51228), [#51351](https://github.com/vllm-project/vllm/pull/51351), [#51362](https://github.com/vllm-project/vllm/pull/51362), [#51421](https://github.com/vllm-project/vllm/pull/51421), [#51369](https://github.com/vllm-project/vllm/pull/51369)

</details>

<details>
<summary>Hardware & arch (17)</summary>

- [#48646](https://github.com/vllm-project/vllm/pull/48646) Reuse equivalent ROCm CI images
- [#50649](https://github.com/vllm-project/vllm/pull/50649) Kimi-K3 Fix KDA NaN on mixed batches and racy autotune config
- [#50802](https://github.com/vllm-project/vllm/pull/50802) Fix AITER all-reduce fusion coverage
- [#50007](https://github.com/vllm-project/vllm/pull/50007) Add tuned selective_state_update float32 config for AMD Instinct MI325X
- [#50126](https://github.com/vllm-project/vllm/pull/50126) Enable pinned memory on supported WSL2 kernels
- [#50841](https://github.com/vllm-project/vllm/pull/50841) Enable tcmalloc for s390x
- [#51357](https://github.com/vllm-project/vllm/pull/51357) Fix ROCm architecture import on non-ROCm platforms
- [#51160](https://github.com/vllm-project/vllm/pull/51160) Support MultiConnector accuracy testing on XPU
- [#50526](https://github.com/vllm-project/vllm/pull/50526) Alias is_current_stream_capturing to XPU in cuda wrapper
- [#51242](https://github.com/vllm-project/vllm/pull/51242) Remove the XPU branch of topk_softplus_sqrt
- Plus 7 more hardware and arch updates: [#51060](https://github.com/vllm-project/vllm/pull/51060), [#50607](https://github.com/vllm-project/vllm/pull/50607), [#51058](https://github.com/vllm-project/vllm/pull/51058), [#51349](https://github.com/vllm-project/vllm/pull/51349), [#51159](https://github.com/vllm-project/vllm/pull/51159), [#51132](https://github.com/vllm-project/vllm/pull/51132), [#51379](https://github.com/vllm-project/vllm/pull/51379)

</details>

<details>
<summary>API & serving (40)</summary>

- [#46727](https://github.com/vllm-project/vllm/pull/46727) Support thinking_token_budget in Model Runner V2
- [#50289](https://github.com/vllm-project/vllm/pull/50289) Add standalone Rust renderer
- [#51438](https://github.com/vllm-project/vllm/pull/51438) Reserve spec-decode lookahead blocks in V2 warmup
- [#50939](https://github.com/vllm-project/vllm/pull/50939) Fix -1 placeholder draft token ids in rejection sampler
- [#50910](https://github.com/vllm-project/vllm/pull/50910) Cache draft logits in model's LM head dtype
- [#51310](https://github.com/vllm-project/vllm/pull/51310) Register Qwen3.6 dSpark acceptance coverage
- [#43417](https://github.com/vllm-project/vllm/pull/43417) Watch frontend processes during engine startup
- [#51089](https://github.com/vllm-project/vllm/pull/51089) Parse request priority from HTTP header
- [#50275](https://github.com/vllm-project/vllm/pull/50275) Don't stop an encoder-instance request before its images are encoded
- [#50916](https://github.com/vllm-project/vllm/pull/50916) Disable uvicorn signal handlers instead of racing them
- Plus 30 more API and serving updates: [#48341](https://github.com/vllm-project/vllm/pull/48341), [#51413](https://github.com/vllm-project/vllm/pull/51413), [#51153](https://github.com/vllm-project/vllm/pull/51153), [#51577](https://github.com/vllm-project/vllm/pull/51577), [#51449](https://github.com/vllm-project/vllm/pull/51449), [#51360](https://github.com/vllm-project/vllm/pull/51360), [#51144](https://github.com/vllm-project/vllm/pull/51144), [#51535](https://github.com/vllm-project/vllm/pull/51535), [#51350](https://github.com/vllm-project/vllm/pull/51350), [#51316](https://github.com/vllm-project/vllm/pull/51316), [#51433](https://github.com/vllm-project/vllm/pull/51433), [#51354](https://github.com/vllm-project/vllm/pull/51354), [#51450](https://github.com/vllm-project/vllm/pull/51450), [#51447](https://github.com/vllm-project/vllm/pull/51447), [#51321](https://github.com/vllm-project/vllm/pull/51321), [#51478](https://github.com/vllm-project/vllm/pull/51478), [#51488](https://github.com/vllm-project/vllm/pull/51488), [#51155](https://github.com/vllm-project/vllm/pull/51155), [#51554](https://github.com/vllm-project/vllm/pull/51554), [#51178](https://github.com/vllm-project/vllm/pull/51178), [#51167](https://github.com/vllm-project/vllm/pull/51167), [#51502](https://github.com/vllm-project/vllm/pull/51502), [#51343](https://github.com/vllm-project/vllm/pull/51343), [#51487](https://github.com/vllm-project/vllm/pull/51487), [#51444](https://github.com/vllm-project/vllm/pull/51444), [#51460](https://github.com/vllm-project/vllm/pull/51460), [#51484](https://github.com/vllm-project/vllm/pull/51484), [#51509](https://github.com/vllm-project/vllm/pull/51509), [#51445](https://github.com/vllm-project/vllm/pull/51445), [#51443](https://github.com/vllm-project/vllm/pull/51443)

</details>

<details>
<summary>Refactors (5)</summary>

- [#50981](https://github.com/vllm-project/vllm/pull/50981) Refactor throughput and reuse serve's get samples
- [#51051](https://github.com/vllm-project/vllm/pull/51051) Remove kernel dead code
- [#51078](https://github.com/vllm-project/vllm/pull/51078) Remove MoE legacy code
- [#50066](https://github.com/vllm-project/vllm/pull/50066) Make PCPManager construction extensible
- [#51491](https://github.com/vllm-project/vllm/pull/51491) (Opened) Sequence parallel refactor

</details>

<details>
<summary>Bugfixes (76)</summary>

- [#49328](https://github.com/vllm-project/vllm/pull/49328) Fix failed-load livelock by marking the lookup verdict as a miss
- [#51455](https://github.com/vllm-project/vllm/pull/51455) Make the GPU sync check thread-local and fix its suppressors
- [#51391](https://github.com/vllm-project/vllm/pull/51391) Prevent Inkling block-end leakage with tools
- [#48977](https://github.com/vllm-project/vllm/pull/48977) Mypy fix for "vllm/model_executor/models/[aA][bB]"
- [#51113](https://github.com/vllm-project/vllm/pull/51113) Keep mamba align prefill chunks block-aligned past last_cache_position
- [#48758](https://github.com/vllm-project/vllm/pull/48758) Fix prefix caching in NixlPush
- [#39935](https://github.com/vllm-project/vllm/pull/39935) Fix level-2 sleep/wake/reload with enable_lora=True
- [#48413](https://github.com/vllm-project/vllm/pull/48413) Fix MiniCPM-V placeholder replacement and image processor loading
- [#51116](https://github.com/vllm-project/vllm/pull/51116) Fall back when MADV_POPULATE_WRITE is unsupported
- [#50958](https://github.com/vllm-project/vllm/pull/50958) Gemma3n/Gemma4: pad variable-length audio batches
- Plus 66 more bugfixes: [#51227](https://github.com/vllm-project/vllm/pull/51227), [#48929](https://github.com/vllm-project/vllm/pull/48929), [#49397](https://github.com/vllm-project/vllm/pull/49397), [#50965](https://github.com/vllm-project/vllm/pull/50965), [#51222](https://github.com/vllm-project/vllm/pull/51222), [#51095](https://github.com/vllm-project/vllm/pull/51095), [#50890](https://github.com/vllm-project/vllm/pull/50890), [#51468](https://github.com/vllm-project/vllm/pull/51468), [#50358](https://github.com/vllm-project/vllm/pull/50358), [#48534](https://github.com/vllm-project/vllm/pull/48534), [#50276](https://github.com/vllm-project/vllm/pull/50276), [#49206](https://github.com/vllm-project/vllm/pull/49206), [#51108](https://github.com/vllm-project/vllm/pull/51108), [#50393](https://github.com/vllm-project/vllm/pull/50393), [#51050](https://github.com/vllm-project/vllm/pull/51050), [#50960](https://github.com/vllm-project/vllm/pull/50960), [#49876](https://github.com/vllm-project/vllm/pull/49876), [#51435](https://github.com/vllm-project/vllm/pull/51435), [#50183](https://github.com/vllm-project/vllm/pull/50183), [#38771](https://github.com/vllm-project/vllm/pull/38771), [#51402](https://github.com/vllm-project/vllm/pull/51402), [#49212](https://github.com/vllm-project/vllm/pull/49212), [#51185](https://github.com/vllm-project/vllm/pull/51185), [#49373](https://github.com/vllm-project/vllm/pull/49373), [#51076](https://github.com/vllm-project/vllm/pull/51076), [#51100](https://github.com/vllm-project/vllm/pull/51100), [#51260](https://github.com/vllm-project/vllm/pull/51260), [#51469](https://github.com/vllm-project/vllm/pull/51469), [#50827](https://github.com/vllm-project/vllm/pull/50827), [#51432](https://github.com/vllm-project/vllm/pull/51432), [#51365](https://github.com/vllm-project/vllm/pull/51365), [#50355](https://github.com/vllm-project/vllm/pull/50355), [#51092](https://github.com/vllm-project/vllm/pull/51092), [#51427](https://github.com/vllm-project/vllm/pull/51427), [#50404](https://github.com/vllm-project/vllm/pull/50404), [#51180](https://github.com/vllm-project/vllm/pull/51180), [#51179](https://github.com/vllm-project/vllm/pull/51179), [#51219](https://github.com/vllm-project/vllm/pull/51219), [#51539](https://github.com/vllm-project/vllm/pull/51539), [#51224](https://github.com/vllm-project/vllm/pull/51224), [#51131](https://github.com/vllm-project/vllm/pull/51131), [#51341](https://github.com/vllm-project/vllm/pull/51341), [#51417](https://github.com/vllm-project/vllm/pull/51417), [#51177](https://github.com/vllm-project/vllm/pull/51177), [#51504](https://github.com/vllm-project/vllm/pull/51504), [#51536](https://github.com/vllm-project/vllm/pull/51536), [#51338](https://github.com/vllm-project/vllm/pull/51338), [#51137](https://github.com/vllm-project/vllm/pull/51137), [#51295](https://github.com/vllm-project/vllm/pull/51295), [#51517](https://github.com/vllm-project/vllm/pull/51517), [#51404](https://github.com/vllm-project/vllm/pull/51404), [#51355](https://github.com/vllm-project/vllm/pull/51355), [#51307](https://github.com/vllm-project/vllm/pull/51307), [#51141](https://github.com/vllm-project/vllm/pull/51141), [#51560](https://github.com/vllm-project/vllm/pull/51560), [#51388](https://github.com/vllm-project/vllm/pull/51388), [#51236](https://github.com/vllm-project/vllm/pull/51236), [#51547](https://github.com/vllm-project/vllm/pull/51547), [#51483](https://github.com/vllm-project/vllm/pull/51483), [#51426](https://github.com/vllm-project/vllm/pull/51426), [#51157](https://github.com/vllm-project/vllm/pull/51157), [#51230](https://github.com/vllm-project/vllm/pull/51230), [#51505](https://github.com/vllm-project/vllm/pull/51505), [#51490](https://github.com/vllm-project/vllm/pull/51490), [#51550](https://github.com/vllm-project/vllm/pull/51550), [#51471](https://github.com/vllm-project/vllm/pull/51471), [#51481](https://github.com/vllm-project/vllm/pull/51481), [#51262](https://github.com/vllm-project/vllm/pull/51262), [#51524](https://github.com/vllm-project/vllm/pull/51524), [#51139](https://github.com/vllm-project/vllm/pull/51139), [#51496](https://github.com/vllm-project/vllm/pull/51496), [#51306](https://github.com/vllm-project/vllm/pull/51306), [#51373](https://github.com/vllm-project/vllm/pull/51373), [#51133](https://github.com/vllm-project/vllm/pull/51133), [#51172](https://github.com/vllm-project/vllm/pull/51172), [#51229](https://github.com/vllm-project/vllm/pull/51229), [#51299](https://github.com/vllm-project/vllm/pull/51299), [#51501](https://github.com/vllm-project/vllm/pull/51501), [#51574](https://github.com/vllm-project/vllm/pull/51574), [#51364](https://github.com/vllm-project/vllm/pull/51364), [#51514](https://github.com/vllm-project/vllm/pull/51514), [#51400](https://github.com/vllm-project/vllm/pull/51400), [#51423](https://github.com/vllm-project/vllm/pull/51423), [#51296](https://github.com/vllm-project/vllm/pull/51296), [#51556](https://github.com/vllm-project/vllm/pull/51556), [#51201](https://github.com/vllm-project/vllm/pull/51201), [#51120](https://github.com/vllm-project/vllm/pull/51120)

</details>

<details>
<summary>Tests, CI & build, Docs, Misc (61)</summary>

- [#50411](https://github.com/vllm-project/vllm/pull/50411) Fused mm preprocess normalisation on the Device
- [#51247](https://github.com/vllm-project/vllm/pull/51247) Fully generalise input embedding handling in Transformers modelling backend
- [#51068](https://github.com/vllm-project/vllm/pull/51068) Prune redundant tests points in `correctness_e2e`
- [#51069](https://github.com/vllm-project/vllm/pull/51069) Prune `PyTorch Compilation Unit Tests`
- [#51408](https://github.com/vllm-project/vllm/pull/51408) Harden Transformers modelling backend multi-modal path
- Plus 56 more minor updates: [#50940](https://github.com/vllm-project/vllm/pull/50940), [#51074](https://github.com/vllm-project/vllm/pull/51074), [#51087](https://github.com/vllm-project/vllm/pull/51087), [#50930](https://github.com/vllm-project/vllm/pull/50930), [#50840](https://github.com/vllm-project/vllm/pull/50840), [#51300](https://github.com/vllm-project/vllm/pull/51300), [#51067](https://github.com/vllm-project/vllm/pull/51067), [#45694](https://github.com/vllm-project/vllm/pull/45694), [#51440](https://github.com/vllm-project/vllm/pull/51440), [#51046](https://github.com/vllm-project/vllm/pull/51046), [#49990](https://github.com/vllm-project/vllm/pull/49990), [#50892](https://github.com/vllm-project/vllm/pull/50892), [#50236](https://github.com/vllm-project/vllm/pull/50236), [#51410](https://github.com/vllm-project/vllm/pull/51410), [#51337](https://github.com/vllm-project/vllm/pull/51337), [#50805](https://github.com/vllm-project/vllm/pull/50805), [#51173](https://github.com/vllm-project/vllm/pull/51173), [#51451](https://github.com/vllm-project/vllm/pull/51451), [#51273](https://github.com/vllm-project/vllm/pull/51273), [#51127](https://github.com/vllm-project/vllm/pull/51127), [#51271](https://github.com/vllm-project/vllm/pull/51271), [#51215](https://github.com/vllm-project/vllm/pull/51215), [#50448](https://github.com/vllm-project/vllm/pull/50448), [#51304](https://github.com/vllm-project/vllm/pull/51304), [#51176](https://github.com/vllm-project/vllm/pull/51176), [#51389](https://github.com/vllm-project/vllm/pull/51389), [#48668](https://github.com/vllm-project/vllm/pull/48668), [#51210](https://github.com/vllm-project/vllm/pull/51210), [#50942](https://github.com/vllm-project/vllm/pull/50942), [#51529](https://github.com/vllm-project/vllm/pull/51529), [#51107](https://github.com/vllm-project/vllm/pull/51107), [#51196](https://github.com/vllm-project/vllm/pull/51196), [#51293](https://github.com/vllm-project/vllm/pull/51293), [#51523](https://github.com/vllm-project/vllm/pull/51523), [#51570](https://github.com/vllm-project/vllm/pull/51570), [#51280](https://github.com/vllm-project/vllm/pull/51280), [#51459](https://github.com/vllm-project/vllm/pull/51459), [#51528](https://github.com/vllm-project/vllm/pull/51528), [#51559](https://github.com/vllm-project/vllm/pull/51559), [#51446](https://github.com/vllm-project/vllm/pull/51446), [#51553](https://github.com/vllm-project/vllm/pull/51553), [#51171](https://github.com/vllm-project/vllm/pull/51171), [#51335](https://github.com/vllm-project/vllm/pull/51335), [#51239](https://github.com/vllm-project/vllm/pull/51239), [#51245](https://github.com/vllm-project/vllm/pull/51245), [#51261](https://github.com/vllm-project/vllm/pull/51261), [#51466](https://github.com/vllm-project/vllm/pull/51466), [#51381](https://github.com/vllm-project/vllm/pull/51381), [#51218](https://github.com/vllm-project/vllm/pull/51218), [#51276](https://github.com/vllm-project/vllm/pull/51276), [#51367](https://github.com/vllm-project/vllm/pull/51367), [#51235](https://github.com/vllm-project/vllm/pull/51235), [#51503](https://github.com/vllm-project/vllm/pull/51503), [#51512](https://github.com/vllm-project/vllm/pull/51512), [#51308](https://github.com/vllm-project/vllm/pull/51308), [#51263](https://github.com/vllm-project/vllm/pull/51263), [#51184](https://github.com/vllm-project/vllm/pull/51184)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: ffcf980fcbd43f7f2497ab08cbdfc9871b963735a16f7a870b600cb9f13246d2 -->
