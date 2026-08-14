# vllm: PR digest (2026-08-09 to 2026-08-13)

_204 merged, 343 newly opened - source vllm-project/vllm, generated 2026-08-13T10:21:22Z_

## TL;DR
- **Model Focus**: DeepSeek (V4/V3.2) and Kimi-K3 dominated the window, with extensive work on MLA (Multi-Head Latent Attention), chunked-context packing, and Decode Context Parallelism (DCP). Qwen and Gemma also saw targeted fixes.
- **Performance & Kernels**: Major throughput and latency wins landed for AMD ROCm (FlyDSL decode-attention for 4-bit TurboQuant KV cache) and NVIDIA (Kimi-K3 fused KDA decode, long-context MLA cache gathers).
- **Architecture & Offloading**: Significant in-progress work is standardizing the KV cache layout across backends and introducing prefetch weight offloading with a schedule planner for large MoE models.
- **Multimodal & Tool Calling**: Merged native support for Dots3 NOTE multimodal models, and opened major migrations to a new streaming parser engine for JSON/tool-calling (Llama 3/4, Hermes).

## Most important PRs
- **[#51255](https://github.com/vllm-project/vllm/pull/51255)** adds native multimodal support for the Dots3 NOTE model family, integrating attention, kernels, and speculative decoding paths across AMD and NVIDIA hardware.
- **[#47896](https://github.com/vllm-project/vllm/pull/47896)** introduces a highly optimized FlyDSL decode-attention kernel for ROCm, unlocking significant performance gains for 4-bit TurboQuant KV caches on AMD GPUs.
- **[#50484](https://github.com/vllm-project/vllm/pull/50484)** implements Decode Context Parallelism (DCP) for Kimi-K3, enabling distributed attention and KV-cache management across multiple GPUs to handle massive context windows.
- **[#51718](https://github.com/vllm-project/vllm/pull/51718)** (newly opened) drives a massive architectural refactor to standardize the KV cache layout across all backends (FlashInfer, Triton, etc.), paving the way for unified portability and offloading.
- **[#51710](https://github.com/vllm-project/vllm/pull/51710)** (newly opened) proposes a schedule planner and prefetch weight offloading system for large Mixture-of-Experts (MoE) models, aiming to drastically reduce memory pressure during distributed inference.

## More changes by area

<details>
<summary>Performance (29)</summary>

- [#50654](https://github.com/vllm-project/vllm/pull/50654) Add Kimi-K3 fused kernel for KDA decode on ROCm
- [#49315](https://github.com/vllm-project/vllm/pull/49315) Add new warmup infrastructure for JITs and migrate Inkling FA4
- [#49436](https://github.com/vllm-project/vllm/pull/49436) Implement 3D-grid tiling of the state-copy Triton kernels
- [#51862](https://github.com/vllm-project/vllm/pull/51862) Remove prefill pipeline stall in chunk KDA for Kimi-K3 on ROCm
- [#51430](https://github.com/vllm-project/vllm/pull/51430) Narrow DeepSeek V4 eager CUDA graph region
- [#51738](https://github.com/vllm-project/vllm/pull/51738) Avoid more GPU-to-CPU syncs on the model execution path
- [#51458](https://github.com/vllm-project/vllm/pull/51458) Avoid some more unnecessary GPU-to-CPU syncs
- [#48223](https://github.com/vllm-project/vllm/pull/48223) Enable dual-stream decode with hipgraphs on ROCm
- [#52024](https://github.com/vllm-project/vllm/pull/52024) Revert dual-stream decode with hipgraphs on ROCm
- [#51725](https://github.com/vllm-project/vllm/pull/51725) Add adaptive budget for spec scheduled token to improve TTFT
- [#51311](https://github.com/vllm-project/vllm/pull/51311) Add flash KDA out kernel for prefill to improve K3 performance
- [#51919](https://github.com/vllm-project/vllm/pull/51919) Cut decode-side TTFT for NIXL P/D via first-token seeding and fast KV side channels
- [#51674](https://github.com/vllm-project/vllm/pull/51674) Add fused CUDA post-conv MTP decode kernel for Qwen3.5 GDN
- [#51885](https://github.com/vllm-project/vllm/pull/51885) Reduce eager-mode reconfiguration downtime for Elastic EP
- [#51794](https://github.com/vllm-project/vllm/pull/51794) Enable CSA multi-stream overlap for DeepSeek-V4 on ROCm
- [#52070](https://github.com/vllm-project/vllm/pull/52070) Disable EAGLE cache-hit block drop for always-K=0 dynamic DSD
- [#51592](https://github.com/vllm-project/vllm/pull/51592) Align speed-bench CLI flags with Python and add flag parity test
- [#51942](https://github.com/vllm-project/vllm/pull/51942) Fuse all-reduce RMSNorm with packed FP8
- [#51883](https://github.com/vllm-project/vllm/pull/51883) Skip unchanged layers in async transfer cycles for EPLB
- [#51589](https://github.com/vllm-project/vllm/pull/51589) Add adaptive sync-less DeepEP v2 prefill dispatch
- [#51540](https://github.com/vllm-project/vllm/pull/51540) Avoid a per-prefill-step GPU-to-CPU sync in the KDA chunk kernels
- [#52033](https://github.com/vllm-project/vllm/pull/52033) Enable dual-stream decode with hipgraphs on ROCm
- [#52080](https://github.com/vllm-project/vllm/pull/52080) Fuse the q-a and kv-a RMSNorms for Kimi-K3 AMD MLA
- [#51861](https://github.com/vllm-project/vllm/pull/51861) Skip the per-step q concat in TRITON_MLA decode
- [#52096](https://github.com/vllm-project/vllm/pull/52096) Reduce AITER MLA FP8 BMM warmup sizes on ROCm
- [#52059](https://github.com/vllm-project/vllm/pull/52059) Split MiniMax-M3 prefill index-score K loop on ROCm
- [#51507](https://github.com/vllm-project/vllm/pull/51507) Launch the top-k/top-p Triton sampler kernel with 8 warps
- [#50333](https://github.com/vllm-project/vllm/pull/50333) Skip detokenization in offline beam search
- [#51774](https://github.com/vllm-project/vllm/pull/51774) Avoid repeated multimodal prompt update scans

</details>

<details>
<summary>Kernels & attention (21)</summary>

- [#51739](https://github.com/vllm-project/vllm/pull/51739) Optimize long-context MLA cache gathers
- [#51772](https://github.com/vllm-project/vllm/pull/51772) Fuse Kimi-K3 chunked-context K/V packing
- [#40958](https://github.com/vllm-project/vllm/pull/40958) Extend ROCm AITER MHA (FA) coverage
- [#50907](https://github.com/vllm-project/vllm/pull/50907) Remove stale SDPA and skinny GEMM workarounds on ROCm
- [#46849](https://github.com/vllm-project/vllm/pull/46849) Fuse AR speculator multi-step decodes back into one CUDA graph
- [#49718](https://github.com/vllm-project/vllm/pull/49718) Add FlashInfer XQA decode support on SM12x
- [#50268](https://github.com/vllm-project/vllm/pull/50268) Enable fused bf16 to fp32 router GEMM on ROCm
- [#52017](https://github.com/vllm-project/vllm/pull/52017) Add B12X causal paged attention backend
- [#52016](https://github.com/vllm-project/vllm/pull/52016) Add B12X dense linear backends
- [#51855](https://github.com/vllm-project/vllm/pull/51855) Support replayssm for K3
- [#51700](https://github.com/vllm-project/vllm/pull/51700) Enable full CUDA graph capture for microbatched steps (DBO)
- [#51551](https://github.com/vllm-project/vllm/pull/51551) Add guarded gfx942 FP8 context prefill for ROCm MLA
- [#51709](https://github.com/vllm-project/vllm/pull/51709) Add unit tests for GDN/FLA Triton kernels
- [#51590](https://github.com/vllm-project/vllm/pull/51590) Measure complete CUDA graph capture footprint for KV budgeting
- [#51987](https://github.com/vllm-project/vllm/pull/51987) Revert FlashInfer XQA decode support on SM12x
- [#52046](https://github.com/vllm-project/vllm/pull/52046) Add PCP support to DeepSeek V3.2 attention
- [#52019](https://github.com/vllm-project/vllm/pull/52019) Skip stage2 for single-split Triton MLA decode
- [#51555](https://github.com/vllm-project/vllm/pull/51555) Add portable Triton paged-MQA-logits kernel for DeepSeek-V4 sparse indexer
- [#51713](https://github.com/vllm-project/vllm/pull/51713) Use the AITER tuned GEMM for full-graph decode attention on ROCm
- [#51647](https://github.com/vllm-project/vllm/pull/51647) Pad non-aligned AITER MLA heads on ROCm
- [#52063](https://github.com/vllm-project/vllm/pull/52063) Avoid AITER FP8 BMM for MLA K projection

</details>

<details>
<summary>MoE & quantization (33)</summary>

- [#43529](https://github.com/vllm-project/vllm/pull/43529) Migrate bitsandbytes support to OOT plugin
- [#51624](https://github.com/vllm-project/vllm/pull/51624) Add unqualized MoE Backend for Power (VSX)
- [#51265](https://github.com/vllm-project/vllm/pull/51265) Add Ling-3.0-flash-fp8 support
- [#44201](https://github.com/vllm-project/vllm/pull/44201) Route BF16 MoE inference through zentorch on AMD CPU
- [#51407](https://github.com/vllm-project/vllm/pull/51407) Add MoE output contract for MoE tail fusion
- [#51148](https://github.com/vllm-project/vllm/pull/51148) Enable GPTQ and AWQ quantization for s390x CPU
- [#47205](https://github.com/vllm-project/vllm/pull/47205) Add tensor-descriptor operand loads for Triton W8A8 scaled_mm on XPU
- [#51860](https://github.com/vllm-project/vllm/pull/51860) Dequantize the fp8 decode query for MLA backends without quant-query support
- [#52018](https://github.com/vllm-project/vllm/pull/52018) Add B12X FP4 MoE backend
- [#51563](https://github.com/vllm-project/vllm/pull/51563) Migrate W4A16 FlyDSL MoE to AITER API on ROCm
- [#51880](https://github.com/vllm-project/vllm/pull/51880) Add online LUT-B quantization for MoE
- [#51754](https://github.com/vllm-project/vllm/pull/51754) Add shared expert fusion for TRTLLM FP8
- [#51695](https://github.com/vllm-project/vllm/pull/51695) Standardize and abstract fused shared expert optimization selection
- [#51707](https://github.com/vllm-project/vllm/pull/51707) Fuse Kimi SiTU activation and per-token FP8 quant on w2 path
- [#51724](https://github.com/vllm-project/vllm/pull/51724) Enable W4A16 DSA
- [#51918](https://github.com/vllm-project/vllm/pull/51918) Add FlyDSL fused mega-MoE backend for DeepSeek V4 on ROCm
- [#51569](https://github.com/vllm-project/vllm/pull/51569) Implement FP8 block padding for unaligned cases
- [#51876](https://github.com/vllm-project/vllm/pull/51876) Shard the MoE experts across NUMA nodes on CPU
- [#51656](https://github.com/vllm-project/vllm/pull/51656) Move MoE sequence parallel boundaries into parallel linear layers
- [#52032](https://github.com/vllm-project/vllm/pull/52032) Add opt-in dynamic NVFP4 MoE GEMM2 quantization
- [#51815](https://github.com/vllm-project/vllm/pull/51815) Enable Chord W4A16 MoE as a humming backend drop-in
- [#51808](https://github.com/vllm-project/vllm/pull/51808) Support activation quant key override for online quantization
- [#51941](https://github.com/vllm-project/vllm/pull/51941) Accept prequantized DeepGEMM inputs
- [#52100](https://github.com/vllm-project/vllm/pull/52100) Preserve TP sharding with explicit EP
- [#51925](https://github.com/vllm-project/vllm/pull/51925) Enable optimized FlashInfer add-RMSNorm NVFP4 fusion
- [#51947](https://github.com/vllm-project/vllm/pull/51947) Reuse packed FP8 logits inputs for MTP
- [#51583](https://github.com/vllm-project/vllm/pull/51583) Fold the MXFP4 block scale in 2 instructions instead of 4 on CPU
- [#51605](https://github.com/vllm-project/vllm/pull/51605) Size batched Triton MoE tiles from per-expert rows
- [#51943](https://github.com/vllm-project/vllm/pull/51943) Fuse attention FP8 quantization for DeepSeek V3.2
- [#51924](https://github.com/vllm-project/vllm/pull/51924) Refine FlashInfer one-sided All2All integration
- [#51800](https://github.com/vllm-project/vllm/pull/51800) Remove quark-specific silent online quantization
- [#51598](https://github.com/vllm-project/vllm/pull/51598) Enable scoped AITER W8A8 support on gfx1100
- [#51933](https://github.com/vllm-project/vllm/pull/51933) Enable torch as mxfp8 linear backend on XPU

</details>

<details>
<summary>Model support (11)</summary>

- [#49797](https://github.com/vllm-project/vllm/pull/49797) Fix Gemma 4 for upcoming Transformers version
- [#48215](https://github.com/vllm-project/vllm/pull/48215) Add tower/connector LoRA support for Ultravox
- [#51831](https://github.com/vllm-project/vllm/pull/51831) Support R3 capture with DeepGEMM MegaMoE
- [#47017](https://github.com/vllm-project/vllm/pull/47017) Enable DeepSeek-V4 on gfx11
- [#51780](https://github.com/vllm-project/vllm/pull/51780) Enable tower and connector LoRA for Keye
- [#51655](https://github.com/vllm-project/vllm/pull/51655) Add Muse Glimmer model support
- [#51833](https://github.com/vllm-project/vllm/pull/51833) Add DeepGrove Maple (MapleForCausalLM)
- [#51558](https://github.com/vllm-project/vllm/pull/51558) Add K-EXAONE-2.0-750B-A37B-DSpark
- [#51949](https://github.com/vllm-project/vllm/pull/51949) Enable LoRA support for tower and connector in Cosmos3-Edge
- [#51553](https://github.com/vllm-project/vllm/pull/51553) Expose per-layer parameters for Gemma4
- [#51797](https://github.com/vllm-project/vllm/pull/51797) Match Qwen3.5 GDN BF16 semantics

</details>

<details>
<summary>Parallelism & scheduling (24)</summary>

- [#47808](https://github.com/vllm-project/vllm/pull/47808) Add DSpark confidence-scheduled verification
- [#48414](https://github.com/vllm-project/vllm/pull/48414) Add canonical CPU layout for parallelism-agnostic KV offload
- [#51243](https://github.com/vllm-project/vllm/pull/51243) Emit self-describing events for partial recurrent blocks in KV offload
- [#51603](https://github.com/vllm-project/vllm/pull/51603) Apply Mamba alignment before encoder caps in V1 scheduler
- [#51601](https://github.com/vllm-project/vllm/pull/51601) Add Scheduler Plugin Framework for V1
- [#52103](https://github.com/vllm-project/vllm/pull/52103) Carry request provenance through stored events in KV offload
- [#52079](https://github.com/vllm-project/vllm/pull/52079) Add GEMM-RS for sequence parallelism in Kimi-K3
- [#51606](https://github.com/vllm-project/vllm/pull/51606) Enable fp8 KV cache with DSpark speculative decoding and code-reorg on ROCm
- [#52097](https://github.com/vllm-project/vllm/pull/52097) Add suffix_gpu drafter for Async Scheduling
- [#51527](https://github.com/vllm-project/vllm/pull/51527) Support prefix caching with heterogeneous P/D logical block sizes in NIXL
- [#52110](https://github.com/vllm-project/vllm/pull/52110) Support pipeline parallelism in sharded state loader
- [#52015](https://github.com/vllm-project/vllm/pull/52015) Support pipeline parallelism for DiffusionGemma
- [#51691](https://github.com/vllm-project/vllm/pull/51691) Certify per-token-head KV quant in the canonical layout
- [#51548](https://github.com/vllm-project/vllm/pull/51548) Add PP-first placement for multiprocess serving
- [#51886](https://github.com/vllm-project/vllm/pull/51886) Add retention interval to OffloadingConnector
- [#51689](https://github.com/vllm-project/vllm/pull/51689) Certify attention-only hybrids in the canonical portability gate
- [#51690](https://github.com/vllm-project/vllm/pull/51690) Look through UniformTypeKVCacheSpecs in the canonical portability gate
- [#51705](https://github.com/vllm-project/vllm/pull/51705) Support decode context parallelism for Kimi-K3 DSpark on ROCm
- [#51988](https://github.com/vllm-project/vllm/pull/51988) Add configurable load-balancing strategy to EPLB
- [#51595](https://github.com/vllm-project/vllm/pull/51595) Count async loads per request in MultiConnector
- [#51576](https://github.com/vllm-project/vllm/pull/51576) Add TieringAdmissionPolicy skeleton (factory/base/always)
- [#52099](https://github.com/vllm-project/vllm/pull/52099) Add explicit expert-parallel topology
- [#51978](https://github.com/vllm-project/vllm/pull/51978) Add layerwise KV cache transfer support with mooncake session API
- [#52101](https://github.com/vllm-project/vllm/pull/52101) Add BF16 PoC integration of MoonEP balanced EP backend

</details>

<details>
<summary>API & serving (27)</summary>

- [#51144](https://github.com/vllm-project/vllm/pull/51144) Support dynamic tools from developer messages in Rust frontend
- [#49577](https://github.com/vllm-project/vllm/pull/49577) Add Mask Replay feature
- [#51447](https://github.com/vllm-project/vllm/pull/51447) Bound generation inputs before expensive work
- [#51178](https://github.com/vllm-project/vllm/pull/51178) Add explicit data-parallel rank routing in Rust frontend gRPC
- [#51478](https://github.com/vllm-project/vllm/pull/51478) Add content_parts to /inference/v1/generate for raw multimodal
- [#51463](https://github.com/vllm-project/vllm/pull/51463) Make `model` optional on all `/derender` request classes
- [#51577](https://github.com/vllm-project/vllm/pull/51577) Migrate llama3_json/llama4_json to the streaming parser engine
- [#52132](https://github.com/vllm-project/vllm/pull/52132) Enhance engine snapshot management and API lifecycle
- [#51891](https://github.com/vllm-project/vllm/pull/51891) Validate request indices and sampler sizes before engine work
- [#52061](https://github.com/vllm-project/vllm/pull/52061) Add native forward-pass metrics emission
- [#51535](https://github.com/vllm-project/vllm/pull/51535) Support allowed_tools in Rust chat requests
- [#51904](https://github.com/vllm-project/vllm/pull/51904) Support stop strings in the token generate route in Rust frontend
- [#51898](https://github.com/vllm-project/vllm/pull/51898) Validate scale-out multimodal data before engine handoff
- [#51892](https://github.com/vllm-project/vllm/pull/51892) Bound frontend work for Responses and tokenize requests
- [#51896](https://github.com/vllm-project/vllm/pull/51896) Reject oversized media before fully downloading it
- [#51937](https://github.com/vllm-project/vllm/pull/51937) Migrate Hermes tool parser to the new streaming Parser Engine
- [#51826](https://github.com/vllm-project/vllm/pull/51826) Add torchcodec as audio loader and implement selective audio backend
- [#51778](https://github.com/vllm-project/vllm/pull/51778) Add prediction token usage details to frontend
- [#51981](https://github.com/vllm-project/vllm/pull/51981) Add per-request prefix-cache write policy
- [#52133](https://github.com/vllm-project/vllm/pull/52133) Add Hunyuan A13B tool parser in Rust frontend
- [#51746](https://github.com/vllm-project/vllm/pull/51746) Add explicit model info cache preparation
- [#51747](https://github.com/vllm-project/vllm/pull/51747) Add OpenTelemetry tracing to GPU-less render server endpoints
- [#51906](https://github.com/vllm-project/vllm/pull/51906) Add routed-experts prompt offset
- [#51615](https://github.com/vllm-project/vllm/pull/51615) Report CPU offload capacity in tokens
- [#52098](https://github.com/vllm-project/vllm/pull/52098) Allow omitting output token IDs from logs
- [#51900](https://github.com/vllm-project/vllm/pull/51900) Cap the cumulative length of realtime sessions
- [#51554](https://github.com/vllm-project/vllm/pull/51554) Add FastSafetensors sharded-state loader

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#51578](https://github.com/vllm-project/vllm/pull/51578) Enable MiniMax-M3 on non-CUDA backends via portable fallbacks
- [#51613](https://github.com/vllm-project/vllm/pull/51613) Batch LoRA slice processing to cut Python-level launch latency on XPU
- [#51956](https://github.com/vllm-project/vllm/pull/51956) Register KV offload mmap region as pinned host memory on XPU

</details>

<details>
<summary>Bugfixes (102)</summary>

- [#48171](https://github.com/vllm-project/vllm/pull/48171) Fix lfm2 tool parser dropping calls with brackets or newlines
- [#49328](https://github.com/vllm-project/vllm/pull/49328) Fix failed-load livelock by marking the lookup verdict as a miss
- [#51011](https://github.com/vllm-project/vllm/pull/51011) Fix fp8 KV cache decode on the AITER MLA backend
- [#51455](https://github.com/vllm-project/vllm/pull/51455) Make the GPU sync check thread-local and fix its suppressors
- [#51721](https://github.com/vllm-project/vllm/pull/51721) Stabilize build context and source caches on ROCm
- [#51865](https://github.com/vllm-project/vllm/pull/51865) Require all requests to be decoding for uniform-decode dispatch
- [#46747](https://github.com/vllm-project/vllm/pull/46747) Recover from P0/P1 processor cache drift in multimodal V1
- [#51622](https://github.com/vllm-project/vllm/pull/51622) Centralize shared mmap cleanup in CPU worker
- [#52003](https://github.com/vllm-project/vllm/pull/52003) Fix mypy for vllm/model_executor/models/[cC][dD]
- [#51837](https://github.com/vllm-project/vllm/pull/51837) Give KV-first attention blocks their own page in hybrid models on ROCm
- [#50528](https://github.com/vllm-project/vllm/pull/50528) Emit REASONING_END for Inkling tool calls that follow no thinking block
- [#50344](https://github.com/vllm-project/vllm/pull/50344) Scope divergent hybrid cache hits to capable connectors
- [#50999](https://github.com/vllm-project/vllm/pull/50999) Use file:// rendezvous for single-node executors to eliminate startup port races
- [#49815](https://github.com/vllm-project/vllm/pull/49815) Apply vision attention sinks in the window attention path
- [#51749](https://github.com/vllm-project/vllm/pull/51749) Generalize KV block zeroing to `AttentionSpec`
- [#51756](https://github.com/vllm-project/vllm/pull/51756) Take the sliding window from the layer, not the KV cache group
- [#51139](https://github.com/vllm-project/vllm/pull/51139) Invalidate retained PyNvVideoCodec decoder after failure
- [#49948](https://github.com/vllm-project/vllm/pull/49948) Fix DoS via sample-rate forgery bypassing audio decode duration guard
- [#49519](https://github.com/vllm-project/vllm/pull/49519) Defer post-load attention weight processing
- [#49758](https://github.com/vllm-project/vllm/pull/49758) Fix expert_map vs AITER expert_mask for non-AITER experts under EP
- [#52058](https://github.com/vllm-project/vllm/pull/52058) Bound KV block zeroing launch geometry
- [#50020](https://github.com/vllm-project/vllm/pull/50020) Support encoder timing stats in model runner V2
- [#51218](https://github.com/vllm-project/vllm/pull/51218) Report FULL_ATTENTION for uniform-base UniformTypeKVCacheSpecs groups
- [#49227](https://github.com/vllm-project/vllm/pull/49227) Mask request stop tokens in xgrammar until grammar terminates
- [#51120](https://github.com/vllm-project/vllm/pull/51120) Return 400 for invalid PyNvVideoCodec video input
- [#50727](https://github.com/vllm-project/vllm/pull/50727) Fix fused block-scale orientation
- [#51843](https://github.com/vllm-project/vllm/pull/51843) Disable fine-grained prefix-cache hits for incompatible hybrid KV layouts
- [#52092](https://github.com/vllm-project/vllm/pull/52092) Ship triton-cpu wheel and fix several hardcoded pin_memory=True
- [#51614](https://github.com/vllm-project/vllm/pull/51614) Emit self-describing CPU events at KV-group block granularity
- [#51766](https://github.com/vllm-project/vllm/pull/51766) Preserve Mamba running CoW after external hits
- [#51768](https://github.com/vllm-project/vllm/pull/51768) Guard DeepSeek V4 MRV1 piecewise CUDA graphs
- [#50074](https://github.com/vllm-project/vllm/pull/50074) Reuse online NVFP4 MoE kernel across reloads
- [#51296](https://github.com/vllm-project/vllm/pull/51296) Align deepseek v4 parser thinking default with tokenizer
- [#51256](https://github.com/vllm-project/vllm/pull/51256) Reserve the bonus query slot in DFlash scheduling budget
- [#51556](https://github.com/vllm-project/vllm/pull/51556) Report Cohere stop sequences correctly
- [#51419](https://github.com/vllm-project/vllm/pull/51419) Fix fp32 weight scale for mxfp4 quantization and per-expert checkpoint mapping
- [#51654](https://github.com/vllm-project/vllm/pull/51654) Fix chat completion 500 on non-object JSON bodies
- [#51259](https://github.com/vllm-project/vllm/pull/51259) Import each packed IPC export once on the consumer side
- [#50734](https://github.com/vllm-project/vllm/pull/50734) Fix Qwen3.5 MTP for text-only checkpoints
- [#50017](https://github.com/vllm-project/vllm/pull/50017) Fix chunked prefill paged decode masked load perf on ROCm
- [#49139](https://github.com/vllm-project/vllm/pull/49139) Fix persistent top-k histogram reuse after short rows
- [#51185](https://github.com/vllm-project/vllm/pull/51185) Patch stable string memleak fix from 2.14 for 2.13
- [#51635](https://github.com/vllm-project/vllm/pull/51635) Use TCP store when AITER custom all-reduce is enabled
- [#50874](https://github.com/vllm-project/vllm/pull/50874) Size monolithic routing replay buffer for DP
- [#51770](https://github.com/vllm-project/vllm/pull/51770) Fix UVA weight offloading for non-pinned-tensor views
- [#46845](https://github.com/vllm-project/vllm/pull/46845) Fix MiniMax-M3 compressed-tensors FP8 MoE SwiGLU params
- [#51813](https://github.com/vllm-project/vllm/pull/51813) Fix and test EPLB balancedness calculation
- [#51359](https://github.com/vllm-project/vllm/pull/51359) Initialize DeepGemmQuantScaleFMT oracle lazily
- [#51840](https://github.com/vllm-project/vllm/pull/51840) Return HIT_PENDING when KV promotion is triggered
- [#51161](https://github.com/vllm-project/vllm/pull/51161) Handle chunked local attention in offloading scheduler
- [#51573](https://github.com/vllm-project/vllm/pull/51573) Emit --no-{key} for false BooleanOptionalAction flags in YAML config
- [#51682](https://github.com/vllm-project/vllm/pull/51682) Give the AMD packed KDA decode kernel the state-index stride
- [#51850](https://github.com/vllm-project/vllm/pull/51850) Support HF-config compat for Inkling
- [#51733](https://github.com/vllm-project/vllm/pull/51733) Fix MLA prefill workspace allocation size
- [#51627](https://github.com/vllm-project/vllm/pull/51627) Make the Apple Silicon BF16 probe fall back instead of raising
- [#43680](https://github.com/vllm-project/vllm/pull/43680) Fix uniform_random routing simulation to sample without replacement
- [#51727](https://github.com/vllm-project/vllm/pull/51727) Fix DeepSeek V4/3.2 tokenizer vocab size overcount crashing guided decoding
- [#51773](https://github.com/vllm-project/vllm/pull/51773) Fix docs on `main`
- [#51602](https://github.com/vllm-project/vllm/pull/51602) Fix dspark parallel_drafting_token_id init bug
- [#51821](https://github.com/vllm-project/vllm/pull/51821) Restore the DeepSeek-V4 input GEMM override point on ROCm
- [#51812](https://github.com/vllm-project/vllm/pull/51812) Align Qwen GDN gates with speculative tokens
- [#51363](https://github.com/vllm-project/vllm/pull/51363) Forward per-head FP8 descales through FA4
- [#51736](https://github.com/vllm-project/vllm/pull/51736) Fix test_sharded_state_loader
- [#51997](https://github.com/vllm-project/vllm/pull/51997) Bound Anthropic stop sequences
- [#50693](https://github.com/vllm-project/vllm/pull/50693) Fix DSpark warmup without sparse index buffer
- [#51819](https://github.com/vllm-project/vllm/pull/51819) Support GELU tanh in FlashInfer B12x MoE
- [#51806](https://github.com/vllm-project/vllm/pull/51806) Fix ExampleConnector KV cache device selection on XPU
- [#51923](https://github.com/vllm-project/vllm/pull/51923) Fix workdir path for triton shim job on XPU
- [#51539](https://github.com/vllm-project/vllm/pull/51539) Fix docs on `main`
- [#51461](https://github.com/vllm-project/vllm/pull/51461) Fix Ernie-4.5-VL encoder CG postprocess for multi-path outputs
- [#51872](https://github.com/vllm-project/vllm/pull/51872) Make fp8_min/fp8_max constexpr in _quantize_pad_fp8_kernel
- [#52007](https://github.com/vllm-project/vllm/pull/52007) Fix ci qwen3.5
- [#52028](https://github.com/vllm-project/vllm/pull/52028) Pin DeepEP by its full commit hash
- [#51928](https://github.com/vllm-project/vllm/pull/51928) Run GDN attention as eager break under breakable cudagraph on XPU
- [#51482](https://github.com/vllm-project/vllm/pull/51482) Restore prepend (LIFO) reuse order when prefix caching is off
- [#51145](https://github.com/vllm-project/vllm/pull/51145) Fix DeepSeek V4 DSpark probabilistic startup on ROCm
- [#51854](https://github.com/vllm-project/vllm/pull/51854) Remove stale FlashAttention metadata arguments
- [#51857](https://github.com/vllm-project/vllm/pull/51857) Fix broken autorefs cross-reference in TurboQuant v2 docstring
- [#51665](https://github.com/vllm-project/vllm/pull/51665) Fix weight tying
- [#51649](https://github.com/vllm-project/vllm/pull/51649) Fix extreme case in pythonic parser argument json safety
- [#51698](https://github.com/vllm-project/vllm/pull/51698) Fix xLAM streaming duplicated arguments on finalize
- [#51684](https://github.com/vllm-project/vllm/pull/51684) Handle quantized qkv_proj in DFlash fused-KV buffers
- [#51662](https://github.com/vllm-project/vllm/pull/51662) Fix Mooncake store request-ID ABA in async job accounting
- [#52044](https://github.com/vllm-project/vllm/pull/52044) Handle DeepseekV4ForCausalLM in benchmark_moe get_model_params
- [#51536](https://github.com/vllm-project/vllm/pull/51536) Fix MiniMAXGemmaRMSNorm crash on non-CUDA platforms
- [#51620](https://github.com/vllm-project/vllm/pull/51620) Route DFlash fused context-KV projection through quant_method for quantized drafters
- [#51802](https://github.com/vllm-project/vllm/pull/51802) Fix NVIDIA DeepSeek V4 mHC warmup
- [#51903](https://github.com/vllm-project/vllm/pull/51903) Fix custom all-reduce graph IPC under expandable_segments
- [#51685](https://github.com/vllm-project/vllm/pull/51685) Take a native fp8 KV cache in TRITON_MLA and fold the non-causal decode
- [#51915](https://github.com/vllm-project/vllm/pull/51915) Enable GLM-5.2-MXFP4 on the deepseek_v32 path and fix sparse attention correctness
- [#52119](https://github.com/vllm-project/vllm/pull/52119) Kill regex compilation subprocess on timeout
- [#51722](https://github.com/vllm-project/vllm/pull/51722) Fix fused QK-norm+RoPE+cache abort by allocating K/V as separate head groups
- [#51824](https://github.com/vllm-project/vllm/pull/51824) Fix crash at startup when DeepEP v2 is used with `--enforce-eager` with TRTLLM Bf16
- [#52022](https://github.com/vllm-project/vllm/pull/52022) Fix store threshold admission counting
- [#51953](https://github.com/vllm-project/vllm/pull/51953) Fix DiffusionGemma runtime OOM via tiled logits projection
- [#52014](https://github.com/vllm-project/vllm/pull/52014) Fix MoRIIO port collisions for deployments using both DP and TP
- [#51560](https://github.com/vllm-project/vllm/pull/51560) Fail fast on Inkling's unsupported GPU architectures
- [#52094](https://github.com/vllm-project/vllm/pull/52094) Revert guard DeepSeek V4 MRV1 piecewise CUDA graphs
- [#51730](https://github.com/vllm-project/vllm/pull/51730) Reap orphaned CPU offload /dev/shm region files
- [#51787](https://github.com/vllm-project/vllm/pull/51787) Restore LRU prefix order after transfers
- [#51764](https://github.com/vllm-project/vllm/pull/51764) Align hybrid block sizes across PP stages
- [#52126](https://github.com/vllm-project/vllm/pull/52126) Prevent PyNvVideoCodec decoder slot limit bypass via ClassVar shadowing
- [#51944](https://github.com/vllm-project/vllm/pull/51944) Add opt-in gate for large Mooncake KV sends
- [#52054](https://github.com/vllm-project/vllm/pull/52054) Chunk prompt-logprobs logits to bound the activation peak
- [#52020](https://github.com/vllm-project/vllm/pull/52020) Reject empty JSON schemas
- [#51547](https://github.com/vllm-project/vllm/pull/51547) Fix usage.prompt_tokens over-counting generation prefix tokens
- [#51584](https://github.com/vllm-project/vllm/pull/51584) Account for the NUMA memory policy when sizing available RAM
- [#51565](https://github.com/vllm-project/vllm/pull/51565) Fix stateless first-chunk classification
- [#51858](https://github.com/vllm-project/vllm/pull/51858) Surface the reasoning end delimiter when no reasoning parser is attached
- [#52050](https://github.com/vllm-project/vllm/pull/52050) Fall back to FA2 for Blackwell head-dim-256 paged attention
- [#51610](https://github.com/vllm-project/vllm/pull/51610) Preserve MCP tool result semantics
- [#52093](https://github.com/vllm-project/vllm/pull/52093) Revert narrow DeepSeek V4 eager CUDA graph region
- [#52045](https://github.com/vllm-project/vllm/pull/52045) Workaround contradictory mamba validation after CPU MLA disables prefix caching
- [#52143](https://github.com/vllm-project/vllm/pull/52143) Fix Inkling structured output stop tokens
- [#51532](https://github.com/vllm-project/vllm/pull/51532) Use global DP index for MooncakeConnector bootstrap registration
- [#51675](https://github.com/vllm-project/vllm/pull/51675) Accept Anthropic x-api-key auth header
- [#52087](https://github.com/vllm-project/vllm/pull/52087) Preserve constant effective K schedule semantics
- [#51568](https://github.com/vllm-project/vllm/pull/51568) Transport E8M0 expert state as byte views
- [#51669](https://github.com/vllm-project/vllm/pull/51669) Fix streaming reasoning content misrouted to content
- [#51856](https://github.com/vllm-project/vllm/pull/51856) Attach request-level tools to existing system message in DeepSeek V4 Python renderer
- [#51550](https://github.com/vllm-project/vllm/pull/51550) Fix RustToolParser streaming final flush
- [#51616](https://github.com/vllm-project/vllm/pull/51616) Ignore Harmony recipients when no tools are configured
- [#51846](https://github.com/vllm-project/vllm/pull/51846) Fix prompt_logprobs=0 bypassing admission guards and chat echo
- [#52047](https://github.com/vllm-project/vllm/pull/52047) Annotate draft KV cache groups on the hybrid grouping path
- [#51757](https://github.com/vllm-project/vllm/pull/51757) Support heterogeneous models failing with AmbiguousGlobalPerLayerAttributeError
- [#51671](https://github.com/vllm-project/vllm/pull/51671) Fix stop buffer desync
- [#51702](https://github.com/vllm-project/vllm/pull/51702) Stop special tokens split across deltas leaking into output for GigaChat3
- [#52062](https://github.com/vllm-project/vllm/pull/52062) Revert KV block zeroing generalization due to ROCm launch overflow
- [#52072](https://github.com/vllm-project/vllm/pull/52072) Apply suppress_tokens on the Gemma 4 MTP sparse path
- [#51852](https://github.com/vllm-project/vllm/pull/51852) Give CPU attention layers their own metadata when head counts differ
- [#51741](https://github.com/vllm-project/vllm/pull/51741) Fall back to native sampler when FlashInfer sampling kernel fails to build
- [#51703](https://github.com/vllm-project/vllm/pull/51703) Record non-ImportError attention backend probe failures instead of crashing engine init
- [#51599](https://github.com/vllm-project/vllm/pull/51599) Decouple async Mamba align D2H counts from InputBatch row shifts
- [#51979](https://github.com/vllm-project/vllm/pull/51979) Release worker RPC payload before next dequeue
- [#51863](https://github.com/vllm-project/vllm/pull/51863) Check readiness before tokenizer init in rust vllm-bench
- [#52013](https://github.com/vllm-project/vllm/pull/52013) Load a dedicated mtp.lm_head draft head
- [#51893](https://github.com/vllm-project/vllm/pull/51893) Cap placement-group wait backoff at the deadline
- [#51723](https://github.com/vllm-project/vllm/pull/51723) Clamp block table indices in align mode to prevent OOB gather
- [#51664](https://github.com/vllm-project/vllm/pull/51664) Fix chart resource references
- [#51538](https://github.com/vllm-project/vllm/pull/51538) Make DSV4 sparse MLA work end-to-end for plain decode, MTP, and DSpark
- [#51895](https://github.com/vllm-project/vllm/pull/51895) Require a PyAV build with the fixed IAMF parser
- [#51870](https://github.com/vllm-project/vllm/pull/51870) Quietly reject invalid post-reasoning speculative drafts
- [#51716](https://github.com/vllm-project/vllm/pull/51716) Resolve short-form GPU UUIDs in CUDA_VISIBLE_DEVICES
- [#49505](https://github.com/vllm-project/vllm/pull/49505) Avoid repeated layerwise reload warning scans

</details>

<details>
<summary>Tests (24)</summary>

- [#50713](https://github.com/vllm-project/vllm/pull/50713) Solidify speculative decoding E2E coverage
- [#50804](https://github.com/vllm-project/vllm/pull/50804) Stabilize tensor IPC multiprocessing tests
- [#51657](https://github.com/vllm-project/vllm/pull/51657) Harden Transformers modelling backend multi-modal path
- [#51446](https://github.com/vllm-project/vllm/pull/51446) Preserve revision pins in secondary artifact loaders
- [#51931](https://github.com/vllm-project/vllm/pull/51931) Use VLLMValidationError in pooling input validation
- [#51753](https://github.com/vllm-project/vllm/pull/51753) Use VLLMValidationError in scoring input validation
- [#52064](https://github.com/vllm-project/vllm/pull/52064) Mirror external test assets in vLLM S3
- [#49579](https://github.com/vllm-project/vllm/pull/49579) Call to EC Connector update_connector_output from scheduler
- [#51726](https://github.com/vllm-project/vllm/pull/51726) Update default `_max_num_batched_tokens` from 8192 to 16384
- [#51652](https://github.com/vllm-project/vllm/pull/51652) Use file rendezvous for local distributed tests
- [#51097](https://github.com/vllm-project/vllm/pull/51097) Preserve non-logitproc entry points in tests
- [#51557](https://github.com/vllm-project/vllm/pull/51557) Stabilize DP supervisor lifecycle tests
- [#51688](https://github.com/vllm-project/vllm/pull/51688) Keep per-layer KV registration when canonical_layout is requested
- [#51879](https://github.com/vllm-project/vllm/pull/51879) Expose data-parallel topology to offloading backends
- [#45042](https://github.com/vllm-project/vllm/pull/45042) Restore MiniCPMV transformers cap, scoped to HF runner only
- [#52144](https://github.com/vllm-project/vllm/pull/52144) Add test/pause resume
- [#51827](https://github.com/vllm-project/vllm/pull/51827) Harden Transformers modelling backend multi-modal path
- [#51767](https://github.com/vllm-project/vllm/pull/51767) Simplify fs manager
- [#51968](https://github.com/vllm-project/vllm/pull/51968) Make tests device-agnostic on XPU
- [#51559](https://github.com/vllm-project/vllm/pull/51559) Extend shared tool-parser parity suite to 6 more parsers
- [#51769](https://github.com/vllm-project/vllm/pull/51769) Warn when EAGLE/MTP speculation costs a large prefix-cache hit
- [#51706](https://github.com/vllm-project/vllm/pull/51706) Add a coverage ratchet for per-parser tool-calling tests
- [#52073](https://github.com/vllm-project/vllm/pull/52073) Test extract_hidden_states on NemotronH hybrid models
- [#51969](https://github.com/vllm-project/vllm/pull/51969) Enforce server-side num_frames ceiling in VideoMediaIO merge

</details>

<details>
<summary>CI & build (41)</summary>

- [#52136](https://github.com/vllm-project/vllm/pull/52136) Add `pydocstyle` to the `ruff` rules
- [#48646](https://github.com/vllm-project/vllm/pull/48646) Reuse equivalent ROCm CI images
- [#47030](https://github.com/vllm-project/vllm/pull/47030) Enable vLLM DI CI with buildkite/slurm
- [#51735](https://github.com/vllm-project/vllm/pull/51735) Parallelize release image publishing
- [#51911](https://github.com/vllm-project/vllm/pull/51911) Add registry layer cache to x86 CPU image build
- [#51732](https://github.com/vllm-project/vllm/pull/51732) Add /ci cancel command
- [#50892](https://github.com/vllm-project/vllm/pull/50892) Bump Flashinfer version to 0.6.16.post3
- [#51877](https://github.com/vllm-project/vllm/pull/51877) Speed Up ROCm Skinny GEMM Tests
- [#51759](https://github.com/vllm-project/vllm/pull/51759) Publish XPU Triton shim index
- [#51276](https://github.com/vllm-project/vllm/pull/51276) Publish protobuf schemas to Buf
- [#51184](https://github.com/vllm-project/vllm/pull/51184) Cache test dependencies before vLLM install
- [#51666](https://github.com/vllm-project/vllm/pull/51666) Persist the openai-harmony tiktoken vocab cache across jobs
- [#51668](https://github.com/vllm-project/vllm/pull/51668) Bump Transformers version to 5.15.0
- [#51905](https://github.com/vllm-project/vllm/pull/51905) Change to use global VLLM_DISABLE_COMPILE_CACHE=1 in Intel GPU CI
- [#52043](https://github.com/vllm-project/vllm/pull/52043) Force source builds for hybrid dependencies
- [#50831](https://github.com/vllm-project/vllm/pull/50831) Install xpu-manager for device monitor
- [#51422](https://github.com/vllm-project/vllm/pull/51422) Upgrade huggingface-hub to 1.27.0
- [#50513](https://github.com/vllm-project/vllm/pull/50513) Update UMD to 26.27
- [#51935](https://github.com/vllm-project/vllm/pull/51935) Add triton shim in xpu requirements
- [#51058](https://github.com/vllm-project/vllm/pull/51058) Upgrade runtime image to Ubuntu 24.04, pick up rdma-core > 44
- [#50787](https://github.com/vllm-project/vllm/pull/50787) Route block-quantized FP8 weights to the W8A8 kernel
- [#51604](https://github.com/vllm-project/vllm/pull/51604) Add VLLM_DISABLE_COMPILE_CACHE=1 for other random failed cases in Intel GPU CI
- [#51424](https://github.com/vllm-project/vllm/pull/51424) Skip precompiled wheel fetch during metadata hooks
- [#51882](https://github.com/vllm-project/vllm/pull/51882) Remove NIXL reinstall step
- [#51566](https://github.com/vllm-project/vllm/pull/51566) Bump CUTLASS DSL to 4.6.2
- [#51213](https://github.com/vllm-project/vllm/pull/51213) Pin block size in test_multi_connector
- [#52127](https://github.com/vllm-project/vllm/pull/52127) Shrink triton-cpu-build layer by dropping build artifacts
- [#50441](https://github.com/vllm-project/vllm/pull/50441) Bump up xpu kernel to v0.1.12.3
- [#50826](https://github.com/vllm-project/vllm/pull/50826) Enable torch linear backend for blockwise gemm on xpu
- [#51832](https://github.com/vllm-project/vllm/pull/51832) Support partial torch requirement contexts
- [#51982](https://github.com/vllm-project/vllm/pull/51982) Add generic CI trace collectors
- [#51851](https://github.com/vllm-project/vllm/pull/51851) Bump the minor-update group across 1 directory with 174 updates
- [#51817](https://github.com/vllm-project/vllm/pull/51817) Copy CPU shared-memory tails at their exact length
- [#51830](https://github.com/vllm-project/vllm/pull/51830) Report torch-nightly results to PyTorch CRCR
- [#51630](https://github.com/vllm-project/vllm/pull/51630) Add more cases in intel GPU CI and reorganize to align non-xpu part
- [#51834](https://github.com/vllm-project/vllm/pull/51834) Add standalone rust vllm-bench image
- [#51955](https://github.com/vllm-project/vllm/pull/51955) Split Quantization job into three directory-based steps
- [#51934](https://github.com/vllm-project/vllm/pull/51934) Add E2E correctness test for QK-norm+RoPE fusion
- [#52108](https://github.com/vllm-project/vllm/pull/52108) Add xpu wheel release to release pipeline
- [#51687](https://github.com/vllm-project/vllm/pull/51687) Rob kimi dev branch

</details>

<details>
<summary>Docs (10)</summary>

- [#51729](https://github.com/vllm-project/vllm/pull/51729) Rewrite weight-transfer docs and standardize examples
- [#51308](https://github.com/vllm-project/vllm/pull/51308) Connect vLLM Recipes with vLLM's native config-based deployment and benchmark
- [#48789](https://github.com/vllm-project/vllm/pull/48789) Add minimal Triton Proton profiling backend
- [#51878](https://github.com/vllm-project/vllm/pull/51878) Support different data types variants and strategies in vLLM Recipes conversion
- [#51734](https://github.com/vllm-project/vllm/pull/51734) Replace batch_norm to numerically identical without cudnn
- [#49353](https://github.com/vllm-project/vllm/pull/49353) Add Crusoe Managed Inference deployment guide
- [#51999](https://github.com/vllm-project/vllm/pull/51999) Warn that --api-key does not gate all endpoints
- [#51500](https://github.com/vllm-project/vllm/pull/51500) Fix typos in speculative decoding docs
- [#52134](https://github.com/vllm-project/vllm/pull/52134) Fix `WhisperEncoderLayer.forward` docstring in `dots3_note`
- [#51570](https://github.com/vllm-project/vllm/pull/51570) Load HF datasets from parquet shards via hf-hub, fixing truncated-cache sampling

</details>

<details>
<summary>Refactors (5)</summary>

- [#51838](https://github.com/vllm-project/vllm/pull/51838) Delete dead code in models
- [#51612](https://github.com/vllm-project/vllm/pull/51612) Promote local KV cache specs via a class-changing replace helper
- [#51917](https://github.com/vllm-project/vllm/pull/51917) Unify uniform decode token count helper
- [#51704](https://github.com/vllm-project/vllm/pull/51704) Backend-published KV packing via customize_spec
- [#51927](https://github.com/vllm-project/vllm/pull/51927) Use common sp utils for Qwen3.5 MoE

</details>

<details>
<summary>Other (20)</summary>

- [#48798](https://github.com/vllm-project/vllm/pull/48798) Add tiering offloading metrics
- [#51235](https://github.com/vllm-project/vllm/pull/51235) Upgrade MiniJinja to 2.22 & remove method lookup workaround
- [#47352](https://github.com/vllm-project/vllm/pull/47352) Share topk index buffer between draft steps
- [#51379](https://github.com/vllm-project/vllm/pull/51379) Restore linear dispatch for small unquantized GEMMs
- [#51251](https://github.com/vllm-project/vllm/pull/51251) Configure custom encoder cache managers from VllmConfig
- [#51672](https://github.com/vllm-project/vllm/pull/51672) Enable test_fused_moe_wn16 on XPU
- [#49444](https://github.com/vllm-project/vllm/pull/49444) Enable test_silu_mul_fp8_quant_deep_gemm on XPU
- [#51841](https://github.com/vllm-project/vllm/pull/51841) Avoid long-blocking H2D copies in ViT
- [#52037](https://github.com/vllm-project/vllm/pull/52037) Skip unused Jina V5 output layers
- [#48668](https://github.com/vllm-project/vllm/pull/48668) Preserve prefix-cache stats on zero-output steps
- [#52035](https://github.com/vllm-project/vllm/pull/52035) Update DeepGEMM pin to deepseek-ai nv_dev tip
- [#51529](https://github.com/vllm-project/vllm/pull/51529) Allow tpu to import kimi_k3.common
- [#50569](https://github.com/vllm-project/vllm/pull/50569) Allow shared expert overlapping for FlashInfer one-sided all-to-all
- [#51473](https://github.com/vllm-project/vllm/pull/51473) Preserve native MXFP4 TP8 shard allocation
- [#51457](https://github.com/vllm-project/vllm/pull/51457) Add ROCm AITER FP8 MLA prefill accuracy test
- [#50977](https://github.com/vllm-project/vllm/pull/50977) Add PrivateUse1 activity support for custom backends in profiler
- [#51881](https://github.com/vllm-project/vllm/pull/51881) Add VLLM_ENABLE_MULTINODE_PROFILING to sync profiler start across DP ranks
- [#51998](https://github.com/vllm-project/vllm/pull/51998) Upstream Cohere parser fixes + tests
- [#52076](https://github.com/vllm-project/vllm/pull/52076) Clearer comments in `BlockPool.free_blocks()`
- [#51875](https://github.com/vllm-project/vllm/pull/51875) Make prefix-cache NONE_HASH deterministic by default

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 99a3bbc68f66e8b1d8165b4741777c04c3ab7cd54a9e81560e1935cd6d1a53fe -->
