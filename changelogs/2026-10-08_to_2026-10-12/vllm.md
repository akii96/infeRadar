# vllm: PR digest (2026-10-08 to 2026-10-12)

_222 merged, 418 newly opened - source vllm-project/vllm, generated 2026-10-12T00:38:12Z_

## TL;DR
- **DeepSeek-V4.1 led the model-labelled work.** Merged PR [#60397](https://github.com/vllm-project/vllm/pull/60397) adds a ROCm "mono" decode layer on MI355X. Follow-ups are open for MI300X/MI325X ([#60731](https://github.com/vllm-project/vllm/pull/60731)) and for all backbone layers ([#61082](https://github.com/vllm-project/vllm/pull/61082)). Merged NVIDIA-side work adds Engram FP8 exchange ([#59923](https://github.com/vllm-project/vllm/pull/59923)) and trims decoder replay ([#59894](https://github.com/vllm-project/vllm/pull/59894)).
- **The ROCm mono-kernel push is the largest perf theme.** Open PRs port the fused decode layer to Qwen3.8 ([#60833](https://github.com/vllm-project/vllm/pull/60833)), Kimi-K3 ([#60683](https://github.com/vllm-project/vllm/pull/60683), [#60997](https://github.com/vllm-project/vllm/pull/60997)), GLM-5 ([#60831](https://github.com/vllm-project/vllm/pull/60831)) and GLM-5.2 ([#60889](https://github.com/vllm-project/vllm/pull/60889)). All are in progress.
- **GLM-5.3-Flash and Kimi-K3 got sparse-MLA and indexer work.** Merged: a BF16 split-K sparse MLA decode kernel ([#58584](https://github.com/vllm-project/vllm/pull/58584)), TP-sharded indexer prefill ([#54951](https://github.com/vllm-project/vllm/pull/54951)) and a generic packed KV layout ([#57169](https://github.com/vllm-project/vllm/pull/57169)).
- **Gemma 4 attracts open tuning work.** Open PRs include tuned Triton FusedMoE configs ([#60504](https://github.com/vllm-project/vllm/pull/60504), [#60849](https://github.com/vllm-project/vllm/pull/60849)) and fused QKV-norm/RoPE/PLE/MoE-routing kernels ([#60674](https://github.com/vllm-project/vllm/pull/60674)).
- **Direction:** cleanup is also heavy: torch.compile sequence parallelism and AsyncTP removed, vendored HF code replaced by Transformers 5.16.1, Python 3.10 dropped. MRV2 is being hardened, and the frontend and structured-decisions API keep expanding.

## Most important PRs
**[#60397](https://github.com/vllm-project/vllm/pull/60397): ROCm mono decode layer for DeepSeek-V4.1-Flash on MI355X**
Adds a fused single-kernel decode path for the whole layer, covering attention and MoE. It cuts launch overhead and is the template for the Qwen3.8, Kimi-K3 and GLM ports now open.

**[#57169](https://github.com/vllm-project/vllm/pull/57169): GLM-5.3-Flash generic packed KV layout with CircularBufferSpec tail**
Moves GLM-5.3-Flash onto a generic packed KV layout and adds a circular-buffer tail with speculative ring slots. It touches 83 files across the attention, KV-cache and speculative-decode paths.

**[#58584](https://github.com/vllm-project/vllm/pull/58584): BF16 split-K sparse MLA decode kernel on ROCm (GLM-5.3-Flash)**
A Triton split-K kernel for sparse MLA decode that improves parallelism on long contexts.

**[#55686](https://github.com/vllm-project/vllm/pull/55686): Shared-expert fusion with online shared_expert quantization**
Lets shared experts fuse with routed experts even when they are quantized separately. The showcase is Quark MXFP4 routed experts.

**[#60517](https://github.com/vllm-project/vllm/pull/60517): Remove torch.compile sequence parallelism and AsyncTP**
Deletes about 4.8k lines of the compile-pass-based SP and AsyncTP implementation, a major simplification of the compile and distributed stack. The open [#60653](https://github.com/vllm-project/vllm/pull/60653) adds SP and async TP to the Transformers backend.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#59923](https://github.com/vllm-project/vllm/pull/59923) DSv4.1: exchange packed FP8 Engram rows across DP and feed wkv MXFP8
- [#59894](https://github.com/vllm-project/vllm/pull/59894) DSv4.1: trim the last KV-source layer in decoder replay
- [#56638](https://github.com/vllm-project/vllm/pull/56638) DSv4.1 ROCm: shared combine_topk_swa_indices kernel replaces the Torch prefill combine
- [#59732](https://github.com/vllm-project/vllm/pull/59732) ROCm: fuse QK-norm/RoPE/gate and the KV-cache write into the QSA prepare launch
- [#59591](https://github.com/vllm-project/vllm/pull/59591) ROCm Kimi-K3: store only the current rank's shards in latent MoE up-proj
- [#59069](https://github.com/vllm-project/vllm/pull/59069) ROCm Kimi-K3: fuse AttnRes output with per-token FP8 input quantization
- [#60684](https://github.com/vllm-project/vllm/pull/60684) MiniMax-M3: MSA prefill attends with the E4M3 query; fmha_sm100 bump
- [#60345](https://github.com/vllm-project/vllm/pull/60345) TokenSpeed MLA decode: minimum KV splits configuration
- [#56875](https://github.com/vllm-project/vllm/pull/56875) Kimi K3 shared-expert sharding with DeepEP v2
- [#60196](https://github.com/vllm-project/vllm/pull/60196) Sort multimodal encoder inputs by modality
- [#60269](https://github.com/vllm-project/vllm/pull/60269) Reduce free KV cache queue overhead
- [#60497](https://github.com/vllm-project/vllm/pull/60497) Cut fallback decode CPU by 69% at 32K
- [#60159](https://github.com/vllm-project/vllm/pull/60159) ROCm: native merge_attn_states kernel on gfx942/gfx950
- [#60246](https://github.com/vllm-project/vllm/pull/60246) Skip the M-RoPE warmup when every holder of the RoPE fuses it
- plus [#58685](https://github.com/vllm-project/vllm/pull/58685) (JIT monitor hooks TileLang compile)

</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#59085](https://github.com/vllm-project/vllm/pull/59085) Cover a whole spec-verify in one DiffKV split-KV program
- [#60452](https://github.com/vllm-project/vllm/pull/60452) Decode an NVFP4 KV cache with XQA on SM12x
- [#60620](https://github.com/vllm-project/vllm/pull/60620) Allow an NVFP4 KV cache on SM90 with fa2
- [#60156](https://github.com/vllm-project/vllm/pull/60156) Preserve small FP8 softmax weights in Triton attention
- [#56959](https://github.com/vllm-project/vllm/pull/56959) Platform-specific MLA prefill backend selection
- [#60647](https://github.com/vllm-project/vllm/pull/60647) HiSparse owns GPU residency instead of editing block-table rows
- [#60434](https://github.com/vllm-project/vllm/pull/60434) Remove the WAR for LL CuTeDSL BF16 GEMM
- [#60021](https://github.com/vllm-project/vllm/pull/60021) ROCm Qwen4Exp: fused PLE Triton kernels

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#60079](https://github.com/vllm-project/vllm/pull/60079) MXFP4 oracle: CUTLASS W4A4 backend and BF16 activation fallback
- [#59612](https://github.com/vllm-project/vllm/pull/59612) 3D activation-quantization fusion, enabled for Pixtral
- [#55104](https://github.com/vllm-project/vllm/pull/55104) ROCm: align AITER W4A4 MoE intermediate size to 128
- [#58053](https://github.com/vllm-project/vllm/pull/58053) Abstract the DeepGemm MegaMOE backend
- [#60388](https://github.com/vllm-project/vllm/pull/60388) RDNA3 W4A16 MoE: handle the N-first CT weight layout
- [#60447](https://github.com/vllm-project/vllm/pull/60447) Size the MoE permute scratch from its inputs

</details>

<details>
<summary>Model support (7)</summary>

- [#58674](https://github.com/vllm-project/vllm/pull/58674) MiniCPM-V 4.7
- [#60415](https://github.com/vllm-project/vllm/pull/60415) zerank-2 reranker
- [#56983](https://github.com/vllm-project/vllm/pull/56983) DFlash2 draft models with GLM-5.3-Flash
- [#60855](https://github.com/vllm-project/vllm/pull/60855) EAGLE3/DFlash aux hidden states for Granite
- [#59853](https://github.com/vllm-project/vllm/pull/59853) Drop the 4x M-RoPE cache headroom for Qwen3-VL, Qwen3.5 and Qwen3.8
- [#60187](https://github.com/vllm-project/vllm/pull/60187) K-EXAONE: restore pre-2.0 configs and apply RoPE to the MTP layer
- [#60954](https://github.com/vllm-project/vllm/pull/60954) Restore AXK1 config defaults

</details>

<details>
<summary>Parallelism & scheduling (9)</summary>

- [#51207](https://github.com/vllm-project/vllm/pull/51207) Shared-memory tensor arena for CPU-to-GPU worker broadcast
- [#52110](https://github.com/vllm-project/vllm/pull/52110) Pipeline-parallel support in the sharded state loader
- [#59523](https://github.com/vllm-project/vllm/pull/59523) Enable the cuMem CUDA-graph pool offload on ROCm
- [#59360](https://github.com/vllm-project/vllm/pull/59360) Release the FlashInfer allreduce workspace with --enable-nccl-comm-suspend
- [#51018](https://github.com/vllm-project/vllm/pull/51018) Pick the DP world-group port at bind time via the coordination store
- [#60161](https://github.com/vllm-project/vllm/pull/60161) Register the HiSparse host pool under a single TP rank (NIXL)
- [#59485](https://github.com/vllm-project/vllm/pull/59485) HiSparse host-pool residency metrics
- [#61060](https://github.com/vllm-project/vllm/pull/61060) Release weight-transfer communicators without stopping inference
- [#57849](https://github.com/vllm-project/vllm/pull/57849) Consolidate RL entrypoints

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#56765](https://github.com/vllm-project/vllm/pull/56765) XPU: tuned Mamba SSU configs for Arc Pro B60
- [#57565](https://github.com/vllm-project/vllm/pull/57565) XPU: tuned Mamba SSU configs for two more B70 shapes
- [#51956](https://github.com/vllm-project/vllm/pull/51956) XPU: register the KV offload mmap region as pinned host memory
- [#59865](https://github.com/vllm-project/vllm/pull/59865) XPU: fix fused_input_norm for multimodal
- [#57787](https://github.com/vllm-project/vllm/pull/57787) XPU: fix accuracy when topk_ids=-1 under DP+EP

</details>

<details>
<summary>API & serving (21)</summary>

- [#59299](https://github.com/vllm-project/vllm/pull/59299) Structured decisions endpoint (/v1/systemone)
- [#60696](https://github.com/vllm-project/vllm/pull/60696) Structured decisions: noul and score question types
- [#60466](https://github.com/vllm-project/vllm/pull/60466) Structured decisions: DiffusionGemma read strategy
- [#60786](https://github.com/vllm-project/vllm/pull/60786) Cache salt and tracing for structured decisions
- [#60677](https://github.com/vllm-project/vllm/pull/60677) Expose /v1/systemone without an opt-in flag
- [#60589](https://github.com/vllm-project/vllm/pull/60589) Rust frontend: --stream-interval and per-request stream_interval
- [#60723](https://github.com/vllm-project/vllm/pull/60723) Accept each connection on the least loaded API worker
- [#54113](https://github.com/vllm-project/vllm/pull/54113) Remove the frontend ZMQ port TOCTOU with inherited listeners
- [#60922](https://github.com/vllm-project/vllm/pull/60922) Rust gRPC: remove the GenerateStream producer task so disconnects abort requests
- [#60836](https://github.com/vllm-project/vllm/pull/60836) is not listed in the data; omitted
- [#59836](https://github.com/vllm-project/vllm/pull/59836) Rust frontend: carry reasoning controls over gRPC
- [#60546](https://github.com/vllm-project/vllm/pull/60546) Rust frontend: pass reasoning controls through render to generate
- [#60115](https://github.com/vllm-project/vllm/pull/60115) Rust gRPC: preserve explicit zero sampling values
- [#59582](https://github.com/vllm-project/vllm/pull/59582) Token-level weight-version spans on final outputs
- [#60728](https://github.com/vllm-project/vllm/pull/60728) Add return_mm_kwargs to render requests
- [#60841](https://github.com/vllm-project/vllm/pull/60841) Cache salt support for generative scoring
- [#48084](https://github.com/vllm-project/vllm/pull/48084) min_p in the Responses API
- [#61042](https://github.com/vllm-project/vllm/pull/61042) Explain disabled scale-out endpoints with opt-in hints
- [#61009](https://github.com/vllm-project/vllm/pull/61009) Restrict default CORS origins
- [#60522](https://github.com/vllm-project/vllm/pull/60522) Move chat_utils.py to renderers
- [#58765](https://github.com/vllm-project/vllm/pull/58765) `vllm download-kernels` for FlashInfer precompiled kernels

</details>

<details>
<summary>Bugfixes (40)</summary>

- [#60695](https://github.com/vllm-project/vllm/pull/60695) Mooncake: save the EAGLE attention proof with hybrid Mamba partial tails
- [#61012](https://github.com/vllm-project/vllm/pull/61012) Mooncake: use the EAGLE replay boundary for sliding-window tails
- [#60533](https://github.com/vllm-project/vllm/pull/60533) Fix inconsistent hybrid Mamba prefix cache boundaries
- [#60354](https://github.com/vllm-project/vllm/pull/60354) Stream every tool call when one delta completes several
- [#57035](https://github.com/vllm-project/vllm/pull/57035) Treat max_tokens as an output upper bound
- [#60736](https://github.com/vllm-project/vllm/pull/60736) MRV2: int64 index mappings to fix row-offset overflow
- [#61013](https://github.com/vllm-project/vllm/pull/61013) MRV2: fix FlashInfer attention and ReplaySSM warmups
- [#60221](https://github.com/vllm-project/vllm/pull/60221) CPU: fused Gumbel-max wrapping-window bias
- [#59880](https://github.com/vllm-project/vllm/pull/59880) Fix speculative block reservations across KV cache groups
- [#59997](https://github.com/vllm-project/vllm/pull/59997) NIXL: transfer the whole PLE short-conv page in P/D
- [#58860](https://github.com/vllm-project/vllm/pull/58860) NIXL: fix receive post-process for different P/D block sizes
- [#51504](https://github.com/vllm-project/vllm/pull/51504) Fix P2P ZMQ socket exhaustion from unbounded peer sessions
- [#60572](https://github.com/vllm-project/vllm/pull/60572) Drain async KV loads in pause(mode="wait")
- [#47616](https://github.com/vllm-project/vllm/pull/47616) Trim token_ids/logprobs past a stop string under spec decode
- [#57633](https://github.com/vllm-project/vllm/pull/57633) Fix multimodal embedding merge in Llama 4 and Mistral Large 3 EAGLE drafters
- [#59655](https://github.com/vllm-project/vllm/pull/59655) DeepSeek V4/V4.1 NVFP4: keep ignored MTP/DSpark experts on MXFP4
- [#55504](https://github.com/vllm-project/vllm/pull/55504) Bound GDN speculative decode query widths
- [#59627](https://github.com/vllm-project/vllm/pull/59627) Feed the token that implicitly ends reasoning to the grammar
- [#58067](https://github.com/vllm-project/vllm/pull/58067) disable_any_whitespace on xgrammar
- [#60359](https://github.com/vllm-project/vllm/pull/60359) Reject unsupported regex inside groups
- [#60748](https://github.com/vllm-project/vllm/pull/60748) Decode choice specs as JSON in outlines and LMFE
- [#52298](https://github.com/vllm-project/vllm/pull/52298) Validate guidance tokenizer compatibility before EngineCore
- [#60747](https://github.com/vllm-project/vllm/pull/60747) LongCat tags in the structural tag
- [#60709](https://github.com/vllm-project/vllm/pull/60709) InternLM2 tool parser dropped streamed characters
- [#59723](https://github.com/vllm-project/vllm/pull/59723) Responses namespace aliases in named tool calling
- [#59263](https://github.com/vllm-project/vllm/pull/59263) Forward reasoning wiring for batch chat completions
- [#60668](https://github.com/vllm-project/vllm/pull/60668) Keep streamed completion text_offset in step with tokens
- [#60286](https://github.com/vllm-project/vllm/pull/60286) Rust frontend: always include token_ids in completion stream choices
- [#59861](https://github.com/vllm-project/vllm/pull/59861) Rust frontend: raw characters in byte-level decode
- [#59412](https://github.com/vllm-project/vllm/pull/59412) ROCm: page-aligned kernel blocks for pooled indexers (GLM-5.3-Flash)
- [#59528](https://github.com/vllm-project/vllm/pull/59528) Keep the GLM-5.3 kpool tail and Qwen4 QSA ring out of the null block
- [#59420](https://github.com/vllm-project/vllm/pull/59420) ROCm: per-sequence context lengths for AITER paged MQA-logits kernels
- [#60389](https://github.com/vllm-project/vllm/pull/60389) ROCm: keep MLA derived weights in place on reload
- [#59147](https://github.com/vllm-project/vllm/pull/59147) GLM-5.3-Flash: honor --mamba-ssm-cache-dtype for the KDA state
- [#54597](https://github.com/vllm-project/vllm/pull/54597) MiniMax-M3: guard sparse decode sentinel indices
- [#60924](https://github.com/vllm-project/vllm/pull/60924) not listed; omitted
- [#60924](https://github.com/vllm-project/vllm/pull/60924)-free list continues: [#60501](https://github.com/vllm-project/vllm/pull/60501) Qwen3-VL video sampling ZeroDivisionError
- [#60225](https://github.com/vllm-project/vllm/pull/60225) LoRA: reject unsupported PEFT features
- [#59924](https://github.com/vllm-project/vllm/pull/59924) LoRA: validate incompatible MoE adapter formats
- [#60812](https://github.com/vllm-project/vllm/pull/60812) LoRA: GPT-OSS gate/up interleaving with mixed MoE formats
- plus 12 more minor bugfixes (including [#45022](https://github.com/vllm-project/vllm/pull/45022), [#55203](https://github.com/vllm-project/vllm/pull/55203), [#60429](https://github.com/vllm-project/vllm/pull/60429), [#60682](https://github.com/vllm-project/vllm/pull/60682), [#52235](https://github.com/vllm-project/vllm/pull/52235), [#60472](https://github.com/vllm-project/vllm/pull/60472), [#59875](https://github.com/vllm-project/vllm/pull/59875))

</details>

<details>
<summary>Refactors (4)</summary>

- [#60623](https://github.com/vllm-project/vllm/pull/60623) Remove vendored code made redundant by Transformers 5.16.1
- [#60402](https://github.com/vllm-project/vllm/pull/60402) Remove Python 3.10 support
- [#60120](https://github.com/vllm-project/vllm/pull/60120) Remove dead code in multiple places
- [#60828](https://github.com/vllm-project/vllm/pull/60828) Deduplicate trace header handling in BaseServing

</details>

<details>
<summary>Tests (6)</summary>

- [#59334](https://github.com/vllm-project/vllm/pull/59334) ROCm: AiterExperts token-padding inf/nan garbage-row coverage
- [#60633](https://github.com/vllm-project/vllm/pull/60633) ROCm: reuse AITER's prebuilt MoE module in the modular-kernel harness
- [#60725](https://github.com/vllm-project/vllm/pull/60725) Allow one fp8 step in the kpool decode fuzz test
- [#60724](https://github.com/vllm-project/vllm/pull/60724) Allow one bf16 ulp in the fused mHC residual check
- [#58878](https://github.com/vllm-project/vllm/pull/58878) Gate CUTLASS W4A8 tests to SM90
- [#60515](https://github.com/vllm-project/vllm/pull/60515) Well-conditioned prompts for FlashInfer ReplaySSM parity tests

</details>

<details>
<summary>CI & build (10)</summary>

- [#57307](https://github.com/vllm-project/vllm/pull/57307) Recipes sweep workflow
- [#60591](https://github.com/vllm-project/vllm/pull/60591) Remove dead in-tree TPU CI scripts
- [#58871](https://github.com/vllm-project/vllm/pull/58871) Find compatible published wheels for precompiled installs
- [#60016](https://github.com/vllm-project/vllm/pull/60016) Enable Zen CPU image build on AMD CI
- [#48074](https://github.com/vllm-project/vllm/pull/48074) Optimize ppc64le runtime image size
- [#61014](https://github.com/vllm-project/vllm/pull/61014) Switch CI tests still on MRV1 to MRV2
- [#60925](https://github.com/vllm-project/vllm/pull/60925) Accept whitespace around /ci commands
- [#58817](https://github.com/vllm-project/vllm/pull/58817) Split Intel XPU jobs to improve B50 utilization
- [#60253](https://github.com/vllm-project/vllm/pull/60253) Run GH200 test on the shared arm64 CI image
- plus 8 more minor CI and build updates

</details>

<details>
<summary>Docs (3)</summary>

- [#60519](https://github.com/vllm-project/vllm/pull/60519) Update ViT CUDA graph design doc
- [#60913](https://github.com/vllm-project/vllm/pull/60913) Document adaptive verification without a confidence head
- [#60259](https://github.com/vllm-project/vllm/pull/60259) Require GCC 13 for CUDA source builds

</details>

<details>
<summary>Other (4)</summary>

- [#60937](https://github.com/vllm-project/vllm/pull/60937) MRV2: detach weight-reload logic from MRV1
- [#60754](https://github.com/vllm-project/vllm/pull/60754) MRV2: miscellaneous code structure updates
- [#41091](https://github.com/vllm-project/vllm/pull/41091) Allow dynamic BackendEnum registration
- [#60923](https://github.com/vllm-project/vllm/pull/60923) Remove scheduled deprecated items

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 1d6f4b365460dba52cf80e82ee91a8f26837efbcfc9866fdecf6571288ceca15 -->
