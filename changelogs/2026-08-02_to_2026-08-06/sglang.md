# sglang: PR digest (2026-08-02 to 2026-08-06)

_243 merged, 332 newly opened - source sgl-project/sglang, generated 2026-08-06T11:45:21Z_

## TL;DR
- **DeepSeek, MiniMax, and GLM** saw the most attention, alongside major new model integrations like **Kimi-K3** ([#32541](https://github.com/sgl-project/sglang/pull/32541)), **MiniMax-H3** ([#33275](https://github.com/sgl-project/sglang/pull/33275)), and **Ling-3.0-flash** (in progress [#33561](https://github.com/sgl-project/sglang/pull/33561)).
- **Performance & Kernels**: Significant work landed for FlashInfer (GDN MTP verify [#33102](https://github.com/sgl-project/sglang/pull/33102), RMSNorm+quant fusion [#32994](https://github.com/sgl-project/sglang/pull/32994)), DeepGEMM MoE dispatch ([#33128](https://github.com/sgl-project/sglang/pull/33128)), and AMD ROCm optimizations (DWDP weight backends [#33310](https://github.com/sgl-project/sglang/pull/33310)).
- **Architecture & Serving**: The Rust server is gaining major capabilities, including OpenAI API support ([#33103](https://github.com/sgl-project/sglang/pull/33103)), native multimodal processing for Qwen VL ([#32365](https://github.com/sgl-project/sglang/pull/32365)), and PD disaggregation ([#33125](https://github.com/sgl-project/sglang/pull/33125)).
- **Speculative Decoding & Caching**: Expanded support for MTP/EAGLE/DSpark with HiCache ([#30393](https://github.com/sgl-project/sglang/pull/30393)), DCP + HiCache L2 support ([#33112](https://github.com/sgl-project/sglang/pull/33112)), and a new Decode-Verify-Rollback mechanism in progress ([#33291](https://github.com/sgl-project/sglang/pull/33291)).
- **Overall Direction**: The engine is heavily investing in multimodal/diffusion pipelines, Rust-based serving infrastructure, and advanced speculative decoding strategies across diverse hardware (NVIDIA, AMD, NPU, Intel XPU).

## Most important PRs
- **[#33275](https://github.com/sgl-project/sglang/pull/33275)** and **[#32541](https://github.com/sgl-project/sglang/pull/32541)**: Merged massive support for the MiniMax-H3 diffusion model and Kimi-K3, bringing extensive attention, MoE, and quantization kernel updates across multiple backends.
- **[#33103](https://github.com/sgl-project/sglang/pull/33103)**: Implements OpenAI APIs in the new Rust-based `sglang` server, marking a major step toward a high-performance, native serving frontend.
- **[#33102](https://github.com/sgl-project/sglang/pull/33102)**: Fuses ReplaySSM ring write into the FlashInfer GDN MTP verify kernel, significantly optimizing speculative decoding verification for state-space models.
- **[#33291](https://github.com/sgl-project/sglang/pull/33291)**: (In-progress) Introduces Decode-Verify-Rollback for deterministic speculative decoding with GDN, overhauling the speculative execution pipeline.
- **[#33829](https://github.com/sgl-project/sglang/pull/33829)**: (In-progress) Adds comprehensive support for `dots.note.omni`, including native encoders, video preprocessing, and MTP decoding.

## More changes by area

<details>
<summary>Performance (10)</summary>

- [#33349](https://github.com/sgl-project/sglang/pull/33349) Speed up the Kimi-K2.5 vision path and match PIL bicubic in the GPU resize
- [#33307](https://github.com/sgl-project/sglang/pull/33307) Broadcast single-image DP vision embedding instead of pad-to-max all-gather
- [#33063](https://github.com/sgl-project/sglang/pull/33063) Stop allocating per-layer scratch inside the decode CUDA graph for TRT-LLM MHA
- [#33839](https://github.com/sgl-project/sglang/pull/33839) Avoid temporary extend state copies in Mamba/GDN backend on AMD
- [#33387](https://github.com/sgl-project/sglang/pull/33387) Fuse compressed metadata initialization for DeepSeek-V4 speculative decoding
- [#33236](https://github.com/sgl-project/sglang/pull/33236) Remove prefill CP KV and compressor materialization for DeepSeek-V4
- [#33293](https://github.com/sgl-project/sglang/pull/33293) Fuse GraniteMoe scaled residual RMSNorm
- [#33484](https://github.com/sgl-project/sglang/pull/33484) Fuse the DeepSeek-V4 value and scale swap-in copy on ROCm
- [#33838](https://github.com/sgl-project/sglang/pull/33838) Optimize Kimi-K3 MoE performance on AMD
- [#33595](https://github.com/sgl-project/sglang/pull/33595) Measure prefill busy time between launches

</details>

<details>
<summary>Kernels & attention (35)</summary>

- [#33443](https://github.com/sgl-project/sglang/pull/33443) Clean up and split DSA indexer
- [#33205](https://github.com/sgl-project/sglang/pull/33205) Unify BaseFusedOp and MultiPlatformOp dispatch
- [#28609](https://github.com/sgl-project/sglang/pull/28609) Facade DSA index-cache: MTP topk-reuse state + index-K storage
- [#33451](https://github.com/sgl-project/sglang/pull/33451) Add FLUX.2 VAE decoder fast path behind quality=high
- [#33587](https://github.com/sgl-project/sglang/pull/33587) Align WAR fences with CUDA graph metadata reads
- [#33546](https://github.com/sgl-project/sglang/pull/33546) Fuse Wan VAE RMSNorm+SiLU behind quality=high
- [#30298](https://github.com/sgl-project/sglang/pull/30298) Add Laguna per-layer LoRA hidden-dim resolution for packed attention
- [#33536](https://github.com/sgl-project/sglang/pull/33536) Fuse DiT FFN tanh-GELU into up-proj GEMM
- [#33136](https://github.com/sgl-project/sglang/pull/33136) Support breakable CUDA graphs for zigzag strategy
- [#33599](https://github.com/sgl-project/sglang/pull/33599) Fuse Kimi-K3 attn-residual aggregation on AMD
- [#32320](https://github.com/sgl-project/sglang/pull/32320) Only split touched SWA pages in FlashMLA page-split kernel
- [#33667](https://github.com/sgl-project/sglang/pull/33667) Pack Ulysses Q/K/V input all-to-all into one collective + reusable a2a staging buffers
- [#33655](https://github.com/sgl-project/sglang/pull/33655) Prefer cuDNN SDPA over FA4 for dense attention on sm_100 (B200)
- [#33137](https://github.com/sgl-project/sglang/pull/33137) Fuse zigzag attention into a single call
- [#33537](https://github.com/sgl-project/sglang/pull/33537) Fix multiple flexibility issues for DP attention
- [#33363](https://github.com/sgl-project/sglang/pull/33363) Unify MLA scaling init and remove dead buffer / scaling code
- [#33575](https://github.com/sgl-project/sglang/pull/33575) Rebuild the shared RoPE cache entry when its buffers are dead
- [#31477](https://github.com/sgl-project/sglang/pull/31477) Enable fused TopK for GLM-5.2 MTP IndexShare
- [#33703](https://github.com/sgl-project/sglang/pull/33703) Add SageAttention packed varlen path for MiniMax-H3
- [#33734](https://github.com/sgl-project/sglang/pull/33734) Add ERNIE-Image bit-exact residual-gate fast path
- [#33479](https://github.com/sgl-project/sglang/pull/33479) Put the DSA cuda-graph page table in the pausable memory region
- [#33427](https://github.com/sgl-project/sglang/pull/33427) Enable post-capture KV sizing with DP attention
- [#32589](https://github.com/sgl-project/sglang/pull/32589) Hoist mamba track-mask host syncs out of the per-layer prefill path for Nemotron
- [#33306](https://github.com/sgl-project/sglang/pull/33306) Avoid TRTLLM prefill output copy
- [#33617](https://github.com/sgl-project/sglang/pull/33617) Enable CuTe DSL BF16 GEMM on SM107
- [#33364](https://github.com/sgl-project/sglang/pull/33364) Add symm_a2a single-node symmetric-memory A2A backend for MLA decode
- [#33856](https://github.com/sgl-project/sglang/pull/33856) Add a unified post-hoc sparsity framework with StreamingLLM visibility
- [#33647](https://github.com/sgl-project/sglang/pull/33647) Add FlashInfer CAKE prefill and decode backends
- [#33444](https://github.com/sgl-project/sglang/pull/33444) Fuse aux hidden state capture and support DFLASH with breakable/full prefill CUDA graphs
- [#33576](https://github.com/sgl-project/sglang/pull/33576) Add Work-Centric (Lean) Attention persistent-CTA decode kernel for long-context serving
- [#33418](https://github.com/sgl-project/sglang/pull/33418) Optimize MLA for Kimi K3 on AMD
- [#33226](https://github.com/sgl-project/sglang/pull/33226) Add FlashInfer prefill context parallelism
- [#33400](https://github.com/sgl-project/sglang/pull/33400) Move JIT kernels into namespace sglang
- [#33315](https://github.com/sgl-project/sglang/pull/33315) Support batchable guest forwards over pinned prefix KV in session context forward
- [#33288](https://github.com/sgl-project/sglang/pull/33288) Bound C4 indexer logits peak memory via varlen routing query-axis chunking for DeepSeek-V4
- plus 25 more kernel and attention updates

</details>

<details>
<summary>MoE & quantization (15)</summary>

- [#32994](https://github.com/sgl-project/sglang/pull/32994) Add flashinfer rmsnorm + quant fusion support SM90, SM100, SM120
- [#33128](https://github.com/sgl-project/sglang/pull/33128) Support DeepGEMM for standard MoE dispatch
- [#33474](https://github.com/sgl-project/sglang/pull/33474) Select DeepGEMM standard layouts by memory budget
- [#33469](https://github.com/sgl-project/sglang/pull/33469) Add scalar scale A support for fp8_gemm
- [#32538](https://github.com/sgl-project/sglang/pull/32538) Support ModelOpt MXFP8 checkpoints
- [#33108](https://github.com/sgl-project/sglang/pull/33108) Add inkling-small MoE support for sm_121
- [#33148](https://github.com/sgl-project/sglang/pull/33148) Route per-tensor FP8 checkpoints to FlashInfer on SM90
- [#33618](https://github.com/sgl-project/sglang/pull/33618) Enable MoE deferred finalize by default and drop its expert_weights dtype workaround
- [#33310](https://github.com/sgl-project/sglang/pull/33310) Add ROCm DWDP weight backends
- [#33561](https://github.com/sgl-project/sglang/pull/33561) Support Ling-3.0-flash (BailingMoeV3)
- [#33249](https://github.com/sgl-project/sglang/pull/33249) Add BF16 PoC integration for Kimi-K3 MoonEP
- [#33571](https://github.com/sgl-project/sglang/pull/33571) Add FlashInfer MegaMOE zero-copy adapter path
- [#33684](https://github.com/sgl-project/sglang/pull/33684) Support static DP/EP layouts in weight cache
- [#33559](https://github.com/sgl-project/sglang/pull/33559) Add triton moe TMA up support
- [#33278](https://github.com/sgl-project/sglang/pull/33278) Support MXFP8 dense Marlin W8A16 on SM80/SM90

</details>

<details>
<summary>Model support (15)</summary>

- [#33140](https://github.com/sgl-project/sglang/pull/33140) Add official DSV4 reasoning effort support
- [#30683](https://github.com/sgl-project/sglang/pull/30683) Batch GLM-Image AR requests
- [#33378](https://github.com/sgl-project/sglang/pull/33378) Add GLM Image usage report
- [#30883](https://github.com/sgl-project/sglang/pull/30883) Add qknorm_rope support for Flux on XPU
- [#27110](https://github.com/sgl-project/sglang/pull/27110) Add Nemotron support on sglang-miles
- [#32046](https://github.com/sgl-project/sglang/pull/32046) Integrate Qwen3.5 gfx950 fmha fp8 hd256 on AMD
- [#33386](https://github.com/sgl-project/sglang/pull/33386) Add Boogu-Image reference-image edit (TI2I / I2I) pipeline
- [#33572](https://github.com/sgl-project/sglang/pull/33572) Add cosmos3 Reasoner to llm only inference
- [#33465](https://github.com/sgl-project/sglang/pull/33465) Support Kimi-K3 on NPU
- [#33554](https://github.com/sgl-project/sglang/pull/33554) Add Nemotron 3.5 Support
- [#33691](https://github.com/sgl-project/sglang/pull/33691) Support Intern-S2-Mobius
- [#33648](https://github.com/sgl-project/sglang/pull/33648) Add K-EXAONE-2.0-750B-A37B support
- [#33673](https://github.com/sgl-project/sglang/pull/33673) Add MiniMax-M3 DSpark support
- [#33681](https://github.com/sgl-project/sglang/pull/33681) Support FP8 Qwen3-VL text encoder for MiniMax-H3
- [#33569](https://github.com/sgl-project/sglang/pull/33569) Support MiniMax H3 on Ascend NPU's

</details>

<details>
<summary>Parallelism & scheduling (25)</summary>

- [#29173](https://github.com/sgl-project/sglang/pull/29173) Add Session-reference-aware Unified Radix Cache for agentic multi-turn workloads
- [#30177](https://github.com/sgl-project/sglang/pull/30177) Support return_hidden_states="last"
- [#32415](https://github.com/sgl-project/sglang/pull/32415) Split multimodal scheduling from mm_utils
- [#30393](https://github.com/sgl-project/sglang/pull/30393) Support packed and sidecar draft caches for MTP/EAGLE/DSpark in HiCache
- [#32588](https://github.com/sgl-project/sglang/pull/32588) Add generation request semantics to gRPC
- [#33725](https://github.com/sgl-project/sglang/pull/33725) Add data-parallel serving (--dp-size) for diffusion
- [#33112](https://github.com/sgl-project/sglang/pull/33112) Add DCP + HiCache L2 Support (ported from kimi-k3)
- [#33298](https://github.com/sgl-project/sglang/pull/33298) Support sampling in the DSPARK graph-folded draft proposal
- [#33299](https://github.com/sgl-project/sglang/pull/33299) Redesign multi-LoRA
- [#33775](https://github.com/sgl-project/sglang/pull/33775) Add capture-safe pynccl all-to-all for diffusion
- [#33138](https://github.com/sgl-project/sglang/pull/33138) Implement random tie breadking for cache_aware sglang router policy
- [#32880](https://github.com/sgl-project/sglang/pull/32880) Bound prefill delayer all-branch delay and decay the max_prefill_bs high-watermark
- [#33403](https://github.com/sgl-project/sglang/pull/33403) Honor explicit min-free-slots thresholds in scheduler
- [#33105](https://github.com/sgl-project/sglang/pull/33105) Support dp attn with client lb
- [#33448](https://github.com/sgl-project/sglang/pull/33448) Bound a request by the aggregate KV pool, not one rank's share in DCP
- [#33133](https://github.com/sgl-project/sglang/pull/33133) Add a queues.prealloc_ready counter to the load snapshot
- [#33545](https://github.com/sgl-project/sglang/pull/33545) Allow optimistic prefill with L2 hierarchical cache and write-back policy
- [#33406](https://github.com/sgl-project/sglang/pull/33406) Support multimodal streaming sessions
- [#33295](https://github.com/sgl-project/sglang/pull/33295) Add ECHO for EAGLE3
- [#33651](https://github.com/sgl-project/sglang/pull/33651) Add Unified KV Cache Layout in L3
- [#33729](https://github.com/sgl-project/sglang/pull/33729) Expose multi-choice generation streams in gRPC
- [#33812](https://github.com/sgl-project/sglang/pull/33812) Add rust server pd lb
- [#33767](https://github.com/sgl-project/sglang/pull/33767) Support Kimi-K3 DCP decode offload to Mooncake L3
- [#33863](https://github.com/sgl-project/sglang/pull/33863) Support PP + PD + DSpark
- [#33676](https://github.com/sgl-project/sglang/pull/33676) Support DeepSeek-V4 DSpark speculative decoding on NPU
- plus 15 more parallelism and scheduling updates

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#31948](https://github.com/sgl-project/sglang/pull/31948) Enable automatic ascend_attn selection for vision attention and graph runners on NPU
- [#28267](https://github.com/sgl-project/sglang/pull/28267) Add causal conv1d on NPU
- [#29027](https://github.com/sgl-project/sglang/pull/29027) Add a fast layernorm for diffusion models and fix BSA on NPU
- [#28040](https://github.com/sgl-project/sglang/pull/28040) Use sgl-kernel implementation of fused_k_norm_rope_flashmla on Intel XPU for DeepSeek V4
- [#33804](https://github.com/sgl-project/sglang/pull/33804) Enable chunked prefill scnearios for Intel XPU

</details>

<details>
<summary>API & serving (15)</summary>

- [#32364](https://github.com/sgl-project/sglang/pull/32364) Add server vision pipeline core (fetch/driver/pipeline) + Qwen VL to sglang-mm
- [#32365](https://github.com/sgl-project/sglang/pull/32365) Integrate native multimodal processing for Qwen VL in rust-server
- [#33125](https://github.com/sgl-project/sglang/pull/33125) Add PD disaggregation support to rust-server
- [#31491](https://github.com/sgl-project/sglang/pull/31491) Add Spectrum multimodal controls
- [#33375](https://github.com/sgl-project/sglang/pull/33375) Add startup, memory, and hybrid SWA diagnostics
- [#33243](https://github.com/sgl-project/sglang/pull/33243) Forward per-request attribution headers on the cache-sim /ingest_ids tee
- [#33548](https://github.com/sgl-project/sglang/pull/33548) Report accelerator count in /v1/loads
- [#33337](https://github.com/sgl-project/sglang/pull/33337) Publish the generated forward-pass-metrics endpoint to the bags
- [#33370](https://github.com/sgl-project/sglang/pull/33370) Add component-aware Redis KV indexer and experimental Router integration
- [#33425](https://github.com/sgl-project/sglang/pull/33425) Add rust sglang server OpenAI Response APIs
- [#33733](https://github.com/sgl-project/sglang/pull/33733) Support SelfLift progressive resolution in diffusion pipeline
- [#33401](https://github.com/sgl-project/sglang/pull/33401) Support gated launch to defer startup memory allocation
- [#33585](https://github.com/sgl-project/sglang/pull/33585) Add unit tests for realtime transcription session
- [#33640](https://github.com/sgl-project/sglang/pull/33640) Support logprobs in /v1/responses non-streaming path
- [#33606](https://github.com/sgl-project/sglang/pull/33606) Accept OpenAI's input_audio content part in chat completions

</details>

<details>
<summary>Tests, CI & build (15)</summary>

- [#32392](https://github.com/sgl-project/sglang/pull/32392) Add NPU PR test cases
- [#33346](https://github.com/sgl-project/sglang/pull/33346) Migrate NPU PR/nightly test cases to a3-560T
- [#31500](https://github.com/sgl-project/sglang/pull/31500) Add DSV4 wide-EP16 4-node 2P1D nightly recipes on AMD
- [#33615](https://github.com/sgl-project/sglang/pull/33615) Route GEMM backend UTs through real layer modules and weight loaders
- [#33756](https://github.com/sgl-project/sglang/pull/33756) Collapse the EAGLE launch matrix and the scoring engine boots on the per-commit runners
- [#33596](https://github.com/sgl-project/sglang/pull/33596) Replace GEMM backend e2e matrices with layer-level unit tests
- [#33333](https://github.com/sgl-project/sglang/pull/33333) Add Kimi-K2.6 MXFP4 wide-EP16 2P1D nightly recipes on AMD
- [#33832](https://github.com/sgl-project/sglang/pull/33832) Remove profiling from nightly tests
- [#33745](https://github.com/sgl-project/sglang/pull/33745) Fold duplicate-server suites and prune the retract matrix on 1-gpu-5090
- [#33498](https://github.com/sgl-project/sglang/pull/33498) Build and release sgl-deep-ep wheels
- [#33384](https://github.com/sgl-project/sglang/pull/33384) Build the Rust extension modules once per run instead of in every CUDA job
- [#33641](https://github.com/sgl-project/sglang/pull/33641) Merge tokenizer worker tests and drop redundant triton attention e2e
- [#33611](https://github.com/sgl-project/sglang/pull/33611) Replace NVFP4 MoE runner backend e2e matrix with a layer-level unit test
- [#33281](https://github.com/sgl-project/sglang/pull/33281) Add MiniMax-H3 2-GPU consistency coverage
- [#33824](https://github.com/sgl-project/sglang/pull/33824) Add high-fidelity CPU-based inference simulator
- plus 45 more minor CI updates

</details>

<details>
<summary>Docs (10)</summary>

- [#33556](https://github.com/sgl-project/sglang/pull/33556) Add Ling-3.0-flash cookbook
- [#33282](https://github.com/sgl-project/sglang/pull/33282) Update skills for MiniMax-H3
- [#33453](https://github.com/sgl-project/sglang/pull/33453) Restrict request-level quality to two validated tiers: lossless (default) and high
- [#32123](https://github.com/sgl-project/sglang/pull/32123) Rename docs_new/ to docs/
- [#24370](https://github.com/sgl-project/sglang/pull/24370) Add cuda graph profile traces to Profiling Enhancements
- [#33712](https://github.com/sgl-project/sglang/pull/33712) Add HiCache + Mooncake cells for Ling-3.0-flash
- [#33580](https://github.com/sgl-project/sglang/pull/33580) Complete the tree-core interface boundary for Unified Radix Cache
- [#33347](https://github.com/sgl-project/sglang/pull/33347) Refresh README news highlights
- [#33860](https://github.com/sgl-project/sglang/pull/33860) Add Community Configs section for contributed recipes
- [#33398](https://github.com/sgl-project/sglang/pull/33398) Add measured H200 Ulysses4 vs TP2+Ulysses2 topology data for MiniMax-H3

</details>

<details>
<summary>Bugfixes (15)</summary>

- [#33367](https://github.com/sgl-project/sglang/pull/33367) Fix pi05 models not applying scale factor for language embeddings
- [#33308](https://github.com/sgl-project/sglang/pull/33308) Drop deprecated multimodal processor residency state
- [#33317](https://github.com/sgl-project/sglang/pull/33317) Fix component accuracy topology reuse in diffusion
- [#31901](https://github.com/sgl-project/sglang/pull/31901) Fix DeepSeek V4 HiSparse PD Transfers with Separate Host and Device KV Indices
- [#33509](https://github.com/sgl-project/sglang/pull/33509) Resolve VLM test image placeholders from the model's own chat template
- [#33214](https://github.com/sgl-project/sglang/pull/33214) Fix DeepSeek-OCR batching crash on variable local-crop counts
- [#31727](https://github.com/sgl-project/sglang/pull/31727) Fix DeepSeek-V4 fused-RMS FP8 scale metadata on gfx950
- [#30206](https://github.com/sgl-project/sglang/pull/30206) Capture legal multi-request prefill CUDA graph batches
- [#33365](https://github.com/sgl-project/sglang/pull/33365) Fix local-path detection for MiniMax-H3 and other non-diffusers models
- [#33428](https://github.com/sgl-project/sglang/pull/33428) Reduce startup log noise and fix Dynamo / CUDA-graph edge cases
- [#33123](https://github.com/sgl-project/sglang/pull/33123) Fix broken Nemotron DP attention
- [#33562](https://github.com/sgl-project/sglang/pull/33562) Clear forward occupancy on idle in metrics
- [#33065](https://github.com/sgl-project/sglang/pull/33065) Honor FlashMLA natural-log LSE in DCP reduction
- [#33478](https://github.com/sgl-project/sglang/pull/33478) Fix NextN weight loading by sharing the unified-loader mappings
- [#33862](https://github.com/sgl-project/sglang/pull/33862) Reclaim redundant host mirrors after storage backup in HiCache
- plus 65 more minor bugfixes

</details>

<details>
<summary>Refactors (10)</summary>

- [#33490](https://github.com/sgl-project/sglang/pull/33490) Retire ServerArgs.override in favour of derive()
- [#33491](https://github.com/sgl-project/sglang/pull/33491) Resolve the draft worker's config per runner, not on a copy
- [#33336](https://github.com/sgl-project/sglang/pull/33336) Keep runtime hicache and weight-version updates off ServerArgs
- [#33338](https://github.com/sgl-project/sglang/pull/33338) Retire the last process-global config field reads
- [#33335](https://github.com/sgl-project/sglang/pull/33335) Build every draft worker from a draft ServerArgs copy
- [#33492](https://github.com/sgl-project/sglang/pull/33492) Make the draft runner carry its own attention backend
- [#33334](https://github.com/sgl-project/sglang/pull/33334) Stop writing config onto the published ServerArgs at three sites
- [#33488](https://github.com/sgl-project/sglang/pull/33488) Retire the alias-form process-global config reads
- [#33489](https://github.com/sgl-project/sglang/pull/33489) Move template-detected parsers to the engine's control-plane overlay
- [#33487](https://github.com/sgl-project/sglang/pull/33487) Pass the Ray placement group as a launch argument
- plus 7 more minor refactors

</details>

<details>
<summary>Other (10)</summary>

- [#33752](https://github.com/sgl-project/sglang/pull/33752) Re-enable a pruned Inkling LoRA unit-test set
- [#33120](https://github.com/sgl-project/sglang/pull/33120) Warn on risky serving-time Triton work
- [#32952](https://github.com/sgl-project/sglang/pull/32952) Drop redundant per-kernel arch overrides in JIT
- [#32434](https://github.com/sgl-project/sglang/pull/32434) Consolidate compiled-kernel caches under SGLANG_CACHE_DIR
- [#33613](https://github.com/sgl-project/sglang/pull/33613) Remove revoke queue after hit-then-alloc refactoring
- [#33637](https://github.com/sgl-project/sglang/pull/33637) Skip sglang-kernel and sgl-deep-gemm reinstall on version match
- [#33348](https://github.com/sgl-project/sglang/pull/33348) Match the replicated draft KV pool's page granularity to its allocator
- [#33351](https://github.com/sgl-project/sglang/pull/33351) Deep-merge nested config overrides and parse request bodies with orjson
- [#32734](https://github.com/sgl-project/sglang/pull/32734) Split tokenizer request metrics by stream
- [#30741](https://github.com/sgl-project/sglang/pull/30741) Prewarm DSV4 MHC post kernel at model load
- plus 25 more minor updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: da7cb91f817b1bb0f82716d16c613b88320377115a7b755ffee6e6d690497010 -->
