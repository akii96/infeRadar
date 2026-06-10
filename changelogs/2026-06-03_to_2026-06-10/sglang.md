# sglang: PR digest (2026-06-03 to 2026-06-10)

_373 merged, 348 newly opened - source sgl-project/sglang, generated 2026-06-10T13:28:42Z_

## TL;DR
- **Model Focus**: DeepSeek dominated attention this window (44 PRs), alongside significant work on GLM, Gemma, and MiniMax. Multimodal and diffusion capabilities expanded heavily with OmniDreams, SANA-WM, and Wan 2.1.
- **Performance & Kernels**: Major investments landed for next-gen hardware formats, including FP8/NVFP4 optimizations for MoE and LoRA, and massive multi-arch ROCm kernel support.
- **Caching & Scheduling**: Introduced TensorCast storage for HiCache, alongside extensive work on chunked prefill, speculative decoding (Spec V2), and stateless scheduler sandboxing.
- **Overall Direction**: The engine is aggressively optimizing for emerging quantization formats (FP8/NVFP4/MXFP4) and multi-arch compatibility (AMD/NPU/Intel XPU), while heavily expanding its diffusion and multimodal serving footprint.

## Most important PRs
- **[#27329](https://github.com/sgl-project/sglang/pull/27329)** introduces an experimental fast LoRA path utilizing the `sgl_trtllm` MoE backend, unlocking significant performance gains for FP8 and NVFP4 models on NVIDIA hardware.
- **[#27745](https://github.com/sgl-project/sglang/pull/27745)** delivers massive multi-arch ROCm kernel support with runtime optimizations, drastically improving the engine's performance and compatibility across AMD GPUs.
- **[#23906](https://github.com/sgl-project/sglang/pull/23906)** executes a major refactor of the CUDA Graph Runner and backend, unifying input buffers and improving maintainability across attention, MoE, and speculative decoding paths.
- **[#27531](https://github.com/sgl-project/sglang/pull/27531)** adds support for the SANA-WM diffusion model with streaming capabilities, marking a major feature addition for the engine's multimodal serving.
- **[#27265](https://github.com/sgl-project/sglang/pull/27265)** introduces TensorCast storage as a new backend for HiCache, expanding the engine's caching flexibility and performance for large-scale deployments.

## More changes by area

<details>
<summary>Performance (17)</summary>

- [#27063](https://github.com/sgl-project/sglang/pull/27063) Optimize gpt-oss-120B performance on AMD
- [#26496](https://github.com/sgl-project/sglang/pull/26496) Changes for SM120 perf and usability for NVFP4
- [#26733](https://github.com/sgl-project/sglang/pull/26733) Nemotron perf changes
- [#27431](https://github.com/sgl-project/sglang/pull/27431) Run LTX-2 VAE decode in channels_last_3d for faster decode and lower peak memory
- [#26861](https://github.com/sgl-project/sglang/pull/26861) Reduce transient allocations in NVFP4 MoE setup
- [#27364](https://github.com/sgl-project/sglang/pull/27364) Reduce radix cache match overhead by changing the match algorithm
- [#27320](https://github.com/sgl-project/sglang/pull/27320) Parallelize create_flashmla_kv_indices over page-blocks
- [#27180](https://github.com/sgl-project/sglang/pull/27180) Add ZMQ IPv6 support, bench_serving sampling params, and reduce routed_dp_rank log noise
- [#27382](https://github.com/sgl-project/sglang/pull/27382) Split-KV flash-decode attention for EAGLE target-verify on Triton backend
- [#27658](https://github.com/sgl-project/sglang/pull/27658) Add compact linear spec cache replay to reduce intermediate cache memory
- [#27105](https://github.com/sgl-project/sglang/pull/27105) Offload the sync HF processor off the TokenizerManager event loop
- [#27776](https://github.com/sgl-project/sglang/pull/27776) Remove sampler hot-path sync for custom logit processors
- [#27183](https://github.com/sgl-project/sglang/pull/27183) YOCO fast-prefill for Gemma4 E2B/E4B
- [#27656](https://github.com/sgl-project/sglang/pull/27656) Fuse QK RMSNorm + gate extraction Triton kernel for Qwen3.5 on HIP
- [#27423](https://github.com/sgl-project/sglang/pull/27423) Support moe reduce scatter for DeepSeek V4 when using DP-Attention+TP-MOE
- [#27689](https://github.com/sgl-project/sglang/pull/27689) Remove blocking D2H in spec-decode plan for FlashInfer MLA
- [#27609](https://github.com/sgl-project/sglang/pull/27609) Disable MiniMax-M2.7 custom all-reduce on gfx942

</details>

<details>
<summary>Kernels & attention (36)</summary>

- [#27380](https://github.com/sgl-project/sglang/pull/27380) Add unified kv attention support in dpsk-v4 for AMD
- [#25418](https://github.com/sgl-project/sglang/pull/25418) Integrate flash_mla_sparse_fwd
- [#27361](https://github.com/sgl-project/sglang/pull/27361) Fix dual-chunk sparse fallback index overflow
- [#27617](https://github.com/sgl-project/sglang/pull/27617) Cache full→SWA out_cache_loc per forward across attention backends
- [#25195](https://github.com/sgl-project/sglang/pull/25195) Support breakable CUDA graph for DeepSeek V4 DP attention
- [#27695](https://github.com/sgl-project/sglang/pull/27695) Bundle set_kv_buffer write targets into KVWriteLoc
- [#27188](https://github.com/sgl-project/sglang/pull/27188) Fix TP2 DeepSeek-R1 nhead=64 MLA decode crash and add nightly coverage
- [#27193](https://github.com/sgl-project/sglang/pull/27193) Replace skip_attn_backend_init with a batch-carried attention plan marker
- [#23280](https://github.com/sgl-project/sglang/pull/23280) Enable Gemma 4 E2B / E4B / 31B/ 26B-A4B on Intel XPU
- [#22299](https://github.com/sgl-project/sglang/pull/22299) Enable Piecewise CUDA Graph for AMD GPUs
- [#27233](https://github.com/sgl-project/sglang/pull/27233) Fuse small kenrels under `gather_spec_extras`
- [#23927](https://github.com/sgl-project/sglang/pull/23927) Replace fp8 mla with fp8 mha kernel for diffusion model aiter backend
- [#27166](https://github.com/sgl-project/sglang/pull/27166) Reland "Support NextN = 2/4 in DSV32"
- [#24870](https://github.com/sgl-project/sglang/pull/24870) Support NextN = 2/4 in DSV32
- [#27138](https://github.com/sgl-project/sglang/pull/27138) Revert "Support NextN = 2/4 in DSV32"
- [#27316](https://github.com/sgl-project/sglang/pull/27316) Delegate init_mha_chunk_metadata in HybridLinearAttnBackend
- [#26460](https://github.com/sgl-project/sglang/pull/26460) Add xpu_attn backend for encoder vision attention on Intel GPU
- [#26894](https://github.com/sgl-project/sglang/pull/26894) Fuse compress norm+rope+hadamard into single Triton kernel on AMD
- [#27475](https://github.com/sgl-project/sglang/pull/27475) Dedup draft `kv_indices` sizing into `spec_utils` helpers
- [#27491](https://github.com/sgl-project/sglang/pull/27491) Fix SWA pool resolution for EAGLE draft workers
- [#27114](https://github.com/sgl-project/sglang/pull/27114) Restore overridden HF config fields and support index_skip_topk_offset for DSA topk sharing
- [#27485](https://github.com/sgl-project/sglang/pull/27485) Fix aiter MLA verify `kv_indices` under-alloc + shared `assert_buffer_fits` guard
- [#27453](https://github.com/sgl-project/sglang/pull/27453) Remove FlashInfer GB transport workaround
- [#26914](https://github.com/sgl-project/sglang/pull/26914) Remove BF16-to-FP32 elementwise cast from compressor GEMM on HIP
- [#27488](https://github.com/sgl-project/sglang/pull/27488) Add CuteDSL Prefill Kernel on SM100
- [#27594](https://github.com/sgl-project/sglang/pull/27594) Add M-aware fp8 block-scale GEMM dispatch in dpsk-v4
- [#27397](https://github.com/sgl-project/sglang/pull/27397) Support JIT fused A GEMM and support GLM-5 hidden size on SM120
- [#27705](https://github.com/sgl-project/sglang/pull/27705) Fuse the DSA indexer Q/K paths into single kernels
- [#27706](https://github.com/sgl-project/sglang/pull/27706) Support DFLASH with DP attention
- [#27638](https://github.com/sgl-project/sglang/pull/27638) Add DFlash speculative decoding for the MiMo-V2.5 Pro MXFP4 target
- [#27429](https://github.com/sgl-project/sglang/pull/27429) Centralize more inline Triton kernels
- [#27673](https://github.com/sgl-project/sglang/pull/27673) Integrating LiteAttention Backend
- [#27436](https://github.com/sgl-project/sglang/pull/27436) Enable breakable CUDA graph for diffusion DiTs
- [#27110](https://github.com/sgl-project/sglang/pull/27110) Nemotron support on sglang-miles
- [#27099](https://github.com/sgl-project/sglang/pull/27099) Add support for DeepSeekV4 on cpu_graph_runner
- [#27178](https://github.com/sgl-project/sglang/pull/27178) Add opt-in PDL support to LoRA kernels
- plus 19 more minor kernel and attention updates

</details>

<details>
<summary>MoE & quantization (21)</summary>

- [#26083](https://github.com/sgl-project/sglang/pull/26083) Implement online nvfp4 quantization
- [#25655](https://github.com/sgl-project/sglang/pull/25655) Add w4a16 moe support to nemotron
- [#26786](https://github.com/sgl-project/sglang/pull/26786) Refactor CPU quantization schemes
- [#27150](https://github.com/sgl-project/sglang/pull/27150) Support Waterfill with dynamic EPLB
- [#26746](https://github.com/sgl-project/sglang/pull/26746) Support optional kwargs in AITER fused_moe runner
- [#26349](https://github.com/sgl-project/sglang/pull/26349) Support specific pass of bias_grouped_topk for xpu
- [#18005](https://github.com/sgl-project/sglang/pull/18005) Online MXFP4 quantization for dense and MOE models with original BF16 weight
- [#26588](https://github.com/sgl-project/sglang/pull/26588) Optimize Gemma4 H200 MoE and extend attention
- [#27100](https://github.com/sgl-project/sglang/pull/27100) Add JIT CUDA + CuTeDSL MoE LoRA-A shrink kernels
- [#27449](https://github.com/sgl-project/sglang/pull/27449) Support per token group quant 8bit v2 jit kernel
- [#27350](https://github.com/sgl-project/sglang/pull/27350) Support Waterfill with MegaMoE backend
- [#27720](https://github.com/sgl-project/sglang/pull/27720) Defer moe finalize
- [#27651](https://github.com/sgl-project/sglang/pull/27651) Add contiguous GEMM path for Standard Dispatcher with DeepGEMM
- [#27349](https://github.com/sgl-project/sglang/pull/27349) Support DSV4 shared expert fusion for DeepEP and MegaMOE
- [#27211](https://github.com/sgl-project/sglang/pull/27211) Add FlashInfer CuteDSL fused combine for DeepEP LL MoE
- [#27204](https://github.com/sgl-project/sglang/pull/27204) Implement QuarkW4A8MXFp4MoE to support amd/gpt-oss-120b-w-mxfp4-a-fp8
- [#27588](https://github.com/sgl-project/sglang/pull/27588) Split fused w13 gate/up global scales for NVFP4 MoE
- [#27112](https://github.com/sgl-project/sglang/pull/27112) Add fused moe triton config for Qwen3.5-397B-A17B in triton3.6.0
- [#27274](https://github.com/sgl-project/sglang/pull/27274) Fix MoE virtual-experts gated gate_up
- [#27636](https://github.com/sgl-project/sglang/pull/27636) Fuse sigmoid + mul into single Triton kernel for shared expert gating
- [#27806](https://github.com/sgl-project/sglang/pull/27806) W4A8 MXFP4 MoE backend for DeepSeek-V4 on SM90

</details>

<details>
<summary>Model support (24)</summary>

- [#26347](https://github.com/sgl-project/sglang/pull/26347) Support for Zyphra zaya1 model
- [#27279](https://github.com/sgl-project/sglang/pull/27279) Add Ideogram 4 FP8 generation support
- [#26106](https://github.com/sgl-project/sglang/pull/26106) Support Command A plus
- [#27379](https://github.com/sgl-project/sglang/pull/27379) Support Ideogram4 NVFP4
- [#27167](https://github.com/sgl-project/sglang/pull/27167) Support encoder-free unified Text/Vision/Audio model
- [#24880](https://github.com/sgl-project/sglang/pull/24880) Add DeepSeek V4 support for HiSparse direct Prefill-to-Decode DRAM
- [#25950](https://github.com/sgl-project/sglang/pull/25950) Mistral3 add tensor parallel support for diffusion text encoder
- [#27393](https://github.com/sgl-project/sglang/pull/27393) Add Ideogram4 DiT tensor parallel support
- [#27118](https://github.com/sgl-project/sglang/pull/27118) Mamba extra buffer lazy support
- [#26963](https://github.com/sgl-project/sglang/pull/26963) Add Cosmos3 Nano T2V GPU test
- [#27096](https://github.com/sgl-project/sglang/pull/27096) Cosmos3 fused qknorm rope
- [#27432](https://github.com/sgl-project/sglang/pull/27432) Fix native text-encoder loading for T5/UMT5 encoder-decoder models
- [#27442](https://github.com/sgl-project/sglang/pull/27442) Add OmniDreams autoregressive video world model
- [#27207](https://github.com/sgl-project/sglang/pull/27207) Progressive resolution growing for Wan 2.1 via GPU DCT upsampling
- [#27639](https://github.com/sgl-project/sglang/pull/27639) Support LongLive 2.0 T2V inference
- [#27447](https://github.com/sgl-project/sglang/pull/27447) Add Evo 2 DNA foundation model with CharLevelTokenizer auto-generation
- [#27420](https://github.com/sgl-project/sglang/pull/27420) Add JoyEcho multi-shot A/V generation support
- [#27277](https://github.com/sgl-project/sglang/pull/27277) Deepseek v4: support mixed dtype compression states
- [#27408](https://github.com/sgl-project/sglang/pull/27408) Add Deepseek V3.2's Keep Sampling mask response support
- [#27576](https://github.com/sgl-project/sglang/pull/27576) Cosmos3 omni sound, action conditioning, and video-to-video
- [#27271](https://github.com/sgl-project/sglang/pull/27271) Add Gemma 4 Unified 12B encoder-free multimodal model support
- [#27392](https://github.com/sgl-project/sglang/pull/27392) Add B200 native diffusion qknorm-rope and norm-scale-shift fast paths
- [#27736](https://github.com/sgl-project/sglang/pull/27736) Progressive resolution growing for Ideogram 4 via GPU DCT upsampling
- [#27590](https://github.com/sgl-project/sglang/pull/27590) Use fused FP8 GEMM for Ideogram4 weight-only linears

</details>

<details>
<summary>Parallelism & scheduling (35)</summary>

- [#27506](https://github.com/sgl-project/sglang/pull/27506) Add more testing for chunked prefill
- [#25464](https://github.com/sgl-project/sglang/pull/25464) Deprecate Spec V1
- [#27607](https://github.com/sgl-project/sglang/pull/27607) Support spec v2 for Frozen-KV MTP; remove v1 worker
- [#27413](https://github.com/sgl-project/sglang/pull/27413) Add scripted-runtime unit, core integration, and chunked-prefill tests
- [#27411](https://github.com/sgl-project/sglang/pull/27411) Add scripted-runtime harness core and wire scheduler/IPC hooks
- [#27394](https://github.com/sgl-project/sglang/pull/27394) Add sticky-session routing policy for agentic router
- [#26576](https://github.com/sgl-project/sglang/pull/26576) Encoder DP mode with per-rank subprocess workers
- [#24984](https://github.com/sgl-project/sglang/pull/24984) Support draft offload for mooncake in HiCache
- [#17260](https://github.com/sgl-project/sglang/pull/17260) Support ngram spec v2
- [#24055](https://github.com/sgl-project/sglang/pull/24055) Batchsize-aware support for adaptive speculative_num_steps
- [#26881](https://github.com/sgl-project/sglang/pull/26881) Support l3 storage for swa and deepseek v4 in UnifiedTree
- [#27285](https://github.com/sgl-project/sglang/pull/27285) Fix crash when using PP + HiCache L2
- [#26922](https://github.com/sgl-project/sglang/pull/26922) Drive KV transfers with a sharded synchronous worker pool
- [#27072](https://github.com/sgl-project/sglang/pull/27072) Publish split write-through fragments for hicache
- [#26480](https://github.com/sgl-project/sglang/pull/26480) Add LoadBasedPolicy for agentic router
- [#27264](https://github.com/sgl-project/sglang/pull/27264) Sync sidecar component hits across TP ranks and make SWA prefetch all-or-nothing
- [#26972](https://github.com/sgl-project/sglang/pull/26972) Spec v2 tree drafting with page_size>1
- [#27655](https://github.com/sgl-project/sglang/pull/27655) Fix compatibility bugs with eagle and unified l3
- [#26997](https://github.com/sgl-project/sglang/pull/26997) Reland spec v2 tree drafting with page_size==1
- [#27391](https://github.com/sgl-project/sglang/pull/27391) Fix SWA admission budget under-counts HiCache load-back consumption
- [#26859](https://github.com/sgl-project/sglang/pull/26859) Add _draft_preprocess_idle call for FrozenKVMTPVerifyInput
- [#27458](https://github.com/sgl-project/sglang/pull/27458) Consolidate the per-decode KV alloc reserve into one helper
- [#27300](https://github.com/sgl-project/sglang/pull/27300) Complete CustomSpecAlgo duck-typing interface and guard against drift
- [#27764](https://github.com/sgl-project/sglang/pull/27764) Extract move_accept_tokens_to_target_kvcache into spec_utils
- [#27446](https://github.com/sgl-project/sglang/pull/27446) Fix PP is_fully_idle missing in-flight microbatches
- [#27174](https://github.com/sgl-project/sglang/pull/27174) Add num_waiting_uncached_tokens load metric
- [#26938](https://github.com/sgl-project/sglang/pull/26938) Fix the _chunked_req_scheduled_last_iter flag with a content-based stash gate
- [#27468](https://github.com/sgl-project/sglang/pull/27468) dflash piecewise cuda graphs support
- [#27599](https://github.com/sgl-project/sglang/pull/27599) Naming cleanup: contiguous draft-loc kernel + `accepted`->`accept`
- [#27628](https://github.com/sgl-project/sglang/pull/27628) Hybrid suffix mtp v2
- [#27250](https://github.com/sgl-project/sglang/pull/27250) Add acceleration policy hooks for diffusion
- [#27585](https://github.com/sgl-project/sglang/pull/27585) Suffix decoding v2
- [#27667](https://github.com/sgl-project/sglang/pull/27667) CI sandbox for stateless scheduler b temp run
- [#27498](https://github.com/sgl-project/sglang/pull/27498) P-EAGLE: parallel draft generation for EAGLE-3
- [#27761](https://github.com/sgl-project/sglang/pull/27761) Fold eagle V2 mixins into base spec-input classes
- plus 36 more minor scheduling and parallelism updates

</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#22786](https://github.com/sgl-project/sglang/pull/22786) Add FlyDSL fused normalization kernels for ROCm diffusion models optimization
- [#22300](https://github.com/sgl-project/sglang/pull/22300) Fix FP8 gemm performance with fp16 models on NVIDIA
- [#27202](https://github.com/sgl-project/sglang/pull/27202) Fix MTP accuracy regression on Qwen3 hybrid models for NPU
- [#27127](https://github.com/sgl-project/sglang/pull/27127) Use sgl_kernel_npu rmsrope accelerate llada2
- [#27790](https://github.com/sgl-project/sglang/pull/27790) Add torch implementation for fused_q_norm_rope on Intel GPU
- [#27772](https://github.com/sgl-project/sglang/pull/27772) Adopt NPU backend initialization for device-specific handling
- [#27804](https://github.com/sgl-project/sglang/pull/27804) Fix HIP fallback modulation math on AMD

</details>

<details>
<summary>API & serving (20)</summary>

- [#27073](https://github.com/sgl-project/sglang/pull/27073) Configure experimental sgl-router via CLI flags instead of a config file
- [#27591](https://github.com/sgl-project/sglang/pull/27591) Add request/TTFT/worker metrics + Grafana dashboard to experimental sgl-router
- [#27148](https://github.com/sgl-project/sglang/pull/27148) Improve realtime WebUI playback pacing
- [#22817](https://github.com/sgl-project/sglang/pull/22817) Extract post-training weight APIs into mixins and add tensor update/checker paths
- [#26119](https://github.com/sgl-project/sglang/pull/26119) Disagg server args, launch helpers, and warmup utils for diffusion
- [#25100](https://github.com/sgl-project/sglang/pull/25100) Apertus Tool/Function and Reasoning parser
- [#27612](https://github.com/sgl-project/sglang/pull/27612) Add /flush_cache endpoint to experimental sgl-router
- [#27297](https://github.com/sgl-project/sglang/pull/27297) Optimize LingBot realtime transport and camera conditioning
- [#23755](https://github.com/sgl-project/sglang/pull/23755) Add pd disaggregation mooncake backend tracing
- [#27363](https://github.com/sgl-project/sglang/pull/27363) Add sglang:weight_load_duration_seconds gauge with source label
- [#27068](https://github.com/sgl-project/sglang/pull/27068) Polish realtime WebUI waiting state
- [#27080](https://github.com/sgl-project/sglang/pull/27080) Fix LingBot realtime consistency GT pin
- [#27249](https://github.com/sgl-project/sglang/pull/27249) Fix realtime webui recording timeline
- [#27716](https://github.com/sgl-project/sglang/pull/27716) Feature/beam search rebased
- [#27139](https://github.com/sgl-project/sglang/pull/27139) Fast recovery for sglang engine
- [#27196](https://github.com/sgl-project/sglang/pull/27196) Pickle to msgpack migration
- [#27386](https://github.com/sgl-project/sglang/pull/27386) Apply chat template before cache-aware hashing
- [#27778](https://github.com/sgl-project/sglang/pull/27778) Add repetition truncation logit processor
- [#27311](https://github.com/sgl-project/sglang/pull/27311) Add startup self-benchmarking for ForwardPassMetrics
- [#27146](https://github.com/sgl-project/sglang/pull/27146) Add optimization in realtime video
- plus 15 more minor API and serving updates

</details>

<details>
<summary>Docs (24)</summary>

- [#26885](https://github.com/sgl-project/sglang/pull/26885) Cookbook renovation
- [#26969](https://github.com/sgl-project/sglang/pull/26969) Add Nemotron 3 Ultra cookbook entry
- [#27767](https://github.com/sgl-project/sglang/pull/27767) Update SGLang-Diffusion docs
- [#27308](https://github.com/sgl-project/sglang/pull/27308) Sync legacy docs/-only updates into docs_new
- [#27032](https://github.com/sgl-project/sglang/pull/27032) Add GLM model best practice docs for NPU
- [#27496](https://github.com/sgl-project/sglang/pull/27496) Update SGLang diffusion skills
- [#27248](https://github.com/sgl-project/sglang/pull/27248) Update Cookbook with Xeon support info
- [#27198](https://github.com/sgl-project/sglang/pull/27198) Add SANA-WM diffusion cookbook
- [#27195](https://github.com/sgl-project/sglang/pull/27195) Add ernie Image diffusion docs
- [#27454](https://github.com/sgl-project/sglang/pull/27454) Support mooncake store layer first layout docs
- [#27322](https://github.com/sgl-project/sglang/pull/27322) Sync LMSYS SGLang blog cards
- [#27353](https://github.com/sgl-project/sglang/pull/27353) Update best practice for qwen3-next-80b-a3b-instruct
- [#27517](https://github.com/sgl-project/sglang/pull/27517) Sync LMSYS SGLang blog cards
- [#25198](https://github.com/sgl-project/sglang/pull/25198) Update Nemotron3-Nano-Omni cookbook to reflect new model paths
- [#26731](https://github.com/sgl-project/sglang/pull/26731) Update documentation for software version upgrades on NPU
- [#27171](https://github.com/sgl-project/sglang/pull/27171) Update unified Text/Vision/Audio model cookbook
- [#27049](https://github.com/sgl-project/sglang/pull/27049) Add DeepSeek-V4 EPLB Waterfill tips
- [#27663](https://github.com/sgl-project/sglang/pull/27663) Best Practice Docs Splitting for NPU
- [#27677](https://github.com/sgl-project/sglang/pull/27677) Replace <code> with backticks and remove obsolete params for NPU
- [#27714](https://github.com/sgl-project/sglang/pull/27714) Add Kimi-K2.6 NVFP4 and update Kimi-K2.5 cookbook guidance
- [#27708](https://github.com/sgl-project/sglang/pull/27708) Add GLM-5.1 NVFP4 to cookbook
- [#27302](https://github.com/sgl-project/sglang/pull/27302) Add MiniCPM5 and MiniCPM-SALA cookbooks
- [#27665](https://github.com/sgl-project/sglang/pull/27665) Add mimo best practice
- [#27672](https://github.com/sgl-project/sglang/pull/27672) Add bucketed multi-dir layout for NIXL file storage

</details>

<details>
<summary>Bugfixes (24)</summary>

- [#27205](https://github.com/sgl-project/sglang/pull/27205) Fix customized_info incremental streaming
- [#27145](https://github.com/sgl-project/sglang/pull/27145) Avoid duplicate zmq bind in multi-tokenizer mode
- [#26882](https://github.com/sgl-project/sglang/pull/26882) Set canary_manager and materialize overlap-loop inputs on Apple Silicon
- [#27201](https://github.com/sgl-project/sglang/pull/27201) Force to use gate_mode interleaved to fix tp2/tp4/tp8 acc issue on AMD
- [#26182](https://github.com/sgl-project/sglang/pull/26182) Fix Req array token-id concatenation
- [#27173](https://github.com/sgl-project/sglang/pull/27173) Fix trace_modules gate disabling default trace contexts
- [#26825](https://github.com/sgl-project/sglang/pull/26825) Fix TokenizerManager crash on top_logprobs with tensor values
- [#27187](https://github.com/sgl-project/sglang/pull/27187) Revert "Fix TokenizerManager crash on top_logprobs with tensor values"
- [#22367](https://github.com/sgl-project/sglang/pull/22367) Correct off-by-one in vocab boundary check for token validation
- [#27011](https://github.com/sgl-project/sglang/pull/27011) Clean up failed NIXL sender state
- [#27372](https://github.com/sgl-project/sglang/pull/27372) Fix KV cache corruption on abort by notifying ongoing prefill
- [#23802](https://github.com/sgl-project/sglang/pull/23802) Fix stop-string check misses early matches during speculative decoding
- [#27004](https://github.com/sgl-project/sglang/pull/27004) Correct DSA/SWA state-page transfer mismatch in PD disaggregation
- [#27608](https://github.com/sgl-project/sglang/pull/27608) Fix prefill bootstrap registration failure with --host 0.0.0.0
- [#26864](https://github.com/sgl-project/sglang/pull/26864) Fix multimodal synthetic benchmark prompt generation to exclude special tokens
- [#27220](https://github.com/sgl-project/sglang/pull/27220) Eliminate TTFT regression for hybrid mamba models with radix cache
- [#27315](https://github.com/sgl-project/sglang/pull/27315) Address multiple vulnerabilities including SSRF and RCE
- [#27239](https://github.com/sgl-project/sglang/pull/27239) Raise a clear error for missing local model/draft paths
- [#27199](https://github.com/sgl-project/sglang/pull/27199) Fix require_reasoning and routing_key dropped in GenerateReqInput
- [#27435](https://github.com/sgl-project/sglang/pull/27435) Fix close MiniMax M2 streaming tool-call blocks
- [#27641](https://github.com/sgl-project/sglang/pull/27641) Fix AttributeError when chunked prefill encounters EVSEmbeddingResult
- [#27337](https://github.com/sgl-project/sglang/pull/27337) Fix qwen3 coder parameter end parsing
- [#27650](https://github.com/sgl-project/sglang/pull/27650) Fix PCG capture fail with aiter fused all-reduce+RMSNorm on AMD
- [#27796](https://github.com/sgl-project/sglang/pull/27796) Fix ZMQ stale socket reconnection in PD disaggregation

</details>

<details>
<summary>Refactors (12)</summary>

- [#27698](https://github.com/sgl-project/sglang/pull/27698) Refactor realtime control state and adapters for diffusion
- [#26742](https://github.com/sgl-project/sglang/pull/26742) Unify CUDA graph runner input buffers behind CudaGraphBufferRegistry
- [#27091](https://github.com/sgl-project/sglang/pull/27091) Unify full→SWA index translation in init_forward_metadata
- [#27192](https://github.com/sgl-project/sglang/pull/27192) Retire DecodeInputBuffers / PrefillInputBuffers in favor of CudaGraphBufferRegistry
- [#27552](https://github.com/sgl-project/sglang/pull/27552) Rename token resolver to `_resolve_spec_v2_tokens` and remove dead V1 helpers
- [#27697](https://github.com/sgl-project/sglang/pull/27697) Refactor realtime and model-specific stage modules for diffusion
- [#26637](https://github.com/sgl-project/sglang/pull/26637) Refactor Req.fill_ids into full_untruncated_fill_ids + fill_len
- [#26768](https://github.com/sgl-project/sglang/pull/26768) Refactor simulated acceptance length generation
- [#27542](https://github.com/sgl-project/sglang/pull/27542) Dynamic encoder registration cleanup
- [#27273](https://github.com/sgl-project/sglang/pull/27273) Extract host KV cache base layer into pool_host package
- [#27334](https://github.com/sgl-project/sglang/pull/27334) Centralize storage backend extra config parsing for hicache
- [#27256](https://github.com/sgl-project/sglang/pull/27256) Extract MambaTokenToKVPoolAllocator into allocator/

</details>

<details>
<summary>Tests, CI & build (55)</summary>

- [#22734](https://github.com/sgl-project/sglang/pull/22734) MSCCL++ Integration
- [#24630](https://github.com/sgl-project/sglang/pull/24630) Diffusion CI Ground Truth Generation for NPU
- [#24689](https://github.com/sgl-project/sglang/pull/24689) Add GitHub test summary and deduplicate test code for NPU
- [#26908](https://github.com/sgl-project/sglang/pull/26908) Add unit tests for nixl backend
- [#27001](https://github.com/sgl-project/sglang/pull/27001) Remove hardcoded model/cache paths from MI35x nightly tests
- [#27126](https://github.com/sgl-project/sglang/pull/27126) Add MiniMax-M2.5 TP=4 nightly accuracy test for MI355X
- [#27502](https://github.com/sgl-project/sglang/pull/27502) Add mixed-prefix gsm8k eval and its CPU unit test
- [#25007](https://github.com/sgl-project/sglang/pull/25007) Add Arm64 INT8 MoE test coverage
- [#27710](https://github.com/sgl-project/sglang/pull/27710) Add UT guarding per-request bookkeeping clock ownership
- [#27242](https://github.com/sgl-project/sglang/pull/27242) Fix torchada preflight lock cleanup and add LLM server smoke test
- [#27410](https://github.com/sgl-project/sglang/pull/27410) Add kv_canary PP self-test fixture and SWA divergence coverage
- [#27644](https://github.com/sgl-project/sglang/pull/27644) Move JIT kernel tests + benchmarks to test/registered/jit
- [#27282](https://github.com/sgl-project/sglang/pull/27282) Pull prebuilt nightly image instead of building per-stage for XPU CI
- [#27404](https://github.com/sgl-project/sglang/pull/27404) Remove DeepSeek V4 release Docker workflow
- [#27156](https://github.com/sgl-project/sglang/pull/27156) Expand stage-a and consolidate stage-b tests into stage-a for XPU CI
- [#27427](https://github.com/sgl-project/sglang/pull/27427) Add GB300 base C CI suite
- [#27721](https://github.com/sgl-project/sglang/pull/27721) Add TP server GPU process regression test
- [#27526](https://github.com/sgl-project/sglang/pull/27526) Re-enable stage B with docker-pull flow and split tests for XPU CI
- [#27461](https://github.com/sgl-project/sglang/pull/27461) Enable async-assert invariant probes by default in CI
- [#27387](https://github.com/sgl-project/sglang/pull/27387) Support configurable mirrors for restricted networks in sgl-kernel
- plus 35 more minor CI and test updates

</details>

<details>
<summary>Other (20)</summary>

- [#25455](https://github.com/sgl-project/sglang/pull/25455) MiMo-V2-Flash Adaptation for NPU
- [#22253](https://github.com/sgl-project/sglang/pull/22253) Support dynamic encoder register
- [#27407](https://github.com/sgl-project/sglang/pull/27407) Route the eager forward path through the CUDA graph input-buffer registry
- [#26757](https://github.com/sgl-project/sglang/pull/26757) Trigger scheduler diagnostics on health failure
- [#27726](https://github.com/sgl-project/sglang/pull/27726) Update MegaMoE handling and rerun benchmarks
- [#26850](https://github.com/sgl-project/sglang/pull/26850) Add parallel-rank dump filenames and pipeline-global layer remapping to dumper
- [#24756](https://github.com/sgl-project/sglang/pull/24756) Optimize ngram decode token table update
- [#10950](https://github.com/sgl-project/sglang/pull/10950) Support encoder_decoder on cpu_graph_runner
- [#23751](https://github.com/sgl-project/sglang/pull/23751) TITO Support for sglang-miles
- [#21197](https://github.com/sgl-project/sglang/pull/21197) Adaptation to support deterministic inference on NPU
- [#24659](https://github.com/sgl-project/sglang/pull/24659) Optimize streaming detokenizer updates
- [#27534](https://github.com/sgl-project/sglang/pull/27534) Downgrade propagated rank failure logs from error to debug
- [#26635](https://github.com/sgl-project/sglang/pull/26635) Improve registration in cpu_graph_runner
- [#27660](https://github.com/sgl-project/sglang/pull/27660) Update amd qwen3.5 cookbook
- [#27071](https://github.com/sgl-project/sglang/pull/27071) Type hicache transfer hook kwargs in unified cache
- [#26548](https://github.com/sgl-project/sglang/pull/26548) Extract release_req and retract_all as module-level free functions
- [#27445](https://github.com/sgl-project/sglang/pull/27445) Complete server warmup before scripted runtime scripts start
- [#27659](https://github.com/sgl-project/sglang/pull/27659) Share BCG output buffers across capture sizes
- [#27756](https://github.com/sgl-project/sglang/pull/27756) Cherry-pick to release/v0.5.13: Share BCG output buffers across capture sizes
- [#27758](https://github.com/sgl-project/sglang/pull/27758) Revert "Share BCG output buffers across capture sizes"

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
