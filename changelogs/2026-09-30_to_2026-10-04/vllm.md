# vllm: PR digest (2026-09-30 to 2026-10-04)

_264 merged, 418 newly opened - source vllm-project/vllm, generated 2026-10-05T00:11:05Z_

## TL;DR

- **DeepSeek (V4/V4.1) got the most labeled attention.** Merged work: faster Engram host lookups (`[#59327](https://github.com/vllm-project/vllm/pull/59327)`), the ROCm a4w4 MoE path (`[#58819](https://github.com/vllm-project/vllm/pull/58819)`), and shared prefill chunk plans on ROCm. Newly opened work includes a deterministic-inference stack (`[#59863](https://github.com/vllm-project/vllm/pull/59863)`, `[#59883](https://github.com/vllm-project/vllm/pull/59883)`, `[#59925](https://github.com/vllm-project/vllm/pull/59925)`, `[#59952](https://github.com/vllm-project/vllm/pull/59952)`, `[#59929](https://github.com/vllm-project/vllm/pull/59929)`), small-head sparse decode on SM90 (`[#59418](https://github.com/vllm-project/vllm/pull/59418)`), and decoder-replay CUDA graphs (`[#59532](https://github.com/vllm-project/vllm/pull/59532)`, `[#59894](https://github.com/vllm-project/vllm/pull/59894)`).
- **GLM-5.3 and MiniMax-M3 had the largest perf work.** GLM-5.3 merged a 3.5–3.9x sparse-MLA index-conversion speedup (`[#59464](https://github.com/vllm-project/vllm/pull/59464)`), a 13.3% E2E gain from fused multi-step decode (`[#57443](https://github.com/vllm-project/vllm/pull/57443)`), and a 4.4–7.7% TTFT gain (`[#58845](https://github.com/vllm-project/vllm/pull/58845)`). MiniMax-M3 got an NVFP4 KV cache (`[#59300](https://github.com/vllm-project/vllm/pull/59300)`), and the open `[#59705](https://github.com/vllm-project/vllm/pull/59705)` and `[#59653](https://github.com/vllm-project/vllm/pull/59653)` add fused sparse-layer decode on ROCm.
- **Spec decode and hybrid/Mamba models are active.** Merged: FlashInfer ReplaySSM for MTP (`[#52928](https://github.com/vllm-project/vllm/pull/52928)`), sampling-mask replay (`[#59359](https://github.com/vllm-project/vllm/pull/59359)`), and a Kimi-K3 FlashInfer speculative KDA backend (`[#54255](https://github.com/vllm-project/vllm/pull/54255)`). Open: RecoverSSM across CUDA, PP and XPU (`[#59366](https://github.com/vllm-project/vllm/pull/59366)`, `[#59983](https://github.com/vllm-project/vllm/pull/59983)`, `[#59982](https://github.com/vllm-project/vllm/pull/59982)`).
- **Direction:** the Rust frontend and parser engine are being built out, the Transformers modeling backend is replacing hand-written models, HiSparse is being hardened, and sleep mode is being extended to NIXL, Mooncake and DeepEP. MXFP4/NVFP4 and AMD AITER/FlyDSL fusions are the quantization thread.

## Most important PRs

**[#54049](https://github.com/vllm-project/vllm/pull/54049) FlashInfer CuteDSL MegaMoE integration**
Merged. It integrates a CuteDSL fused MoE kernel backed by FlashInfer, and the change touches distributed, quantization and spec-decode paths.

**[#52928](https://github.com/vllm-project/vllm/pull/52928) FlashInfer ReplaySSM for MTP**
Merged. It uses FlashInfer to replay SSM state during MTP verification on hybrid Mamba/GDN models. This avoids state recomputation after rejected drafts.

**[#59300](https://github.com/vllm-project/vllm/pull/59300) NVFP4 KV cache for MiniMax-M3 MSA sparse attention**
Merged. It stores KV in NVFP4 on the sparse attention path, cutting KV memory. The open `[#59791](https://github.com/vllm-project/vllm/pull/59791)` extends NVFP4 KV to SM120/121 with FlashInfer.

**[#59464](https://github.com/vllm-project/vllm/pull/59464) GLM-5.3 sparse MLA index conversion reuse**
Merged. It converts the sparse MLA indices once and reuses them across layers, giving a 3.5–3.9x kernel speedup.

**[#59705](https://github.com/vllm-project/vllm/pull/59705) ROCm MiniMax-M3 fused sparse-layer decode**
Opened, not merged. A 5.9k-line mono decode kernel for AMD that fuses the sparse-layer decode steps. It is paired with the AITER variant in `[#59653](https://github.com/vllm-project/vllm/pull/59653)`.

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#59327](https://github.com/vllm-project/vllm/pull/59327) faster DSv4.1 Engram host lookups
- [#58167](https://github.com/vllm-project/vllm/pull/58167) AITER topk backend for GLM-5.3-Flash decode (ROCm)
- [#58344](https://github.com/vllm-project/vllm/pull/58344) Kimi-K3 prefill checkpoints on ROCm
- [#53913](https://github.com/vllm-project/vllm/pull/53913) vectorized CPU sampler kernel
- [#40337](https://github.com/vllm-project/vllm/pull/40337) flash-maxsim Triton kernels for late-interaction scoring
- [#52162](https://github.com/vllm-project/vllm/pull/52162) shard decode requests across PCP ranks
- [#57930](https://github.com/vllm-project/vllm/pull/57930) HiSparse: avoid repeated prefix scans
- [#57978](https://github.com/vllm-project/vllm/pull/57978) parallelize AITER MLA page-index expansion
- [#57640](https://github.com/vllm-project/vllm/pull/57640) fuse Kimi-K3 MLA decode KV write and Q-prep via AITER
- [#58569](https://github.com/vllm-project/vllm/pull/58569) drop redundant copy after ragged sparse MLA
- [#58008](https://github.com/vllm-project/vllm/pull/58008) single Triton kernel for kpool top-k fitting
- [#57979](https://github.com/vllm-project/vllm/pull/57979) stride-aware decode KDA
- [#58797](https://github.com/vllm-project/vllm/pull/58797) lazily allocate pinned PLE buffer
- [#58623](https://github.com/vllm-project/vllm/pull/58623) custom all-reduce under batch invariance
- [#58845](https://github.com/vllm-project/vllm/pull/58845) skip qlnorm for MHA
- [#59753](https://github.com/vllm-project/vllm/pull/59753) SM121 skinny-GEMM plans for Qwen4Exp
- [#59214](https://github.com/vllm-project/vllm/pull/59214) SM100 low-latency decode GEMM plans for Qwen4Exp
- [#58542](https://github.com/vllm-project/vllm/pull/58542) skip sampled-token broadcasts under PP
- [#58763](https://github.com/vllm-project/vllm/pull/58763) slice pure spec-decode rows in GDN
- [#59735](https://github.com/vllm-project/vllm/pull/59735) keep non-spec GDN decode on the standard path
- [#59731](https://github.com/vllm-project/vllm/pull/59731) tune MoE weighted-sum launch config
- [#56151](https://github.com/vllm-project/vllm/pull/56151) MiniMax-M3 Triton indexer decode retune

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#59377](https://github.com/vllm-project/vllm/pull/59377) deterministic split-K LoRA shrink for batch invariance
- [#54093](https://github.com/vllm-project/vllm/pull/54093) aarch64 CPU Conv1d kernel
- [#58482](https://github.com/vllm-project/vllm/pull/58482) occupancy-adaptive Triton split-K segments on SM120
- [#59481](https://github.com/vllm-project/vllm/pull/59481) keep FP8 MMA in MiniMax-M3 Triton indexer scorers
- [#59235](https://github.com/vllm-project/vllm/pull/59235) HiSparse MTP verification with a union residency kernel
- [#59462](https://github.com/vllm-project/vllm/pull/59462) TokenSpeed MLA with block-interleaved DCP
- [#54805](https://github.com/vllm-project/vllm/pull/54805) revert AITER PA gluon decode from ROCM_AITER_FA
- [#57097](https://github.com/vllm-project/vllm/pull/57097) fuse QK-norm/RoPE/gate and KV write into the QSA pre-indexer
- [#58769](https://github.com/vllm-project/vllm/pull/58769) Kimi-K3 kernels: make_block_ptr to tensor descriptors
- [#57172](https://github.com/vllm-project/vllm/pull/57172) fused SYCL LayerNorm on XPU
- [#59550](https://github.com/vllm-project/vllm/pull/59550) ROCM_ATTN sliding-window boundary fix

</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#59455](https://github.com/vllm-project/vllm/pull/59455) bind routed-experts capture to the MoE layer
- [#54024](https://github.com/vllm-project/vllm/pull/54024) CPU Zen DA8W4 int4 for dense and MoE
- [#50030](https://github.com/vllm-project/vllm/pull/50030) per-token NVFP4 CuTe-DSL MoE backend
- [#57995](https://github.com/vllm-project/vllm/pull/57995) fp8 combine in FlashInfer one-sided MoE all2all
- [#58819](https://github.com/vllm-project/vllm/pull/58819) ROCm a4w4 MoE for DSv4.1 on AITER
- [#58262](https://github.com/vllm-project/vllm/pull/58262) MiMo-V2.6 MXFP4 on gfx942
- [#51274](https://github.com/vllm-project/vllm/pull/51274) Kimi-K3 gfx942 MXFP4-to-int4 conversion
- [#55368](https://github.com/vllm-project/vllm/pull/55368) pad AITER MoE intermediate size
- [#56050](https://github.com/vllm-project/vllm/pull/56050) detect NVFP4 in ModelOpt mixed checkpoints
- [#55161](https://github.com/vllm-project/vllm/pull/55161) fall back for high-rank MoE LoRA

</details>

<details>
<summary>Model support (12)</summary>

- [#57387](https://github.com/vllm-project/vllm/pull/57387) upstream GLM-5.3 and Qwen4-Exp configs
- [#59701](https://github.com/vllm-project/vllm/pull/59701) GPT-NeoX, Phi, Seed-OSS and Jais2 moved to the Transformers backend
- [#59679](https://github.com/vllm-project/vllm/pull/59679) Glm, Arcee, CWM and Mellum moved to the Transformers backend
- [#55335](https://github.com/vllm-project/vllm/pull/55335) K2 Horizon partial-RoPE permutation folded into weights
- [#57168](https://github.com/vllm-project/vllm/pull/57168) compile support for Pixtral vision encoders
- [#58268](https://github.com/vllm-project/vllm/pull/58268) W4A16 Whisper on CPU
- [#58890](https://github.com/vllm-project/vllm/pull/58890) Qwen3-Omni M-RoPE offset fix
- [#55389](https://github.com/vllm-project/vllm/pull/55389) device-side mm normalization for GLM4V/GLM5Next
- [#55902](https://github.com/vllm-project/vllm/pull/55902) EAGLE3/DSpark PP for Sarvam MLA
- [#58648](https://github.com/vllm-project/vllm/pull/58648) MiniMax-M3 MTP embedding sharing under PP
- [#57197](https://github.com/vllm-project/vllm/pull/57197) MiniMax-M3 EAGLE3 aux-state relay at PP>1
- [#59565](https://github.com/vllm-project/vllm/pull/59565) GLM-5.3 image encoder cache sizing

</details>

<details>
<summary>Parallelism & scheduling (12)</summary>

- [#52641](https://github.com/vllm-project/vllm/pull/52641) EPLB contention-aware expert migration batching
- [#58399](https://github.com/vllm-project/vllm/pull/58399) native ModelExpress weight transfer backend
- [#59139](https://github.com/vllm-project/vllm/pull/59139) PP with PCP in Model Runner V2
- [#57652](https://github.com/vllm-project/vllm/pull/57652) KV-offload replicated layout for multi-group MLA
- [#54483](https://github.com/vllm-project/vllm/pull/54483) NIXL host-buffer KV copy coalescing
- [#59160](https://github.com/vllm-project/vllm/pull/59160) release CUDA graph pool on sleep
- [#59156](https://github.com/vllm-project/vllm/pull/59156) release WorkspaceManager scratch on sleep
- [#59158](https://github.com/vllm-project/vllm/pull/59158) offload KV-init state on sleep
- [#58411](https://github.com/vllm-project/vllm/pull/58411) randomized dummy inputs in MRV2
- [#58921](https://github.com/vllm-project/vllm/pull/58921) per-module LM heads for multi-layer MTP on MRV2
- [#59359](https://github.com/vllm-project/vllm/pull/59359) sampling mask replay for MRV2 MTP
- [#56807](https://github.com/vllm-project/vllm/pull/56807) watermarking context dedup in spec decode

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#56063](https://github.com/vllm-project/vllm/pull/56063) Triton W8A8 block-FP8 tuning for Intel B70
- [#54706](https://github.com/vllm-project/vllm/pull/54706) RDNA3 W4A16 split-K accuracy and determinism fix
- [#59149](https://github.com/vllm-project/vllm/pull/59149) W4A16 AWQ/GPTQ on POWER10 VSX
- [#59159](https://github.com/vllm-project/vllm/pull/59159) DSv4 FP8 sparse decode graph-capturable on XPU
- [#59320](https://github.com/vllm-project/vllm/pull/59320) encoder-only runner for XPU EC producers

</details>

<details>
<summary>API & serving (26)</summary>

- [#59005](https://github.com/vllm-project/vllm/pull/59005) Rust frontend `hf` response-template parser
- [#59143](https://github.com/vllm-project/vllm/pull/59143) Rust frontend: replay output grammars through XGrammar
- [#59393](https://github.com/vllm-project/vllm/pull/59393) Rust frontend: structural-tag grammar snapshots
- [#59395](https://github.com/vllm-project/vllm/pull/59395) Rust frontend: split argument grammars
- [#58358](https://github.com/vllm-project/vllm/pull/58358) Rust frontend: token-aware marker parsing for Kimi K3
- [#58357](https://github.com/vllm-project/vllm/pull/58357) Rust frontend: UTF-8 token anchoring
- [#59659](https://github.com/vllm-project/vllm/pull/59659) expose gRPC port in Python `vllm serve`
- [#59316](https://github.com/vllm-project/vllm/pull/59316) Rust frontend Shutdown RPC
- [#59148](https://github.com/vllm-project/vllm/pull/59148) Rust frontend uses the MiMo structural-tag builder
- [#58602](https://github.com/vllm-project/vllm/pull/58602) chat_parsing core ported from Transformers
- [#58603](https://github.com/vllm-project/vllm/pull/58603) richer chat_parsing streaming events
- [#58604](https://github.com/vllm-project/vllm/pull/58604) parse tool calls and reasoning from checkpoint templates
- [#59321](https://github.com/vllm-project/vllm/pull/59321) Step-3.5 parsers ported to the streaming parser engine
- [#56403](https://github.com/vllm-project/vllm/pull/56403) constrain non-strict GLM-4.7 tool calls
- [#58588](https://github.com/vllm-project/vllm/pull/58588) `output_mode` on `/inference/v1/generate`
- [#56984](https://github.com/vllm-project/vllm/pull/56984) per-row candidate IDs for prefill scoring
- [#52864](https://github.com/vllm-project/vllm/pull/52864) sleep-mode API responses and metrics
- [#51350](https://github.com/vllm-project/vllm/pull/51350) weight checker dev endpoint
- [#55781](https://github.com/vllm-project/vllm/pull/55781) HTTP weight-operation outcome tracking
- [#48867](https://github.com/vllm-project/vllm/pull/48867) `--custom-histogram-buckets`
- [#58874](https://github.com/vllm-project/vllm/pull/58874) KV-fetch stage gauges for P/D
- [#58739](https://github.com/vllm-project/vllm/pull/58739) built-in JSON log formatter
- [#59357](https://github.com/vllm-project/vllm/pull/59357) authenticate shared-memory multimodal cache handles
- [#50300](https://github.com/vllm-project/vllm/pull/50300) chat-template DoS fix
- [#57305](https://github.com/vllm-project/vllm/pull/57305) benchmark sweep warmup and recovery
- [#59247](https://github.com/vllm-project/vllm/pull/59247) Rust bench: warn on default temperature

</details>

<details>
<summary>Bugfixes (50)</summary>

- [#59309](https://github.com/vllm-project/vllm/pull/59309) HiSparse MTP acceptance collapse under FULL graphs
- [#59036](https://github.com/vllm-project/vllm/pull/59036) HiSparse: never allocate GPU pages without host backing
- [#59450](https://github.com/vllm-project/vllm/pull/59450) HiSparse KV sizing
- [#59651](https://github.com/vllm-project/vllm/pull/59651) HiSparse: keep spec expansion out of core KV sizing
- [#59007](https://github.com/vllm-project/vllm/pull/59007) HiSparse host prefix publication after completion
- [#59494](https://github.com/vllm-project/vllm/pull/59494) HiSparse chunked-prefill livelock
- [#59282](https://github.com/vllm-project/vllm/pull/59282) HiSparse GPU prefix copy adoption
- [#59495](https://github.com/vllm-project/vllm/pull/59495) HiSparse: host reads once the admission window fills
- [#59046](https://github.com/vllm-project/vllm/pull/59046) derender detokenization seeding
- [#59307](https://github.com/vllm-project/vllm/pull/59307) Responses API streamed final response
- [#59859](https://github.com/vllm-project/vllm/pull/59859) Responses API: reuse streamed item ids in the harmony response
- [#59652](https://github.com/vllm-project/vllm/pull/59652) Responses reasoning content-part events
- [#59173](https://github.com/vllm-project/vllm/pull/59173) Responses: ignore reused prompt token ids for media
- [#59555](https://github.com/vllm-project/vllm/pull/59555) vocab check on reused prompt token ids
- [#58975](https://github.com/vllm-project/vllm/pull/58975) pooling multimodal cache misses
- [#59695](https://github.com/vllm-project/vllm/pull/59695) SHM processor cache refcounting
- [#59504](https://github.com/vllm-project/vllm/pull/59504) async KV load zeroing exemption
- [#59175](https://github.com/vllm-project/vllm/pull/59175) mamba prefill checkpoint reservation in align mode
- [#59536](https://github.com/vllm-project/vllm/pull/59536) GDN prefill checkpoint metadata per cache group
- [#51899](https://github.com/vllm-project/vllm/pull/51899) prefix-cache extra-key source tags
- [#59335](https://github.com/vllm-project/vllm/pull/59335) LoRA path in prefix-cache block hashes
- [#59441](https://github.com/vllm-project/vllm/pull/59441) MoRIIO heartbeats under the GIL
- [#59347](https://github.com/vllm-project/vllm/pull/59347) Mooncake: suppress completion for empty pulls
- [#59862](https://github.com/vllm-project/vllm/pull/59862) release KV-offload CPU lookup pins on reset
- [#58875](https://github.com/vllm-project/vllm/pull/58875) NIXL notifications after KV expiry
- [#54442](https://github.com/vllm-project/vllm/pull/54442) structured output sampling from an unmasked row
- [#55935](https://github.com/vllm-project/vllm/pull/55935) preserve sampling masks in streaming
- [#59779](https://github.com/vllm-project/vllm/pull/59779) watermarking draft prompt lengths under CUDA graphs
- [#59293](https://github.com/vllm-project/vllm/pull/59293) Transformers-backend attention layer naming in spec decode
- [#59500](https://github.com/vllm-project/vllm/pull/59500) batch-invariance NCCL pins vs the weight-transfer group
- [#56891](https://github.com/vllm-project/vllm/pull/56891) FlashInfer all_reduce backend selection
- [#58887](https://github.com/vllm-project/vllm/pull/58887) AITER MLA FP8 prefill metadata race
- [#59029](https://github.com/vllm-project/vllm/pull/59029) encoder-only prompts larger than one step
- [#59015](https://github.com/vllm-project/vllm/pull/59015) empty streaming input
- [#59286](https://github.com/vllm-project/vllm/pull/59286) reject LoRA adapters named after a served model
- [#59419](https://github.com/vllm-project/vllm/pull/59419) strip the Anthropic billing header
- [#57693](https://github.com/vllm-project/vllm/pull/57693) Anthropic tool_addition/removal blocks
- [#47598](https://github.com/vllm-project/vllm/pull/47598) Anthropic named tool calls as tool_use
- [#45290](https://github.com/vllm-project/vllm/pull/45290) forced named tool choice with empty parameters
- [#40986](https://github.com/vllm-project/vllm/pull/40986) streaming errors before the first token
- [#47933](https://github.com/vllm-project/vllm/pull/47933) abort finish_reason for scale-out streams
- [#59654](https://github.com/vllm-project/vllm/pull/59654) GLM string argument whitespace
- [#59491](https://github.com/vllm-project/vllm/pull/59491) off-by-one max_token_id
- [#59373](https://github.com/vllm-project/vllm/pull/59373) DeepSeek-V4 VL dummy image size
- [#59699](https://github.com/vllm-project/vllm/pull/59699) InfiniBand state in TP1 snapshots
- [#59661](https://github.com/vllm-project/vllm/pull/59661) CRIU failure logging
- [#51994](https://github.com/vllm-project/vllm/pull/51994) DiffusionGemma attention mask under CUDA graph replay
- [#59107](https://github.com/vllm-project/vllm/pull/59107) DiffusionGemma narrower canvas on CPU
- [#58083](https://github.com/vllm-project/vllm/pull/58083) Mamba2 quantized in_proj loading on CPU for TP>1
- [#56691](https://github.com/vllm-project/vllm/pull/56691) single-channel audio normalization
- plus 5 more minor fixes ([#58756](https://github.com/vllm-project/vllm/pull/58756), [#49821](https://github.com/vllm-project/vllm/pull/49821), [#59529](https://github.com/vllm-project/vllm/pull/59529), [#59251](https://github.com/vllm-project/vllm/pull/59251), [#58932](https://github.com/vllm-project/vllm/pull/58932))

</details>

<details>
<summary>Refactors (7)</summary>

- [#59762](https://github.com/vllm-project/vllm/pull/59762) remove Transformers < 5.16.1 code paths
- [#58997](https://github.com/vllm-project/vllm/pull/58997) remove deprecated mamba_cache_mode "all"
- [#58916](https://github.com/vllm-project/vllm/pull/58916) remove dead test code
- [#59781](https://github.com/vllm-project/vllm/pull/59781) remove dead env and config
- [#59200](https://github.com/vllm-project/vllm/pull/59200) share workspace and runner init between GPU and XPU workers
- [#59525](https://github.com/vllm-project/vllm/pull/59525) use vllm_runner in the fusions_e2e conftest
- [#59348](https://github.com/vllm-project/vllm/pull/59348) BERT/RoBERTa embedding class attribute

</details>

<details>
<summary>Tests (12)</summary>

- [#55939](https://github.com/vllm-project/vllm/pull/55939) MyPy errors in test groups (part 3)
- [#59428](https://github.com/vllm-project/vllm/pull/59428) disable mypy arg-type/assignment checks in tests
- [#59402](https://github.com/vllm-project/vllm/pull/59402) mypy errors in `models/[kK]*`
- [#55840](https://github.com/vllm-project/vllm/pull/55840) async scheduling accuracy tests for spec decode
- [#59229](https://github.com/vllm-project/vllm/pull/59229) Kimi-K3 prefix cache reuse with KV offload, P/D and DCP
- [#59332](https://github.com/vllm-project/vllm/pull/59332) ROCm MoE padding transparency tests
- [#59333](https://github.com/vllm-project/vllm/pull/59333) AiterExperts padding correctness tests
- [#59399](https://github.com/vllm-project/vllm/pull/59399) scoped processor kwargs precedence
- [#59195](https://github.com/vllm-project/vllm/pull/59195) keep fused device input normalization under encoder compile
- [#53692](https://github.com/vllm-project/vllm/pull/53692) batch-invariance consistency test fixes
- [#58125](https://github.com/vllm-project/vllm/pull/58125) shutdown wait-timeout deflake
- [#59507](https://github.com/vllm-project/vllm/pull/59507) multi-API-server metrics deflake

</details>

<details>
<summary>CI & build (14)</summary>

- [#59621](https://github.com/vllm-project/vllm/pull/59621) Transformers bumped to 5.18.0
- [#59315](https://github.com/vllm-project/vllm/pull/59315) Dependabot security bumps
- [#59427](https://github.com/vllm-project/vllm/pull/59427) pyjwt and rand bumps
- [#59288](https://github.com/vllm-project/vllm/pull/59288) Rubin images on the public CUDA base image
- [#56679](https://github.com/vllm-project/vllm/pull/56679) AMD coverage for distributed, model and eval tests
- [#59256](https://github.com/vllm-project/vllm/pull/59256) remove duplicate MI355 DPX jobs
- [#59595](https://github.com/vllm-project/vllm/pull/59595) drop four CPU-only groups from the legacy AMD pipeline
- [#59657](https://github.com/vllm-project/vllm/pull/59657) pre-commit check for agent files and skills
- [#59913](https://github.com/vllm-project/vllm/pull/59913) auto-label pooling PRs
- [#59192](https://github.com/vllm-project/vllm/pull/59192) mooncake auto-label rule
- [#59521](https://github.com/vllm-project/vllm/pull/59521) weight-sync metrics CI relaxation
- [#59417](https://github.com/vllm-project/vllm/pull/59417) zero-sum DeepSeek-OCR pixel tensors
- [#58946](https://github.com/vllm-project/vllm/pull/58946) bound UniProc startup threads to CPUs
- [#59859](https://github.com/vllm-project/vllm/pull/59859) see Bugfixes

</details>

<details>
<summary>Docs (6)</summary>

- [#57084](https://github.com/vllm-project/vllm/pull/57084) PR checklist skill for coding agents
- [#58003](https://github.com/vllm-project/vllm/pull/58003) API compatibility checking skill
- [#59459](https://github.com/vllm-project/vllm/pull/59459) Reviewers page
- [#59196](https://github.com/vllm-project/vllm/pull/59196) ECMooncakeConnector docs
- [#59361](https://github.com/vllm-project/vllm/pull/59361) score centering via top-k logprobs
- plus about 64 more small PRs not itemized in the input

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 9c6f836a30ed39bfa18c789baa9adc585308a4b8be24e1591aa91952309b2604 -->
