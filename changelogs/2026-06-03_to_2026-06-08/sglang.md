# sglang: PR digest (2026-06-03 to 2026-06-08)

_278 merged, 223 newly opened - source sgl-project/sglang, generated 2026-06-10T16:15:03Z_

## TL;DR
- **Model Focus:** DeepSeek V4 dominated model-specific work, with extensive updates for DP attention, HiSparse DRAM offloading, and FlashInfer sparse MLA decode. Gemma 4, GLM-5, and MiniMax also saw notable optimizations.
- **Multimodal & Diffusion:** Massive expansion in diffusion capabilities, including SANA-WM streaming, Ideogram 4 FP8 generation, and progressive resolution growing via GPU DCT upsampling (yielding up to 2X speedups). In-progress work targets OmniDreams and Wan 2.1.
- **Performance & Kernels:** Major kernel additions include an experimental fast LoRA path using the `sgl_trtllm` MoE backend for FP8/NVFP4, and new JIT CUDA + CuTeDSL MoE LoRA-A shrink kernels.
- **Speculative Decoding:** Speculative decoding V1 is officially deprecated as the engine shifts entirely to V2. Ongoing work introduces suffix decoding v2 and P-EAGLE parallel draft generation.
- **Hardware & Architecture:** AMD platforms received significant attention with MXFP4 online quantization, FlyDSL fused normalization for ROCm diffusion, and gpt-oss-120B optimizations. Intel XPU added support for Gemma 4.

## Most important PRs
- **[#27329](https://github.com/sgl-project/sglang/pull/27329)** Introduces an experimental fast LoRA path utilizing the `sgl_trtllm` MoE backend for FP8 and NVFP4 models, significantly improving LoRA serving performance on NVIDIA hardware.
- **[#27524](https://github.com/sgl-project/sglang/pull/27524)** Implements progressive resolution growing for image and video diffusion models using GPU DCT upsampling, delivering up to a 2X speedup during generation.
- **[#25464](https://github.com/sgl-project/sglang/pull/25464)** Officially deprecates Speculative Decoding V1, cleaning up the codebase to focus entirely on the more efficient V2 architecture and its adaptive scheduling features.
- **[#25195](https://github.com/sgl-project/sglang/pull/25195)** Adds support for breakable CUDA graphs in DeepSeek V4 Data Parallel (DP) attention, enabling more flexible and efficient execution for large-scale DeepSeek deployments.
- **[#27100](https://github.com/sgl-project/sglang/pull/27100)** Proposes newly-opened JIT-compiled CUDA and CuTeDSL kernels for MoE LoRA-A shrinking, aiming to further optimize LoRA adapter overhead.

## More changes by area

<details>
<summary>Performance (19)</summary>

- [#27063](https://github.com/sgl-project/sglang/pull/27063) Optimize gpt-oss-120B performance on AMD
- [#26496](https://github.com/sgl-project/sglang/pull/26496) Improve SM120 performance and usability for NVFP4
- [#26733](https://github.com/sgl-project/sglang/pull/26733) Optimize Nemotron performance
- [#24756](https://github.com/sgl-project/sglang/pull/24756) Optimize ngram decode token table update
- [#26861](https://github.com/sgl-project/sglang/pull/26861) Reduce transient allocations in NVFP4 MoE setup
- [#27364](https://github.com/sgl-project/sglang/pull/27364) Reduce radix cache match overhead by changing the match algorithm
- [#27320](https://github.com/sgl-project/sglang/pull/27320) Parallelize create_flashmla_kv_indices over page-blocks
- [#24659](https://github.com/sgl-project/sglang/pull/24659) Optimize streaming detokenizer updates
- [#26874](https://github.com/sgl-project/sglang/pull/26874) Speed up dump comparator percentile computation using numpy
- [#25000](https://github.com/sgl-project/sglang/pull/25000) Reduce mamba prefill allocation overhead
- [#27383](https://github.com/sgl-project/sglang/pull/27383) Optimize LingBot realtime SP cache path
- [#27382](https://github.com/sgl-project/sglang/pull/27382) Split-KV flash-decode attention for EAGLE target-verify on AMD
- [#27146](https://github.com/sgl-project/sglang/pull/27146) Add optimization in realtime video for diffusion
- [#27105](https://github.com/sgl-project/sglang/pull/27105) Offload the sync HF processor off the TokenizerManager event loop
- [#27181](https://github.com/sgl-project/sglang/pull/27181) Implement LoRA Async Pipelining Per Request Load
- [#27183](https://github.com/sgl-project/sglang/pull/27183) Add YOCO fast-prefill for Gemma4 E2B/E4B
- [#27609](https://github.com/sgl-project/sglang/pull/27609) Disable MiniMax-M2.7 custom all-reduce on gfx942
- [#27254](https://github.com/sgl-project/sglang/pull/27254) Optimize tokenizer manager detokenizer receive loop
- [#27464](https://github.com/sgl-project/sglang/pull/27464) Reduce SSE overhead for large batch sizes in bench_one_batch_server

</details>

<details>
<summary>Kernels & attention (31)</summary>

- [#22786](https://github.com/sgl-project/sglang/pull/22786) Add FlyDSL fused normalization kernels for ROCm diffusion models
- [#27091](https://github.com/sgl-project/sglang/pull/27091) Unify full-to-SWA index translation in init_forward_metadata
- [#25418](https://github.com/sgl-project/sglang/pull/25418) Integrate flash_mla_sparse_fwd
- [#27193](https://github.com/sgl-project/sglang/pull/27193) Replace skip_attn_backend_init with a batch-carried attention plan marker
- [#27407](https://github.com/sgl-project/sglang/pull/27407) Route the eager forward path through the CUDA graph input-buffer registry
- [#27233](https://github.com/sgl-project/sglang/pull/27233) Fuse small kernels under `gather_spec_extras`
- [#27096](https://github.com/sgl-project/sglang/pull/27096) Add Cosmos3 fused qknorm rope
- [#27166](https://github.com/sgl-project/sglang/pull/27166) Support NextN = 2/4 in DSV32
- [#24870](https://github.com/sgl-project/sglang/pull/24870) Support NextN = 2/4 in DSV32
- [#27138](https://github.com/sgl-project/sglang/pull/27138) Revert "Support NextN = 2/4 in DSV32"
- [#26894](https://github.com/sgl-project/sglang/pull/26894) Fuse compress norm+rope+hadamard into single Triton kernel on AMD
- [#26914](https://github.com/sgl-project/sglang/pull/26914) Remove BF16-to-FP32 elementwise cast from compressor GEMM on HIP
- [#25773](https://github.com/sgl-project/sglang/pull/25773) Add fused_rope for Intel XPU
- [#27289](https://github.com/sgl-project/sglang/pull/27289) Remove redundant fp8 scale transpose-copy on decode for DSV4 on ROCm
- [#21332](https://github.com/sgl-project/sglang/pull/21332) Apply trtllm MHA kernel for GLM-5 on Blackwell
- [#27397](https://github.com/sgl-project/sglang/pull/27397) Support JIT fused A GEMM (MLA down projection) and GLM-5 hidden size on SM120
- [#27392](https://github.com/sgl-project/sglang/pull/27392) Add B200 native diffusion qknorm-rope and norm-scale-shift fast paths
- [#27436](https://github.com/sgl-project/sglang/pull/27436) Enable breakable CUDA graph (BCG) for diffusion DiTs
- [#27421](https://github.com/sgl-project/sglang/pull/27421) Add per-position token_ids_logprob for sparse OPD top-k scoring
- [#27178](https://github.com/sgl-project/sglang/pull/27178) Add opt-in PDL support to LoRA kernels
- [#27455](https://github.com/sgl-project/sglang/pull/27455) Add FlashInfer sparse MLA decode for DSv4-Flash
- [#27276](https://github.com/sgl-project/sglang/pull/27276) Correct FlashMLA sparse prefill under DSA context parallel
- [#27263](https://github.com/sgl-project/sglang/pull/27263) Fuse Wan VAE causal conv padding
- [#27513](https://github.com/sgl-project/sglang/pull/27513) Add torchembed as optional RoPE backend
- [#27389](https://github.com/sgl-project/sglang/pull/27389) Use fused flash attention for vision encoder on XPU
- [#27127](https://github.com/sgl-project/sglang/pull/27127) Use sgl_kernel_npu rmsrope to accelerate llada2
- [#27301](https://github.com/sgl-project/sglang/pull/27301) Support FA3 attn full overlap for Spec v2
- [#27177](https://github.com/sgl-project/sglang/pull/27177) Support trtllm mha attn full overlap for Spec v2
- [#27307](https://github.com/sgl-project/sglang/pull/27307) Convert DeepSeek V4 APE layout through weight loader
- [#27566](https://github.com/sgl-project/sglang/pull/27566) Optimize hc_head() for DeepSeekV4ModelNextN
- [#27441](https://github.com/sgl-project/sglang/pull/27441) Revise GEMMARMS normalization support for NPU

</details>

<details>
<summary>MoE & quantization (19)</summary>

- [#25655](https://github.com/sgl-project/sglang/pull/25655) Add w4a16 MoE support to Nemotron
- [#18005](https://github.com/sgl-project/sglang/pull/18005) Implement online MXFP4 quantization for dense and MOE models on AMD
- [#27150](https://github.com/sgl-project/sglang/pull/27150) Support Waterfill with dynamic EPLB
- [#26746](https://github.com/sgl-project/sglang/pull/26746) Support optional kwargs in AITER fused_moe runner
- [#26349](https://github.com/sgl-project/sglang/pull/26349) Support specific pass of bias_grouped_topk for XPU
- [#25347](https://github.com/sgl-project/sglang/pull/25347) Enable OOT platforms to provide custom quant configs
- [#25239](https://github.com/sgl-project/sglang/pull/25239) Support FlashInfer 4over6 NVFP4
- [#27401](https://github.com/sgl-project/sglang/pull/27401) Enable flashinfer_trtllm NVFP4 fused-MoE via SigmoidRenorm routing
- [#27204](https://github.com/sgl-project/sglang/pull/27204) Implement QuarkW4A8MXFp4MoE to support amd/gpt-oss-120b-w-mxfp4-a-fp8
- [#27449](https://github.com/sgl-project/sglang/pull/27449) Support per token group quant 8bit v2 jit kernel
- [#27350](https://github.com/sgl-project/sglang/pull/27350) Support Waterfill with MegaMoE backend
- [#27211](https://github.com/sgl-project/sglang/pull/27211) Add FlashInfer CuteDSL fused combine for DeepEP LL MoE
- [#27349](https://github.com/sgl-project/sglang/pull/27349) Support DSV4 shared expert fusion for DeepEP and MegaMOE
- [#27588](https://github.com/sgl-project/sglang/pull/27588) Split fused w13 gate/up global scales for NVFP4 MoE
- [#27112](https://github.com/sgl-project/sglang/pull/27112) Add fused MoE triton config for Qwen3.5-397B-A17B in triton3.6.0
- [#27590](https://github.com/sgl-project/sglang/pull/27590) Use fused FP8 GEMM for Ideogram4 weight-only linears
- [#27594](https://github.com/sgl-project/sglang/pull/27594) Add M-aware fp8 block-scale GEMM dispatch in dpsk-v4
- [#27107](https://github.com/sgl-project/sglang/pull/27107) Add environ to opt-in `CU_MEM_HANDLE_TYPE_FABRIC` for DeepEP
- [#27561](https://github.com/sgl-project/sglang/pull/27561) Support DeepSeek-V4 shared_expert and ep normal using fused swiglu and quant

</details>

<details>
<summary>Model support (22)</summary>

- [#27531](https://github.com/sgl-project/sglang/pull/27531) Add SANA-WM with streaming support
- [#27279](https://github.com/sgl-project/sglang/pull/27279) Add Ideogram 4 FP8 generation support
- [#26106](https://github.com/sgl-project/sglang/pull/26106) Support Command A plus
- [#27379](https://github.com/sgl-project/sglang/pull/27379) Support Ideogram4 NVFP4
- [#27167](https://github.com/sgl-project/sglang/pull/27167) Support encoder-free unified Text/Vision/Audio model
- [#27443](https://github.com/sgl-project/sglang/pull/27443) Precompute Ideogram4 denoising metadata
- [#27151](https://github.com/sgl-project/sglang/pull/27151) Skip unused WanVAE halo send copies
- [#27442](https://github.com/sgl-project/sglang/pull/27442) Add OmniDreams autoregressive video world model
- [#27250](https://github.com/sgl-project/sglang/pull/27250) Add acceleration policy hooks for diffusion
- [#27207](https://github.com/sgl-project/sglang/pull/27207) Implement progressive resolution growing for Wan 2.1 via GPU DCT upsampling
- [#27168](https://github.com/sgl-project/sglang/pull/27168) Update diffusion features post release
- [#27447](https://github.com/sgl-project/sglang/pull/27447) Add Evo 2 (StripedHyena 2) DNA foundation model
- [#27420](https://github.com/sgl-project/sglang/pull/27420) Add JoyEcho multi-shot A/V generation support
- [#27277](https://github.com/sgl-project/sglang/pull/27277) Support mixed dtype compression states for Deepseek v4
- [#27408](https://github.com/sgl-project/sglang/pull/27408) Add Deepseek V3.2's Keep Sampling mask response support
- [#27576](https://github.com/sgl-project/sglang/pull/27576) Add Cosmos3 omni (sound, action conditioning, video-to-video)
- [#27271](https://github.com/sgl-project/sglang/pull/27271) Add Gemma 4 Unified (12B) encoder-free multimodal model support
- [#27110](https://github.com/sgl-project/sglang/pull/27110) Add Nemotron support on sglang-miles
- [#27375](https://github.com/sgl-project/sglang/pull/27375) Add support for JetBrains' Mellum v2 code generation model
- [#27381](https://github.com/sgl-project/sglang/pull/27381) Support native loading for PEFT 0.18+ batched-MoE adapters
- [#27223](https://github.com/sgl-project/sglang/pull/27223) Support Wan multi-output prompt conditioning
- [#27115](https://github.com/sgl-project/sglang/pull/27115) Make Nano-Nemotron VL video sampling configurable

</details>

<details>
<summary>Parallelism & scheduling (55)</summary>

- [#27411](https://github.com/sgl-project/sglang/pull/27411) Add scripted-runtime harness core and wire scheduler/IPC hooks
- [#26576](https://github.com/sgl-project/sglang/pull/26576) Implement encoder DP mode with per-rank subprocess workers
- [#26119](https://github.com/sgl-project/sglang/pull/26119) Disaggregate server args, launch helpers, and warmup utils
- [#24984](https://github.com/sgl-project/sglang/pull/24984) Support draft offload for mooncake
- [#24055](https://github.com/sgl-project/sglang/pull/24055) Add batchsize-aware support for adaptive speculative_num_steps
- [#24880](https://github.com/sgl-project/sglang/pull/24880) Add DeepSeek V4 support for HiSparse direct Prefill-to-Decode DRAM
- [#27393](https://github.com/sgl-project/sglang/pull/27393) Add Ideogram4 DiT tensor parallel support
- [#26881](https://github.com/sgl-project/sglang/pull/26881) Support l3 storage for swa and deepseek v4
- [#27118](https://github.com/sgl-project/sglang/pull/27118) Add Mamba extra buffer lazy support
- [#22253](https://github.com/sgl-project/sglang/pull/22253) Support dynamic encoder register
- [#26757](https://github.com/sgl-project/sglang/pull/26757) Trigger scheduler diagnostics on health failure
- [#26922](https://github.com/sgl-project/sglang/pull/26922) Drive KV transfers with a sharded synchronous worker pool
- [#27072](https://github.com/sgl-project/sglang/pull/27072) Publish split write-through fragments for hicache
- [#26850](https://github.com/sgl-project/sglang/pull/26850) Add parallel-rank dump filenames and pipeline-global layer remapping to dumper
- [#23755](https://github.com/sgl-project/sglang/pull/23755) Add pd disaggregation mooncake backend tracing
- [#27264](https://github.com/sgl-project/sglang/pull/27264) Sync sidecar component hits across TP ranks and make SWA prefetch all-or-nothing
- [#26972](https://github.com/sgl-project/sglang/pull/26972) Support Spec v2 tree drafting (topk>1) with page_size>1
- [#26997](https://github.com/sgl-project/sglang/pull/26997) Reland spec v2 tree drafting (eagle topk>1) with page_size==1
- [#26859](https://github.com/sgl-project/sglang/pull/26859) Add _draft_preprocess_idle call to FrozenKVMTPVerifyInput
- [#27458](https://github.com/sgl-project/sglang/pull/27458) Consolidate the per-decode KV alloc reserve into one helper
- [#27475](https://github.com/sgl-project/sglang/pull/27475) Dedup draft `kv_indices` sizing into `spec_utils` helpers
- [#25395](https://github.com/sgl-project/sglang/pull/25395) Add CP sync to UnifiedTree
- [#27412](https://github.com/sgl-project/sglang/pull/27412) Add scripted-runtime KV-pool and lock-ref exhauster primitives
- [#27463](https://github.com/sgl-project/sglang/pull/27463) Support `topk > 1` tree drafting for mamba/hybrid-linear models on spec v2
- [#27454](https://github.com/sgl-project/sglang/pull/27454) Support mooncake store layer first layout
- [#27071](https://github.com/sgl-project/sglang/pull/27071) Type hicache transfer hook kwargs in unified cache
- [#25002](https://github.com/sgl-project/sglang/pull/25002) Enable trtllm_mha draft-extend CUDA graph with v2 semantics
- [#27445](https://github.com/sgl-project/sglang/pull/27445) Complete server warmup before scripted runtime scripts start
- [#27228](https://github.com/sgl-project/sglang/pull/27228) Enable runtime busy memory check for speculation topk>1
- [#26937](https://github.com/sgl-project/sglang/pull/26937) Add per-rank staggered weight loading for improved TP I/O concurrency
- [#27486](https://github.com/sgl-project/sglang/pull/27486) Add defensive guards for EAGLE draft KV indexing
- [#27238](https://github.com/sgl-project/sglang/pull/27238) Add quiet mode for busy mem check
- [#27085](https://github.com/sgl-project/sglang/pull/27085) Deduplicate PD logprob normalization
- [#27143](https://github.com/sgl-project/sglang/pull/27143) Batch USP replicated KV prefix all-to-all
- [#27492](https://github.com/sgl-project/sglang/pull/27492) Add all_to_all_single to GroupCoordinator
- [#27293](https://github.com/sgl-project/sglang/pull/27293) Don't cache C128 State pool in L3
- [#27512](https://github.com/sgl-project/sglang/pull/27512) Clamp multimodal pad sentinels in spec-v2 draft prefill embedding
- [#27265](https://github.com/sgl-project/sglang/pull/27265) Add TensorCast storage as a new HiCache backend
- [#27262](https://github.com/sgl-project/sglang/pull/27262) Add V2 Transport Modules of SGLang Diffusion Disaggregation
- [#27585](https://github.com/sgl-project/sglang/pull/27585) Implement Suffix decoding v2
- [#27498](https://github.com/sgl-project/sglang/pull/27498) Add P-EAGLE: parallel draft generation for EAGLE-3
- [#27509](https://github.com/sgl-project/sglang/pull/27509) Support DDTree speculative decode
- [#27113](https://github.com/sgl-project/sglang/pull/27113) Add dp_rank sharding for MultiDetokenizerRouter
- [#27582](https://github.com/sgl-project/sglang/pull/27582) Implement Suffix speculative decoding
- [#27378](https://github.com/sgl-project/sglang/pull/27378) Support HiCache for MiMo-V2 models
- [#27551](https://github.com/sgl-project/sglang/pull/27551) Make FDFO a framework capability for all dLLM algorithms
- [#27313](https://github.com/sgl-project/sglang/pull/27313) Add context parallel strategy abstractions
- [#27563](https://github.com/sgl-project/sglang/pull/27563) Support NIXL DRAM KV destinations for HiSparse
- [#27593](https://github.com/sgl-project/sglang/pull/27593) Let custom allreduce support VMM based allocation
- [#27312](https://github.com/sgl-project/sglang/pull/27312) Simplify prefill context parallel server args
- [#27557](https://github.com/sgl-project/sglang/pull/27557) Add L3 SWA periodic checkpoint
- [#27260](https://github.com/sgl-project/sglang/pull/27260) Align dispatch logic for mooncake backend
- [#27370](https://github.com/sgl-project/sglang/pull/27370) Support CPU memory share across TPs for Hisparse
- [#27469](https://github.com/sgl-project/sglang/pull/27469) Add sliding window attention draft layer support for dflash
- [#27165](https://github.com/sgl-project/sglang/pull/27165) Support greedy grammar-constrained decoding for DFlash verification
- plus 10 more minor scheduling updates

</details>

<details>
<summary>Hardware & arch (9)</summary>

- [#23280](https://github.com/sgl-project/sglang/pull/23280) Enable Gemma 4 E2B / E4B / 31B/ 26B-A4B on Intel XPU
- [#22299](https://github.com/sgl-project/sglang/pull/22299) Enable Piecewise CUDA Graph for AMD GPUs
- [#10950](https://github.com/sgl-project/sglang/pull/10950) Support encoder_decoder on cpu_graph_runner
- [#26356](https://github.com/sgl-project/sglang/pull/26356) Support torch_npu profiler patch API drift
- [#26145](https://github.com/sgl-project/sglang/pull/26145) Explicitly enable AVX512 & AMX instruction set on CPU
- [#25885](https://github.com/sgl-project/sglang/pull/25885) Support alt stream for Qwen3.5 on AMD platform
- [#27136](https://github.com/sgl-project/sglang/pull/27136) Add XPU jit kernel support
- [#27099](https://github.com/sgl-project/sglang/pull/27099) Add support for DeepSeekV4 on cpu_graph_runner
- [#27584](https://github.com/sgl-project/sglang/pull/27584) Update CUDA memory allocation methods for compatibility

</details>

<details>
<summary>API & serving (29)</summary>

- [#27073](https://github.com/sgl-project/sglang/pull/27073) Configure experimental sgl-router via CLI flags instead of a config file
- [#27148](https://github.com/sgl-project/sglang/pull/27148) Improve realtime WebUI playback pacing
- [#27394](https://github.com/sgl-project/sglang/pull/27394) Add sticky-session routing policy to agentic router
- [#27297](https://github.com/sgl-project/sglang/pull/27297) Optimize LingBot realtime transport and camera conditioning
- [#25100](https://github.com/sgl-project/sglang/pull/25100) Add Apertus Tool/Function and Reasoning parser
- [#26480](https://github.com/sgl-project/sglang/pull/26480) Add LoadBasedPolicy to agentic router
- [#23751](https://github.com/sgl-project/sglang/pull/23751) Add TITO Support
- [#27363](https://github.com/sgl-project/sglang/pull/27363) Add sglang:weight_load_duration_seconds gauge
- [#27068](https://github.com/sgl-project/sglang/pull/27068) Polish realtime WebUI waiting state
- [#27180](https://github.com/sgl-project/sglang/pull/27180) Add ZMQ IPv6 support and bench_serving sampling params
- [#27174](https://github.com/sgl-project/sglang/pull/27174) Add num_waiting_uncached_tokens load metric
- [#25337](https://github.com/sgl-project/sglang/pull/25337) Fix default device detection for OOT platform plugins
- [#27451](https://github.com/sgl-project/sglang/pull/27451) Classify malformed-multimodal rejects as invalid_request
- [#27139](https://github.com/sgl-project/sglang/pull/27139) Implement fast recovery for sglang engine
- [#27311](https://github.com/sgl-project/sglang/pull/27311) Add startup self-benchmarking for ForwardPassMetrics
- [#27564](https://github.com/sgl-project/sglang/pull/27564) Add Prometheus metrics for the EPD encoder server
- [#27448](https://github.com/sgl-project/sglang/pull/27448) Support audio input in bench_serving
- [#27268](https://github.com/sgl-project/sglang/pull/27268) Add load_lora_adapter_from_distributed api
- [#27122](https://github.com/sgl-project/sglang/pull/27122) Report multimodal token counts in usage.prompt_tokens_details
- [#27606](https://github.com/sgl-project/sglang/pull/27606) Add `--tokenizer-only` flag for cpu only tokens-in/tokens-out
- [#27270](https://github.com/sgl-project/sglang/pull/27270) Accept standard tools in the Responses API
- [#27532](https://github.com/sgl-project/sglang/pull/27532) Add output of error reasons for router exceptions
- [#27395](https://github.com/sgl-project/sglang/pull/27395) Add ForcedSequenceLogitProcessor
- [#27134](https://github.com/sgl-project/sglang/pull/27134) Expose FIFO/MRU/FILO radix eviction policies via CLI
- [#27565](https://github.com/sgl-project/sglang/pull/27565) Emit cached_tokens even when zero
- [#27399](https://github.com/sgl-project/sglang/pull/27399) Respect explicit --max-running-requests instead of clamping to heuristic
- [#27515](https://github.com/sgl-project/sglang/pull/27515) Allow OOT platform plugins to provide custom torch distributed backend
- [#27434](https://github.com/sgl-project/sglang/pull/27434) Add SGLANG_DISABLE_SHM_MM env to force CPU multimodal IPC transport
- [#27298](https://github.com/sgl-project/sglang/pull/27298) Avoid encode/decode round-trip and id-space splice in jinja path

</details>

<details>
<summary>Refactors (19)</summary>

- [#26742](https://github.com/sgl-project/sglang/pull/26742) Unify CUDA graph runner input buffers behind CudaGraphBufferRegistry
- [#26676](https://github.com/sgl-project/sglang/pull/26676) Move SWATokenToKVPoolAllocator to allocator/swa.py
- [#26786](https://github.com/sgl-project/sglang/pull/26786) Refactor CPU quantization schemes
- [#27192](https://github.com/sgl-project/sglang/pull/27192) Retire DecodeInputBuffers / PrefillInputBuffers in favor of CudaGraphBufferRegistry
- [#27552](https://github.com/sgl-project/sglang/pull/27552) Rename token resolver to `_resolve_spec_v2_tokens`
- [#27256](https://github.com/sgl-project/sglang/pull/27256) Extract MambaTokenToKVPoolAllocator into allocator/
- [#26637](https://github.com/sgl-project/sglang/pull/26637) Refactor Req.fill_ids into full_untruncated_fill_ids + fill_len
- [#27599](https://github.com/sgl-project/sglang/pull/27599) Cleanup naming: contiguous draft-loc kernel + `accepted`->`accept`
- [#27542](https://github.com/sgl-project/sglang/pull/27542) Cleanup dynamic encoder registration
- [#26768](https://github.com/sgl-project/sglang/pull/26768) Refactor simulated acceptance length generation
- [#26548](https://github.com/sgl-project/sglang/pull/26548) Extract release_req and retract_all as module-level free functions
- [#27196](https://github.com/sgl-project/sglang/pull/27196) Migrate from pickle to msgpack
- [#27429](https://github.com/sgl-project/sglang/pull/27429) Centralize more inline Triton kernels
- [#27273](https://github.com/sgl-project/sglang/pull/27273) Extract host KV cache base layer into pool_host package
- [#27334](https://github.com/sgl-project/sglang/pull/27334) Centralize storage backend extra config parsing
- [#27610](https://github.com/sgl-project/sglang/pull/27610) Avoid scattered assignment of extend_input_len and extend_fill_len
- [#27575](https://github.com/sgl-project/sglang/pull/27575) Avoid over-general name of Req.fill_len
- [#27611](https://github.com/sgl-project/sglang/pull/27611) Inline extend_range accessors
- [#27570](https://github.com/sgl-project/sglang/pull/27570) Avoid redundant state by removing the full_untruncated_fill_ids field

</details>

<details>
<summary>Bugfixes (80)</summary>

- [#27361](https://github.com/sgl-project/sglang/pull/27361) Fix dual-chunk sparse fallback index overflow
- [#27188](https://github.com/sgl-project/sglang/pull/27188) Fix TP2 DeepSeek-R1 nhead=64 MLA decode crash
- [#27285](https://github.com/sgl-project/sglang/pull/27285) Fix crash when using PP + HiCache L2
- [#27316](https://github.com/sgl-project/sglang/pull/27316) Delegate init_mha_chunk_metadata in HybridLinearAttnBackend
- [#27205](https://github.com/sgl-project/sglang/pull/27205) Fix customized_info incremental streaming
- [#27145](https://github.com/sgl-project/sglang/pull/27145) Avoid duplicate zmq bind in multi-tokenizer mode
- [#27391](https://github.com/sgl-project/sglang/pull/27391) Fix SWA admission budget under-counts HiCache load-back consumption
- [#27300](https://github.com/sgl-project/sglang/pull/27300) Complete CustomSpecAlgo duck-typing interface
- [#26882](https://github.com/sgl-project/sglang/pull/26882) Set canary_manager and materialize overlap-loop inputs on Apple Silicon
- [#27201](https://github.com/sgl-project/sglang/pull/27201) Force to use gate_mode interleaved to fix tp2/tp4/tp8 acc issue
- [#27432](https://github.com/sgl-project/sglang/pull/27432) Fix native text-encoder loading for T5/UMT5 encoder-decoder models
- [#27315](https://github.com/sgl-project/sglang/pull/27315) Address multiple vulnerabilities (SSRF, RCE, path traversal, auth bypass)
- [#27460](https://github.com/sgl-project/sglang/pull/27460) Fix MLA EAGLE draft CUDA-graph `kv_indices` under-allocation
- [#27360](https://github.com/sgl-project/sglang/pull/27360) Fix fa3 EAGLE draft-decode expand page_table scatter OOB
- [#27438](https://github.com/sgl-project/sglang/pull/27438) Fix DSV4 FP8 E4M3 dtype selection on ROCm gfx94x
- plus 65 more minor bugfixes

</details>

<details>
<summary>Tests & CI (53)</summary>

- [#27433](https://github.com/sgl-project/sglang/pull/27433) Add nightly test npu dashboard
- [#27413](https://github.com/sgl-project/sglang/pull/27413) Add scripted-runtime unit, core integration, and chunked-prefill tests
- [#24630](https://github.com/sgl-project/sglang/pull/24630) Add NPU Diffusion CI Ground Truth Generation
- [#24689](https://github.com/sgl-project/sglang/pull/24689) Add NPU GitHub test summary and deduplicate test code
- [#27427](https://github.com/sgl-project/sglang/pull/27427) Add GB300 base C CI suite
- [#27182](https://github.com/sgl-project/sglang/pull/27182) Add nightly Intel XPU Docker release workflow
- [#27461](https://github.com/sgl-project/sglang/pull/27461) Enable async-assert invariant probes by default in CI
- [#27156](https://github.com/sgl-project/sglang/pull/27156) Expand XPU CI stage-a and consolidate stage-b tests
- [#27001](https://github.com/sgl-project/sglang/pull/27001) Remove hardcoded model/cache paths from MI35x nightly tests
- [#27126](https://github.com/sgl-project/sglang/pull/27126) Add MiniMax-M2.5 TP=4 nightly accuracy test for MI355X
- plus 43 more minor test and CI updates

</details>

<details>
<summary>Docs (22)</summary>

- [#26885](https://github.com/sgl-project/sglang/pull/26885) Cookbook renovation
- [#26969](https://github.com/sgl-project/sglang/pull/26969) Add Nemotron 3 Ultra cookbook entry
- [#27308](https://github.com/sgl-project/sglang/pull/27308) Sync legacy docs/-only updates into docs_new (Mintlify)
- [#27032](https://github.com/sgl-project/sglang/pull/27032) Add GLM model best practice docs
- [#27496](https://github.com/sgl-project/sglang/pull/27496) Update SGLang diffusion skills
- [#27248](https://github.com/sgl-project/sglang/pull/27248) Update Cookbook with Xeon support info
- [#27195](https://github.com/sgl-project/sglang/pull/27195) Add ernie Image diffusion docs
- [#27322](https://github.com/sgl-project/sglang/pull/27322) Sync LMSYS SGLang blog cards
- [#27353](https://github.com/sgl-project/sglang/pull/27353) Update best practice for qwen3-next-80b-a3b-instruct
- [#27517](https://github.com/sgl-project/sglang/pull/27517) Sync LMSYS SGLang blog cards
- plus 12 more minor documentation updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
