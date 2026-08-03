# vllm: PR digest (2026-07-29 to 2026-08-02)

_189 merged, 341 newly opened - source vllm-project/vllm, generated 2026-08-02T22:12:00Z_

## TL;DR
- **Model Focus**: **Kimi K3** dominated this window with massive PRs landing core model files, Triton kernels, and Python frontend support, alongside ongoing work for DCP and KDA decode fusions. **DeepSeek** (V3.2 and V4) also saw heavy attention with sequence parallelism, eager break optimizations, and redundant kernel removals.
- **Hardware & Arch**: Expanded hardware support significantly, merging AMD **gfx1250 ROCm** architecture enablement and opening PRs for upcoming **SM100 native FP4 decode** (via VMM-backed SharedEP) and **consumer Blackwell (RTX 5090)** NVFP4 KV cache.
- **Performance & Kernels**: Needle-moving performance work includes a unified engine-based parser for Mistral, sequence pooling for embedding models, and in-progress work on a new `Gdn ucache` backend and uneven decode context parallelism for heterogeneous TP ranks.
- **Disaggregated Serving**: Advanced disaggregated serving capabilities with a new detokenization streaming derender, prefill token ID reuse on the decode chat path, and per-layer canonical KV page mappings for parallelism-agnostic offload.

## Most important PRs
- **[#50089](https://github.com/vllm-project/vllm/pull/50089)** - **[Model] Add Kimi K3 support: model files and kernels [1/N]**: Introduces core model architecture, Triton kernels, and distributed components for the Kimi K3 model, marking a major new model family addition.
- **[#50392](https://github.com/vllm-project/vllm/pull/50392)** - **[Kernel][MoE] Add VMM-backed SharedEP for native FP4 decode on SM100**: (Newly opened) Implements native FP4 decode support for upcoming Blackwell SM100 GPUs using Virtual Memory Management for shared expert parallelism.
- **[#46516](https://github.com/vllm-project/vllm/pull/46516)** - **Enable gfx1250 ROCm architecture**: Adds comprehensive support for AMD's gfx1250 architecture, including Triton backends, attention, MoE, and quantization kernels.
- **[#48947](https://github.com/vllm-project/vllm/pull/48947)** - **[PARSER][Mistral] unified engine-based parser for reasoning and tool calls**: Unifies the parsing logic for Mistral models, improving handling of reasoning blocks and tool calls directly within the engine.
- **[#50736](https://github.com/vllm-project/vllm/pull/50736)** - **[Feature] Uneven decode context parallelism for heterogeneous TP ranks**: (Newly opened) Enables efficient decode context parallelism across mismatched GPUs by allowing uneven distribution of tensor parallel ranks.

## More changes by area

<details>
<summary>Performance (27)</summary>

- [#49236](https://github.com/vllm-project/vllm/pull/49236) Optimize workspace reuse for eager break, 3.9% E2E TTFT improvement for DSv4
- [#50219](https://github.com/vllm-project/vllm/pull/50219) Optimize inference perf and add oneDNN INT8 GEMM for s390x
- [#49731](https://github.com/vllm-project/vllm/pull/49731) Replicate DSpark Markov head across TP ranks
- [#50590](https://github.com/vllm-project/vllm/pull/50590) Reduce startup log noise
- [#50298](https://github.com/vllm-project/vllm/pull/50298) Remove redundant full kernel for dsv4, 1.88x kernel performance improvement
- [#49750](https://github.com/vllm-project/vllm/pull/49750) RMSNorm uncontiguous support, 1.2~3.1x kernel performance improvement
- [#50312](https://github.com/vllm-project/vllm/pull/50312) Fix redundant memory allocation and copy for dsv4 pp buffer
- [#50654](https://github.com/vllm-project/vllm/pull/50654) (open) Kimi-K3 Fused kernel for KDA decode
- [#50670](https://github.com/vllm-project/vllm/pull/50670) (open) Opt-in fused QK norm+RoPE, SiLU+FP8, and ShortConv decode kernels for LFM2.5
- [#50737](https://github.com/vllm-project/vllm/pull/50737) (open) Optimize DSpark Markov head with addmm
- [#50233](https://github.com/vllm-project/vllm/pull/50233) (open) Overlap mixed GDN decode and prefill recurrent kernels
- [#50619](https://github.com/vllm-project/vllm/pull/50619) (open) Fix Kimi-K3 DSpark FP8 MLA verification
- [#50657](https://github.com/vllm-project/vllm/pull/50657) (open) Fuse and FP8-pack Kimi-K3 latent MoE output tail
- [#50593](https://github.com/vllm-project/vllm/pull/50593) (open) Fuse AttnRes state updates and norms for Kimi-K3
- [#50637](https://github.com/vllm-project/vllm/pull/50637) (open) Fuse Kimi-K3 AttnRes with RMSNorm
- [#50666](https://github.com/vllm-project/vllm/pull/50666) (open) Dispatch Kimi-K3 KDA group64 projection
- [#50554](https://github.com/vllm-project/vllm/pull/50554) (open) Fuse KDA upper-triangle zeroing for Kimi-K3
- [#50636](https://github.com/vllm-project/vllm/pull/50636) (open) Select wvSplitK only in measured-profitable gfx950 regions
- [#50716](https://github.com/vllm-project/vllm/pull/50716) (open) Speed up multimodal placeholder and token-match scanning
- [#50395](https://github.com/vllm-project/vllm/pull/50395) (open) Enable clamped SwiGLU and fused unpermute for NVFP4 CUTLASS
- [#50459](https://github.com/vllm-project/vllm/pull/50459) (open) Optimize memory for GLM 5.2
- [#50664](https://github.com/vllm-project/vllm/pull/50664) (open) Fuse Kimi-K3 MLA output gate
- [#50585](https://github.com/vllm-project/vllm/pull/50585) (open) Optimize k3 dspark fused kv, 3.8~4x kernel performance improvement
- [#50212](https://github.com/vllm-project/vllm/pull/50212) (open) Fuse Qwen3-VL attention prologue into single AITER kernel
- [#50410](https://github.com/vllm-project/vllm/pull/50410) (open) Balance requests across PP batches
- [#50566](https://github.com/vllm-project/vllm/pull/50566) (open) Eliminate per-decode allocations and output copy
- [#50592](https://github.com/vllm-project/vllm/pull/50592) (open) Return KDA projection output directly for Kimi-K3

</details>

<details>
<summary>Kernels & attention (32)</summary>

- [#48770](https://github.com/vllm-project/vllm/pull/48770) Enable masked MHA for sparse MLA prefills
- [#49937](https://github.com/vllm-project/vllm/pull/49937) Add AITER FP8 ViT encoder attention
- [#48257](https://github.com/vllm-project/vllm/pull/48257) Support cached K/V in Triton prefix-prefill
- [#49291](https://github.com/vllm-project/vllm/pull/49291) Mamba Fused-kernel support for align-mode DS-conv state migration
- [#48757](https://github.com/vllm-project/vllm/pull/48757) Fuse Transformers Residual Add + RMSNorm
- [#50476](https://github.com/vllm-project/vllm/pull/50476) Mask the AITER MLA small-head verify flatten causally
- [#46981](https://github.com/vllm-project/vllm/pull/46981) Unify XPU RMSNorm kernels with vllm_c
- [#50339](https://github.com/vllm-project/vllm/pull/50339) Avoid encoder block-mask compile explosion
- [#50148](https://github.com/vllm-project/vllm/pull/50148) Use KVCacheSpec for AttentionMetadataBuilder type hints
- [#48047](https://github.com/vllm-project/vllm/pull/48047) Remove sparse-MLA q-head padding for FlashInfer >=0.6.14
- [#50242](https://github.com/vllm-project/vllm/pull/50242) K3 DSpark AR fusion
- [#40289](https://github.com/vllm-project/vllm/pull/40289) Detect Triton-AMD kernels at their new aiter location
- [#47121](https://github.com/vllm-project/vllm/pull/47121) Route weightless RMSNorm to _C dispatch
- [#50244](https://github.com/vllm-project/vllm/pull/50244) Compile CustomOp.forward_native for ReLU^2
- [#50380](https://github.com/vllm-project/vllm/pull/50380) (open) Add Gdn ucache backend
- [#50466](https://github.com/vllm-project/vllm/pull/50466) (open) Optimize fused QK norm RoPE on B200 and H100
- [#50226](https://github.com/vllm-project/vllm/pull/50226) (open) Optimize SM103 GDN causal-conv prefills
- [#50294](https://github.com/vllm-project/vllm/pull/50294) (open) Optimize FA4 mm_prefix range lookup
- [#50613](https://github.com/vllm-project/vllm/pull/50613) (open) Per-request scheduling for MLA chunked context
- [#50659](https://github.com/vllm-project/vllm/pull/50659) (open) Fuse mixed-batch KDA boundary operations
- [#50439](https://github.com/vllm-project/vllm/pull/50439) (open) Extend FlashInfer decode support on SM90 and SM100
- [#50721](https://github.com/vllm-project/vllm/pull/50721) (open) Enable routed-experts capture
- [#50279](https://github.com/vllm-project/vllm/pull/50279) (open) Fuse strided GDN RMSNorm gating on SM103
- [#50572](https://github.com/vllm-project/vllm/pull/50572) (open) Integrate FlashInfer BF16 CuTeDSL Low Latency GEMM
- [#50372](https://github.com/vllm-project/vllm/pull/50372) (open) Fuse FlashInfer GDN prefill state I/O
- [#50626](https://github.com/vllm-project/vllm/pull/50626) (open) Move Marlin lock storage to WorkspaceManager
- [#50400](https://github.com/vllm-project/vllm/pull/50400) (open) Fused vision q/k roper kernel for Kimi
- [#50201](https://github.com/vllm-project/vllm/pull/50201) (open) Harden top_k_per_row against NaN and under-filled output
- [#50371](https://github.com/vllm-project/vllm/pull/50371) (open) Enable 12-head MLA persistent decode
- [#50758](https://github.com/vllm-project/vllm/pull/50758) (open) Remove attention layer name from unified_kv_cache_update for torch.compile
- [#50449](https://github.com/vllm-project/vllm/pull/50449) (open) Unify ViT FlashAttention backend selection
- [#50553](https://github.com/vllm-project/vllm/pull/50553) (open) Fuse SiTU activation + FP8 quant in persistent MoE kernel

</details>

<details>
<summary>MoE & quantization (22)</summary>

- [#48949](https://github.com/vllm-project/vllm/pull/48949) Use MXFP4 linear kernel abstraction for emulation backend
- [#47124](https://github.com/vllm-project/vllm/pull/47124) Add W4A16(moe) / MXFP4(linear/moe) Support for XPU
- [#49580](https://github.com/vllm-project/vllm/pull/49580) Integrate CuTeDSL MoE for ReLU2 NVFP4
- [#43229](https://github.com/vllm-project/vllm/pull/43229) FP4 Qutlass Integration
- [#42436](https://github.com/vllm-project/vllm/pull/42436) Add VLLM_TRITON_USE_TD tensor-descriptor path for fused_moe
- [#46720](https://github.com/vllm-project/vllm/pull/46720) B-preshuffle the attention fp8 projections for DSV4
- [#50378](https://github.com/vllm-project/vllm/pull/50378) Pass pointers to FlyDSL MoE kernels
- [#50273](https://github.com/vllm-project/vllm/pull/50273) Honor `--linear-backend` for ModelOpt W4A16
- [#50116](https://github.com/vllm-project/vllm/pull/50116) Clean-up weight prepack for INT8 MoE
- [#48876](https://github.com/vllm-project/vllm/pull/48876) Add Inkling compressed-tensors dynamic FP8 support
- [#50019](https://github.com/vllm-project/vllm/pull/50019) Enable ModelOpt FP8 emulation on SM80
- [#50415](https://github.com/vllm-project/vllm/pull/50415) (open) Add MoNe experts pruning support
- [#50622](https://github.com/vllm-project/vllm/pull/50622) (open) Split AITER CK and Triton MXFP4 W4A16 into separate backends
- [#50501](https://github.com/vllm-project/vllm/pull/50501) (open) Add int4 w4a8 backend for INC linear layers
- [#50396](https://github.com/vllm-project/vllm/pull/50396) (open) Add ARK W4A16(moe) Support
- [#50317](https://github.com/vllm-project/vllm/pull/50317) (open) Add dual RMSNorm quant fusion pattern
- [#50383](https://github.com/vllm-project/vllm/pull/50383) (open) Shard the K3 Latent-MoE up-projection on large batches
- [#50535](https://github.com/vllm-project/vllm/pull/50535) (open) Use AITER tuned GEMM for the MoE router gate
- [#50556](https://github.com/vllm-project/vllm/pull/50556) (open) Add prepare/finalize factory registry for MoE OOT
- [#50401](https://github.com/vllm-project/vllm/pull/50401) (open) Add per-layer online quantization configuration
- [#50205](https://github.com/vllm-project/vllm/pull/50205) (open) TRT-LLM FP8 MoE SM100 compatibility
- [#50617](https://github.com/vllm-project/vllm/pull/50617) (open) Serve modelopt_mixed checkpoints with FP8_PB layers

</details>

<details>
<summary>Model support (28)</summary>

- [#50000](https://github.com/vllm-project/vllm/pull/50000) Add Kimi K3 model support
- [#50093](https://github.com/vllm-project/vllm/pull/50093) Add Kimi K3 support: Python frontend
- [#50032](https://github.com/vllm-project/vllm/pull/50032) Add MSA speculative decode verification for MiniMax-M3
- [#47207](https://github.com/vllm-project/vllm/pull/47207) Migrate Deepseek V3.2 to vllm/models/deepseek_v32/
- [#49934](https://github.com/vllm-project/vllm/pull/49934) Unify multiple-path encoder cuda graph support
- [#48791](https://github.com/vllm-project/vllm/pull/48791) Enable sequence pooling for embedding and classification models
- [#50574](https://github.com/vllm-project/vllm/pull/50574) Enable encoder token embedding
- [#50293](https://github.com/vllm-project/vllm/pull/50293) Enable encoder token classification
- [#50210](https://github.com/vllm-project/vllm/pull/50210) Support Qwen3.5 text-only dense and MoE models
- [#50092](https://github.com/vllm-project/vllm/pull/50092) Add default video_processor for Minimax-M3
- [#50313](https://github.com/vllm-project/vllm/pull/50313) Revert "[Misc][Minimax-M3]add default video_processor"
- [#50661](https://github.com/vllm-project/vllm/pull/50661) Enable BGE M3 pooling embed token_classify
- [#50515](https://github.com/vllm-project/vllm/pull/50515) Restore Mistral tool-parser compatibility after unification
- [#50500](https://github.com/vllm-project/vllm/pull/50500) Support Kimi-K3 quantized models via Compressed-Tensors
- [#50484](https://github.com/vllm-project/vllm/pull/50484) (open) Add DCP support for Kimi-K3
- [#50229](https://github.com/vllm-project/vllm/pull/50229) (open) Migrate Kimi K3 to Parser Engine
- [#50496](https://github.com/vllm-project/vllm/pull/50496) (open) Add Apertus 1.5 model support
- [#50319](https://github.com/vllm-project/vllm/pull/50319) (open) Enable gfx942 serving for Kimi-K3
- [#50658](https://github.com/vllm-project/vllm/pull/50658) (open) Project DSpark aux states before SP all-gather for Kimi K3
- [#50551](https://github.com/vllm-project/vllm/pull/50551) (open) SSM decode checkpoints for prefix caching for Kimi K3
- [#50493](https://github.com/vllm-project/vllm/pull/50493) (open) Support DCP partial prefix cache hit for Kimi-K3
- [#50723](https://github.com/vllm-project/vllm/pull/50723) (open) Support sparse checkpoint updates through native weight loaders
- [#50487](https://github.com/vllm-project/vllm/pull/50487) (open) Tap the pre-norm AttnRes mixture as the Kimi K3 DFlash aux state
- [#50688](https://github.com/vllm-project/vllm/pull/50688) (open) Support jina-embeddings-v5-text-nano
- [#50411](https://github.com/vllm-project/vllm/pull/50411) (open) Do normalize and rescale in device for multimodal models
- [#50524](https://github.com/vllm-project/vllm/pull/50524) (open) Add K-EXAONE-2.0-750B-A37B
- [#50580](https://github.com/vllm-project/vllm/pull/50580) (open) DeepSeek V4 0731 reasoning effort prompts
- [#50354](https://github.com/vllm-project/vllm/pull/50354) (open) Add Mage-VL multimodal model support
- [#50647](https://github.com/vllm-project/vllm/pull/50647) (open) Add EPLB support for Kimi K3

</details>

<details>
<summary>Parallelism & scheduling (32)</summary>

- [#48892](https://github.com/vllm-project/vllm/pull/48892) Add multi-layer MTP speculator for Model Runner V2
- [#48408](https://github.com/vllm-project/vllm/pull/48408) Add per-layer canonical KV page mappings for parallelism-agnostic offload
- [#48981](https://github.com/vllm-project/vllm/pull/48981) Stateful Trainer Send: IPC for RL
- [#49762](https://github.com/vllm-project/vllm/pull/49762) Support NIXL P/D for hybrid MLA+SSM models
- [#46789](https://github.com/vllm-project/vllm/pull/46789) Implement Sequence Parallelism for DSV4
- [#50094](https://github.com/vllm-project/vllm/pull/50094) Move CPUOffloadingSpec onto SharedOffloadRegion
- [#50301](https://github.com/vllm-project/vllm/pull/50301) Enable single-copy MLA layout for CPUOffloadingSpec
- [#50498](https://github.com/vllm-project/vllm/pull/50498) Optionally disable lookup on PD decode
- [#49647](https://github.com/vllm-project/vllm/pull/49647) Enable NVLink all-reduce paths on SM107
- [#49582](https://github.com/vllm-project/vllm/pull/49582) Add has_pending_push_work to EC Connector
- [#50246](https://github.com/vllm-project/vllm/pull/50246) (open) Add DFly speculative decoding and D-Cut support
- [#50465](https://github.com/vllm-project/vllm/pull/50465) (open) Batch-sharded sample for speculative decoding
- [#50422](https://github.com/vllm-project/vllm/pull/50422) (open) Session Aware Eviction Policy for KV offload
- [#50735](https://github.com/vllm-project/vllm/pull/50735) (open) Add --rank-tp-ratio for uneven tensor parallelism on mismatched GPUs
- [#50499](https://github.com/vllm-project/vllm/pull/50499) (open) Support packed MLA KV layouts in pipeline-parallel push prefill
- [#50457](https://github.com/vllm-project/vllm/pull/50457) (open) Run an all-sliding DFlash drafter with prefix caching enabled
- [#50366](https://github.com/vllm-project/vllm/pull/50366) (open) DCP: consume owner-sharded Top-K candidates through symmetric memory
- [#50494](https://github.com/vllm-project/vllm/pull/50494) (open) Support attention-HMA layouts in pipeline-parallel push prefill
- [#50505](https://github.com/vllm-project/vllm/pull/50505) (open) Size custom all-reduce buffers at init so batch-invariant mode can use them
- [#50611](https://github.com/vllm-project/vllm/pull/50611) (open) DCP support for MLA models
- [#50733](https://github.com/vllm-project/vllm/pull/50733) (open) Add --rank-gpu-id / --rank-gpu-memory-mib for explicit TP rank placement
- [#50514](https://github.com/vllm-project/vllm/pull/50514) (open) Spec decode under pipeline parallel
- [#50507](https://github.com/vllm-project/vllm/pull/50507) (open) Support partial-tail prefix reuse with fine-grained prefix matching
- [#50546](https://github.com/vllm-project/vllm/pull/50546) (open) Let MultiConnector compose sub-connector hits
- [#50306](https://github.com/vllm-project/vllm/pull/50306) (open) Gather MM embeddings for all MTP modules
- [#50374](https://github.com/vllm-project/vllm/pull/50374) (open) Add MooncakePromMetrics and wire via build_prom_metrics
- [#50732](https://github.com/vllm-project/vllm/pull/50732) (open) Emit inactive KV blocks for decode affinity
- [#50656](https://github.com/vllm-project/vllm/pull/50656) (open) Optionally TP-shard sequence-parallel MLPs instead of replicating
- [#50667](https://github.com/vllm-project/vllm/pull/50667) (open) Allow replicated MLA layout for multi-group caches
- [#50299](https://github.com/vllm-project/vllm/pull/50299) (open) Add TP-invariant tree kernels across TP sizes
- [#50321](https://github.com/vllm-project/vllm/pull/50321) (open) Support partial secondary-tier load results
- [#50382](https://github.com/vllm-project/vllm/pull/50382) (open) Default query replication for GLM sparse attention

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#50387](https://github.com/vllm-project/vllm/pull/50387) Bump up CPU kernels to latest version
- [#50006](https://github.com/vllm-project/vllm/pull/50006) Add tuned selective_state_update float16 config for AMD Instinct MI325X
- [#50573](https://github.com/vllm-project/vllm/pull/50573) (open) Added SVE128 and SVE256 support to vectorizer backend
- [#50288](https://github.com/vllm-project/vllm/pull/50288) (open) Add NVFP4 KV cache support for consumer Blackwell (RTX 5090)
- [#50534](https://github.com/vllm-project/vllm/pull/50534) (open) Add tuned Mamba SSU configs for Intel Arc Pro B70

</details>

<details>
<summary>API & serving (33)</summary>

- [#47189](https://github.com/vllm-project/vllm/pull/47189) Cohere chat v2 api support
- [#47301](https://github.com/vllm-project/vllm/pull/47301) Add detokenization streaming derender for disaggregated serving
- [#49341](https://github.com/vllm-project/vllm/pull/49341) Send multimodal tensors in auxiliary frames for Rust Frontend
- [#49665](https://github.com/vllm-project/vllm/pull/49665) Standardize request error handling with VLLMError hierarchy
- [#49604](https://github.com/vllm-project/vllm/pull/49604) Add --limit-mm-per-prompt support to Rust Frontend
- [#48543](https://github.com/vllm-project/vllm/pull/48543) Add diarized_json support for MOSS-Transcribe-Diarize
- [#49114](https://github.com/vllm-project/vllm/pull/49114) Add CachePolicyFactory for pluggable/external eviction policies
- [#49686](https://github.com/vllm-project/vllm/pull/49686) Expose mm hash algothrim selection to cli args
- [#48145](https://github.com/vllm-project/vllm/pull/48145) Reuse prefill token ids on the decode chat path for disaggregated serving
- [#50033](https://github.com/vllm-project/vllm/pull/50033) Add KV event source discovery to Rust Frontend gRPC
- [#50403](https://github.com/vllm-project/vllm/pull/50403) Preserve bare Inkling text in Python and Rust parsers
- [#50408](https://github.com/vllm-project/vllm/pull/50408) Warm up the renderer properly
- [#49914](https://github.com/vllm-project/vllm/pull/49914) Lazily initialize chat media connectors
- [#50406](https://github.com/vllm-project/vllm/pull/50406) Improve startup failure and readiness logs for Rust Frontend
- [#49608](https://github.com/vllm-project/vllm/pull/49608) Offload raw-prompt preprocessing to renderer thread pool in AsyncLLM
- [#49498](https://github.com/vllm-project/vllm/pull/49498) Add cache_salt support to Anthropic Messages API
- [#50575](https://github.com/vllm-project/vllm/pull/50575) (open) Upgrade the Rust tool parser bridge to unified parsing
- [#50570](https://github.com/vllm-project/vllm/pull/50570) (open) Add RTSP live-stream captioning via DeepStream backend
- [#50584](https://github.com/vllm-project/vllm/pull/50584) (open) Add DRY (Don't Repeat Yourself) sampling
- [#50550](https://github.com/vllm-project/vllm/pull/50550) (open) Add stream reasoning and tool calls from the derender endpoint
- [#50195](https://github.com/vllm-project/vllm/pull/50195) (open) Add stateless /v1/responses/render endpoint
- [#50198](https://github.com/vllm-project/vllm/pull/50198) (open) Add MiniCPM5 XML tool parser
- [#50390](https://github.com/vllm-project/vllm/pull/50390) (open) Remove duplicate image preprocessing in EPD and enable preprocess on GPU
- [#50368](https://github.com/vllm-project/vllm/pull/50368) (open) Add multimodal image inference to Rust Frontend gRPC
- [#50698](https://github.com/vllm-project/vllm/pull/50698) (open) Add supervisor-side control channel for Elastic EP scaling
- [#50289](https://github.com/vllm-project/vllm/pull/50289) (open) Add standalone Rust renderer
- [#50362](https://github.com/vllm-project/vllm/pull/50362) (open) Add verbose_json support for MOSS-Transcribe-Diarize
- [#50370](https://github.com/vllm-project/vllm/pull/50370) (open) Propagate W3C trace headers to engine-core requests
- [#50283](https://github.com/vllm-project/vllm/pull/50283) (open) Add --enable-nan-fault-tolerance for NaN detection and request abort
- [#50544](https://github.com/vllm-project/vllm/pull/50544) (open) Support strict=false in response_format json_schema
- [#50448](https://github.com/vllm-project/vllm/pull/50448) (open) Deduplicate request preprocessing for `/tokenize`
- [#50540](https://github.com/vllm-project/vllm/pull/50540) (open) Align tool rendering for Kimi K3
- [#50402](https://github.com/vllm-project/vllm/pull/50402) (open) Add logs to local the garbled text issue

</details>

<details>
<summary>Refactors (4)</summary>

- [#44570](https://github.com/vllm-project/vllm/pull/44570) Combine CompressedTensorsWNA16MarlinMoEMethod with CompressedTensorsWNA16MoEMethod
- [#44941](https://github.com/vllm-project/vllm/pull/44941) Rename FusedMoE to FusedMoEFactory
- [#50285](https://github.com/vllm-project/vllm/pull/50285) (open) Remove multiple dead codes
- [#50582](https://github.com/vllm-project/vllm/pull/50582) (open) AITER MoE environment variable cleanup

</details>

<details>
<summary>Bugfixes (85)</summary>

- [#45227](https://github.com/vllm-project/vllm/pull/45227) AITER MLA: size MTP verification decode metadata for real qlen/dtype
- [#48245](https://github.com/vllm-project/vllm/pull/48245) Fix `num_output_placeholders` preemption underflow
- [#48438](https://github.com/vllm-project/vllm/pull/48438) Preserve Marlin runtime tensor storage across weight reload
- [#49343](https://github.com/vllm-project/vllm/pull/49343) Fix eagle draft max position embeddings
- [#49570](https://github.com/vllm-project/vllm/pull/49570) Fix mypy errors in some tests/ directories
- [#50153](https://github.com/vllm-project/vllm/pull/50153) Fix NIXL mamba state pairing for multi-slot block tables
- [#41357](https://github.com/vllm-project/vllm/pull/41357) Prevent stale multiproc RPC deadlines from becoming unbounded waits
- [#50304](https://github.com/vllm-project/vllm/pull/50304) Fix AMD nightly distributed regressions
- [#50297](https://github.com/vllm-project/vllm/pull/50297) Fix P/D preemption race condition
- [#50302](https://github.com/vllm-project/vllm/pull/50302) Universally align block table width to 128 tokens
- [#50420](https://github.com/vllm-project/vllm/pull/50420) Use default tool call IDs for Kimi K3 for conversation-level uniqueness
- [#49840](https://github.com/vllm-project/vllm/pull/49840) Shut down private Tensorizer engines
- [#50352](https://github.com/vllm-project/vllm/pull/50352) Reject encoder-backbone jina-embeddings-v5 checkpoints with a clear error
- [#49757](https://github.com/vllm-project/vllm/pull/49757) Stop dummy runs from writing mamba state through stale block-table rows
- [#50137](https://github.com/vllm-project/vllm/pull/50137) Don't transpose fused MoE quantization scales in `RoutedExperts.load_weights`
- [#50326](https://github.com/vllm-project/vllm/pull/50326) Rebase KV lease deadlines onto worker clock
- [#41602](https://github.com/vllm-project/vllm/pull/41602) Fix /wake_up crash on hybrid models (Mamba/DeltaNet)
- [#50349](https://github.com/vllm-project/vllm/pull/50349) Fix FP8 block scale layout for MLA compatibility
- [#49975](https://github.com/vllm-project/vllm/pull/49975) Include media IO config in MM cache hash
- [#50437](https://github.com/vllm-project/vllm/pull/50437) Remove redundant kv cache write for CPU
- plus 65 more minor bugfixes

</details>

<details>
<summary>Tests, CI & Docs (77)</summary>

- [#50330](https://github.com/vllm-project/vllm/pull/50330) Organize speculative decoding E2E tests by coverage
- [#50109](https://github.com/vllm-project/vllm/pull/50109) `--jit-monitor-mode error` e2e tests for kernel warmup infra
- [#50132](https://github.com/vllm-project/vllm/pull/50132) Add comment-based Buildkite triggers
- [#50318](https://github.com/vllm-project/vllm/pull/50318) Retry failed steps on new PR commits
- [#50414](https://github.com/vllm-project/vllm/pull/50414) Improve comment-triggered authorization and retries
- [#50600](https://github.com/vllm-project/vllm/pull/50600) Add Understanding the Latency Metrics docs
- [#50397](https://github.com/vllm-project/vllm/pull/50397) Document Ray cluster trust model and env var propagation
- [#49066](https://github.com/vllm-project/vllm/pull/49066) Add documentation for pynvvideocodec video decoding backend
- [#50141](https://github.com/vllm-project/vllm/pull/50141) Clarify mono audio requirement
- [#50308](https://github.com/vllm-project/vllm/pull/50308) Remove tcmalloc warning from CPU docs
- plus 67 more minor test, CI, and documentation updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 8e9d006ab09153f624a8d02a7043d320642c5c0d43288c6c2341a2c0668c273f -->
