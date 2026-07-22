# vllm: PR digest (2026-07-08 to 2026-07-12)

_140 merged, 298 newly opened - source vllm-project/vllm, generated 2026-07-12T22:06:32Z_

## TL;DR
- **DeepSeek** dominated model-specific work, with merged support for DeepSeek-V4 DSpark speculative decoding on AMD ROCm, and newly opened PRs for online C128 compression and FlashInfer CUTLASS MXFP4 MoE wiring. Qwen and Mistral also saw targeted optimizations.
- **Performance & Architecture** saw major structural shifts, including a merged KV-cache layout refactor packing K/V into the content dimension, and newly opened work on a PCIe-safe serving stack for SM120 with async-TP and FlashInfer full cudagraphs.
- **Speculative Decoding & Parallelism** advanced significantly, with merged runtime draft weight updates and newly opened support for Decode Context Parallelism (DCP) with Eagle and FlashInfer fused A2A backends.
- **Multimodal & Frontend** capabilities expanded, notably merging video support into the Rust frontend and adding an endpoint plugins framework.
- **Overall Direction**: The engine is heavily optimizing for next-gen architectures (DeepSeek-V4, SM120, AMD MI350X) with aggressive KV cache compression (KVCrush), hybrid attention support, and deep integration of FlashInfer and Triton backends for MoE and speculative decoding.

## Most important PRs
- **[#44455](https://github.com/vllm-project/vllm/pull/44455)** Packs K/V into the content dimension across attention backends (FlashInfer, Triton). This major KV-cache layout refactor standardizes memory access patterns for better performance across AMD and NVIDIA hardware.
- **[#46384](https://github.com/vllm-project/vllm/pull/46384)** Enables partial prefix cache hits for hybrid models. This allows the distributed KV-cache to reuse prefixes even when hybrid architectures (like Mamba + Attention) diverge in their caching needs.
- **[#47959](https://github.com/vllm-project/vllm/pull/47959)** Integrates multimodal video support directly into the Rust frontend. This significantly expands the capabilities of the high-performance serving path.
- **[#47979](https://github.com/vllm-project/vllm/pull/47979)** (Opened) Introduces an SM120 PCIe serving stack featuring sequence parallelism, async tensor parallelism, and FlashInfer speculative decoding with full CUDA graphs for PCIe-safe multi-GPU communication.
- **[#47967](https://github.com/vllm-project/vllm/pull/47967)** (Opened) Proposes KVCrush, a new KV cache compression mechanism for vLLM. This aims to drastically reduce memory footprint for long-context generation.

## More changes by area

<details>
<summary>Performance (15)</summary>

- [#45182](https://github.com/vllm-project/vllm/pull/45182) Integrate TRTLLM BF16 MoE Modular Kernel
- [#46117](https://github.com/vllm-project/vllm/pull/46117) [ROCm] MXFP8 dense-linear + grouped-MoE GEMM optimizations for MiniMax-M3
- [#47006](https://github.com/vllm-project/vllm/pull/47006) [Qwen] Replace MOE all-reduce with reduce-scatter
- [#47631](https://github.com/vllm-project/vllm/pull/47631) Minimax M3 - Support cross-layer allreduce-norm fusion
- [#46998](https://github.com/vllm-project/vllm/pull/46998) fuse more rmsnorm and all-reduce in qwen3.5
- [#48018](https://github.com/vllm-project/vllm/pull/48018) (Opened) ReplaySSM: cache SSM inputs for faster Mamba2 standard decode
- [#48382](https://github.com/vllm-project/vllm/pull/48382) (Opened) Reload layout-preserving weights directly
- [#48188](https://github.com/vllm-project/vllm/pull/48188) (Opened) Speed up Mamba chunk metadata computation by ~6x
- [#48156](https://github.com/vllm-project/vllm/pull/48156) (Opened) Warm up dense (paged) FA4 attention kernels
- [#48363](https://github.com/vllm-project/vllm/pull/48363) (Opened) Warm up hybrid Mamba2 Triton kernels reported by the JIT monitor
- [#48247](https://github.com/vllm-project/vllm/pull/48247) (Opened) [ROCm] Add AITER custom AG/RS
- [#48223](https://github.com/vllm-project/vllm/pull/48223) (Opened) [ROCm] Dual-stream decode with hipgraphs
- [#48110](https://github.com/vllm-project/vllm/pull/48110) (Opened) Vectorize _copy_mamba_state_block to uint64 for temporal
- [#48143](https://github.com/vllm-project/vllm/pull/48143) (Opened) Optimize `clamp` to `clamp_`
- [#48300](https://github.com/vllm-project/vllm/pull/48300) (Opened) Revert "[Perf] fuse more rmsnorm and all-reduce in qwen3.5"

</details>

<details>
<summary>Kernels & attention (25)</summary>

- [#40996](https://github.com/vllm-project/vllm/pull/40996) DCP supports hybrid attention
- [#47502](https://github.com/vllm-project/vllm/pull/47502) [Minimax-M3] Using tok_sparse_select from MSA instead of triton kernels
- [#48335](https://github.com/vllm-project/vllm/pull/48335) FP32 router GEMV optimization
- [#47404](https://github.com/vllm-project/vllm/pull/47404) [ROCm] Synchronize sparse MLA metadata before graph replay
- [#47914](https://github.com/vllm-project/vllm/pull/47914) Support hybrid (SWA + full attention) DFlash drafters
- [#47785](https://github.com/vllm-project/vllm/pull/47785) handle topk_ids padding in align sum kernel
- [#45149](https://github.com/vllm-project/vllm/pull/45149) [ROCM][DSV32] Enable UNIFORM_BATCH CG mode in rocm_aiter_mla_sparse
- [#48196](https://github.com/vllm-project/vllm/pull/48196) (Opened) DCP sparse MLA output-merge optimizations
- [#48119](https://github.com/vllm-project/vllm/pull/48119) (Opened) Support online C128 compression for DeepSeek V4
- [#48407](https://github.com/vllm-project/vllm/pull/48407) (Opened) Skip sparse indexer for short sequences
- [#48162](https://github.com/vllm-project/vllm/pull/48162) (Opened) Batch-level prefill/decode attention backend routing
- [#47973](https://github.com/vllm-project/vllm/pull/47973) (Opened) BF16x3 router GEMM
- [#47942](https://github.com/vllm-project/vllm/pull/47942) (Opened) Add sparse MLA topology index policy and benchmark
- [#48012](https://github.com/vllm-project/vllm/pull/48012) (Opened) Allow selecting a different attention backend per KV-cache group
- [#48257](https://github.com/vllm-project/vllm/pull/48257) (Opened) [ROCm] Support cached K/V (key/value=None) in Triton prefix-prefill
- [#47976](https://github.com/vllm-project/vllm/pull/47976) (Opened) Add unit test for fused_recurrent_gated_delta_rule kernel
- [#48287](https://github.com/vllm-project/vllm/pull/48287) (Opened) add pad-aware swiglu limit kernel
- [#48385](https://github.com/vllm-project/vllm/pull/48385) (Opened) add pad-aware reduce path
- [#48235](https://github.com/vllm-project/vllm/pull/48235) (Opened) Optimize 4-bit GQA decode for group size 4
- [#48216](https://github.com/vllm-project/vllm/pull/48216) (Opened) group-aware recovery for KV load failures on hybrid models
- [#48254](https://github.com/vllm-project/vllm/pull/48254) (Opened) [CPU] Add triton-free staged writes for MRV2
- [#48166](https://github.com/vllm-project/vllm/pull/48166) (Opened) Optimize hybrid postprocess with single loop
- [#48190](https://github.com/vllm-project/vllm/pull/48190) (Opened) Make the DeepGEMM JIT cache key portable across install layouts
- [#48384](https://github.com/vllm-project/vllm/pull/48384) (Opened) remove kernel_block_sizes check in get_preferred_block_size
- [#48120](https://github.com/vllm-project/vllm/pull/48120) (Opened) Stage the postprocess inputs with a single loop over the request list

</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#47851](https://github.com/vllm-project/vllm/pull/47851) Bound peak memory when repacking FP4 MoE weights for Marlin
- [#48268](https://github.com/vllm-project/vllm/pull/48268) Add VLLM_FLASHINFER_AUTOTUNE_SKIP_OPS and skip CuTeDSL fp4_gemm autotuning by default
- [#46661](https://github.com/vllm-project/vllm/pull/46661) Allow FlashInfer A2A backends for TRTLLM FP8 MoE Modular
- [#47939](https://github.com/vllm-project/vllm/pull/47939) (Opened) [GLM 5.2] Integrate NVFP4 MegaMoE
- [#48309](https://github.com/vllm-project/vllm/pull/48309) (Opened) Add fused MoE Triton configs for NVIDIA GeForce RTX 4090D
- [#47948](https://github.com/vllm-project/vllm/pull/47948) (Opened) Add flashinfer.moe_ep (NCCL-EP) all2all backends
- [#48427](https://github.com/vllm-project/vllm/pull/48427) (Opened) [ROCm] MiniMax-M3: Enable fp8_per_channel for MXFP8 checkpoints
- [#48044](https://github.com/vllm-project/vllm/pull/48044) (Opened) Fused Shared Expert Support for AMD Quark DeepSeek-V4 Model Checkpoints
- [#47972](https://github.com/vllm-project/vllm/pull/47972) (Opened) Support DeepSeek-V4 AMD Quark NVFP4 with emulation kernel
- [#48015](https://github.com/vllm-project/vllm/pull/48015) (Opened) [ROCm] Avoid HIP init at config time via lazy aiter import in Quark OCP-MX

</details>

<details>
<summary>Model support (16)</summary>

- [#47729](https://github.com/vllm-project/vllm/pull/47729) Support MOSS-Transcribe-Diarize
- [#47872](https://github.com/vllm-project/vllm/pull/47872) [HunyuanVL] Use native transformers processor and adapt to transformers 5.13
- [#47857](https://github.com/vllm-project/vllm/pull/47857) Add LongCat-Flash-Lite (n-gram embedding)
- [#48153](https://github.com/vllm-project/vllm/pull/48153) Migrate MistralLarge3ForCausalLM to AutoWeightsLoader
- [#48211](https://github.com/vllm-project/vllm/pull/48211) Cosmos3: enable registry tests and register Cosmos3-Super
- [#48410](https://github.com/vllm-project/vllm/pull/48410) (Opened) Apertus 1.5 multimodality
- [#48279](https://github.com/vllm-project/vllm/pull/48279) (Opened) Add Nemotron Ministral masked block-diffusion LM
- [#48291](https://github.com/vllm-project/vllm/pull/48291) (Opened) Add Cosmos3 Edge Reasoner model
- [#47957](https://github.com/vllm-project/vllm/pull/47957) (Opened) Add Shuka-1 model support (sarvamai/shuka-1)
- [#48270](https://github.com/vllm-project/vllm/pull/48270) (Opened) Add GraniteSWA and GraniteMoeSWA
- [#48302](https://github.com/vllm-project/vllm/pull/48302) (Opened) Add LongCat-2.0 (LongCat Sparse Attention + MTP)
- [#48250](https://github.com/vllm-project/vllm/pull/48250) (Opened) Support MLA properly in the Transformers modeling backend
- [#48215](https://github.com/vllm-project/vllm/pull/48215) (Opened) Add tower/connector LoRA support for Ultravox
- [#48355](https://github.com/vllm-project/vllm/pull/48355) (Opened) extended EPLB support for Mistral Large 3 and additional MoE backends
- [#48350](https://github.com/vllm-project/vllm/pull/48350) (Opened) Optimize Qwen3.5 on H20
- [#47991](https://github.com/vllm-project/vllm/pull/47991) (Opened) Add RobertaForTokenClassification / XLMRobertaForTokenClassification

</details>

<details>
<summary>Parallelism & scheduling (38)</summary>

- [#45880](https://github.com/vllm-project/vllm/pull/45880) [NIXL] Support pipeline-parallel prefill in push mode
- [#47419](https://github.com/vllm-project/vllm/pull/47419) [ROCm] Enable DeepSeek-V4 DSpark speculative decoding on AMD
- [#46725](https://github.com/vllm-project/vllm/pull/46725) Runtime Draft Weight Update for Speculative Decoding
- [#47923](https://github.com/vllm-project/vllm/pull/47923) Emit tier-owned BlockStored events from FS/OBJ secondary tiers
- [#47317](https://github.com/vllm-project/vllm/pull/47317) [Mooncake] Apply SWA lookup mask before hashing/key build
- [#46865](https://github.com/vllm-project/vllm/pull/46865) MultiConnector: give every sub-connector the request's real blocks in `update_state_after_alloc`
- [#47987](https://github.com/vllm-project/vllm/pull/47987) Make tiering offload region DP-replica aware
- [#47849](https://github.com/vllm-project/vllm/pull/47849) Add free block iterator for CPU offload scheduling
- [#47941](https://github.com/vllm-project/vllm/pull/47941) (Opened) P2P NIXL + CPU EC Connector
- [#48263](https://github.com/vllm-project/vllm/pull/48263) (Opened) [NIXL] Recover all dedup'd HMA pool members under PP
- [#48021](https://github.com/vllm-project/vllm/pull/48021) (Opened) Generic P2P secondary tier: peer lookup and serving via ParentManager
- [#47984](https://github.com/vllm-project/vllm/pull/47984) (Opened) [ROCm] Support speculative decode with AITER sparse PA for MiniMax-M3
- [#48280](https://github.com/vllm-project/vllm/pull/48280) (Opened) Heterogeneous rank-to-GPU mapping + Qwen3.5/3.6 GGUF enablement
- [#47981](https://github.com/vllm-project/vllm/pull/47981) (Opened) Support attention-HMA PP prefill in NixlPushConnector
- [#48409](https://github.com/vllm-project/vllm/pull/48409) (Opened) Add runtime LoRA weight updates
- [#48042](https://github.com/vllm-project/vllm/pull/48042) (Opened) Stateful Trainer Send: New Abstractions [1/N]
- [#48150](https://github.com/vllm-project/vllm/pull/48150) (Opened) Move KV cache layout parsing into the offloading connector
- [#48393](https://github.com/vllm-project/vllm/pull/48393) (Opened) Warm _mtp_shared_head_rmsnorm_kernel at startup
- [#48392](https://github.com/vllm-project/vllm/pull/48392) (Opened) DFlash/DSpark draft support under decode context parallelism
- [#48288](https://github.com/vllm-project/vllm/pull/48288) (Opened) Internal session id for offloading
- [#48434](https://github.com/vllm-project/vllm/pull/48434) (Opened) Coalesce contiguous descriptor runs before batch submission
- [#48244](https://github.com/vllm-project/vllm/pull/48244) (Opened) Skip redundant draft token alloc + sampling
- [#48246](https://github.com/vllm-project/vllm/pull/48246) (Opened) PrefillDelayer for better DPA scheduling
- [#48248](https://github.com/vllm-project/vllm/pull/48248) (Opened) Add FlashInfer fused A2A backend for decode context parallelism
- [#48180](https://github.com/vllm-project/vllm/pull/48180) (Opened) Add DCP + Eagle support for Tokenspeed MLA backends
- [#48249](https://github.com/vllm-project/vllm/pull/48249) (Opened) [ROCm] Enable AITER QuickReduce + RMSNorm fusion
- [#48414](https://github.com/vllm-project/vllm/pull/48414) (Opened) Fragment-major canonical CPU layout for KV offload
- [#48204](https://github.com/vllm-project/vllm/pull/48204) (Opened) Reference implementation: per-request effective proposal lengths
- [#48281](https://github.com/vllm-project/vllm/pull/48281) (Opened) Add P2P reachability metadata to FS/OBJ KV events
- [#48389](https://github.com/vllm-project/vllm/pull/48389) (Opened) Add device-neutral KVConnector host-contract mixins
- [#48069](https://github.com/vllm-project/vllm/pull/48069) (Opened) [Mooncake] Add tenant ID support to MooncakeStoreConnector
- [#48123](https://github.com/vllm-project/vllm/pull/48123) (Opened) Add per-request lookup_scope to skip secondary tier lookups
- [#48230](https://github.com/vllm-project/vllm/pull/48230) (Opened) [Mooncake] Skip lookup for locally reused prefix
- [#48408](https://github.com/vllm-project/vllm/pull/48408) (Opened) Add per-layer KV head region schema for TP-agnostic offload
- [#48399](https://github.com/vllm-project/vllm/pull/48399) (Opened) Simplify KVBlockZeroer index tensor handling
- [#48009](https://github.com/vllm-project/vllm/pull/48009) (Opened) Unify `_logical_to_remote_kernel_block_ids`
- [#48243](https://github.com/vllm-project/vllm/pull/48243) (Opened) Add operator opt-out for the expandable_segments KV-connector rejection
- [#48209](https://github.com/vllm-project/vllm/pull/48209) (Opened) Vectorize prep xfer list creation

</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#47945](https://github.com/vllm-project/vllm/pull/47945) [ROCm] Add tuned selective_state_update float16 config for AMD Instinct MI300X
- [#47947](https://github.com/vllm-project/vllm/pull/47947) [ROCm] Add tuned selective_state_update float32 config for AMD Instinct MI300X
- [#47943](https://github.com/vllm-project/vllm/pull/47943) Add tuned selective_state_update float32 config for AMD Instinct MI355
- [#48213](https://github.com/vllm-project/vllm/pull/48213) (Opened) [CPU] Add CPU-tuned autotune configs for Mamba2/SSD Triton kernels
- [#48212](https://github.com/vllm-project/vllm/pull/48212) (Opened) [CPU] Add CPU-tuned autotune configs for FLA (GDN) Triton kernels
- [#48159](https://github.com/vllm-project/vllm/pull/48159) (Opened) [ROCm] Add tuned selective_state_update config for AMD MI350
- [#48373](https://github.com/vllm-project/vllm/pull/48373) (Opened) [ROCm] Retune MI355 selective_state_update float32 config on the unified effective_batch grid

</details>

<details>
<summary>API & serving (38)</summary>

- [#44301](https://github.com/vllm-project/vllm/pull/44301) Support include_reasoning param for non-Harmony models
- [#42433](https://github.com/vllm-project/vllm/pull/42433) Add EC Transfer Params
- [#46718](https://github.com/vllm-project/vllm/pull/46718) Add runtime monitor for post-warmup TileLang compilation
- [#42424](https://github.com/vllm-project/vllm/pull/42424) Deepstream video backend
- [#47173](https://github.com/vllm-project/vllm/pull/47173) Add /abort_requests to the RLHF dev API router
- [#47608](https://github.com/vllm-project/vllm/pull/47608) Add human-readable integer support for more cli-args
- [#46793](https://github.com/vllm-project/vllm/pull/46793) Support bad_words in the /v1/completions endpoint
- [#47883](https://github.com/vllm-project/vllm/pull/47883) [Rust Frontend] Add roundtrip fixtures for more chat parsers
- [#47454](https://github.com/vllm-project/vllm/pull/47454) Add endpoint plugins framework
- [#45261](https://github.com/vllm-project/vllm/pull/45261) Report prefix-cache-reused blocks in full report mode
- [#48107](https://github.com/vllm-project/vllm/pull/48107) (Opened) [Rust] Port in vllm-bench
- [#48088](https://github.com/vllm-project/vllm/pull/48088) (Opened) Paged shared memory storage for multimodal
- [#48083](https://github.com/vllm-project/vllm/pull/48083) (Opened) Add Confident Decoding (phase 1: Llama + core utilities)
- [#48157](https://github.com/vllm-project/vllm/pull/48157) (Opened) Compose auto tool-call grammar with response_format schema
- [#48352](https://github.com/vllm-project/vllm/pull/48352) (Opened) Version prefix-cache keys for local runtime LoRA reloads
- [#48369](https://github.com/vllm-project/vllm/pull/48369) (Opened) Add offline prefix-cache workload analyzer CLI
- [#48136](https://github.com/vllm-project/vllm/pull/48136) (Opened) Add p-less sampling: a hyperparameter-free truncation method
- [#48121](https://github.com/vllm-project/vllm/pull/48121) (Opened) Expose canonical KV cache group metadata
- [#48142](https://github.com/vllm-project/vllm/pull/48142) (Opened) Add Min-k sampling: temperature-invariant logit-space truncation
- [#48048](https://github.com/vllm-project/vllm/pull/48048) (Opened) session id plumbing into requests
- [#48033](https://github.com/vllm-project/vllm/pull/48033) (Opened) extend the existing service protocol
- [#48240](https://github.com/vllm-project/vllm/pull/48240) (Opened) [Rust Frontend] Add weight transfer lifecycle APIs
- [#48070](https://github.com/vllm-project/vllm/pull/48070) (Opened) first-class session_id for conversation-aware routing
- [#48130](https://github.com/vllm-project/vllm/pull/48130) (Opened) Bound realtime STT audio_queue and per-session audio bytes
- [#48013](https://github.com/vllm-project/vllm/pull/48013) (Opened) [Rust Frontend] add mistral reasoning parser
- [#48138](https://github.com/vllm-project/vllm/pull/48138) (Opened) [Rust Frontend] Add HTTP access log with disable and endpoint-exclusion flags
- [#48390](https://github.com/vllm-project/vllm/pull/48390) (Opened) Support fp32 lm_head for generation models via head_dtype
- [#48145](https://github.com/vllm-project/vllm/pull/48145) (Opened) Reuse prefill token ids on the decode chat path for disaggregated serving
- [#48349](https://github.com/vllm-project/vllm/pull/48349) (Opened) [Rust Frontend] Add Granite4 and Hermes4 tool roundtrips
- [#48218](https://github.com/vllm-project/vllm/pull/48218) (Opened) Encoder cache extension hooks
- [#47985](https://github.com/vllm-project/vllm/pull/47985) (Opened) Add encoder cache profiling implementation
- [#47964](https://github.com/vllm-project/vllm/pull/47964) (Opened) Add streaming/non-streaming parity tests for truncated tool calls
- [#48034](https://github.com/vllm-project/vllm/pull/48034) (Opened) [Rust Frontend] Tolerate whitespace before the outer brace in JSON tool-call parsers
- [#48187](https://github.com/vllm-project/vllm/pull/48187) (Opened) Cache xgrammar JSON schema validation
- [#48030](https://github.com/vllm-project/vllm/pull/48030) (Opened) Log fully resolved pooling config at startup
- [#47965](https://github.com/vllm-project/vllm/pull/47965) (Opened) [Rust Frontend] Wait for mock engine endpoints before ZMQ connect
- [#48292](https://github.com/vllm-project/vllm/pull/48292) (Opened) Log result wait time in iteration details
- [#48133](https://github.com/vllm-project/vllm/pull/48133) (Opened) Tag torch.compile log lines with the component being compiled

</details>

<details>
<summary>Tests, CI & build (26)</summary>

- [#46017](https://github.com/vllm-project/vllm/pull/46017) Improvement of Docker image build for IBM Power using prebuilt wheels
- [#48186](https://github.com/vllm-project/vllm/pull/48186) Right-size test-area timeouts from nightly durations
- [#46893](https://github.com/vllm-project/vllm/pull/46893) GSM8K eval integration test for KV offloading
- [#48101](https://github.com/vllm-project/vllm/pull/48101) Annotate built Docker image tags on the Buildkite build page
- [#47180](https://github.com/vllm-project/vllm/pull/47180) Add TORCH_NIGHTLY=1 build mode
- [#48222](https://github.com/vllm-project/vllm/pull/48222) [Rust Frontend] Pin cargo tool versions
- [#48126](https://github.com/vllm-project/vllm/pull/48126) Add XPU nightly and release image publishing to DockerHub
- [#47867](https://github.com/vllm-project/vllm/pull/47867) Bump Transformers version to 5.13.1
- [#48079](https://github.com/vllm-project/vllm/pull/48079) [XPU] remove is_xxx from moe class and bump up kernels
- [#47880](https://github.com/vllm-project/vllm/pull/47880) Add Intel XPU Docker release pipeline
- [#48072](https://github.com/vllm-project/vllm/pull/48072) [CPU] Add Qwen2-VL multimodal tests for CPU backend
- [#48328](https://github.com/vllm-project/vllm/pull/48328) Point CI at Transformers release rather than release branch
- [#48041](https://github.com/vllm-project/vllm/pull/48041) Build arm64 PR and postmerge image builds for Blackwell SM10x and SM110
- [#48169](https://github.com/vllm-project/vllm/pull/48169) [ROCm] Move remaining engine/samplers AMD steps to mi325_1
- [#44472](https://github.com/vllm-project/vllm/pull/44472) [XPU] Enable v1/sample tests on XPU CI
- [#48056](https://github.com/vllm-project/vllm/pull/48056) Pin PyNvVideoCodec to tested 2.0.4 wheel
- [#48161](https://github.com/vllm-project/vllm/pull/48161) Increase extract hidden states TP2 timeout
- [#48091](https://github.com/vllm-project/vllm/pull/48091) (Opened) add yaml for xpu
- [#48387](https://github.com/vllm-project/vllm/pull/48387) (Opened) [AMD] Configure MI300 tests for native execution without DinD
- [#48323](https://github.com/vllm-project/vllm/pull/48323) (Opened) Add MultiConnector (Nixl+Offloading) PD + spec decode tests
- [#48345](https://github.com/vllm-project/vllm/pull/48345) (Opened) Updating
- [#48164](https://github.com/vllm-project/vllm/pull/48164) (Opened) Add PyTorch stable ABI audit check
- [#48289](https://github.com/vllm-project/vllm/pull/48289) (Opened) Build macOS arm64 CPU wheel natively on the macmini queue
- [#48253](https://github.com/vllm-project/vllm/pull/48253) (Opened) Add chat eval mode to GSM8K harness + gpt-oss-20b config
- [#48155](https://github.com/vllm-project/vllm/pull/48155) (Opened) Update PyTorch to 2.13.0, torchvision to 0.28.0, triton to 3.7.1
- plus 5 more minor CI updates ([#48146](https://github.com/vllm-project/vllm/pull/48146), [#48394](https://github.com/vllm-project/vllm/pull/48394), [#48219](https://github.com/vllm-project/vllm/pull/48219), [#47781](https://github.com/vllm-project/vllm/pull/47781), [#48170](https://github.com/vllm-project/vllm/pull/48170))

</details>

<details>
<summary>Docs (4)</summary>

- [#48096](https://github.com/vllm-project/vllm/pull/48096) Remove PersimmonForCausalLM and FuyuForCausalLM model architectures
- [#48100](https://github.com/vllm-project/vllm/pull/48100) Migrate Olmo and Olmo2 to the Transformers modeling backend
- [#47989](https://github.com/vllm-project/vllm/pull/47989) Remove TeleChatForCausalLM
- [#48359](https://github.com/vllm-project/vllm/pull/48359) (Opened) Add Nika to serving integrations

</details>

<details>
<summary>Bugfixes (96)</summary>

- [#47728](https://github.com/vllm-project/vllm/pull/47728) Free out-of-window blocks on the processed-token basis under async scheduling
- [#45984](https://github.com/vllm-project/vllm/pull/45984) Fix thinking_token_budget not enforced after natural </think> re-entry
- [#42478](https://github.com/vllm-project/vllm/pull/42478) Fix Qwen3-ASR transcription streaming postprocessing
- [#44303](https://github.com/vllm-project/vllm/pull/44303) Fix http_requests_total metric recording some 4xx errors as 5xx
- [#48046](https://github.com/vllm-project/vllm/pull/48046) Use int8 workspace for FlashInfer MLA decode
- [#47158](https://github.com/vllm-project/vllm/pull/47158) [ROCm] fixed aiter master flag and expert parallelism compatibility on minimax-m3-mxfp8
- [#48085](https://github.com/vllm-project/vllm/pull/48085) Fix race condition in KVBlockZeroer
- [#43117](https://github.com/vllm-project/vllm/pull/43117) route MiMo-V2-Omni media fetch through MediaConnector
- [#47381](https://github.com/vllm-project/vllm/pull/47381) Order uniform decodes first so spec decodes aren't misclassified as prefills
- [#47772](https://github.com/vllm-project/vllm/pull/47772) Align CrossEncoder token type ids after truncation
- [#41811](https://github.com/vllm-project/vllm/pull/41811) correct load_weights track logic and enable weight integrity
- [#47493](https://github.com/vllm-project/vllm/pull/47493) DSV4 TP16 garbage output
- [#46276](https://github.com/vllm-project/vllm/pull/46276) weights processing peak memory reduction for nvfp4 MoE layers
- [#47892](https://github.com/vllm-project/vllm/pull/47892) Fix NVML capability lookup for visible devices
- [#48333](https://github.com/vllm-project/vllm/pull/48333) stop resolve_items leaking in-flight media fetch tasks on partial failure
- [#48112](https://github.com/vllm-project/vllm/pull/48112) bge-m3-sparse-plugin mismatch requests
- [#48010](https://github.com/vllm-project/vllm/pull/48010) Fix embed scaling + CUDA graphs in Transformers modelling backend
- [#48330](https://github.com/vllm-project/vllm/pull/48330) Guard mixed-dtype allreduce RMSNorm quant fusions
- [#47912](https://github.com/vllm-project/vllm/pull/47912) [ROCm] Fix pooling startup workspace lock
- [#47690](https://github.com/vllm-project/vllm/pull/47690) Support ark_linear base layer in _get_lora_device
- [#46694](https://github.com/vllm-project/vllm/pull/46694) Fix PD async KV load lookahead handling for MTP spec decode
- [#47766](https://github.com/vllm-project/vllm/pull/47766) [ROCm] Key sparse-MLA persistent metadata on per-request context lengths
- [#47033](https://github.com/vllm-project/vllm/pull/47033) Re-enable benchmarking of librispeech dataset
- [#47888](https://github.com/vllm-project/vllm/pull/47888) Avoid blocking model launching when no system ffmpeg available for TorchCodec
- [#47296](https://github.com/vllm-project/vllm/pull/47296) Guard CUDA-only rms_norm_per_block_quant in FUSED_OPS for non-CUDA builds
- [#47366](https://github.com/vllm-project/vllm/pull/47366) [AMD] Fix ROCm OOM in eagle_correctness_heavy by reserving CUDA graph memory
- [#47944](https://github.com/vllm-project/vllm/pull/47944) [XPU] Fix torch.compile DEVICE_LOST by avoiding view-mutation in LoRA shrink
- [#42642](https://github.com/vllm-project/vllm/pull/42642) Fix FlashAttention MLA prefill V unpadding
- [#47874](https://github.com/vllm-project/vllm/pull/47874) [ROCm] Fix double-transpose of fused w3 expert weights
- [#47028](https://github.com/vllm-project/vllm/pull/47028) Avoid leaking Pydantic repr in tool_choice error message
- [#48008](https://github.com/vllm-project/vllm/pull/48008) Fix the docs build
- [#45313](https://github.com/vllm-project/vllm/pull/45313) Register VLLM_BUILD_* and VLLM_IMAGE_TAG provenance env vars
- [#48113](https://github.com/vllm-project/vllm/pull/48113) Fix DFlash draft/target layer-count mismatch
- [#47848](https://github.com/vllm-project/vllm/pull/47848) [CPU] Fix flaky ShortConv prefill test on ARM (uninitialized weights)
- [#48073](https://github.com/vllm-project/vllm/pull/48073) [CPU] Fix Qwen-Next SSM type for AMX GDN
- [#47980](https://github.com/vllm-project/vllm/pull/47980) BugFix Eval Small Models Distributed test for DiffusionGemma
- [#47894](https://github.com/vllm-project/vllm/pull/47894) [ROCm] Fix empty-tensor .max() crash in AITER FA
- [#48135](https://github.com/vllm-project/vllm/pull/48135) Preserve tensor causal metadata for grouped attention
- [#48232](https://github.com/vllm-project/vllm/pull/48232) [XPU] Fix InternS1ProForConditionalGeneration AssertionError
- [#47911](https://github.com/vllm-project/vllm/pull/47911) hash speculative draft model config
- [#47797](https://github.com/vllm-project/vllm/pull/47797) Allocate HY V3 expert_bias in float32 to prevent silent downcasting
- [#47801](https://github.com/vllm-project/vllm/pull/47801) Cast LSE to fp32 in a2a combine to fix bf16 bitcast crash
- [#47144](https://github.com/vllm-project/vllm/pull/47144) [ROCm] Change AttentionCGSuppoort in TritonMLA to UNIFORM_SINGLE_TOKEN_DECODE
- [#48132](https://github.com/vllm-project/vllm/pull/48132) Reset num_accepted_tokens on add_request in all modes
- [#39988](https://github.com/vllm-project/vllm/pull/39988) Fix turboquant FP8 cast failure for BF16 models on Ampere GPUs
- [#48045](https://github.com/vllm-project/vllm/pull/48045) Fix FlashMLA dense fp8 metadata crash (num_sm_parts clamp)
- [#47314](https://github.com/vllm-project/vllm/pull/47314) Fix packed HND KV cache reshape for FlashAttention
- [#48276](https://github.com/vllm-project/vllm/pull/48276) Register Qwen/Qwen3.5-4B example model
- [#48102](https://github.com/vllm-project/vllm/pull/48102) Fix stale transfer_jobs after reset_cache + harden job completion
- [#48361](https://github.com/vllm-project/vllm/pull/48361) (Opened) Fix hybrid-Mamba prefix-cache corruption under MTP/EAGLE speculative decoding
- [#48425](https://github.com/vllm-project/vllm/pull/48425) (Opened) Handle per-group prefix-hit divergence for hybrid models with KV connector
- [#48032](https://github.com/vllm-project/vllm/pull/48032) (Opened) Make Marlin MoE route alignment deterministic
- [#48303](https://github.com/vllm-project/vllm/pull/48303) (Opened) Complete FlashInfer CUTLASS MXFP4 MoE wiring for DeepSeek-family models
- [#48000](https://github.com/vllm-project/vllm/pull/48000) (Opened) MiniMax-M3 tool parser: stream tool-call arguments incrementally
- [#48295](https://github.com/vllm-project/vllm/pull/48295) (Opened) Stream tool calls that arrive whole in a single delta in llama3_json, jamba and ernie45 parsers
- [#48245](https://github.com/vllm-project/vllm/pull/48245) (Opened) Fix `num_output_placeholders` preemption underflow
- [#48002](https://github.com/vllm-project/vllm/pull/48002) (Opened) Stream JSON envelope argument values
- [#48368](https://github.com/vllm-project/vllm/pull/48368) (Opened) Fix KV connector throughput metric under concurrent transfers
- [#47950](https://github.com/vllm-project/vllm/pull/47950) (Opened) Combination of sleep mode and speculative decoding cause crash (ROCm / MI250)
- [#48028](https://github.com/vllm-project/vllm/pull/48028) (Opened) Support non-gated MoE in online quantization and Marlin MoE tile padding
- [#48171](https://github.com/vllm-project/vllm/pull/48171) (Opened) Fix lfm2 tool parser dropping calls with brackets or newline
- [#48304](https://github.com/vllm-project/vllm/pull/48304) (Opened) Honor DeepSeek V4 checkpoints' MTP-layer compress_ratio entry
- [#47988](https://github.com/vllm-project/vllm/pull/47988) (Opened) Handle E8M0 block scales in CUTLASS and Triton FP8 linear kernels
- [#48261](https://github.com/vllm-project/vllm/pull/48261) (Opened) Fix stale attn metadata in speculator prefill cudagraph capture
- [#48413](https://github.com/vllm-project/vllm/pull/48413) (Opened) Fix MiniCPM-V placeholder replacement and image processor loading on Transformers v5
- [#48173](https://github.com/vllm-project/vllm/pull/48173) (Opened) [ROCm] Pad block-FP8 MoE intermediate size for TP when not divisible by block_n
- [#47955](https://github.com/vllm-project/vllm/pull/47955) (Opened) Stream full single-delta tool calls
- [#48317](https://github.com/vllm-project/vllm/pull/48317) (Opened) Count per-group blocks in get_max_concurrency_for_kv_cache_config
- [#48262](https://github.com/vllm-project/vllm/pull/48262) (Opened) Gemma4 parser: classify channel-less output consistently in streaming and non-streaming
- [#48001](https://github.com/vllm-project/vllm/pull/48001) (Opened) Use DeepSeek tool slot name for wrapper unwrapping
- [#48337](https://github.com/vllm-project/vllm/pull/48337) (Opened) Fix level-2 sleep/wake crash with enable_lora=True
- [#48003](https://github.com/vllm-project/vllm/pull/48003) (Opened) Fix corrupted output with FlashInfer + decode context parallelism
- [#48365](https://github.com/vllm-project/vllm/pull/48365) (Opened) Gemma4: don't crash when a KV-shared layer has no same-type target
- [#47963](https://github.com/vllm-project/vllm/pull/47963) (Opened) Report finish_reason='length' for tool calls truncated by max_tokens in streaming
- [#48343](https://github.com/vllm-project/vllm/pull/48343) (Opened) DeepSeek V3: don't truncate final streamed tool arguments that don't end with '}'
- [#48210](https://github.com/vllm-project/vllm/pull/48210) (Opened) Pin FlashInfer bmm_fp8 to cuBLAS on sm_12x to avoid cuDNN hot-path stalls
- [#48141](https://github.com/vllm-project/vllm/pull/48141) (Opened) Fix P/D preemption race condition
- [#48432](https://github.com/vllm-project/vllm/pull/48432) (Opened) Support heterogeneous attention head counts per layer in Transformers backend
- [#48282](https://github.com/vllm-project/vllm/pull/48282) (Opened) Emit added/done lifecycle events for zero-delta streaming items
- [#48353](https://github.com/vllm-project/vllm/pull/48353) (Opened) Hermes tool parser: parse tool call JSON by object boundary, not literal </tool_call>
- [#48371](https://github.com/vllm-project/vllm/pull/48371) (Opened) Fix OOB expert_map read in moe_fused_mul_sum with invalid topk_ids
- [#48226](https://github.com/vllm-project/vllm/pull/48226) (Opened) Keep fully-excluded fused MoE experts unquantized
- [#48109](https://github.com/vllm-project/vllm/pull/48109) (Opened) [XPU] Fix Mamba state pointer overflow
- [#47954](https://github.com/vllm-project/vllm/pull/47954) (Opened) Anchor empty-args detection to the current tool in xlam and hunyuan_a13b streaming parsers
- [#48195](https://github.com/vllm-project/vllm/pull/48195) (Opened) Fix per-group prefix-hit divergence for hybrid Mamba + KV connector
- [#48313](https://github.com/vllm-project/vllm/pull/48313) (Opened) Pick KV cache block size from all attention backends
- [#48134](https://github.com/vllm-project/vllm/pull/48134) (Opened) Limit chat top_logprobs in responses
- [#48416](https://github.com/vllm-project/vllm/pull/48416) (Opened) Fix xgrammar feature gate bypass when JSON Schema type is a list
- [#48006](https://github.com/vllm-project/vllm/pull/48006) (Opened) Reject invalid DeepSeek history tool arguments
- [#48321](https://github.com/vllm-project/vllm/pull/48321) (Opened) Responses API: resolve explicit null background/truncation to their defaults
- [#48375](https://github.com/vllm-project/vllm/pull/48375) (Opened) Honor drop_eagle_block in MambaManager
- [#48251](https://github.com/vllm-project/vllm/pull/48251) (Opened) Preserve post-load tensors across weight reloads
- [#48331](https://github.com/vllm-project/vllm/pull/48331) (Opened) Guard dynamic video sampling metadata
- [#48104](https://github.com/vllm-project/vllm/pull/48104) (Opened) use real per-chunk offsets for segment timestamps
- [#48348](https://github.com/vllm-project/vllm/pull/48348) (Opened) InternLM2: stream tool calls that arrive whole in a single delta
- [#48149](https://github.com/vllm-project/vllm/pull/48149) (Opened) Fix silent text-LoRA no-op for remaining VLM wrapper models
- [#48420](https://github.com/vllm-project/vllm/pull/48420) (Opened) Fix Qwen3-Omni crash on video with no audio track when use_audio_in_video=True
- [#48167](https://github.com/vllm-project/vllm/pull/48167) (Opened) Fix FlashInfer non-causal draft attention (DFlash/DSpark) on Blackwell
- [#48339](https://github.com/vllm-project/vllm/pull/48339) (Opened) Flatten list message content when echoing in streaming chat completions
- [#48039](https://github.com/vllm-project/vllm/pull/48039) (Opened) Let pooling chunked prefill use full context
- [#48334](https://github.com/vllm-project/vllm/pull/48334) (Opened) [XPU] FP8 o_proj with fp8_bmm and contiguous scale fix
- [#48341](https://github.com/vllm-project/vllm/pull/48341) (Opened) Auto-enable async scheduling for draft models
- [#48023](https://github.com/vllm-project/vllm/pull/48023) (Opened) Fix/spec draft inherit model weights
- [#48128](https://github.com/vllm-project/vllm/pull/48128) (Opened) prevent VTE crash from empty indicator_tokens
- [#48160](https://github.com/vllm-project/vllm/pull/48160) (Opened) Olmo3 reasoning parser drops content sharing a streaming delta with </think>
- [#48419](https://github.com/vllm-project/vllm/pull/48419) (Opened) fix allowed_token_ids_mask aliasing in InputBatch.swap_states
- [#47968](https://github.com/vllm-project/vllm/pull/47968) (Opened) Return early for unlisted tool names in InternLM2 parser
- [#48092](https://github.com/vllm-project/vllm/pull/48092) (Opened) Convert media fetch connection/DNS failures to HTTP 422
- [#48179](https://github.com/vllm-project/vllm/pull/48179) (Opened) Presize shared MoE Workspace To Worst-Case Size Before Lock
- [#48351](https://github.com/vllm-project/vllm/pull/48351) (Opened) YaRN RoPE: honor explicit attention_factor from the rope config
- [#48366](https://github.com/vllm-project/vllm/pull/48366) (Opened) Prevent NaN poisoning in xpu_mla_sparse for fully-masked index chunks
- [#48421](https://github.com/vllm-project/vllm/pull/48421) (Opened) Skip no-LoRA tokens (index -1) in CPU torch bgmv ops
- [#48386](https://github.com/vllm-project/vllm/pull/48386) (Opened) recompute ernie45 response-end index after stripping prefix
- [#47996](https://github.com/vllm-project/vllm/pull/47996) (Opened) [ROCm] Fix failing ROCm quick reduce test
- [#48411](https://github.com/vllm-project/vllm/pull/48411) (Opened) Include inline per-token-head scales in offloaded page transfer width
- [#48115](https://github.com/vllm-project/vllm/pull/48115) (Opened) Escape control characters in xgrammar choice grammar
- [#48404](https://github.com/vllm-project/vllm/pull/48404) (Opened) Size the sparse-indexer expanded block table from the runner's block-table width
- [#48433](https://github.com/vllm-project/vllm/pull/48433) (Opened) Preserve async load reservations
- [#48075](https://github.com/vllm-project/vllm/pull/48075) (Opened) Disable fused allreduce when NVLink multicast is unavailable
- [#48007](https://github.com/vllm-project/vllm/pull/48007) (Opened) Preserve partial args for truncated tool calls
- [#48114](https://github.com/vllm-project/vllm/pull/48114) (Opened) Fix/gemma4 per layer attn no fa4
- [#48241](https://github.com/vllm-project/vllm/pull/48241) (Opened) Domino inference patches for speculators-format checkpoints

</details>

<details>
<summary>Refactors (3)</summary>

- [#48158](https://github.com/vllm-project/vllm/pull/48158) Remove unused rocm kernel `combine_topk_swa_indices_ragged`
- [#48200](https://github.com/vllm-project/vllm/pull/48200) (Opened) StructuredOutputManager x Speculative Decoding Refactor
- [#48424](https://github.com/vllm-project/vllm/pull/48424) (Opened) Fix mypy for `vllm/model_executor/layers/fla/ops`

</details>

<details>
<summary>Other (21)</summary>

- [#48220](https://github.com/vllm-project/vllm/pull/48220) Remove dead code in ViT functionality test
- [#47388](https://github.com/vllm-project/vllm/pull/47388) Persist and reuse the memory-profiling result across boots (opt-in)
- [#47844](https://github.com/vllm-project/vllm/pull/47844) [Rust Frontend] Handle `continue_final_message` with renderer sentinel
- [#48278](https://github.com/vllm-project/vllm/pull/48278) DP Supervisor Log Improvement
- [#46415](https://github.com/vllm-project/vllm/pull/46415) Sanitize server file paths from validation error responses
- [#47744](https://github.com/vllm-project/vllm/pull/47744) Pass request context to CPU offload cache policy touch
- [#47053](https://github.com/vllm-project/vllm/pull/47053) only materialize tokens when thinking budget is in req
- [#48154](https://github.com/vllm-project/vllm/pull/48154) [ROCm] Revert Part of `[ROCm] Fix pooling startup workspace lock` [#47912](https://github.com/vllm-project/vllm/pull/47912)
- [#47946](https://github.com/vllm-project/vllm/pull/47946) Skip DeepEP MoE layer tests without P2P access
- [#43896](https://github.com/vllm-project/vllm/pull/43896) Correct model layer aliasing for Bert style models
- [#47731](https://github.com/vllm-project/vllm/pull/47731) [ROCm] Minimize comment in RocmAttention q_scale check
- [#48144](https://github.com/vllm-project/vllm/pull/48144) update marlin M size for EP
- [#47044](https://github.com/vllm-project/vllm/pull/47044) `kv_sharing_fast_prefill` correction
- [#48014](https://github.com/vllm-project/vllm/pull/48014) Move MRV1 `late_interaction_runner.py` out of MRV2 subtree
- [#47969](https://github.com/vllm-project/vllm/pull/47969) Remove unused _get_kv_cache_config_deepseek_v4 alias
- [#47962](https://github.com/vllm-project/vllm/pull/47962) [XPU] Disable fuse_rope_kvcache_cat_mla & qk_norm_rope_ fusion on XPU
- [#47970](https://github.com/vllm-project/vllm/pull/47970) Remove router weight upcast for DSv2-related models
- [#47884](https://github.com/vllm-project/vllm/pull/47884) Fix Batched DeepGEMM
- [#47995](https://github.com/vllm-project/vllm/pull/47995) updated flash_attn GIT_TAG to point to torch Stable ABI FA3 commit
- [#47316](https://github.com/vllm-project/vllm/pull/47316) Use meta tensor for KV cache stride calculation
- [#48269](https://github.com/vllm-project/vllm/pull/48269) [Revert] Update vllm ...builds FA3 with torch stable API

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 90f0c2bc745beabb92b3507f145560718637be319962001b5d89e33e463a06e9 -->
