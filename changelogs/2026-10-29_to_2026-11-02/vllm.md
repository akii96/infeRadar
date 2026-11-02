# vllm: PR digest (2026-10-29 to 2026-11-02)

_249 merged, 445 newly opened - source vllm-project/vllm, generated 2026-11-02T00:39:23Z_

## TL;DR
- **DeepSeek (V3.2/V4/V4.1) got the most attention (57 labels).** Merged work covered Engram host-table sharing, a compressed-KV gather, ROCm gfx950 mono decode and SWA replay, and PCP with PP/DP. Newly opened work adds Hopper-specialized V4.1-Flash decode (`[#64893](https://github.com/vllm-project/vllm/pull/64893)`) and more ROCm mono/K2 tuning.
- **Perf work centered on small-batch decode and sparse attention.** Merged: a fused scoring+top-k sparse-indexer prefill kernel without materialized logits, BF16 persistent top-k, fused norm+quant for Qwen3.5, and SM100 GLM low-latency BF16 GEMM. Open: W8A16 skinny GEMMs for block-FP8 on Hopper, sorted-A TMA FP8 MoE (reported 6-7.6% E2E on GLM-5.3), and MoE-LoRA kernel tuning.
- **New model enablement is broad.** MiniMax-M3.1-Flash with kernels, Ming3-ASR, Canary STT and Step-5 on ROCm are merged. Mistral Large 4 (`[#64534](https://github.com/vllm-project/vllm/pull/64534)`) is the largest open PR, with a merged recipe; Muse Spark, Qwen3.8 and Qwen4Exp saw MoE, NVFP4/MXFP4 and ROCm work.
- **Direction:** a Rust frontend reaching Python parity, MRV2 (model runner V2) extended to spec-decode, CPU and DBO, and KV-transfer/offload hardening (NIXL, Mooncake, MoRIIO), plus heavy ROCm gfx942/gfx950 investment.

## Most important PRs
**[#64111](https://github.com/vllm-project/vllm/pull/64111) - New MiniMax-M3.1-Flash model and kernels**
Adds the model, attention/MoE/quant kernels and spec-decode support in one 29k-line change spanning NVIDIA and AMD. It is the largest merged feature of the window.

**[#60618](https://github.com/vllm-project/vllm/pull/60618) - Single-launch fused scoring+top-k for sparse-indexer prefill**
Computes indexer scores and top-k in one kernel without materializing the logits tensor. This cuts memory and launch overhead for DSA-style sparse attention prefill.

**[#61995](https://github.com/vllm-project/vllm/pull/61995) - Enable MRv2 for non-triton CPU backends**
Brings Model Runner V2 to CPU, moving the new runner closer to feature parity across hardware.

**[#63205](https://github.com/vllm-project/vllm/pull/63205) - MRV2 speculator config classes and custom speculators**
Introduces a config-driven speculator framework in MRV2. The open `[#64844](https://github.com/vllm-project/vllm/pull/64844)` builds on it with a speculative round contract.

**[#46370](https://github.com/vllm-project/vllm/pull/46370) - Fault-tolerant EP via scale-down**
Initial support for expert parallelism that shrinks the EP group on failure instead of taking the engine down.

## More changes by area

<details>
<summary>Performance (29)</summary>

- [#63842](https://github.com/vllm-project/vllm/pull/63842) compute prompt block hashes in the Rust frontend
- [#64509](https://github.com/vllm-project/vllm/pull/64509) fused norm+quant and gate+quant for Qwen3.5 on NVIDIA
- [#64138](https://github.com/vllm-project/vllm/pull/64138) read BF16 logits directly in persistent top-k for DSA
- [#60103](https://github.com/vllm-project/vllm/pull/60103) HiSparse fused slot invalidation and shorter resolver path
- [#62009](https://github.com/vllm-project/vllm/pull/62009) symm_mem EPLB weight-migration backend and fused MegaMoE replica mapping for DSv4
- [#62359](https://github.com/vllm-project/vllm/pull/62359) share Engram host tables as host-NUMA cuMem across DP ranks
- [#59131](https://github.com/vllm-project/vllm/pull/59131) gather compressed KV once per source group in DSv4.1 prefill
- [#64955](https://github.com/vllm-project/vllm/pull/64955) fuse padding skipping in grouped/Muse MoE routing
- [#64653](https://github.com/vllm-project/vllm/pull/64653) use MoE-LoRA shrink/expand kernels for up to 64 tokens
- [#64638](https://github.com/vllm-project/vllm/pull/64638) fuse all-gather and norm for Muse Spark hybrid MoE
- [#64419](https://github.com/vllm-project/vllm/pull/64419) allocate GDN output uninitialized and write FlashInfer prefill in place
- [#64425](https://github.com/vllm-project/vllm/pull/64425) overlap Qwen3.5 GDN in_proj_ba on the aux stream
- [#62956](https://github.com/vllm-project/vllm/pull/62956) SM121 TP=2 skinny-GEMM plans for GLM-5.3-Flash
- [#64481](https://github.com/vllm-project/vllm/pull/64481) GLM low-latency BF16 GEMM on SM100
- [#64650](https://github.com/vllm-project/vllm/pull/64650) SM103 skinny GEMM plans for Qwen3.8 TP=1
- [#57770](https://github.com/vllm-project/vllm/pull/57770) split-vocab Triton argmax for the DSpark greedy draft
- [#64269](https://github.com/vllm-project/vllm/pull/64269) batched token heads for ColBERT reranking
- [#64841](https://github.com/vllm-project/vllm/pull/64841) lower peak memory for chunked prompt logprobs (MRV2)
- [#64674](https://github.com/vllm-project/vllm/pull/64674) incremental decode of streamed custom-tool input
- [#63005](https://github.com/vllm-project/vllm/pull/63005) build run-batch TypeAdapters once
- [#64673](https://github.com/vllm-project/vllm/pull/64673) skip tool-argument conversions after a replaced value
- [#63927](https://github.com/vllm-project/vllm/pull/63927) keep offload event metadata out of the cyclic GC
- [#59322](https://github.com/vllm-project/vllm/pull/59322) avoid repeated hash-prefix scans in KV offload
- [#60477](https://github.com/vllm-project/vllm/pull/60477) all-reduce partial hidden_states before the PP send in DSA
- [#64094](https://github.com/vllm-project/vllm/pull/64094) prefix-cache SWA replay on gfx950 for DSv4.1
- [#64101](https://github.com/vllm-project/vllm/pull/64101) mono decode at TP8 on MI355X
- [#63885](https://github.com/vllm-project/vllm/pull/63885) build SWA decode metadata in one launch on ROCm
- [#64004](https://github.com/vllm-project/vllm/pull/64004) cut gfx942 MXFP4-to-int4 requant time under pure TP
- [#63915](https://github.com/vllm-project/vllm/pull/63915) fuse MXFP8 activation quant into the 1x32 dot_scaled linear (M<=16)
- [#64008](https://github.com/vllm-project/vllm/pull/64008) reuse compiled FlyDSL host launchers

</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#64553](https://github.com/vllm-project/vllm/pull/64553) CUDA routing kernel for Muse Spark Open
- [#64037](https://github.com/vllm-project/vllm/pull/64037) SM90 split-K in the Triton indexer for MiniMax-M3
- [#64494](https://github.com/vllm-project/vllm/pull/64494) size-gated PDL for silu_and_mul_nvfp4_quant
- [#64064](https://github.com/vllm-project/vllm/pull/64064) ROCm AITER unified attention for MiMo-V2.6
- [#63761](https://github.com/vllm-project/vllm/pull/63761) fix int32 token-offset overflows in Qwen3.5 attention and GDN prefill kernels
- [#56155](https://github.com/vllm-project/vllm/pull/56155) resolve per-layer KV dtype in the attention runtime
- [#62990](https://github.com/vllm-project/vllm/pull/62990) DSpark adaptive verification with DCP on ROCM_AITER_MLA
- [#60229](https://github.com/vllm-project/vllm/pull/60229) adaptive verification for GLM-5.3-Flash spec decode

</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#64378](https://github.com/vllm-project/vllm/pull/64378) ROCm NVFP4 MoE re-quantization and fused shared experts via online quant
- [#64525](https://github.com/vllm-project/vllm/pull/64525) hybrid MegaMoE/TRT-LLM execution for Muse Spark NVFP4
- [#63179](https://github.com/vllm-project/vllm/pull/63179) fuse tiny-M MXFP8 quant into the block32 GEMM on ROCm
- [#61529](https://github.com/vllm-project/vllm/pull/61529) fp8 KV and indexer caches on the AMD QSA path
- [#64368](https://github.com/vllm-project/vllm/pull/64368) draft_lm_head_quantization for DSpark drafters on ROCm
- [#62192](https://github.com/vllm-project/vllm/pull/62192) pin FlashInfer FP8 bmm and W4A16 NVFP4 kernels for batch invariance
- [#65000](https://github.com/vllm-project/vllm/pull/65000) combine the NVFP4 linear overrides for batch invariance

</details>

<details>
<summary>Model support (9)</summary>

- [#63585](https://github.com/vllm-project/vllm/pull/63585) Ming3-ASR
- [#64215](https://github.com/vllm-project/vllm/pull/64215) NVIDIA Canary speech-to-text
- [#61837](https://github.com/vllm-project/vllm/pull/61837) Step-5-Preview on ROCm
- [#62424](https://github.com/vllm-project/vllm/pull/62424) native GLM-5.3 chat rendering in the Rust frontend
- [#64071](https://github.com/vllm-project/vllm/pull/64071) metadata-only image/video inputs for GLM-5.3-Flash
- [#58468](https://github.com/vllm-project/vllm/pull/58468) update the RADIO vision encoder to the current Transformers version
- [#51012](https://github.com/vllm-project/vllm/pull/51012) deprecate torch.compile for Qwen3.5
- [#64110](https://github.com/vllm-project/vllm/pull/64110) remove the FlashAttention dependency in Qwen4Exp
- [#59958](https://github.com/vllm-project/vllm/pull/59958) PLE disk offload for Qwen4Exp

</details>

<details>
<summary>Parallelism & scheduling (14)</summary>

- [#61361](https://github.com/vllm-project/vllm/pull/61361) MORI EP V2 support
- [#63098](https://github.com/vllm-project/vllm/pull/63098) enable PCP with PP or DP for DSv4.1
- [#64356](https://github.com/vllm-project/vllm/pull/64356) batch-sharded draft logits refactor
- [#63886](https://github.com/vllm-project/vllm/pull/63886) batch-sharded sequential block for DSpark
- [#63219](https://github.com/vllm-project/vllm/pull/63219) per-request draft retention for structured output under PP
- [#64458](https://github.com/vllm-project/vllm/pull/64458) fix MRV2 PP spec-decode broadcast
- [#64457](https://github.com/vllm-project/vllm/pull/64457) keep offline DP ranks' collectives aligned under async scheduling
- [#30614](https://github.com/vllm-project/vllm/pull/30614) default EPLB num_redundant_experts to the minimum valid value
- [#63275](https://github.com/vllm-project/vllm/pull/63275) trace replay with speculative decoding
- [#62111](https://github.com/vllm-project/vllm/pull/62111) fix multi-layer MTP module selection for Qwen3.5/Qwen3-Next
- [#64751](https://github.com/vllm-project/vllm/pull/64751) honor draft MoE/attention backend overrides for MRV2 standalone drafts
- [#64830](https://github.com/vllm-project/vllm/pull/64830) move V2-only checks into V1 unsupported features
- [#64338](https://github.com/vllm-project/vllm/pull/64338) fix FlashInfer attention warmup deadlock under PP>1
- [#59961](https://github.com/vllm-project/vllm/pull/59961) carry shared indexer top-k across PP stages (DSv3.2)

</details>

<details>
<summary>KV cache, connectors & offload (24)</summary>

- [#54307](https://github.com/vllm-project/vllm/pull/54307) heterogeneous TP sharing for hybrid KV cache in Mooncake Store
- [#63416](https://github.com/vllm-project/vllm/pull/63416) pair NIXL KV regions by layer
- [#64193](https://github.com/vllm-project/vllm/pull/64193) renew Mooncake prefill KV leases from the decoder
- [#63513](https://github.com/vllm-project/vllm/pull/63513) Mooncake skip padding in stored KV blocks
- [#59934](https://github.com/vllm-project/vllm/pull/59934) sleep mode with MooncakeStoreConnector
- [#60867](https://github.com/vllm-project/vllm/pull/60867) MoRIIO hybrid READ for multiple attention groups
- [#62905](https://github.com/vllm-project/vllm/pull/62905) NIXL ucx_backend_params key
- [#64582](https://github.com/vllm-project/vllm/pull/64582) fix NIXL Mamba region stride on block-outermost layouts
- [#57662](https://github.com/vllm-project/vllm/pull/57662) dedup NIXL transfer regions by (base_addr, block_len)
- [#52838](https://github.com/vllm-project/vllm/pull/52838) GPU-CPU KV transfer fault degrades the cache instead of killing the engine
- [#63618](https://github.com/vllm-project/vllm/pull/63618) let idle P2P-only engines park
- [#64256](https://github.com/vllm-project/vllm/pull/64256) fail timed-out P2P loads at once
- [#64251](https://github.com/vllm-project/vllm/pull/64251) fault a peer whose source WRITE stalls
- [#63566](https://github.com/vllm-project/vllm/pull/63566) pin shared-prefix junction on sparse-group offload cuts
- [#62979](https://github.com/vllm-project/vllm/pull/62979) reserve in-flight HiSparse imports' host pages at admission
- [#62444](https://github.com/vllm-project/vllm/pull/62444) refresh CPU LRU for GPU-hit prefixes in SimpleCPUOffload
- [#64400](https://github.com/vllm-project/vllm/pull/64400) dedupe in-flight partial-tail loads
- [#63249](https://github.com/vllm-project/vllm/pull/63249) preserve stored-event prefix order
- [#63937](https://github.com/vllm-project/vllm/pull/63937) skip offload of partial blocks from errored requests
- [#63788](https://github.com/vllm-project/vllm/pull/63788) keep completed transfers when telemetry is unavailable
- [#59099](https://github.com/vllm-project/vllm/pull/59099) make reset_cache re-entrant
- [#62613](https://github.com/vllm-project/vllm/pull/62613) self-describing events for recurrent state groups
- [#63695](https://github.com/vllm-project/vllm/pull/63695) carry request context on raw stored events
- [#63900](https://github.com/vllm-project/vllm/pull/63900), [#62930](https://github.com/vllm-project/vllm/pull/62930) offload cleanup and a guard rejecting secondary tiers on multi-node engines

</details>

<details>
<summary>API & serving (26)</summary>

- [#64450](https://github.com/vllm-project/vllm/pull/64450) Rust frontend: handshake owner serves a range of DP ranks
- [#64451](https://github.com/vllm-project/vllm/pull/64451) Rust frontend: hybrid and external DP LB
- [#64232](https://github.com/vllm-project/vllm/pull/64232) Rust frontend: structured access log per response
- [#64218](https://github.com/vllm-project/vllm/pull/64218) Rust frontend: return_weight_versions
- [#64514](https://github.com/vllm-project/vllm/pull/64514) Rust frontend: VLLM_SKIP_MODEL_NAME_VALIDATION
- [#64223](https://github.com/vllm-project/vllm/pull/64223) Rust frontend: --max-log-len
- [#64222](https://github.com/vllm-project/vllm/pull/64222) Rust frontend: --root-path
- [#64526](https://github.com/vllm-project/vllm/pull/64526) Rust frontend: return_prompt_text
- [#64219](https://github.com/vllm-project/vllm/pull/64219), [#64220](https://github.com/vllm-project/vllm/pull/64220), [#64513](https://github.com/vllm-project/vllm/pull/64513), [#64274](https://github.com/vllm-project/vllm/pull/64274), [#64512](https://github.com/vllm-project/vllm/pull/64512) Rust frontend parity fixes (usage details, echo logprobs, generate envelope, template rejection, UMBP metrics)
- [#63896](https://github.com/vllm-project/vllm/pull/63896) thinking_token_budget in the Responses API
- [#64575](https://github.com/vllm-project/vllm/pull/64575) reject Anthropic-defined tools by type in /v1/messages
- [#63594](https://github.com/vllm-project/vllm/pull/63594) probe non-jinja renderers for inline system message support
- [#64503](https://github.com/vllm-project/vllm/pull/64503) enforce request-template trust for structured decisions
- [#64336](https://github.com/vllm-project/vllm/pull/64336) direct weight reload into the live model
- [#64357](https://github.com/vllm-project/vllm/pull/64357) run the model post-load hook once per load/reload
- [#64869](https://github.com/vllm-project/vllm/pull/64869) allow the weights mapper to transform weights
- [#63692](https://github.com/vllm-project/vllm/pull/63692) stop preload groups when a daemon rank exits (Fast Start)
- [#63247](https://github.com/vllm-project/vllm/pull/63247) device-neutral compile cache via compile_on_one_rank
- [#60218](https://github.com/vllm-project/vllm/pull/60218) opt-in infrastructure for OOT plugins
- [#64169](https://github.com/vllm-project/vllm/pull/64169) Mistral parser uses get_grammar_for_chat_request (requires mistral-common 1.13.0)
- #64363 and related small items are omitted from the shown list

</details>

<details>
<summary>Bugfixes (35)</summary>

- [#64279](https://github.com/vllm-project/vllm/pull/64279) fix KV-cache corruption under whole-graph compile (reverts #42129)
- [#63382](https://github.com/vllm-project/vllm/pull/63382) fix NaN logits from uninitialized fused NVFP4 act+quant scales
- [#64999](https://github.com/vllm-project/vllm/pull/64999) restore GDN in_proj_ba overlap on CUDA
- [#63116](https://github.com/vllm-project/vllm/pull/63116) size AITER MLA persistent metadata for every decode query length
- [#63816](https://github.com/vllm-project/vllm/pull/63816) guard NaN scores in gfx942 mono routing
- [#63047](https://github.com/vllm-project/vllm/pull/63047) budget DSv4.1 prefill memory missed by startup profiling
- [#63054](https://github.com/vllm-project/vllm/pull/63054) 64-bit row offsets in the Triton W4A16 GEMM on ROCm
- [#60163](https://github.com/vllm-project/vllm/pull/60163) fix Humming FP8 linear for per-tensor/per-channel weights
- [#51953](https://github.com/vllm-project/vllm/pull/51953) fix DiffusionGemma OOM via tiled logits projection
- [#58780](https://github.com/vllm-project/vllm/pull/58780) stream DeepSeek V4/V3.2 string tool arguments incrementally
- [#64675](https://github.com/vllm-project/vllm/pull/64675) Qwen3 closed tool parameters parsed once while streaming
- [#64535](https://github.com/vllm-project/vllm/pull/64535) GLM-4.7 closed tool arguments parsed once while streaming
- [#64615](https://github.com/vllm-project/vllm/pull/64615) leave GLM-4.7 array/object tool arguments unpinned
- [#61542](https://github.com/vllm-project/vllm/pull/61542) preserve whitespace in HYV4 argument names
- [#62967](https://github.com/vllm-project/vllm/pull/62967) drain in-flight gRPC RPCs within --shutdown-timeout
- [#64630](https://github.com/vllm-project/vllm/pull/64630) exact-size reusable pinned CPU backup for level-1 sleep
- [#63384](https://github.com/vllm-project/vllm/pull/63384) migrate OLMoE to the Transformers backend and fix MoE LoRA
- [#63489](https://github.com/vllm-project/vllm/pull/63489) refuse adapters with LoRA on modules vLLM does not wrap
- [#63174](https://github.com/vllm-project/vllm/pull/63174) skip redundant weight clones for owned-tensor loaders
- [#64495](https://github.com/vllm-project/vllm/pull/64495) preserve multimodal processor-cache hits during eviction
- [#64367](https://github.com/vllm-project/vllm/pull/64367) consume prompt-embedding sentinel IDs before model execution
- [#64362](https://github.com/vllm-project/vllm/pull/64362) chat template fallback for OpenVLA
- [#64105](https://github.com/vllm-project/vllm/pull/64105) MiniCPM OCR downsample mode
- [#64757](https://github.com/vllm-project/vllm/pull/64757) report prompt_tokens_details in batched chat completions
- [#57990](https://github.com/vllm-project/vllm/pull/57990) preserve prompt_logprobs in /v1/completions/derender
- [#61973](https://github.com/vllm-project/vllm/pull/61973) preserve batch audio handler error status codes
- [#64449](https://github.com/vllm-project/vllm/pull/64449) send DP rendezvous in coordinated-DP INIT (Rust frontend)
- [#64390](https://github.com/vllm-project/vllm/pull/64390) Rust vllm-bench rejects --max-concurrency 0
- [#64557](https://github.com/vllm-project/vllm/pull/64557) count tool-call deltas as tokens in Rust vllm-bench
- [#62753](https://github.com/vllm-project/vllm/pull/62753) same token counting fix in Python bench
- [#61777](https://github.com/vllm-project/vllm/pull/61777) aggregate DP running requests for profiling
- [#62674](https://github.com/vllm-project/vllm/pull/62674) retry incomplete HTTP response bodies
- [#57022](https://github.com/vllm-project/vllm/pull/57022) fail loudly instead of a no-op NCCL weight transfer
- [#61380](https://github.com/vllm-project/vllm/pull/61380) resolve HF paths when loading sharded state
- [#48951](https://github.com/vllm-project/vllm/pull/48951), [#63053](https://github.com/vllm-project/vllm/pull/63053), [#63218](https://github.com/vllm-project/vllm/pull/63218), [#54399](https://github.com/vllm-project/vllm/pull/54399), [#63415](https://github.com/vllm-project/vllm/pull/63415), [#64065](https://github.com/vllm-project/vllm/pull/64065), [#60873](https://github.com/vllm-project/vllm/pull/60873) assorted model, XPU, ROCm and compile fixes

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#64733](https://github.com/vllm-project/vllm/pull/64733) MiniMax-M3.1 PP: NIXL pull from PP prefill stages and Q8KV4 prefill workspace on SM10x
- [#59938](https://github.com/vllm-project/vllm/pull/59938) XPU multimodal_rotary_embedding kernel for mrope
- [#62481](https://github.com/vllm-project/vllm/pull/62481) monitor FlyDSL JIT compilation after warmup (ROCm)

</details>

<details>
<summary>Tests (9)</summary>

- [#61794](https://github.com/vllm-project/vllm/pull/61794) UMBP embedded runtime and MORI integration coverage
- [#62996](https://github.com/vllm-project/vllm/pull/62996) un-skip AITER MXFP4 padding-matrix and token-padding tests
- [#62976](https://github.com/vllm-project/vllm/pull/62976) AITER_MOE_SORT_BACKEND MXFP4 DSV4 coverage
- [#64342](https://github.com/vllm-project/vllm/pull/64342) fix mypy for the multimodels tests folder
- [#64532](https://github.com/vllm-project/vllm/pull/64532) lift skinny-GEMM cap in the gfx942 draft lm_head test
- [#64655](https://github.com/vllm-project/vllm/pull/64655) check skinny-GEMM guard dispatch without torch.profiler
- [#63297](https://github.com/vllm-project/vllm/pull/63297) keep KDA prefill checkpoints with the gluon backend
- [#62007](https://github.com/vllm-project/vllm/pull/62007) DeepSeek-V3 NIXL accuracy steps on ROCm
- [#64602](https://github.com/vllm-project/vllm/pull/64602) remove retired A100 queue steps, keep AMD mirrors standalone

</details>

<details>
<summary>CI & build (12)</summary>

- [#61939](https://github.com/vllm-project/vllm/pull/61939) ROCm CI/release revamp: collapse image tiers, unify build pipeline
- [#64779](https://github.com/vllm-project/vllm/pull/64779) upgrade to huggingface_hub 2
- [#64049](https://github.com/vllm-project/vllm/pull/64049) and [#64529](https://github.com/vllm-project/vllm/pull/64529) bump Transformers to 5.21.1 and 5.22.0
- [#64591](https://github.com/vllm-project/vllm/pull/64591), [#64590](https://github.com/vllm-project/vllm/pull/64590) and [#64595](https://github.com/vllm-project/vllm/pull/64595) enroll Kernels, LM Eval and Compile/PyTorch/CUDA/ABI jobs in automatic sharding
- [#64635](https://github.com/vllm-project/vllm/pull/64635) continue PyTorch Fullgraph sharding
- [#64387](https://github.com/vllm-project/vllm/pull/64387) import the merge-base image cache in PR builds
- [#64577](https://github.com/vllm-project/vllm/pull/64577) prebuild mamba-ssm and causal-conv1d in the ROCm CI image
- plus 1 more minor CI update

</details>

<details>
<summary>Docs (14)</summary>

- [#64527](https://github.com/vllm-project/vllm/pull/64527) Mistral-Large-4-1T-A52B recipe
- [#64792](https://github.com/vllm-project/vllm/pull/64792) Mistral Large 4 TP4 and lowest-latency ROCm presets
- [#64821](https://github.com/vllm-project/vllm/pull/64821), [#64909](https://github.com/vllm-project/vllm/pull/64909), [#64910](https://github.com/vllm-project/vllm/pull/64910) MiniMax-M3.1-Flash GB300/GB200 AgentX presets
- [#64805](https://github.com/vllm-project/vllm/pull/64805) MiniMax-M3.1-Flash MI355X TP4 preset
- [#64322](https://github.com/vllm-project/vllm/pull/64322), [#64804](https://github.com/vllm-project/vllm/pull/64804) DeepSeek-V4/V4.1-Flash MI355X AgentX profiles
- [#64665](https://github.com/vllm-project/vllm/pull/64665), [#64617](https://github.com/vllm-project/vllm/pull/64617) Kimi-K3 GB300 and B300 presets
- [#64607](https://github.com/vllm-project/vllm/pull/64607) Qwen3.5-397B B200 NVFP4 TP2 agentic preset
- [#38741](https://github.com/vllm-project/vllm/pull/38741) Scheduler section in the V1 architecture overview
- [#60899](https://github.com/vllm-project/vllm/pull/60899) add k8s-aibom to deployment integrations

</details>

<details>
<summary>Newly opened, in progress (highlights)</summary>

- [#64534](https://github.com/vllm-project/vllm/pull/64534) Add Mistral Large 4 (23k lines, 170 files)
- [#64893](https://github.com/vllm-project/vllm/pull/64893) DeepSeek-V4.1-Flash specialized decode on Hopper (H200 TP4)
- [#64844](https://github.com/vllm-project/vllm/pull/64844) MRV2 speculative round contract for custom speculators
- [#64823](https://github.com/vllm-project/vllm/pull/64823) native gfx950 mxfp4_mla kernel for GLM-5.3-Flash prefill
- [#64631](https://github.com/vllm-project/vllm/pull/64631) shard the MiniMax M3.1 NVFP4 index cache with indexer CP
- [#64671](https://github.com/vllm-project/vllm/pull/64671) Gloo DP/EP for wide expert parallelism on CPU
- [#64983](https://github.com/vllm-project/vllm/pull/64983) and [#64980](https://github.com/vllm-project/vllm/pull/64980) W8A16 skinny GEMMs for block-FP8 on Hopper
- [#64760](https://github.com/vllm-project/vllm/pull/64760) sorted-A TMA FP8 MoE down projection on H200
- [#64464](https://github.com/vllm-project/vllm/pull/64464) HPC-Ops MoE backend for SM120
- [#64699](https://github.com/vllm-project/vllm/pull/64699) Qwen3.5 GDN ReplaySSM standard decode in MRV2
- [#64421](https://github.com/vllm-project/vllm/pull/64421) Elastic EP native local-range resizing
- [#64924](https://github.com/vllm-project/vllm/pull/64924) remove the in-tree LMCache integration
- [#65004](https://github.com/vllm-project/vllm/pull/65004) histogram-bracket top-p sampler for large p-only batches
- [#64528](https://github.com/vllm-project/vllm/pull/64528) bump ruff to 0.17.2 across 279 files

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f03bc82afdf5018e9f38a1394d686c43f9084e4428177e12957ffe79a570fb74 -->
