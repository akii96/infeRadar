# sglang: PR digest (2026-09-02 to 2026-09-06)

_290 merged, 428 newly opened - source sgl-project/sglang, generated 2026-09-06T23:15:10Z_

## TL;DR
- **Model focus:** DeepSeek (V4 on AMD/SM120), GLM-5.3-Flash and MiniMax-H3 diffusion got the most label attention. Kimi-K3 and Qwen3.x GDN/KDA kernels also got steady work.
- **Biggest perf work:** KDA NVFP4 and FP8 skinny GEMMs on SM120 (`[#36865](https://github.com/sgl-project/sglang/pull/36865)`, `[#38082](https://github.com/sgl-project/sglang/pull/38082)`), Kimi-K3 ROCm KDA decode fusion and Triton MLA prefill on gfx950 (`[#34198](https://github.com/sgl-project/sglang/pull/34198)`, `[#35770](https://github.com/sgl-project/sglang/pull/35770)`), and the DeepSeek-V4 FP4 indexer on AMD (`[#37353](https://github.com/sgl-project/sglang/pull/37353)`, `[#37764](https://github.com/sgl-project/sglang/pull/37764)`, `[#37423](https://github.com/sgl-project/sglang/pull/37423)`, `[#37658](https://github.com/sgl-project/sglang/pull/37658)`).
- **GLM-5.3-Flash landed, then was trimmed:** the main PR merged, but follow-ups removed context-parallel and experimental DSA pieces. Many stacked GLM and Qwen-Next PRs are still open.
- **Direction:** unified-memory and SWA allocator consolidation, a more capable Router with load-aware and bucket-aware policies, and ongoing diffusion work (MiniMax-H3 sparse attention, residency planning). Open PRs show heavy investment in HiCache, speculative decoding on unified pools, and a big config refactor.

## Most important PRs
**`[#36507](https://github.com/sgl-project/sglang/pull/36507)` GLM-5.3-Flash support**
Adds the model with its DSA/MLA attention, MoE, and speculative-decode paths, plus multi-hardware wiring. The kernels were split out as `[#37477](https://github.com/sgl-project/sglang/pull/37477)`. Later PRs stripped the CP and optional-backend pieces to keep the merge reviewable.

**`[#36865](https://github.com/sgl-project/sglang/pull/36865)` KDA NVFP4 GEMM for Qwen3.x on SM120**
Adds an NVFP4 GEMM for the KDA linear-attention projections on consumer Blackwell. `[#38082](https://github.com/sgl-project/sglang/pull/38082)` adds an FP8 skinny GEMM for the same hardware.

**`[#34198](https://github.com/sgl-project/sglang/pull/34198)` Kimi-K3 fused ROCm KDA decode boundary**
Fuses ops at the KDA decode boundary on ROCm to cut launch overhead. It pairs with the gfx950 Triton MLA prefill optimization in `[#35770](https://github.com/sgl-project/sglang/pull/35770)`.

**`[#37353](https://github.com/sgl-project/sglang/pull/37353)` FP4 indexer for DeepSeek V4 on AMD**
Enables the FP4 DSA indexer on ROCm and shrinks indexer memory and bandwidth. Follow-ups fuse the prefill-schedule preamble (`[#37764](https://github.com/sgl-project/sglang/pull/37764)`), move oproj_a to fp8 (`[#37423](https://github.com/sgl-project/sglang/pull/37423)`), and fuse inverse-RoPE into the fp8 wo_a quant (`[#37658](https://github.com/sgl-project/sglang/pull/37658)`).

**`[#38108](https://github.com/sgl-project/sglang/pull/38108)` Router bucket-aware policy domains and native cache indexing**
Adds bucket-aware routing domains with native cache indexing. It builds on `[#37731](https://github.com/sgl-project/sglang/pull/37731)` (composable scoring and eligibility) and `[#37843](https://github.com/sgl-project/sglang/pull/37843)` (load-aware prefill admission).

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#37622](https://github.com/sgl-project/sglang/pull/37622) fuses gating and short convolution for LFM2 on SM90
- [#36267](https://github.com/sgl-project/sglang/pull/36267) optimizes Qwen3.5 GDN prefill projection layouts
- [#36970](https://github.com/sgl-project/sglang/pull/36970) selects ReplaySSM verify loop unrolling by shape
- [#35544](https://github.com/sgl-project/sglang/pull/35544) amortizes GDN ReplaySSM checkpoint materialization
- [#33838](https://github.com/sgl-project/sglang/pull/33838) Kimi-K3 MoE optimization on AMD
- [#37938](https://github.com/sgl-project/sglang/pull/37938) vectorizes alloc_extend_naive, removing the per-request Python loop
- [#37324](https://github.com/sgl-project/sglang/pull/37324) walks the radix tree by offset instead of re-slicing token storage
- [#37330](https://github.com/sgl-project/sglang/pull/37330) reduces tokenizer overhead and offloads CUDA VMM publication
- [#37512](https://github.com/sgl-project/sglang/pull/37512) builds the unified read stream directly, without the page-table rectangle
- [#37511](https://github.com/sgl-project/sglang/pull/37511) sizes the unified read-table grid from bs and fuses tombstone scatters
- [#36723](https://github.com/sgl-project/sglang/pull/36723) makes free_swa sync-free at page_size 1
- [#35546](https://github.com/sgl-project/sglang/pull/35546) prunes EAGLE draft-extend logits to selected rows
- [#31755](https://github.com/sgl-project/sglang/pull/31755) reduces reserved GPU memory in requant_weight_ue8m0
- [#38038](https://github.com/sgl-project/sglang/pull/38038) reuses output storage across full prefill CUDA graphs

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#37477](https://github.com/sgl-project/sglang/pull/37477) GLM-5.3-Flash kernels ported from `[#36507](https://github.com/sgl-project/sglang/pull/36507)`
- [#37591](https://github.com/sgl-project/sglang/pull/37591) makes the ROCm DSA indexer top-k exact with cooperative selection
- [#38152](https://github.com/sgl-project/sglang/pull/38152) supports NoPE layers in the tokenspeed_mla FP8 prefill hook
- [#37693](https://github.com/sgl-project/sglang/pull/37693) supports decode context parallelism for the trtllm_mla family on unified memory
- [#34893](https://github.com/sgl-project/sglang/pull/34893) MiniMax H3 cube sparse attention for diffusion
- [#37480](https://github.com/sgl-project/sglang/pull/37480) FastH3 with a VSA-H3 attention backend
- [#37332](https://github.com/sgl-project/sglang/pull/37332) SM120 support for SubBlock sparse attention
- [#37959](https://github.com/sgl-project/sglang/pull/37959) request-scoped Skip Softmax attention for diffusion
- [#37437](https://github.com/sgl-project/sglang/pull/37437) SpargeAttention backend
- [#36735](https://github.com/sgl-project/sglang/pull/36735) key masks on USPAttention's replicated-prefix path
- [#38044](https://github.com/sgl-project/sglang/pull/38044) fuses LingBot MoE group-limited top-k selection
- [#37910](https://github.com/sgl-project/sglang/pull/37910) fuses LingBot gated residual and RMSNorm modulate
- [#38042](https://github.com/sgl-project/sglang/pull/38042) Helios per-token gated-residual fusion
- [#37096](https://github.com/sgl-project/sglang/pull/37096) fuses FLUX.2 NVFP4 FC1, SwiGLU and FC2 quantization
- [#38020](https://github.com/sgl-project/sglang/pull/38020) ports Wan VAE decoder fast paths to the Qwen-Image VAE
- [#33911](https://github.com/sgl-project/sglang/pull/33911) generalizes the persistent CuTe JIT cache

</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#37629](https://github.com/sgl-project/sglang/pull/37629) enables FP8 and Quark MXFP4 MoE on gfx950 for GLM-5.3-Flash
- [#37880](https://github.com/sgl-project/sglang/pull/37880) reverts [#37629](https://github.com/sgl-project/sglang/pull/37629)
- [#34874](https://github.com/sgl-project/sglang/pull/34874) MXFP4 experts for Kimi K3 on the DeepGEMM runner in symmetric memory
- [#32405](https://github.com/sgl-project/sglang/pull/32405) migrates SM100 trtllm-gen mxfp4 MoE onto MoeRunner
- [#37552](https://github.com/sgl-project/sglang/pull/37552) quantization refactor: removes dead code and dedups FP4 marlin helpers
- [#36380](https://github.com/sgl-project/sglang/pull/36380) Cosmos3 fp8 mixed precision
- [#38033](https://github.com/sgl-project/sglang/pull/38033) K2 Horizon FP8 checkpoint support
- [#37489](https://github.com/sgl-project/sglang/pull/37489) preserves FP32 in the SM107 MXFP8 fallback
- [#35751](https://github.com/sgl-project/sglang/pull/35751) GPT-OSS MXFP4 checkpoints on Intel XPU

</details>

<details>
<summary>Model support (11)</summary>

- [#36805](https://github.com/sgl-project/sglang/pull/36805) Hy4-preview
- [#37654](https://github.com/sgl-project/sglang/pull/37654) native IFM K2 Horizon serving
- [#37667](https://github.com/sgl-project/sglang/pull/37667) native UNO speculative decoding serving
- [#32151](https://github.com/sgl-project/sglang/pull/32151) Nanbeige4.2
- [#33572](https://github.com/sgl-project/sglang/pull/33572) Cosmos3 Reasoner for LLM-only inference
- [#37068](https://github.com/sgl-project/sglang/pull/37068) file-backed PLE table backend for Qwen4-Exp on unified-memory devices
- [#38121](https://github.com/sgl-project/sglang/pull/38121) loads Qwen3.8-Flash-Next-NVFP4 (ModelOpt MIXED_PRECISION)
- [#37480](https://github.com/sgl-project/sglang/pull/37480) FastH3 (4-step VSA-distilled MiniMax-H3)
- [#37266](https://github.com/sgl-project/sglang/pull/37266) MiniMax-H3 tiered AdaLN plan cache
- [#37945](https://github.com/sgl-project/sglang/pull/37945) MiniMax-H3 warmup at the served clip shape
- [#37825](https://github.com/sgl-project/sglang/pull/37825) K2 Horizon MoE without MoVA

</details>

<details>
<summary>Parallelism & scheduling (22)</summary>

- [#37674](https://github.com/sgl-project/sglang/pull/37674) extracts PP dynamic chunk sizing into DynamicChunkSizer
- [#37669](https://github.com/sgl-project/sglang/pull/37669) applies the attention-CP broadcast result in PP dynamic-chunk profiling
- [#37675](https://github.com/sgl-project/sglang/pull/37675) broadcasts PP dynamic-chunk profiling failures so all ranks disable together
- [#37546](https://github.com/sgl-project/sglang/pull/37546) makes attention-TP sequence sharding a per-forward batch property
- [#36223](https://github.com/sgl-project/sglang/pull/36223) makes strategy prefill CP canonical (CP V1 deprecation 2/5)
- [#37484](https://github.com/sgl-project/sglang/pull/37484) temporarily removes GLM-5.3 Flash prefill CP
- [#37487](https://github.com/sgl-project/sglang/pull/37487) temporarily removes GLM-5.3 Flash decode CP
- [#38060](https://github.com/sgl-project/sglang/pull/38060) removes remaining GLM-5.3 CP additions
- [#38078](https://github.com/sgl-project/sglang/pull/38078) gathers CP-sharded tokens before TP-sharded dense MLP under prefill CP
- [#37274](https://github.com/sgl-project/sglang/pull/37274) allows a custom policy for adaptive speculative decoding
- [#36403](https://github.com/sgl-project/sglang/pull/36403) speculative decoding with unified SWA memory
- [#34565](https://github.com/sgl-project/sglang/pull/34565) SWA branching-point caching in the unified tree
- [#37424](https://github.com/sgl-project/sglang/pull/37424) HiCache buffer mode supports sidecar pool
- [#37503](https://github.com/sgl-project/sglang/pull/37503) HiCache L3 prefetch lifecycle metrics
- [#37578](https://github.com/sgl-project/sglang/pull/37578) UMBP external linker (Unified Cache 6/N)
- [#37381](https://github.com/sgl-project/sglang/pull/37381) external linker mode end to end (Unified Cache 5/N)
- [#37636](https://github.com/sgl-project/sglang/pull/37636) exports scheduler stage wall time
- [#37461](https://github.com/sgl-project/sglang/pull/37461) rolling scheduler utilization counters
- [#38139](https://github.com/sgl-project/sglang/pull/38139) Router publishes cache-aware load state
- [#36384](https://github.com/sgl-project/sglang/pull/36384) streamed LoRA weight updates for sglang-miles
- [#37502](https://github.com/sgl-project/sglang/pull/37502) counts the parked chunked-prefill request in the busy memory check
- [#37888](https://github.com/sgl-project/sglang/pull/37888) coordinates FullCG prefix variants across DP ranks

</details>

<details>
<summary>Hardware & arch (10)</summary>

- [#32733](https://github.com/sgl-project/sglang/pull/32733) CPU FP8 KV cache
- [#36349](https://github.com/sgl-project/sglang/pull/36349) migrates FlyDSL fused norm kernels to the v0.3.0 API (AMD diffusion)
- [#37720](https://github.com/sgl-project/sglang/pull/37720) stages large pageable H2D copies instead of pinning them in ROCm
- [#37118](https://github.com/sgl-project/sglang/pull/37118) defines DSA head-gate graph helpers on HIP
- [#37193](https://github.com/sgl-project/sglang/pull/37193) weekly XPU simple model enablement
- [#37230](https://github.com/sgl-project/sglang/pull/37230) enables the nightly-xpu-8-gpu suite
- [#37340](https://github.com/sgl-project/sglang/pull/37340) Intel XPU regular Docker image release workflow
- [#35176](https://github.com/sgl-project/sglang/pull/35176) fuses the KDA input projection into a single GEMM on ROCm
- [#38112](https://github.com/sgl-project/sglang/pull/38112) fixes failing NPU PR-test cases
- [#37760](https://github.com/sgl-project/sglang/pull/37760) fixes Kimi-K2.6 and dsv4-flash NPU CI cases

</details>

<details>
<summary>API & serving (7)</summary>

- [#38108](https://github.com/sgl-project/sglang/pull/38108) see above
- [#34488](https://github.com/sgl-project/sglang/pull/34488) adds response-level input/output token ids to chat completions
- [#36630](https://github.com/sgl-project/sglang/pull/36630) captures masks from sampler support
- [#37327](https://github.com/sgl-project/sglang/pull/37327) aligns the Rust server launcher and request validation
- [#37967](https://github.com/sgl-project/sglang/pull/37967) bounds Rust multimodal media ingress
- [#34660](https://github.com/sgl-project/sglang/pull/34660) refactors mm code for the Rust tokenizer manager
- [#37469](https://github.com/sgl-project/sglang/pull/37469) real-traffic replay in bench_one_batch_server

</details>

<details>
<summary>Bugfixes (28)</summary>

- [#36944](https://github.com/sgl-project/sglang/pull/36944) contains EPD request lifecycle failures
- [#36945](https://github.com/sgl-project/sglang/pull/36945) hardens EPD receiver validation and liveness
- [#36949](https://github.com/sgl-project/sglang/pull/36949) makes EPD cache publication transactional
- [#36988](https://github.com/sgl-project/sglang/pull/36988) retires aborted disaggregated prefill results
- [#37320](https://github.com/sgl-project/sglang/pull/37320) fixes alpha-channel images and tool-result media ordering
- [#37836](https://github.com/sgl-project/sglang/pull/37836) fixes mamba radix cache SSM state indexing
- [#37505](https://github.com/sgl-project/sglang/pull/37505) fixes the DP attention decode-to-extend prefix off-by-one
- [#37853](https://github.com/sgl-project/sglang/pull/37853) cherry-pick of [#37505](https://github.com/sgl-project/sglang/pull/37505) to v0.5.19
- [#37560](https://github.com/sgl-project/sglang/pull/37560) fixes unified SWA v2p sizing for non-owners
- [#37278](https://github.com/sgl-project/sglang/pull/37278) aligns write-through pending across tree cores
- [#35255](https://github.com/sgl-project/sglang/pull/35255) fixes abort handling after client disconnect
- [#37965](https://github.com/sgl-project/sglang/pull/37965) preserves mapped courier tensor lifetime
- [#37971](https://github.com/sgl-project/sglang/pull/37971) disambiguates mixed GLM4V image and video offsets
- [#38039](https://github.com/sgl-project/sglang/pull/38039) unifies the causal_conv1d dtype for MiniCPM-V-4.6 GDN prefill
- [#38079](https://github.com/sgl-project/sglang/pull/38079) fixes GLM-5.3 DFlash graph counts and startup DeepGEMM budget
- [#37660](https://github.com/sgl-project/sglang/pull/37660) fixes FP4 indexer OOR on AMD
- [#37858](https://github.com/sgl-project/sglang/pull/37858) caps the DSA MQA-logits budget at AITER's limit (cherry-pick)
- [#30315](https://github.com/sgl-project/sglang/pull/30315) fixes AMD DSV4 unified-KV pool sizing
- [#38163](https://github.com/sgl-project/sglang/pull/38163) reverts [#30315](https://github.com/sgl-project/sglang/pull/30315)
- [#36407](https://github.com/sgl-project/sglang/pull/36407) fixes native MoE handling of noncontiguous top-k IDs
- [#37199](https://github.com/sgl-project/sglang/pull/37199) avoids duplicate MoE reduction for gpt-oss with DP attention
- [#37471](https://github.com/sgl-project/sglang/pull/37471) loads the Qwen3.5 MTP embedding under PP
- [#37510](https://github.com/sgl-project/sglang/pull/37510) fixes Muse Glimmer ModelOpt mixed weight mapping
- [#37494](https://github.com/sgl-project/sglang/pull/37494) skips an absent radix lock during cache cleanup
- [#37567](https://github.com/sgl-project/sglang/pull/37567) fixes buffer-mode idle tracking and VLM memory sizing
- [#34424](https://github.com/sgl-project/sglang/pull/34424) fixes ROCm VAE Conv2D fast path with spatial-parallel decode
- [#34187](https://github.com/sgl-project/sglang/pull/34187) reworks the Kimi K3 skipped-think fix as opt-in
- [#36320](https://github.com/sgl-project/sglang/pull/36320) fixes MiniMax H3 WebUI inference settings

</details>

<details>
<summary>Refactors (13)</summary>

- [#38072](https://github.com/sgl-project/sglang/pull/38072) moves unified-memory allocators into allocator/
- [#37729](https://github.com/sgl-project/sglang/pull/37729) requires page-aligned starts in free_segment
- [#37876](https://github.com/sgl-project/sglang/pull/37876) routes hybrid SWA full-side kv-row frees through free_segment
- [#37481](https://github.com/sgl-project/sglang/pull/37481) splits duplicate insert frees at the SWA eviction floor
- [#36646](https://github.com/sgl-project/sglang/pull/36646) resolves SWA ownership at enqueue time
- [#37550](https://github.com/sgl-project/sglang/pull/37550) converges the two SWA predicates
- [#37854](https://github.com/sgl-project/sglang/pull/37854) cherry-pick of [#37550](https://github.com/sgl-project/sglang/pull/37550)
- [#37206](https://github.com/sgl-project/sglang/pull/37206) drops the in-tree MNNVL CuTe DSL port for FlashInfer 0.6.18
- [#37795](https://github.com/sgl-project/sglang/pull/37795) lets eviction policies take construction parameters
- [#38128](https://github.com/sgl-project/sglang/pull/38128) consolidates plain state-dict diffusion loaders
- [#36824](https://github.com/sgl-project/sglang/pull/36824) removes diffusion component loader capability switches
- [#37616](https://github.com/sgl-project/sglang/pull/37616) filters duplicate precision variants across custom loaders
- [#37816](https://github.com/sgl-project/sglang/pull/37816) composes third-party component bundles safely

</details>

<details>
<summary>Tests (6)</summary>

- [#38093](https://github.com/sgl-project/sglang/pull/38093) prunes redundant unified-memory allocator and pool tests
- [#37990](https://github.com/sgl-project/sglang/pull/37990) removes obsolete NPU PR nightly cases
- [#38172](https://github.com/sgl-project/sglang/pull/38172) guards allocated VRAM peak in diffusion CI
- [#37915](https://github.com/sgl-project/sglang/pull/37915) makes diffusion nightly performance measurements robust
- [#37872](https://github.com/sgl-project/sglang/pull/37872) fixes UNO test adapter subdirectory resolution
- [#38076](https://github.com/sgl-project/sglang/pull/38076) adds H200 serving recipe E2E coverage for GLM-5.3

</details>

<details>
<summary>CI & build (14)</summary>

- [#37210](https://github.com/sgl-project/sglang/pull/37210) replaces black-jupyter with ruff-format (touches 1411 files)
- [#37881](https://github.com/sgl-project/sglang/pull/37881) Lark notifications for CUDA CI status and queue time
- [#37884](https://github.com/sgl-project/sglang/pull/37884) improves the Lark CI cards
- [#37618](https://github.com/sgl-project/sglang/pull/37618) adds /rerun-test --changed
- [#37504](https://github.com/sgl-project/sglang/pull/37504) installs sgl-eval from PyPI
- [#37258](https://github.com/sgl-project/sglang/pull/37258) builds Rust extensions on hosted runners in parallel
- [#37820](https://github.com/sgl-project/sglang/pull/37820) builds Rust extensions for aarch64
- [#37696](https://github.com/sgl-project/sglang/pull/37696) pins the Rust TreeCore build to the resolved libtorch
- [#37647](https://github.com/sgl-project/sglang/pull/37647) authenticates and retries git clones in install scripts
- [#37864](https://github.com/sgl-project/sglang/pull/37864) cherry-pick of [#37647](https://github.com/sgl-project/sglang/pull/37647)
- [#37865](https://github.com/sgl-project/sglang/pull/37865) cherry-pick of [#37485](https://github.com/sgl-project/sglang/pull/37485)
- [#37485](https://github.com/sgl-project/sglang/pull/37485) graceful teardown for PD and HiSparse fixtures
- [#37395](https://github.com/sgl-project/sglang/pull/37395) renames Xeon CPU CI suites
- plus 3 more minor CI and NPU pipeline updates ([#38011](https://github.com/sgl-project/sglang/pull/38011), [#35489](https://github.com/sgl-project/sglang/pull/35489), [#37665](https://github.com/sgl-project/sglang/pull/37665))

</details>

<details>
<summary>Docs (14)</summary>

- [#36987](https://github.com/sgl-project/sglang/pull/36987) replaces the stale diffusion compatibility matrix
- [#37655](https://github.com/sgl-project/sglang/pull/37655) K2 Horizon cookbook recipes and H200 results
- [#37576](https://github.com/sgl-project/sglang/pull/37576) GLM-5.3-Flash cookbook speed data
- [#37878](https://github.com/sgl-project/sglang/pull/37878) Kimi-K3 B300 speed numbers
- [#37829](https://github.com/sgl-project/sglang/pull/37829) AMD V4 cookbook update
- [#37781](https://github.com/sgl-project/sglang/pull/37781) AMD Kimi-K3 cookbook update
- [#37737](https://github.com/sgl-project/sglang/pull/37737) DeepSeek-V4 DGX Spark cookbook
- [#37492](https://github.com/sgl-project/sglang/pull/37492) verifies DeepSeek-V4 Flash Vision on GB300
- [#38026](https://github.com/sgl-project/sglang/pull/38026) DeepSeek-V4 Pro B200 FP4 HiCache DSpark
- [#37723](https://github.com/sgl-project/sglang/pull/37723) K2 Horizon MoE model names
- [#37750](https://github.com/sgl-project/sglang/pull/37750) TPU model list refresh
- [#35674](https://github.com/sgl-project/sglang/pull/35674) diffusion layerwise-offload streaming guide
- [#37456](https://github.com/sgl-project/sglang/pull/37456) verifies the DGX Spark H3 recipe
- [#32172](https://github.com/sgl-project/sglang/pull/32172) clarifies OpenAI chat template defaults

</details>

<details>
<summary>Other (14)</summary>

- [#33824](https://github.com/sgl-project/sglang/pull/33824) CPU-based inference simulator
- [#37916](https://github.com/sgl-project/sglang/pull/37916) diffusion warmup memory measurement (1/4)
- [#38071](https://github.com/sgl-project/sglang/pull/38071) removes experimental GLM-5.3 DSA metadata optimizations
- [#38061](https://github.com/sgl-project/sglang/pull/38061) extracts KPool-specific DSA backend helpers
- [#38058](https://github.com/sgl-project/sglang/pull/38058) drops optional FlashAttention and FlashInfer MLA changes for GLM-5.3
- [#38057](https://github.com/sgl-project/sglang/pull/38057) removes GLM-5.3 serving lifecycle changes
- [#29927](https://github.com/sgl-project/sglang/pull/29927) SM120 DeepSeek-V4 DeepGEMM paged-MQA indexer, FP4 MoE and page-split
- [#37285](https://github.com/sgl-project/sglang/pull/37285) pins host-cache size via mmap and cudaHostRegister
- [#37890](https://github.com/sgl-project/sglang/pull/37890) improves BCG warmup frame-count diagnostics
- [#37804](https://github.com/sgl-project/sglang/pull/37804) reduces diffusion hot-path log noise
- [#37422](https://github.com/sgl-project/sglang/pull/37422) cumulative extra-high quality tier for diffusion
- [#35922](https://github.com/sgl-project/sglang/pull/35922) adds profiler spans for diffusion request phases
- [#37855](https://github.com/sgl-project/sglang/pull/37855) gates the aiter memory-reserve exemption behind an env var
- [#37737](https://github.com/sgl-project/sglang/pull/37737) plus about 90 more merged PRs not shown in the data

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f11bbb8f9e097409f68d362a95f575a3f1d7d38df34b414c59ef1106d6ce7948 -->
