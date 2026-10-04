# vllm: PR digest (2026-08-26 to 2026-08-30)

_180 merged, 380 newly opened - source vllm-project/vllm, generated 2026-08-30T23:30:24Z_

## TL;DR
- **DeepSeek V4 and Kimi-K3 got the most perf attention.** Merged: ROCm DSV4 fusions (SWA RMSNorm + FP8 quant, C4 compressor GEMMs) and a Humming MoE SwiGLU clamp kernel. Kimi-K3 got MoE tail, low-latency GEMM, `eh_proj`, and MLA gate/QKV-A merge work. Open: a large Kimi-K3 ROCm MXFP4 fusion series.
- **Merged kernel wins:**
  - The low-M fused latent MoE tail for Kimi-K3.
  - Hopper low-latency GEMM tuning, with a claimed 4–97% gain.
  - FlashInfer BF16 CuTeDSL low-latency GEMM.
  - SM100 head-dim-256 attention.
  - AITER PA gluon decode for MiniMax-M3 MTP on ROCm.
- **New model families landing:** merged Hy4-preview. Open are Qwen3.8-Flash-Next (plus several PLE-offload variants), GLM-5.3-Flash, PLaMo3 parsers, and Ling 3.0 D-Spark.
- **Direction:**
  - Long-context and disaggregated serving: DCP/PCP for MLA, Mooncake hybrid KV connectors, and NIXL DCP.
  - Spec decode (DSpark, adaptive verification, EAGLE/MTP) with Model Runner V2 now the default.
  - A Rust frontend.
- **Churn:** one merge-and-revert pair, and a revert of [#50488](https://github.com/vllm-project/vllm/pull/50488) is already open.

## Most important PRs
**[#54160](https://github.com/vllm-project/vllm/pull/54160) Hy4-preview model support.**
Adds a new model family end to end, touching attention, MoE, quantization and speculative decoding across 47 files. It is the biggest merged change in the window.

**[#54168](https://github.com/vllm-project/vllm/pull/54168) Low-M fused latent MoE tail for Kimi-K3.**
Optimizes the small-batch decode path of Kimi-K3's latent MoE on NVIDIA, where launch overhead and tail kernels dominate latency.

**[#52849](https://github.com/vllm-project/vllm/pull/52849) AITER PA gluon decode for MiniMax-M3 (ROCm).**
Enables the gluon paged-attention decode kernel for MTP and dense layers, speeding decode on AMD.

**[#50611](https://github.com/vllm-project/vllm/pull/50611) NIXL prefill/decode DCP support for MLA models.**
Lets decode-context-parallel MLA models, with FlashInfer support, run under disaggregated prefill/decode. A companion merge ([#54012](https://github.com/vllm-project/vllm/pull/54012)) uses FlashInfer native CP for MLA decode.

**[#53183](https://github.com/vllm-project/vllm/pull/53183) Model Runner V2 on by default for all models.**
Makes the new runner the default. Several MRV2 fixes also merged: spec-decode gumbel noise decoupling, KV release on shutdown, and skipping the DP sync before draft prefill.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#54088](https://github.com/vllm-project/vllm/pull/54088) Hopper low-latency GEMM tuning for Kimi
- [#53942](https://github.com/vllm-project/vllm/pull/53942) Optimize `eh_proj` linear for Kimi K3
- [#53819](https://github.com/vllm-project/vllm/pull/53819) Tune fused_moe FP8 config for Qwen3.5 on L40S (+7%)
- [#53878](https://github.com/vllm-project/vllm/pull/53878) Fuse sparse MLA Q concat with head padding (GLM5.2)
- [#53685](https://github.com/vllm-project/vllm/pull/53685) Native CUDA SwiGLU clamp kernel for Humming MoE (DSv4)
- [#45457](https://github.com/vllm-project/vllm/pull/45457) Reuse topk SparseMatrix routing metadata in GPT-OSS MoE
- [#52033](https://github.com/vllm-project/vllm/pull/52033) ROCm dual-stream decode with hipgraphs
- [#51321](https://github.com/vllm-project/vllm/pull/51321) Optimize Rust frontend SSE streaming hot path
- [#54148](https://github.com/vllm-project/vllm/pull/54148) Reduce copy in Rust frontend auxiliary frame resolution
- [#54299](https://github.com/vllm-project/vllm/pull/54299) Avoid H2D copies from non-pinned CPU tensors
- [#54292](https://github.com/vllm-project/vllm/pull/54292), [#54293](https://github.com/vllm-project/vllm/pull/54293), [#54295](https://github.com/vllm-project/vllm/pull/54295), [#53412](https://github.com/vllm-project/vllm/pull/53412) Pin CPU tensors and split transfers before non-blocking H2D
- [#53606](https://github.com/vllm-project/vllm/pull/53606) Tune FlashInfer all-reduce thresholds for SM103 TP8

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#52980](https://github.com/vllm-project/vllm/pull/52980) SM100 head-dim-256 optimized attention
- [#50572](https://github.com/vllm-project/vllm/pull/50572) FlashInfer BF16 CuTeDSL low-latency GEMM
- [#53785](https://github.com/vllm-project/vllm/pull/53785) Dense and masked MHA for GLM-5
- [#53396](https://github.com/vllm-project/vllm/pull/53396) DS conv-state layout in fused KDA decode kernel
- [#51171](https://github.com/vllm-project/vllm/pull/51171) FULL cudagraphs for AITER MLA spec decode (ROCm)
- [#51040](https://github.com/vllm-project/vllm/pull/51040) FP8 asm MLA prefill for small head counts (ROCm K3)
- [#53540](https://github.com/vllm-project/vllm/pull/53540) Fuse SWA q/kv RMSNorm and FP8 group quant for DSV4 (ROCm)
- [#53838](https://github.com/vllm-project/vllm/pull/53838) Fuse DSV4 C4 compressor GEMMs (ROCm)
- [#54277](https://github.com/vllm-project/vllm/pull/54277) FlashInfer MLA for DSpark drafting
- [#53705](https://github.com/vllm-project/vllm/pull/53705) HPC-ops rope norm with strided KV cache
- [#52185](https://github.com/vllm-project/vllm/pull/52185) Pixtral packed multimodal encoder attention

</details>

<details>
<summary>MoE & quantization (6)</summary>

- [#53097](https://github.com/vllm-project/vllm/pull/53097) Fused shared experts for block-quantized FP8 (ROCm)
- [#51398](https://github.com/vllm-project/vllm/pull/51398) DeepEPv2 MXFP8 activation scale dispatch
- [#53311](https://github.com/vllm-project/vllm/pull/53311) Enable all2all fi_one_sided by default
- [#53141](https://github.com/vllm-project/vllm/pull/53141) Remove AITER FP4 ASM GEMM env var; w4a4 uses preshuffle triton+asm by default
- [#54427](https://github.com/vllm-project/vllm/pull/54427) Route weight-only NVFP4 checkpoints through W4A16
- [#52736](https://github.com/vllm-project/vllm/pull/52736) Quark docs: online quantization

</details>

<details>
<summary>Model support (7)</summary>

- [#47625](https://github.com/vllm-project/vllm/pull/47625) ViT full CUDA graph for Idefics3 and SmolVLM
- [#54239](https://github.com/vllm-project/vllm/pull/54239) Speculative decoding for PLaMo3
- [#53797](https://github.com/vllm-project/vllm/pull/53797) Load dflash2 in speculators format
- [#54380](https://github.com/vllm-project/vllm/pull/54380) Honor cap_pixels_per_frame in Qwen3-VL profiling
- [#54015](https://github.com/vllm-project/vllm/pull/54015) Merge Kimi-K3 MLA gate into QKV-A projection
- [#53557](https://github.com/vllm-project/vllm/pull/53557) Tower/connector LoRA for Qwen3-Omni
- [#53650](https://github.com/vllm-project/vllm/pull/53650) and [#53839](https://github.com/vllm-project/vllm/pull/53839) Add models to the batch-invariance docs

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#53751](https://github.com/vllm-project/vllm/pull/53751) Checkpoint-coordinate sparse NCCL weight updates (RL)
- [#52497](https://github.com/vllm-project/vllm/pull/52497) Rank-local IPC weight updates (RL)
- [#53324](https://github.com/vllm-project/vllm/pull/53324) MooncakeStore with hybrid DCP prefix caching
- [#53333](https://github.com/vllm-project/vllm/pull/53333) Start async KV loads after forward launch
- [#49994](https://github.com/vllm-project/vllm/pull/49994) EC offloading connector uses events instead of StepTracker
- [#53779](https://github.com/vllm-project/vllm/pull/53779) Identify externally transferable KV cache groups
- [#53694](https://github.com/vllm-project/vllm/pull/53694) Skip DP sync before EAGLE/MTP draft prefill
- [#53515](https://github.com/vllm-project/vllm/pull/53515) Persistent input buffers for PCP PIECEWISE graphs
- [#53869](https://github.com/vllm-project/vllm/pull/53869) PCP slot mappings for PIECEWISE capture
- [#53253](https://github.com/vllm-project/vllm/pull/53253) Gate cross-node MNNVL all-reduce by group capability
- [#50932](https://github.com/vllm-project/vllm/pull/50932) Fix buffer size for DSpark with FlashInfer MNNVL allreduce

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#53443](https://github.com/vllm-project/vllm/pull/53443) Opt-in Rubin Docker builds
- [#53712](https://github.com/vllm-project/vllm/pull/53712) Update ROCr and clr in base image
- [#51471](https://github.com/vllm-project/vllm/pull/51471) CPU MLA prefill backend selection
- [#54048](https://github.com/vllm-project/vllm/pull/54048) cuBLAS out_dtype router GEMM on all CUDA archs (GB10)
- [#38434](https://github.com/vllm-project/vllm/pull/38434) Improve ROCm detection in WSL

</details>

<details>
<summary>API & serving (14)</summary>

- [#45803](https://github.com/vllm-project/vllm/pull/45803) `/v1/messages/render` for Anthropic Messages API
- [#53218](https://github.com/vllm-project/vllm/pull/53218) Rust frontend: OpenAI request/response edge cases
- [#48584](https://github.com/vllm-project/vllm/pull/48584) Rust frontend: `truncate_prompt_tokens` and `truncation_side`
- [#53756](https://github.com/vllm-project/vllm/pull/53756) Rust gRPC: enforce LoRA path validation
- [#53760](https://github.com/vllm-project/vllm/pull/53760) Rust gRPC: audio and video inputs
- [#53528](https://github.com/vllm-project/vllm/pull/53528) Rust frontend: take raw buffer in mm tensor lowering
- [#53946](https://github.com/vllm-project/vllm/pull/53946) Improve sweep recommendations and short-alias parsing
- [#52529](https://github.com/vllm-project/vllm/pull/52529) Only echo assistant turn in batched chat completions
- [#51157](https://github.com/vllm-project/vllm/pull/51157) Let pooling requests set padding
- [#54108](https://github.com/vllm-project/vllm/pull/54108) Separate adaptive verification config validation
- [#54353](https://github.com/vllm-project/vllm/pull/54353) Bound cache_salt length
- [#54324](https://github.com/vllm-project/vllm/pull/54324) Validate scale-out transfer params
- [#42644](https://github.com/vllm-project/vllm/pull/42644) Thread kv_transfer_params into /inference/v1/generate
- [#53920](https://github.com/vllm-project/vllm/pull/53920) Warn on warm prefix cache in random serve benchmark

</details>

<details>
<summary>Bugfixes (50)</summary>

- [#51358](https://github.com/vllm-project/vllm/pull/51358) Save exact Mamba boundary states (Mooncake)
- [#53663](https://github.com/vllm-project/vllm/pull/53663) Fix Mamba prefill truncation ordering (Mooncake)
- [#50488](https://github.com/vllm-project/vllm/pull/50488) Capture widest uniform decode batch (spec decode; revert opened as [#54352](https://github.com/vllm-project/vllm/pull/54352))
- [#54418](https://github.com/vllm-project/vllm/pull/54418) Keep default CUDA graph sizes memory-safe for spec decode
- [#54282](https://github.com/vllm-project/vllm/pull/54282) Decouple draft gumbel noise from target
- [#53962](https://github.com/vllm-project/vllm/pull/53962) Don't pad spec decode up to max_model_len
- [#53507](https://github.com/vllm-project/vllm/pull/53507), [#53508](https://github.com/vllm-project/vllm/pull/53508) Sleep-mode buffer and KV allocation isolation
- [#54162](https://github.com/vllm-project/vllm/pull/54162), [#54246](https://github.com/vllm-project/vllm/pull/54246) Release model and KV on MRV2 shutdown
- [#52047](https://github.com/vllm-project/vllm/pull/52047) Annotate draft KV groups on hybrid path (AMD)
- [#53955](https://github.com/vllm-project/vllm/pull/53955) Release CUDA graph profiling memory before KV allocation
- [#54044](https://github.com/vllm-project/vllm/pull/54044) Reset Mamba align metadata on profiling teardown
- [#52707](https://github.com/vllm-project/vllm/pull/52707) Prevent negative external block allocation
- [#54284](https://github.com/vllm-project/vllm/pull/54284) Keep encoder cache entry until last occurrence freed
- [#54021](https://github.com/vllm-project/vllm/pull/54021) Handle padded GPU cache storage in KV offload
- [#52914](https://github.com/vllm-project/vllm/pull/52914) Synchronize device on DP pause
- [#50969](https://github.com/vllm-project/vllm/pull/50969), [#53666](https://github.com/vllm-project/vllm/pull/53666), [#53621](https://github.com/vllm-project/vllm/pull/53621) RayExecutorV2 TCPStore and test fixes
- [#53008](https://github.com/vllm-project/vllm/pull/53008) Fix ncclCommQueryProperties heap overflow on NCCL 2.31+
- [#53293](https://github.com/vllm-project/vllm/pull/53293) Set breakable graph env before Ray actor import
- [#53698](https://github.com/vllm-project/vllm/pull/53698) Fix MoRIIO shared KV region registration
- [#54247](https://github.com/vllm-project/vllm/pull/54247) Pre-allocate wvSplitKrc workspaces (ROCm)
- [#53818](https://github.com/vllm-project/vllm/pull/53818) Capture CUDA graphs on current stream (ROCm)
- [#53641](https://github.com/vllm-project/vllm/pull/53641) gpu_sync_allowed for AITER FA
- [#53856](https://github.com/vllm-project/vllm/pull/53856) and similar ROCm fixes tracked above
- [#54111](https://github.com/vllm-project/vllm/pull/54111) Remove race in fused groupwise RMSNorm quant
- [#53409](https://github.com/vllm-project/vllm/pull/53409) Fix int32 token offset overflow in fused SiLU block quant
- [#53877](https://github.com/vllm-project/vllm/pull/53877) Keep packed GDN decode beta in FP32
- [#52743](https://github.com/vllm-project/vllm/pull/52743) Fix GDN decode preprocessor guard for Ampere
- [#53109](https://github.com/vllm-project/vllm/pull/53109) Allocate packed outputs in fused_q_kv_rmsnorm
- [#54167](https://github.com/vllm-project/vllm/pull/54167) Fix Kimi-K3 low-latency GEMM fallback init
- [#53773](https://github.com/vllm-project/vllm/pull/53773) Fix Kimi K3 illegal memory access
- [#54005](https://github.com/vllm-project/vllm/pull/54005) Fix K3 DSpark config for 96-head drafts
- [#53884](https://github.com/vllm-project/vllm/pull/53884) Make Gemma4 MTP suppress_tokens masking CUDA-graph-safe
- [#54152](https://github.com/vllm-project/vllm/pull/54152) Keep Moondream3 MoE all-reduce out of fused-path try
- [#54056](https://github.com/vllm-project/vllm/pull/54056) Fix Humming MoE activation_output aliasing
- [#53755](https://github.com/vllm-project/vllm/pull/53755) Update FlashMLA for sparse decode workspace fix
- [#54400](https://github.com/vllm-project/vllm/pull/54400) Avoid global config lookup in sparse indexer forward
- [#52222](https://github.com/vllm-project/vllm/pull/52222) Fix GPT-OSS strict tool-call grammar for Harmony
- [#48922](https://github.com/vllm-project/vllm/pull/48922), [#53763](https://github.com/vllm-project/vllm/pull/53763) Tool call JSON and namespace tool guards
- [#54089](https://github.com/vllm-project/vllm/pull/54089), [#52830](https://github.com/vllm-project/vllm/pull/52830) Reasoning end detection and adapter fixes
- [#53965](https://github.com/vllm-project/vllm/pull/53965) Preserve parallel HY-V3 calls in one streaming delta
- [#53704](https://github.com/vllm-project/vllm/pull/53704), [#53939](https://github.com/vllm-project/vllm/pull/53939) Logprobs fixes
- [#47815](https://github.com/vllm-project/vllm/pull/47815) Streamed completion logprob offsets with echo
- [#54196](https://github.com/vllm-project/vllm/pull/54196) Validate stop_token_ids against vocab
- [#53999](https://github.com/vllm-project/vllm/pull/53999), [#54439](https://github.com/vllm-project/vllm/pull/54439), [#54346](https://github.com/vllm-project/vllm/pull/54346), [#53830](https://github.com/vllm-project/vllm/pull/53830), [#53854](https://github.com/vllm-project/vllm/pull/53854) Multimodal fixes
- [#52168](https://github.com/vllm-project/vllm/pull/52168) Restore multimodal on plain "vllm" throughput backend
- [#50858](https://github.com/vllm-project/vllm/pull/50858) Disable TP for Qwen3-Omni audio encoder when heads % TP != 0
- [#50536](https://github.com/vllm-project/vllm/pull/50536) Guard LlamaBidirectionalConfig against missing pooling
- [#36255](https://github.com/vllm-project/vllm/pull/36255) token_ids_cpu swap copies only valid indices
- [#52545](https://github.com/vllm-project/vllm/pull/52545) Fail closed on missing precompiled CUDA variant
- [#54023](https://github.com/vllm-project/vllm/pull/54023) Revert renderer warmup overlap (fork deadlock)
- [#53220](https://github.com/vllm-project/vllm/pull/53220), [#54412](https://github.com/vllm-project/vllm/pull/54412) Doc fixes

</details>

<details>
<summary>Refactors (6)</summary>

- [#52821](https://github.com/vllm-project/vllm/pull/52821) Remove dead quantization code
- [#53843](https://github.com/vllm-project/vllm/pull/53843) LoRA VocabParallelEmbedding cleanup
- [#54231](https://github.com/vllm-project/vllm/pull/54231) Deprecate PyAV video decoder backend
- [#53697](https://github.com/vllm-project/vllm/pull/53697) Remove unused DSV4 top-k buffer helper
- [#53853](https://github.com/vllm-project/vllm/pull/53853) Delegate PCP compatibility checks to PCP manager
- [#53378](https://github.com/vllm-project/vllm/pull/53378) Preserve AOT cache reuse in Elastic EP

</details>

<details>
<summary>Tests (12)</summary>

- [#53531](https://github.com/vllm-project/vllm/pull/53531) Qwen3-VL batch-invariance tests
- [#54099](https://github.com/vllm-project/vllm/pull/54099) Remove wrongly added e2e test
- [#52764](https://github.com/vllm-project/vllm/pull/52764) Overlap renderer warmup and engine init (later reverted by [#54023](https://github.com/vllm-project/vllm/pull/54023))
- [#54079](https://github.com/vllm-project/vllm/pull/54079), [#53466](https://github.com/vllm-project/vllm/pull/53466), [#54130](https://github.com/vllm-project/vllm/pull/54130) Mypy typing fixes
- [#54312](https://github.com/vllm-project/vllm/pull/54312), [#54271](https://github.com/vllm-project/vllm/pull/54271), [#54310](https://github.com/vllm-project/vllm/pull/54310), [#52367](https://github.com/vllm-project/vllm/pull/52367), [#54132](https://github.com/vllm-project/vllm/pull/54132) Test deflakes and fixes
- [#53120](https://github.com/vllm-project/vllm/pull/53120) Offloader fix for submodules missed by make_layers
- [#52227](https://github.com/vllm-project/vllm/pull/52227) Count store offers for CPU offload store_threshold

</details>

<details>
<summary>CI & build (15)</summary>

- [#50920](https://github.com/vllm-project/vllm/pull/50920) ROCm CI Stage E gating
- [#54313](https://github.com/vllm-project/vllm/pull/54313) Upgrade FlashInfer to 0.6.18
- [#54263](https://github.com/vllm-project/vllm/pull/54263) Advisory PR title format check
- [#54420](https://github.com/vllm-project/vllm/pull/54420) Add MIG slice size to H200 job labels
- [#54326](https://github.com/vllm-project/vllm/pull/54326) Mark L4 steps for EKS migration
- [#53591](https://github.com/vllm-project/vllm/pull/53591), [#53594](https://github.com/vllm-project/vllm/pull/53594), [#54249](https://github.com/vllm-project/vllm/pull/54249), [#53949](https://github.com/vllm-project/vllm/pull/53949) ROCm CI fixes
- [#54330](https://github.com/vllm-project/vllm/pull/54330) Add explicit step keys to 18 hardware test steps
- [#49218](https://github.com/vllm-project/vllm/pull/49218), [#49600](https://github.com/vllm-project/vllm/pull/49600), [#53732](https://github.com/vllm-project/vllm/pull/53732), [#54468](https://github.com/vllm-project/vllm/pull/54468), [#53866](https://github.com/vllm-project/vllm/pull/53866) CI fixes
- plus 4 more minor updates (XPU Dockerfile and kernels bumps, tpu-inference v0.28.0, codeowners, agent skill doc)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: c381d70c57a0f4b85c5d5708185333919e9a9e8d231c0b586115b0b22d3d5fb2 -->
