# vllm: PR digest (2026-06-03 to 2026-06-10)

_252 merged, 445 newly opened - source vllm-project/vllm, generated 2026-06-10T13:13:48Z_

## TL;DR
- **DeepSeek V4** dominated model updates, gaining a new TRTLLM generation attention kernel, XPU decode paths, and newly opened work for Dynamic Context Parallelism (DCP) and disaggregated serving.
- **Major architectural refactors** are underway, including a massive inversion of the `FusedMoE`/`MoERunner` stack and a newly opened, sweeping overhaul of the attention backends.
- **Performance & Quantization** saw significant movement with new Triton NVFP4 KV cache support, W4A16 HIP kernels for AMD RDNA3, and integration of DeepEP v2 for WideEP.
- **Model support** expanded with Gemma4 MTP and Unified (encoder-free) support, plus newly opened work for LLaVA-OneVision-2 and Bailing hybrid models.
- **API & Serving** capabilities grew with dynamic LoRA endpoints, tokenization endpoints, and a Rust frontend rewrite of the DP Supervisor.

## Most important PRs
- **[#41184](https://github.com/vllm-project/vllm/pull/41184)** (Merged): Inverts the `FusedMoE` and `MoERunner` architecture, standardizing MoE execution across AMD, NVIDIA, and Intel XPU backends.
- **[#43827](https://github.com/vllm-project/vllm/pull/43827)** (Merged): Adds a highly optimized TRTLLM generation attention kernel specifically for DeepSeek V4, significantly improving decode performance.
- **[#44580](https://github.com/vllm-project/vllm/pull/44580)** (Opened): Initiates a massive refactor of all attention backends to standardize KV cache layouts and simplify integration of new attention variants.
- **[#44967](https://github.com/vllm-project/vllm/pull/44967)** (Opened): Introduces Dynamic Context Parallelism (DCP) for long-context serving, enabling efficient distributed attention across multiple GPUs.
- **[#44389](https://github.com/vllm-project/vllm/pull/44389)** (Opened): Adds Triton software NVFP4 KV cache support, paving the way for ultra-low precision KV caching on supported hardware.

<details>
<summary>Performance (26)</summary>

- [#43447](https://github.com/vllm-project/vllm/pull/43447) [Prefix Caching] DeepSeekv4 - Support selective prefix-cache retention for sliding-window KV cache
- [#40576](https://github.com/vllm-project/vllm/pull/40576) [MM][Perf][CG] Support ViT full CUDA graph for glm4_1v image and video inference
- [#44700](https://github.com/vllm-project/vllm/pull/44700) [PERF] [Qwen3.5] Split mixed prefill+decode batches: route decodes to the recurrent kernel
- [#44173](https://github.com/vllm-project/vllm/pull/44173) [Kernel] Speed up silu_and_mul_per_block_quant with warp-shuffle reduction + vectorized I/O
- [#45066](https://github.com/vllm-project/vllm/pull/45066) Revert "[Kernel] Speed up silu_and_mul_per_block_quant with warp-shuf…"
- [#44212](https://github.com/vllm-project/vllm/pull/44212) [Perf] Improve multimodal item handling from O(n) to O(log n) per step
- [#39419](https://github.com/vllm-project/vllm/pull/39419) [SpecDecode] Reduce TP communication for large-vocab draft models speculative decoding
- [#44830](https://github.com/vllm-project/vllm/pull/44830) [Kernel][Perf] Tune fused_moe FP8 config for Qwen3-Next-80B tp=4 on H100 (+25% at batch 96-512)
- [#44891](https://github.com/vllm-project/vllm/pull/44891) perf: add push-based allreduce for small tensor reductions
- [#44786](https://github.com/vllm-project/vllm/pull/44786) [Frontend] Reduce multimodal preprocessing cache contention
- [#44787](https://github.com/vllm-project/vllm/pull/44787) [Model] Optimize Qwen3-VL image-only preprocessing with compact patches
- [#44394](https://github.com/vllm-project/vllm/pull/44394) [MM][Perf] Add PaddleOCR-VL encoder CUDA graph support
- [#45106](https://github.com/vllm-project/vllm/pull/45106) [Multimodal] Add PixelPrune visual token pruning for Qwen3-VL
- [#44606](https://github.com/vllm-project/vllm/pull/44606) [Perf] Maybe improve sparse topk heuristic
- [#44572](https://github.com/vllm-project/vllm/pull/44572) [Perf] SM90 cutlass fp8 mm supports odd M by swap_ab, 180~290% kernel performance improvement
- [#44944](https://github.com/vllm-project/vllm/pull/44944) [PERF] Fuse multi-group block table staged writes
- [#44584](https://github.com/vllm-project/vllm/pull/44584) [Kernel][Perf] Triton unified attention: window-align the KV-tile iteration for sliding-window / chunked attention
- [#44677](https://github.com/vllm-project/vllm/pull/44677) [Core] DBO ++: Overlap TP all-reduce with compute
- [#44474](https://github.com/vllm-project/vllm/pull/44474) [Performance] Optimize multimodal embedding merger with static shape pattern for XLA and CUDA Graphs
- [#45061](https://github.com/vllm-project/vllm/pull/45061) [Perf] Optimize DSv4 prefill chunk planning, 4.0% E2E Throughput Improvement
- [#45126](https://github.com/vllm-project/vllm/pull/45126) [Kernel] NVIDIA-tuned tile configs + PID swizzling for triton_scaled_mm (up to 1.6x on H800, 2.0x on L20)
- [#44251](https://github.com/vllm-project/vllm/pull/44251) [Perf] Add tuned selective_state_update configs for H200 and RTX PRO …
- [#42191](https://github.com/vllm-project/vllm/pull/42191) [Perf] Apply single-pass min_larger finding and binary search in Triton Top-p path.
- [#42646](https://github.com/vllm-project/vllm/pull/42646) [perf] Add gemma RMS AR fusion
- [#42212](https://github.com/vllm-project/vllm/pull/42212) [Perf] Triton fast path for small CPU→GPU `swap_blocks_batch` in the offloading connector
- [#41759](https://github.com/vllm-project/vllm/pull/41759) [MM][Perf][CG] Support ViT full CUDA graph for InternVL
</details>

<details>
<summary>Kernels & attention (21)</summary>

- [#44365](https://github.com/vllm-project/vllm/pull/44365) [10b/n] Migrate custom all-reduce, DeepSeek V4 fused MLA, MiniMax reduce-RMS, and MXFP8 MoE to libtorch stable ABI
- [#44230](https://github.com/vllm-project/vllm/pull/44230) optimize the compressor 128 split cutedsl kernel
- [#44176](https://github.com/vllm-project/vllm/pull/44176) [Perf] fuse qk rmsnorm rope gate for qwen3.5
- [#44334](https://github.com/vllm-project/vllm/pull/44334) [10/n] Migrate cuda_view and silu_and_mul_per_block_quant kernels to torch stale ABI.
- [#42129](https://github.com/vllm-project/vllm/pull/42129) [Inductor] Fast-path Inductor fallback for vllm::*/vllm_aiter::* custom ops
- [#42472](https://github.com/vllm-project/vllm/pull/42472) [Model Runner V2] Use FlashInfer sampler
- [#42453](https://github.com/vllm-project/vllm/pull/42453) [Feature] Support batch invariant rms norm with residual
- [#44442](https://github.com/vllm-project/vllm/pull/44442) [Minor] Remove FlashInfer version check in topk_topp_sampler
- [#44561](https://github.com/vllm-project/vllm/pull/44561) [DSV4] Move more ops out of eager breakpoint
- [#44565](https://github.com/vllm-project/vllm/pull/44565) [10c/n] Start Migrate MoE kernels to torch stable ABI
- [#44501](https://github.com/vllm-project/vllm/pull/44501) [WIP][Kernel][CuTeDSL] Quant Scaled MM Per (Tensor/token/channel) FP8/INT8 kernel in CuTeDSL
- [#45001](https://github.com/vllm-project/vllm/pull/45001) [Kernel][FP8][Test] Add CUDA qkv_padded_fp8_quant for ViT FP8
- [#44667](https://github.com/vllm-project/vllm/pull/44667) [NVFP4][Emulation] Fuse NVFP4 weight dequantization with compute in triton kernel for w13/w2 MOE MLP linears
- [#45151](https://github.com/vllm-project/vllm/pull/45151) [Kernel] Fuse per-group FP8 dynamic quant into Triton attention epilogue
- [#45111](https://github.com/vllm-project/vllm/pull/45111) [Attention] Re-enable cross-layer KV cache layout for MLA via stride-aware kernels
- [#44518](https://github.com/vllm-project/vllm/pull/44518) [Model] Use native packed audio attention for Qwen2.5-Omni to remove standalone flash-attn dependency
- [#44810](https://github.com/vllm-project/vllm/pull/44810) feat: add optional torchembed RoPE backend
- [#44452](https://github.com/vllm-project/vllm/pull/44452) [Kernel][MoE] Delegate finalize output-buffer allocation to prepare_finalize
- [#44685](https://github.com/vllm-project/vllm/pull/44685) add cute helion kernel
- [#45120](https://github.com/vllm-project/vllm/pull/45120) [Kernel] Fuse softmax into grouped_topk CUDA kernel
- [#44932](https://github.com/vllm-project/vllm/pull/44932) Add FP8 KV Cache + FP8 Prefill support with Flashinfer Backend + DCP
</details>

<details>
<summary>MoE & quantization (8)</summary>

- [#44340](https://github.com/vllm-project/vllm/pull/44340) [Quant] Support compressed-tensors WNA8O8Int linears and WNInt embeddings
- [#44132](https://github.com/vllm-project/vllm/pull/44132) [Quantization] add online fp8 ptpc
- [#44581](https://github.com/vllm-project/vllm/pull/44581) [Feature] KVarN: Variance-Normalized KV-Cache Quantization (4-bit K, 2-bit V)
- [#44564](https://github.com/vllm-project/vllm/pull/44564) [KV Cache Quantization] SQuat: Subspace-orthogonal KV Cache Quantization
- [#44553](https://github.com/vllm-project/vllm/pull/44553) Add H20-3e FP8 fused-MoE tuned config for E=256,N=512 (Qwen3.6 A3B)
- [#44675](https://github.com/vllm-project/vllm/pull/44675) Add tuned fused_moe config for Nemotron-Super on H200
- [#44960](https://github.com/vllm-project/vllm/pull/44960) [GGUF] Add IQ4_NL MMQ kernel support
- [#44818](https://github.com/vllm-project/vllm/pull/44818) [Perf] Add H200 BF16 fused MoE configs for Gemma4 (E=128,N=704)
</details>

<details>
<summary>Model support (21)</summary>

- [#44429](https://github.com/vllm-project/vllm/pull/44429) [Model] Add Gemma4 Unified (encoder-free) support
- [#42175](https://github.com/vllm-project/vllm/pull/42175) [Core][Model] Gemma4: Unified FA4 for all layers + FlashAttention mm_prefix support
- [#45127](https://github.com/vllm-project/vllm/pull/45127) [Model] Remove obsolete ERNIE models
- [#44417](https://github.com/vllm-project/vllm/pull/44417) [videoloader] implement glm46v video loader
- [#44609](https://github.com/vllm-project/vllm/pull/44609) Support MiniCPMV batched preprocessing
- [#43519](https://github.com/vllm-project/vllm/pull/43519) Add model support for granite speech plus
- [#44999](https://github.com/vllm-project/vllm/pull/44999) Model/colbert autoweightsloader
- [#44707](https://github.com/vllm-project/vllm/pull/44707) [Cohere] Enable Cohere Mini Code model and update Command A-plus test registry
- [#44785](https://github.com/vllm-project/vllm/pull/44785) [Model] Add LLaVA-OneVision-2 (LlavaOnevision2ForConditionalGeneration)
- [#44530](https://github.com/vllm-project/vllm/pull/44530) Add ColBERT embedding_mode for asymmetric query/document encoding
- [#45131](https://github.com/vllm-project/vllm/pull/45131) Deprecated 1st generation Qwen and QwenVL models
- [#44880](https://github.com/vllm-project/vllm/pull/44880) [Feature] Support MTP speculative decoding for Bailing hybrid models
- [#44963](https://github.com/vllm-project/vllm/pull/44963) fix: [Feature]: Support `Phi4Flash` model in V1
- [#44930](https://github.com/vllm-project/vllm/pull/44930) [Model] Add encoder CUDA graph support to Lfm2VL
- [#44723](https://github.com/vllm-project/vllm/pull/44723) [Bailing] Add MTP (Multi-Token Prediction) draft model support
- [#44792](https://github.com/vllm-project/vllm/pull/44792) Add Orthrus model support
- [#44590](https://github.com/vllm-project/vllm/pull/44590) Add Thor selective state update configs
- [#44720](https://github.com/vllm-project/vllm/pull/44720) [Model][Test] Add Qwen3.6 (dense + MoE) to multimodal ViT CUDA graph support
- [#45123](https://github.com/vllm-project/vllm/pull/45123) [vLLM Model] Migrate deepseekv2 to vllm/models
- [#45129](https://github.com/vllm-project/vllm/pull/45129) [Model] Remove Mono-InternVL (InternLM2VEForCausalLM)
- [#39425](https://github.com/vllm-project/vllm/pull/39425) Remove `raw_inputs` from transformers backend
</details>

<details>
<summary>Parallelism & scheduling (42)</summary>

- [#44854](https://github.com/vllm-project/vllm/pull/44854) [Connector] Remove `P2pNcclConnector`
- [#41183](https://github.com/vllm-project/vllm/pull/41183) [WideEP] Integrate DeepEP v2
- [#35669](https://github.com/vllm-project/vllm/pull/35669) Feature/offloading manager stats
- [#37505](https://github.com/vllm-project/vllm/pull/37505) [KVCache] Support Pluggable KVCacheSpec
- [#41968](https://github.com/vllm-project/vllm/pull/41968) Add objectstore as a secondary tier to multi-tier kv cache offloading
- [#41980](https://github.com/vllm-project/vllm/pull/41980) use split_group for pytorch process group creation
- [#41633](https://github.com/vllm-project/vllm/pull/41633) [EPLB] Nixl communicator optimization. Zero-copy transfers
- [#43720](https://github.com/vllm-project/vllm/pull/43720) [KVConnector][1/N] PP-aware handshake aggregation and intermediate-PP output plumbing
- [#44669](https://github.com/vllm-project/vllm/pull/44669) [Core][Engine] allow DP ray placement groups to be set on specific nodes
- [#43799](https://github.com/vllm-project/vllm/pull/43799) [Mooncake] Use all HCAs on multi-NIC hosts instead of GPU-indexed RNIC selection
- [#44420](https://github.com/vllm-project/vllm/pull/44420) [feature] add index share feature for DSA MTP
- [#43874](https://github.com/vllm-project/vllm/pull/43874) [NixlConnector] Initiate deprecation cycle for `kv_both` role
- [#42554](https://github.com/vllm-project/vllm/pull/42554) [PD][Nixl] Mamba prefix caching mode support
- [#44661](https://github.com/vllm-project/vllm/pull/44661) [Disagg][NIXL] slice_tp_for_transfer
- [#44994](https://github.com/vllm-project/vllm/pull/44994) [Feat] Add fast EP scaling with NCCL communicator split
- [#45112](https://github.com/vllm-project/vllm/pull/45112) [Draft] DeepSeek V4 PP/PD disaggregated serving with Mooncake
- [#44573](https://github.com/vllm-project/vllm/pull/44573) Add DeepSeek-V4 DCP decode support
- [#45027](https://github.com/vllm-project/vllm/pull/45027) Multitenant kvcache
- [#44698](https://github.com/vllm-project/vllm/pull/44698) [Spec][PP] Support MTP speculative decoding under pipeline parallelism (PP>1)
- [#44465](https://github.com/vllm-project/vllm/pull/44465) Vram semaphore infra
- [#44586](https://github.com/vllm-project/vllm/pull/44586) [MRV2][Spec Decode] DFlash
- [#45043](https://github.com/vllm-project/vllm/pull/45043) llmd+vllm+mori-ep(inter node wide-ep)+mori-io(write) for 2p2d with dp=ep=16 tp=1
- [#45018](https://github.com/vllm-project/vllm/pull/45018) [Feature] SLEM speculative decoding for heterogeneous vocabularies
- [#44848](https://github.com/vllm-project/vllm/pull/44848) [Core] Enable KimiLinear (KDA/GDN + MLA) PD Separation via NIXL
- [#44794](https://github.com/vllm-project/vllm/pull/44794) [Core] FlowPrefill: adaptive sub-chunk preemption for v1 Scheduler
- [#44453](https://github.com/vllm-project/vllm/pull/44453) [Experiment][Model Runner V2][Spec Decode] sharded rejection sampling
- [#44865](https://github.com/vllm-project/vllm/pull/44865) [KV Offload] Reshape the transfer data model: per group specs and offloaded side alignment offset
- [#44528](https://github.com/vllm-project/vllm/pull/44528) [KV Connector][Mooncake] Pipeline-parallel support for PD-disaggregated serving with Mooncake connector
- [#44428](https://github.com/vllm-project/vllm/pull/44428) [Feature] Add fault tolerance framework (simplified) for DP+EP external LB deployments
- [#45053](https://github.com/vllm-project/vllm/pull/45053) [KV Offload] Replace OffloadingHandler with OffloadingWorker
- [#44816](https://github.com/vllm-project/vllm/pull/44816) [Model Runner V2][Spec Decode]Support peagle spec decode
- [#44577](https://github.com/vllm-project/vllm/pull/44577) [DSv4] Pack KV caches into contiguous per-block allocations for DeepSeek V4
- [#44956](https://github.com/vllm-project/vllm/pull/44956) [KV Connector][Mooncake] Add store group semantics
- [#44597](https://github.com/vllm-project/vllm/pull/44597) Add global cache scope for ngram prompt lookup
- [#45056](https://github.com/vllm-project/vllm/pull/45056) [WIP][Model] Enable MiMo 2.5 DFlash
- [#44583](https://github.com/vllm-project/vllm/pull/44583) [NIXL] Per-region KV transfer classes for mixed full-attn + MLA groups
- [#44510](https://github.com/vllm-project/vllm/pull/44510) [Model Runner V2] Support thinking_token_budget for mrv2
- [#44919](https://github.com/vllm-project/vllm/pull/44919) [Mooncake] Auto-discover compatible RDMA devices for Mooncake Connector
- [#44558](https://github.com/vllm-project/vllm/pull/44558) [Core] Add prefill step cadence for better non-PD DP balancing
- [#45013](https://github.com/vllm-project/vllm/pull/45013) [EPLB] Enable nixl eplb communicator for elastic ep
- [#44541](https://github.com/vllm-project/vllm/pull/44541) [KV Offloading] Implement `reset_cache` for `TieringOffloadingManager`
- [#44791](https://github.com/vllm-project/vllm/pull/44791) [KVConnector] Add prefix-length threshold for lazy SimpleCPUOffloadConnector
- [#44774](https://github.com/vllm-project/vllm/pull/44774) [KV Connector] Mooncake store: prefix-cache retention interval for sparse attention
</details>

<details>
<summary>Hardware & arch (33)</summary>

- [#42953](https://github.com/vllm-project/vllm/pull/42953) feat: add DeepSeek-V4 XPU attention decode path
- [#44075](https://github.com/vllm-project/vllm/pull/44075) [ROCm][Perf] Fused MoE W4A16 HIP kernel for AMD RDNA3 (gfx1100)
- [#42864](https://github.com/vllm-project/vllm/pull/42864) [ROCm][Compile] Fuse AR + RMSNorm + per-group FP8 quant (+ DSv3.2 indexer fan-out)
- [#40426](https://github.com/vllm-project/vllm/pull/40426) [ROCM] [FEAT] Integrate Aiter hipBLASLt GEMM online tuning
- [#37149](https://github.com/vllm-project/vllm/pull/37149) [XPU][Feature] transparent sleep mode support for XPU platform
- [#42832](https://github.com/vllm-project/vllm/pull/42832) [ROCm][GPT-OSS] Fuse RoPE + static Q FP8 quant on fused RoPE+KV path
- [#42758](https://github.com/vllm-project/vllm/pull/42758) Enable perf_token_group_quant/_C_stable_libtorch for ROCm
- [#43689](https://github.com/vllm-project/vllm/pull/43689) [SharedOffloadRegion] Align blocks to page-size
- [#44144](https://github.com/vllm-project/vllm/pull/44144) [DSV4][XPU] Add MHC fused_post_pre support
- [#36423](https://github.com/vllm-project/vllm/pull/36423) [XPU] Support cpu kv offloading and tiering offloading on XPU platform
- [#41002](https://github.com/vllm-project/vllm/pull/41002) [ROCm][perf] Use workspace manager for sparse indexer allocations
- [#40470](https://github.com/vllm-project/vllm/pull/40470) [Attention] Extract KV-cache update from CPU attention backend
- [#39968](https://github.com/vllm-project/vllm/pull/39968) [XPU] Add XPU block-scaled W8A8 fp8 path
- [#42139](https://github.com/vllm-project/vllm/pull/42139) [XPU][MoE] support block_fp8_moe on xpu
- [#44945](https://github.com/vllm-project/vllm/pull/44945) [ROCm][Perf] Use fused softplus-sqrt-topk router under AITER fused-MoE
- [#44804](https://github.com/vllm-project/vllm/pull/44804) [ROCm][gpt-oss] Hybrid CDNA4 swizzle gate for A8W4 MoE
- [#44771](https://github.com/vllm-project/vllm/pull/44771) [XPU][Minor] format moe kernel name and add in kernel list
- [#44393](https://github.com/vllm-project/vllm/pull/44393) [Attention][CPU] Standardize kv layout to blocks first
- [#42838](https://github.com/vllm-project/vllm/pull/42838) [ROCm][MLA] Replace torch.cat in sparse-MLA forward_mqa with fused concat_mla_q
- [#44419](https://github.com/vllm-project/vllm/pull/44419) [CPU][Spec Decode] Warn about throughput loss when libiomp5 is not preloaded
- [#44540](https://github.com/vllm-project/vllm/pull/44540) [XPU] add xpu branch in compressed_tensors_moe_w4a4_mxfp4
- [#44674](https://github.com/vllm-project/vllm/pull/44674) [ROCm][Kernel] Enable permute_cols for ROCm
- [#44437](https://github.com/vllm-project/vllm/pull/44437) [ROCm][Compile] Fuse RMSNorm + MXFP4 quant via AITER Triton kernels (DeepSeek-R1)
- [#44976](https://github.com/vllm-project/vllm/pull/44976) [ROCm][Kernel][AITER] BlockScale FP8 SplitK zero-init fusion
- [#44400](https://github.com/vllm-project/vllm/pull/44400) [ROCm][Perf] Enable W4A16 FlyDSL MoE
- [#44544](https://github.com/vllm-project/vllm/pull/44544) [ROCm][MLA] AITER FP8 ASM prefill backend
- [#44975](https://github.com/vllm-project/vllm/pull/44975) Improve Intel macOS CPU extension stability
- [#44834](https://github.com/vllm-project/vllm/pull/44834) [CPU][Zen] Route Int8 MoE inference through zentorch on AMD
- [#44876](https://github.com/vllm-project/vllm/pull/44876) [Aiter][ROCm] QKV-split + QK-RMSNorm + RoPE + KV-cache-write fusion
- [#44899](https://github.com/vllm-project/vllm/pull/44899) [ROCm][DSv4][Perf] Flash-decode split-K decode attention kernel
- [#44977](https://github.com/vllm-project/vllm/pull/44977) [ROCm][MLA] Fuse MLA q/kv RMSNorm + FP8 per-token quant in the FP8 attention path
- [#45103](https://github.com/vllm-project/vllm/pull/45103) [ROCm][DSV4][Perf] Fuse inverse-RoPE and cache bf16 wo_a in o-projection
- [#44851](https://github.com/vllm-project/vllm/pull/44851) Add SM120 NVFP4 KV cache support
- [#44991](https://github.com/vllm-project/vllm/pull/44991) [CPU] Skip Triton kernel monkey-patches when Triton-CPU is available
- [#44639](https://github.com/vllm-project/vllm/pull/44639) [CPU][Perf]Added tanh AOR for faster gelu activations.
- [#44987](https://github.com/vllm-project/vllm/pull/44987) [XPU] eplb
- [#45033](https://github.com/vllm-project/vllm/pull/45033) [ROCm][MLA] Add AITER FlashAttention MLA prefill backend (`ROCM_AITER_FA`)
</details>

<details>
<summary>API & serving (43)</summary>

- [#43778](https://github.com/vllm-project/vllm/pull/43778) [Rust Frontend] Add dynamic LoRA endpoints
- [#44479](https://github.com/vllm-project/vllm/pull/44479) [Frontend] Consolidate online serving utils.
- [#44222](https://github.com/vllm-project/vllm/pull/44222) [Rust Frontend] Add /tokenize and /detokenize endpoints
- [#44391](https://github.com/vllm-project/vllm/pull/44391) [Rust Frontend] Support include_reasoning=false
- [#44552](https://github.com/vllm-project/vllm/pull/44552) [Rust Frontend] Add seed_oss and step3p5 reasoning parsers
- [#44321](https://github.com/vllm-project/vllm/pull/44321) [Rust Frontend] Support API key authentication
- [#43590](https://github.com/vllm-project/vllm/pull/43590) [Frontend][Responses API] Fold developer-role input messages into system instructions
- [#44213](https://github.com/vllm-project/vllm/pull/44213) [Rust Frontend] Add Phi-4 mini JSON tool parser
- [#43942](https://github.com/vllm-project/vllm/pull/43942) [Rust Frontend] Add /server_info to Rust frontend
- [#44499](https://github.com/vllm-project/vllm/pull/44499) [Rust Frontend] Add /pause, /resume, /is_paused endpoints
- [#44901](https://github.com/vllm-project/vllm/pull/44901) [Rust Frontend] Support Kimi K2 tool call IDs
- [#44591](https://github.com/vllm-project/vllm/pull/44591) [Rust Frontend] Batch auto-abort requests by engine
- [#44500](https://github.com/vllm-project/vllm/pull/44500) [Rust Frontend] Skip loading multimodal processor if `--language-model-only` is specified
- [#44595](https://github.com/vllm-project/vllm/pull/44595) [Misc] usage_stats: report more engine, spec-decode, and EP config
- [#43838](https://github.com/vllm-project/vllm/pull/43838) [Platform] Add is_cumem_allocator_available
- [#43774](https://github.com/vllm-project/vllm/pull/43774) [Rust Frontend] Add server router extension hook
- [#45045](https://github.com/vllm-project/vllm/pull/45045) [Render] Add reasoning and tool call parsing to `/derender`
- [#45003](https://github.com/vllm-project/vllm/pull/45003) [Frontend] Integrate xgrammar builtin structural tags for strict tool calling
- [#44445](https://github.com/vllm-project/vllm/pull/44445) [Frontend] Add OpenAI-compatible online Batch and Files API
- [#44713](https://github.com/vllm-project/vllm/pull/44713) [Rust Frontend] Add Granite tool and reasoning parsers
- [#44624](https://github.com/vllm-project/vllm/pull/44624) [Rust Frontend] Add Python bridge for Rust tool parsers
- [#44776](https://github.com/vllm-project/vllm/pull/44776) [Draft][Rust] Add video modality support for vllm-rs
- [#44404](https://github.com/vllm-project/vllm/pull/44404) [Profiler] Get Detailed MultiModal Data Preprocessing Timing Stats
- [#44887](https://github.com/vllm-project/vllm/pull/44887) [Rust Frontend] Populate `cached_token_count` in responses
- [#44915](https://github.com/vllm-project/vllm/pull/44915) [Feature] Migrate DP Supervisor from Python to Rust
- [#44535](https://github.com/vllm-project/vllm/pull/44535) [Profiler] Support multiple profiling windows
- [#44664](https://github.com/vllm-project/vllm/pull/44664) [Responses] Support required function tools for GPT-OSS Harmony
- [#44938](https://github.com/vllm-project/vllm/pull/44938) [Rust Frontend] Support prompt-only completions
- [#45026](https://github.com/vllm-project/vllm/pull/45026) Stop setting CUDA_VISIBLE_DEVICES internally in vLLM, add device_ids arg
- [#45030](https://github.com/vllm-project/vllm/pull/45030) [Frontend][Metrics] Export vllm:lora_requests_info from the Rust frontend
- [#45097](https://github.com/vllm-project/vllm/pull/45097) [API] Add /health/decode endpoint exposing engine forward-progress liveness
- [#45095](https://github.com/vllm-project/vllm/pull/45095) [Examples] Add cumem sleep/wake allocator probe
- [#45137](https://github.com/vllm-project/vllm/pull/45137) [Rust Frontend] Add external→internal request-id map for abort()
- [#44900](https://github.com/vllm-project/vllm/pull/44900) [Feat][Rust Frontend] Add --root-path support for reverse proxy routing
- [#44890](https://github.com/vllm-project/vllm/pull/44890) Add release_kv_cache() API
- [#44800](https://github.com/vllm-project/vllm/pull/44800) [Core] Add `VLLM_GPU_SYNC_CHECK` env var
- [#44760](https://github.com/vllm-project/vllm/pull/44760) [Rust Frontend] Support parallel_tool_calls
- [#44633](https://github.com/vllm-project/vllm/pull/44633) [Feature][Frontend] Add APC prefix cache hit rate to PD usage details
- [#44487](https://github.com/vllm-project/vllm/pull/44487) [Metrics][Spec Decoding] Add per-request acceptance rate Prometheus histogram
- [#44402](https://github.com/vllm-project/vllm/pull/44402) [Core] Implement fine-grained timing spans for requests.
- [#44822](https://github.com/vllm-project/vllm/pull/44822) Feature/cache accounting OpenAI anthropic api
- [#44549](https://github.com/vllm-project/vllm/pull/44549) [Security] Replace diskcache to eliminate pickle deserialization
- [#45034](https://github.com/vllm-project/vllm/pull/45034) [Example] Add Top-n-sigma logit truncation custom logits processor
- [#44382](https://github.com/vllm-project/vllm/pull/44382) [Rust Frontend] Add /abort_requests endpoint
- [#44922](https://github.com/vllm-project/vllm/pull/44922) [Metrics] Add vllm:request_received counter labeled by input modality
</details>

<details>
<summary>Tests (22)</summary>

- [#42457](https://github.com/vllm-project/vllm/pull/42457) [Bench] Add BFCL dataset for vllm bench serve tool-calling workloads
- [#44471](https://github.com/vllm-project/vllm/pull/44471) [Misc] Add unit tests for pooler head classes
- [#44436](https://github.com/vllm-project/vllm/pull/44436) [ROCm][CI] Add test for Aiter unified attn kernel
- [#44819](https://github.com/vllm-project/vllm/pull/44819) [CI] Consolidate multimodal entrypoint tests.
- [#44051](https://github.com/vllm-project/vllm/pull/44051) [CI] Stabilize the multi-audio OpenAI server path
- [#44244](https://github.com/vllm-project/vllm/pull/44244) [Benchmark] Enable reasoning-model (thinking) benchmarking via `--chat-template-kwargs` for client-rendered datasets
- [#44708](https://github.com/vllm-project/vllm/pull/44708) [Benchmark] Auto-detect and correct client/server tokenizer mismatch for random dataset
- [#44805](https://github.com/vllm-project/vllm/pull/44805) Added extra_repr() to pooler classes to improve debuggability
- [#44516](https://github.com/vllm-project/vllm/pull/44516) feat(multi-turn-bench): add api_key and custom headers for multi turn benchmark
- [#42865](https://github.com/vllm-project/vllm/pull/42865) [KV Connector] Update lmcache kv_offloading_backend to use LMCacheMPConnector
- [#42736](https://github.com/vllm-project/vllm/pull/42736) [Kernel][Test] Make kernel tests for mamba dual-HW (CUDA + XPU)
- [#44593](https://github.com/vllm-project/vllm/pull/44593) [Misc] Replaced asserts with proper exceptions to improve UX for pooling
- [#43307](https://github.com/vllm-project/vllm/pull/43307) [Kernel][Test] Extend lightning_attn and awq_triton kernel tests to XPU
- [#44174](https://github.com/vllm-project/vllm/pull/44174) [CI] Align PD tests to HMA on by default
- [#44574](https://github.com/vllm-project/vllm/pull/44574) Preserve layout-changing clones
- [#44459](https://github.com/vllm-project/vllm/pull/44459) # Helion `scaled_mm` vs cutlass — benchmark command & result
- [#45016](https://github.com/vllm-project/vllm/pull/45016) [Kernel][XPU] Add unit tests for Mamba-2 SSD chunk kernels
- [#44587](https://github.com/vllm-project/vllm/pull/44587) [ASR] Add Long Audio benchmark and correctness test
- [#44673](https://github.com/vllm-project/vllm/pull/44673) Add speculative decoding correctness gate
- [#44375](https://github.com/vllm-project/vllm/pull/44375) [Test][KVConnector] Improve LMCache connector test coverage
- [#44704](https://github.com/vllm-project/vllm/pull/44704) [CI] Add opt-in statistically-calibrated lm-eval accuracy gate (Wilson lower bound)
- [#45105](https://github.com/vllm-project/vllm/pull/45105) worker: opt-in NCCL_ASYNC_ERROR_HANDLING preservation for hang detection (#45094)
- [#44385](https://github.com/vllm-project/vllm/pull/44385) [Misc] Add unit test for chunk_local_cumsum kernels
</details>

<details>
<summary>CI & build (23)</summary>

- [#36949](https://github.com/vllm-project/vllm/pull/36949) [ROCm][CI] Optimize ROCm Docker build: registry cache, DeepEP, and ci-bake script
- [#42793](https://github.com/vllm-project/vllm/pull/42793) [ROCm][CI] Stage C mirrors
- [#44947](https://github.com/vllm-project/vllm/pull/44947) [CI] Reorganize entrypoints CI
- [#43663](https://github.com/vllm-project/vllm/pull/43663) [XPU][CI] Add more test cases in Intel GPU CI
- [#44981](https://github.com/vllm-project/vllm/pull/44981) [Rust Frontend] [CI] Unify Rust artifact builds with setuptools-rust
- [#44761](https://github.com/vllm-project/vllm/pull/44761) [ROCm][CI] Stabilizing teardown and timeout of flaky tests to prevent rare OOMs
- [#44481](https://github.com/vllm-project/vllm/pull/44481) [XPU][CI] Refine docker image build and pull/create lock mechanism in Intel GPU CI
- [#44823](https://github.com/vllm-project/vllm/pull/44823) [ROCm][CI] Defer AITER sampler import and isolate server test PYTHONPATH
- [#44046](https://github.com/vllm-project/vllm/pull/44046) [ROCm][CI] Stabilize memory-release in the Hybrid model generation tests
- [#44040](https://github.com/vllm-project/vllm/pull/44040) [ROCm][CI] Stabilize ModernBERT token-classification parity against Hugging Face
- [#44809](https://github.com/vllm-project/vllm/pull/44809) [ROCm][CI] Re-route NixlConnector jobs
- [#43022](https://github.com/vllm-project/vllm/pull/43022) [ROCm][CI] Stabilize sleep-mode memory release
- [#44605](https://github.com/vllm-project/vllm/pull/44605) [CI/Build] Disable CPU-Compatibility Tests
- [#43625](https://github.com/vllm-project/vllm/pull/43625) [ROCm] Bump fastsafetensors to v0.3.2 from PyPI, remove git source build
- [#44255](https://github.com/vllm-project/vllm/pull/44255) [ROCm][CI] Specifying time outs for the lm eval models
- [#44369](https://github.com/vllm-project/vllm/pull/44369) [ROCm][CI] Skip fp8 reload tests on gfx90a (MI250)
- [#42262](https://github.com/vllm-project/vllm/pull/42262) [WIP][XPU] upgrade torch-xpu to 2.12
- [#44497](https://github.com/vllm-project/vllm/pull/44497) [CI] Reverted gitignore changes
- [#44649](https://github.com/vllm-project/vllm/pull/44649) [CI] Bump mistral-common
- [#44352](https://github.com/vllm-project/vllm/pull/44352) [CI] Add missing vllm/parser/ CI trigger and fix test_parse.py
- [#44463](https://github.com/vllm-project/vllm/pull/44463) [CI] Resolve release V2 docker build after ROCm CI wheels change
- [#44647](https://github.com/vllm-project/vllm/pull/44647) [CI] Bump mypy version `1.19.1` -> `1.20.2`
- [#44370](https://github.com/vllm-project/vllm/pull/44370) [ROCm][CI] Move Model Executor test step from MI250 to MI300 (gfx942)
- [#45041](https://github.com/vllm-project/vllm/pull/45041) Bump the minor-update group across 1 directory with 150 updates
</details>

<details>
<summary>Docs (8)</summary>

- [#34894](https://github.com/vllm-project/vllm/pull/34894) [DOC] Add INT8 W4A8 docs and Arm's supported quantization schemes
- [#44635](https://github.com/vllm-project/vllm/pull/44635) Speed up docs build
- [#44415](https://github.com/vllm-project/vllm/pull/44415) [Docs] Add KV offloading usage guide (single- and multi-tier)
- [#43756](https://github.com/vllm-project/vllm/pull/43756) [Bench] benchmark_serving_multi_turn: make non-standard conversation_id payload opt-in
- [#44388](https://github.com/vllm-project/vllm/pull/44388) [Doc] Update ViT CUDA graph interfaces
- [#44853](https://github.com/vllm-project/vllm/pull/44853) [Docs] Add Rust frontend contributor guide
- [#44924](https://github.com/vllm-project/vllm/pull/44924) [Doc][MoE Refactor] Fused MoE design doc
- [#45107](https://github.com/vllm-project/vllm/pull/45107) [Docs] Multi-tenant sleep-mode operational guidance
</details>

<details>
<summary>Bugfixes (77)</summary>

- [#43150](https://github.com/vllm-project/vllm/pull/43150) [BUG] Fix FP64 Gumbel precision coverage
- [#44330](https://github.com/vllm-project/vllm/pull/44330) [Bugfix] GPT-OSS instruction rendering
- [#44311](https://github.com/vllm-project/vllm/pull/44311) [Rust Frontend] Fix several hf chat template rendering issues
- [#44683](https://github.com/vllm-project/vllm/pull/44683) [Bugfix][Rust Frontend] Fix missing added tokens in hf/fastokens tokenizer
- [#44560](https://github.com/vllm-project/vllm/pull/44560) [BugFix] Resolve multiple async kv load deadlock
- [#44450](https://github.com/vllm-project/vllm/pull/44450) [Model Runner V2] Fix mrv2 mm lora issue
- [#44559](https://github.com/vllm-project/vllm/pull/44559) [Bugfix][Voxtral] Add fetch_audio to MistralCommonFeatureExtractor (transformers>=5.10 compat)
- [#39091](https://github.com/vllm-project/vllm/pull/39091) [Bugfix][Reasoning] Nemotron V3: surface reasoning as content when thinking is unterminated
- [#44648](https://github.com/vllm-project/vllm/pull/44648) [Bugfix] [ROCm] [Critical] fallback to regular abi for ROCm
- [#44629](https://github.com/vllm-project/vllm/pull/44629) [PD][Bugfix] Fix KV Cache sharing with HMA
- [#44983](https://github.com/vllm-project/vllm/pull/44983) [Bugfix] Fix minimax_qk_norm_fusion
- [#44347](https://github.com/vllm-project/vllm/pull/44347) [Bugfix] Update TrtLLM MoE routing methods
- [#45002](https://github.com/vllm-project/vllm/pull/45002) [Bugfix] fix qwen3.5 ep weight loading
- [#44907](https://github.com/vllm-project/vllm/pull/44907) [Cohere] Cohere2 moe parser fix
- [#42752](https://github.com/vllm-project/vllm/pull/42752) [Bugfix] Honor tool_choice="none" in Chat Completions streaming
- [#44735](https://github.com/vllm-project/vllm/pull/44735) [Bugfix] Canonicalize FP8 weight layout to (K, N) at the source
- [#44729](https://github.com/vllm-project/vllm/pull/44729) [Bugfix][Rust Frontend] Set a structured-output backend so requests do not 500
- [#42978](https://github.com/vllm-project/vllm/pull/42978) [ROCm][MLA][Bugfix] Reserve FP8 prefill workspace before lock for Kimi-K2.5
- [#44057](https://github.com/vllm-project/vllm/pull/44057) [Bugfix] Reject non-positive values for ParallelConfig int knobs
- [#44897](https://github.com/vllm-project/vllm/pull/44897) [Bugfix][MoE] Fix fused MoE expert mapping helper call sites
- [#44952](https://github.com/vllm-project/vllm/pull/44952) [Bugfix][CI] Gemma3 Transformers multimodal encoder profiling and build prompt-embedding fixtures
- [#44747](https://github.com/vllm-project/vllm/pull/44747) [Cohere] Fix Cohere2MoE weight loading when using Transformers ≥5.10
- [#38804](https://github.com/vllm-project/vllm/pull/38804) Fix sarvam forward compatibility with transformers v5
- [#39498](https://github.com/vllm-project/vllm/pull/39498) [Bugfix] Add deepseek_v32 to Quark dynamic MXFP4 model type check
- [#43862](https://github.com/vllm-project/vllm/pull/43862) [Bugfix] fix crash in postprocess for null tool args
- [#45029](https://github.com/vllm-project/vllm/pull/45029) Revert "[Bugfix][CI] Gemma3 Transformers multimodal encoder profiling and build prompt-embedding fixtures"
- [#44380](https://github.com/vllm-project/vllm/pull/44380) [Bugfix] Fix test_cutlass_moe.py
- [#44620](https://github.com/vllm-project/vllm/pull/44620) [Bugfix][Rust Frontend] Fix UTF-8 char-boundary panic in incremental detokenizer
- [#44613](https://github.com/vllm-project/vllm/pull/44613) [Bugfix][MoE] Snapshot max_cudagraph_capture_size into FusedMoEConfig
- [#43684](https://github.com/vllm-project/vllm/pull/43684) [Bugfix][ROCm] `ApplyRotaryEmb`: fall back to native when flash_attn rotary grid would exceed the HIP per-dim limit
- [#44678](https://github.com/vllm-project/vllm/pull/44678) [ROCm][CI] fix test_rope_kvcache_fusion.py
- [#43659](https://github.com/vllm-project/vllm/pull/43659) Handle spinloop ext load failure gracefully
- [#44348](https://github.com/vllm-project/vllm/pull/44348) [Bugfix] Fix unstreamed tool call args dropped in Responses API streaming
- [#44128](https://github.com/vllm-project/vllm/pull/44128) [Misc] Remove dead VLLM_RPC_TIMEOUT env var and fix profiling doc that references it
- [#44425](https://github.com/vllm-project/vllm/pull/44425) [CI/Build] Fix LoRA testing
- [#44914](https://github.com/vllm-project/vllm/pull/44914) [Bug] Fix deepseek v4 OOM issue
- [#44476](https://github.com/vllm-project/vllm/pull/44476) [Bugfix][Compile] Guard per_token_group_fp8_quant lookup on non-CUDA platforms
- [#44618](https://github.com/vllm-project/vllm/pull/44618) [Bugfix] Fix test_invocations flaky failure with newer openai SDK
- [#44021](https://github.com/vllm-project/vllm/pull/44021) [Cohere] fix RoutingMethodType
- [#44694](https://github.com/vllm-project/vllm/pull/44694) [Bugfix] Fix Qwen3.5-FP8 nightly fail. Guard fused_add_rms_norm input/weight dtype mismatch in RMSNorm + quant fusion
- [#44103](https://github.com/vllm-project/vllm/pull/44103) [Bugfix][Mooncake] Fix per-group block_size/block_hash and group_idx in MooncakeStoreConnector KV events
- [#44744](https://github.com/vllm-project/vllm/pull/44744) [Security] Fix remote DoS via invalid recovered token reinjection
- [#44970](https://github.com/vllm-project/vllm/pull/44970) [Security] Fix DoS via audio decompression bomb in speech-to-text endpoint
- [#44253](https://github.com/vllm-project/vllm/pull/44253) [Bug Fix][Model Runner V2][Spec Decode] Warmup & capture with different attention states for speculator prefill
- [#44042](https://github.com/vllm-project/vllm/pull/44042) [CI] Reject out-of-vocabulary before they reach the GPU logprob path
- [#45054](https://github.com/vllm-project/vllm/pull/45054) [Bugfix] Fix weight loading issues caused by [#41184](https://github.com/vllm-project/vllm/pull/41184)
- [#44410](https://github.com/vllm-project/vllm/pull/44410) [Bugfix] Fix VLLMNotFoundError when using LoRA adapter name in poolin…
- [#44509](https://github.com/vllm-project/vllm/pull/44509) [Bugfix] MiniCPM-V-4.6 video inference crash: placeholder count mismatches visual embedding count
- [#39562](https://github.com/vllm-project/vllm/pull/39562) [Bugfix]: Fix assertion in MambaManager.allocate_slots()
- [#45057](https://github.com/vllm-project/vllm/pull/45057) [Bugfix] Handle HWC images in ImageProcessorItems.get_image_size
- [#44686](https://github.com/vllm-project/vllm/pull/44686) Fix Harmony tool descriptions for optional fields
- [#44493](https://github.com/vllm-project/vllm/pull/44493) [Bugfix]Fix Kimi-K2.5 FlashInfer ViT metadata
- [#44974](https://github.com/vllm-project/vllm/pull/44974) [Security] Fix image EXIF orientation and tRNS transparency handling
- [#45022](https://github.com/vllm-project/vllm/pull/45022) [Bugfix][Core][Model] Voxtral realtime: fix boot-OOM / silent-hang / max-len crash on 16 GiB, + optional unbounded duration (RFC, default-off)
- [#44807](https://github.com/vllm-project/vllm/pull/44807) [Model] TEMP Fix for DFlash SWA PR (#40898)
- [#44986](https://github.com/vllm-project/vllm/pull/44986) [Core][Eagle] Fix prefix cache efficiency in prefill phase
- [#44551](https://github.com/vllm-project/vllm/pull/44551) fix: Correct reasoning-end detection for prompt history
- [#44653](https://github.com/vllm-project/vllm/pull/44653) [Bugfix] Fix Gemma4 streaming tool call parsing
- [#44844](https://github.com/vllm-project/vllm/pull/44844) [Bugfix] Fix Gemma4 streaming tool call parsing
- [#44784](https://github.com/vllm-project/vllm/pull/44784) [Bugfix] Prevent cuMemcpyBatchAsync segfault with MTP and KV offloading
- [#44751](https://github.com/vllm-project/vllm/pull/44751) [Bugfix] Gracefully shut down GPU workers when engine-core startup times out or is interrupted (#32116)
- [#44543](https://github.com/vllm-project/vllm/pull/44543) [Bugfix] Couple audio+video in mm processor cache for use_audio_in_video (fixes #44538)
- [#44492](https://github.com/vllm-project/vllm/pull/44492) [Bugfix][Spec-Decode][MLA] Fix CUDA graph capture assertion and missing draft seq_lens_cpu_upper_bound for EAGLE on SINGLE_ONLY MLA backends
- [#45012](https://github.com/vllm-project/vllm/pull/45012) Handle structured output grammar compilation failures
- [#44838](https://github.com/vllm-project/vllm/pull/44838) [PD] Guard bidirectional KV reuse for rewritten history
- [#44619](https://github.com/vllm-project/vllm/pull/44619) [Structured Output] Limit whitespace in JSON schema FSM to prevent runaway whitespace (issue #38696)
- [#45050](https://github.com/vllm-project/vllm/pull/45050) fix: [Feature]: Default eplb num_redundant_experts to the lowest valid val...
- [#44532](https://github.com/vllm-project/vllm/pull/44532) [Bugfix] Fix Gemma4 tool call parser using vocab key instead of decoded token string
- [#44727](https://github.com/vllm-project/vllm/pull/44727) [Bugfix] Fix shape mismatch crash and add logprob_token_ids support in RejectionSampler
- [#44625](https://github.com/vllm-project/vllm/pull/44625) [Bugfix][KV Connector] Gracefully fall back when LMCacheConnectorV1 is degraded
- [#44392](https://github.com/vllm-project/vllm/pull/44392) [Bugfix][Core] Filter reasoning boundary tokens before structured-output FSM advance
- [#44847](https://github.com/vllm-project/vllm/pull/44847) [Bugfix][DeepSeekV4] Add BF16 MTP O-proj fallback for unquantized draft weights
- [#44680](https://github.com/vllm-project/vllm/pull/44680) [Bugfix][Rust Frontend] Validate out-of-vocab token ids in request params
- [#44762](https://github.com/vllm-project/vllm/pull/44762) fix: Pin Ray placement group bundles to allowlisted nodes during scale up
- [#44627](https://github.com/vllm-project/vllm/pull/44627) [Bugfix] Don't crash engine on malformed output-socket frame (#44486)
- [#44628](https://github.com/vllm-project/vllm/pull/44628) [Bugfix][Quantization] Fp8 family: match modules_to_not_convert by substring
- [#44414](https://github.com/vllm-project/vllm/pull/44414) [BugFix] Fix Traceback due to malformed MessagePack (#24655)
- [#44777](https://github.com/vllm-project/vllm/pull/44777) [Bugfix][Frontend] pythonic tool parser: accept negative numbers / unary ops as literal arguments
- [#44993](https://github.com/vllm-project/vllm/pull/44993) [Bugfix][Structured Output][Spec Decode] Advance grammar across reasoning boundary
- [#44743](https://github.com/vllm-project/vllm/pull/44743) [Security] Fix remote DoS from grammar-rejected spec tokens padded with -1
- [#44424](https://github.com/vllm-project/vllm/pull/44424) [Bugfix] Fix CPU memory leak related to not cleaning up old remotes data
- [#44741](https://github.com/vllm-project/vllm/pull/44741) [Bugfix] Gemma4 streaming parser for multi-boundary tool deltas
- [#44778](https://github.com/vllm-project/vllm/pull/44778) Fix FP8 KV wake-up for nested KV cache containers
- [#44868](https://github.com/vllm-project/vllm/pull/44868) [Bugfix] Refresh forward-context tensors before FULL CUDA graph replay
- [#44968](https://github.com/vllm-project/vllm/pull/44968) [Security] Fix DoS via out-of-range stop_token_ids crashing CUDA
- [#44845](https://github.com/vllm-project/vllm/pull/44845) Fix discarded speculative rows leaking logprobs
- [#44913](https://github.com/vllm-project/vllm/pull/44913) Fix tiered offload madv fallback
- [#45055](https://github.com/vllm-project/vllm/pull/45055) [ROCm] Fix AMD build from shuffle mask dtype error while compiling `silu_and_mul_per_block_quant_kernel`
- [#44927](https://github.com/vllm-project/vllm/pull/44927) fix(structured_output): pass new_token_ids to should_advance() to fix MTP spec-decode off-by-one
- [#44384](https://github.com/vllm-project/vllm/pull/44384) [Bugfix][Model] Fix Qwen3 deepstack buffer device mismatch
- [#44401](https://github.com/vllm-project/vllm/pull/44401) [Bugfix] Don't crash EngineCore when structured output grammar compilation fails
- [#45025](https://github.com/vllm-project/vllm/pull/45025) [Bugfix][Rust Frontend] Stop unescaping XML-style tool-call parameter values
- [#44745](https://github.com/vllm-project/vllm/pull/44745) Fix negative cudagraph memory estimate
- [#44504](https://github.com/vllm-project/vllm/pull/44504) fix: logprobs values change with requested count due to token-string collision
- [#45145](https://github.com/vllm-project/vllm/pull/45145) [Bugfix] Clean up ModelOpt LM head state before tying weights
- [#45048](https://github.com/vllm-project/vllm/pull/45048) [Bugfix] GPT-OSS Autodrop reasoning in Response API and cleanup
- [#44409](https://github.com/vllm-project/vllm/pull/44409) [Bugfix] Two-phase KV allocation for cross-group prefix cache hits (supersedes #33775)
- [#44813](https://github.com/vllm-project/vllm/pull/44813) [Bugfix] Replace sequential port scan with atomic port=0 in get_open_ports_list
- [#45118](https://github.com/vllm-project/vllm/pull/45118) [Security] Add timeout guard for regex compilation in structured outp…
- [#44431](https://github.com/vllm-project/vllm/pull/44431) [Bugfix] Don't double-count local prefix cache stats on scheduling retries
- [#44921](https://github.com/vllm-project/vllm/pull/44921) [Bugfix] Lazily import the humming quantization backend
- [#45122](https://github.com/vllm-project/vllm/pull/45122) Fix LFM2 ShortConv quant config propagation
- [#44645](https://github.com/vllm-project/vllm/pull/44645) [Bugfix] Stream Llama4 weight loading to avoid host-OOM with copy-returning loaders
- [#44656](https://github.com/vllm-project/vllm/pull/44656) [fix] Enable parallel tool calls for Harmony (gpt-oss) models
- [#45060](https://github.com/vllm-project/vllm/pull/45060) [Bugfix]Fix out-of-vocabulary recovered token on all-NaN logits (root cause of empty spec-decode output)
- [#44602](https://github.com/vllm-project/vllm/pull/44602) fix(anthropic): preserve inline system message position for prefix caching
</details>

<details>
<summary>Refactors (31)</summary>

- [#44569](https://github.com/vllm-project/vllm/pull/44569) [DSV4] Refactor DeepseekV4Attention
- [#43556](https://github.com/vllm-project/vllm/pull/43556) [Attention] Mamba attention module refactor - LINEAR
- [#44596](https://github.com/vllm-project/vllm/pull/44596) [Refactor][Mistral] Extract parsing logic into MistralParser
- [#43167](https://github.com/vllm-project/vllm/pull/43167) Remove KV cache scale boilerplate from model weight loading methods
- [#44699](https://github.com/vllm-project/vllm/pull/44699) [DSV4] Decouple DS V4 Sparse MLA Metadata from DS V3.2
- [#44884](https://github.com/vllm-project/vllm/pull/44884) [Rust Frontend] Extract shared options in route helper params
- [#42443](https://github.com/vllm-project/vllm/pull/42443) Refactor CT NVFP4 linear to use a single class
- [#44856](https://github.com/vllm-project/vllm/pull/44856) [Rust Frontend] [Refactor] Refine utility call interfaces
- [#43707](https://github.com/vllm-project/vllm/pull/43707) [Logs Refactor] Optimize shutdown logs, easier to follow and consistent
- [#44454](https://github.com/vllm-project/vllm/pull/44454) [1/N][KV-Cache Layout Refactor] Refactor DSV4 KV cache config construction
- [#45081](https://github.com/vllm-project/vllm/pull/45081) [Refactor] Remove dead states from chat completion serving
- [#41471](https://github.com/vllm-project/vllm/pull/41471) [Refactor] Remove dead code in tests and parallel_state
- [#44539](https://github.com/vllm-project/vllm/pull/44539) [mamba] unify KDA conv states into one cache to match 2-state SSM layout
- [#45011](https://github.com/vllm-project/vllm/pull/45011) [Refactor] Rename rocm_moe.py to rocm_moe_rdna.py
- [#44346](https://github.com/vllm-project/vllm/pull/44346) [Refactor] Suppress SyntaxWarning from ast.literal_eval in tool parsers
- [#44122](https://github.com/vllm-project/vllm/pull/44122) [Refactor] Remove dead code fp quant
- [#44367](https://github.com/vllm-project/vllm/pull/44367) [DSV4] Minor cleanup for DeepseekV4MegaMoEExperts
- [#44458](https://github.com/vllm-project/vllm/pull/44458) [4/N][KV-Cache Layout Refactor] Standardize KV cache layout
- [#45104](https://github.com/vllm-project/vllm/pull/45104) [Refactor] Chat Completions Harmony Refactor and Bugfixes
- [#44570](https://github.com/vllm-project/vllm/pull/44570) [MoE Refactor] Combine CompressedTensorsWNA16MarlinMoEMethod with CompressedTensorsWNA16MoEMethod
- [#44681](https://github.com/vllm-project/vllm/pull/44681) [Refactor] Remove dead cutlass mxfp8 code
- [#44857](https://github.com/vllm-project/vllm/pull/44857) [Attention] Mamba attention module refactor - Final part
- [#44455](https://github.com/vllm-project/vllm/pull/44455) [2/N][KV-Cache Layout Refactor] Pack K/V into the content dim across attention backends
- [#44992](https://github.com/vllm-project/vllm/pull/44992) Deprecations for v0.23 and v0.24
- [#44589](https://github.com/vllm-project/vllm/pull/44589) Remove unnecessary `load_weights` methods
- [#44449](https://github.com/vllm-project/vllm/pull/44449) Lwilkinson/kv layout/kv content pack
- [#44941](https://github.com/vllm-project/vllm/pull/44941) [MoE Refactor] Rename FusedMoE to FusedMoEFactory
- [#44562](https://github.com/vllm-project/vllm/pull/44562) Refactor MoE Oracles to use base class MoEKernelOracle
- [#44514](https://github.com/vllm-project/vllm/pull/44514) Deprecate old FP8 online quantization classes
- [#44456](https://github.com/vllm-project/vllm/pull/44456) [3/N][KV-Cache Layout Refactor] Standardize Mamba cache; drop `get_transfer_cache_regions`
- [#44381](https://github.com/vllm-project/vllm/pull/44381) Refactor RMSNorm vectorized launch checks
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
