# vllm: PR digest (2026-11-08 to 2026-11-12)

_369 merged, 610 newly opened - source vllm-project/vllm, generated 2026-11-12T18:01:54Z_

## TL;DR
- **DeepSeek (V4.1) and the new GLM-5.3 / Kimi K3.1 / MiniMax-M3 / Muse Spark / Qwen4Exp families dominate.** Most perf work targets "specialized decode" paths: DSpark drafts, mHC, Engram and ShardQ on NVIDIA, plus AMD monokernels on MI355X/gfx942.
- **MoE and quantization wins:** DeepGEMM Mega MoE gained SM90 MXFP4 and block-FP8 paths and FlashInfer MoE-EP. TRT-LLM monolithic MoE now skips DP padding rows. Other additions: MXFP6, ModelOpt INT8 per-block and NVFP4 fusions, AITER fused SiLU+FP8 quant, and FlyDSL MXFP8 GEMM.
- **Sampler and spec-decode kernels dominate the new PRs.** They include CuTe DSL and Triton top-k/top-p (~3x faster), top-k cutoffs applied during verification, and Mamba2 ReplaySSM/FlashInfer SSD.
- **The direction is serving infrastructure and decode-latency tuning.** That means Rust frontend and Rust engine-core parity, PD-disaggregation connectors (NIXL, Mooncake, MoRIIO), extensible KV cache, fast-start, and TP-replicated attention experiments.

## Most important PRs
**[#63102](https://github.com/vllm-project/vllm/pull/63102) [Perf][GLM-5.3-Flash] Specialized decode for GB300 TP4**
Adds a specialized decode path for GLM-5.3-Flash on GB300. The newly opened [#66865](https://github.com/vllm-project/vllm/pull/66865) (Qwen3.8-Flash-Next) and [#67095](https://github.com/vllm-project/vllm/pull/67095) (ROCm GLM-5.3) follow the same recipe.

**[#66532](https://github.com/vllm-project/vllm/pull/66532) / [#66037](https://github.com/vllm-project/vllm/pull/66037) Kimi K3.1 serving at TP8**
These are two parts of the split series. They add NVIDIA specialized decode, ROCm TP8 support, and KV cache and attention changes to serve Kimi K3.1 at TP8. [#66604](https://github.com/vllm-project/vllm/pull/66604) also writes draft KV at block-stride slots.

**[#62603](https://github.com/vllm-project/vllm/pull/62603) [Perf][MoE] SM90 block-FP8 MegaMoE via FlashInfer MoE-EP**
Brings the fused MegaMoE kernel to Hopper block-FP8. Together with [#64061](https://github.com/vllm-project/vllm/pull/64061) (SM90 MXFP4 DeepGEMM Mega MoE) it broadens fused MoE coverage beyond Blackwell.

**[#61869](https://github.com/vllm-project/vllm/pull/61869) [Perf][DSv4.1] DSpark draft on the specialized decode**
Runs the DSpark speculative draft inside DeepSeek V4.1's specialized decode path. Related merges: [#66652](https://github.com/vllm-project/vllm/pull/66652) (CuTe DSL mHC for batches up to 336 tokens) and [#66552](https://github.com/vllm-project/vllm/pull/66552) (Engram 128-row tiles).

**[#66318](https://github.com/vllm-project/vllm/pull/66318) [Kernel][Mamba] Mamba2 ReplaySSM spec decode on Triton**
Enables speculative decoding for Mamba2 hybrids on the Triton backend. This makes hybrid models usable with spec decode without relying on special backends.

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#65349](https://github.com/vllm-project/vllm/pull/65349) warm up JIT kernels reached only by long prefills, eager drafters and constrained decoding
- [#59981](https://github.com/vllm-project/vllm/pull/59981) V2 runner decode optimizations for NVIDIA Confidential Computing
- [#65521](https://github.com/vllm-project/vllm/pull/65521) FlashInfer mega mHC for MHCFusedPostPreOp (GLM-5.3-Flash)
- [#65896](https://github.com/vllm-project/vllm/pull/65896) copy-engine PP transport, on by default on NVLink
- [#66512](https://github.com/vllm-project/vllm/pull/66512) faster QSA kernel for large fp8 batches on Blackwell (Qwen4Exp)
- [#65972](https://github.com/vllm-project/vllm/pull/65972) skip DP padding rows in TRT-LLM monolithic MoE
- [#61498](https://github.com/vllm-project/vllm/pull/61498) mono decode layer for Kimi-K3 on MI355X
- [#66549](https://github.com/vllm-project/vllm/pull/66549) ShardQ token sharding extended to norms and A projections (GLM-5.3)
- [#66764](https://github.com/vllm-project/vllm/pull/66764) fuse DSpark draft norms and Markov sampling (Muse Spark)
- [#65227](https://github.com/vllm-project/vllm/pull/65227) encoder CUDA graphs: one replay per batch
- [#66047](https://github.com/vllm-project/vllm/pull/66047) shard sparse-indexer decode rows across TP (DSv4.1, ROCm)
- [#65524](https://github.com/vllm-project/vllm/pull/65524) replay one row for far prefill chunks (DSv4.1)
- [#61942](https://github.com/vllm-project/vllm/pull/61942) skip DSA indexer scoring for short dense-MHA prefills
- [#64560](https://github.com/vllm-project/vllm/pull/64560) fuse decode W_UK absorb, q concat and fp8 quant via AITER
- [#63893](https://github.com/vllm-project/vllm/pull/63893) tuned K1 at TP4 for DSv4.1 mono
- [#66660](https://github.com/vllm-project/vllm/pull/66660) EPLB rebalanced-expert copy in one launch per weight
- [#67040](https://github.com/vllm-project/vllm/pull/67040) DeepGEMM BF16 MegaMoE for unquantized GLM-5.3
- [#66537](https://github.com/vllm-project/vllm/pull/66537) H200 FP8 config for GLM-5.3-Flash TP8
- [#65028](https://github.com/vllm-project/vllm/pull/65028) serialize SSE chunks before building the event (Rust frontend)
- [#65822](https://github.com/vllm-project/vllm/pull/65822) MoRIIO WRITE skips blocks already in the decoder prefix cache
- [#61501](https://github.com/vllm-project/vllm/pull/61501) opt-in FlashInfer SSD prefill scan
- [#65077](https://github.com/vllm-project/vllm/pull/65077) honor FP8 activations for Humming linear on SM100/SM110

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#63383](https://github.com/vllm-project/vllm/pull/63383) ROCM_RDNA_ATTN backend for gfx1151
- [#66018](https://github.com/vllm-project/vllm/pull/66018) FlashInfer MSA backend for MiniMax-M3 on SM90/SM120
- [#60321](https://github.com/vllm-project/vllm/pull/60321) mxfp4_mla KV cache for rope-free sparse MLA on ROCm
- [#66036](https://github.com/vllm-project/vllm/pull/66036) tensor-scale FP8 KV cache for sparse MLA (DSv4/4.1, ROCm)
- [#63847](https://github.com/vllm-project/vllm/pull/63847) persistent_topk on ROCm
- [#59384](https://github.com/vllm-project/vllm/pull/59384) fuse BF16 ReLU2 with NVFP4 quantization
- [#46558](https://github.com/vllm-project/vllm/pull/46558) enable FlashInfer mm-prefix attention
- [#65203](https://github.com/vllm-project/vllm/pull/65203) sync FlashAttention with upstream
- [#54899](https://github.com/vllm-project/vllm/pull/54899) pad AITER MLA decode head count to a native tile under DCP
- [#64001](https://github.com/vllm-project/vllm/pull/64001) avoid runtime JIT for combine_topk_swa_indices inputs
- [#66400](https://github.com/vllm-project/vllm/pull/66400) drop sparse MLA metadata host sync, use persistent AITER for long prefills

</details>

<details>
<summary>MoE & quantization (13)</summary>

- [#46871](https://github.com/vllm-project/vllm/pull/46871) XPU all-to-all EP backend for batched MoE
- [#64315](https://github.com/vllm-project/vllm/pull/64315) Qwen4Exp routed experts on DeepGEMM MegaMoE (MXFP8/MXFP4)
- [#65479](https://github.com/vllm-project/vllm/pull/65479) MXFP8 linear on AITER FlyDSL GEMM (MiniMax-M3.1)
- [#63721](https://github.com/vllm-project/vllm/pull/63721) fuse SiLU-and-mul with per-token FP8 quant in TritonExperts
- [#63727](https://github.com/vllm-project/vllm/pull/63727) gfx942 FP8 W8A8 fused-MoE configs for Muse Spark
- [#66139](https://github.com/vllm-project/vllm/pull/66139) online FP8 routed experts for Muse Spark on Hopper
- [#65272](https://github.com/vllm-project/vllm/pull/65272) ModelOpt INT8_PB_WO linear layers
- [#61666](https://github.com/vllm-project/vllm/pull/61666) compressed-tensors MXFP6
- [#64767](https://github.com/vllm-project/vllm/pull/64767) ModelOpt NVFP4 W4A16 token embeddings
- [#61897](https://github.com/vllm-project/vllm/pull/61897) routed experts capture (R3) with PP
- [#51006](https://github.com/vllm-project/vllm/pull/51006) pluggable fused MoE routers
- [#66859](https://github.com/vllm-project/vllm/pull/66859) RoutedScaleMode enum replacing bool flags
- [#61530](https://github.com/vllm-project/vllm/pull/61530) MXFP4-packed Engram embedding tables (DSV4.1)

</details>

<details>
<summary>Model support (10)</summary>

- [#65848](https://github.com/vllm-project/vllm/pull/65848) Ling VL video, YaRN, vision DP
- [#66334](https://github.com/vllm-project/vllm/pull/66334) Muse Spark Open cleanup
- [#65904](https://github.com/vllm-project/vllm/pull/65904) MiniMax-M3 moved to AutoWeightsLoader
- [#66393](https://github.com/vllm-project/vllm/pull/66393) Transformers backend: migrate Gemma and StableLM
- [#66559](https://github.com/vllm-project/vllm/pull/66559) Transformers backend: migrate Phi3
- [#66827](https://github.com/vllm-project/vllm/pull/66827) serve Qwen2-MoE with the Transformers backend
- [#65735](https://github.com/vllm-project/vllm/pull/65735) transcription in the Transformers backend
- [#66546](https://github.com/vllm-project/vllm/pull/66546) EAGLE3 aux hidden states with PP in the Transformers backend
- [#66388](https://github.com/vllm-project/vllm/pull/66388) upstream config for MOSS-Transcribe-Diarize
- [#66238](https://github.com/vllm-project/vllm/pull/66238) Qwen3-VL-4B recipe for Xeon 6

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#63796](https://github.com/vllm-project/vllm/pull/63796) DSpark sliding-window MLA drafts under DCP
- [#66177](https://github.com/vllm-project/vllm/pull/66177) centralize aux hidden-state relay for spec decode with PP
- [#65217](https://github.com/vllm-project/vllm/pull/65217) prefill_context_kv_only for P/D prefill instances
- [#66224](https://github.com/vllm-project/vllm/pull/66224) simplify prefill_schedule_interval outside DP
- [#61725](https://github.com/vllm-project/vllm/pull/61725) max_async_kv_loads_per_step cap
- [#64693](https://github.com/vllm-project/vllm/pull/64693) MoRIIO PP for prefill instances in PD serving
- [#65448](https://github.com/vllm-project/vllm/pull/65448) lookahead block hashes in remaining KV connectors
- [#65943](https://github.com/vllm-project/vllm/pull/65943) reuse Mooncake PD TransferEngine in the store connector
- [#66605](https://github.com/vllm-project/vllm/pull/66605) external connectors can declare KV memory registration
- [#61797](https://github.com/vllm-project/vllm/pull/61797) UMBP lazy GPU cache offloading
- [#61424](https://github.com/vllm-project/vllm/pull/61424) collect iteration details during scheduling

</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#64715](https://github.com/vllm-project/vllm/pull/64715) UMBP standalone mode for DSv4.1-Flash on ROCm
- [#66319](https://github.com/vllm-project/vllm/pull/66319) Mamba cache stochastic rounding on gfx950
- [#66321](https://github.com/vllm-project/vllm/pull/66321) prefill context parallel for GLM-5.2 sparse MLA on ROCm
- [#54899](https://github.com/vllm-project/vllm/pull/54899) AITER MLA DCP head padding (see Kernels)

</details>

<details>
<summary>API & serving (21)</summary>

- [#65993](https://github.com/vllm-project/vllm/pull/65993) Rust frontend: multimodal and LoRA in the renderer
- [#66529](https://github.com/vllm-project/vllm/pull/66529) Rust frontend: stream DeepSeek DSML tool-call args
- [#66531](https://github.com/vllm-project/vllm/pull/66531) Rust frontend: stream MiniMax M3 tool-call args
- [#66767](https://github.com/vllm-project/vllm/pull/66767) Rust frontend: match MiniMax M3 markers by token identity
- [#65864](https://github.com/vllm-project/vllm/pull/65864) Rust frontend: return routed experts on non-streaming responses
- [#66119](https://github.com/vllm-project/vllm/pull/66119) Rust frontend: --log-level and --logging-config
- [#66539](https://github.com/vllm-project/vllm/pull/66539) Rust frontend: JSON log formatter
- [#66106](https://github.com/vllm-project/vllm/pull/66106) Rust frontend: tool_reference content parts
- [#66104](https://github.com/vllm-project/vllm/pull/66104) Rust frontend: request_render_duration metric
- [#66105](https://github.com/vllm-project/vllm/pull/66105) Rust frontend: SimpleCPUOffload connector metrics
- [#66187](https://github.com/vllm-project/vllm/pull/66187) Rust frontend: media_io_kwargs video fps
- [#66528](https://github.com/vllm-project/vllm/pull/66528) Rust frontend: tool-call args in template JSON style
- [#66103](https://github.com/vllm-project/vllm/pull/66103) Rust frontend: join text parts for DeepSeek V3.2
- [#60274](https://github.com/vllm-project/vllm/pull/60274) Rust frontend: --enable-force-include-usage
- [#65541](https://github.com/vllm-project/vllm/pull/65541) Rust bench alignment with Python
- [#66691](https://github.com/vllm-project/vllm/pull/66691) bump xgrammar to 0.2.9
- [#57796](https://github.com/vllm-project/vllm/pull/57796) features with content_parts in /generate
- [#63753](https://github.com/vllm-project/vllm/pull/63753), [#65168](https://github.com/vllm-project/vllm/pull/65168) fast-start compiled cache seeding and shared stores
- [#61076](https://github.com/vllm-project/vllm/pull/61076) RL: configurable staging for sharded RDT
- [#66073](https://github.com/vllm-project/vllm/pull/66073) keyframe-aware sampling for PyNvVideoCodec

</details>

<details>
<summary>Bugfixes (50)</summary>

- [#66398](https://github.com/vllm-project/vllm/pull/66398) DiffusionGemma logprobs without host syncs
- [#63401](https://github.com/vllm-project/vllm/pull/63401) size extensible KV cache from exact VRAM use
- [#66731](https://github.com/vllm-project/vllm/pull/66731) extensible KV cache reserve on full token budget
- [#66523](https://github.com/vllm-project/vllm/pull/66523) release warmup blocks before CUDA graph capture
- [#65137](https://github.com/vllm-project/vllm/pull/65137) same-host NIXL on NVLink with extensible KV cache
- [#58619](https://github.com/vllm-project/vllm/pull/58619) partial-tail offload for hybrid models under DCP
- [#65939](https://github.com/vllm-project/vllm/pull/65939) Mooncake store prefix lookup circuit breaker
- [#67080](https://github.com/vllm-project/vllm/pull/67080) skip Mooncake saves after failed existence checks
- [#66190](https://github.com/vllm-project/vllm/pull/66190) Qwen2.5-Omni video encoder budget
- [#66432](https://github.com/vllm-project/vllm/pull/66432) Qwen2-VL video budget
- [#66608](https://github.com/vllm-project/vllm/pull/66608) pass only video count to get_num_frames_with_most_features
- [#65177](https://github.com/vllm-project/vllm/pull/65177) INT8 MoE per-channel weight scale indexing
- [#66419](https://github.com/vllm-project/vllm/pull/66419) --cpu-offload-gb with Transformers backend
- [#64329](https://github.com/vllm-project/vllm/pull/64329) apply q_scale only to FP8 queries in FlashInfer
- [#64165](https://github.com/vllm-project/vllm/pull/64165) FlashInfer plan buffer race with PP
- [#66486](https://github.com/vllm-project/vllm/pull/66486) MoE LoRA correctness under DP+EP
- [#64437](https://github.com/vllm-project/vllm/pull/64437) 3D MoE LoRA wrapper for Gemma4
- [#65842](https://github.com/vllm-project/vllm/pull/65842) FP16 shared-expert division only where models compensate
- [#65406](https://github.com/vllm-project/vllm/pull/65406) expert down-projection bias counted once under TP
- [#49539](https://github.com/vllm-project/vllm/pull/49539) AutoGPTQ keeps unquantized routed experts
- [#64485](https://github.com/vllm-project/vllm/pull/64485) EPLB async rearrangement interval
- [#63357](https://github.com/vllm-project/vllm/pull/63357) --response-role and echo in chat derender
- [#64041](https://github.com/vllm-project/vllm/pull/64041) reasoning and cached tokens in derender usage
- [#65744](https://github.com/vllm-project/vllm/pull/65744) normalize Chat Completions tools validation
- [#65932](https://github.com/vllm-project/vllm/pull/65932) pool HF fast tokenizers in BaseRenderer
- [#66773](https://github.com/vllm-project/vllm/pull/66773) Rust frontend exits on permanent engine failure
- [#64742](https://github.com/vllm-project/vllm/pull/64742) Rust frontend cancellation during submission
- [#66380](https://github.com/vllm-project/vllm/pull/66380) Rust frontend reasoning not reopened after prompt close
- [#66891](https://github.com/vllm-project/vllm/pull/66891) tool-result media in Inkling renderer
- [#67008](https://github.com/vllm-project/vllm/pull/67008) honor X-Vllm-Priority in scale-out generate
- [#66777](https://github.com/vllm-project/vllm/pull/66777) SageMaker /invocations error reporting
- [#66117](https://github.com/vllm-project/vllm/pull/66117) reject translation on non-translating models
- [#66348](https://github.com/vllm-project/vllm/pull/66348) granite_20b_fc system message rendering
- [#58094](https://github.com/vllm-project/vllm/pull/58094) rope hf_overrides propagated to MTP draft
- [#63432](https://github.com/vllm-project/vllm/pull/63432) rotary cache for nested-config and YaRN drafts
- [#66081](https://github.com/vllm-project/vllm/pull/66081) non-deferred structured-output draft retrieval
- [#62769](https://github.com/vllm-project/vllm/pull/62769) sync adaptive DSpark decisions across TP ranks
- [#66289](https://github.com/vllm-project/vllm/pull/66289) Triton GemmaRMSNorm for arch<sm80 (Qwen3.5)
- [#66390](https://github.com/vllm-project/vllm/pull/66390) host sync in dots.ocr vision encoder
- [#66201](https://github.com/vllm-project/vllm/pull/66201) MiMo-V2 omni video grid labels
- [#65351](https://github.com/vllm-project/vllm/pull/65351), [#65535](https://github.com/vllm-project/vllm/pull/65535) encoder CUDA graph aliasing and precomputed embeddings
- [#54548](https://github.com/vllm-project/vllm/pull/54548) keep is_embed in rendered placeholders
- [#65755](https://github.com/vllm-project/vllm/pull/65755) Step5 FP32 residual truncation at PP boundaries
- [#51951](https://github.com/vllm-project/vllm/pull/51951) Inkling sconv cache block-size mismatch
- [#64298](https://github.com/vllm-project/vllm/pull/64298), [#67098](https://github.com/vllm-project/vllm/pull/67098) KV offload fetch failure and ARC eviction order
- [#61492](https://github.com/vllm-project/vllm/pull/61492) periodic stats line fields
- [#63337](https://github.com/vllm-project/vllm/pull/63337) stopped vs dead engine core on shutdown
- [#65996](https://github.com/vllm-project/vllm/pull/65996) multimodal prefix-LM ranges on every PP stage

</details>

<details>
<summary>Bugfixes, ROCm-specific (8)</summary>

- [#61872](https://github.com/vllm-project/vllm/pull/61872) restore MoE weight padding
- [#64403](https://github.com/vllm-project/vllm/pull/64403) unused index caches in MiniMax-M3 sharing layers
- [#65092](https://github.com/vllm-project/vllm/pull/65092) reserve kpool decode indexer logits during profiling
- [#66397](https://github.com/vllm-project/vllm/pull/66397) build DSv4.1 replay builders at warmup
- [#62675](https://github.com/vllm-project/vllm/pull/62675) pad Qwen4Exp PLE n-gram inputs for piecewise graphs
- [#66399](https://github.com/vllm-project/vllm/pull/66399) remove step-path GPU syncs
- [#66400](https://github.com/vllm-project/vllm/pull/66400) sparse MLA host sync (see Kernels)
- [#64560](https://github.com/vllm-project/vllm/pull/64560) see Performance

</details>

<details>
<summary>Refactors (7)</summary>

- [#67085](https://github.com/vllm-project/vllm/pull/67085) remove dead code models
- [#66834](https://github.com/vllm-project/vllm/pull/66834) remove dual-chunk attention leftovers
- [#67035](https://github.com/vllm-project/vllm/pull/67035) remove TeleChat2 and TeleChat3
- [#65084](https://github.com/vllm-project/vllm/pull/65084) shared encoder CUDA graph buffer reuse
- [#66518](https://github.com/vllm-project/vllm/pull/66518) overridable CuMemAllocator helpers
- [#65877](https://github.com/vllm-project/vllm/pull/65877) separate Mooncake PD and Store connector packages
- [#66287](https://github.com/vllm-project/vllm/pull/66287) remove level-2 sleep workarounds

</details>

<details>
<summary>CI & build (14)</summary>

- [#65158](https://github.com/vllm-project/vllm/pull/65158) check-docstring-style pre-commit hook and single-backtick docstrings
- [#55387](https://github.com/vllm-project/vllm/pull/55387) default CUDA build moved to 13.2
- [#65765](https://github.com/vllm-project/vllm/pull/65765) Rubin nightly images on CUDA 13.5
- [#65576](https://github.com/vllm-project/vllm/pull/65576) AWS EFA in main image
- [#58795](https://github.com/vllm-project/vllm/pull/58795) prebuild mamba-ssm and causal-conv1d
- [#66291](https://github.com/vllm-project/vllm/pull/66291) PP equivalence tests for text models
- [#66196](https://github.com/vllm-project/vllm/pull/66196), [#66678](https://github.com/vllm-project/vllm/pull/66678) NIXL PD sweep and examples run as sharded pytest
- [#66309](https://github.com/vllm-project/vllm/pull/66309), [#66307](https://github.com/vllm-project/vllm/pull/66307), [#66312](https://github.com/vllm-project/vllm/pull/66312), [#67073](https://github.com/vllm-project/vllm/pull/67073) ROCm CI mirrors and test areas
- [#66603](https://github.com/vllm-project/vllm/pull/66603), [#66034](https://github.com/vllm-project/vllm/pull/66034) XPU B70 job migrations
- [#66737](https://github.com/vllm-project/vllm/pull/66737) revert of ZenCPU zen5 tests

</details>

<details>
<summary>Docs & recipes (8)</summary>

- [#64070](https://github.com/vllm-project/vllm/pull/64070) Qwen3.5 recipe cleanup
- [#66642](https://github.com/vllm-project/vllm/pull/66642), [#66433](https://github.com/vllm-project/vllm/pull/66433) Kimi-K3.1-Pro GB300/B300 presets
- [#66343](https://github.com/vllm-project/vllm/pull/66343) Kimi-K3.1-Pro MI355X preset
- [#67184](https://github.com/vllm-project/vllm/pull/67184) MiniMax-M3.1-Flash GB300 presets
- [#66268](https://github.com/vllm-project/vllm/pull/66268) MiniMax-M3.1-Flash MI355X PD disaggregation
- [#67071](https://github.com/vllm-project/vllm/pull/67071) stop setting gpu_memory_utilization in extensible KV cache docs/tests
- [#66704](https://github.com/vllm-project/vllm/pull/66704) warn when gpu_memory_utilization withholds memory

</details>

<details>
<summary>Other (5)</summary>

- [#66483](https://github.com/vllm-project/vllm/pull/66483) time target sampling in vllm bench forward
- [#57810](https://github.com/vllm-project/vllm/pull/57810) keep offloaded KV tier across pause/sleep
- [#56192](https://github.com/vllm-project/vllm/pull/56192) RDMA-capable OBJ KV offload tier
- [#67074](https://github.com/vllm-project/vllm/pull/67074)-range minor items not shown: plus ~169 more small merges
- [#66674](https://github.com/vllm-project/vllm/pull/66674) exportable extensible KV cache for LMCache MP

</details>

<details>
<summary>Newly opened (in progress, notable)</summary>

- [#66862](https://github.com/vllm-project/vllm/pull/66862) Rust engine core: scheduler, KV manager, connectors with bitwise parity
- [#66889](https://github.com/vllm-project/vllm/pull/66889) native xgrammar for the Rust engine core
- [#66497](https://github.com/vllm-project/vllm/pull/66497) DeepSeek-V4.1 on A100 (SM80) and H100 (SM90)
- [#66865](https://github.com/vllm-project/vllm/pull/66865) Qwen3.8-Flash-Next specialized decode on GB300
- [#67095](https://github.com/vllm-project/vllm/pull/67095) GLM-5.3 specialized decode on ROCm
- [#66415](https://github.com/vllm-project/vllm/pull/66415) Muse Spark PTPC FP8 specialized decode on gfx942
- [#67149](https://github.com/vllm-project/vllm/pull/67149) FlashTopK fused MQA+top-k prefill backend
- [#66792](https://github.com/vllm-project/vllm/pull/66792), [#66630](https://github.com/vllm-project/vllm/pull/66630), [#66521](https://github.com/vllm-project/vllm/pull/66521), [#66639](https://github.com/vllm-project/vllm/pull/66639) top-k/top-p sampler kernels (Triton, CuTe DSL, CUDA)
- [#66534](https://github.com/vllm-project/vllm/pull/66534) top-k cutoffs during spec-decode verification
- [#67045](https://github.com/vllm-project/vllm/pull/67045), [#66881](https://github.com/vllm-project/vllm/pull/66881), [#67160](https://github.com/vllm-project/vllm/pull/67160) hybrid Mamba prefix caching with spec decode
- [#66837](https://github.com/vllm-project/vllm/pull/66837) spec-driven TP slicing for NIXL
- [#66866](https://github.com/vllm-project/vllm/pull/66866)-range TP-replicated attention experiments: [#66867](https://github.com/vllm-project/vllm/pull/66867), [#66868](https://github.com/vllm-project/vllm/pull/66868), [#66869](https://github.com/vllm-project/vllm/pull/66869), [#66870](https://github.com/vllm-project/vllm/pull/66870), [#66871](https://github.com/vllm-project/vllm/pull/66871), [#66872](https://github.com/vllm-project/vllm/pull/66872), [#67285](https://github.com/vllm-project/vllm/pull/67285)
- [#66371](https://github.com/vllm-project/vllm/pull/66371), [#66372](https://github.com/vllm-project/vllm/pull/66372), [#66373](https://github.com/vllm-project/vllm/pull/66373), [#66374](https://github.com/vllm-project/vllm/pull/66374) XPU expert offload
- [#66472](https://github.com/vllm-project/vllm/pull/66472) Foundry-persisted CUDA graphs for fast start

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f4b95a08b680ad281aa9255b8ca6176c8a55fa91757f73526f7ef9d0d2c6444a -->
