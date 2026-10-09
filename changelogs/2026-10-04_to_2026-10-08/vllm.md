# vllm: PR digest (2026-10-04 to 2026-10-08)

_260 merged, 475 newly opened - source vllm-project/vllm, generated 2026-10-08T16:28:26Z_

## TL;DR
- **DeepSeek (V4 / V4.1) got the most attention (40 labels).** Merged work covers CUDA-graph replay layers (`[#59532](https://github.com/vllm-project/vllm/pull/59532)`), AITER MegaMoEV2 on ROCm (`[#59685](https://github.com/vllm-project/vllm/pull/59685)`), and fused MLA dual-RMSNorm + FP8 quant. In flight: a ROCm mono decode layer (`[#60397](https://github.com/vllm-project/vllm/pull/60397)`), deterministic DeepEP MoE (`[#59925](https://github.com/vllm-project/vllm/pull/59925)`), and LiteTopK decode kernels (`[#59922](https://github.com/vllm-project/vllm/pull/59922)`).
- **Performance work was mostly ROCm and sparse-MLA/GDN.** Merged: a RDNA3/4 segmented attention backend (`[#59132](https://github.com/vllm-project/vllm/pull/59132)`), a BF16 split-K sparse-MLA decode kernel for GLM-5.3-Flash (`[#58584](https://github.com/vllm-project/vllm/pull/58584)`), and an AITER FlyDSL GDN prefill backend (`[#57560](https://github.com/vllm-project/vllm/pull/57560)`). Also a MoE win: NCCL symmetric reduce-scatter without staging (`[#49194](https://github.com/vllm-project/vllm/pull/49194)`).
- **KV cache and quantization are widening.** Merged: a 4-bit UltraQuant KV cache (`[#57053](https://github.com/vllm-project/vllm/pull/57053)` is spec-decode; the KV backend is `[#57057](https://github.com/vllm-project/vllm/pull/57057)`), NVFP4 KV on SM8x/SM12x (`[#46963](https://github.com/vllm-project/vllm/pull/46963)`), and online shared-expert and re-quantization APIs (`[#55686](https://github.com/vllm-project/vllm/pull/55686)`, `[#55684](https://github.com/vllm-project/vllm/pull/55684)`). Gemma 4 gets the main new-PR attention, including a 38k-line MoE tuning config PR (`[#60504](https://github.com/vllm-project/vllm/pull/60504)`).
- **Direction:** Model Runner V2 plus speculative decoding (n-gram, suffix, sparse LM head), a Rust frontend and structured-output hardening, and cleanup (removal of Python 3.10, TPU CI, and torch.compile SP/AsyncTP).

## Most important PRs
**[#57057](https://github.com/vllm-project/vllm/pull/57057) — UltraQuant 4-bit KV cache backend (FlyDSL, D=256).** Adds a new attention backend with a 4-bit quantized KV cache on AMD. It cuts KV memory substantially for long contexts.

**[#59132](https://github.com/vllm-project/vllm/pull/59132) — ROCM_SEGMENTED_ATTN backend for RDNA3/3.5/4.** A new attention backend that brings segmented-attention performance to consumer and workstation AMD GPUs. It is a large addition (+4.4k lines).

**[#60517](https://github.com/vllm-project/vllm/pull/60517) — Remove torch.compile sequence parallelism and AsyncTP.** Deletes about 4.8k lines of compile-pass SP/AsyncTP code, a significant simplification of the distributed compile path. The Transformers backend gets its own SP/AsyncTP in the open `[#60653](https://github.com/vllm-project/vllm/pull/60653)`.

**[#59532](https://github.com/vllm-project/vllm/pull/59532) — DSv4.1 decoder replay layers in CUDA graphs.** Runs replay layers in CUDA graphs and trims in PIECEWISE graphs. This should reduce launch overhead on DeepSeek decode.

**[#49194](https://github.com/vllm-project/vllm/pull/49194) — Remove staging from NCCL symmetric reduce-scatter (MoE).** Eliminates an extra copy in the MoE reduce-scatter path, cutting memory traffic and latency for EP/DP.

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#57947](https://github.com/vllm-project/vllm/pull/57947) ROCm: reach fused QSA pre-indexer from AMD path
- [#52668](https://github.com/vllm-project/vllm/pull/52668) ROCm: stacked hipBLASLt GEMM for bf16x3 router
- [#59128](https://github.com/vllm-project/vllm/pull/59128) Skip padded work in block-FP8 DeepGEMM experts
- [#59533](https://github.com/vllm-project/vllm/pull/59533) Merge QSA QKVG and indexer QK projections (Qwen4Exp)
- [#56301](https://github.com/vllm-project/vllm/pull/56301) W4A16 gfx11 stride padding
- [#52619](https://github.com/vllm-project/vllm/pull/52619) Medium-skinny dispatch in RDNAHybridW4A16
- [#59221](https://github.com/vllm-project/vllm/pull/59221) AITER fused shared experts on gfx950 (GLM-5.3-Flash)
- [#59591](https://github.com/vllm-project/vllm/pull/59591) Kimi-K3 latent MoE up-proj stores only local shards
- [#56720](https://github.com/vllm-project/vllm/pull/56720) DSv4.1 one-pass dequant for compressed K cache
- [#56638](https://github.com/vllm-project/vllm/pull/56638) DSv4.1 shared combine_topk_swa_indices kernel on ROCm
- [#60269](https://github.com/vllm-project/vllm/pull/60269) Reduce free KV cache queue overhead
- [#60215](https://github.com/vllm-project/vllm/pull/60215) MRV2: avoid stream syncs in NonUvaBuffer copies
- [#60083](https://github.com/vllm-project/vllm/pull/60083) HiSparse: cache per-request residency
- [#60027](https://github.com/vllm-project/vllm/pull/60027) Qwen4Exp HC up projection stays on skinny GEMM
- [#59632](https://github.com/vllm-project/vllm/pull/59632) SM121 TP=2 skinny-GEMM plans
- [#58685](https://github.com/vllm-project/vllm/pull/58685) JIT monitor hooks TileLang compile
- [#52213](https://github.com/vllm-project/vllm/pull/52213) Trigger perf-eval via release pipeline
- [#57053](https://github.com/vllm-project/vllm/pull/57053) Honor dynamic K in autoregressive speculators (1.2-1.3x kernel speedup)
- [#59069](https://github.com/vllm-project/vllm/pull/59069) Kimi-K3 fuse AttnRes output with per-token FP8 quant
- [#54857](https://github.com/vllm-project/vllm/pull/54857) Fuse MLA dual RMSNorm + FP8 group quant for DeepSeek-R1
- [#60021](https://github.com/vllm-project/vllm/pull/60021) Fused PLE Triton kernels on AMD (Qwen4Exp)
- [#59965](https://github.com/vllm-project/vllm/pull/59965) Default MLA DCP verify to round-robin asm decode on ROCm

</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#57560](https://github.com/vllm-project/vllm/pull/57560) AITER FlyDSL GDN prefill backend
- [#58584](https://github.com/vllm-project/vllm/pull/58584) BF16 split-K sparse-MLA decode (GLM-5.3-Flash)
- [#46963](https://github.com/vllm-project/vllm/pull/46963) NVFP4 KV cache on SM8x/SM12x with FlashInfer
- [#59246](https://github.com/vllm-project/vllm/pull/59246) fp8_ds_mla KV cache for NoPE-512 on SM90
- [#58128](https://github.com/vllm-project/vllm/pull/58128) FP8 KV cache for Triton DiffKV and MiMo-V2.6-Flash
- [#59211](https://github.com/vllm-project/vllm/pull/59211) DCP support for GLM-5.3-Flash kpool sparse indexer
- [#57329](https://github.com/vllm-project/vllm/pull/57329) Mamba2 internal prefill checkpoints
- [#59377](https://github.com/vllm-project/vllm/pull/59377) Deterministic split-K=8 LoRA shrink for batch invariance
- [#56881](https://github.com/vllm-project/vllm/pull/56881) Kimi-K3 fused K/V pack kernel on DCP prefill
- [#60064](https://github.com/vllm-project/vllm/pull/60064) DSv4.1 permute mega-attention weights at load
- [#60434](https://github.com/vllm-project/vllm/pull/60434) Remove WAR for LL CuTeDSL BF16 GEMM
- [#60029](https://github.com/vllm-project/vllm/pull/60029) Pad to 64 Q heads in flashMLA sparse
- [#56959](https://github.com/vllm-project/vllm/pull/56959) Platform-specific MLA prefill backend selection

</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#55686](https://github.com/vllm-project/vllm/pull/55686) Shared-expert fusion with online quantization (Quark MXFP4)
- [#55684](https://github.com/vllm-project/vllm/pull/55684) Layer re-quantization via online quant API (MXFP8 to FP8 PTPC)
- [#56740](https://github.com/vllm-project/vllm/pull/56740) Per-token NVFP4 MoE for ReLU2
- [#58877](https://github.com/vllm-project/vllm/pull/58877) OAI Triton MXFP4 MoE on SM12x
- [#56997](https://github.com/vllm-project/vllm/pull/56997) Prefer Humming before Marlin on SM90
- [#53065](https://github.com/vllm-project/vllm/pull/53065) Tune Triton fused MoE for Intel XPU
- [#58053](https://github.com/vllm-project/vllm/pull/58053) Abstract DeepGemm MegaMOE backend
- [#59685](https://github.com/vllm-project/vllm/pull/59685) AITER MegaMoEV2 for DSv4 on ROCm
- [#59927](https://github.com/vllm-project/vllm/pull/59927) DSv4 MegaMoE shared-expert finalize ordering

</details>

<details>
<summary>Model support (7)</summary>

- [#60254](https://github.com/vllm-project/vllm/pull/60254) EmbeddingGemma2 multimodal pooling
- [#60289](https://github.com/vllm-project/vllm/pull/60289) Streamline EmbeddingGemma 2 config; harmonize Triton prefill attention
- [#57441](https://github.com/vllm-project/vllm/pull/57441) Video support for the Transformers backend
- [#59278](https://github.com/vllm-project/vllm/pull/59278) Device-side mm normalization for Kimi K2.5/K3
- [#60080](https://github.com/vllm-project/vllm/pull/60080) LongCat-Flash MLA norms scaled at load
- [#60152](https://github.com/vllm-project/vllm/pull/60152) Skip checkpoint shards an MTP head does not load
- [#59285](https://github.com/vllm-project/vllm/pull/59285) MiniMax-M3 kernels moved to Triton tensor descriptors

</details>

<details>
<summary>Parallelism & scheduling (8)</summary>

- [#40704](https://github.com/vllm-project/vllm/pull/40704) MRV2 n-gram speculative decoding on GPU
- [#58463](https://github.com/vllm-project/vllm/pull/58463) Remove eager metadata rebuild in MTP fused multi-step decode
- [#60335](https://github.com/vllm-project/vllm/pull/60335) Rename AR speculators to StandaloneAR / TargetDependentAR
- [#59160](https://github.com/vllm-project/vllm/pull/59160) Release CUDA graph pool on sleep
- [#51018](https://github.com/vllm-project/vllm/pull/51018) Pick DP world-group port at bind time
- [#55804](https://github.com/vllm-project/vllm/pull/55804) EPLB: group-local ranks for P2P
- [#59788](https://github.com/vllm-project/vllm/pull/59788) Per-DP-engine RNG streams
- [#60398](https://github.com/vllm-project/vllm/pull/60398) Bound execute_dummy_batch RPC waits

</details>

<details>
<summary>Hardware & arch (6)</summary>

- [#57565](https://github.com/vllm-project/vllm/pull/57565) XPU tuned Mamba SSU configs for B70
- [#59159](https://github.com/vllm-project/vllm/pull/59159) XPU DeepSeek V4 FP8 sparse decode graph-capturable
- [#60367](https://github.com/vllm-project/vllm/pull/60367) ROCm sleep-mode cuMem host mapping
- [#60090](https://github.com/vllm-project/vllm/pull/60090) Build NIXL with NIXL EP in Rubin image
- [#60142](https://github.com/vllm-project/vllm/pull/60142) Qwen4Exp FP8 PLE kernel compiles below SM89
- [#60221](https://github.com/vllm-project/vllm/pull/60221) CPU fused Gumbel-max window bias fix

</details>

<details>
<summary>API & serving (21)</summary>

- [#56801](https://github.com/vllm-project/vllm/pull/56801) Watermark compatibility validation
- [#57875](https://github.com/vllm-project/vllm/pull/57875) Per-session profiling controls (Python and Rust frontends)
- [#59299](https://github.com/vllm-project/vllm/pull/59299) Structured decisions endpoint
- [#58181](https://github.com/vllm-project/vllm/pull/58181) Integer token IDs for generate logprobs
- [#56318](https://github.com/vllm-project/vllm/pull/56318) Metrics: cached prompt tokens by cache tier
- [#58949](https://github.com/vllm-project/vllm/pull/58949) HiSparse steady-state concurrency and host-tier gauges
- [#55937](https://github.com/vllm-project/vllm/pull/55937) Mooncake-style timed-trace replay in vllm bench
- [#59408](https://github.com/vllm-project/vllm/pull/59408) Rust frontend: share SchemaRoot between coercion and grammars
- [#59744](https://github.com/vllm-project/vllm/pull/59744) Rust frontend: remove PyO3 tool-parser bridge
- [#59743](https://github.com/vllm-project/vllm/pull/59743) Port MiniMax M3 tool parser to parser engine
- [#59837](https://github.com/vllm-project/vllm/pull/59837) Rust gRPC forbidden token sequences and cache usage
- [#60203](https://github.com/vllm-project/vllm/pull/60203) Rust frontend: pass tool defer_loading to templates
- [#60115](https://github.com/vllm-project/vllm/pull/60115) Rust gRPC preserves explicit zero sampling values
- [#59563](https://github.com/vllm-project/vllm/pull/59563) Rust frontend backtracks from safe text at complete marker
- [#60073](https://github.com/vllm-project/vllm/pull/60073) Extract parse/assembly from batch chat derender
- [#57849](https://github.com/vllm-project/vllm/pull/57849) Consolidate RL entrypoints
- [#60114](https://github.com/vllm-project/vllm/pull/60114) gsm8k_eval.py chat-completion options
- [#60022](https://github.com/vllm-project/vllm/pull/60022) Restrict Pillow image formats on untrusted media
- [#58925](https://github.com/vllm-project/vllm/pull/58925) Optimize encoder cudagraph padding
- [#41091](https://github.com/vllm-project/vllm/pull/41091) Allow dynamic BackendEnum registration
- [#58457](https://github.com/vllm-project/vllm/pull/58457) Check aligned KV block sizes against every attention backend

</details>

<details>
<summary>Bugfixes (60)</summary>

- [#54113](https://github.com/vllm-project/vllm/pull/54113) Eliminate frontend ZMQ port TOCTOU
- [#56531](https://github.com/vllm-project/vllm/pull/56531) Route all speculation-capable rows through spec path for recurrent state
- [#55053](https://github.com/vllm-project/vllm/pull/55053) MoRI-IO KV block offset with MTP
- [#55471](https://github.com/vllm-project/vllm/pull/55471) NIXL: recover invalidated pull peer metadata
- [#60354](https://github.com/vllm-project/vllm/pull/60354) Stream every tool call when one delta completes several
- [#59879](https://github.com/vllm-project/vllm/pull/59879) Build tool-call grammars from rendered tools
- [#60062](https://github.com/vllm-project/vllm/pull/60062) Pass reasoning_ended through render to generate
- [#60036](https://github.com/vllm-project/vllm/pull/60036) Cap JSON schema nesting
- [#60071](https://github.com/vllm-project/vllm/pull/60071) SimpleCPU honors speculative cacheability
- [#54844](https://github.com/vllm-project/vllm/pull/54844) Mistral pre-v11 tolerates unexpected tool-call JSON
- [#60210](https://github.com/vllm-project/vllm/pull/60210) Index Mamba align state by request slot in MRV2
- [#59061](https://github.com/vllm-project/vllm/pull/59061) Flag multi-branch allOf unsupported for xgrammar
- [#59412](https://github.com/vllm-project/vllm/pull/59412) Page-aligned kernel blocks for pooled indexers (GLM-5.3-Flash)
- [#54835](https://github.com/vllm-project/vllm/pull/54835) Model-default reasoning parser in GPU-less render server
- [#59197](https://github.com/vllm-project/vllm/pull/59197) DSv4.1 skip SWA bounded replay for KV loads
- [#58124](https://github.com/vllm-project/vllm/pull/58124) reload_weights with runai_streamer
- [#57635](https://github.com/vllm-project/vllm/pull/57635) Persist FlashInfer autotune cache per rank (deadlock fix)
- [#40986](https://github.com/vllm-project/vllm/pull/40986) Return streaming errors before first token
- [#59723](https://github.com/vllm-project/vllm/pull/59723) Responses namespace aliases in named tool calling
- [#59859](https://github.com/vllm-project/vllm/pull/59859) Reuse streamed item ids in final harmony response
- [#60161](https://github.com/vllm-project/vllm/pull/60161) NIXL: register HiSparse host pool under single TP rank
- [#58709](https://github.com/vllm-project/vllm/pull/58709) Guidance disable_additional_properties preserves literals
- [#57992](https://github.com/vllm-project/vllm/pull/57992) Scope DSpark non-causal capability to builder layers
- [#59655](https://github.com/vllm-project/vllm/pull/59655) DSV4 NVFP4 keeps ignored MTP/DSpark experts on MXFP4
- [#58067](https://github.com/vllm-project/vllm/pull/58067) disable_any_whitespace on xgrammar
- [#60572](https://github.com/vllm-project/vllm/pull/60572) Drain async KV loads in pause(wait)
- [#47933](https://github.com/vllm-project/vllm/pull/47933) Preserve abort finish_reason for scale-out streams
- [#54850](https://github.com/vllm-project/vllm/pull/54850) Malformed $defs in tool schema returns 400
- [#59031](https://github.com/vllm-project/vllm/pull/59031) Load stacked expert weights for non-gated MoE
- [#60388](https://github.com/vllm-project/vllm/pull/60388) RDNA3 W4A16 MoE N-first CT layout
- [#59164](https://github.com/vllm-project/vllm/pull/59164) MoRIIO exclude sync READ destinations from KV zeroing
- [#60411](https://github.com/vllm-project/vllm/pull/60411) Read safetensors headers of checkpoints with other names
- [#59942](https://github.com/vllm-project/vllm/pull/59942) Retain encoder cache refs for repeated mm inputs
- [#56891](https://github.com/vllm-project/vllm/pull/56891) FlashInfer all_reduce backend selection
- [#59751](https://github.com/vllm-project/vllm/pull/59751) Restrict FlashInfer sparse MLA FULL graphs to decode
- [#59074](https://github.com/vllm-project/vllm/pull/59074) Respect Inductor deterministic mode in combo kernels
- [#60429](https://github.com/vllm-project/vllm/pull/60429) HiSparse drop write-only prefill mirror buffer
- [#58911](https://github.com/vllm-project/vllm/pull/58911) Emit buffered post-reasoning text without tool parser
- [#59759](https://github.com/vllm-project/vllm/pull/59759) Retire stale Mamba spec blocks in checkpoint steps
- [#56974](https://github.com/vllm-project/vllm/pull/56974) GLM-5.3-Flash KDA kernel gridDim.z fix
- [#60389](https://github.com/vllm-project/vllm/pull/60389) ROCm keep MLA derived weights on reload
- [#57816](https://github.com/vllm-project/vllm/pull/57816) Reset SimpleCPU eager-store state on MRV2 resume
- [#58088](https://github.com/vllm-project/vllm/pull/58088) Restore KVCR construction via secondary-tier factory
- [#47838](https://github.com/vllm-project/vllm/pull/47838) Preserve logprobs when top_logprobs is null
- [#59749](https://github.com/vllm-project/vllm/pull/59749) Validate tool-parser/tokenizer compatibility at startup
- [#60156](https://github.com/vllm-project/vllm/pull/60156) Preserve small FP8 softmax weights in Triton attention
- [#59873](https://github.com/vllm-project/vllm/pull/59873) NIXL heartbeats count as engine activity
- [#58165](https://github.com/vllm-project/vllm/pull/58165) FlashInfer autotune must round M up
- [#59842](https://github.com/vllm-project/vllm/pull/59842) Qwen3-Omni interleaved M-RoPE boundary
- [#55708](https://github.com/vllm-project/vllm/pull/55708) Preserve spec metrics when coalescing outputs
- [#60309](https://github.com/vllm-project/vllm/pull/60309) /cohere/v2/chat returns 4xx for client errors
- [#59105](https://github.com/vllm-project/vllm/pull/59105) Reserve bonus KV slot for fill-in DSpark
- [#59103](https://github.com/vllm-project/vllm/pull/59103) Drop stale block hashes on session truncation
- [#60060](https://github.com/vllm-project/vllm/pull/60060) not present; plus ~10 more minor fixes ([#58560](https://github.com/vllm-project/vllm/pull/58560), [#59733](https://github.com/vllm-project/vllm/pull/59733), [#60194](https://github.com/vllm-project/vllm/pull/60194), [#60501](https://github.com/vllm-project/vllm/pull/60501), [#56198](https://github.com/vllm-project/vllm/pull/56198), [#59550](https://github.com/vllm-project/vllm/pull/59550), [#59975](https://github.com/vllm-project/vllm/pull/59975), [#59992](https://github.com/vllm-project/vllm/pull/59992), [#58373](https://github.com/vllm-project/vllm/pull/58373), [#60281](https://github.com/vllm-project/vllm/pull/60281))

</details>

<details>
<summary>Refactors (3)</summary>

- [#60129](https://github.com/vllm-project/vllm/pull/60129) Deprecate sonet dataset
- [#60017](https://github.com/vllm-project/vllm/pull/60017) LoRA code cleanup
- [#48962](https://github.com/vllm-project/vllm/pull/48962) Migrate vendored DeepGEMM to TORCH_LIBRARY (abi3)

</details>

<details>
<summary>CI & build (10)</summary>

- [#60402](https://github.com/vllm-project/vllm/pull/60402) Remove Python 3.10 support
- [#60591](https://github.com/vllm-project/vllm/pull/60591) Remove dead TPU CI scripts
- [#60024](https://github.com/vllm-project/vllm/pull/60024) Remove LoRA tensorizer
- [#59621](https://github.com/vllm-project/vllm/pull/59621) Bump Transformers to 5.18.0
- [#60381](https://github.com/vllm-project/vllm/pull/60381) Bump Transformers to 5.19.0
- [#59050](https://github.com/vllm-project/vllm/pull/59050) Wire 9 tests/models files into Buildkite
- [#58817](https://github.com/vllm-project/vllm/pull/58817) Split Intel XPU CI jobs for B50
- [#60100](https://github.com/vllm-project/vllm/pull/60100) ROCm: wait for engine teardown between LM Eval models
- [#59948](https://github.com/vllm-project/vllm/pull/59948) Consolidate RL entrypoint tests
- plus 4 more minor CI updates ([#60323](https://github.com/vllm-project/vllm/pull/60323), [#59913](https://github.com/vllm-project/vllm/pull/59913), [#52888](https://github.com/vllm-project/vllm/pull/52888), [#59521](https://github.com/vllm-project/vllm/pull/59521))

</details>

<details>
<summary>Docs (2)</summary>

- [#57786](https://github.com/vllm-project/vllm/pull/57786) Model recipes skill
- [#60519](https://github.com/vllm-project/vllm/pull/60519) Update ViT CUDA graph design doc

</details>

<details>
<summary>Other (3)</summary>

- [#60170](https://github.com/vllm-project/vllm/pull/60170) CPU recipes tool: detect head constraints for TP selection
- [#59899](https://github.com/vllm-project/vllm/pull/59899) Update KVCR adapter to pool-and-index API
- [#60241](https://github.com/vllm-project/vllm/pull/60241) Warm DP engines before load-balance test

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 0451040e6df2e4814289df57c8c342ad8cdafc20ab2c6ec262efbcaec2662d00 -->
