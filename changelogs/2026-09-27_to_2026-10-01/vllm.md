# vllm: PR digest (2026-09-27 to 2026-10-01)

_306 merged, 450 newly opened - source vllm-project/vllm, generated 2026-10-01T16:18:42Z_

## TL;DR
- **DeepSeek-V4.1 got the most model-specific attention (34 labels).** Work spanned ROCm (aiter MXFP4 sparse indexer, fused mHC Triton kernel, a4w4 MoE) and NVIDIA (fused WO-A + inverse RoPE + MXFP8 quant on SM100/SM103, faster Engram lookups, decoder SWA bounded replay). Newly opened: SM90 small-head sparse decode, Humming MXFP4 MoE on Hopper, and CUDA-graphed replay layers.
- **Sparse and MLA attention and hybrid-model decode drew the most kernel effort.** Merged: sparse MLA Gluon kernel, FlashInfer ReplaySSM for Mamba MTP, and removal of a D2H sync in the SM90 sparse MLA plan. Newly opened: GLM-5.3 index-conversion and fused-Q kernels, QSA on SM90, and GDN RecoverSSM verify in a fused CUDA MTP kernel.
- **Quantization and MoE:** the merged work is W4A8 int4 on CPU (Zen), the per-token NVFP4 CuTe-DSL MoE backend, and AITER MoE padding. Opened PRs add NVFP4/MXFP4 activation-quant fusions, padded-work skipping in DeepGEMM experts, and ModelOpt IQ2/Q8_0 via b12x.
- **Direction:** the Rust frontend and parser engine are being built out (grammars, tool-call markers, `n` choices). KV connectors, HiSparse, and sleep-mode support are growing. MRV2 is gaining feature parity (spec decode with a draft model, Elastic EP, PP+PCP). CI and mypy cleanup continue.

## Most important PRs
**[#58671](https://github.com/vllm-project/vllm/pull/58671) – ROCm DSv4.1 paged MXFP4 sparse indexer on aiter's MQA-logits kernel.** It gives DeepSeek-V4.1 sparse attention on AMD an MXFP4 paged indexer path. This is the largest model-specific kernel work merged this window.

**[#58634](https://github.com/vllm-project/vllm/pull/58634) – Fused small-batch WO-A + inverse RoPE + MXFP8 quant (SM100/SM103).** It collapses three DSv4.1 decode-path ops into one launch, which cuts launch overhead and memory traffic at small batch sizes.

**[#52928](https://github.com/vllm-project/vllm/pull/52928) – FlashInfer ReplaySSM support for Mamba MTP.** It adds FlashInfer-backed state replay for speculative (MTP) verification on hybrid SSM models, in place of rolling back state.

**[#57952](https://github.com/vllm-project/vllm/pull/57952) – Mooncake KV connector packs hybrid/MLA KV into coalesced transfer regions.** Fewer, larger transfers speed up prefill/decode disaggregation for MLA and hybrid-cache models.

**[#43091](https://github.com/vllm-project/vllm/pull/43091) – Model Runner V2 supports spec decode with a draft model.** It closes a key MRV2 feature gap. Related MRV2 work merged this window includes sampling-mask replay for MTP ([#59359](https://github.com/vllm-project/vllm/pull/59359)) and Elastic EP ([#53934](https://github.com/vllm-project/vllm/pull/53934)).

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#58957](https://github.com/vllm-project/vllm/pull/58957) fuse HC down-projection and SiLU for Qwen4Exp on NVIDIA
- [#59327](https://github.com/vllm-project/vllm/pull/59327) faster DSv4.1 Engram host lookups (sorted rows, inline big lookups)
- [#58684](https://github.com/vllm-project/vllm/pull/58684) remove D2H sync from FlashInfer SM90 sparse MLA plan under async scheduling
- [#58495](https://github.com/vllm-project/vllm/pull/58495) add TP=2/4/8 per-rank shapes to the sm_120 batch-invariant matmul table
- [#57407](https://github.com/vllm-project/vllm/pull/57407) layer-aware CSA2 multi-stream overlap for DSv4.1-Flash on ROCm
- [#58655](https://github.com/vllm-project/vllm/pull/58655) run delayed mHC seams through aiter's fused Triton kernel (ROCm)
- [#53913](https://github.com/vllm-project/vllm/pull/53913) vectorized CPU sampler kernel
- [#58845](https://github.com/vllm-project/vllm/pull/58845) skip qlnorm for MHA on GLM 5.3 (4.4–7.7% TTFT)
- [#58114](https://github.com/vllm-project/vllm/pull/58114) reduce PLE metadata construction overhead for Qwen3.8
- [#58762](https://github.com/vllm-project/vllm/pull/58762) reuse Mamba/GDN metadata across KV cache groups in MRV2
- [#58400](https://github.com/vllm-project/vllm/pull/58400) allow FULL decode graphs for one-token prompt tails in MRV2
- [#58880](https://github.com/vllm-project/vllm/pull/58880) fused MiniMax2 routing with non-unit routed scaling
- [#58651](https://github.com/vllm-project/vllm/pull/58651) fuse per-layer QK RoPE into one in-place kernel for KimiViT
- [#57640](https://github.com/vllm-project/vllm/pull/57640) fuse MLA decode KV-cache write and Q-prep via AITER for Kimi-K3
- [#58542](https://github.com/vllm-project/vllm/pull/58542) skip sampled-token broadcasts for requests that leave the engine under PP
- [#58371](https://github.com/vllm-project/vllm/pull/58371) fused multi-step draft decode for FlashInfer trtllm-gen
- [#57214](https://github.com/vllm-project/vllm/pull/57214) avoid blocking seq_lens D2H copy for pooling in the FlashInfer metadata builder
- [#58008](https://github.com/vllm-project/vllm/pull/58008) single Triton kernel to fit kpool top-k indices to AITER (GLM-5.3-Flash)
- [#57979](https://github.com/vllm-project/vllm/pull/57979) stride-aware decode KDA on ROCm
- [#58797](https://github.com/vllm-project/vllm/pull/58797) allocate the pinned PLE prefetch buffer lazily on ROCm
- [#54956](https://github.com/vllm-project/vllm/pull/54956) sharded latent MoE up-projection under EP for Kimi-K3
- [#58705](https://github.com/vllm-project/vllm/pull/58705) docs build roughly 5x faster

</details>

<details>
<summary>Kernels & attention (9)</summary>

- [#53492](https://github.com/vllm-project/vllm/pull/53492) enable the sparse MLA Gluon kernel from Aiter
- [#56861](https://github.com/vllm-project/vllm/pull/56861) AITER ASM round-robin decode route for DCP multi-token verify
- [#54093](https://github.com/vllm-project/vllm/pull/54093) optimized aarch64 CPU Conv1d kernel
- [#54967](https://github.com/vllm-project/vllm/pull/54967) zentorch SDPA for CPU MLA prefill
- [#58482](https://github.com/vllm-project/vllm/pull/58482) occupancy-adaptive Triton split-K segment count on SM120
- [#59081](https://github.com/vllm-project/vllm/pull/59081) fp8 indexer cache on the Triton indexer for non-SM100 (MiniMax M3)
- [#56960](https://github.com/vllm-project/vllm/pull/56960) KDA prefill checkpoints for GLM-5.3-Flash
- [#54255](https://github.com/vllm-project/vllm/pull/54255) FlashInfer speculative KDA backend for Kimi-K3
- [#57097](https://github.com/vllm-project/vllm/pull/57097) fuse QK-norm/RoPE/gate and KV write into the QSA pre-indexer launch

</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#54024](https://github.com/vllm-project/vllm/pull/54024) DA8W4 (W4A8) int4 for dense and MoE on CPU Zen
- [#50030](https://github.com/vllm-project/vllm/pull/50030) per-token NVFP4 CuTe-DSL MoE backend
- [#58819](https://github.com/vllm-project/vllm/pull/58819) opt-in a4w4 MoE for DSv4.1 on AITER
- [#55368](https://github.com/vllm-project/vllm/pull/55368) pad AITER MoE intermediate size at allocation and round expert-group count
- [#58262](https://github.com/vllm-project/vllm/pull/58262) MiMo-V2.6 MXFP4 on gfx942
- [#58201](https://github.com/vllm-project/vllm/pull/58201) VLLM_ROCM_USE_AITER_MOE_SITUV2 selects a4w4/a8w4/a16w4
- [#52798](https://github.com/vllm-project/vllm/pull/52798) canonical N-first weight format for compressed-tensors WNA16 MoE
- [#58268](https://github.com/vllm-project/vllm/pull/58268) W4A16 Whisper on the CPU WNA16 kernel
- [#59149](https://github.com/vllm-project/vllm/pull/59149) W4A16 (AWQ/GPTQ) on POWER10 via VSX

</details>

<details>
<summary>Model support (9)</summary>

- [#58132](https://github.com/vllm-project/vllm/pull/58132) decoder-side SWA bounded replay for DeepSeek-V4.1
- [#55335](https://github.com/vllm-project/vllm/pull/55335) fold partial-RoPE permutation into q/k weights (K2 Horizon)
- [#58673](https://github.com/vllm-project/vllm/pull/58673) encoder CUDA graph for MiniMax-M3
- [#56575](https://github.com/vllm-project/vllm/pull/56575) engine-based plamo3 parser
- [#57168](https://github.com/vllm-project/vllm/pull/57168) compile support for Pixtral vision encoders
- [#57531](https://github.com/vllm-project/vllm/pull/57531) Mistral3 image preprocessing optimization
- [#57928](https://github.com/vllm-project/vllm/pull/57928) device normalization for Llama Nemotron VL embed/rerank
- [#55389](https://github.com/vllm-project/vllm/pull/55389) device-side mm normalization for GLM4V/GLM5Next
- [#51289](https://github.com/vllm-project/vllm/pull/51289) device-side mm normalization for Qwen3VL/Qwen3.5/Qwen4Next

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#58947](https://github.com/vllm-project/vllm/pull/58947) rework the scheduler skipped_waiting queue
- [#57652](https://github.com/vllm-project/vllm/pull/57652) expand KV-offload replicated_layout detection to multi-group MLA
- [#50499](https://github.com/vllm-project/vllm/pull/50499) packed MLA KV layouts in PP push prefill (NIXL)
- [#57700](https://github.com/vllm-project/vllm/pull/57700) K3 DSpark hybrid READ for MoRIIO
- [#49300](https://github.com/vllm-project/vllm/pull/49300) CUSTOM_MEM_POOL support for Mooncake
- [#57251](https://github.com/vllm-project/vllm/pull/57251) Prometheus metrics for SimpleCPUOffloadConnector
- [#59139](https://github.com/vllm-project/vllm/pull/59139) PP with PCP in MRV2
- [#55477](https://github.com/vllm-project/vllm/pull/55477) Fast Start PP support
- [#57298](https://github.com/vllm-project/vllm/pull/57298) charge daemon-held weights against gpu_memory_utilization
- [#58946](https://github.com/vllm-project/vllm/pull/58946) bound UniProc EngineCore startup threads to available CPUs
- [#58411](https://github.com/vllm-project/vllm/pull/58411) randomized dummy inputs in MRV2

</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#57172](https://github.com/vllm-project/vllm/pull/57172) dispatch nn.LayerNorm to a fused SYCL kernel on XPU
- [#54874](https://github.com/vllm-project/vllm/pull/54874) preserve non-contiguous strides when pinning CPU tensors for UVA on XPU
- [#58693](https://github.com/vllm-project/vllm/pull/58693) video inference via torchcodec on s390x
- [#58796](https://github.com/vllm-project/vllm/pull/58796) include vLLM Recipes tooling in the CPU release image

</details>

<details>
<summary>API & serving (35)</summary>

- [#59005](https://github.com/vllm-project/vllm/pull/59005) Rust frontend `hf` parser for response templates
- [#59143](https://github.com/vllm-project/vllm/pull/59143) replay roundtrip output grammars through XGrammar (Rust frontend)
- [#59395](https://github.com/vllm-project/vllm/pull/59395) split argument grammars into schema resolution and per-model rendering
- [#59393](https://github.com/vllm-project/vllm/pull/59393) snapshot structural-tag grammars as readable outlines
- [#58358](https://github.com/vllm-project/vllm/pull/58358) token-aware marker parsing for Kimi K3 (Rust)
- [#58357](https://github.com/vllm-project/vllm/pull/58357) anchor tokens after pending UTF-8 bytes (Rust)
- [#59004](https://github.com/vllm-project/vllm/pull/59004) relax schema-aware tool argument conversion (Rust)
- [#59048](https://github.com/vllm-project/vllm/pull/59048) attributed input for Rust parser tests and benchmarks
- [#59316](https://github.com/vllm-project/vllm/pull/59316) Shutdown control RPC for the Rust frontend
- [#59020](https://github.com/vllm-project/vllm/pull/59020) support raise_exception in chat templates (Rust)
- [#58602](https://github.com/vllm-project/vllm/pull/58602) port chat_parsing core from Transformers
- [#58603](https://github.com/vllm-project/vllm/pull/58603) enrich chat_parsing streaming events
- [#50584](https://github.com/vllm-project/vllm/pull/50584) DRY as a custom logits processor example in MRV2
- [#54335](https://github.com/vllm-project/vllm/pull/54335) fixed-token prefill scoring
- [#54628](https://github.com/vllm-project/vllm/pull/54628) Responses API backend for `vllm bench serve`
- [#57305](https://github.com/vllm-project/vllm/pull/57305) sweep warmup and failure recovery for benchmarks
- [#52864](https://github.com/vllm-project/vllm/pull/52864) align sleep-mode API responses and operation metrics
- [#51350](https://github.com/vllm-project/vllm/pull/51350) weight checker dev endpoint
- [#55781](https://github.com/vllm-project/vllm/pull/55781) track HTTP weight operation outcomes and concurrency
- [#56807](https://github.com/vllm-project/vllm/pull/56807) context deduplication for watermarked speculative decoding
- [#48867](https://github.com/vllm-project/vllm/pull/48867) --custom-histogram-buckets option
- [#58739](https://github.com/vllm-project/vllm/pull/58739) built-in JSON log formatter
- [#55128](https://github.com/vllm-project/vllm/pull/55128) switch Python Harmony dependency to oss-harmony
- [#58019](https://github.com/vllm-project/vllm/pull/58019) strict MiMo-V2.6 tool calling
- [#58552](https://github.com/vllm-project/vllm/pull/58552) /health endpoint for the weight cache daemon
- [#57766](https://github.com/vllm-project/vllm/pull/57766) variable num_labels for LoRA sequence classification
- [#55029](https://github.com/vllm-project/vllm/pull/55029) attach resolved logprobs to streaming derender chunks
- [#59079](https://github.com/vllm-project/vllm/pull/59079) stock torch.compile mode in MRV2
- [#48133](https://github.com/vllm-project/vllm/pull/48133) tag torch.compile log lines with the component being compiled
- [#59247](https://github.com/vllm-project/vllm/pull/59247) warn when temperature is left to the server default (Rust benchmark)
- [#58003](https://github.com/vllm-project/vllm/pull/58003) API compatibility checking skill
- [#57084](https://github.com/vllm-project/vllm/pull/57084) PR checklist skill for coding agents
- [#58646](https://github.com/vllm-project/vllm/pull/58646) ROCm added to the kernel-microbenchmark skill
- [#59357](https://github.com/vllm-project/vllm/pull/59357) authenticate shared-memory multimodal cache handles
- [#59335](https://github.com/vllm-project/vllm/pull/59335) include the LoRA path in prefix-cache block hashes

</details>

<details>
<summary>Bugfixes (60)</summary>

- [#59235](https://github.com/vllm-project/vllm/pull/59235) HiSparse MTP verification via a union residency kernel
- [#59036](https://github.com/vllm-project/vllm/pull/59036) never allocate GPU pages without host backing (HiSparse)
- [#59007](https://github.com/vllm-project/vllm/pull/59007) preserve host prefix publication after request completion (HiSparse)
- [#59282](https://github.com/vllm-project/vllm/pull/59282) adopt GPU prefix copies after the hit's allocation (HiSparse)
- [#59495](https://github.com/vllm-project/vllm/pull/59495) switch to host reads once a request fills its admission window (HiSparse)
- [#56372](https://github.com/vllm-project/vllm/pull/56372) fix flat/scoped mm_processor_kwargs merge
- [#56086](https://github.com/vllm-project/vllm/pull/56086) support response_format with tool_choice=auto
- [#50502](https://github.com/vllm-project/vllm/pull/50502) enforce parallel_tool_calls=false in the required-tool grammar
- [#59298](https://github.com/vllm-project/vllm/pull/59298) honor parallel_tool_calls=false in the Responses API
- [#59307](https://github.com/vllm-project/vllm/pull/59307) build the streamed final Responses object from streamed items
- [#59173](https://github.com/vllm-project/vllm/pull/59173) ignore reused prompt token ids for media in /v1/responses
- [#55771](https://github.com/vllm-project/vllm/pull/55771) validate reused prompt token ids; render messages for media and echo
- [#58927](https://github.com/vllm-project/vllm/pull/58927) count Responses reasoning tokens per tool round
- [#55596](https://github.com/vllm-project/vllm/pull/55596) preserve built-in tool output call IDs
- [#47598](https://github.com/vllm-project/vllm/pull/47598) report named Anthropic tool calls as tool_use
- [#59419](https://github.com/vllm-project/vllm/pull/59419) strip the x-anthropic-billing-header from chat completions
- [#58958](https://github.com/vllm-project/vllm/pull/58958) apply Harmony adjust_request in batched chat completions
- [#50300](https://github.com/vllm-project/vllm/pull/50300) fix chat template resource-exhaustion DoS
- [#59236](https://github.com/vllm-project/vllm/pull/59236) return 400 for malformed RL dev route bodies
- [#55935](https://github.com/vllm-project/vllm/pull/55935) preserve sampling masks in DELTA and TITO streaming
- [#54442](https://github.com/vllm-project/vllm/pull/54442) don't sample structured-output requests from an unmasked row
- [#43931](https://github.com/vllm-project/vllm/pull/43931) clear stale allowed_token_ids mask in InputBatch.condense
- [#51810](https://github.com/vllm-project/vllm/pull/51810) route Step3p5 forced tool choices through the XML parser
- [#49602](https://github.com/vllm-project/vllm/pull/49602) hoist $defs in Cohere parser tool schema
- [#47512](https://github.com/vllm-project/vllm/pull/47512) avoid JSON constraints for native tool parsers
- [#56994](https://github.com/vllm-project/vllm/pull/56994) force reasoning mode for GLM-5.3 templates in the GLM MoE parser
- [#59205](https://github.com/vllm-project/vllm/pull/59205) skip engine-derived metrics under --disable-log-stats (Rust)
- [#58956](https://github.com/vllm-project/vllm/pull/58956) account for new requests in DP routing (Rust)
- [#59251](https://github.com/vllm-project/vllm/pull/59251) stop vllm-bench chat latency at the last token (Rust)
- [#58643](https://github.com/vllm-project/vllm/pull/58643) fix Rust frontend startup with a config-only model
- [#58919](https://github.com/vllm-project/vllm/pull/58919) retry Mooncake bootstrap registration on timeout
- [#58967](https://github.com/vllm-project/vllm/pull/58967) keep Mooncake bootstrap ports bound during startup on ROCm
- [#50047](https://github.com/vllm-project/vllm/pull/50047) release a dead peer's NIXL state without waiting for TTL
- [#51899](https://github.com/vllm-project/vllm/pull/51899) tag prefix-cache extra keys by source
- [#59175](https://github.com/vllm-project/vllm/pull/59175) fix mamba prefill checkpoint block reservation and eviction in align mode
- [#59536](https://github.com/vllm-project/vllm/pull/59536) keep GDN prefill checkpoint metadata local to each cache group
- [#58784](https://github.com/vllm-project/vllm/pull/58784) reject draft slots that were never proposed (MRV2 spec decode)
- [#58921](https://github.com/vllm-project/vllm/pull/58921) per-module LM heads for multi-layer MTP on MRV2
- [#57197](https://github.com/vllm-project/vllm/pull/57197) MiniMax-M3 EAGLE3 aux-state relay at PP>1
- [#58648](https://github.com/vllm-project/vllm/pull/58648) share target embeddings with MTP under PP (MiniMax M3)
- [#57568](https://github.com/vllm-project/vllm/pull/57568) implement get_top_tokens() on the ROCm DeepSeek V4 MTP drafter
- [#59373](https://github.com/vllm-project/vllm/pull/59373) pick a worst-case DeepSeek-V4 VL dummy image size
- [#55647](https://github.com/vllm-project/vllm/pull/55647) take GLM-5.3-Flash video placeholder timestamps from the pixel path's frame sampler
- [#55222](https://github.com/vllm-project/vllm/pull/55222) GLM-5.3-Flash fp8 plan dtype on SM90 sparse MLA and indexer prefill workspace sizing
- [#58904](https://github.com/vllm-project/vllm/pull/58904) GLM-5.2 shared-expert fusion and MTP on the ROCm DSA path
- [#58058](https://github.com/vllm-project/vllm/pull/58058) drop -1 sentinels in ragged sparse-MLA indices (ROCm)
- [#58887](https://github.com/vllm-project/vllm/pull/58887) race on AITER MLA FP8 prefill scheduling metadata under async scheduling
- [#58182](https://github.com/vllm-project/vllm/pull/58182) compiled ViT attention output layouts
- [#58364](https://github.com/vllm-project/vllm/pull/58364) TorchCodec audio IO correctness
- [#58950](https://github.com/vllm-project/vllm/pull/58950) moe_wna16 w13 zero-point shard split for 8-bit asym GPTQ
- [#57163](https://github.com/vllm-project/vllm/pull/57163) stop sleep(level=2) from zeroing compressed-tensors KV scales
- [#58360](https://github.com/vllm-project/vllm/pull/58360) detect the CUDA toolkit the way FlashInfer does in has_flashinfer()
- [#58498](https://github.com/vllm-project/vllm/pull/58498) don't sync-police or retry FlashInfer all-reduce workspace creation in eager mode
- [#52142](https://github.com/vllm-project/vllm/pull/52142) standalone torch.compile cache loading after relocation
- [#59029](https://github.com/vllm-project/vllm/pull/59029) schedule encoder-only prompts larger than one step
- [#58259](https://github.com/vllm-project/vllm/pull/58259) resumable request + async scheduling handoff race
- [#57447](https://github.com/vllm-project/vllm/pull/57447) preserve logprobs across streaming continuations
- [#57648](https://github.com/vllm-project/vllm/pull/57648) add_dp_placement_groups does not require ray[default]
- [#58611](https://github.com/vllm-project/vllm/pull/58611) pass stateless process-group timeouts explicitly
- [#58747](https://github.com/vllm-project/vllm/pull/58747) preserve application log record factories
- [#59107](https://github.com/vllm-project/vllm/pull/59107) narrower canvas with sync scheduling for DiffusionGemma on CPU
- [#59125](https://github.com/vllm-project/vllm/pull/59125) revert the DSA candidate-block torch.topk replacement (reverts [#58208](https://github.com/vllm-project/vllm/pull/58208))

</details>

<details>
<summary>Tests (7)</summary>

- [#58125](https://github.com/vllm-project/vllm/pull/58125) deflake the shutdown wait-timeout test
- [#59507](https://github.com/vllm-project/vllm/pull/59507) deflake the multi-API-server metrics test and Mooncake PD ports
- [#58269](https://github.com/vllm-project/vllm/pull/58269) make XPU test_mamba_prefix_cache block-size agnostic
- [#58239](https://github.com/vllm-project/vllm/pull/58239) mypy typing for Ultravox and Unlimited-OCR models
- [#58251](https://github.com/vllm-project/vllm/pull/58251) mypy typing for Voxtral and vision models
- [#58254](https://github.com/vllm-project/vllm/pull/58254) mypy typing for Whisper models
- plus the mypy test-dir sweeps [#55939](https://github.com/vllm-project/vllm/pull/55939), [#51043](https://github.com/vllm-project/vllm/pull/51043), [#59428](https://github.com/vllm-project/vllm/pull/59428)

</details>

<details>
<summary>CI & build (16)</summary>

- [#55840](https://github.com/vllm-project/vllm/pull/55840) async scheduling accuracy tests for spec decode
- [#57237](https://github.com/vllm-project/vllm/pull/57237) split H200 MIG Spec Decode Speculators + MTP into 4 named jobs
- [#50519](https://github.com/vllm-project/vllm/pull/50519) missing ROCm test coverage for upstream parity
- [#59137](https://github.com/vllm-project/vllm/pull/59137) expand MI355 mirrors and route MIG-sized jobs to DPX
- [#58683](https://github.com/vllm-project/vllm/pull/58683) mirror large-model GSM8K evaluations on MI355
- [#58433](https://github.com/vllm-project/vllm/pull/58433) mirror generic GEMM-RS/AR on MI355
- [#58654](https://github.com/vllm-project/vllm/pull/58654) mirror split kernel groups on MI355
- [#58284](https://github.com/vllm-project/vllm/pull/58284) MI355 TP2 AR-RMS and B200 fusion mirrors
- [#58055](https://github.com/vllm-project/vllm/pull/58055) allowlist-shrink batch 1 in misc.yaml
- [#59066](https://github.com/vllm-project/vllm/pull/59066) bound the CRCR report by build age
- [#59315](https://github.com/vllm-project/vllm/pull/59315) and [#59249](https://github.com/vllm-project/vllm/pull/59249) bump Dependabot and security packages
- [#58652](https://github.com/vllm-project/vllm/pull/58652) shard Pooling entrypoints into named jobs, reverted by [#59011](https://github.com/vllm-project/vllm/pull/59011)
- [#59256](https://github.com/vllm-project/vllm/pull/59256) remove duplicate MI355 DPX jobs
- [#59595](https://github.com/vllm-project/vllm/pull/59595) drop four no-GPU CPU groups from the legacy AMD pipeline
- [#56073](https://github.com/vllm-project/vllm/pull/56073) upgrade MoRI for WideEP DP16 CI

</details>

<details>
<summary>Refactors (3)</summary>

- [#58997](https://github.com/vllm-project/vllm/pull/58997) remove deprecated mamba_cache_mode "all"
- [#58916](https://github.com/vllm-project/vllm/pull/58916) remove dead test code
- [#58983](https://github.com/vllm-project/vllm/pull/58983) move DeepSeek-V4/V4.1 multi-stream overlap gate to the ROCm platform

</details>

<details>
<summary>Newly opened (in progress) (selected)</summary>

- [#59281](https://github.com/vllm-project/vllm/pull/59281), [#59276](https://github.com/vllm-project/vllm/pull/59276), [#59275](https://github.com/vllm-project/vllm/pull/59275) UMBP KV connector (layer-wise loading, distributed mode, standalone mode), about 35k added lines in total
- [#59168](https://github.com/vllm-project/vllm/pull/59168) pluggable EPLB expert placement and replica routing
- [#59132](https://github.com/vllm-project/vllm/pull/59132) ROCM_SEGMENTED_ATTN backend for RDNA3/3.5/4
- [#59209](https://github.com/vllm-project/vllm/pull/59209) HiSparse for QSA
- [#59366](https://github.com/vllm-project/vllm/pull/59366) fused CUDA MTP kernel for GDN RecoverSSM verify
- [#59304](https://github.com/vllm-project/vllm/pull/59304) and [#59303](https://github.com/vllm-project/vllm/pull/59303) PCP for hybrid GLM KDA and sparse MLA
- [#59059](https://github.com/vllm-project/vllm/pull/59059) layer-sharded MLA cache with NCCL broadcast (KVPP)
- [#59561](https://github.com/vllm-project/vllm/pull/59561) and [#59258](https://github.com/vllm-project/vllm/pull/59258) CuTe DSL all-reduce epilogues and fusion backend
- [#59010](https://github.com/vllm-project/vllm/pull/59010) SM90 native sparse prefill for QSA
- [#59418](https://github.com/vllm-project/vllm/pull/59418), [#59532](https://github.com/vllm-project/vllm/pull/59532), [#59131](https://github.com/vllm-project/vllm/pull/59131), [#59488](https://github.com/vllm-project/vllm/pull/59488) DSv4.1 perf (small-head decode, CUDA-graphed replay layers, KV gather, Humming MXFP4)
- [#59384](https://github.com/vllm-project/vllm/pull/59384) and [#59467](https://github.com/vllm-project/vllm/pull/59467) NVFP4 quant fusions (ReLU2; GELU-tanh+Mul for Gemma)
- [#59128](https://github.com/vllm-project/vllm/pull/59128) and [#59044](https://github.com/vllm-project/vllm/pull/59044) skip padded work in DeepGEMM experts
- [#59342](https://github.com/vllm-project/vllm/pull/59342) nvfp4_ds_mla on FlashInfer MLA sparse
- [#59300](https://github.com/vllm-project/vllm/pull/59300) NVFP4 KV cache for MiniMax-M3 MSA
- [#59243](https://github.com/vllm-project/vllm/pull/59243) experimental dynamic TP reconfiguration
- [#59486](https://github.com/vllm-project/vllm/pull/59486) and [#59604](https://github.com/vllm-project/vllm/pull/59604) ModelOpt IQ2/Q8_0 via b12x (two PRs for the same change)
- [#59531](https://github.com/vllm-project/vllm/pull/59531) and [#59479](https://github.com/vllm-project/vllm/pull/59479) gfx1151 W8A8 skinny GEMM (two PRs for the same change)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 9732fe8be380820fd2d87a58201a2aceec4d78838e87e9c2febd443091fe5533 -->
