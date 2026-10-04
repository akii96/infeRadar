# sglang: PR digest (2026-09-09 to 2026-09-13)

_254 merged, 442 newly opened - source sgl-project/sglang, generated 2026-09-13T23:22:57Z_

## TL;DR
- **DeepSeek V4.1 dominated the window.** Merged work covered FlashMLA V4.1 fp8/fp4 paged KV layouts, a two-level DeepGEMM candidate indexer, and DSpark verify and MoE fusions on Blackwell (BS1 reached 803 tok/s). The new-model PRs ([#38798](https://github.com/sgl-project/sglang/pull/38798), [#38950](https://github.com/sgl-project/sglang/pull/38950), [#39186](https://github.com/sgl-project/sglang/pull/39186)) are still open.
- **GLM-5.3 Flash, MiniMax-H3 and Qwen3.8-Next** were the next most active. GLM got KPool metadata fusion, breakable prefill CUDA graphs and NVFP4 loading. MiniMax-H3 got diffusion backends and SM90 Sage sparse attention. Qwen3.8 got PD state transfer and NVFP4 on DGX Spark.
- **Kernel and MoE work centered on Blackwell and Hopper.** Merged: FlashInfer MegaMoE, MXFP4 expert-pack JIT kernels, and DSA top-k v2. In flight: a CUTLASS MXFP4×BF16 grouped-GEMM for SM90, NCCL EP Triton MoE and MXFP4 KV cache on SM120.
- **AMD and NPU pushed hard.** AMD merged a Triton sparse-MLA backend and aiter DCP. The open queue holds large gfx950 DSV4/GLM enablement. NPU merged Ascend HiCache L3 and DSA KV offload.
- **Direction:** cleanup is also under way, including a 12.7k-line deletion of legacy kernels and CUDA 12 retirement. HiCache and Unified Cache and the Rust TreeCore are being reworked, and the router is gaining cache-aware routing.

## Most important PRs
**[#32114](https://github.com/sgl-project/sglang/pull/32114) Delete cutlass_mla, non-Marlin GPTQ, AWQ AOT kernel, Dual Chunk Flash Attention**
Removes about 12.6k lines of legacy kernels and their tests and CI. This shrinks the build and maintenance surface.

**[#38944](https://github.com/sgl-project/sglang/pull/38944) DSV4.1 two-level candidate indexer on DeepGEMM paged sparse MQA logits**
Enables a two-level candidate indexer on DeepGEMM's paged sparse MQA logits. It is a core attention-path optimization for DeepSeek V4.1 long-context sparse decode.

**[#39123](https://github.com/sgl-project/sglang/pull/39123) Paged KV cache layouts for FlashMLA V4.1 fp8/fp4**
Adds paged KV layouts for FlashMLA's V4.1 fp8 and fp4 formats. These are the memory-format foundation for V4.1 serving, and [#39171](https://github.com/sgl-project/sglang/pull/39171) bumps FlashMLA to match.

**[#31470](https://github.com/sgl-project/sglang/pull/31470) Support FlashInfer Mega Moe**
Integrates a fused FlashInfer MegaMoE path on NVIDIA. It is a large MoE throughput lever that follow-up work (BF16 and NVFP4 W4A16 variants) builds on.

**[#30575](https://github.com/sgl-project/sglang/pull/30575) Enable Fast Triton Sparse MLA backend on AMD**
Brings a fast Triton sparse-MLA backend to ROCm. This is DSA-style attention that AMD lacked a fast path for.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#38879](https://github.com/sgl-project/sglang/pull/38879) DeepSeek-V4.1 DSpark verify and MoE kernel optimizations on Blackwell
- [#38976](https://github.com/sgl-project/sglang/pull/38976) Small-batch DSpark optimization on Blackwell (BS1 803 tok/s)
- [#39068](https://github.com/sgl-project/sglang/pull/39068) Fuse DSpark verify compression, indexer and projections
- [#36411](https://github.com/sgl-project/sglang/pull/36411) Qwen3-VL unique-image serving perf on H100
- [#39177](https://github.com/sgl-project/sglang/pull/39177) Scope graph-pool borrowing and reduce fragmentation
- [#39116](https://github.com/sgl-project/sglang/pull/39116) AMD DSpark accept-length fix and host-bubble reduction on DSV4

</details>

<details>
<summary>Kernels & attention (18)</summary>

- [#30805](https://github.com/sgl-project/sglang/pull/30805) Integrate TRT-LLM DSv4 attention for SM100/103
- [#38829](https://github.com/sgl-project/sglang/pull/38829) DSA top-k v2 long-context cluster rework and NaN padding
- [#39305](https://github.com/sgl-project/sglang/pull/39305) Exact bf16 consumer top-k adapted from DeepSelect
- [#33672](https://github.com/sgl-project/sglang/pull/33672) Raw-index output in TopK v2
- [#39098](https://github.com/sgl-project/sglang/pull/39098) Port of raw-index TopK v2 output to DSV4.1
- [#38830](https://github.com/sgl-project/sglang/pull/38830) Port expert-pack MXFP4 kernels to load_jit and fix launch limits
- [#39138](https://github.com/sgl-project/sglang/pull/39138) Commit engram decode history inside the hash kernel
- [#36655](https://github.com/sgl-project/sglang/pull/36655) SM120 exact query-head widths for DSv4 sparse MLA decode
- [#38851](https://github.com/sgl-project/sglang/pull/38851) Make paged sparse-decode gather memory-safe
- [#38855](https://github.com/sgl-project/sglang/pull/38855) Dequantize FP8 cached prefixes in sparse prefill kernels
- [#38964](https://github.com/sgl-project/sglang/pull/38964) Keep DSpark SWA paged with bounded encoder replay
- [#34432](https://github.com/sgl-project/sglang/pull/34432) AMD DCP support for the aiter backend
- [#37659](https://github.com/sgl-project/sglang/pull/37659) Parallelize aiter spec-decode KV index building
- [#38757](https://github.com/sgl-project/sglang/pull/38757) Route aiter head_dim>256 prefill through Triton unified_attention
- [#38754](https://github.com/sgl-project/sglang/pull/38754) aiter: honor per-layer softmax scale
- [#38756](https://github.com/sgl-project/sglang/pull/38756) aiter: resolve SWA KV pool for draft workers
- [#38755](https://github.com/sgl-project/sglang/pull/38755) aiter: fail loudly on cross-layer KV sharing in target_verify
- [#38960](https://github.com/sgl-project/sglang/pull/38960) Remove unused tokenwise QSA implementation

</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#38328](https://github.com/sgl-project/sglang/pull/38328) Admit the unified Triton MoE router on ROCm
- [#37679](https://github.com/sgl-project/sglang/pull/37679) GraniteMoE: load split per-expert quantized weights
- [#38612](https://github.com/sgl-project/sglang/pull/38612) Kimi-K3: accept fp32 routing weights in fused MoE finalize
- [#38578](https://github.com/sgl-project/sglang/pull/38578) LoRA MoE in full and breakable prefill CUDA graphs
- [#34330](https://github.com/sgl-project/sglang/pull/34330) AMD: fix weight checking for AITER-shuffled block FP8
- [#38748](https://github.com/sgl-project/sglang/pull/38748) AMD: online MXFP4 quantization of bf16 MTP draft experts for Qwen3.5
- [#38527](https://github.com/sgl-project/sglang/pull/38527) INT4 and FP4 lanes in Ling-3.0-flash-VL cookbook

</details>

<details>
<summary>Model support (20)</summary>

- [#36606](https://github.com/sgl-project/sglang/pull/36606) Diffusion: SenseNova-U1.5-8B-MoT
- [#37903](https://github.com/sgl-project/sglang/pull/37903) Diffusion: VDN-H3 with hybrid_window_attn_h3 backend
- [#37982](https://github.com/sgl-project/sglang/pull/37982) MiniMax-H3 SM90 Sage compute for SubBlock sparse attention
- [#38455](https://github.com/sgl-project/sglang/pull/38455) MiniMax-H3 Singularity hybrid checkpoints
- [#33366](https://github.com/sgl-project/sglang/pull/33366) MiniMax H3 on XPU
- [#35599](https://github.com/sgl-project/sglang/pull/35599) NemotronH_Omni_Reasoning_V3
- [#34556](https://github.com/sgl-project/sglang/pull/34556) Mamba 1 and 2 inference
- [#39126](https://github.com/sgl-project/sglang/pull/39126) Qwen3.8 NVFP4 on DGX Spark with file-backed PLE
- [#36651](https://github.com/sgl-project/sglang/pull/36651) Qwen3.8-Next PD state transfer
- [#38845](https://github.com/sgl-project/sglang/pull/38845) GLM-5.3 Flash KPool metadata fusion
- [#38522](https://github.com/sgl-project/sglang/pull/38522) Opt-in GLM-5.3 Flash breakable prefill CUDA graphs
- [#38621](https://github.com/sgl-project/sglang/pull/38621) GLM-5.3 Flash NVFP4 loading
- [#38250](https://github.com/sgl-project/sglang/pull/38250) NPU: GLM5.2 and FP8 DSA indexer KV cache for 950
- [#38693](https://github.com/sgl-project/sglang/pull/38693) granite_thinking_parser for Granite 4.2
- [#38297](https://github.com/sgl-project/sglang/pull/38297) Auto-detect GLM-5.3 chat templates as glm45/glm47 parsers
- [#38951](https://github.com/sgl-project/sglang/pull/38951) DeepSeek V4.1 tool-call structural tag with DSML names
- [#38963](https://github.com/sgl-project/sglang/pull/38963) Fix DSV4.1 VL routing dropping the fused shared expert
- [#38584](https://github.com/sgl-project/sglang/pull/38584) Optimize Qwen-Image-Edit attention on Hopper
- [#38549](https://github.com/sgl-project/sglang/pull/38549) Qwen-Image-Layered outputs and CFG2 rounding
- [#38591](https://github.com/sgl-project/sglang/pull/38591) Lossless BCG for FLUX.1-dev

</details>

<details>
<summary>Parallelism & scheduling (17)</summary>

- [#36848](https://github.com/sgl-project/sglang/pull/36848) HiCache segment lock protocol replaces skip_lock_node_ids
- [#36631](https://github.com/sgl-project/sglang/pull/36631) Sampling masks with overlap scheduling
- [#36899](https://github.com/sgl-project/sglang/pull/36899) Domino rollout for DFlash V2
- [#37069](https://github.com/sgl-project/sglang/pull/37069) TP>1 Domino rollout for DFlash V2
- [#37565](https://github.com/sgl-project/sglang/pull/37565) NPU DFlash spec decode for MiMo-V2.5-Pro (mxfp4)
- [#38356](https://github.com/sgl-project/sglang/pull/38356) kv-shard 1/4: logical-page placement with UnifiedRadixCache
- [#37709](https://github.com/sgl-project/sglang/pull/37709) Transfer DCP-replicated DSPARK draft KV in DCP1→DCP-N relayouts
- [#38949](https://github.com/sgl-project/sglang/pull/38949) Static DSpark PD for DeepSeek V4.1
- [#36612](https://github.com/sgl-project/sglang/pull/36612) Share PD prefill→decode failure notification across backends
- [#36713](https://github.com/sgl-project/sglang/pull/36713) Evict Full KV for Mamba byte shortfalls in unified memory
- [#38577](https://github.com/sgl-project/sglang/pull/38577) HiCache LoRA storage pages isolated by extra key
- [#38165](https://github.com/sgl-project/sglang/pull/38165) Publish fresh streamed LoRA versions alongside generation
- [#38936](https://github.com/sgl-project/sglang/pull/38936) Disable NCCL graph buffer registration for TP LM-head all-to-all
- [#37933](https://github.com/sgl-project/sglang/pull/37933) Keep shared MAX_LEN prefill graph bucket for MegaMoE sparse-DP
- [#38349](https://github.com/sgl-project/sglang/pull/38349) Fix PureSWA tail release without insertion
- [#38249](https://github.com/sgl-project/sglang/pull/38249) Fix NPU pp2 hang
- [#39165](https://github.com/sgl-project/sglang/pull/39165) Default --dcp-comm-backend to fi_a2a/a2a

</details>

<details>
<summary>Hardware & arch (14)</summary>

- [#38827](https://github.com/sgl-project/sglang/pull/38827) NPU: Ascend Memcache HiCache L3 backend
- [#38826](https://github.com/sgl-project/sglang/pull/38826) NPU: HiCache L2 IO via Memfabric acc_offload
- [#33089](https://github.com/sgl-project/sglang/pull/33089) NPU: sparsity-driven KV offload for DeepSeek DSA
- [#38775](https://github.com/sgl-project/sglang/pull/38775) NPU DeepEP test and nightly tuning
- [#38174](https://github.com/sgl-project/sglang/pull/38174) NPU: mf device urma and host rdma trans type
- [#38807](https://github.com/sgl-project/sglang/pull/38807) NPU: glm5.2 fp8 memory optimization
- [#34722](https://github.com/sgl-project/sglang/pull/34722) NPU: LTX-2/2.3 performance
- [#30548](https://github.com/sgl-project/sglang/pull/30548) Spec decode for intel_xpu attention backend
- [#32798](https://github.com/sgl-project/sglang/pull/32798) DFLASH for XPU
- [#35051](https://github.com/sgl-project/sglang/pull/35051) XPU: pack device-pointer tables as uint64
- [#36278](https://github.com/sgl-project/sglang/pull/36278) XPU Gemma3RMSNorm forward, test and benchmark
- [#38269](https://github.com/sgl-project/sglang/pull/38269) AMD unified KV for DeepSeek-V4 in direct external linkers
- [#33939](https://github.com/sgl-project/sglang/pull/33939) AMD gfx1151 Docker image
- [#38758](https://github.com/sgl-project/sglang/pull/38758) Allow aiter attention backend for Gemma-4

</details>

<details>
<summary>API & serving (9)</summary>

- [#38690](https://github.com/sgl-project/sglang/pull/38690) Responses API: custom tools, encrypted reasoning replay, developer tier
- [#39122](https://github.com/sgl-project/sglang/pull/39122) Gate /v1/responses persistence behind --enable-response-store
- [#36141](https://github.com/sgl-project/sglang/pull/36141) /v1/responses support in HTTP PD router
- [#35503](https://github.com/sgl-project/sglang/pull/35503) Propagate PD routing metadata through /v1/responses
- [#35486](https://github.com/sgl-project/sglang/pull/35486) Fix empty-prompt routing for token-first chat encoders
- [#38985](https://github.com/sgl-project/sglang/pull/38985) Fix DSV4.1 /v1/responses empty prompt routing
- [#38814](https://github.com/sgl-project/sglang/pull/38814) Router: preserve global cache affinity with bucket routing
- [#37994](https://github.com/sgl-project/sglang/pull/37994) Rust: gate health on startup warmup completion
- [#34430](https://github.com/sgl-project/sglang/pull/34430) rust-server: node-local HTTP ports for DP attention

</details>

<details>
<summary>Tests (10)</summary>

- [#37015](https://github.com/sgl-project/sglang/pull/37015) Unit test for muse_glimmer_format
- [#38336](https://github.com/sgl-project/sglang/pull/38336) Offline Transformers loader compatibility checks
- [#38881](https://github.com/sgl-project/sglang/pull/38881) Drop GPTQ dynamic-config test for deleted kernel
- [#39013](https://github.com/sgl-project/sglang/pull/39013) Trim DSV4 trtllm B200 tests
- [#38791](https://github.com/sgl-project/sglang/pull/38791) Enable ROCm LoRA logprob accuracy coverage
- [#38732](https://github.com/sgl-project/sglang/pull/38732) Simulator comparison tolerance headroom
- [#34977](https://github.com/sgl-project/sglang/pull/34977) is_dummy truth-table wire tests for mooncake and nixl
- [#38581](https://github.com/sgl-project/sglang/pull/38581) Restore AMD CI registrations dropped by #37436
- plus 2 more minor test updates

</details>

<details>
<summary>CI & build (17)</summary>

- [#38404](https://github.com/sgl-project/sglang/pull/38404) Retire the CUDA 12 lane
- [#38763](https://github.com/sgl-project/sglang/pull/38763) Publish ROCm 10 release images and kernel wheel
- [#38659](https://github.com/sgl-project/sglang/pull/38659) ROCm 10 default for AMD PR and nightly tests
- [#38767](https://github.com/sgl-project/sglang/pull/38767) Retire ROCm 7.0 kernel wheel
- [#38694](https://github.com/sgl-project/sglang/pull/38694) Drop dead miles ROCm 7.0 nightly image
- [#38734](https://github.com/sgl-project/sglang/pull/38734) /run-full-ci and /run-extra-ci slash commands
- [#38736](https://github.com/sgl-project/sglang/pull/38736) Answer unrecognized slash commands
- [#38770](https://github.com/sgl-project/sglang/pull/38770) Temporarily disable GB300 tests
- [#38842](https://github.com/sgl-project/sglang/pull/38842) Revert GB300 disable
- [#38014](https://github.com/sgl-project/sglang/pull/38014) Merge XPU stage-a+b jobs
- [#38801](https://github.com/sgl-project/sglang/pull/38801) Raise smg-grpc-servicer floor
- [#39241](https://github.com/sgl-project/sglang/pull/39241) Fix DeepGEMM release dependencies
- [#39163](https://github.com/sgl-project/sglang/pull/39163) Fix DeepGEMM sanitizer setup and Blackwell timeouts
- [#39255](https://github.com/sgl-project/sglang/pull/39255) Diffusion GT generation without publish token
- [#38629](https://github.com/sgl-project/sglang/pull/38629) Don't fail nightly on unreadable perf dump
- [#38782](https://github.com/sgl-project/sglang/pull/38782) Expose nightly server telemetry coverage
- plus 1 more minor CI update

</details>

<details>
<summary>Docs (14)</summary>

- [#38802](https://github.com/sgl-project/sglang/pull/38802) DeepSeek-V4.1 Flash cookbook
- [#38611](https://github.com/sgl-project/sglang/pull/38611) NVFP4 export in Qwen3.8-27B cookbook
- [#38844](https://github.com/sgl-project/sglang/pull/38844) HiCache L2 knob in DeepSeek-V4.1 Playground
- [#38861](https://github.com/sgl-project/sglang/pull/38861) Make remaining DSV4.1 NVIDIA cells start
- [#38839](https://github.com/sgl-project/sglang/pull/38839) Fix DSV4.1 reasoning example
- [#39213](https://github.com/sgl-project/sglang/pull/39213) GLM-5.3-Flash cookbook MTP and EP1 recipe
- [#39230](https://github.com/sgl-project/sglang/pull/39230) GLM-5.2 MXFP4 recipe update on MI355X
- [#39106](https://github.com/sgl-project/sglang/pull/39106) Triton DSA backend for GLM-5.2 MXFP4 on MI355X
- [#39252](https://github.com/sgl-project/sglang/pull/39252) AMD dspark config for deepseek-v4
- [#39029](https://github.com/sgl-project/sglang/pull/39029) Kimi-K3 MI350X/MI355X cookbook numbers
- [#39190](https://github.com/sgl-project/sglang/pull/39190) Kimi-K3 DCP under HiCache L1+L2 with DSPARK
- [#39104](https://github.com/sgl-project/sglang/pull/39104) MI355X MXFP4 HiCache defaults for Qwen3.5 cookbook
- [#38534](https://github.com/sgl-project/sglang/pull/38534) JoyEcho H200 residency and BCG recipe
- [#36230](https://github.com/sgl-project/sglang/pull/36230) Update prefill CP documentation
- [#36773](https://github.com/sgl-project/sglang/pull/36773) Sync LMSYS blog cards

</details>

<details>
<summary>Bugfixes (13)</summary>

- [#33922](https://github.com/sgl-project/sglang/pull/33922) Fix Qwen3.5 GDN multi-item scoring
- [#34820](https://github.com/sgl-project/sglang/pull/34820) Store mamba prefix-cache checkpoints at configured SSM dtype
- [#38596](https://github.com/sgl-project/sglang/pull/38596) Fix KV-canary workspace accounting after graph capture
- [#39136](https://github.com/sgl-project/sglang/pull/39136) Preserve GLM tool argument types across JSON Schema unions
- [#38988](https://github.com/sgl-project/sglang/pull/38988) Fix RunAI checkpoint index filtering
- [#38908](https://github.com/sgl-project/sglang/pull/38908) Fix gpt-oss RunAI streamer weight ownership
- [#38957](https://github.com/sgl-project/sglang/pull/38957) Fix HiCache with DSV4.1 encoder SWA replay
- [#34459](https://github.com/sgl-project/sglang/pull/34459) Fix DSV4 routing sqrtsoftplus underflow
- [#38730](https://github.com/sgl-project/sglang/pull/38730) Fix custom logit processor params with num_tokens_in_batch
- [#39038](https://github.com/sgl-project/sglang/pull/39038) Session: work with PD and fix empty continuations
- [#38564](https://github.com/sgl-project/sglang/pull/38564) Stamp SP state on dummy forward batches
- [#39120](https://github.com/sgl-project/sglang/pull/39120) Fix multimodal embedding cache retaining batches via views
- [#37564](https://github.com/sgl-project/sglang/pull/37564) and [#37254](https://github.com/sgl-project/sglang/pull/37254) AMD aiter bpreshuffle GEMM and Quark MiniMax-M3 MXFP4 loading fixes

</details>

<details>
<summary>Refactors (10)</summary>

- [#38699](https://github.com/sgl-project/sglang/pull/38699) Diffusion utility ownership refactor
- [#33555](https://github.com/sgl-project/sglang/pull/33555) Unify RoPE execution for DiT models via CustomOp
- [#38954](https://github.com/sgl-project/sglang/pull/38954) Generalize DeepSeek V4 compressed pool management
- [#38947](https://github.com/sgl-project/sglang/pull/38947) Clarify DSV4 metadata names for V4.1
- [#38946](https://github.com/sgl-project/sglang/pull/38946) Remove prerelease DSV4.1 config aliases
- [#38993](https://github.com/sgl-project/sglang/pull/38993) Generalize attention graph variants in the decode runner
- [#38752](https://github.com/sgl-project/sglang/pull/38752) Single writer for config declaration stash
- [#38753](https://github.com/sgl-project/sglang/pull/38753) msgspec.Struct for config tier
- [#35644](https://github.com/sgl-project/sglang/pull/35644) Drop `_component` suffix in unified_cache components
- [#38041](https://github.com/sgl-project/sglang/pull/38041) Revert multi-layer EAGLE shared-read event publish

</details>

<details>
<summary>Other (20)</summary>

- [#32114](https://github.com/sgl-project/sglang/pull/32114) sibling cleanup: see Most important PRs
- [#37303](https://github.com/sgl-project/sglang/pull/37303) Rust TreeCore runtime and CI parity hardening
- [#37306](https://github.com/sgl-project/sglang/pull/37306) Rust TreeCore external cache linker
- [#37584](https://github.com/sgl-project/sglang/pull/37584) Port SWA branching-point caching to Rust TreeCore
- [#38482](https://github.com/sgl-project/sglang/pull/38482) Preserve aux LRU recency on node splits
- [#38486](https://github.com/sgl-project/sglang/pull/38486) Host store event for storage-prefetch refills
- [#38483](https://github.com/sgl-project/sglang/pull/38483) Release buffer prefetch anchor locks during cleanup
- [#37914](https://github.com/sgl-project/sglang/pull/37914) Support MTP/EAGLE/DSpark draft KV in external linker
- [#38169](https://github.com/sgl-project/sglang/pull/38169) Stage Inkling MTP draft metadata before verify
- [#38558](https://github.com/sgl-project/sglang/pull/38558) Large MTP batches in short-convolution metadata
- [#38535](https://github.com/sgl-project/sglang/pull/38535) Diffusion snapshot-offload component residency
- [#38689](https://github.com/sgl-project/sglang/pull/38689) Diffusion: pick attention backend by measurement
- [#38529](https://github.com/sgl-project/sglang/pull/38529) SANA-WM convolution and streaming GDN optimization
- [#38182](https://github.com/sgl-project/sglang/pull/38182) Wan VAE channels_last and Triton NHWC upsample
- [#38530](https://github.com/sgl-project/sglang/pull/38530) Fuse LongCat Image normalization and modulation
- [#38533](https://github.com/sgl-project/sglang/pull/38533) Preserve BF16 rounding in Hopper LTX QKNorm/RoPE fusion
- [#39202](https://github.com/sgl-project/sglang/pull/39202), [#39137](https://github.com/sgl-project/sglang/pull/39137), [#39134](https://github.com/sgl-project/sglang/pull/39134) Config/parallel-state cleanups
- [#39182](https://github.com/sgl-project/sglang/pull/39182) Provider hook for prefill-buffer ceilings
- [#39178](https://github.com/sgl-project/sglang/pull/39178), [#39176](https://github.com/sgl-project/sglang/pull/39176), [#39180](https://github.com/sgl-project/sglang/pull/39180) Graph-pool capacity check, executable reuse, stream affinity
- plus about 54 more PRs not shown in the source data

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 60e0fb54ea74dd6bab6b2639b0ff6b70933d619888d9408132dd38205262d73a -->
