# ATOM: PR digest (2026-11-08 to 2026-11-12)

_72 merged, 94 newly opened - source ROCm/ATOM, generated 2026-11-12T18:26:48Z_

## TL;DR
- **DeepSeek-V4.1 dominated** the window. Merged work includes the DSpark monokernel decode on MI355X ([#3091](https://github.com/ROCm/ATOM/pull/3091)) and the gfx1250 single-launch decode step ([#3109](https://github.com/ROCm/ATOM/pull/3109)). Open PRs add AITER-backed mono decode ([#3215](https://github.com/ROCm/ATOM/pull/3215), claims AgentX TP4 c8 ITL -31%), EP16 MegaMoE ([#3228](https://github.com/ROCm/ATOM/pull/3228)), MI308X/gfx942 bring-up ([#3102](https://github.com/ROCm/ATOM/pull/3102)), and many fused-quant and indexer kernel tweaks.
- **Speculative decoding** got heavy investment. Probability-ratio rejection sampling merged ([#2582](https://github.com/ROCm/ATOM/pull/2582)). Open DSpark probabilistic-verify PRs ([#3139](https://github.com/ROCm/ATOM/pull/3139), [#3224](https://github.com/ROCm/ATOM/pull/3224), [#3134](https://github.com/ROCm/ATOM/pull/3134)) cover vocab-split verification, in-place logits reads, and a fused Markov chain.
- **Kimi-K3/K3.1 and MiniMax-M3.1** are the next largest areas. Kimi work covers PP/P-D offload, DCP sparse prefill and profiling harnesses. MiniMax-M3.1 work is open: one-launch decode router, shared-expert fusion, and indexer context parallelism (CP) for decode.
- **KV offload and routing infrastructure** is a big theme: LMCache and Mooncake Store tiers, prefix-spread DP routing, P/D admission control, and a multi-part mesh KV-events series.
- The overall direction is fewer kernel launches per decode step and deeper fusion (quant, shared expert, router), with a growing KV-tiering and routing layer around it.

## Most important PRs
**[#3091](https://github.com/ROCm/ATOM/pull/3091) DeepSeek-V4.1 monokernel decode on MI355X**
Adds a high-interactivity monokernel decode path for DeepSeek-V4.1-Flash (TP4, DSpark) on gfx950. It is the main merged latency play of the window.

**[#3109](https://github.com/ROCm/ATOM/pull/3109) DSV4.1 single-launch decode step on gfx1250 (FlyDSL)**
Collapses a whole decode step into a single FlyDSL launch for gfx1250. Follow-ups ([#3176](https://github.com/ROCm/ATOM/pull/3176), open) extend it to C16 with FP8 KV and FP4 index caches.

**[#2582](https://github.com/ROCm/ATOM/pull/2582) Probability-ratio rejection sampling for spec decode**
Adds proper probabilistic rejection sampling behind draft_probs instead of greedy matching. This should improve acceptance quality and is the base for the open DSpark verify PRs.

**[#3136](https://github.com/ROCm/ATOM/pull/3136) TBO: stage, publish and finish attention metadata once per micro-batch**
A large refactor (164 files) of two-batch-overlap metadata handling across attention backends. It broke DSV4.1 on the vLLM plugin, which [#3189](https://github.com/ROCm/ATOM/pull/3189) then fixed.

**[#3215](https://github.com/ROCm/ATOM/pull/3215) (open) DSV4.1 mono decode on AITER decode-layer ops**
Switches mono decode to AITER ops via ATOM_DSV41_MONO_BACKEND=aiter. The PR reports a 31% ITL reduction at AgentX TP4 c8.

## More changes by area

<details>
<summary>Performance (23)</summary>

- [#2771](https://github.com/ROCm/ATOM/pull/2771) keep Qwen4_exp PLE n-gram table in page-locked host memory read over UVA
- [#2847](https://github.com/ROCm/ATOM/pull/2847) Qwen3.8-Flash-Next TP prefill follow-ups: FlyDSL QSA drafter, row-sharded indexer, SP drafter
- [#2938](https://github.com/ROCm/ATOM/pull/2938) read strided Kimi-K3 AttnRes block residual without copy
- [#3128](https://github.com/ROCm/ATOM/pull/3128) widen DSV4.1 indexer block-maxima grid, 128-wide candidate tiles
- [#3253](https://github.com/ROCm/ATOM/pull/3253) bring #3042/#3099 into perf branch for recipe F8
- [#3139](https://github.com/ROCm/ATOM/pull/3139) (open) vocab-split probabilistic verification for DSpark
- [#3224](https://github.com/ROCm/ATOM/pull/3224) (open) probabilistic verify reads target logits in place
- [#3134](https://github.com/ROCm/ATOM/pull/3134) (open) fused Markov chain for larger batches, bonus sampling on side stream
- [#3225](https://github.com/ROCm/ATOM/pull/3225) (open) base MI455 Qwen3.8 performance
- [#3107](https://github.com/ROCm/ATOM/pull/3107) (open) MI455 Qwen3.8 AgentX perf
- [#3116](https://github.com/ROCm/ATOM/pull/3116) (open) MiniMax-M3 indexer-CP decode by live blocks, one-launch candidate exchange
- [#3258](https://github.com/ROCm/ATOM/pull/3258) (open) KDA Conv1D state/input register reuse for decode
- [#3135](https://github.com/ROCm/ATOM/pull/3135) (open) lm_head writes shard directly into the peer-visible pool
- [#3132](https://github.com/ROCm/ATOM/pull/3132) (open) add shared expert output in MegaMoE combine on mori v2 EP
- [#3199](https://github.com/ROCm/ATOM/pull/3199) (open) fuse TP all-reduce + Gemma RMSNorm with MXFP8 quant
- [#3130](https://github.com/ROCm/ATOM/pull/3130) (open) DSpark draft attention reads context and draft KV as two CSR sources
- [#3131](https://github.com/ROCm/ATOM/pull/3131) (open) quantize DSpark context taps in place
- [#3127](https://github.com/ROCm/ATOM/pull/3127) (open) fuse quantized-pool compress tail into one Triton kernel
- [#3251](https://github.com/ROCm/ATOM/pull/3251) (open) read MiniMax-M3 DSpark taps from next-layer all-reduce
- [#3276](https://github.com/ROCm/ATOM/pull/3276) (open) trace FlyDSL fp8 block-scale GEMM kernels at startup
- [#3133](https://github.com/ROCm/ATOM/pull/3133) (open) pass FP4 logits lane-max summaries to indexer top-k
- [#3193](https://github.com/ROCm/ATOM/pull/3193) (open) use aiter's fused DCP merge for decode partials
- [#3188](https://github.com/ROCm/ATOM/pull/3188) (open) tune quantized UVA lookup geometry on gfx1250

</details>

<details>
<summary>Kernels & attention (22)</summary>

- [#2809](https://github.com/ROCm/ATOM/pull/2809) migrate V4/V4.1 FP4 indexer scoring to the OPUS config API
- [#2715](https://github.com/ROCm/ATOM/pull/2715) plan padded sparse MTP verify MLA work over real tokens only
- [#3272](https://github.com/ROCm/ATOM/pull/3272) run Kimi-K3.1 DCP sparse prefill at native 96 gathered heads
- [#3273](https://github.com/ROCm/ATOM/pull/3273) column-sharded latent tail op for Kimi-K3.1 decode
- [#3268](https://github.com/ROCm/ATOM/pull/3268) split Kimi-K3.1 KDA in_proj GEMM at prefill sizes
- [#3270](https://github.com/ROCm/ATOM/pull/3270) read ReplaySSM KDA beta in place
- [#2831](https://github.com/ROCm/ATOM/pull/2831) fuse wo_a->wo_b mxfp8 quant into batched GEMM epilogue
- [#2808](https://github.com/ROCm/ATOM/pull/2808) fuse DSpark context-KV main_norm + group32 quantize_fp8
- [#3178](https://github.com/ROCm/ATOM/pull/3178) (open) Qwen3.5 FHMoE shared expert inside gfx1250 grouped MoE
- [#3101](https://github.com/ROCm/ATOM/pull/3101) (open) leapquant GDN
- [#3114](https://github.com/ROCm/ATOM/pull/3114) (open) route MiniMax-M3 SP QKV through aiter.sp_qkv_fused
- [#3104](https://github.com/ROCm/ATOM/pull/3104) (open) decode-time indexer context parallelism on MXFP4 index cache
- [#3179](https://github.com/ROCm/ATOM/pull/3179) (open) serve DSV4.1 FP8 sparse attention via flydsl-sparse-mla-provider
- [#3180](https://github.com/ROCm/ATOM/pull/3180) (open) opt-in FlyDSL BF16 sparse decode from plugin_poc
- [#3146](https://github.com/ROCm/ATOM/pull/3146) (open) caller-owned attention output buffers for V4
- [#3220](https://github.com/ROCm/ATOM/pull/3220) (open) packed FP4 KV cache for gfx1250 Triton MLA decode
- [#3266](https://github.com/ROCm/ATOM/pull/3266) (open) GLM-5.2 mono serves BF16-attention checkpoint
- [#3282](https://github.com/ROCm/ATOM/pull/3282) (open) plan Kimi-K3.1 DCP sparse prefill MLA work once per forward
- [#3110](https://github.com/ROCm/ATOM/pull/3110) (open) quantize MXFP8 query 8 heads per program in rope/window seam
- [#3221](https://github.com/ROCm/ATOM/pull/3221) (open) DSV4.1 mono drops K2 index stage for spilling widths
- [#3202](https://github.com/ROCm/ATOM/pull/3202) (open) coarsen DCP A2A pack kernel
- [#3145](https://github.com/ROCm/ATOM/pull/3145) (open) Wan2.1 VAE with conv3d dispatched to AITER FlyDSL

</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#3205](https://github.com/ROCm/ATOM/pull/3205) (open) MiniMax-M3.1 decode router shares launch with shared-expert SwiGLU
- [#3195](https://github.com/ROCm/ATOM/pull/3195) (open) one-launch decode router on gfx950
- [#3214](https://github.com/ROCm/ATOM/pull/3214) (open) run M3.1 shared gate_up GEMM inside router launch
- [#3207](https://github.com/ROCm/ATOM/pull/3207) (open) fold M3.1 shared expert output into routed GEMM2
- [#3198](https://github.com/ROCm/ATOM/pull/3198) (open) fuse SwiGLU-OAI with MXFP8 quant of down_proj input
- [#3228](https://github.com/ROCm/ATOM/pull/3228) (open) DSv4.1 EP16 MegaMoE and serving warmup
- [#3187](https://github.com/ROCm/ATOM/pull/3187) (open) MegaMoE lets AITER pick small/large/staged routes
- [#3164](https://github.com/ROCm/ATOM/pull/3164) (open) fuse FP8 shared expert into MXFP4 MoE
- [#3235](https://github.com/ROCm/ATOM/pull/3235) (open) --spec-decode-kv-cache-dtype for drafts with own pool
- [#3144](https://github.com/ROCm/ATOM/pull/3144) (open) gfx1250 MoE iod weight preshuffle

</details>

<details>
<summary>Model support (9)</summary>

- [#3137](https://github.com/ROCm/ATOM/pull/3137) GLM-5.3-Flash prefix caching and MTP on vLLM plugin
- [#3117](https://github.com/ROCm/ATOM/pull/3117) Kimi-K3 plugin LMCache MP offload with KDA state in PAGE object
- [#2598](https://github.com/ROCm/ATOM/pull/2598) DeepSeek-V4.1-Flash LMCache tier offload via MP server
- [#2709](https://github.com/ROCm/ATOM/pull/2709) Kimi-K3 PP8 P/D prefill: PAGE-backed state checkpoints
- [#2721](https://github.com/ROCm/ATOM/pull/2721) MiniMax-M3.1 P/D from PP4 prefill into TP4 decode (KV transfer)
- [#3102](https://github.com/ROCm/ATOM/pull/3102) (open) DeepSeek-V4.1-Flash on MI308X (gfx942)
- [#3223](https://github.com/ROCm/ATOM/pull/3223) (open) Qwen3.5 MoE MXFP4 bring-up on gfx1250
- [#3156](https://github.com/ROCm/ATOM/pull/3156) (open) gfx942 post seams on AITER ASM mHC seam
- [#3186](https://github.com/ROCm/ATOM/pull/3186) (open) EPLB on layers before the decoder

</details>

<details>
<summary>Parallelism & scheduling (24)</summary>

- [#2755](https://github.com/ROCm/ATOM/pull/2755) prefix-spread DP routing with Mooncake Store recovery
- [#3216](https://github.com/ROCm/ATOM/pull/3216) prefix_spread single lookup walk, dp_routing package
- [#3229](https://github.com/ROCm/ATOM/pull/3229) prefix_spread trim/evict counters
- [#3217](https://github.com/ROCm/ATOM/pull/3217) scheduler re-ranks waiting only on load events
- [#3059](https://github.com/ROCm/ATOM/pull/3059) Lumen-RL pause/resume generation and preempt before KV/weight changes
- [#3106](https://github.com/ROCm/ATOM/pull/3106) stop bounding delayer fill probe by prompt length
- [#3097](https://github.com/ROCm/ATOM/pull/3097) (open) shared Mooncake Store: share_cache DP routing, early tier load
- [#3236](https://github.com/ROCm/ATOM/pull/3236) (open) keep weights on GPU across restarts (ATOM_PRELOAD)
- [#3194](https://github.com/ROCm/ATOM/pull/3194) (open) KV offload over Mori UMBP standalone server
- [#3267](https://github.com/ROCm/ATOM/pull/3267) (open) pluggable KV pool backend with MORI-UMBP L1
- [#3125](https://github.com/ROCm/ATOM/pull/3125) (open) lmcache_mp names prompts by chunk hashes
- [#3100](https://github.com/ROCm/ATOM/pull/3100) (open) pass optional LMCache ATOM adapter args
- [#3103](https://github.com/ROCm/ATOM/pull/3103) (open) high-priority Mooncake copies, tokenize cache, two-node Store in ATOMesh
- [#3151](https://github.com/ROCm/ATOM/pull/3151) (open) resolve parallel mapping before worker init
- [#3147](https://github.com/ROCm/ATOM/pull/3147) (open) bound decode admission by pending receive KV bytes
- [#3165](https://github.com/ROCm/ATOM/pull/3165) (open) reserve decode growth when admitting P/D receives
- [#3173](https://github.com/ROCm/ATOM/pull/3173) (open) export decode admission metrics
- [#3238](https://github.com/ROCm/ATOM/pull/3238) (open) export KV held by deferred frees
- [#3256](https://github.com/ROCm/ATOM/pull/3256) (open) check KV connector reserve after agreement
- [#3196](https://github.com/ROCm/ATOM/pull/3196) (open) DP prefill rank whose cost sets the target prefills chunk whole
- [#3281](https://github.com/ROCm/ATOM/pull/3281) (open) row-shard Kimi-K3.1 latent MoE tail on large prefill
- [#3275](https://github.com/ROCm/ATOM/pull/3275) (open) publish vLLM event encoding and replay frames
- [#3277](https://github.com/ROCm/ATOM/pull/3277) (open) serve each DP rank's publisher at /kv_event_sources
- [#3201](https://github.com/ROCm/ATOM/pull/3201) (open) abort before decode pull retires prefill send claim

</details>

<details>
<summary>Hardware & arch (0)</summary>

- No separate entries; hardware work is listed under Model support and Kernels.

</details>

<details>
<summary>API & serving (14)</summary>

- [#3090](https://github.com/ROCm/ATOM/pull/3090) strict function tools on /beta/chat/completions
- [#3061](https://github.com/ROCm/ATOM/pull/3061) hold Kimi-K3 tool calls to schemas with structured-output grammar
- [#3115](https://github.com/ROCm/ATOM/pull/3115) image input on /v1/responses and /v1/messages
- [#3111](https://github.com/ROCm/ATOM/pull/3111) check and load chat images in the server
- [#3083](https://github.com/ROCm/ATOM/pull/3083) opt-in independent per-row sampling noise
- [#3159](https://github.com/ROCm/ATOM/pull/3159) (open) Kimi-K3 chat prompt ids from tokenizer's segment encoder
- [#3124](https://github.com/ROCm/ATOM/pull/3124) (open) keep structured-output extras optional at startup
- [#3141](https://github.com/ROCm/ATOM/pull/3141) mesh routing decision metrics on router port
- [#3142](https://github.com/ROCm/ATOM/pull/3142) (open) sampled decision log, dispatched DP rank
- [#3206](https://github.com/ROCm/ATOM/pull/3206) (open) WIP session affinity table around routing policies
- [#3161](https://github.com/ROCm/ATOM/pull/3161) (open) key chat routing by image/video identity
- [#3209](https://github.com/ROCm/ATOM/pull/3209) (open) agentic prefill routing 1/3: route on text
- [#3210](https://github.com/ROCm/ATOM/pull/3210) (open) agentic prefill routing 2/3: in-flight prefill tokens
- [#3211](https://github.com/ROCm/ATOM/pull/3211) (open) agentic prefill routing 3/3: agentic policy

</details>

<details>
<summary>Mesh / KV events and Rust runtime (8)</summary>

- [#3126](https://github.com/ROCm/ATOM/pull/3126) (open) atomesh engine_v1 protocol and Rust link to EngineCore
- [#3122](https://github.com/ROCm/ATOM/pull/3122) (open) OpenAI-compatible chat rendering and tokenizer fixes
- [#3252](https://github.com/ROCm/ATOM/pull/3252) (open) KV events 1/6 interfaces and data model
- [#3254](https://github.com/ROCm/ATOM/pull/3254) (open) KV events 2/6 config, CLI flags, metrics
- [#3257](https://github.com/ROCm/ATOM/pull/3257) (open) KV events 3/6 msgpack decoder and per-rank admission
- [#3269](https://github.com/ROCm/ATOM/pull/3269) (open) KV events 4/6 prefix index
- [#3274](https://github.com/ROCm/ATOM/pull/3274) (open) KV events 5/6 index provider and policy hook
- [#3280](https://github.com/ROCm/ATOM/pull/3280) Kimi-K3.1 decode profiling harness with per-layer trace parser

</details>

<details>
<summary>Bugfixes (30)</summary>

- [#2668](https://github.com/ROCm/ATOM/pull/2668) refresh state images in LMCache LRU on tier hit
- [#2932](https://github.com/ROCm/ATOM/pull/2932) serialize UVA registration across DP ranks
- [#3237](https://github.com/ROCm/ATOM/pull/3237) use aiter's FlyDSL QSA prefill scorer instead of vendored copy
- [#3076](https://github.com/ROCm/ATOM/pull/3076) preserve invalid DP rows when reassigning shared experts
- [#3184](https://github.com/ROCm/ATOM/pull/3184) mono programs write QSA RoPE position cache
- [#3105](https://github.com/ROCm/ATOM/pull/3105) fix delayed P/D KV completion reporting
- [#3155](https://github.com/ROCm/ATOM/pull/3155) fence in-process state store on slot->PAGE copy
- [#3108](https://github.com/ROCm/ATOM/pull/3108) drop FlyDSL paged-decode API probe
- [#3052](https://github.com/ROCm/ATOM/pull/3052) accept optional explicit FlyDSL plans
- [#2933](https://github.com/ROCm/ATOM/pull/2933) quantize fused shared-expert activation for native MX w2
- [#3189](https://github.com/ROCm/ATOM/pull/3189) start DSV4.1 on vLLM plugin again after [#3136](https://github.com/ROCm/ATOM/pull/3136)
- [#3226](https://github.com/ROCm/ATOM/pull/3226) launch Qwen3.8/DSV4.1 hi programs through compiled functions
- [#3073](https://github.com/ROCm/ATOM/pull/3073) format Inductor fallback log text only when emitted
- [#3113](https://github.com/ROCm/ATOM/pull/3113) release completed TBO job before workers idle
- [#3098](https://github.com/ROCm/ATOM/pull/3098) allocate k draft KV positions for block drafters
- [#3063](https://github.com/ROCm/ATOM/pull/3063) include DSA index keys in Kimi-K3.1 offload
- [#3167](https://github.com/ROCm/ATOM/pull/3167) page QSA through scheduled requests' block-table rows
- [#3185](https://github.com/ROCm/ATOM/pull/3185) fix gfx1250 single-launch crash with no drafter hidden states
- [#3169](https://github.com/ROCm/ATOM/pull/3169) run V4 TBO comm stream at high priority
- [#3271](https://github.com/ROCm/ATOM/pull/3271) (open) keep UVA rows in GTT host memory, one copy per NUMA node
- [#3171](https://github.com/ROCm/ATOM/pull/3171) (open) reconcile KV block counts across TP and PCP workers
- [#3203](https://github.com/ROCm/ATOM/pull/3203) (open) P/D producer reports first token from sampling forward
- [#3200](https://github.com/ROCm/ATOM/pull/3200) (open) Qwen3.5 MTP drafter loads on dense target
- [#3197](https://github.com/ROCm/ATOM/pull/3197) (open) token-graph recording keeps no live argument
- [#3163](https://github.com/ROCm/ATOM/pull/3163) (open) keep SGLang draft-extend CUDA graph runner for plugin drafters
- [#3099](https://github.com/ROCm/ATOM/pull/3099) (open) reserve block 0 as null page under PAGE checkpoints
- [#3219](https://github.com/ROCm/ATOM/pull/3219) (open) pass Triton decode only sequences owning rows of q
- [#3265](https://github.com/ROCm/ATOM/pull/3265) (open) write every slot of MLA indptr span on replicated row
- [#3279](https://github.com/ROCm/ATOM/pull/3279) (open) thread-local trace slots for FlyDSL >= 0.5
- [#3182](https://github.com/ROCm/ATOM/pull/3182) fix dspark served-step test arguments

</details>

<details>
<summary>CI & build (14)</summary>

- [#2762](https://github.com/ROCm/ATOM/pull/2762) port automated PR-review pipeline from aiter as rocm-atom-bot
- [#3121](https://github.com/ROCm/ATOM/pull/3121) AgentX / Non-AgentX dashboard
- [#3230](https://github.com/ROCm/ATOM/pull/3230) benchmark vLLM PR CI models at SGLang concurrencies
- [#2985](https://github.com/ROCm/ATOM/pull/2985) local-model completeness check for accuracy runs, prefill CP flags
- [#3232](https://github.com/ROCm/ATOM/pull/3232) skip mocker benchmark on PRs, fix cargo cache
- [#3062](https://github.com/ROCm/ATOM/pull/3062) read SGLang benchmark matrix from file in summary job
- [#3071](https://github.com/ROCm/ATOM/pull/3071) remove Atomesh TW weekly schedule
- [#3153](https://github.com/ROCm/ATOM/pull/3153) defense-in-depth guards for self-hosted runners
- [#3181](https://github.com/ROCm/ATOM/pull/3181) bump Mooncake for THP-backed RDMA segments
- [#3218](https://github.com/ROCm/ATOM/pull/3218) run agentic benchmarks on pitt MI350X pool
- [#3154](https://github.com/ROCm/ATOM/pull/3154) (open) ATOM test result gates
- [#3208](https://github.com/ROCm/ATOM/pull/3208) (open) atomesh CI: drop MI350X nightly, free busy GPUs, unprivileged RDMA smoke

</details>

<details>
<summary>Refactors (2)</summary>

- [#3278](https://github.com/ROCm/ATOM/pull/3278) comment update for Kimi-K3.1 split KDA in_proj
- [#3186](https://github.com/ROCm/ATOM/pull/3186)-style cleanup: none beyond [#3256](https://github.com/ROCm/ATOM/pull/3256) listed above

</details>

<details>
<summary>Docs (5)</summary>

- [#3204](https://github.com/ROCm/ATOM/pull/3204) refresh DSV4.1-Flash agentic recipe settings
- [#3233](https://github.com/ROCm/ATOM/pull/3233) match DSV4.1-Flash agentic recipe to InferenceX config
- [#3255](https://github.com/ROCm/ATOM/pull/3255) (open) Qwen3.5 AgentX MXFP4 recipe
- [#3168](https://github.com/ROCm/ATOM/pull/3168) README: add ATOM Meets Mooncake blog
- [#3170](https://github.com/ROCm/ATOM/pull/3170) README: add FlyDSL mono kernels blog

</details>

<details>
<summary>Other (3)</summary>

- [#3264](https://github.com/ROCm/ATOM/pull/3264) Kimi-K3.1 16K prefill profiling harness with trace parser
- [#3182](https://github.com/ROCm/ATOM/pull/3182) test(dspark) served-step argument fix
- plus minor items covered above

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 73f4da9e69f69c1770cd52c94e0725e47be3b22ff7ec7db222ad94f951e56606 -->
