# vllm: PR digest (2026-10-25 to 2026-10-29)

_383 merged, 647 newly opened - source vllm-project/vllm, generated 2026-10-29T16:26:27Z_

## TL;DR
- **Model attention:** DeepSeek (V4/V4.1) got the most labeled work (74 PRs). MiniMax-M3.1 and Muse Spark were the big new-model landings. Kimi-K3, GLM-5.3-Flash and Qwen4Exp saw heavy decode-kernel and ROCm tuning, and most of that work is still open.
- **Merged perf:** a 3x faster MXFP4 activation-quant kernel ([#63101](https://github.com/vllm-project/vllm/pull/63101)), TMA for MoE up/down proj (+3.1–3.4% E2E on GLM5.3), a CuteDSL BF16x3 router GEMM on Hopper, and DeepGEMM sparse MQA logits on the FP8 indexer cache for DSv4.1. Several MLA/KDA/DSA decode and gather fusions landed on ROCm AITER.
- **Opened but unmerged:** large stacked MonoKernel and specialized-decode series for GLM-5.3-Flash, DSv4.1, Kimi-K3 and Muse Spark. They include MXFP4 KV caches on gfx950 and a claimed 1.5x GB300 decode for Muse Spark ([#64077](https://github.com/vllm-project/vllm/pull/64077)). MegaMoE and HPC-Ops MoE backends for SM90/SM120 are also in review.
- **Direction:** agentic-workload latency and low-precision KV and weights (MXFP4, FP8, NVFP4, 3-bit). KV offload and P2P hardening, Rust frontend parity with Python, and Fast Start weight-cache restarts are the other threads.

## Most important PRs
**[#64111](https://github.com/vllm-project/vllm/pull/64111) New Model: MiniMax-M3.1-Flash with kernels.** Adds the model with attention, MoE, quantization, speculative-decode and multimodal support across FlashInfer, NVIDIA and AMD. It is the largest merged feature of the window.

**[#61879](https://github.com/vllm-project/vllm/pull/61879) Muse Spark Open support.** Lands a new model family with FlashInfer and Triton attention, MoE and quantization paths. Follow-ups ([#64525](https://github.com/vllm-project/vllm/pull/64525), [#63871](https://github.com/vllm-project/vllm/pull/63871)) already add hybrid MegaMoE/TRT-LLM NVFP4 execution and fix dummy-loaded weights.

**[#63638](https://github.com/vllm-project/vllm/pull/63638) Opt-in KV-balanced FP8 MLA decode for Kimi K3 agentic workloads.** Rebalances KV work across decode so long agentic contexts do not leave SMs idle. It is gated behind an opt-in flag.

**[#59774](https://github.com/vllm-project/vllm/pull/59774) ROCM_OCTAVE: native 3-bit KV cache backend for AMD.** Adds a 3-bit KV attention backend, a large capacity gain for long-context serving on ROCm.

**[#63101](https://github.com/vllm-project/vllm/pull/63101) MXFP4 activation quant optimization.** The new kernel is 3x faster and gives about 5% end-to-end throughput, which helps any MXFP4 MoE or linear path.

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#61903](https://github.com/vllm-project/vllm/pull/61903) CuteDSL BF16x3 router GEMM for fp32 router weights on Hopper
- [#63820](https://github.com/vllm-project/vllm/pull/63820) TMA for MoE up/down proj, +3.1–3.4% E2E on GLM5.3
- [#62011](https://github.com/vllm-project/vllm/pull/62011) DeepGEMM sparse MQA logits on the FP8 indexer cache (DSv4.1)
- [#53166](https://github.com/vllm-project/vllm/pull/53166) Fuse Kimi-K3 MLA chunked-context gather on AITER
- [#60110](https://github.com/vllm-project/vllm/pull/60110) Fold q_b_proj and W_UK into one GEMM for Kimi-K3 MLA decode (ROCm)
- [#59668](https://github.com/vllm-project/vllm/pull/59668) Single-launch DSA decode candidate mask on ROCm (DSv4.1)
- [#63018](https://github.com/vllm-project/vllm/pull/63018) Tile the NVFP4 compressed-KV dequant-gather (DSv4.1)
- [#62091](https://github.com/vllm-project/vllm/pull/62091) Read Engram tables from peers' HBM instead of DP collectives
- [#63063](https://github.com/vllm-project/vllm/pull/63063) Stack DeepSeek V4.1 context WKV projections for DSpark
- [#63155](https://github.com/vllm-project/vllm/pull/63155) Capture decoder replay graphs on the model graphs' stream
- [#58305](https://github.com/vllm-project/vllm/pull/58305) Compact FP8 KV rows for NoPE MLA models on SM120
- [#64481](https://github.com/vllm-project/vllm/pull/64481) GLM low-latency BF16 GEMM on SM100
- [#64419](https://github.com/vllm-project/vllm/pull/64419) GDN core output allocated uninitialized, FlashInfer prefill written in place
- [#63342](https://github.com/vllm-project/vllm/pull/63342) block_m=128 for the fused KDA prefill conv1d (Kimi-K3, ROCm)
- [#63633](https://github.com/vllm-project/vllm/pull/63633) MRV2: stage buffers by reference and copy straight into UVA
- [#63789](https://github.com/vllm-project/vllm/pull/63789) Rust frontend: skip detokenization for gRPC requests that read no text
- [#62478](https://github.com/vllm-project/vllm/pull/62478) Vectorize Mooncake transfer descriptor build
- [#63142](https://github.com/vllm-project/vllm/pull/63142) Coalesce descending block ids for Mooncake TE
- [#63889](https://github.com/vllm-project/vllm/pull/63889) Reduce KVCR adapter overhead
- [#61263](https://github.com/vllm-project/vllm/pull/61263) Reduce HiSparse residency hash probes
- [#60710](https://github.com/vllm-project/vllm/pull/60710) Dense weight cache for W4A16 RDNA hybrid prefill
- [#59478](https://github.com/vllm-project/vllm/pull/59478) AITER FlyDSL INT4 QuickReduce

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#57420](https://github.com/vllm-project/vllm/pull/57420) Triton query-tiled sparse prefill for MiniMax-M3, tuned on Hopper
- [#64064](https://github.com/vllm-project/vllm/pull/64064) ROCm AITER unified attention for MiMo-V2.6
- [#60154](https://github.com/vllm-project/vllm/pull/60154) Fuse inverse RoPE and MXFP8 quant into the aiter sparse MLA (DSv4/4.1)
- [#63179](https://github.com/vllm-project/vllm/pull/63179) Fuse tiny-M MXFP8 quant into the block32 GEMM (ROCm)
- [#63915](https://github.com/vllm-project/vllm/pull/63915) Fuse MXFP8 activation quant into the 1x32 dot_scaled linear for M <= 16
- [#63637](https://github.com/vllm-project/vllm/pull/63637) Fuse MXFP8 quant into Gemma input_layernorm for MiniMax-M3.1
- [#62936](https://github.com/vllm-project/vllm/pull/62936) Make persistent TopK exact on candidate overflow
- [#63421](https://github.com/vllm-project/vllm/pull/63421) Replace torch.compile'd AV draft-budget selection with a Triton kernel
- [#62219](https://github.com/vllm-project/vllm/pull/62219) H100 tuned batch-invariant matmul configs for Llama-3.1-8B and Qwen3-8B
- [#63999](https://github.com/vllm-project/vllm/pull/63999) Forward launch grid to Triton kernel overrides
- [#62525](https://github.com/vllm-project/vllm/pull/62525) Gemma 4: skip CUDA-graph padding rows in the routing kernel

</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#61457](https://github.com/vllm-project/vllm/pull/61457) Per-layer fused shared expert selection
- [#61685](https://github.com/vllm-project/vllm/pull/61685) Locality-domain allocation for FlashInfer CuTeDSL NVFP4
- [#62763](https://github.com/vllm-project/vllm/pull/62763) H200 FP8 fused MoE config for Beam-1.0 TP8
- [#51605](https://github.com/vllm-project/vllm/pull/51605) XPU: resize batched Triton MoE tiles and change grid order
- [#59255](https://github.com/vllm-project/vllm/pull/59255) Expert parallelism for AITER Triton W4A16 MoE
- [#62407](https://github.com/vllm-project/vllm/pull/62407) Keep deleted and renamed params registered after process_weights_after_loading
- [#63506](https://github.com/vllm-project/vllm/pull/63506) Fast Start: key weight cache on MoE and linear kernel backends
- [#62133](https://github.com/vllm-project/vllm/pull/62133) Fix OAI Triton MXFP4 MoE on SM110
- [#63698](https://github.com/vllm-project/vllm/pull/63698) Valid ModelOpt NVFP4 MoE dummy scales
- [#63382](https://github.com/vllm-project/vllm/pull/63382) Fix NaN logits from uninitialized fused act+quant scales

</details>

<details>
<summary>Model support (13)</summary>

- [#64282](https://github.com/vllm-project/vllm/pull/64282) Add Nemotron-3.5-Transcribe
- [#63585](https://github.com/vllm-project/vllm/pull/63585) Support Ming3-ASR
- [#60149](https://github.com/vllm-project/vllm/pull/60149) Add Dory support
- [#62201](https://github.com/vllm-project/vllm/pull/62201) Native Lfm2BidirectionalModel
- [#58468](https://github.com/vllm-project/vllm/pull/58468) Update RADIO vision encoder to match current Transformers
- [#61270](https://github.com/vllm-project/vllm/pull/61270) MTP drafts in the Transformers modeling backend
- [#51012](https://github.com/vllm-project/vllm/pull/51012) Deprecate torch.compile for Qwen3.5 models
- [#64287](https://github.com/vllm-project/vllm/pull/64287) Remove Keye-VL and Keye-VL-1.5
- [#57924](https://github.com/vllm-project/vllm/pull/57924) Move Nemotron VL image normalization to device
- [#64525](https://github.com/vllm-project/vllm/pull/64525) Hybrid MegaMoE/TRT-LLM for Muse Spark NVFP4
- [#60234](https://github.com/vllm-project/vllm/pull/60234) Pipeline parallelism for Qwen4Exp PLE models and MTP drafter
- [#61529](https://github.com/vllm-project/vllm/pull/61529) fp8 KV and indexer caches on the AMD QSA path (Qwen4Exp)
- [#63332](https://github.com/vllm-project/vllm/pull/63332) Qwen3.8-Flash-Next MI355X Quark MXFP4 recipe

</details>

<details>
<summary>Parallelism & scheduling (14)</summary>

- [#61589](https://github.com/vllm-project/vllm/pull/61589) Lookahead block hashes for EAGLE prefix caching
- [#61464](https://github.com/vllm-project/vllm/pull/61464) DBO with speculative decoding and DCP on MRV2
- [#61994](https://github.com/vllm-project/vllm/pull/61994) PCP with DSpark for DeepSeek-V4.1
- [#60229](https://github.com/vllm-project/vllm/pull/60229) Adaptive verification for GLM-5.3-Flash
- [#62990](https://github.com/vllm-project/vllm/pull/62990) DSpark adaptive verification with DCP on ROCM_AITER_MLA (Kimi-K3)
- [#64356](https://github.com/vllm-project/vllm/pull/64356) Batch-sharded draft logits refactor
- [#63554](https://github.com/vllm-project/vllm/pull/63554) Batch-sharded draft logits sampling
- [#63275](https://github.com/vllm-project/vllm/pull/63275) Trace replay with speculative decoding
- [#63819](https://github.com/vllm-project/vllm/pull/63819) Close DFlash/DSpark JIT warmup gaps
- [#61258](https://github.com/vllm-project/vllm/pull/61258) Best-effort NUMA binding by default
- [#63256](https://github.com/vllm-project/vllm/pull/63256) RL: declare weight ownership and layout on ParamMeta
- [#62557](https://github.com/vllm-project/vllm/pull/62557) RL: per-update source ranks for NCCL weight transfer
- [#63460](https://github.com/vllm-project/vllm/pull/63460) Share NCCL trainer rendezvous initialization
- [#63237](https://github.com/vllm-project/vllm/pull/63237) Initialize routed-experts capturer before KV profiling

</details>

<details>
<summary>KV cache, offload & connectors (24)</summary>

- [#53902](https://github.com/vllm-project/vllm/pull/53902) Fill kv_offload_config_info with CPU cache capacity
- [#61961](https://github.com/vllm-project/vllm/pull/61961) Load small CPU-tier hits synchronously within the step
- [#63513](https://github.com/vllm-project/vllm/pull/63513) Mooncake store: skip padding in stored KV blocks
- [#59934](https://github.com/vllm-project/vllm/pull/59934) Sleep mode with MooncakeStoreConnector
- [#62905](https://github.com/vllm-project/vllm/pull/62905) ucx_backend_params key for NIXL
- [#62317](https://github.com/vllm-project/vllm/pull/62317) NIXL: read only a group's own regions in hybrid SSM transfers
- [#62592](https://github.com/vllm-project/vllm/pull/62592) HiSparse platform backend for device operations
- [#61793](https://github.com/vllm-project/vllm/pull/61793) UMBP: MORI embedded DRAM runtime and transfer handling
- [#61792](https://github.com/vllm-project/vllm/pull/61792) UMBP: tests for async lookup, hybrid cache, events and metrics
- [#63779](https://github.com/vllm-project/vllm/pull/63779) Let a tier fail a promotion and defer releasing chunks
- [#57646](https://github.com/vllm-project/vllm/pull/57646) Expose processed prefix at request finalization
- [#60469](https://github.com/vllm-project/vllm/pull/60469) Align KVCR cache recency with request prefixes
- [#62930](https://github.com/vllm-project/vllm/pull/62930) Reject secondary tiers on multi-node engines
- [#52838](https://github.com/vllm-project/vllm/pull/52838) AMD: GPU-CPU KV transfer fault degrades cache instead of killing engine
- [#63618](https://github.com/vllm-project/vllm/pull/63618) Let idle P2P-only engines park
- [#64250](https://github.com/vllm-project/vllm/pull/64250) Retain unconfirmed source WRITEs across session teardown
- [#64256](https://github.com/vllm-project/vllm/pull/64256) Fail a timed-out P2P load at once
- [#64251](https://github.com/vllm-project/vllm/pull/64251) Fault a peer whose source WRITE stalls
- [#63207](https://github.com/vllm-project/vllm/pull/63207) Stop DEALER monitor before closing its reader
- [#63628](https://github.com/vllm-project/vllm/pull/63628) Roll back failed P2P NIXL registration
- [#61019](https://github.com/vllm-project/vllm/pull/61019) OffloadingConnector partial tails with EAGLE/MTP groups
- [#62929](https://github.com/vllm-project/vllm/pull/62929) Hold promotions after cache reset until jobs report
- [#61780](https://github.com/vllm-project/vllm/pull/61780) Treat failed secondary-tier stores as back-pressure
- plus 7 more minor KV-offload bugfixes ([#61050](https://github.com/vllm-project/vllm/pull/61050), [#63652](https://github.com/vllm-project/vllm/pull/63652), [#63266](https://github.com/vllm-project/vllm/pull/63266), [#63566](https://github.com/vllm-project/vllm/pull/63566), [#62444](https://github.com/vllm-project/vllm/pull/62444), [#60810](https://github.com/vllm-project/vllm/pull/60810), [#60960](https://github.com/vllm-project/vllm/pull/60960))

</details>

<details>
<summary>API & serving (26)</summary>

- [#63769](https://github.com/vllm-project/vllm/pull/63769) Rust frontend: --enable-log-outputs and --enable-log-deltas
- [#62456](https://github.com/vllm-project/vllm/pull/62456) Rust frontend: one structured outputs backend for every route
- [#61877](https://github.com/vllm-project/vllm/pull/61877) Per-request speculative decoding metrics
- [#63292](https://github.com/vllm-project/vllm/pull/63292) Group prompt-cache usage, report created_cache_tokens
- [#63959](https://github.com/vllm-project/vllm/pull/63959) Export vllm:engine_sleep_state
- [#63962](https://github.com/vllm-project/vllm/pull/63962) Export vllm:num_requests_kv_fetch_by_stage
- [#63767](https://github.com/vllm-project/vllm/pull/63767) Export request metric series at startup
- [#63765](https://github.com/vllm-project/vllm/pull/63765) Report VllmConfig in /server_info
- [#47840](https://github.com/vllm-project/vllm/pull/47840) Configurable HTTP body limit
- [#63963](https://github.com/vllm-project/vllm/pull/63963) Accept list-form chat templates
- [#63964](https://github.com/vllm-project/vllm/pull/63964) Reject max_tokens above max_model_len
- [#63960](https://github.com/vllm-project/vllm/pull/63960) Count gpt-oss reasoning tokens
- [#63764](https://github.com/vllm-project/vllm/pull/63764) Advance streamed completion text_offset
- [#63766](https://github.com/vllm-project/vllm/pull/63766) Serialize unset completions keys as null
- [#63772](https://github.com/vllm-project/vllm/pull/63772) Stream kv_transfer_params on final chunk
- [#63768](https://github.com/vllm-project/vllm/pull/63768) Accept parenthesized and name-only Gemma 4 tool calls
- [#63762](https://github.com/vllm-project/vllm/pull/63762) Separate DeepSeek V4 content blocks
- [#61094](https://github.com/vllm-project/vllm/pull/61094) --reasoning-effort-map
- [#62312](https://github.com/vllm-project/vllm/pull/62312) Rust frontend --reasoning-effort-map
- [#64097](https://github.com/vllm-project/vllm/pull/64097) /v1/completions in run-batch
- [#63812](https://github.com/vllm-project/vllm/pull/63812) Forward response_format to mistral-common
- [#64169](https://github.com/vllm-project/vllm/pull/64169) MistralParser grammar via get_grammar_for_chat_request, requires mistral-common 1.13.0
- [#63569](https://github.com/vllm-project/vllm/pull/63569) Migrate llama3_json parser to parser engine
- [#64186](https://github.com/vllm-project/vllm/pull/64186) Opt-in multi-worker CUDA checkpoint sleep
- [#62570](https://github.com/vllm-project/vllm/pull/62570) Checkpoint lifecycle with HTTP prepare/status/resume
- [#63088](https://github.com/vllm-project/vllm/pull/63088) Fast Start: daemon-to-daemon warmup cache seeding

</details>

<details>
<summary>Bugfixes (28)</summary>

- [#64279](https://github.com/vllm-project/vllm/pull/64279) Fix KV-cache corruption under whole-graph compile (reverts #42129)
- [#58744](https://github.com/vllm-project/vllm/pull/58744) Gather nvfp4_ds_mla chunked-context KV with the NVFP4 kernel
- [#63791](https://github.com/vllm-project/vllm/pull/63791) FlashInfer sparse MLA: at most 65535 tokens per trtllm-gen call
- [#59986](https://github.com/vllm-project/vllm/pull/59986) Keep DSV4.1 sparse prefill out of FULL cudagraphs
- [#63914](https://github.com/vllm-project/vllm/pull/63914) Keep DSV4.1 specialized decode FlashInfer paths on newer FlashInfer
- [#63047](https://github.com/vllm-project/vllm/pull/63047) Budget DSv4.1 prefill memory missed by startup profile
- [#63099](https://github.com/vllm-project/vllm/pull/63099) Match DSv4.1 FP8 config in FSE compatibility check (ROCm)
- [#58780](https://github.com/vllm-project/vllm/pull/58780) Stream DeepSeek V4/V3.2 string tool arguments incrementally
- [#61557](https://github.com/vllm-project/vllm/pull/61557) Preserve grammar-invalid drafts for rejection sampling
- [#53104](https://github.com/vllm-project/vllm/pull/53104) Fix eagle draft sharing with a quantized lm_head
- [#62796](https://github.com/vllm-project/vllm/pull/62796) Align adaptive draft prefill graph padding
- [#60991](https://github.com/vllm-project/vllm/pull/60991) Fuse GLM-5.3 KDA q|k|v convs into one conv1d parameter
- [#59223](https://github.com/vllm-project/vllm/pull/59223) Preserve FP8 indexer WK pairs across load_weights calls
- [#63409](https://github.com/vllm-project/vllm/pull/63409) Pass zero positions to Kimi-K3 fused MLA decode q-prep
- [#62330](https://github.com/vllm-project/vllm/pull/62330) Finalize NIXL DCP interleave size before profiling
- [#57662](https://github.com/vllm-project/vllm/pull/57662) Dedup NIXL transfer regions
- [#63827](https://github.com/vllm-project/vllm/pull/63827) Defer async KV loads on HiSparse decoders
- [#62739](https://github.com/vllm-project/vllm/pull/62739) Read resident HiSparse prefill rows by request state slot
- [#57368](https://github.com/vllm-project/vllm/pull/57368) Release consumed MRV2 CPU inputs
- [#55200](https://github.com/vllm-project/vllm/pull/55200) Reject prompt-wide truncation for Jina ranking
- [#64367](https://github.com/vllm-project/vllm/pull/64367) Consume prompt embedding sentinel IDs before model execution
- [#61636](https://github.com/vllm-project/vllm/pull/61636) Fix double pinning of 3D MoE LoRA
- [#63738](https://github.com/vllm-project/vllm/pull/63738) CPU_ATTN encoder-only attention bidirectional
- [#60514](https://github.com/vllm-project/vllm/pull/60514) Fall back when nvcc is missing
- [#63601](https://github.com/vllm-project/vllm/pull/63601) Keep PIN_MEMORY eager
- [#55699](https://github.com/vllm-project/vllm/pull/55699) Stop SSL certificate watchers on exit
- [#57411](https://github.com/vllm-project/vllm/pull/57411) Bound FunAudioChat runtime audio
- plus 5 more minor fixes ([#59694](https://github.com/vllm-project/vllm/pull/59694), [#58885](https://github.com/vllm-project/vllm/pull/58885), [#60856](https://github.com/vllm-project/vllm/pull/60856), [#61128](https://github.com/vllm-project/vllm/pull/61128), [#63707](https://github.com/vllm-project/vllm/pull/63707), [#64390](https://github.com/vllm-project/vllm/pull/64390), [#64227](https://github.com/vllm-project/vllm/pull/64227), [#63872](https://github.com/vllm-project/vllm/pull/63872), [#63873](https://github.com/vllm-project/vllm/pull/63873), [#61777](https://github.com/vllm-project/vllm/pull/61777))

</details>

<details>
<summary>Docs & recipes (13)</summary>

- [#64527](https://github.com/vllm-project/vllm/pull/64527) Mistral-Large-4-1T-A52B recipe
- [#63552](https://github.com/vllm-project/vllm/pull/63552) Kimi-K3 AgentX lanes as tuned presets
- [#63852](https://github.com/vllm-project/vllm/pull/63852) Kimi-K3 GB300 xPyD and 3P1D DEP16 presets
- [#63520](https://github.com/vllm-project/vllm/pull/63520) Kimi-K3 MI355X recipe alignment
- [#63560](https://github.com/vllm-project/vllm/pull/63560) DeepSeek-V4.1-Flash AgentX presets
- [#64316](https://github.com/vllm-project/vllm/pull/64316) DeepSeek-V4-Pro B200 presets
- [#63534](https://github.com/vllm-project/vllm/pull/63534) MiniMax-M3 AgentX presets
- [#64114](https://github.com/vllm-project/vllm/pull/64114) MiniMax-M3 GB200 presets
- [#63868](https://github.com/vllm-project/vllm/pull/63868) MiniMax-M3 MI355X monokernel profile
- [#64283](https://github.com/vllm-project/vllm/pull/64283) MiniMax-M3.1-Flash GB200 presets
- [#64284](https://github.com/vllm-project/vllm/pull/64284) MiniMax-M3.1-Flash GB300 presets
- [#64108](https://github.com/vllm-project/vllm/pull/64108) MiniMax-M3.1-Flash B300 presets
- [#64180](https://github.com/vllm-project/vllm/pull/64180) autotrust/JEV-27B-VL recipe
- [#63064](https://github.com/vllm-project/vllm/pull/63064) Standalone Mooncake EGM deployment docs

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#63490](https://github.com/vllm-project/vllm/pull/63490) ROCm MiniMax-M3.1: move DBO under pure TP and SP prefill to separate PRs
- [#59774](https://github.com/vllm-project/vllm/pull/59774) also listed above (ROCM_OCTAVE)
- [#58768](https://github.com/vllm-project/vllm/pull/58768) vllm-openai-efa Docker target

</details>

<details>
<summary>CI, build & tests (11)</summary>

- [#63609](https://github.com/vllm-project/vllm/pull/63609) Disable jobs with unpinned runtime installs
- [#63608](https://github.com/vllm-project/vllm/pull/63608) Disable jobs with unlocked transitive dependencies
- [#64010](https://github.com/vllm-project/vllm/pull/64010) Re-enable disabled jobs whose installs are locked
- [#63408](https://github.com/vllm-project/vllm/pull/63408) One test path per line in Buildkite pytest commands
- [#62141](https://github.com/vllm-project/vllm/pull/62141) Mirror ReplaySSM, MiniMax-M3 attention kernels and Kimi K3 prefix cache on MI355
- [#62120](https://github.com/vllm-project/vllm/pull/62120) Move B200 Kernels and MoE Refactor evals to automatic shards
- [#62537](https://github.com/vllm-project/vllm/pull/62537) Move L4 Distributed Models and LoRA TP to automatic shards
- [#63042](https://github.com/vllm-project/vllm/pull/63042) MyPy strict checking for model test subdirectories
- [#62497](https://github.com/vllm-project/vllm/pull/62497) End-to-end CLI test for bench mm-processor
- [#63616](https://github.com/vllm-project/vllm/pull/63616) Steady-state PP in bench forward
- plus 8 more minor benchmark and test updates ([#63622](https://github.com/vllm-project/vllm/pull/63622), [#63613](https://github.com/vllm-project/vllm/pull/63613), [#64167](https://github.com/vllm-project/vllm/pull/64167), [#63996](https://github.com/vllm-project/vllm/pull/63996), [#62734](https://github.com/vllm-project/vllm/pull/62734), [#63963](https://github.com/vllm-project/vllm/pull/63963))

</details>

<details>
<summary>Newly opened, in progress (highlights)</summary>

- [#64534](https://github.com/vllm-project/vllm/pull/64534) Add Mistral Large 4
- [#64077](https://github.com/vllm-project/vllm/pull/64077) Muse Spark specialized decode, 1.5x on GB300
- [#64364](https://github.com/vllm-project/vllm/pull/64364) DSv4.1 TP4 c1 specialized decode
- [#63921](https://github.com/vllm-project/vllm/pull/63921) DSv4.1 latency_specialized decode extension on NVIDIA
- [#64121](https://github.com/vllm-project/vllm/pull/64121) GLM-5.3-Flash MonoKernel mxfp4_mla KV cache (ROCm)
- [#64198](https://github.com/vllm-project/vllm/pull/64198) MiniMax-M3 MXFP4 K/V and index cache on gfx950
- [#64289](https://github.com/vllm-project/vllm/pull/64289) SM90 MXFP4 MegaMoE via FlashInfer MoE-EP
- [#64464](https://github.com/vllm-project/vllm/pull/64464) HPC-Ops MoE backend for SM120
- [#63956](https://github.com/vllm-project/vllm/pull/63956) Token-sharded sparse-MLA prefill under TP
- [#64126](https://github.com/vllm-project/vllm/pull/64126) KV checksums for offloading connectors and Mooncake
- [#64483](https://github.com/vllm-project/vllm/pull/64483) mm_tensor_ipc cuda_ipc_pool
- [#64528](https://github.com/vllm-project/vllm/pull/64528) Bump ruff to v0.17.2

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 3ed079e48f81ee30f80332a473c9da3690a2802acfae0d2097fc5c805a5e1b76 -->
