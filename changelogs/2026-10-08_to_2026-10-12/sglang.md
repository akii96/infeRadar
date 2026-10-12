# sglang: PR digest (2026-10-08 to 2026-10-12)

_325 merged, 406 newly opened - source sgl-project/sglang, generated 2026-10-12T00:57:17Z_

## TL;DR
- **DeepSeek (V4/V4.1) got the most attention**, then GLM-5.x and MiniMax (H3/M3), then Qwen3.8. Merged work: native block32 DeepGEMM on SM90 (`[#42604](https://github.com/sgl-project/sglang/pull/42604)`), a mxfp8 dispatch cache (`[#42156](https://github.com/sgl-project/sglang/pull/42156)`), MegaMoE with DP attention (`[#43228](https://github.com/sgl-project/sglang/pull/43228)`), mega-mHC (`[#42808](https://github.com/sgl-project/sglang/pull/42808)`) and Quark MXFP4 on AMD (`[#31054](https://github.com/sgl-project/sglang/pull/31054)`). Newly opened DSv4.1 work targets decoder/encoder SWA bounded replay, breakable prefill graphs and zigzag CP.
- **Perf work is spread across several areas.** MiniMax-H3 diffusion got fused QK-norm+RoPE (`[#43337](https://github.com/sgl-project/sglang/pull/43337)`, `[#43508](https://github.com/sgl-project/sglang/pull/43508)`), fused RMSNorm/AdaLN (`[#43327](https://github.com/sgl-project/sglang/pull/43327)`) and Ulysses exchange moved to the copy engine (`[#43164](https://github.com/sgl-project/sglang/pull/43164)`, `[#43361](https://github.com/sgl-project/sglang/pull/43361)`, `[#43521](https://github.com/sgl-project/sglang/pull/43521)`). Qwen3.8-Flash-Next BF16 decode on Blackwell was optimized (`[#42175](https://github.com/sgl-project/sglang/pull/42175)`), and KDA got FlashInfer prefill and MTP-verify rebalancing.
- **AMD opened a large wave of Kimi-K3 and Qwen3.8 kernel PRs** (the `[#43126](https://github.com/sgl-project/sglang/pull/43126)`-`[#43132](https://github.com/sgl-project/sglang/pull/43132)` series, `[#43481](https://github.com/sgl-project/sglang/pull/43481)`, `[#43516](https://github.com/sgl-project/sglang/pull/43516)`, `[#43558](https://github.com/sgl-project/sglang/pull/43558)`): FlyDSL persistent decode, FP8 MoE, MXFP4 GEMMs, MLA/KDA kernels, DeepSeek-V4.1 mono decode. All are still open.
- **Direction:** the unified-memory KV pool is being extended to speculative decoding, and DSpark/DFlash speculative decoding is being tightened. `sgl-router` is moving chat, completions and tool parsing onto `/generate` through `sglang-processor`. A large stage-boundary refactor underpins Kimi K3, while the diffusion side keeps adding models and dedups code.

## Most important PRs
**[#42753](https://github.com/sgl-project/sglang/pull/42753) – Translate each KV loc once per iteration.** Large refactor (97 files) that computes the KV location mapping once per iteration instead of per attention path. It is the groundwork for the unified-memory pool across FlashInfer, Triton, MLA and speculative decoding.

**[#37628](https://github.com/sgl-project/sglang/pull/37628) / [#37627](https://github.com/sgl-project/sglang/pull/37627) / [#40491](https://github.com/sgl-project/sglang/pull/40491) – Unified-memory pool for speculative decoding.** Fuses the draft model's KV into the target's page envelope and translates every spec read/write path. EAGLE/EAGLE3 are admitted on mamba-MHA and MLA hosts, and a related PR admits DFLASH/DSPARK.

**[#41887](https://github.com/sgl-project/sglang/pull/41887) – Blackwell dual GEMM fusion for MLP.** Adds a fused dual-GEMM path on Blackwell, a new kernel for dense MLPs.

**[#42604](https://github.com/sgl-project/sglang/pull/42604) – Native block32 DeepGEMM for DeepSeek-V4.1 on SM90.** Uses native block32 scaling on Hopper for V4.1, avoiding emulation. It lands together with the mxfp8 dispatch cache (`[#42156](https://github.com/sgl-project/sglang/pull/42156)`).

**[#43000](https://github.com/sgl-project/sglang/pull/43000) – Serve DeepSeek-V4.1 Flash through sglang-processor.** Part of the router series (`[#42996](https://github.com/sgl-project/sglang/pull/42996)`-`[#42999](https://github.com/sgl-project/sglang/pull/42999)`) that serves chat, completions and tool calls via `/generate` with shared reasoning parsing.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#42683](https://github.com/sgl-project/sglang/pull/42683) rebalance KDA MTP verify precompute and state sync
- [#43013](https://github.com/sgl-project/sglang/pull/43013) fuse short-conv checkpoint tracking metadata
- [#43227](https://github.com/sgl-project/sglang/pull/43227) avoid gate copies in gated RMSNorm
- [#39696](https://github.com/sgl-project/sglang/pull/39696) batch Mooncake hybrid-pool metadata and puts
- [#42238](https://github.com/sgl-project/sglang/pull/42238) reduce multi-detokenizer router IPC sends
- [#38959](https://github.com/sgl-project/sglang/pull/38959) reduce PP+PD bootstrap consensus latency
- [#42889](https://github.com/sgl-project/sglang/pull/42889) serialize OpenAI responses in one pass
- [#43602](https://github.com/sgl-project/sglang/pull/43602) keep the TP all-reduce inside the torch.compile graph for diffusion
- [#43117](https://github.com/sgl-project/sglang/pull/43117) decode plain base64 MiniMax-H3 materials without a per-character loop
- [#37662](https://github.com/sgl-project/sglang/pull/37662) FastH3 8-step, native Blackwell VSA, batched VAE decode
- [#41819](https://github.com/sgl-project/sglang/pull/41819) encode MP4 while VAE decodes
- [#43164](https://github.com/sgl-project/sglang/pull/43164) pipeline MiniMax-H3 Ulysses exchange over the copy engine
- [#43337](https://github.com/sgl-project/sglang/pull/43337) MiniMax-H3 QK-norm+RoPE two rows per warp
- [#43327](https://github.com/sgl-project/sglang/pull/43327) fuse MiniMax-H3 RMSNorm and indexed AdaLN

</details>

<details>
<summary>Kernels & attention (17)</summary>

- [#43361](https://github.com/sgl-project/sglang/pull/43361) move MiniMax-H3 pipelined Ulysses copies off the SMs
- [#43521](https://github.com/sgl-project/sglang/pull/43521) pipeline USPAttention Ulysses exchanges over the copy engine
- [#43508](https://github.com/sgl-project/sglang/pull/43508) head_dim-128 QK-norm+RoPE two rows per warp for all RoPE layouts
- [#42019](https://github.com/sgl-project/sglang/pull/42019) Gemma4 FA4 on SM90 with head-dim 512
- [#41400](https://github.com/sgl-project/sglang/pull/41400) integrate FlashInfer prefill checkpoints for KDA
- [#43246](https://github.com/sgl-project/sglang/pull/43246) default safe-gate Blackwell KDA prefill to FlashInfer
- [#42857](https://github.com/sgl-project/sglang/pull/42857) Helion MTP verification for KDA
- [#41105](https://github.com/sgl-project/sglang/pull/41105) capture GLM-5.3-Flash KDA extend in breakable prefill CUDA graphs
- [#41933](https://github.com/sgl-project/sglang/pull/41933) fuse QSA prefill KV gather and dtype conversion
- [#42957](https://github.com/sgl-project/sglang/pull/42957) TileLang FP8 KV cache for DSA on CUDA
- [#43332](https://github.com/sgl-project/sglang/pull/43332) fix GDN CuTe DSL decode state layout
- [#38615](https://github.com/sgl-project/sglang/pull/38615) MiniMax-M3 decode top-k in register buckets
- [#38841](https://github.com/sgl-project/sglang/pull/38841) MiniMax-M3 paged K/V tile loads and tiny router GEMM
- [#42614](https://github.com/sgl-project/sglang/pull/42614) MiniMax-M3 indexer CP packed scoring for EAGLE verify
- [#34537](https://github.com/sgl-project/sglang/pull/34537) AMD aiter asm for Kimi K3 target verify
- [#43346](https://github.com/sgl-project/sglang/pull/43346) sort only leading max(top_k) columns in the torch sampler
- [#42810](https://github.com/sgl-project/sglang/pull/42810) SwiGLU-OAI MXFP8 producer

</details>

<details>
<summary>MoE & quantization (11)</summary>

- [#39392](https://github.com/sgl-project/sglang/pull/39392) DSv4 R3 capture and MXFP4 online updates
- [#31054](https://github.com/sgl-project/sglang/pull/31054) Quark DeepSeek-V4-MXFP4 on AMD with shared-expert fusion and MTP
- [#39199](https://github.com/sgl-project/sglang/pull/39199) per-token NVFP4 MoE for ReLU2
- [#41072](https://github.com/sgl-project/sglang/pull/41072) skip post-experts EP all-reduce on FlashInfer cutlass FP4 path
- [#31768](https://github.com/sgl-project/sglang/pull/31768) LLaDA2.2 Block Routing MoE
- [#41133](https://github.com/sgl-project/sglang/pull/41133) AMD one-launch small-M MoE router for Qwen3.5
- [#41134](https://github.com/sgl-project/sglang/pull/41134) AMD small-M W8A8 FP8 GEMM for Qwen3.5 on gfx950
- [#41982](https://github.com/sgl-project/sglang/pull/41982) gfx950 small-batch MoE expert-count gate and FP8 block-scale kernel
- [#43188](https://github.com/sgl-project/sglang/pull/43188) bench: even round-robin simulated experts across EP ranks
- [#43062](https://github.com/sgl-project/sglang/pull/43062) ModelOpt FP8 quantization for Pi0.5
- [#42152](https://github.com/sgl-project/sglang/pull/42152) AMD drop static input_scale on aiter per-token FP8

</details>

<details>
<summary>Model support (16)</summary>

- [#36311](https://github.com/sgl-project/sglang/pull/36311) HunyuanImage-3.0-Instruct
- [#42941](https://github.com/sgl-project/sglang/pull/42941) Wan-Animate-2
- [#37907](https://github.com/sgl-project/sglang/pull/37907) LLaDA-Image BF16 generation and editing
- [#41492](https://github.com/sgl-project/sglang/pull/41492) SANA-Video 2.0
- [#42721](https://github.com/sgl-project/sglang/pull/42721) Clef and Clef-Flash on /v1/systemone
- [#42782](https://github.com/sgl-project/sglang/pull/42782) EmbeddingGemma 2
- [#42645](https://github.com/sgl-project/sglang/pull/42645) pplx-decider-v1.1
- [#43391](https://github.com/sgl-project/sglang/pull/43391) Qwen-Image 2.1 Turbo
- [#31773](https://github.com/sgl-project/sglang/pull/31773) dLLM JointThresholdInDel decoding
- [#43228](https://github.com/sgl-project/sglang/pull/43228) DP attention with MegaMoE for DSv4.1
- [#42808](https://github.com/sgl-project/sglang/pull/42808) mega-mHC for DSv4.1
- [#42044](https://github.com/sgl-project/sglang/pull/42044) GLM-5.3-Flash prefill CP on layer boundaries
- [#39723](https://github.com/sgl-project/sglang/pull/39723) Qwen3.8 collocated prefill CP
- [#43012](https://github.com/sgl-project/sglang/pull/43012) block verification for the DFlash family
- [#43478](https://github.com/sgl-project/sglang/pull/43478) DSv4.1 DSPARK TP and DP EP accuracy coverage
- [#43165](https://github.com/sgl-project/sglang/pull/43165) init full-to-SWA mapping for request-window pools in DSv4.1

</details>

<details>
<summary>Parallelism & scheduling (22)</summary>

- [#40102](https://github.com/sgl-project/sglang/pull/40102) kv-shard Control Plane C
- [#43177](https://github.com/sgl-project/sglang/pull/43177) overlap scheduler startup with DP controller
- [#43180](https://github.com/sgl-project/sglang/pull/43180) metrics for per-rank DP attention pairs and imbalance
- [#43283](https://github.com/sgl-project/sglang/pull/43283) keep DP-converted decode batch as running batch
- [#42720](https://github.com/sgl-project/sglang/pull/42720) skip decode when last token already in flight
- [#43290](https://github.com/sgl-project/sglang/pull/43290) hold back decode rows that do not fit the KV pool
- [#43298](https://github.com/sgl-project/sglang/pull/43298) requeue preempted requests when admission admits nothing
- [#41593](https://github.com/sgl-project/sglang/pull/41593) refresh waiting requests' cached prefixes under FCFS-like policies
- [#43444](https://github.com/sgl-project/sglang/pull/43444) fix deterministic-inference hang for short prefill chunks
- [#43029](https://github.com/sgl-project/sglang/pull/43029) use committed length in spec mamba track boundary check
- [#43567](https://github.com/sgl-project/sglang/pull/43567) invalidate lazy Mamba checkpoints before in-place tracking
- [#43442](https://github.com/sgl-project/sglang/pull/43442) reclaim parked optimistic prefills when slots run out
- [#43410](https://github.com/sgl-project/sglang/pull/43410) receive decode KV into separate paged SWA host pools (PD)
- [#43562](https://github.com/sgl-project/sglang/pull/43562) fold decode restore outcome into MIN-reduced KV poll
- [#43329](https://github.com/sgl-project/sglang/pull/43329) harden PPConsensusStore wire format
- [#43211](https://github.com/sgl-project/sglang/pull/43211) unblock CUDA graph startup for hybrid parallelism
- [#43303](https://github.com/sgl-project/sglang/pull/43303) size DP-local decode graphs by runner gather requirement
- [#43206](https://github.com/sgl-project/sglang/pull/43206) unified pool: allocate without transfer waits, pin SWA reservations
- [#42455](https://github.com/sgl-project/sglang/pull/42455) publish LoRA adapter names in KV events
- [#43198](https://github.com/sgl-project/sglang/pull/43198) serve disabled pure-SWA models with PureSWARadixCache
- [#43200](https://github.com/sgl-project/sglang/pull/43200) serve disabled hybrid-SWA models with UnifiedRadixCache
- [#43185](https://github.com/sgl-project/sglang/pull/43185) count reclaimable tokens in unified tree ledgers

</details>

<details>
<summary>Hardware & arch (8)</summary>

- [#35594](https://github.com/sgl-project/sglang/pull/35594) thread vendor KV pool classes through builders; PlatformCapabilities
- [#41030](https://github.com/sgl-project/sglang/pull/41030) eliminate remaining gfx95 FP8 scale relayout copies
- [#42982](https://github.com/sgl-project/sglang/pull/42982) saturate FP8 KV commits on AMD instead of e4m3fnuz NaN overflow
- [#39840](https://github.com/sgl-project/sglang/pull/39840) AMD per-batch-size graph capture fix
- [#43292](https://github.com/sgl-project/sglang/pull/43292) MLX sync decode KV once at release
- [#43282](https://github.com/sgl-project/sglang/pull/43282) MLX drain in-flight jobs before retract-mode pause
- [#40404](https://github.com/sgl-project/sglang/pull/40404) NPU cudagraph runner unit tests
- [#41857](https://github.com/sgl-project/sglang/pull/41857) split Intel XPU nightly into kernel-main and kernel-wheel jobs

</details>

<details>
<summary>API & serving (13)</summary>

- [#42998](https://github.com/sgl-project/sglang/pull/42998) /v1/chat/completions through /generate with reasoning parsing
- [#42999](https://github.com/sgl-project/sglang/pull/42999) parse tool calls when chat goes through /generate
- [#42997](https://github.com/sgl-project/sglang/pull/42997) /v1/completions through /generate
- [#42996](https://github.com/sgl-project/sglang/pull/42996) share reasoning splitter and tool constraint across hosts
- [#42664](https://github.com/sgl-project/sglang/pull/42664) rust-processor DeepSeek-V4 parity harness
- [#42665](https://github.com/sgl-project/sglang/pull/42665) render DeepSeek-V4 through sglang-processor
- [#42989](https://github.com/sgl-project/sglang/pull/42989) preserve PD routing in chat and completions
- [#43233](https://github.com/sgl-project/sglang/pull/43233) read finished /generate streams to the end
- [#41259](https://github.com/sgl-project/sglang/pull/41259) parallelize long chat prompt encoding
- [#40453](https://github.com/sgl-project/sglang/pull/40453) InstantTensor loader support
- [#43004](https://github.com/sgl-project/sglang/pull/43004) warm up each rust listener in-process
- [#43143](https://github.com/sgl-project/sglang/pull/43143) pass media fps hint to multimodal processors
- [#43084](https://github.com/sgl-project/sglang/pull/43084) don't report deleted video jobs as completed

</details>

<details>
<summary>Refactors (17)</summary>

- [#43460](https://github.com/sgl-project/sglang/pull/43460) declare model stages from a shared function
- [#43459](https://github.com/sgl-project/sglang/pull/43459) declare pipeline neighbours from a shared function
- [#43457](https://github.com/sgl-project/sglang/pull/43457) bind a layer stack in one pass per stage
- [#43455](https://github.com/sgl-project/sglang/pull/43455) explicit checked residual read/update capabilities
- [#43458](https://github.com/sgl-project/sglang/pull/43458) decide exit's fixed facts at stage build
- [#43456](https://github.com/sgl-project/sglang/pull/43456) decide input-scattered eligibility in one place
- [#43453](https://github.com/sgl-project/sglang/pull/43453) record bound stage path behavior
- [#42898](https://github.com/sgl-project/sglang/pull/42898) Kimi K3 fused collectives through stage boundaries
- [#42936](https://github.com/sgl-project/sglang/pull/42936) remove Kimi K3's own layer communication
- [#42894](https://github.com/sgl-project/sglang/pull/42894) run Kimi K3 through stage boundaries
- [#42897](https://github.com/sgl-project/sglang/pull/42897) attention-TP dense FFNs and unpadded batches on stage boundaries
- [#42287](https://github.com/sgl-project/sglang/pull/42287) TCPCG retire backend selection (3/9)
- [#42286](https://github.com/sgl-project/sglang/pull/42286) TCPCG bind live batches in BCG eager calls (2/9)
- [#42923](https://github.com/sgl-project/sglang/pull/42923) match_prefix returns only matched length
- [#43023](https://github.com/sgl-project/sglang/pull/43023) init_load_back returns only loaded length
- [#43201](https://github.com/sgl-project/sglang/pull/43201) delete ChunkCache
- [#41452](https://github.com/sgl-project/sglang/pull/41452) anchored lock receipt for non-root releases

</details>

<details>
<summary>Bugfixes (15)</summary>

- [#43454](https://github.com/sgl-project/sglang/pull/43454) keep residual rows and sums consistent across appends and handoffs
- [#42892](https://github.com/sgl-project/sglang/pull/42892) return FFN output to attention rows at pipeline handoff
- [#42896](https://github.com/sgl-project/sglang/pull/42896) run attention on a padded extend batch's real rows
- [#42895](https://github.com/sgl-project/sglang/pull/42895) shard Kimi K3 shared experts over the right TP group
- [#42891](https://github.com/sgl-project/sglang/pull/42891) merge DSV4 TBO microbatches without a residual
- [#43475](https://github.com/sgl-project/sglang/pull/43475) repair multimodal VMM lease cleanup
- [#43633](https://github.com/sgl-project/sglang/pull/43633) replay Qwen-Image-2.1 BCG graphs across prompt lengths
- [#38671](https://github.com/sgl-project/sglang/pull/38671) MiniMax H3 honors requested step count
- [#43385](https://github.com/sgl-project/sglang/pull/43385) keep LoRA unmerged under merge_mode auto when rounding loses the update
- [#42422](https://github.com/sgl-project/sglang/pull/42422) TeaCache CFG state lifecycle
- [#41706](https://github.com/sgl-project/sglang/pull/41706) CFG per-sample norm
- [#23772](https://github.com/sgl-project/sglang/pull/23772) Z-Image CFG combine formula
- [#40765](https://github.com/sgl-project/sglang/pull/40765) wait for multimodal process teardown
- [#35721](https://github.com/sgl-project/sglang/pull/35721) health checks no longer perturb DP routing
- [#43690](https://github.com/sgl-project/sglang/pull/43690) select VSA-H3 for FastH3 by default

</details>

<details>
<summary>Tests (8)</summary>

- [#43081](https://github.com/sgl-project/sglang/pull/43081) remove unregistered chunked-prefill tests under test/manual
- [#43195](https://github.com/sgl-project/sglang/pull/43195) clean unnecessary DSV4 tests
- [#43470](https://github.com/sgl-project/sglang/pull/43470) remove GLM-5.3-Flash PTX KDA prefill nightly
- [#42986](https://github.com/sgl-project/sglang/pull/42986) rebase LTX H100 timing references
- [#43229](https://github.com/sgl-project/sglang/pull/43229) avoid HF Hub API calls when local cache is complete
- [#38520](https://github.com/sgl-project/sglang/pull/38520) docs drift check for server_arguments.mdx
- [#42860](https://github.com/sgl-project/sglang/pull/42860) dedup Qwen-VL inputs and accuracy suites
- [#43568](https://github.com/sgl-project/sglang/pull/43568) BCG warns instead of disabling on unvalidated models

</details>

<details>
<summary>CI & build (4)</summary>

- [#43503](https://github.com/sgl-project/sglang/pull/43503) drop low-signal CPU tests; Rust workspace tests in own workflow
- [#43022](https://github.com/sgl-project/sglang/pull/43022) dedicated sglang-processor workflow
- [#42807](https://github.com/sgl-project/sglang/pull/42807) upgrade sglang-radix-tree to PyO3 0.29
- [#42666](https://github.com/sgl-project/sglang/pull/42666) update Dynamo frontend crates

</details>

<details>
<summary>Docs (5)</summary>

- [#42726](https://github.com/sgl-project/sglang/pull/42726) AgentX cookbook for GLM-5.2, DSV4, DSV4.1
- [#43083](https://github.com/sgl-project/sglang/pull/43083) AgentX cookbook for Qwen3.5 / Qwen3.8-Flash-Next
- [#43472](https://github.com/sgl-project/sglang/pull/43472) standardize diffusion cookbook command builders
- [#43380](https://github.com/sgl-project/sglang/pull/43380) Wan-Animate-2 cookbook picker
- [#43235](https://github.com/sgl-project/sglang/pull/43235) Clef cookbook

</details>

<details>
<summary>Other (many diffusion refactors and minor items)</summary>

- [#43064](https://github.com/sgl-project/sglang/pull/43064) remove unused diffusion helpers and write-only state
- [#42841](https://github.com/sgl-project/sglang/pull/42841) share KL VAE encode/decode and tiling
- [#42843](https://github.com/sgl-project/sglang/pull/42843) dedup Qwen Image RoPE and SenseNova backbones
- [#42899](https://github.com/sgl-project/sglang/pull/42899) dedup UniPC solvers and Gemma3 shard loading
- [#42848](https://github.com/sgl-project/sglang/pull/42848) share sigma schedules and causal cross-attention
- [#42856](https://github.com/sgl-project/sglang/pull/42856) share ModelOpt checkpoint conversion I/O
- [#43495](https://github.com/sgl-project/sglang/pull/43495) ComfyUI fails early instead of dropping features in SGLD mode
- [#43492](https://github.com/sgl-project/sglang/pull/43492) ComfyUI executor conditioning-cache fixes
- [#43490](https://github.com/sgl-project/sglang/pull/43490) ComfyUI FluxAdapter fixes
- [#43656](https://github.com/sgl-project/sglang/pull/43656) LTX video/audio through shared bounded MP4 path
- [#43501](https://github.com/sgl-project/sglang/pull/43501) dynamic LoRA delta inside the second GEMM
- [#42854](https://github.com/sgl-project/sglang/pull/42854) distributed weight updates for diffusion
- [#39606](https://github.com/sgl-project/sglang/pull/39606) HiCache staged write-back for page-unified KV layout
- [#43174](https://github.com/sgl-project/sglang/pull/43174) HiCache re-admit split node's queued write
- [#41591](https://github.com/sgl-project/sglang/pull/41591) hybrid MLA/KDA DCP with file and Mooncake HiCache L3
- [#43596](https://github.com/sgl-project/sglang/pull/43596) build Mamba host pools from device buffer infos
- [#43595](https://github.com/sgl-project/sglang/pull/43595) share MLA host capacity initialization
- [#43620](https://github.com/sgl-project/sglang/pull/43620) DSpark single step interface for markov heads
- [#43621](https://github.com/sgl-project/sglang/pull/43621) DSpark MarkovSampleStep
- [#43622](https://github.com/sgl-project/sglang/pull/43622) DSpark eager markov block via MarkovSampleStep
- [#43668](https://github.com/sgl-project/sglang/pull/43668) DSpark same markov block in draft graph tail
- [#43670](https://github.com/sgl-project/sglang/pull/43670) DSpark greedy draft option
- [#43301](https://github.com/sgl-project/sglang/pull/43301) chunk and cache audio items spanning placeholder runs
- [#43159](https://github.com/sgl-project/sglang/pull/43159) Qwen3.8 GB300 long-context recipe
- [#41601](https://github.com/sgl-project/sglang/pull/41601) thinking budget guide
- [#43176](https://github.com/sgl-project/sglang/pull/43176) share prefill graph output buffer across shapes
- plus ~40 more minor diffusion, test-dedup and ComfyUI changes

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 961b00b364a757bced79dfbdd1526800ec5f49a9f79de361326dc176df68fd97 -->
