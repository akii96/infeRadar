# vllm: PR digest (2026-07-26 to 2026-07-30)

_218 merged, 315 newly opened - source vllm-project/vllm, generated 2026-07-30T11:17:19Z_

## TL;DR
- **Model Support**: **Kimi K3** dominated merged work with end-to-end support across Python/Rust frontends, Triton/FlashInfer backends, and MoE/attention kernels. **DeepSeek-V4** is the focus of major in-flight work migrating attention and MoE kernels to a new JIT warmup infrastructure.
- **Hardware & Architecture**: Significant in-progress work targets **NVIDIA SM100 (Blackwell)**, adding NVFP4 KV cache support and VMM-backed SharedEP for native FP4 decode. **CPU** inference saw merged INT8 fused MoE for Arm and in-flight FP8 W8A8 support.
- **Speculative Decoding & State**: Heavy investment in recurrent state caching, with newly opened PRs introducing `ReplaySSM` to cache SSM inputs for faster Gated DeltaNet (GDN) and Mamba2 speculative decoding.
- **Distributed & KV Offload**: Merged generic P2P secondary tier for KV offloading and NIXL heterogeneous block sizes for hybrid models. In-flight work adds Shared-DCP peer-addressable decode data paths.

## Most important PRs
- **[#50089](https://github.com/vllm-project/vllm/pull/50089)** merges end-to-end support for the Kimi K3 model family, including comprehensive Triton and FlashInfer kernels, MoE routing, and integration across both Python and Rust frontends.
- **[#50174](https://github.com/vllm-project/vllm/pull/50174)** opens a new JIT warmup infrastructure with provider registries and orchestration, actively being used to migrate DeepSeek-V4 attention, MoE, and MHC TileLang kernels to reduce first-request latency.
- **[#50392](https://github.com/vllm-project/vllm/pull/50392)** opens VMM-backed SharedEP (Expert Parallelism) for native FP4 decode on NVIDIA SM100, leveraging FlashInfer to optimize MoE execution on upcoming Blackwell hardware.
- **[#49887](https://github.com/vllm-project/vllm/pull/49887)** opens `ReplaySSM`, a mechanism to cache SSM inputs for faster Gated DeltaNet (GDN) speculative decoding, with a companion PR bringing the same optimization to Mamba2.
- **[#48021](https://github.com/vllm-project/vllm/pull/48021)** merges a generic P2P secondary tier for KV offloading, introducing peer lookup and serving via `ParentManager` to lay the groundwork for more advanced disaggregated KV cache architectures.

## More changes by area

<details>
<summary>Performance (27)</summary>

- [#48637](https://github.com/vllm-project/vllm/pull/48637) [CPU][Perf] INT8 Fused MoE Kernel for Arm CPUs
- [#48577](https://github.com/vllm-project/vllm/pull/48577) [CPU][Spec Decode] Optimize GDN conv path for speculative decoding
- [#49903](https://github.com/vllm-project/vllm/pull/49903) [Core] Warm up runner-owned Triton kernels before the first request
- [#48407](https://github.com/vllm-project/vllm/pull/48407) [Attention] Skip sparse indexer scoring for dense short prefills
- [#48442](https://github.com/vllm-project/vllm/pull/48442) [Perf] Zero-copy torch.Tensor pickling in shm_broadcast MessageQueue
- [#49618](https://github.com/vllm-project/vllm/pull/49618) perf: dispatch non-grouped bias-less topk routing methods to fused path
- [#49731](https://github.com/vllm-project/vllm/pull/49731) [Spec Decode][Perf] Replicate DSpark Markov head across TP ranks
- [#49607](https://github.com/vllm-project/vllm/pull/49607) [Perf] Hash videos by source bytes
- [#48774](https://github.com/vllm-project/vllm/pull/48774) [Perf] Tune LL BF16 Router GEMM
- [#49531](https://github.com/vllm-project/vllm/pull/49531) [Perf] DeepSeek-OCR-2 TTFT Optimize
- [#50004](https://github.com/vllm-project/vllm/pull/50004) [DSv4 Perf] Adaptive topk width, 1.0% E2E throughput improvement
- [#49750](https://github.com/vllm-project/vllm/pull/49750) [Perf] RMSNorm uncontiguous support, 1.2~3.1x kernel performance improvement
- [#49524](https://github.com/vllm-project/vllm/pull/49524) [Perf] Isolate MM preprocessing on its own executor
- [#47711](https://github.com/vllm-project/vllm/pull/47711) [MRV2][Performance] Skip no-op FP32 logits materialization
- [#48739](https://github.com/vllm-project/vllm/pull/48739) [Perf] Make merge attention context count a runtime argument
- [#50233](https://github.com/vllm-project/vllm/pull/50233) [Model][Perf] Overlap mixed GDN decode and prefill recurrent kernels
- [#50106](https://github.com/vllm-project/vllm/pull/50106) [ROCm][Perf] DeepSeek-V4 skip ragged layout packing for topk indices in sparse attn prefill
- [#50395](https://github.com/vllm-project/vllm/pull/50395) [Perf][MoE] Enable clamped SwiGLU and fused unpermute for NVFP4 CUTLASS
- [#49870](https://github.com/vllm-project/vllm/pull/49870) [ROCm][Perf] Speed up single-group MoE routing
- [#50410](https://github.com/vllm-project/vllm/pull/50410) perf(scheduler): balance requests across PP batches
- [#50114](https://github.com/vllm-project/vllm/pull/50114) [Core][Perf] Skip no-op block-hasher calls between full-block boundaries
- [#50230](https://github.com/vllm-project/vllm/pull/50230) [Perf][CUDA] Programmatic dependent launch for the DSA decode kernels
- [#50365](https://github.com/vllm-project/vllm/pull/50365) [Perf][Sparse MLA] Drop the atomic contention in the index remap
- [#50298](https://github.com/vllm-project/vllm/pull/50298) [DSv4 Perf] Remove redundant full kernel for dsv4, 1.88x kernel performance improvement
- [#49872](https://github.com/vllm-project/vllm/pull/49872) [ROCm][Perf] Speed up large MoE ReLU-squared on gfx90a
- [#50212](https://github.com/vllm-project/vllm/pull/50212) [ROCm][Perf][Model] Fuse Qwen3-VL attention prologue into single AITER kernel
- [#50185](https://github.com/vllm-project/vllm/pull/50185) attn_res kernel latency improvements

</details>

<details>
<summary>Kernels & attention (39)</summary>

- [#50090](https://github.com/vllm-project/vllm/pull/50090) [Kimi-K3] Add AttnRes kernels
- [#49937](https://github.com/vllm-project/vllm/pull/49937) [ROCm] Add AITER FP8 ViT encoder attention
- [#49348](https://github.com/vllm-project/vllm/pull/49348) [ROCm][Quark][6/N] Use MXFP4 linear kernel abstraction for `aiter` backend
- [#49152](https://github.com/vllm-project/vllm/pull/49152) [KV-offload][FS] : Batch store/load_block in C
- [#49291](https://github.com/vllm-project/vllm/pull/49291) [Kernel][Mamba] Fused-kernel support for align-mode DS-conv state migration with num_accepted_tokens > 1
- [#46340](https://github.com/vllm-project/vllm/pull/46340) [Kernel] TD operand loads for batched MoE GEMM (moe_mmk) on XPU
- [#42436](https://github.com/vllm-project/vllm/pull/42436) fused_moe: add VLLM_TRITON_USE_TD tensor-descriptor path
- [#42669](https://github.com/vllm-project/vllm/pull/42669) [Attention] Integrate FlashAttention 4 SM100 headdim 256 support
- [#46491](https://github.com/vllm-project/vllm/pull/46491) [AMD] Revert `Mxfp4MoeBackend.TRITON_UNFUSED` fallback
- [#49995](https://github.com/vllm-project/vllm/pull/49995) [MRV2] Always build attn metadata at capture time (#49364)
- [#47773](https://github.com/vllm-project/vllm/pull/47773) [ROCm] Cache fp32 upcast of static e8m0 weight scale in AITER scaled_mm
- [#45841](https://github.com/vllm-project/vllm/pull/45841) add epilogue hook to flex attention
- [#50244](https://github.com/vllm-project/vllm/pull/50244) [torch.compile] Compile `CustomOp.forward_native` for ReLU^2 to avoid raw torch ops inside opaque custom ops
- [#50176](https://github.com/vllm-project/vllm/pull/50176) [2/N][warmup][DSv4] Migrate attention kernels
- [#50380](https://github.com/vllm-project/vllm/pull/50380) Gdn ucache backend
- [#50177](https://github.com/vllm-project/vllm/pull/50177) [3/N][warmup][DSv4] Migrate MoE kernels
- [#50140](https://github.com/vllm-project/vllm/pull/50140) WIP: FlashInfer ReplaySSM kernel
- [#50175](https://github.com/vllm-project/vllm/pull/50175) [1/N][warmup][DSv4] Migrate shared NVIDIA and MLA kernels
- [#50246](https://github.com/vllm-project/vllm/pull/50246) [Feature]: Add DFly speculative decoding and D-Cut support（Related to issue 50245）
- [#49847](https://github.com/vllm-project/vllm/pull/49847) [Kernel] ReplaySSM: cache SSM inputs for faster Mamba2 speculative decode
- [#50172](https://github.com/vllm-project/vllm/pull/50172) [Feature] Qwen3-Next (GDN): mamba_cache_mode="all" prefix caching with speculative decoding (MTP) on V1
- [#50178](https://github.com/vllm-project/vllm/pull/50178) [4/N][warmup][DSv4] Migrate MHC TileLang kernels
- [#50226](https://github.com/vllm-project/vllm/pull/50226) [Kernel] Optimize SM103 GDN causal-conv prefills
- [#50306](https://github.com/vllm-project/vllm/pull/50306) [Model Runner V2][Spec Decode] Gather MM embeddings for all MTP modules
- [#50062](https://github.com/vllm-project/vllm/pull/50062) [Model Runner V2][Spec Decode] Add KV cache support for multi-layer MTP
- [#50032](https://github.com/vllm-project/vllm/pull/50032) [Attention][MiniMax-M3] Add MSA speculative decode verification
- [#49969](https://github.com/vllm-project/vllm/pull/49969) [Spec Decode] Add top-k DSpark Markov projection
- [#50156](https://github.com/vllm-project/vllm/pull/50156) [Cohere][Spec Decode] Add CohereEagleProposer to support multi layer eagle drafts
- [#50279](https://github.com/vllm-project/vllm/pull/50279) [Kernel] Fuse strided GDN RMSNorm gating on SM103
- [#50372](https://github.com/vllm-project/vllm/pull/50372) [Kernel] Fuse FlashInfer GDN prefill state I/O
- [#50400](https://github.com/vllm-project/vllm/pull/50400) [Kernel][Kimi] fused vision q/k roper kernel
- [#50201](https://github.com/vllm-project/vllm/pull/50201) [Kernel] Harden top_k_per_row against NaN and under-filled output
- [#50294](https://github.com/vllm-project/vllm/pull/50294) [Kernel][Model] Optimize FA4 mm_prefix range lookup
- [#49862](https://github.com/vllm-project/vllm/pull/49862) [Kernel] Guard A8 Marlin repack K alignment
- [#50157](https://github.com/vllm-project/vllm/pull/50157) [Kernel] Add support for Flashinfer Mamba SSU algorithm selection
- [#50193](https://github.com/vllm-project/vllm/pull/50193) [Helion] Improve fused QK config selection
- [#50371](https://github.com/vllm-project/vllm/pull/50371) [ROCm] Enable 12-head MLA persistent decode
- [#50339](https://github.com/vllm-project/vllm/pull/50339) [FlexAttention] Avoid encoder block-mask compile explosion
- [#50148](https://github.com/vllm-project/vllm/pull/50148) [Attention]: Use KVCacheSpec for AttentionMetadataBuilder type hints

</details>

<details>
<summary>MoE & quantization (20)</summary>

- [#47124](https://github.com/vllm-project/vllm/pull/47124) [Quantization][Autoround][XPU] Add W4A16(moe) / MXFP4(linear/moe) Support
- [#47514](https://github.com/vllm-project/vllm/pull/47514) [Quantization][INC]Add MXFP8 Linear Support
- [#49580](https://github.com/vllm-project/vllm/pull/49580) Integrate CuTeDSL MoE for ReLU2 NVFP4
- [#43229](https://github.com/vllm-project/vllm/pull/43229) [CompressedTensors] FP4 Qutlass Integration
- [#48876](https://github.com/vllm-project/vllm/pull/48876) [Model] Add Inkling compressed-tensors dynamic FP8 support
- [#50016](https://github.com/vllm-project/vllm/pull/50016) [HelionLinearBackend][4/N] Add HelionINT8ScaledMMLinearKernel
- [#49979](https://github.com/vllm-project/vllm/pull/49979) [Kernel] Add SM90 W4AFP8 grouped MoE CUTLASS operator
- [#50415](https://github.com/vllm-project/vllm/pull/50415) Add MoNe experts pruning support
- [#50168](https://github.com/vllm-project/vllm/pull/50168) LUT-B quantization accuracy prototype
- [#50096](https://github.com/vllm-project/vllm/pull/50096) [Kernel] Use expanding ldmatrix for Marlin W4A8
- [#50396](https://github.com/vllm-project/vllm/pull/50396) [Quantization][Autoround][ARK] Add ARK W4A16(moe) Support
- [#50317](https://github.com/vllm-project/vllm/pull/50317) add dual RMSNorm quant fusion pattern
- [#50030](https://github.com/vllm-project/vllm/pull/50030) [Quantization] Add per-token NVFP4 CuTe-DSL MoE backend
- [#50113](https://github.com/vllm-project/vllm/pull/50113) [MoE] Consolidate expert placement strategy resolution
- [#49932](https://github.com/vllm-project/vllm/pull/49932) [Linear] [Kernel] add block-wise scaled_mm
- [#50401](https://github.com/vllm-project/vllm/pull/50401) [Feature][Quantization] Add per-layer online quantization configuration (#50281)
- [#50205](https://github.com/vllm-project/vllm/pull/50205) trtllm fp8 moe sm100 compatibility
- [#50383](https://github.com/vllm-project/vllm/pull/50383) Shard the K3 Latent-MoE up-projection on large batches
- [#50378](https://github.com/vllm-project/vllm/pull/50378) [ROCm] Pass pointers to FlyDSL MoE kernels
- [#50273](https://github.com/vllm-project/vllm/pull/50273) [Quantization] Honor `--linear-backend` for ModelOpt W4A16

</details>

<details>
<summary>Model support (18)</summary>

- [#48841](https://github.com/vllm-project/vllm/pull/48841) [ROCm] [Model] Enable TML inkling
- [#48791](https://github.com/vllm-project/vllm/pull/48791) [ModelRunner V2] Enable sequence pooling for embedding and classification models
- [#47750](https://github.com/vllm-project/vllm/pull/47750) [Feature] Add VidCom2 video token pruning
- [#49331](https://github.com/vllm-project/vllm/pull/49331) [ModelRunner V2] Support encoder-only attention
- [#50210](https://github.com/vllm-project/vllm/pull/50210) [Model] Support Qwen3.5 text-only dense and MoE models
- [#50092](https://github.com/vllm-project/vllm/pull/50092) [Misc][Minimax-M3]add default video_processor
- [#50313](https://github.com/vllm-project/vllm/pull/50313) Revert "[Misc][Minimax-M3]add default video_processor ([#50092](https://github.com/vllm-project/vllm/pull/50092))"
- [#48912](https://github.com/vllm-project/vllm/pull/48912) [Model] Enable EVS for Qwen3.5
- [#45429](https://github.com/vllm-project/vllm/pull/45429) [Model] Support top_k and top_p sampling for DiffusionGemma
- [#50138](https://github.com/vllm-project/vllm/pull/50138) Codex/kimi k3 dspark pp
- [#50077](https://github.com/vllm-project/vllm/pull/50077) [Model] Add native RWKV7 serving, fused execution, and quantization
- [#50229](https://github.com/vllm-project/vllm/pull/50229) [Parser] Migrate Kimi K3 to Parser Engine
- [#49997](https://github.com/vllm-project/vllm/pull/49997) 3a80b-kda-attnres-dsrouting
- [#49934](https://github.com/vllm-project/vllm/pull/49934) [1/N] Unify multiple-path encoder cuda graph support
- [#50107](https://github.com/vllm-project/vllm/pull/50107) Support mm_processor_cache in the Transformers multimodal backend
- [#49852](https://github.com/vllm-project/vllm/pull/49852) [MRV2][Multimodal] Enable encoder cuda graph for model runner v2
- [#50354](https://github.com/vllm-project/vllm/pull/50354) [Model] Add Mage-VL multimodal model support
- [#50293](https://github.com/vllm-project/vllm/pull/50293) [Model Runner V2] Enable encoder token classification

</details>

<details>
<summary>Parallelism & scheduling (35)</summary>

- [#48906](https://github.com/vllm-project/vllm/pull/48906) [KV Offload] Deduplicate replicated MLA KV in the shared CPU region
- [#49502](https://github.com/vllm-project/vllm/pull/49502) [3/N][Core][KV Connector] Support reliable partial-tail KV offload for sub-block prompts
- [#47288](https://github.com/vllm-project/vllm/pull/47288) [Elastic EP] Async preparation
- [#49612](https://github.com/vllm-project/vllm/pull/49612) [KV Connector] Support NIXL heterogeneous P/D block sizes for hybrid models
- [#46116](https://github.com/vllm-project/vllm/pull/46116) [Core][KV-transfer] MoRIIO: heterogeneous TP<->DP prefill/decode read routing
- [#48123](https://github.com/vllm-project/vllm/pull/48123) [KV Offloading] Per-request tier filtering with TierFilter/TierMatcher
- [#49762](https://github.com/vllm-project/vllm/pull/49762) [KV Connector] Support NIXL P/D for hybrid MLA+SSM models
- [#49114](https://github.com/vllm-project/vllm/pull/49114) Add CachePolicyFactory for pluggable/external eviction policies
- [#49858](https://github.com/vllm-project/vllm/pull/49858) [KV Offload] Make compact secondary identity TP-independent
- [#46877](https://github.com/vllm-project/vllm/pull/46877) [Core][Distributed] Add process-checkpoint lifecycle hooks for communicators (starting with Flashinfer)
- [#50094](https://github.com/vllm-project/vllm/pull/50094) [KV Offload] Move CPUOffloadingSpec onto SharedOffloadRegion
- [#48879](https://github.com/vllm-project/vllm/pull/48879) [Core] Fail fast when /dev/shm is too small for the shm ring buffer
- [#49647](https://github.com/vllm-project/vllm/pull/49647) [Rubin] Enable NVLink all-reduce paths on SM107
- [#49582](https://github.com/vllm-project/vllm/pull/49582) [EC Connector] Add has_pending_push_work
- [#49345](https://github.com/vllm-project/vllm/pull/49345) [PD][NixlPush] Skip extra `add_remote_agent` step in D->P handshake
- [#50009](https://github.com/vllm-project/vllm/pull/50009) [DCP][Performance] Add Shared-DCP peer-addressable decode data paths
- [#50251](https://github.com/vllm-project/vllm/pull/50251) [Draft][Reload] Add manifest-driven load receipts and update scopes
- [#50010](https://github.com/vllm-project/vllm/pull/50010) [DCP][Kernel] Add Shared-DCP consumer-direct Top-K
- [#49994](https://github.com/vllm-project/vllm/pull/49994) [EC Connector] EC Offloading Connector use events instead of StepTracker
- [#50422](https://github.com/vllm-project/vllm/pull/50422) [kv_offload] Session Aware Eviction Policy
- [#50063](https://github.com/vllm-project/vllm/pull/50063) [Kimi-K3] MoRIIO KV transfer of hybrid mamba/KDA (conv+ssm) recurrent state (READ + WRITE)
- [#50366](https://github.com/vllm-project/vllm/pull/50366) DCP: consume owner-sharded Top-K candidates through symmetric memory
- [#49956](https://github.com/vllm-project/vllm/pull/49956) [Metrics] Export EPLB rebalancing state and events
- [#50045](https://github.com/vllm-project/vllm/pull/50045) Backpressure
- [#50087](https://github.com/vllm-project/vllm/pull/50087) [KV Offload] Per-request store strategy hook (covers #42050 + admission seam)
- [#50390](https://github.com/vllm-project/vllm/pull/50390) [EPD] Remove duplicate image preprocessing in EPD and enable preprocess on GPU
- [#50134](https://github.com/vllm-project/vllm/pull/50134) [Core] Add KV event state snapshots
- [#50374](https://github.com/vllm-project/vllm/pull/50374) [KV Connector][Mooncake] Add MooncakePromMetrics and wire via build_prom_metrics
- [#49919](https://github.com/vllm-project/vllm/pull/49919) [Core] Explicitly manage torch CPU threads in workers
- [#50070](https://github.com/vllm-project/vllm/pull/50070) [CUDA] Select the canonical runtime for host-registration fallback
- [#50301](https://github.com/vllm-project/vllm/pull/50301) [KV Offload] Enable single-copy MLA layout for CPUOffloadingSpec
- [#50382](https://github.com/vllm-project/vllm/pull/50382) [DCP] Expose query replication for GLM sparse attention
- [#50299](https://github.com/vllm-project/vllm/pull/50299) [Core] Add TP-invariant tree kernels across TP sizes
- [#50321](https://github.com/vllm-project/vllm/pull/50321) [KV Offload] Support partial secondary-tier load results
- [#50002](https://github.com/vllm-project/vllm/pull/50002) [Core] Zero KV cache when NaN logits detected

</details>

<details>
<summary>Hardware & arch (13)</summary>

- [#49571](https://github.com/vllm-project/vllm/pull/49571) [Hardware][Power] Add FAST_EXP for Power
- [#49394](https://github.com/vllm-project/vllm/pull/49394) [XPU] Enable QK Norm + RoPE fusion pass on XPU
- [#47121](https://github.com/vllm-project/vllm/pull/47121) [XPU] Route weightless RMSNorm to _C dispatch
- [#50387](https://github.com/vllm-project/vllm/pull/50387) [CPU] Bump up CPU kernels to latest version
- [#49942](https://github.com/vllm-project/vllm/pull/49942) [CPU] Add CPU FP8 W8A8 linear/MoE support
- [#50133](https://github.com/vllm-project/vllm/pull/50133) [CPU] Migrate unquantized MoE to the modular-kernel experts structure
- [#50288](https://github.com/vllm-project/vllm/pull/50288) [SM120] Add NVFP4 KV cache support for consumer Blackwell (RTX 5090)
- [#49943](https://github.com/vllm-project/vllm/pull/49943) [XPU] Support mxfp4 Sequence Parallelism on XPU
- [#49891](https://github.com/vllm-project/vllm/pull/49891) SM120 NVFP4 KV cache support + MTP cudagraph fix + KV offload crash fix
- [#49888](https://github.com/vllm-project/vllm/pull/49888) [ROCm] Support AITER paged attention on gfx90a
- [#50319](https://github.com/vllm-project/vllm/pull/50319) [ROCm][Kimi-K3] Enable gfx942 serving
- [#50219](https://github.com/vllm-project/vllm/pull/50219) [CPU][s390x] Optimize inference perf and add oneDNN INT8 GEMM for s390x
- [#50038](https://github.com/vllm-project/vllm/pull/50038) [XPU] Gate FlashAttention-in-graph on oneAPI 2026.0+ runtime support

</details>

<details>
<summary>API & serving (35)</summary>

- [#50093](https://github.com/vllm-project/vllm/pull/50093) [Model] Add Kimi K3 support: Python frontend [2/2]
- [#47301](https://github.com/vllm-project/vllm/pull/47301) [Frontend] Add detokenization streaming derender for disaggregated serving
- [#49491](https://github.com/vllm-project/vllm/pull/49491) [Rust Frontend][gRPC] Add server and model discovery
- [#49341](https://github.com/vllm-project/vllm/pull/49341) [Rust Frontend] Send multimodal tensors in auxiliary frames
- [#49665](https://github.com/vllm-project/vllm/pull/49665) [Frontend][Core] Standardize request error handling with VLLMError hierarchy
- [#49992](https://github.com/vllm-project/vllm/pull/49992) [Rust Frontend] Add ordinary-text tokenizer encoding
- [#49604](https://github.com/vllm-project/vllm/pull/49604) [Rust Frontend] Add --limit-mm-per-prompt support
- [#48543](https://github.com/vllm-project/vllm/pull/48543) [Frontend] Add diarized_json support for MOSS-Transcribe-Diarize
- [#47494](https://github.com/vllm-project/vllm/pull/47494) [Rust Frontend] Align sampling validation with Python
- [#48145](https://github.com/vllm-project/vllm/pull/48145) [Frontend] Reuse prefill token ids on the decode chat path for disaggregated serving
- [#50033](https://github.com/vllm-project/vllm/pull/50033) [Rust Frontend][gRPC] Add KV event source discovery
- [#49040](https://github.com/vllm-project/vllm/pull/49040) [Core][Frontend] Add weight version tagging for RL rollouts
- [#49754](https://github.com/vllm-project/vllm/pull/49754) [Frontend] expose stream_interval as req sampling param
- [#49944](https://github.com/vllm-project/vllm/pull/49944) [Rust Frontend] Keep `--max-model-len` engine-owned
- [#50129](https://github.com/vllm-project/vllm/pull/50129) [Rust Frontend] Extract shared tracing setup logic into `vllm-tracing`
- [#49914](https://github.com/vllm-project/vllm/pull/49914) [Frontend] Lazily initialize chat media connectors
- [#49907](https://github.com/vllm-project/vllm/pull/49907) [Tokenizer] Use HF config for HF tokenizers
- [#50034](https://github.com/vllm-project/vllm/pull/50034) [Core][PCP] Select MRV2 when PCP is enabled
- [#50195](https://github.com/vllm-project/vllm/pull/50195) [Frontend] Add stateless /v1/responses/render endpoint
- [#49879](https://github.com/vllm-project/vllm/pull/49879) [FEAT] Support fast engine recovery through weight cache
- [#49998](https://github.com/vllm-project/vllm/pull/49998) [Rust Frontend] Support EngineCore reattachment across frontend restarts
- [#50198](https://github.com/vllm-project/vllm/pull/50198) [Rust Frontend] Add MiniCPM5 XML tool parser
- [#49929](https://github.com/vllm-project/vllm/pull/49929) [Model Loader] Introduce custom weight copy
- [#50368](https://github.com/vllm-project/vllm/pull/50368) [Rust Frontend][gRPC] Add multimodal image inference
- [#50362](https://github.com/vllm-project/vllm/pull/50362) [Frontend] Add verbose_json support for MOSS-Transcribe-Diarize
- [#50289](https://github.com/vllm-project/vllm/pull/50289) [Rust Frontend] Add standalone Rust renderer
- [#49855](https://github.com/vllm-project/vllm/pull/49855) [Rust Frontend] Support --allowed-local-media-path and --allowed-media-domains
- [#50370](https://github.com/vllm-project/vllm/pull/50370) [Rust Frontend] Propagate W3C trace headers to engine-core requests
- [#50164](https://github.com/vllm-project/vllm/pull/50164) [Frontend][Rust] Support mm_processor_kwargs in chat completions
- [#49885](https://github.com/vllm-project/vllm/pull/49885) [Feature][Frontend] Make strict tool calling an explicit override
- [#50283](https://github.com/vllm-project/vllm/pull/50283) [Core] Add --enable-nan-fault-tolerance for NaN detection and request abort
- [#50403](https://github.com/vllm-project/vllm/pull/50403) [Frontend] Preserve bare Inkling text in Python and Rust parsers
- [#49990](https://github.com/vllm-project/vllm/pull/49990) Resolve revision to commit_hash once per model load (when loading from HF Hub)
- [#50058](https://github.com/vllm-project/vllm/pull/50058) [Rust Frontend] Prevent invalid token IDs in random benchmarks
- [#50402](https://github.com/vllm-project/vllm/pull/50402) add logs to local the garbled text issue

</details>

<details>
<summary>Tests (22)</summary>

- [#49957](https://github.com/vllm-project/vllm/pull/49957) Improve Transformers modelling backend `fx` tracer
- [#47920](https://github.com/vllm-project/vllm/pull/47920) [Tests][Spec Decode] Add gemma4 MTP acceptance rates test
- [#50081](https://github.com/vllm-project/vllm/pull/50081) [Rust][Benchmark] Make `vllm bench serve` Rust delegation opt-in
- [#49974](https://github.com/vllm-project/vllm/pull/49974) [Test] dynamic_shapes_compilation
- [#50110](https://github.com/vllm-project/vllm/pull/50110) [Test] Make EPD correctness tests configurable for XPU
- plus 17 more minor test updates

</details>

<details>
<summary>CI & build (28)</summary>

- [#50132](https://github.com/vllm-project/vllm/pull/50132) [CI] Add comment-based Buildkite triggers
- [#50318](https://github.com/vllm-project/vllm/pull/50318) [CI] Retry failed steps on new PR commits
- [#50414](https://github.com/vllm-project/vllm/pull/50414) [CI] Improve comment-triggered authorization and retries
- [#49422](https://github.com/vllm-project/vllm/pull/49422) [XPU][CI] Add more test cases in Intel GPU CI
- [#48257](https://github.com/vllm-project/vllm/pull/48257) [ROCm] [CI] Support cached K/V (key/value=None) in Triton prefix-prefill
- plus 23 more minor CI and build updates

</details>

<details>
<summary>Docs (8)</summary>

- [#49066](https://github.com/vllm-project/vllm/pull/49066) [docs] Add documentation for pynvvideocodec video decoding backend
- [#45432](https://github.com/vllm-project/vllm/pull/45432) [Docs] Expand llm-d integration page
- [#50308](https://github.com/vllm-project/vllm/pull/50308) [DOC][CPU] remove tcmalloc warning from CPU docs
- [#49782](https://github.com/vllm-project/vllm/pull/49782) [Doc] Add compile cache volume example to the Docker deployment page
- [#49376](https://github.com/vllm-project/vllm/pull/49376) [Docs] Document NVFP4 GEMM kernel selection and Marlin weight-only fallback
- [#50071](https://github.com/vllm-project/vllm/pull/50071) [Misc][Docs] Add comprehensive Responses API documentation and unit tests
- [#50260](https://github.com/vllm-project/vllm/pull/50260) Docs/output token control sampling params
- [#50397](https://github.com/vllm-project/vllm/pull/50397) docs(security): document Ray cluster trust model and env var propagation

</details>

<details>
<summary>Bugfixes (117)</summary>

- [#49877](https://github.com/vllm-project/vllm/pull/49877) [Bugfix][KV Offload][P2P] Scope serve state to fetch rounds
- [#48245](https://github.com/vllm-project/vllm/pull/48245) [BugFix] Fix `num_output_placeholders` preemption underflow
- [#49987](https://github.com/vllm-project/vllm/pull/49987) Fix MQA with tensor parallelism on transformers modeling backend
- [#49747](https://github.com/vllm-project/vllm/pull/49747) [MXFP8][ROCm] Fix MXFP8 MoE backend selection
- [#49343](https://github.com/vllm-project/vllm/pull/49343) [BugFix] eagle draft max position embeddings
- plus 112 more minor bugfixes

</details>

<details>
<summary>Refactors (5)</summary>

- [#49745](https://github.com/vllm-project/vllm/pull/49745) [Refactor] Remove dead code in multiple files
- [#46765](https://github.com/vllm-project/vllm/pull/46765) [ROCm][Quantization][5/N] Refactor quark_moe w8a8-int8 w/ oracle
- [#49988](https://github.com/vllm-project/vllm/pull/49988) [Misc][PD] Nixl cleanup `get_backend_aware_kv_block_len` and `virtually_split_kv_in_blocks`
- [#50285](https://github.com/vllm-project/vllm/pull/50285) [Refactor] Remove multiple dead codes
- [#50066](https://github.com/vllm-project/vllm/pull/50066) [Refactor][PCP] Make PCPManager construction extensible

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 47123fe67378decfbb2a280a4e29c83b22691bfc715ddfc4a64336df3a207324 -->
