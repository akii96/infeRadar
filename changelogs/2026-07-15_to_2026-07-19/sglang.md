# sglang: PR digest (2026-07-15 to 2026-07-19)

_224 merged, 292 newly opened - source sgl-project/sglang, generated 2026-07-19T22:11:22Z_

## TL;DR
- **DeepSeek & GLM Dominate**: DeepSeek (V4/V3.2) and GLM (5.2) received the most attention, with major optimizations for MLA (Multi-Head Latent Attention), MoE routing, and speculative decoding (MTP/EAGLE).
- **Next-Gen Quantization**: Significant push for FP4, NVFP4, and MXFP4 quantization formats, including SM120 (Blackwell) FP4 KV cache support and MegaMoE FlashInfer integration.
- **Inkling Model Family**: Massive in-progress work (~57k LOC) to support the new "Inkling" model family across attention, MoE, multimodal, and speculative decoding paths.
- **Kernel Architecture**: Continued execution of the RFC #29630 kernel decoupling, migrating DSA, DSV4, JIT ops, and diffusion kernels into the unified `sglang.kernels` namespace.
- **Distributed & Scheduling**: Major enhancements to distributed execution, including runtime Elastic EP scale-up, CP-v2 zigzag context parallelism, and sync-free HiCache memory management.

## Most important PRs
- **[#31358](https://github.com/sgl-project/sglang/pull/31358)** Introduces massive foundational support for the Inkling model family across all major components (attention, MoE, multimodal, speculative decoding), representing over 57k lines of newly opened code.
- **[#30164](https://github.com/sgl-project/sglang/pull/30164)** Implements runtime scale-up for Elastic Expert Parallelism (EP), allowing dynamic adjustment of MoE distributed execution without restarting the cluster.
- **[#21601](https://github.com/sgl-project/sglang/pull/21601)** Adds FP4 KV cache support targeting upcoming NVIDIA SM120 (Blackwell) GPUs, integrating with the FlashInfer backend for next-generation memory bandwidth savings.
- **[#25663](https://github.com/sgl-project/sglang/pull/25663)** Refactors the Ascend NPU Mixture-of-Experts (MoE) implementation to align with the community Triton design, significantly reducing code duplication.
- **[#30792](https://github.com/sgl-project/sglang/pull/30792)** Migrates DSA and DeepSeek-V4 attention kernels into the unified `sglang.kernels` namespace, marking a major milestone in the RFC #29630 kernel decoupling effort.

## More changes by area

<details>
<summary>Performance (17)</summary>

- [#31049](https://github.com/sgl-project/sglang/pull/31049) Rewrite JIT custom all-reduce (v2) with decoupled kernel/storage
- [#31227](https://github.com/sgl-project/sglang/pull/31227) Shard Kimi DP image feature transport
- [#31304](https://github.com/sgl-project/sglang/pull/31304) Improve CPU silu performance via rcp14
- [#30947](https://github.com/sgl-project/sglang/pull/30947) Fuse topk=1 draft postprocess for EAGLE
- [#30948](https://github.com/sgl-project/sglang/pull/30948) Fuse TP vocab-parallel embedding for EAGLE
- [#28983](https://github.com/sgl-project/sglang/pull/28983) Enable SGLANG_OPT_FP8_WO_A_GEMM on Hopper for DeepSeek-V4
- [#31472](https://github.com/sgl-project/sglang/pull/31472) Fuse topk=1 target verify finalization
- [#31465](https://github.com/sgl-project/sglang/pull/31465) Fuse draft-extend topk=1 postprocess
- [#31329](https://github.com/sgl-project/sglang/pull/31329) Fuse speculative relay scatter for EAGLE
- [#31341](https://github.com/sgl-project/sglang/pull/31341) Optimize HiSparse small-batch perf with multi-CTA cache sharding
- [#31593](https://github.com/sgl-project/sglang/pull/31593) GPU embedding pool for zmq_to_scheduler to cut H2D/D2H
- [#31479](https://github.com/sgl-project/sglang/pull/31479) Coalesce cache events for kv-events
- [#31434](https://github.com/sgl-project/sglang/pull/31434) Cache uniform ragged-verify layout for DSpark verify-all compact
- [#31558](https://github.com/sgl-project/sglang/pull/31558) Avoid FLA L2-norm recompilation by token count
- [#31284](https://github.com/sgl-project/sglang/pull/31284) Parallelize compute_position prefix-sum for large batch
- [#31587](https://github.com/sgl-project/sglang/pull/31587) Enable CUDA IPC pool handle cache by default
- [#31607](https://github.com/sgl-project/sglang/pull/31607) Fix perf regression of zeroing of TensorRT-LLM MLA workspace
</details>

<details>
<summary>Kernels & attention (26)</summary>

- [#29690](https://github.com/sgl-project/sglang/pull/29690) Fuse preprocess kernels of trtllm-gen attention
- [#30113](https://github.com/sgl-project/sglang/pull/30113) Add FlashInfer SM100 KDA decode + MTP backend
- [#30514](https://github.com/sgl-project/sglang/pull/30514) Integrate Q8KV8 FP8 Sparse MLA Prefill into DSA Backend
- [#31468](https://github.com/sgl-project/sglang/pull/31468) Remove per-step host syncs in DFlash for CPU overlap
- [#29972](https://github.com/sgl-project/sglang/pull/29972) Support MiMo V2.5 with zigzag context parallelism
- [#26852](https://github.com/sgl-project/sglang/pull/26852) Reuse fused FP8 KV cache write on AMD standard aiter prefill/decode
- [#30997](https://github.com/sgl-project/sglang/pull/30997) Fix heterogeneous attn-TP scatter transfer for Qwen3.5
- [#31619](https://github.com/sgl-project/sglang/pull/31619) Migrate MLA prefill CP to CP-v2 zigzag strategy
- [#31090](https://github.com/sgl-project/sglang/pull/31090) Enable sync-free spec via device-side draft-extend in flashmla
- [#31474](https://github.com/sgl-project/sglang/pull/31474) Fix KDA prefix caching under mamba extra_buffer
- [#31391](https://github.com/sgl-project/sglang/pull/31391) Enable Kimi multimodal breakable prefill CUDA graph replay
- [#30365](https://github.com/sgl-project/sglang/pull/30365) Remove per-step seqlen D2H from speculative for DSV4 overlap scheduler
- [#31244](https://github.com/sgl-project/sglang/pull/31244) Converge DP-attention spec width scaling onto num_tokens_per_req
- [#31439](https://github.com/sgl-project/sglang/pull/31439) Wrap split backends once on full-attention backends
- [#31241](https://github.com/sgl-project/sglang/pull/31241) Refine fused A GEMM dispatch
- [#31480](https://github.com/sgl-project/sglang/pull/31480) Add arch-independent torch paged-MQA-logits backend with fused Triton fast path
- [#31446](https://github.com/sgl-project/sglang/pull/31446) Add MHA hisparse support for MiniMax M3
- [#31481](https://github.com/sgl-project/sglang/pull/31481) Enable sparse MLA decode+prefill on SM120/SM121 via flashinfer
- [#31628](https://github.com/sgl-project/sglang/pull/31628) Fuse cuda-graph metadata rebuild into one triton kernel for trtllm_mla
- [#31432](https://github.com/sgl-project/sglang/pull/31432) Add tbo for deepseekv4-hisparse
- [#31247](https://github.com/sgl-project/sglang/pull/31247) Integrate embedding KV-cache-skip fast path into torch_native backend
- [#31560](https://github.com/sgl-project/sglang/pull/31560) Support context parallelism with tensor parallelism
- [#30940](https://github.com/sgl-project/sglang/pull/30940) Gate TP4 o_proj/qkv CK block-FP8 GEMM shapes to Triton
- [#31514](https://github.com/sgl-project/sglang/pull/31514) Decode context parallel for Kimi K2.5 NVFP4
- [#31394](https://github.com/sgl-project/sglang/pull/31394) TRTLLMHAAttnBackend inherits from AttentionBackend
- [#31246](https://github.com/sgl-project/sglang/pull/31246) Run torch.compile sum-reduce under no_grad
</details>

<details>
<summary>MoE & quantization (27)</summary>

- [#31109](https://github.com/sgl-project/sglang/pull/31109) Remove QServe and FBGEMM FP8 quantization
- [#30272](https://github.com/sgl-project/sglang/pull/30272) Implement SM120 DeepSeek V4 flashinfer_mxfp4 moe runner backend
- [#25763](https://github.com/sgl-project/sglang/pull/25763) Support DeepSeek-V4 Wint4Abf16 and Win4Afp8
- [#23795](https://github.com/sgl-project/sglang/pull/23795) Add W4A4 MXFP4 quantization support for Qwen3 Dense on Ascend NPU
- [#31114](https://github.com/sgl-project/sglang/pull/31114) Push test case scripts from test repo to main upstream
- [#28439](https://github.com/sgl-project/sglang/pull/28439) Use sgl-kernel implementation for V2 Compressor on Intel XPU
- [#30238](https://github.com/sgl-project/sglang/pull/30238) Support two batch overlap with MTP on DeepSeekV4 for AMD
- [#29007](https://github.com/sgl-project/sglang/pull/29007) Fix MoE TP allreduce to use NCCL symmetric memory
- [#28309](https://github.com/sgl-project/sglang/pull/28309) Support Flashinfer one-sided A2A + CuteDSL MoE for Nemotron Ultra
- [#31653](https://github.com/sgl-project/sglang/pull/31653) Fix SM120 NVFP4 KV cache test OOM
- [#31269](https://github.com/sgl-project/sglang/pull/31269) Add SM90 nvfp4 kvcache for Deepseek v4 & GLM-5.2
- [#31470](https://github.com/sgl-project/sglang/pull/31470) Add Mega MoE FlashInfer support
- [#31408](https://github.com/sgl-project/sglang/pull/31408) Support MegaMOE NVFP4 & MXFP8 through FlashInfer
- [#31712](https://github.com/sgl-project/sglang/pull/31712) Add fused activation + FP8 quantization JIT kernel for Triton MoE
- [#31555](https://github.com/sgl-project/sglang/pull/31555) Add W4A16Sparse24 dense-dequant fallback for compressed-tensors int4
- [#31652](https://github.com/sgl-project/sglang/pull/31652) Fuse FP8 KV-cache quantization into the store kernel
- [#31322](https://github.com/sgl-project/sglang/pull/31322) Add FlyDSL MegaMoE backend for DeepSeek MoE on AMD
- [#31282](https://github.com/sgl-project/sglang/pull/31282) Support mixed MXFP8 and NVFP4 modelopt checkpoints
- [#31429](https://github.com/sgl-project/sglang/pull/31429) Enable FP8 DeepEP dispatch for humming MoE backend
- [#31529](https://github.com/sgl-project/sglang/pull/31529) Handle BF16 and FP8 DeepEP dispatch in CUTLASS W4A8 MoE
- [#31330](https://github.com/sgl-project/sglang/pull/31330) Support FP32 NVFP4 global scale in Marlin
- [#30976](https://github.com/sgl-project/sglang/pull/30976) Load right mtp lm head quantization
- [#31449](https://github.com/sgl-project/sglang/pull/31449) Fix/Refactor routed scaling factor application in MoE routing
- [#28428](https://github.com/sgl-project/sglang/pull/28428) Use sgl-kernel implementation of silu_and_mul_clamp
- [#31382](https://github.com/sgl-project/sglang/pull/31382) Support FlashInfer CuTe DSL for online NVFP4 draft MoE
- [#31463](https://github.com/sgl-project/sglang/pull/31463) Support MiniMax-M3 Wint4Abf16 and Win4Afp8 on hopper
- [#31510](https://github.com/sgl-project/sglang/pull/31510) Fix MXFP8 online quantization pipeline
</details>

<details>
<summary>Speculative decoding (22)</summary>

- [#31380](https://github.com/sgl-project/sglang/pull/31380) Consolidate verify step into eagle_worker_common
- [#31257](https://github.com/sgl-project/sglang/pull/31257) Extract stateless draft prepare helpers
- [#31013](https://github.com/sgl-project/sglang/pull/31013) Single-source num_tokens_per_req derivation
- [#31255](https://github.com/sgl-project/sglang/pull/31255) Split capture width from num_tokens_per_req and gate replay
- [#31078](https://github.com/sgl-project/sglang/pull/31078) Consolidate spec-worker weight updates into BaseSpecWorker
- [#31294](https://github.com/sgl-project/sglang/pull/31294) Skip no-op EAGLE sampling renormalization
- [#31527](https://github.com/sgl-project/sglang/pull/31527) Allocate verify tree-mask scratch on target backend only
- [#31364](https://github.com/sgl-project/sglang/pull/31364) Enable sync-free eagle spec via fixed-window draft-extend metadata
- [#31381](https://github.com/sgl-project/sglang/pull/31381) Build topk>1 verify replay page table on-device for fa3
- [#31497](https://github.com/sgl-project/sglang/pull/31497) Add JIT fused top-k/top-p renorm for EAGLE verify
- [#31457](https://github.com/sgl-project/sglang/pull/31457) Enable GLM-5.2 DSpark compact ragged graph on ROCm
- [#31722](https://github.com/sgl-project/sglang/pull/31722) Enable MTP/spec decoding with HiSparse on DSV4 unified-KV for AMD
- [#31683](https://github.com/sgl-project/sglang/pull/31683) Enable GLM-5.2-MXFP4 MTP speculative decoding on ROCm
- [#31422](https://github.com/sgl-project/sglang/pull/31422) Add DSpark compact-verify on DSA backends + sync-free verify-all
- [#31613](https://github.com/sgl-project/sglang/pull/31613) Add decoupled enumeration slot table + GPU landing buffer
- [#31499](https://github.com/sgl-project/sglang/pull/31499) Extract shared forward step and introduce EagleWorkerContext
- [#31716](https://github.com/sgl-project/sglang/pull/31716) Add ctx axis to adaptive spec route
- [#31328](https://github.com/sgl-project/sglang/pull/31328) Add correctness-first Domino support to DFlash V2
- [#31516](https://github.com/sgl-project/sglang/pull/31516) Add adaptive speculative decoding CI coverage
- [#31620](https://github.com/sgl-project/sglang/pull/31620) Replace torch.multinomial with native torch op
- [#31566](https://github.com/sgl-project/sglang/pull/31566) Preserve verify capture mode on idle DP ranks
- [#31616](https://github.com/sgl-project/sglang/pull/31616) Fix page-align EAGLE KV allocation
</details>

<details>
<summary>Parallelism & scheduling (38)</summary>

- [#29432](https://github.com/sgl-project/sglang/pull/29432) Fix bookkeeping fields not encapsulated with real allocations
- [#30182](https://github.com/sgl-project/sglang/pull/30182) Empty _REQ_TYPES_WITH_OPAQUE_FIELDS on msgpack IPC path
- [#19320](https://github.com/sgl-project/sglang/pull/19320) Optimize HiCache L2 mem allocation on L3 miss
- [#30672](https://github.com/sgl-project/sglang/pull/30672) Avoid mutating ScheduleBatch fields in place
- [#30675](https://github.com/sgl-project/sglang/pull/30675) Rewrite pause_generation retract path as req-level release
- [#26411](https://github.com/sgl-project/sglang/pull/26411) Measure load-back duration with CUDA events in HiCache
- [#29428](https://github.com/sgl-project/sglang/pull/29428) Decouple cache backend from owned committed kv details
- [#29427](https://github.com/sgl-project/sglang/pull/29427) Introduce req.kv container for coupled owned kv field lifecycle
- [#22591](https://github.com/sgl-project/sglang/pull/22591) Add SGLANG_MAX_NEW_TOKENS_LIMIT to cap per-request max_new_tokens
- [#30670](https://github.com/sgl-project/sglang/pull/30670) Pass per-forward overrides to ForwardBatch.init_new explicitly
- [#31643](https://github.com/sgl-project/sglang/pull/31643) Reset only used mamba state on radix cache hit
- [#30674](https://github.com/sgl-project/sglang/pull/30674) Fix missed hisparse release and stale field cleanup in pause retract
- [#30669](https://github.com/sgl-project/sglang/pull/30669) Remove dead ScheduleBatch fields and avoid inplace seq_lens bump
- [#30673](https://github.com/sgl-project/sglang/pull/30673) Fix non-existent abort mode in Scheduler.pause_generation
- [#30676](https://github.com/sgl-project/sglang/pull/30676) Avoid implicit running_batch access in dllm and pdmux scheduling
- [#31662](https://github.com/sgl-project/sglang/pull/31662) Respect cache_protected_len in ChunkCache and disabled-radix release paths
- [#31335](https://github.com/sgl-project/sglang/pull/31335) Implement alloc-page-aligned memory management
- [#31466](https://github.com/sgl-project/sglang/pull/31466) Support prefill/decode disaggregation in DSpark
- [#31305](https://github.com/sgl-project/sglang/pull/31305) Add paged LoRA memory pool with page-level eviction
- [#31713](https://github.com/sgl-project/sglang/pull/31713) Add DeepSeek V4 SWA recompute
- [#31626](https://github.com/sgl-project/sglang/pull/31626) Implement Beam search dev branch
- [#31357](https://github.com/sgl-project/sglang/pull/31357) Drain Mooncake transfers before releasing KV pages
- [#31586](https://github.com/sgl-project/sglang/pull/31586) Decouple prefill chunk size from decode block size in dLLM
- [#31664](https://github.com/sgl-project/sglang/pull/31664) Align input limits across heterogeneous prefill/decode workers
- [#31425](https://github.com/sgl-project/sglang/pull/31425) Fix HiCache TP/PP write-through & load-back consensus
- [#31715](https://github.com/sgl-project/sglang/pull/31715) Make HiCache device eviction sync-free
- [#31647](https://github.com/sgl-project/sglang/pull/31647) Fix abort request counter accounting for abort_all
- [#31674](https://github.com/sgl-project/sglang/pull/31674) Preserve speculative draft weights across release/resume_memory_occupation
- [#31488](https://github.com/sgl-project/sglang/pull/31488) Overlap grammar (constrained decoding) with speculative decode verify
- [#31402](https://github.com/sgl-project/sglang/pull/31402) Fix non-blocking HiCache storage prefetch misses
- [#31687](https://github.com/sgl-project/sglang/pull/31687) Move WAR barrier to right after each run_batch launch
- [#30677](https://github.com/sgl-project/sglang/pull/30677) Avoid relaying per-step outputs through ScheduleBatch fields
- [#29353](https://github.com/sgl-project/sglang/pull/29353) Add SGLANG_FORCE_COARSE_WAR_BARRIER opt-in
- [#31517](https://github.com/sgl-project/sglang/pull/31517) Publish idle scheduler metrics immediately
- [#31321](https://github.com/sgl-project/sglang/pull/31321) Release Mamba cache after PP dynamic chunk profiling
- [#31708](https://github.com/sgl-project/sglang/pull/31708) Centralize Mooncake PG configuration
- [#31326](https://github.com/sgl-project/sglang/pull/31326) Avoid redundant tensor clones in Mamba radix cache
- [#31427](https://github.com/sgl-project/sglang/pull/31427) Protect HiRadix host KV until load-back ack
</details>

<details>
<summary>Model support (18)</summary>

- [#24013](https://github.com/sgl-project/sglang/pull/24013) Batch cross-request ViT encoding and reuse attention metadata
- [#31027](https://github.com/sgl-project/sglang/pull/31027) Support n>1 outputs for GLM-Image generation
- [#30904](https://github.com/sgl-project/sglang/pull/30904) Unify multimodal feature transport
- [#31029](https://github.com/sgl-project/sglang/pull/31029) Add LoRA IPC weight sync via lora_merge mode for Diffusion
- [#30036](https://github.com/sgl-project/sglang/pull/30036) Support RL rollout for Wan pipeline via per-request scheduler switch
- [#31233](https://github.com/sgl-project/sglang/pull/31233) Opt in Qwen and Wan multi-output conditioning expansion
- [#31354](https://github.com/sgl-project/sglang/pull/31354) Use SGLang server for ERNIE-Image prompt enhancement
- [#31467](https://github.com/sgl-project/sglang/pull/31467) Update baselines for GLM-Image on NPU
- [#31251](https://github.com/sgl-project/sglang/pull/31251) Add lora GLM-5.2 FP8 based model support
- [#31512](https://github.com/sgl-project/sglang/pull/31512) Add nightly test for GLM5.2 LayerSplit
- [#31276](https://github.com/sgl-project/sglang/pull/31276) Support PLaMo3 from Preferred Networks
- [#31491](https://github.com/sgl-project/sglang/pull/31491) Add Spectrum multimodal feature support
- [#31590](https://github.com/sgl-project/sglang/pull/31590) Add Cosmos3 Edge and Distilled checkpoints support
- [#31506](https://github.com/sgl-project/sglang/pull/31506) Decode input_audio media containers with PyAV
- [#31438](https://github.com/sgl-project/sglang/pull/31438) Parallelize multimodal preprocessing with customized worker num
- [#31538](https://github.com/sgl-project/sglang/pull/31538) Support resident layers for DiT diffusion models
- [#31583](https://github.com/sgl-project/sglang/pull/31583) GPU image preprocessing for Kimi-K2.5 on encoder server
- [#31522](https://github.com/sgl-project/sglang/pull/31522) Support GDN in_proj_ba adapters for Qwen3.5
</details>

<details>
<summary>Hardware & arch (26)</summary>

- [#31307](https://github.com/sgl-project/sglang/pull/31307) Fill non-CUDA coverage for HIP and Ascend NPU backends
- [#30547](https://github.com/sgl-project/sglang/pull/30547) Honor --max-running-requests in MLX model runner stub
- [#30651](https://github.com/sgl-project/sglang/pull/30651) Add MORI disagg backend for AMD and bump MI355X image
- [#30688](https://github.com/sgl-project/sglang/pull/30688) Fix MoE functionality on RDNA via Python-level fallback dispatch
- [#30355](https://github.com/sgl-project/sglang/pull/30355) Fix triton attention backend for DeepSeek MLA on MI355
- [#31688](https://github.com/sgl-project/sglang/pull/31688) Fix ROCm fused KV and KDA paths
- [#31038](https://github.com/sgl-project/sglang/pull/31038) Route topk_sigmoid and topk_softmax to AOT sgl-kernel-xpu symbols
- [#31634](https://github.com/sgl-project/sglang/pull/31634) Fix sglang-kernel build for MUSA
- [#31403](https://github.com/sgl-project/sglang/pull/31403) Fix RMSNorm on AMD devices without AITER
- [#31290](https://github.com/sgl-project/sglang/pull/31290) Fix DP-attention reduce_scatterv / all_gatherv on Intel XPU
- [#31342](https://github.com/sgl-project/sglang/pull/31342) Disable CUDA IPC multimodal transport on ROCm
- [#31532](https://github.com/sgl-project/sglang/pull/31532) Auto-disable tc_piecewise and breakable prefill CUDA graphs under DCP
- [#30506](https://github.com/sgl-project/sglang/pull/30506) Disable DSA fused top-k v2 on ROCm
- [#31098](https://github.com/sgl-project/sglang/pull/31098) Don't fail server startup when psutil can't parse /proc/meminfo
- [#29669](https://github.com/sgl-project/sglang/pull/29669) Skip MXFP8 autotune on dense GEMM
- [#31601](https://github.com/sgl-project/sglang/pull/31601) Extract post-memory-pool wiring
- [#30359](https://github.com/sgl-project/sglang/pull/30359) Enable mamba-extra-buffer for Qwen3.5 on ROCm
- [#31580](https://github.com/sgl-project/sglang/pull/31580) Add oot torch profiler activity support
- [#31455](https://github.com/sgl-project/sglang/pull/31455) Bisect target-verify CUDA Graph replay synchronization
- [#31686](https://github.com/sgl-project/sglang/pull/31686) Record WAR read-done event in-graph
- [#31340](https://github.com/sgl-project/sglang/pull/31340) Fix FP8 Triton dtype selection on A100
- [#31727](https://github.com/sgl-project/sglang/pull/31727) Fix DeepSeek-V4 fused-RMS FP8 scale metadata on gfx950
- [#31689](https://github.com/sgl-project/sglang/pull/31689) Avoid batch-size specialization in masked KV writes
- [#31557](https://github.com/sgl-project/sglang/pull/31557) Bound audio embedding memory
- [#31576](https://github.com/sgl-project/sglang/pull/31576) Make encoder register/unregister health-check robust
- [#31421](https://github.com/sgl-project/sglang/pull/31421) Make aiter imports on startup path optional
</details>

<details>
<summary>API & serving (11)</summary>

- [#31272](https://github.com/sgl-project/sglang/pull/31272) Stamp selected worker on dispatch-stage errors via Server-Timing
- [#31530](https://github.com/sgl-project/sglang/pull/31530) Allow extra labels on HTTP request/response Prometheus metrics
- [#31401](https://github.com/sgl-project/sglang/pull/31401) Fix inkling effort rounding and responses API passthrough
- [#31726](https://github.com/sgl-project/sglang/pull/31726) Add build_app/init_app_state factory for embedding OpenAI server in ASGI hosts
- [#31685](https://github.com/sgl-project/sglang/pull/31685) Support /abort_request in sgl-model-gateway
- [#31419](https://github.com/sgl-project/sglang/pull/31419) Return 404 for unknown models on OpenAI-compatible endpoints
- [#31633](https://github.com/sgl-project/sglang/pull/31633) Add sglext output ids field
- [#31461](https://github.com/sgl-project/sglang/pull/31461) Allow max_running_requests to be tuned at runtime via /set_internal_state
- [#31710](https://github.com/sgl-project/sglang/pull/31710) Allow runtime schedule_policy switching via /set_internal_state
- [#31412](https://github.com/sgl-project/sglang/pull/31412) Add token-weighted prefix cache hit rate panel
- [#31389](https://github.com/sgl-project/sglang/pull/31389) Add configurable FlashInfer autotune skips
</details>

<details>
<summary>Refactors (18)</summary>

- [#30838](https://github.com/sgl-project/sglang/pull/30838) Refactor dtype traits into DTypeTrait and unify warp reductions
- [#31546](https://github.com/sgl-project/sglang/pull/31546) Simplify sglang.kernels tests to idiomatic pytest style
- [#31292](https://github.com/sgl-project/sglang/pull/31292) Decouple KernelBackend from device + device-based CapabilityRequirement
- [#30795](https://github.com/sgl-project/sglang/pull/30795) Relocate vendored fla and mamba kernel trees to sglang.kernels
- [#30793](https://github.com/sgl-project/sglang/pull/30793) Migrate linear-attention, MiniMax-sparse and diffusion kernels to sglang.kernels
- [#31624](https://github.com/sgl-project/sglang/pull/31624) Move output logprob processing into logprob_processor layer
- [#31411](https://github.com/sgl-project/sglang/pull/31411) Migrate CP knob to canonical prefill-CP flags
- [#20071](https://github.com/sgl-project/sglang/pull/20071) Refactor logprob processor layer
- [#31582](https://github.com/sgl-project/sglang/pull/31582) Sweep decoupled scattered kernels into sglang.kernels.ops
- [#31559](https://github.com/sgl-project/sglang/pull/31559) Bundle triton_kernels under sglang.third_party
- [#31697](https://github.com/sgl-project/sglang/pull/31697) Move JIT quant ops into kernels.ops.quantization
- [#31531](https://github.com/sgl-project/sglang/pull/31531) Separate ROCm-specific DeepSeek MHA and MLA forward paths
- [#31693](https://github.com/sgl-project/sglang/pull/31693) Move JIT norm ops into kernels.ops.layernorm
- [#31695](https://github.com/sgl-project/sglang/pull/31695) Move JIT dsv3 gemm ops into kernels.ops.gemm
- [#31694](https://github.com/sgl-project/sglang/pull/31694) Move JIT activation ops into kernels.ops.activation
- [#31696](https://github.com/sgl-project/sglang/pull/31696) Move JIT set_mla_kv_buffer into kernels.ops.kvcache
- [#31666](https://github.com/sgl-project/sglang/pull/31666) Move shared JIT infra to sglang.kernels._jit
- [#31453](https://github.com/sgl-project/sglang/pull/31453) Extract complex RoPE implementation to layers/rotary_embedding
</details>

<details>
<summary>Docs (22)</summary>

- [#31360](https://github.com/sgl-project/sglang/pull/31360) Add Inkling cookbook
- [#30109](https://github.com/sgl-project/sglang/pull/30109) Simplify diffusion new model guide
- [#30520](https://github.com/sgl-project/sglang/pull/30520) Update CPU model support info in Cookbook
- [#31610](https://github.com/sgl-project/sglang/pull/31610) Replace pinned nightly/dev images with :latest in cookbook
- [#31242](https://github.com/sgl-project/sglang/pull/31242) Sync LMSYS SGLang blog cards
- [#31386](https://github.com/sgl-project/sglang/pull/31386) Sync LMSYS SGLang blog cards
- [#31550](https://github.com/sgl-project/sglang/pull/31550) Mark B300/GB300 recipes verified in Inkling cookbook
- [#31489](https://github.com/sgl-project/sglang/pull/31489) Remove Inkling H200 LoRA BF16 cookbook command
- [#31316](https://github.com/sgl-project/sglang/pull/31316) Update model names supported on Ascend NPU
- [#31577](https://github.com/sgl-project/sglang/pull/31577) Update GLM5.2 Cookbook with LayerSplit usage
- plus 12 more minor documentation updates
</details>

<details>
<summary>Tests & CI (24)</summary>

- [#31396](https://github.com/sgl-project/sglang/pull/31396) Fix runner utilization report undercounting busy time
- [#31509](https://github.com/sgl-project/sglang/pull/31509) Wait for GPU memory release before each test class setUpClass
- [#31371](https://github.com/sgl-project/sglang/pull/31371) Remove nightly registrations redundant with scheduled stage runs
- [#31484](https://github.com/sgl-project/sglang/pull/31484) Upgrade llguidance to 1.7.6
- [#31204](https://github.com/sgl-project/sglang/pull/31204) Skip unsafe automatic prefill graph capture
- [#31035](https://github.com/sgl-project/sglang/pull/31035) Fix CUDA 12 NVIDIA wheel cleanup
- [#31367](https://github.com/sgl-project/sglang/pull/31367) Stamp capture-time num_tokens_per_req in multi-layer EAGLE
- [#31571](https://github.com/sgl-project/sglang/pull/31571) Exclude current process memory from GPU idle check
- [#31088](https://github.com/sgl-project/sglang/pull/31088) Register CPU-bound / triton unit tests for AMD 1-GPU PR CI
- [#31492](https://github.com/sgl-project/sglang/pull/31492) Register JIT kernel benchmarks to jit-kernel-benchmark-test-amd
- plus 14 more minor CI and test updates
</details>

<details>
<summary>Bugfixes (59)</summary>

- [#30868](https://github.com/sgl-project/sglang/pull/30868) Fix VLM CUDA graph shape stability
- [#30621](https://github.com/sgl-project/sglang/pull/30621) Fix image URL response for multiple outputs
- [#31343](https://github.com/sgl-project/sglang/pull/31343) Fix MiMo-V2 on Blackwell FA3 fallback and TP-aware audio weight loading
- [#31639](https://github.com/sgl-project/sglang/pull/31639) Account zero-logprob sequences correctly in chunked logprob stitching
- [#29508](https://github.com/sgl-project/sglang/pull/29508) Fix quickreduce acc error in cudagraph mode
- [#31094](https://github.com/sgl-project/sglang/pull/31094) Remove deprecated Mamba flags and fix FP8 GEMM docstrings
- [#30867](https://github.com/sgl-project/sglang/pull/30867) Fix image benchmark backend parity
- [#30682](https://github.com/sgl-project/sglang/pull/30682) Preserve tokenizer worker fanout when skip_tokenizer_init is enabled
- [#31211](https://github.com/sgl-project/sglang/pull/31211) Fix processor config loading for object-storage model paths
- [#31392](https://github.com/sgl-project/sglang/pull/31392) Wire detokenizer soft watchdog into multi-http-worker event loop
- [#31369](https://github.com/sgl-project/sglang/pull/31369) Fix mamba track-boundary seqlen under overlap scheduler
- [#31232](https://github.com/sgl-project/sglang/pull/31232) Fix Ministral3 accuracy issue by aligning YaRN RoPE scaling
- [#31131](https://github.com/sgl-project/sglang/pull/31131) Fix DSV4 JIT build on rocm
- [#31519](https://github.com/sgl-project/sglang/pull/31519) Update PR #25015 revert for fused topk=1 draft postprocess
- [#29430](https://github.com/sgl-project/sglang/pull/29430) Fix abusing presence of req.req_pool_idx
- [#31368](https://github.com/sgl-project/sglang/pull/31368) Fix early-send cached-prefix KV racing prefill forward on mori
- [#31092](https://github.com/sgl-project/sglang/pull/31092) Fix post-capture KV sizing for SWA pools
- [#31134](https://github.com/sgl-project/sglang/pull/31134) Fix LongCat n-gram embedding in PD-disaggregated scheduler loops
- [#31495](https://github.com/sgl-project/sglang/pull/31495) Fix num_running_reqs gauge on disagg prefill servers
- [#31515](https://github.com/sgl-project/sglang/pull/31515) Fix stale imports in test_fused_fp8_kv_write.py
- plus 39 more minor bugfixes and reverts
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f4f24b2c0d3d0a9ee8c97b7156b58677da110476e81cd12f216e464f979134c5 -->
