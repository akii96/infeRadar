# sglang: PR digest (2026-07-29 to 2026-08-02)

_228 merged, 339 newly opened - source sgl-project/sglang, generated 2026-08-02T22:25:48Z_

## TL;DR
- **Model Focus**: DeepSeek-V4/V3.2 dominated attention with major FP8/MXFP4 sparse prefill and MoE optimizations, followed by Kimi K3 (standalone kernels, DCP, reasoning) and MiniMax-M3 (SM100 FP8 attention, NPU adaptation).
- **Performance & Kernels**: Significant kernel work landed for SM120/SM100 (FA4 kernels, FlashInfer MXFP4), alongside fused MoE-front prep, zigzag attention for CP4+EP4, and AITER sparse-MLA for AMD ROCm.
- **Rust Server**: A massive ongoing effort to implement a Rust-based SGLang server, merging tokenizer, egress/ingress, and API handlers, with newly opened work on OpenAI APIs and PD disaggregation.
- **Speculative Decoding & Parallelism**: Major in-progress work on Decode-Verify-Rollback for GDN, EAGLE3 speculative decoding with pipeline parallelism, and extensive DCP (Distributed Context Parallelism) optimizations.
- **Hardware & Diffusion**: Broadened hardware support (Ascend 950 NPU, Intel XPU FP8 KV cache, AMD gfx1250) and expanded diffusion model capabilities (MiniMax-H3, LingBot-Video, SANA-Video).

## Most important PRs
- **[#31778](https://github.com/sgl-project/sglang/pull/31778)** Enhances Ascend NPU support and CUDA graph features across the stack, touching attention, MoE, and speculative decoding in a massive 217k-line update.
- **[#32796](https://github.com/sgl-project/sglang/pull/32796)** Brings Distributed Context Parallelism (DCP) to Kimi K3 on AMD hardware in a huge in-progress effort spanning over 300 files.
- **[#32890](https://github.com/sgl-project/sglang/pull/32890)** Ports standalone Kimi K3 kernels in-tree, enabling advanced attention, MoE, and quantization features for the Kimi architecture.
- **[#33101](https://github.com/sgl-project/sglang/pull/33101)** Proposes EAGLE3 speculative decoding support combined with pipeline parallelism, a major architectural addition for draft-model scaling.
- **[#31888](https://github.com/sgl-project/sglang/pull/31888)** Delivers critical Q8-path and shared-path optimizations for FP8 sparse prefill on DeepSeek-V3.2 and GLM-5.2.

## More changes by area

<details>
<summary>Performance (35)</summary>

- [#32731](https://github.com/sgl-project/sglang/pull/32731) Optimize GPT-OSS CP4+EP4 prefill with breakable graphs and single-call zigzag attention
- [#31854](https://github.com/sgl-project/sglang/pull/31854) perf(diffusion): CUDA-IPC zero-staging all-to-all for 2-rank Ulysses
- [#32699](https://github.com/sgl-project/sglang/pull/32699) perf(kimi-k3): fuse MoE-front prep (route + trtllm pack + mxfp8 quant) into one launch
- [#32223](https://github.com/sgl-project/sglang/pull/32223) [perf] Assemble flat prompt top logprobs scheduler-side as numpy arrays
- [#32784](https://github.com/sgl-project/sglang/pull/32784) [diffusion] optimization: accelerate CUDA video output finalization
- [#32823](https://github.com/sgl-project/sglang/pull/32823) perf(kimi-k3): optimize KDA MTP ns0 memory path
- [#32701](https://github.com/sgl-project/sglang/pull/32701) [Perf] Free KV pages by segment in the paged allocator without a device sync
- [#30511](https://github.com/sgl-project/sglang/pull/30511) [HiCache] Merge HiCache event checks to reduce decode overhead
- [#32886](https://github.com/sgl-project/sglang/pull/32886) [Perf] Skip the target-verify tree mask fill when the backend never reads it
- [#32887](https://github.com/sgl-project/sglang/pull/32887) [Perf] Fast-path chain-style draft token organization in multi-layer EAGLE
- [#32697](https://github.com/sgl-project/sglang/pull/32697) perf(diffusion): decode Wan VAE in BF16
- [#32315](https://github.com/sgl-project/sglang/pull/32315) [AMD] Speed up DSV4 MoE weight loading from mmap views
- [#32483](https://github.com/sgl-project/sglang/pull/32483) perf(hisparse): eliminate redundant swap output fill
- [#31128](https://github.com/sgl-project/sglang/pull/31128) [Perf][DSA] Pass topk_length to flash_mla_sparse_fwd in the sparse attention path
- [#32230](https://github.com/sgl-project/sglang/pull/32230) [AMD] MiniMax-M3: opt-in custom/quick all-reduce on ROCm
- [#32764](https://github.com/sgl-project/sglang/pull/32764) perf(kimi-k3): free the gemm_ag producer grid from the AR push-counter array
- [#32716](https://github.com/sgl-project/sglang/pull/32716) enhance(diffusion): optmize vae cache logic by cache manager
- [#32714](https://github.com/sgl-project/sglang/pull/32714) [PoC] Optimize GPT-OSS CP4+EP4 prefill with breakable graphs and single-call zigzag attention
- [#33236](https://github.com/sgl-project/sglang/pull/33236) [Perf][DSV4] Remove prefill CP KV and compressor materialization
- [#32975](https://github.com/sgl-project/sglang/pull/32975) perf: add fused norm + RoPE + uniform fp8 store for TRT-LLM DSv4 sparse attention
- [#32935](https://github.com/sgl-project/sglang/pull/32935) [AMD] perf: fuse Kimi MLA projection and MXFP4 value quantization
- [#33290](https://github.com/sgl-project/sglang/pull/33290) perf(gdn): fuse Q/K L2 normalization on AMD
- [#33293](https://github.com/sgl-project/sglang/pull/33293) perf: fuse GraniteMoe scaled residual RMSNorm
- [#32963](https://github.com/sgl-project/sglang/pull/32963) [NVIDIA] Skip fusion of the post-experts all-reduce under hybrid MoE EP+TP
- [#33034](https://github.com/sgl-project/sglang/pull/33034) perf(gemma4): replace dense image masks with spans
- [#33009](https://github.com/sgl-project/sglang/pull/33009) perf: compact sparse logit bias storage
- [#33047](https://github.com/sgl-project/sglang/pull/33047) [dLLM] Cut per-step host overhead in the dLLM extend path
- [#32755](https://github.com/sgl-project/sglang/pull/32755) [Perf] Occupancy tuning for DSA indexer fp8-quant Q kernel
- [#33209](https://github.com/sgl-project/sglang/pull/33209) Reduce the padding overhead of unaligned MXFP8 GEMM shapes
- [#32832](https://github.com/sgl-project/sglang/pull/32832) [AMD] [sgl-kernel] Bypass caches for peer traffic in ROCm custom all-reduce
- [#32946](https://github.com/sgl-project/sglang/pull/32946) [Perf][LMCache] Skip redundant MP prefix lookups
- [#32860](https://github.com/sgl-project/sglang/pull/32860) [diffusion] fuse Wan VAE DupUp3D shortcut add
- [#33062](https://github.com/sgl-project/sglang/pull/33062) [qwen3.5] perf: Skip the GDN qkvzba split kernel on single-token forwards
- [#33220](https://github.com/sgl-project/sglang/pull/33220) [CUDA Graph] Reduce memory by reusing a process-wide capture stream
- [#33085](https://github.com/sgl-project/sglang/pull/33085) perf(hisparse): 128-bit non-temporal swap-in copy on ROCm

</details>

<details>
<summary>Kernels & attention (40)</summary>

- [#32819](https://github.com/sgl-project/sglang/pull/32819) feat(kda): optimize PTX prefill kernel
- [#32842](https://github.com/sgl-project/sglang/pull/32842) [Kernel] Remove unreachable AOT headers
- [#30971](https://github.com/sgl-project/sglang/pull/30971) [minimax-m3] fp8 attention GEMMs on SM100 (fp8_e4m3 KV + trtllm_mha)
- [#33023](https://github.com/sgl-project/sglang/pull/33023) feat(inkling): migrate short convs onto the ShortConv attention backend
- [#32692](https://github.com/sgl-project/sglang/pull/32692) [gdn] support replayssm with extra buffer
- [#32971](https://github.com/sgl-project/sglang/pull/32971) [unified-memory] Support MLA-hybrid-Mamba (Kimi-Linear) on the Triton backend
- [#30756](https://github.com/sgl-project/sglang/pull/30756) Integrate pplx a2a backend
- [#32972](https://github.com/sgl-project/sglang/pull/32972) [unified-memory] Let Kimi-Linear use the paged MLA attention backends
- [#32813](https://github.com/sgl-project/sglang/pull/32813) [Kernel] Fuse KV-cache writes for asymmetric K/V (head_dim != v_head_dim)
- [#32920](https://github.com/sgl-project/sglang/pull/32920) [Spec] Compact the target-verify mask when nothing reads it
- [#33116](https://github.com/sgl-project/sglang/pull/33116) [Inkling] Hold the short-conv per-step state on one metadata struct
- [#33046](https://github.com/sgl-project/sglang/pull/33046) [unified-memory] Support fa3, the default MLA backend on pre-Blackwell hosts
- [#21094](https://github.com/sgl-project/sglang/pull/21094) [DLLM] vectorized joint/low-confidence decoding and skip redundant attn init
- [#32477](https://github.com/sgl-project/sglang/pull/32477) [Kernel] Skip KV writes to reserved padding slots
- [#32641](https://github.com/sgl-project/sglang/pull/32641) [AMD] Add triton topk renorm kernel and enable renorm CI unittest
- [#25545](https://github.com/sgl-project/sglang/pull/25545) [Spec] Add `trtllm_mha` support for Gemma 4 MTP draft attention backend
- [#32947](https://github.com/sgl-project/sglang/pull/32947) Glm52 dsa fallback
- [#32991](https://github.com/sgl-project/sglang/pull/32991) feat(attention): add architecture-owned SM12x FA4 kernels
- [#33102](https://github.com/sgl-project/sglang/pull/33102) [gdn] fused replayssm ring write into flashinfer gdn mtp verify kernel
- [#33216](https://github.com/sgl-project/sglang/pull/33216) kernel: port CUTLASS fp8_scaled_mm to JIT and expand SM120 M tiles
- [#32741](https://github.com/sgl-project/sglang/pull/32741) [RFC][WIP] MXFP4 KV Cache Decode Kernel for DSV4 on Hopper
- [#32961](https://github.com/sgl-project/sglang/pull/32961) [RFC] Attune: automated pre-flight attention-backend tuner
- [#33205](https://github.com/sgl-project/sglang/pull/33205) [Kernel] Unify BaseFusedOp and MultiPlatformOp dispatch
- [#32779](https://github.com/sgl-project/sglang/pull/32779) [SM120&90] Add CUDA fused Triton sparse-MLA prefill backend for DSA
- [#32919](https://github.com/sgl-project/sglang/pull/32919) Fuse GDN decode projection unpack with Conv1D
- [#33135](https://github.com/sgl-project/sglang/pull/33135) [GPT-OSS] Support FlashInfer A2A and routed MoE runner
- [#33073](https://github.com/sgl-project/sglang/pull/33073) [Kimi-K3] Fuse NVIDIA KDA prefill staging
- [#33070](https://github.com/sgl-project/sglang/pull/33070) [Kimi-K3] Share replicated-Q weight storage
- [#33072](https://github.com/sgl-project/sglang/pull/33072) [Kimi-K3] Avoid temporal-state copies on prefix restore
- [#33069](https://github.com/sgl-project/sglang/pull/33069) [Kimi-K3] Add direct-final NVLS Query publication
- [#33226](https://github.com/sgl-project/sglang/pull/33226) Add FlashInfer prefill context parallelism
- [#33288](https://github.com/sgl-project/sglang/pull/33288) [dsv4] Bound C4 indexer logits peak memory via varlen routing query-axis chunking
- [#32973](https://github.com/sgl-project/sglang/pull/32973) feat: enable MTP with DSv4 TRT-LLM Sparse Attention
- [#33071](https://github.com/sgl-project/sglang/pull/33071) [Kimi-K3] Enable fused KDA decode for TP4
- [#33137](https://github.com/sgl-project/sglang/pull/33137) [CP] Fuse zigzag attention into a single call
- [#33222](https://github.com/sgl-project/sglang/pull/33222) [Kernel] Add split-K tactics to CuTe DSL TGV BF16 GEMM for large-K small-N shapes
- [#33237](https://github.com/sgl-project/sglang/pull/33237) feat(dsa): adopt fused FlashInfer page-table top-k
- [#33068](https://github.com/sgl-project/sglang/pull/33068) amd: fuse quantized in_proj layers in Qwen3.5
- [#33161](https://github.com/sgl-project/sglang/pull/33161) [NPU][dLLM] Stop materializing fp32 [tokens, vocab] logits in the denoise step
- [#33175](https://github.com/sgl-project/sglang/pull/33175) [Attention] Reshape the fused-QKV q slice for FA3 instead of copying it

</details>

<details>
<summary>MoE & quantization (17)</summary>

- [#30768](https://github.com/sgl-project/sglang/pull/30768) [llm][npu][quant] Add W8A8 MXFP8 quantization for Qwen3 MoE on Ascend NPU
- [#32668](https://github.com/sgl-project/sglang/pull/32668) Enable GPT-OSS FlashInfer MXFP4 on SM120
- [#29016](https://github.com/sgl-project/sglang/pull/29016) Add SM90 FP8 MegaMoE support for DeepSeek-V4
- [#31220](https://github.com/sgl-project/sglang/pull/31220) Qwen3.5-MoE: support modelopt_fp4 checkpoints that quantize attention
- [#31382](https://github.com/sgl-project/sglang/pull/31382) [Qwen3.5][MTP] Support FlashInfer CuTe DSL for online NVFP4 draft MoE
- [#31510](https://github.com/sgl-project/sglang/pull/31510) Fixing MXFP8 online quantization pipeline
- [#32843](https://github.com/sgl-project/sglang/pull/32843) [Quant] Keep the flashinfer_deepgemm FP8 GEMM to 1 <= M < 32
- [#32036](https://github.com/sgl-project/sglang/pull/32036) [AMD] Minimax-M3 : unblock mxfp8 block convert on gfx950
- [#32994](https://github.com/sgl-project/sglang/pull/32994) Add flashinfer rmsnorm + quant fusion support SM90, SM100, SM120
- [#33208](https://github.com/sgl-project/sglang/pull/33208) [MXFP8] Use FlashInfer CUTLASS for dense GEMM on SM120, delete Triton path
- [#33128](https://github.com/sgl-project/sglang/pull/33128) Support DeepGEMM for standard MoE dispatch
- [#33104](https://github.com/sgl-project/sglang/pull/33104) [NVIDiA][MoE][FP4] Enable NVFP4 shared-expert fusion for FlashInfer TRTLLM-gen kernels
- [#32944](https://github.com/sgl-project/sglang/pull/32944) [MoE] Fuse swiglu moe up gemm epilogue
- [#33115](https://github.com/sgl-project/sglang/pull/33115) [ModelOpt FP4] Support online MoE weight quantization
- [#33278](https://github.com/sgl-project/sglang/pull/33278) Support MXFP8 dense Marlin W8A16 on SM80/SM90
- [#32778](https://github.com/sgl-project/sglang/pull/32778) feat(kimi-k3): run native MXFP4 MoE with humming for hopper
- [#33274](https://github.com/sgl-project/sglang/pull/33274) Add H20 FP8 fused MoE Triton configs for Qwen3.5-397B

</details>

<details>
<summary>Model support (14)</summary>

- [#33275](https://github.com/sgl-project/sglang/pull/33275) [diffusion] model: support minimax-h3
- [#30211](https://github.com/sgl-project/sglang/pull/30211) [diffusion] encoder_parallel: unify encoder folding and batch data-parallel encoding
- [#31538](https://github.com/sgl-project/sglang/pull/31538) [diffusion] support resident layers for DiT
- [#32696](https://github.com/sgl-project/sglang/pull/32696) feat(diffusion): add regional torch compile
- [#31989](https://github.com/sgl-project/sglang/pull/31989) feat: Support nvidia/MiniMax-M3-NVFP4
- [#28691](https://github.com/sgl-project/sglang/pull/28691) Add LFM2.5 embedding model support
- [#32848](https://github.com/sgl-project/sglang/pull/32848) [diffusion][model] Support LingBot-Video MoE: image-to-video, text-to-image, refiner, and prompt rewriting
- [#33182](https://github.com/sgl-project/sglang/pull/33182) [Model] Add Boogu-Image base T2I support
- [#33122](https://github.com/sgl-project/sglang/pull/33122) [Diffusion] Add Lumina-Image-2.0 (NextDiT) support
- [#32921](https://github.com/sgl-project/sglang/pull/32921) [diffusion][model] Add native SANA-Video T2V support
- [#32883](https://github.com/sgl-project/sglang/pull/32883) [Model] Add MageVL multimodal model support
- [#32979](https://github.com/sgl-project/sglang/pull/32979) [Model] Apertus 1.5
- [#33156](https://github.com/sgl-project/sglang/pull/33156) Add SGLang support for GraniteSWA and GraniteMoeSWA models
- [#33140](https://github.com/sgl-project/sglang/pull/33140) Add DeepSeek V4 Flash 0731 reasoning effort support

</details>

<details>
<summary>Parallelism & scheduling (40)</summary>

- [#29173](https://github.com/sgl-project/sglang/pull/29173) feat: Session-reference-aware Unified Radix Cache for agentic multi-turn workloads
- [#32612](https://github.com/sgl-project/sglang/pull/32612) Support DCP for Kimi Linear model
- [#32837](https://github.com/sgl-project/sglang/pull/32837) feat: support Kimi Linear PD disaggregation with DCP
- [#30482](https://github.com/sgl-project/sglang/pull/30482) [4/N][CP] Support interleave strategy for cp v2
- [#32828](https://github.com/sgl-project/sglang/pull/32828) [Kimi] Support DCP + DSpark (ported from kimi-k3 branch)
- [#33112](https://github.com/sgl-project/sglang/pull/33112) [Feat] DCP + HiCache L2 Support (ported from kimi-k3)
- [#31987](https://github.com/sgl-project/sglang/pull/31987) [BCG][3/N] Enable bcg on dsa & deepep a2a backend
- [#32228](https://github.com/sgl-project/sglang/pull/32228) Skip mamba lock during decoding
- [#29735](https://github.com/sgl-project/sglang/pull/29735) [GDN] Support FlashInfer GDN prefill with extra-buffer radix cache
- [#32708](https://github.com/sgl-project/sglang/pull/32708) Split #32584 into 2/2: [LoRA] Shard attention LoRA by attn-TP and allow dynamic LoRA with dp attention
- [#32115](https://github.com/sgl-project/sglang/pull/32115) [MLX] Size request capacity by attention DP
- [#31869](https://github.com/sgl-project/sglang/pull/31869) [PD+PP] Honor PP consensus for bootstrap and prealloc
- [#27089](https://github.com/sgl-project/sglang/pull/27089) Disable extra NCCL CUDA event synchronization with symm mem
- [#30553](https://github.com/sgl-project/sglang/pull/30553) [2/N] elastic-ep: Enable EPLB after scale-up
- [#32707](https://github.com/sgl-project/sglang/pull/32707) Split #32584 into 1/2: [LoRA] Guard DP-attention idle forwards against stale LoRA batch state
- [#32595](https://github.com/sgl-project/sglang/pull/32595) Support SGLANG_SIMULATE_ACC_LEN for DFLASH
- [#32797](https://github.com/sgl-project/sglang/pull/32797) [PD] Handle abort requests in PP mode
- [#32620](https://github.com/sgl-project/sglang/pull/32620) Eliminate redundant DSA state transfers (Mooncake)
- [#32025](https://github.com/sgl-project/sglang/pull/32025) [PD] NIXL connector: shard by destination
- [#33111](https://github.com/sgl-project/sglang/pull/33111) SGLang scale-down number of processes.
- [#32851](https://github.com/sgl-project/sglang/pull/32851) [DCP] Optimize shared Output, Query, and Indexer/Top-K via peer memory
- [#33295](https://github.com/sgl-project/sglang/pull/33295) feat(spec): add ECHO for EAGLE3
- [#33218](https://github.com/sgl-project/sglang/pull/33218) [PD Disagg][HiSparse] Treat the CPU KV buffer as RadixCache L1
- [#32771](https://github.com/sgl-project/sglang/pull/32771) [Feature] Enable DeepSeek V4 IndexCache with PD, CP, and HiCache coverage
- [#33249](https://github.com/sgl-project/sglang/pull/33249) [MoonEP] BF16 PoC integration for Kimi-K3
- [#32793](https://github.com/sgl-project/sglang/pull/32793) [Feature] PP Support PD + DSpark
- [#33136](https://github.com/sgl-project/sglang/pull/33136) [CP] Support breakable CUDA graphs for zigzag strategy
- [#33036](https://github.com/sgl-project/sglang/pull/33036) [diffusion] feat: overlap declared-parallel pipeline stages
- [#33091](https://github.com/sgl-project/sglang/pull/33091) [unified-memory] Stop eviction when shared allocation capacity is sufficient
- [#32732](https://github.com/sgl-project/sglang/pull/32732) [P/D disagg] Support decode radix cache for mamba/SSM hybrid models (KDA/MLA)
- [#33043](https://github.com/sgl-project/sglang/pull/33043) Support PD disaggregation with DCP + DSPARK
- [#33239](https://github.com/sgl-project/sglang/pull/33239) spec: give the v2 draft workers their own ServerArgs copy
- [#33196](https://github.com/sgl-project/sglang/pull/33196) [dLLM] Schedule dLLM prefill and decode rows into one mixed round
- [#33190](https://github.com/sgl-project/sglang/pull/33190) [dLLM] Run several denoise forwards per scheduled FDFO round
- [#32795](https://github.com/sgl-project/sglang/pull/32795) Support DCP in TRTLLM MHA decode
- [#32911](https://github.com/sgl-project/sglang/pull/32911) [Scheduler] Add HRRN schedule policy to significantly reduce TTFT
- [#32997](https://github.com/sgl-project/sglang/pull/32997) [PD] mori: support DCP KV relayout in the moriio transfer backend
- [#33284](https://github.com/sgl-project/sglang/pull/33284) [Spec] Gate GLM-5.2 MTP index sharing by backend capability
- [#33121](https://github.com/sgl-project/sglang/pull/33121) [NemotronH] Support EPLB
- [#32775](https://github.com/sgl-project/sglang/pull/32775) Add a consecutive-prefill budget to bound decode starvation

</details>

<details>
<summary>Hardware & arch (22)</summary>

- [#31948](https://github.com/sgl-project/sglang/pull/31948) [NPU] Enable automatic ascend_attn selection for vision attention and graph runners
- [#31747](https://github.com/sgl-project/sglang/pull/31747) [AMD] DSv4: bring HIP compress-state pool into the memory_saver KV_CACHE region
- [#31739](https://github.com/sgl-project/sglang/pull/31739) [NPU] adapt dflash v2 on npu
- [#31221](https://github.com/sgl-project/sglang/pull/31221) [AMD] Derive AITER verify tokens-per-req from input shape
- [#32941](https://github.com/sgl-project/sglang/pull/32941) [minimax m3][npu]Adaptation of Minimax M3(w8a8) for NPU platforms [1/2]
- [#32726](https://github.com/sgl-project/sglang/pull/32726) [AMD] Enable intranode flydsl-a2a
- [#32754](https://github.com/sgl-project/sglang/pull/32754) [AMD] Enable gfx1250 Support
- [#32733](https://github.com/sgl-project/sglang/pull/32733) [CPU] Support FP8 KV cache
- [#33089](https://github.com/sgl-project/sglang/pull/33089) [NPU] Add sparsity-driven KV offload for DeepSeek DSA on Ascend
- [#32984](https://github.com/sgl-project/sglang/pull/32984) [MLX] Upgrade Torch 2.13 and clarify bridge ownership
- [#33030](https://github.com/sgl-project/sglang/pull/33030) [NPU] add Ascend 950 (Atlas A5) backend paths for DeepSeek-V4
- [#33022](https://github.com/sgl-project/sglang/pull/33022) [ROCm] Use the AITER sparse-MLA kernel for DSA prefill and decode
- [#32978](https://github.com/sgl-project/sglang/pull/32978) [ROCm] Add the AITER sparse-MLA kernel for DSA decode as option
- [#33113](https://github.com/sgl-project/sglang/pull/33113) [AMD] Add AITER HIP backend for packed GDN decode on gfx950
- [#32767](https://github.com/sgl-project/sglang/pull/32767) [AMD] Add moonmath MLA attention backend with A16W8 decode for CDNA3 (MI300X)
- [#33040](https://github.com/sgl-project/sglang/pull/33040) [minimax m3][npu]Adaptation of Minimax M3(w8a8) for NPU platforms [2/2]
- [#32870](https://github.com/sgl-project/sglang/pull/32870) [AMD] Add MFMA decode GEMM for gfx942/gfx950
- [#32798](https://github.com/sgl-project/sglang/pull/32798) DFLASH support added for XPU
- [#32792](https://github.com/sgl-project/sglang/pull/32792) [XPU]Enable HiSparse hierarchical sparse KV cache on Intel XPU
- [#32974](https://github.com/sgl-project/sglang/pull/32974) [AMD] Enable Mori-EP on kimi-k3
- [#32964](https://github.com/sgl-project/sglang/pull/32964) [AMD] Add gfx1201 fallbacks for failing MoE kernels
- [#32805](https://github.com/sgl-project/sglang/pull/32805) [NPU] Support Jet-Nemotron-2B on Ascend

</details>

<details>
<summary>API & serving (44)</summary>

- [#32872](https://github.com/sgl-project/sglang/pull/32872) add the rust server tokenizer, detokenizer, and egress modules
- [#33025](https://github.com/sgl-project/sglang/pull/33025) [Kimi K3] Add reasoning, tool-call, and OpenAI serving support
- [#32358](https://github.com/sgl-project/sglang/pull/32358) sglang rust server tokenizer manager, ring and runtime
- [#32342](https://github.com/sgl-project/sglang/pull/32342) sglang rust server egress message
- [#32242](https://github.com/sgl-project/sglang/pull/32242) sglang rust server request message
- [#29799](https://github.com/sgl-project/sglang/pull/29799) support rust sglang server
- [#30177](https://github.com/sgl-project/sglang/pull/30177) [Feature] Support return_hidden_states="last"
- [#32343](https://github.com/sgl-project/sglang/pull/32343) sglang rust server sampling message
- [#32875](https://github.com/sgl-project/sglang/pull/32875) add the rust server api frame codec and http server entry
- [#32874](https://github.com/sgl-project/sglang/pull/32874) add the rust server ingress tests, guard, and submit modules
- [#32873](https://github.com/sgl-project/sglang/pull/32873) add the rust server ingress request validation and api server common types
- [#32481](https://github.com/sgl-project/sglang/pull/32481) embedding: centralize capabilities and complete OpenAI compatibility
- [#32876](https://github.com/sgl-project/sglang/pull/32876) add the rust server native api handlers and runtime threads
- [#32877](https://github.com/sgl-project/sglang/pull/32877) wire the rust server modules into lib, runtime, and tokenizer manager
- [#30256](https://github.com/sgl-project/sglang/pull/30256) Add Mooncake tenant id support
- [#33243](https://github.com/sgl-project/sglang/pull/33243) feat(sgl-router): forward per-request attribution headers on the cache-sim /ingest_ids tee
- [#31859](https://github.com/sgl-project/sglang/pull/31859) Support fastsafetensors no-GDS loading and page-cache release
- [#31960](https://github.com/sgl-project/sglang/pull/31960) [feat] Optional base64 encoding for the flat prompt top logprob arrays
- [#30903](https://github.com/sgl-project/sglang/pull/30903) feat: log multimodal encoder DP tradeoffs
- [#32672](https://github.com/sgl-project/sglang/pull/32672) Follow up on #30157 post-merge review
- [#32710](https://github.com/sgl-project/sglang/pull/32710) [RFC] Rust Tree Core Full Component
- [#33103](https://github.com/sgl-project/sglang/pull/33103) feat: rust sglang server openai apis
- [#32927](https://github.com/sgl-project/sglang/pull/32927) feat(load-monitor): add Router-side engine load monitoring
- [#32729](https://github.com/sgl-project/sglang/pull/32729) [Router] Add KV event gap replay for sgl-router
- [#32929](https://github.com/sgl-project/sglang/pull/32929) [NCCL RAS] Integrate runtime diagnostics into health checks (detection + reporting)
- [#33125](https://github.com/sgl-project/sglang/pull/33125) [rust-server] PD disaggregation support
- [#32822](https://github.com/sgl-project/sglang/pull/32822) sglang rust server api http utils
- [#33219](https://github.com/sgl-project/sglang/pull/33219) [rust-server] bump hf-hub to 1.0 so the tokenizer cache lookup honors HUGGINGFACE_HUB_CACHE
- [#32744](https://github.com/sgl-project/sglang/pull/32744) [weight daemon][WIP] support draft model
- [#33211](https://github.com/sgl-project/sglang/pull/33211) feat: rust sglang server Vertex APIs
- [#32824](https://github.com/sgl-project/sglang/pull/32824) sglang rust server abis
- [#32826](https://github.com/sgl-project/sglang/pull/32826) sglang rust server python part 1
- [#32821](https://github.com/sgl-project/sglang/pull/32821) [feat] Runtime attach/detach of HiCache storage backend for UnifiedRa…
- [#33279](https://github.com/sgl-project/sglang/pull/33279) [FEAT] Weight Deamon abstraction
- [#32773](https://github.com/sgl-project/sglang/pull/32773) [Router] Add optional admin auth for /flush_cache
- [#32827](https://github.com/sgl-project/sglang/pull/32827) sglang rust server python part 2
- [#32985](https://github.com/sgl-project/sglang/pull/32985) [diffusion] feat: add --encode-only serving mode returning encoder outputs via POST /encode
- [#32949](https://github.com/sgl-project/sglang/pull/32949) [Feature] Support opt-in dp_rank-targeted health probes on /health and /health_generate
- [#33056](https://github.com/sgl-project/sglang/pull/33056) [Rust Server] Return kv_events from /server_info like Python
- [#32753](https://github.com/sgl-project/sglang/pull/32753) [Router] Wire decode-affinity outcome metric
- [#33215](https://github.com/sgl-project/sglang/pull/33215) Dump requests sample fraction
- [#33061](https://github.com/sgl-project/sglang/pull/33061) Support llguidance reasoning grammar
- [#33032](https://github.com/sgl-project/sglang/pull/33032) Add native gRPC reflection

</details>

<details>
<summary>Tests, CI & build (11)</summary>

- [#32760](https://github.com/sgl-project/sglang/pull/32760) docker: add Kimi K3 images
- [#32871](https://github.com/sgl-project/sglang/pull/32871) update Cargo.lock for the rust sglang-server dependencies
- [#31952](https://github.com/sgl-project/sglang/pull/31952) Add pr tests
- [#32392](https://github.com/sgl-project/sglang/pull/32392) [NPU] Add PR test cases
- [#32981](https://github.com/sgl-project/sglang/pull/32981) bump dynamo-tokenizers to 1.7.0
- [#32917](https://github.com/sgl-project/sglang/pull/32917) [diffusion][benchmark] Add reproducible request-manifest offline benchmark
- [#32788](https://github.com/sgl-project/sglang/pull/32788) [Kernel] Add inventory guards and clean benchmark layout
- [#33171](https://github.com/sgl-project/sglang/pull/33171) test: recover the config-namespace-migration deferrals
- [#32649](https://github.com/sgl-project/sglang/pull/32649) add NPU GSM8K accuracy tests for 7 models
- [#31409](https://github.com/sgl-project/sglang/pull/31409) [AMD] Replace MI325 with MI300 CI Runners
- plus 47 more minor CI updates

</details>

<details>
<summary>Docs (21)</summary>

- [#32951](https://github.com/sgl-project/sglang/pull/32951) Add Inkling-Small cookbook
- [#30614](https://github.com/sgl-project/sglang/pull/30614) [Diffusion][Docs] Ascend A2, A3 add basic usage and benchmark results in diffusion cookbook
- [#32857](https://github.com/sgl-project/sglang/pull/32857) [NPU][DOC] Restructure ascend-npus docs into layered navigation
- [#32835](https://github.com/sgl-project/sglang/pull/32835) [docs] Rotate popular models on the landing pages, lead the Cookbook nav with Kimi
- [#33083](https://github.com/sgl-project/sglang/pull/33083) [Docs] Add DeepSeek-V4 Flash Official (0731) recipe
- [#33173](https://github.com/sgl-project/sglang/pull/33173) docs: rewrite the runtime-context skill for the namespace-bag config model
- [#32956](https://github.com/sgl-project/sglang/pull/32956) [Docs] Add a Conventions section to the add-jit-kernel skill
- [#32763](https://github.com/sgl-project/sglang/pull/32763) Add compute-mamba-ratio skill
- [#33131](https://github.com/sgl-project/sglang/pull/33131) feat(cookbook): add DGX Spark support for Inkling-Small
- [#32836](https://github.com/sgl-project/sglang/pull/32836) Add diffusion cookbook model tags
- [#33109](https://github.com/sgl-project/sglang/pull/33109) [Docs] Add verified H200 and B200 DeepSeek-V4 Flash Official results
- [#32838](https://github.com/sgl-project/sglang/pull/32838) docs: sync LMSYS SGLang blog cards
- [#32834](https://github.com/sgl-project/sglang/pull/32834) [docs] Kimi-K3: widen the H200 High-Throughput recipe to 4x8 TP32/EP32
- [#32932](https://github.com/sgl-project/sglang/pull/32932) docs: surface diffusion AR and PE guides
- [#33157](https://github.com/sgl-project/sglang/pull/33157) [Docs] Add RTX 5090 DeepSeek-V4 recipe
- [#32789](https://github.com/sgl-project/sglang/pull/32789) Add decode-lock skip to compute-mamba-ratio
- [#32661](https://github.com/sgl-project/sglang/pull/32661) docs(kimi-k3): clarify VLM compatibility
- [#32959](https://github.com/sgl-project/sglang/pull/32959) docs(cookbook): Qwen3.6 config-driven deployment + measured speed benchmarks
- [#33282](https://github.com/sgl-project/sglang/pull/33282) docs(diffusion): update skills for MiniMax-H3
- [#33081](https://github.com/sgl-project/sglang/pull/33081) docs: add DSpark deployment guide
- [#33203](https://github.com/sgl-project/sglang/pull/33203) [docs] deterministic inference: add a coverage map, document the numerics env vars, refresh the backend list

</details>

<details>
<summary>Bugfixes (16)</summary>

- [#32958](https://github.com/sgl-project/sglang/pull/32958) [Cherry-pick of [#32861](https://github.com/sgl-project/sglang/pull/32861)] Fix Inkling tool-call parsing recovery, content handling, and streaming
- [#32104](https://github.com/sgl-project/sglang/pull/32104) [EPD][VLM] Fix Kimi-VL 2D encoder grids
- [#32447](https://github.com/sgl-project/sglang/pull/32447) [MLX] Fix overlap-loop request bookkeeping and graceful shutdown
- [#32118](https://github.com/sgl-project/sglang/pull/32118) Fix nightly CI: NVFP4 cuda-graph crash, NVILA batching, CuTe paged-KV zero-size, Kimi-VL OOM
- [#32736](https://github.com/sgl-project/sglang/pull/32736) [Bugfix] compressed-tensors: mixed-precision checkpoints silently load unquantized
- [#30240](https://github.com/sgl-project/sglang/pull/30240) Fix DeepSeek V4 loading with RunAI Model Streamer.
- [#32962](https://github.com/sgl-project/sglang/pull/32962) Fix silently wrong EPLB output with --moe-a2a-backend none (rank-invariant dispatch)
- [#32490](https://github.com/sgl-project/sglang/pull/32490) fix(dsa): correct packed FlashInfer top-k and backend selection semantics
- [#33183](https://github.com/sgl-project/sglang/pull/33183) Harden Kimi K3 parser edge cases
- [#31968](https://github.com/sgl-project/sglang/pull/31968) [Disagg][NIXL] Fix heterogeneous attn-TP KV transfer for replicated GQA heads (NIXL_ERR_NOT_FOUND)
- [#31727](https://github.com/sgl-project/sglang/pull/31727) [AMD] Fix DeepSeek-V4 fused-RMS FP8 scale metadata on gfx950
- [#31563](https://github.com/sgl-project/sglang/pull/31563) fix mqa preshuffle layout issue for deepseek v4
- [#33149](https://github.com/sgl-project/sglang/pull/33149) fix(kimi-k3): align kimi-k3 branch with DCP + DSpark fix and cleanup
- [#33041](https://github.com/sgl-project/sglang/pull/33041) fix(kimi-k3): support canonical DCP decode offload to Mooncake L3
- [#33265](https://github.com/sgl-project/sglang/pull/33265) Fix quantized DeepSeek-V4 dropping the fused wq_a+wkv projections
- plus 49 more minor bugfixes

</details>

<details>
<summary>Refactors (13)</summary>

- [#32812](https://github.com/sgl-project/sglang/pull/32812) refactor(kimi-k3): put the gemm_ar kernels back in-tree and fold the PTX headers into their consumers
- [#33013](https://github.com/sgl-project/sglang/pull/33013) config: read resolved config via namespace accessors
- [#33170](https://github.com/sgl-project/sglang/pull/33170) config: route parallel config-leaf reads through get_parallel()
- [#32648](https://github.com/sgl-project/sglang/pull/32648) [Kernel] Move sgl-kernel under sglang.kernels.aot
- [#32709](https://github.com/sgl-project/sglang/pull/32709) [Refactor] Remove dead allocator `backup_state` / `restore_state`
- [#32881](https://github.com/sgl-project/sglang/pull/32881) [misc] Remove unused multi_layer_draft_forward_cg module
- [#33242](https://github.com/sgl-project/sglang/pull/33242) [DO NOT MERGE] ServerArgs.override burndown — stack review & CI
- [#33144](https://github.com/sgl-project/sglang/pull/33144) [Diffusion] Migrate FlyDSL fused norm kernels to the v0.3.0 stable API
- [#32912](https://github.com/sgl-project/sglang/pull/32912) [MLX] Make BaseTpWorker a runner-free backend boundary
- [#33240](https://github.com/sgl-project/sglang/pull/33240) config: keep runtime hicache and weight-version updates off ServerArgs
- [#33244](https://github.com/sgl-project/sglang/pull/33244) config: retire the last process-global config field reads
- [#33238](https://github.com/sgl-project/sglang/pull/33238) config: retire three ServerArgs.override sites that no reader needed
- [#32952](https://github.com/sgl-project/sglang/pull/32952) [JIT] Drop redundant per-kernel arch overrides

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 9fc3db63ca6660dcd48b0b642e3444fcc11ba3494f61e50927b9c3ed1844e42c -->
