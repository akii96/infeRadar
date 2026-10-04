# vllm: PR digest (2026-09-02 to 2026-09-06)

_196 merged, 451 newly opened - source vllm-project/vllm, generated 2026-09-06T23:00:23Z_

## TL;DR
- **Model focus:** DeepSeek (V4 and Vision) got the most label attention. Newer families (GLM-5.3-Flash, Kimi-K3, Qwen3.8/Qwen4Exp "Flash-Next", K2-Horizon, MiniMax-M3) got the most code churn. GLM-5.3-Flash landed as a roughly 18k-line merge.
- **Perf work:** Mostly model-specific kernels. Merged: QSA sparse-indexer prefill/decode split and PLE fusions for Qwen4Exp, a MiniMax-M3 ROCm indexer/top-k rewrite, Kimi-K3 KDA overlap and MLA epilogue fusion, a DSV3 GEMM unlock (12-81% kernel speedup), and a Model Runner V2 GPU mask compaction. Open: GDN decode optimizations, hybrid NVFP4 LM-head sampling, and low-SM multimem reduce-scatter.
- **Portability:** There is a large open push on DeepSeek-V4 beyond Hopper/Blackwell: SM12x and pre-SM90 sparse-MLA Triton fallbacks, a CPU backend, ROCm HIP compressor and AITER routing, and ROCm Vision. Merged: a CPU AMX-FP8 attention path for Diamond Rapids and Triton fallbacks for HY-V4.
- **Direction:** Day-0 support for new architectures, KV offload/connector hardening (NIXL, Mooncake, CPU offload), Model Runner V2 parity, a heavy Rust frontend build-out, and CI sharding.

## Most important PRs
**[#53906](https://github.com/vllm-project/vllm/pull/53906) GLM-5.3-Flash support**
Adds the model across attention, KV-cache, quantization, multimodal and spec-decode, with FlashInfer and AMD/NVIDIA paths. It is the window's largest merge. Follow-ups in [#55119](https://github.com/vllm-project/vllm/pull/55119) (EPLB) and the open [#55219](https://github.com/vllm-project/vllm/pull/55219) (packed KV layout) build on it.

**[#54566](https://github.com/vllm-project/vllm/pull/54566) DeepSeek-V4-Flash-Vision-Exp**
Adds the multimodal DeepSeek-V4 variant, with FlashInfer attention and MoE changes. Open work ([#55107](https://github.com/vllm-project/vllm/pull/55107)) is extending it to ROCm.

**[#54682](https://github.com/vllm-project/vllm/pull/54682) MiniMax-M3 ROCm decode indexer and top-k**
Reworks the sparse-attention decode indexer and top-k path for gfx9 (AMD) with about 2k added lines. It targets decode latency for sparse-attention models on AMD.

**[#54517](https://github.com/vllm-project/vllm/pull/54517) Fused Qwen4Exp PLE kernels**
Fuses the per-layer-embedding kernels for Qwen3.8-Flash-Next. Related merges separate the QSA prefill/decode indexer paths ([#54513](https://github.com/vllm-project/vllm/pull/54513)) and improve sparse GQA ([#54873](https://github.com/vllm-project/vllm/pull/54873)).

**[#50945](https://github.com/vllm-project/vllm/pull/50945) Model Runner V2: DBO support**
Adds dual-batch overlap in eager mode to MRV2. Together with eagle3 plus pipeline parallelism ([#50514](https://github.com/vllm-project/vllm/pull/50514)), this moves MRV2 toward feature parity with V1.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#54901](https://github.com/vllm-project/vllm/pull/54901) compact sampling masks on GPU instead of unpacking the full-vocab bitmask on CPU
- [#55202](https://github.com/vllm-project/vllm/pull/55202) ensure async H2D copies use pinned memory in more places
- [#54660](https://github.com/vllm-project/vllm/pull/54660) avoid more H2D copies from non-pinned tensors
- [#54845](https://github.com/vllm-project/vllm/pull/54845) low-M FP32 router GEMM for gfx950
- [#54896](https://github.com/vllm-project/vllm/pull/54896) cut Kimi-K3 MLA decode concat/cache epilogue latency
- [#54565](https://github.com/vllm-project/vllm/pull/54565) enable DSV3 GEMM for inner-contiguous and row-strided tensors
- [#55242](https://github.com/vllm-project/vllm/pull/55242) Kimi K3 NVFP4: align in_proj weights by 128 to avoid an elementwise copy
- [#52494](https://github.com/vllm-project/vllm/pull/52494) fuse MLA q/kv RMSNorm in the AMD Kimi-K3 wrapper
- [#55404](https://github.com/vllm-project/vllm/pull/55404) build GDN cudagraph-capture metadata without a device sync
- [#55062](https://github.com/vllm-project/vllm/pull/55062) accumulate Conformer attention scores with baddbmm
- [#55020](https://github.com/vllm-project/vllm/pull/55020) prefetch the weight before the PDL wait in fused_q_kv_rmsnorm
- [#55061](https://github.com/vllm-project/vllm/pull/55061) size the DSv4 dequant gather launch grid by rows
- [#55285](https://github.com/vllm-project/vllm/pull/55285) use SDPA for BLIP-2 Q-Former attention
- [#55415](https://github.com/vllm-project/vllm/pull/55415), [#55331](https://github.com/vllm-project/vllm/pull/55331), [#55012](https://github.com/vllm-project/vllm/pull/55012) minor multimodal and Rust-frontend perf tweaks

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#54651](https://github.com/vllm-project/vllm/pull/54651) Triton kernel for small-batch top-p-only masking
- [#55059](https://github.com/vllm-project/vllm/pull/55059) Triton iHC pre/post fallback for HY V4
- [#54697](https://github.com/vllm-project/vllm/pull/54697) overlap low-M TP8 KDA projections for Kimi-K3
- [#54687](https://github.com/vllm-project/vllm/pull/54687) reuse Qwen4Exp HC combine-norm for MTP input
- [#54915](https://github.com/vllm-project/vllm/pull/54915) compact indexer logits workspace for Qwen3.8-Flash-Next prefill
- [#54251](https://github.com/vllm-project/vllm/pull/54251) warm up Qwen GDN gated RMSNorm
- [#54859](https://github.com/vllm-project/vllm/pull/54859) bump FlashKDA to fix an unstable inverse
- [#54110](https://github.com/vllm-project/vllm/pull/54110) fall back from persistent top-k on low-shared-memory GPUs
- [#54819](https://github.com/vllm-project/vllm/pull/54819) sync FlashAttention with upstream
- [#53835](https://github.com/vllm-project/vllm/pull/53835) build fused GDN MTP decode for SM110
- [#51415](https://github.com/vllm-project/vllm/pull/51415) manual ActivationQuantFusionPass initial application

</details>

<details>
<summary>MoE & quantization (11)</summary>

- [#51285](https://github.com/vllm-project/vllm/pull/51285) targeted online quantization config based on user patterns
- [#51392](https://github.com/vllm-project/vllm/pull/51392) online quantization with partially pre-quantized checkpoints
- [#54747](https://github.com/vllm-project/vllm/pull/54747) handle padded routes in CUTLASS MoE permutations
- [#55069](https://github.com/vllm-project/vllm/pull/55069) allow TRTLLM FP8 block-scale MoE with SwiGLU clamp
- [#55511](https://github.com/vllm-project/vllm/pull/55511) tuned fused MoE config for E=256,N=512 on A100 80GB PCIe
- [#54606](https://github.com/vllm-project/vllm/pull/54606) enable Kimi-K3 SiTU on the CuteDSL MoE backend
- [#51453](https://github.com/vllm-project/vllm/pull/51453) register Triton W4A16 GEMM as a custom op
- [#46009](https://github.com/vllm-project/vllm/pull/46009) preserve unquantized weight storage on ROCm MoE
- [#54770](https://github.com/vllm-project/vllm/pull/54770) register Quark per-block FP8 scales as weight_scale
- [#54882](https://github.com/vllm-project/vllm/pull/54882), [#54722](https://github.com/vllm-project/vllm/pull/54722) FP8 PLE weight loading and scale validation
- [#50220](https://github.com/vllm-project/vllm/pull/50220) fix MoE fused sum row offsets

</details>

<details>
<summary>Model support (7)</summary>

- [#55063](https://github.com/vllm-project/vllm/pull/55063) K2-Horizon model support
- [#54884](https://github.com/vllm-project/vllm/pull/54884) Rust frontend: token-attributed text in reasoning and unified parsers
- [#53614](https://github.com/vllm-project/vllm/pull/53614) Kimi K3 internal prefix checkpoints with partial prefix caching and spec decode
- [#55119](https://github.com/vllm-project/vllm/pull/55119) EPLB support for GLM-5.3-Flash
- [#54941](https://github.com/vllm-project/vllm/pull/54941) Transformers backend: find attention via a fuser and attach vLLM's layer
- [#54969](https://github.com/vllm-project/vllm/pull/54969) enable torch.compile for StableLM
- [#51826](https://github.com/vllm-project/vllm/pull/51826) torchcodec audio loader with selective audio backend

</details>

<details>
<summary>Parallelism & scheduling (8)</summary>

- [#47941](https://github.com/vllm-project/vllm/pull/47941) P2P NIXL + CPU EC connector
- [#52957](https://github.com/vllm-project/vllm/pull/52957) sync DP state on the first step of a wave
- [#54856](https://github.com/vllm-project/vllm/pull/54856) MRV2 spec decode: skip DP sync for uniform decodes
- [#54962](https://github.com/vllm-project/vllm/pull/54962) wait for previous PP tensor sends before the next forward
- [#55111](https://github.com/vllm-project/vllm/pull/55111) account for PCP in multi-node world-size validation
- [#54803](https://github.com/vllm-project/vllm/pull/54803) adjust_dcp_kv_cache_interleave_size for NixlConnector only
- [#54908](https://github.com/vllm-project/vllm/pull/54908) materialize prefill keys on non-owner DCP ranks
- [#54921](https://github.com/vllm-project/vllm/pull/54921) Fast Start

</details>

<details>
<summary>Hardware & arch (7)</summary>

- [#49410](https://github.com/vllm-project/vllm/pull/49410) native AMX-FP8 attention for Diamond Rapids CPU
- [#49209](https://github.com/vllm-project/vllm/pull/49209) batch-invariant matmul/linear kernels for XPU
- [#53678](https://github.com/vllm-project/vllm/pull/53678) fused GemmaRMSNorm path on XPU
- [#53037](https://github.com/vllm-project/vllm/pull/53037) fix device assignment for DP external LB on XPU
- [#52826](https://github.com/vllm-project/vllm/pull/52826) bump AITER to 0.1.21.post1
- [#54171](https://github.com/vllm-project/vllm/pull/54171) fix ROCm profiler hang from queue interposition
- [#55461](https://github.com/vllm-project/vllm/pull/55461) fall back to T1 when ARC cannot reclaim enough entries from T2

</details>

<details>
<summary>API & serving (17)</summary>

- [#54883](https://github.com/vllm-project/vllm/pull/54883) Rust frontend: report reasoning tokens in chat usage
- [#54837](https://github.com/vllm-project/vllm/pull/54837) Rust frontend: --lora-modules static adapter loading
- [#54999](https://github.com/vllm-project/vllm/pull/54999) Rust frontend: TLS in render server
- [#52755](https://github.com/vllm-project/vllm/pull/52755) Rust frontend: Mooncake/NIXL KV-connector metrics
- [#54659](https://github.com/vllm-project/vllm/pull/54659) expose multimodal metadata for disaggregated prefill
- [#54814](https://github.com/vllm-project/vllm/pull/54814) gRPC: preserve multimodal metadata for remote-prefill decode
- [#54579](https://github.com/vllm-project/vllm/pull/54579) gate scale-out endpoints behind an opt-in flag
- [#54557](https://github.com/vllm-project/vllm/pull/54557) overlap renderer warmup with engine core initialization
- [#54982](https://github.com/vllm-project/vllm/pull/54982) reasoning_token_count in reasoning parser
- [#45241](https://github.com/vllm-project/vllm/pull/45241) site-packages support for reasoning/tool parser plugins
- [#54285](https://github.com/vllm-project/vllm/pull/54285) warn on removed guided-decoding fields
- [#51886](https://github.com/vllm-project/vllm/pull/51886) retention interval for OffloadingConnector
- [#51381](https://github.com/vllm-project/vllm/pull/51381) echo session_id on GPU BlockStored events
- [#51444](https://github.com/vllm-project/vllm/pull/51444) validate cache salts before LMCache
- [#51445](https://github.com/vllm-project/vllm/pull/51445) server-generated keys for late-interaction query caches
- [#51898](https://github.com/vllm-project/vllm/pull/51898) validate scale-out multimodal data before engine handoff
- [#54935](https://github.com/vllm-project/vllm/pull/54935) cap GLMGA video sampling

</details>

<details>
<summary>Bugfixes (42)</summary>

- [#54325](https://github.com/vllm-project/vllm/pull/54325) populate SimpleCPUOffload BlockStored metadata
- [#53532](https://github.com/vllm-project/vllm/pull/53532) fix eager SimpleCPUOffload cache registration and final flush
- [#54362](https://github.com/vllm-project/vllm/pull/54362) fix SWA store reachability during chunked prefill
- [#52807](https://github.com/vllm-project/vllm/pull/52807) recurrent group's unhashed block no longer truncates the load boundary
- [#50883](https://github.com/vllm-project/vllm/pull/50883) scale UniformTypeKVCacheSpecs groups by DCP
- [#54872](https://github.com/vllm-project/vllm/pull/54872) ignore stale async lookup results
- [#55075](https://github.com/vllm-project/vllm/pull/55075) skip cleaned-up async lookup batches
- [#54288](https://github.com/vllm-project/vllm/pull/54288) stop offloading the final sampled token's KV slot
- [#54759](https://github.com/vllm-project/vllm/pull/54759) ensure tracker progress for oversized offers
- [#52923](https://github.com/vllm-project/vllm/pull/52923) wait for offload keys before storing chunks
- [#51667](https://github.com/vllm-project/vllm/pull/51667) fix cross-batch buffer race corrupting DiskBackend loads
- [#54878](https://github.com/vllm-project/vllm/pull/54878), [#54879](https://github.com/vllm-project/vllm/pull/54879) DecodeBenchConnector prefix selection and circular buffers
- [#54518](https://github.com/vllm-project/vllm/pull/54518) don't assert on a doubly cleaned-up failed NIXL transfer
- [#51690](https://github.com/vllm-project/vllm/pull/51690) look through UniformTypeKVCacheSpecs in the portability gate
- [#54854](https://github.com/vllm-project/vllm/pull/54854) DSV4 historical developer message handling
- [#54838](https://github.com/vllm-project/vllm/pull/54838) implicitly close DeepSeek DSML parameters
- [#54815](https://github.com/vllm-project/vllm/pull/54815) RoPE for deepseek-v4 sparse SWA layers
- [#45091](https://github.com/vllm-project/vllm/pull/45091) DeepSeek V4 FlashMLA auto KV cache dtype
- [#55299](https://github.com/vllm-project/vllm/pull/55299) seed the -1 sentinel in the DSv4 prefill sparse index workspace
- [#55042](https://github.com/vllm-project/vllm/pull/55042) DeepSeek-V4 registry platform guard
- [#55341](https://github.com/vllm-project/vllm/pull/55341) warm up kernels before capturing CUDA graphs on V2
- [#55455](https://github.com/vllm-project/vllm/pull/55455) defer adaptive verification until after kernel warmup
- [#54869](https://github.com/vllm-project/vllm/pull/54869) lazy-import FlashInfer PCIe IPC all-reduce in kernel_warmup
- [#54782](https://github.com/vllm-project/vllm/pull/54782) raise for unavailable piecewise CUDA graphs
- [#55234](https://github.com/vllm-project/vllm/pull/55234) restore DSpark cache-group capability under optimized Python
- [#54826](https://github.com/vllm-project/vllm/pull/54826) honour the draft's attention_backend on MRV2
- [#54374](https://github.com/vllm-project/vllm/pull/54374) drop FlashAttention AOT schedule for a sliding-window DFlash drafter
- [#55126](https://github.com/vllm-project/vllm/pull/55126) pad resumed speculative decode requests
- [#55245](https://github.com/vllm-project/vllm/pull/55245) spec decode warmup device selection
- [#55178](https://github.com/vllm-project/vllm/pull/55178) preserve Mamba state for padded prompt tails
- [#55375](https://github.com/vllm-project/vllm/pull/55375) state index strides in fused Qwen4Exp PLE conv
- [#55288](https://github.com/vllm-project/vllm/pull/55288) double BOS in LLM.chat() for multimodal models
- [#54994](https://github.com/vllm-project/vllm/pull/54994), [#54918](https://github.com/vllm-project/vllm/pull/54918), [#55448](https://github.com/vllm-project/vllm/pull/55448) multimodal cache and warmup fixes
- [#54886](https://github.com/vllm-project/vllm/pull/54886) reject tokenizer-less Qwen VL processor init
- [#54847](https://github.com/vllm-project/vllm/pull/54847) ColQwen3.5 pooler projector init
- [#53829](https://github.com/vllm-project/vllm/pull/53829) CohereASR streaming audio-token estimate
- [#49869](https://github.com/vllm-project/vllm/pull/49869) GLM-OCR MTP weight loading
- [#55083](https://github.com/vllm-project/vllm/pull/55083) retain vocab embeddings during replacement
- [#54913](https://github.com/vllm-project/vllm/pull/54913) launch render hanging on shutdown
- [#50254](https://github.com/vllm-project/vllm/pull/50254) finish VLLMValidationError migration in chat_utils
- [#54887](https://github.com/vllm-project/vllm/pull/54887) reject non-positive max concurrency

</details>

<details>
<summary>Refactors (4)</summary>

- [#54177](https://github.com/vllm-project/vllm/pull/54177) mypy typing fixes for L models
- [#54169](https://github.com/vllm-project/vllm/pull/54169) mypy typing fixes for P models
- [#55041](https://github.com/vllm-project/vllm/pull/55041) deprecate the "all" mamba cache mode
- [#54954](https://github.com/vllm-project/vllm/pull/54954) MoE kernels test cleanup

</details>

<details>
<summary>Tests (10)</summary>

- [#54893](https://github.com/vllm-project/vllm/pull/54893) MTP placeholder-token regression coverage
- [#54817](https://github.com/vllm-project/vllm/pull/54817) Kimi-K3-pruned75-DSpark-TP4 gsm8k eval
- [#54852](https://github.com/vllm-project/vllm/pull/54852) DSpark evals on ROCm
- [#53497](https://github.com/vllm-project/vllm/pull/53497) expert-parallelism coverage in external LB tests
- [#54379](https://github.com/vllm-project/vllm/pull/54379) avoid logging test server environment values
- [#54558](https://github.com/vllm-project/vllm/pull/54558) batch the swap_blocks verification
- [#54996](https://github.com/vllm-project/vllm/pull/54996) stabilize B12X linear kernel checks
- [#55315](https://github.com/vllm-project/vllm/pull/55315) split a top-k boundary-ties test to remove a Triton-specific assumption
- [#54957](https://github.com/vllm-project/vllm/pull/54957) FULL cudagraph mode for the Ernie4.5-VL ViT test
- plus 4 more minor test updates ([#55457](https://github.com/vllm-project/vllm/pull/55457), [#54984](https://github.com/vllm-project/vllm/pull/54984), [#54861](https://github.com/vllm-project/vllm/pull/54861), [#55266](https://github.com/vllm-project/vllm/pull/55266))

</details>

<details>
<summary>CI & build (36)</summary>

- [#54695](https://github.com/vllm-project/vllm/pull/54695), [#55308](https://github.com/vllm-project/vllm/pull/55308), [#55136](https://github.com/vllm-project/vllm/pull/55136), [#55011](https://github.com/vllm-project/vllm/pull/55011), [#55354](https://github.com/vllm-project/vllm/pull/55354) AMD timeout calibration and raises
- [#55014](https://github.com/vllm-project/vllm/pull/55014) build and publish TheRock nightly docker images
- [#55002](https://github.com/vllm-project/vllm/pull/55002), [#52650](https://github.com/vllm-project/vllm/pull/52650) mooncake in the ROCm image
- [#55246](https://github.com/vllm-project/vllm/pull/55246) bump ROCk base image
- [#55057](https://github.com/vllm-project/vllm/pull/55057) MiniMax reduce RMS kernel coverage on ROCm
- [#53399](https://github.com/vllm-project/vllm/pull/53399) MTP spec-decode acceptance coverage on ROCm
- [#54898](https://github.com/vllm-project/vllm/pull/54898) prefetch safetensors weights in AMD CI
- [#55410](https://github.com/vllm-project/vllm/pull/55410) restore Wikitext coverage for Qwen OCP-MX
- [#54751](https://github.com/vllm-project/vllm/pull/54751) shard CPU jobs above the 24h P90 threshold
- [#52350](https://github.com/vllm-project/vllm/pull/52350), [#52352](https://github.com/vllm-project/vllm/pull/52352), [#52344](https://github.com/vllm-project/vllm/pull/52344), [#54753](https://github.com/vllm-project/vllm/pull/54753) test sharding
- [#50314](https://github.com/vllm-project/vllm/pull/50314) Zen5 image build
- [#55317](https://github.com/vllm-project/vllm/pull/55317) fix flaky CPU CI image building
- [#53905](https://github.com/vllm-project/vllm/pull/53905) bump Transformers to 5.16.1
- [#54190](https://github.com/vllm-project/vllm/pull/54190) bump CUTLASS to v4.7.1
- [#55055](https://github.com/vllm-project/vllm/pull/55055)-class revert pair [#55026](https://github.com/vllm-project/vllm/pull/55026) and [#55392](https://github.com/vllm-project/vllm/pull/55392) for Nemotron Omni
- [#54991](https://github.com/vllm-project/vllm/pull/54991) revert flaky test_quark_int8_w8a8_moe
- plus 16 more minor CI updates ([#55409](https://github.com/vllm-project/vllm/pull/55409), [#50504](https://github.com/vllm-project/vllm/pull/50504), [#54895](https://github.com/vllm-project/vllm/pull/54895), [#54860](https://github.com/vllm-project/vllm/pull/54860), [#55349](https://github.com/vllm-project/vllm/pull/55349), [#55044](https://github.com/vllm-project/vllm/pull/55044), [#53762](https://github.com/vllm-project/vllm/pull/53762), [#55023](https://github.com/vllm-project/vllm/pull/55023), [#55094](https://github.com/vllm-project/vllm/pull/55094), [#54989](https://github.com/vllm-project/vllm/pull/54989), [#54863](https://github.com/vllm-project/vllm/pull/54863), [#53437](https://github.com/vllm-project/vllm/pull/53437), [#54171](https://github.com/vllm-project/vllm/pull/54171)-adjacent infra, [#55529](https://github.com/vllm-project/vllm/pull/55529), and others)

</details>

<details>
<summary>Docs (6)</summary>

- [#55019](https://github.com/vllm-project/vllm/pull/55019) Triton kernel-writing skill
- [#55028](https://github.com/vllm-project/vllm/pull/55028) expose the Triton skill to Claude
- [#54995](https://github.com/vllm-project/vllm/pull/54995) kernel benchmark sanity references
- [#54980](https://github.com/vllm-project/vllm/pull/54980) missing return annotations flagged by griffe
- [#54265](https://github.com/vllm-project/vllm/pull/54265) example for Renderer.render_cmpl()
- [#54944](https://github.com/vllm-project/vllm/pull/54944) official FunASR Nano vLLM checkpoint

</details>

<details>
<summary>Other (3)</summary>

- [#55271](https://github.com/vllm-project/vllm/pull/55271) note that enforce_eager also disables torch.compile
- [#55214](https://github.com/vllm-project/vllm/pull/55214) package glm5next nvidia subtree and fix its docstrings
- [#55054](https://github.com/vllm-project/vllm/pull/55054) optimize PLE MTP metadata transfers

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 2df74e793b67a31f0010b151711edcf7cf58e558a303f3b56cadb452e8795515 -->
