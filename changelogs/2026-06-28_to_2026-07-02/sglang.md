# sglang: PR digest (2026-06-28 to 2026-07-02)

_176 merged, 220 newly opened - source sgl-project/sglang, generated 2026-07-02T11:57:04Z_

## TL;DR
- **Models & Direction**: DeepSeek (V4/R1) and GLM (5.2) dominated model-specific work, with major pushes for DeepSeek V4 Flash MTP, sparse MLA prefill, and GLM-5.2 FP8 DSA support. MiniMax M3 also saw massive NPU adaptation work.
- **Memory & Cache**: Massive overhaul of memory management, merging a unified memory pool for hybrid Mamba/SWA models and a page-major KV/state layout, alongside in-progress work on Radix Cache splitting and FlexKV.
- **Kernels & Quantization**: Shipped SM90 Q8KV8 FP8 Sparse MLA prefill JIT kernels and fused NVFP4 expert quantization for CUTLASS MoE. Ongoing work is consolidating MoE routing onto a unified Triton backend that outperforms AOT on Hopper/Blackwell.
- **Speculative Decoding**: Heavy investment in speculative decoding infrastructure, including decoupled transport layers, DSpark support for prefill-decode disaggregation, and XPU speculative decoding support.
- **Hardware**: Broad hardware expansion, notably AMD (tiered DRAM+SSD L3 HiCache, Quark MXFP4 MoE), Intel XPU (full graph and spec decode support), and Ascend NPU (DeepSeek V4 and MiniMax M3 support).

## Most important PRs
- **[#29678](https://github.com/sgl-project/sglang/pull/29678)** introduces a unified memory pool for hybrid Mamba and Sliding Window Attention (SWA) models, allowing seamless memory sharing across different attention paradigms and significantly improving memory utilization.
- **[#25751](https://github.com/sgl-project/sglang/pull/25751)** ships an SM90 Q8KV8 FP8 Sparse MLA Prefill JIT kernel, delivering a highly optimized, torch-compiled Triton backend for Hopper architectures that drastically improves prefill throughput.
- **[#25377](https://github.com/sgl-project/sglang/pull/25377)** implements a UMBP tiered DRAM + SSD L3 storage backend for HiCache on AMD, leveraging a hugepage host allocator to enable massive out-of-core KV cache capacity on ROCm.
- **[#29771](https://github.com/sgl-project/sglang/pull/29771)** consolidates ungrouped and grouped MoE gate/top-k operations onto a single unified Triton router, an in-progress change that already outperforms AOT compilation on B200/H100/H200.
- **[#29705](https://github.com/sgl-project/sglang/pull/29705)** expands DSpark speculative decoding to support prefill-decode disaggregation (PD) and Data Parallel (DP) attention, allowing large-scale deployments to scale speculative drafting across distributed workers efficiently.

## More changes by area

<details>
<summary>Performance (16)</summary>

- [#29499](https://github.com/sgl-project/sglang/pull/29499) Optimize DSA CUDA graph replay metadata generation
- [#28612](https://github.com/sgl-project/sglang/pull/28612) Optimize C128 state pool allocation using request state pool
- [#29223](https://github.com/sgl-project/sglang/pull/29223) Shard Kimi-K2.5 Eagle3 draft fc + symm-mem AG
- [#28287](https://github.com/sgl-project/sglang/pull/28287) Optimize HiCache hash generation with bulk token byte conversion
- [#18612](https://github.com/sgl-project/sglang/pull/18612) Fuse SiLU+Mul into NVFP4 Expert Quantization for CUTLASS MoE
- [#29638](https://github.com/sgl-project/sglang/pull/29638) Add TileLang FP8 blockwise GEMM backend
- [#29666](https://github.com/sgl-project/sglang/pull/29666) Optimize Quest sparse algorithm retrieval and page representation
- [#29800](https://github.com/sgl-project/sglang/pull/29800) prefill CUDA graph + deterministic MTP for AMD MI355X
- [#29723](https://github.com/sgl-project/sglang/pull/29723) Add fused all-reduce RMSNorm per-token FP8/MXFP4 quant
- [#29825](https://github.com/sgl-project/sglang/pull/29825) use torch.empty for HiCache dummy read buffers to skip a memset
- [#29921](https://github.com/sgl-project/sglang/pull/29921) avoid per-step D2H .item() sync in cuda-graph loc translate
- [#29677](https://github.com/sgl-project/sglang/pull/29677) compact Triton extend-attention for ragged prefill (AMD/HIP-only)
- [#29804](https://github.com/sgl-project/sglang/pull/29804) Fuse MoE combine multiply-reduce into one Metal kernel
- [#29722](https://github.com/sgl-project/sglang/pull/29722) Speed up weight loading on NVIDIA Grace via temporary pinned H2D copy
- [#27948](https://github.com/sgl-project/sglang/pull/27948) Skip custom all-reduce v2 CUDA graph capture with torch memory saver
- [#29382](https://github.com/sgl-project/sglang/pull/29382) use faster exp in silu_and_mul

</details>

<details>
<summary>Kernels & attention (35)</summary>

- [#29533](https://github.com/sgl-project/sglang/pull/29533) page-major (layer-major within a page) KV/state layout
- [#29867](https://github.com/sgl-project/sglang/pull/29867) shared ShortConvAttnBackend for ZAYA1 CCA + LFM2 short conv
- [#29472](https://github.com/sgl-project/sglang/pull/29472) Add FlashKDA prefill backend for safe-gate KDA linear attention
- [#29613](https://github.com/sgl-project/sglang/pull/29613) Use cos_sin_cache for DSA indexer fusion
- [#29343](https://github.com/sgl-project/sglang/pull/29343) fa3/fa4: device-side page table; drop seq_lens_cpu D2H sync
- [#29775](https://github.com/sgl-project/sglang/pull/29775) Enable FlashMLA sparse prefill by default
- [#29509](https://github.com/sgl-project/sglang/pull/29509) GLM-4.7-Flash optimize with fused kernels
- [#29576](https://github.com/sgl-project/sglang/pull/29576) Fix DSA indexer fusion bug causing excessive memory consumption
- [#29420](https://github.com/sgl-project/sglang/pull/29420) Remove per-batch D2H syncs in MTP to avoid bubbles between 2 batches
- [#29460](https://github.com/sgl-project/sglang/pull/29460) Fix SWA cache loc slicing for all attention backends
- [#29741](https://github.com/sgl-project/sglang/pull/29741) Support LongCat 2.0 for Ascend NPU
- [#29839](https://github.com/sgl-project/sglang/pull/29839) integrate hpc-ops attention and MoE backends
- [#29847](https://github.com/sgl-project/sglang/pull/29847) Add DSA CP shared KV cache
- [#29737](https://github.com/sgl-project/sglang/pull/29737) Add cuLA KVBuffer backend for Lightning Attention
- [#29843](https://github.com/sgl-project/sglang/pull/29843) Fuse cuda-graph metadata rebuild into one triton kernel
- [#29706](https://github.com/sgl-project/sglang/pull/29706) Enable EAGLE tree drafting (topk>1) verify+draft on trtllm_mla / cutedsl_mla
- [#29776](https://github.com/sgl-project/sglang/pull/29776) Add GFusion and EBSampling
- [#29930](https://github.com/sgl-project/sglang/pull/29930) layer-split prefill KV cache across CP ranks
- [#29619](https://github.com/sgl-project/sglang/pull/29619) Add an opt-in non-paged indexer for long-context prefill
- [#29690](https://github.com/sgl-project/sglang/pull/29690) Fuse the preprocess kernels of trtllm-gen attention
- [#29639](https://github.com/sgl-project/sglang/pull/29639) Build device-side tensor descriptors in extend attention kernel
- [#29826](https://github.com/sgl-project/sglang/pull/29826) Add DPSK V4 multi-head tiled FlashMLA sparse decode kernel
- [#29786](https://github.com/sgl-project/sglang/pull/29786) Support chunked prefill for DeepSeek-V4
- [#29589](https://github.com/sgl-project/sglang/pull/29589) fa3/fa4: sync-free for all backends and phases
- [#29699](https://github.com/sgl-project/sglang/pull/29699) When attention TP for linear and full attention, use Flashinfer allreduce fusion
- [#29732](https://github.com/sgl-project/sglang/pull/29732) Refactor NPU state layout and add unit tests for verification
- [#29881](https://github.com/sgl-project/sglang/pull/29881) Avoid logits multimem all-gather on cross-node TP groups
- [#29665](https://github.com/sgl-project/sglang/pull/29665) Size FA3 speculative page tables from req_to_token capacity
- [#29624](https://github.com/sgl-project/sglang/pull/29624) drop dead cu_seqlens_k_new arg in FA3 backend non-append-KV calls
- [#29711](https://github.com/sgl-project/sglang/pull/29711) Use DeepGEMM out API for DSA schedule metadata
- [#29720](https://github.com/sgl-project/sglang/pull/29720) use 64-bit indexing in merge_state_v2 kernel to prevent integer overflow
- [#29581](https://github.com/sgl-project/sglang/pull/29581) Fix aiter/wave cuda_graph_custom_mask undersize on long-context spec verify
- [#29798](https://github.com/sgl-project/sglang/pull/29798) avoid DSA indexer CPU seq lens fallback
- [#29724](https://github.com/sgl-project/sglang/pull/29724) Fix DSA draft-extend metadata on HIP gpu-only path
- [#29899](https://github.com/sgl-project/sglang/pull/29899) size dsv3_fused_a_gemm pipeline by the device shared-memory limit

</details>

<details>
<summary>MoE & quantization (29)</summary>

- [#27204](https://github.com/sgl-project/sglang/pull/27204) Implement QuarkW4A8MXFp4MoE to support amd/gpt-oss-120b-w-mxfp4-a-fp8
- [#28974](https://github.com/sgl-project/sglang/pull/28974) weight checker refactor: add precision branch; allow ULP quant err
- [#25835](https://github.com/sgl-project/sglang/pull/25835) Triton moe fused gate
- [#29761](https://github.com/sgl-project/sglang/pull/29761) compressed-tensors WNA16 MoE: don't assume a "Linear" config group
- [#26255](https://github.com/sgl-project/sglang/pull/26255) Add support for flashinfer MOE A2A to Qwen3 BF16 model path
- [#29640](https://github.com/sgl-project/sglang/pull/29640) Add Qwen3 MoE tests for PP compatibility with CP and DP
- [#29463](https://github.com/sgl-project/sglang/pull/29463) Reland: run routed experts on main stream in dual-stream MoE
- [#29685](https://github.com/sgl-project/sglang/pull/29685) Skip routed expert capture for draft model under spec v2
- [#29659](https://github.com/sgl-project/sglang/pull/29659) Support Transformers v5 packed MoE expert weights
- [#29461](https://github.com/sgl-project/sglang/pull/29461) Fix FlashInfer A2A dispatcher during CUDA graph capture
- [#28676](https://github.com/sgl-project/sglang/pull/28676) fix deepseek v4 MXFP8 flashinfer_trtllm_routed MoE weight update
- [#29694](https://github.com/sgl-project/sglang/pull/29694) Fix int8 per-token quant Triton portability
- [#29762](https://github.com/sgl-project/sglang/pull/29762) mxfp on a5 initial support
- [#29778](https://github.com/sgl-project/sglang/pull/29778) Add DWDP (Distributed Weight Data Parallelism) for MoE prefill
- [#29922](https://github.com/sgl-project/sglang/pull/29922) Add DeepSeek-V3 grouped routing to the unified Triton router
- [#29727](https://github.com/sgl-project/sglang/pull/29727) Add blockwise_fp8 online weight quantization
- [#29718](https://github.com/sgl-project/sglang/pull/29718) Fuse simulated expert choice into one triton kernel
- [#29534](https://github.com/sgl-project/sglang/pull/29534) Handle FP4 MegaMOE fallback for DeepSeek-V4
- [#29919](https://github.com/sgl-project/sglang/pull/29919) Fix and Fuse DeepSeek-V4 FP8 wo_a quantization
- [#29652](https://github.com/sgl-project/sglang/pull/29652) Add H200 FP8 MoE config for GLM
- [#29848](https://github.com/sgl-project/sglang/pull/29848) Experiment: materialize MoE weights before copy
- [#29856](https://github.com/sgl-project/sglang/pull/29856) Fix BF16 routing bias dtype for TRT-LLM MoE
- [#29643](https://github.com/sgl-project/sglang/pull/29643) support num_experts > hidden_dim/8 in silu_and_mul masked post-quant
- [#29931](https://github.com/sgl-project/sglang/pull/29931) Fix NVFP4 Marlin MoE Backend routed scaling on Hopper
- [#29682](https://github.com/sgl-project/sglang/pull/29682) Fix Quark crash on W4A8 ProgressiveSpec (list) configs
- [#29918](https://github.com/sgl-project/sglang/pull/29918) Gate broken CK block-FP8 GEMM shapes to aiter-triton-GEMM
- [#29669](https://github.com/sgl-project/sglang/pull/29669) Skip MXFP8 autotune on dense GEMM, which causes IMA
- [#29760](https://github.com/sgl-project/sglang/pull/29760) Feat/flashmla fp8 dcp
- [#29588](https://github.com/sgl-project/sglang/pull/29588) Capture routed expert metadata for HashTopK

</details>

<details>
<summary>Model support (32)</summary>

- [#28958](https://github.com/sgl-project/sglang/pull/28958) Support nvidia/LocateAnything-3B
- [#27887](https://github.com/sgl-project/sglang/pull/27887) Add HrmTextForCausalLM (Hierarchical Reasoning Model - Text)
- [#29667](https://github.com/sgl-project/sglang/pull/29667) Add fused EH norm for DeepSeek NextN
- [#28471](https://github.com/sgl-project/sglang/pull/28471) add AMD MI300X/MI325X/MI355X support for GLM-5.2
- [#27455](https://github.com/sgl-project/sglang/pull/27455) Add FlashInfer sparse MLA decode for DSv4-Flash
- [#28731](https://github.com/sgl-project/sglang/pull/28731) drop redundant serve flags (GLM-5.2) + fix M3 page-size note
- [#29557](https://github.com/sgl-project/sglang/pull/29557) GLM-5.2 NVFP4 B300: TP8 recipe + 3 strategies
- [#29674](https://github.com/sgl-project/sglang/pull/29674) add B200 NVFP4 recipes + benchmarks to GLM-5.2 cookbook
- [#29905](https://github.com/sgl-project/sglang/pull/29905) add Qwen3.6-27B-NVFP4 variant to cookbook
- [#29381](https://github.com/sgl-project/sglang/pull/29381) Fix glm 4.6v
- [#29505](https://github.com/sgl-project/sglang/pull/29505) Qwen3-VL-30B use split_qkv_rmsnorm_rope for extend
- [#29627](https://github.com/sgl-project/sglang/pull/29627) Qwen3-VL-8B use split_qkv_rmsnorm_rope for extend
- [#29470](https://github.com/sgl-project/sglang/pull/29470) Tune the threshold of router GEMM
- [#29827](https://github.com/sgl-project/sglang/pull/29827) Tiny update dsv4 doc
- [#29788](https://github.com/sgl-project/sglang/pull/29788) minimax m3 npu adaptor
- [#29586](https://github.com/sgl-project/sglang/pull/29586) GLM-5.2 FP8 DSA support on SM120 (RTX PRO 6000)
- [#29538](https://github.com/sgl-project/sglang/pull/29538) Add DSpark speculative decoding for DeepSeek-V4
- [#29850](https://github.com/sgl-project/sglang/pull/29850) Support MOSS-Transcribe-Diarize model and adapter
- [#29641](https://github.com/sgl-project/sglang/pull/29641) Support mlaprolog, fp8 KVcache(only MLA) and ChunkPrefill for A5(950PR/DT) NPU
- [#29651](https://github.com/sgl-project/sglang/pull/29651) Support prefill-decode disaggregation for DeepSeek V4 on NPU
- [#29609](https://github.com/sgl-project/sglang/pull/29609) Support BF16 Compress State for Online C128
- [#29644](https://github.com/sgl-project/sglang/pull/29644) support CP with TP & DP < TP
- [#29837](https://github.com/sgl-project/sglang/pull/29837) Fix GLM-DSA raw config restoration
- [#29892](https://github.com/sgl-project/sglang/pull/29892) Support GLM-5.2 moe router use FP32
- [#29569](https://github.com/sgl-project/sglang/pull/29569) Support megamoe for CP
- [#29821](https://github.com/sgl-project/sglang/pull/29821) Experiment with sync DSV4 weight loading
- [#29890](https://github.com/sgl-project/sglang/pull/29890) treat v_head_dim=0 as unset when deriving model shapes
- [#29628](https://github.com/sgl-project/sglang/pull/29628) Fix Ministral3 double-construction
- [#29883](https://github.com/sgl-project/sglang/pull/29883) fix strip streaming empty-string suffix from DSV4 tool arguments
- [#29692](https://github.com/sgl-project/sglang/pull/29692) Use fused A GEMM for `fc1_latent_proj` in NemotronH
- [#29550](https://github.com/sgl-project/sglang/pull/29550) minimax M2 tool call unit tests
- [#29552](https://github.com/sgl-project/sglang/pull/29552) Handle Qwen2 attention partitioning with DP attention

</details>

<details>
<summary>Parallelism & scheduling (35)</summary>

- [#29211](https://github.com/sgl-project/sglang/pull/29211) Fix KV-event publisher port collision under pure data parallelism
- [#29520](https://github.com/sgl-project/sglang/pull/29520) fix prefill-aware SWA floor tracking
- [#29352](https://github.com/sgl-project/sglang/pull/29352) skip swa recovery on locked full kv
- [#29436](https://github.com/sgl-project/sglang/pull/29436) first-class session identity in SGLang
- [#29571](https://github.com/sgl-project/sglang/pull/29571) include CP size in PP rank offset
- [#29842](https://github.com/sgl-project/sglang/pull/29842) pad customized_info for mixed output batches
- [#29217](https://github.com/sgl-project/sglang/pull/29217) Fix step-bounded profiling for bench tools on Apple Silicon
- [#29535](https://github.com/sgl-project/sglang/pull/29535) Add scheduler metrics reporter init hook
- [#29351](https://github.com/sgl-project/sglang/pull/29351) keep full kv when swa skips leaf data
- [#29350](https://github.com/sgl-project/sglang/pull/29350) fix swa eviction boundary for unfinished inserts
- [#29296](https://github.com/sgl-project/sglang/pull/29296) Fix encoder health check with global cache TP
- [#29546](https://github.com/sgl-project/sglang/pull/29546) Clean up follow-ups for eagle hidden dim clean up
- [#29543](https://github.com/sgl-project/sglang/pull/29543) Fix DP-attention SHM feature finalization race
- [#29556](https://github.com/sgl-project/sglang/pull/29556) dflash: drop verify_done barrier; rely on scheduler WAR fallback
- [#29354](https://github.com/sgl-project/sglang/pull/29354) clear stale mamba cow source on rematch
- [#29642](https://github.com/sgl-project/sglang/pull/29642) Copy decode result on forward_stream instead of copy_stream
- [#29901](https://github.com/sgl-project/sglang/pull/29901) Radix Cache Split: Current Status 07/01
- [#29701](https://github.com/sgl-project/sglang/pull/29701) Flexkv main connector
- [#29574](https://github.com/sgl-project/sglang/pull/29574) Paper Reproduction of LMetric Multiplication Scheduling in SGLang Gateway
- [#29735](https://github.com/sgl-project/sglang/pull/29735) Support FlashInfer GDN prefill with extra-buffer radix cache
- [#29734](https://github.com/sgl-project/sglang/pull/29734) Auto-select FlashInfer GDN prefill on validated SM100 configs
- [#29730](https://github.com/sgl-project/sglang/pull/29730) Fix prefill DP rank routing under plain DP (non-DP-attention)
- [#29757](https://github.com/sgl-project/sglang/pull/29757) Fix fake-transfer prefill: chunked KV leak + radix cache exclusion
- [#29834](https://github.com/sgl-project/sglang/pull/29834) Fix scheduler crash on prefill-unreachable decode abort
- [#29819](https://github.com/sgl-project/sglang/pull/29819) Fix UnifiedRadixCache HiCache load-back readiness
- [#29898](https://github.com/sgl-project/sglang/pull/29898) Fix PrefillDelayer deadlock: bound the "all"-branch delay by max_delay_passes
- [#29817](https://github.com/sgl-project/sglang/pull/29817) write_back policy refinement
- [#29620](https://github.com/sgl-project/sglang/pull/29620) Skip L3 prefetch when storage has no hit in prefill scheduler
- [#29860](https://github.com/sgl-project/sglang/pull/29860) Fix SWA eviction tombstoning the last leaf
- [#29792](https://github.com/sgl-project/sglang/pull/29792) Fix Mamba track-boundary bookkeeping under overlap scheduling
- [#29662](https://github.com/sgl-project/sglang/pull/29662) Fix SWA pool exhaustion in decode _pre_alloc by passing swa_num_tokens
- [#29802](https://github.com/sgl-project/sglang/pull/29802) sync kv_committed_len before release to retain deco…
- [#29893](https://github.com/sgl-project/sglang/pull/29893) Remove cpu-gpu sync in kv allocator free
- [#29689](https://github.com/sgl-project/sglang/pull/29689) Gdn stash elim option a
- [#29879](https://github.com/sgl-project/sglang/pull/29879) Add forward-pass decode interference metrics

</details>

<details>
<summary>Speculative decoding (24)</summary>

- [#23180](https://github.com/sgl-project/sglang/pull/23180) Speculative decoding support on XPU
- [#29595](https://github.com/sgl-project/sglang/pull/29595) Enable FlashInfer autotune for spec draft
- [#29464](https://github.com/sgl-project/sglang/pull/29464) Fix EAGLE draft hidden dim extraction and centralize spec helpers
- [#27750](https://github.com/sgl-project/sglang/pull/27750) extend weight checker to speculative draft worker(s)
- [#29446](https://github.com/sgl-project/sglang/pull/29446) Add Laguna XS.2.1 DFlash support to SGLang
- [#29232](https://github.com/sgl-project/sglang/pull/29232) Replace shared-infra dflash special-cases with capabilities
- [#29395](https://github.com/sgl-project/sglang/pull/29395) Capture DFLASH draft greedy sampling inside the draft decode cuda graph
- [#29338](https://github.com/sgl-project/sglang/pull/29338) Add DFLASH basic sanity CI test
- [#29645](https://github.com/sgl-project/sglang/pull/29645) Support real draft tokens to simulated acceptance
- [#23838](https://github.com/sgl-project/sglang/pull/23838) Validate vocabulary compatibility in STANDALONE mode
- [#29622](https://github.com/sgl-project/sglang/pull/29622) Budget EAGLE/STANDALONE draft KV pool in SWA pool configurators
- [#29654](https://github.com/sgl-project/sglang/pull/29654) Fix index_share_for_mtp_iteration being a no-op in EAGLE MTP draft
- [#29541](https://github.com/sgl-project/sglang/pull/29541) Publish DFLASH verify read-done event for fine-grained WAR barrier
- [#29610](https://github.com/sgl-project/sglang/pull/29610) Decoupled speculative decoding: pluggable transport layer + IPC threads
- [#29907](https://github.com/sgl-project/sglang/pull/29907) Add DDTree speculative decoding
- [#29587](https://github.com/sgl-project/sglang/pull/29587) DFlash tree drafting: host-side tree-construction core
- [#29917](https://github.com/sgl-project/sglang/pull/29917) Add DSpark speculative decoding for Qwen3
- [#29787](https://github.com/sgl-project/sglang/pull/29787) Anchor GLM-5.2 MTP IndexShare topk on the draft-extend step
- [#29696](https://github.com/sgl-project/sglang/pull/29696) Size speculative attention metadata from req_to_token capacity
- [#29868](https://github.com/sgl-project/sglang/pull/29868) Decoupled speculative decoding: ignore_decode_budget for the drafter engine
- [#29858](https://github.com/sgl-project/sglang/pull/29858) Build SWA window kv buffers for the EAGLE draft-extend cuda-graph path
- [#29611](https://github.com/sgl-project/sglang/pull/29611) Make `build_tree_kernel_efficient` enforce `seq_lens_sum` contract
- [#29781](https://github.com/sgl-project/sglang/pull/29781) Enable EAGLE for GLM5.2-MXFP4
- [#29876](https://github.com/sgl-project/sglang/pull/29876) Fix EAGLE speculative decoding with DSA backend on gfx950 (MI355X)

</details>

<details>
<summary>Hardware & arch (45)</summary>

- [#29492](https://github.com/sgl-project/sglang/pull/29492) update best practicce docs from testcase
- [#29053](https://github.com/sgl-project/sglang/pull/29053) Enable XPU graph support (decode full-graph + prefill tc_piecewise)
- [#29708](https://github.com/sgl-project/sglang/pull/29708) Add LTX2 QKNorm split-RoPE CUDA fast path
- [#28348](https://github.com/sgl-project/sglang/pull/28348) Enable NIXL PD disaggregation for ROCm(1/n)
- [#29497](https://github.com/sgl-project/sglang/pull/29497) Fix model failures on Xeon
- [#29378](https://github.com/sgl-project/sglang/pull/29378) enable fused_sigmoid_mul on CPU device
- [#28714](https://github.com/sgl-project/sglang/pull/28714) Split 3/4: disagg K-only index-K transfer
- [#29458](https://github.com/sgl-project/sglang/pull/29458) Enable Breakable Cuda Graph as Default
- [#29779](https://github.com/sgl-project/sglang/pull/29779) Share one logits output buffer across prefill/decode/draft cuda-graph runners
- [#22394](https://github.com/sgl-project/sglang/pull/22394) Support flashinfer a2a with flashinfer_trtllm_routed moe
- [#29625](https://github.com/sgl-project/sglang/pull/29625) CUDA graph executable dedup via cudaGraphExecUpdate
- [#20072](https://github.com/sgl-project/sglang/pull/20072) Padding for dim divisibility in TP3/6 cases
- [#27060](https://github.com/sgl-project/sglang/pull/27060) Use NIXL path-mode
- [#29310](https://github.com/sgl-project/sglang/pull/29310) Detect for double-free in HostKVCache
- [#29616](https://github.com/sgl-project/sglang/pull/29616) Frozen-KV MTP: delay target KV binding to pool init + reset stale draft out_cache_loc
- [#28053](https://github.com/sgl-project/sglang/pull/28053) Disable dsr1 prefill cudagraphs by default
- [#29161](https://github.com/sgl-project/sglang/pull/29161) Defer DSA MLA CP KV gather for fp8 trtllm prefill in PD mode
- [#29829](https://github.com/sgl-project/sglang/pull/29829) Fix block_table batch size mismatch in GLM-4.7-Flash DeepEP + MTP without CUDA Graphs
- [#29166](https://github.com/sgl-project/sglang/pull/29166) Inline H2D during CUDA graph capture to avoid stream isolation in Offloader
- [#28925](https://github.com/sgl-project/sglang/pull/28925) pin flashinfer allreduce-fusion backend for TP-partial capture contract
- [#29681](https://github.com/sgl-project/sglang/pull/29681) default prefill_aware_swa=False on MlxModelRunnerStub
- [#29146](https://github.com/sgl-project/sglang/pull/29146) revise interface get cpu copy for npu mem pool to align with gpu
- [#29029](https://github.com/sgl-project/sglang/pull/29029) Fix a ModelSlim loading failure
- [#29598](https://github.com/sgl-project/sglang/pull/29598) Accept in_capture in Ascend replay metadata
- [#29493](https://github.com/sgl-project/sglang/pull/29493) Add scoring_func for mimo_v2
- [#29823](https://github.com/sgl-project/sglang/pull/29823) fix draft host pool allocator type
- [#29752](https://github.com/sgl-project/sglang/pull/29752) Add experimental MoL route-decode KV reuse patch
- [#29884](https://github.com/sgl-project/sglang/pull/29884) Cookbook: Laguna-XS-2.1 (DFlash low-latency + high-throughput)
- [#29859](https://github.com/sgl-project/sglang/pull/29859) Unified Mooncake Registration for Logical Anchors and Draft Pools
- [#29716](https://github.com/sgl-project/sglang/pull/29716) add client-side metadata cache for HiCacheFile storage
- [#29832](https://github.com/sgl-project/sglang/pull/29832) Enable mamba extra_buffer on ROCm + shared-prefix donate correctness test
- [#29895](https://github.com/sgl-project/sglang/pull/29895) Route OOT available-memory queries through current_platform
- [#29668](https://github.com/sgl-project/sglang/pull/29668) resolve Mooncake local_hostname per node for runtime attach
- [#29754](https://github.com/sgl-project/sglang/pull/29754) MooncakeStore(standalone) check fails for DeepSeek-V4 logical anchor pool
- [#29756](https://github.com/sgl-project/sglang/pull/29756) Fix MiniMax M3 state transfer in Mori PD
- [#29753](https://github.com/sgl-project/sglang/pull/29753) Fix rope sin cos pre-calculation for Qwen3.5 and Qwen3_next during Pipeline Parallelism
- [#29621](https://github.com/sgl-project/sglang/pull/29621) Extract reusable VMM shareable-handle helpers from register_graph_inputs
- [#27915](https://github.com/sgl-project/sglang/pull/27915) DeepSeek V4 7/N: Support fused_rope_inplace on XPU using triton
- [#29935](https://github.com/sgl-project/sglang/pull/29935) Add memory saver support for Intel XPU via upstream torch_memory_saver
- [#29657](https://github.com/sgl-project/sglang/pull/29657) Support Deepseek V4 piecewise cuda graph on ROCm platform
- [#29707](https://github.com/sgl-project/sglang/pull/29707) Add NIXL KV-transfer leg to MI355X disaggregation nightly
- [#29855](https://github.com/sgl-project/sglang/pull/29855) 3/N Add Kimi K2.6 FP8 MI355X 1P1D nightly recipes
- [#29637](https://github.com/sgl-project/sglang/pull/29637) enable hisparse prefetch utilizing IndexShare for GLM-5.2 and more
- [#29544](https://github.com/sgl-project/sglang/pull/29544) add PD disaggregation to GLM-5.2 cookbook playground
- [#29615](https://github.com/sgl-project/sglang/pull/29615) Make mem_fraction_static reserve disaggregation-mode aware
- [#29865](https://github.com/sgl-project/sglang/pull/29865) Support alternative BF16 GEMM

</details>

<details>
<summary>Multimodal & Diffusion (34)</summary>

- [#29791](https://github.com/sgl-project/sglang/pull/29791) Add 5090 diffusion consumer GPU guard
- [#29824](https://github.com/sgl-project/sglang/pull/29824) CI: tighten multimodal-gen consistency thresholds
- [#29664](https://github.com/sgl-project/sglang/pull/29664) Reuse shared AlignedVector and tidy jit_kernel/diffusion
- [#29688](https://github.com/sgl-project/sglang/pull/29688) support Krea-2 + run-driven `has_separate_cfg`
- [#29862](https://github.com/sgl-project/sglang/pull/29862) Add --offload-during-compile to fit max-autotune on tight-memory GPUs
- [#29649](https://github.com/sgl-project/sglang/pull/29649) keep image-model auxiliary components resident under auto memory policy
- [#29789](https://github.com/sgl-project/sglang/pull/29789) clean diffusion dead code
- [#29434](https://github.com/sgl-project/sglang/pull/29434) nightly: track SGLang-Diffusion only
- [#29519](https://github.com/sgl-project/sglang/pull/29519) warmup: default to model sampling resolution (declare Z-Image default)
- [#29545](https://github.com/sgl-project/sglang/pull/29545) CI: make consistency GT probe robust to transient CDN failures
- [#29514](https://github.com/sgl-project/sglang/pull/29514) fix --warmup silently downgrading server-based warmup to request mode
- [#29364](https://github.com/sgl-project/sglang/pull/29364) Document VAE decode parallel group axes
- [#29767](https://github.com/sgl-project/sglang/pull/29767) Relax ModelOpt NVFP4 diffusion consistency thresholds
- [#29537](https://github.com/sgl-project/sglang/pull/29537) remove multimodal piecewise CUDA graph gate test
- [#29672](https://github.com/sgl-project/sglang/pull/29672) Fix causal Conv3D cat/pad fusion crashes for wan2.2 t2v
- [#29742](https://github.com/sgl-project/sglang/pull/29742) Fix Z-Image accuracy
- [#29656](https://github.com/sgl-project/sglang/pull/29656) make mm_inputs msgpack-native
- [#29852](https://github.com/sgl-project/sglang/pull/29852) refactor cuda attention backend resolver
- [#29712](https://github.com/sgl-project/sglang/pull/29712) separate image loader
- [#29631](https://github.com/sgl-project/sglang/pull/29631) add cache-dit support for Ideogram 4
- [#29777](https://github.com/sgl-project/sglang/pull/29777) Support SP for Krea-2
- [#29831](https://github.com/sgl-project/sglang/pull/29831) Prefer official diffusion consistency GT
- [#29888](https://github.com/sgl-project/sglang/pull/29888) NVILA: fix video request crash from stale .asnumpy()
- [#29553](https://github.com/sgl-project/sglang/pull/29553) make mm_data_mooncake msgpack-native (drop PickleWrapper)
- [#29772](https://github.com/sgl-project/sglang/pull/29772) Fix USPAttention replicated-prefix head sharding for GQA
- [#29755](https://github.com/sgl-project/sglang/pull/29755) cache cross-attn K/V across denoise steps for Helios
- [#29774](https://github.com/sgl-project/sglang/pull/29774) Shard QwenImage DiT across TP ranks
- [#29903](https://github.com/sgl-project/sglang/pull/29903) fix: Z-Image online fp8 quantization crash with dit_cpu_offload
- [#29926](https://github.com/sgl-project/sglang/pull/29926) Fix Diffusion GT generation pipelines
- [#29647](https://github.com/sgl-project/sglang/pull/29647) Fix ROCm causal Conv3D cat-pad fallback
- [#29863](https://github.com/sgl-project/sglang/pull/29863) Refresh LTX HQ consistency GT
- [#29936](https://github.com/sgl-project/sglang/pull/29936) remap vision_tower.vision_model.* weights for flattened SiglipVisionModel
- [#29673](https://github.com/sgl-project/sglang/pull/29673) disable layernorm torch.compile on ROCm to avoid memory-access fault
- [#29911](https://github.com/sgl-project/sglang/pull/29911) Remove redundant xpu graph backend

</details>

<details>
<summary>API & serving (20)</summary>

- [#29684](https://github.com/sgl-project/sglang/pull/29684) engine: zstd request-body decompression + header overrides
- [#29799](https://github.com/sgl-project/sglang/pull/29799) support rust sglang server
- [#29915](https://github.com/sgl-project/sglang/pull/29915) Log every engine /abort_request with a router_reason label + Prom counter
- [#29810](https://github.com/sgl-project/sglang/pull/29810) Add OpenAI-compatible tokenize endpoints
- [#29560](https://github.com/sgl-project/sglang/pull/29560) HTTP server: expose uvicorn/Granian operator tunables
- [#29920](https://github.com/sgl-project/sglang/pull/29920) resolve special-token suffix at runtime for compatibility
- [#29719](https://github.com/sgl-project/sglang/pull/29719) Fix SSE error JSON format and inject api_key in PD requests
- [#29565](https://github.com/sgl-project/sglang/pull/29565) Release LoRA usage for aborted waiting-queue requests
- [#29582](https://github.com/sgl-project/sglang/pull/29582) Preserve single quotes inside JSON values in Llama32 streaming tool calls
- [#29744](https://github.com/sgl-project/sglang/pull/29744) include $defs for named tool_choice schemas
- [#29539](https://github.com/sgl-project/sglang/pull/29539) Avoid empty content prelude in chat streams
- [#29658](https://github.com/sgl-project/sglang/pull/29658) Reject API keys in multi-tokenizer mode where auth is not enforced
- [#29579](https://github.com/sgl-project/sglang/pull/29579) Add --default-chat-template-kwargs server arg
- [#29703](https://github.com/sgl-project/sglang/pull/29703) Fix missing cache_read_input_tokens in streaming responses
- [#29745](https://github.com/sgl-project/sglang/pull/29745) avoid appending port to URL hosts with ports
- [#29882](https://github.com/sgl-project/sglang/pull/29882) populate batch req rids and per-request http_worker_ipc for mult…
- [#29820](https://github.com/sgl-project/sglang/pull/29820) return 400 for negative token ids in /v1/detokenize
- [#29813](https://github.com/sgl-project/sglang/pull/29813) fix tokenizer load blocking /health on tokio worker thread
- [#29717](https://github.com/sgl-project/sglang/pull/29717) fix fastsafetensors multi-node device + configurable bbuf/threads
- [#29923](https://github.com/sgl-project/sglang/pull/29923) Emit HiCache L3 KV events

</details>

<details>
<summary>Tests, CI & build (48)</summary>

- [#29784](https://github.com/sgl-project/sglang/pull/29784) 2/N Add DSV4 DP8/EP8 and MTP MI355X 1P1D nightly recipes
- [#29066](https://github.com/sgl-project/sglang/pull/29066) Migrate JIT tests to runner config registration
- [#28908](https://github.com/sgl-project/sglang/pull/28908) Initially add nightly GSM8K accuracy tests for Llama-3.1-8B (TP=2) and Qwen3-32B (TP=4)
- [#29393](https://github.com/sgl-project/sglang/pull/29393) Bump transformers to 5.12.1
- [#29290](https://github.com/sgl-project/sglang/pull/29290) Cover DeepSeek-R1 MXFP4 TP4 MTP nightly CI
- [#29765](https://github.com/sgl-project/sglang/pull/29765) Update AMD local registry address
- plus 42 more minor CI updates

</details>

<details>
<summary>Docs (10)</summary>

- [#28586](https://github.com/sgl-project/sglang/pull/28586) Checking and modifying Markdown formatting issues and link validity
- [#29591](https://github.com/sgl-project/sglang/pull/29591) Use --cuda-graph-max-bs-decode in tests, examples, and docs
- [#29307](https://github.com/sgl-project/sglang/pull/29307) sync LMSYS SGLang blog cards
- [#29871](https://github.com/sgl-project/sglang/pull/29871) Add no-getattr rule; refine no-dataclasses rule
- [#29676](https://github.com/sgl-project/sglang/pull/29676) Add --prerelease=allow so uv installs the latest sglang
- plus 5 more minor doc updates

</details>

<details>
<summary>Bugfixes & Refactors (28)</summary>

- [#29872](https://github.com/sgl-project/sglang/pull/29872) Fix chunked SGMV (csgmv) CUDA graph segment replay
- [#29770](https://github.com/sgl-project/sglang/pull/29770) cleanup garbage code
- [#29156](https://github.com/sgl-project/sglang/pull/29156) Fix bounded checkpoint prefetching and buffered drop-cache handling
- [#29271](https://github.com/sgl-project/sglang/pull/29271) make write_token dynamic
- [#28190](https://github.com/sgl-project/sglang/pull/28190) do not promote failed runs to the comparison baseline
- plus 23 more minor bugfixes and refactors

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 76e5c1b5a58f8f071f6830dec96b0164d28da36408627f479d634d5c2776d838 -->
