# sglang: PR digest (2026-07-22 to 2026-07-26)

_202 merged, 279 newly opened - source sgl-project/sglang, generated 2026-07-26T22:19:06Z_

## TL;DR
- **Models & Performance:** DeepSeek (V4) and MiniMax dominated model-specific work. DeepSeek V4 saw major in-progress work for Shared KV Cache in prefill CP, strict bit-exact SWA HiCache, and Q8KV8 sparse MLA prefill. MiniMax-M3 received AITER MoE and sparse prefill tuning.
- **Architecture & Refactoring:** A massive, multi-phase refactoring of the kernel subsystem was merged, migrating tangled JIT subsystems and operator groups into a unified `sglang.kernels` namespace and retiring `sglang.jit_kernel`.
- **Rust Rewrite:** Significant in-progress work points to a new Rust-based server architecture, with newly opened PRs building out the control plane, runtime, tokenizer manager, and multimodal processing pipelines.
- **Scheduling & Parallelism:** Merged major structural changes to scheduling, including spinning off `TreeCore` from the Radix Cache and adding fast engine recovery through weight caching. Disaggregated serving (DSpark PD) is seeing heavy active development for streaming hidden-state transfers.
- **Hardware:** Expanded hardware support merged for AMD (GFX1250 ROCm bringup), Intel XPU platform integration, and extensive NPU quantization and attention fixes.

## Most important PRs
- **[#32045](https://github.com/sgl-project/sglang/pull/32045)** Completes a massive architectural migration of tangled JIT subsystems and operator groups into a unified `sglang.kernels` namespace, standardizing the kernel execution path across backends.
- **[#29901](https://github.com/sgl-project/sglang/pull/29901)** Refactors the Radix Cache by spinning off `TreeCore`, decoupling the tree topology management from the cache allocator to improve maintainability and scheduling flexibility.
- **[#27139](https://github.com/sgl-project/sglang/pull/27139)** Introduces fast engine recovery via a weight cache, drastically reducing model loading times and improving availability during node restarts or crashes.
- **[#21637](https://github.com/sgl-project/sglang/pull/21637)** Adds distributed checkpointing (DCP) All-to-All and FlashInfer-MNNVL communication backends, significantly optimizing tensor-parallel and pipeline-parallel communication overhead.
- **[#32129](https://github.com/sgl-project/sglang/pull/32129)** Proposes OSCAR mixed-precision INT2 KV cache support (`--kv-cache-dtype int2`), which will drastically reduce memory footprint and increase batch size capacity for long-context workloads.

## More changes by area

<details>
<summary>Performance (15)</summary>

- [#31986](https://github.com/sgl-project/sglang/pull/31986) Stack dspark dense draft per-layer ctx KV projection into one GEMM
- [#31552](https://github.com/sgl-project/sglang/pull/31552) Speed up Marlin MoE with occupancy-aware launch specialization
- [#32109](https://github.com/sgl-project/sglang/pull/32109) Skip blocks past per-request live length in full-width Triton kernels
- [#32296](https://github.com/sgl-project/sglang/pull/32296) Halve the non-finite sanitization overhead in per_token_group_quant
- [#31985](https://github.com/sgl-project/sglang/pull/31985) Fold dspark dense draft embedding into the draft graph via forward_embed
- [#32319](https://github.com/sgl-project/sglang/pull/32319) Remove redundant draft metadata copies for DeepSeek V4
- [#32090](https://github.com/sgl-project/sglang/pull/32090) Fuse offline C128 speculative-draft state cleanup into a single kernel launch
- [#32223](https://github.com/sgl-project/sglang/pull/32223) Assemble flat prompt top logprobs scheduler-side as numpy arrays
- [#32010](https://github.com/sgl-project/sglang/pull/32010) Support ragged verify graphs in the DSA attention backend
- [#32272](https://github.com/sgl-project/sglang/pull/32272) Use non-interleaved paged KV input for trtllm sm90/120 prefill
- [#32219](https://github.com/sgl-project/sglang/pull/32219) Cut spec-v2 host-seam overhead in hybrid-linear MTP decode
- [#32194](https://github.com/sgl-project/sglang/pull/32194) Skip unused draft metadata for DeepSeek V4
- [#32068](https://github.com/sgl-project/sglang/pull/32068) Skip FlashInfer draft verify mask allocation
- [#32383](https://github.com/sgl-project/sglang/pull/32383) Optimize EmbeddingGemma prefill performance
- [#32323](https://github.com/sgl-project/sglang/pull/32323) Fill Qwen3.5 speed benchmarks (B200 + B300)

</details>

<details>
<summary>Kernels & attention (62)</summary>

- [#31666](https://github.com/sgl-project/sglang/pull/31666) Move JIT infra + operator groups into sglang.kernels (Phase 3+4)
- [#32072](https://github.com/sgl-project/sglang/pull/32072) Retire sglang.jit_kernel into sglang.kernels
- [#32148](https://github.com/sgl-project/sglang/pull/32148) Unify _jit_ naming, drop empty/model groups, add elementwise
- [#32015](https://github.com/sgl-project/sglang/pull/32015) Migrate JIT operator groups into kernels.ops (no shims)
- [#32160](https://github.com/sgl-project/sglang/pull/32160) Sweep missed dedicated kernels into kernels.ops
- [#30924](https://github.com/sgl-project/sglang/pull/30924) Unify the quant kernel family (flat + masked)
- [#30280](https://github.com/sgl-project/sglang/pull/30280) Delete sgl-kernel AOT router GEMM and fused A GEMM
- [#32294](https://github.com/sgl-project/sglang/pull/32294) Add NPU attention unit tests for ascend_backend
- [#31897](https://github.com/sgl-project/sglang/pull/31897) Refactor rope kernels on CPU
- [#30540](https://github.com/sgl-project/sglang/pull/30540) Add HPC-Ops attention backend
- [#26888](https://github.com/sgl-project/sglang/pull/26888) Add target_verify support for speculative decoding
- [#31834](https://github.com/sgl-project/sglang/pull/31834) Support a same-size mixed q dtype in the fused RoPE kernels
- [#31904](https://github.com/sgl-project/sglang/pull/31904) Fix mixed exponent bases in Triton chunk prefill
- [#32178](https://github.com/sgl-project/sglang/pull/32178) Support ENCODER_ONLY target-verify in the trtllm_mha backend
- [#13397](https://github.com/sgl-project/sglang/pull/13397) Add CPU kernel for shm_allgather_into_tensor and shm_reduce_scatter_tensor
- [#29973](https://github.com/sgl-project/sglang/pull/29973) Prevent Lightning Attention extra-buffer mamba state corruption
- [#31943](https://github.com/sgl-project/sglang/pull/31943) Reject online weight updates while the HPC-Ops router GEMM split cache is active
- [#31340](https://github.com/sgl-project/sglang/pull/31340) Fix FP8 Triton dtype selection on A100
- [#31087](https://github.com/sgl-project/sglang/pull/31087) Dispatch indexer topk_transform_512 through DSATopKBackend
- [#27059](https://github.com/sgl-project/sglang/pull/27059) Add FP4 Indexer for DeepSeek V4 on SM120
- [#32181](https://github.com/sgl-project/sglang/pull/32181) Fix trtllm_mla backend + fp8 kv cache without rope
- [#31312](https://github.com/sgl-project/sglang/pull/31312) Fix LongCat n-gram token-table crashes on padded batches
- [#32251](https://github.com/sgl-project/sglang/pull/32251) Read per-runner kv cache dtype off model_runner
- [#32411](https://github.com/sgl-project/sglang/pull/32411) Fix token count localization for replicated attention-TP forwards
- [#32277](https://github.com/sgl-project/sglang/pull/32277) Clamp degenerate all-sentinel draft rows to token 0 in dspark
- [#32288](https://github.com/sgl-project/sglang/pull/32288) Fix stale flashinfer-MLA fallback poisoning spec verify capture
- [#32346](https://github.com/sgl-project/sglang/pull/32346) Cherry-pick fix for stale flashinfer-MLA fallback
- [#30567](https://github.com/sgl-project/sglang/pull/30567) Support CuteDSL GEMM BF16 on SM100
- [#32130](https://github.com/sgl-project/sglang/pull/32130) Fix performance degradation of Qwen3.5-397B-A17B on NPU
- [#32134](https://github.com/sgl-project/sglang/pull/32134) Fix GPT-OSS-120b break on gfx1250
- [#32076](https://github.com/sgl-project/sglang/pull/32076) Fix Inkling kernel imports after migration
- [#31754](https://github.com/sgl-project/sglang/pull/31754) Fix unnecessary gather/scatter on CPU for non-contiguous Mamba statepool
- [#31867](https://github.com/sgl-project/sglang/pull/31867) Update non-vit vision part for cumulative seqlen on NPU
- [#32126](https://github.com/sgl-project/sglang/pull/32126) Seed the GDN CuteDSL correctness test inputs
- [#31863](https://github.com/sgl-project/sglang/pull/31863) Remove duplicate code in NPU attention
- [#32114](https://github.com/sgl-project/sglang/pull/32114) Delete cutlass_mla, non-Marlin GPTQ, AWQ AOT kernel, and Dual Chunk Flash Attention
- [#32222](https://github.com/sgl-project/sglang/pull/32222) Add DeepSeek v4 optimized sgl-kernel for CPU
- [#32059](https://github.com/sgl-project/sglang/pull/32059) Shared KV Cache for Prefill CP for DeepSeek V4
- [#32214](https://github.com/sgl-project/sglang/pull/32214) Strict bit-exact SWA HiCache for DeepSeek-V4
- [#32307](https://github.com/sgl-project/sglang/pull/32307) Optimization sana-videa and ltx2
- [#32094](https://github.com/sgl-project/sglang/pull/32094) Add LiteTopk fused indexer top-k prefill path for SM100
- [#32314](https://github.com/sgl-project/sglang/pull/32314) HiSparse V2: HiCache as the logical KV pool for HiSparse
- [#32327](https://github.com/sgl-project/sglang/pull/32327) Add Q8KV8 sparse MLA prefill runtime backend
- [#32368](https://github.com/sgl-project/sglang/pull/32368) Enable DSV4 unified-KV HiSparse PD over MoRI
- [#32374](https://github.com/sgl-project/sglang/pull/32374) Remove overlap scheduler host syncs for pure TP
- [#32451](https://github.com/sgl-project/sglang/pull/32451) Add MLX block paged attention decode
- [#32053](https://github.com/sgl-project/sglang/pull/32053) Add configurable target verify budget for DFlash V2
- [#32035](https://github.com/sgl-project/sglang/pull/32035) Support dspark c128 online compressor
- [#32452](https://github.com/sgl-project/sglang/pull/32452) Support HND KV cache layout in CPU offload
- [#32417](https://github.com/sgl-project/sglang/pull/32417) Remove FlashInfer and MRoPE host syncs
- [#32207](https://github.com/sgl-project/sglang/pull/32207) Support MTP when PP enabled in prefill nodes on NPU
- [#32118](https://github.com/sgl-project/sglang/pull/32118) Fix nightly CI NVFP4 cuda-graph crash and NVILA batching
- [#32439](https://github.com/sgl-project/sglang/pull/32439) ROCm: add Triton fallback for DSV4 indexer query
- [#32265](https://github.com/sgl-project/sglang/pull/32265) MiniMax-M3: fuse sparse QK norm, RoPE and cache writes with AITER
- [#32407](https://github.com/sgl-project/sglang/pull/32407) Replace ngram FULL_MASK Python for-loop with Triton kernel
- [#32391](https://github.com/sgl-project/sglang/pull/32391) Take the attention backend name from the backend instead of server_args
- [#32303](https://github.com/sgl-project/sglang/pull/32303) Scope Gemma 4 image masks to sliding attention
- [#32060](https://github.com/sgl-project/sglang/pull/32060) Avoid oversized speculative verify-mask fill for DSV4
- [#32087](https://github.com/sgl-project/sglang/pull/32087) Fix Triton SWA decode window dropping the oldest in-window key
- [#32183](https://github.com/sgl-project/sglang/pull/32183) Fix DSpark verifier state rewrite window
- [#32024](https://github.com/sgl-project/sglang/pull/32024) Fall back from SM100 CuTe prefill on SM12x
- [#32419](https://github.com/sgl-project/sglang/pull/32419) Use explicit speculative forward state for DSV4
- [#32115](https://github.com/sgl-project/sglang/pull/32115) Size request capacity by attention DP on MLX
- [#32046](https://github.com/sgl-project/sglang/pull/32046) Qwen3.5 integration gfx950 fmha fp8 hd256
- [#32140](https://github.com/sgl-project/sglang/pull/32140) Fix broken nsa_backend backward-compat shim
- [#32192](https://github.com/sgl-project/sglang/pull/32192) Native qk_rope_head_dim=0 sparse MLA decode in trtllm-gen DSA backend
- [#32269](https://github.com/sgl-project/sglang/pull/32269) Support XQA backend for SpecDec verify
- [#32320](https://github.com/sgl-project/sglang/pull/32320) Only split touched SWA pages in FlashMLA page-split kernel
- [#32370](https://github.com/sgl-project/sglang/pull/32370) Optimize FP32 LM head for bf16/fp16
- [#32186](https://github.com/sgl-project/sglang/pull/32186) Reduce DSpark import side effects
- [#32062](https://github.com/sgl-project/sglang/pull/32062) Plan wrappers from layer-local attention metadata for FlashInfer

</details>

<details>
<summary>MoE & quantization (42)</summary>

- [#24651](https://github.com/sgl-project/sglang/pull/24651) Add fused all-reduce RMSNorm per-group quant for Qwen3.5 FP8
- [#30541](https://github.com/sgl-project/sglang/pull/30541) Add HPC-Ops FP8 MoE runner backend
- [#31017](https://github.com/sgl-project/sglang/pull/31017) Add DeepSeek-reference 1e-20 epsilon to top-k renormalization
- [#29569](https://github.com/sgl-project/sglang/pull/29569) Support megamoe for CP on DSV4
- [#32248](https://github.com/sgl-project/sglang/pull/32248) Migrate CompressedTensorsW4A4Nvfp4MoE TRT-LLM path onto MoeRunner
- [#32125](https://github.com/sgl-project/sglang/pull/32125) Add LongCat-Flash-Lite-FP8 8-GPU nightly test + fix NextN rope_theta
- [#31346](https://github.com/sgl-project/sglang/pull/31346) Fail fast on fp8_e4m3 KV with tilelang DSA backend on CUDA
- [#31825](https://github.com/sgl-project/sglang/pull/31825) Support NVFP4_AWQ checkpoints in ModelOpt FP4 path
- [#31998](https://github.com/sgl-project/sglang/pull/31998) Rename A5 product name
- [#31796](https://github.com/sgl-project/sglang/pull/31796) Fix rl update weights Parameter object has no attribute weight_LOADER
- [#29523](https://github.com/sgl-project/sglang/pull/29523) Make DeepEP auto serve flashinfer_cutedsl FP4
- [#31793](https://github.com/sgl-project/sglang/pull/31793) Disable global-slot shared-expert fusion under per-rank EP backends
- [#32246](https://github.com/sgl-project/sglang/pull/32246) Fix nvfp4 online scale with pcg
- [#32259](https://github.com/sgl-project/sglang/pull/32259) Cherry-pick fix nvfp4 online scale with pcg
- [#31085](https://github.com/sgl-project/sglang/pull/31085) Support FlashInfer TRT-LLM NVFP4 MoE in the RL weight checker
- [#31762](https://github.com/sgl-project/sglang/pull/31762) Only apply routed_scaling_factor in moe_sum_reduce
- [#32113](https://github.com/sgl-project/sglang/pull/32113) Fix w4a8 MoE performance degradation on NPU
- [#31782](https://github.com/sgl-project/sglang/pull/31782) Fix startup bug in olmoe 1b 7b on NPU
- [#32040](https://github.com/sgl-project/sglang/pull/32040) Ascend fuseep use moe ep group
- [#32049](https://github.com/sgl-project/sglang/pull/32049) Fix Marlin MoE test ServerArgs initialization
- [#32329](https://github.com/sgl-project/sglang/pull/32329) Add NCCL EP as optional moe-a2a-backend
- [#32280](https://github.com/sgl-project/sglang/pull/32280) Fix LLaDA2.2 block-routing MoE for Ascend
- [#32266](https://github.com/sgl-project/sglang/pull/32266) Add W8A8 MXFP8 quantization support for Qwen3.5 on Ascend NPU
- [#32058](https://github.com/sgl-project/sglang/pull/32058) Add fused SiLU+clamp+mul+FP8 quant AOT kernel for DeepSeek V4 EP MoE
- [#32033](https://github.com/sgl-project/sglang/pull/32033) Support native W4AFP8 checkpoint schemas
- [#32398](https://github.com/sgl-project/sglang/pull/32398) Enable NVFP4 for model weight loading daemon
- [#32119](https://github.com/sgl-project/sglang/pull/32119) Add SM12x b12x NVFP4 MoE support
- [#32405](https://github.com/sgl-project/sglang/pull/32405) Migrate SM100 trtllm-gen mxfp4 MoE onto MoeRunner
- [#32395](https://github.com/sgl-project/sglang/pull/32395) Single-launch moe_align for tiny batches with many experts
- [#32443](https://github.com/sgl-project/sglang/pull/32443) Fuse gated RMSNorm and FP8 quantization for Qwen3.5
- [#32120](https://github.com/sgl-project/sglang/pull/32120) Add GLM-5.2 MXFP4 1P1D DI/CI recipes
- [#32173](https://github.com/sgl-project/sglang/pull/32173) Support static W4A8 FP8 activation quantization for MoE
- [#32116](https://github.com/sgl-project/sglang/pull/32116) Add Kimi-K2.6 wide-EP16 2P1D nightly recipes
- [#32048](https://github.com/sgl-project/sglang/pull/32048) Enable Kimi K2.6 wideEP
- [#32133](https://github.com/sgl-project/sglang/pull/32133) Enable MiniMax-M3 MXFP8 AITER MoE
- [#31989](https://github.com/sgl-project/sglang/pull/31989) Support nvidia/MiniMax-M3-NVFP4
- [#32229](https://github.com/sgl-project/sglang/pull/32229) Use flashinfer_cutlass for auto MoE on SM100
- [#32304](https://github.com/sgl-project/sglang/pull/32304) Extend hpc_ops dynamic-scheduled decode to bf16
- [#32315](https://github.com/sgl-project/sglang/pull/32315) Speed up DSV4 MoE weight loading from mmap views
- [#31994](https://github.com/sgl-project/sglang/pull/31994) Mori ep decode small cap
- [#32190](https://github.com/sgl-project/sglang/pull/32190) MiniMax-M3: run MoE via aiter FlyDSL native MXFP8 SwiGLU
- [#32340](https://github.com/sgl-project/sglang/pull/32340) Amd/dsv4 shared experts fusion top6
- [#32261](https://github.com/sgl-project/sglang/pull/32261) Fuse Gemma3RMSNorm CUDA path into gemma_rmsnorm kernel

</details>

<details>
<summary>Model support (15)</summary>

- [#32364](https://github.com/sgl-project/sglang/pull/32364) sglang-mm: server vision pipeline core + Qwen VL
- [#32365](https://github.com/sgl-project/sglang/pull/32365) rust-server: native multimodal processing for Qwen VL
- [#32415](https://github.com/sgl-project/sglang/pull/32415) Split multimodal scheduling from mm_utils
- [#32341](https://github.com/sgl-project/sglang/pull/32341) Add LingBot-Video MoE 30B T2V support
- [#32041](https://github.com/sgl-project/sglang/pull/32041) Add FA MXFP8 quantization support for Wan2.2 Diffusion on Ascend NPU
- [#32397](https://github.com/sgl-project/sglang/pull/32397) sglang-mm: turbojpeg + PNG streaming + buffer pool
- [#32104](https://github.com/sgl-project/sglang/pull/32104) Fix Kimi-VL 2D encoder grids
- [#32258](https://github.com/sgl-project/sglang/pull/32258) Validate precomputed image token counts for Gemma 4
- [#32425](https://github.com/sgl-project/sglang/pull/32425) Make multimodal loading opt-in for Gemma 4
- [#32151](https://github.com/sgl-project/sglang/pull/32151) Add support for Nanbeige4.2
- [#32401](https://github.com/sgl-project/sglang/pull/32401) Support standalone text-only Qwen3.5 checkpoints
- [#32375](https://github.com/sgl-project/sglang/pull/32375) Support EmbeddingGemma
- [#32231](https://github.com/sgl-project/sglang/pull/32231) Apply Gemma4 local/global head-dim remap to standalone gemma4_text configs
- [#32221](https://github.com/sgl-project/sglang/pull/32221) Support Gemma 4 language-only startup
- [#32102](https://github.com/sgl-project/sglang/pull/32102) Add Gemma 4 E2B text generation with native caches

</details>

<details>
<summary>Parallelism & scheduling (75)</summary>

- [#31814](https://github.com/sgl-project/sglang/pull/31814) Read resolved config via namespace accessors
- [#32100](https://github.com/sgl-project/sglang/pull/32100) Revert RuntimeContext config-namespace reads/roles
- [#31812](https://github.com/sgl-project/sglang/pull/31812) Route runtime config adjustments through the namespace bags
- [#31810](https://github.com/sgl-project/sglang/pull/31810) Add resolved-config namespace bags and accessors
- [#31816](https://github.com/sgl-project/sglang/pull/31816) Read parallel config leaves via get_parallel()
- [#31811](https://github.com/sgl-project/sglang/pull/31811) Make ServerArgs read-only with a single audited mutation entry
- [#31815](https://github.com/sgl-project/sglang/pull/31815) Load-time declarations write the config bags
- [#31817](https://github.com/sgl-project/sglang/pull/31817) Publish resolved config in unit fixtures for the namespace API
- [#32108](https://github.com/sgl-project/sglang/pull/32108) Cherry-pick sampling mask support to sglang-miles
- [#23534](https://github.com/sgl-project/sglang/pull/23534) Add XPU device support for LMCache radix cache integration
- [#29326](https://github.com/sgl-project/sglang/pull/29326) Add shared memory allocator for host KV cache
- [#30981](https://github.com/sgl-project/sglang/pull/30981) Support staged write-back for asymmetric MHA
- [#32270](https://github.com/sgl-project/sglang/pull/32270) Support pipeline-parallel hybrid-linear transfer
- [#31744](https://github.com/sgl-project/sglang/pull/31744) Fix recovery lifecycle and add manual coverage for Elastic EP
- [#30986](https://github.com/sgl-project/sglang/pull/30986) Fix mamba state corruption and slot leak when load_back aborts
- [#31144](https://github.com/sgl-project/sglang/pull/31144) Prevent decode scheduler from blocking on ZMQ sends to a stalled prefill peer
- [#31217](https://github.com/sgl-project/sglang/pull/31217) Robustness and failure handling for Disagg StagingBuffer
- [#31230](https://github.com/sgl-project/sglang/pull/31230) Add a per-path cap for cached states in Mamba
- [#31813](https://github.com/sgl-project/sglang/pull/31813) Record the publishing process role in runtime_context
- [#31845](https://github.com/sgl-project/sglang/pull/31845) Write-back policy fix for unified tree
- [#32379](https://github.com/sgl-project/sglang/pull/32379) Fix SWA admission livelock on cached-prefix resumes
- [#31592](https://github.com/sgl-project/sglang/pull/31592) Harden zmq_to_scheduler receiver failures
- [#32339](https://github.com/sgl-project/sglang/pull/32339) Enable multi-node custom-AR v2 on a single NVLink clique
- [#32245](https://github.com/sgl-project/sglang/pull/32245) Add prefill and decode load counters to LoadSnapshot
- [#32023](https://github.com/sgl-project/sglang/pull/32023) Enable decode retraction ordering under speculative decoding
- [#30096](https://github.com/sgl-project/sglang/pull/30096) Support grammar-constrained decoding in speculative verify
- [#31962](https://github.com/sgl-project/sglang/pull/31962) Fix flush_cache() no-op after pause_generation in retract
- [#31181](https://github.com/sgl-project/sglang/pull/31181) Support Mamba branching in Unified Radix Cache with HiCache
- [#30954](https://github.com/sgl-project/sglang/pull/30954) Allow fused MHC opt-in with standalone TileLang pre disabled
- [#31753](https://github.com/sgl-project/sglang/pull/31753) Grammar-constrained decoding, incl. tool_choice=auto
- [#31708](https://github.com/sgl-project/sglang/pull/31708) Centralize Mooncake PG configuration
- [#32373](https://github.com/sgl-project/sglang/pull/32373) Fix --hicache-size allocating ~2x host memory on hybrid SWA
- [#31920](https://github.com/sgl-project/sglang/pull/31920) Add model-aware key isolation to Mooncake Store
- [#32029](https://github.com/sgl-project/sglang/pull/32029) Unify pinned host pool release on graceful shutdown
- [#30412](https://github.com/sgl-project/sglang/pull/30412) Fix multi-tokenizer disaggregation metrics labels
- [#32184](https://github.com/sgl-project/sglang/pull/32184) Reserve the mamba pool's +1 padding slot in the memory budget solve
- [#32353](https://github.com/sgl-project/sglang/pull/32353) Consolidate the grammar sync decision into ScheduleBatch.grammar_needs_sync
- [#32016](https://github.com/sgl-project/sglang/pull/32016) Evict only the KV shortfall in evict_from_tree_cache
- [#32122](https://github.com/sgl-project/sglang/pull/32122) Include disagg prefill waiting queue in FPM
- [#32389](https://github.com/sgl-project/sglang/pull/32389) Fix prefill suspension caused by delayed negotiate_should_allow_prefill invocation
- [#32424](https://github.com/sgl-project/sglang/pull/32424) Implement streaming hidden-state transfer for Mooncake
- [#32423](https://github.com/sgl-project/sglang/pull/32423) Integrate hidden-state bootstrap into PD scheduling
- [#32177](https://github.com/sgl-project/sglang/pull/32177) Prototype live P-to-D token handoff
- [#32162](https://github.com/sgl-project/sglang/pull/32162) Support hisparse multi-step swap io kernel
- [#32018](https://github.com/sgl-project/sglang/pull/32018) Support tensor-parallel Domino rollout
- [#32017](https://github.com/sgl-project/sglang/pull/32017) Overlap checkpoint staging with CUDA graph capture during startup
- [#32281](https://github.com/sgl-project/sglang/pull/32281) Enable dspark under pipeline parallelism
- [#32042](https://github.com/sgl-project/sglang/pull/32042) Restore disaggregated decode overlap with resource leases
- [#32422](https://github.com/sgl-project/sglang/pull/32422) Add hidden-state transfer primitives and draft injection
- [#32238](https://github.com/sgl-project/sglang/pull/32238) Support upsert when loading adapters from distributed
- [#32201](https://github.com/sgl-project/sglang/pull/32201) Add one-sided RMA support with ncclPutSignal/ncclWaitSignal
- [#32236](https://github.com/sgl-project/sglang/pull/32236) Add per-component cache-source breakdown for DeepSeek V4
- [#32209](https://github.com/sgl-project/sglang/pull/32209) Fix PD decode hang with DP attention and GLM-5.2 MTP
- [#32081](https://github.com/sgl-project/sglang/pull/32081) Two stage intra turn prefix cache
- [#32278](https://github.com/sgl-project/sglang/pull/32278) Fix decode_hicache send metadata bug
- [#32228](https://github.com/sgl-project/sglang/pull/32228) Skip mamba lock during decoding
- [#32429](https://github.com/sgl-project/sglang/pull/32429) Add zero-copy NVLS multicast to custom-AR v2
- [#31993](https://github.com/sgl-project/sglang/pull/31993) Measure KV transfer speed per actual transfer for disaggregation
- [#32026](https://github.com/sgl-project/sglang/pull/32026) Dev-only debug mode: fault-tolerant event loop
- [#32450](https://github.com/sgl-project/sglang/pull/32450) Fix hybrid-SSM + radix cache crashes in the auxiliary-state component
- [#32147](https://github.com/sgl-project/sglang/pull/32147) Mooncake: report KV transfer latency metric
- [#32413](https://github.com/sgl-project/sglang/pull/32413) Handle unsupported decode KV retraction
- [#32208](https://github.com/sgl-project/sglang/pull/32208) O(1) slot allocation in ReqToTokenPool.alloc()
- [#32052](https://github.com/sgl-project/sglang/pull/32052) Fix hybrid recurrent-state commit for radix cache
- [#32215](https://github.com/sgl-project/sglang/pull/32215) Make memory release admission safe
- [#32388](https://github.com/sgl-project/sglang/pull/32388) Observability enhancement for L2
- [#32446](https://github.com/sgl-project/sglang/pull/32446) Release per-request state on extend batches
- [#32447](https://github.com/sgl-project/sglang/pull/32447) Honor gracefully_exit in event_loop_overlap_mlx
- [#32455](https://github.com/sgl-project/sglang/pull/32455) Make LMCache MP store non-blocking on request finish
- [#32082](https://github.com/sgl-project/sglang/pull/32082) Fix speculative draft load format resolution
- [#32080](https://github.com/sgl-project/sglang/pull/32080) Add cache-agnostic in-batch prefix defer baseline
- [#32216](https://github.com/sgl-project/sglang/pull/32216) Use exact paged-KV accounting at context boundary
- [#32213](https://github.com/sgl-project/sglang/pull/32213) Propagate memory saver to hybrid-SWA KV pools
- [#32196](https://github.com/sgl-project/sglang/pull/32196) Keep EAGLE DP graph and token metadata consistent
- [#32247](https://github.com/sgl-project/sglang/pull/32247) Fix Qwen3.5 TP1-attention prefill -> TP4 decode fails
- [#32153](https://github.com/sgl-project/sglang/pull/32153) Fix flush_cache() no-op after pause_generation
- [#32454](https://github.com/sgl-project/sglang/pull/32454) Fix prefill delayer timeout rank divergence
- [#32137](https://github.com/sgl-project/sglang/pull/32137) Read resolved config via RuntimeContext namespace accessors (re-land)
- [#32313](https://github.com/sgl-project/sglang/pull/32313) Optimize TP LMHead with All-to-All

</details>

<details>
<summary>Hardware & arch (13)</summary>

- [#32043](https://github.com/sgl-project/sglang/pull/32043) GFX1250 ROCm bringup: infra, build, kernels and models
- [#31949](https://github.com/sgl-project/sglang/pull/31949) Add Intel XPU Platform support
- [#32055](https://github.com/sgl-project/sglang/pull/32055) Fix ROCm 7.15 Helios image release
- [#31757](https://github.com/sgl-project/sglang/pull/31757) Build Miles nightly ROCm images with docker/build.py
- [#32142](https://github.com/sgl-project/sglang/pull/32142) Update ROCM version to 7.15.0a20260712
- [#32073](https://github.com/sgl-project/sglang/pull/32073) Fix performance degradation of Qwen3.5 model on NPU
- [#32392](https://github.com/sgl-project/sglang/pull/32392) Add PR test cases for NPU
- [#32175](https://github.com/sgl-project/sglang/pull/32175) AMD ROCm enablement for GLM-5.x
- [#32092](https://github.com/sgl-project/sglang/pull/32092) Add experimental gfx1201 inference support
- [#32438](https://github.com/sgl-project/sglang/pull/32438) Stabilize B580 XPU CI
- [#32284](https://github.com/sgl-project/sglang/pull/32284) Enable pinned host memory for Intel XPU
- [#32165](https://github.com/sgl-project/sglang/pull/32165) Tune MiniMax-M3 sparse prefill on ROCm
- [#32039](https://github.com/sgl-project/sglang/pull/32039) Qwen3.5 MoRI: fix expert routing, decode CUDA graph, and AITER buffer capacity

</details>

<details>
<summary>API & serving (34)</summary>

- [#24256](https://github.com/sgl-project/sglang/pull/24256) Add presharded load format
- [#31809](https://github.com/sgl-project/sglang/pull/31809) Annotate ServerArgs fields with their runtime-config namespace
- [#31832](https://github.com/sgl-project/sglang/pull/31832) Decode input_audio media containers with PyAV
- [#30917](https://github.com/sgl-project/sglang/pull/30917) Add return_token_ids support to completions and chat completions APIs
- [#31076](https://github.com/sgl-project/sglang/pull/31076) Add native gRPC sidecar module launcher
- [#32074](https://github.com/sgl-project/sglang/pull/32074) Cherry-pick native gRPC sidecar module launcher
- [#30832](https://github.com/sgl-project/sglang/pull/30832) Add 'anyOf' schema support for qwen3_coder tool call parser
- [#32348](https://github.com/sgl-project/sglang/pull/32348) Report accelerator type in /v1/loads
- [#30938](https://github.com/sgl-project/sglang/pull/30938) Warn on small Mamba chunked prefill size
- [#31975](https://github.com/sgl-project/sglang/pull/31975) Treat partial_json_parser AssertionError as incomplete JSON
- [#32369](https://github.com/sgl-project/sglang/pull/32369) sglang rust server control plane api
- [#32366](https://github.com/sgl-project/sglang/pull/32366) sglang rust server runtime
- [#32121](https://github.com/sgl-project/sglang/pull/32121) Add typed multi-choice generation via gRPC
- [#32249](https://github.com/sgl-project/sglang/pull/32249) sglang rust server tm egress
- [#32358](https://github.com/sgl-project/sglang/pull/32358) sglang rust server tokenizer manager, ring and runnable interface
- [#32342](https://github.com/sgl-project/sglang/pull/32342) sglang rust server egress message
- [#32244](https://github.com/sgl-project/sglang/pull/32244) sglang rust server tokenizer and detokenizer
- [#32361](https://github.com/sgl-project/sglang/pull/32361) sglang rust server tm ingress
- [#32242](https://github.com/sgl-project/sglang/pull/32242) sglang rust server request message
- [#32343](https://github.com/sgl-project/sglang/pull/32343) sglang rust server sampling message
- [#32237](https://github.com/sgl-project/sglang/pull/32237) Support aborting requests by rid prefix
- [#32078](https://github.com/sgl-project/sglang/pull/32078) Opt-in flat response format for prompt top logprobs
- [#32322](https://github.com/sgl-project/sglang/pull/32322) Reconcile k8s service discovery with periodic full LIST
- [#32275](https://github.com/sgl-project/sglang/pull/32275) Support Ascend Mamba host transfers
- [#32185](https://github.com/sgl-project/sglang/pull/32185) Standalone-process mode + hugetlb-backed shared host buffer
- [#32428](https://github.com/sgl-project/sglang/pull/32428) Extract reasoning-request normalization into standalone helpers
- [#32338](https://github.com/sgl-project/sglang/pull/32338) Add unit tests for request_headers and managers utils
- [#32274](https://github.com/sgl-project/sglang/pull/32274) Extract context from incoming request headers
- [#32295](https://github.com/sgl-project/sglang/pull/32295) Strip whitespace when parsing legacy and Envs boolean/int fields
- [#32167](https://github.com/sgl-project/sglang/pull/32167) Fix streaming tool calls losing arguments when completed in the final delta
- [#32152](https://github.com/sgl-project/sglang/pull/32152) Add attention-backend auto-tune CLI
- [#32141](https://github.com/sgl-project/sglang/pull/32141) Support --load-format dummy for KimiLinearForCausalLM

</details>

<details>
<summary>Tests, CI & build (51)</summary>

- [#32014](https://github.com/sgl-project/sglang/pull/32014) Create rust workspace
- [#30613](https://github.com/sgl-project/sglang/pull/30613) Nightly Test Coverage - Minimax-M3-MXFP8 Accuracy Test
- [#32095](https://github.com/sgl-project/sglang/pull/32095) Add Inkling per-commit server test
- [#32128](https://github.com/sgl-project/sglang/pull/32128) Reclassify kernel tests by ops group + move helpers out
- [#32069](https://github.com/sgl-project/sglang/pull/32069) Register the Helios release workflow on main
- plus 46 more minor CI and test updates

</details>

<details>
<summary>Docs (8)</summary>

- [#32127](https://github.com/sgl-project/sglang/pull/32127) Sync LMSYS SGLang blog cards
- [#31413](https://github.com/sgl-project/sglang/pull/31413) Add Qwen3.6 35B NVFP4 to cookbook
- [#32205](https://github.com/sgl-project/sglang/pull/32205) Update npu quickstart
- [#32347](https://github.com/sgl-project/sglang/pull/32347) Bump docs install version to 0.5.16
- [#32310](https://github.com/sgl-project/sglang/pull/32310) Add clusterdOS integration reference
- [#32414](https://github.com/sgl-project/sglang/pull/32414) Add Reasoning-Aware Compression (RAC) pruning recipe
- [#32224](https://github.com/sgl-project/sglang/pull/32224) Add DWDP documentation
- [#32123](https://github.com/sgl-project/sglang/pull/32123) Rename docs_new/ to docs/

</details>

<details>
<summary>Bugfixes (24)</summary>

- [#32262](https://github.com/sgl-project/sglang/pull/32262) Fix Kimi-Linear state transfer across heterogeneous TP
- [#29830](https://github.com/sgl-project/sglang/pull/29830) Fix presharded cache-key gaps
- [#31769](https://github.com/sgl-project/sglang/pull/31769) Fix Cohere2MoeConfig import crash from huggingface_hub strict
- [#32239](https://github.com/sgl-project/sglang/pull/32239) Fix dynamo recompile limit in allreduce and bf16 gemm
- [#32292](https://github.com/sgl-project/sglang/pull/32292) Cherry-pick Fix dynamo recompile limit
- [#31870](https://github.com/sgl-project/sglang/pull/31870) Fix WAR race: never write MoE runner output into hidden_states in place
- [#32188](https://github.com/sgl-project/sglang/pull/32188) Two root causes of the H100 deepep TBO CI break
- [#32279](https://github.com/sgl-project/sglang/pull/32279) Fail fast when a safetensors index references missing shard files
- [#31275](https://github.com/sgl-project/sglang/pull/31275) Fix HTTP dispatch lock blocking cross-request encoder batching
- [#31752](https://github.com/sgl-project/sglang/pull/31752) Fix DS/Kimi crash on non-first PP ranks when resolving input length
- [#31988](https://github.com/sgl-project/sglang/pull/31988) Fix reward/classification models broken by load_weights v2 dispatch
- [#32254](https://github.com/sgl-project/sglang/pull/32254) Fix inkling multi layer mtp draft extend cuda graph
- [#32260](https://github.com/sgl-project/sglang/pull/32260) Cherry-pick Fix inkling multi layer mtp draft extend cuda graph
- [#30112](https://github.com/sgl-project/sglang/pull/30112) Bugfix for extra device memory on Ascend
- [#32096](https://github.com/sgl-project/sglang/pull/32096) Fix get_server_args import lint error
- [#32360](https://github.com/sgl-project/sglang/pull/32360) Report which limit bound max_running_requests
- [#32070](https://github.com/sgl-project/sglang/pull/32070) Use per-DP-rank loads for power-of-two routing
- [#32318](https://github.com/sgl-project/sglang/pull/32318) Fix FlashInfer MNNVL workspace size check
- [#32027](https://github.com/sgl-project/sglang/pull/32027) DeepSeek tool-call parser: one malformed call drops all valid calls
- [#32334](https://github.com/sgl-project/sglang/pull/32334) Fix GPT-OSS EAGLE3 hidden states
- [#32107](https://github.com/sgl-project/sglang/pull/32107) Fix ReDoS in PythonicDetector's tool-call locator regex
- [#32299](https://github.com/sgl-project/sglang/pull/32299) Resolve MiniMax-M3 top-level oneOf parameter schemas
- [#32387](https://github.com/sgl-project/sglang/pull/32387) Top_logprobs entries silently collapse on decode-text collision
- [#32301](https://github.com/sgl-project/sglang/pull/32301) Honor MiniMax thinking controls

</details>

<details>
<summary>Refactors (5)</summary>

- [#32240](https://github.com/sgl-project/sglang/pull/32240) sglang rust server environ fsm error id gen
- [#32435](https://github.com/sgl-project/sglang/pull/32435) Load initial expert location metadata on CPU
- [#32434](https://github.com/sgl-project/sglang/pull/32434) Consolidate compiled-kernel caches under SGLANG_CACHE_DIR
- [#32093](https://github.com/sgl-project/sglang/pull/32093) Adapt device agnostic API usage
- [#32437](https://github.com/sgl-project/sglang/pull/32437) Move presharded checkpoints under SGLANG_CACHE_DIR

</details>

<details>
<summary>Other (11)</summary>

- [#32308](https://github.com/sgl-project/sglang/pull/32308) Add leveled invariant-check primitive for nan/inf/oob validity checks
- [#30822](https://github.com/sgl-project/sglang/pull/30822) Use deterministic seeded coins for EAGLE rejection sampling
- [#32409](https://github.com/sgl-project/sglang/pull/32409) Hold the grammar bitmask in one GrammarMask type across all decode paths
- [#32393](https://github.com/sgl-project/sglang/pull/32393) Share the grammar mask build and verify-tree staging across spec workers
- [#32412](https://github.com/sgl-project/sglang/pull/32412) Use native batched llguidance mask generation
- [#32427](https://github.com/sgl-project/sglang/pull/32427) Add fill_draft_extend_prepare_buffers_native for NPU
- [#32380](https://github.com/sgl-project/sglang/pull/32380) Derive NGRAM grammar tree links on the host
- [#32110](https://github.com/sgl-project/sglang/pull/32110) Enable grammar overlap scheduling for STANDALONE speculative decoding
- [#30026](https://github.com/sgl-project/sglang/pull/30026) Add deterministic inference for eagle parity test
- [#32317](https://github.com/sgl-project/sglang/pull/32317) Add --verify-attention-backend for speculative target verify
- [#32085](https://github.com/sgl-project/sglang/pull/32085) Bound the grammar-compile thread pool and expose SGLANG_GRAMMAR_COMPILE_MAX_WORKERS

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 8ecd342697c0ed88d8d573a4617735e69875f749e03961c6d8b9e63a88ee4fc0 -->
