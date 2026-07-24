# sglang: PR digest (2026-07-19 to 2026-07-23)

_187 merged, 293 newly opened - source sgl-project/sglang, generated 2026-07-23T11:30:13Z_

## TL;DR
- **DeepSeek focus**: DeepSeek V4, V3.2, and R1 received major attention, including a new Shared KV Cache for Prefill Context Parallelism, SWA recompute, and DSA Q8KV8 FP8 Sparse Prefill optimizations.
- **Kernel Refactoring**: The massive RFC #29630 migration is complete, moving tangled JIT subsystems and operator groups into a unified `sglang.kernels` namespace and retiring `sglang.jit_kernel`.
- **Performance & Memory**: Major memory and throughput wins include the introduction of OSCAR mixed-precision INT2 KV caching, Distributed Weight Data Parallelism (DWDP) for MoE prefill, and Decode Context Parallelism (DCP) for DSA models.
- **Hardware & Quantization**: AMD GFX1250 ROCm bringup was merged, alongside extensive NPU support enhancements and new NVFP4 MoE support for SM12x architectures.

## Most important PRs
- **[#32045](https://github.com/sgl-project/sglang/pull/32045)** [Kernel] Phase 4 batch-3: migrate tangled JIT subsystems + new groups into kernels.ops (RFC #29630)
  Completes the massive refactor retiring `sglang.jit_kernel` and unifying operator groups into a clean `sglang.kernels` namespace.
- **[#31681](https://github.com/sgl-project/sglang/pull/31681)** Add Inkling model support
  Merges comprehensive support for the Inkling model family, touching attention, MoE, multimodal, and speculative decoding paths.
- **[#32129](https://github.com/sgl-project/sglang/pull/32129)** [Feature] OSCAR mixed-precision INT2 KV cache (--kv-cache-dtype int2)
  Introduces highly compressed INT2 KV caching via Triton, significantly reducing memory footprint for long-context workloads.
- **[#29778](https://github.com/sgl-project/sglang/pull/29778)** [Feature] Add DWDP (Distributed Weight Data Parallelism) for MoE prefill
  Implements DWDP to optimize MoE prefill performance and memory distribution across workers.
- **[#32059](https://github.com/sgl-project/sglang/pull/32059)** [Feat][DeepSeek V4] Shared KV Cache for Prefill CP
  Enables shared KV caching during prefill context parallelism for DeepSeek V4, drastically cutting memory overhead for large contexts.

## More changes by area

<details>
<summary>Performance (15)</summary>

- [#31986](https://github.com/sgl-project/sglang/pull/31986) Stack dspark dense draft per-layer ctx KV projection into one GEMM
- [#32109](https://github.com/sgl-project/sglang/pull/32109) Skip blocks past per-request live length in full-width Triton kernels
- [#31301](https://github.com/sgl-project/sglang/pull/31301) Avoid temporary VLM encoder gather padding
- [#31981](https://github.com/sgl-project/sglang/pull/31981) Skip page-table columns past kv length in DSA draft-extend metadata kernel
- [#32130](https://github.com/sgl-project/sglang/pull/32130) Fix performance degradation of Qwen3.5-397B-A17B on NPU
- [#28416](https://github.com/sgl-project/sglang/pull/28416) Write FlashInfer TRT-LLM MoE output directly for GLM5
- [#31311](https://github.com/sgl-project/sglang/pull/31311) Fix LongCat-2.0 real EP double all-reduce + ScMoE RoPE crash
- [#31931](https://github.com/sgl-project/sglang/pull/31931) Optimize DeepSeek-V4 performance on NPU
- [#31963](https://github.com/sgl-project/sglang/pull/31963) Fuse RMSNorm and FP8 quant in JIT CUDA kernels
- [#32090](https://github.com/sgl-project/sglang/pull/32090) Fuse offline C128 speculative-draft state cleanup into a single kernel launch
- [#31824](https://github.com/sgl-project/sglang/pull/31824) Fuse draft extend metadata prep for speculative decoding
- [#32010](https://github.com/sgl-project/sglang/pull/32010) Support ragged verify graphs in the DSA attention backend
- [#31958](https://github.com/sgl-project/sglang/pull/31958) Compute input logprobs without materializing the full-vocab log-softmax
- [#32194](https://github.com/sgl-project/sglang/pull/32194) Skip unused draft metadata in DeepSeek V4 speculative decoding
- [#31854](https://github.com/sgl-project/sglang/pull/31854) CUDA-IPC zero-staging all-to-all for 2-rank Ulysses in diffusion models

</details>

<details>
<summary>Kernels & attention (32)</summary>

- [#30540](https://github.com/sgl-project/sglang/pull/30540) Add HPC-Ops attention backend
- [#31050](https://github.com/sgl-project/sglang/pull/31050) Preserve attention LSE through the custom-op boundary
- [#29972](https://github.com/sgl-project/sglang/pull/29972) Support MiMo V2.5 with zigzag context parallelism
- [#30981](https://github.com/sgl-project/sglang/pull/30981) Support staged write-back for asymmetric MHA in hicache
- [#30868](https://github.com/sgl-project/sglang/pull/30868) Fix VLM CUDA graph shape stability
- [#31904](https://github.com/sgl-project/sglang/pull/31904) Fix mixed exponent bases in Triton chunk prefill
- [#29973](https://github.com/sgl-project/sglang/pull/29973) Prevent Lightning Attention extra-buffer mamba state corruption
- [#31838](https://github.com/sgl-project/sglang/pull/31838) Fix pad-row top-k masking with custom_routing_function under DP attention
- [#31732](https://github.com/sgl-project/sglang/pull/31732) Support GPT-OSS zigzag CP with TRTLLM-MHA
- [#31474](https://github.com/sgl-project/sglang/pull/31474) Fix KDA prefix caching under mamba extra_buffer and enable it for kimi_linear
- [#31667](https://github.com/sgl-project/sglang/pull/31667) Make Q contiguous before TRT-LLM MHA decode
- [#31688](https://github.com/sgl-project/sglang/pull/31688) Fix ROCm fused KV and KDA paths
- [#31714](https://github.com/sgl-project/sglang/pull/31714) Bump CuTe DSL to 4.6.0
- [#31250](https://github.com/sgl-project/sglang/pull/31250) Add XPU path for causal_conv1d_fn and causal_conv1d_update
- [#31778](https://github.com/sgl-project/sglang/pull/31778) Enhance NPU support, CUDA graph features, and bug fixes
- [#32114](https://github.com/sgl-project/sglang/pull/32114) Delete cutlass_mla, non-Marlin GPTQ, AWQ AOT kernel, and Dual Chunk Flash Attention
- [#31967](https://github.com/sgl-project/sglang/pull/31967) KVarN: KV-cache compression for hybrid linear-attention models
- [#31790](https://github.com/sgl-project/sglang/pull/31790) Add standalone Quest GPU kernel primitives
- [#32094](https://github.com/sgl-project/sglang/pull/32094) Add LiteTopk fused indexer top-k prefill path for SM100
- [#31820](https://github.com/sgl-project/sglang/pull/31820) Use piecewise cuda graphs
- [#32152](https://github.com/sgl-project/sglang/pull/32152) Add attention-backend auto-tune CLI
- [#31834](https://github.com/sgl-project/sglang/pull/31834) Support a same-size mixed q dtype in the fused RoPE kernels
- [#31760](https://github.com/sgl-project/sglang/pull/31760) Handle partial-DP padding in Decode page-table transform
- [#31689](https://github.com/sgl-project/sglang/pull/31689) Avoid batch-size specialization in masked KV writes
- [#32183](https://github.com/sgl-project/sglang/pull/32183) Fix dspark verifier rewrite window
- [#32024](https://github.com/sgl-project/sglang/pull/32024) Fall back from SM100 CuTe prefill on SM12x for linear attention
- [#32192](https://github.com/sgl-project/sglang/pull/32192) Native qk_rope_head_dim=0 sparse MLA decode in trtllm-gen DSA backend
- [#32140](https://github.com/sgl-project/sglang/pull/32140) Fix broken nsa_backend backward-compat shim
- [#31686](https://github.com/sgl-project/sglang/pull/31686) Record the WAR read-done event in-graph to cover replay-time metadata reads
- [#32178](https://github.com/sgl-project/sglang/pull/32178) Support ENCODER_ONLY target-verify in the trtllm_mha backend
- [#31940](https://github.com/sgl-project/sglang/pull/31940) Use pip FA4 by default
- [#31959](https://github.com/sgl-project/sglang/pull/31959) Add SM120 support for trtllm mha prefill

</details>

<details>
<summary>MoE & quantization (34)</summary>

- [#30924](https://github.com/sgl-project/sglang/pull/30924) Trait-driven per_token_group_quant: unify the quant kernel family
- [#24651](https://github.com/sgl-project/sglang/pull/24651) Add fused all-reduce RMSNorm per-group quant for Qwen3.5 FP8 on AMD
- [#28291](https://github.com/sgl-project/sglang/pull/28291) Reland Online MXFP4 quantization 2/N - FP8 to MXFP4 requantization on AMD GPUs
- [#30514](https://github.com/sgl-project/sglang/pull/30514) Integrate Q8KV8 FP8 Sparse MLA Prefill into the DSA Backend
- [#31302](https://github.com/sgl-project/sglang/pull/31302) Fix issues about npu docs found by aidd
- [#31456](https://github.com/sgl-project/sglang/pull/31456) Fix modelslim quant tensor name on NPU
- [#29131](https://github.com/sgl-project/sglang/pull/29131) Adapt MiMo-V2.5-W8A8 on NPU
- [#31825](https://github.com/sgl-project/sglang/pull/31825) Support NVFP4_AWQ checkpoints in ModelOpt FP4 path
- [#31748](https://github.com/sgl-project/sglang/pull/31748) Lower AutoRound quantization MMLU threshold
- [#31772](https://github.com/sgl-project/sglang/pull/31772) Fix LLaDA2 MoE OOM after the FRACTAL_NZ cast on NPU
- [#31707](https://github.com/sgl-project/sglang/pull/31707) Bugfix for W4A8MoE bias 3D dimension mismatch problem on NPU
- [#32113](https://github.com/sgl-project/sglang/pull/32113) Fix w4a8 MoE performance degradation on NPU
- [#31762](https://github.com/sgl-project/sglang/pull/31762) Only apply routed_scaling_factor in moe_sum_reduce for marlin_nvfp4
- [#31669](https://github.com/sgl-project/sglang/pull/31669) Add SM120 scatter fallback
- [#31608](https://github.com/sgl-project/sglang/pull/31608) Guard TMA down path for LoRA hooks
- [#31961](https://github.com/sgl-project/sglang/pull/31961) Change the FP8 per-tensor GEMM backend on SM120 to cuBLAS
- [#30940](https://github.com/sgl-project/sglang/pull/30940) Gate TP4 o_proj/qkv CK block-FP8 GEMM shapes to Triton on AMD
- [#31889](https://github.com/sgl-project/sglang/pull/31889) Cache AITER expert mask across decode on AMD
- [#32040](https://github.com/sgl-project/sglang/pull/32040) Ascend fuseep use moe ep group on NPU
- [#31782](https://github.com/sgl-project/sglang/pull/31782) Fix startup bug in olmoe 1b 7b on NPU
- [#32049](https://github.com/sgl-project/sglang/pull/32049) Fix Marlin MoE test ServerArgs initialization
- [#31888](https://github.com/sgl-project/sglang/pull/31888) Q8KV8 FP8 Sparse Prefill on GLM-5.2 & DeepSeek-V3.2
- [#31882](https://github.com/sgl-project/sglang/pull/31882) Add clean BF16 SGL LoRA MoE execution slice
- [#31712](https://github.com/sgl-project/sglang/pull/31712) Add fused activation + FP8 quantization JIT kernel for Triton MoE path
- [#32058](https://github.com/sgl-project/sglang/pull/32058) Add fused SiLU+clamp+mul+FP8 quant AOT kernel for DeepSeek V4 EP MoE path
- [#32155](https://github.com/sgl-project/sglang/pull/32155) Add W8A8 MXFP8 quantization support for Qwen3.5 on Ascend NPU
- [#31791](https://github.com/sgl-project/sglang/pull/31791) Add SM90 MXFP8 Inference Support with DeepGEMM for MiniMax-M3
- [#32033](https://github.com/sgl-project/sglang/pull/32033) Support native W4AFP8 checkpoint schemas
- [#32119](https://github.com/sgl-project/sglang/pull/32119) Add SM12x b12x NVFP4 MoE support in FlashInfer
- [#31836](https://github.com/sgl-project/sglang/pull/31836) Add single-token fused Triton fast path for MoE decode
- [#32120](https://github.com/sgl-project/sglang/pull/32120) Add GLM-5.2 MXFP4 1P1D DI/CI recipes
- [#32173](https://github.com/sgl-project/sglang/pull/32173) Support static W4A8 FP8 activation quantization for MoE
- [#32116](https://github.com/sgl-project/sglang/pull/32116) Add Kimi-K2.6 wide-EP16 2P1D nightly recipes
- [#31994](https://github.com/sgl-project/sglang/pull/31994) Add MoRI EP decode small cap

</details>

<details>
<summary>Model support (15)</summary>

- [#31918](https://github.com/sgl-project/sglang/pull/31918) Add Laguna-S-2.1 to Cookbook
- [#28671](https://github.com/sgl-project/sglang/pull/28671) AutoWeightLoader support Sglang native models 1: demo
- [#31769](https://github.com/sgl-project/sglang/pull/31769) Fix Cohere2MoeConfig import crash from huggingface_hub strict
- [#31837](https://github.com/sgl-project/sglang/pull/31837) Fix MiniMax-M3 crash on ROCm by making its override fields resolvable
- [#31663](https://github.com/sgl-project/sglang/pull/31663) Place empty Qwen encoder-DP embeddings on the communication device
- [#31675](https://github.com/sgl-project/sglang/pull/31675) Fix DeepSeek MLA prefill shape mismatch on HIP eager fallback
- [#31713](https://github.com/sgl-project/sglang/pull/31713) Add DeepSeek V4 SWA recompute
- [#31781](https://github.com/sgl-project/sglang/pull/31781) Support DeepSeek V4 with FlexKV
- [#31722](https://github.com/sgl-project/sglang/pull/31722) Enable MTP/spec decoding with HiSparse on DSV4 unified-KV
- [#32151](https://github.com/sgl-project/sglang/pull/32151) Add support for Nanbeige4.2
- [#31768](https://github.com/sgl-project/sglang/pull/31768) Add LLaDA2.2 Block Routing MoE support
- [#32102](https://github.com/sgl-project/sglang/pull/32102) Add Gemma 4 E2B text generation with native caches on MLX
- [#31840](https://github.com/sgl-project/sglang/pull/31840) Add minimal DFLASH support for Inkling
- [#31956](https://github.com/sgl-project/sglang/pull/31956) Optimize MiniMax-M2.7 on CPU
- [#32027](https://github.com/sgl-project/sglang/pull/32027) Fix DeepSeek tool-call parser dropping valid calls

</details>

<details>
<summary>Parallelism & scheduling (30)</summary>

- [#31835](https://github.com/sgl-project/sglang/pull/31835) Negotiate PrefillDelayer only after KV-budget admission checks
- [#31443](https://github.com/sgl-project/sglang/pull/31443) Optimize hybrid/DSA L3 prefetch result sync and usable-prefix clamping
- [#31687](https://github.com/sgl-project/sglang/pull/31687) Move the WAR barrier to right after each `run_batch` launch
- [#29353](https://github.com/sgl-project/sglang/pull/29353) Add `SGLANG_FORCE_COARSE_WAR_BARRIER` opt-in for a whole-forward WAR barrier
- [#31746](https://github.com/sgl-project/sglang/pull/31746) Release hierarchical cache host pool on graceful shutdown
- [#31871](https://github.com/sgl-project/sglang/pull/31871) Graceful teardown in kl_mamba hicache tests to release pinned host pool
- [#31971](https://github.com/sgl-project/sglang/pull/31971) Gate Mamba slot-donation debug asserts behind SGLANG_MAMBA_DEBUG_ASSERTS
- [#31982](https://github.com/sgl-project/sglang/pull/31982) Gate Mamba slot-donation debug asserts behind SGLANG_MAMBA_DEBUG_ASSERTS
- [#31880](https://github.com/sgl-project/sglang/pull/31880) Fix garbled characters illusion problems in prefix cache mtp scenarios on NPU
- [#31308](https://github.com/sgl-project/sglang/pull/31308) Remove redundant parameters of build_xxx_stack in HiCache
- [#27877](https://github.com/sgl-project/sglang/pull/27877) Reuse block KV/req slots in place across FDFO rounds
- [#30986](https://github.com/sgl-project/sglang/pull/30986) Fix mamba state corruption and slot leak when load_back aborts
- [#31887](https://github.com/sgl-project/sglang/pull/31887) Add durable L3 prefetch checkpoints in HiCache
- [#32177](https://github.com/sgl-project/sglang/pull/32177) Prototype live P-to-D token handoff for disaggregation
- [#32042](https://github.com/sgl-project/sglang/pull/32042) Restore disaggregated decode overlap with resource leases
- [#31767](https://github.com/sgl-project/sglang/pull/31767) Finalize queued streaming-session turns on abort
- [#31716](https://github.com/sgl-project/sglang/pull/31716) Add a ctx axis to the adaptive spec _route
- [#31798](https://github.com/sgl-project/sglang/pull/31798) Make decode queue consensus authoritative
- [#31715](https://github.com/sgl-project/sglang/pull/31715) Make device eviction sync-free in hicache
- [#31750](https://github.com/sgl-project/sglang/pull/31750) Add per-position speculative acceptance metrics
- [#31883](https://github.com/sgl-project/sglang/pull/31883) Restore per-tier KV cache hit metrics in hicache
- [#31902](https://github.com/sgl-project/sglang/pull/31902) Drop prefetched host refill under an un-backed-up parent in UnifiedTree
- [#32052](https://github.com/sgl-project/sglang/pull/32052) Fix hybrid recurrent-state commit for radix cache
- [#31845](https://github.com/sgl-project/sglang/pull/31845) Write-back policy fix for unified tree
- [#32080](https://github.com/sgl-project/sglang/pull/32080) Add cache-agnostic in-batch prefix defer baseline
- [#31758](https://github.com/sgl-project/sglang/pull/31758) Align KV cache eviction priority direction with scheduler
- [#31866](https://github.com/sgl-project/sglang/pull/31866) Validate logit bias before scheduling
- [#31710](https://github.com/sgl-project/sglang/pull/31710) Allow runtime schedule_policy switching via /set_internal_state
- [#31780](https://github.com/sgl-project/sglang/pull/31780) Fix mamba mem_cache tests on non-CUDA (XPU) devices
- [#31698](https://github.com/sgl-project/sglang/pull/31698) Reuse per-step cuda events uniformly

</details>

<details>
<summary>Hardware & arch (14)</summary>

- [#32043](https://github.com/sgl-project/sglang/pull/32043) GFX1250 ROCm bringup: infra, build, kernels and models
- [#30246](https://github.com/sgl-project/sglang/pull/30246) Add 8 XPU nightly tests, enable 1-gpu suite
- [#30273](https://github.com/sgl-project/sglang/pull/30273) Enable breakable prefill CUDA graph on XPU
- [#31654](https://github.com/sgl-project/sglang/pull/31654) Clean up prefill CUDA graph runner
- [#31764](https://github.com/sgl-project/sglang/pull/31764) Temporarily disable GB300 jobs
- [#32069](https://github.com/sgl-project/sglang/pull/32069) Register the Helios release workflow on main for AMD
- [#32055](https://github.com/sgl-project/sglang/pull/32055) Fix ROCm 7.15 Helios image release
- [#31757](https://github.com/sgl-project/sglang/pull/31757) Build Miles nightly ROCm images with docker/build.py and test ROCm 7.2
- [#31919](https://github.com/sgl-project/sglang/pull/31919) Fix CUDA import on non-CUDA platforms
- [#31649](https://github.com/sgl-project/sglang/pull/31649) Enable GPT-OSS TinyGEMM on CUDA 13
- [#32142](https://github.com/sgl-project/sglang/pull/32142) Update ROCM version to 7.15.0a20260712
- [#32092](https://github.com/sgl-project/sglang/pull/32092) Add experimental gfx1201 inference support on AMD
- [#31949](https://github.com/sgl-project/sglang/pull/31949) Add Intel XPU Platform support
- [#31948](https://github.com/sgl-project/sglang/pull/31948) Enable automatic ascend_attn selection for vision attention and graph runners on NPU

</details>

<details>
<summary>API & serving (25)</summary>

- [#31814](https://github.com/sgl-project/sglang/pull/31814) Read resolved config via namespace accessors
- [#31809](https://github.com/sgl-project/sglang/pull/31809) Annotate ServerArgs fields with their runtime-config namespace
- [#31812](https://github.com/sgl-project/sglang/pull/31812) Route runtime config adjustments through the namespace bags
- [#31810](https://github.com/sgl-project/sglang/pull/31810) Add resolved-config namespace bags and accessors
- [#31816](https://github.com/sgl-project/sglang/pull/31816) Read parallel config leaves via get_parallel()
- [#31076](https://github.com/sgl-project/sglang/pull/31076) Add native gRPC sidecar module launcher
- [#32074](https://github.com/sgl-project/sglang/pull/32074) Cherry-pick native gRPC sidecar module launcher
- [#31811](https://github.com/sgl-project/sglang/pull/31811) Make ServerArgs read-only with a single audited mutation entry
- [#31784](https://github.com/sgl-project/sglang/pull/31784) Align reasoning_effort schema across chat, tokenize, and responses
- [#31815](https://github.com/sgl-project/sglang/pull/31815) Load-time declarations write the config bags
- [#32137](https://github.com/sgl-project/sglang/pull/32137) Read resolved config via RuntimeContext namespace accessors (re-land)
- [#32121](https://github.com/sgl-project/sglang/pull/32121) Add typed multi-choice generation via gRPC
- [#31726](https://github.com/sgl-project/sglang/pull/31726) Add build_app/init_app_state factory for embedding the OpenAI server in external ASGI hosts
- [#31964](https://github.com/sgl-project/sglang/pull/31964) Per-pod HTTP and bootstrap port overrides for hostNetwork PD co-location
- [#31960](https://github.com/sgl-project/sglang/pull/31960) Optional base64 encoding for the flat prompt top logprob arrays
- [#32078](https://github.com/sgl-project/sglang/pull/32078) Opt-in flat response format for prompt top logprobs
- [#31907](https://github.com/sgl-project/sglang/pull/31907) Fix concurrency limiter token leaks and lost wakeups
- [#31933](https://github.com/sgl-project/sglang/pull/31933) Add PD circuit-breaker fail-fast regression tests
- [#31723](https://github.com/sgl-project/sglang/pull/31723) Add anti-starvation aging to the lpm schedule policy
- [#31724](https://github.com/sgl-project/sglang/pull/31724) Reject dynamic LoRA updates with tokenizer-worker-num > 1
- [#31808](https://github.com/sgl-project/sglang/pull/31808) Fix LoRA usage-counter accounting across request lifecycle paths
- [#31911](https://github.com/sgl-project/sglang/pull/31911) Support stream output for tools in qwen3.5
- [#32167](https://github.com/sgl-project/sglang/pull/32167) Fix streaming tool calls losing arguments when completed in the final delta
- [#32085](https://github.com/sgl-project/sglang/pull/32085) Bound the grammar-compile thread pool and expose SGLANG_GRAMMAR_COMPILE_MAX_WORKERS
- [#32107](https://github.com/sgl-project/sglang/pull/32107) Fix ReDoS in PythonicDetector's tool-call locator regex

</details>

<details>
<summary>Speculative decoding (15)</summary>

- [#28695](https://github.com/sgl-project/sglang/pull/28695) Support ReplaySSM Ring Spec-Verify
- [#30437](https://github.com/sgl-project/sglang/pull/30437) Support speculative decoding with extra_buffer_lazy in Mamba
- [#31488](https://github.com/sgl-project/sglang/pull/31488) Overlap grammar (constrained decoding) with speculative decode verify
- [#32110](https://github.com/sgl-project/sglang/pull/32110) Enable grammar overlap scheduling for STANDALONE speculative decoding
- [#31738](https://github.com/sgl-project/sglang/pull/31738) Fix stop boundaries for grammar-constrained speculative decoding
- [#31677](https://github.com/sgl-project/sglang/pull/31677) Extract DFlash compact draft-cache rebuild helpers
- [#32023](https://github.com/sgl-project/sglang/pull/32023) Enable decode retraction ordering under speculative decoding
- [#31273](https://github.com/sgl-project/sglang/pull/31273) Fix no-padding CUDA graph admission
- [#31785](https://github.com/sgl-project/sglang/pull/31785) Speculative decoding × decode context parallelism (DFlash/EAGLE)
- [#31830](https://github.com/sgl-project/sglang/pull/31830) Decoupled enumeration transport + IPC threads
- [#32053](https://github.com/sgl-project/sglang/pull/32053) Add configurable target verify budget for DFlash V2
- [#31753](https://github.com/sgl-project/sglang/pull/31753) Grammar-constrained decoding, incl. tool_choice=auto for DSPARK
- [#31807](https://github.com/sgl-project/sglang/pull/31807) Use device-agnostic module for cache cleanup in draft weight sharing
- [#32082](https://github.com/sgl-project/sglang/pull/32082) Fix speculative draft load format resolution
- [#32060](https://github.com/sgl-project/sglang/pull/32060) Avoid oversized speculative verify-mask fill in DeepSeek V4

</details>

<details>
<summary>Multimodal & Diffusion (12)</summary>

- [#31438](https://github.com/sgl-project/sglang/pull/31438) Parallelize multimodal preprocessing with customized worker num
- [#31875](https://github.com/sgl-project/sglang/pull/31875) Add ViT patch-based admission control for multimodal requests
- [#31298](https://github.com/sgl-project/sglang/pull/31298) Warm up Kimi VLM vision encoder at startup
- [#31565](https://github.com/sgl-project/sglang/pull/31565) Msgpack raw-bytes transport for Diffusion
- [#31263](https://github.com/sgl-project/sglang/pull/31263) Run weight update under torch.inference_mode() for diffusion post_training
- [#31873](https://github.com/sgl-project/sglang/pull/31873) Create empty vision embeddings on model device
- [#31832](https://github.com/sgl-project/sglang/pull/31832) Decode input_audio media containers with PyAV
- [#31921](https://github.com/sgl-project/sglang/pull/31921) Add optional realtime TAEHV decode
- [#31852](https://github.com/sgl-project/sglang/pull/31852) Full-forward CUDA graph for the DiT (opt-in)
- [#31857](https://github.com/sgl-project/sglang/pull/31857) Bound audio embedding memory for Inkling
- [#31914](https://github.com/sgl-project/sglang/pull/31914) Validate multimodal embedding hidden size before scatter
- [#32104](https://github.com/sgl-project/sglang/pull/32104) Fix Kimi-VL 2D encoder grids

</details>

<details>
<summary>Disaggregation & Distributed (20)</summary>

- [#27894](https://github.com/sgl-project/sglang/pull/27894) Add NIXL disaggregation functional tests
- [#30913](https://github.com/sgl-project/sglang/pull/30913) Support upsert when loading adapters from tensors/distributed
- [#32108](https://github.com/sgl-project/sglang/pull/32108) Cherry-pick sampling mask support to sglang-miles
- [#30912](https://github.com/sgl-project/sglang/pull/30912) Support aborting requests by rid prefix for multi-lora needs
- [#31733](https://github.com/sgl-project/sglang/pull/31733) Unify logprob results into a single `LogprobResult` and rename chunk env vars
- [#31576](https://github.com/sgl-project/sglang/pull/31576) Make encoder register/unregister health-check robust
- [#31708](https://github.com/sgl-project/sglang/pull/31708) Centralize Mooncake PG configuration
- [#31831](https://github.com/sgl-project/sglang/pull/31831) Add expected_checksums verification to load_lora_adapter_from_tensors
- [#32029](https://github.com/sgl-project/sglang/pull/32029) Unify pinned host pool release on graceful shutdown
- [#31325](https://github.com/sgl-project/sglang/pull/31325) Handle numpy arrays in cross-role transfer field extraction for disagg
- [#31759](https://github.com/sgl-project/sglang/pull/31759) Serialize LoRAUpdateOutput via msgspec_to_builtins on the from_distributed route
- [#32162](https://github.com/sgl-project/sglang/pull/32162) Support hisparse multi-step swap io kernel
- [#31922](https://github.com/sgl-project/sglang/pull/31922) Prevent outbound ZMQ endpoint cache FD exhaustion
- [#31966](https://github.com/sgl-project/sglang/pull/31966) Harden PD receiver threads against malformed messages
- [#32147](https://github.com/sgl-project/sglang/pull/32147) Report KV transfer latency metric and set KVPoll.Transferring in Mooncake
- [#31744](https://github.com/sgl-project/sglang/pull/31744) Fix recovery lifecycle and add manual coverage for Elastic EP
- [#31926](https://github.com/sgl-project/sglang/pull/31926) Fix silent SSD offload corruption when TP/PP ranks share ssd_offload_path
- [#31776](https://github.com/sgl-project/sglang/pull/31776) Pool early-send CUDA events to bound HSA signals
- [#31877](https://github.com/sgl-project/sglang/pull/31877) Track true end-to-end KV transfer latency + per-chunk avg bandwidth
- [#31968](https://github.com/sgl-project/sglang/pull/31968) Fix heterogeneous attn-TP KV transfer for replicated GQA heads

</details>

<details>
<summary>Tests, CI & build (36)</summary>

- [#31941](https://github.com/sgl-project/sglang/pull/31941) Remove obsolete auto-benchmark remnants
- [#30280](https://github.com/sgl-project/sglang/pull/30280) Delete sgl-kernel AOT router GEMM and fused A GEMM
- [#32100](https://github.com/sgl-project/sglang/pull/32100) Revert RuntimeContext config-namespace reads/roles
- [#32191](https://github.com/sgl-project/sglang/pull/32191) Rebase to v0.5.15.post1 for internal testing
- [#32095](https://github.com/sgl-project/sglang/pull/32095) Add Inkling per-commit server test
- [#31983](https://github.com/sgl-project/sglang/pull/31983) Point diffusion CI writes to sgl-project/ci-data-diffusion
- [#31927](https://github.com/sgl-project/sglang/pull/31927) Bump FlashInfer to 0.6.15.post1
- [#31950](https://github.com/sgl-project/sglang/pull/31950) Add OrangeRedeng and Alisehen to CI_PERMISSIONS.json
- [#31717](https://github.com/sgl-project/sglang/pull/31717) Add houseroad to CI_PERMISSIONS.json
- [#31980](https://github.com/sgl-project/sglang/pull/31980) Add wangfakang to CI_PERMISSIONS.json
- [#32091](https://github.com/sgl-project/sglang/pull/32091) Fix failures on main
- [#32193](https://github.com/sgl-project/sglang/pull/32193) Skip sm120 deepgemm test temporarily
- [#31615](https://github.com/sgl-project/sglang/pull/31615) Register newly-added JIT kernel benchmarks for jit-kernel-benchmark-test-amd
- [#31792](https://github.com/sgl-project/sglang/pull/31792) Split ROCm 7.2 Stage-B large 1-GPU tests into three partitions
- [#32054](https://github.com/sgl-project/sglang/pull/32054) Use variable to specify repo and branch location
- [#32011](https://github.com/sgl-project/sglang/pull/32011) Shift nightly image build & pipeline schedule ahead by 2 hours
- [#31841](https://github.com/sgl-project/sglang/pull/31841) Add sm120 tests to DeepGemm release pipeline
- [#31702](https://github.com/sgl-project/sglang/pull/31702) Lower VL PP gsm8k threshold to 0.60
- [#31749](https://github.com/sgl-project/sglang/pull/31749) Run nvidia nightly every 2 days at 14:00 UTC
- [#31916](https://github.com/sgl-project/sglang/pull/31916) Update FLA directory in CODEOWNERS
- [#32174](https://github.com/sgl-project/sglang/pull/32174) Correct runner for testing deepgemm
- [#31735](https://github.com/sgl-project/sglang/pull/31735) Update CI test est_time values
- [#31906](https://github.com/sgl-project/sglang/pull/31906) Reuse PR test stages and throttle matrix fanout on AMD
- [#32014](https://github.com/sgl-project/sglang/pull/32014) Create rust workspace
- [#31952](https://github.com/sgl-project/sglang/pull/31952) Add pr tests
- [#32164](https://github.com/sgl-project/sglang/pull/32164) Add CPU coverage for video decoder backends
- [#32003](https://github.com/sgl-project/sglang/pull/32003) Route scheduled jobs to MI300 with model cache on AMD
- [#31846](https://github.com/sgl-project/sglang/pull/31846) Quarantine pre-existing nested unit failures + enable remainder on AMD
- [#31844](https://github.com/sgl-project/sglang/pull/31844) Enable nested unit tests behind LAPACK/msgpack env skips on AMD
- [#31843](https://github.com/sgl-project/sglang/pull/31843) Enable nested unit tests needing harness stub fixes on AMD
- [#31829](https://github.com/sgl-project/sglang/pull/31829) Harden AITER rebuild so a bad commit can't wipe out aiter
- [#31872](https://github.com/sgl-project/sglang/pull/31872) Cover CUDA arch-suffix defaulting in JIT tests
- [#32136](https://github.com/sgl-project/sglang/pull/32136) Add XPU topk_transform ut
- [#32154](https://github.com/sgl-project/sglang/pull/32154) Add CPU coverage for async invariant probes
- [#31990](https://github.com/sgl-project/sglang/pull/31990) Add unit tests for mem_cache/common helpers
- [#31789](https://github.com/sgl-project/sglang/pull/31789) Add kernel io-backend end-to-end test for mamba HiCache

</details>

<details>
<summary>Docs (6)</summary>

- [#31363](https://github.com/sgl-project/sglang/pull/31363) Re-benchmark DeepSeek-V4 on sglang 0.5.15
- [#32127](https://github.com/sgl-project/sglang/pull/32127) Sync LMSYS SGLang blog cards
- [#31823](https://github.com/sgl-project/sglang/pull/31823) Add measured accuracy numbers to benchmark cards for Inkling
- [#31998](https://github.com/sgl-project/sglang/pull/31998) Rename A5 product name
- [#31734](https://github.com/sgl-project/sglang/pull/31734) Propose commit-gated PD optimistic prefill
- [#32123](https://github.com/sgl-project/sglang/pull/32123) Rename docs_new/ to docs/

</details>

<details>
<summary>Bugfixes (24)</summary>

- [#31962](https://github.com/sgl-project/sglang/pull/31962) Fix flush_cache() no-op after pause_generation in retract
- [#31860](https://github.com/sgl-project/sglang/pull/31860) Fix dropped tool calls when a stream delta carries several
- [#32016](https://github.com/sgl-project/sglang/pull/32016) Evict only the KV shortfall in evict_from_tree_cache
- [#31754](https://github.com/sgl-project/sglang/pull/31754) Fix unnecessary gather/scatter on CPU for non-contiguous Mamba statepool
- [#31988](https://github.com/sgl-project/sglang/pull/31988) Fix reward/classification models broken by `load_weights` v2 dispatch
- [#31701](https://github.com/sgl-project/sglang/pull/31701) Fix vit graph tnd cu seqlens on NPU
- [#31312](https://github.com/sgl-project/sglang/pull/31312) Fix LongCat n-gram token-table crashes on padded batches
- [#31787](https://github.com/sgl-project/sglang/pull/31787) Fix dropped Inkling reasoning at stream end
- [#32047](https://github.com/sgl-project/sglang/pull/32047) Fix stale per-token group quant callers
- [#31334](https://github.com/sgl-project/sglang/pull/31334) Fix mxfp4 padding size on CPU
- [#31705](https://github.com/sgl-project/sglang/pull/31705) Fix idle-rank dummy-extend sparse-prefill crash under DP breakable CUDA graph
- [#32096](https://github.com/sgl-project/sglang/pull/32096) Fix get_server_args import lint error
- [#31942](https://github.com/sgl-project/sglang/pull/31942) Fix extra_buffer_lazy guard bypass
- [#31541](https://github.com/sgl-project/sglang/pull/31541) Bug fix in compress to support XPU
- [#32070](https://github.com/sgl-project/sglang/pull/32070) Use per-DP-rank loads for power-of-two routing in gateway
- [#31771](https://github.com/sgl-project/sglang/pull/31771) Fix hybrid-SWA HiCache load-back
- [#31725](https://github.com/sgl-project/sglang/pull/31725) Avoid cross-node JIT build races on shared NFS caches
- [#31909](https://github.com/sgl-project/sglang/pull/31909) Only export request gauges on attn CP rank 0
- [#32181](https://github.com/sgl-project/sglang/pull/32181) Fix trtllm_mla backend + fp8 kv cache without rope
- [#31937](https://github.com/sgl-project/sglang/pull/31937) Call post_load_weights on direct/custom weight-update paths
- [#32087](https://github.com/sgl-project/sglang/pull/32087) Fix Triton SWA decode window dropping the oldest in-window key
- [#31728](https://github.com/sgl-project/sglang/pull/31728) Truncate xgrammar accepted_tokens in place on rollback
- [#31892](https://github.com/sgl-project/sglang/pull/31892) Fix multi-tokenizer BatchEmbeddingOutput repack dropping fields
- [#31691](https://github.com/sgl-project/sglang/pull/31691) Validate Manifest.from_dict inputs in model_file_verifier

</details>

<details>
<summary>Refactors (10)</summary>

- [#31666](https://github.com/sgl-project/sglang/pull/31666) Phase 3+4: move JIT infra + operator groups into sglang.kernels
- [#32072](https://github.com/sgl-project/sglang/pull/32072) RFC #29630 finale: retire sglang.jit_kernel into sglang.kernels
- [#32148](https://github.com/sgl-project/sglang/pull/32148) Classification cleanup: unify _jit_ naming, drop empty/model groups, add elementwise
- [#32015](https://github.com/sgl-project/sglang/pull/32015) Phase 4 batch-2: migrate JIT operator groups into kernels.ops
- [#32128](https://github.com/sgl-project/sglang/pull/32128) Reclassify kernel tests by ops group + move helpers out of the package
- [#31655](https://github.com/sgl-project/sglang/pull/31655) Unify input logprob processing on a single chunked path
- [#31897](https://github.com/sgl-project/sglang/pull/31897) Refactor rope kernels on CPU
- [#31736](https://github.com/sgl-project/sglang/pull/31736) Localize VLM deepstack warmup to tc backend
- [#32186](https://github.com/sgl-project/sglang/pull/32186) Reduce DSpark import side effects
- [#32073](https://github.com/sgl-project/sglang/pull/32073) Revert Ascend MoE implementation refactor to fix issues

</details>

<details>
<summary>Other (11)</summary>

- [#31819](https://github.com/sgl-project/sglang/pull/31819) Revert MiniMax-M3 to dev image in cookbook
- [#32076](https://github.com/sgl-project/sglang/pull/32076) Fix Inkling kernel imports after migration
- [#31230](https://github.com/sgl-project/sglang/pull/31230) Add a per-path cap for cached states in Mamba
- [#30938](https://github.com/sgl-project/sglang/pull/30938) Warn on small Mamba chunked prefill size
- [#27127](https://github.com/sgl-project/sglang/pull/27127) Use sgl_kernel_npu rmsrope accelerate llada2
- [#13397](https://github.com/sgl-project/sglang/pull/13397) Add kernel for shm_allgather_into_tensor and shm_reduce_scatter_tensor on CPU
- [#31939](https://github.com/sgl-project/sglang/pull/31939) Add Inkling to nightly test
- [#15912](https://github.com/sgl-project/sglang/pull/15912) Update ascend LoRA backend to support new kernels
- [#31863](https://github.com/sgl-project/sglang/pull/31863) Remove duplicate code in NPU attention
- [#31874](https://github.com/sgl-project/sglang/pull/31874) Fix rl update weights 'Parameter' object has no attribute 'weight_LOADER'
- [#31796](https://github.com/sgl-project/sglang/pull/31796) Fix rl update weights 'Parameter' object has no attribute 'weight_LOADER'

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 9866a5ba508898eae6f50c46fcf9b0f84cdafe9fb4080532453c13c7ec1719af -->
