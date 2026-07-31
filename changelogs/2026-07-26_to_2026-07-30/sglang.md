# sglang: PR digest (2026-07-26 to 2026-07-30)

_185 merged, 312 newly opened - source sgl-project/sglang, generated 2026-07-30T11:27:14Z_

## TL;DR
- **Model Focus**: Massive in-progress push to support the **Kimi K3** family across NVIDIA, AMD (DCP), and Ascend NPUs, alongside heavy optimization for **DeepSeek-V4/V3.2** and **GLM-5.2** (FP8 sparse prefill, SM90 MegaMoE, and low-latency serving).
- **Rust Server Rewrite**: Significant merged and newly-opened work is migrating the core server, tokenizer manager, and API routing to Rust for lower overhead and better concurrency.
- **Disaggregation & PD**: Major architectural shifts in prefill-decode (PD) disaggregation, introducing Mooncake-based hidden-state transfers, Prefill-to-Prefill KV transfers, and DAG-based declarative topology scheduling for diffusion models.
- **Hardware & Quantization**: Expanding Ascend NPU support (W8A8/W4A8 MXFP for Qwen3 MoE), AMD ROCm enhancements (MI300X MLA attention, SharedEP), and widespread MXFP4/MXFP8 quantization pipeline fixes.

## Most important PRs
- **[#32544](https://github.com/sgl-project/sglang/pull/32544)** - Adds massive day-zero support for the Kimi K3 architecture across NVIDIA, AMD (with DCP), and Ascend NPUs. This includes standalone kernels and MoE routing, laying the foundation for serving the Kimi K3 family.
- **[#32566](https://github.com/sgl-project/sglang/pull/32566)** - Drives a major ongoing rewrite moving the core server, request handling, and prefill-decode disaggregation logic into Rust. This shift aims to significantly lower overhead and improve concurrency for high-throughput serving.
- **[#31888](https://github.com/sgl-project/sglang/pull/31888)** - Optimizes Q8-Path and Shared-Path for Q8KV8 FP8 sparse prefill on GLM-5.2 and DeepSeek-V3.2. This significantly improves prefill performance for these models via highly-tuned Triton kernels.
- **[#32550](https://github.com/sgl-project/sglang/pull/32550)** - Replaces the fixed 3-stage role orchestration in diffusion models with a DAG-based declarative topology scheduler. This enables more flexible, efficient, and scalable multi-node diffusion pipelines.
- **[#32482](https://github.com/sgl-project/sglang/pull/32482)** - Introduces SharedEP, a shared-object Expert Parallelism backend for NVIDIA GPUs. This optimizes MoE routing and reduces decode latency for large MoE models.

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#31931](https://github.com/sgl-project/sglang/pull/31931) Optimize DeepSeek-V4 performance on NPU
- [#32731](https://github.com/sgl-project/sglang/pull/32731) Optimize GPT-OSS CP4+EP4 prefill with breakable graphs and single-call zigzag attention
- [#32699](https://github.com/sgl-project/sglang/pull/32699) Fuse MoE-front prep into one launch for Kimi-K3
- [#32219](https://github.com/sgl-project/sglang/pull/32219) Cut spec-v2 host-seam overhead in hybrid-linear MTP decode
- [#32784](https://github.com/sgl-project/sglang/pull/32784) Accelerate CUDA video output finalization for diffusion
- [#32823](https://github.com/sgl-project/sglang/pull/32823) Optimize KDA MTP ns0 memory path for Kimi-K3
- [#32571](https://github.com/sgl-project/sglang/pull/32571) Retire padding blocks for Kimi-K3 KDA MTP verify
- [#32701](https://github.com/sgl-project/sglang/pull/32701) Free KV pages by segment in the paged allocator without a device sync
- [#30511](https://github.com/sgl-project/sglang/pull/30511) Merge HiCache event checks to reduce decode overhead
- [#32383](https://github.com/sgl-project/sglang/pull/32383) Optimize EmbeddingGemma prefill performance
- [#32886](https://github.com/sgl-project/sglang/pull/32886) Skip the target-verify tree mask fill when the backend never reads it
- [#32887](https://github.com/sgl-project/sglang/pull/32887) Fast-path chain-style draft token organization in multi-layer EAGLE
- [#32764](https://github.com/sgl-project/sglang/pull/32764) Free the gemm_ag producer grid from the AR push-counter array for Kimi-K3
- [#32230](https://github.com/sgl-project/sglang/pull/32230) Opt-in custom/quick all-reduce on ROCm for MiniMax-M3
- [#32716](https://github.com/sgl-project/sglang/pull/32716) Optimize VAE cache logic by cache manager for diffusion
- [#32714](https://github.com/sgl-project/sglang/pull/32714) Optimize GPT-OSS CP4+EP4 prefill with breakable graphs and single-call zigzag attention
- [#32526](https://github.com/sgl-project/sglang/pull/32526) Skip inactive target-verify metadata tails for DeepSeek-V4 speculative decoding
- [#32633](https://github.com/sgl-project/sglang/pull/32633) Add GLM-5.2-FP8 bs=1 low-latency serving stack for multi-node GB300
- [#32755](https://github.com/sgl-project/sglang/pull/32755) Tune grid-stride and occupancy for DSA indexer fp8-quant Q kernel
- [#32656](https://github.com/sgl-project/sglang/pull/32656) Fuse target-verify metadata prologue for DeepSeek-V4 speculative decoding
- [#32832](https://github.com/sgl-project/sglang/pull/32832) Bypass caches for peer traffic in ROCm custom all-reduce
- [#32885](https://github.com/sgl-project/sglang/pull/32885) Capture target-verify metadata rebuild inside the decode cuda graph

</details>

<details>
<summary>Kernels & attention (31)</summary>

- [#32636](https://github.com/sgl-project/sglang/pull/32636) Remove unused kernel implementations and stale registry entries
- [#32819](https://github.com/sgl-project/sglang/pull/32819) Optimize PTX prefill kernel for KDA
- [#30825](https://github.com/sgl-project/sglang/pull/30825) Support chunked cached-prefix prefill
- [#32813](https://github.com/sgl-project/sglang/pull/32813) Fuse KV-cache writes for asymmetric K/V
- [#29735](https://github.com/sgl-project/sglang/pull/29735) Support FlashInfer GDN prefill with extra-buffer radix cache
- [#21094](https://github.com/sgl-project/sglang/pull/21094) Vectorize joint/low-confidence decoding and skip redundant attn init
- [#30090](https://github.com/sgl-project/sglang/pull/30090) Add dynamic cuDNN SDPA attention backend for diffusion
- [#28956](https://github.com/sgl-project/sglang/pull/28956) Pack aux hidden states into a preallocated buffer
- [#32304](https://github.com/sgl-project/sglang/pull/32304) Extend hpc_ops dynamic-scheduled decode to bf16
- [#30872](https://github.com/sgl-project/sglang/pull/30872) Enable multimodal prefill BCG for VL and audio models
- [#32427](https://github.com/sgl-project/sglang/pull/32427) Add fill_draft_extend_prepare_buffers_native for NPU
- [#32477](https://github.com/sgl-project/sglang/pull/32477) Skip KV writes to reserved padding slots
- [#32396](https://github.com/sgl-project/sglang/pull/32396) Handle NaNs in fused top-k=1 for EAGLE
- [#32890](https://github.com/sgl-project/sglang/pull/32890) Port standalone Kimi K3 kernels
- [#32480](https://github.com/sgl-project/sglang/pull/32480) Add SM100 relative-bias decode kernel and paged dispatch for FA4
- [#32741](https://github.com/sgl-project/sglang/pull/32741) Add MXFP4 KV Cache Decode Kernel for DSV4 on Hopper
- [#32593](https://github.com/sgl-project/sglang/pull/32593) Enable Helion backend for Kimi Delta-Attention
- [#32779](https://github.com/sgl-project/sglang/pull/32779) Add CUDA fused Triton sparse-MLA prefill backend for DSA
- [#32919](https://github.com/sgl-project/sglang/pull/32919) Fuse GDN decode projection unpack with Conv1D
- [#32692](https://github.com/sgl-project/sglang/pull/32692) Support replayssm with extra buffer for GDN
- [#32667](https://github.com/sgl-project/sglang/pull/32667) Add K/V-gather sequence parallel attention for diffusion
- [#32645](https://github.com/sgl-project/sglang/pull/32645) Fuse GDN decode split and causal conv for Qwen3.5
- [#32474](https://github.com/sgl-project/sglang/pull/32474) Fuse prefill QKV causal convolution and layout for KDA
- [#32577](https://github.com/sgl-project/sglang/pull/32577) Add AITER fused mHC post+pre with cross-layer boundary dispatch for DeepSeek-V4
- [#32673](https://github.com/sgl-project/sglang/pull/32673) Add windowed draft-decode attention for built-in EAGLE / MTP drafts
- [#32443](https://github.com/sgl-project/sglang/pull/32443) Fuse gated RMSNorm and FP8 quantization for Qwen3.5
- [#32417](https://github.com/sgl-project/sglang/pull/32417) Remove FlashInfer and MRoPE host syncs for DFLASH
- [#32920](https://github.com/sgl-project/sglang/pull/32920) Merge attention backends' verify-buffer hooks into one VerifyBuffersToFill
- [#32595](https://github.com/sgl-project/sglang/pull/32595) Support SGLANG_SIMULATE_ACC_LEN for DFLASH
- [#32556](https://github.com/sgl-project/sglang/pull/32556) Autotune flashinfer extend buckets at warmup
- [#32624](https://github.com/sgl-project/sglang/pull/32624) Add TP16/32 support for K3 fused KDA decode

</details>

<details>
<summary>MoE & quantization (18)</summary>

- [#30768](https://github.com/sgl-project/sglang/pull/30768) Add W8A8 MXFP8 quantization for Qwen3 MoE on Ascend NPU
- [#29016](https://github.com/sgl-project/sglang/pull/29016) Add SM90 FP8 MegaMoE support for DeepSeek-V4
- [#31510](https://github.com/sgl-project/sglang/pull/31510) Fix MXFP8 online quantization pipeline
- [#32036](https://github.com/sgl-project/sglang/pull/32036) Unblock mxfp8 block convert on gfx950 for Minimax-M3
- [#32616](https://github.com/sgl-project/sglang/pull/32616) Restore previous division behavior in per-token group quantization
- [#32435](https://github.com/sgl-project/sglang/pull/32435) Load initial expert location metadata on CPU
- [#31393](https://github.com/sgl-project/sglang/pull/31393) Determine topk norm_type through scoring_func on NPU
- [#32619](https://github.com/sgl-project/sglang/pull/32619) Add ROCm SharedEP backend for MoE
- [#32565](https://github.com/sgl-project/sglang/pull/32565) Expand weight loader v2 PR2 coverage
- [#32602](https://github.com/sgl-project/sglang/pull/32602) Add W4A4 MXFP4 quantization support for Qwen3.5 MoE on Ascend NPU
- [#32524](https://github.com/sgl-project/sglang/pull/32524) Add memory-efficient contiguous DeepGEMM path for pure TP on MiniMax-M3
- [#32601](https://github.com/sgl-project/sglang/pull/32601) Add W4A8 MXFP quantization support for Qwen3.5 MoE on Ascend NPU
- [#32581](https://github.com/sgl-project/sglang/pull/32581) Add PRQ KV-cache quantization for Quant-VideoGen
- [#32576](https://github.com/sgl-project/sglang/pull/32576) Drive DSA backend defaulting and validation from a declarative compatibility table
- [#32665](https://github.com/sgl-project/sglang/pull/32665) Add extension points for custom MoE runner backends
- [#32778](https://github.com/sgl-project/sglang/pull/32778) Run native MXFP4 MoE with humming for Hopper on Kimi-K3
- [#32506](https://github.com/sgl-project/sglang/pull/32506) Defer gfx950 A8W8 quantization to AITER
- [#32538](https://github.com/sgl-project/sglang/pull/32538) Support ModelOpt MXFP8 checkpoints
- [#32687](https://github.com/sgl-project/sglang/pull/32687) Add LFM2 MoE tuned config for H200

</details>

<details>
<summary>Model support (23)</summary>

- [#30988](https://github.com/sgl-project/sglang/pull/30988) Support LoRA under the breakable/full prefill CUDA graph
- [#31538](https://github.com/sgl-project/sglang/pull/31538) Support resident layers for DiT diffusion models
- [#32375](https://github.com/sgl-project/sglang/pull/32375) Support EmbeddingGemma
- [#32401](https://github.com/sgl-project/sglang/pull/32401) Support standalone text-only Qwen3.5 checkpoints
- [#31840](https://github.com/sgl-project/sglang/pull/31840) Add minimal DFLASH support for Inkling
- [#32696](https://github.com/sgl-project/sglang/pull/32696) Add regional torch compile for diffusion
- [#32457](https://github.com/sgl-project/sglang/pull/32457) Serve bare Qwen3Model backbone natively as an embedding model
- [#28691](https://github.com/sgl-project/sglang/pull/28691) Add LFM2.5 embedding model support
- [#32421](https://github.com/sgl-project/sglang/pull/32421) Allow load_lora_adapter_from_distributed under dp attention
- [#30780](https://github.com/sgl-project/sglang/pull/30780) Wire Lfm2MoeForCausalLM into the LFM2 serving override tables
- [#32796](https://github.com/sgl-project/sglang/pull/32796) Add Kimi K3 DCP support for AMD
- [#32541](https://github.com/sgl-project/sglang/pull/32541) Support Kimi-K3
- [#32528](https://github.com/sgl-project/sglang/pull/32528) Add native BAGEL multimodal support for diffusion
- [#32848](https://github.com/sgl-project/sglang/pull/32848) Support LingBot-Video MoE
- [#32681](https://github.com/sgl-project/sglang/pull/32681) Add native MiMo-V2.5 multimodal input for rust-server
- [#32883](https://github.com/sgl-project/sglang/pull/32883) Add MageVL multimodal model support
- [#32921](https://github.com/sgl-project/sglang/pull/32921) Add native SANA-Video T2V support
- [#32517](https://github.com/sgl-project/sglang/pull/32517) Support ZAYA1 native transformers checkpoint format
- [#32742](https://github.com/sgl-project/sglang/pull/32742) Add fixed output vocabulary mapping for Qwen2
- [#32584](https://github.com/sgl-project/sglang/pull/32584) Support LoRA under DP attention
- [#32708](https://github.com/sgl-project/sglang/pull/32708) Shard attention LoRA by attn-TP and allow dynamic LoRA with dp attention
- [#32635](https://github.com/sgl-project/sglang/pull/32635) Add Qwen3.5 and GLM-5 support for HCU
- [#32860](https://github.com/sgl-project/sglang/pull/32860) Fuse Wan VAE DupUp3D shortcut add

</details>

<details>
<summary>Parallelism & scheduling (41)</summary>

- [#32612](https://github.com/sgl-project/sglang/pull/32612) Support DCP for Kimi Linear model
- [#30482](https://github.com/sgl-project/sglang/pull/30482) Support interleave strategy for cp v2
- [#32228](https://github.com/sgl-project/sglang/pull/32228) Skip mamba lock during decoding
- [#32115](https://github.com/sgl-project/sglang/pull/32115) Size request capacity by attention DP on MLX
- [#31869](https://github.com/sgl-project/sglang/pull/31869) Honor PP consensus for bootstrap and prealloc
- [#32339](https://github.com/sgl-project/sglang/pull/32339) Enable multi-node custom-AR v2 on a single NVLink clique
- [#27089](https://github.com/sgl-project/sglang/pull/27089) Disable extra NCCL CUDA event synchronization with symm mem
- [#30553](https://github.com/sgl-project/sglang/pull/30553) Enable EPLB after scale-up for elastic-ep
- [#32850](https://github.com/sgl-project/sglang/pull/32850) Emit step trace span for multi-layer draft-extend graph replays
- [#32580](https://github.com/sgl-project/sglang/pull/32580) Per-rank tensor serialization for LoRA under dp_size > 1
- [#32797](https://github.com/sgl-project/sglang/pull/32797) Handle abort requests in PP mode
- [#32267](https://github.com/sgl-project/sglang/pull/32267) Drain NIXL completion notifications before enforcing WaitingForInput timeout
- [#31543](https://github.com/sgl-project/sglang/pull/31543) Pool decode bootstrap HTTP sessions
- [#32620](https://github.com/sgl-project/sglang/pull/32620) Eliminate redundant DSA state transfers for Mooncake
- [#32025](https://github.com/sgl-project/sglang/pull/32025) Shard NIXL connector by destination
- [#32726](https://github.com/sgl-project/sglang/pull/32726) Enable intranode flydsl-a2a for AMD
- [#32851](https://github.com/sgl-project/sglang/pull/32851) Optimize shared Output, Query, and Indexer/Top-K via peer memory for DCP
- [#32478](https://github.com/sgl-project/sglang/pull/32478) Add Prefill-to-Prefill KV transfer over Mooncake
- [#32424](https://github.com/sgl-project/sglang/pull/32424) Implement streaming hidden-state transfer for Mooncake
- [#32564](https://github.com/sgl-project/sglang/pull/32564) Don't release KV pages while Mooncake transfers are in flight
- [#32423](https://github.com/sgl-project/sglang/pull/32423) Integrate hidden-state bootstrap into PD scheduling
- [#32771](https://github.com/sgl-project/sglang/pull/32771) Enable DeepSeek V4 IndexCache with PD, CP, and HiCache coverage
- [#32422](https://github.com/sgl-project/sglang/pull/32422) Add hidden-state transfer primitives and draft injection
- [#32529](https://github.com/sgl-project/sglang/pull/32529) Enable Two-Batch Overlap in Draft Models
- [#32793](https://github.com/sgl-project/sglang/pull/32793) Support PD + DSpark in PP mode
- [#32837](https://github.com/sgl-project/sglang/pull/32837) Support Kimi Linear PD disaggregation with DCP
- [#32514](https://github.com/sgl-project/sglang/pull/32514) Add component_types field to BlockStored for per-component placement tracking
- [#32560](https://github.com/sgl-project/sglang/pull/32560) Add native ncclAllToAll a2a backend with NCCL symmetric memory for DCP
- [#32623](https://github.com/sgl-project/sglang/pull/32623) Add MoRI fabric backend for scale-up KV transfer on AMD
- [#32732](https://github.com/sgl-project/sglang/pull/32732) Support decode radix cache for mamba/SSM hybrid models
- [#32413](https://github.com/sgl-project/sglang/pull/32413) Handle unsupported decode KV retraction
- [#32775](https://github.com/sgl-project/sglang/pull/32775) Add a consecutive-prefill budget to bound decode starvation
- [#32455](https://github.com/sgl-project/sglang/pull/32455) Make LMCache MP store non-blocking on request finish
- [#32909](https://github.com/sgl-project/sglang/pull/32909) Keep decode status thread alive on bad messages for Mooncake
- [#32637](https://github.com/sgl-project/sglang/pull/32637) Optimize delayed sample and mrope position computation
- [#32880](https://github.com/sgl-project/sglang/pull/32880) Bound prefill delayer all-branch delay and decay max_prefill_bs high-watermark
- [#32888](https://github.com/sgl-project/sglang/pull/32888) Fill the chunked-prefill compute budget exactly on AMD gfx95
- [#32911](https://github.com/sgl-project/sglang/pull/32911) Add HRRN scheduler policy to significantly reduce TTFT
- [#32429](https://github.com/sgl-project/sglang/pull/32429) Add zero-copy NVLS multicast to custom-AR v2
- [#32603](https://github.com/sgl-project/sglang/pull/32603) Support MiniMax-M3 sparse KV CPU copy
- [#32795](https://github.com/sgl-project/sglang/pull/32795) Support DCP in TRTLLM MHA decode

</details>

<details>
<summary>Hardware & arch (27)</summary>

- [#26928](https://github.com/sgl-project/sglang/pull/26928) Support GLM-5.1 inference on SM120 (Blackwell Desktop)
- [#32668](https://github.com/sgl-project/sglang/pull/32668) Enable GPT-OSS FlashInfer MXFP4 on SM120
- [#30954](https://github.com/sgl-project/sglang/pull/30954) Allow fused MHC opt-in with standalone TileLang pre disabled on SM120
- [#31747](https://github.com/sgl-project/sglang/pull/31747) Bring HIP compress-state pool into memory_saver KV_CACHE region for DSv4
- [#31739](https://github.com/sgl-project/sglang/pull/31739) Adapt dflash v2 on NPU
- [#31189](https://github.com/sgl-project/sglang/pull/31189) Add Ascend transfer version compatibility
- [#32613](https://github.com/sgl-project/sglang/pull/32613) Add Gemma3RMSNorm.forward_hip to unbreak ROCm
- [#32604](https://github.com/sgl-project/sglang/pull/32604) Support Kimi-K3 on Ascend 910C
- [#32754](https://github.com/sgl-project/sglang/pull/32754) Enable gfx1250 Support
- [#32733](https://github.com/sgl-project/sglang/pull/32733) Support FP8 KV cache on CPU
- [#32451](https://github.com/sgl-project/sglang/pull/32451) Add MLX block paged attention decode for Apple Silicon
- [#32503](https://github.com/sgl-project/sglang/pull/32503) Enable HiCache support on Intel XPU
- [#32500](https://github.com/sgl-project/sglang/pull/32500) Support Ascend Mamba states with FIA and async IO
- [#32908](https://github.com/sgl-project/sglang/pull/32908) Add capability-based Gemma RMSNorm dispatch on NPU
- [#32767](https://github.com/sgl-project/sglang/pull/32767) Add moonmath MLA attention backend with A16W8 decode for CDNA3
- [#32452](https://github.com/sgl-project/sglang/pull/32452) Support HND KV cache layout in CPU offload for MHA
- [#32611](https://github.com/sgl-project/sglang/pull/32611) Enable transcription & audio-understanding for ASR/audio/speech models on XPU
- [#32543](https://github.com/sgl-project/sglang/pull/32543) Enable RDNA (wave32) build with multi-arch warp size for sgl-kernel
- [#32870](https://github.com/sgl-project/sglang/pull/32870) Add MFMA decode GEMM for gfx942/gfx950
- [#32479](https://github.com/sgl-project/sglang/pull/32479) Add optional b12x PCIe all-reduce for SM120
- [#32618](https://github.com/sgl-project/sglang/pull/32618) Add fp8_per_tensor_scaled_mm_cpu kernel
- [#32439](https://github.com/sgl-project/sglang/pull/32439) Add Triton fallback for DSV4 indexer query on ROCm
- [#32495](https://github.com/sgl-project/sglang/pull/32495) Enable non-greedy MTP sampling on NPU
- [#32798](https://github.com/sgl-project/sglang/pull/32798) Add DFLASH support for XPU
- [#32792](https://github.com/sgl-project/sglang/pull/32792) Enable HiSparse hierarchical sparse KV cache on Intel XPU
- [#32512](https://github.com/sgl-project/sglang/pull/32512) Preserve auxiliary state before chained decode lookahead on MLX
- [#32805](https://github.com/sgl-project/sglang/pull/32805) Support Jet-Nemotron-2B on Ascend

</details>

<details>
<summary>API & serving (47)</summary>

- [#32358](https://github.com/sgl-project/sglang/pull/32358) Add Rust server tokenizer manager, ring and runtime
- [#32342](https://github.com/sgl-project/sglang/pull/32342) Add Rust server egress message
- [#32242](https://github.com/sgl-project/sglang/pull/32242) Add Rust server request message
- [#32676](https://github.com/sgl-project/sglang/pull/32676) Support regex compatible with python re lib
- [#32343](https://github.com/sgl-project/sglang/pull/32343) Add Rust server sampling message
- [#32481](https://github.com/sgl-project/sglang/pull/32481) Centralize embedding capabilities and complete OpenAI compatibility
- [#32078](https://github.com/sgl-project/sglang/pull/32078) Opt-in flat response format for prompt top logprobs
- [#30256](https://github.com/sgl-project/sglang/pull/30256) Add Mooncake tenant id support
- [#31417](https://github.com/sgl-project/sglang/pull/31417) Return 400 instead of 500 for unfetchable or unparseable multimodal inputs
- [#31960](https://github.com/sgl-project/sglang/pull/31960) Optional base64 encoding for flat prompt top logprob arrays
- [#32617](https://github.com/sgl-project/sglang/pull/32617) Support parser auto-detection for Kimi K3
- [#32498](https://github.com/sgl-project/sglang/pull/32498) Handle per-item embeddings in cache misses
- [#32710](https://github.com/sgl-project/sglang/pull/32710) Add Rust Tree Core Full Component
- [#32585](https://github.com/sgl-project/sglang/pull/32585) Add sglang rust server Vertex API
- [#32428](https://github.com/sgl-project/sglang/pull/32428) Extract reasoning-request normalization into standalone helpers
- [#32662](https://github.com/sgl-project/sglang/pull/32662) Add experimental Redis-backed KV indexer and bridge
- [#32523](https://github.com/sgl-project/sglang/pull/32523) Add push-based engine load reporting
- [#32682](https://github.com/sgl-project/sglang/pull/32682) Add encoder-aligned windowing for long audio items in realtime ASR
- [#32660](https://github.com/sgl-project/sglang/pull/32660) Report per-token weight-version spans in generation meta info
- [#32729](https://github.com/sgl-project/sglang/pull/32729) Add KV event gap replay for sgl-router
- [#32629](https://github.com/sgl-project/sglang/pull/32629) Add pluggable ScoringPolicy to Selector routing
- [#32689](https://github.com/sgl-project/sglang/pull/32689) Add Responses support
- [#32822](https://github.com/sgl-project/sglang/pull/32822) Add sglang rust server api http utils
- [#32599](https://github.com/sgl-project/sglang/pull/32599) Add sgl router segment cache
- [#32588](https://github.com/sgl-project/sglang/pull/32588) Add generation request semantics to gRPC
- [#32744](https://github.com/sgl-project/sglang/pull/32744) Support draft model in weight daemon
- [#32872](https://github.com/sgl-project/sglang/pull/32872) Add rust server tokenizer, detokenizer, and egress modules
- [#32875](https://github.com/sgl-project/sglang/pull/32875) Add rust server api frame codec and http server entry
- [#32874](https://github.com/sgl-project/sglang/pull/32874) Add rust server ingress tests, guard, and submit modules
- [#32873](https://github.com/sgl-project/sglang/pull/32873) Add rust server ingress request validation and api server common types
- [#32824](https://github.com/sgl-project/sglang/pull/32824) Add sglang rust server abis
- [#32876](https://github.com/sgl-project/sglang/pull/32876) Add rust server native api handlers and runtime threads
- [#32877](https://github.com/sgl-project/sglang/pull/32877) Wire rust server modules into lib, runtime, and tokenizer manager
- [#32865](https://github.com/sgl-project/sglang/pull/32865) Integrate rust server with scheduler, entrypoints, and engine
- [#32826](https://github.com/sgl-project/sglang/pull/32826) Add sglang rust server python part 1
- [#32821](https://github.com/sgl-project/sglang/pull/32821) Runtime attach/detach of HiCache storage backend for UnifiedRadixCache
- [#32891](https://github.com/sgl-project/sglang/pull/32891) NIXL storage registration acquire/release for HiCache
- [#32773](https://github.com/sgl-project/sglang/pull/32773) Add optional admin auth for /flush_cache in Router
- [#32476](https://github.com/sgl-project/sglang/pull/32476) Add canary sentinel verification for unified tree MHA/SWA
- [#32827](https://github.com/sgl-project/sglang/pull/32827) Add sglang rust server python part 2
- [#32864](https://github.com/sgl-project/sglang/pull/32864) Add python foundations for rust server
- [#32488](https://github.com/sgl-project/sglang/pull/32488) Select RunAI shards for MTP draft models
- [#32610](https://github.com/sgl-project/sglang/pull/32610) Propagate tool_result.is_error into the rendered prompt for Anthropic
- [#32501](https://github.com/sgl-project/sglang/pull/32501) Route request to 2 groups base requests lens
- [#32753](https://github.com/sgl-project/sglang/pull/32753) Wire decode-affinity outcome metric in Router
- [#32705](https://github.com/sgl-project/sglang/pull/32705) Scope NIXL clear() to the clearing instance's key suffix
- [#32535](https://github.com/sgl-project/sglang/pull/32535) Add engine load scorer to router

</details>

<details>
<summary>Tests (22)</summary>

- [#32294](https://github.com/sgl-project/sglang/pull/32294) Add NPU attention unit tests
- [#32788](https://github.com/sgl-project/sglang/pull/32788) Add inventory guards and clean benchmark layout
- [#32371](https://github.com/sgl-project/sglang/pull/32371) Fix GLM4-7B-Flash accuracy test configuration and tune Qwen3.6 performance tests
- [#32820](https://github.com/sgl-project/sglang/pull/32820) Clean up DCP tests
- [#32642](https://github.com/sgl-project/sglang/pull/32642) Add benchmark script for HPC-Ops bf16xfp32 router GEMM
- [#32448](https://github.com/sgl-project/sglang/pull/32448) Move fused swiglu tests to test/registered for MLX
- [#31706](https://github.com/sgl-project/sglang/pull/31706) Fix previously flaky test of test_mooncake_ep_small.py
- [#31925](https://github.com/sgl-project/sglang/pull/31925) Skip test_update_weights_from_disk on ROCm
- [#32598](https://github.com/sgl-project/sglang/pull/32598) Add npu unit test for ascend_gdn_backend
- [#32505](https://github.com/sgl-project/sglang/pull/32505) Add unit tests for ascend_torch_native_backend
- [#32917](https://github.com/sgl-project/sglang/pull/32917) Add reproducible request-manifest offline benchmark for diffusion
- [#32649](https://github.com/sgl-project/sglang/pull/32649) Add NPU GSM8K accuracy tests for 7 models
- [#32534](https://github.com/sgl-project/sglang/pull/32534) Improve NPU multi-node test robustness
- [#32628](https://github.com/sgl-project/sglang/pull/32628) Add unit tests for usage_processor and chat_encoding
- [#32675](https://github.com/sgl-project/sglang/pull/32675) Add unit tests for srt/dllm/config.py DllmConfig
- [#32866](https://github.com/sgl-project/sglang/pull/32866) Add tests and eval support for rust server
- [#32416](https://github.com/sgl-project/sglang/pull/32416) Add CPU unit tests for OpenAI utility helpers
- [#32568](https://github.com/sgl-project/sglang/pull/32568) Add Kimi-K3 8-GPU MI35x nightly accuracy CI
- [#32794](https://github.com/sgl-project/sglang/pull/32794) Add unit tests for logprob_result_processor
- [#32570](https://github.com/sgl-project/sglang/pull/32570) Add GLM-5.2-FP8 8-GPU MI35x nightly accuracy CI
- [#32722](https://github.com/sgl-project/sglang/pull/32722) Test GLM-5.2 PD + DP attention + MTP
- [#32829](https://github.com/sgl-project/sglang/pull/32829) Graceful teardown for kv_canary and EAGLE spec fixtures

</details>

<details>
<summary>CI & build (22)</summary>

- [#32760](https://github.com/sgl-project/sglang/pull/32760) Add Kimi K3 docker images
- [#32489](https://github.com/sgl-project/sglang/pull/32489) Add local ZIP uploader for whl releases
- [#31409](https://github.com/sgl-project/sglang/pull/31409) Replace MI325 with MI300 CI Runners
- [#30613](https://github.com/sgl-project/sglang/pull/30613) Add Nightly Test Coverage for Minimax-M3-MXFP8 Accuracy
- [#32735](https://github.com/sgl-project/sglang/pull/32735) Fail lint when a registered file's TestCase classes never run
- [#32679](https://github.com/sgl-project/sglang/pull/32679) Update CI_PERMISSIONS.json
- [#32545](https://github.com/sgl-project/sglang/pull/32545) Clone branch source in Docker images for Kimi-K3
- [#32469](https://github.com/sgl-project/sglang/pull/32469) Fix pip setup in AMD Miles nightly builds
- [#32559](https://github.com/sgl-project/sglang/pull/32559) Update mi35x ROCm image to k3-20260727
- [#32879](https://github.com/sgl-project/sglang/pull/32879) Revert ROCm AITER pin
- [#32453](https://github.com/sgl-project/sglang/pull/32453) Add oulgen to CI_PERMISSIONS.json
- [#32596](https://github.com/sgl-project/sglang/pull/32596) Update sgl-kernel-npu tag
- [#31917](https://github.com/sgl-project/sglang/pull/31917) Update codeowners for NPU quantization
- [#32717](https://github.com/sgl-project/sglang/pull/32717) Update CodeOwner
- [#32608](https://github.com/sgl-project/sglang/pull/32608) Update codeowners
- [#32632](https://github.com/sgl-project/sglang/pull/32632) Run AITER Scout on Saturdays
- [#32871](https://github.com/sgl-project/sglang/pull/32871) Update Cargo.lock for rust sglang-server dependencies
- [#32765](https://github.com/sgl-project/sglang/pull/32765) Test pr32754 for AMD
- [#32458](https://github.com/sgl-project/sglang/pull/32458) Update CI test est_time values
- [#32719](https://github.com/sgl-project/sglang/pull/32719) Re-enable GB300 CI jobs
- [#32438](https://github.com/sgl-project/sglang/pull/32438) Stabilize B580 XPU CI
- [#32643](https://github.com/sgl-project/sglang/pull/32643) Add Kimi K3 ROCm 7.2 nightly image

</details>

<details>
<summary>Docs (20)</summary>

- [#32542](https://github.com/sgl-project/sglang/pull/32542) Add the Kimi-K3 serving cookbook
- [#30614](https://github.com/sgl-project/sglang/pull/30614) Add Ascend A2, A3 basic usage and benchmark results in diffusion cookbook
- [#32835](https://github.com/sgl-project/sglang/pull/32835) Rotate popular models on the landing pages and lead Cookbook nav with Kimi
- [#32763](https://github.com/sgl-project/sglang/pull/32763) Add compute-mamba-ratio skill
- [#32586](https://github.com/sgl-project/sglang/pull/32586) Mark every Kimi-K3 cell in-progress and land Playground Switch base
- [#32639](https://github.com/sgl-project/sglang/pull/32639) Clarify diffusion stage reuse guidance
- [#32592](https://github.com/sgl-project/sglang/pull/32592) Update Kimi-K3 GB200 recipes from measured 4x4 runs
- [#32836](https://github.com/sgl-project/sglang/pull/32836) Add diffusion cookbook model tags
- [#32465](https://github.com/sgl-project/sglang/pull/32465) Add inkling dspark command to cookbook
- [#32590](https://github.com/sgl-project/sglang/pull/32590) Sync LMSYS SGLang blog cards
- [#32834](https://github.com/sgl-project/sglang/pull/32834) Widen the H200 High-Throughput recipe to 4x8 TP32/EP32 for Kimi-K3
- [#32547](https://github.com/sgl-project/sglang/pull/32547) Point Kimi-K3 references to public branch
- [#32661](https://github.com/sgl-project/sglang/pull/32661) Clarify VLM compatibility for Kimi-K3
- [#32647](https://github.com/sgl-project/sglang/pull/32647) Update supported features on ascend npu
- [#32749](https://github.com/sgl-project/sglang/pull/32749) Update feature name to follow code changement on NPU
- [#32799](https://github.com/sgl-project/sglang/pull/32799) Update Inkling cookbook install command
- [#32654](https://github.com/sgl-project/sglang/pull/32654) Update sglang cookbook
- [#32436](https://github.com/sgl-project/sglang/pull/32436) Add OpenAPI specification covering all SGLang endpoint use cases
- [#32414](https://github.com/sgl-project/sglang/pull/32414) Add Reasoning-Aware Compression (RAC) pruning recipe
- [#32857](https://github.com/sgl-project/sglang/pull/32857) Restructure ascend-npus docs into layered navigation

</details>

<details>
<summary>Bugfixes (84)</summary>

- [#32664](https://github.com/sgl-project/sglang/pull/32664) Fix named persistent symmetric buffers for Kimi-K3 fused collectives
- [#32861](https://github.com/sgl-project/sglang/pull/32861) Fix Inkling tool-call parsing recovery, content handling, and streaming
- [#30017](https://github.com/sgl-project/sglang/pull/30017) Fix diffusion output stability on MPS
- [#31902](https://github.com/sgl-project/sglang/pull/31902) Drop prefetched host refill under an un-backed-up parent in UnifiedTree
- [#32104](https://github.com/sgl-project/sglang/pull/32104) Fix Kimi-VL 2D encoder grids
- [#32447](https://github.com/sgl-project/sglang/pull/32447) Fix overlap-loop request bookkeeping and graceful shutdown on MLX
- [#32118](https://github.com/sgl-project/sglang/pull/32118) Fix NVFP4 cuda-graph crash, NVILA batching, CuTe paged-KV zero-size, and Kimi-VL OOM
- [#28370](https://github.com/sgl-project/sglang/pull/28370) Fix invalid escape warnings in tool parsers
- [#32736](https://github.com/sgl-project/sglang/pull/32736) Fix mixed-precision checkpoints silently loading unquantized
- [#32540](https://github.com/sgl-project/sglang/pull/32540) Honor Poolside template thinking defaults for reasoning
- [#31968](https://github.com/sgl-project/sglang/pull/31968) Fix heterogeneous attn-TP KV transfer for replicated GQA heads
- [#32621](https://github.com/sgl-project/sglang/pull/32621) Fix top_k/p sampling issue on AMD code path
- [#30260](https://github.com/sgl-project/sglang/pull/30260) Fix --mm-process-config crash when video config contains
- [#32867](https://github.com/sgl-project/sglang/pull/32867) Count multi-layer draft-extend replays in the fwd-occupancy device timer
- [#31957](https://github.com/sgl-project/sglang/pull/31957) Reject Moss vision metadata mismatches
- [#32818](https://github.com/sgl-project/sglang/pull/32818) Route asymmetric-KV models to fa4 on SM100 and pin MiMoV2 FP8 MoE
- [#32757](https://github.com/sgl-project/sglang/pull/32757) Fix Kimi K3 reasoning leak in the Responses API
- [#31563](https://github.com/sgl-project/sglang/pull/31563) Fix MQA preshuffle layout issue for DeepSeek-V4
- [#31992](https://github.com/sgl-project/sglang/pull/31992) Correct DSA KV memory budget for hisparse
- [#31596](https://github.com/sgl-project/sglang/pull/31596) Materialize Qwen3-VL features on the vision device
- [#32743](https://github.com/sgl-project/sglang/pull/32743) Fix dual-DiT models crash with placeholder weights after compile-time offload
- [#32695](https://github.com/sgl-project/sglang/pull/32695) Size VSA top-k from padded blocks for diffusion
- [#32563](https://github.com/sgl-project/sglang/pull/32563) Fix S3 speculative draft loading
- [#32555](https://github.com/sgl-project/sglang/pull/32555) Fix decode track-save reading the stale tail of the CUDA-graph track buffer
- [#31361](https://github.com/sgl-project/sglang/pull/31361) Prevent self-killing diffusion worker when PID 1 is the real parent
- [#32373](https://github.com/sgl-project/sglang/pull/32373) Fix --hicache-size allocating ~2x host memory on hybrid SWA
- [#32625](https://github.com/sgl-project/sglang/pull/32625) Fix attention backends for models with per-layer head counts
- [#32013](https://github.com/sgl-project/sglang/pull/32013) Fix ModelSlim MXFP4 packed weight loading on NPU
- [#32400](https://github.com/sgl-project/sglang/pull/32400) Enable strict thinking for DeepSeek-V4
- [#27614](https://github.com/sgl-project/sglang/pull/27614) Fix LFM 2 tool parser
- [#32318](https://github.com/sgl-project/sglang/pull/32318) Fix FlashInfer MNNVL workspace size check
- [#32210](https://github.com/sgl-project/sglang/pull/32210) Fix MTP IndexShare warm-up for attention DP and prefill CP on NPU
- [#32071](https://github.com/sgl-project/sglang/pull/32071) Fix Mooncake source-MR lifecycle for multi-TP /send
- [#31591](https://github.com/sgl-project/sglang/pull/31591) Early-release mooncake GPU embeddings and fix gpu_id via scheduler.ps
- [#32809](https://github.com/sgl-project/sglang/pull/32809) Honor weight-check skips for quantized entries
- [#32663](https://github.com/sgl-project/sglang/pull/32663) Fix MoE reduce-scatterv eligibility check
- [#31793](https://github.com/sgl-project/sglang/pull/31793) Disable global-slot shared-expert fusion under per-rank EP backends on AMD
- [#31280](https://github.com/sgl-project/sglang/pull/31280) Fix accuracy for afmoe model introduced by topk refactor on NPU
- [#30742](https://github.com/sgl-project/sglang/pull/30742) Make RowParallelLinear k-size tuple-aware for FP8
- [#32420](https://github.com/sgl-project/sglang/pull/32420) Preserve tensor stride when offloading rollout weights to pinned host memory
- [#32430](https://github.com/sgl-project/sglang/pull/32430) Fix compressed-tensors NVFP4 MoE W13 layout
- [#32389](https://github.com/sgl-project/sglang/pull/32389) Fix prefill suspension caused by delayed negotiate_should_allow_prefill invocation
- [#32157](https://github.com/sgl-project/sglang/pull/32157) Fix per-shard FP8 scale shape for single-GPU fused linears
- [#32022](https://github.com/sgl-project/sglang/pull/32022) Restrict MoE weights to local PP layers for Qwen3.5
- [#32884](https://github.com/sgl-project/sglang/pull/32884) Fix Marlin MoE kernel import
- [#31849](https://github.com/sgl-project/sglang/pull/31849) Keep fused qk-norm-rope out of dynamo tracing
- [#31339](https://github.com/sgl-project/sglang/pull/31339) Prevent ReqTimeStats from being dropped during IPC serialization
- [#32711](https://github.com/sgl-project/sglang/pull/32711) Fix DSv4 MTP condition on NPU graph
- [#31629](https://github.com/sgl-project/sglang/pull/31629) Enable graph capture and MSCCL++ for attention TP groups
- [#32001](https://github.com/sgl-project/sglang/pull/32001) Send expert weights contiguous tensor across cards during EPLB rebalance
- [#32180](https://github.com/sgl-project/sglang/pull/32180) Prevent TBO crash when return_logprob is enabled
- [#32491](https://github.com/sgl-project/sglang/pull/32491) Enforce lifecycle-based admission control in router
- [#32905](https://github.com/sgl-project/sglang/pull/32905) Fix rfork remote instance weight transfer
- [#32567](https://github.com/sgl-project/sglang/pull/32567) Fix Kimi-K3 reasoning parser on elided think close
- [#32450](https://github.com/sgl-project/sglang/pull/32450) Fix hybrid-SSM + radix cache crashes in the auxiliary-state component on MLX
- [#32745](https://github.com/sgl-project/sglang/pull/32745) Fix Qwen3.5 GemmaRMSNorm on Ascend 950
- [#32892](https://github.com/sgl-project/sglang/pull/32892) Complete Mamba sidecar backups after branch reconstruction
- [#32828](https://github.com/sgl-project/sglang/pull/32828) Fix DCP + DSPARK draft KV pool OOB and add static-verify coverage
- [#32658](https://github.com/sgl-project/sglang/pull/32658) Preserve accumulator precision for radix checkpoints in KDA
- [#32740](https://github.com/sgl-project/sglang/pull/32740) Fix ModelOpt mixed-precision MXFP8 loading for Nemotron Nano FP4
- [#32922](https://github.com/sgl-project/sglang/pull/32922) Fix silent greedy fallback in speculative decoding verify on ROCm
- [#32758](https://github.com/sgl-project/sglang/pull/32758) Bound Mooncake synchronous transfer batches for GLM-5.2-NVFP4
- [#32554](https://github.com/sgl-project/sglang/pull/32554) Link JIT modules against the pip CUDA runtime
- [#32539](https://github.com/sgl-project/sglang/pull/32539) Fix tools leaking in the reasoning content for DeepSeek
- [#32768](https://github.com/sgl-project/sglang/pull/32768) Fix Responses reasoning state propagation
- [#32686](https://github.com/sgl-project/sglang/pull/32686) Reduce DeepGEMM warmup buffers below 4096
- [#32460](https://github.com/sgl-project/sglang/pull/32460) Fix TRTLLM MHA CUDA-graph metadata race with the overlap scheduler
- [#32456](https://github.com/sgl-project/sglang/pull/32456) Classify client cancel/disconnect aborts as HTTP 499
- [#32721](https://github.com/sgl-project/sglang/pull/32721) Fix glm47 parser dropping the outer } on object-valued final arguments
- [#32490](https://github.com/sgl-project/sglang/pull/32490) Correct packed FlashInfer top-k and backend selection semantics
- [#32894](https://github.com/sgl-project/sglang/pull/32894) Support ByteDance/Ouro-1.4B via Transformers backend fallback
- [#32670](https://github.com/sgl-project/sglang/pull/32670) Fuse high-rank RMSNorm and guard mixed-dtype weights for Gemma3
- [#32522](https://github.com/sgl-project/sglang/pull/32522) Render tool_reference schema regardless of tool_result part order
- [#32852](https://github.com/sgl-project/sglang/pull/32852) Fix double Mamba ping-pong flip after spec verify on NPU
- [#32600](https://github.com/sgl-project/sglang/pull/32600) Fix partial pinned offload rollback
- [#32644](https://github.com/sgl-project/sglang/pull/32644) Restore serialized Marlin checkpoint support
- [#32558](https://github.com/sgl-project/sglang/pull/32558) Fix KV metrics token to block capacity reporting
- [#32782](https://github.com/sgl-project/sglang/pull/32782) Disable prefill CUDA graph for the whole trtllm_mla backend family
- [#32858](https://github.com/sgl-project/sglang/pull/32858) Fix DCP KV head mapping for GQA models
- [#32839](https://github.com/sgl-project/sglang/pull/32839) Fix DeepSeek-V4 fused-RMS FP8 scale metadata on gfx950
- [#32513](https://github.com/sgl-project/sglang/pull/32513) Thread LTX-2 linear prefixes for ModelOpt NVFP4
- [#32780](https://github.com/sgl-project/sglang/pull/32780) Guard paged allocator before kernel launch
- [#32859](https://github.com/sgl-project/sglang/pull/32859) Guard host-list token_ids_logprobs normalization
- [#32849](https://github.com/sgl-project/sglang/pull/32849) Fix the AITER DSA MLA decode path for GLM5.2 on ROCm
- [#32902](https://github.com/sgl-project/sglang/pull/32902) Fix Llama 4 FA3 local attention with paged KV cache
- [#32454](https://github.com/sgl-project/sglang/pull/32454) Fix prefill delayer timeout rank divergence

</details>

<details>
<summary>Refactors (14)</summary>

- [#32812](https://github.com/sgl-project/sglang/pull/32812) Put the gemm_ar kernels back in-tree and fold the PTX headers into their consumers for Kimi-K3
- [#32651](https://github.com/sgl-project/sglang/pull/32651) Remove stale kernels and dead code for diffusion
- [#32484](https://github.com/sgl-project/sglang/pull/32484) Move /mem_cache/unifed_cache_component dir to /mem_cache/unified_cache
- [#32709](https://github.com/sgl-project/sglang/pull/32709) Remove dead allocator backup_state / restore_state
- [#32881](https://github.com/sgl-project/sglang/pull/32881) Remove unused multi_layer_draft_forward_cg module
- [#32694](https://github.com/sgl-project/sglang/pull/32694) Move sampling tokenizer validation helper
- [#32496](https://github.com/sgl-project/sglang/pull/32496) Tidy server_args.py section grouping and drop unused alias
- [#32688](https://github.com/sgl-project/sglang/pull/32688) Clean up array-like msgspec structs
- [#32502](https://github.com/sgl-project/sglang/pull/32502) Move mamba-max-states-per-path validation into _handle_mamba_backend
- [#32842](https://github.com/sgl-project/sglang/pull/32842) Remove unreachable AOT headers
- [#32415](https://github.com/sgl-project/sglang/pull/32415) Split multimodal scheduling from mm_utils
- [#32912](https://github.com/sgl-project/sglang/pull/32912) Make BaseTpWorker a runner-free backend boundary on MLX
- [#32713](https://github.com/sgl-project/sglang/pull/32713) Migrate --disable-cuda-graph to per-phase --cuda-graph-backend-{decode,prefill}=disabled
- [#32434](https://github.com/sgl-project/sglang/pull/32434) Consolidate compiled-kernel caches under SGLANG_CACHE_DIR

</details>

<details>
<summary>Other (1)</summary>

- [#32672](https://github.com/sgl-project/sglang/pull/32672) Follow up on post-merge review

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: e9174785b7493ef87304ec9f44db646ae74125f515a63843dc4474d66bf42269 -->
