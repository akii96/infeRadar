# vllm: PR digest (2026-09-09 to 2026-09-13)

_240 merged, 480 newly opened - source vllm-project/vllm, generated 2026-09-13T23:11:55Z_

## TL;DR
- **DeepSeek-V4 / V4.1-Flash dominated** (71 labeled PRs). Merged: model definitions (`[#56228](https://github.com/vllm-project/vllm/pull/56228)`), support (`[#56214](https://github.com/vllm-project/vllm/pull/56214)`), a CPU backend (`[#55355](https://github.com/vllm-project/vllm/pull/55355)`), ROCm vision (`[#55107](https://github.com/vllm-project/vllm/pull/55107)`), and Engram async prefetch with DP sharding (`[#56512](https://github.com/vllm-project/vllm/pull/56512)`). A warmup/JIT migration series (`[#53566](https://github.com/vllm-project/vllm/pull/53566)`, `[#56323](https://github.com/vllm-project/vllm/pull/56323)`, `[#50178](https://github.com/vllm-project/vllm/pull/50178)`) also landed.
- **Perf work centers on sparse-MLA/DSA and Kimi-K3 KDA.** Merged: DeepSelect TopK for the DSA indexer (`[#56464](https://github.com/vllm-project/vllm/pull/56464)`), fused KDA prefill kernels on ROCm (`[#54038](https://github.com/vllm-project/vllm/pull/54038)`), 4-6x faster grouped FP8 MLA cache insertion (`[#55356](https://github.com/vllm-project/vllm/pull/55356)`), and a 5-8% E2E gain from avoiding KDA mixed-batch gather/scatter (`[#56159](https://github.com/vllm-project/vllm/pull/56159)`). Many ROCm AITER mHC and sparse-prefill PRs also merged.
- **Long-context and KV scaling** moved forward. HiSparse host-resident sparse-MLA decode merged (`[#53781](https://github.com/vllm-project/vllm/pull/53781)`), as did PCP+DCP on sparse-MLA (`[#56157](https://github.com/vllm-project/vllm/pull/56157)`). A draft follow-up (`[#56109](https://github.com/vllm-project/vllm/pull/56109)`) is open.
- **Open pipeline is hardware- and kernel-heavy.** It includes the DSv4.1 attention MegaKernel (`[#56344](https://github.com/vllm-project/vllm/pull/56344)`), DeepGEMM Mega-mHC and Mega-Gate (`[#56255](https://github.com/vllm-project/vllm/pull/56255)`, `[#56266](https://github.com/vllm-project/vllm/pull/56266)`), RDNA4 FlyDSL attention and MoE kernels (`[#55996](https://github.com/vllm-project/vllm/pull/55996)`, `[#56488](https://github.com/vllm-project/vllm/pull/56488)`), Ampere/Ada Triton fallbacks for DSv4 (`[#56120](https://github.com/vllm-project/vllm/pull/56120)`), and an NCCL EP all2all backend (`[#56241](https://github.com/vllm-project/vllm/pull/56241)`).
- **Direction:** push DeepSeek V4.1 and Kimi-K3 to production-grade speed across NVIDIA and AMD. In parallel, the Rust frontend keeps maturing and watermarking and tool-call parser hardening landed.

## Most important PRs
**[#53781](https://github.com/vllm-project/vllm/pull/53781) HiSparse host-resident sparse-MLA decode hot-buffering**
Keeps the sparse-MLA KV cache in host memory and hot-buffers the active pages on the GPU during decode. This lets long-context sparse models exceed GPU KV capacity. It is the base of an ongoing N-part series.

**[#56228](https://github.com/vllm-project/vllm/pull/56228) DeepSeek-V4.1-Flash model definitions (with [#56214](https://github.com/vllm-project/vllm/pull/56214))**
Adds the V4.1-Flash architecture and its end-to-end support: attention, MTP/spec-decode and multimodal paths on NVIDIA and AMD. This is the biggest model-enablement change in the window.

**[#55355](https://github.com/vllm-project/vllm/pull/55355) DeepSeek-V4 CPU backend**
Brings DSv4 to CPU, covering attention, MoE and quantization kernels. It widens the hardware footprint of the model.

**[#56464](https://github.com/vllm-project/vllm/pull/56464) DeepSelect TopK for the DSA sparse indexer**
Replaces the top-k selection in the sparse-attention indexer with a faster kernel. This hits a hot decode path for DSA models.

**[#54038](https://github.com/vllm-project/vllm/pull/54038) ROCm fused KDA prefill kernels for Kimi-K3 (reland)**
Fuses the Kimi Delta Attention prefill path on AMD. It is paired with Hopper overlap fixes (`[#55426](https://github.com/vllm-project/vllm/pull/55426)`) and mixed-batch optimizations (`[#56159](https://github.com/vllm-project/vllm/pull/56159)`).

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#52664](https://github.com/vllm-project/vllm/pull/52664) AITER indexer scoring and top-k for MiniMax-M3 sparse attention (ROCm)
- [#56503](https://github.com/vllm-project/vllm/pull/56503) AITER mHC for the DSV4.1 delayed pre block (ROCm)
- [#54855](https://github.com/vllm-project/vllm/pull/54855) Route large DSV4 sparse prefill to AITER OPUS
- [#56562](https://github.com/vllm-project/vllm/pull/56562) Fuse DSV4.1 input metadata prep with Triton
- [#55899](https://github.com/vllm-project/vllm/pull/55899) BF16x3 router GEMM accuracy fix, default on sm100
- [#55736](https://github.com/vllm-project/vllm/pull/55736) GLM-5.3-Flash decode hot-path cleanups
- [#54889](https://github.com/vllm-project/vllm/pull/54889) Fuse empty-shard LSE mask into DCP A2A pack kernel
- [#56478](https://github.com/vllm-project/vllm/pull/56478) Fix odd-row perf cliff in per-token-group quant
- [#55819](https://github.com/vllm-project/vllm/pull/55819) UVA-backed contents for MRV2 apply_write
- [#56657](https://github.com/vllm-project/vllm/pull/56657) Reduce EPD Python proxy serialization overhead
- [#48247](https://github.com/vllm-project/vllm/pull/48247) AITER custom AG/RS for DP-only on ROCm
- [#56098](https://github.com/vllm-project/vllm/pull/56098) Tune multi-stream shared experts; wvSplitKrc fixes
- [#51692](https://github.com/vllm-project/vllm/pull/51692) bpreshuffled blockscaled FP8 GEMM (ROCm)
- [#55499](https://github.com/vllm-project/vllm/pull/55499) Fix TRTLLM ragged prefill perf regression

</details>

<details>
<summary>Kernels & attention (9)</summary>

- [#56305](https://github.com/vllm-project/vllm/pull/56305) Triton/FlashInfer composite for multimodal prefix attention
- [#50439](https://github.com/vllm-project/vllm/pull/50439) Extend XQA decode on SM90
- [#51925](https://github.com/vllm-project/vllm/pull/51925) FlashInfer add-RMSNorm NVFP4 fusion
- [#56215](https://github.com/vllm-project/vllm/pull/56215) Optional Q-norm in fused DSv4 MLA epilogue; group_size=32 for packed FP8
- [#55887](https://github.com/vllm-project/vllm/pull/55887) Shared-KV prefill in AITER attention
- [#55888](https://github.com/vllm-project/vllm/pull/55888) Avoid FlexAttention recompiles when request counts change
- [#55864](https://github.com/vllm-project/vllm/pull/55864) Fix FlashInfer KV sharing with omitted K/V
- [#56485](https://github.com/vllm-project/vllm/pull/56485) flashKDA bf16 checkpoint state
- [#53280](https://github.com/vllm-project/vllm/pull/53280) Cooperative writes in batched_moe_align_block_size

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#55522](https://github.com/vllm-project/vllm/pull/55522) Migrate RDNA3 W4A16 MoE to the oracle/experts path
- [#55465](https://github.com/vllm-project/vllm/pull/55465) Fast Start fp4 support
- [#53319](https://github.com/vllm-project/vllm/pull/53319) NVFP4 in the torch linear backend
- [#55713](https://github.com/vllm-project/vllm/pull/55713) NVFP4 DSpark gathered top-k projection
- [#52501](https://github.com/vllm-project/vllm/pull/52501) Detect unloaded NVFP4 scales with a NaN sentinel
- [#55548](https://github.com/vllm-project/vllm/pull/55548) Use stored rsLoRA scaling in MoE expert packing

</details>

<details>
<summary>Model support (8)</summary>

- [#56208](https://github.com/vllm-project/vllm/pull/56208) DeepSeek-V4.1-Flash in Rust and Python frontends
- [#55921](https://github.com/vllm-project/vllm/pull/55921) Bailing V3 VL
- [#55107](https://github.com/vllm-project/vllm/pull/55107) DeepSeek V4 Vision on ROCm
- [#55897](https://github.com/vllm-project/vllm/pull/55897) LoRA for DeepSeek-V4 Flash Vision
- [#55690](https://github.com/vllm-project/vllm/pull/55690) QKV-Fuser for Gemma4 (Transformers backend)
- [#55768](https://github.com/vllm-project/vllm/pull/55768) Gemma 4 de-JITification
- [#54371](https://github.com/vllm-project/vllm/pull/54371) Qwen4Exp UVA PLE-offload and Engram TP
- [#56554](https://github.com/vllm-project/vllm/pull/56554) Remove compressor-aware image sentinel padding for DSV4.1

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#56629](https://github.com/vllm-project/vllm/pull/56629) Share HiSparse host cache across TP ranks
- [#56061](https://github.com/vllm-project/vllm/pull/56061) Expose HiSparse cache metrics via KV connector stats
- [#56395](https://github.com/vllm-project/vllm/pull/56395) Simplify HiSparse cache init
- [#56107](https://github.com/vllm-project/vllm/pull/56107) PCP support for single-module MTP and replicated DSpark
- [#46994](https://github.com/vllm-project/vllm/pull/46994) MTP spec decode under pipeline parallelism
- [#56512](https://github.com/vllm-project/vllm/pull/56512) Engram async prefetch and DP sharding
- [#54985](https://github.com/vllm-project/vllm/pull/54985) Elastic EP reuses CUDA graphs across reconfiguration
- [#56645](https://github.com/vllm-project/vllm/pull/56645) Expose PCP producer KV shards as NIXL transfer ranks
- [#56145](https://github.com/vllm-project/vllm/pull/56145) MRV2 fast-prefill
- [#56122](https://github.com/vllm-project/vllm/pull/56122) Dual-key Gumbel-max watermarking for spec decode
- [#54736](https://github.com/vllm-project/vllm/pull/54736) SimpleCPU fine-grained hybrid prefix hits

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#54640](https://github.com/vllm-project/vllm/pull/54640) Public CUDA 13.4 Rubin build path
- [#55352](https://github.com/vllm-project/vllm/pull/55352) Faster LM head on Arm CPUs
- [#54968](https://github.com/vllm-project/vllm/pull/54968) forward_xpu for Mixer2RMSNormGated and FusedRMSNormGated
- [#55942](https://github.com/vllm-project/vllm/pull/55942) forward_xpu for Ernie4_5_VLRotaryEmbedding
- [#56349](https://github.com/vllm-project/vllm/pull/56349) Auto-enable breakable CUDA graphs for DeepseekV41 on ROCm

</details>

<details>
<summary>API & serving (14)</summary>

- [#56392](https://github.com/vllm-project/vllm/pull/56392) Unified Cohere parser
- [#54053](https://github.com/vllm-project/vllm/pull/54053) Watermarked generation and detection (Gumbel-max)
- [#55047](https://github.com/vllm-project/vllm/pull/55047) Rust frontend accepts preprocessed multimodal gRPC features
- [#55417](https://github.com/vllm-project/vllm/pull/55417) Rust frontend whitespace framing in model output
- [#56174](https://github.com/vllm-project/vllm/pull/56174) Strongly typed wire dtypes and modalities in Rust frontend
- [#56378](https://github.com/vllm-project/vllm/pull/56378) `generation` blocks in HF chat template (Rust)
- [#56386](https://github.com/vllm-project/vllm/pull/56386) HF revisions, offline mode and cache dir (Rust)
- [#56405](https://github.com/vllm-project/vllm/pull/56405) Surface engine generation errors over gRPC
- [#55411](https://github.com/vllm-project/vllm/pull/55411) Simplify Rust reasoning parser init
- [#56018](https://github.com/vllm-project/vllm/pull/56018) Resolve unified and split parser selections consistently
- [#56058](https://github.com/vllm-project/vllm/pull/56058) Normalize HTTP method labels in metrics
- [#56369](https://github.com/vllm-project/vllm/pull/56369) Move non-OpenAI content out of the OpenAI folder
- [#56573](https://github.com/vllm-project/vllm/pull/56573) Report actual input token usage for scoring APIs
- plus 6 more minor frontend and Rust updates ([#54821](https://github.com/vllm-project/vllm/pull/54821), [#55328](https://github.com/vllm-project/vllm/pull/55328), [#56103](https://github.com/vllm-project/vllm/pull/56103), [#56090](https://github.com/vllm-project/vllm/pull/56090), [#55240](https://github.com/vllm-project/vllm/pull/55240), [#56365](https://github.com/vllm-project/vllm/pull/56365))

</details>

<details>
<summary>Bugfixes (22)</summary>

- [#56141](https://github.com/vllm-project/vllm/pull/56141) Tolerate misspelled DSML tool_calls wrapper
- [#55954](https://github.com/vllm-project/vllm/pull/55954) Parse DSML tool calls when the wrapper is omitted
- [#56260](https://github.com/vllm-project/vllm/pull/56260) Align DeepSeek tool-call args with deepseek-recipe
- [#55212](https://github.com/vllm-project/vllm/pull/55212) Initialize DCP metadata after batch partitioning (MRV2)
- [#56181](https://github.com/vllm-project/vllm/pull/56181) Fix DP token padding in dflash attention metadata
- [#56446](https://github.com/vllm-project/vllm/pull/56446) Align YaRN with Transformers; stop re-scaling max_model_len
- [#50388](https://github.com/vllm-project/vllm/pull/50388) Fix ValueError on KV load failure with hybrid KV cache
- [#49675](https://github.com/vllm-project/vllm/pull/49675) Stop zero-progress preemption cascades for deferred KV frees
- [#55450](https://github.com/vllm-project/vllm/pull/55450) Retire Mamba states across null gaps
- [#54713](https://github.com/vllm-project/vllm/pull/54713) Retain both replay boundaries for EAGLE resend
- [#55095](https://github.com/vllm-project/vllm/pull/55095) Fall back to full decode graphs for noncompiled models
- [#56452](https://github.com/vllm-project/vllm/pull/56452) Fix DeepGEMM FP8 warmup coverage
- [#55426](https://github.com/vllm-project/vllm/pull/55426) Fix KDA projection overlap on Hopper
- [#56610](https://github.com/vllm-project/vllm/pull/56610) Fix ROCm elastic EP scaling deadlock
- [#55290](https://github.com/vllm-project/vllm/pull/55290) Fail the request, not the engine, on missing remote encoding
- [#56621](https://github.com/vllm-project/vllm/pull/56621) Submit CPU stores on no-forward steps (KV offload)
- [#56138](https://github.com/vllm-project/vllm/pull/56138) Pin EPLB and MLA host-to-device buffers
- [#54192](https://github.com/vllm-project/vllm/pull/54192) Avoid MistralCommonBackend for HF tokenizers
- [#56652](https://github.com/vllm-project/vllm/pull/56652) Keep image kwargs out of Gemma4 video preprocessing
- [#52516](https://github.com/vllm-project/vllm/pull/52516) Fix Mooncake heterogeneous TP with replicated GQA heads
- [#56033](https://github.com/vllm-project/vllm/pull/56033) Fix Mooncake heterogeneous PP transfer completion
- plus 12 more minor bugfixes (ROCm AITER, Rust frontend, multimodal, EC connector, NIXL)

</details>

<details>
<summary>Refactors (6)</summary>

- [#52615](https://github.com/vllm-project/vllm/pull/52615) Rename kv_offload `block` to `chunk`
- [#56078](https://github.com/vllm-project/vllm/pull/56078) Unify XD-RoPE into M-RoPE
- [#55353](https://github.com/vllm-project/vllm/pull/55353) Deprecations scheduled for 0.29
- [#56191](https://github.com/vllm-project/vllm/pull/56191) Simplify noncompiled cudagraph fallback
- [#54033](https://github.com/vllm-project/vllm/pull/54033) Backend extension points for ECCPUWorker
- [#48866](https://github.com/vllm-project/vllm/pull/48866) Consolidate Prometheus histogram bucket defaults

</details>

<details>
<summary>CI & build (10)</summary>

- [#54973](https://github.com/vllm-project/vllm/pull/54973) E2E test for scale-out EC connector
- [#56541](https://github.com/vllm-project/vllm/pull/56541) Sample GPU util and memory alongside test timelines
- [#56329](https://github.com/vllm-project/vllm/pull/56329) Explicit key for every Buildkite step, with enforcing hook
- [#55252](https://github.com/vllm-project/vllm/pull/55252) ROCm CI Stage F gating
- [#55667](https://github.com/vllm-project/vllm/pull/55667) HY-V4 generation coverage on ROCm CI
- [#55163](https://github.com/vllm-project/vllm/pull/55163) Upload CPU nightly image to Docker Hub
- [#56247](https://github.com/vllm-project/vllm/pull/56247) Fix flaky Rust downloads and triton-cpu cache coupling
- [#56654](https://github.com/vllm-project/vllm/pull/56654) Revert explicit Triton JIT warmup migration (MRV2)
- [#56429](https://github.com/vllm-project/vllm/pull/56429) Revert Kimi-K3 DCP pipeline_parallel fix ([#53664](https://github.com/vllm-project/vllm/pull/53664))
- plus 8 more minor CI/XPU/ROCm updates

</details>

<details>
<summary>Docs & other (4)</summary>

- [#56414](https://github.com/vllm-project/vllm/pull/56414) Nebius Serverless AI deployment guide
- [#54522](https://github.com/vllm-project/vllm/pull/54522) CPU EC Connector usage docs
- [#55476](https://github.com/vllm-project/vllm/pull/55476) Clarify security reporter credit and CVE timing
- plus ~15 more small doc, typing and test tweaks

</details>

<details>
<summary>Newly opened, in progress (highlights)</summary>

- [#56109](https://github.com/vllm-project/vllm/pull/56109) HiSparse evictable resident pages (draft, on [#53781](https://github.com/vllm-project/vllm/pull/53781))
- [#56344](https://github.com/vllm-project/vllm/pull/56344) DSv4.1 attention MegaKernel
- [#56633](https://github.com/vllm-project/vllm/pull/56633) Fold mHC post block into delayed pre projection
- [#56120](https://github.com/vllm-project/vllm/pull/56120) DSv4 Triton fallbacks for SM80
- [#56488](https://github.com/vllm-project/vllm/pull/56488) MiniMax-M3 MXFP8 FlyDSL MoE
- [#56177](https://github.com/vllm-project/vllm/pull/56177) Shared GPU expert pool for NVFP4 Marlin offload
- [#56241](https://github.com/vllm-project/vllm/pull/56241) NCCL EP all2all backend
- [#56685](https://github.com/vllm-project/vllm/pull/56685) Humming integration

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: bc64669bbd3eb62c5cefc752fef70739b45fa2f93682f28d80241133f08447cf -->
