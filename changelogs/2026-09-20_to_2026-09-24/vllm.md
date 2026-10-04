# vllm: PR digest (2026-09-20 to 2026-09-24)

_246 merged, 524 newly opened - source vllm-project/vllm, generated 2026-09-24T14:21:56Z_

## TL;DR
- **DeepSeek-V4/V4.1 led model attention.** Merged work was mostly MXFP8 and communication fusion on the decode path: `[#57428](https://github.com/vllm-project/vllm/pull/57428)` fuses the wo_b GEMM with the sequence-parallel reduce-scatter, `[#57643](https://github.com/vllm-project/vllm/pull/57643)` fuses TP all-reduce with mHC input preparation, and `[#57603](https://github.com/vllm-project/vllm/pull/57603)` overlaps mHC coefficients. ROCm added sparse-decode fusions (`[#58456](https://github.com/vllm-project/vllm/pull/58456)`, `[#57435](https://github.com/vllm-project/vllm/pull/57435)`) and FP8 WO_A (`[#54894](https://github.com/vllm-project/vllm/pull/54894)`).
- **Kernels and quantization.** Humming was integrated (`[#56685](https://github.com/vllm-project/vllm/pull/56685)`) and now shares persistent workspaces with Marlin (`[#57421](https://github.com/vllm-project/vllm/pull/57421)`). `[#58051](https://github.com/vllm-project/vllm/pull/58051)` skips non-local expert slots in TritonExperts. `[#53175](https://github.com/vllm-project/vllm/pull/53175)` brings Gemma4 FP8 KV with FA4 head-dim 512. `[#58001](https://github.com/vllm-project/vllm/pull/58001)` removes the AllSpark INT8 backend.
- **ROCm is the biggest hardware story.** MRoPE QK-norm/RoPE/KV fusion (`[#50212](https://github.com/vllm-project/vllm/pull/50212)`), MiniMax-M3 and Hy4 fusions, BF16 AsyncTP, and many MI355 CI mirrors landed. Newly opened RDNA3/RDNA4 work includes an all-reduce backend, a W8A8 FP8 kernel and a KV-split decode kernel.
- **Direction.** Merged work is MLA/sparse-attention and MXFP8 optimization for DeepSeek and GLM-class models, plus Kimi-K3 and DSpark spec-decode, EPD and KV-connector plumbing, and the Rust frontend. A FlashInfer 0.7.0 bump (`[#58069](https://github.com/vllm-project/vllm/pull/58069)`) merged, but a revert (`[#58530](https://github.com/vllm-project/vllm/pull/58530)`) is already open over a deterministic structured-output regression.

## Most important PRs
**[#57428](https://github.com/vllm-project/vllm/pull/57428) - Fuse MXFP8 wo_b GEMM with sequence-parallel reduce-scatter (DSV4.1).** Merges the output-projection GEMM with the reduce-scatter, cutting a communication and memory-traffic round-trip on the DeepSeek-V4.1 attention output path on NVIDIA.

**[#56685](https://github.com/vllm-project/vllm/pull/56685) - Humming feature integration.** Brings the Humming low-bit GEMM/MoE quantization backend into core. Follow-ups add asymmetric zero-point support with compressed-tensors (`[#46528](https://github.com/vllm-project/vllm/pull/46528)`) and a shared workspace with Marlin (`[#57421](https://github.com/vllm-project/vllm/pull/57421)`).

**[#58456](https://github.com/vllm-project/vllm/pull/58456) - ROCm DSv4.1: emit MXFP8 from the sparse decode reduce, run wo_a as grouped FP8 GEMM.** Removes a separate quantization pass and uses a grouped FP8 GEMM on the AMD decode path. It continues the sparse-decode fusion series (`[#57435](https://github.com/vllm-project/vllm/pull/57435)`, `[#57451](https://github.com/vllm-project/vllm/pull/57451)`).

**[#50212](https://github.com/vllm-project/vllm/pull/50212) - ROCm QK-norm/RoPE/KV-cache fusion extended to MRoPE.** Brings the fused kernel to multimodal-RoPE models such as Qwen-VL class, cutting kernel launches in attention prep.

**[#45635](https://github.com/vllm-project/vllm/pull/45635) - Block-keyed storage for routed-expert outputs (AuxOutput).** New storage layer for returning routed-expert outputs, plus R3-style plumbing. A Mooncake backend is open in `[#57968](https://github.com/vllm-project/vllm/pull/57968)`.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#56045](https://github.com/vllm-project/vllm/pull/56045) refactor Arm CPU paged attention for speed
- [#57526](https://github.com/vllm-project/vllm/pull/57526) ROCm path and backbone compile for Hy4
- [#57458](https://github.com/vllm-project/vllm/pull/57458) reduce GLM sparse MLA preparation overhead
- [#55385](https://github.com/vllm-project/vllm/pull/55385) wire FA and FlashMLA for sm90 GLM5Next NoPE SparseMLA
- [#57534](https://github.com/vllm-project/vllm/pull/57534) fuse kpool tail slot mapping into one Triton kernel
- [#58225](https://github.com/vllm-project/vllm/pull/58225) narrow Triton prefill KV tile on RDNA3/4
- [#57586](https://github.com/vllm-project/vllm/pull/57586) breakable CUDA graphs by default under batch-invariant mode
- [#47842](https://github.com/vllm-project/vllm/pull/47842) avoid extra reshape kernel in Qwen GDN output norm
- [#57396](https://github.com/vllm-project/vllm/pull/57396) remove CPU-GPU sync in heterogeneous-vocab spec decode
- [#57528](https://github.com/vllm-project/vllm/pull/57528) offload streaming derender detokenization
- [#53283](https://github.com/vllm-project/vllm/pull/53283) use wvSplitK for single-output GEMMs on ROCm
- [#58512](https://github.com/vllm-project/vllm/pull/58512) Conv3dLayer for MiniMax M3 patch embedding
- [#57434](https://github.com/vllm-project/vllm/pull/57434) reuse decode topk ragged metadata across layers (ROCm DSv4.1)
- [#57416](https://github.com/vllm-project/vllm/pull/57416) give prefill-only batch the model state's logit row count

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#54535](https://github.com/vllm-project/vllm/pull/54535) packed LBHNC AITER QK-norm fusion for MiniMax-M3
- #99999 omitted
- [#58099](https://github.com/vllm-project/vllm/pull/58099) fuse AITER static FP8 attention output
- [#54508](https://github.com/vllm-project/vllm/pull/54508) Zen CPU encoder attention on zentorch SDPA
- [#56252](https://github.com/vllm-project/vllm/pull/56252) fp32 attention sinks on CPU
- [#55277](https://github.com/vllm-project/vllm/pull/55277) NoPE sparse MLA on FlashInfer SM120
- [#57546](https://github.com/vllm-project/vllm/pull/57546) route kpool indexer top-k through SparseIndexerTopk dispatcher
- [#55721](https://github.com/vllm-project/vllm/pull/55721) SYCL apply_rotary_emb on XPU
- [#52052](https://github.com/vllm-project/vllm/pull/52052) use silu_and_mul_with_clamp torch op on ROCm
- [#55001](https://github.com/vllm-project/vllm/pull/55001) refactor ROCm tuned gemms
- [#58069](https://github.com/vllm-project/vllm/pull/58069) upgrade FlashInfer to 0.7.0

</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#58234](https://github.com/vllm-project/vllm/pull/58234) use GateLinear for all MoE models
- [#57176](https://github.com/vllm-project/vllm/pull/57176) select per-token NVFP4 MoE backends explicitly
- [#50814](https://github.com/vllm-project/vllm/pull/50814) opt-in load-time MXFP4 dequantization
- [#57784](https://github.com/vllm-project/vllm/pull/57784) bf16 MoE router and MXFP4 MoE for MiMo V2
- [#51800](https://github.com/vllm-project/vllm/pull/51800) remove Quark silent online quantization
- [#57732](https://github.com/vllm-project/vllm/pull/57732) make FP8 and MLA weight transforms reusable pure functions
- [#58030](https://github.com/vllm-project/vllm/pull/58030) GELU for AiterExperts in modular-kernel coverage
- [#58469](https://github.com/vllm-project/vllm/pull/58469) share BF16 baselines across quant comparison tests
- [#57867](https://github.com/vllm-project/vllm/pull/57867) reject hash routing for unsupported monolithic backends

</details>

<details>
<summary>Model support (10)</summary>

- [#57250](https://github.com/vllm-project/vllm/pull/57250) structured generation mode for DiffusionGemma
- [#44229](https://github.com/vllm-project/vllm/pull/44229) DeepSeek-V4 FIM completion rendering
- [#56625](https://github.com/vllm-project/vllm/pull/56625) encoder CUDA graph for deepseek-v4.1-flash
- [#51915](https://github.com/vllm-project/vllm/pull/51915) GLM-5.2-MXFP4 on deepseek_v32 path with sparse attention fixes
- [#52362](https://github.com/vllm-project/vllm/pull/52362) ROCm DSv4 DSpark adaptive verification
- [#52988](https://github.com/vllm-project/vllm/pull/52988) variable-length decode for Kimi-K3 adaptive verification
- [#50592](https://github.com/vllm-project/vllm/pull/50592) Kimi-K3 AMD: return KDA/MLA projections directly
- [#57933](https://github.com/vllm-project/vllm/pull/57933) MiMo V2.6 parser support in Rust frontend
- [#47736](https://github.com/vllm-project/vllm/pull/47736) honor video fps for temporal M-RoPE in Qwen2.5-VL
- [#57491](https://github.com/vllm-project/vllm/pull/57491) keep Engram tables in host memory on ROCm

</details>

<details>
<summary>Parallelism & scheduling (14)</summary>

- [#56956](https://github.com/vllm-project/vllm/pull/56956) DSpark pipeline-parallel targets (revert open in `[#58484](https://github.com/vllm-project/vllm/pull/58484)`)
- [#57075](https://github.com/vllm-project/vllm/pull/57075) prefill context parallelism with data parallelism
- [#58098](https://github.com/vllm-project/vllm/pull/58098) BF16 AsyncTP fusion on ROCm
- [#51052](https://github.com/vllm-project/vllm/pull/51052) MoRIIO transfer of hybrid mamba/KDA state in READ mode
- [#57783](https://github.com/vllm-project/vllm/pull/57783) generalize Mamba prefill checkpoint builder
- [#57312](https://github.com/vllm-project/vllm/pull/57312) cache MTP draft model in separate daemon group
- [#57386](https://github.com/vllm-project/vllm/pull/57386) DP support in weight cache daemon
- [#58065](https://github.com/vllm-project/vllm/pull/58065) async scheduling for DFlash
- [#57951](https://github.com/vllm-project/vllm/pull/57951) soften long-prefill threshold
- [#58459](https://github.com/vllm-project/vllm/pull/58459) tune long-prefill threshold adaptiveness
- [#53423](https://github.com/vllm-project/vllm/pull/53423) KV hints request envelope
- [#54176](https://github.com/vllm-project/vllm/pull/54176) dynamic EPD proxy
- [#57887](https://github.com/vllm-project/vllm/pull/57887) metadata-only audio inputs for EPD
- [#58086](https://github.com/vllm-project/vllm/pull/58086) skip LM shards for --mm-encoder-only

</details>

<details>
<summary>Hardware & arch (8)</summary>

- [#55881](https://github.com/vllm-project/vllm/pull/55881) batch-invariant mode for Dense/MoE on XPU
- [#53300](https://github.com/vllm-project/vllm/pull/53300) CPU GDN with NIXL DS conv-state layout
- [#51600](https://github.com/vllm-project/vllm/pull/51600) XPU graph on by default
- [#56013](https://github.com/vllm-project/vllm/pull/56013) XPU to PyTorch 2.14
- [#57277](https://github.com/vllm-project/vllm/pull/57277) xpu sample kernel in MRV2 sampler
- [#58133](https://github.com/vllm-project/vllm/pull/58133) gate AVX10.2 paths on compiler support
- [#56547](https://github.com/vllm-project/vllm/pull/56547) device-memory-utilization CLI alias for CPU
- [#57460](https://github.com/vllm-project/vllm/pull/57460) unified platform-aware torch profiling

</details>

<details>
<summary>API & serving (14)</summary>

- [#51360](https://github.com/vllm-project/vllm/pull/51360) reusable TP1 engine snapshots
- [#55269](https://github.com/vllm-project/vllm/pull/55269) parser-owned output grammar interfaces (Rust frontend)
- [#57340](https://github.com/vllm-project/vllm/pull/57340) full-output grammars from reasoning parsers
- [#58311](https://github.com/vllm-project/vllm/pull/58311) custom chat roles for HF templates
- [#58306](https://github.com/vllm-project/vllm/pull/58306) --sse-keep-alive-interval
- [#58330](https://github.com/vllm-project/vllm/pull/58330) mark new frontend-owned serve args unsupported/no-op
- [#51922](https://github.com/vllm-project/vllm/pull/51922) mm-processor benchmark
- [#58084](https://github.com/vllm-project/vllm/pull/58084) separate MM instrumentation from request timing
- [#58109](https://github.com/vllm-project/vllm/pull/58109) model-owned vision processors via specs
- [#57634](https://github.com/vllm-project/vllm/pull/57634) vision preprocessing context for Nemotron-H
- [#43310](https://github.com/vllm-project/vllm/pull/43310) per-request spec-decode metrics in generate API
- [#57922](https://github.com/vllm-project/vllm/pull/57922) streaming parity tests/docs for derender
- [#58163](https://github.com/vllm-project/vllm/pull/58163) request JSON body debug logging
- [#57913](https://github.com/vllm-project/vllm/pull/57913) move supports_multimodal_inputs and cache out of registry

</details>

<details>
<summary>Bugfixes (40)</summary>

- [#49648](https://github.com/vllm-project/vllm/pull/49648) migrate Granite tool parser to streaming Parser Engine
- [#57076](https://github.com/vllm-project/vllm/pull/57076) bound prompt after multimodal expansion
- [#57696](https://github.com/vllm-project/vllm/pull/57696) reject encoder-cache hits with mismatched counts
- [#56810](https://github.com/vllm-project/vllm/pull/56810) skip non-prefix-cacheable groups in SimpleCPUOffload
- [#57389](https://github.com/vllm-project/vllm/pull/57389) NIXL DCP pulls across MLA cache regions
- [#58188](https://github.com/vllm-project/vllm/pull/58188) NIXL push completion reporting
- [#53743](https://github.com/vllm-project/vllm/pull/53743) external LB DP rank handling
- [#55390](https://github.com/vllm-project/vllm/pull/55390) annotate MTP draft KV groups positionally
- [#49845](https://github.com/vllm-project/vllm/pull/49845) pick KV block size supported by all backends
- [#58275](https://github.com/vllm-project/vllm/pull/58275) capture prefill kernels for mixed FULL graphs
- [#58061](https://github.com/vllm-project/vllm/pull/58061) GLM-5.3-Flash dense MLP on SP shard
- [#49435](https://github.com/vllm-project/vllm/pull/49435) SM100 fp8_ds_mla cache scales
- [#58092](https://github.com/vllm-project/vllm/pull/58092) register MRV2 sampler JIT warmups (ROCm)
- [#54631](https://github.com/vllm-project/vllm/pull/54631) separate DSpark width from MTP validation
- [#51565](https://github.com/vllm-project/vllm/pull/51565) GDN stateless first-chunk classification
- [#57914](https://github.com/vllm-project/vllm/pull/57914) Engram fallback without /dev/shm
- [#56448](https://github.com/vllm-project/vllm/pull/56448) cap DFlash/DSpark profiling batch
- [#53758](https://github.com/vllm-project/vllm/pull/53758) Mistral3 placeholder grid
- [#48416](https://github.com/vllm-project/vllm/pull/48416) xgrammar feature gate with list-typed JSON Schema
- [#58378](https://github.com/vllm-project/vllm/pull/58378) MM timing no longer enables debug tracing
- [#58189](https://github.com/vllm-project/vllm/pull/58189) backport Inductor custom-op pattern fix
- [#57006](https://github.com/vllm-project/vllm/pull/57006) validate mixed prompt-embedding mask lengths
- [#56250](https://github.com/vllm-project/vllm/pull/56250) disallow MRV1+PP>1+async+structured output
- [#58150](https://github.com/vllm-project/vllm/pull/58150) narrow AuxOutput KV restrictions
- [#57833](https://github.com/vllm-project/vllm/pull/57833) prefer fresh MM payloads over stale cache
- [#56734](https://github.com/vllm-project/vllm/pull/56734) stop dummy draft steps writing KV via stale rows
- [#57866](https://github.com/vllm-project/vllm/pull/57866) reject unsupported EP for AITER MXFP4 MoE
- [#57984](https://github.com/vllm-project/vllm/pull/57984) skip fused silu-mul quant when swiglu clamp set
- [#57874](https://github.com/vllm-project/vllm/pull/57874) restrict mHC overlap to full CUDA graphs
- [#58212](https://github.com/vllm-project/vllm/pull/58212) skip VllmConfig re-validation for submodel views
- [#56579](https://github.com/vllm-project/vllm/pull/56579) avoid NaN in Triton softcap
- [#57453](https://github.com/vllm-project/vllm/pull/57453) retain offload event metadata
- [#57919](https://github.com/vllm-project/vllm/pull/57919) reject FSE=1 with DPA+ETP for DSV4
- [#55442](https://github.com/vllm-project/vllm/pull/55442) defer disposable GLM MTP head
- [#58215](https://github.com/vllm-project/vllm/pull/58215) bound DeepSelect sentinel columns
- [#57769](https://github.com/vllm-project/vllm/pull/57769) Whisper crash on >30s audio
- [#56168](https://github.com/vllm-project/vllm/pull/56168) CPU MoE OOB write with fp32 router weights
- [#58342](https://github.com/vllm-project/vllm/pull/58342) flaky sharded-sampling tests
- [#58419](https://github.com/vllm-project/vllm/pull/58419) TileLang mHC RMSNorm on 64-wide wavefronts
- plus 10 more minor fixes

</details>

<details>
<summary>Tests (10)</summary>

- [#57545](https://github.com/vllm-project/vllm/pull/57545) organize structured output utility tests
- [#55612](https://github.com/vllm-project/vllm/pull/55612) chunked prefill in batch-invariance suite
- [#57467](https://github.com/vllm-project/vllm/pull/57467) compute expected hybrid prefix-cache hit
- [#58093](https://github.com/vllm-project/vllm/pull/58093) MoRI graph replay and output lifetime
- [#58091](https://github.com/vllm-project/vllm/pull/58091) GDN prefill numerics
- [#57450](https://github.com/vllm-project/vllm/pull/57450) HIP device memory for teardown waits
- [#57869](https://github.com/vllm-project/vllm/pull/57869) reduce host memory for FP32 HF references
- [#58272](https://github.com/vllm-project/vllm/pull/58272) V2 scheduler for diffusion tests
- [#57174](https://github.com/vllm-project/vllm/pull/57174) Mooncake review nits
- plus 8 more minor test updates

</details>

<details>
<summary>CI & build (21)</summary>

- [#54867](https://github.com/vllm-project/vllm/pull/54867) pre-commit check tethering tests to Buildkite
- [#57876](https://github.com/vllm-project/vllm/pull/57876) ten AMD parity groups
- [#57877](https://github.com/vllm-project/vllm/pull/57877) mirror portable suites on ROCm
- [#58095](https://github.com/vllm-project/vllm/pull/58095) Mooncake and NIXL accuracy on ROCm
- [#58281](https://github.com/vllm-project/vllm/pull/58281) MI355 NVFP4 and MoRI mirrors
- [#58282](https://github.com/vllm-project/vllm/pull/58282) TurboQuant mirrors on MI355
- [#58432](https://github.com/vllm-project/vllm/pull/58432) MI355 TurboQuant t3nc mirror
- [#58369](https://github.com/vllm-project/vllm/pull/58369) Fusion E2E TP2 Quick group on MI355
- [#58012](https://github.com/vllm-project/vllm/pull/58012) MI355 Kimi-K3 group
- [#50922](https://github.com/vllm-project/vllm/pull/50922) ROCm Stage G gating
- [#58097](https://github.com/vllm-project/vllm/pull/58097) kernel symbol map from csrc build
- [#57965](https://github.com/vllm-project/vllm/pull/57965) split H200 LM Eval into per-model jobs
- [#57113](https://github.com/vllm-project/vllm/pull/57113) split TurboQuant KV LM Eval
- [#55608](https://github.com/vllm-project/vllm/pull/55608) zstd for CI images
- [#58140](https://github.com/vllm-project/vllm/pull/58140) pre-built Triton on CPU
- [#58006](https://github.com/vllm-project/vllm/pull/58006) Triton 3.8.x in The Rock image
- [#58050](https://github.com/vllm-project/vllm/pull/58050) remove MRV2 test from Intel GPU CI
- [#57945](https://github.com/vllm-project/vllm/pull/57945) CUDA 12 KV connector dependency selection
- [#57554](https://github.com/vllm-project/vllm/pull/57554) DeepGEMM CUDA 12.9 builds
- [#58474](https://github.com/vllm-project/vllm/pull/58474) Triton cache overrides and AMD timeout headroom
- plus 1 more minor CI update

</details>

<details>
<summary>Refactors (6)</summary>

- [#58002](https://github.com/vllm-project/vllm/pull/58002) remove dead code in multiple places
- [#57621](https://github.com/vllm-project/vllm/pull/57621) remove dead kernel code
- [#58001](https://github.com/vllm-project/vllm/pull/58001) remove AllSpark INT8 W8A16 GEMM
- [#57980](https://github.com/vllm-project/vllm/pull/57980) MRV2 cleanup
- [#57382](https://github.com/vllm-project/vllm/pull/57382) rename mamba fine-grained prefix cache flag
- [#57967](https://github.com/vllm-project/vllm/pull/57967) move get_dummy_processor_inputs into MM processor

</details>

<details>
<summary>Docs & other (7)</summary>

- [#57910](https://github.com/vllm-project/vllm/pull/57910) Engram feature page
- [#57742](https://github.com/vllm-project/vllm/pull/57742) ECMooncakeConnector EPD example
- [#57314](https://github.com/vllm-project/vllm/pull/57314) refresh Kthena guide
- [#57306](https://github.com/vllm-project/vllm/pull/57306) one-step recipe serving
- [#57958](https://github.com/vllm-project/vllm/pull/57958) fix legacy hf CLI references
- [#57891](https://github.com/vllm-project/vllm/pull/57891) retain frozen weights across level-2 sleep
- [#57937](https://github.com/vllm-project/vllm/pull/57937) drop redundant VLLM_PLE_CPU_OFFLOAD env var

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f81e9dde9505486a028a0abaa406b6cf0e236f4ddcec80a7fb0c516b063ac457 -->
